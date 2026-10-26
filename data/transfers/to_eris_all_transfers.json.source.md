# Source and provenance

- **Artifact:** `data/transfers/to_eris_all_transfers.json`
- **SHA-256:** `2d5b6381b579a676f3d879148b60449d7418566a55f97272d61fc59f07c50fc2`
- **Artifact timestamp (UTC):** 2026-10-26T14:40:34.993089+00:00
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
