#!/usr/bin/env python3
"""Derive ampLUNA backing and governance exposure without assuming the 30M source."""
from decimal import Decimal, getcontext
import json
from pipeline_utils import ROOT, load_json

getcontext().prec = 40
hub = load_json('data/ampluna/hub_state.json')
holders = load_json('data/ampluna/holder_top40.json')
accounts = load_json('data/ampluna/top20_accounts.json')['accounts']
pol = load_json('data/ampluna/pol_multisig.json')
vamp = load_json('data/governance_4853/vamp_review.json')
bonds = load_json('data/ampluna/direct_hub_bonds.json')
D = Decimal
supply = D(holders['total_supply'])
backing = D(hub['data']['total_uluna'])
tvl = D(hub['data']['tvl_uluna'])
assumed = D('30000000000000')
rows = []
for index, (holder, account) in enumerate(zip(holders['holders'][:20], accounts), 1):
    balance = D(holder['balance'])
    rows.append({
        'rank': index, 'address': holder['address'],
        'balance_ampluna': str(balance / D(1e6)),
        'share_of_supply_percent': float(balance * 100 / supply),
        **account,
    })
result = {
    'confirmed': {
        'ampluna_total_supply': str(supply / D(1e6)),
        'total_uluna_backing': str(backing / D(1e6)),
        'total_uluna_tvl_including_unbonding_and_available': str(tvl / D(1e6)),
        'exchange_rate_uluna_per_ampluna': hub['data']['exchange_rate'],
        'holder_account_count': holders['account_count'],
        'top20_balance_ampluna': str(sum(D(x['balance_ampluna']) for x in rows)),
        'top20_share_of_supply_percent': sum(x['share_of_supply_percent'] for x in rows),
        'top20_accounts': rows,
        'pol_multisig': pol,
        'deployment_dao_direct_bonds': bonds,
        'governance_4853_at_capture': {
            'hub_current_vote': vamp['prop_gauge']['current_vote'],
            'gauge_yes_vp': vamp['prop_gauge']['yes_vp'],
            'gauge_no_vp': vamp['prop_gauge']['no_vp'],
            'gauge_nwv_vp': vamp['prop_gauge']['nwv_vp'],
            'gauge_abstain_vp': vamp['prop_gauge']['abstain_vp'],
        },
    },
    'community_backing': {
        'confirmed_direct_bonds_uluna': bonds['confirmed_deployment_dao_total_uluna'],
        'confirmed_direct_bonds_percent_of_current_backing': float(D(bonds['confirmed_deployment_dao_total_uluna']) * 100 / backing),
        'remaining_backing_not_attributed_by_this_analysis': str((backing - D(bonds['confirmed_deployment_dao_total_uluna'])) / D(1e6)),
        'caution': 'The full 30M proposal allocation was not all directly bonded. Gross historical bonds exceed current backing because of redemptions, sales and rebalancing; they cannot be assigned as current ownership.',
    },
    'governance_assessment': {
        'issue': 'Community-backed assets may affect native governance through the ampLUNA hub. This is a material conflict-of-interest and disclosure concern, not proof of capture or a completed improper vote. The confirmed direct deployment-DAO bond is 15M LUNA; other large gross bonders are separately identified in direct_hub_bonds.json.',
        'current_evidence_boundary': 'At the preserved 4853 capture the hub had no native ballot and all prop-gauge categories were zero. Potential influence and actual exercise are separate.',
        'required_controls': [
            'Publish community-backed ampLUNA balances and hub voting intentions before contract votes.',
            'Record deployment-DAO votes, recusals and the basis for any hub ballot.',
            'Separate upgrade admin, config owner, vote operator and deployment-DAO authority.',
            'Preserve independent validator ballots and disclose hub overrides.',
        ],
    },
}
(ROOT / 'data/ampluna/governance_backing_analysis.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'backing_luna': result['confirmed']['total_uluna_backing'], 'confirmed_deployment_dao_bond_share_percent': result['community_backing']['confirmed_direct_bonds_percent_of_current_backing'], 'top20_share_percent': result['confirmed']['top20_share_of_supply_percent'], 'hub_vote_at_capture': result['confirmed']['governance_4853_at_capture']['hub_current_vote']}, indent=2))
