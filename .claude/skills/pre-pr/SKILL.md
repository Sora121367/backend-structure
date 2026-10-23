---
description: Check the branch before opening a PR
disable-model-invocation: true
---
1. `git fetch origin && git diff --stat origin/main...HEAD` — list changed files and size. Warn if over ~400 lines or touching more than one module.
2. Confirm every changed controller/endpoint matches `contracts/openapi.yaml`.
3. Search the diff for secrets, tokens, passwords, `System.out`, TODOs without an owner, and logs of personal data.
4. Run tests for each changed module (`./gradlew :modules:<m>:test`, `cd ai-service && uv run pytest`).
5. Draft the PR title (Conventional Commits) and fill in `.github/pull_request_template.md`.
