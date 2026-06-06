/* terminal.js — 「研究终端」共享交互：全局搜索过滤 + 表头排序。
   依赖元素（可选，缺失自动跳过）：#searchInput #resetSearch #rowCount #emptyState
   过滤目标：table.sortable 的行 + .filter-item 元素。 */
(function () {
  const input = document.getElementById('searchInput');
  const resetBtn = document.getElementById('resetSearch');
  const rowCount = document.getElementById('rowCount');
  const emptyState = document.getElementById('emptyState');
  const tables = Array.from(document.querySelectorAll('table.sortable'));
  const items = Array.from(document.querySelectorAll('.filter-item'));
  const norm = v => (v || '').toLowerCase().trim();
  const asNum = v => {
    const c = v.replace(/[$,%+~]/g, '').replace(/[^0-9.\-]/g, '');
    if (!c || c === '-' || c === '.') return null;
    const n = Number(c); return Number.isFinite(n) ? n : null;
  };
  function update() {
    if (!input) return;
    const q = norm(input.value); let vis = 0;
    tables.forEach(t => Array.from(t.tBodies[0]?.rows || []).forEach(r => {
      const m = !q || norm(r.innerText).includes(q); r.hidden = !m; if (m) vis++;
    }));
    items.forEach(el => {
      const m = !q || norm(el.innerText).includes(q);
      el.classList.toggle('hidden-by-filter', !m); if (m) vis++;
    });
    if (rowCount) rowCount.textContent = vis + ' 条匹配';
    if (emptyState) emptyState.classList.toggle('visible', Boolean(q) && vis === 0);
  }
  tables.forEach(table => {
    Array.from(table.tHead?.rows[0]?.cells || []).forEach((th, i) => {
      const b = th.querySelector('button'); if (!b) return;
      b.addEventListener('click', () => {
        const dir = th.dataset.sort === 'asc' ? 'desc' : 'asc';
        Array.from(th.parentElement.children).forEach(c => c.dataset.sort = '');
        th.dataset.sort = dir;
        const rows = Array.from(table.tBodies[0].rows);
        rows.sort((a, c) => {
          const av = a.cells[i]?.innerText.trim() || '', bv = c.cells[i]?.innerText.trim() || '';
          const an = asNum(av), bn = asNum(bv);
          const cmp = (an !== null && bn !== null) ? an - bn
            : av.localeCompare(bv, 'zh-Hans-u-co-pinyin', { numeric: true, sensitivity: 'base' });
          return dir === 'asc' ? cmp : -cmp;
        });
        rows.forEach(r => table.tBodies[0].appendChild(r));
      });
    });
  });
  if (resetBtn && input) resetBtn.addEventListener('click', () => { input.value = ''; update(); input.focus(); });
  if (input) input.addEventListener('input', update);
  update();
})();
