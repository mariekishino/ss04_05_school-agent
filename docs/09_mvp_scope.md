# MVP Scope

## 1. Purpose of the MVP

The MVP exists to validate one core hypothesis:

> A small-school administrative task can be completed through natural conversation inside an existing community space, without forcing the student or teacher to use a traditional booking interface.

The first environment is a fictional small piano school using Discord.

The MVP is **not** intended to prove that the system can manage an entire school.

It is intended to prove that one real administrative workflow can be delegated safely to an AI agent from end to end.

---

## 2. Core MVP User Story

The primary user story is:

> As a piano student or parent, I can ask the secretary in natural language to reschedule an existing lesson, receive valid alternative times, choose one conversationally, and have the lesson actually updated without the teacher manually handling the request.

Example:

```text
Student:
@secretary Can I change my October 3 lesson?

Secretary:
Yes. October 5 at 17:00 and October 6 at 18:00 are available.
Which would you prefer?

Student:
The 5th please.

Secretary:
Your lesson has been moved to October 5 at 17:00.
```

The Google Calendar event must actually be changed.

---

## 3. MVP Boundary

The MVP begins at:

```text
Student sends a message in Discord
```

and ends at:

```text
The requested lesson is safely updated
and confirmation is returned to Discord.
```

The complete MVP path is:

```text
Discord
   ↓
Discord Bot
   ↓
Agent Inbox
   ↓
Agent Core
   ↓
Student Identity
   ↓
School Rules
   ↓
Google Calendar
   ↓
Agent Outbox
   ↓
Discord Bot
   ↓
Discord
```

---

## 4. In Scope

The MVP must support the following.

### Discord communication

- Receive an explicit request directed to the secretary bot
- Identify the Discord user and channel
- Return responses to the correct Discord context

### Agent Inbox / Outbox

- Persist incoming work
- Track processing state
- Persist outgoing responses
- Track delivery state

### Student identity

The system can map:

```text
Discord user
    ↓
internal student_id
```

Only the minimum identity model necessary for the PoC is required.

### Intent interpretation

The agent can recognize at least:

```text
RESCHEDULE_LESSON
```

Other intents may be recognized for testing, but they are not required for MVP completion.

### Existing lesson lookup

The system can identify the lesson the student is referring to.

Example:

```text
"my October 3 lesson"
```

must resolve to the correct existing booking.

### School rules

At minimum, implement one deterministic scheduling rule.

Example:

```text
Rescheduling less than 24 hours before a lesson
requires teacher approval.
```

The rule must be implemented in deterministic application logic rather than left entirely to LLM judgment.

### Google Calendar read

The system can:

- locate the existing lesson
- inspect relevant schedule availability
- find valid alternative slots

### Multi-turn task state

The system must understand that:

```text
Student:
Can I change October 3?

Agent:
October 5 at 17:00 or October 6 at 18:00.

Student:
The 5th.
```

is one continuing reschedule task.

### Google Calendar write

After explicit student confirmation, the system can update the actual lesson event.

Before mutation, availability should be rechecked.

### Confirmation

The student receives confirmation only after the calendar change succeeds.

### Basic auditability

For a state-changing action, the system records enough information to determine:

```text
what changed
when it changed
which task caused it
```

---

## 5. Human Approval in MVP

Human approval is included only for one simple policy-exception path.

Example:

```text
Student requests a change inside the 24-hour deadline.
```

Expected behavior:

```text
Student request
     ↓
Agent checks rule
     ↓
NEEDS_APPROVAL
     ↓
Teacher approves or declines
     ↓
Task resumes
```

The approval interface may initially be simple.

A polished teacher dashboard is not required.

The purpose is to prove that the agent can stop and return control to a human when it should not act autonomously.

---

## 6. Explicitly Out of Scope

The following are **not part of the MVP**.

### Additional communication channels

Do not implement:

- LINE
- Gmail
- SMS
- Web chat
- WhatsApp
- Slack

Discord is the only required external communication channel.

### Full school management

Do not implement:

- billing
- payments
- invoices
- attendance analytics
- student enrollment
- contracts
- teacher payroll
- accounting

### Full event management

Do not implement complete workflows for:

- recitals
- event registration
- ticketing
- attendance collection
- event payments

Discord may still be used manually for event/community discussion.

### AI video analysis

Students may manually share videos in Discord, but the MVP does not analyze performance videos.

### Advanced community intelligence

Do not implement:

- automatic community summaries
- sentiment analysis
- student progress inference
- automatic relationship analysis

### Multi-school architecture

The MVP supports one fictional piano school.

Do not optimize for:

- multiple schools
- franchises
- tenant isolation
- large organizations

### Multi-teacher scheduling

Assume one teacher unless implementation naturally makes multiple teachers trivial.

### Production-scale infrastructure

Do not introduce infrastructure such as Kafka, RabbitMQ, Kubernetes, or distributed databases for the MVP.

SQLite is acceptable.

### Custom mobile/web application

Do not build a student-facing application.

Discord is the student-facing interface.

### Polished teacher dashboard

A custom dashboard is not required for MVP completion.

---

## 7. Dot Is Not an MVP Dependency

Dot is intentionally excluded from the core MVP completion criteria.

The MVP must work without Dot:

```text
Discord
   ↓
Agent System
   ↓
Google Calendar
   ↓
Discord
```

After the core workflow works, Dot can be evaluated as a teacher-facing console.

Possible later experience:

```text
Teacher:
What happened today?

Dot:
Two reschedules were completed.
One cancellation was received.
One request requires your approval.
```

This is a separate product hypothesis:

> Can a conversational teacher console make school operations easier to understand and supervise?

It should not block validation of the core agent workflow.

---

## 8. MVP Definition of Done

The MVP is complete when the following scenario succeeds reliably.

### Setup

There is:

- one Discord server
- one teacher
- at least two fictional students
- existing lessons in Google Calendar
- basic student records
- one rescheduling policy

### Test

Student A sends:

```text
@secretary Can I change my October 3 lesson?
```

The system:

1. receives the Discord message
2. identifies Student A
3. identifies the October 3 lesson
4. recognizes the request as `RESCHEDULE_LESSON`
5. evaluates the scheduling rule
6. checks Google Calendar
7. finds valid alternative slots
8. replies with alternatives

Student replies:

```text
October 5 please.
```

The system:

9. associates the reply with the existing task
10. resolves the selected slot
11. rechecks availability
12. updates Google Calendar
13. records the state change
14. sends confirmation to Discord

The Calendar must show the new booking.

---

## 9. Safety Test

The MVP must also pass one exception scenario.

Student requests a change that violates the configured scheduling rule.

The system must:

```text
recognize the rule violation
        ↓
NOT change the Calendar
        ↓
set NEEDS_APPROVAL
        ↓
inform the student that teacher confirmation is required
        ↓
allow the teacher to approve or decline
```

The agent must never silently override the rule.

---

## 10. Success Criteria

The MVP succeeds if we can demonstrate:

### Functional

A complete rescheduling workflow can occur through natural Discord conversation.

### Operational

The teacher does not manually search the calendar or manually perform the normal reschedule.

### Safety

The agent stops when a defined policy exception requires human judgment.

### Architectural

Discord-specific behavior remains outside Agent Core.

The workflow should conceptually allow:

```text
Discord
```

to later be replaced or supplemented by:

```text
LINE
Email
Web
```

without rewriting the business logic.

### Understandability

The human developer can explain:

```text
how the message entered
where it was stored
how the task was represented
how the agent interpreted it
which rule was evaluated
which tool was called
what state changed
how the response returned
```

If the system works but this flow cannot be clearly explained, the learning goal has not been met.

---

## 11. Post-MVP

After the MVP works, evaluate the next hypotheses separately.

### Teacher Console

Can Dot provide a useful operational view for the teacher?

### Community Intelligence

Can the agent answer questions across announcements, events, and school history without damaging privacy or community feel?

### Multi-channel

Can LINE, email, or web communication feed the same Agent Inbox?

### Additional workflows

Possible next workflows:

```text
CANCEL_LESSON
ASK_SCHEDULE
ASK_POLICY
ASK_EVENT
RECITAL_RESPONSE
```

### Product validation

Only after the technical PoC works should the project seriously evaluate:

- real teacher pain points
- willingness to pay
- onboarding friction
- Discord suitability for actual families
- privacy expectations
- competing products

---

## 12. Scope Rule

When deciding whether to add something during MVP development, ask:

> Is this required for the end-to-end lesson rescheduling scenario or its safety path?

If the answer is no, it belongs after the MVP unless it fixes a fundamental architectural problem.