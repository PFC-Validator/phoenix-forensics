import collections,csv,itertools,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
D=json.loads((R/'data/mb_voting_record.json').read_text())
A={'Philipp':'terra1gaxzcygjyz7gq8gq9tjy02qq38kcf84um9wy0a','MB_current':'terra1vv9zaygt7csc4wnufwk4snq2jle2sdh73vml73','MB_prior':'terra15vwmgac9tlcgkrkjn4rq3r0md003ufsqp64vaw','Vini':'terra18ruqkccl5tp493uhvra0u6jylrzq8t8dv5qs4c','Rose':'terra14p3mc04s7jcaxvvetlzehvhx9gdx6w4nm3zzw3'}
def vote(r,a):return next((v['vote'] for v in r['votes'] if v['voter']==a),'not_recorded')
profiles={}
for name,a in A.items():
 rows=[(r,vote(r,a)) for r in D['records']]
 counts=collections.Counter(v for _,v in rows)
 recent=collections.Counter(v for r,v in rows if r['proposal_created_utc']>='2026-09-26')
 profiles[name]={'address':a,'counts':dict(counts),'recent_counts':dict(recent),'authored':[{'id':r['proposal_id'],'title':r['title']} for r in D['records'] if r['proposer_wallet']==a],'no':[{'id':r['proposal_id'],'title':r['title'],'status':r['status_as_of_refresh']} for r in D['records'] if vote(r,a)=='no'],'abstain':[{'id':r['proposal_id'],'title':r['title'],'status':r['status_as_of_refresh']} for r in D['records'] if vote(r,a)=='abstain']}
profiles['MB_current']['observed_window']='A126–A289: 135 ballots in 164 proposals (82.3%)'
profiles['MB_prior']['observed_window']='A1–A125: 118 ballots in 125 proposals (94.4%)'
profiles['Vini']['observed_window']='115 ballots in 289 proposals (39.8%); no joining-window adjustment inferred'
profiles['Rose']['observed_window']='241 ballots in 289 proposals (83.4%)'
profiles['MB_current']['combined_with_prior']='253 ballots: 252 YES, 1 NO, zero abstain'
pairs=[]
for a,b in itertools.combinations(A,2):
 rows=[(r,vote(r,A[a]),vote(r,A[b])) for r in D['records']]
 shared=[x for x in rows if x[1]!='not_recorded' and x[2]!='not_recorded']
 same=sum(va==vb for _,va,vb in shared)
 pairs.append({'a':a,'b':b,'shared':len(shared),'same':same,'different':len(shared)-same,'same_pct':round(same/len(shared)*100,1) if shared else None})
out=json.loads((R/'data/treasury/outbound_transfers.json').read_text())
usdc='ibc/2C962DAB9F57FE0921435426AE75196009FAA1981BF86991203C8411F8980FDB'
for name in ['MB_current','Vini','Rose']:
 xs=[x for x in out if x['recipient']==A[name] and x['denom']==usdc]
 profiles[name]['treasury_usdc_total']=sum(x['amount'] for x in xs)/1e6
profiles['Rose']['otc_luna_receipt']=237323.047934
profiles['Rose']['otc_wbtc_supplied']=0.19657723
profiles['Vini']['eris_fixed_multisig_weight']=10
profiles['Vini']['eris_multisig_record']='8 YES ballots in 9 proposals; no ballot on proposal 8; all recorded ballots YES'
profiles['Vini']['native_4853']='no ballot'
profiles['MB_current']['native_4853']='no ballot'
profiles['MB_prior']['native_4853']='no ballot'
profiles['Rose']['native_4853']='no ballot'
profiles['Rose']['eris_otc']='237,323.047934 LUNA received from Treasury; 0.19657723 WBTC supplied, memo www.erisprotocol.com'
result={'directors':profiles,'pair_agreement':pairs,'notes':['Missing ballot is not NO or abstention. Agreement does not prove coordination. Payment totals are scoped to 2 Jan–24 Oct 2026 and are not lifetime income.']}
(R/'data/phoenix/director_profiles.json').write_text(json.dumps(result,indent=2))
with (R/'data/phoenix/director_vote_patterns.csv').open('w',newline='') as f:
 fields=['proposal_id','created_utc','title','status','Philipp','MB_current','MB_prior','Vini','Rose']
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in D['records']:
  w.writerow({'proposal_id':r['proposal_id'],'created_utc':r['proposal_created_utc'],'title':r['title'],'status':r['status_as_of_refresh'],**{n:vote(r,a) for n,a in A.items()}})
think=json.loads((R/'data/thinktank/votes.json').read_text())
with (R/'data/thinktank/votes.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['proposal_id','voter','vote','power']);w.writeheader()
 for pid,obj in think.items():
  for v in obj['data']['votes']:w.writerow({'proposal_id':pid,'voter':v['voter'],'vote':v['vote'],'power':v['power']})
rebel_payment=json.loads((R/'data/transfers/rebel_eris_invoice_2026-06-07.json').read_text())
rebel={'project_wallet':'terra1rnwr9zjgf6204lyk37w0l6hhtaptke5m2cfpmf','role':'Think Tank veto member, weight 1 of 6','threshold':'66% (four YES votes required)','thinktank_ballots':[],'thinktank_proposals':5,'invoice':{'txhash':'02B838A200BCF19F693FC461F3DF09ADD1A3D81AB789A0B260034DF8A6C3AC80','time':rebel_payment['tx_response']['timestamp'],'from':'terra1rgggsspquaxjp4lmegx7a3q4l9lg44hnu7rjxa','to':'terra1rnwr9zjgf6204lyk37w0l6hhtaptke5m2cfpmf','amount_usdc':7500,'memo':rebel_payment['tx']['body']['memo']},'other_published_addresses':[{'address':'terra17w74x9vrqq4a338ssh9y9r4m9s3f6zef7wy5ms','attribution':'Rebel Defi handle in archived governance comments','native_4853':'no ballot','bounded_transfer_matches':0},{'address':'terra1pnxgfvlaywamhykr4nfeep8n2ejd2mactz3un8','attribution':'Rebel in 2023 multisig-member document','native_4853':'no ballot','bounded_transfer_matches':0},{'address':'terra1lelhxdzwn9ddecv6sv0kcxj5tguurxnzcxuf76','attribution':'Orbital Command validator account; Rebel association is documented separately','native_4853':'YES','eris_hub_delegated_luna':1124005.906919}],'cautions':['No direct transfer to fixed multisig signers found in bounded searches. Think Tank and validator roles are separate from the Phoenix board and ERIS fixed multisig.']}
(R/'data/phoenix/rebel_profile.json').write_text(json.dumps(rebel,indent=2))
print(json.dumps({'director_profiles':profiles,'pair_agreement':pairs,'rebel':rebel},indent=2))
