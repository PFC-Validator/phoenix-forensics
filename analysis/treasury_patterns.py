import json,re,collections,datetime,pathlib,csv
R=pathlib.Path(__file__).resolve().parents[1]
d=json.load((R/'data/treasury/outbound_all_tx_responses.json').open())
treasury='terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5'
rows=[]
for r in (d if isinstance(d,list) else d.get('tx_responses',[])):
 for e in r.get('events',[]):
  if e.get('type')!='transfer':continue
  a={x['key']:x['value'] for x in e.get('attributes',[])}
  if a.get('sender')!=treasury:continue
  m=re.fullmatch(r'(\d+)(.+)',a.get('amount',''))
  if not m:continue
  rows.append({'txhash':r['txhash'],'time':r['timestamp'],'height':r['height'],'recipient':a['recipient'],'amount':int(m.group(1)),'denom':m.group(2)})
print('range',min(x['time'] for x in rows),max(x['time'] for x in rows),'events',len(rows),'txs',len({x['txhash'] for x in rows}))
by=collections.defaultdict(lambda:{'count':0,'total':0,'times':[],'amounts':collections.Counter(),'hashes':[]})
for x in rows:
 k=(x['recipient'],x['denom']);v=by[k];v['count']+=1;v['total']+=x['amount'];v['times'].append(x['time']);v['amounts'][x['amount']]+=1;v['hashes'].append(x['txhash'])
for (a,den),v in sorted(by.items(),key=lambda kv:-kv[1]['total']):
 print(a,den,'count',v['count'],'total',v['total']/1e6,'first',min(v['times']),'last',max(v['times']),'amounts',[(k/1e6,n) for k,n in v['amounts'].most_common(12)])
month=collections.defaultdict(float)
for x in rows:month[(x['time'][:7],x['denom'])]+=x['amount']/1e6
print('MONTHLY')
for k,v in sorted(month.items()):print(k,round(v,6))
with (R/'data/treasury/outbound_transfers.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(R/'data/treasury/outbound_transfers.json').write_text(json.dumps(rows,indent=2))
