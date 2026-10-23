# Module: classroom

- Owner: <name>
- Classroom → course → documents. Invites: long random codes, rate-limited, revocable; instructor invites only for instructor accounts. Removing a document must trigger deletion of chunks in the AI service via the outbox (ADR-0003).
- Only edit files inside `modules/classroom/` unless I explicitly ask otherwise. If you need a change in another module or in `contracts/`, stop and tell me.
- Test: `./gradlew :modules:classroom:test`
