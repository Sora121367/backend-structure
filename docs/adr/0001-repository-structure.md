# ADR-0001: Four repositories; backend repo holds shared contracts

- Status: Accepted
- Date: 2026-10-23

## Context
Web (Next.js), iOS (SwiftUI), Android (Compose) and the backend (Spring Boot + Python AI service) are built by different people, each with Claude Code.

## Decision
- Four repos: `backend`, `frontend`, `ios`, `android`.
- `backend` is a Gradle multi-module Spring Boot project plus an `ai-service/` folder (Python, not a Gradle module). Both deploy as separate services.
- The spec, ADRs, `contracts/openapi.yaml`, `contracts/ai-service.yaml` and Keycloak realm config live in `backend`. Client repos read them from a sibling checkout at `../backend` (read-only).
- Clients use API clients generated from `openapi.yaml`, never hand-written DTOs.

## Consequences
- Every developer clones all repos they need side by side under one folder.
- Contract changes are separate PRs in `backend`, reviewed by the backend owner and at least one client owner.
- CI in `backend` uses change detection so Java and Python jobs run only when needed.
