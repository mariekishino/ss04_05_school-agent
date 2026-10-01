# AGENTS.md

## Project

Community-first AI agent PoC for a small piano school.

Read these documents before making architectural changes:

- docs/00_product_vision.md
- docs/01_architecture.md
- docs/04_development_plan.md
- docs/05_design_principles.md
- docs/08_development_workflow.md
- docs/09_mvp_scope.md

## Development rules

- Work on one small observable behavior at a time.
- Do not implement features outside the current issue.
- Do not redesign the architecture without explaining why.
- Keep Discord-specific logic outside Agent Core.
- Keep deterministic business rules outside the LLM.
- Do not introduce Dot as a core dependency.
- Do not add post-MVP features unless explicitly requested.
- Prefer the simplest implementation that satisfies the current acceptance criteria.

## Before coding

State briefly:

1. what you are changing
2. which files you expect to touch
3. what is explicitly out of scope

## After coding

Report:

1. files changed
2. behavior implemented
3. tests/checks run
4. known limitations
5. any architectural concern discovered

## Security

Never commit:

- `.env`
- Discord bot tokens
- API keys
- Google OAuth secrets
- real student data

Use synthetic test data during the PoC.