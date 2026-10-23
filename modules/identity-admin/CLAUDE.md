# Module: identity-admin

- Owner: <name>
- Keycloak Admin REST API via the confidential client insighthub-admin-service (least privilege). Never store or log temporary passwords. Excel import: validate → preview → confirm, idempotent by student ID/email, background job with per-row report, file deleted after import. Every admin action → audit log.
- Only edit files inside `modules/identity-admin/` unless I explicitly ask otherwise. If you need a change in another module or in `contracts/`, stop and tell me.
- Test: `./gradlew :modules:identity-admin:test`
