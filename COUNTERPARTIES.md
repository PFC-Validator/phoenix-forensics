# Significant counterparty wallets

This is an address-level relationship map for forensic accounting. It does not infer identities or common ownership. “OTC” means an asset exchange, not compensation. “Operations” means proposal execution, liquidity deployment, or protocol activity rather than an ordinary payment.

## Highest-priority relationships

| Address | Documented relationship and why it matters |
|---|---|
| `terra1rgggsspquaxjp4lmegx7a3q4l9lg44hnu7rjxa` | **ERIS protocol fee account**, identified by the hub’s `fee_config.protocol_fee_contract`. Sent Rebel **7,500 USDC** with memo `invoice` on 7 June 2026. This is a direct commercial relationship relevant to Think Tank independence. |
| `terra1l0ny38guhwrzczesgvk2zwj7xcen63jzmpusjv9hemvua9vptcyqwqy7pl` | **LA/operations recipient and proposal executor.** Received 100,000 USDC and 2.5 million LUNA in the 2026 transfer set, plus other assets. The checked transactions execute proposals 27, 29, 36, 40, and 44. Do not treat these gross flows as personal income. |
| `terra1y6hfmr3lxxj6srduhlfz96x7sga2984pr757a0nrfuqxa9rqxapqcjv4zz` | **Creda Portfolio contract**, not an unidentified person. It has substantial transfers with ERIS, including 20,000 and 9,662.817117-USDC withdrawals. The public contract registry identifies this address as Portfolio. |
| `terra1p3sea2vjewtr9ap4hv7nc75k5jc852ftf0w5u06wsk420y5urc9s9xtxdj` | **Transmuter/swap contract.** A 45,000-USDC transfer to ERIS was a `swap` message, not a payment to an individual. Related flows should be reconciled as asset exchanges and liquidity operations. |
| `terra1d4pvkg4skggnzcd6twx8qt6vsfaf0auw4dr9v9` | **PF operations address.** Received 35,000 USDC for Ethereum ASTRO OTC and 200,000 LUNA for Demex liquidity in the action inventory. It was also configured as `BURN_RECIPIENT` on 22 September 2026; the label alone does not prove burning. |
| `terra1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8pm7utl` | **Cosmos SDK distribution module account**, confirmed by deriving `sha256("distribution")[:20]` and Bech32-encoding it with the `terra` prefix. It appears in reward/commission events for many validators and is not a shared operations wallet or evidence of common ownership. |
| `terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg` | **Phoenix board DAO**, not a person. Received 500,000 LUNA in two 2026 transfers. All four board members have equal 25 weight and proposals require 75% approval. |
| `terra15l7567hhxttv2k5enmu4k8uez8e3cx3sxqfg6fsq4zzuwuzy2fqsjq00gr` | **Think Tank DAO.** Separate veto body with six equal voters and 66% threshold. Its role should be included when evaluating independent oversight of related grants. |

## Large OTC counterparties

These addresses received large LUNA amounts from Treasury, but the checked messages are `execute_otc`. They are counterparties in asset exchanges, not demonstrated compensation recipients.

| Address | Gross LUNA received | Offer IDs / classification |
|---|---:|---|
| `terra1alxk3fmhcl0ga80gl9yj9zp3ezjm4sdh8a9l9c` | 795,991.566014 | 50-weight ERIS signer; offers 91, 106, 111. Related-party trades requiring price review, not salary. |
| `terra1cv3rpu6eec50ftvaenww3qerm8ajxvpkjupd4l` | 1,644,033.154828 | Offers 106 and 111; multiple tranches. Role not established. |
| `terra1wlfagw79h0tushlz7uhvg3kxg5qq6zeg6axazf` | 1,270,812.326939 | Offers 92 and 105; multiple tranches. Role not established. |
| `terra1jr9868jj8yevqsal3ac63c82zgntame3u2lj8m` | 731,487.038374 | Offer 88; two tranches. Role not established. |
| `terra1yct7ls8kw3x2ucm66rxg7mgtyvw7kr5v4t4xsx` | 568,266.376727 | Offer 92; three tranches. Role not established. |
| `terra1625fll40qld9wvypc2jfc2rwrhe9732vdky9cx` | 358,701.106753 | Offer 91; three tranches. Role not established. |
| `terra14p3mc04s7jcaxvvetlzehvhx9gdx6w4nm3zzw3` | 237,323.047934 | Rose’s board wallet; offer 91 with 0.19657723 WBTC supplied. Not compensation. |

These flows should be valued using the supplied asset and execution-time price. LUNA totals alone do not establish expense, gain, or loss.

## Recurring contributor-payment addresses

The Treasury action history and 2026 transfers show recurring payment relationships beyond the four directors:

| Address | Pattern in retrieved records |
|---|---|
| `terra1azcpczz2jfysyl6m3wx3scpunt4lgcujpkyzt2` | **65,000 USDC** across 13 payments of 5,000, labeled core payments in the action inventory. |
| `terra12jrvhyc4fn2zvhcw8t7cnyy2udgpvdcm8g7egn` | **32,500 USDC** across 11 payments, primarily 3,000 each, labeled comms payments. |
| `terra1ez76cl0ldavltjuakex0sjpjrwhdedt2mclsxu` | **14,500 USDC** across ten payments, primarily 1,500 each, labeled ambassador payments. |
| `terra1lqqsydqeeccndxcaatgryf4ra8ujnrluk5meqs` | Recurring 1,800-USDC moderator-payment schedules in the action inventory. |
| `terra1xtyq8trkwwvpyjf4z0vltyr0c260pnnfm8vy68` | Recurring 1,500-USDC moderator-payment schedules in the action inventory. |

These are material recurring expenses to reconcile against contracts, work product, and independent approval. Address labels describe action names, not identity attribution.

## Other grant and operations recipients

The action inventory identifies additional significant recipients that should be kept separate from payroll and OTC flows:

| Address | Action / amount / classification |
|---|---|
| `terra1fnyxf85yd7z5wvwa2fxxspynh40ex9ajlgjr4dg7s9f6rhjma0uqfqr650` | Action 16: **70,000 USDC** legal-contingency fund. |
| `terra1dgmanyfy7ch3qn0g6fvpm6e60pwxdheuujfkee` | Action 11: **15,000 USDC** across two Solid milestones. |
| `terra18xcx0vq9szk4kczgk289g3l9t9yt70t4ygkg9z` | Action 21: **50,000 USDC** across two Boost milestones. |
| `terra1hc3pepchfrf86wpfwm7vrw4d9t6y903cc6lr8m` | Action 33: **50,000 USDC** Streamweave launch milestone. |
| `terra18gqpvh0vktgqena9728zuharqhc4628w9muwjw` | Action 32: **30,000 USDC** LA Secondary Frontend milestones; also a current Think Tank member. |
| `terra1yu2wca4v3kkx8sq58ury249lkzhq5y43rk557srsqrnawtfcl3yqe9j895` | Action 19: **20,000 USDC** Ophir DAO audit grant, cancelled rather than paid. |
| `terra1l0ny38guhwrzczesgvk2zwj7xcen63jzmpusjv9hemvua9vptcyqwqy7pl` | Action 27: LA participation; action 103: 1,000,000 LUNA transfer; action 110: 100,000 USDC migration. Operational classification required. |

## Contracts and administrative addresses that should not be treated as people

- `terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5` — Phoenix Treasury.
- `terra1hwxg6s732eparz3ys7sa4t5f64ngpd2w8syrca6z7ckv3fs9uqnsvrpcqa` — TLA permissions registry.
- `terra10788fkzah89xrdm27zkj5yvhj9x3494lxawzm5qq3vvxcqz2yzaqyd3enk` — ERIS staking hub and source of delegations to YES and VETO validators.
- `terra1e0mrzy8077druuu42vs0hu7ugguade0cj65dgtauyaw4gsl4kv0qtdf2au` — CW20-ICS20, whose admin moved to the Phoenix board with the hub in ERIS proposal 9.
- `terra1e9zwkd9epy8863d3ezmp5m4fsf95ceknhtmadwjt9rukvf8wtflstlecx8` — ERIS fixed multisig with 70/90 threshold.
- `terra1q0vny4wx2pfteh9zq323wh48c654xacpfq5tew` — retained migration admin on Treasury and the TLA registry.
- `terra1kefa2zgjn45ctj32d3tje5jdwus7px6n2klgzl` — retained registry and hub configuration owner.

## Why these relationships matter

1. **Related-party execution:** beneficiaries, proposers, voters, and executors must be compared, not just payment recipients.
2. **Correct accounting classification:** OTC, swaps, proposal execution, protocol withdrawals, and validator commission are not interchangeable with compensation.
3. **Oversight coverage:** the Think Tank veto body, recurring contributors, operations wallets, and grant recipients all affect the completeness of an independence review.
4. **Role separation:** a contract or DAO address does not establish a person, employer, owner, or exclusive key holder.
5. **Disclosure gaps:** recurring commercial relationships with no memo or public agreement—especially monthly validator-to-ERIS payments—deserve explicit documentation. Protocol module accounts must be excluded from counterparty inference.

## Source records

- `data/treasury/large_operations_summary.json` and `data/treasury/large_operations/` — original large-transfer messages.
- `data/treasury/actions/` — action terms, recipients, milestones, and cancellation/done state.
- `data/transfers/relationship_*.json` — protocol withdrawal, swap, and commission originals.
- `data/eris_multisig/hub_config.json` — protocol fee-account and delegation configuration.
- `data/thinktank/` — veto-body membership and ballots.
- Creda’s public [contract registry](https://github.com/credafinance/creda-docs/blob/7b331d79039c8f33645816b7e978ab96c905b4f8/developers/contract-addresses.mdx), which identifies the Portfolio address.

## Unresolved evidence requests

- The agreement behind the monthly validator-to-ERIS transfers.
- Execution-time price and allocation details for the large OTC offers.
- Independent approval and cost/deliverable support for recurring contributor and grant payments.
- Role documentation for operational addresses not identified in public registries.
