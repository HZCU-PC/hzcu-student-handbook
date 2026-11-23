/* 学期安排页：按本机日期算出「本周第几周 / 距考试 / 距寒假」，
   并把今天的格子、当前周的进度条段落点亮。
   所有日期来自页面上的 data-* 属性（由 scripts/gen_semester_schedule.py 写入），
   换学年只要重新生成页面，这段脚本不用改。 */
(function () {
  "use strict";

  var DAY = 86400000;

  function startOfDay(d) {
    return new Date(d.getFullYear(), d.getMonth(), d.getDate());
  }

  function parseDate(value) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value || "");
    if (!m) return null;
    return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  }

  function daysBetween(from, to) {
    return Math.round((startOfDay(to) - startOfDay(from)) / DAY);
  }

  function addDays(d, n) {
    return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
  }

  function iso(d) {
    var m = d.getMonth() + 1;
    var day = d.getDate();
    return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (day < 10 ? "0" : "") + day;
  }

  function shortDate(d) {
    return d.getMonth() + 1 + "/" + d.getDate();
  }

  function each(list, fn) {
    Array.prototype.forEach.call(list, fn);
  }

  function setText(root, key, value) {
    var el = root && root.querySelector('[data-sp="' + key + '"]');
    if (el) el.textContent = value;
  }

  function render() {
    var cal = document.querySelector(".semester-cal");
    var rail = document.querySelector(".semester-rail");
    var cfgEl = cal || rail;
    if (!cfgEl || !cfgEl.dataset.weeksStart) return;

    var start = parseDate(cfgEl.dataset.weeksStart);
    var total = Number(cfgEl.dataset.weeksTotal || 0);
    var exam = parseDate(cfgEl.dataset.examStart);
    var brk = parseDate(cfgEl.dataset.winterBreak);
    if (!start || !total) return;

    var today = startOfDay(new Date());
    var diff = daysBetween(start, today);
    var week = Math.floor(diff / 7) + 1;
    var before = diff < 0;
    var after = week > total;
    var inTerm = !before && !after;
    var examWeek = exam ? Math.floor(daysBetween(start, exam) / 7) + 1 : 0;

    /* ---------- 进度条 ---------- */
    if (rail) {
      each(rail.querySelectorAll(".semester-bar i"), function (el, i) {
        var n = i + 1;
        el.classList.toggle("is-past", !before && (after || n < week));
        el.classList.toggle("is-now", inTerm && n === week);
        el.classList.toggle("is-exam", examWeek > 0 && n >= examWeek);
      });

      if (before) {
        setText(rail, "week", "未开学");
        setText(rail, "range", "距开学 " + Math.abs(diff) + " 天");
      } else if (after) {
        setText(rail, "week", "已结束");
        setText(rail, "range", "共 " + total + " 周");
      } else {
        var from = addDays(start, (week - 1) * 7);
        setText(rail, "week", "第 " + week + " 周");
        setText(rail, "range", shortDate(from) + " — " + shortDate(addDays(from, 6)));
      }

      if (exam) {
        var toExam = daysBetween(today, exam);
        setText(rail, "to-exam", toExam > 0 ? String(toExam) : "已开始");
        var wrap = rail.querySelector('[data-sp="to-exam"]');
        if (wrap && toExam <= 0 && wrap.parentNode) wrap.parentNode.classList.add("is-on");
      }

      if (brk) {
        var toBreak = daysBetween(today, brk);
        setText(rail, "to-break", toBreak > 0 ? String(toBreak) : "已开始");
      }
    }

    /* ---------- 今天的格子 ---------- */
    var key = iso(today);
    each(document.querySelectorAll(".sg-cd[data-date]"), function (el) {
      el.classList.toggle("is-today", el.dataset.date === key);
    });

    /* ---------- 周次速查里高亮本周 ---------- */
    each(document.querySelectorAll(".semester-lookup tr[data-row-week]"), function (tr) {
      tr.classList.toggle("is-now", inTerm && Number(tr.dataset.rowWeek) === week);
    });

    /* ---------- 底部读数 ---------- */
    var readout = document.querySelector(".semester-readout");
    if (readout) {
      if (before) {
        readout.textContent = "距开学 " + Math.abs(diff) + " 天";
      } else if (after) {
        readout.textContent = "本学期已结束";
      } else {
        var monday = addDays(start, (week - 1) * 7);
        readout.innerHTML =
          "第 <b>" + week + "</b> 周 · " + shortDate(monday) + " — " + shortDate(addDays(monday, 6));
      }
    }
  }

  /* ---------- 悬停看任意一周 ---------- */
  function bindHover() {
    var cal = document.querySelector(".semester-cal");
    if (!cal) return;
    var readout = cal.querySelector(".semester-readout");
    var grid = cal.querySelector(".semester-grid");
    if (!readout || !grid) return;

    function clear() {
      each(grid.querySelectorAll(".is-hl"), function (el) {
        el.classList.remove("is-hl");
      });
      each(grid.querySelectorAll(".sg-wn.on"), function (el) {
        el.classList.remove("on");
      });
      render(); // 复位读数（顺便把本周的状态重新点亮）
    }

    cal.addEventListener("mouseover", function (e) {
      var cell = e.target.closest("[data-col]");
      if (!cell) return;
      var col = cell.dataset.col;
      var date = parseDate(cell.dataset.date || "");
      if (!date) return;

      each(grid.querySelectorAll(".is-hl"), function (el) {
        el.classList.remove("is-hl");
      });
      each(grid.querySelectorAll('[data-col="' + col + '"]'), function (el) {
        if (el.classList.contains("sg-cd")) el.classList.add("is-hl");
      });
      each(grid.querySelectorAll(".sg-wn"), function (el) {
        el.classList.toggle("on", el.dataset.col === col);
      });

      var monday = addDays(date, -((date.getDay() + 6) % 7));
      var label = cell.dataset.week ? "第 " + cell.dataset.week + " 周" : cell.dataset.colLabel;
      readout.innerHTML =
        "<b>" + (label || "") + "</b>" +
        (label ? " · " : "") +
        shortDate(monday) + " — " + shortDate(addDays(monday, 6));
    });

    cal.addEventListener("mouseleave", clear);
  }

  function boot() {
    render();
    bindHover();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  // Material 的即时导航会替换内容区，需要重新计算
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(render);
  }
})();
