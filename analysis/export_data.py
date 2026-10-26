import csv,json,pathlib
from pipeline_utils import RECENT_CUTOFF
R=pathlib.Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
def write(p,fields,rows):
    with (R/p).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
d=load('data/mb_voting_record.json')
rows=[]
for r in d['records']:
    rows.append({k:r.get(k) for k in ['proposal_id','id','proposal_created_utc','title','status_as_of_refresh','proposer_name','proposer_wallet','mb_combined_vote','mb_wallet_used','mb_vote_utc','mb_vote_txhash','philipp_vote','philipp_vote_utc','philipp_vote_txhash','comparison_with_philipp','proposal_url','ballot_query_url']})
fields=list(rows[0])
write('data/phoenix_board_votes_all.csv',fields,rows)
write('data/phoenix_board_votes_last4weeks.csv',fields,[r for r in rows if r['proposal_created_utc']>=RECENT_CUTOFF])
ev=load('data/eris_multisig/votes.json')
write('data/eris_multisig_votes_all.csv',['proposal_id','voter','vote','weight'],[v for vs in ev.values() for v in vs])
nv=load('data/native_4853/votes.json')['votes']
write('data/native_4853_votes_all.csv',['proposal_id','voter','option','weight'],[{'proposal_id':v['proposal_id'],'voter':v['voter'],'option':option['option'],'weight':option['weight']} for v in nv for option in v['options']])
nt=load('data/native_4853/vote_transactions.json')
rows=[]
for i,r in enumerate(nt.get('tx_responses',[])):
    msgs=r.get('tx',{}).get('body',{}).get('messages',[])
    if not msgs and nt.get('txs'):
        if len(nt['txs']) != len(nt['tx_responses']):
            raise ValueError('Cannot pair txs with tx_responses safely')
        msgs=nt['txs'][i].get('body',{}).get('messages',[])
    for m in msgs:
        if 'Vote' in m.get('@type',''):
            rows.append({'txhash':r['txhash'],'timestamp':r['timestamp'],'height':r['height'],'voter':m.get('voter'),'proposal_id':m.get('proposal_id'),'option':m.get('option'),'type':m.get('@type')})
write('data/native_4853_vote_transactions.csv',['txhash','timestamp','height','voter','proposal_id','option','type'],rows)
hd=load('data/eris_multisig/hub_delegations.json')['delegation_responses']
write('data/eris_hub_delegations.csv',['validator_address','uluna','luna'],[{'validator_address':x['delegation']['validator_address'],'uluna':x['balance']['amount'],'luna':int(x['balance']['amount'])/1e6} for x in hd])
print('exported',len(rows),'native vote messages and',len(d['records']),'board proposals')
