# Initial Data Model

Use SQLite for the first PoC.

## students

```text
id
display_name
discord_user_id
discord_private_channel_id
regular_lesson_day
regular_lesson_time
lesson_duration_minutes
active
created_at
updated_at
```

## agent_inbox

```text
id
source
external_user_id
channel_id
external_message_id
text
status
created_at
processed_at
error
```

States: `pending`, `processing`, `processed`, `failed`.

## agent_outbox

```text
id
task_id
destination
channel_id
reply_to_external_message_id
text
status
created_at
sent_at
error
```

States: `pending`, `sending`, `sent`, `failed`.

## tasks

A task is the business operation, not an individual message.

```text
id
student_id
type
status
target_lesson_id
context_json
created_at
updated_at
```

Types may include `RESCHEDULE_LESSON`, `CANCEL_LESSON`, `ASK_SCHEDULE`, `ASK_POLICY`, `ASK_EVENT`, `UNKNOWN`.

States may include `OPEN`, `WAITING_FOR_STUDENT`, `NEEDS_APPROVAL`, `EXECUTING`, `COMPLETED`, `FAILED`.

## lessons

```text
id
student_id
calendar_event_id
start_at
end_at
status
created_at
updated_at
```

## approvals

```text
id
task_id
reason
status
decision_by
created_at
decided_at
```

## audit_log

```text
id
actor
action
entity_type
entity_id
before_json
after_json
created_at
```

The system should always be able to answer: **What exactly did the agent change?**
