#!/usr/bin/env python3
"""Compute director and Rebel profiles from preserved records; no typed-in figures."""
import collections
import csv
import itertools
import json
from pipeline_utils import ROOT, RECENT_CUTOFF, USDC, WBTC, load_json

D = load_json('data/mb_voting_record.json')
A = {
    'Philipp': 'terra1gaxzcygjyz7gq8gq9tjy02qq38kcf84um9wy0a',
    'MB_current': 'terra1vv9zaygt7csc4wnufwk4snq2jle2sdh73vml73',
    'MB_prior': 'terra15vwmgac9tlcgkrkjn4rq3r0md003ufsqp64vaw',
    'Vini': 'terra18ruqkccl5tp493uhvra0u6jylrzq8t8dv5qs4c',
    'Rose': 'terra14p3mc04s7jcaxvvetlzehvhx9gdx6w4nm3zzw3',
}

def vote(record, address):
    return next((v['vote'] for v in record['votes'] if v['voter'] == address), 'not_recorded')

def ballots_for(name):
    return [(r, vote(r, A[name])) for r in D['records']]

def ballot_total(counts):
    return sum(counts[key] for key in ('yes', 'no', 'abstain'))

profiles = {}
for name, address in A.items():
    rows = ballots_for(name)
    counts = collections.Counter(v for _, v in rows)
    recent = collections.Counter(v for r, v in rows if r['proposal_created_utc'] >= RECENT_CUTOFF)
    profiles[name] = {
        'address': address,
        'counts': dict(counts),
        'recent_counts': dict(recent),
        'authored': [{'id': r['proposal_id'], 'title': r['title']} for r in D['records'] if r['proposer_wallet'] == address],
        'no': [{'id': r['proposal_id'], 'title': r['title'], 'status': r['status_as_of_refresh']} for r in D['records'] if vote(r, address) == 'no'],
        'abstain': [{'id': r['proposal_id'], 'title': r['title'], 'status': r['status_as_of_refresh']} for r in D['records'] if vote(r, address) == 'abstain'],
    }

for name, first, last in [('MB_current', 126, 289), ('MB_prior', 1, 125)]:
    scoped = [(r, vote(r, A[name])) for r in D['records'] if first <= int(r['id']) <= last]
    ballots = sum(v != 'not_recorded' for _, v in scoped)
    profiles[name]['observed_window'] = f'A{first}–A{last}: {ballots} ballots in {len(scoped)} proposals ({ballots / len(scoped) * 100:.1f}%)'
for name in ['Vini', 'Rose']:
    counts = profiles[name]['counts']
    ballots = ballot_total(counts)
    suffix = '; no joining-window adjustment inferred' if name == 'Vini' else ''
    profiles[name]['observed_window'] = f'{ballots} ballots in {len(D["records"])} proposals ({ballots / len(D["records"]) * 100:.1f}%){suffix}'
combined = collections.Counter(profiles['MB_current']['counts'])
combined.update(profiles['MB_prior']['counts'])
profiles['MB_current']['combined_with_prior'] = f'{ballot_total(combined)} ballots: {combined["yes"]} YES, {combined["no"]} NO, {"zero" if combined["abstain"] == 0 else combined["abstain"]} abstain'

pairs = []
for a, b in itertools.combinations(A, 2):
    rows = [(r, vote(r, A[a]), vote(r, A[b])) for r in D['records']]
    shared = [x for x in rows if x[1] != 'not_recorded' and x[2] != 'not_recorded']
    same = sum(va == vb for _, va, vb in shared)
    pairs.append({'a': a, 'b': b, 'shared': len(shared), 'same': same, 'different': len(shared) - same, 'same_pct': round(same / len(shared) * 100, 1) if shared else None})

out = load_json('data/treasury/outbound_transfers.json')
for name in ['MB_current', 'Vini', 'Rose']:
    xs = [x for x in out if x['recipient'] == A[name] and x['denom'] == USDC]
    profiles[name]['treasury_usdc_total'] = sum(x['amount'] for x in xs) / 1e6

rose_tx = load_json('data/treasury/claims/221979DDA2653A2A5856B091BF32919DBF6F4AE1DEB802BC5E8D0BCC46D8B677.json')
messages = rose_tx['tx']['body']['messages']
funds = [coin for message in messages for coin in message.get('funds', []) if coin['denom'] == WBTC]
assert len(funds) == 1
profiles['Rose']['otc_wbtc_supplied'] = int(funds[0]['amount']) / 1e8
luna_receipts = []
for event in rose_tx['tx_response']['events']:
    if event['type'] != 'transfer':
        continue
    attrs = {a['key']: a['value'] for a in event['attributes']}
    if attrs.get('sender') == 'terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5' and attrs.get('recipient') == A['Rose'] and attrs.get('amount', '').endswith('uluna'):
        luna_receipts.append(int(attrs['amount'][:-5]))
assert len(luna_receipts) == 1
profiles['Rose']['otc_luna_receipt'] = luna_receipts[0] / 1e6
profiles['Rose']['eris_otc'] = f'{profiles["Rose"]["otc_luna_receipt"]:,.6f} LUNA received from Treasury; {profiles["Rose"]["otc_wbtc_supplied"]:.8f} WBTC supplied, memo www.erisprotocol.com'

voters = load_json('data/eris_multisig/voters.json')['data']['voters']
profiles['Vini']['eris_fixed_multisig_weight'] = next(v['weight'] for v in voters if v['addr'] == A['Vini'])
eris_votes = load_json('data/eris_multisig/votes.json')
vini_eris = [(int(pid), v['vote']) for pid, votes in eris_votes.items() for v in votes if v['voter'] == A['Vini']]
missing_eris = sorted(set(map(int, eris_votes)) - {pid for pid, _ in vini_eris})
assert all(vote_value == 'yes' for _, vote_value in vini_eris)
profiles['Vini']['eris_multisig_record'] = f'{len(vini_eris)} YES ballots in {len(eris_votes)} proposals; no ballot on proposal {", ".join(map(str, missing_eris))}; all recorded ballots YES'
native_ballots = {v['voter']: v['options'] for v in load_json('data/native_4853/votes.json')['votes']}
for name in ['Vini', 'MB_current', 'MB_prior', 'Rose']:
    profiles[name]['native_4853'] = native_ballots.get(A[name], 'no ballot')

payment_dates = [x['time'] for x in out]
result = {
    'directors': profiles,
    'pair_agreement': pairs,
    'notes': [f'Missing ballot is not NO or abstention. Agreement does not prove coordination. Payment totals are scoped to {min(payment_dates)[:10]}–{max(payment_dates)[:10]} and are not lifetime income.'],
    'recent_cutoff': RECENT_CUTOFF,
}
(ROOT / 'data/phoenix/director_profiles.json').write_text(json.dumps(result, indent=2) + '\n')
with (ROOT / 'data/phoenix/director_vote_patterns.csv').open('w', newline='') as f:
    fields = ['proposal_id', 'created_utc', 'title', 'status', *A]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for record in D['records']:
        writer.writerow({'proposal_id': record['proposal_id'], 'created_utc': record['proposal_created_utc'], 'title': record['title'], 'status': record['status_as_of_refresh'], **{name: vote(record, address) for name, address in A.items()}})

think = load_json('data/thinktank/votes.json')
with (ROOT / 'data/thinktank/votes.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['proposal_id', 'voter', 'vote', 'power'])
    writer.writeheader()
    for pid, obj in think.items():
        for item in obj['data']['votes']:
            writer.writerow({'proposal_id': pid, 'voter': item['voter'], 'vote': item['vote'], 'power': item['power']})

rebel_address = 'terra1rnwr9zjgf6204lyk37w0l6hhtaptke5m2cfpmf'
rebel_payment = load_json('data/transfers/rebel_eris_invoice_2026-06-07.json')
invoice_events = []
for event in rebel_payment['tx_response']['events']:
    if event['type'] != 'transfer':
        continue
    attrs = {a['key']: a['value'] for a in event['attributes']}
    if attrs.get('recipient') == rebel_address and attrs.get('amount', '').endswith(USDC):
        invoice_events.append(attrs)
assert len(invoice_events) == 1
invoice = invoice_events[0]
rebel_ballots = [{'proposal_id': int(pid), **v} for pid, obj in think.items() for v in obj['data']['votes'] if v['voter'] == rebel_address]
orbital_operator = 'terravaloper1lelhxdzwn9ddecv6sv0kcxj5tguurxnzcfs5wf'
hub = load_json('data/eris_multisig/hub_delegations.json')['delegation_responses']
orbital_delegation = next(int(x['balance']['amount']) for x in hub if x['delegation']['validator_address'] == orbital_operator)
rebel = {
    'project_wallet': rebel_address,
    'role': 'Think Tank veto member, weight 1 of 6',
    'threshold': '66% (four YES votes required)',
    'thinktank_ballots': rebel_ballots,
    'thinktank_proposals': len(think),
    'invoice': {
        'txhash': rebel_payment['tx_response']['txhash'],
        'time': rebel_payment['tx_response']['timestamp'],
        'from': invoice['sender'], 'to': invoice['recipient'],
        'amount_usdc': int(invoice['amount'].split('ibc/', 1)[0]) / 1e6,
        'memo': rebel_payment['tx']['body']['memo'],
    },
    'other_published_addresses': [
        {'address': 'terra17w74x9vrqq4a338ssh9y9r4m9s3f6zef7wy5ms', 'attribution': 'Rebel Defi handle in archived governance comments', 'native_4853': native_ballots.get('terra17w74x9vrqq4a338ssh9y9r4m9s3f6zef7wy5ms', 'no ballot'), 'bounded_transfer_matches': 0},
        {'address': 'terra1pnxgfvlaywamhykr4nfeep8n2ejd2mactz3un8', 'attribution': 'Rebel in 2023 multisig-member document', 'native_4853': native_ballots.get('terra1pnxgfvlaywamhykr4nfeep8n2ejd2mactz3un8', 'no ballot'), 'bounded_transfer_matches': 0},
        {'address': 'terra1lelhxdzwn9ddecv6sv0kcxj5tguurxnzcxuf76', 'attribution': 'Orbital Command validator account; Rebel association is documented separately', 'native_4853': native_ballots.get('terra1lelhxdzwn9ddecv6sv0kcxj5tguurxnzcxuf76', 'no ballot'), 'eris_hub_delegated_luna': orbital_delegation / 1e6},
    ],
    'cautions': ['No direct transfer to fixed multisig signers found in bounded searches. Think Tank and validator roles are separate from the Phoenix board and ERIS fixed multisig.'],
}
(ROOT / 'data/phoenix/rebel_profile.json').write_text(json.dumps(rebel, indent=2) + '\n')
print(json.dumps({'director_profiles': profiles, 'pair_agreement': pairs, 'rebel': rebel}, indent=2))
