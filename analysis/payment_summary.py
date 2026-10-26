#!/usr/bin/env python3
"""Generate the payment summary reproducibly from completed transfer/action captures."""
import json
from pipeline_utils import ROOT, load_json

ERIS = 'terra1vm5azhvaxeanc7auxh02y8jmxrk8tj93f6aywp'
SIGNER = 'terra1alxk3fmhcl0ga80gl9yj9zp3ezjm4sdh8a9l9c'
VALIDATORS = {
    'terra15lsftv92eyssjwkh2393s0nhjc07kryqeux5s6': 'Galactic Punks',
    'terra1pet430t7ykswxuyhh56d4gk6rt7qgu9as43fnu': 'Lion DAO',
}
transfers = load_json('data/transfers/to_eris_all_transfers.json')
monthly = []
for row in transfers:
    if row['sender'] not in VALIDATORS or row['denom'] != 'uluna':
        continue
    monthly.append({
        'txhash': row['txhash'], 'time': row['time'], 'height': row['height'],
        'sender': row['sender'], 'amount': row['amount'], 'denom': row['denom'],
        'validator': VALIDATORS[row['sender']], 'luna': row['amount'] / 1e6,
        'explorer': 'https://chainsco.pe/terra2/tx/' + row['txhash'],
    })
monthly.sort(key=lambda x: (x['time'], x['validator']))
assert len(monthly) == 20
monthly_totals = {name: sum(x['amount'] for x in monthly if x['validator'] == name) / 1e6 for name in sorted(set(VALIDATORS.values()))}

outbound = load_json('data/treasury/outbound_transfers.json')
otc_rows = [x for x in outbound if x['recipient'] == SIGNER and x['denom'] == 'uluna']
assert len(otc_rows) == 10
signer_otc = {
    'recipient': SIGNER,
    'gross_luna_received': sum(x['amount'] for x in otc_rows) / 1e6,
    'classification': 'OTC asset exchanges, not compensation',
    'transactions': [
        {'txhash': x['txhash'], 'time': x['time'], 'luna_received': x['amount'] / 1e6, 'explorer': 'https://chainsco.pe/terra2/tx/' + x['txhash']}
        for x in otc_rows
    ],
}
actions_after100 = load_json('data/treasury/actions/actions_after100.json')['data']
action120 = next(x for x in actions_after100 if x['id'] == 120)
summary = {
    'validator_to_multisig_native_matches': load_json('data/transfers/validator_multisig_native_matches.json'),
    'validator_to_multisig_wasm_matches': load_json('data/transfers/validator_multisig_wasm_matches.json'),
    'monthly_validator_to_eris': monthly,
    'monthly_totals': monthly_totals,
    'signer_otc': signer_otc,
    'october_stewardship_actions': {str(i): load_json(f'data/treasury/actions/{i}.json') for i in [97, 100, 118, 119]},
    'action_120': action120,
    've3_bribe_manager': load_json('data/counterparties/ve3_bribe_manager_flows.json'),
}
(ROOT / 'data/payment_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({'monthly_totals': monthly_totals, 'signer_otc_luna': signer_otc['gross_luna_received'], 'october_actions': [97, 100, 118, 119, 120], 've3_bribe_manager': summary['ve3_bribe_manager']['by_asset']}, indent=2))
