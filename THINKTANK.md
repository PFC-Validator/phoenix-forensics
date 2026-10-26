# Phoenix Think Tank: authority, voting and wallet relationships

**Evidence cutoff:** preserved chain responses captured on 26 October 2026; additional public-source review on 26 October 2026.  
**Privacy scope:** entity names, public handles/launch labels and addresses only. No identity research or surname attribution. Launch labels are aliases used in the source document, not independent identity findings.

## Assessment

The Think Tank is a separate six-member DAO whose stated purpose is to veto large or qualifying rolling Treasury expenditures. It is not merely a research or advisory group.

The preserved record supports four oversight concerns:

1. **No substantive veto proposal received a YES or NO vote.** Proposals 2–5 received only one or two abstentions and otherwise no recorded ballots. They expired rejected. This means the veto did not activate; it is not evidence of affirmative informed approval of the underlying expenditure.
2. **Agenda and technical-message concentration.** All five preserved proposals were created by the 0xPhilipp-associated Think Tank wallet. The launch document describes that member as `auto abstain, helping with technical messages only`; the wallet did abstain on all five. Abstention limits direct voting influence but does not remove influence over proposal timing, wording or construction.
3. **Proposal 5 has no executable message.** Even a four-YES result would not itself have called the Treasury `veto` method. It could still have been a signal vote, but its title and description call it an optional veto. The missing target/message requires explanation.
4. **Members have economic relationships requiring disclosure review.** Treasury grants/payments and an ERIS invoice are documented below. These relationships do not establish common ownership or improper influence, but they matter when the body is presented as independent oversight.

Counterevidence and limitations matter: the technical member abstained, including on the test payment to that same wallet; no rationale fields are populated; and non-participation does not establish motive. The current member list matches the launch list, but historical group-contract changes at every proposal height have not yet been reconstructed.

## 1. Authority and design

The DAO's on-chain name is **Phoenix Directive Veto Multi-Sig**, with the description: `This Multi-Sig has veto rights over the Phoenix Directive Treasury contract.`

| Control | Preserved configuration |
|---|---|
| DAO | `terra15l7567hhxttv2k5enmu4k8uez8e3cx3sxqfg6fsq4zzuwuzy2fqsjq00gr` |
| Voting module | `terra19rcv689easxyt4w2h5aznpmkxdnvlmkmwsss7gszpwzqh2ftcmsqgqdkrd` |
| Proposal module | `terra1ykz3hhlpxu7820vkn5ucfzlf4tx2wuqehg026n4x2ha08k4f0fwqw0jl8e` |
| Members | Six addresses, weight 1 each |
| Passing threshold | 66% of total power: effectively **4 YES of 6** |
| Maximum voting period | 172,800 seconds: **2 days** |
| Revoting | Disabled |
| Execution | Members only |
| DAO admin | The Think Tank DAO itself |

The original Directive says initial membership was finalized by the Stewardship Team and the veto multisig would then be self-organized. It describes Think Tank vetoes for spending requests over $50,000, with a three-day lockup. The launch discussion also describes rolling-30-day thresholds and says unclaimed amounts can be vetoed after the lock period. Those rolling rules must be evaluated from the Treasury contract/action values, not from individual payment size alone.

## 2. Complete preserved voting record

`NO BALLOT` means no ballot was returned in the preserved proposal vote query; it does not mean a NO vote.

| Launch label / handle | Address | P1 test | P2 Votion veto | P3 Creda veto | P4 Estima veto | P5 migration veto |
|---|---|---|---|---|---|---|
| 4719 | `terra13qjx…5zlz` | YES | NO BALLOT | NO BALLOT | NO BALLOT | NO BALLOT |
| 7183 | `terra18gqp…muwjw` | YES | NO BALLOT | NO BALLOT | NO BALLOT | NO BALLOT |
| David | `terra1j00t…nsn0` | YES | NO BALLOT | ABSTAIN | NO BALLOT | NO BALLOT |
| Rebel | `terra1rnwr…pmf` | NO BALLOT | NO BALLOT | NO BALLOT | NO BALLOT | NO BALLOT |
| 0xPhilipp | `terra1vm5a…aywp` | ABSTAIN | ABSTAIN | ABSTAIN | ABSTAIN | ABSTAIN |
| Ryan | `terra1y835…l03e` | YES | ABSTAIN | NO BALLOT | NO BALLOT | NO BALLOT |
| **Result** | | **Executed: 4 YES, 1 ABSTAIN** | **Rejected: 2 ABSTAIN** | **Rejected: 2 ABSTAIN** | **Rejected: 1 ABSTAIN** | **Rejected: 1 ABSTAIN** |

Across the four substantive veto proposals, the five non-technical members supplied only **two ballots out of 20 possible ballots**, both abstentions. This is a participation observation, not proof of a deliberate decision or coordinated inactivity.

### Proposal targets and status

| Think Tank proposal | Target / message | Related Treasury record |
|---|---|---|
| P1, 2024-10-08 expiry | Sent 0.1 LUNA to the 0xPhilipp-associated wallet; proposer abstained | Executed test |
| P2, 2025-02-09 expiry | Treasury `veto(id: 28)` | Action 28, Votion: 50,000 USDC; both milestones marked claimed |
| P3, 2025-10-09 expiry | Treasury `veto(id: 72)` | Action 72, Creda: 210,000 USDC; all four milestones marked claimed |
| P4, 2026-09-25 expiry | Treasury `veto(id: 112)` | Action 112, Estima: 125,000 USDC total; 45,000 marked claimed at capture, later milestones not enabled/claimed |
| P5, 2026-10-07 expiry | **No messages and no Treasury action ID** | Contextually similar to action 109, USDC.inj Migration App Part 1, but no explicit on-chain linkage; do not treat the mapping as proven |

For P4, the veto expired about 44 minutes before action 112's recorded `active_from`. For P2 and P3 the action records show later activation times, but action creation/update semantics have not been reconstructed sufficiently to use those intervals as evidence of a process breach.

## 3. Relationships to already identified wallets and entities

### Direct financial or governance relationships

| Member | Documented relationship | Classification and caution |
|---|---|---|
| **0xPhilipp** | Think Tank wallet is the named recipient of actions 28, 72 and 112. It also proposed all four veto proposals concerning those grants or the migration work and abstained on each. | Direct beneficiary and agenda-setting overlap. Abstention is a mitigating fact, but disclosure/recusal rules and independent message review remain relevant. |
| **0xPhilipp** | Associated payment wallet `terra1gaxz…wy0a` is recipient of action 109's 5,000-USDC migration-app payment. On 1 September 2026 it sent 5,000 USDC to the Think Tank wallet in transaction `9A139FB6…03B8C`. | Transfer between two publicly attributed associated wallets, not an independent third-party relationship. |
| **7183** | Recipient of action 32, LA Secondary Frontend Grant: 5,000 + 25,000 USDC, both marked claimed. | 30,000-USDC Treasury grant relationship. The preserved outbound-transfer subset does not include the original claim transactions, so the action state is the evidence here. |
| **David** | Action 60 scheduled three 700-USDC delegation-program payments to this wallet and is marked done with no open payments. Action 77 paid a separate 1,000-USDC Bonus Liquidity Deployment; transaction `8E29E90F…AFC6FC3` confirms receipt on 5 January 2026. | 2,100 USDC scheduled delegation-program payments plus 1,000 USDC directly evidenced. Do not infer the work was or was not performed from payment state alone. |
| **Rebel** | ERIS protocol fee account `terra1rggg…rjxa` sent 7,500 USDC on 7 June 2026 with memo `invoice`, transaction `02B838A2…C3AC80`. | Direct commercial relationship with ERIS, not a Phoenix Treasury payment. Relevant to independence and disclosure. |
| **4719** | Public governance monitor indexes this validator account as voting YES on native proposal 4819, the Phoenix Directive recovery/funding proposal. | Native governance participation, not evidence of a payment or common ownership. No ballot from this address appears in the preserved 4853 snapshot. |
| **Ryan** | YES on the Think Tank test and ABSTAIN on the Votion veto; no additional financial link to the reviewed addresses was found in the preserved corpus. | Governance relationship only in the current evidence. |

### Protocol interactions that should not be overstated

Rebel's Think Tank wallet also has preserved user interactions with:

- **Creda Portfolio:** supply, repay, borrow and withdraw messages.
- **USDC transmuter:** a swap of approximately 9.157907 USDC.
- **ERIS hub:** three `harvest` calls.

These are direct contract interactions, but ordinary protocol use and potentially permissionless harvest calls do not prove employment, ownership, payment for votes or control of those contracts. The 7,500-USDC invoice is the stronger commercial evidence.

### Bounded negative findings

A review of **906 unique preserved transaction responses** found:

- No direct native transfer between two different Think Tank member addresses.
- No direct native transfer between a Think Tank member and any of the five ERIS fixed-multisig signers.
- No direct native transfer between a Think Tank member and the MB, Vini or Rose board addresses.
- Only the 0xPhilipp-associated 5,000-USDC transfer between two associated wallets described above.
- Only 0xPhilipp's Think Tank/ERIS validator account appears among the six Think Tank addresses in the preserved 4853 ballots; it voted YES.

These are bounded findings, not a claim that complete histories for all six addresses have been downloaded. Full sender/recipient histories for 4719, 7183, David and Ryan remain a collection gap.

## 4. Distribution-module false lead corrected

`terra1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8pm7utl` is the **Cosmos SDK distribution module account**, not a shared operations wallet. This is independently reproducible by deriving the module address as `sha256("distribution")[:20]` and Bech32-encoding it with the `terra` prefix; the result exactly matches the address. Terra Finder also shows reward and validator-commission withdrawal activity.

It must therefore be excluded as evidence of a shared counterparty, common ownership or an operations relationship among Galactic Punks, Lion DAO, Orbital Command and ERIS. The actual validator signatures, commission recipients and subsequent transfers remain separate questions.

## 5. What is needed for a defensible governance judgment

1. Historical Think Tank membership at every proposal height and all add/remove transactions.
2. Proposal creation and execution transactions, especially for P5's empty message and the timing of P3/action 72.
3. The written recusal/conflict policy and any disclosure of the grant, payment and invoice relationships above.
4. Whether any member besides the technical member can or does create correctly formed veto proposals.
5. Notification records showing members were made aware of veto windows; abstention and absent ballots have different operational implications if notice was missing.
6. Contracts, invoices and deliverables for actions 28, 32, 60, 72, 77, 109 and 112, plus the ERIS invoice.
7. Treasury contract logic for rolling thresholds, post-lock vetoes and `active_from` updates.
8. Complete address histories for the four members whose current evidence is comparatively sparse.

## Primary records

- `data/thinktank/config.json` — threshold, voting period, execution and revoting rules.
- `data/thinktank/dump_state.json` — DAO name, purpose and module addresses.
- `data/thinktank/members.json` — six current members and weights.
- `data/thinktank/proposals.json` — all five proposals, messages, statuses and tallies.
- `data/thinktank/votes.json` / `votes.csv` — all returned ballots.
- `data/treasury/actions/` — actions 28, 32, 60, 72, 77, 109 and 112.
- `data/treasury/outbound_transactions.json` — original 1,000-USDC Treasury claim/payment transaction.
- `data/transfers/rebel_eris_invoice_2026-06-07.json` — original ERIS invoice transaction.
- `data/transfers/rebel_project_sender.json` and `rebel_project_recipient.json` — preserved protocol interactions.
- `repos/phoenix-docs/the-phoenix-directive.md` — governance role and appointment design.
- `repos/phoenix-docs/treasury_launch.md` — launch membership, auto-abstain description and threshold discussion.
- [Public native 4819 governance monitor](https://monitor.burrito.money/luna/governance/4819) — validator identity and YES ballot for 4719.
- [Terra Finder distribution account](https://finder.terra.money/mainnet/address/terra1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8pm7utl) — reward/commission activity corroboration.
