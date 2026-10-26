# Source and provenance

- **Artifact:** `data/phoenix/Rose_treasury_transactions.json`
- **SHA-256:** `62febea68f8c777d02ad5c7c835b976b960cec88451fed8a7c1d06b4a3b09041`
- **Artifact timestamp (UTC):** 2026-10-26T15:40:22.029175+00:00
- **Classification:** Primary source response
- **Acquisition / transformation:** Read-only HTTP GET; response body preserved without intentional modification.

## Immediate source(s)

- https://terra2.tdrsys.com/cosmos/tx/v1beta1/txs?query=message.sender='terra14p3mc04s7jcaxvvetlzehvhx9gdx6w4nm3zzw3'&limit=100&page=1&order_by=ORDER_BY_ASC

## Upstream original source(s)

- https://terra2.tdrsys.com/cosmos/tx/v1beta1/txs?query=message.sender='terra14p3mc04s7jcaxvvetlzehvhx9gdx6w4nm3zzw3'&limit=100&page=1&order_by=ORDER_BY_ASC

## Scope, limits, and notes

Account transaction query capped at 100; Treasury/OTC entries were subsequently filtered. truncated window: 100 saved of 171 reported responses; 71 missing. Do not use this file alone for lifetime totals, cross-wallet comparisons, or absence claims.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
