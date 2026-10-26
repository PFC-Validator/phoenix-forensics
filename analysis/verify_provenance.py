import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASES=['data','downloads','repos','website/source-records/original-pages','website/dist/record']
missing=[];bad_hash=[];missing_upstreams=[];count=0;not_established=[]
for base in BASES:
 for path in (ROOT/base).rglob('*'):
  if not path.is_file() or path.name.endswith('.source.md'):continue
  count+=1
  side=path.with_name(path.name+'.source.md')
  if not side.exists():
   missing.append(str(path));continue
  text=side.read_text()
  digest=hashlib.sha256(path.read_bytes()).hexdigest()
  if f'**SHA-256:** `{digest}`' not in text:bad_hash.append(str(path))
  if '## Immediate source(s)' not in text or '## Upstream original source(s)' not in text:missing_upstreams.append(str(path))
  if 'Upstream not established' in text:not_established.append(str(path))
assert not missing,missing
assert not bad_hash,bad_hash
assert not missing_upstreams,missing_upstreams
board=json.loads((ROOT/'data/mb_voting_record.upstream.json').read_text())
assert len(board['records'])==289
ledger=json.loads((ROOT/'downloads/packaged_ledger.upstream.json').read_text())
original=json.loads((ROOT/'downloads/packaged_ledger.json').read_text())
expected=sum(len(original.get(k,[])) for k in ['original_operations','related_tla_and_treasury_operations_after_cutoff','additional_between_one_and_three_month_admin_deadlines'])
assert len(ledger['operations'])==expected,(len(ledger['operations']),expected)
register=json.loads((ROOT/'PROVENANCE.json').read_text())
assert register['file_count']==count,(register['file_count'],count)
print(json.dumps({'artifacts_with_sidecars':count,'upstream_not_established':len(not_established),'board_upstream_records':len(board['records']),'authority_upstream_operations':len(ledger['operations']),'hash_and_section_checks':'passed'},indent=2))
