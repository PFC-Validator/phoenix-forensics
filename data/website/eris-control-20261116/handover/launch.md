# Launching Terra Liquidity Alliance

- **Thread ID:** 24385
- **Author:** 0xPhilipp (`cosmos142v8lp8m8fgj3zegg9mzsq9k5n2z2r06cn04h5`)
- **Created:** 2024-08-12T08:46:56.607Z
- **Last edited:** 2024-08-12T18:52:56.915Z
- **Stage:** discussion
- **Views:** 2377
- **Reactions:** 4
- **Comments:** 16
- **Source:** https://common.xyz/terra/discussion/24385-launching-terra-liquidity-alliance

---

The Terra Liquidity Alliance is an innovative and forward-looking initiative designed to revitalize the Terra ecosystem, offering sustainable growth, community empowerment, and enhanced liquidity provisioning. We believe this proposal represents a critical step forward and invites the Terra community to join us in realizing this vision for the future of DeFi on Terra.

**Overview**

The Terra ecosystem has faced significant challenges in recent times, particularly with the recall of TFL-provided liquidity and the exploit of Axelar Assets. This has resulted in an all-time low in LUNA-Stablecoin liquidity on-chain.

To address these challenges and lay the foundation for sustainable ecosystem growth, we propose the launch of the Terra Liquidity Alliance, an advanced and powerful liquidity provisioning and DeFi solution that integrates innovative mechanics such as Alliance and ve-tokenomics.

On 6/8/24 the Terra community voted in support of funding for the development of the Liquidity Alliance development by ERIS protocol. [https://analytics.smartstake.io/terra/proposal/4813](https://analytics.smartstake.io/terra/proposal/4813)
This development work has now been completed and fully audited. 

[**Liquidity Alliance Proposal**](https://commonwealth.im/terra/discussion/20123-terra-liquidity-alliance)

[**Liquidity Alliance Documentation**](https://docs.erisprotocol.com/products/liquidity-hub/) 

[**Completed Contract Code**](https://github.com/erisprotocol/contracts-ve3) 

[**Completed Contract Audit**](https://github.com/SCV-Security/PublicReports/blob/main/Eris%20Protocol/ERIS%20-%20Contracts%20ve3%20-%20Audit%20Report%20v1.0.pdf)

**Objective**

Our primary goal is to bootstrap deep on-chain LUNA-Stablecoin liquidity and create a decentralized, community-driven mechanism for managing liquidity and project incentives on Terra. By doing so, we aim to increase chain activity, trading volume, and overall ecosystem engagement.

**Key Components**



1. **Implementation of ve(3,3) Tokenomics:**
    * Introduce voter escrow (ve) tokenomics to incentivize LPs, reduce token supply, and reward active ecosystem participation.
    * Promote efficient resource allocation and fair competition among Terra DEXes for liquidity and rewards.

2. **Bootstrapping LUNA-Stablecoin Liquidity:**
    * Target an initial liquidity depth of $10M for LUNA-USDC and LUNA-USDT pairs across Terra DEXes.
    * Whitelist additional LPs for ecosystem projects, allowing community-driven decisions on liquidity allocation.


3. **Creating New Utility and Revenue for LUNA Holders:**
    * Introduce mechanisms for LUNA holders to participate in voting, earn bribes, and benefit from rebase rewards, creating a positive feedback loop for ecosystem engagement.

4. **Building Protocol-Owned Liquidity (PoL):**
    * Implement a 10% annual take rate from LP staking to build community-owned liquidity, reducing reliance on incentives.


5. **Fair and Market-Based Incentive Mechanism:**
    * Allow DEXes to compete for Alliance Rewards, fostering a dynamic and decentralized liquidity provisioning environment.


6. **Integration with Alliance Module:**
    * Utilize staking rewards to incentivize LUNA-Stablecoin liquidity, driving increased chain activity and trade volume on Terra.

**Launch Plan**

The launch plan consists of configuring three new Alliances through the Alliance module. 

These are outlined below: 

**1. Stable Liquidity Alliance**: Propose an alliance with a share of 8% staking rewards for LUNA-Stablecoin liquidity



* Target liquidity: 5 M$
* Target APY: 50% (2.5 M$ incentives per year, 6.8k $ per day, ~21k LUNA per day @0.33)
* Reward weight: 10 % 
* The reward share will slowly increase from 0% to the target over the span of 3 months.
* Take rate of Alliance: 0%,
* Take rate of listed LPs: 10%, changeable by Phoenix Directive Stewardship
* Whitelisted assets: 
  * LUNA-USDC (native)
  * LUNA-USDT (native)
  * LUNA-SOLID

**2. Project Liquidity Alliance**: Propose an alliance with a share of 4% staking rewards for Terra Ecosystem liquidity



* Target liquidity: 2.5 M$
* Target APY: 50% (2.5 M$ incentives per year, 6.8k $ per day, ~21k LUNA per day @0.33)
* Reward weight: 5 % 
* The reward share will slowly increase from 0% to the target over the span of 6 months.
* Take rate of Alliance: 0%,
* Take rate of listed LPs: 10%, changeable by Phoenix Directive Stewardship
* Whitelisted assets: 
  * LUNA-ASTRO
  * LUNA-ROAR
  * LUNA-WHALE
  * LUNA-ampLUNA
  * LUNA-bLUNA
  * LUNA-stLUNA
  * LUNA-SWTH
  * USDC-SOLID

**3. Bluechip Liquidity Alliance**: Propose an alliance with a share of 4% staking rewards for bluechip liquidity



* Target liquidity: 2.5 M$
* Target APY: 50% (2.5 M$ incentives per year, 6.8k $ per day, ~21k LUNA per day @0.33)
* Reward weight: 5 % 
* The reward share will slowly increase from 0% to the target over the span of 6 months.
* Take rate of Alliance: 0%,
* Take rate of listed LPs: 10%, changeable by Phoenix Directive Stewardship
* Whitelisted assets: 
  * LUNA-wBTC
  * LUNA-wstETH
  * LUNA-wBNB
  * LUNA-ATOM
  * USDC-USDT
  * LUNA-INJ
  * LUNA-wSOL


Notes: 

- The parameters have been calculated by the yearly emission approximation of 100 M LUNA (~ $ 33 M)

- The target take rate of LP tokens will be based on the trading APR of the LP tokens and have a min take rate of 10%. This will be re-analyzed after the liquidity alliance was live for 3 months.

- Phoenix Directive will publish an application form to whitelist additional LP tokens. Any DEX on Terra and other ecosystem can apply for their pairs to be listed. 

- Delegations of virtual tokens will be distributed based on the delegation program recommendations until a new delegation program has been established.

- The proposed liquidity alliances will reduce the theoretical regular staking yield from ~19 % to ~16 %.

- Full Alliance parameter calculation: [Alliance Estimator](https://estimator.alliance.money/?importData=eyJhbGxpYW5jZUFzc2V0cyI6eyIxNzIzMjAyMTgwODY3Ijp7Im5hbWUiOiJST0FSIiwiaW5wdXRWYWx1ZXMiOnsibHNkQW5udWFsRXN0aW1hdGUiOiI1IiwiYXNzZXRQcmljZSI6IjAuMDAwMDAxMSIsImFsbGlhbmNlUmV3YXJkV2VpZ2h0IjoiMC4wMDQiLCJhbm51YWxpemVkVGFrZVJhdGUiOiIwIiwiYXNzZXRTdGFrZWRJbkFsbGlhbmNlIjoiMTAzNjI3MDk2MzUxIn19LCIxNzIzMjAyMzIxMjU4Ijp7Im5hbWUiOiJBbGxpYW5jZSBEQU8iLCJpbnB1dFZhbHVlcyI6eyJsc2RBbm51YWxFc3RpbWF0ZSI6IjAiLCJhc3NldFByaWNlIjoiMCIsImFsbGlhbmNlUmV3YXJkV2VpZ2h0IjoiMC4wMDgiLCJhbm51YWxpemVkVGFrZVJhdGUiOiIwIiwiYXNzZXRTdGFrZWRJbkFsbGlhbmNlIjoiMCJ9fSwiMTcyMzIwMjM5MTY5OSI6eyJuYW1lIjoiQ2hhaW4gQWxsaWFuY2UiLCJpbnB1dFZhbHVlcyI6eyJsc2RBbm51YWxFc3RpbWF0ZSI6IjAiLCJhc3NldFByaWNlIjoiMCIsImFsbGlhbmNlUmV3YXJkV2VpZ2h0IjoiMC4wMyIsImFubnVhbGl6ZWRUYWtlUmF0ZSI6IjAiLCJhc3NldFN0YWtlZEluQWxsaWFuY2UiOiIwIn19LCIxNzIzMjAyNDM0OTk3Ijp7Im5hbWUiOiJTdGFibGUgTGlxdWlkaXR5IiwiaW5wdXRWYWx1ZXMiOnsibHNkQW5udWFsRXN0aW1hdGUiOiIwIiwiYXNzZXRQcmljZSI6IjAiLCJhbGxpYW5jZVJld2FyZFdlaWdodCI6IjAuMSIsImFubnVhbGl6ZWRUYWtlUmF0ZSI6IjAiLCJhc3NldFN0YWtlZEluQWxsaWFuY2UiOiIwIn19LCIxNzIzMjAyNDM1NTU3Ijp7Im5hbWUiOiJQcm9qZWN0IExpcXVpZGl0eSIsImlucHV0VmFsdWVzIjp7ImxzZEFubnVhbEVzdGltYXRlIjoiMCIsImFzc2V0UHJpY2UiOiIwIiwiYWxsaWFuY2VSZXdhcmRXZWlnaHQiOiIwLjA1IiwiYW5udWFsaXplZFRha2VSYXRlIjoiMCIsImFzc2V0U3Rha2VkSW5BbGxpYW5jZSI6IjAifX0sIjE3MjMyMDI0MzU4NzUiOnsibmFtZSI6IkJsdWUgTGlxdWlkaXR5IiwiaW5wdXRWYWx1ZXMiOnsibHNkQW5udWFsRXN0aW1hdGUiOiIwIiwiYXNzZXRQcmljZSI6IjAiLCJhbGxpYW5jZVJld2FyZFdlaWdodCI6IjAuMDUiLCJhbm51YWxpemVkVGFrZVJhdGUiOiIwIiwiYXNzZXRTdGFrZWRJbkFsbGlhbmNlIjoiMCJ9fX0sIm5hdGl2ZUlucHV0VmFsdWVzIjp7ImNvbHVtbk5hbWUiOiJOYXRpdmUgQXNzZXQiLCJpbmZsYXRpb25SYXRlIjoiNyIsImxzZEFubnVhbEVzdGltYXRlIjpudWxsLCJ0b3RhbFRva2VuU3VwcGx5IjoiMTIwMDAwMDAwMCIsImFzc2V0UHJpY2UiOiIwLjMzIiwiYWxsaWFuY2VSZXdhcmRXZWlnaHQiOiIxIiwiYXNzZXRTdGFrZWRJbkFsbGlhbmNlIjoiNDIzNTc1MDAwIiwiZGVub20iOiJMVU5BIn19)

**Access Rights can be validated on-chain**

[terra1hwxg6s732eparz3ys7sa4t5f64ngpd2w8syrca6z7ckv3fs9uqnsvrpcqa](https://chainsco.pe/terra2/address/terra1hwxg6s732eparz3ys7sa4t5f64ngpd2w8syrca6z7ckv3fs9uqnsvrpcqa/state)

* **Contract Admin**: Is allowed to migrate contracts
* **Owner**: Is allowed to change technical configurations in contracts
* **ASSET_WHITELIST_CONTROLLER**: Is allowed to change whitelisted assets (LP tokens) on the staking contract, which voters are allowed to vote for.
* **BRIBE_WHITELIST_CONTROLLER**: Is allowed to change whitelisted assets that can be used as bribes on the bribe-manager
* **DELEGATION_CONTROLLER**: Is allowed to control delegation of alliance-connectors.
* **FEE_COLLECTOR**: Is receiving fees from adding bribes
* **TAKE_RECIPIENT**: Is receiving the take rate from asset-staking
* **VE_GUARDIAN**: Is able to blacklist malicious voters in case of emergency
* **FREE_BRIBES**: Is allowed to add bribes to the bribe-manager without paying a fee
* Contract registry:
  * ASSET_GAUGE
  * ASSET_STAKING__bluechip
  * ASSET_STAKING__project
  * ASSET_STAKING__stable
  * BRIBE_MANAGER
  * VOTING_ESCROW
  * CONNECTOR__bluechip
  * CONNECTOR__project
  * CONNECTOR__stable

**Wallets**


* **Phoenix Directive Stewardship**: terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg
* **Owner**: ERIS wallet terra1kefa2zgjn45ctj32d3tje5jdwus7px6n2klgzl, Ownership transferred to PD Stewardship after 3 months.
* **Admin**: ERIS wallet terra1q0vny4wx2pfteh9zq323wh48c654xacpfq5tew, Contract Admin will be transferred to PD Stewardship after 1 month.

**Note: Terra IBC Exploit - Recovery Plan**

The IBC exploit does not have a big impact on Liquidity Alliance, as whitelisted assets will start with native USDC / USDT variants which were not exploited. There has been ongoing work led by the Phoenix Directive together with other key ecosystem partners to resolve this. We expect that and a governance proposal will be posted soon.

[https://x.com/phoenix_dir/status/1821040630988206588](https://x.com/phoenix_dir/status/1821040630988206588)

---

## Comments (16)

**Razzien (`terra1ja7w3eccf5n8qz0vrn2e2w39n546rh52mnlcmr`)** — 2024-08-12T10:24:55.667Z (edited 2024-08-14T14:15:46.265Z) — 👍 2

I do Like allot this proposal!
But i Would add more 2 pools on BlueChips
Luna-Inj and Luna-wsol

Eitherway i support this proposal :)

**miscellaneoushonor66 (`terra1q6a7twpytu4hw6mzwu8l38nvdmtvd8wet4n77h`)** — 2024-08-12T14:15:08.876Z (edited 2024-08-14T14:15:25.199Z) — 👍 3

Thank you for the initiative and proposal.

However, kindly consider LUNA-SWTH for Project Liquidity Alliance under Whitelisted assets.

Though it is not a direct Terra project, it has demonstrated a good partnership with Terra by being one of the first to integrate the Terra Alliance module. Demex has a LUNA perpetual market for trading and their Nitron money market has LUNA, ampLUNA, stLUNA for lending and borrowing.

Having a continued partnership with your first partners Migaloo and Carbon would continue to foster a good relationship and benefits to all stakeholders.

**Anonymous (`terra1kt5wxtdjewnwlg68scjpknxaz0jgvzskxs3lta`)** — 2024-08-12T18:04:19.143Z

Carbon and Migaloo are good partner I also think Shade is also a good one maybe add Silk to the List. It is a great stablecoin. What is Terra without a decentralized stablecoin :)

**Anonymous (`terra1dyh999cuqjkhadpfhh878sar73mrzy65695309`)** — 2024-08-13T18:53:18.953Z (edited 2024-08-14T14:14:12.651Z) — 👍 1

I strongly support this proposal. Could you add LUNA-CAPA and LUNA-URA as whitelisted assets in Project Liquidity Alliance.

> **0xPhilipp (`cosmos142v8lp8m8fgj3zegg9mzsq9k5n2z2r06cn04h5`)** — 2024-08-20T07:13:30.950Z
> 
> URA still hasn't resolved the issue with their roadmap.
> CAPA makes sense to list, but more activeness from the project would be great.

> > **Anonymous (`terra1dyh999cuqjkhadpfhh878sar73mrzy65695309`)** — 2024-08-20T11:47:33.151Z (edited 2024-08-20T11:50:58.391Z)
> > 
> > [@0xPhilipp](/profile/id/58974) 
> > I believe you could be a valuable leader for the URA community. Given the Terra community's trust in you, I anticipate URA holders would also support your leadership. I think the community would propose allocating 10-15% of the total supply to the ERIs team to lead this project and establish this DEX as the Terra community's preferred platform.

**Qasim Saleem Qureshi (`cosmos17de5rquzac94s6xjn5pfcylsw8uwsp8syq2c3r`)** — 2024-08-14T11:17:38.464Z (edited 2024-08-14T14:13:52.418Z) — 👍 1

Totally support the above proposal and waiting to Vote on it.
kindly post it without any more delay.

Waiting to Vote on it ASAP

**Rose | Phoenix Foundation (`terra14cmsxkl9ynpvrqnqnvd7dv8ecnrdserhn3seme`)** — 2024-08-15T15:07:48.205Z (edited 2024-08-16T16:48:05.454Z) — 👍 2

Generally in support, and thank you for your work on this! 

I am just hesitant about whitelisting SOLID pools as the team has been MIA for a month. I have hope that they will stick around and maintain the protocol/dapp, but that's not enough to incentivise it imo. There needs to be a plan for it to be used more in Cosmos. 

Otherwise we may as well switch to another decentralised stablecoin like SILK from Secret, USC from Carbon or TOR if Thorchain decides to make that a tradeable asset. But choosing and incentivising one of those is a problem for another day.

> **Anonymous (`terra1nyau5wrqj500arqf6xncsum7f25dzqzhwl33k7`)** — 2024-08-15T19:27:46.837Z (edited 2024-08-16T16:48:03.552Z) — 👍 2
> 
> Hi, Rose. Here is my opinions.
> 
> I'm just a long-term SOLID user. And I hope the flourishing of countless dApps and the prosperity of Terra.
> 
> Several dApps have been struggling due to a lack of development funds following the shutdown of TFL operations and the IBC exploit, leaving them barely operational. 
> 
> SOLID is one of these cases, and adopting the Alliance is crucial. Given the current situation, how many dApps on Terra can realistically plan for the future? After the IBC exploit, SOLID holds significant value as the only stablecoin still functioning on Terra. Moreover, according to [@Daniel](/profile/id/99707) , the SOLID team is still active. 
> 
> I hope that supporting Alliance will help stimulate the activation of dApps within Terra.

> > **Rose | Phoenix Foundation (`terra14cmsxkl9ynpvrqnqnvd7dv8ecnrdserhn3seme`)** — 2024-08-15T23:18:03.302Z (edited 2024-08-16T16:47:56.225Z) — 👍 2
> > 
> > Fair call. Though it would be reassuring to see Daniel in the group chat more than once a month.

> > > **Anonymous (`terra1nyau5wrqj500arqf6xncsum7f25dzqzhwl33k7`)** — 2024-08-16T16:51:25.390Z
> > > 
> > > Thanks for your response, Rose.
> > > 
> > > I hope that these pools, which I propose, will support the Alliance:
> > > 
> > > 1) CAPA/LUNA in Astroport and Ura
> > > 2) CAPA/SOLID in Astroport and Ura
> > > 3) *USDC(noble)/SOLID in Astroport
> > > 
> > > *The USDC(noble)/SOLID pool is not official on Coinhall and needs to be audited.
> > > 
> > > [@Daniel](/profile/id/99707) , Could you confirm if you will apply these pools?

**Anonymous (`terra1nyau5wrqj500arqf6xncsum7f25dzqzhwl33k7`)** — 2024-08-18T19:51:43.963Z (edited 2024-08-20T12:02:44.809Z) — 👍 1

I strongly support this proposal. 
But may I have a question? I'm curious why it's wstETH instead of wETH.

> **0xPhilipp (`cosmos142v8lp8m8fgj3zegg9mzsq9k5n2z2r06cn04h5`)** — 2024-08-20T07:10:12.977Z (edited 2024-08-20T12:02:41.140Z) — 👍 1
> 
> Probably best to just use both. 
> 
> - wstETH provides additional value to LPs due to Lido staking rewards
> - wstETH is a better collateral for money markets / stablecoins like solid
> - wstETH provides opportunity to work with Lido / Neutron

> > **Anonymous (`terra1nyau5wrqj500arqf6xncsum7f25dzqzhwl33k7`)** — 2024-08-20T12:04:44.227Z
> > 
> > OK, I see. Thank you for your kind answer.

> > **Rose | Phoenix Foundation (`terra14cmsxkl9ynpvrqnqnvd7dv8ecnrdserhn3seme`)** — 2024-08-20T14:03:04.233Z
> > 
> > Will this be wstETH ibc-transferred directly from Neutron to Terra? As I recall before Neutron there was another version of wstETH in Cosmos but now the Neutron one is "canonical", right?

**Heisemberg (`terra16vzhe8500360lc8kp4hgapk8rk07ehucsuxa7v`)** — 2024-08-26T14:06:24.685Z

Excellent proposal, I believe that Terra without stablecoin is castrated, as if its soul is missing, perhaps we need to focus on a trusted stablecoin and give an alternative with Solid, but I notice little movement, we need to be active and work...

