# Email OTP authenticator (Keycloak SPI, Java)

Custom authenticator for the "reset credentials" flow (spec Feature 1, Forgot password).
Not a Spring Boot module: it is built as a JAR and copied into Keycloak's `providers/` folder.

To scaffold (ask Claude Code from this folder, plan mode):
> Scaffold a Keycloak authenticator SPI project here (Gradle, Java 21, matching the Keycloak version in docker/compose.infra.yaml) for email OTP in the reset-credentials flow, following spec Feature 1. Plan first; no implementation of the OTP logic yet.

Security requirements (from the spec): single-use, 2–5 min validity, hashed OTP, lock after 5 wrong attempts, same message whether or not the email exists, rate limits per email and IP.
