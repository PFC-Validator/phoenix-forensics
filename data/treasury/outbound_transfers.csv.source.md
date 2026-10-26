# Source and provenance

- **Artifact:** `data/treasury/outbound_transfers.csv`
- **SHA-256:** `bfe2313985c93f6a803d14bd899274223861f707b1e66e9fc47149656d58ba12`
- **Artifact timestamp (UTC):** 2026-10-26T14:39:36.551951+00:00
- **Sidecar generated (UTC):** 2026-10-26T16:04:44.133694+00:00
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/treasury_patterns.py`.
- **Transformation:** `analysis/treasury_patterns.py`

## Immediate source(s)

- data/treasury/outbound_all_tx_responses.json

## Upstream original source(s)

- data/treasury/outbound_all_tx_responses.json

## Scope, limits, and notes

Only transfer events whose sender is the Phoenix Treasury; amount/denom decoded.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
