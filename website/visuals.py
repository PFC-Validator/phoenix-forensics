"""Evidence figures for the Holder briefing; static meaning precedes enhancement."""
from pathlib import Path
from html import escape
import re

ROOT=Path(__file__).parent
CONTROLLER=(ROOT/'motion-controller.js').read_text()

CASES=[
 dict(slug='superbolt',name='Superbolt',title='One invoice. Three roles.',
      intro='A company invoice on Neutron connects the proposer, voter and recipient.',
      roles=[('Philipp proposes','Invoice payment','P3 · invoice 2024-002'),('Philipp votes YES','A beneficiary participates','3 YES votes in total'),('Philipp receives','7,500 USDC','Paid 23 August 2024')],
      note='The proposal received three YES votes, including Philipp’s. This was not a unilateral approval. Payment followed the next day.',
      source='/governance/#beneficiary-votes',source_label='Inspect Superbolt approvals',raw='/record/evidence/exhibits/legacy/Belege/E10a.json'),
 dict(slug='creda',name='Creda',title='Approving a milestone for his project.',
      intro='A Terra project milestone: compare its approval with a later capture of the analytics page.',
      roles=[('Philipp proposes','Enable analytics milestone','A215'),('Philipp votes YES','Milestone release approved','75 YES weight of 100'),('Creda receives','10,000 USDC','Paid 27 January 2026')],
      note='Philipp proposed and voted for the analytics release. A later capture showed placeholders on the dedicated analytics page; it does not establish that no work was delivered.',
      source='/governance/#delivery',source_label='Compare approval and output',raw='/record/evidence/exhibits/legacy/Belege/E05b.json'),
 dict(slug='estima',name='Estima',title='The grant and its release were different votes.',
      intro='The original Terra project grant was approved by the other three directors; Philipp participated in releasing its kickoff payment.',
      roles=[('Other directors approve','125,000-USDC grant','A266 · other three directors'),('Philipp votes YES','Release the kickoff stage','A271'),('Estima receives','45,000 USDC','Paid 3 October 2026')],
      note='The 45,000-USDC kickoff was already paid. Another 80,000 USDC remained conditional and unpaid in the snapshot. Project funding is not a statement of personal profit.',
      source='/governance/#estima-release',source_label='Inspect Estima grant and release',raw='/record/evidence/exhibits/legacy/Belege/E05g.json')
]

def person(x,y,stroke):
    return f'<g fill="none" stroke="{stroke}" stroke-width="1.5" aria-hidden="true"><circle cx="{x}" cy="{y-5}" r="5"/><path d="M{x-9} {y+12}v-4a9 9 0 0 1 18 0v4"/></g>'

def role_svg(case,mobile=False,prefix='case'):
    slug=f'{prefix}-{case["slug"]}'+('-mobile' if mobile else '-wide')
    w,h=(320,576) if mobile else (768,224)
    boxes=[(40,40,240,112),(40,208,240,112),(40,376,240,112)] if mobile else [(40,32,208,120),(280,32,208,120),(520,32,208,120)]
    paths=['M160 152V208','M160 320V376'] if mobile else ['M248 92H280','M488 92H520']
    content=f'<svg class="role-svg {"role-mobile" if mobile else "role-wide"}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{escape(case["name"])}: decision and beneficiary</title><desc id="{slug}-desc">{escape(case["intro"]+" "+case["note"])}</desc><defs><marker id="{slug}-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><path d="M0 0 8 3 0 6Z" fill="#b8dfbd"/></marker></defs>'
    for p in paths: content+=f'<path d="{p}" fill="none" stroke="#b8dfbd" stroke-width="1.5" marker-end="url(#{slug}-arrow)"/>'
    for i,((x,y,bw,bh),(title,detail,sub)) in enumerate(zip(boxes,case['roles'])):
        focal=i==1;fill='#d9ecdf' if focal else '#173d32';ink='#173d32' if focal else '#f1f7f3';muted='#345b48' if focal else '#c4d9cb';stroke='#b8dfbd' if focal else '#87aa95'
        content+=f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{fill}" stroke="{stroke}"/>'
        # Small person marks identify a human decision; the project receipt uses a document mark.
        if i<2 or case['slug']=='superbolt':content+=person(x+bw-28 if not mobile and title=='Other directors approve' else x+24,y+27,ink)
        else:content+=f'<path d="M{x+17} {y+15}h14v24h-14z M{x+20} {y+23}h8 M{x+20} {y+28}h8" fill="none" stroke="{ink}" stroke-width="1.5" aria-hidden="true"/>'
        ty=y+56
        if not mobile and title=='Other directors approve':
            content+=f'<text x="{x+16}" y="{y+48}" font-family="Source Sans 3, sans-serif" font-size="16" font-weight="600" fill="{ink}">Other directors</text><text x="{x+16}" y="{y+66}" font-family="Source Sans 3, sans-serif" font-size="16" font-weight="600" fill="{ink}">approve</text>'
            ty=y+64
        else:
            content+=f'<text x="{x+16}" y="{ty}" font-family="Source Sans 3, sans-serif" font-size="16" font-weight="600" fill="{ink}">{escape(title)}</text>'
        content+=f'<text x="{x+16}" y="{ty+24}" font-family="Source Sans 3, sans-serif" font-size="12" fill="{muted}">{escape(detail)}</text>'
        content+=f'<text x="{x+16}" y="{ty+44}" font-family="ui-monospace, monospace" font-size="9" fill="{muted}">{escape(sub)}</text>'
    ly=528 if mobile else 184
    content+=f'<path d="M40 {ly}H{w-40}" stroke="#87aa95"/><text x="40" y="{ly+24}" font-family="Source Sans 3, sans-serif" font-size="11" fill="#c4d9cb">'+('Proposal → approval → receipt' if mobile else 'Arrows show the recorded decision-to-payment sequence, not sole control or proof of wrongdoing.')+'</text></svg>'
    return content

def roles_section():
    tabs='<div class="case-controls" role="tablist" aria-label="Choose a funding example" hidden>'+''.join(f'<button type="button" id="tab-{c["slug"]}" role="tab" aria-controls="panel-{c["slug"]}" aria-selected="{str(i==0).lower()}">{c["name"]}</button>' for i,c in enumerate(CASES))+'</div>'
    panels=''
    for i,c in enumerate(CASES):
        panels+=f'<section class="case-panel" id="panel-{c["slug"]}" aria-labelledby="case-title-{c["slug"]}"><div class="case-heading"><h2 id="case-title-{c["slug"]}">{c["title"]}</h2><p>{c["intro"]}</p></div><div class="role-canvas">{role_svg(c)}{role_svg(c,True)}</div><div class="case-foot"><p>{c["note"]}</p><a href="{c["source"]}">{c["source_label"]} <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg></a></div></section>'
    return '<div class="case-study" data-cases>'+tabs+panels+'</div>'

EVENTS=[
 ('30 Sep 2026','Philipp votes YES','A271 releases the kickoff stage.','Release vote','/record/evidence/exhibits/legacy/Belege/E05g.json'),
 ('3 Oct · 14:47 UTC','Estima is paid','45,000 USDC reaches the project account.','Kickoff payment','/record/evidence/exhibits/legacy/Belege/E05e.json'),
 ('3 Oct · 15:02 UTC','A272 is submitted','14 minutes 35 seconds after payment.','A272 submission','/record/evidence/exhibits/legacy/Belege/E09a.json'),
 ('24 Oct snapshot','A272 failed','Four equal seats and 75% remain.','Captured outcome','/record/evidence/exhibits/legacy/Belege/E09c.json')
]

def timeline_svg(mobile=False,prefix='sequence'):
    slug=prefix+('-mobile' if mobile else '-wide');w,h=(320,748) if mobile else (768,320)
    content=f'<svg class="sequence-svg {"sequence-mobile" if mobile else "sequence-wide"}" viewBox="0 0 {w} {h}" role="img" xmlns="http://www.w3.org/2000/svg" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">Estima payment and A272: the sequence</title><desc id="{slug}-desc">Philipp voted for the Estima release on 30 September; payment and the A272 submission followed on 3 October, with A272 recorded failed in the later snapshot; timing alone does not establish motive.</desc>'
    if mobile:
        # Breaks between clusters mark unequal durations; this is not a proportional axis.
        for y in [96,264,432]:content+=f'<path d="M52 {y}v48m-4 0 8 8m-8 0 8 8m-4 0v56" fill="none" stroke="#729a83" stroke-width="1.5"/>'
    else:
        for x in [76,252,428]:content+=f'<path d="M{x} 108h44m0-4 8 8m0-8 8 8m0-4h68" fill="none" stroke="#729a83" stroke-width="1.5"/>'
    for i,(date,title,detail,short,url) in enumerate(EVENTS):
        x,y=(40,52+i*168) if mobile else (40+i*176,76)
        cx=x+12;cy=y+20 if mobile else 108
        content+=f'<g data-motion-item data-step="{i+1}" aria-label="{escape(date+": "+title+". "+detail) if not mobile else short}"><circle class="sequence-ring" cx="{cx}" cy="{cy}" r="12" fill="#fff" stroke="#28654f" stroke-width="1.5"/><text x="{cx}" y="{cy+4}" text-anchor="middle" fill="#203e35" font-family="Source Sans 3, sans-serif" font-size="12" font-weight="600">{i+1}</text>'
        if mobile:
            content+=f'<text x="{x+36}" y="{y+24}" font-family="ui-monospace, monospace" font-size="9" fill="#526459">{escape(date)}</text><text x="{x+36}" y="{y+56}" font-family="Source Sans 3, sans-serif" font-size="12" font-weight="600" fill="#203e35">{escape(title)}</text>'
            line1,line2={0:('A271 releases','the kickoff stage.'),1:('45,000 USDC reaches','the project account.'),2:('14 minutes 35 seconds','after payment.'),3:('Four equal seats;','75% threshold remains.')}[i]
            content+=f'<text x="{x+36}" y="{y+80}" font-family="Source Sans 3, sans-serif" font-size="12" fill="#526459">{line1}</text><text x="{x+36}" y="{y+100}" font-family="Source Sans 3, sans-serif" font-size="12" fill="#526459">{line2}</text>'
        else:
            content+=f'<text x="{x}" y="64" font-family="ui-monospace, monospace" font-size="9" fill="#526459">{escape(date)}</text><text x="{x}" y="164" font-family="Source Sans 3, sans-serif" font-size="16" font-weight="600" fill="#203e35">{escape(title)}</text>'
            line1,line2={0:('A271 releases','the kickoff stage.'),1:('45,000 USDC reaches','the project account.'),2:('14 minutes 35 seconds','after payment.'),3:('Four equal seats;','75% threshold remains.')}[i]
            content+=f'<text x="{x}" y="196" font-family="Source Sans 3, sans-serif" font-size="12" fill="#526459">{line1}</text><text x="{x}" y="216" font-family="Source Sans 3, sans-serif" font-size="12" fill="#526459">{line2}</text>'
        content+=f'<path class="sequence-underline" data-motion-decorative aria-hidden="true" focusable="false" pathLength="1" d="M{x+36 if mobile else x} {y+116 if mobile else 244}h{168 if mobile else 152}" fill="none" stroke="#28654f" stroke-width="2"/>'
        content+='</g>'
    ly=712 if mobile else 280
    content+=f'<path d="M40 {ly}H{w-40}" stroke="#cddbd3"/><text x="40" y="{ly+24}" font-family="Source Sans 3, sans-serif" font-size="11" fill="#526459">'+('Axis breaks: unequal intervals.' if mobile else 'Chronological order. Axis breaks mark unequal intervals; horizontal distance is not elapsed time.')+'</text></svg>'
    return content

def timeline_section(prefix='home-sequence'):
    controls='''<div data-motion-controls role="group" aria-label="Timeline playback controls"><button type="button" data-motion-action="prev" aria-label="Previous event">Previous</button><button type="button" data-motion-action="play" aria-pressed="false">Play timeline</button><button type="button" data-motion-action="pause" aria-pressed="true">Pause</button><button type="button" data-motion-action="next" aria-label="Next event">Next</button><button type="button" data-motion-action="replay">Replay</button><span data-motion-status-visible aria-hidden="true">Event <span data-motion-step-label>4</span> of 4</span></div>'''
    return f'''<section class="sequence-section" id="{prefix}" data-motion-root data-motion-mode="step" data-step-count="4" data-step-current="4" data-frame="static" data-static-frame="complete" style="--motion-total:2880ms"><div class="sequence-intro"><div><h2>The Estima decision timeline</h2><p>Follow the Estima payment and the proposal to change the board.</p></div><a class="quiet-link" href="/timeline/">Read the full timeline</a></div><div class="sequence-canvas">{timeline_svg(prefix=prefix)}{timeline_svg(True,prefix=prefix)}</div>{controls}<p class="sequence-static-note">All four events are shown. Motion is optional.</p><p class="sequence-help">Play the sequence, or use Previous and Next. Keyboard: left/right arrows to step; Home/End to jump.</p><p class="visually-hidden" data-motion-status role="status" aria-live="polite" aria-atomic="true"></p><div class="sequence-sources">{''.join(f'<a href="{url}">{short}</a>' for date,title,detail,short,url in EVENTS)}</div><p class="sequence-caveat">The payment, submission and outcome are recorded facts. Their timing alone does not establish motive. A272 failed.</p><noscript><p>The complete timeline is shown. Playback controls require JavaScript.</p></noscript></section>'''

def motion_script():return '<script data-diagram-controls>'+CONTROLLER+'</script>'

def write_standalones(dist):
    font='<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600&amp;family=Source+Sans+3:wght@400;600&amp;display=swap" rel="stylesheet">'
    base='''body{margin:0;padding:24px;background:#fff;color:#203e35;font:18px/1.5 'Source Sans 3',sans-serif}main{max-width:1120px;margin:auto;min-width:0}h1,h2{font-family:'Public Sans',sans-serif;font-weight:600}h1{font-size:28px}svg{display:block;width:100%}.role-canvas,.sequence-canvas{max-width:100%;min-width:0;overflow-x:auto}.role-svg{min-width:768px}.role-mobile,.sequence-mobile{display:none}.sequence-svg{min-width:768px}.sequence-help,.sequence-caveat{font-size:16px}.sequence-sources{display:none}.visually-hidden{position:absolute;clip:rect(0,0,0,0);width:1px;height:1px;overflow:hidden}.sequence-section{--motion-hold:720ms;--motion-step:480ms;--motion-fast:160ms;--motion-total:2880ms}.sequence-ring{transition:fill 480ms cubic-bezier(.2,.8,.2,1)}.sequence-underline{opacity:0;stroke-dasharray:1;stroke-dashoffset:1}.motion-ready .is-current .sequence-underline{opacity:1;animation:sequence-trace 480ms cubic-bezier(.2,.8,.2,1) forwards}@keyframes sequence-trace{to{stroke-dashoffset:0}}.is-current .sequence-ring{fill:#b8dfbd}.motion-ready [data-motion-controls]{display:flex;gap:8px;flex-wrap:wrap}[data-motion-controls]{display:none}[data-motion-controls][hidden]{display:none!important}[data-motion-controls] button{min-width:44px;min-height:44px;border:1px solid #729a83;background:#fff;border-radius:4px;color:#203e35;font:600 14px 'Source Sans 3',sans-serif}[data-motion-controls] button:focus-visible{outline:3px solid #28654f;outline-offset:3px}[data-motion-controls] button:disabled{opacity:.45;cursor:default}[data-motion-controls] button[aria-pressed=true]{background:#e9f1ed}@media(max-width:700px){.role-wide,.sequence-wide{display:none}.role-mobile,.sequence-mobile{display:block}.role-mobile,.sequence-mobile{min-width:320px}}@media(prefers-reduced-motion:reduce){[data-motion-item]{opacity:1!important;transform:none!important}[data-motion-controls],[data-motion-decorative]{display:none!important}*{animation:none!important;transition:none!important}}@media print{[data-motion-controls],[data-motion-decorative]{display:none!important}[data-motion-item]{opacity:1!important;transform:none!important}svg{min-width:0}.role-canvas,.sequence-canvas{overflow:visible}}'''
    for c in CASES:
        title=c['name']+': decision and beneficiary';body=f'<main><h1>{title}</h1><p>{c["intro"]}</p><div class="role-canvas" style="background:#173d32">{role_svg(c,prefix="standalone")}{role_svg(c,True,prefix="standalone")}</div><p>{c["note"]}</p><p>Source: Philipp Payments, supporting records, {c["name"]} payment approvals.</p></main>'
        (dist/'diagrams'/f'{c["slug"]}-roles.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>{font}<style>{base}</style></head><body>{body}</body></html>')
    section=timeline_section('estima-sequence').replace('<a class="quiet-link" href="/timeline/">Read the full timeline</a>','')
    section=re.sub(r'<div class="sequence-sources">.*?</div>','',section)
    (dist/'diagrams'/'estima-sequence.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Estima payment and A272: the sequence</title>{font}<style>{base}</style></head><body><main><h1>Estima payment and A272</h1>{section}</main>{motion_script()}</body></html>')
