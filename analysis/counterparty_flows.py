#!/usr/bin/env python3
"""Classify material protocol-contract counterparties without mixing assets."""
import json
from pipeline_utils import ROOT, USDC, load_json

ADDRESS = 'terra1tuuwm8yrj54qeg0c8xu00aha9ryatyhtczq8qq2q8tntuw0auzas9037wh'
FUEL = 'ibc/4B44179AC2F0BEE50C16A673B3B886398988692885B2848A1C8AEF27148B3961'
ASSETS = {'uluna': ('LUNA', 6), FUEL: ('FUEL', 6), USDC: ('USDC', 6)}
rows = [x for x in load_json('data/transfers/to_eris_all_transfers.json') if x['sender'] == ADDRESS]
assert rows and all(x['denom'] in ASSETS for x in rows)
responses = {x['txhash']: x for x in load_json('data/transfers/to_eris_all_tx_responses.json')}
for txhash in {x['txhash'] for x in rows}:
    messages = responses[txhash]['tx']['body']['messages']
    assert any('claim_bribes' in message.get('msg', {}) for message in messages)

by_asset = {}
for denom, (asset, decimals) in ASSETS.items():
    selected = [x for x in rows if x['denom'] == denom]
    by_asset[asset] = {
        'denom': denom,
        'transfer_events': len(selected),
        'total': sum(x['amount'] for x in selected) / 10 ** decimals,
        'october_2026': sum(x['amount'] for x in selected if x['time'].startswith('2026-10')) / 10 ** decimals,
    }
result = {
    'address': ADDRESS,
    'contract_label': 've3-bribe-manager',
    'classification': 'Protocol voting-incentive receipts through claim_bribes; not an unidentified personal wallet or ordinary payment sender.',
    'source_transaction_count': len({x['txhash'] for x in rows}),
    'first_receipt': min(x['time'] for x in rows),
    'last_receipt': max(x['time'] for x in rows),
    'by_asset': by_asset,
    'caution': 'Do not add LUNA, FUEL and USDC as if they were one asset. Contract receipts do not establish common ownership or personal income.',
    'transactions': rows,
}
(ROOT / 'data/counterparties/ve3_bribe_manager_flows.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'transactions'}, indent=2))
