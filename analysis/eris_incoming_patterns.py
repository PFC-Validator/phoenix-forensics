import json,re,collections,pathlib,csv
R=pathlib.Path(__file__).resolve().parents[1]
d=json.load((R/'data/transfers/to_eris_all_tx_responses.json').open())
target='terra1vm5azhvaxeanc7auxh02y8jmxrk8tj93f6aywp'
rows=[]
for r in d:
 for e in r.get('events',[]):
  if e.get('type')!='transfer':continue
  a={x['key']:x['value'] for x in e.get('attributes',[])}
  if a.get('recipient')!=target:continue
  m=re.fullmatch(r'(\d+)(.+)',a.get('amount',''))
  if not m:continue
  rows.append({'txhash':r['txhash'],'time':r['timestamp'],'height':r['height'],'sender':a['sender'],'amount':int(m.group(1)),'denom':m.group(2)})
by=collections.defaultdict(lambda:{'count':0,'total':0,'times':[],'amounts':collections.Counter()})
for x in rows:
 k=(x['sender'],x['denom']);v=by[k];v['count']+=1;v['total']+=x['amount'];v['times'].append(x['time']);v['amounts'][x['amount']]+=1
for (a,den),v in sorted(by.items(),key=lambda kv:-kv[1]['total']):
 if v['total']>=1e6:
  print(a,den,'count',v['count'],'total',v['total']/1e6,'first',min(v['times']),'last',max(v['times']),'amounts',[(k/1e6,n) for k,n in v['amounts'].most_common(8)])
with (R/'data/transfers/to_eris_all_transfers.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(R/'data/transfers/to_eris_all_transfers.json').write_text(json.dumps(rows,indent=2))
