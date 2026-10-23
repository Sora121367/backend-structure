# Spring Boot modules (Java 21, Gradle 9.5.1 wrapper, Spring Boot 4.x)

## Build and test
- Always use the wrapper (`./gradlew`), never a locally installed `gradle`. The wrapper pins Gradle 9.5.1; the toolchain pins Java 21.
- All: `./gradlew build` · One module: `./gradlew :modules:classroom:test` · Run app: `./gradlew :modules:app:bootRun`
- Infra for local dev: `docker compose -f modules/compose.spring.yaml up -d` (from repo root).

## Module boundaries (the main source of conflicts — keep them strict)
- Package root per module: `com.insighthub.<module>` (e.g. `com.insighthub.identityadmin`).
- The top-level package is the module's **public API**: service interfaces, DTOs (records), domain events.
- Everything else goes in `com.insighthub.<module>.internal..` (entities, repositories, controllers, mappers). Never import another module's `internal` package.
- Modules talk through public service interfaces or Spring application events — never another module's entities or repositories.
- Only `modules:app` depends on every module. Feature modules depend on `common` (and, if unavoidable, another module's public API — ask first).
- `common` changes go in their own small PR.

## Layers inside a module
`internal/web` (controllers, generated from or matching `contracts/openapi.yaml`) → `internal/service` → `internal/persistence` (JPA entities, Spring Data repositories).

## Code rules
- Java records for DTOs; no Lombok on entities' equals/hashCode.
- Controllers: path, names and schemas must match `contracts/openapi.yaml` exactly. If they don't, the contract wins.
- Authorization: `@PreAuthorize` for realm roles + an explicit membership/ownership check in the service for every classroom/workspace/document ID.
- Errors: throw domain exceptions; `common` maps them to Problem Details with a `code`.
- Migrations: only in `modules/app/src/main/resources/db/migration`, named per ADR-0002. Use `/new-migration`.
- Calls to the AI service go through one client in `workspace` / `classroom` built from `contracts/ai-service.yaml`, always with a Scope built here.
- Tests: unit tests for services; `@WebMvcTest` for controllers; Testcontainers (PostgreSQL) for repositories and migrations.
