# Design Principles

1. **Community first.** Preserve conversation, announcements, reactions, video sharing, and community history.

2. **Automate administration, not relationships.** Teaching feedback, encouragement, sensitive conversations, and educational judgment remain human.

3. **Channels are adapters.** Discord is not the product core.

4. **Keep Agent Core independent.** Prefer `Adapter -> Inbox -> Agent -> Outbox -> Adapter`.

5. **Deterministic rules stay deterministic.** A fixed 24-hour deadline belongs in code, not LLM judgment.

6. **Human-in-the-loop is a feature.** Escalate policy exceptions, ambiguous identity, conflicting state, and uncertain high-impact actions.

7. **Keep structured source-of-truth data outside chat history.** Discord history is context, not the booking database.

8. **Dot is replaceable.** The core system must survive without Dot.

9. **Audit state changes.** Record what changed, when, why, and which task caused it.

10. **Start narrow.** First vertical: piano school. First workflow: lesson rescheduling. Generalize later.
