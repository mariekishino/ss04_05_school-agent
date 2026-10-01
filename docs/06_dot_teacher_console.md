# Dot / Teacher Console

## Intended role

Discord is where the community lives. Dot is a candidate place where the teacher talks to the secretary and sees operational state.

```text
Students -> Discord -> Bot -> Inbox -> Agent -> DB/Rules/Calendar -> Outbox
                                      |
                                      v
                                     Dot
                                      ^
                                      |
                                   Teacher
```

Desired teacher queries:

```text
What happened today?
What needs my approval?
Who has not replied about the recital?
What changed in next week's schedule?
Does anyone need a response from me?
```

Possible summary:

```text
TODAY
Lessons: 6
Reschedules completed: 2
Absences: 1
Needs attention: 1

RECITAL
Participating: 18
No response: 4
Videos submitted: 12
```

## Constraint

Direct Discord access from Dot was not confirmed during initial design discussion, while Slack connectivity was known to exist.

Therefore:

- do not assume Dot can read Discord
- do not couple Discord Bot directly to Dot
- let the backend own operational state
- connect Dot later through a supported interface

If Dot cannot fill this role, another teacher console should be able to replace it.
