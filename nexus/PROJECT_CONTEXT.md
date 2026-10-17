# PROYECTO ZERO — Project Context

## Mission
Build NEXUS, a personal hybrid AI assistant that acts as a critical partner, strategist, and close collaborator. It should help plan and execute technical and business work, preserve useful context, and verify results rather than merely sound confident.

## Decisions already made
- Project name: PROYECTO ZERO.
- Assistant name: NEXUS.
- Personality: critical partner + strategist + close companion.
- Platform: hybrid computer + cloud.
- Memory preference: primarily cloud eventually, so it can be accessed from different devices.
- Learning: NEXUS can learn from task outcomes and propose improvements, but the user reviews changes before they affect behavior.
- Budget: start with free tools where possible; spend only when value is demonstrated.
- Development priority: get a working prototype quickly, then improve it incrementally.

## User environment
- Windows PC.
- Known hardware: Intel i5 2nd generation, 8 GB DDR3 RAM; not a suitable target for large local language models.
- Recommended initial strategy: run the app locally, use a cloud model API for advanced reasoning once configured, and consider a small local model only as an optional later addition.
- User prefers concise, practical, step-by-step guidance in Spanish and does not want to repeat decisions already made.

## Intended capabilities
- Conversational interface and persistent memory.
- Project and decision context.
- Model-provider adapters for hybrid AI.
- File/code assistance and verified task execution.
- Business support: planning, costs, sales, inventory, and workflows.
- Later: voice, vision/camera, and more autonomous task execution.

## Safety rules
- Never store secrets in source control.
- Require explicit approval for purchases, transfers, commercial messages, publishing/production changes, and important deletions.
- Log meaningful actions and provide a stop mechanism.
- Keep remote access disabled until authentication, access controls, and a secure deployment are in place.
- Treat model outputs as suggestions until checked; use tests or deterministic checks when possible.
- No self-modification of core rules without review.

## Current truth
The first version is a foundation, not a finished autonomous AI. Its chat is in demo mode until a provider adapter is configured. SQLite is local initially; cloud memory and multi-device access come later after authentication and deployment are designed.
