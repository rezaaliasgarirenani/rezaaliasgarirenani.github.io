(() => {
  'use strict';
  const filters = document.querySelector('.filter-group');
  const papers = [...document.querySelectorAll('.publication')];
  const count = document.querySelector('#publication-count');
  filters.hidden = false;
  filters.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    filters.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    const kind = button.dataset.filter;
    let visible = 0;
    papers.forEach(paper => { paper.hidden = kind !== 'all' && paper.dataset.kind !== kind; if (!paper.hidden) visible++; });
    count.textContent = kind === 'all' ? '6 contributions / 2023–2026' : `${visible} ${kind === 'journal' ? 'journal article' : 'conference contributions'}`;
  });
})();
