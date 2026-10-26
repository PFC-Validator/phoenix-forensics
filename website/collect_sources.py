from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from urllib.request import Request, urlopen
import json

BASE = 'https://philipp-payments.pages.dev/'
ROOT = Path(__file__).parent
DEST = ROOT / 'dist' / 'record'
class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for k in ('href','src'):
            if d.get(k): self.links.append(d[k])

def normalized(link, current):
    if link.startswith('data/'): current=BASE
    u = urlparse(urljoin(current, link))
    if u.netloc != urlparse(BASE).netloc: return None
    return u._replace(query='', fragment='').geturl()

def fetch(url):
    rel = unquote(urlparse(url).path).lstrip('/')
    if not rel or rel.endswith('/'): rel += 'index.html'
    path = DEST / rel
    if '..' in Path(rel).parts: return (url, [], 'unsafe path')
    try:
        if not path.exists():
            req = Request(url, headers={'User-Agent':'LUNA-holder-briefing-source-preservation/1.0'})
            with urlopen(req, timeout=30) as r: body = r.read()
            path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(body)
        else: body = path.read_bytes()
        links = []
        if rel.endswith('.html'):
            p=Links(); p.feed(body.decode()); links=p.links
        elif rel.endswith('.json'):
            def walk(x):
                if isinstance(x,dict):
                    for v in x.values(): walk(v)
                elif isinstance(x,list):
                    for v in x: walk(v)
                elif isinstance(x,str) and (x.startswith(('/', 'data/', './', '../')) or x.startswith(BASE)) and not any(c in x for c in ('\n',' ')) and __import__('re').search(r'\.(json|csv|txt|md|html|pdf|png|svg|wasm)(?:$|[?#])',x):
                    links.append(x)
            try: walk(json.loads(body))
            except (ValueError, UnicodeError): pass
        return url, [v for x in links if (v:=normalized(x,url))], None
    except Exception as e: return url, [], str(e)

seen=set(); pending=[BASE]; report=[]
with ThreadPoolExecutor(max_workers=8) as ex:
    while pending and len(seen)<700:
        batch=[x for x in dict.fromkeys(pending) if x not in seen]; pending=[]
        seen.update(batch)
        for url, links, error in ex.map(fetch,batch):
            report.append({'url':url,'error':error})
            pending.extend(x for x in links if x not in seen)
    # app.js builds ledger URLs from metadata, so ensure its declared data dependencies are retained.
for asset in ('app.js','site.js'):
    path=DEST/asset
    if path.exists():
        import re
        for link in re.findall(r'[\'"](data/[^\'"`]+\.(?:json|csv))[\'"]',path.read_text()):
            u=normalized(link,BASE)
            if u and u not in seen:
                url,links,error=fetch(u);report.append({'url':url,'error':error})
(ROOT/'source-records'/'download-register.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'downloaded':len(report),'errors_count':sum(bool(x['error']) for x in report),'errors_sample':[x for x in report if x['error']][:8],'bytes':sum(x.stat().st_size for x in DEST.rglob('*') if x.is_file())}))
