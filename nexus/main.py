from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
DB_PATH = os.getenv("DB_PATH", "nexus_memory.db")
if not Path(DB_PATH).is_absolute():
    DB_PATH = str(BASE_DIR / DB_PATH)

app = FastAPI(title="NEXUS | PROYECTO ZERO", version="0.1.0")
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            tag TEXT NOT NULL DEFAULT 'general',
            created_at TEXT NOT NULL
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            rationale TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            reviewed_at TEXT
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            detail TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")


init_db()


def log_event(kind: str, detail: str) -> None:
    with db() as con:
        con.execute("INSERT INTO events(kind, detail, created_at) VALUES(?,?,?)",
                    (kind, detail[:2000], now_iso()))


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)


class MemoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=4000)
    tag: str = Field(default="general", max_length=80)


class ProposalCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    rationale: str = Field(min_length=1, max_length=2000)


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/status")
def status():
    provider = os.getenv("AI_PROVIDER", "demo").lower()
    configured = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "name": os.getenv("APP_NAME", "NEXUS"),
        "project": "PROYECTO ZERO",
        "version": app.version,
        "mode": "demo" if provider == "demo" or not configured else "provider_pending",
        "provider": provider,
        "api_key_configured": configured,
        "memory": "sqlite",
        "remote_access": "disabled_by_design"
    }


@app.post("/api/chat")
def chat(body: ChatRequest):
    text = body.message.strip()
    with db() as con:
        memories = con.execute(
            "SELECT content, tag FROM memories ORDER BY id DESC LIMIT 8"
        ).fetchall()
    # Deliberately transparent demo response. A real model adapter is a later step.
    memory_hint = "Hay recuerdos guardados disponibles." if memories else "Todavía no hay recuerdos guardados."
    answer = (
        "NEXUS está iniciado en modo DEMO: todavía no estoy conectado a un modelo de IA. "
        "No voy a fingir que razoné con un modelo externo. "
        f"Recibí tu mensaje ({len(text)} caracteres). {memory_hint} "
        "Siguiente paso de desarrollo: conectar un proveedor de IA de forma segura y probarlo."
    )
    log_event("chat_demo", f"user_chars={len(text)}")
    return {"reply": answer, "mode": "demo", "model_connected": False}


@app.get("/api/memories")
def list_memories():
    with db() as con:
        rows = con.execute("SELECT * FROM memories ORDER BY id DESC").fetchall()
    return {"items": [dict(r) for r in rows]}


@app.post("/api/memories")
def create_memory(body: MemoryCreate):
    content = body.content.strip()
    if not content:
        raise HTTPException(400, "El recuerdo no puede estar vacío.")
    with db() as con:
        cur = con.execute(
            "INSERT INTO memories(content, tag, created_at) VALUES(?,?,?)",
            (content, body.tag.strip() or "general", now_iso())
        )
        memory_id = cur.lastrowid
    log_event("memory_created", f"id={memory_id}; tag={body.tag}")
    return {"id": memory_id, "content": content, "tag": body.tag, "created": True}


@app.delete("/api/memories/{memory_id}")
def delete_memory(memory_id: int):
    with db() as con:
        cur = con.execute("DELETE FROM memories WHERE id=?", (memory_id,))
    if cur.rowcount == 0:
        raise HTTPException(404, "Recuerdo no encontrado.")
    log_event("memory_deleted", f"id={memory_id}")
    return {"deleted": True, "id": memory_id}


@app.get("/api/proposals")
def list_proposals():
    with db() as con:
        rows = con.execute("SELECT * FROM proposals ORDER BY id DESC").fetchall()
    return {"items": [dict(r) for r in rows]}


@app.post("/api/proposals")
def create_proposal(body: ProposalCreate):
    with db() as con:
        cur = con.execute(
            "INSERT INTO proposals(title, rationale, status, created_at) VALUES(?,?,?,?)",
            (body.title.strip(), body.rationale.strip(), "pending", now_iso())
        )
        proposal_id = cur.lastrowid
    log_event("proposal_created", f"id={proposal_id}; title={body.title}")
    return {"id": proposal_id, "status": "pending"}


@app.post("/api/proposals/{proposal_id}/review")
def review_proposal(proposal_id: int, decision: Literal["approve", "reject"]):
    status_value = "approved" if decision == "approve" else "rejected"
    with db() as con:
        cur = con.execute(
            "UPDATE proposals SET status=?, reviewed_at=? WHERE id=? AND status='pending'",
            (status_value, now_iso(), proposal_id)
        )
    if cur.rowcount == 0:
        raise HTTPException(404, "Propuesta pendiente no encontrada.")
    log_event("proposal_reviewed", f"id={proposal_id}; decision={status_value}")
    return {"id": proposal_id, "status": status_value}


@app.get("/api/events")
def list_events():
    with db() as con:
        rows = con.execute("SELECT * FROM events ORDER BY id DESC LIMIT 100").fetchall()
    return {"items": [dict(r) for r in rows]}
