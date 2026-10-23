---
description: Create a Flyway migration with the team naming rule
argument-hint: <what the migration does>
disable-model-invocation: true
---
Migration: $ARGUMENTS

1. Read `docs/conventions.md` (Database) and ADR-0002. Look at existing files in `modules/app/src/main/resources/db/migration/`.
2. Name: `V<yyyyMMdd_HHmm>__<snake_description>.sql` using the current date and time (run `date +%Y%m%d_%H%M`).
3. Only CREATE/ALTER for this task. UUID PKs, TIMESTAMPTZ, VARCHAR + CHECK for enums, indexes for every FK and filter column.
4. Never edit an existing migration. Never add an FK to tables in the vector DB.
5. Show me the SQL before writing the file. Then add/adjust a Testcontainers test that runs Flyway.
