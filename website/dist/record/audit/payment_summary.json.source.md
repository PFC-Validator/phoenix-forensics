# Source and provenance

- **Artifact:** `data/payment_summary.json`
- **SHA-256:** `04157614c7a17b7c121b2d505abdc9ed4b2965376131b68016ad3d0af62fa735`
- **Artifact timestamp (UTC):** 2026-10-26T14:53:34.248715+00:00
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/payment_summary.py`.
- **Transformation:** `analysis/payment_summary.py`

## Immediate source(s)

- data/transfers/to_eris_all_transfers.json
- data/treasury/outbound_transfers.json
- data/treasury/actions/
- data/counterparties/ve3_bribe_manager_flows.json

## Upstream original source(s)

- data/transfers/to_eris_all_transfers.json
- data/treasury/outbound_transfers.json
- data/treasury/actions/
- data/counterparties/ve3_bribe_manager_flows.json

## Scope, limits, and notes

Summarizes monthly validator transfers, signer OTC flows, and action rosters; no new external data.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
