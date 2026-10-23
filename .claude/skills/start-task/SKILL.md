---
description: Start a backend task in one module with a plan first
argument-hint: <module> <what to build>
disable-model-invocation: true
---
Task: $ARGUMENTS

1. Read `modules/<module>/CLAUDE.md` (or `ai-service/CLAUDE.md`) and the spec section in `docs/project-instructions.md` that covers this task. Read the relevant part of `contracts/`.
2. Check: does this task need a contract change, a migration, or a change outside the module? If yes, list exactly what and STOP — don't edit anything yet.
3. Otherwise write a short plan: files to create/change, tests to add, open questions. Wait for my approval.
4. After approval: implement inside the module only, add tests, run the module's tests, and show a summary of what changed.
