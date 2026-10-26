# Payment and ownership review

**Scope:** Phoenix Treasury actions and outbound transfers, validator/ERIS transfer links, and the five fixed-multisig signer accounts.  
**Raw transfer coverage:** 2 January–24 October 2026, plus the Treasury action inventory reaching back to 2024.  
**Privacy:** handles, roles, and public addresses only. No identity attribution.

For “TFL fund,” this review uses the **Phoenix Treasury** created in the post-TFL structure, not an original TFL corporate wallet.

## Key conclusions

1. **No direct transfer was found between the four reviewed validators and the five fixed-multisig signer addresses**, in either native-transfer or CW20-style event searches. This is a bounded result dependent on transaction indexing and is not a claim that no such transfer can exist.
2. **Galactic Punks and Lion DAO have a substantial recurring payment relationship with the ERIS validator/grant account.** Ten monthly transfers from each total **221,962 LUNA**. The transactions have no memo, so their purpose is not established by chain data alone.
3. **That recurring relationship is relevant to ownership, independence, and hosting questions**, but it does not prove legal ownership, common key custody, vote buying, or that ERIS operates either validator.
4. **The roughly 795,992 LUNA sent from Treasury to the 50-weight multisig signer is not salary or a grant.** Original messages show OTC trades in which the signer supplied USDC/WBTC and received LUNA. Counting gross LUNA outflow as compensation would be an accounting error.
5. **Director compensation is recurring and highly specific.** October actions 118–120 cover Philipp, Rose, and MB, but not the member targeted by A272. Separate infra payments to that member continue.
6. **Close-together payments are not automatically duplicates.** MB’s two 5,640-USDC claims 27 seconds apart were separate entitlements inside action 100.
7. **Large related-party grants need separate classification from operating swaps and liquidity deployments.** The ERIS grant recipient received 210,000 USDC under the completed Creda action and 45,000 USDC under Estima’s kickoff.

## 1. Validator-to-multisig transfer search

Reviewed validator accounts:

- Galactic Punks: `terra15lsftv92eyssjwkh2393s0nhjc07kryqeux5s6`
- Lion DAO: `terra1pet430t7ykswxuyhh56d4gk6rt7qgu9as43fnu`
- Orbital Command: `terra1lelhxdzwn9ddecv6sv0kcxj5tguurxnzcxuf76`
- ERIS: `terra1vm5azhvaxeanc7auxh02y8jmxrk8tj93f6aywp`

Reviewed fixed-multisig signers:

- `terra18ruqkccl5tp493uhvra0u6jylrzq8t8dv5qs4c`
- `terra1alxk3fmhcl0ga80gl9yj9zp3ezjm4sdh8a9l9c`
- `terra1rmyzqglwrwmajvp4qa2c7pel7c960amdyrh0ty`
- `terra1scku27w5rsg4392zcaf2y9gnrh0w62t578ez7p`
- `terra1t0vq0c9dwmqpfuyu4xhqg5g5efh8asqhyy64gk`

**Matches found:** none in the searched native `transfer` or `wasm.from`/`wasm.to` records. Raw queries and empty match files are in `data/transfers/`.

The negative finding does not include transfers mediated by unknown intermediaries, other chains, exchanges, or accounts outside these explicit sets.

## 2. Recurring validator-to-ERIS payments

These are direct `MsgSend` transactions to the ERIS validator/grant recipient. They are **not** transfers to the five fixed-multisig signer addresses.

| Date (UTC) | Galactic Punks → ERIS | Lion DAO → ERIS |
|---|---:|---:|
| 5 Feb | [9,559](https://chainsco.pe/terra2/tx/4BAA58BB5F32BDF0A6DF96CBDBF9A835B47A7F0ACBC49FF66B95267043A70851) | [8,859](https://chainsco.pe/terra2/tx/C13FC82C3E57FA01DA98E0C8BB3C78F8F4433649538CC8D02A0A49A91BCD4F44) |
| 20 Feb | [10,338](https://chainsco.pe/terra2/tx/59D56C13BB9251E3E42E48903B4B6586639B1DF44D0C4BAD07E40044812C66D8) | [9,523](https://chainsco.pe/terra2/tx/C056284E0CA32BA5A7833E1BE266EF5DD621DB2B727AD3107DE3E685AF87550C) |
| 10 Mar | [8,608](https://chainsco.pe/terra2/tx/CDD304F215808F3746F609642A39F7350269AFF9C16E5A0558759F4BB8FF79E8) | [8,126](https://chainsco.pe/terra2/tx/59829352DFA1E7D084DA5E64C284D40A60D2DABBC269992F5D800324FD1E040B) |
| 13 Apr | [11,339](https://chainsco.pe/terra2/tx/953F30F2B206C731CE8C082523E97232844B5A10E52D4E0EC44D4629FB0A0F26) | [10,359](https://chainsco.pe/terra2/tx/CC856F170BEC2BF78AE32591BBBAC1DDF77D4509263ADD1F567EB6B9B019B7EC) |
| 14 May | [9,454](https://chainsco.pe/terra2/tx/F59143F1EE77BA1814E4461BD7A8E12CCF915D7B8A756032C2F919D7547F1EE1) | [8,537](https://chainsco.pe/terra2/tx/22160ACD93A568D601B1E6E0701B35918719EF3694960DBD25990B88CA112CEF) |
| 17 Jun | [11,442](https://chainsco.pe/terra2/tx/B0110C4EAF591D149ADF791EC26BDDEDF38DF780C52E292CF2671915A0DD3D54) | [10,448](https://chainsco.pe/terra2/tx/C38430934A68E3190834217E44BD282C3E3368ACA4E5BA802C8723EEB9519DEF) |
| 21 Jul | [12,884](https://chainsco.pe/terra2/tx/B1B791C9227C1ADDDC5B1E7073D776AFF51584C5622E307EA7319199DDBDD213) | [11,889](https://chainsco.pe/terra2/tx/EC387A1CC216CA57664C7C74C5DEF18990915D76B1E31BB95E6785C2B671C9E5) |
| 18 Aug | [13,290](https://chainsco.pe/terra2/tx/553B9BD95F3145F349CFE42760E1E5376CE3D76A2CDC240200E942275051117D) | [12,448](https://chainsco.pe/terra2/tx/905C272C8C00140B0B51231994B82AB98549DC130E2849F8A059EC2808DC9E6D) |
| 16 Sep | [14,556](https://chainsco.pe/terra2/tx/28E06296F03C506121EBDE15697D138DA183906B09261EB80844B6FCD2AE4093) | [12,384](https://chainsco.pe/terra2/tx/88BDA63A50EFF45EAB125B4F86255A70E696C333FD010C3E5AB3B6EA7619CA9B) |
| 19 Oct | [15,265](https://chainsco.pe/terra2/tx/C940EBF82897A30739149AE35316C0E4A8019D18BD7BEC0998DE1E2C9B9E22E2) | [12,654](https://chainsco.pe/terra2/tx/B77EAB89F4F3CB9F99E0CB6FFEE29446EE8E2195BB7BEB212C24D5BC1559EC5C) |
| **Total** | **116,735 LUNA** | **105,227 LUNA** |

The amounts are in LUNA, not USD. Both series occur on the same dates, minutes apart. All 20 original transaction responses are preserved in `data/transfers/monthly_validator_to_eris/` and the four initially inspected records also have `_archive.json` copies under `data/transfers/`.

### Interpretation

This is evidence of an **ongoing economic relationship**, potentially a service, infrastructure, commission-sharing, or other operating arrangement. The synchronized cadence and rising amounts make it materially different from an isolated grant or one-off payment.

It does not, without an agreement or invoice, establish:

- that the payments purchase validator hosting;
- that ERIS controls validator keys or governance votes;
- that payments are for voting in a particular direction;
- that either validator is owned by ERIS.

A useful next step is to obtain the underlying service agreement and compare each payment to validator commission income and any delegation-program terms. The transfers should be disclosed when evaluating these validators’ votes on ERIS-connected proposals.

## 3. Treasury payments to the 50-weight signer: OTC, not compensation

The 50-weight signer `terra1alxk…l9c` received **795,991.566014 LUNA** from Treasury across ten transactions. Original messages identify them as `execute_otc` calls with memo `www.erisprotocol.com`.

| OTC offer | Signer supplied | LUNA received | Interpretation |
|---|---:|---:|---|
| 91 | 0.13130679 WBTC | 158,523.586975 | Tranche of a larger LUNA→WBTC offer. Not a grant. |
| 106 | 11,000 USDC | 212,970.771890 | Three tranches. Not duplicate compensation. |
| 111 | 22,623.438571 USDC | 424,497.207149 | Six tranches. Not duplicate compensation. |

The original transactions are in `data/treasury/signer_payments/`; offer terms are in `data/treasury/actions/91.json`, `106.json`, and `111.json`.

### Governance relevance

- These are still **related-party trades** and should be reviewed for price, slippage, and consistency with independently quoted rates.
- Repetition is explained by tranche execution, not by repeated salary entitlements.
- The signer’s own tranches are below 50,000 USDC, but the full offers are approximately 49,568 USDC, 50,000 USDC, and 70,000 USDC. Review should use the whole offer and related actions when applying oversight thresholds. The current records do not prove deliberate threshold-splitting.
- Gross LUNA outflow should not be added to grant, payroll, or “income to multisig participant” totals.

## 4. Recurring compensation and selective October exclusion

### Actual recurring amounts through 24 October

| Recipient | Recurring pattern observed |
|---|---|
| Philipp | 8,640 USDC ten times, plus a separate 5,000-USDC migration-app action |
| MB | 5,640 USDC ten times, including two entitlement claims 27 seconds apart on 29 August, plus 696 USDC |
| Rose | 4,575 USDC six times, then 4,800 USDC four times, plus 95.70 USDC |
| A272-targeted member | 5,000 USDC nine times through 15 September; 16,900-USDC audit payment; recurring 400/440/485-USDC infra payments |
| Other recurring recipients | 5,000-USDC core payments, 3,000-USDC comms payments, and 1,500-USDC ambassador payments |

### Action 100 resolves MB’s same-day claims

Action 100, `stewardship payments (2026-07-01 - 2026-10-01)`, contains three separate monthly entitlements for each director. MB’s two 29 August claims were different entries in that schedule, not proof of an accidental duplicate. All three 5,000-USDC entitlements for the A272-targeted member were paid by 15 September.

### October actions show selective exclusion

- Action 118: Philipp, 8,640 USDC, done.
- Action 119: Rose, 4,800 USDC, done.
- Action 120: MB, 5,640 USDC, done.
- No new October Stewardship action for the A272-targeted member appears in the inventory through action 121.
- Actions 97 and 121 separately provide that member 485-USDC infra payments.

This supports a finding of **exclusion from the new Stewardship compensation round**. It does not establish the reason, that the earlier schedule was unpaid, or that a future payment cannot be created.

## 5. Large related-party grants and one-offs

| Action | Recipient and terms | Governance relevance |
|---|---|---|
| Creda, action 72 | 40,000 kickoff + 100,000 mainnet + 60,000 eMode/isolation + 10,000 analytics = **210,000 USDC**, all marked claimed | Philipp proposed and voted on A209/A215; each passed with exactly 75 YES weight. |
| Estima, action 112 | 45,000 kickoff + 45,000 mainnet + 35,000 analytics/integration = **125,000 USDC total schedule** | A266 was approved without Philipp; A271 released the first 45,000 with Philipp in the minimum passing set. |
| Solid audit, action 102 | **16,900 USDC** to the A272-targeted member’s address | The member proposed and voted on A249. A272 alleges an agreed recusal was breached; the chain proves participation, not the alleged agreement. |
| Migration, action 110 | **100,000 USDC** to the operations/liquidity address | Should be classified as operational liquidity, not personal compensation, without further recipient evidence. |

Other large LUNA and virtual-asset transfers should not be treated as USD-equivalent expenses without asset identification, decimals, and valuation at execution time. Some are liquidity deployments or protocol operations rather than compensation.

## 6. Patterns worth investigating next

### A. Beneficiary versus decider

Match every payment recipient to the proposal author, YES voters, executor, and anyone who verified the milestone. A payment can be validly approved and still lack independent oversight.

### B. Gross versus net flows

Separate:

- grants and compensation;
- OTC purchases and sales;
- liquidity deployment;
- reimbursements;
- fee distributions;
- internal transfers between controlled wallets.

Do not add upstream project funding and downstream distributions as if both were income.

### C. Entitlement period versus claim date

Use the action’s `claimable_after_s` values. Multiple claims on one day can represent different months. A missing calendar-month claim does not automatically mean an entitlement was withheld.

### D. Payment exclusion and replacement

Compare each new action roster with the prior roster. The October exclusion is visible only because actions 118–120 were compared with action 100 and the A272-targeted member’s separate infra actions.

### E. Price and execution quality

For OTC trades, compare execution rate, timestamped independent market price, slippage, tranche sizes, and whether a related party received preferential allocation.

### F. Oversight thresholds

Aggregate related tranches, milestone stages, and same-project actions before deciding whether they fall above the Directive’s 50,000/150,000-USDC review levels. Splitting is not established merely because several small transactions exist.

### G. Admin and owner influence over future payments

Current payment history does not prove future safety. Review who can change recipients, create actions, cancel schedules, replace contract code, or redirect fees. These powers are separate from multisig membership.

### H. Off-chain agreements and missing metadata

The monthly validator transfers have no memo. Request the service agreement, invoices, pricing formula, and governance disclosure rather than inventing a purpose from the amount pattern.

### I. Recipient continuity

Track previous and current wallets without assuming exclusive custody. Reconcile MB’s prior/current addresses and the A125 seat replacement before calculating lifetime totals.

### J. Delivery and valuation

For every grant, retain the statement of work, cost basis, competing quote where relevant, measurable deliverable, independent acceptance evidence, and any post-payment performance metric.

## 7. Local evidence map

- `data/payment_summary.json` — compact summary and 20 monthly payment rows.
- `data/treasury/outbound_all_tx_responses.json` — 169 raw Treasury transactions.
- `data/treasury/outbound_transfers.csv` — 170 outbound transfer events.
- `data/treasury/actions/` — payment, milestone, and OTC terms, including actions 72, 91, 97, 100, 106, 111, 118, 119, and the full inventory.
- `data/treasury/claims/` — close-together payment claims.
- `data/treasury/signer_payments/` — all ten OTC transactions involving the 50-weight signer.
- `data/transfers/` — validator/signer queries and special transfer originals.
- `data/transfers/monthly_validator_to_eris/` — all 20 monthly payment originals.
- `analysis/treasury_patterns.py`, `analysis/eris_incoming_patterns.py` — repeatable grouping and CSV exports.

## 8. Remaining evidence requests

1. The agreement or pricing formula behind the monthly Galactic Punks/Lion DAO payments to ERIS.
2. The approval and disclosure history for that arrangement, including whether it predates 4853.
3. Any explanation for omitting the A272-targeted member from the October Stewardship round while continuing infra payments.
4. Independent market-rate checks for the related-party OTC offers.
5. A payment-action export that includes every recipient, entitlement period, claim, cancellation, and executed transaction for independent reconciliation.
