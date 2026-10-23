# ADR-0002: Timestamped migrations, one reviewer

- Status: Accepted
- Date: 2026-10-23

## Context
Several people add Flyway migrations in parallel. Sequential numbers (`V7`, `V8`) collide.

## Decision
- Flyway: `V<yyyyMMdd_HHmm>__<description>.sql`, all in `modules/app/src/main/resources/db/migration`.
- Flyway `outOfOrder` is enabled in dev only.
- Alembic (AI service) uses its default revision IDs; only the AI owner adds them.
- One named reviewer approves every migration PR.

## Consequences
Merged migrations are never edited. Fix forward with a new migration.
