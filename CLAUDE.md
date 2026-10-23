# InsightHub — backend repo

This repo holds the Spring Boot service (Gradle multi-module), the AI service (Python/FastAPI),
and everything the four InsightHub repos share: the spec, decisions (ADRs), API contracts and Keycloak config.
Frontend, iOS and Android live in their own repos and read this one as read-only context.

## Source of truth (read before designing anything new)
- Spec: `docs/project-instructions.md` — scope, features, decisions, AI rules. Read the relevant section before designing a feature. If a request conflicts with it, point out the conflict before proceeding.
- Decisions: `docs/adr/` — one file per decision. Never contradict an accepted ADR silently.
- Conventions: @docs/conventions.md — naming, errors, API style, git workflow.
- Data model: `docs/erd.png` (Spring Boot DB). The vector DB belongs to the AI service.

## Repo map
| Path | What | Rules file |
|---|---|---|
| `modules/` | Spring Boot modules (Java 21, Gradle 9.5.1) | `modules/CLAUDE.md` + one per module |
| `ai-service/` | Python/FastAPI: ingestion, RAG, generation (NOT a Gradle module) | `ai-service/CLAUDE.md` |
| `contracts/openapi.yaml` | Public API used by web, iOS, Android | `contracts/README.md` |
| `contracts/ai-service.yaml` | Internal API: Spring Boot → AI service | `contracts/README.md` |
| `keycloak/` | Realm config as code + custom OTP authenticator | `keycloak/README.md` |
| `docker/`, `compose.yaml` | Local dev infrastructure | — |

## Hard rules (never break these)
1. **Contract first.** Never add, rename or remove an endpoint, field or status code without changing `contracts/` first. Contract changes go in their own PR (`/contract-change`). If a task needs a contract change, STOP and tell me.
2. **Scope filter is mandatory.** Every vector or keyword search in the AI service filters by the scope the backend sends. A search without a scope filter must fail. The AI service never decides access itself.
3. **Personal-workspace content never reaches shared resources.** Only sets generated in a course workspace can be shared, and only to that course. Enforce on the backend.
4. **Quiz results are never stored** — no attempts, answers or scores on the server.
5. **Two databases, two owners.** Spring Boot owns the app DB (Flyway). The AI service owns the vector DB (Alembic). Neither touches the other's DB. No foreign keys across them (see ADR-0003).
6. **Identity lives in Keycloak.** No passwords, temporary passwords or OTPs in Spring Boot tables or logs.
7. **Fully local AI.** No cloud LLM or embedding calls. The only outside call is web search, with the rewritten query only.
8. **No secrets in git.** Use `.env` (gitignored); add new variables to `.env.example`.

## Ask before you change these (stop and tell me)
- `contracts/**`, `docs/**`, any `CLAUDE.md`
- Flyway or Alembic migrations (use `/new-migration`)
- `settings.gradle.kts`, `build.gradle.kts`, `gradle/libs.versions.toml`
- `modules/common/**` (everyone depends on it)
- `keycloak/realm-export.json`, `compose*.yaml`, `.github/**`

## How to work in this repo
- Claude is always started at the repo root (that's where the shared `.claude/` settings and hooks load from). The prompt names the module to work in; read that module's `CLAUDE.md` before editing it.
- One task = one module. Don't change both Spring Boot and the AI service in one task unless I ask.
- For anything non-trivial, plan first and show me the plan before editing.
- Write or update tests with every change. Run the module's tests before saying you're done.
- Keep PRs small (aim for under ~400 changed lines). Conventional commits (`feat(classroom): ...`).

## Glossary (spec term → code term)
- material / source → `documents` table · course workspace / personal workspace → `workspaces.type` = `COURSE` / `PERSONAL`
- shared set → `shared_resources` · flashcard set → `flashcard_decks`
