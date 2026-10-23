# Keycloak (realm config as code)

`realm-export.json` is imported automatically by `docker/compose.infra.yaml` on first start (realm `insighthub`).
It is a **starting point**: roles, clients, password policy, brute-force lockout, locales. Still to add (each as its own small PR):

- [ ] Audience mapper so access tokens carry `aud: insighthub-api`
- [ ] Service-account roles for `insighthub-admin-service` (realm-management: manage-users, view-users, query-users only)
- [ ] Required action `UPDATE_PASSWORD` default for created users (done by Spring Boot when creating users)
- [ ] Email (SMTP) settings via environment, not in this file
- [ ] Login theme (Khmer + English, accessible) in `themes/`
- [ ] Custom "reset credentials" flow using the OTP authenticator in `otp-authenticator/` (spec Feature 1)
- [ ] Production redirect URIs (per environment, not hard-coded here)

## Workflow for realm changes
1. Change the realm in the local admin console (http://localhost:8180, admin/admin).
2. Export: `docker compose exec keycloak /opt/keycloak/bin/kc.sh export --realm insighthub --file /tmp/realm.json --users skip`
   then `docker compose cp keycloak:/tmp/realm.json keycloak/realm-export.json`.
3. Review the diff (remove secrets and generated IDs you didn't mean to change), open a PR.
4. Others reset their realm: `docker compose down -v keycloak keycloak-db` then `up` again.

Secrets in this file are **dev-only**. Production secrets come from deployment config.
