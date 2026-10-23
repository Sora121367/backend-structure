# InsightHub — backend

Spring Boot (Java 21, Gradle 9.5.1 multi-module) + AI service (Python/FastAPI) + shared contracts, spec and Keycloak config.

| Need | Command (repo root) |
|---|---|
| Spring dev infra (Keycloak, MinIO, Redis, Mailpit, app DB) | `docker compose -f modules/compose.spring.yaml up -d` |
| AI dev infra (+ vector DB) | `docker compose -f ai-service/compose.ai.yaml up -d` (`--profile gpu` adds Ollama) |
| Everything in containers | `docker compose --profile app up -d --build` |
| Build / test Spring | `./gradlew build` · `./gradlew :modules:classroom:test` |
| AI service | `cd ai-service && uv sync && uv run pytest` |
| API mock for client teams | `npx @stoplight/prism-cli mock contracts/openapi.yaml` |

Local URLs: Keycloak http://localhost:8180 (admin/admin) · MinIO console http://localhost:9001 · Mailpit http://localhost:8025 · app DB :5432 · vector DB :5433

Working with Claude Code: start `claude` **at this repo root**, then use `/start-task <module> <task>`.
Team skills: `/start-task`, `/contract-change`, `/new-migration`, `/resolve-conflicts`, `/pre-pr`.
Setup steps: `SETUP-GUIDE.md`. Rules: `CLAUDE.md`, `docs/conventions.md`, `docs/adr/`.
