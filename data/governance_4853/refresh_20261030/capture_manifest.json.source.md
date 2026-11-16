# Source and provenance

- **Artifact:** `data/governance_4853/refresh_20261030/capture_manifest.json`
- **SHA-256:** `871f9e0bce74817340072442e1c8bafcd064db4946579816b3cc91320449a78c`
- **Timestamp basis:** No original acquisition timestamp established; file mtime is not used as acquisition evidence.
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `analysis/refresh_4853.py`.
- **Transformation:** `analysis/refresh_4853.py`

## Immediate source(s)

- data/governance_4853/refresh_20261030/block_before.json
- data/governance_4853/refresh_20261030/proposal.json
- data/governance_4853/refresh_20261030/tally.json
- data/governance_4853/refresh_20261030/votes.json
- data/governance_4853/refresh_20261030/hub_delegations.json
- data/governance_4853/refresh_20261030/validators.json
- data/governance_4853/refresh_20261030/parameters.json
- data/governance_4853/refresh_20261030/pool.json
- data/governance_4853/refresh_20261030/active_gauge.json
- data/governance_4853/refresh_20261030/block_after.json

## Upstream original source(s)

- data/governance_4853/refresh_20261030/block_before.json
- data/governance_4853/refresh_20261030/proposal.json
- data/governance_4853/refresh_20261030/tally.json
- data/governance_4853/refresh_20261030/votes.json
- data/governance_4853/refresh_20261030/hub_delegations.json
- data/governance_4853/refresh_20261030/validators.json
- data/governance_4853/refresh_20261030/parameters.json
- data/governance_4853/refresh_20261030/pool.json
- data/governance_4853/refresh_20261030/active_gauge.json
- data/governance_4853/refresh_20261030/block_after.json

## Scope, limits, and notes

New dated snapshot; earlier 26 October evidence retained. Decimal arithmetic; Bech32 operator payload re-encoded for account ballots; bonded delegations only; hypothetical full-hub YES replaces the existing hub ballot where present, otherwise inherited validator options; excludes synthetic Alliance weight.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
