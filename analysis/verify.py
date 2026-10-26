import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
board=load('data/mb_voting_record.json')
assert len(board['records'])==289
assert board['summary']['mb_votes_by_proposer']['Philipp']['yes']==251
assert board['summary']['mb_votes_by_proposer']['Philipp']['recorded']==252
assert [p['id'] for p in board['records']]==list(range(1,290))
a272=load('data/phoenix/key_proposals.json')['272']
assert a272['proposal']['proposal']['status']=='rejected'
assert a272['proposal']['proposal']['votes']=={'yes':'50','no':'25','abstain':'0'}
assert len(a272['votes'])==3
props=load('data/eris_multisig/proposals.json')['data']['proposals']
assert len(props)==9 and props[-1]['status']=='executed'
ev=load('data/eris_multisig/votes.json')
assert all(v['vote']=='yes' for votes in ev.values() for v in votes)
assert sum(v['weight'] for v in ev['9'])==70
native=load('data/native_4853/votes.json')['votes']
assert len(native)==79
assert len(load('data/native_4853/vote_transactions.json')['tx_responses'])==87
hub=load('data/eris_multisig/hub_delegations.json')['delegation_responses']
assert len(hub)==11
assert not any(x['delegation']['validator_address']=='terravaloper1pet430t7ykswxuyhh56d4gk6rt7qgu9as6a5r0' and int(x['balance']['amount']) for x in hub)
print('Verified: 289 board proposals; 79 current 4853 ballots; 87 vote transactions; 9 ERIS proposals; A272 and delegation assertions.')
