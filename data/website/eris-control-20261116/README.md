# ERIS contracts and community assets — 16 November 2026

This bounded review compares 27 named Terra contracts, approved and rejected funding/launch decisions, and public handover statements. It does not establish all ERIS deployments, legal asset ownership, private key custody, private agreements, complete revenue-sharing compliance, or abusive intent.

- `chain/`: sequential latest-state queries, full contract inventory, UTC acquisition URLs/status/hashes, and read-only reproduction scripts. Main bracket heights 23,779,539–23,779,552; later vault/gauge checks have their own manifest. Queries are not pinned to a common height. One unsuccessful CW20 `config` query is retained; its minter query identifies the actual arb vault.
- `approvals/`: native governance and Board decisions plus publisher archives; FINDINGS.md distinguishes awards, release approvals, rejected requests and terms not established.
- `handover/`: P9/A292 and hub history, scoped public-response summaries and research notes. Whole forum threads were reviewed locally but excluded from versioned evidence; original retrieval records and hashes remain. This is deliberate curation, not a claim those summaries are raw responses.
- `technical/`: upstream migration implementation and the published Treasury audit. These do not establish a reproducible build match for the live Treasury or a complete security audit.

The public subset is maintained in `website/source-records/control-20261116/`, then copied to `website/dist/record/control-20261116/`. All public assertions are bounded by the evidence page. Grants and contract balances are not equated with personal profit or legal ownership. TLA’s one-/three-month deadlines are not silently extended to Treasury or every ERIS product.

## Principal result

The named ERIS upgrade address remains administrator of the Treasury and reviewed TLA/Creda components. ERIS’s configuration address owns the TLA and Creda registries. The Board is the ordinary Treasury controller and holds upgrade administration of the hub/bridge after P9; A292 is now executed. Upgrade authority can replace in-contract spending/veto rules, creating conditional asset-loss and operational risks. No destructive action or misuse is asserted or tested.
