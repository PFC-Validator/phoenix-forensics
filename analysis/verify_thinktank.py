#!/usr/bin/env python3
"""Verify the authored Think Tank review against preserved primary records."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data'
TT_PATH = D / 'thinktank'
MEMBERS = json.loads((TT_PATH / 'members.json').read_text())['data']['members']
ADDRS = {m['addr'] for m in MEMBERS}
PHILIPP = 'terra1vm5azhvaxeanc7auxh02y8jmxrk8tj93f6aywp'
REBEL = 'terra1rnwr9zjgf6204lyk37w0l6hhtaptke5m2cfpmf'
DAVID = 'terra1j00tmfa8el568llp3y96dquc9j2fcczmccnsn0'
MEMBER_7183 = 'terra18gqpvh0vktgqena9728zuharqhc4628w9muwjw'
TREASURY = 'terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5'

assert len(ADDRS) == 6 and all(m['weight'] == 1 for m in MEMBERS)
config = json.loads((TT_PATH / 'config.json').read_text())['data']
assert config['threshold']['absolute_percentage']['percentage']['percent'] == '0.66'
assert config['max_voting_period']['time'] == 172800
assert config['only_members_execute'] is True and config['allow_revoting'] is False

proposals = json.loads((TT_PATH / 'proposals.json').read_text())['data']['proposals']
assert len(proposals) == 5
assert all(p['proposal']['proposer'] == PHILIPP for p in proposals)
assert [p['proposal']['votes'] for p in proposals[1:]] == [
    {'yes': '0', 'no': '0', 'abstain': '2'},
    {'yes': '0', 'no': '0', 'abstain': '2'},
    {'yes': '0', 'no': '0', 'abstain': '1'},
    {'yes': '0', 'no': '0', 'abstain': '1'},
]
assert proposals[-1]['proposal']['msgs'] == []
assert proposals[1]['proposal']['msgs'][0]['wasm']['execute']['contract_addr'] == TREASURY

votes = json.loads((TT_PATH / 'votes.json').read_text())
assert all(v['voter'] != REBEL for group in votes.values() for v in group['data']['votes'])
assert sum(len(votes[str(i)]['data']['votes']) for i in range(1, 6)) == 11
non_technical_veto_ballots = sum(
    v['voter'] != PHILIPP
    for i in range(2, 6)
    for v in votes[str(i)]['data']['votes']
)
assert non_technical_veto_ballots == 2
assert all(
    v['vote'] == 'abstain'
    for i in range(2, 6)
    for v in votes[str(i)]['data']['votes']
    if v['voter'] != PHILIPP
)

# Collect the action inventory without assuming one aggregate file contains every action.
actions = {}
def collect_actions(obj):
    if isinstance(obj, dict):
        if 'id' in obj and 'name' in obj and 'setup' in obj:
            actions[obj['id']] = obj
        for value in obj.values():
            collect_actions(value)
    elif isinstance(obj, list):
        for value in obj:
            collect_actions(value)
for path in (D / 'treasury' / 'actions').glob('*.json'):
    collect_actions(json.loads(path.read_text()))

for action_id, recipient, total in [
    (28, PHILIPP, '50000'),
    (72, PHILIPP, '210000'),
    (112, PHILIPP, '125000'),
    (32, MEMBER_7183, '30000'),
]:
    action = actions[action_id]
    assert recipient in json.dumps(action['setup']) and action['total_usd'] == total
assert actions[32]['done'] is True
assert [m['claimed'] for m in actions[32]['runtime']['milestone']['milestones']] == [True, True]
assert actions[112]['runtime']['milestone']['milestones'][0]['claimed'] is True
assert all(not m['claimed'] for m in actions[112]['runtime']['milestone']['milestones'][1:])
assert json.dumps(actions[60]['setup']).count(DAVID) == 3
assert actions[60]['total_usd'] == '4200' and actions[60]['done'] is True
assert DAVID in json.dumps(actions[77]['setup']) and actions[77]['total_usd'] == '1000'

# Native-transfer graph over unique preserved transaction responses.
txs = {}
def collect_txs(obj):
    if isinstance(obj, dict):
        if 'txhash' in obj and ('events' in obj or 'logs' in obj) and ('timestamp' in obj or 'time' in obj):
            txs.setdefault(obj['txhash'], obj)
        for value in obj.values():
            collect_txs(value)
    elif isinstance(obj, list):
        for value in obj:
            collect_txs(value)
for folder in ['transfers', 'treasury', 'phoenix', 'eris_multisig', 'native_4853', 'thinktank']:
    for path in (D / folder).rglob('*.json'):
        collect_txs(json.loads(path.read_text()))
assert len(txs) == 906

edges = []
for txhash, tx in txs.items():
    for event in tx.get('events', []):
        if event.get('type') != 'transfer':
            continue
        attrs = {a['key']: a['value'] for a in event.get('attributes', [])}
        sender, recipient = attrs.get('sender'), attrs.get('recipient')
        if sender in ADDRS or recipient in ADDRS:
            edges.append((txhash, sender, recipient, attrs.get('amount')))

signers = {
    v['addr'] for v in json.loads((D / 'eris_multisig' / 'voters.json').read_text())['data']['voters']
}
other_board = {
    'terra1vv9zaygt7csc4wnufwk4snq2jle2sdh73vml73',
    'terra15vwmgac9tlcgkrkjn4rq3r0md003ufsqp64vaw',
    'terra18ruqkccl5tp493uhvra0u6jylrzq8t8dv5qs4c',
    'terra14p3mc04s7jcaxvvetlzehvhx9gdx6w4nm3zzw3',
}
assert not [e for e in edges if e[1] in ADDRS and e[2] in ADDRS and e[1] != e[2]]
assert not [e for e in edges if (e[1] in ADDRS and e[2] in signers) or (e[2] in ADDRS and e[1] in signers)]
assert not [e for e in edges if (e[1] in ADDRS and e[2] in other_board) or (e[2] in ADDRS and e[1] in other_board)]
assert any(
    h == '9A139FB60B44B4B055E8699E982C57B429A86EF2C0BF4CD50E2A0B06C5703B8C'
    and s == 'terra1gaxzcygjyz7gq8gq9tjy02qq38kcf84um9wy0a'
    and r == PHILIPP and amount.startswith('5000000000ibc/')
    for h, s, r, amount in edges
)
assert any(
    h == '8E29E90F6A058D61B74BC6F1004486431753E05532D50DBE08C340520AFC6FC3'
    and s == TREASURY and r == DAVID and amount.startswith('1000000000ibc/')
    for h, s, r, amount in edges
)

# Verify the Cosmos SDK distribution module account derivation independently.
def bech32_module_address(name):
    raw = hashlib.sha256(name.encode()).digest()[:20]
    def convert(data):
        acc = bits = 0
        result = []
        for value in data:
            acc = (acc << 8) | value
            bits += 8
            while bits >= 5:
                bits -= 5
                result.append((acc >> bits) & 31)
        if bits:
            result.append((acc << (5 - bits)) & 31)
        return result
    def polymod(values):
        chk = 1
        generators = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
        for value in values:
            top = chk >> 25
            chk = (chk & 0x1ffffff) << 5 ^ value
            for i, generator in enumerate(generators):
                if (top >> i) & 1:
                    chk ^= generator
        return chk
    hrp = 'terra'
    data = convert(raw)
    expanded = [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
    checksum = polymod(expanded + data + [0] * 6) ^ 1
    values = data + [(checksum >> (5 * (5 - i))) & 31 for i in range(6)]
    return hrp + '1' + ''.join('qpzry9x8gf2tvdw0s3jn54khce6mua7l'[x] for x in values)

assert bech32_module_address('distribution') == 'terra1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8pm7utl'
print(json.dumps({
    'thinktank_proposals': len(proposals),
    'substantive_veto_yes_votes': 0,
    'substantive_veto_no_votes': 0,
    'non_technical_veto_ballots': non_technical_veto_ballots,
    'unique_preserved_transactions_checked': len(txs),
    'transfer_graph_scope': 'Bounded preserved union; monitored wallet histories include truncated sender-only windows and are not a census.',
    'direct_thinktank_to_thinktank_transfers_in_preserved_union': 0,
    'direct_thinktank_to_eris_signer_transfers_in_preserved_union': 0,
    'direct_thinktank_to_other_board_transfers_in_preserved_union': 0,
    'distribution_module_derivation': 'verified',
}, indent=2))
