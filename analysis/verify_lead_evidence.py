#!/usr/bin/env python3
"""Read-only verification of captured primary records and supplemental accounting."""
import base64
import hashlib
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path
from collect_lead_transactions import ROOT, BASE, EVM
from integrate_lead_evidence import AMP, ARB, BOARD, CERES, ESCROW, TRANSFER, attributes, one
from pipeline_utils import parse_coins


def load(path):
    return json.loads((ROOT / path).read_text())


manifest = load('data/leads/capture_manifest.json')
records = load('data/leads/transactions.json')
transfers = load('data/leads/transfers.json')
unquantified = load('data/leads/unquantified_transfer_events.json')
findings = {r['id']: r for r in load('data/leads/verified_findings.json')['findings']}
requested = load('data/leads/requests.json')['transactions']
checksummed = set()
for line in (BASE / 'SHA256SUMS').read_text().splitlines():
    digest, relative = line.split('  ', 1)
    path = BASE / relative
    assert path.resolve().is_relative_to(BASE.resolve())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, relative
    checksummed.add(relative)
assert checksummed == {p.relative_to(BASE).as_posix() for p in BASE.rglob('*') if p.is_file() and not p.name.endswith('.source.md') and p.name != 'SHA256SUMS'}
assert {(r['chain'], r['hash']) for r in requested} == {(r['chain'], r['hash']) for r in manifest['transactions']}
assert all(1 <= i <= 59 for r in requested for i in r['lead_ids'])
success = {(r['chain'], r['hash']): r for r in manifest['transactions'] if r['status'] == 'successful_primary_record'}
assert set(success) == {(r['chain'], r['hash']) for r in records}
raw_docs = {}
for r in success.values():
    raw = (ROOT / r['file']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == r['sha256']
    d = json.loads(raw)
    raw_docs[(r['chain'], r['hash'])] = d
    if r['chain'] in EVM:
        assert int(d['result']['status'], 16) == 1
        assert d['result']['transactionHash'].lower() == r['hash']
    else:
        assert int(d['tx_response']['code']) == 0
        assert d['tx_response']['txhash'].upper() == r['hash']
for meta in list((BASE / 'transactions').glob('*.capture.json')) + list((BASE / 'queries').glob('*.capture.json')) + list((BASE / 'rpc').glob('*.capture.json')):
    r = json.loads(meta.read_text())
    assert hashlib.sha256((ROOT / r['file']).read_bytes()).hexdigest() == r['sha256']
checks = load('data/leads/rpc_manifest.json')['checks']
for r in checks:
    assert r['status'] == 'tx_bytes_hash_and_execution_match', r
    rpc = load(r['file'])['result']
    assert hashlib.sha256(base64.b64decode(rpc['tx'], validate=True)).hexdigest().upper() == r['hash']
    lcd = load(r['lcd_file'])['tx_response']
    assert rpc['height'] == lcd['height'] and int(rpc['tx_result']['code']) == int(lcd['code']) == 0
assert {r['hash'] for r in checks} == {r['hash'] for r in records if r['chain'] == 'terra2'}
seen = set()
for r in transfers:
    key = (r['chain'], r['hash'], r['event_index'], r['asset'])
    assert key not in seen, key
    seen.add(key)
    assert r['amount_base'].isdigit()
    if r['decimals'] is None:
        assert r['amount_display'] is None
    else:
        assert Decimal(r['amount_display']) * Decimal(10) ** r['decimals'] == int(r['amount_base'])
    d = raw_docs[(r['chain'], r['hash'])]
    if r['asset_kind'] == 'erc20':
        e = d['result']['logs'][r['event_index']]
        assert e['topics'][0] == TRANSFER and e['address'] == r['asset']
        assert '0x' + e['topics'][1][-40:] == r['sender']
        assert '0x' + e['topics'][2][-40:] == r['recipient']
        assert int(e['data'], 16) == int(r['amount_base'])
    else:
        e = d['tx_response']['events'][r['event_index']]
        a = attributes(e)
        if r['asset_kind'] == 'native':
            assert e['type'] == 'transfer'
            assert one(a, 'sender') == r['sender'] and one(a, 'recipient') == r['recipient']
            assert any(c['denom'] == r['asset'] and c['amount'] == int(r['amount_base']) for c in parse_coins(one(a, 'amount')))
        else:
            assert e['type'] == 'wasm' and one(a, '_contract_address') == r['asset']
            assert one(a, 'from') == r['sender'] and one(a, 'to') == r['recipient']
            assert one(a, 'amount') == r['amount_base']
# Every nonempty native transfer is represented once per denomination. Empty
# events are preserved explicitly rather than silently skipped or made zero.
expected = set()
empty = set()
for (chain, h), d in raw_docs.items():
    for i, e in enumerate(d.get('tx_response', {}).get('events', [])):
        if e['type'] != 'transfer':
            continue
        a = attributes(e)
        if one(a, 'amount') == '':
            empty.add((chain, h, i))
        else:
            expected.update((chain, h, i, c['denom']) for c in parse_coins(one(a, 'amount')))
assert expected == {(r['chain'], r['hash'], r['event_index'], r['asset']) for r in transfers if r['asset_kind'] == 'native'}
assert empty == {(r['chain'], r['hash'], r['event_index']) for r in unquantified}
locks = load('data/leads/voting_locks.json')
assert len(locks) == 8 and len({r['token_id'] for r in locks}) == 8
for r in locks:
    events = raw_docs[(r['chain'], r['hash'])]['tx_response']['events']
    funding = attributes(events[r['funding_event_index']])
    created = attributes(events[r['event_index']])
    assert one(funding, '_contract_address') == AMP and one(funding, 'from') == BOARD and one(funding, 'to') == ESCROW
    assert one(funding, 'amount') == r['amount_base']
    assert one(created, 'owner') == r['owner'] and one(created, 'token_id') == r['token_id']
    assert one(created, 'lock_end') == 'permanent'
assert findings['phoenix_A43_locks']['facts']['total_ampLUNA'] == '83000'
assert findings['phoenix_A43_locks']['facts']['recipient_yes_weight'] == 75
assert findings['phoenix_A33_locks']['facts']['total_ampLUNA'] == '21600.000001'
assert findings['superbolt_distribution']['facts']['yes_ballots'] == 3
assert findings['superbolt_distribution']['facts']['recipient_yes_ballots'] == 3
assert findings['superbolt_distribution']['facts']['total_USDC'] == '90000'
assert findings['receipt_redemption']['facts']['ampLUNA_total'] == '2383.589113'
assert findings['receipt_redemption']['facts']['gas_fee_share_LUNA'] == '0.01066'
assert findings['restriction_assignment']['facts']['seconds_between'] == 1342352
assert findings['ceres_removal_rebalance']['facts']['seconds_after_removal'] == 40
assert findings['ceres_removal_rebalance']['facts']['total_LUNA'] == '1680127.496132'
assert findings['ceres_removal_rebalance']['facts']['from_removed_validator_LUNA'] == '662828.893153'
assert [r['LUNA_component'] for r in findings['creda_reserve_collections']['facts']['collections']] == ['5701.254836', '2679.750683']
assert len(findings['compounder_fee_samples']['facts']['fee_transfers']) == 2
assert {r['asset'] for r in findings['compounder_fee_samples']['facts']['fee_transfers']} == {AMP, ARB}
assert int(load('data/leads/queries/base_chain_id.json')['result'], 16) == 8453
assert int(load('data/leads/queries/injective_evm_chain_id.json')['result'], 16) == 1776
for r in load('data/leads/query_manifest.json')['queries']:
    if r.get('requested_height') is not None:
        assert r['status'] in ['unavailable', 'historical_height_confirmed']
        if r['status'] == 'historical_height_confirmed':
            assert r['response_headers']['x-cosmos-block-height'] == str(r['requested_height'])
for r in findings.values():
    assert r['limits'] and r['sources']
    for source in r['sources']:
        assert (ROOT / source).exists()
review_path = BASE / 'year_review_analysis.json'
if review_path.exists():
    review = json.loads(review_path.read_text())
    assert review['identified_named_project_grants_USDC'] == '265000'
    assert review['review_period_grants_excluding_earlier_votion_USDC'] == '215000'
    assert review['liquidity_capital_USDC_separate_from_expense'] == '100000'
    assert review['treasury_actions']['72']['milestone_state_claimed_USDC'] == '210000'
    assert review['treasury_actions']['28']['milestone_state_claimed_USDC'] == '50000'
    metrics = load('data/leads/queries/review_creda_metrics.json')['data']
    assert all(Decimal(a['total_collateral_usd']) <= Decimal(a['total_supplied_usd']) for a in metrics['assets'])
    supplied = Decimal(metrics['total_supplied_usd'])
    values = {}
    for name in ['operations', 'board', 'tla_single']:
        portfolio = load('data/leads/queries/review_creda_portfolio_' + name + '.json')['data']
        value = Decimal(portfolio['total_supplied_value'])
        assert value == sum(Decimal(a['value']) for a in portfolio['supplied'])
        values[name] = value
    assert Decimal(review['approximate_share_supplied_percent']['combined_public_contract_positions']) == sum(values.values()) / supplied * 100
print(json.dumps({'verification': 'passed', 'successful_primary_transactions': len(records),
                  'terra_tx_byte_hash_matches': len(checks), 'transfer_rows': len(transfers),
                  'empty_amount_events_preserved': len(unquantified), 'bounded_findings': len(findings),
                  'unavailable_transactions': sum(r['status'] == 'unavailable' for r in manifest['transactions'])}, indent=2))
