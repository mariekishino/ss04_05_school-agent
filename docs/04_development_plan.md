# Development Plan

Build one layer at a time.

## Phase 1 — Discord transport

```text
Discord -> Bot -> Terminal
```

No AI, DB, Calendar, or Dot.

## Phase 2 — Inbox

Add SQLite:

```text
Discord -> Bot -> agent_inbox
```

## Phase 3 — Outbox

Manually insert an Outbox record and make the bot deliver it:

```text
agent_outbox -> Bot -> Discord
```

Now transport works in both directions.

## Phase 4 — Agent interpretation

Add an LLM and convert natural language into structured intent.

```json
{
  "intent": "RESCHEDULE_LESSON",
  "date": "2026-10-03"
}
```

Do not grant calendar-write access yet.

## Phase 5 — Identity and rules

Map Discord identity to internal student ID. Implement deterministic policy in code.

Example:

```text
reschedule_deadline_hours = 24
max_reschedules_per_month = 2
lesson_duration_minutes = 45
```

## Phase 6 — Google Calendar

Read-only tools first:

```text
get_lesson()
find_available_slots()
```

Then mutations:

```text
reschedule_lesson()
cancel_lesson()
```

## Phase 7 — Multi-turn task state

Support follow-ups like `The 5th` by tying messages to an existing task/conversation.

## Phase 8 — Human approval

Implement `NEEDS_APPROVAL`.

## Phase 9 — Teacher console / Dot

Only after the operational core works, test Dot as the teacher-facing interface.

## Phase 10 — More channels

Add LINE, email, or web adapters only after Discord works.

## Suggested stack

```text
Python
discord.py
SQLite
OpenAI API or another LLM API
Google Calendar API
FastAPI only if/when an HTTP API is needed
```
