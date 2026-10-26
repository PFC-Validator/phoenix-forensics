"""Scan tracked files without printing any candidate secret values."""
import json,pathlib,re,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
FILES=[f for f in subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0') if f]
PATTERNS={
 'private_key_block':re.compile(rb'-----BEGIN (?:OPENSSH |RSA |EC |DSA |PGP )?PRIVATE KEY-----'),
 'github_token':re.compile(rb'\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|gho_[A-Za-z0-9]{20,}|ghu_[A-Za-z0-9]{20,}|ghs_[A-Za-z0-9]{20,}|ghr_[A-Za-z0-9]{20,})'),
 'aws_access_key':re.compile(rb'\bAKIA[A-Z0-9]{16}\b'),
 'slack_token':re.compile(rb'\bxox[baprs]-[A-Za-z0-9-]{10,}'),
 'google_api_key':re.compile(rb'\bAIza[A-Za-z0-9_-]{30,}'),
 'stripe_key':re.compile(rb'\b[sr]k_(?:live|test)_[A-Za-z0-9]{16,}'),
 'openai_key':re.compile(rb'\bsk-[A-Za-z0-9_-]{20,}'),
 'credential_url':re.compile(rb'https?://[^\s/:@]+:[^\s/@]+@'),
 'auth_header':re.compile(rb'(?i)(?:authorization|proxy-authorization)\s*[:=]\s*(?:bearer|basic)\s+[A-Za-z0-9_./+=-]{8,}'),
 'generic_secret_assignment':re.compile(rb'(?i)\b(?:gh[_-]?token|github[_-]?token|token|secret|password|credential|private[_-]?key|api[_-]?token|api[_-]?secret|access[_-]?token|refresh[_-]?token|client[_-]?secret|session[_-]?key)\b\s*[:=]\s*[\"\'][^\"\'\r\n]{3,}[\"\']'),
}
findings=[]
for f in FILES:
 p=ROOT/f
 try:data=p.read_bytes()
 except OSError:continue
 if b'\0' in data[:8192]:continue
 for kind,pattern in PATTERNS.items():
  for match in pattern.finditer(data):
   findings.append({'file':f,'type':kind,'line':data.count(b'\n',0,match.start())+1})
sensitive_names={'.env','.env.local','.env.production','id_rsa','id_dsa','credentials','credentials.json','.git-credentials'}
filename_issues=[f for f in FILES if any(part in sensitive_names or part.endswith(('.pem','.p12','.pfx','.key')) for part in pathlib.PurePosixPath(f).parts)]
symlinks=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_symlink() and '.git' not in p.relative_to(ROOT).parts]
result={'tracked_files_scanned':len(FILES),'findings':findings,'sensitive_filenames':filename_issues,'symlinks':symlinks,'candidate_values_included':False}
print(json.dumps(result,indent=2))
sys.exit(1 if findings or filename_issues or symlinks else 0)
