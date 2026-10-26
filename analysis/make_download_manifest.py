import base64,json,html,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
LCD='https://terra-phoenix-api.highstakes.ch'
MAIN='terra1660g9mle5kfsq8c0p4k4hgr9ujdyr3m48c22cawy0akr98rmwksqehqnup'
CORE='terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg'
GROUP='terra1pq9f4a8cn4cdvvm9j7v0mu8n5elf44tgtre8mzrfz3j4x6yyl2yq4hnkuk'
ERIS='terra1e9zwkd9epy8863d3ezmp5m4fsf95ceknhtmadwjt9rukvf8wtflstlecx8'
HUB='terra10788fkzah89xrdm27zkj5yvhj9x3494lxawzm5qq3vvxcqz2yzaqyd3enk'
ICS='terra1e0mrzy8077druuu42vs0hu7ugguade0cj65dgtauyaw4gsl4kv0qtdf2au'
items=[]
def add(name,url): items.append((name,url))
def smart(contract,q):
    encoded=base64.b64encode(json.dumps(q,separators=(',',':')).encode()).decode()
    return f'{LCD}/cosmwasm/wasm/v1/contract/{contract}/smart/{encoded}'
for pid in (4813,4817,4853):
    for suffix in ('','/votes?pagination.limit=1000','/tally','/deposits?pagination.limit=1000'):
        add(f'native/{pid}{suffix.replace("/","_").replace("?","_")}.json',f'{LCD}/cosmos/gov/v1/proposals/{pid}{suffix}')
add('phoenix/proposal_modules.json',smart(CORE,{'proposal_modules':{}}))
add('phoenix/config.json',smart(MAIN,{'config':{}}))
add('phoenix/members.json',smart(GROUP,{'list_members':{'limit':100}}))
for start in range(0,300,30):
    q={'list_proposals':{'limit':30}}
    if start:q['list_proposals']['start_after']=start
    add(f'phoenix/proposals_{start+1:03d}_{start+30:03d}.json',smart(MAIN,q))
for pid in range(1,301):
    add(f'phoenix/votes/A{pid}.json',smart(MAIN,{'list_votes':{'proposal_id':pid,'limit':100}}))
add('eris_multisig/config.json',smart(ERIS,{'config':{}}))
add('eris_multisig/proposals.json',smart(ERIS,{'list_proposals':{'limit':100}}))
for pid in range(1,10):add(f'eris_multisig/votes/{pid}.json',smart(ERIS,{'list_votes':{'proposal_id':pid,'limit':100}}))
for name,addr in [('hub',HUB),('ics20',ICS)]:
    add(f'eris_multisig/{name}_contract_info.json',f'{LCD}/cosmwasm/wasm/v1/contract/{addr}')
add('eris_multisig/hub_config.json',smart(HUB,{'config':{}}))
for path in [
'evidence/exhibits/voting_record/mb_voting_record.csv','evidence/exhibits/voting_record/mb_voting_record.json','evidence/exhibits/voting_record/findings.txt','evidence/source_index.json','evidence/SHA256SUMS.txt','evidence/transaction_chronology.json','evidence/exhibits/current/board_config.json','evidence/exhibits/current/board_members.json','evidence/exhibits/current/proposal9.json','evidence/exhibits/current/proposal9_votes.json','evidence/exhibits/current/hub_info.json','evidence/exhibits/current/ics20_info.json','evidence/exhibits/current/hub_config.json','evidence/exhibits/current/bylaws_current.pdf','evidence/exhibits/legacy/Belege/E05c.json','evidence/exhibits/legacy/Belege/E09a.json','evidence/exhibits/legacy/Belege/E09b.json','evidence/exhibits/legacy/Belege/E09c.json','evidence/censorship-records/vegas-post-revision.json','evidence/censorship-records/forum-thread-2026-10-19.json']:
    add('packet/'+path,'https://philipp-payments.pages.dev/'+path)
links='\n'.join(f'<p><a href="{html.escape(url,quote=True)}" download="{html.escape(name,quote=True)}">{html.escape(name)}</a></p>' for name,url in items)
(ROOT/'downloads'/'index.html').write_text('<!doctype html><title>Audit downloads</title>'+links)
(ROOT/'data/download_manifest.json').write_text(json.dumps([{'file':n,'url':u} for n,u in items],indent=2))
print(len(items),'links',ROOT/'downloads'/'index.html')
