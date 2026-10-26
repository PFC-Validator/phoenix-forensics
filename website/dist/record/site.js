/* Reading controls for the current publication. Original captures are not modified. */
(() => {
  'use strict';
  const rail = document.querySelector('.reader-index');
  const narrow = matchMedia('(max-width: 1100px)');
  const setRailMode = () => { if (rail) rail.open = !narrow.matches; };
  setRailMode();
  narrow.addEventListener('change', setRailMode);
  const closeMenus = () => {
    document.querySelectorAll('.site-menu[open],.page-toggle[open]').forEach(el => { el.open = false; });
    if (rail && narrow.matches) rail.open = false;
  };
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      const active = document.querySelector('.reader-index[open]');
      closeMenus();
      if (active && narrow.matches) active.querySelector('summary').focus();
    }
  });
  document.querySelectorAll('.site-nav a,.section-nav a,.reader-links a,.reader-top').forEach(link => {
    link.addEventListener('click', closeMenus);
  });
  const links = [...document.querySelectorAll('.reader-links a')];
  const sections = links.map(link => ({link, node: document.getElementById(link.hash.slice(1))})).filter(item => item.node);
  let scheduled = false;
  const updateCurrent = () => {
    scheduled = false;
    let current = null;
    for (const item of sections) {
      const box = item.node.getBoundingClientRect();
      if (box.top <= (narrow.matches ? 175 : 150)) current = item;
    }
    for (const item of sections) {
      if (item === current) item.link.setAttribute('aria-current', 'location');
      else item.link.removeAttribute('aria-current');
    }
    const panel = document.querySelector('.reader-panel');
    if (current && panel && !narrow.matches && !panel.matches(':hover')) {
      const row = current.link.getBoundingClientRect();
      const bounds = panel.getBoundingClientRect();
      if (row.bottom > bounds.bottom) panel.scrollTop += row.bottom - bounds.bottom + 25;
      else if (row.top < bounds.top) panel.scrollTop -= bounds.top - row.top + 25;
    }
  };
  if (sections.length) {
    addEventListener('scroll', () => {
      if (!scheduled) { scheduled = true; requestAnimationFrame(updateCurrent); }
    }, {passive:true});
    addEventListener('resize', updateCurrent, {passive:true});
    updateCurrent();
  }
  // Horizontal tables remain complete and keyboard-scrollable on small screens.
  const tableStates = new WeakMap();
  const refreshTables = () => {
    document.querySelectorAll('.record-page .table-wrap,.record-page .table-scroll').forEach(wrap => {
      const table = wrap.querySelector('table');
      if (!table) return;
      let hint = tableStates.get(wrap);
      if (!hint) {
        hint = document.createElement('div');
        hint.className = 'table-overflow-hint';
        hint.innerHTML = '<span>Scroll to view all columns</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12h18M7 8l-4 4 4 4m10-8 4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>';
        wrap.before(hint);
        tableStates.set(wrap,hint);
        const heading = wrap.closest('section')?.querySelector('h2');
        wrap.setAttribute('role','region');
        wrap.setAttribute('aria-label',heading ? heading.textContent.trim()+' — data table' : 'Scrollable data table');
      }
      const overflow = table.scrollWidth > wrap.clientWidth + 2;
      hint.hidden = !overflow;
      if (overflow || wrap.scrollHeight > wrap.clientHeight + 2) wrap.tabIndex = 0;
      else wrap.removeAttribute('tabindex');
    });
  };
  refreshTables();
  addEventListener('resize',refreshTables,{passive:true});
  for (const id of ['contract-table','funding-table']) {
    const node = document.getElementById(id);
    if (node) new MutationObserver(refreshTables).observe(node,{childList:true});
  }
})();
