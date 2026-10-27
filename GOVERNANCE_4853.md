# Potential governance issues: 4853, ERIS voting power and related validators

**Evidence cutoff:** 26 October 2026, during live review.  
**Privacy scope:** entities, public handles and addresses only. No identity attribution is made for the large vAMP account.

**Source-independence disclosure:** the primary HighStakes LCD is operated by a validator inside this review: HighStakes voted ABSTAIN and has approximately 3.254M LUNA of hub delegation. It is not neutral infrastructure. Hub and ICS20 configuration were cross-checked exactly against tdrsys; sequential live-tally reads are preserved separately rather than forced into agreement.

## Executive assessment

The evidence supports credible findings of **outcome-changing influence concentration, conflicts requiring disclosure, and weaknesses in internal governance processes**. It does not currently support a definitive allegation of common ownership, coordinated voting, vote buying or a single ERIS-controlled bloc.

Three points are particularly important:

1. **A full ERIS-hub YES would be outcome-changing.** At the captured tally it would move 4853 from failing to passing, subject to no other changes.
2. **One currently unattributed account can exceed the vAMP quorum by itself.** The account has 215,228 vAMP at proposal period 208, against an approximately 76,792 participation-quorum requirement.
3. **The actual situation has not yet reached that outcome.** The 4853 prop-gauge has zero recorded vAMP votes, and the ampLUNA hub has no current native ballot. The scenario is therefore an influence-capability finding, not proof of what will happen.

## 1. Current native position

The refreshed response at approximately **26 October 2026, 19:03 UTC** contained **83 current ballots** and this tally. The earlier `data/native_4853/tally.json` capture at approximately 14:14 UTC had 34.184M VETO; the difference is live tally drift, not conflicting analysis.

| Option | LUNA | Interpretation |
|---|---:|---|
| YES | 40,037,384.529 | 41.62% of non-abstain votes |
| NO | 17,466,527.882 | — |
| NO WITH VETO | 38,686,323.995 | 32.57% of all votes, below 33.4% |
| ABSTAIN | 22,600,302.011 | — |

At this capture, 4853 has quorum but is **not passing**, because YES is below 50% of non-abstain votes. VETO has not independently reached its threshold either.

Primary sources:

- [Current ballots](https://terra-phoenix-api.highstakes.ch/cosmos/gov/v1/proposals/4853/votes?pagination.limit=1000)
- [Current tally](https://terra-phoenix-api.highstakes.ch/cosmos/gov/v1/proposals/4853/tally)
- [Proposal 4853](https://ping.pub/terra/gov/4853)

## 2. What an ERIS-hub vote changes

The ampLUNA hub currently delegates approximately **32.2055M LUNA**. Under Cosmos governance, a delegator's vote overrides the validator's vote for that delegation. It does not delete the validator's ballot; it changes which option receives that voting power.

Current hub delegation distribution. **Ballot options and hub-delegation amounts below come from primary LCD records, not from validator total-weight estimates.** Smart Stake analytics supplies secondary total ballot weights such as 8.6M for ERIS and 21.4M for Smart Stake; those are different measurements. The primary native votes response contains options but no per-ballot LUNA weights.

| Validator | Current ballot | Hub delegation | Effect if the whole hub votes YES |
|---|---|---:|---|
| Galactic Punks | YES | 7.862M LUNA | Remains YES; no net option change |
| ERIS | YES | 3.879M LUNA | Remains YES; no net option change |
| Orbital Command | YES | 1.127M LUNA | Remains YES; no net option change |
| Smart Stake | NO WITH VETO | 7.862M LUNA | Moves from VETO to YES |
| Ceres Ventures | NO WITH VETO | 1.127M LUNA | Moves from VETO to YES |
| HighStakes | ABSTAIN | 3.254M LUNA | Moves from ABSTAIN to YES |
| BackBone Labs | No current ballot | 3.344M LUNA | Enters the counted vote as YES |
| cosmosrescue | No current ballot | 3.750M LUNA | Enters the counted vote as YES |

The remaining hub-backed validators' current ballots and delegations do not change the YES scenario. Zero-balance delegations have no material effect.

### Full-hub-YES scenario

| Metric | Current | If entire hub votes YES |
|---|---:|---:|
| YES | 40.037M | **59.371M** |
| NO | 17.466M | 17.466M |
| NO WITH VETO | 38.686M | **29.700M** |
| ABSTAIN | 22.600M | **19.346M** |
| YES share of non-abstain votes | 41.62% | **55.73%** |
| VETO share of all votes | 32.57% | **23.59%** |
| Outcome, other things equal | Failing | **Passing** |

The increment to YES is approximately **19.334M LUNA**. Approximately **7.093M** additional LUNA enters the total counted vote because BackBone and cosmosrescue currently have no ballot.

### Important limitations

- This is native **ampLUNA-hub** voting power only. Phoenix/TLA synthetic Alliance voting weight is separate and is not voted by the ERIS hub.
- BackBone and cosmosrescue are the only two currently unvoted validators in the reviewed set with material current hub delegations. Other unvoted validators do not gain voting power from an ERIS-hub ballot merely by being in its validator set.
- A prop-gauge ballot can be **weighted**, so full YES is a scenario, not a required outcome.

Sources: [hub delegations](https://terra-phoenix-api.highstakes.ch/cosmos/staking/v1beta1/delegations/terra10788fkzah89xrdm27zkj5yvhj9x3494lxawzm5qq3vvxcqz2yzaqyd3enk?pagination.limit=1000) and `repos/contracts-tokenfactory/contracts/hub/src/gov.rs`.

## 3. The vAMP quorum and the large account

The 4853 prop-gauge is initialized and active. Its current state is:

- `yes_vp = 0`
- `no_vp = 0`
- `abstain_vp = 0`
- `nwv_vp = 0`
- `current_vote = null`
- total period voting power: **767,921,061,697 base-unit vAMP = 767,921.061697 vAMP**
- quorum: **10%**, or **76,792,106,169.7 base-unit vAMP = 76,792.1061697 vAMP**
- `use_weighted_vote = true`

The gauge was initialized by the retained ERIS configuration owner at **24 October 2026, 13:24:02 UTC**, transaction `6A5828AA5C758C77C201877E5EB1F6F6273C19A3425FBF658E8570680FCDE14C`.

### Period-208 balances

| Account | vAMP at period 208 | Share of total | Assessment |
|---|---:|---:|---|
| `terra149h2na…mkk0z` | **215,228** | **28.03%** | Can exceed the participation quorum alone |
| 0xPhilipp ERIS account `terra1vm5a…aywp` | **35,913** | 4.68% | Below quorum alone |
| ERIS protocol fee account `terra1rggg…rjxa` | **47,338** | 6.16% | Below quorum alone |
| **Combined** | **298,479** | **38.87%** | Substantial potential influence if aligned |

If the large account votes YES and no opposing votes are cast, its support is enough to trigger a 100%-YES weighted hub vote. If other vAMP participants vote differently, the hub's native vote can be split. Reaching quorum is therefore not evidence of unanimity or of an inevitable full-YES outcome.

The large account has **46 Galactic Punks NFTs**, four pixeLions NFTs and three Space Toadz NFTs, and substantial ERIS-protocol activity. Its controller has not been established from public evidence. It should be described as an **unattributed vAMP account**, not as an ERIS-owned or ERIS-controlled account.

Sources:

- [Prop-gauge configuration](https://terra2.tdrsys.com/cosmwasm/wasm/v1/contract/terra1z0cxlq62a9dsjhz7g7hhgpuplcl32c0qeckhm9jyggln0rxq6z8syesq8j/smart/eyJjb25maWciOnt9fQ==)
- [Active prop-gauge proposals](https://terra2.tdrsys.com/cosmwasm/wasm/v1/contract/terra1z0cxlq62a9dsjhz7g7hhgpuplcl32c0qeckhm9jyggln0rxq6z8syesq8j/smart/eyJhY3RpdmVfcHJvcHMiOnt9fQ==)
- [Finished prop-gauge proposals](https://terra2.tdrsys.com/cosmwasm/wasm/v1/contract/terra1z0cxlq62a9dsjhz7g7hhgpuplcl32c0qeckhm9jyggln0rxq6z8syesq8j/smart/eyJmaW5pc2hlZF9wcm9wcyI6e319)
- [Large-account period-208 balance](https://terra2.tdrsys.com/cosmwasm/wasm/v1/contract/terra1ep7exp42jjtwgjly36y4vgylz82fplnjwpkz95wljzwfald8zwwqggsdzz/smart/eyJ1c2VyX3ZhbXBfYXRfcGVyaW9kIjp7InVzZXIiOiJ0ZXJyYTE0OWgybmE5ODhja2EwNXJ3Y3BtbnFmc2U2NHI2dnNwbWZta2sweiIsInBlcmlvZCI6MjA4fX0=)
- [Large account on Mintscan](https://www.mintscan.io/terra/address-estimation/terra149h2na988cka05rwcpmnqfse64r6vspmfmkk0z)
- [Prop-gauge vote construction](https://github.com/erisprotocol/contracts-tokenfactory/blob/main/contracts/amp-governance/prop_gauges/src/vote.rs)

## 4. Conflicts and overlapping relationships

The following are documented relationships, not proof of a coordinated scheme:

- The 4853 proposer is the ERIS validator and a prior Foundation grant recipient. It voted YES on its own proposal.
- The retained ERIS configuration owner initialized the 4853 prop-gauge.
- Galactic Punks and Lion DAO have recurring monthly transfers to ERIS. The agreements behind these payments remain unresolved; they could be hosting or service payments.
- The large vAMP account also received direct LUNA transfers from Galactic Punks, including **32,928 LUNA on 18 October 2026**, 23,293 LUNA on 20 February, 17,441 LUNA on 5 February and 6,240 LUNA on 10 March. Its NFT holdings make reward distributions a plausible explanation that must be tested before treating the transfers as ownership or payroll evidence.
- Rebel's Think Tank wallet received **7,500 USDC** from the ERIS protocol fee account with memo `invoice`. That is direct commercial evidence, not proof of vote influence.
- 0xPhilipp's Think Tank wallet is the recipient on Treasury grants that were also the subject of Think Tank veto proposals. It abstained on those proposals, which is a mitigating fact but not a complete conflict-management framework.

These relationships justify disclosure, recusal analysis and scrutiny of payment terms. They do not, on their own, establish common ownership or an express voting agreement.

## 5. Lion DAO and Ryan: a specific process concern

The transfer, ballot and timing facts are supported by primary records. `RyanLion` is a DAO-interface display handle: confidence is **high for the hash-anchored transaction and voting-power facts, and moderate for the display-name attribution** pending a first-party account/profile declaration. No real-world identity is inferred.

1. The original delegation committee lists **RyanLion — LionDAO + validator (The Lion Dao)** and **Philipp — Eris + validator operations (The Lion Dao)**.
2. On 22 October, Ryan's Think Tank wallet transferred **513,657.706575846 ROAR** to the account displayed as `RyanLion` on DAO DAO, transaction `1D67ECAB44A5CC61825A210D051E1282A095A60B74DF614D4AD26CD38CDA556F`.
3. On A33, `RyanLion` voted YES with **60.002 billion ROAR**, equal to **26.154% of total eligible voting power** and **99.866% of all YES voting power**.
4. Ryan's A33 vote was cast at **24 October, 15:28:25 UTC**. Lion DAO's validator switched from ABSTAIN to YES at **25 October, 05:06:13 UTC**, 13 hours 37 minutes 48 seconds later, while A33 remained open until **26 October, 13:16:42 UTC**.
5. A33 ended with **30.43% YES**, **1.875% NO**, and **67.70% ABSTAIN** among votes cast. The ampROAR hub voted ABSTAIN.

This is a credible **internal-process and independence concern**: a validator changed its native vote before the DAO's own signalling vote concluded, and one account overwhelmingly determined the YES side. It is not evidence that the final outcome was different from the validator's eventual vote, because both ended at YES. Nor does the small ROAR transfer explain the recipient's much larger pre-existing voting power.

Sources:

- [Original delegation committee record](https://github.com/phoenix-directive/docs/blob/main/common_backup/2024-01-08_14807_terra-delegation-committee-phase-1-recommendation.md)
- [Ryan wallet-link transaction](https://www.mintscan.io/terra/tx/1D67ECAB44A5CC61825A210D051E1282A095A60B74DF614D4AD26CD38CDA556F)
- [Lion DAO A33](https://daodao.zone/dao/terra1tkersa2mqwy2h8exj799qx2xrhdu0dkymk9psp6v0k4kz4tkxucssgluec/proposals/A33)
- [Ryan's A33 ballot](https://www.mintscan.io/terra/tx/F2AF959329FDFB3C50B96A4560B7DD1A79B2E32CF5132CF85B3195B457BAC57A)
- [Lion validator's change to YES](https://www.mintscan.io/terra/tx/4B356AF4C770CDD9729FDC39451C086BA188EF5A82EB7F1D0FCBE2AF28C5A0D2)

### One actor, several documented roles

The public handle/address links already in the corpus place 0xphilipp in several distinct roles: a Phoenix board seat; the Think Tank technical member that proposed all five preserved proposals and abstained on each; the 50-of-90 ERIS fixed-multisig seat; the 4853 proposer and a YES voter; an ERIS validator receiving hub delegation; and a recipient/beneficiary in Treasury actions that also had Think Tank veto proposals. The 50-weight signer also appears as an OTC counterparty. These are different addresses and powers, not proof of one key, one command structure or coordinated action. The governance issue is that disclosure, recusal and independent checks must work across all of these roles.

## 6. Think Tank oversight concern

The Think Tank record independently supports an oversight finding:

- Four substantive veto proposals received **no YES and no NO votes**; only one or two abstentions.
- The 0xPhilipp-associated technical member proposed all five preserved proposals and abstained on all five.
- Proposal 5 contains **no executable message**, so even four YES votes would not itself have executed a Treasury veto.
- Members have grant, payment or commercial relationships relevant to independence and disclosure.

This is evidence of a weak or inactive safeguard, not proof of deliberate capture. Abstentions, absent ballots, notification failures and incomplete historical membership records must be distinguished before assigning motive.

See `THINKTANK.md` for the complete ballot matrix and member-payment links.

## 7. Counterevidence and alternative explanations

A balanced assessment must also state:

- Smart Stake and Ceres voted **NO WITH VETO**, despite receiving ERIS-hub delegations.
- HighStakes is **ABSTAIN**, not YES.
- Eleven reviewed allocation-linked validators have not voted, so the reviewed validators are not acting as a single completed voting bloc.
- The large vAMP account has not yet cast a ballot on the 4853 prop-gauge.
- Recurring payments may be hosting fees, validator rewards or legitimate service compensation.
- Permissionless execution and ordinary protocol use do not prove coordination.
- The prop-gauge's weighted mechanism can represent dissent rather than forcing a unified result.

## 8. Publishable conclusions

### Supported

1. **Outcome-changing influence is concentrated.** A full ERIS-hub YES would pass 4853, and one account can independently meet the prop-gauge participation quorum.
2. **Relevant conflicts exist and should be disclosed.** They include grant/beneficiary overlap, recurring validator payments, an ERIS invoice, and direct Galactic Punks transfers to the large vAMP account.
3. **Internal processes need review.** Lion DAO's early validator vote, dominant RyanLion voting power, and the Think Tank's non-participation and empty veto message are concrete process concerns.

### Not supported as definitive allegations

- That the large vAMP account is controlled by ERIS or Galactic Punks.
- That ERIS, Phoenix or the reviewed validators are acting under a single command structure.
- That payments were intended to purchase votes.
- That 4853 has already passed or that the full-hub-YES scenario has occurred.

## 9. Evidence required before stronger findings

1. Complete prop-gauge voting history and the final native 4853 tally after voting closes.
2. Current and historical vAMP lock ownership disclosures at entity/handle level, without identity research.
3. Galactic Punks reward-distribution rules explaining the transfers to the large account.
4. Lion DAO validator-hosting terms and the rule requiring adherence to the DAO signalling result, including whether early voting is permitted.
5. Contracts and pricing for recurring validator-to-ERIS payments and the ERIS invoice to Rebel.
6. Think Tank membership at each historical proposal, notification records and an explanation for the empty veto message.
7. Proof of the actual handover status for retained contract administration and the prop-gauge owner.

