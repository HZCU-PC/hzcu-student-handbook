/* AI 论文索引 · 站点脚本 */
(function () {
  function init() {

const DATA = JSON.parse(document.getElementById('papers-json').textContent);
const BY = Object.fromEntries(DATA.map(p => [p.id, p]));
/* 来源页（如 ai-timeline）：从时间线深链进入时，关闭介绍后自动返回该页。 */
const FROM = new URLSearchParams(location.search).get('from');
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g,
  c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const grid = document.getElementById('grid');
const cards = [...grid.querySelectorAll('.card')];
const countEl = document.getElementById('count');
const SHOT = {};
cards.forEach(c => { SHOT[c.dataset.id] = c.querySelector('.shot').innerHTML; });

let state = { field: 'all', kind: 'all', country: 'all', org: 'all', q: '' };
let ORDER = [], NAV = { prev: null, next: null };

function apply() {
  const q = state.q.trim().toLowerCase();
  let list = cards.filter(c => {
    const d = c.dataset;
    if (state.field !== 'all' && d.field !== state.field) return false;
    if (state.kind !== 'all' && d.kind !== state.kind) return false;
    if (state.country !== 'all' && d.country !== state.country) return false;
    if (state.org !== 'all' && d.org !== state.org) return false;
    if (!q) return true;
    const p = BY[d.id];
    return (p.id + ' ' + p.zh + ' ' + p.en + ' ' + p.venue + ' ' + p.org + ' ' + p.country + ' ' +
            p.field + ' ' + p.kind + ' ' + p.authors).toLowerCase().includes(q);
  });
  list.sort((a, b) => {
    const pa = BY[a.dataset.id], pb = BY[b.dataset.id];
    if (sortKey === 'cite') return (pb.crank || 0) - (pa.crank || 0) || pb.year - pa.year;
    if (sortKey === 'id') return pa.id.localeCompare(pb.id);
    return pa.year - pb.year || pa.id.localeCompare(pb.id);
  });
  grid.innerHTML = '';
  list.forEach(c => grid.appendChild(c));
  countEl.innerHTML = '<b>' + list.length + '</b> / 45 篇';
  document.getElementById('empty').style.display = list.length ? 'none' : 'block';
  ORDER = list.map(c => BY[c.dataset.id]);
  const on = new Set(list.map(c => c.dataset.id));
  document.querySelectorAll('.tl-dot').forEach(d => {
    d.style.opacity = on.has(d.dataset.id) ? '' : '.18';
  });
}

function bindGroup(group, key) {
  document.querySelectorAll('.sitem[data-group="' + group + '"]').forEach(b => {
    b.addEventListener('click', () => {
      document.querySelectorAll('.sitem[data-group="' + group + '"]').forEach(x => x.classList.remove('on'));
      b.classList.add('on');
      state[key] = b.dataset.value;
      apply();
    });
  });
}
['field', 'kind', 'country', 'org'].forEach(g => bindGroup(g, g));

const qEl = document.getElementById('q');
qEl.addEventListener('input', e => { state.q = e.target.value; apply(); });
document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement !== qEl) { e.preventDefault(); qEl.focus(); }
});
const sortEl = document.getElementById('sort');
let sortKey = 'year';
sortEl.addEventListener('change', e => { sortKey = e.target.value; apply(); });

/* ---------- 弹窗 ---------- */
const scrim = document.getElementById('scrim'), sheet = document.getElementById('sheet');
const enc = encodeURIComponent;
function linkRow(cls, k, label, url) {
  return '<a class="ln ' + cls + '" href="' + url + '" target="_blank" rel="noopener"><b>' + k + '</b>' + label + '</a>';
}
function open(id) {
  const p = BY[id]; if (!p) return;
  const byYear = (a, b) => a.year - b.year || a.id.localeCompare(b.id);
  let list = ORDER.length ? ORDER : DATA.slice().sort(byYear);
  let i = list.findIndex(x => x.id === id);
  if (i < 0) { list = DATA.slice().sort(byYear); i = list.findIndex(x => x.id === id); }
  const prevP = i > 0 ? list[i - 1] : null, nextP = i < list.length - 1 ? list[i + 1] : null;
  NAV = { prev: prevP && prevP.id, next: nextP && nextP.id };

  const qs = enc(p.en);
  const isArx = /arxiv/i.test(p.link);
  const links = [
    linkRow('primary', '原文', isArx ? 'arXiv 预印本' : '出版方官方页', p.link),
    linkRow('', '检索', 'Google Scholar', 'https://scholar.google.com/scholar?q=' + qs),
    linkRow('', '脉络', 'Semantic Scholar 被引', 'https://www.semanticscholar.org/search?q=' + qs),
    linkRow('', '国内', '知网检索', 'https://kns.cnki.net/kns8s/defaultresult/index?kw=' + qs),
    linkRow('', '预印本', 'arXiv 搜索', 'https://arxiv.org/search/?query=' + qs + '&searchtype=all')
  ].join('');

  const rels = (p.rel || []).map(([tid, label]) => {
    const t = BY[tid]; if (!t) return '';
    return '<button class="relrow" data-go="' + tid + '"><span class="rid">' + tid + '</span>' +
      '<span class="rnm">' + esc(t.zh) + '</span><span class="rlb">' + esc(label) + '</span></button>';
  }).join('');

  sheet.innerHTML = `
    <button class="sheet-close" id="closeX" aria-label="关闭">×</button>
    <div class="sheet-in">
      <div class="sheet-shot">${(SHOT[id] || '').replace(/<span class="cite[^>]*>[^<]*<\/span>/g, '')}
        <div class="shot-cap">首页版式预览<br>非原文截图</div></div>
      <div class="sheet-body">
        <div class="stags">
          <span class="tag t-field" style="background:${p.tint};color:${p.color}">${esc(p.field)}</span>
          <span class="tag">${esc(p.kind)}</span>
          <span class="tag">${esc(p.country)}</span>
          <span class="tag tag-y">${p.year}</span>
        </div>
        <h2>${esc(p.zh)}</h2>
        <p class="hook">${esc(p.hook)}</p>
        <p class="sen">${esc(p.en)}</p>
        <div class="metarow">
          <span>${esc(p.org)}</span><span>${esc(p.venue)}</span>
          <span>被引 <b>${esc(p.citations || '—')}</b></span>
        </div>
        <div class="kv" style="margin-top:-6px"><h4>作者</h4><p style="font-size:12.5px">${esc(p.authors)}</p></div>
        <div class="kv"><h4>解决的问题</h4><p>${esc(p.solve).replace(/\n\n/g, '</p><p>')}</p></div>
        <div class="kv"><h4>核心方法</h4><p>${esc(p.method).replace(/\n\n/g, '</p><p>')}</p></div>
        <div class="kv"><h4>带来的影响</h4><p>${esc(p.impact).replace(/\n\n/g, '</p><p>')}</p></div>
        <div class="kv"><h4>相关论文索引</h4><div class="relbox">${rels}</div></div>
        <div class="kv"><h4>检索与原文</h4><div class="links">${links}</div></div>
        <div class="snav">
          <button class="snav-btn" data-id="${prevP ? prevP.id : ''}" ${prevP ? '' : 'disabled'}>‹ ${prevP ? esc(prevP.zh) : '已是第一篇'}</button>
          <span class="snav-n">${i + 1} / ${list.length}</span>
          <button class="snav-btn" data-id="${nextP ? nextP.id : ''}" ${nextP ? '' : 'disabled'}>${nextP ? esc(nextP.zh) : '已是最后一篇'} ›</button>
        </div>
      </div>
    </div>`;
  scrim.classList.add('on'); sheet.classList.add('on');
  document.body.style.overflow = 'hidden';
  document.getElementById('closeX').addEventListener('click', close);
  sheet.querySelectorAll('.snav-btn').forEach(b => b.addEventListener('click', () => {
    if (!b.disabled && b.dataset.id) open(b.dataset.id);
  }));
  sheet.querySelectorAll('.relrow').forEach(b => b.addEventListener('click', () => open(b.dataset.go)));
  sheet.scrollTop = 0;
}
function close() {
  scrim.classList.remove('on'); sheet.classList.remove('on');
  document.body.style.overflow = '';
  /* 从其它页面深链进入时，关闭介绍后回到原页（history 可保留滚动位置）。 */
  if (FROM && history.length > 1) history.back();
}
scrim.addEventListener('click', close);
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') { close(); return; }
  if (!sheet.classList.contains('on')) return;
  if (e.key === 'ArrowLeft' && NAV.prev) { e.preventDefault(); open(NAV.prev); }
  if (e.key === 'ArrowRight' && NAV.next) { e.preventDefault(); open(NAV.next); }
});
grid.addEventListener('click', e => {
  const c = e.target.closest('.card'); if (c) open(c.dataset.id);
});
grid.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ' ') {
    const c = e.target.closest('.card'); if (c) { e.preventDefault(); open(c.dataset.id); }
  }
});
document.querySelectorAll('.tl-dot').forEach(d => d.addEventListener('click', () => open(d.dataset.id)));

/* 深链 */
const q0 = new URLSearchParams(location.search).get('q');
if (q0) { qEl.value = q0; state.q = q0; }
apply();
const deep = new URLSearchParams(location.search).get('id');
if (deep && BY[deep.toUpperCase()]) open(deep.toUpperCase());

  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
