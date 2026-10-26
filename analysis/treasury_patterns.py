import json,collections,pathlib,csv
from pipeline_utils import parse_coins, display_amount
R=pathlib.Path(__file__).resolve().parents[1]
d=json.load((R/'data/treasury/outbound_all_tx_responses.json').open())
treasury='terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5'
rows=[]
for r in (d if isinstance(d,list) else d.get('tx_responses',[])):
 for e in r.get('events',[]):
  if e.get('type')!='transfer':continue
  a={x['key']:x['value'] for x in e.get('attributes',[])}
  if a.get('sender')!=treasury:continue
  for coin in parse_coins(a.get('amount','')):
   rows.append({'txhash':r['txhash'],'time':r['timestamp'],'height':r['height'],'recipient':a['recipient'],'amount':coin['amount'],'denom':coin['denom']})
print('range',min(x['time'] for x in rows),max(x['time'] for x in rows),'events',len(rows),'txs',len({x['txhash'] for x in rows}))
by=collections.defaultdict(lambda:{'count':0,'total':0,'times':[],'amounts':collections.Counter(),'hashes':[]})
for x in rows:
 k=(x['recipient'],x['denom']);v=by[k];v['count']+=1;v['total']+=x['amount'];v['times'].append(x['time']);v['amounts'][x['amount']]+=1;v['hashes'].append(x['txhash'])
for (a,den),v in sorted(by.items(),key=lambda kv:-kv[1]['total']):
 print(a,den,'count',v['count'],'total',display_amount(v['total'],den),'first',min(v['times']),'last',max(v['times']),'amounts',[(display_amount(k,den),n) for k,n in v['amounts'].most_common(12)])
month=collections.defaultdict(int)
for x in rows:month[(x['time'][:7],x['denom'])]+=x['amount']
print('MONTHLY')
for (period,denom),amount in sorted(month.items()):print(period,denom,display_amount(amount,denom))
with (R/'data/treasury/outbound_transfers.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(R/'data/treasury/outbound_transfers.json').write_text(json.dumps(rows,indent=2))
