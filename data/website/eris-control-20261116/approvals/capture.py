import urllib.request,json,pathlib,hashlib,datetime,concurrent.futures
root=pathlib.Path(__file__).parent
jobs={f'native-{n}.json':f'https://terra-phoenix-api.highstakes.ch/cosmos/gov/v1/proposals/{n}' for n in [3460,3796,4813,4816,4817,4822,4823,4830,4836]}
jobs['docs-tree.json']='https://api.github.com/repos/phoenix-directive/docs/git/trees/main?recursive=1'
if __name__=='__main__':
 def capture(item):
  name,url=item; t=datetime.datetime.now(datetime.timezone.utc).isoformat()
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Evidence-review/1.0'}),timeout=60) as r:
    body=r.read();status=r.status
   (root/name).write_bytes(body)
   rec={'file':name,'url':url,'captured_at_utc':t,'status':status,'sha256':hashlib.sha256(body).hexdigest()}
  except Exception as e: rec={'file':name,'url':url,'captured_at_utc':t,'error':str(e)}
  return rec
 manifest=list(concurrent.futures.ThreadPoolExecutor(6).map(capture,jobs.items()))
 (root/'capture-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for r in manifest: print(r['file'],r.get('status',r.get('error')))
