---
description: Propose an API contract change as its own PR (contracts/ only)
argument-hint: <what endpoint/field and why>
disable-model-invocation: true
---
Contract change: $ARGUMENTS

1. Read `contracts/README.md` and `docs/conventions.md` (API section).
2. Edit ONLY files in `contracts/`. No server or client code.
3. Follow conventions: `/api/v1`, kebab-case paths, camelCase fields, operationId, tag = module, Problem Details errors, reuse components.
4. Bump `info.version`: additive → minor; removal/rename → major and tell me the PR needs the `breaking` label.
5. Run `npx @redocly/cli lint contracts/openapi.yaml contracts/ai-service.yaml`.
6. Give me: a PR title (`contract: ...`), a description listing every added/changed operation, and which client teams must review.
