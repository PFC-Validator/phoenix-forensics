# ERIS handover: promises, responses and completed actions

Research checked 16 November 2026, approximately 17:41–17:43 UTC. This is a bounded review of official public statements and retained chain evidence, not a complete inventory of every contract or private agreement. Fresh source URLs, retrieval timestamps and SHA-256 hashes are in `capture_manifest.json`. Raw forum captures are research inputs; do not publish them wholesale because they contain unrelated allegations and identifying user metadata. Use selected evidence and public role handles in authored website copy.

## What was promised

The 12 August 2024 TLA launch document names the ERIS configuration wallet `terra1kefa2zgjn45ctj32d3tje5jdwus7px6n2klgzl` and migration-admin wallet `terra1q0vny4wx2pfteh9zq323wh48c654xacpfq5tew`. It says ownership would move to PD Stewardship after three months and migration administration after one month. It separately defines migration, configuration, asset whitelist, bribe whitelist, delegation, fee collector, take recipient and emergency guardian powers. These are distinct permissions, not a single undifferentiated title to assets.

Original forum URL: https://common.xyz/terra/discussion/24385-launching-terra-liquidity-alliance
Official retained copy (freshly retrieved as `launch.md`): https://github.com/phoenix-directive/docs/blob/7cebbd26048f0e1568a2aed55177090b90788d8b/common_backup/2024-08-12_24385_launching-terra-liquidity-alliance.md#L164-L169

Scope caution: this is a TLA commitment. It should not automatically be applied to every ERIS product or every later Foundation contract. The original document also expressly identifies LP take rates as changeable by Stewardship. The subsequently published Treasury launch has its own protections and operational rationale.

The 26 September 2024 Treasury launch describes the Treasury as an audited open-source smart contract, funded via Alliance rewards. It specifies Think Tank and Terra governance spending-veto windows, quarterly reporting, governance's ability to stop future Alliance funding and governance dissolution/clawback. Its linked repository is `erisprotocol/contracts-ve3/tree/main/contracts/phoenix-treasury`.

Official retained copy (freshly retrieved as `treasury-launch.md`): https://github.com/phoenix-directive/docs/blob/7cebbd26048f0e1568a2aed55177090b90788d8b/common_backup/2024-09-26_25020_phoenix-directive-launching-treasury.md

The launch text is primary evidence of the represented safeguards. Its statements alone do not establish that every currently deployed version implements them exactly, or that source/build access is currently adequate.

## ERIS's explanation and the approval gap

On 19 October 2026 at 20:54:48 UTC, 0xPhilipp stated that ERIS retained TLA administration because it continued to develop, maintain and operate those contracts. He said unresolved concerns about the current Board made transfer inappropriate in the ERIS team's view, and welcomed an Emergency Supervisor examining the matter.

Source: https://forum.phoenix.money/t/47/55 (post ID 195; fresh full post in `topic-47-extra-20.json`).

This is an express explanation for retained authority and should accompany the concern. It does not itself identify a Board or Terra governance decision extending the one-/three-month timetable. The next response specifically requested who approved departure, under what authority and when: https://forum.phoenix.money/t/47/56 (post ID 196). Later requests appear at posts 59 and 100. In the reviewed thread no approval record answering those questions was identified. Say “no approved extension was identified in the reviewed records,” not “no extension exists” or a legal conclusion of wrongdoing.

On 2 November 2026, Vini supported administration of PF contracts and TLA sitting with Stewardship, and PF having source/maintenance documentation in its GitHub organisation with clear licensing and access. He expressly called it his individual view, not an agreed Board statement. Source: https://forum.phoenix.money/t/64/5 (post ID 287, `topic-64.json`). This is support for a handover, not an executed transfer or a binding collective decision.

The freshly captured latest removal/reform discussion (topic 72, 22 posts through 16 November 14:18 UTC) does not add an ERIS commitment to complete the handover. It does contain later proposal-author revisions that request a complete permissions inventory and operating/source-access dossier. Those are proposed requirements, not proof of compliance or breach.

## Completed handover: give it explicit credit

ERIS multisig proposal 8 had the title “Transfer Ownership of Amplifier and CW20-ICS20 to Phoenix Foundation” but is rejected. Proposal 9 carries the same title and is executed. Both contain exactly two Wasm `update_admin` messages targeting:

- ampLUNA hub `terra10788fkzah89xrdm27zkj5yvhj9x3494lxawzm5qq3vvxcqz2yzaqyd3enk`;
- CW20-ICS20 `terra1e0mrzy8077druuu42vs0hu7ugguade0cj65dgtauyaw4gsl4kv0qtdf2au`.

The new migration admin in both messages is the Phoenix Board `terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg`. Fresh proposal query: `eris-proposals.json`.

Proposal 9 was submitted 22 October 2026, transaction `8BD973209AD252D6D1226968387FE34C6F387F6B4A706BE2468E4A2C4ACE06FE`, and executed 25 October 2026 at 05:11:51 UTC in transaction `86E599263604B396BFB0F35F2F4E505E2EA758B024315B1C055C14994E6242D9`, height 23,442,759, execution code 0. Existing preserved transaction and RPC cross-check live under `data/eris_multisig/transactions.json` and `data/leads/rpc/terra2_86E599263604B396BFB0F35F2F4E505E2EA758B024315B1C055C14994E6242D9.json`.

Explorer: https://chainsco.pe/terra2/tx/86E599263604B396BFB0F35F2F4E505E2EA758B024315B1C055C14994E6242D9

A fresh transaction-by-hash request returned HTTP 500; a fresh RPC request returned 404. The execution date above therefore comes from the previously retained primary response and its original checks, while executed proposal status was freshly confirmed.

These messages transferred code-upgrade administration. They did not call the hub's internal ownership-transfer methods, change ICS20's `gov_contract`, or mention the Treasury/TLA registry. A complete account must give credit for the code-upgrade control now held by the Board. That is a powerful remedy/control layer even while internal settings remain elsewhere; it is inaccurate to imply ERIS retains unqualified exclusive control of these two contracts.

## A292: Board exercised the transferred upgrade authority

The fresh A292 query reports **executed**, 75 YES / 0 NO / 0 ABSTAIN, a single migration to code 2726 with `{}` payload. Fresh hub history shows code 2726 adopted at height 23,563,595. Files: `A292.json`, `hub-history.json`.

The existing focused 30 October review in `investigations/a292-code-review/REPORT.md` verified byte-for-byte identity of code 2726 with ERIS's March 2024 v1.8.0 publisher release, and code 1257 with v1.5.0. It tested selected exact-binary behavior, not a full security audit or independent source build.

That review found the upgrade preserves internal owner, fee configuration, vote operator and existing timings. It adds owner-controlled `epoch_period` and `unbond_period` updates. The added checks reject zero but impose no operational minimum/maximum or consistency check with chain staking unbonding beyond u64. Bad settings could disrupt batching or delay withdrawals. The internal owner already could change the governance vote operator, fee settings (reward-fee cap 10%), donation settings and delegation strategy. A normal governance vote requires the configured vote operator rather than ownership by itself.

Do not call this an unapproved ERIS code replacement or a covert new takeover: the Board approved and executed this upgrade using its newly received administration. The governance issue is whether the approved upgrade's additional owner powers were understood and whether intended policy/limits are published.

Primary source comparison: https://github.com/erisprotocol/contracts-terra/blob/dbcaa4db951f2bec6e239ccf94f25c85f3bed80a/contracts/hub/src/execute.rs#L852-L911

## Historical examples of retained permissions being used

Retained primary transaction records were read directly for these narrow facts:

- 8 October 2024 12:21:10 UTC, height 12,412,391, `B71CF351EB8A85620E18821288C35A4C73DD6B43B9751C08E937C8AC9FCEAF2F`, code 0: the ERIS configuration address executed registry `set_addresses`, assigning `PDT_CONFIG_OWNER` to itself. This demonstrates actual use of registry authority. It does not establish that this isolated action lacked off-chain authorization.
- 1 October 2025 11:27:33 UTC, height 17,655,127, `DC3118AA7A0A8BEC96AA7006074DF66A83321DEC0CEEDB2015B56AE83D80EB64`, code 0: that address set `FEE_COLLECTOR` to `terra1rgggsspquaxjp4lmegx7a3q4l9lg44hnu7rjxa`. Attribute only the specific role; this is not evidence that all Treasury funds or every TLA fee were transferred.

Primary preserved files: `data/leads/transactions/terra2_<hash>.json`, with source sidecars and RPC captures. Forum source locators are in https://forum.phoenix.money/t/47/54. The forum's broader allegations are not adopted here.

## Source access and evidence limits

Unauthenticated public GitHub API lookup of `erisprotocol/contracts-ve3` returned 404 on 16 November at 17:41 UTC, recorded in the capture manifest. This confirms public source could not be accessed through that location at review time; it cannot distinguish deletion, relocation or a private repository and does not establish that Foundation/auditor access is absent. The Treasury and TLA launch documents advertised public source at that repository.

Website conclusions should distinguish legal ownership, token balances, migration authority, current internal permissions, and operating/source access. Neither an admin address nor a grant proves ERIS legally owns all assets held by a contract. Retained authority may expose Treasury/users to loss, interruption, fee changes and dependency even without evidence of intentional abuse. Documented safeguards must be assessed against every privileged layer; a threshold inside replacement code is not an immutable restriction on a migration administrator.
