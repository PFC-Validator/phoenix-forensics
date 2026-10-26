# Source and provenance

- **Artifact:** `data/governance_4853/scenario.json`
- **SHA-256:** `53e8e38a46d6e3629183001249951ea58a8e0e55182be423f7a6636285b14116`
- **Artifact timestamp (UTC):** 2026-10-26T19:03:09.682997+00:00
- **Sidecar generated (UTC):** 2026-10-26T19:09:26.023477+00:00
- **Classification:** Derived dataset
- **Acquisition / transformation:** Local transformation using `Full-hub-YES scenario recalculation`.
- **Transformation:** `Full-hub-YES scenario recalculation`

## Immediate source(s)

- data/governance_4853/live_tally.json
- data/native_4853/votes.json
- data/eris_multisig/hub_delegations.json

## Upstream original source(s)

- data/governance_4853/live_tally.json
- data/native_4853/votes.json
- data/eris_multisig/hub_delegations.json

## Scope, limits, and notes

Validator operator addresses converted to account addresses using the same Bech32 payload; each non-YES hub delegation moved mechanically to YES. Synthetic Alliance weight excluded.

This sidecar records provenance only. It does not independently validate every assertion in the artifact.
