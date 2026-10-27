# Source and provenance

- **Artifact:** `data/ampluna/governance_backing_analysis.json`
- **SHA-256:** `0e1c845933d08e3206a322ef022bf5dd8ad0ecfc0f36ee943e3a365a1acbd88d`
- **Timestamp basis:** No original acquisition timestamp established; file mtime is not used as acquisition evidence.
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/ampluna_backing.py`.
- **Transformation:** `analysis/ampluna_backing.py`

## Immediate source(s)

- data/ampluna/hub_state.json
- data/ampluna/holder_top40.json
- data/ampluna/top20_accounts.json
- data/ampluna/pol_multisig.json
- data/ampluna/direct_hub_bonds.json
- data/governance_4853/vamp_review.json

## Upstream original source(s)

- data/ampluna/hub_state.json
- data/ampluna/holder_top40.json
- data/ampluna/top20_accounts.json
- data/ampluna/pol_multisig.json
- data/ampluna/direct_hub_bonds.json
- data/governance_4853/vamp_review.json

## Scope, limits, and notes

Separates confirmed backing and holder facts from the explicit 30M scenario and actual voting action.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
