(async () => {
'use strict';

let DATA;
try {
  const response = await fetch('plans.json', { cache: 'no-store' });
  if (!response.ok) throw new Error(`plans.json HTTP ${response.status}`);
  DATA = await response.json();
} catch (error) {
  const tree = document.getElementById('tree');
  if (tree) tree.innerHTML = `<div class="empty"><div class="empty-mark">!</div><b>培养方案数据加载失败</b><p>请刷新页面重试；若直接打开本地文件，请通过站点预览访问。</p></div>`;
  console.error(error);
  return;
}

function initEmbeddedTheme() {
  try {
    if (window.parent === window) {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.dataset.theme = 'dark';
      }
      return;
    }
    const parentBody = window.parent.document.body;
    const apply = () => {
      const scheme = parentBody.getAttribute('data-md-color-scheme');
      document.documentElement.dataset.theme = scheme === 'slate' ? 'dark' : 'light';
    };
    apply();
    new MutationObserver(apply).observe(parentBody, {
      attributes: true,
      attributeFilter: ['data-md-color-scheme']
    });
  } catch (error) {
    /* 跨域或独立打开时保持默认浅色 */
  }
}
initEmbeddedTheme();
const PLANS = DATA.plans;
const COLLEGE = DATA.meta.college;

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fmt = (n) => {
  const v = Math.round(Number(n) * 10) / 10;
  return Number.isInteger(v) ? String(v) : v.toFixed(1);
};
const CN = ['零', '一', '二', '三', '四', '五', '六', '七', '八'];

const MODULE_ORDER = [
  '通识必修课程', '通识限选课程', '通识选修课程', '大类基础课程',
  '专业必修课程', '专业选修课程', '第二课堂', '第三课堂', '第四课堂'
];
const CAT_ORDER = [
  '数学与自然科学类', '计算机与信息类', '工程与大类基础类',
  '专业必修', '专业选修', '思想政治类', '外语类', '军体类',
  '创新创业类', '通识选修（人文社科）', '通识必修（其他）', '第二/三/四课堂'
];
const NATURE_ORDER = ['必修', '限选', '未标注'];

const MODE_META = {
  major: {
    kicker: 'PRIMARY TREE · 01',
    title: '学院 → 门类·专业类 → 专业 → 培养类型 → 课程模块 → 课程',
    desc: '主树：先看专业与培养类型，再展开课程模块。点击课程查看课程号、学期、模块与所属方案。'
  },
  module: {
    kicker: 'BY MODULE · 02',
    title: '课程模块 → 培养方案 → 课程',
    desc: '按培养要求组织：通识必修、通识限选、通识选修、大类基础、专业必修、专业选修等。同一课程在不同方案中归属不同模块时，会分别出现。'
  },
  year: {
    kicker: 'BY YEAR · 03',
    title: '学年 → 学期 → 课程',
    desc: '按学习时间组织：大一至大四，每学期一组；跨方案重复课程合并显示，并在行尾标出方案数。同一课程在不同方案中安排不同学期时，会分别出现。'
  },
  category: {
    kicker: 'BY KNOWLEDGE · 04',
    title: '知识大类 → 课程',
    desc: '按知识领域组织：数学与自然科学、计算机与信息、外语、思想政治、创新创业等。知识大类取自原网页“按大类”分类；同一课程归类不同时，会分别出现。'
  },
  nature: {
    kicker: 'BY REQUIREMENT · 05',
    title: '必修性质 → 课程模块 → 课程',
    desc: '按课程性质组织：必修、限选、未标注；再按课程模块细分。同一课程在不同方案中性质不同时，会在两组中分别出现。'
  }
};

const PLAN_BY_ID = new Map(PLANS.map((p) => [p.id, p]));
const PLAN_ORDER = { m25: 0, m26: 1, m27: 2, m11: 3 };
const planSort = (a, b) => (PLAN_ORDER[a.id.slice(-3)] ?? 9) - (PLAN_ORDER[b.id.slice(-3)] ?? 9);

PLANS.forEach((p) => {
  p.courses.forEach((c) => { c.pid = p.id; });
});

const ALL_CATS = [...new Set(PLANS.flatMap((p) => p.courses.map((c) => c.c)))].sort((a, b) => {
  const ia = CAT_ORDER.indexOf(a), ib = CAT_ORDER.indexOf(b);
  return (ia < 0 ? 999 : ia) - (ib < 0 ? 999 : ib) || a.localeCompare(b, 'zh-CN');
});

const ALL_MODULES = [...new Set(PLANS.flatMap((p) => p.courses.map((c) => c.m)))];

const OFFERS = new Map();
PLANS.forEach((p) => {
  p.courses.forEach((c) => {
    const key = `${p.year}|${c.k}`;
    if (!OFFERS.has(key)) OFFERS.set(key, []);
    OFFERS.get(key).push({ ...c, plan: p, pid: p.id });
  });
});

const state = {
  year: '2026',
  mode: 'major',
  planId: 'all',
  nature: 'all',
  years: new Set(['1', '2', '3', '4']),
  cats: new Set(ALL_CATS),
  query: '',
  open: new Set(),
  resetOpen: true,
  first: true
};

let NODE_MAP = new Map();
let controlsYear = null;
let drawerReturnFocus = null;
let modalReturnFocus = null;

/* ── 小工具 ───────────────────────────────────────── */
function groupBy(items, keyFn) {
  const map = new Map();
  for (const item of items) {
    const k = keyFn(item);
    if (!map.has(k)) map.set(k, []);
    map.get(k).push(item);
  }
  return map;
}

function sortEntries(map, order) {
  return [...map.entries()].sort((a, b) => {
    const ia = order.indexOf(a[0]), ib = order.indexOf(b[0]);
    return (ia < 0 ? 999 : ia) - (ib < 0 ? 999 : ib) || String(a[0]).localeCompare(String(b[0]), 'zh-CN');
  });
}

function sortNumericEntries(map) {
  return [...map.entries()].sort((a, b) => Number(a[0]) - Number(b[0]));
}

function sortCourses(a, b) {
  return (a.ry - b.ry) || (Number(a.q) - Number(b.q)) || a.n.localeCompare(b.n, 'zh-CN');
}

function yearName(ry) { return `大${CN[ry] || ry}`; }
function academicYear(ry) {
  const start = Number(state.year) + Number(ry) - 1;
  return `${start}-${start + 1}`;
}
function termName(ry, q) { return `${yearName(ry)}${q === '1' ? '上' : q === '2' ? '下' : ''}`; }

function highlight(text) {
  const q = state.query.trim();
  if (!q) return esc(text);
  const source = String(text ?? '');
  const idx = source.toLowerCase().indexOf(q.toLowerCase());
  if (idx < 0) return esc(source);
  return esc(source.slice(0, idx)) + '<mark>' + esc(source.slice(idx, idx + q.length)) + '</mark>' + esc(source.slice(idx + q.length));
}

function natureClass(label) {
  if (label.includes('必修')) return 'req';
  if (label.includes('限选')) return 'elec';
  return 'mixed';
}

function currentPlans() {
  return PLANS.filter((p) => p.year === state.year && (state.planId === 'all' || p.id === state.planId)).sort(planSort);
}

function normalizeState() {
  if (state.planId !== 'all' && !PLANS.some((p) => p.id === state.planId && p.year === state.year)) state.planId = 'all';
  if (state.nature !== 'all' && !PLANS.some((p) => p.year === state.year && p.courses.some((c) => c.z === state.nature))) state.nature = 'all';
}

function filterCourses(plans) {
  const q = state.query.trim().toLowerCase();
  const out = [];
  for (const p of plans) {
    for (const c of p.courses) {
      if (state.nature !== 'all' && c.z !== state.nature) continue;
      if (!state.years.has(String(c.ry))) continue;
      if (!state.cats.has(c.c)) continue;
      if (q) {
        const hay = `${c.n} ${c.k} ${c.c} ${c.m} ${c.om} ${c.d} ${c.t}`.toLowerCase();
        if (!hay.includes(q)) continue;
      }
      out.push({ ...c, plan: p, pid: p.id });
    }
  }
  return out;
}

function calcStats(plans, courses) {
  const records = courses.reduce((s, c) => s + (c.dup || 1), 0);
  const codes = new Set(courses.map((c) => c.k));
  const active = plans.filter((p) => courses.some((c) => c.pid === p.id));
  const credits = active.map((p) => p.credits);
  return {
    plans: active.length,
    records,
    unique: codes.size,
    cats: new Set(courses.map((c) => c.c)).size,
    min: credits.length ? Math.min(...credits) : null,
    max: credits.length ? Math.max(...credits) : null
  };
}

/* ── 节点构造 ─────────────────────────────────────── */
function makeGroup(id, type, label, children, extra = {}) {
  children = children.filter(Boolean);
  const codes = new Set();
  const planIds = new Set();
  let records = 0, credits = 0;
  for (const ch of children) {
    records += ch.records || 0;
    credits += ch.credits || 0;
    ch.codes.forEach((k) => codes.add(k));
    ch.planIds.forEach((pid) => planIds.add(pid));
  }
  return {
    id, type, label, children,
    records, credits, codes, planIds,
    unique: codes.size,
    ...extra
  };
}

function makeSingleCourse(c, id) {
  const offers = OFFERS.get(`${c.plan.year}|${c.k}`) || [c];
  const node = {
    id, type: 'course', label: c.n, course: c, offers,
    merged: false, records: c.dup || 1, credits: c.x,
    codes: new Set([c.k]), planIds: new Set([c.pid]), unique: 1
  };
  NODE_MAP.set(id, node);
  return node;
}

function makeMergedCourse(m, id) {
  const node = {
    id, type: 'course', label: m.n, course: m, offers: m.offers,
    merged: true, records: m.dup, credits: m.x,
    codes: new Set([m.k]), planIds: new Set(m.offers.map((o) => o.pid)), unique: 1
  };
  NODE_MAP.set(id, node);
  return node;
}

function planNode(p, courses) {
  const modules = sortEntries(groupBy(courses, (c) => c.m), MODULE_ORDER);
  const children = modules.map(([m, list]) => makeGroup(
    `mod|${p.id}|${m}`, 'module', m,
    list.map((c) => makeSingleCourse(c, `c|${p.id}|${m}|${c.i}`)),
    {}
  ));
  return makeGroup(`p|${p.id}`, 'plan', p.track || p.major, children, {
    plan: p,
    isMajorPlan: !p.track,
    partial: false,
    sub: p.track ? `培养方案 · ${p.discipline} · ${p.majorClass}` : '专业 · 培养方案'
  });
}

function mergeCourses(list) {
  const map = new Map();
  for (const c of list) {
    if (!map.has(c.k)) map.set(c.k, []);
    map.get(c.k).push(c);
  }
  return [...map.entries()].map(([k, offers]) => {
    offers.sort(sortCourses);
    const first = offers[0];
    const xs = [...new Set(offers.map((o) => o.x))].sort((a, b) => a - b);
    const zs = [...new Set(offers.map((o) => o.z))];
    const mods = [...new Set(offers.map((o) => o.m))];
    const terms = [...new Set(offers.map((o) => o.term))];
    const cats = [...new Set(offers.map((o) => o.c))];
    return {
      k, n: first.n,
      x: first.x, xMin: xs[0], xMax: xs[xs.length - 1],
      z: zs.length === 1 ? zs[0] : '混合', zList: zs,
      m: mods.length === 1 ? mods[0] : '多模块', mList: mods,
      term: terms.length === 1 ? first.term : '多学期', termList: terms,
      c: cats.length === 1 ? first.c : '多领域', cList: cats,
      offers, planCount: new Set(offers.map((o) => o.pid)).size,
      dup: offers.reduce((s, o) => s + (o.dup || 1), 0),
      first
    };
  }).sort((a, b) => (a.first.ry - b.first.ry) || (Number(a.first.q) - Number(b.first.q)) || a.n.localeCompare(b.n, 'zh-CN'));
}

/* ── 建树 ─────────────────────────────────────────── */
function buildTree(plans, courses) {
  NODE_MAP = new Map();
  const byPlan = new Map(plans.map((p) => [p.id, []]));
  courses.forEach((c) => { if (byPlan.has(c.pid)) byPlan.get(c.pid).push(c); });
  const active = plans.filter((p) => byPlan.get(p.id).length).sort(planSort);
  let children = [];

  if (state.mode === 'major') {
    const dMap = groupBy(active, (p) => `${p.discipline} · ${p.majorClass}`);
    const dOrder = ['工学 · 计算机类', '理学 · 统计学类'];
    children = sortEntries(dMap, dOrder).map(([dkey, dPlans]) => {
      const mMap = groupBy(dPlans, (p) => p.major);
      const mOrder = ['计算机科学与技术', '软件工程', '应用统计学'];
      const majorNodes = sortEntries(mMap, mOrder).map(([major, mPlans]) => {
        mPlans.sort(planSort);
        if (mPlans.length === 1 && !mPlans[0].track) {
          return planNode(mPlans[0], byPlan.get(mPlans[0].id));
        }
        const trackNodes = mPlans.map((p) => planNode(p, byPlan.get(p.id)));
        return makeGroup(`m|${dkey}|${major}`, 'major', major, trackNodes, {
          sub: mPlans.map((p) => p.track).filter(Boolean).join(' / ') || `${mPlans.length} 套方案`
        });
      });
      return makeGroup(`d|${dkey}`, 'discipline', dkey, majorNodes, {
        sub: `${new Set(dPlans.map((p) => p.major)).size} 个专业 · ${dPlans.length} 套方案`
      });
    });
  }

  if (state.mode === 'module') {
    const mods = sortEntries(groupBy(courses, (c) => c.m), MODULE_ORDER);
    children = mods.map(([m, list]) => {
      let kids;
      if (active.length > 1) {
        const pMap = groupBy(list, (c) => c.pid);
        kids = sortEntries(pMap, active.map((p) => p.id)).map(([pid, cs]) => {
          const p = PLAN_BY_ID.get(pid);
          return makeGroup(`p|${p.id}|m|${m}`, 'plan', p.planLabel,
            cs.map((c) => makeSingleCourse(c, `c|${p.id}|m|${m}|${c.i}`)),
            { plan: p, partial: true }
          );
        });
      } else {
        kids = list.map((c) => makeSingleCourse(c, `c|${c.pid}|m|${m}|${c.i}`));
      }
      return makeGroup(`mod|${m}`, 'module', m, kids, {});
    });
  }

  if (state.mode === 'year') {
    const years = sortNumericEntries(groupBy(courses, (c) => c.ry));
    children = years.map(([ry, list]) => {
      const terms = sortNumericEntries(groupBy(list, (c) => c.q));
      const termNodes = terms.map(([q, tlist]) => {
        const merged = mergeCourses(tlist);
        return makeGroup(`term|${ry}|${q}`, 'term', termName(ry, q),
          merged.map((m) => makeMergedCourse(m, `c|y|${ry}|${q}|${m.k}`)),
          { sub: `${academicYear(ry)} 第${q}学期` }
        );
      });
      return makeGroup(`yr|${ry}`, 'year', yearName(ry), termNodes, {
        sub: `${academicYear(ry)} 学年`
      });
    });
  }

  if (state.mode === 'category') {
    const cats = sortEntries(groupBy(courses, (c) => c.c), ALL_CATS);
    children = cats.map(([cat, list]) => {
      const merged = mergeCourses(list);
      return makeGroup(`cat|${cat}`, 'category', cat,
        merged.map((m) => makeMergedCourse(m, `c|cat|${cat}|${m.k}`)),
        {}
      );
    });
  }

  if (state.mode === 'nature') {
    const nats = sortEntries(groupBy(courses, (c) => c.z), NATURE_ORDER);
    children = nats.map(([z, list]) => {
      const mods = sortEntries(groupBy(list, (c) => c.m), MODULE_ORDER);
      const modNodes = mods.map(([m, mlist]) => {
        const merged = mergeCourses(mlist);
        return makeGroup(`mod|nat|${z}|${m}`, 'module', m,
          merged.map((mc) => makeMergedCourse(mc, `c|nat|${z}|${m}|${mc.k}`)),
          {}
        );
      });
      return makeGroup(`nat|${z}`, 'nature', z, modNodes, {});
    });
  }

  return makeGroup('root', 'college', COLLEGE, children, {
    sub: `${state.year} 级 · ${active.length} 套培养方案`
  });
}

function defaultOpenIds(root, planCount) {
  const ids = new Set([root.id]);
  if (state.mode === 'major') {
    root.children.forEach((d) => {
      ids.add(d.id);
      d.children.forEach((n) => {
        if (n.type === 'plan') {
          if (planCount === 1) ids.add(n.id);
        } else {
          ids.add(n.id);
          n.children.forEach((t) => { if (t.type === 'plan' && planCount === 1) ids.add(t.id); });
        }
      });
    });
  } else if (state.mode === 'year') {
    root.children.forEach((y) => ids.add(y.id));
  } else if (state.mode === 'nature') {
    root.children.forEach((n) => ids.add(n.id));
  }
  return ids;
}

/* ── 渲染：结构 ───────────────────────────────────── */
const ICONS = { college: '院', discipline: '类', major: '专', plan: '案', module: '模', year: '年', term: '期', category: '域', nature: '性' };

function iconFor(node) {
  if (node.type === 'plan') return node.isMajorPlan ? '专' : '案';
  return ICONS[node.type] || '·';
}

function pillsFor(node) {
  switch (node.type) {
    case 'college':
      return `<span class="pill">${node.records} 条</span><span class="pill credit">${node.unique} 门</span>`;
    case 'discipline':
      return `<span class="pill">${node.records} 条</span><span class="pill credit">${node.unique} 门</span>`;
    case 'major':
      return `<span class="pill">${node.planIds.size} 套</span><span class="pill">${node.records} 条</span>`;
    case 'plan': {
      const p = node.plan;
      if (node.partial) {
        return `<span class="pill credit">${node.records} 门</span><span class="pill">${p.classes} 班</span>`;
      }
      const count = node.records === p.courseCount ? `${p.courseCount} 门` : `${node.records} / ${p.courseCount} 门`;
      return `<span class="pill credit">${count}</span><span class="pill sum">最低 ${p.credits} 学分</span><span class="pill">${p.classes} 班</span>`;
    }
    case 'module': {
      const sum = node.planIds.size === 1
        ? `<span class="pill sum" title="所列课程学分合计，不等于最低毕业学分">Σ${fmt(node.credits)}</span>`
        : `<span class="pill">${node.planIds.size} 方案</span>`;
      return `<span class="pill">${node.unique} 门</span>${sum}`;
    }
    case 'year':
      return `<span class="pill">${node.unique} 门</span><span class="pill">${node.records} 条</span>`;
    case 'term':
      return `<span class="pill">${node.unique} 门</span>`;
    case 'category':
      return `<span class="pill">${node.unique} 门</span><span class="pill">${node.planIds.size} 方案</span>`;
    case 'nature':
      return `<span class="pill">${node.unique} 门</span><span class="pill">${node.planIds.size} 方案</span>`;
    default:
      return '';
  }
}

function subContext(node) {
  const c = node.course;
  if (state.mode === 'year' || state.mode === 'category') return c.m;
  return c.c;
}

function courseHTML(node, depth) {
  const c = node.course;
  const xLabel = node.merged ? (c.xMin === c.xMax ? fmt(c.xMin) : `${fmt(c.xMin)}–${fmt(c.xMax)}`) : fmt(c.x);
  const zLabel = node.merged ? (c.z === '混合' ? '必修/限选' : c.z) : c.z;
  const nClass = natureClass(zLabel);
  const planCount = node.merged ? c.planCount : 0;
  const tags = [
    `<span class="pill credit">${xLabel} 学分</span>`,
    `<span class="pill ${nClass}">${esc(zLabel)}</span>`,
    c.term ? `<span class="pill term">${esc(c.term)}</span>` : '',
    planCount > 1 ? `<span class="pill plans" title="${planCount} 个培养方案开设">×${planCount}</span>` : ''
  ].filter(Boolean).join('');

  return `<div class="node type-course" data-id="${esc(node.id)}">
    <button type="button" class="row" role="treeitem" aria-level="${depth + 1}" data-course="1" data-id="${esc(node.id)}">
      <span class="caret-space" aria-hidden="true"></span>
      <span class="course-dot ${nClass}" aria-hidden="true"></span>
      <span class="course-body">
        <span class="course-title">${highlight(c.n)}</span>
        <span class="course-sub">${esc(c.k)} · ${esc(subContext(node))}</span>
      </span>
      <span class="course-tags">${tags}</span>
    </button>
  </div>`;
}

function nodeHTML(node, depth, forceOpen) {
  if (node.type === 'course') return courseHTML(node, depth);
  const open = forceOpen || state.open.has(node.id);
  const sub = node.sub ? `<span class="node-sub">${esc(node.sub)}</span>` : '';
  const pidAttr = node.plan ? ` data-pid="${esc(node.plan.id)}"` : '';
  return `<div class="node type-${node.type}${open ? ' is-open' : ''}" data-id="${esc(node.id)}">
    <button type="button" class="row" role="treeitem" aria-level="${depth + 1}" aria-expanded="${open}"${pidAttr}>
      <span class="caret" aria-hidden="true"></span>
      <span class="n-icon" aria-hidden="true">${iconFor(node)}</span>
      <span class="node-label"><b>${highlight(node.label)}</b>${sub}</span>
      <span class="node-meta">${pillsFor(node)}</span>
    </button>
    <div class="children" role="group"${open ? '' : ' hidden'}>${node.children.map((ch) => nodeHTML(ch, depth + 1, forceOpen)).join('')}</div>
  </div>`;
}

function emptyHTML() {
  return `<div class="empty">
    <div class="empty-mark">空</div>
    <b>没有符合条件的课程</b>
    <p>可以调整年级、必修性质、学年或知识大类；也可以清除关键词。</p>
    <button type="button" data-action="reset-filters">清除全部筛选</button>
  </div>`;
}

/* ── 渲染：控件与统计 ─────────────────────────────── */
function renderPlanCards() {
  const ps = PLANS.filter((p) => p.year === state.year).sort(planSort);
  $('#planCards').innerHTML = ps.map((p) => {
    const active = state.planId === p.id;
    const accent = p.discipline === '工学' ? 'var(--teal)' : 'var(--ochre)';
    const dup = p.uniqueCount < p.courseCount;
    return `<button type="button" class="plan-card${active ? ' on' : ''}" data-pid="${esc(p.id)}" aria-pressed="${active}" style="--accent:${accent}" title="计划 ${p.courseCount} 门${dup ? `，去重 ${p.uniqueCount} 门` : ''} · 最低毕业 ${p.credits} 学分 · ${p.classes} 个班">
      <span class="plan-tag">${esc(p.discipline)} · ${esc(p.majorClass)}</span>
      <span class="plan-title">${esc(p.planLabel)}</span>
      <span class="plan-nums"><span class="big">${p.credits}</span><span class="unit">最低毕业学分</span></span>
      <span class="plan-sub"><span>${p.courseCount} 门${dup ? '<span class="dup" title="含 1 条重复记录，去重后 ' + p.uniqueCount + ' 门">†</span>' : ''}</span><span>${p.classes} 个班</span></span>
    </button>`;
  }).join('');
}

function renderHeader(st) {
  const meta = MODE_META[state.mode];
  $('#mapKicker').textContent = meta.kicker;
  $('#mapTitle').textContent = meta.title;
  $('#mapDesc').textContent = meta.desc;
  $('#mapCount').innerHTML = `<b>${st.plans}</b> 套方案 · <b>${st.records}</b> 条记录 · <b>${st.unique}</b> 门不同课程`;
}

function renderStats(st) {
  $('#statPlans').textContent = st.plans;
  $('#statRecords').textContent = st.records;
  $('#statUnique').textContent = st.unique;
  $('#statCats').textContent = st.cats;
  $('#statCredits').textContent = st.min == null ? '—' : (st.min === st.max ? String(st.min) : `${st.min}–${st.max}`);
}

function renderTree(root) {
  const forceOpen = !!state.query.trim();
  $('#tree').innerHTML = root.children.length ? nodeHTML(root, 0, forceOpen) : emptyHTML();
}

function renderPlanSelect() {
  const ps = PLANS.filter((p) => p.year === state.year).sort(planSort);
  const groups = groupBy(ps, (p) => `${p.discipline} · ${p.majorClass}`);
  let html = `<option value="all">全部培养方案（${ps.length}）</option>`;
  for (const [g, list] of groups) {
    html += `<optgroup label="${esc(g)}">` + list.map((p) => `<option value="${esc(p.id)}">${esc(p.planLabel)}</option>`).join('') + '</optgroup>';
  }
  $('#planSelect').innerHTML = html;
  if (state.planId !== 'all' && !ps.some((p) => p.id === state.planId)) state.planId = 'all';
  $('#planSelect').value = state.planId;
}

function renderNatureChips() {
  const counts = {};
  PLANS.filter((p) => p.year === state.year).forEach((p) => p.courses.forEach((c) => {
    counts[c.z] = (counts[c.z] || 0) + (c.dup || 1);
  }));
  const total = Object.values(counts).reduce((s, n) => s + n, 0);
  const items = [['all', '全部', total], ...NATURE_ORDER.filter((z) => counts[z]).map((z) => [z, z, counts[z]])];
  if (!items.some(([v]) => v === state.nature)) state.nature = 'all';
  $('#natureChips').innerHTML = items.map(([v, label, n]) =>
    `<button type="button" class="chip${state.nature === v ? ' on' : ''}" data-nature="${esc(v)}" aria-pressed="${state.nature === v}">${esc(label)}<span class="n">${n}</span></button>`
  ).join('');
}

function renderYearChips() {
  const counts = { 1: 0, 2: 0, 3: 0, 4: 0 };
  PLANS.filter((p) => p.year === state.year).forEach((p) => p.courses.forEach((c) => {
    if (counts[c.ry] != null) counts[c.ry] += (c.dup || 1);
  }));
  $('#yearChips').innerHTML = [1, 2, 3, 4].map((ry) =>
    `<button type="button" class="chip${state.years.has(String(ry)) ? ' on' : ''}" data-year="${ry}" aria-pressed="${state.years.has(String(ry))}">${yearName(ry)}<span class="n">${counts[ry]}</span></button>`
  ).join('');
}

function renderCategoryList() {
  const counts = {};
  PLANS.filter((p) => p.year === state.year).forEach((p) => p.courses.forEach((c) => {
    counts[c.c] = (counts[c.c] || 0) + (c.dup || 1);
  }));
  $('#catList').innerHTML = ALL_CATS.map((cat) =>
    `<div class="cat-row"><label><input type="checkbox" data-cat="${esc(cat)}"${state.cats.has(cat) ? ' checked' : ''}><span class="cat-name">${esc(cat)}</span></label><span class="cat-n">${counts[cat] || 0}</span></div>`
  ).join('');
}

function syncControls(st) {
  $$('.year-switch button').forEach((b) => {
    const on = b.dataset.year === state.year;
    b.classList.toggle('on', on);
    b.setAttribute('aria-selected', String(on));
  });
  $$('#modebar button').forEach((b) => b.classList.toggle('on', b.dataset.mode === state.mode));
  $('#planSelect').value = state.planId;
  const p = state.planId === 'all' ? null : PLAN_BY_ID.get(state.planId);
  $('#planHint').textContent = p ? '已选 1 套' : '全部';
  $$('#natureChips .chip').forEach((b) => {
    const on = b.dataset.nature === state.nature;
    b.classList.toggle('on', on);
    b.setAttribute('aria-pressed', String(on));
  });
  $$('#yearChips .chip').forEach((b) => {
    const on = state.years.has(String(b.dataset.year));
    b.classList.toggle('on', on);
    b.setAttribute('aria-pressed', String(on));
  });
  $$('#catList input[data-cat]').forEach((el) => { el.checked = state.cats.has(el.dataset.cat); });
  const nCats = state.cats.size;
  $('#catSummary').textContent = nCats === ALL_CATS.length ? '全部' : nCats === 0 ? '未选择' : `已选 ${nCats} / ${ALL_CATS.length}`;
  $('#searchStatus').textContent = state.query ? `匹配 ${st.records} 条 · ${st.unique} 门` : '课程名 / 课程号 / 模块 / 大类';
  $('#searchClear').classList.toggle('on', !!state.query);
  if ($('#search').value !== state.query) $('#search').value = state.query;

  let activeFilters = 0;
  if (state.planId !== 'all') activeFilters++;
  if (state.nature !== 'all') activeFilters++;
  if (state.years.size < 4) activeFilters++;
  if (state.cats.size < ALL_CATS.length) activeFilters++;
  if (state.query.trim()) activeFilters++;
  const badge = $('#filterBadge');
  badge.textContent = activeFilters;
  badge.style.display = activeFilters ? 'inline-block' : 'none';
  $('#mobileFilter').setAttribute('aria-expanded', String($('#sidebar').classList.contains('open')));
  $('#mobileFilterLabel').textContent = $('#sidebar').classList.contains('open') ? '收起筛选' : '筛选与统计';
}

/* ── 主渲染 ───────────────────────────────────────── */
function renderAll() {
  normalizeState();
  const plans = currentPlans();
  const courses = filterCourses(plans);
  const st = calcStats(plans, courses);
  const root = buildTree(plans, courses);

  if (state.first || state.resetOpen) {
    const activePlanCount = new Set(courses.map((c) => c.pid)).size;
    state.open = defaultOpenIds(root, state.first ? plans.length : activePlanCount);
    state.resetOpen = false;
    state.first = false;
  }

  renderPlanCards();
  renderHeader(st);
  renderTree(root);
  renderStats(st);

  if (controlsYear !== state.year) {
    renderPlanSelect();
    renderNatureChips();
    renderYearChips();
    renderCategoryList();
    controlsYear = state.year;
  }
  syncControls(st);
}

/* ── 交互 ─────────────────────────────────────────── */
function setYear(year) {
  if (state.year === year) return;
  state.year = year;
  if (state.planId !== 'all' && !PLANS.some((p) => p.id === state.planId && p.year === year)) state.planId = 'all';
  state.query = '';
  state.resetOpen = true;
  controlsYear = null;
  renderAll();
}

function setMode(mode) {
  if (state.mode === mode) return;
  state.mode = mode;
  state.resetOpen = true;
  renderAll();
}

function setPlan(pid) {
  state.planId = pid;
  state.resetOpen = true;
  renderAll();
}

function toggleGroup(row) {
  const nodeEl = row.closest('.node');
  if (!nodeEl) return;
  const children = nodeEl.querySelector(':scope > .children');
  if (!children) return;
  const willOpen = children.hidden;
  children.hidden = !willOpen;
  nodeEl.classList.toggle('is-open', willOpen);
  row.setAttribute('aria-expanded', String(willOpen));
  if (willOpen) state.open.add(nodeEl.dataset.id);
  else state.open.delete(nodeEl.dataset.id);
}

function expandAll() {
  $$('#tree .node').forEach((n) => {
    if (n.querySelector(':scope > .children')) state.open.add(n.dataset.id);
  });
  renderAll();
}

function resetView() {
  state.query = '';
  state.resetOpen = true;
  renderAll();
}

function resetFilters() {
  state.planId = 'all';
  state.nature = 'all';
  state.years = new Set(['1', '2', '3', '4']);
  state.cats = new Set(ALL_CATS);
  state.query = '';
  state.resetOpen = true;
  renderAll();
}

/* ── 课程详情 ─────────────────────────────────────── */
function openCourse(id) {
  const node = NODE_MAP.get(id);
  if (!node || node.type !== 'course') return;
  const c = node.course;
  const offers = (node.offers || [c]).slice().sort((a, b) => planSort(PLAN_BY_ID.get(a.pid), PLAN_BY_ID.get(b.pid)) || (a.ry - b.ry) || (Number(a.q) - Number(b.q)));
  const xs = [...new Set(offers.map((o) => o.x))].sort((a, b) => a - b);
  const zs = [...new Set(offers.map((o) => o.z))];
  const terms = [...new Set(offers.map((o) => o.term))];
  const mods = [...new Set(offers.map((o) => o.m))];
  const oms = [...new Set(offers.map((o) => o.om).filter(Boolean))];
  const omLabel = oms.join(' / ');
  const cats = [...new Set(offers.map((o) => o.c))];
  const hours = [...new Set(offers.map((o) => o.h))].sort((a, b) => a - b);
  const depts = [...new Set(offers.map((o) => o.d).filter(Boolean))];
  const xLabel = xs.length === 1 ? fmt(xs[0]) : `${fmt(xs[0])}–${fmt(xs[xs.length - 1])}`;
  const zLabel = zs.length === 1 ? zs[0] : '必修/限选';
  const termLabel = terms.length === 1 ? terms[0] : '多学期';
  const modLabel = mods.length === 1 ? mods[0] : '多模块';
  const showOm = omLabel && (oms.length > 1 || omLabel !== modLabel);
  const catLabel = cats.length === 1 ? cats[0] : '多领域';
  const hLabel = hours.length === 1 ? String(hours[0]) : `${hours[0]}–${hours[hours.length - 1]}`;
  const deptLabel = depts.length === 1 ? depts[0] : `${depts.length} 个开课单位`;
  const allRequired = offers.every((o) => o.rq === 1);
  const planCount = new Set(offers.map((o) => o.pid)).size;
  const p0 = PLAN_BY_ID.get(offers[0].pid);
  const path = ['计算机与计算科学学院', `${p0.discipline} · ${p0.majorClass}`, p0.major + (p0.track ? ` · ${p0.track}` : ''), modLabel, '课程'];
  const dup = offers.some((o) => o.dup > 1);

  $('#drawerKicker').textContent = `${c.k} · ${xLabel} 学分`;
  $('#drawerTitle').textContent = c.n;
  $('#drawerMeta').textContent = `${zLabel} · ${termLabel}${planCount > 1 ? ` · ${planCount} 个方案` : ''}`;

  const offerHTML = offers.map((o) => {
    const p = PLAN_BY_ID.get(o.pid);
    return `<button type="button" class="offer" data-offer-pid="${esc(p.id)}" title="只看这套方案">
      <b>${esc(p.planLabel)}</b>
      <small>${esc(o.m)} · ${esc(o.z)} · ${esc(o.term)}（${esc(o.y)} 第${esc(o.q)}学期）</small>
      ${o.dup > 1 ? `<em>原表 2 条重复记录，已合并</em>` : ''}
    </button>`;
  }).join('');

  $('#drawerBody').innerHTML = `
    <div class="detail-grid">
      <div class="detail-item"><span>课程性质</span><b>${esc(zLabel)}${allRequired ? ' · 必上' : ''}</b></div>
      <div class="detail-item"><span>建议学期</span><b>${esc(termLabel)}</b></div>
      <div class="detail-item"><span>课程模块</span><b>${esc(modLabel)}</b></div>
      ${showOm ? `<div class="detail-item"><span>原表模块</span><b>${esc(omLabel)}</b></div>` : ''}
      <div class="detail-item"><span>知识大类</span><b>${esc(catLabel)}</b></div>
      <div class="detail-item"><span>学时</span><b>${esc(hLabel)}</b></div>
      <div class="detail-item"><span>开课院系</span><b>${esc(deptLabel)}</b></div>
      <div class="detail-item${showOm ? '' : ' wide'}"><span>课程号 / 开设方案</span><b>${esc(c.k)} · ${planCount} 套方案</b></div>
    </div>
    <div class="drawer-section">
      <h4>所属培养方案 <span style="margin-left:auto;font-weight:400;color:var(--faint);font-size:9px;letter-spacing:.04em">全年级开设</span></h4>
      ${offerHTML}
    </div>
    <div class="drawer-section">
      <h4>知识位置</h4>
      <div class="path">${path.map(esc).join(' <span style="color:#c9bfa9">›</span> ')}</div>
      ${planCount > 1 ? '<p class="drawer-note" style="border:0;margin-top:6px;padding:0">路径以第一个方案为例；不同方案中的模块归属可能不同，完整列表见上。</p>' : ''}
    </div>
    ${dup ? '<p class="drawer-note">原表重复记录：2026 软件工程的“大模型技术与实践”出现 2 次，本图合并为 1 门；计划课程数仍按教务口径 76 门计。</p>' : ''}
    <p class="drawer-note">先修关系：原文件未提供课程先修关系；本图只表达课程归属与分类，不代表修读顺序。</p>
  `;

  $('#drawer').classList.add('on');
  $('#drawer').setAttribute('aria-hidden', 'false');
  $('#scrim').classList.add('on');
  document.body.classList.add('locked');
  $('#drawerBody').scrollTop = 0;
  drawerReturnFocus = document.activeElement;
  $('#drawerClose').focus();
}

function closeDrawer() {
  $('#drawer').classList.remove('on');
  $('#drawer').setAttribute('aria-hidden', 'true');
  $('#scrim').classList.remove('on');
  if (!$('#overviewWrap').classList.contains('on')) document.body.classList.remove('locked');
  if (drawerReturnFocus && document.contains(drawerReturnFocus)) drawerReturnFocus.focus();
  drawerReturnFocus = null;
}

function setMobileFilters(open) {
  $('#sidebar').classList.toggle('open', open);
  document.body.classList.toggle('filters-open', open && window.innerWidth <= 900);
  $('#mobileFilter').setAttribute('aria-expanded', String(open));
  $('#mobileFilterLabel').textContent = open ? '收起筛选' : '筛选与统计';
}

/* ── 总览 ─────────────────────────────────────────── */
function renderOverview() {
  const years = ['2025', '2026'];
  let rows = '';
  for (const y of years) {
    rows += `<tr class="year-row"><td colspan="8">${y} 级</td></tr>`;
    PLANS.filter((p) => p.year === y).sort(planSort).forEach((p) => {
      const note = p.uniqueCount < p.courseCount ? `含 1 条重复记录，去重 ${p.uniqueCount} 门` : '—';
      rows += `<tr>
        <td>${y}</td>
        <td>${esc(p.discipline)} · ${esc(p.majorClass)}</td>
        <td>${esc(p.major)}</td>
        <td>${p.track ? esc(p.track) : '<span class="muted">—</span>'}</td>
        <td class="num">${p.courseCount}</td>
        <td class="num">${p.credits}</td>
        <td>${p.classes}</td>
        <td class="muted">${note}</td>
      </tr>`;
    });
  }
  $('#overviewTable').innerHTML = `<table>
    <thead><tr><th>年级</th><th>门类 / 专业类</th><th>专业</th><th>培养类型</th><th>计划课程数</th><th>最低毕业学分</th><th>班级数</th><th>备注</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>`;

  $('#overviewNotes').innerHTML = `
    <div class="modal-note"><b>专业与培养类型</b><p>拔尖创新班属于计算机科学与技术专业下的培养类型，不是独立专业。计算机类共 3 套方案：计科普通班、计科拔尖创新班、软件工程。</p></div>
    <div class="modal-note"><b>课程数与学分</b><p>计划课程数按教务口径；最低毕业学分来自方案页。“Σ”是所列课程学分合计，不等于最低毕业学分，因为选修课有选择空间。</p></div>
    <div class="modal-note"><b>重复记录</b><p>2026 软件工程的“大模型技术与实践”在原表出现 2 次，本图合并展示；计划课程数仍记为 76 门，去重后为 75 门。</p></div>
    <div class="modal-note"><b>先修关系</b><p>原文件只提供课程归属与分类，未提供先修关系。本图不能直接代表课程先后顺序，先修关系需另行梳理。</p></div>
  `;
}

function openOverview() {
  renderOverview();
  modalReturnFocus = document.activeElement;
  $('#overviewWrap').classList.add('on');
  $('#overviewWrap').setAttribute('aria-hidden', 'false');
  document.body.classList.add('locked');
  $('#overviewClose').focus();
}

function closeOverview() {
  $('#overviewWrap').classList.remove('on');
  $('#overviewWrap').setAttribute('aria-hidden', 'true');
  if (!$('#drawer').classList.contains('on')) document.body.classList.remove('locked');
  if (modalReturnFocus && document.contains(modalReturnFocus)) modalReturnFocus.focus();
  modalReturnFocus = null;
}

/* ── 事件绑定 ─────────────────────────────────────── */
function bindEvents() {
  $$('.year-switch button').forEach((b) => b.addEventListener('click', () => setYear(b.dataset.year)));
  $$('#modebar button').forEach((b) => b.addEventListener('click', () => setMode(b.dataset.mode)));

  $('#planSelect').addEventListener('change', (e) => setPlan(e.target.value));

  $('#planCards').addEventListener('click', (e) => {
    const card = e.target.closest('[data-pid]');
    if (!card) return;
    setPlan(state.planId === card.dataset.pid ? 'all' : card.dataset.pid);
  });

  $('#natureChips').addEventListener('click', (e) => {
    const b = e.target.closest('[data-nature]');
    if (!b) return;
    state.nature = b.dataset.nature;
    renderAll();
  });

  $('#yearChips').addEventListener('click', (e) => {
    const b = e.target.closest('[data-year]');
    if (!b) return;
    const ry = String(b.dataset.year);
    const next = new Set(state.years);
    if (next.has(ry)) {
      if (next.size === 1) return;
      next.delete(ry);
    } else {
      next.add(ry);
    }
    state.years = next;
    renderAll();
  });

  $('#allYears').addEventListener('click', () => {
    state.years = new Set(['1', '2', '3', '4']);
    renderAll();
  });

  $('#catList').addEventListener('change', (e) => {
    const input = e.target.closest('input[data-cat]');
    if (!input) return;
    const cat = input.dataset.cat;
    if (input.checked) state.cats.add(cat); else state.cats.delete(cat);
    renderAll();
  });

  $('#catsAll').addEventListener('click', () => {
    state.cats = new Set(ALL_CATS);
    renderAll();
  });

  $('#catsNone').addEventListener('click', () => {
    state.cats = new Set();
    renderAll();
  });

  $('#resetFilters').addEventListener('click', resetFilters);

  let searchTimer = null;
  $('#search').addEventListener('input', (e) => {
    const value = e.target.value;
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      state.query = value;
      renderAll();
    }, 120);
  });
  $('#searchClear').addEventListener('click', () => {
    state.query = '';
    renderAll();
    $('#search').focus();
  });

  $('#expandAll').addEventListener('click', expandAll);
  $('#resetView').addEventListener('click', resetView);

  $('#tree').addEventListener('click', (e) => {
    const action = e.target.closest('[data-action]');
    if (action) {
      if (action.dataset.action === 'reset-filters') resetFilters();
      return;
    }
    const row = e.target.closest('.row');
    if (!row) return;
    if (row.dataset.course) {
      openCourse(row.dataset.id);
    } else {
      toggleGroup(row);
    }
  });

  $('#tree').addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
    const row = e.target.closest('.row');
    if (!row) return;
    const visible = $$('#tree .row').filter((r) => r.offsetParent !== null);
    const idx = visible.indexOf(row);
    if (idx < 0) return;
    e.preventDefault();
    const next = visible[idx + (e.key === 'ArrowDown' ? 1 : -1)];
    if (next) next.focus();
  });

  $('#drawerClose').addEventListener('click', closeDrawer);
  $('#scrim').addEventListener('click', closeDrawer);
  $('#drawerBody').addEventListener('click', (e) => {
    const offer = e.target.closest('[data-offer-pid]');
    if (!offer) return;
    state.planId = offer.dataset.offerPid;
    state.resetOpen = true;
    drawerReturnFocus = null;
    closeDrawer();
    renderAll();
  });

  $('#overviewBtn').addEventListener('click', openOverview);
  $('#overviewClose').addEventListener('click', closeOverview);
  $('#overviewWrap').addEventListener('click', (e) => { if (e.target === $('#overviewWrap')) closeOverview(); });

  $('#mobileFilter').addEventListener('click', () => {
    setMobileFilters(!$('#sidebar').classList.contains('open'));
  });

  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    if ($('#sidebar').classList.contains('open')) { setMobileFilters(false); return; }
    if ($('#overviewWrap').classList.contains('on')) { closeOverview(); return; }
    if ($('#drawer').classList.contains('on')) { closeDrawer(); return; }
    if (state.query) { state.query = ''; renderAll(); }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) setMobileFilters(false);
  });
}

/* ── 启动 ─────────────────────────────────────────── */
function init() {
  bindEvents();
  renderAll();
}
init();

})();
