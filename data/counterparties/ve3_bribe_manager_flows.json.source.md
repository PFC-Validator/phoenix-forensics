# Source and provenance

- **Artifact:** `data/counterparties/ve3_bribe_manager_flows.json`
- **SHA-256:** `7dfd299b6eb985432126d51ff71d82d5d0fad020c3ede3784a52fbf8297512c0`
- **Timestamp basis:** No original acquisition timestamp established; file mtime is not used as acquisition evidence.
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/counterparty_flows.py`.
- **Transformation:** `analysis/counterparty_flows.py`

## Immediate source(s)

- data/transfers/to_eris_all_transfers.json
- data/transfers/to_eris_all_tx_responses.json
- data/counterparties/ve3_bribe_manager_contract.json

## Upstream original source(s)

- data/transfers/to_eris_all_transfers.json
- data/transfers/to_eris_all_tx_responses.json
- data/counterparties/ve3_bribe_manager_contract.json

## Scope, limits, and notes

Separates LUNA, FUEL and USDC voting-incentive receipts and verifies claim_bribes messages; no combined cross-asset total.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
