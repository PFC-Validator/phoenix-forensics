# Governance authorizations and limits — 16 November 2026

This is a focused comparison of retained and newly retrieved primary proposal records. It is not a complete audit of every ERIS contract or grant, and it does not establish legal ownership of software, user deposits, or Treasury assets. A contract field named `owner` is a technical permission, not proof of legal title. No claim of improper intent follows from the presence of an admin key.

## Decisions verified on chain

| Decision | Result / what was authorized | Limits relevant to the website |
| --- | --- | --- |
| Native 3460, original ERIS grant | Rejected. Requested 450,000 LUNA, described as $720,000. | Do not count as awarded funding. |
| Native 3796, revised ERIS grant | Passed. 312,500 LUNA, described as $500,000: audits $100k, marketing $35k, infrastructure $15k, salaries $350k. Community multisig; 50% initially, remaining 50% vested over ten months after milestones. Milestones: Amp Governance, Arb Repeater, Warp integration. | Development funding does not establish that the community bought all ERIS software/IP, or that ERIS gained beneficial ownership of user deposits. Linked forum text has revenue-sharing and decentralization commitments, below. |
| Native 4813, TLA development | Passed. 384,615 LUNA, described as $200k development plus $50k auditing. | Follow-on launch terms explicitly limit initial ERIS control; no perpetual control entitlement identified in the reviewed proposal. |
| Native 4816, Phoenix Directive formation | Passed. 243,902 LUNA, described as $100k: $60k BORG legal framework; $40k infrastructure, Treasury contract development/audit and volatility buffer. Summary calls BORG services public goods for Terra. | Does not convey Treasury assets to ERIS. Do not claim all $100k went to ERIS. |
| Native 4817, TLA launch | Passed. Creates the stable/project/bluechip Alliance assets. Explicitly links forum launch discussion 24385 for full terms. | The linked launch text publishes one-month migration-admin and three-month configuration-owner handovers. It is the strongest explicit dated commitment. |
| Native 4822, Treasury launch | Passed. Creates Treasury virtual-token Alliance with reward weight 14%; summary describes allocating 10% of chain staking rewards to Phoenix Directive. | Linked launch text promises audited OSS, spending vetoes, governance defunding and clawback. Do not extend the TLA's specific one/three-month deadlines to Treasury as though the Treasury document independently states them. |
| Native 4823, Alliance reform | Passed. Establishes single-asset Alliance and adjusts other assets. | Funding/alliance design, not a found transfer of Treasury title to ERIS. |
| Native 4830, decentralize TLA pool whitelisting | Rejected. Sought collective-governance whitelisting/de-whitelisting and restoration of SWTH-rSWTH. | Important counterevidence: this was not an adopted new mandate. Its rejection does not by itself repeal the earlier migration/configuration handover promises. |
| Native 4836, TLA pool relocation | Rejected. Summary proposes relocation of non-LUNA pools and selected LUNA pools. | Not an adopted mandate. Pool policy changes are distinct from contract ownership/migration authority. |
| Board A107, Votion grant | Executed. 50,000 USDC in two 25,000 milestones. | Funding action contains no explicit IP assignment or perpetual control entitlement. |
| Board A189 / A190, Creda grant | A189 rejected; corrected A190 executed. A190 sets 210,000 USDC: 40k kickoff, 100k mainnet, 60k eMode/isolation, 10k analytics. | One corrected award, not two grants. Proposal description is a period; executable message is milestone funding, not an IP/control contract. |
| Board A209 / A215, Creda release | Executed. A209 enables first three milestones (200k); A215 enables analytics (10k). | Milestone release is not independent technical acceptance, and neither action transfers migration or registry ownership. |
| Board A258 / A266, Estima | A258 rejected; A266 executed. A266 funds 125,000 USDC: 45k kickoff, 45k mainnet, 35k analytics/TLA integration. | A258's 150k proposed scope is not an additional approved award. Other directors approved A266 without a recorded 0xPhilipp vote; retain that counterevidence. |
| Board A271, Estima kickoff | Executed; enables 45,000-USDC first milestone. | Approval does not establish the remaining 80,000 USDC was paid. Retained payment record shows 45k paid; fresh Treasury action state was not queried in this subtask. |

Native originals: `https://terra-phoenix-api.highstakes.ch/cosmos/gov/v1/proposals/{ID}`. Board public URLs: `https://dao.phoenix.money/dao/terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg/proposals/A{ID}`. Exact smart-query URLs and SHA-256 digests are in `board-manifest.json`. Native and archive source URLs, UTC acquisition timestamps and hashes are in `capture-manifest.json` and `supplement-manifest.json`. Some initial native requests returned 429; successful retries are recorded in the supplement manifest.

## Published commitments and their scope

### Revised ERIS grant, discussion 8789 (2023)

Original: https://common.xyz/terra/discussion/8789-revised-eris-grant-proposal

Primary publisher archive: `2023-01-02_8789_revised-eris-grant-proposal.md`, retrieved from the Phoenix documentation repository at the tree SHA recorded in the manifest.

- Lines 85–95 and 145–147 promise 10% of ERIS protocol revenues on Terra/feather chains for the community pool. They contemplate replacement with a 10% total-supply airdrop if ERIS introduces a revenue-capturing token. Revenue reconciliation, what contracts are in scope, whether repayment has been fulfilled, and any superseding approved terms are unanswered in this pass.
- Lines 106–119 place full open source including bots, Enterprise management, Warp execution and four-year maintenance in an answer about running out of cash. The text says these are included in funding, but frames the list as the fallback if all else fails. Do not turn it into an unconditional dated code handover promise.
- Lines 129–143 describe intended progressive decentralization and possible future community protocol ownership. This does not itself prove completed ownership transfer.
- Lines 149–151 let community multisig holders return unspent funding if milestones do not make significant progress; this is a grant-funding control, not general confiscation of user assets.

### TLA development, discussion 20123 (May 2024)

Original: https://common.xyz/terra/discussion/20123-terra-liquidity-alliance

Archive: `2024-05-28_20123_terra-liquidity-alliance.md`.

- Lines 94 and 134 describe the Community Pool acquiring LP positions through take rates: chain-owned liquidity, not ERIS-owned LP assets.
- Lines 115–116 and 134 describe Terra governance determining the take rate. The later launch text assigns take-rate changes to Phoenix Stewardship; describe this chronology, not an unexplained single permanent rule.
- Line 127 promises a 20% grant refund if URA cannot agree a valid takeover/development plan. Whether this condition arose or a refund occurred has not been established; do not allege default.
- Lines 155–165 identify funding and ERIS as implementation partner. No reviewed text expressly conveys permanent technical control or legal ownership of community assets to ERIS.

### TLA launch, discussion 24385 (August 2024)

Original: https://common.xyz/terra/discussion/24385-launching-terra-liquidity-alliance

Archive: `2024-08-12_24385_launching-terra-liquidity-alliance.md`.

- Lines 144–145 explicitly distinguish migration administrator from configuration owner.
- Lines 168–169 identify ERIS configuration address `terra1kefa2zgjn45ctj32d3tje5jdwus7px6n2klgzl` and ERIS administrator `terra1q0vny4wx2pfteh9zq323wh48c654xacpfq5tew`, promising transfers to PD Stewardship after three months and one month respectively.
- These are TLA launch promises. Current state and partial transfers must be checked separately; an operational-controller assignment is not the same as migration-admin or registry ownership handover.

### Treasury launch, discussion 25020 (September/October 2024)

Original: https://common.xyz/terra/discussion/25020-phoenix-directive-launching-treasury

Archive: `2024-09-26_25020_phoenix-directive-launching-treasury.md`.

- Calls Treasury an audited OSS smart contract; describes 3-day Think Tank veto for >$50k and 10-day governance veto for >$150k; says governance can stop Alliance funding and claw back locked Treasury funds.
- The author’s October 2 comment states rolling 30-day veto thresholds ($150k / $450k), and veto after a lock only for amounts recipients have not claimed.
- These governance promises make upgrade authority material: a retained key able to replace code is a different control layer from ordinary spending votes and in-code veto protections.
- The document does not contain its own one-/three-month transfer timetable. Apply the timetable directly to TLA, and ask separately why Treasury shares the retained administrator and registry, on what authority, and with what safeguards.

## What is supported, and what still needs disclosure

Supported: community-approved development and funding; explicit temporary TLA admin/owner allocation; governance and Board roles; successful and rejected decisions with amounts. Not established: all ERIS contracts on Terra, ERIS legal ownership of each asset/software component, complete fee/revenue-sharing compliance, all grant agreements or side letters, exhaustive later governance decisions, every source/license obligation, or any abusive use of retained keys.

Recommended framing: “What does ERIS control, what does the community own, and what was actually authorized?” Ask for a complete contract and asset register mapping each migration administrator, configuration owner, operating controller, fee recipient, funding source, applicable approved terms, and completed transfer transaction. Separate legal ownership, custody of depositor assets, and permission to upgrade contracts.
