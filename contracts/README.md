# Contracts

| File | Consumers | Style |
|---|---|---|
| `openapi.yaml` | frontend, iOS, Android (generated clients) + Spring Boot (implements it) | Contract-first |
| `ai-service.yaml` | Spring Boot (generated Java client) + AI service (implements it) | AI service is code-first; CI exports FastAPI's OpenAPI and fails if it differs from this file |

## How to change a contract
1. Branch `contract/<short-name>`. Change **only** files in `contracts/` (use `/contract-change` in Claude Code).
2. Bump `info.version`: additive = minor (1.4.0 → 1.5.0); removal/rename = major, PR labeled `breaking`.
3. Reviewers: backend owner + at least one client owner (CODEOWNERS does this).
4. After merge, tag `api-v<version>` (e.g. `api-v1.5.0`). CI publishes the generated clients for that tag.
5. Then implement the server side in a separate PR. Clients can start right away against the mock server:
   `npx @stoplight/prism-cli mock contracts/openapi.yaml`

## Rules
- Every endpoint has `operationId` (camelCase, unique), a tag (= Spring module), and documented error responses.
- Reuse `components/schemas` and `components/responses`; don't inline the same object twice.
- Never delete an endpoint in one step: mark `deprecated: true`, ship, remove later.
