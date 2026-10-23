# Module: common

- Owner: Tech lead
- Security config, Problem Details, base entities, audit log, outbox. Everyone depends on this: keep it small, change it in separate PRs, never put feature logic here.
- Only edit files inside `modules/common/` unless I explicitly ask otherwise. If you need a change in another module or in `contracts/`, stop and tell me.
- Test: `./gradlew :modules:common:test`
