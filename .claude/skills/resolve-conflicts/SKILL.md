---
description: Resolve git rebase/merge conflicts safely and explain each choice
disable-model-invocation: true
---
1. Run `git status` and list every conflicted file.
2. If any conflicted file is in `contracts/`, a migration folder, `docs/`, a `CLAUDE.md`, or the Gradle root files: STOP and tell me which — a human decides those with the other owner.
3. For each other file: read both sides and the commits that introduced them (`git log --merge -p -- <file>`), keep the intent of both, and explain each resolution in one line.
4. Run the affected module's tests. Don't continue the rebase until I confirm.
