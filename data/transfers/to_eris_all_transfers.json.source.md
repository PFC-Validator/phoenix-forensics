# Source and provenance

- **Artifact:** `data/transfers/to_eris_all_transfers.json`
- **SHA-256:** `6894d3f6b8ed2ce624a1242bb3261e7aa8a28acfc68b0e85b0e5ada319d67eb5`
- **Artifact timestamp (UTC):** 2026-10-26T14:40:34.993089+00:00
- **Sidecar generated (UTC):** 2026-10-26T15:34:56.410530+00:00
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/eris_incoming_patterns.py`.
- **Transformation:** `analysis/eris_incoming_patterns.py`

## Immediate source(s)

- data/transfers/to_eris_all_tx_responses.json

## Upstream original source(s)

- data/transfers/to_eris_all_tx_responses.json

## Scope, limits, and notes

Transfer events filtered to the ERIS recipient; decodes amount and denom.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
