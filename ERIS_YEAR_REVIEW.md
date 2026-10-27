# ERIS 2025–2026 review: funding and claim checks

Reviewed 27 October 2026 against the [ERIS article](https://medium.com/@eris_protocol/eris-protocol-a-year-in-review-2025-2026-2973e303bed0), primary Treasury action queries, current Creda metrics and public-contract positions, the prior verified transaction supplement, funder reporting and incident-response documentation. This is a bounded review, not a complete audit of every delivery or security claim. No website publication is implied.

## Assessment

The article describes identifiable products and operational work, but does not supply a funding reconciliation or enough evidence for several strong quantitative and attribution claims. Substantial Phoenix support is documented. Funding an achievement does not negate the work; it changes how holders should understand its cost, sponsorship and independence. There is no sound percentage assigning all achievements to Treasury versus external sources.

## Funding attributable to named projects

| Work | Phoenix Treasury support | External evidence | Scope qualification |
|---|---:|---|---|
| Creda | **210,000 USDC**, action 72; four milestones marked claimed | No additional external grant verified for Creda in this review | 40,000 kickoff + 100,000 launch + 60,000 eMode/isolation + 10,000 analytics. Funding does not establish acceptance quality or net profit. |
| Votion | **50,000 USDC**, action 28; both milestones marked claimed | AADAO reports **$50,000 paid** for the Hydro vote aggregator, with jointly verified completion | The Phoenix award began in February 2025, before the article's October 2025–October 2026 period. Hydro work is a separate scope; two awards alone do not establish duplicate billing. |
| USDC migration application | **5,000 USDC**, action 109, named application funding; completed action with no open payments | No separate external development funding verified here | Earlier transaction review also records the application payment. |
| USDC migration liquidity | **100,000 USDC**, action 110, completed allocation to the liquidity/operations DAO | No separate external capital contribution verified here | This is liquidity capital, not another 100,000 of developer compensation. The article itself acknowledges Foundation seeding. |
| Public apps, maintenance and security operations | Recurring Stewardship compensation and potentially other operating budgets | Protocol fees and validator receipts exist, but their allocation to these tasks is not established | The prior completed Treasury capture records ten 8,640-USDC receipts in January–October 2026. No timesheets or project cost allocation establish how much supported each listed task. |

The identified direct project grants total **265,000 USDC** across Creda, Votion and the migration application. Excluding the earlier Votion award, **215,000 USDC** relates to the two grants initiated within the review period. The separate external Votion award is funder-reported; this review did not replay its settlement transactions. These figures are neither a complete ERIS budget nor a causal split of the year's achievements. Do not add liquidity deployments, payroll, deposits and grants as one expense total.

Treasury actions were freshly re-queried: [28](https://terra2.tdrsys.com/cosmwasm/wasm/v1/contract/terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5/smart/eyJhY3Rpb24iOnsiaWQiOjI4fX0=), [72](https://terra2.tdrsys.com/cosmwasm/wasm/v1/contract/terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5/smart/eyJhY3Rpb24iOnsiaWQiOjcyfX0=), [109](https://terra2.tdrsys.com/cosmwasm/wasm/v1/contract/terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5/smart/eyJhY3Rpb24iOnsiaWQiOjEwOX19), [110](https://terra2.tdrsys.com/cosmwasm/wasm/v1/contract/terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5/smart/eyJhY3Rpb24iOnsiaWQiOjExMH19). External Votion payment and acceptance are [AADAO's reported findings](https://forum.cosmos.network/t/aadao-wind-down-oversight-updates-and-reports/15913/22).

## Creda size and funding concentration

The retained [current primary metrics query](https://terra2.tdrsys.com/cosmwasm/wasm/v1/contract/terra1y6hfmr3lxxj6srduhlfz96x7sga2984pr757a0nrfuqxa9rqxapqcjv4zz/smart/eyJtZXRyaWNzIjp7fX0=) reports about **$552,694 supplied**, **$130,637 borrowed** and **$425,717 designated collateral**. A separate read of the [Creda markets page](https://creda.finance/markets) displayed approximately $552.72K market size and $130.71K borrows. These sequential live reads are close, not identical snapshots.

These observations do not reproduce the article's current $1M TVL statement. Collateral is a designation of supplied balances, not an additional pool to add to supply; per-asset responses demonstrate the overlap. A different dated peak or TVL definition could explain the article's number, but it must be supplied and reconciled. The current comparison does not prove that Creda never reached $1M.

Sequential current portfolio queries identify roughly **$131,446** in the operations and board contracts combined, about **23.8%** of supply, and approximately **$100,406**, or **18.2%**, through the TLA single pool. Combined, these public-contract positions account for about **42%** of supplied value. Queries did not establish one common block height, so these are approximate contemporaneous comparisons. The operations DAO describes its purpose as holding LA locks and chain-owned liquidity.

The TLA position is pooled user capital and is not established as entirely Treasury-funded. The remaining approximately 58% is not proven to be independent external-user capital either. Positions demonstrate where deposits sit; their full funding origin and beneficial ownership require separate tracing.

Current LUNA utilization is approximately **73.85%**, with about **18.46% annual borrow rate**. This supports actual borrowing demand at the snapshot. It does not establish a year-long demand series, broad adoption, many independent borrowers or demand sufficient to justify all development spending.

## Other accuracy checks

| Claim area | Assessment |
|---|---|
| Products and applications | Creda and the migration tool are identifiable, with corresponding funding and execution evidence. The claimed exclusive authorship, launch date and operation of every listed application were not independently replayed. The six launches within the period are arithmetically consistent with the list; the August 2025 website contribution is outside that period and Insight is explicitly pending. |
| No bad debt and all positions healthy | Not independently established across every borrower and the full year. Current aggregate metrics or healthy oracle-price flags are insufficient to establish this historical claim. No contrary bad-debt finding is asserted here. |
| Sole remaining Cosmos money market | Too broad without defining the category and competitors. Nolus has current [Cosmos SDK lending documentation](https://docs.nolus.io/docs/protocol/lending/deposit-withdraw) and [mainnet infrastructure documentation](https://docs.nolus.io/network/rpc-endpoints); its lending model differs. The article does not establish ecosystem-wide exclusivity. |
| Approximately $10M saved by two contributors | Not independently substantiated as an attributed, dated dollar calculation. The [Cosmos Labs incident account](https://forum.cosmos.network/t/neutron-governance-attack-cosmos-hub-response-and-recovery-update/17369) documents collective response and recovery, including 1,227,121 ATOM moved to recovery custody after theft and some funds lost. It covers the Hub side only and does not disprove a contribution by ERIS elsewhere. Prevented theft, recovered assets, assets at risk and final restitution must be separated. |
| Station compromise and approximately 10M LUNA restricted | The full incident, restricted-address inventory and contributor-attribution chain were not independently replayed in this review. Restricted value is not automatically recovered or returned value. |
| All contracts audited | Public [SCV audit reports](https://github.com/SCV-Security/PublicReports/tree/main/Eris%20Protocol) exist for several ERIS components. This supports the existence of audits, not blanket coverage of every deployed 2026 revision. Auditor, scope, commit, deployed code checksum, outstanding issues and remediation must be matched. |
| Private source for security | The article provides a material first-party explanation for the previously noted source gap: intentional withholding is the stated rationale. That explanation should accompany the gap finding. It does not independently establish stronger security or let outsiders verify current code. |
| Depositor-oriented design | An evaluative statement, not an audited outcome. Creda's own [take-rate documentation](https://docs.creda.finance/concepts/take-rate) describes fees on supplied balances in addition to reserve factors on borrower interest. Assess net outcomes after fees and risk. |

## Evidence and limits

`data/leads/year_review_analysis.json` reproduces the action totals, current metric fields, public-contract position values and approximate shares. Its supporting exact responses are `data/leads/queries/review_*.json`, each with acquisition metadata and a provenance sidecar. `analysis/integrate_lead_evidence.py` regenerates the calculations offline. The external payment remains labelled funder-reported.

This review does not convert gross grants or protocol revenues into personal profit, identify unattributed wallet controllers, or attribute intent. The article does not claim that every contribution was unpaid or self-financed; its omission is a missing consolidated funding account. A more complete report would connect each achievement to its payer, grant scope, paid amount, capital allocation, deliverable, acceptance record and current outcome.
