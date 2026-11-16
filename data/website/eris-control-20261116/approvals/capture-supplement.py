import urllib.request,json,pathlib,hashlib,datetime,time
root=pathlib.Path(__file__).parent
base='https://raw.githubusercontent.com/phoenix-directive/docs/'+json.load(open(root/'docs-tree.json'))['sha']+'/'
paths=[t['path'] for t in json.load(open(root/'docs-tree.json'))['tree'] if any(s in t['path'] for s in ['8789_', '20123_', '24385_', '25020_', '23826_'])]
jobs={p.rsplit('/',1)[1]:base+p for p in paths}
jobs.update({f'native-{n}.json':f'https://terra-phoenix-api.highstakes.ch/cosmos/gov/v1/proposals/{n}' for n in [4813,4823,4836]})
manifest=[]
for name,url in jobs.items():
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Evidence-review/1.0'}),timeout=60) as r:body=r.read();status=r.status
  (root/name).write_bytes(body);rec={'file':name,'url':url,'captured_at_utc':t,'status':status,'sha256':hashlib.sha256(body).hexdigest()}
 except Exception as e:rec={'file':name,'url':url,'captured_at_utc':t,'error':str(e)}
 manifest.append(rec);print(name,rec.get('status',rec.get('error')),flush=True);time.sleep(2)
(root/'supplement-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
