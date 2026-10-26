(() => {
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function openHash() {
    if (!location.hash) return;
    let target;
    try { target = document.querySelector(location.hash); } catch { return; }
    if (!target) return;
    if (target.matches('details')) target.open = true;
    for (let p = target.parentElement; p; p = p.parentElement) if (p.matches('details')) p.open = true;
    target.scrollIntoView({block:'start'});
  }
  window.addEventListener('hashchange', openHash);
  openHash();
  document.querySelectorAll('[data-share]').forEach(button => button.addEventListener('click', async () => {
    const status = document.querySelector('.share-status');
    try {
      await navigator.clipboard.writeText(new URL(location.pathname + location.search + location.hash, 'https://phoenix-foundation-irregularities.pfc.zone').href);
      status.textContent = 'Link copied. Ready to share.';
    } catch {
      status.textContent = 'Copy the URL from your browser to share this page.';
    }
  }));
})();
