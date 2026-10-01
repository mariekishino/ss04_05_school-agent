# Architecture

## Rule

Do not build a giant smart Discord bot.

Separate communication, transport, reasoning, business rules, operational data, actions, and teacher UI.

## Components

```text
Discord
   |
Discord Bot / Adapter
   |
Agent Inbox
   |
Agent Core
   +-- Student DB
   +-- School Rules
   +-- Google Calendar
   |
Agent Outbox
   |
Discord Bot / Adapter
   |
Discord
```

### Discord Bot

The bot is the system's **ear and mouth**.

It receives Discord events, captures IDs/text, normalizes messages, writes Inbox records, delivers Outbox records, and records delivery success.

It does NOT decide policy or business meaning.

### Agent Inbox

Inbox is work waiting for the agent. For the PoC, it can be a SQLite table.

Example:

```json
{
  "source": "discord",
  "external_user_id": "123456",
  "channel_id": "987654",
  "message_id": "555555",
  "text": "Can I change my October 3 lesson?",
  "status": "pending"
}
```

### Agent Core

The agent handles language and orchestration:

```text
identify actor
-> interpret intent
-> resolve target
-> check policy
-> call tools
-> decide whether approval is required
-> produce action/response
```

Use ordinary deterministic code for fixed business rules.

### Agent Outbox

Outbox is work ready to be delivered.

```json
{
  "destination": "discord",
  "channel_id": "987654",
  "text": "October 5 at 17:00 and October 6 at 18:00 are available.",
  "status": "pending"
}
```

### Database

Operational source of truth for students, identities, tasks, lessons, approvals, Inbox/Outbox, and audit records.

### Google Calendar

Schedule interface. Candidate tools:

```text
get_lesson(student_id, date)
find_available_slots(start, end)
reschedule_lesson(lesson_id, new_time)
cancel_lesson(lesson_id)
```

### Dot

Dot is a possible **teacher-facing console**, not a hard dependency and not necessarily Agent Core.

```text
Teacher <-> Dot <-> Agent / School State
```

Its external integration capabilities must be verified before the core architecture depends on it.
