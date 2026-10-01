# Product Vision

## Problem

Small schools handle individual messages, schedule changes, cancellations, make-up rules, announcements, recitals, video sharing, parent questions, and reminders.

Booking SaaS can solve scheduling but often removes the conversational/community feeling. Broadcast tools can feel impersonal. The teacher still absorbs much of the administrative work.

## Vision

Build a **community-first school agent**.

The online space should still feel like a school:

- shared announcements
- reactions and participation
- video sharing
- natural teacher communication
- private teacher/student spaces
- an AI secretary for administrative work

The AI is not the teacher. It is the administrative secretary living alongside the community.

## Discord PoC

```text
Piano School

INFORMATION
  # announcements
  # schedule

COMMUNITY
  # general
  # performances
  # music

EVENTS
  # recital-2026

SECRETARY
  # ask-secretary

PRIVATE LESSONS
  # student-a
  # student-b
  # student-c

STAFF ONLY
  # teacher
  # approval
  # agent-log
```

A private channel can contain the teacher, student/parent, and secretary bot.

## Long-term direction

Discord is a channel, not the product core.

```text
Discord ---\
LINE -------\
Email -------> Agent Inbox -> Agent Core -> Agent Outbox
Web --------/
```

Channels become adapters. The core operates on people, tasks, policies, and business state.
