# Source and provenance

- **Artifact:** `data/governance_4853/refresh_20261027/votes.csv`
- **SHA-256:** `01de36cea4dd31b4cb7c1bcc38b9fde0aaa9ecbadd87dc2ca7426d69285ec158`
- **Timestamp basis:** No original acquisition timestamp established; file mtime is not used as acquisition evidence.
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/refresh_4853.py`.
- **Transformation:** `analysis/refresh_4853.py`

## Immediate source(s)

- data/governance_4853/refresh_20261027/block_before.json
- data/governance_4853/refresh_20261027/proposal.json
- data/governance_4853/refresh_20261027/tally.json
- data/governance_4853/refresh_20261027/votes.json
- data/governance_4853/refresh_20261027/hub_delegations.json
- data/governance_4853/refresh_20261027/validators.json
- data/governance_4853/refresh_20261027/parameters.json
- data/governance_4853/refresh_20261027/pool.json
- data/governance_4853/refresh_20261027/active_gauge.json
- data/governance_4853/refresh_20261027/block_after.json

## Upstream original source(s)

- data/governance_4853/refresh_20261027/block_before.json
- data/governance_4853/refresh_20261027/proposal.json
- data/governance_4853/refresh_20261027/tally.json
- data/governance_4853/refresh_20261027/votes.json
- data/governance_4853/refresh_20261027/hub_delegations.json
- data/governance_4853/refresh_20261027/validators.json
- data/governance_4853/refresh_20261027/parameters.json
- data/governance_4853/refresh_20261027/pool.json
- data/governance_4853/refresh_20261027/active_gauge.json
- data/governance_4853/refresh_20261027/block_after.json

## Scope, limits, and notes

New dated snapshot; earlier 26 October evidence retained. Decimal arithmetic; Bech32 operator payload re-encoded for account ballots; bonded delegations only; hypothetical full-hub YES, excluding synthetic Alliance weight.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
