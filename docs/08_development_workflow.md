# Development Workflow

## Purpose

This document defines **how this project is developed**, not what features it contains.

The project should be built as a sequence of small, observable, reviewable changes. The goal is to keep the architecture understandable while using Codex as an implementation assistant.

The default loop is:

```text
Design
  ↓
Define one small issue
  ↓
Codex implements
  ↓
Human code review
  ↓
Run and test
  ↓
Fix if necessary
  ↓
Update design docs if the design changed
  ↓
Commit
  ↓
Next issue
```

---

## 1. Development strategy: vertical slices

Prefer thin end-to-end slices over completing entire layers in isolation.

Avoid:

```text
Build all DB tables
  ↓
Build all Discord features
  ↓
Build all Agent features
  ↓
Build all Calendar features
```

Prefer:

```text
Discord -> Terminal
          ✓

Discord -> Inbox
          ✓

Outbox -> Discord
          ✓

Discord -> Inbox -> Agent -> structured intent
                              ✓

Discord -> Agent -> Calendar read -> Discord
                                      ✓

Discord -> Agent -> Calendar write -> Discord
                                       ✓
```

Each step should produce something observable and testable.

---

## 2. Issue size

One issue should represent **one observable behavior**.

Bad issue:

```text
Implement Discord Bot
```

Too broad.

Better:

```text
Receive secretary mentions from Discord
```

Example acceptance criteria:

```text
Given:
  The Discord bot is online.

When:
  A student writes:
  "@secretary hello"

Then:
  The application prints:
  - Discord user ID
  - channel ID
  - message ID
  - message text
```

Next issue:

```text
Persist incoming Discord messages
```

Acceptance criteria:

```text
Given:
  The bot receives a secretary mention.

When:
  The message is processed.

Then:
  One row is inserted into agent_inbox.

And:
  status = pending
```

Next issue:

```text
Deliver pending Discord outbox messages
```

Acceptance criteria:

```text
Given:
  agent_outbox contains a pending Discord message.

When:
  The dispatcher runs.

Then:
  The message appears in the correct Discord channel.

And:
  the outbox row becomes sent.
```

---

## 3. Human and Codex responsibilities

### Human owns

The human developer owns:

- product direction
- architecture
- issue definition
- responsibility boundaries
- acceptance criteria
- security decisions
- business rules
- final code review
- final merge/commit decision

### Codex owns

Codex may:

- inspect the repository
- implement the current issue
- add focused tests
- explain implementation choices
- identify edge cases
- propose small refactors
- run relevant tests and checks

Codex should not silently redesign the entire architecture.

### Working model

Treat Codex as an implementation engineer, not as the project owner.

```text
Human
  ↓
Defines behavior and constraints

Codex
  ↓
Implements a small change

Human
  ↓
Reviews:
- Why is this responsibility here?
- What state changes?
- What can fail?
- Is the code understandable?
- Does this still match the architecture?

Human + Codex
  ↓
Test and refine
```

Do not ask Codex to "build the whole piano agent".

---

## 4. Before implementation

Every issue should answer:

### What behavior are we adding?

Example:

```text
Store a Discord secretary mention in agent_inbox.
```

### What is explicitly out of scope?

Example:

```text
No LLM interpretation.
No Calendar integration.
No automatic reply.
```

### What proves it works?

Example:

```text
After sending one Discord message, exactly one pending Inbox row exists with the correct IDs and text.
```

### Which component owns the behavior?

Example:

```text
Discord adapter:
  receives and normalizes the event

Repository/storage layer:
  persists the Inbox record
```

If these questions are unclear, the issue is probably too large or the design is not ready.

---

## 5. Codex task format

A useful Codex request should contain:

```text
Goal
Context
Scope
Out of scope
Acceptance criteria
Constraints
Tests/checks
```

Example:

```text
Goal:
Persist Discord secretary mentions into agent_inbox.

Context:
The bot already receives Discord messages and prints their metadata.
See docs/01_architecture.md and docs/04_development_plan.md.

Scope:
- Add the minimal SQLite setup.
- Add agent_inbox.
- Store user ID, channel ID, message ID, text, timestamp, and pending status.

Out of scope:
- LLM calls
- Agent Core
- Outbox
- Google Calendar
- Dot

Acceptance criteria:
Sending one @secretary message creates exactly one pending Inbox record.

Constraints:
Keep Discord-specific code out of the database layer.

Tests:
Add the smallest useful test for Inbox persistence and report how you verified it.
```

---

## 6. Review workflow

Do not accept a Codex change only because it runs.

Review the diff.

For every meaningful change, check:

### Responsibility

Does this code belong in this module?

Example warning sign:

```text
discord_bot.py
  -> interprets reschedule policy
```

That violates the architecture.

### State

Ask:

```text
What data is created?
What data changes?
What states can this object enter?
```

### Failure

Ask:

```text
What if Discord delivery fails?
What if SQLite is locked?
What if the same event arrives twice?
What if Calendar changes between proposal and confirmation?
```

Not every failure must be solved immediately, but important ones should be visible.

### Readability

Prefer code that can be understood without asking the model to explain it.

### Scope

Reject unrelated cleanup or architecture expansion unless it is necessary for the issue.

---

## 7. Testing strategy

Testing should grow with risk.

### Transport

Verify:

```text
Discord event received
correct IDs captured
correct channel used
outgoing message delivered
```

### Persistence

Verify:

```text
Inbox insert
Outbox insert
status transitions
task association
```

### Agent interpretation

Use fixed examples.

```text
"Can I change my October 3 lesson?"
-> RESCHEDULE_LESSON

"What time is the recital?"
-> ASK_EVENT
```

Structured output should be validated before business logic uses it.

### Business rules

Business rules should have deterministic unit tests.

Example:

```text
23 hours before lesson
-> requires approval

25 hours before lesson
-> normal reschedule path
```

### Calendar mutations

Test read behavior before write behavior.

Before a real mutation:

```text
resolve target
check current state
validate requested action
confirm availability
execute mutation
verify resulting state
write audit record
```

---

## 8. Definition of Done

An issue is done when:

- acceptance criteria pass
- relevant tests/checks pass
- the behavior has been manually observed when appropriate
- no secrets are committed
- the diff contains no unexplained unrelated work
- architecture boundaries remain intact
- state-changing behavior is sufficiently logged/auditable
- documentation is updated if the design changed
- the human developer understands the implementation

"Codex finished" is not the Definition of Done.

---

## 9. Architecture changes

Implementation will expose wrong assumptions. That is expected.

When architecture needs to change:

```text
Observation
  ↓
Design decision
  ↓
Update documentation
  ↓
Change implementation
```

Do not let architecture evolve only inside code.

Example:

```text
Observation:
One reschedule operation spans multiple Discord messages.

Decision:
Message and Task are separate concepts.

Reason:
"The 5th please" only makes sense in the context of the open reschedule task.

Impact:
Add tasks table.
Associate messages with task state.
```

For important decisions, add a short decision note to the relevant document or introduce an ADR later if needed.

---

## 10. Git workflow

Keep Git simple.

`main` should represent a working state.

For isolated Codex changes, small feature branches are useful:

```text
main
  |
  +-- feat/discord-receive
  |
  +-- feat/agent-inbox
  |
  +-- feat/agent-outbox
  |
  +-- feat/intent-parser
```

For a very small solo PoC, a branch for every tiny change is not mandatory.

The more important rule is:

**one Codex task = one focused, reviewable change set.**

Example commits:

```text
feat: receive Discord secretary mentions
feat: persist messages to agent inbox
feat: dispatch Discord outbox messages
feat: classify lesson reschedule requests
feat: read available calendar slots
```

Avoid commits such as:

```text
update stuff
agent improvements
finish backend
```

---

## 11. Secrets and environment

Never commit:

```text
.env
Discord bot tokens
OpenAI API keys
Google OAuth secrets
database files containing real user data
```

Keep `.env.example` with variable names only.

Example:

```text
DISCORD_BOT_TOKEN=
OPENAI_API_KEY=
GOOGLE_CALENDAR_ID=
```

Use test identities and synthetic student data during early development.

---

## 12. Current execution order

The initial sequence is:

```text
1. Discord message -> terminal
2. Discord message -> Inbox
3. Outbox -> Discord
4. Natural language -> structured intent
5. Discord identity -> student identity
6. School rules
7. Calendar read
8. Multi-turn task state
9. Calendar write
10. Human approval
11. Teacher console / Dot
12. Additional communication adapters
```

Do not skip ahead because a later feature is more exciting.

The purpose of this sequence is to keep failures local and understandable.

---

## 13. First issue

The initial development task is:

```text
Receive explicit secretary mentions from Discord and print normalized message metadata to the terminal.
```

Success looks like:

```text
[RECEIVED]
source: discord
user_id: ...
channel_id: ...
message_id: ...
text: hello
```

No database, LLM, Calendar, or Dot should be introduced in this issue.

For completed work, verification status, and the next issue, read
[Progress and restart notes](10_progress.md) before resuming development.
