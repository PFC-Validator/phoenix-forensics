# Source and provenance

- **Artifact:** `data/phoenix/MB_prior_treasury_transactions.json`
- **SHA-256:** `fbf97e1626256ec9234211acca5322180c0db2bbb3be363381045a89b263e771`
- **Artifact timestamp (UTC):** 2026-10-26T15:40:21.220828+00:00
- **Sidecar generated (UTC):** 2026-10-26T16:04:44.088394+00:00
- **Classification:** Primary source response
- **Acquisition / transformation:** Read-only HTTP GET; response body preserved without intentional modification.

## Immediate source(s)

- https://terra2.tdrsys.com/cosmos/tx/v1beta1/txs?query=message.sender='terra15vwmgac9tlcgkrkjn4rq3r0md003ufsqp64vaw'&limit=100&page=1&order_by=ORDER_BY_ASC

## Upstream original source(s)

- https://terra2.tdrsys.com/cosmos/tx/v1beta1/txs?query=message.sender='terra15vwmgac9tlcgkrkjn4rq3r0md003ufsqp64vaw'&limit=100&page=1&order_by=ORDER_BY_ASC

## Scope, limits, and notes

Account transaction query capped at 100; Treasury/OTC entries were subsequently filtered.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
