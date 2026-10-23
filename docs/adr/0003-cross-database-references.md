# ADR-0003: No foreign keys across the app DB and the vector DB

- Status: Proposed — confirm in team meeting
- Date: 2026-10-23

## Context
The ERD draws `chunks.document_id → documents.id`, but `chunks` lives in the vector DB (AI service) and `documents` in the app DB (Spring Boot). A foreign key cannot cross databases. Deleting a document, leaving a classroom or deleting a user must still remove the derived chunks.

## Decision (proposed)
- `chunks.document_id` is an indexed UUID column without an FK.
- Spring Boot writes deletion events to an outbox table in the same transaction; a worker calls the AI service delete endpoint with retries. AI delete endpoints are idempotent.
- A nightly reconciliation job removes chunks whose `document_id` no longer exists.
- `ingest_jobs` stays in the app DB; the AI service reports progress to Spring Boot (callback or queue — see ADR-0004).

## Consequences
Update the ERD. `contracts/ai-service.yaml` must define delete-by-document and delete-by-workspace endpoints.
