"""Publish neutral evidence guides instead of mirroring accusatory commentary."""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import re

POLICY = ('This briefing examines funding decisions and governance procedures, not personal character. '
          'It does not allege dishonesty or infer intent from a payment, vote or sequence of events. '
          'Discussion and corrections should address specific records; personal attacks, unwanted contact and harassment have no place here.')

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.href=None; self.label=[]
    def handle_starttag(self, tag, attrs):
        if tag=='a': self.href=dict(attrs).get('href'); self.label=[]
    def handle_data(self, text):
        if self.href: self.label.append(text)
    def handle_endtag(self, tag):
        if tag=='a' and self.href:
            self.links.append((self.href, ''.join(self.label))); self.href=None

def apply_editorial(dist, page, head):
    dist=Path(dist)
    # The older narrative is not a neutral editorial voice. Retain the underlying
    # financial/technical downloads, with clearly labelled curated source guides.
    routes={'':'Source records','payments/':'Payment source records','evidence/':'Supporting evidence',
            'history/':'Chronology source records','handover/':'Contract administration records','sources/':'Source library'}
    renamed={'handover':'Handover terms and response','authority':'Recorded technical operations',
             'current':'Dated contract configuration','payments':'Payment proposals and approvals',
             'delivery':'Milestone terms and recorded delivery','governance':'A272 proposal and outcome',
             'votes':'Voting records','timeline':'Dated transaction records','sources':'Source downloads',
             'methods':'Accounting method and qualifications','supporting':'Additional funding context',
             'promise':'Published handover terms','method':'Scope and counting method'}
    for route,title in routes.items():
        path=dist/'record'/route/'index.html'
        if not path.exists(): continue
        original=path.read_text()
        ids=list(dict.fromkeys(re.findall(r'\bid=["\']([^"\']+)',original)))
        parser=Links(); parser.feed(original)
        links=[]; seen=set()
        for href,label in parser.links:
            target=urljoin('/record/'+route,unescape(href))
            if not target.startswith('/record/') or urlparse(target).fragment: continue
            if any(x in target for x in ('censorship-records','forum-statements','events.json','events.csv','public-identity')): continue
            local=dist/urlparse(target).path.lstrip('/')
            if not local.is_file() or local.suffix not in {'.json','.csv','.txt','.pdf','.rs'}: continue
            if target in seen: continue
            seen.add(target)
            # File names identify downloads without inheriting editorial link labels.
            links.append('<li><a href="'+escape(target,quote=True)+'">'+escape(local.name)+'</a></li>')
        anchors=''.join('<span id="'+escape(i,quote=True)+'"></span>' for i in ids if i not in {'main-record','public-identity','pressure','censorship','forum-records'})
        body=head(title,'A curated guide to the underlying funding and governance records.')
        body+='<div class="wrap page-content reading">'+anchors+'<p class="context-note">'+POLICY+'</p>'
        body+='<p>The original site’s commentary is not reproduced here. These guides retain relevant source downloads; the shorter briefing explains their scope, caveats and alternative explanations.</p>'
        body+='<p><a href="/funding/">Funding and accounting method</a> · <a href="/governance/">Approvals, delivery and technical control</a> · <a href="/timeline/">Dated chronology</a></p>'
        body+='<h2>Read the records in context</h2><p>Project receipts are not a measure of personal profit. A beneficiary’s participation does not alone establish wrongdoing. Timing and voting agreement do not establish motive. Dated captures do not describe every later development.</p>'
        body+='<details class="evidence-detail"><summary>Available source downloads ('+str(len(links))+')</summary><ul>'+''.join(links)+'</ul></details></div>'
        page(title,body,'/record/'+route)
    # Do not serve personal-allegation galleries or the older authored chronology.
    # Primary proposals, votes, transfers and technical records remain available.
    import shutil,json
    folder=dist/'record/evidence/censorship-records'
    if folder.exists(): shutil.rmtree(folder)
    for rel in ['history/events.json','history/events.csv']:
        p=dist/'record'/rel
        if p.exists(): p.unlink()
    removed=('censorship-records','events.json','events.csv')
    def prune(v):
        if isinstance(v,list):
            return [prune(x) for x in v if not (isinstance(x,dict) and any(isinstance(y,str) and any(t in y for t in removed) for k,y in x.items() if k in {'url','file','path'}))]
        if isinstance(v,dict): return {k:prune(x) for k,x in v.items()}
        return v
    for rel in ['evidence/source_index.json','history/sources/source-index.json','history/manifest.json','verification.json']:
        p=dist/'record'/rel
        if p.exists(): p.write_text(json.dumps(prune(json.loads(p.read_text())),ensure_ascii=False,indent=2))
    (dist/'record/llms.txt').write_text('LUNA Holder Briefing\nNeutral funding and governance briefing.\nSources and method: /sources/\nFunding: /funding/\nGovernance: /governance/\nTimeline: /timeline/\n'+POLICY+'\n')
