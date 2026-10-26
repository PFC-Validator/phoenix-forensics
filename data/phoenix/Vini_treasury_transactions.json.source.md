# Source and provenance

- **Artifact:** `data/phoenix/Vini_treasury_transactions.json`
- **SHA-256:** `3bf431b01fae5d5b9361a1d2150d2d588f47eb1d0d8642c472ab6a2e94f506fa`
- **Artifact timestamp (UTC):** 2026-10-26T15:40:21.694971+00:00
- **Sidecar generated (UTC):** 2026-10-26T16:04:44.093997+00:00
- **Classification:** Primary source response
- **Acquisition / transformation:** Read-only HTTP GET; response body preserved without intentional modification.

## Immediate source(s)

- https://terra2.tdrsys.com/cosmos/tx/v1beta1/txs?query=message.sender='terra18ruqkccl5tp493uhvra0u6jylrzq8t8dv5qs4c'&limit=100&page=1&order_by=ORDER_BY_ASC

## Upstream original source(s)

- https://terra2.tdrsys.com/cosmos/tx/v1beta1/txs?query=message.sender='terra18ruqkccl5tp493uhvra0u6jylrzq8t8dv5qs4c'&limit=100&page=1&order_by=ORDER_BY_ASC

## Scope, limits, and notes

Account transaction query capped at 100; Treasury/OTC entries were subsequently filtered.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
