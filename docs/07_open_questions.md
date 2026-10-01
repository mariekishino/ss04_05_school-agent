# Open Questions

## Dot

- Can Dot receive external events or webhooks?
- Can it read from a custom backend/database?
- Can it call custom actions?
- Can an approval request trigger Dot?
- Can a teacher's decision be written back to the backend?
- What latency is practical?

## Discord

- Process only explicit `@secretary` mentions, or all messages in `#ask-secretary`?
- Which private channels may the bot read?
- How should parent/student permissions differ?
- How much Discord history should be exposed to the agent?

## Identity

Long term, one person may have multiple endpoints:

```text
student_id = 42
  discord_user_id = ...
  email = ...
  line_user_id = ...
```

When and how should account linking happen?

## Calendar

- One school calendar or one per teacher?
- How are recurring lessons represented?
- How are breaks and unavailable periods represented?
- How is double-booking prevented?
- What is the source of truth if DB and Calendar disagree?

## Policy

- Reschedule deadline?
- Monthly reschedule limit?
- Cancellation behavior?
- Teacher override?
- What requires explicit student confirmation?

## Privacy and safety

Especially for children's schools:

- least-privilege channel access
- retention policy
- audit logs
- parent/guardian identity
- sensitive data minimization
- clear separation between community context and private operational data
