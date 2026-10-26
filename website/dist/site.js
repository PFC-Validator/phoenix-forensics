(() => {
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const money = v => v == null ? 'Unpriced' : new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(Number(v));
  const date = v => {const d=new Date(v);return Number.isNaN(d.getTime()) ? 'Date not recorded' : new Intl.DateTimeFormat('en-GB',{dateStyle:'medium',timeZone:'UTC'}).format(d)+' UTC';};
  const safeLink=(u,label)=>{try{const x=new URL(u,location.origin);return /^https?:$/.test(x.protocol)?`<a href="${esc(x.href)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`:'';}catch{return '';}};
  const search=document.querySelector('#payment-search'),filter=document.querySelector('#payment-category');
  const payments=[...document.querySelectorAll('.payment')];
  function applyFilter(){let n=0;for(const p of payments){const show=p.dataset.search.includes(search.value.toLowerCase().trim())&&(!filter.value||p.dataset.category===filter.value);p.hidden=!show;if(show)n++;}document.querySelector('#record-count').textContent=`${n} of ${payments.length} records`;document.querySelector('#empty-state').hidden=n>0;}
  if(search){search.addEventListener('input',applyFilter);filter.addEventListener('change',applyFilter);document.querySelector('#clear-filter').addEventListener('click',()=>{search.value='';filter.value='';applyFilter();search.focus();});}

  // Progressive enhancement: every case stays readable when JavaScript is off.
  for(const root of document.querySelectorAll('[data-cases]')){
    const controls=root.querySelector('.case-controls');
    const tabs=[...controls.querySelectorAll('[role=tab]')];
    const panels=[...root.querySelectorAll('.case-panel')];
    function selectCase(index,moveFocus=false){
      tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;});
      panels.forEach((panel,i)=>{panel.hidden=i!==index;panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby',tabs[i].id);});
      if(moveFocus)tabs[index].focus();
    }
    tabs.forEach((tab,i)=>{
      tab.addEventListener('click',()=>selectCase(i));
      tab.addEventListener('keydown',event=>{
        let next=i;
        if(event.key==='ArrowRight')next=(i+1)%tabs.length;
        else if(event.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;
        else if(event.key==='Home')next=0;
        else if(event.key==='End')next=tabs.length-1;
        else return;
        event.preventDefault();selectCase(next,true);
      });
    });
    selectCase(0);controls.hidden=false;root.classList.add('case-ready');
  }

  const cache=new Map();let ledger;
  async function json(url){if(cache.has(url))return cache.get(url);const r=await fetch(url);if(!r.ok)throw Error('File unavailable');const d=await r.json();cache.set(url,d);return d;}
  function receipt(r){return `<li><div class="receipt-heading"><time>${esc(date(r.date))}</time><span>${esc(r.amount)} ${esc(r.asset)} · ${money(r.usd)}</span></div>${safeLink(r.explorer||r.source,r.tx?`Transaction ${r.tx.slice(0,12)}…`:`Block ${r.height} · ${r.event==null?'transfer':'event '+r.event}`)}<details><summary>Wallets and valuation</summary><dl>${[['From',r.sender],['To',r.recipient],['Beneficiary',r.beneficiary],['USD',r.usd],['Price time',r.price_time],['Method',r.price_method],['Unpriced',r.unpriced_reason],['Purpose',r.purpose]].filter(([,v])=>v!=null&&v!=='').map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>${safeLink(r.source,'Original chain response')}</details></li>`;}
  async function loadReceipts(details,page=0){const host=details.querySelector('.receipt-host');host.innerHTML='<p role="status">Loading receipt records…</p>';try{ledger=ledger||await json('/record/data/ledger-index.json');const meta=ledger[details.dataset.ledger];const chunk=await json('/record/'+meta.pages[Math.floor(page/5)]);const rows=chunk.slice(page%5*50,page%5*50+50);const total=Math.ceil(meta.count/50);host.innerHTML=`<p class="note">${meta.count.toLocaleString()} receipt events · ${meta.unique_transactions.toLocaleString()} ordinary transactions${meta.unpriced?' · '+meta.unpriced+' unpriced entries':''}. Newest first.</p><ol class="receipts">${rows.map(receipt).join('')}</ol><div class="pager"><button class="prev" ${page===0?'disabled':''}>Previous</button><span>Page ${page+1} of ${total}</span><button class="next" ${page>=total-1?'disabled':''}>Next</button></div>`;host.querySelector('.prev').addEventListener('click',()=>loadReceipts(details,page-1));host.querySelector('.next').addEventListener('click',()=>loadReceipts(details,page+1));details.dataset.loaded='true';}catch{host.innerHTML='<p role="alert">These receipts could not be loaded. Try again, or open the preserved payment record.</p><button class="text-button retry">Try again</button> <a href="/record/#received">Preserved payment record</a>';host.querySelector('.retry').addEventListener('click',()=>loadReceipts(details,page));}}
  for(const d of document.querySelectorAll('[data-ledger]'))d.addEventListener('toggle',()=>{if(d.open&&!d.dataset.loaded)loadReceipts(d);});
  function openHash(){if(location.hash){let target;try{target=document.querySelector(location.hash);}catch{return;}if(target){if(target.matches('details'))target.open=true;for(let p=target.parentElement;p;p=p.parentElement)if(p.matches('details'))p.open=true;target.scrollIntoView({block:'start'});}}}
  window.addEventListener('hashchange',openHash);openHash();
  for(const a of document.querySelectorAll('a[data-open-evidence]'))a.addEventListener('click',()=>{const el=document.getElementById(a.hash.slice(1));if(el)el.open=true;});
  document.querySelectorAll('[data-share]').forEach(b=>b.addEventListener('click',async()=>{const status=document.querySelector('.share-status');try{await navigator.clipboard.writeText(new URL(location.pathname+location.search+location.hash,'https://phoenix-foundation-irregularities.pfc.zone').href);status.textContent='Link copied. Ready to share.';}catch{status.textContent='Copy the URL from your browser to share this page.';}}));
})();
