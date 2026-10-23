# Module: notification

- Owner: <name>
- Device tokens, FCM/APNs, email notices, spaced-repetition reminders. Listens to other modules' events; other modules never call it synchronously for business logic.
- Only edit files inside `modules/notification/` unless I explicitly ask otherwise. If you need a change in another module or in `contracts/`, stop and tell me.
- Test: `./gradlew :modules:notification:test`
