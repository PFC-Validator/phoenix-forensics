# Source and provenance

- **Artifact:** `data/treasury/outbound_transfers.json`
- **SHA-256:** `3987f287cdd746cda91b4ac91b41b9757356778d4a3d2d6e3c40527b6a81a52b`
- **Artifact timestamp (UTC):** 2026-10-26T14:39:36.552581+00:00
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
