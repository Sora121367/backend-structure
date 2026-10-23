# ADR-0004: Queue for long-running AI jobs

- Status: Proposed — decide before Feature 4 starts
- Date: 2026-10-23

## Context
Parsing, OCR, transcription, embedding and generation take seconds to minutes. Spec Section 2 requires async jobs with status reporting.

## Options
| Option | Pros | Cons |
|---|---|---|
| Redis + arq/Celery (Python workers) | Simple, one extra container, good Python support | Spring Boot side needs a Redis client for status |
| RabbitMQ | Mature routing, both Java and Python clients | One more system to operate |

## Decision
_To decide._ Local dev compose currently starts Redis.

## Consequences
Define job payloads, retries, timeouts, idempotency keys and status callbacks in `contracts/ai-service.yaml`.
