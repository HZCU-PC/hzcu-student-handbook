/* 学期安排页：按本机日期算出「本周第几周 / 距考试 / 距寒假」。
   数据来自页面上的 data-* 属性（由 scripts/gen_semester_schedule.py 写入），
   所以换学年只要重新生成页面，这段脚本不用改。 */
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

  function render() {
    var box = document.querySelector(".semester-progress");
    if (!box) return;

    var start = parseDate(box.dataset.weeksStart);
    var total = Number(box.dataset.weeksTotal || 0);
    var exam = parseDate(box.dataset.examStart);
    var brk = parseDate(box.dataset.winterBreak);
    if (!start || !total) return;

    var weekEl = box.querySelector(".sp-week");
    var examEl = box.querySelector(".sp-exam");
    var brkEl = box.querySelector(".sp-break");
    var today = startOfDay(new Date());
    var diff = daysBetween(start, today);
    var week = Math.floor(diff / 7) + 1;

    if (diff < 0) {
      if (weekEl) weekEl.textContent = "未开学";
      if (examEl && exam) examEl.textContent = daysBetween(today, exam);
      if (brkEl && brk) brkEl.textContent = daysBetween(today, brk);
      return;
    }

    if (week > total) {
      if (weekEl) weekEl.textContent = "已结束";
      box.querySelectorAll(".sp-exam, .sp-break").forEach(function (el) {
        var wrap = el.parentNode;
        if (wrap) wrap.textContent = "本学期已结束";
      });
      return;
    }

    if (weekEl) weekEl.textContent = String(week);

    if (examEl && exam) {
      var toExam = daysBetween(today, exam);
      examEl.textContent = toExam > 0 ? String(toExam) : "已开始";
    }

    if (brkEl && brk) {
      var toBreak = daysBetween(today, brk);
      brkEl.textContent = toBreak > 0 ? String(toBreak) : "已开始";
    }

    // 落在考试周里时，把进度条标成强调态
    if (exam && today >= startOfDay(exam)) {
      box.classList.add("is-exam");
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }

  // Material 的即时导航会替换内容区，需要重新计算
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(render);
  }
})();
