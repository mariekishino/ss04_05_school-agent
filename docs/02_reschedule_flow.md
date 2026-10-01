# Lesson Reschedule Flow

This is the first complete workflow.

## Normal case

```text
Student:
@secretary Can I change my October 3 lesson?
```

1. Discord Bot receives the message.
2. Bot stores a normalized event in `agent_inbox`.
3. Agent processes it.
4. Agent resolves student, intent, target lesson, policy, and available alternatives.
5. Agent writes a response to `agent_outbox`.
6. Bot sends the response.
7. Student chooses a slot.
8. Reply becomes another Inbox event tied to the existing task.
9. Agent rechecks availability, updates Calendar, records the action, and confirms.

Example:

```text
Student: Can I change October 3?
Secretary: October 5 at 17:00 or October 6 at 18:00.
Student: The 5th please.
Secretary: Confirmed for October 5 at 17:00.
```

## Exception

If a rule says changes inside 24 hours are normally not eligible:

```text
task.status = NEEDS_APPROVAL
```

The student gets an immediate acknowledgement while the teacher receives an approval request.

## Autonomy levels

```text
Read-only factual question -> automatic
Show available slots -> automatic
Change booking -> confirm intent, then execute
Policy exception -> teacher approval
```

The goal is **safe delegation**, not maximum autonomy.
