import base64,datetime,hashlib,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
PACKET='https://philipp-payments.pages.dev/evidence/'
LCD='https://terra-phoenix-api.highstakes.ch'
ARCHIVE='https://terra2.tdrsys.com'
FORUM='https://forum.phoenix.money'
SMART='https://analytics.smartstake.io/terra/proposal/4853'
source_index=json.loads((ROOT/'data/source_index.json').read_text())
packet_by_file={x['file']:x for x in source_index['sources'] if x.get('file')}

def smart(contract,q):
    return f'{LCD}/cosmwasm/wasm/v1/contract/{contract}/smart/{base64.b64encode(json.dumps(q,separators=(",",":")).encode()).decode()}'
MAIN='terra1660g9mle5kfsq8c0p4k4hgr9ujdyr3m48c22cawy0akr98rmwksqehqnup'
CORE='terra1k8ug6dkzntczfzn76wsh24tdjmx944yj6mk063wum7n20cwd7lxq4lppjg'
GROUP='terra1pq9f4a8cn4cdvvm9j7v0mu8n5elf44tgtre8mzrfz3j4x6yyl2yq4hnkuk'
ERIS='terra1e9zwkd9epy8863d3ezmp5m4fsf95ceknhtmadwjt9rukvf8wtflstlecx8'
HUB='terra10788fkzah89xrdm27zkj5yvhj9x3494lxawzm5qq3vvxcqz2yzaqyd3enk'
TREASURY='terra16st8yfprkdl06kccktshd3p2vccq93xcn9mkhjl8s4jumyjtd4kqye0me5'
REGISTRY='terra1hwxg6s732eparz3ys7sa4t5f64ngpd2w8syrca6z7ckv3fs9uqnsvrpcqa'
ICS='terra1e0mrzy8077druuu42vs0hu7ugguade0cj65dgtauyaw4gsl4kv0qtdf2au'
URL_RE=re.compile(r'https?://[^\s"\'<>\]\)}]+')

def urls_in_file(path,limit=12):
    try:text=path.read_text(errors='ignore')
    except OSError:return []
    found=[]
    for u in URL_RE.findall(text):
        u=u.rstrip('.,;')
        if u not in found:found.append(u)
    return found[:limit]

def info(classification,sources,upstream,method,transformation='None',notes='',expected_sha=None):
    return {'classification':classification,'immediate_sources':sources,'upstream_sources':upstream,'method':method,'transformation':transformation,'notes':notes,'expected_sha256':expected_sha}

def direct(urls,notes=''):
    return info('Primary source response',urls,urls,'Read-only HTTP GET; response body preserved without intentional modification.',notes=notes)

def derived(parents,script,notes=''):
    return info('Derived dataset',parents,parents,f'Local transformation using `{script}`.',transformation=script,notes=notes)

def packet_ledger_upstream():
    ledger=json.loads((ROOT/'downloads/packaged_ledger.json').read_text())
    rows=[]
    for section in ['original_operations','related_tla_and_treasury_operations_after_cutoff','additional_between_one_and_three_month_admin_deadlines']:
        for x in ledger.get(section,[]):
            rows.append({k:x.get(k) for k in ['timestamp','hash','label','kind','contract','sender','block_height','explorer_url','primary_source_file','source_file','old_sha256','new_sha256','approval_status']})
    (ROOT/'downloads/packaged_ledger.upstream.json').write_text(json.dumps({'upstream_note':'Per-operation original transaction links. Local primary_source_file names are retained; an independent public URL is not established for every named supporting file.','operations':rows},indent=2))

def board_upstream():
    d=json.loads((ROOT/'data/mb_voting_record.json').read_text())
    rows=[]
    for x in d['records']:
        rows.append({k:x.get(k) for k in ['proposal_id','title','ballot_query_url','proposal_source','mb_vote_lcd_tx_url','philipp_vote_lcd_tx_url','creation_time_source','ballot_sha256','ballot_capture_utc']})
    (ROOT/'data/mb_voting_record.upstream.json').write_text(json.dumps({'source_index_note':'The packet source index states that 597 raw response bodies and prior verification files were included. These per-record fields identify original ballot/proposal queries and vote transactions.','records':rows},indent=2))
packet_ledger_upstream();board_upstream()

def for_path(rel):
    p=rel.as_posix()
    if p=='data/mb_voting_record.json':
        immediate=PACKET+'exhibits/voting_record/mb_voting_record.json'
        return info('Preserved compiled evidence with embedded primary locators',[immediate],['data/mb_voting_record.upstream.json','data/source_index.json'],'Read-only retrieval from the supplied evidence packet.',notes='Upstream is established per record by ballot_query_url, proposal_source.source_url, vote LCD URLs, transaction hashes, and source hashes. Packet source index VOTE says 597 raw response bodies and prior verification files were included. This is not a claim that the compiled JSON is itself a raw chain response.')
    if p=='downloads/packaged_ledger.json':
        immediate=PACKET+'exhibits/authority/packaged_ledger.json'
        return info('Preserved analytical ledger with original transaction locators',[immediate],['downloads/packaged_ledger.upstream.json','data/source_index.json'],'Read-only retrieval from the supplied evidence packet.',notes='Each operation has an original explorer_url and block height. Supporting primary_source_file values are local retained-file names, not independent public URLs; those are marked upstream-not-established rather than inferred.')
    if p=='data/mb_voting_record.upstream.json':
        return derived(['data/mb_voting_record.json'],'analysis/generate_provenance.py','Operation-level upstream index generated from embedded source locators; no new chain data.')
    if p=='downloads/packaged_ledger.upstream.json':
        return derived(['downloads/packaged_ledger.json'],'analysis/generate_provenance.py','Operation-level upstream index generated from embedded transaction locators; no new chain data.')
    if p=='data/source_index.json':
        return info('Secondary source manifest',[PACKET+'source_index.json'],['https://philipp-payments.pages.dev/'],'Read-only retrieval from supplied packet.',notes='The manifest itself is not a primary chain record. Its per-file url fields are original upstream sources where non-null; null means upstream is not established by the packet.')
    if p=='data/SHA256SUMS.txt':
        return info('Secondary checksum manifest',[PACKET+'SHA256SUMS.txt'],['data/source_index.json'],'Read-only retrieval from supplied packet.',notes='Checksums support comparison with preserved packet files; they do not establish an upstream chain source by themselves.')
    if p=='data/download_manifest.json':
        return derived(['analysis/make_download_manifest.py'],'analysis/make_download_manifest.py','Generated URL manifest; source endpoints are listed inside the file.')
    if p=='data/payment_summary.json':
        return derived(['data/transfers/to_eris_all_transfers.json','data/treasury/outbound_transfers.json','data/treasury/actions/'],'analysis/generate_provenance.py and earlier payment-summary script','Summarizes monthly validator transfers, signer OTC flows, and action rosters; no new external data.')
    if p.startswith('data/native_4853/'):
        name=pathlib.PurePosixPath(p).name
        if name=='proposal.json':return direct([LCD+'/cosmos/gov/v1/proposals/4853'])
        if name=='votes.json':return direct([LCD+'/cosmos/gov/v1/proposals/4853/votes?pagination.limit=1000'],'Complete current ballot set at capture; later votes may change it.')
        if name=='tally.json':return direct([LCD+'/cosmos/gov/v1/proposals/4853/tally'],'Live tally at capture, not final result.')
        if name=='vote_transactions.json':return direct([LCD+"/cosmos/tx/v1beta1/txs?query=proposal_vote.proposal_id='4853'&pagination.limit=100&order_by=ORDER_BY_ASC"],'Contains vote transactions including superseded ballots.')
        if name=='signer_alx_vote_tx.json':return direct([LCD+'/cosmos/tx/v1beta1/txs/B8210663C2B8D7BE90F655FE11C7994FBCDFCF4FEB9890F3F2662FDEDB485AD6'])
    if p.startswith('data/smartstake_4853/'):
        return info('Explorer-derived table capture',[SMART],[LCD+'/cosmos/gov/v1/proposals/4853/votes?pagination.limit=1000'],'Read-only extraction of Smart Stake validator rows and account links.',notes='Explorer labels/stake values are secondary; native API records are primary cross-checks.')
    if p.startswith('data/current/'):
        name=pathlib.PurePosixPath(p).name
        if name=='registry_contract.json':return direct([LCD+'/cosmwasm/wasm/v1/contract/'+REGISTRY])
        if name=='registry_owner.json':return direct([smart(REGISTRY,{'ownership':{}})])
        if name=='treasury_contract.json':return direct([LCD+'/cosmwasm/wasm/v1/contract/'+TREASURY])
    if p.startswith('data/phoenix/'):
        name=pathlib.PurePosixPath(p).name
        if name=='current_config.json':return direct([smart(MAIN,{'config':{}})])
        if name=='current_members.json':return direct([smart(GROUP,{'list_members':{'limit':100}})])
        if name=='key_proposals.json':return direct([smart(MAIN,{'proposal':{'proposal_id':'<each of A116,A159,A175,A209,A215,A249,A266,A271,A272>'}}),smart(MAIN,{'list_votes':{'proposal_id':'<same IDs>','limit':100}})],'Fresh payload and ballot queries for the listed proposals.')
        if name=='recent_votes.json':return derived(['data/mb_voting_record.json'],'analysis/export_data.py','Filtered to proposals created on/after 2026-09-26.')
    if p=='data/phoenix_board_votes_all.csv':return derived(['data/mb_voting_record.json'],'analysis/export_data.py','CSV projection of preserved A1–A289 records.')
    if p=='data/phoenix_board_votes_last4weeks.csv':return derived(['data/mb_voting_record.json'],'analysis/export_data.py','CSV filtered to proposals created on/after 2026-09-26.')
    if p.startswith('data/forum/'):
        name=pathlib.PurePosixPath(p).name
        base=FORUM+'/t/phoenix-foundation-appointment-of-an-emergency-supervisor/47'
        if name=='topic_first20.json':return direct([base+'.json'],'Initial topic response and post-stream metadata, not all 92 posts.')
        if name=='posts_54_57.json':return direct([base+'/55.json'])
        if name=='posts_90_92.json':return direct([base+'/91.json'])
        if name=='post146_revision2.json':return direct([FORUM+'/posts/146/revisions/2.json'])
        if name=='suspension_fields.json':return direct([FORUM+'/u/PhoenixPinion.json',FORUM+'/u/MaxP.json',FORUM+'/u/Ex_TFL.json'],'Only public username/suspension fields retained; no identity investigation.')
    if p.startswith('data/eris_multisig/'):
        name=pathlib.PurePosixPath(p).name
        if name=='proposals.json':return direct([smart(ERIS,{'list_proposals':{'limit':100}})])
        if name=='votes.json':return direct([smart(ERIS,{'list_votes':{'proposal_id':'<1 through 9>','limit':100}})])
        if name=='voters.json':return direct([smart(ERIS,{'list_voters':{'limit':100}})])
        if name=='threshold.json':return direct([smart(ERIS,{'threshold':{}})])
        if name=='hub_config.json':return direct([smart(HUB,{'config':{}})])
        if name=='hub_delegations.json':return direct([LCD+'/cosmos/staking/v1beta1/delegations/'+HUB+'?pagination.limit=1000'])
        if name=='validator_profiles.json':return direct([LCD+'/cosmos/staking/v1beta1/validators/<Galactic Punks, Lion DAO, or ERIS operator address>'])
        if name=='transactions.json':return direct([LCD+"/cosmos/tx/v1beta1/txs?query=execute._contract_address='"+ERIS+"'&pagination.limit=100&order_by=ORDER_BY_DESC"])
        if name=='signer_alx_transactions.json':return direct([LCD+"/cosmos/tx/v1beta1/txs?query=message.sender='terra1alxk3fmhcl0ga80gl9yj9zp3ezjm4sdh8a9l9c'&pagination.limit=100&order_by=ORDER_BY_DESC"],'Sender search returned no useful history; the direct vote transaction is preserved separately.')
    if p=='data/eris_multisig_votes_all.csv':return derived(['data/eris_multisig/votes.json'],'analysis/export_data.py')
    if p=='data/eris_hub_delegations.csv':return derived(['data/eris_multisig/hub_delegations.json'],'analysis/export_data.py')
    if p=='data/native_4853_votes_all.csv':return derived(['data/native_4853/votes.json'],'analysis/export_data.py')
    if p=='data/native_4853_vote_transactions.csv':return derived(['data/native_4853/vote_transactions.json'],'analysis/export_data.py','Only vote messages exposed in structured transaction bodies; raw JSON retains all 87 responses.')
    if p.startswith('data/transfers/monthly_validator_to_eris/') or (p.startswith('data/transfers/validator_to_eris_') and p.endswith('.json')):
        h=pathlib.PurePosixPath(p).name.replace('_archive.json','').replace('.json','')
        return direct([ARCHIVE+'/cosmos/tx/v1beta1/txs/'+h])
    if p.startswith('data/transfers/wasm_') and p.endswith('.json'):
        name=pathlib.PurePosixPath(p).name
        if name.startswith('wasm_to_'):
            addr=name[len('wasm_to_'):-len('.json')]
            return direct([ARCHIVE+f"/cosmos/tx/v1beta1/txs?query=wasm.to='{addr}'&limit=100&page=1&order_by=ORDER_BY_DESC"])
        if name.startswith('wasm_from_'):
            addr=name[len('wasm_from_'):-len('.json')]
            return direct([ARCHIVE+f"/cosmos/tx/v1beta1/txs?query=wasm.from='{addr}'&limit=100&page=1&order_by=ORDER_BY_DESC"])
    if p=='data/transfers/validator_multisig_native_matches.json':
        return derived(['data/transfers/to_*.json'],'Native transfer matching','Empty match set; bounded by indexed history and explicit addresses.')
    if p=='data/transfers/validator_multisig_wasm_matches.json':
        return derived(['data/transfers/wasm_*.json'],'Contract-token event matching','Empty match set; bounded by indexed history and explicit addresses.')
    if p.startswith('data/transfers/to_') and (p.endswith('.json') or p.endswith('.csv')):
        name=pathlib.PurePosixPath(p).name
        if name=='to_eris_all_tx_responses.json':return direct([ARCHIVE+"/cosmos/tx/v1beta1/txs?query=transfer.recipient='terra1vm5azhvaxeanc7auxh02y8jmxrk8tj93f6aywp'&limit=100&page=1&order_by=ORDER_BY_DESC",ARCHIVE+"/cosmos/tx/v1beta1/txs?query=transfer.recipient='terra1vm5azhvaxeanc7auxh02y8jmxrk8tj93f6aywp'&limit=100&page=2&order_by=ORDER_BY_DESC"],'Deduplicated complete 172-response capture.')
        if name=='to_eris_all_pages.json':return derived(['data/transfers/to_eris_all_tx_responses.json'],'Browser pagination loop','Pagination metadata only.')
        if name=='to_eris_all_transfers.json':return derived(['data/transfers/to_eris_all_tx_responses.json'],'analysis/eris_incoming_patterns.py','Transfer events filtered to the ERIS recipient; decodes amount and denom.')
        if name=='to_eris_all_transfers.csv':return derived(['data/transfers/to_eris_all_transfers.json'],'analysis/eris_incoming_patterns.py')
        if name=='validator_multisig_native_matches.json':return derived(['data/transfers/to_*.json'],'Native transfer matching','Empty match set; bounded by indexed history and explicit addresses.')
        if name=='validator_multisig_wasm_matches.json':return derived(['data/transfers/wasm_*.json'],'Contract-token event matching','Empty match set; bounded by indexed history and explicit addresses.')
        if name.startswith('wasm_to_'):
            addr=name[len('wasm_to_'):-len('.json')];return direct([ARCHIVE+f"/cosmos/tx/v1beta1/txs?query=wasm.to='{addr}'&limit=100&page=1&order_by=ORDER_BY_DESC"])
        if name.startswith('wasm_from_'):
            addr=name[len('wasm_from_'):-len('.json')];return direct([ARCHIVE+f"/cosmos/tx/v1beta1/txs?query=wasm.from='{addr}'&limit=100&page=1&order_by=ORDER_BY_DESC"])
        addr=name[len('to_'):-len('.json')]
        archive=name.endswith('_archive.json')
        if archive:addr=addr[:-len('_archive')]
        base=ARCHIVE if archive else LCD
        return direct([base+f"/cosmos/tx/v1beta1/txs?query=transfer.recipient='{addr}'&pagination.limit=1000&order_by=ORDER_BY_DESC"],'Recipient query may return pruning errors for some providers; archive fallback is separately identified.')
    if p.startswith('data/treasury/signer_payments/') or p.startswith('data/treasury/claims/'):
        h=pathlib.PurePosixPath(p).stem
        return direct([ARCHIVE+'/cosmos/tx/v1beta1/txs/'+h])
    if p.startswith('data/treasury/actions/'):
        name=pathlib.PurePosixPath(p).stem
        if name=='recent_actions':return direct([smart(TREASURY,{'actions':{'limit':50}})],'Actions 1–50.')
        if name=='actions_after50':return direct([smart(TREASURY,{'actions':{'start_after':50,'limit':50}})],'Actions 51–100.')
        if name=='actions_after100':return direct([smart(TREASURY,{'actions':{'start_after':100,'limit':50}})],'Actions 101–121 at capture.')
        return direct([smart(TREASURY,{'action':{'id':int(name)}})])
    if p.startswith('data/treasury/'):
        name=pathlib.PurePosixPath(p).name
        if name=='outbound_transactions.json':return direct([ARCHIVE+f"/cosmos/tx/v1beta1/txs?query=transfer.sender='{TREASURY}'&pagination.limit=1000&order_by=ORDER_BY_ASC"],'Initial 100-response capture; superseded by the complete 169-response file.')
        if name=='outbound_all_tx_responses.json':return direct([ARCHIVE+f"/cosmos/tx/v1beta1/txs?query=transfer.sender='{TREASURY}'&limit=100&page=1&order_by=ORDER_BY_ASC",ARCHIVE+f"/cosmos/tx/v1beta1/txs?query=transfer.sender='{TREASURY}'&limit=100&page=2&order_by=ORDER_BY_ASC"],'Deduplicated complete 169-response capture.')
        if name=='outbound_all_pages.json':return derived(['data/treasury/outbound_all_tx_responses.json'],'Browser legacy page loop','Pagination metadata only.')
        if name in ['outbound_transfers.json','outbound_transfers.csv']:return derived(['data/treasury/outbound_all_tx_responses.json'],'analysis/treasury_patterns.py','Only transfer events whose sender is the Phoenix Treasury; amount/denom decoded.')
    if p.startswith('repos/contracts-tokenfactory/'):
        rel=p.removeprefix('repos/contracts-tokenfactory/')
        url='https://raw.githubusercontent.com/erisprotocol/contracts-tokenfactory/main/'+rel
        return direct([url],'Public source at main when captured; repository commit 967d9e8482f0519365e22c8a8afb93cb4e9d1549 was identified separately.')
    if p.startswith('repos/phoenix-docs/'):
        name=pathlib.PurePosixPath(p).name
        if name=='tla_launch.md':return direct(['https://raw.githubusercontent.com/phoenix-directive/docs/7cebbd26048f0e1568a2aed55177090b90788d8b/common_backup/2024-08-12_24385_launching-terra-liquidity-alliance.md'])
        if name=='the-phoenix-directive.md':return direct(['https://raw.githubusercontent.com/phoenix-directive/docs/main/the-phoenix-directive.md'])
        if name=='community-guidelines.md':return direct(['https://raw.githubusercontent.com/phoenix-directive/docs/main/community-guidelines.md'])
    if p.startswith('website/source-records/original-pages/'):
        rel=p.removeprefix('website/source-records/original-pages/')
        immediate='https://philipp-payments.pages.dev/'+rel
        return info('Preserved packet HTML',[immediate],['data/source_index.json'],'Read-only retrieval of supplied packet HTML.',notes='The HTML is an immediate secondary source. Upstream original records are linked by the packet and source index, not by this HTML itself.')
    if p in ['website/dist/record/evidence/exhibits/voting_record/mb_voting_record.json','website/dist/record/evidence/exhibits/voting_record/mb_voting_record.csv']:
        immediate=PACKET+'exhibits/voting_record/'+pathlib.PurePosixPath(p).name
        return info('Preserved compiled voting evidence',[immediate],['data/mb_voting_record.upstream.json','data/source_index.json'],'Read-only retrieval or retained publication copy from the supplied evidence packet.','The operation-level upstream index links original ballot/proposal queries and vote transactions. Packet source index VOTE notes 597 raw response bodies and prior verification files.')
    if p=='website/dist/record/evidence/exhibits/authority/packaged_ledger.json':
        immediate=PACKET+'exhibits/authority/packaged_ledger.json'
        return info('Preserved analytical authority ledger',[immediate],['downloads/packaged_ledger.upstream.json','data/source_index.json'],'Read-only retrieval or retained publication copy from the supplied evidence packet.','Original transaction URLs are indexed per operation. Supporting retained-file names without public URLs are marked upstream-not-established.')
    if p.startswith('website/dist/record/evidence/'):
        rel=p.removeprefix('website/dist/record/evidence/')
        immediate=PACKET+rel
        entry=packet_by_file.get(rel)
        upstream=[];notes='';expected=None
        if entry:
            expected=entry.get('source_sha256')
            if entry.get('url'):upstream.append(entry['url'])
            notes=(entry.get('handling','')+' '+entry.get('note','')).strip()
        extra=urls_in_file(ROOT/p)
        for u in extra:
            if u!=immediate and u not in upstream:upstream.append(u)
        if not upstream:upstream=['UPSTREAM_NOT_ESTABLISHED']
        return info('Preserved packet artifact' if entry else 'Packet-linked artifact',[immediate],upstream,'Read-only retrieval or retained publication copy from the supplied evidence packet.',notes=notes,expected_sha=expected)
    if p.startswith('website/dist/record/readable/'):
        return derived(['website/dist/record/evidence/','data/source_index.json'],'website publication pipeline','Readable text generated from preserved evidence; original upstream URLs are in source_index and the underlying artifacts.')
    if p.startswith('website/dist/record/history/'):
        upstream=urls_in_file(ROOT/p) or ['website/dist/record/history/manifest.json','website/dist/record/history/sources/source-index.json']
        return info('Website history record or generated presentation', ['website build inputs'],upstream,'Existing website build/preservation pipeline; no independent re-download by this provenance script.',notes='Consult the local manifest/source-index for the original chain or forum response. Generated HTML is presentation, not primary evidence.')
    if p.startswith('website/dist/record/'):
        upstream=urls_in_file(ROOT/p) or ['data/source_index.json']
        return info('Website record or generated presentation',['website build inputs'],upstream,'Existing website build/preservation pipeline; no independent re-download by this provenance script.',notes='Generated presentation is not primary evidence; use the linked original response where available.')
    raise ValueError('No provenance rule for '+p)

def write_sidecar(path):
    rel=path.relative_to(ROOT)
    meta=for_path(rel)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    acquired=datetime.datetime.fromtimestamp(path.stat().st_mtime,datetime.timezone.utc).isoformat()
    generated=datetime.datetime.now(datetime.timezone.utc).isoformat()
    lines=['# Source and provenance','',f'- **Artifact:** `{rel.as_posix()}`',f'- **SHA-256:** `{digest}`',f'- **Artifact timestamp (UTC):** {acquired}',f'- **Sidecar generated (UTC):** {generated}',f'- **Classification:** {meta["classification"]}',f'- **Acquisition / transformation:** {meta["method"]}']
    if meta['transformation']!='None':lines.append(f'- **Transformation:** `{meta["transformation"]}`')
    if meta['expected_sha256']:
        status='matches packet source hash' if digest==meta['expected_sha256'] else 'does not match packet source hash (possibly publication transformation or different capture)'
        lines.append(f'- **Packet source SHA-256:** `{meta["expected_sha256"]}` ({status})')
    lines += ['','## Immediate source(s)','']
    lines += [f'- {x}' for x in meta['immediate_sources']]
    lines += ['','## Upstream original source(s)','']
    if meta['upstream_sources']==['UPSTREAM_NOT_ESTABLISHED']:
        lines += ['- **Upstream not established from the available records.** No original public URL is asserted.']
    else:
        lines += [f'- {x}' for x in meta['upstream_sources']]
    if meta['notes']:lines += ['','## Scope, limits, and notes','',meta['notes']]
    lines += ['','This sidecar records provenance only. It does not independently validate every assertion in the artifact.']
    out=path.with_name(path.name+'.source.md')
    out.write_text('\n'.join(lines)+'\n')

roots=[ROOT/'data',ROOT/'downloads',ROOT/'repos',ROOT/'website/source-records/original-pages',ROOT/'website/dist/record']
files=[]
for base in roots:
    for path in base.rglob('*'):
        if path.is_file() and not path.name.endswith('.source.md') and '.git' not in path.parts:
            files.append(path)
for path in files:write_sidecar(path)
index={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file_count':len(files),'convention':'Each artifact has a sibling <filename>.source.md with immediate and upstream sources, acquisition/transformation, notes, and SHA-256. UPSTREAM_NOT_ESTABLISHED means no original public source is asserted.','files':[str(p.relative_to(ROOT))+'.source.md' for p in files]}
(ROOT/'PROVENANCE.json').write_text(json.dumps(index,indent=2))
(ROOT/'PROVENANCE.md').write_text('# Provenance register\n\nEvery artifact under `data/`, `downloads/`, `repos/`, `website/source-records/original-pages/`, and `website/dist/record/` has a sibling `*.source.md` file.\n\nEach sidecar identifies the immediate source and, where established, the upstream original chain/forum/GitHub record. It also records acquisition or transformation, timestamps, SHA-256, and limitations. `UPSTREAM_NOT_ESTABLISHED` means no source is inferred.\n\nFor the supplied packet, `data/source_index.json` is used to map preserved files to original URLs. The voting record and authority ledger additionally have operation-level upstream indexes.\n\nTotal artifacts with sidecars: **'+str(len(files))+'**.\n')
print('sidecars',len(files))
