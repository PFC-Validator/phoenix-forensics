# Source and provenance

- **Artifact:** `data/phoenix/MB_current_treasury_transactions.json`
- **SHA-256:** `d407acddf52f2b0318144c648b5c271899567a3c25060401a06328ef75c88457`
- **Artifact timestamp (UTC):** 2026-10-26T15:40:21.045033+00:00
- **Classification:** Primary source response
- **Acquisition / transformation:** Read-only HTTP GET; response body preserved without intentional modification.

## Immediate source(s)

- https://terra2.tdrsys.com/cosmos/tx/v1beta1/txs?query=message.sender='terra1vv9zaygt7csc4wnufwk4snq2jle2sdh73vml73'&limit=100&page=1&order_by=ORDER_BY_ASC

## Upstream original source(s)

- https://terra2.tdrsys.com/cosmos/tx/v1beta1/txs?query=message.sender='terra1vv9zaygt7csc4wnufwk4snq2jle2sdh73vml73'&limit=100&page=1&order_by=ORDER_BY_ASC

## Scope, limits, and notes

Account transaction query capped at 100; Treasury/OTC entries were subsequently filtered. truncated window: 100 saved of 161 reported responses; 61 missing. Do not use this file alone for lifetime totals, cross-wallet comparisons, or absence claims.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
