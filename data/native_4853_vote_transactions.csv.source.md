# Source and provenance

- **Artifact:** `data/native_4853_vote_transactions.csv`
- **SHA-256:** `562b063a919acf31f9a52a823c90b35171b656c3e820a2c78917e57312485450`
- **Artifact timestamp (UTC):** 2026-10-26T14:19:35.276563+00:00
- **Sidecar generated (UTC):** 2026-10-26T16:04:44.085078+00:00
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/export_data.py`.
- **Transformation:** `analysis/export_data.py`

## Immediate source(s)

- data/native_4853/vote_transactions.json

## Upstream original source(s)

- data/native_4853/vote_transactions.json

## Scope, limits, and notes

Only vote messages exposed in structured transaction bodies; raw JSON retains all 87 responses.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
