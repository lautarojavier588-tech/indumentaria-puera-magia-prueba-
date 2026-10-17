# PROYECTO ZERO — NEXUS

NEXUS is the personal AI assistant prototype for PROYECTO ZERO.

## Current stage
This is Stage 1: a local, safe foundation with a dashboard, persistent SQLite memory, and reviewable improvement proposals. The chat currently runs in DEMO mode; it is not connected to an AI provider yet.

## Requirements
- Windows 10/11
- Python 3.11 or newer

## Run locally
Open PowerShell in this folder (`nexus`) and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
py -m uvicorn main:app --reload
```

Then open http://127.0.0.1:8000

If PowerShell blocks activation, use Command Prompt instead:
```bat
py -m venv .venv
.venv\Scripts\activate.bat
py -m pip install -r requirements.txt
copy .env.example .env
py -m uvicorn main:app --reload
```

## Safety
- Keep this service on your own computer for now. Do not expose it publicly.
- Never commit API keys, passwords, tokens, or your real `.env` file.
- NEXUS must ask for approval before purchases, money transfers, external messages, production changes, or important deletion.
- The assistant must not silently change its own rules. Improvement proposals require human review.

## Roadmap
1. Local dashboard + durable memory + proposal review.
2. Connect a cloud AI provider through environment variables.
3. Add provider adapters and optional local models.
4. Add authentication and cloud database before remote access.
5. Add business tools, file operations, voice, and vision with explicit permissions.
