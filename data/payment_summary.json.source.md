# Source and provenance

- **Artifact:** `data/payment_summary.json`
- **SHA-256:** `e907b1dfe443fe2c14feb896cd6a56e67c9672f5d1eb6ab04818a44ebf9dd15d`
- **Artifact timestamp (UTC):** 2026-10-26T14:53:34.248715+00:00
- **Sidecar generated (UTC):** 2026-10-26T16:04:44.082242+00:00
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/generate_provenance.py and earlier payment-summary script`.
- **Transformation:** `analysis/generate_provenance.py and earlier payment-summary script`

## Immediate source(s)

- data/transfers/to_eris_all_transfers.json
- data/treasury/outbound_transfers.json
- data/treasury/actions/

## Upstream original source(s)

- data/transfers/to_eris_all_transfers.json
- data/treasury/outbound_transfers.json
- data/treasury/actions/

## Scope, limits, and notes

Summarizes monthly validator transfers, signer OTC flows, and action rosters; no new external data.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
