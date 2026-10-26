(() => {
  const dialog = document.querySelector('#ledger');
  const body = document.querySelector('#ledger-body');
  const prev = document.querySelector('#previous');
  const next = document.querySelector('#next');
  const pageStatus = document.querySelector('#page-status');
  const cache = new Map();
  let index, selected, page = 0, request = 0;
  const money = n => n == null ? 'Unpriced' : new Intl.NumberFormat('en-US', {style:'currency',currency:'USD',minimumFractionDigits:2}).format(Number(n));
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const date = d => d ? new Intl.DateTimeFormat('en-GB',{dateStyle:'medium',timeStyle:'short',timeZone:'UTC'}).format(new Date(d))+' UTC' : 'Date unavailable';
  const amount = n => n==null ? '' : new Intl.NumberFormat('en-US',{maximumFractionDigits:8}).format(Number(n));
  function link(url,label) { return url && /^(https?:\/\/|data\/)/.test(url) ? '<a href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">'+esc(label)+'</a>' : ''; }
  async function json(url) {
    if (cache.has(url)) return cache.get(url);
    const r=await fetch(url); if(!r.ok) throw new Error('Receipt file could not be loaded.');
    const d=await r.json();cache.set(url,d);return d;
  }
  function cell(label,value) { return value == null || value === '' ? '' : '<dt>'+esc(label)+'</dt><dd>'+esc(value)+'</dd>'; }
  function renderReceipt(r) {
    const hash=r.tx || ('Block '+r.height+' · EndBlock event '+r.event);
    const detail=cell('Transaction',r.tx)+cell('Chain',r.chain)+cell('Block',r.height)+cell('Event / coin',r.event == null ? null : r.event+' / '+(r.coin ?? ''))+cell('From',r.sender)+cell('To',r.recipient)+cell('Beneficiary',r.beneficiary && r.beneficiary!==r.recipient ? r.beneficiary : null)+cell('Token amount',r.amount+' '+r.asset)+cell('Denomination',r.denomination)+cell('USD, unrounded',r.usd)+cell('Price time',r.price_time)+cell('Price method',r.price_method)+cell('Market quote',r.market_quote)+cell('USD conversion',r.fx_quote)+cell('Unpriced reason',r.unpriced_reason)+cell('Purpose',r.purpose);
    return '<li><div class="receipt-top"><div><time>'+esc(date(r.date))+'</time><div class="receipt-amount">'+esc(amount(r.amount)+' '+r.asset)+'</div></div><div class="num">'+money(r.usd)+'</div></div><div class="receipt-evidence">'+link(r.explorer||r.source,r.tx ? hash.slice(0,12)+'…'+hash.slice(-8)+' ↗' : hash+' ↗')+(r.explorer && r.source ? link(r.source,'Raw chain record ↗') : '')+'</div>'+(!r.tx?'<p class="receipt-link-note">Governance block transfer; no ordinary transaction hash.</p>':'')+'<details><summary>Full transaction, wallets &amp; valuation</summary><dl>'+detail+'</dl>'+((r.price_sources||[]).map((u,i)=>link(u,'Price source '+(i+1)+' ↗')).join(' · '))+'</details></li>';
  }
  async function render() {
    const ticket=++request;
    const meta=index[selected], last=Math.ceil(meta.count/50);
    prev.disabled=true;next.disabled=true;
    body.innerHTML='<p class="caption">Loading receipt events…</p>';
    pageStatus.textContent='Page '+(page+1)+' of '+last.toLocaleString('en-US');
    try {
      const chunk=await json(meta.pages[Math.floor(page/5)]);
      if(ticket!==request)return;
      const start=(page%5)*50;
      body.innerHTML='<ol class="receipt-list">'+chunk.slice(start,start+50).map(renderReceipt).join('')+'</ol>';
      prev.disabled=page===0;next.disabled=page>=last-1;
    } catch (e) {
      if(ticket!==request)return;
      body.innerHTML='<p class="load-error">The receipt file could not be loaded. Close this view and try again, or use the downloadable ledger.</p>';
      pageStatus.textContent='Receipt file unavailable';
    }
  }
  document.querySelectorAll('[data-ledger]').forEach(button=>button.addEventListener('click',async()=>{
    selected=button.dataset.ledger;page=0;
    body.textContent='Loading…';
    if(!dialog.open)dialog.showModal();
    try {
      index=index||await json('data/ledger-index.json');
      const meta=index[selected];
      document.querySelector('#ledger-title').textContent=meta.title;
      document.querySelector('#ledger-context').textContent=meta.meaning;
      document.querySelector('#ledger-summary').textContent=meta.count.toLocaleString('en-US')+' receipt events · '+money(meta.usd)+' at historical references'+(meta.unpriced ? ' · '+meta.unpriced+' unpriced entries' : '')+'. Newest first.';
      await render();dialog.scrollTop=0;
    }catch(e){body.innerHTML='<p class="load-error">The receipt index could not be loaded. Please use the downloadable ledger.</p>';}
  }));
  document.querySelector('.close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',()=>{request++;});
  prev.addEventListener('click',async()=>{if(page>0){page--;await render();dialog.scrollTop=0;}});
  next.addEventListener('click',async()=>{if(index && page+1<Math.ceil(index[selected].count/50)){page++;await render();dialog.scrollTop=0;}});
})();
