# Conventions

Short and binding. Change only by PR + ADR.

## Git
- Branches: `feat/<module>-<short-name>`, `fix/...`, `contract/...`, `chore/...`. Short-lived (≤ 3 days).
- Rebase on `main` at least daily. Squash-merge PRs.
- Commits: Conventional Commits — `feat(classroom): add invite revoke`, `fix(ai): ...`, `contract: ...`.
- PR size: aim for < 400 changed lines. One module per PR when possible.
- Every PR: tests pass, CI green, one human approval (two for `contracts/` and migrations).

## Database (Spring Boot app DB, PostgreSQL)
- Tables `snake_case`, plural (`classroom_invites`). Columns `snake_case`.
- PK `id UUID`. Timestamps `TIMESTAMPTZ` (`created_at`, `updated_at`, `deleted_at` for soft delete).
- Enums stored as `VARCHAR` with a CHECK constraint (easier to migrate than PG enums).
- Flyway file name: `V<yyyyMMdd_HHmm>__<snake_description>.sql`, e.g. `V20261023_1430__create_classrooms.sql`. Never edit a merged migration; add a new one.

## Vector DB (AI service, pgvector)
- Alembic only. Scope columns are indexed: `scope_type, classroom_id, course_id, workspace_id, owner_id, document_id`.
- `document_id` is a plain UUID (no FK — the documents table lives in the other DB).

## API (contracts/openapi.yaml)
- Base path `/api/v1`. Resources plural, kebab-case: `/api/v1/classrooms/{classroomId}/invites`.
- JSON fields `camelCase`. IDs are UUID strings. Dates ISO-8601 UTC.
- Errors: RFC 9457 Problem Details (`application/problem+json`) with an extra `code` field (e.g. `CLASSROOM_NOT_FOUND`) the clients can translate.
- Pagination: `?page=0&size=20` → `{ items, page, size, totalItems }`.
- Long jobs return `202 Accepted` + a job resource; clients poll or receive a push/SSE event.
- Streaming answers: Server-Sent Events.
- Versioning: additive changes = minor version; removals/renames = breaking (deprecate first, remove after web + iOS + Android moved).

## Logging and security
- Never log tokens, passwords, OTPs, file contents, chat contents or Excel rows.
- Every request: role check (JWT) + ownership/membership check (Spring Boot). Never trust IDs sent by the client.

## Languages
- UI text and emails in Khmer and English. No hard-coded user-facing strings in the backend; return error `code`s.
