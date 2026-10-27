# Supplemental transaction verification

Public records retrieved on 27 October 2026. This supplement extends the audit datasets without replacing the main report or its earlier evidence cutoff. The website includes selected findings and supporting records as a separately dated supplement.

## Coverage and verification strength

The allowlisted governance and financial leads supplied 54 distinct transaction locators. Successful execution records were captured for **48**: 38 Terra, four Neutron, one Archway, one Injective Cosmos, three Base and one Injective EVM. Six remain unavailable from the endpoints tried; that does not establish that the transactions do not exist.

For all **38 Terra transactions**, SHA-256 recomputed from the RPC's original encoded transaction bytes matches the cited hash; RPC block height and execution code also match the LCD response. The archive RPC and LCD may share infrastructure. This is not independent consensus or inclusion-proof verification. Other chains have provider execution records; EVM receipts have successful status, matching hashes, chain-ID checks and token-decimal calls.

The derived supplement contains **466 transfer rows**, **eight funded voting locks**, **seven redelegations**, and **23 bounded findings**. A finding may validate only part of a lead. Every finding retains its sources and limitations. Eight native transfer events with empty amount fields are preserved separately and never treated as zero.

## Material additions

| Record | What was checked | Governance relevance and boundary |
|---|---|---|
| Phoenix A43 | Execution created four permanent locks, IDs 429–432, funded with 20,750 ampLUNA each: **83,000 ampLUNA** total. Three recipient wallets supplied the passing **75/100 YES** weight. | Documents beneficiary participation in a voting-power award. TLA locks are distinct from native LUNA ballots. No breach or personal-profit finding. |
| Phoenix A33 | Execution created permanent locks 412–415, funded with **21,600.000001 ampLUNA** total. Proposal and ballot responses are retained. | Adds a publicly funded voting-power relationship; the full historical role and later ownership histories are separate checks. This is Phoenix A33, not Lion DAO A33. |
| Lock states | Current queries show fixed end periods for 429 and 432, and an additional 1 ampLUNA in 432 relative to creation. | Exact change transactions and compliance with award conditions remain unresolved. The current state does not establish a breach. |
| Ceres removal and rebalance | Removal at **9 October 2026, 03:09:55 UTC**; rebalance 40 seconds later. Seven redelegations total **1,680,127.496132 LUNA**, including **662,828.893153 LUNA** away from the removed validator. | Demonstrates actual allocation changes. No inference about retaliation or motive; hub staking and Alliance allocations remain separate. |
| Superbolt P35 | Four payments total **90,000 USDC**, split 45,000 + 15,000 + 15,000 + 15,000. Proposal and ballots show **three YES votes**, each from a recipient wallet. The IBC trace resolves to `uusdc`; six-decimal USDC units are explicit. | Beneficiary participation extends beyond Phoenix. No cross-chain personal-identity attribution. Project funding and onward distributions are stages of a flow, not additive receipts. |
| Receipt redemption | BURN_RECIPIENT assignment and four redemption legs producing **2,383.589113 ampLUNA** for the assigned address. Four gas fee-share payouts total **0.010660 LUNA**. | Establishes recoverable value and a distinct fee stream; it does not establish exclusive personal custody or complete intervening receipt history. |
| Restriction list | Assignment on **3 October, 02:21:42 UTC**, clearing on **18 October, 15:14:14 UTC**: **15 days, 12 hours, 52 minutes, 32 seconds** between the events. Both preceding migration transactions succeeded. | This supplement verifies configuration events, not a full intervening replay, all deployed binary checks or an actual failed withdrawal. |
| Creda reserves | Reserve-withdrawal executions collected multiple assets; their LUNA components were **5,701.254836** on 26 January and **2,679.750683** on 28 September 2026. | Realized protocol receipts, not personal profit. Other collected assets remain separate. No lifetime revenue estimate. |
| Votion fee samples | Two compounder transfers to the fee account: **0.981321 arbLUNA** and **0.272683 ampLUNA**. | Receipt tokens retain their own units. Gas fee sharing is separate. The proposed longer fee history remains unverified. |
| Milestone receipts | **10,000 USDC** analytics receipt and **45,000 USDC** Estima kickoff receipt. | Payment is established; missing delivery, adequate acceptance and later use are separate questions. Other directors approved Estima's original grant, as documented in the existing report. |
| Liquidity custody | Withdrawal credited **324,177.631924 USDC** and **2,662,226.103195 ampLUNA** to the deployment DAO, rather than the executor. | Prevents incorrectly treating the executor's transaction as personal income. |
| Permission changes | FEE_COLLECTOR assignment, PDT_CONFIG_OWNER assignment, arbLUNA collateral addition, and two migration-admin transfers are captured. Current Treasury, escrow, hub and Creda permission responses are stored separately. | Distinguishes migration administration, internal ownership, vote operator and reserve controller. The previous PDT_CONFIG_OWNER value is not established by the assignment alone. |
| Large unattributed account | Three transfer examples checked. The 32,928-LUNA receipt is timestamped **19 October 2026, 02:24:24 UTC**. | Corrects the UTC date of this example for subsequent analysis; the claimed 26-payment/303,490-LUNA history and the wallet controller remain unverified. |

The existing report's A272 finding is unchanged: the proposal failed. Neither these transfers nor voting agreement or timing establishes coordinated motive. Use `0xphilipp` for authored references; personal-identity, company-history and cross-account identification research was excluded from the imported lead inventory. Public transaction data retain relevant original labels without adopting them as identity findings.

## Open checks

- **Six transaction records unavailable:** four Ethereum transactions from leads 44–45, one Axelar transaction and one Cosmos Hub transaction from lead 44. Exact hashes, attempted endpoints and failures are in `data/leads/capture_manifest.json`.
- **Historical state snapshots not established:** 14 requested state queries did not return headers confirming the requested block heights. Successful unpinned queries are explicitly current records and cannot reproduce the claimed historical snapshots. One obsolete Neutron trace route also failed; the replacement denomination route succeeded and its trace hash was checked.
- **Cross-chain linkage remains partial:** the Terra swap/IBC transaction, Injective EVM receipt and Base receipts were captured. Full IBC acknowledgement and CCTP message/nonce matching was not completed. No exchange-customer, fiat cash-out or personal-use conclusion is made.
- **Full histories remain open:** cumulative fees, all lock changes/rewards, grant-to-delivery acceptance, historical validator eligibility and Alliance allocation continuity, and legal-fund voting capabilities are not established by the transaction samples.
- **Overlap is explicit:** previously captured milestone, validator-payment and handover examples are not added again to existing totals. The supplement is a separate ledger keyed by chain and transaction hash. Earlier snapshots remain intact.

## Datasets and reproduction

- `data/leads/verified_findings.json`: structured facts, source files and limits.
- `data/leads/lead_status.json`: disposition for each lead 1–59; no global narrative-verification flag.
- `data/leads/transactions/`, `queries/`, `rpc/`: exact response bodies with acquisition logs and provenance sidecars.
- `data/leads/transfers.json` and `transfers.csv`: event-level native, CW20 and ERC20 movements with raw amounts and supported display units. A movement is not automatically income.
- `data/leads/voting_locks.json`, `redelegations.json`, `fee_share_annotations.json`, `unquantified_transfer_events.json`: separate evidence types. Fee annotations are not added again to bank transfers.
- `data/leads/SHA256SUMS`: supplemental artifact checksums, excluding the manifest itself and provenance sidecars. The earlier integrity manifests are preserved.

Offline derivation and verification:

```sh
python3 analysis/integrate_lead_evidence.py
python3 analysis/generate_provenance.py
python3 analysis/verify_lead_evidence.py
python3 analysis/verify_provenance.py
```

Explicit network capture commands (successful captures are reused):

```sh
python3 analysis/collect_lead_transactions.py
python3 analysis/collect_lead_queries.py
python3 analysis/crosscheck_lead_transactions.py
```

Run offline derivation and provenance again after any capture changes. The website build copies these research datasets into `dist/record/audit/leads/` and presents selected findings with their stated limits. Building does not publish the live site.
