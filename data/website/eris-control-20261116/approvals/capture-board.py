import urllib.request,json,pathlib,hashlib,datetime,time,base64
root=pathlib.Path(__file__).parent
base='https://terra-phoenix-api.highstakes.ch/cosmwasm/wasm/v1/contract/terra1660g9mle5kfsq8c0p4k4hgr9ujdyr3m48c22cawy0akr98rmwksqehqnup/smart/'
jobs={f'board-A{n}.json':base+base64.b64encode(json.dumps({'proposal':{'proposal_id':n}},separators=(',',':')).encode()).decode() for n in [107,189,190,209,215,258,266,271]}
manifest=[]
for name,url in jobs.items():
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Evidence-review/1.0'}),timeout=45) as r:body=r.read();status=r.status
  (root/name).write_bytes(body);rec={'file':name,'url':url,'captured_at_utc':t,'status':status,'sha256':hashlib.sha256(body).hexdigest()}
 except Exception as e:rec={'file':name,'url':url,'captured_at_utc':t,'error':str(e)}
 manifest.append(rec);print(name,rec.get('status',rec.get('error')),flush=True);time.sleep(2)
(root/'board-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
