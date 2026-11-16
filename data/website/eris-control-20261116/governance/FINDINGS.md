# Native Terra governance recovery — 16 November 2026

Two independent public REST endpoints report Terra v2.22.0, core commit `e68dd029990a4cf347157f2426cabba4d9eb5c30`, wasmd v0.54.10 and Cosmos SDK v0.50.15-terra.0. The inspected pinned application configures Wasm authority as the governance-module address and forwards the relevant messages unchanged to Wasmd. Raw source, version responses and acquisition hashes are retained here. This is source analysis tied to reported live versions, not a byte-matched audit of all running validators or a transaction simulation.

## Available mechanisms

- `MsgUpdateAdmin`, governance-module sender: reassigns the chain-level migration administrator without the existing administrator's consent. It does not change contract-internal owners or role registries.
- `MsgMigrateContract`, governance-module sender: adopts replacement code; a reviewed migration can repair internal ownership/roles and preserve existing balances/state. Requires exact storage compatibility, uploaded code, suitable IBC callbacks where applicable and successful execution.
- `MsgSudoContract`, governance-module authority: invokes the current binary's actual sudo entrypoint. It does not generically impersonate an owner or rewrite arbitrary storage.
- `MsgExecuteContract`: preserves ordinary sender and application authorization. Native governance messages must have the governance account as their sole signer. The pinned legacy router registers gov and Alliance, not a legacy Wasm arbitrary-sender route.
- Alliance governance can alter Treasury funding, but changes to inflows are distinct from custody or recovery of assets already paid.

The reviewed `GovAuthorizationPolicy.CanModifyContract` returns true even without a current administrator. Thus clearing a contract admin does not remove this governance recovery route.

## Deployed bytecode check

Downloaded code 3347 (Treasury) and 2726 (hub) hashes match their LCD code metadata. Parsing their actual Wasm export tables finds no `sudo` function. Direct sudo proposals therefore cannot operate these current deployments. This does not prevent a separate governance migration. No claim is made that every other reviewed contract lacks sudo.

`verification.json` records the binaries' hashes, exports, node-reported dependencies and exact source URLs. `collect.py` performs read-only retrieval and export parsing. It submits no transactions.

## Practical limit

A text-only vote does not change contracts. Administrator-only changes leave internal permissions active. Exact executable proposal messages require fork testing and post-execution role checks; proposal acceptance is not proof that execution will succeed. Existing keys can act before execution, and contract recovery cannot automatically reverse external transfers, produce missing source/credentials, establish legal title or certify deliverables.
