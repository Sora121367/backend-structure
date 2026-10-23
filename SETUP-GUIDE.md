# Backend repo: setup for team work with Claude Code

This guide gets the backend repo (Spring Boot multi-module + AI service) ready for the first feature. It doesn't include any feature implementation.
**Lead** = tech lead. **Everyone** = every backend and AI developer.

## Step 0. Kickoff meeting, 30 minutes (Lead + team)

| Decide | Write it in |
|---|---|
| Owner of each module: `identity-admin`, `profile`, `classroom`, `workspace`, `learning-resource`, `notification`, `ai-service`, `keycloak` | `.github/CODEOWNERS` and `modules/*/CLAUDE.md` (replace `<name>`) |
| Who reviews all migrations, and who approves contract changes | `.github/CODEOWNERS` |
| ADR-0003: no foreign key across the app DB and the vector DB | `docs/adr/0003-...md`: set Status to Accepted |
| ADR-0004: queue for AI jobs (Redis or RabbitMQ) | `docs/adr/0004-job-queue.md` |
| Branch, commit and PR rules (already drafted) | `docs/conventions.md` |

## Step 1. Install tools (Everyone)

- Git, Docker Desktop (Compose 2.20 or newer), `jq`, JDK 21 (Temurin recommended), Python 3.12, [uv](https://docs.astral.sh/uv/)
- A Claude plan that includes Claude Code (Pro, Max, Team or Enterprise)
- Claude Code (docs: https://code.claude.com/docs/en/setup)

```bash
curl -fsSL https://claude.ai/install.sh | bash      # macOS / Linux / WSL
irm https://claude.ai/install.ps1 | iex             # Windows PowerShell
claude                                              # first run: log in through the browser
```

On Windows, use WSL or Git Bash, because the team hook is a bash script.

## Step 2. Prepare and push the repo (Lead)

```bash
unzip insighthub-backend.zip && cd backend
cp "<path>/project-instructions-ai-learning-platform.md" docs/project-instructions.md   # replace the placeholder
# Edit .github/CODEOWNERS (@your-org/..., @member-x) and the <name> lines in modules/*/CLAUDE.md
# Check the Spring Boot version in gradle/libs.versions.toml against https://start.spring.io

git init -b main
git add .
git commit -m "chore: initial backend skeleton, contracts, docs and Claude Code setup"
git remote add origin git@github.com:<org>/insighthub-backend.git    # private, empty repo
git push -u origin main
```

Then check that it works:

```bash
./gradlew wrapper --gradle-version 9.5.1               # once: refresh gradlew scripts and wrapper jar to 9.5.1, then commit them
./gradlew --version                                      # should show Gradle 9.5.1 and a JVM 21
./gradlew build                                          # the first run downloads Gradle 9.5.1 and Spring Boot
docker compose -f modules/compose.spring.yaml up -d      # Keycloak, MinIO, Redis, Mailpit, app DB
```

Open http://localhost:8180 (admin/admin) and confirm the realm `insighthub` exists. Emails go to Mailpit at http://localhost:8025.

## Step 3. Protect `main` (Lead)

In GitHub, go to Settings → Rules → Rulesets and create a ruleset for `main`:

- Require a pull request, with **1 approval** and **review from Code Owners**
- Require status checks, and add **only `ci-ok`** (the Java, Python and contract jobs may be skipped by path filters; `ci-ok` always runs)
- Block force pushes, and require linear history
- In Settings → General, allow squash merge only and turn on "Automatically delete head branches"

## Step 4. Set up each laptop (Everyone)

```bash
mkdir -p ~/work/insighthub && cd ~/work/insighthub
git clone git@github.com:<org>/insighthub-backend.git backend
cd backend && cp .env.example .env
claude                       # ALWAYS start Claude at the repo root
```

**Always start Claude at the repo root.** Claude Code loads the shared settings and hooks only from the folder where you start it. To work on one module, name the module in your prompt; don't `cd` into it.

**First-session check (5 minutes):**

| Type in Claude Code | You should see |
|---|---|
| `/memory` | The root `CLAUDE.md` is loaded |
| `/permissions` | The allow, ask and deny rules from `.claude/settings.json` |
| `/hooks` | The PostToolUse format hook |
| `/` | `/start-task`, `/contract-change`, `/new-migration`, `/resolve-conflicts`, `/pre-pr` |
| "Summarize the hard rules of this repo" | The 8 hard rules from `CLAUDE.md` |

Personal preferences go in `CLAUDE.local.md`. It is gitignored, so it never changes the team's rules.

**Which services to start:**

| You work on | Command |
|---|---|
| Spring Boot | `docker compose -f modules/compose.spring.yaml up -d`, then run the app from the IDE or with `./gradlew :modules:app:bootRun` |
| AI service, no GPU | Set `OLLAMA_URL` in `.env` to the shared GPU server, then `docker compose -f ai-service/compose.ai.yaml up -d` |
| AI service, with GPU | `docker compose -f ai-service/compose.ai.yaml --profile gpu up -d` |
| Everything in containers | `docker compose --profile app up -d --build` |

## Step 5. Setup tasks with Claude Code (before any feature)

Do these in order, one PR each. Use plan mode (Shift+Tab) and read the plan before you approve it.

| # | Who | Prompt |
|---|---|---|
| 1 | Lead | `Add Spotless (google-java-format) to build.gradle.kts and enable the Java line in .claude/hooks/format.sh. Plan first.` |
| 2 | Lead | `Add Spring Modulith (version matching our Spring Boot line) and a test in modules:app that verifies module boundaries. Plan first.` |
| 3 | AI owner | `/start-task ai-service Set up the FastAPI skeleton: dependencies in pyproject.toml, app/main.py with only /health, app/worker.py stub, Alembic config. No business logic.` |
| 4 | Backend lead | `/contract-change Feature 1 and 2 endpoints (current user, profile, complete-profile prompt) per spec Features 1–2` |
| 5 | Backend lead | `/new-migration create the tables from docs/erd.png for users, instructor_profiles, student_profiles` (one migration per feature area, not the whole ERD at once) |
| 6 | Lead | `Add a GitHub Actions workflow that publishes generated API clients (TypeScript npm, Swift package, Kotlin) on tags api-v*. Plan first.` |
| 7 | Lead | `Add a breaking-change check for contracts/openapi.yaml to ci.yml (compare with main, fail unless the PR has the 'breaking' label).` |
| 8 | Auth owner | `Read keycloak/README.md and do the first checklist item (audience mapper). Then export the realm as described.` |

When these are merged, tag the first contract: `git tag api-v0.1.0 && git push origin api-v0.1.0`.

## Step 6. Daily workflow (Everyone)

```
morning    git pull  →  git switch -c feat/<module>-<short-name>
work       claude → /start-task <module> <task>      (Claude plans → you approve → it codes and tests)
           one task = one module; rebase daily: git pull --rebase origin main
before PR  claude → /pre-pr   → open the PR (under ~400 lines) → a human reviews every line
```

**When a feature changes the API:** first a contract-only PR (`/contract-change`), reviewed by the backend owner and one client owner, then merge and tag `api-vX.Y.Z`. After that, a second PR implements the endpoints.

## Step 7. When things conflict

| Situation | What to do |
|---|---|
| Git conflict in your branch | Run `git pull --rebase origin main`, then `/resolve-conflicts`. Check each resolution Claude explains, and run the tests. |
| Conflict in `contracts/`, a migration, `docs/`, a `CLAUDE.md` or the Gradle root files | Claude stops. Resolve it with the other owner. |
| Two people's Claude sessions chose different conventions | Decide together, write an ADR in `docs/adr/`, and add one line to the relevant `CLAUDE.md`. |
| A request contradicts the spec | Claude points it out. The lead decides and updates `docs/project-instructions.md`. |
| Claude keeps ignoring a rule | Make the rule shorter and more specific, or enforce it with CI, a permission rule or a test. |

## Ready-for-first-feature checklist (Lead)

- [ ] The real spec is in `docs/project-instructions.md`
- [ ] CODEOWNERS and module owners are filled in, and ADR-0003 and ADR-0004 are decided
- [ ] The repo is pushed, `main` is protected with `ci-ok`, and CI is green
- [ ] Every developer passed the Step 4 check, and the local stack starts on every laptop
- [ ] Setup tasks 1–8 are merged, and `api-v0.1.0` is tagged
- [ ] The AI owner has the shared GPU server URL, or Ollama runs locally
