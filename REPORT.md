# Phoenix Foundation governance review

**Evidence cutoff:** 26 October 2026, approximately 14:14 UTC  
**Timeline window:** 26 September–26 October 2026, with 22–23 September as immediate context  
**Privacy scope:** handles, roles, and public wallet/contract addresses only. No identity research or surname attribution is used in this report.

**Payment addendum:** see `PAYMENTS.md` for validator-to-ERIS recurring transfers, Treasury compensation, related-party OTC flows, and the October compensation-roster comparison.

## Executive assessment

The records support several **governance risks requiring explanation and remediation**, but they do not establish a single coordinated capture scheme.

1. **A272 was an actual concentration-of-power proposal, not merely a personnel vote.** Its two messages would have removed one of four equal board members and reduced the approval threshold from 75% to 60%, producing a 2-of-3 board. It failed with 50 YES, 25 NO, and the fourth member not voting. Calling the ballot itself “2–2” is inaccurate.
2. **The 4853 proposer has direct, disclosed-on-chain relationships with both ERIS and prior Foundation funding.** The proposer account is the ERIS validator account and the A266 grant recipient. It voted YES on its own proposal with approximately 8.6 million LUNA of voting power.
3. **ERIS-linked stake is material on both sides of 4853.** The ERIS hub delegates to major YES validators and to Smart Stake, the largest VETO validator. This is evidence of influence potential, not proof of coordinated voting or control.
4. **The published TLA handover remains incomplete.** The original 2024 text promised migration administration after one month and configuration ownership after three. Current queries still show the ERIS admin wallet on Treasury and the TLA registry, and the ERIS configuration wallet as registry owner. ERIS proposal 9 transferred two other admins to the Phoenix board on 25 October, but did not complete the wider handover.
5. **Beneficiary participation is a system-wide issue, not confined to one director.** A116, A159, A175, A209, A215, A249, and A271 each passed with exactly the minimum 75/100 YES weight and included a proposal author or beneficiary in the YES set. A266 deliberately did not include Philipp, while the subsequent A271 release did.
6. **ERIS multisig authority is concentrated by weight.** One signer holds 50 of 90 weight; that signer plus any two 10-weight signers reaches the 70-weight threshold. All recorded ballots across nine proposals are YES. Rejections resulted from missing ballots, not NO votes.
7. **Public source transparency has a material gap.** `contracts-tokenfactory` shows a latest commit dated 17 October 2024, while the preserved ledger records 2026 deployments adding incentive and wallet restrictions. I did not locate corresponding source in the public ERIS organization. This does not prove source is unavailable elsewhere.
8. **Forum governance events need process review.** A public revision identifies a participant editing another user's post and removing a quoted passage, without an edit reason. Guidelines were added 19 October. One reviewed account is currently suspended; two others have no current public suspension fields. These facts do not, alone, establish improper censorship.

**4853 was not passing at the captured tally.** It had quorum, but YES was only 43.66% of non-abstain votes. VETO was 29.91% of all votes, below the 33.4% veto threshold. The vote remains open until 31 October 2026 at 03:40:11 UTC.

## 1. Downloaded voting records

The `data/` directory contains fresh chain responses, preserved compiled records with original query/transaction locators, and CSV exports.

| Dataset | Coverage | Local record |
|---|---|---|
| Phoenix main board | A1–A289; every ballot, proposal status, timestamps and transaction locators | `data/mb_voting_record.json`, `data/phoenix_board_votes_all.csv` |
| Last-four-weeks board subset | 21 proposals, A269–A289 | `data/phoenix/recent_votes.json`, `data/phoenix_board_votes_last4weeks.csv` |
| Key board proposals | A116, A159, A175, A209, A215, A249, A266, A271, A272, with fresh payloads and ballots | `data/phoenix/key_proposals.json` |
| Terra 4853 | All 79 current ballots; 87 vote transactions; live proposal and tally | `data/native_4853/`, `data/native_4853_votes_all.csv`, `data/native_4853_vote_transactions.csv` |
| ERIS fixed multisig | All nine proposals, all ballots, five voters and 70/90 threshold | `data/eris_multisig/`, `data/eris_multisig_votes_all.csv` |
| ERIS hub | Configuration, current delegations, validator descriptions and relevant transactions | `data/eris_multisig/hub_*`, `data/eris_hub_delegations.csv` |
| Forum | Initial topic segment, key posts 54–57 and 90–92, revision and current suspension fields | `data/forum/` |
| Voting source code | Hub vote functions, state checks, prop-gauge voting and query logic | `repos/contracts-tokenfactory/` |

The full native transaction JSON is authoritative where older transaction bodies are not decoded by the current LCD response. The CSV contains the 77 vote messages exposed in structured form; the raw set contains all 87 responses.

“all voting history” here means all requested **Phoenix board, ERIS fixed-multisig, and 4853** records. It does not mean every Terra governance proposal since chain genesis.

## 2. Phoenix board: A272 and subsequent operation

### Exact A272 mechanics

- [A272](https://dao.phoenix.money/dao/terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg/proposals/A272) was created **3 October 2026 at 15:02:16 UTC**.
- Message 1 removes `terra18ruq…s4c` from the four-member group.
- Message 2 sets `absolute_percentage` to `0.6`.
- The three remaining seats would each carry 25 weight; two YES votes would provide 50/75 = 66.67%, above 60%.
- The existing four-seat threshold is 75%, requiring 75/100, normally three YES votes.
- Final tally: **50 YES, 25 NO, zero abstentions; one member did not vote**. Status: **rejected**.
- [Current config](https://terra-phoenix-api.highstakes.ch/cosmwasm/wasm/v1/contract/terra1660g9mle5kfsq8c0p4k4hgr9ujdyr3m48c22cawy0akr98rmwksqehqnup/smart/eyJjb25maWciOnt9fQ==) remains 75%; [current membership](https://terra-phoenix-api.highstakes.ch/cosmwasm/wasm/v1/contract/terra1pq9f4a8cn4cdvvm9j7v0mu8n5elf44tgtre8mzrfz3j4x6yyl2yq4hnkuk/smart/eyJsaXN0X21lbWJlcnMiOnsibGltaXQiOjEwMH19) remains four equal seats.

The opening emergency-supervisor post described a 2–2 deadlock. The chain instead shows 2 YES, 1 NO, and 1 absent ballot. Later 4853 text uses “persistent Stewardship dysfunction” rather than a literal vote split.

### The board did not become generally unable to act

A273–A289 show routine approvals after A272. A275 reached its vote threshold but failed execution, which is different from governance deadlock. This is counterevidence to a claim of total operational paralysis. It does not resolve whether the underlying personnel dispute is an “Adverse Event” under the bylaws.

### Voting alignment is documented; coordination is not

The A1–A289 record shows MB voted YES on **251 of 252 Philipp proposals where MB cast a ballot**. The single NO was A28; MB voted YES on corrected A29 five minutes ten seconds later. This is an unusually high agreement rate and warrants review of independence. It is not, by itself, evidence of an agreement or common control.

A284 supplies a later difference: MB YES, Philipp ABSTAIN. A281 also has MB YES with no Philipp ballot.

## 3. Beneficiary participation and milestone approvals

Fresh proposal payloads and ballots confirm:

| Proposal | On-chain action and governance fact |
|---|---|
| A116 | Philipp proposed and joined exactly 75 YES weight for Votion/LA Frontend milestones and a claim. |
| A159 | Setup recurring Stewardship payments; recipients were among the voters supplying exactly 75 YES weight. |
| A175 | Philipp proposed and joined exactly 75 YES weight for a Votion milestone. |
| A209 | Philipp proposed and joined exactly 75 YES weight for Creda milestones 1–3. |
| A215 | Philipp proposed and joined exactly 75 YES weight for Creda milestone 4. |
| A249 | The targeted A272 member proposed a 16,900-USDC security-audit payment to that member's own address and joined exactly 75 YES weight. A272's description alleges an agreed recusal was breached; the vote proves participation, while the alleged agreement needs separate records. |
| A266 | Established a 125,000-USDC Estima grant: 45,000 kickoff, 45,000 mainnet launch, 35,000 analytics/integration. Philipp did **not** vote; the other three directors approved it. |
| A271 | Enabled the 45,000-USDC kickoff. Philipp proposed and joined exactly 75 YES weight. |

These records establish beneficiary participation and the structural importance of each deciding vote. They do not prove work was undelivered, prices were unreasonable, or a specific legal/bylaw violation. A fair review should apply one conflict-of-interest standard to every director.

Relevant originals: [A249](https://dao.phoenix.money/dao/terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg/proposals/A249), [A266](https://dao.phoenix.money/dao/terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg/proposals/A266), [A271](https://dao.phoenix.money/dao/terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg/proposals/A271).

## 4. Handover and retained technical power

The [original TLA launch document at a fixed commit](https://github.com/phoenix-directive/docs/blob/7cebbd26048f0e1568a2aed55177090b90788d8b/common_backup/2024-08-12_24385_launching-terra-liquidity-alliance.md#L164-L169) says:

- migration “Contract Admin” transfers to Stewardship after one month;
- configuration “Ownership” transfers after three months;
- it identifies the ERIS admin wallet `terra1q0v…tew` and configuration wallet `terra1kefa…gzl`.

Fresh 26 October queries show:

- Treasury migration admin remains `terra1q0vny4wx2pfteh9zq323wh48c654xacpfq5tew`.
- TLA registry migration admin remains the same wallet.
- Registry configuration owner remains `terra1kefa2zgjn45ctj32d3tje5jdwus7px6n2klgzl`, with no pending owner.
- The hub's stored owner remains the configuration wallet.

In [forum post 55](https://forum.phoenix.money/t/phoenix-foundation-appointment-of-an-emergency-supervisor/47/55), Philipp states ERIS retained administration because it continued to operate the contracts and did not consider transfer to the current board appropriate. That is a direct explanation, not evidence of an approved replacement handover date.

The preserved authority ledger lists **31 privileged operations in 19 successful transactions** after its conservative 27 November 2024 cutoff. I verified the original commitment and current roles but did not independently replay every historical operation in this pass. The ledger and transaction hashes are in `downloads/packaged_ledger.json`.

### ERIS proposal 9 is a partial corrective action

ERIS proposal 9 passed with exactly 70/90 YES weight and was executed at **25 October 2026, 05:11:51 UTC**, transaction [`86E599…42D9`](https://chainsco.pe/terra2/tx/86E599263604B396BFB0F35F2F4E505E2EA758B024315B1C055C14994E6242D9). Fresh contract queries confirm both the ampLUNA hub and CW20-ICS20 now have the Phoenix board as migration admin.

That transfer does **not** change the Treasury admin, TLA registry admin/owner, or the hub's separate stored owner.

## 5. ERIS voting mechanics and multisig connections

### Three separate systems must not be conflated

1. **Fixed multisig:** five voters with weights 50, 10, 10, 10, 10; absolute threshold 70 of 90.
2. **Hub chain-governance voting:** `contracts/hub/src/gov.rs` requires `assert_vote_operator`; the authorized operator can make the hub cast a normal or weighted native governance vote.
3. **vAMP prop gauges:** users accumulate proposal-specific voting power from vote-escrow locks. `vote.rs` removes a prior vote before applying the new one, checks quorum, and asks the hub to cast either a weighted distribution or the currently wanted vote. The contract owner can initialize/remove proposals, remove users, and change quorum/weighting configuration.

Relevant code: [`gov.rs`](https://github.com/erisprotocol/contracts-tokenfactory/blob/main/contracts/hub/src/gov.rs), [`state.rs`](https://github.com/erisprotocol/contracts-tokenfactory/blob/main/contracts/hub/src/state.rs), [`prop_gauges/vote.rs`](https://github.com/erisprotocol/contracts-tokenfactory/blob/main/contracts/amp-governance/prop_gauges/src/vote.rs), [`queries.rs`](https://github.com/erisprotocol/contracts-tokenfactory/blob/main/contracts/amp-governance/prop_gauges/src/queries.rs).

The current hub config response did not expose a `vote_operator`; no 4853 ballot exists from the hub contract, and the queried transaction-event searches returned no hub vote. Those searches are not a complete archive-level proof that the hub never voted historically.

### Multisig voting history

- Every recorded ballot in all nine proposals is YES.
- Proposals 5, 6, and 8 were rejected because they reached only 60, 60, and 50 weight respectively—not because of NO ballots.
- Every executed proposal included the 50-weight signer.
- Proposal 9 reached exactly 70: the 50-weight signer plus two 10-weight signers.

Connections established by matching public addresses:

- `terra18ruq…s4c` is both a Phoenix board member and a 10-weight ERIS signer. A272 targeted that seat. The signer voted YES on ERIS proposal 9 after the dispute began, transferring admins to the board. This is counterevidence to a simplistic claim of uniform action against that member.
- `terra1alxk…l9c` is the 50-weight ERIS signer and cast a direct YES ballot on 4853 at **24 October, 03:57:49 UTC**, transaction [`B82106…85AD6`](https://chainsco.pe/terra2/tx/B8210663C2B8D7BE90F655FE11C7994FBCDFCF4FEB9890F3F2662FDEDB485AD6). Its 50/90 multisig weight has no effect on native Terra voting weight; Smart Stake displays its native stake as approximately zero.
- Lion DAO's account is not an ERIS multisig voter, but it executed proposal 9 at 05:11:51 on 25 October, about five minutes after changing its 4853 vote from ABSTAIN to YES. CW3 execution after passage can be permissionless, so this proves operational interaction and timing—not membership or coordinated voting.

## 6. Proposal 4853: influence analysis

### Direct proposer relationship

The native proposal was submitted **24 October 2026 at 03:40:11 UTC** by `terra1vm5azhvaxeanc7auxh02y8jmxrk8tj93f6aywp`.

That same underlying address is:

- the ERIS validator, `terravaloper1vm5azhvaxeanc7auxh02y8jmxrk8tj93f43e7j`;
- the recipient of the 125,000-USDC A266 grant;
- the account that voted YES on 4853 at **24 October, 13:00:13 UTC**, transaction [`B51BA6…B271`](https://chainsco.pe/terra2/tx/B51BA6772D336A35A81606DB7656BFDC085E6799E1510B72DC9F884A4083B271).

These are direct financial and governance relationships relevant to independence and disclosure. Voting on one's own proposal is ordinary Cosmos governance behavior and is not independently an irregularity.

### Captured tally

At approximately **26 October 2026, 14:14 UTC**:

| Option | LUNA | Share of total votes |
|---|---:|---:|
| YES | 40,028,648.81 | 35.03% |
| NO | 17,465,754.10 | 15.28% |
| VETO | 34,183,906.27 | 29.91% |
| ABSTAIN | 22,598,990.31 | 19.78% |
| **Total** | **114,277,299.49** | **30.58% of 373,651,005 staked** |

YES / (YES + NO + VETO) = **43.66%**, below the required majority. Quorum was reached. VETO remained below 33.4%.

Primary APIs: [proposal](https://terra-phoenix-api.highstakes.ch/cosmos/gov/v1/proposals/4853), [all votes](https://terra-phoenix-api.highstakes.ch/cosmos/gov/v1/proposals/4853/votes?pagination.limit=1000), [tally](https://terra-phoenix-api.highstakes.ch/cosmos/gov/v1/proposals/4853/tally). Cross-checks: [Smart Stake](https://analytics.smartstake.io/terra/proposal/4853), [Ping](https://ping.pub/terra/gov/4853). Ping reported its Terra LCD disconnected, so its zero tally fields were not used.

### ERIS-hub delegation links

Fresh [hub delegation records](https://terra-phoenix-api.highstakes.ch/cosmos/staking/v1beta1/delegations/terra10788fkzah89xrdm27zkj5yvhj9x3494lxawzm5qq3vvxcqz2yzaqyd3enk?pagination.limit=1000) show approximately:

| Validator | 4853 vote | ERIS-hub delegated LUNA | Interpretation |
|---|---|---:|---|
| Galactic Punks | YES | 7,862,461 | Material ERIS-linked YES stake; not hosting proof. |
| ERIS | YES | 3,878,960 | Direct proposer/validator relationship. |
| Orbital Command | YES | 1,124,006 | Material ERIS-linked YES stake. |
| Smart Stake | VETO | 7,862,461 | Strong counterexample to a unified ERIS vote narrative. |
| Another VETO validator | VETO | 1,123,807 | Additional ERIS-linked stake on the opposing side. |
| Lion DAO | YES | 0 in current response | Validator-set inclusion and execution interaction, but no current hub delegation. |

The three named YES recipients together account for about **12.87 million LUNA** of hub-delegated stake. Galactic Punks, ERIS, Orbital Command, and Lion DAO are all in the hub's current validator set; their total validator voting power was approximately 39.4 million LUNA, about 98% of the captured YES tally. That figure describes concentration within a validator set, not control by ERIS.

The hub currently delegates about **32.20 million LUNA** across 11 validators. Its delegation strategy is gauge-based. The presence of large delegations on both YES and VETO sides is the strongest evidence against treating “ERIS-linked” as a single voting bloc.

### Vote changes

The raw set contains 87 vote transactions but 79 current ballots. Examples include Galactic Punks voting YES early, Lion DAO changing ABSTAIN to YES, and other accounts changing YES to NO or ABSTAIN. Vote changes are permitted and are not themselves manipulation. Timestamps are preserved for further review of delegation changes, validator announcements, and forum activity.

## 7. Galactic Punks and Lion DAO hosting review

**Finding: common hosting or operation by ERIS is unproven.**

- Their validator records have distinct consensus keys and project-specific descriptions.
- Galactic Punks' description presents a community-led validator supporting GalacticDAO and NFTs.
- Lion DAO's description presents its own DAO ecosystem.
- No matching hosting statement was located in the searched ERIS GitHub organization or public web results.
- Galactic Punks receives a large ERIS-hub delegation; Lion DAO currently receives none.
- Galactic Punks' listed website did not resolve during review; Lion DAO's listed website is parked. Those conditions limit current official-site verification and should not be used as attribution evidence.

Accordingly, the evidence supports **delegation and governance relationships**, not “hosted by ERIS.” A hosting finding would require an explicit infrastructure statement, shared operational configuration with meaningful provenance, or another primary operations record.

## 8. Last-four-weeks chronology

All times UTC. Allegations are identified separately from executed chain actions.

| Date | Record |
|---|---|
| **22 Sep, context** | Registry owner set `BURN_RECIPIENT`; staking contracts migrated to code 4033; incentive blacklists added, then broad entries removed about 2h42m later. The name `BURN_RECIPIENT` does not itself prove assets were burned. |
| **23 Sep, context** | Treasury migration admin moved between the two ERIS wallets, not to the Phoenix board, transaction [`5202CA…F3D3`](https://chainsco.pe/terra2/tx/5202CA47D1B467EA0C2441B3EDF1B40674D8633EC232C0E06F32C7DCC38BF3D3). |
| **28 Sep** | A269 burn proposal executed with 75 YES weight. |
| **30 Sep** | A270 grant and A271 Estima kickoff executed. A271 included Philipp's YES in the minimum passing set. |
| **3 Oct, 02:14–02:21** | Code 4037 deployed; an address-specific list configured; code 4038 changed the restriction to read that list; a different address was then configured. The 4853 proposer/grant recipient was the first configured address. The ledger proves configuration, not a failed live withdrawal. |
| **3 Oct, 15:02** | A272 created: removal plus 60% threshold. |
| **3–4 Oct** | A272 rejected 50/25/0 with one absent member. A273 payments executed. |
| **4 Oct** | A274 executed; A275 passed its vote but failed execution. |
| **8 Oct** | A276–A281 approved payment and liquidity actions. A281 passed without Philipp or Rose ballots; the other three supplied 75 YES. |
| **13–14 Oct** | A282 and A283 executed, further counterevidence to general board paralysis. |
| **16 Oct, 01:55** | Emergency-supervisor discussion opened. Initial post described a 2–2 split and proposed an independent review. |
| **16 Oct, 11:56** | [Revision record](https://forum.phoenix.money/posts/146/revisions/2.json) identifies `0xphilipp` editing post 146 and removing a quoted passage about board structure and later talks. No edit reason is recorded. |
| **17 Oct** | A284 created. Current bylaws PDF modified in GitHub at 12:41; the commit message says reference fixes. I did not establish substantive clause changes from the binary diff. |
| **18 Oct, 15:14** | `ASSET_STAKING_FIX` emptied, transaction [`EDC654…6230`](https://chainsco.pe/terra2/tx/EDC654FA72CA8BA3921596AD93648C55DA676BCDD427FE1475DA3B853CA56230). The admin/owner powers remained. |
| **19 Oct, 00:20–00:39** | A284: Philipp ABSTAIN, MB YES; proposal later executed. |
| **19 Oct, 02:18** | Community guidelines added in commit [`ee361d…eb95`](https://github.com/phoenix-directive/docs/commit/ee361d66c5f9e3603ba2efa55376914caed2eb95). The text encourages sourced criticism but labels baseless criticism as FUD/bannable. This date does not prove retroactive application. |
| **19 Oct, 03:01–07:39** | A285 opened; A286 and A287 executed. |
| **19 Oct, 20:54** | [Post 55](https://forum.phoenix.money/t/phoenix-foundation-appointment-of-an-emergency-supervisor/47/55) publicly confirmed retained ERIS administration and denied a voting agreement. |
| **19 Oct, 22:09** | [Post 57](https://forum.phoenix.money/t/phoenix-foundation-appointment-of-an-emergency-supervisor/47/57) offered an off-chain commitment to vote only NO/ABSTAIN during a temporary 2-of-3 period, except for onboarding directors. This does not remove on-chain authority. |
| **22 Oct** | A288 rejected; A289 executed three minutes later in proposal creation time, with 75 YES weight. |
| **23 Oct, 01:55** | [Post 91](https://forum.phoenix.money/t/phoenix-foundation-appointment-of-an-emergency-supervisor/47/91) said a standing Supervisor was in office and A272 had not been referred to that Supervisor. This is a participant statement requiring independent governance-record verification. |
| **24 Oct, 03:40** | Native 4853 submitted by the ERIS validator/grant recipient. |
| **24 Oct, 03:57** | The 50-weight ERIS multisig signer voted YES on 4853. |
| **24 Oct, 09:38** | ERIS proposal 9 reached 70/90 with its third YES ballot. |
| **24 Oct, 13:00** | The 4853 proposer/ERIS validator voted YES on its own proposal. |
| **25 Oct, 05:06** | Lion DAO changed from ABSTAIN to YES on 4853. |
| **25 Oct, 05:11** | The same Lion DAO account executed ERIS proposal 9, transferring the two admins to the Phoenix board. |
| **26 Oct** | Current queries confirmed new admins, the wider remaining handover gaps, and the 4853 tally above. `Ex_TFL` has a public suspension-until field; the other two reviewed profiles have no current suspension fields. |

## 9. Items that remain unproven or need more evidence

- Any express voting agreement, common key custody, or coordinated instruction among directors, multisig signers, or validators.
- ERIS hosting/operation of Galactic Punks or Lion DAO.
- That every use of retained authority was unauthorized; no replacement authorization was located in the reviewed corpus, but the review is not a legal completeness guarantee.
- A failed live withdrawal caused by the wallet-specific restriction. The evidence proves deployment/configuration and offline behavior tests, not a live affected-user failure.
- Substantive bylaw changes from the 17 October binary PDF modification.
- That an adverse event meets the bylaws' legal threshold, or that 4853's proposed interpretation of supervisor powers is correct.
- Deliverability, fair pricing, or absence of all work associated with grants and milestones.
- Complete historical native voting by the hub; the current ballot and targeted event searches are bounded.

## 10. Recommended governance follow-up

1. Publish a role-by-role handover matrix: contract, code admin, configuration owner, operational controller, fee recipient, current address, promised address, and executing transaction.
2. Require machine-readable conflict disclosures on proposals: proposer, voters, beneficiaries, related contracts, and financial relationships. Apply the same recusal rule to all members.
3. Keep at least three independent consents for spending and membership changes. Do not treat an off-chain voting undertaking as a substitute for on-chain limits.
4. For 4853, disclose the proposer's ERIS and prior-grant relationships and publish the proposed supervisor's independence statement and remuneration source before final voting.
5. Publish exact source or reproducible build hashes for codes 4033, 4037, and 4038, plus the governance authorization for restriction features.
6. Preserve forum moderation reasons, editor role, revision history, and suspension appeals. Do not apply newly published guidelines retroactively without an explicit policy.
7. Re-run this analysis at 4853 close, including delegation snapshots and vote changes, to distinguish changing voting power from changing ballots.
