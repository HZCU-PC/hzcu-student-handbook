/* 双轨时间线 · 全站脚本 */
const D = window.DATA;
const P = D.papers, ERAS = D.eras, CLUES = D.clues;
const byId = Object.fromEntries(P.map(p => [p.id, p]));
const TRACK = { B: { name: "突破轨", cls: "b" }, F: { name: "前沿轨", cls: "f" } };

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => (s || "").replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
const paperUrl = p => "paper.html?id=" + p.id;

/* ---------- 极简 markdown → html（用于评选标准等文档段落） ---------- */
function md(src) {
  if (!src) return "";
  const lines = src.split("\n").filter(l => l.trim() !== "" && !/^\*.*\*$/.test(l.trim()));
  let out = "", inTable = false, inList = false;
  for (let raw of lines) {
    const l = raw.trim();
    if (/^\|/.test(l)) {
      const cells = l.split("|").slice(1, -1).map(c => c.trim());
      if (/^[-: ]+$/.test(cells.join(""))) continue;
      if (!inTable) { out += "<table>"; inTable = true; }
      const tag = /^[|]/.test(l) && out.endsWith("<table>") ? "th" : "td";
      out += "<tr>" + cells.map(c => `<${tag}>${inline(c)}</${tag}>`).join("") + "</tr>";
      continue;
    }
    if (inTable) { out += "</table>"; inTable = false; }
    if (/^>/.test(l)) { out += `<blockquote>${inline(l.replace(/^>\s*/, ""))}</blockquote>`; continue; }
    if (/^[-*]\s/.test(l)) {
      if (!inList) { out += "<ul>"; inList = true; }
      out += `<li>${inline(l.replace(/^[-*]\s+/, ""))}</li>`; continue;
    }
    if (inList) { out += "</ul>"; inList = false; }
    if (/^#{3,4}\s/.test(l)) { out += `<h4>${inline(l.replace(/^#+\s+/, ""))}</h4>`; continue; }
    out += `<p>${inline(l)}</p>`;
  }
  if (inTable) out += "</table>";
  if (inList) out += "</ul>";
  return out;
}
function inline(s) {
  return esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/`(.+?)`/g, "<code>$1</code>");
}

/* ---------- 双尺度轴：年 → x 比例（0~1） ---------- */
const SPLIT = 2011.5, Y0 = 1986, Y1 = 2026;
function xRatio(year) {
  if (year <= SPLIT) return 0.30 * (year - Y0) / (SPLIT - Y0);
  return 0.30 + 0.70 * (year - SPLIT) / (Y1 - SPLIT);
}
function eraOf(year) {
  return ERAS.find(e => {
    const [a, b] = e.range.split("-").map(Number);
    return year >= a && year <= b;
  }) || ERAS[ERAS.length - 1];
}

/* ---------- 双轨条渲染（hero / 迷你导航） ---------- */
function renderStrip(host, opts = {}) {
  const W = host.clientWidth || 1000;
  const compact = !!opts.compact;
  const years = [...new Set(P.map(p => p.year))].sort((a, b) => a - b);
  let html = "";
  for (const tr of ["B", "F"]) {
    html += `<div class="lane${compact ? "" : " lane-dark"}"><span class="tag">${TRACK[tr].name}</span>`;
    ERAS.forEach((e, i) => {
      const [a, b] = e.range.split("-").map(Number);
      html += `<div class="era-band" style="left:${xRatio(a) * 100}%;width:${(xRatio(b) - xRatio(a)) * 100}%;background:${i % 2 ? "#0091ff" : "#0064e0"}"></div>`;
    });
    for (const y of years) {
      const list = P.filter(p => p.year === y && p.track === tr);
      list.forEach((p, i) => {
        const size = compact ? 9 : (p.track === "B" ? 14 : 12);
        html += `<a class="dot ${TRACK[tr].cls}" data-id="${p.id}" title="${esc(p.zh || p.en)}"
          style="left:${xRatio(y) * 100}%;width:${size}px;height:${size}px;margin-top:${i * -16}px"></a>`;
      });
    }
    html += `</div>`;
  }
  if (!compact) {
    html += `<div class="ticks">`;
    for (let y = 1986; y <= 2011; y += 5) html += `<i style="left:${xRatio(y) * 100}%"></i><b style="left:${xRatio(y) * 100}%">${y}</b>`;
    html += `<i style="left:${xRatio(2011.5) * 100}%"></i>`;
    for (let y = 2012; y <= 2026; y += 2) html += `<i style="left:${xRatio(y) * 100}%"></i><b style="left:${xRatio(y) * 100}%">${y}</b>`;
    html += `</div>`;
  }
  host.innerHTML = html;
}

/* ---------- 全局：导航 / 迷你导航 / 速查抽屉 ---------- */
function initChrome() {
  const page = document.body.dataset.page;
  $$(".nav-links a").forEach(a => a.classList.toggle("on", a.dataset.page === page));

  // 迷你双轨导航条
  const mn = $("#mininav");
  if (mn) {
    renderStrip($(".mn-body", mn), { compact: true });
    const [a, b] = ["1986", "2026"];
    ERAS.forEach(e => {
      const [s, t] = e.range.split("-").map(Number);
      const el = document.createElement("div");
      el.className = "mn-era";
      el.style.left = xRatio(s) * 100 + "%";
      el.style.width = (xRatio(t) - xRatio(s)) * 100 + "%";
      el.innerHTML = `<b>${esc(e.name)}</b>`;
      $(".mn-body", mn).appendChild(el);
    });
    if (page === "paper") {
      const id = new URLSearchParams(location.search).get("id");
      const p = byId[id];
      if (p) {
        $(".mn-head .cur", mn).textContent = `${p.id} · ${p.year} · ${p.zh || p.en}`;
        const dot = $(`.mn-body .dot[data-id="${p.id}"]`);
        if (dot) dot.classList.add("now");
      }
    } else {
      $(".mn-head .cur", mn).textContent = "当前位置：滚动或悬停任意节点定位";
    }
    const show = () => mn.classList.add("show");
    setTimeout(show, 400);
    addEventListener("scroll", () => {
      mn.classList.toggle("show", scrollY > 240 || page === "timeline");
    });
    $$(".mn-body .dot").forEach(d => d.addEventListener("click", e => { e.preventDefault(); location.href = paperUrl(byId[d.dataset.id]); }));
  }

  // 速查抽屉
  const drawer = $("#drawer"), scrim = $("#scrim");
  const openD = () => { drawer.classList.add("open"); scrim.classList.add("on"); $(".search input", drawer).focus(); };
  const closeD = () => { drawer.classList.remove("open"); scrim.classList.remove("on"); };
  $("#openIndex")?.addEventListener("click", openD);
  $("#closeDrawer")?.addEventListener("click", closeD);
  scrim?.addEventListener("click", closeD);
  addEventListener("keydown", e => {
    if (e.key === "Escape") closeD();
    if (e.key === "/" && !/input/i.test(e.target.tagName)) { e.preventDefault(); openD(); }
  });
  const listEl = $("#drawerList");
  const draw = q => {
    const qq = (q || "").trim().toLowerCase();
    const rows = P.filter(p => !qq || (p.zh + p.en + p.id + p.venue + p.year + (p.tags || []).join("")).toLowerCase().includes(qq));
    listEl.innerHTML = rows.map(p => `<a class="item" href="${paperUrl(p)}"><span class="id">${p.id}</span><i class="${TRACK[p.track].cls}"></i><span>${esc(p.zh || p.en)}</span><span class="yr">${p.year}</span></a>`).join("")
      || `<p style="padding:16px;color:var(--steel);font-size:14px">没有匹配的论文</p>`;
  };
  draw();
  $(".search input", drawer).addEventListener("input", e => draw(e.target.value));
}

/* ---------- 筛选项（时间线 / 索引共用） ---------- */
function buildFilters(host, onChange) {
  const state = { track: "all", era: "all" };
  const counts = () => {
    const f = P.filter(p => (state.track === "all" || p.track === state.track) && (state.era === "all" || eraOf(p.year).name === state.era));
    return f;
  };
  const groups = [
    { key: "track", items: [{ v: "all", l: "全部轨道" }, { v: "B", l: "突破轨" }, { v: "F", l: "前沿轨" }] },
    { key: "era", items: [{ v: "all", l: "全部时代" }, ...ERAS.map(e => ({ v: e.name, l: e.name }))] }
  ];
  host.innerHTML = groups.map(g =>
    `<div class="pills">` + g.items.map(i => `<button class="pill${i.v === "all" ? " active" : ""}" data-k="${g.key}" data-v="${i.v}">${esc(i.l)}<span class="n"></span></button>`).join("") + `</div>`
  ).join("");
  const refresh = () => {
    $$(".pill", host).forEach(b => {
      const k = b.dataset.k, v = b.dataset.v;
      b.classList.toggle("active", state[k] === v);
      const n = v === "all" ? P.length : P.filter(p => k === "track" ? p.track === v : eraOf(p.year).name === v).length;
      $(".n", b).textContent = n;
    });
    onChange(P.filter(p => (state.track === "all" || p.track === state.track) && (state.era === "all" || eraOf(p.year).name === state.era)));
  };
  $$(".pill", host).forEach(b => b.addEventListener("click", () => { state[b.dataset.k] = b.dataset.v; refresh(); }));
  refresh();
  return state;
}

/* ---------- 动效：进入视口渐显 + 圆点错峰入场 ---------- */
function initMotion() {
  const els = $$("section .sec-head, section .card, .era, .md");
  els.forEach(el => el.classList.add("reveal"));
  if (!("IntersectionObserver" in window)) {
    els.forEach(el => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver(es => {
      es.forEach(e => {
        if (!e.isIntersecting) return;
        const sibs = [...e.target.parentElement.children].filter(c => c.classList?.contains("reveal"));
        e.target.style.transitionDelay = Math.min(sibs.indexOf(e.target), 6) * 0.07 + "s";
        e.target.classList.add("in");
        io.unobserve(e.target);
      });
    }, { threshold: .12 });
    els.forEach(el => io.observe(el));
  }

  // 双轨条圆点错峰入场（按 x 顺序）
  $$("#heroStrip .dot, .mn-body .dot").forEach(d => {
    d.style.animationDelay = (parseFloat(d.style.left) / 100 * 0.8) + "s";
  });
  // 时代章节名片错峰
  $$(".era").forEach((era, i) => {
    era.style.animationDelay = (i * 0.1) + "s";
    $$(".chip", era).forEach((c, k) => c.style.animationDelay = (0.15 + k * 0.05) + "s");
  });
  $$(".clue").forEach((c, k) => c.style.animationDelay = (0.1 + k * 0.09) + "s");
}

document.addEventListener("DOMContentLoaded", () => { initChrome(); initMotion(); });
