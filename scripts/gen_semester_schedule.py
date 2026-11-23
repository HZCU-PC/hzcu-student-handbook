#!/usr/bin/env python3
"""生成 docs/semester.md 的学期安排正文。

所有日期数据集中在 DATA 里，改日期只改这一处，重新运行本脚本即可：

    python scripts/gen_semester_schedule.py

数据来源：浙大城市学院 2026—2027 学年校历（第一学期 / 秋冬学期）。
官方原文由学校公众号发布，本页只做搬运与整理；日期以教务处最新通知为准。

页面结构：概览数据带 → 学期进度条 → 整月校历网格（事件写在格子里）→ 关键节点
→ 周次速查（折叠）→ 节奏建议 → 维护说明。样式在 docs/stylesheets/semester.css，
「本周第几周 / 今天高亮」由 docs/javascripts/semester-progress.js 按本机日期算。
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

DATA = {
    "academic_year": "2026—2027",
    "term": "第一学期（秋冬学期）",
    "weeks_start": "2026-09-14",   # 第 1 周星期一
    "weeks_total": 19,
    "exam_start": "2027-01-12",
    "exam_end": "2027-01-20",
    "winter_break": "2027-01-21",
    "spring_start": "2027-02-22",  # 第二学期开课（日期以官方通知为准）
    "grid_start": "2026-08-31",    # 网格首列星期一（让 9/1 落在完整的月份里）
    "grid_end": "2027-01-31",      # 网格末列星期日（1 月排满）
    "events": [
        ("2026-08-28", None, "本科生、研究生新生报到注册", ""),
        ("2026-08-29", "2026-09-13", "新生始业教育、军训", "专升本新生不参加军训"),
        ("2026-09-11", None, "本科生老生报到注册", "在校生返校"),
        ("2026-09-14", None, "全校开始上课", "第 1 周星期一"),
        ("2026-09-20", None, "上双周周五课程", "中秋节调休补课"),
        ("2026-09-25", "2026-09-27", "中秋节放假调休", ""),
        ("2026-10-01", "2026-10-07", "国庆节放假调休", ""),
        ("2026-10-10", None, "上单周周五课程", "国庆节调休补课"),
        ("2026-10-30", "2026-10-31", "校运动会", ""),
        ("2026-11-09", "2026-11-15", "期中考试", "不停课，按课表照常上课"),
        ("2027-01-01", None, "元旦法定假日", "调休安排另行通知"),
        ("2027-01-12", "2027-01-20", "全校停课考试", "考试周"),
        ("2027-01-21", None, "寒假开始", "2027 年春节为 2 月 6 日"),
    ],
}

WEEKDAY_CN = "一二三四五六日"

# 格子里的短标签：日期区间 -> (文字, 类型)
# 类型决定底色：hol=放假（琥珀）、exam=停课考试（墨）、mid=期中（浅墨），
# 其余（make 补课 / start 开课 / info 军训、运动会）只给文字，不铺底。
MARKS = [
    ("2026-08-29", "2026-09-13", "军训", "info"),
    ("2026-09-14", None, "开课", "start"),
    ("2026-09-20", None, "补课", "make"),
    ("2026-09-25", "2026-09-27", "中秋", "hol"),
    ("2026-10-01", "2026-10-07", "国庆", "hol"),
    ("2026-10-10", None, "补课", "make"),
    ("2026-10-30", "2026-10-31", "运动会", "info"),
    ("2026-11-09", "2026-11-15", "期中", "mid"),
    ("2027-01-01", None, "元旦", "hol"),
    ("2027-01-12", "2027-01-20", "考试", "exam"),
    ("2027-01-21", "2027-01-31", "寒假", "hol"),
]

# 周次速查表里的备注
WEEK_NOTES = {
    2: ("中秋节调休", "hol"),
    3: ("国庆节调休", "hol"),
    4: ("国庆节调休", "hol"),
    7: ("校运动会", "info"),
    9: ("期中考试（不停课）", "mid"),
    18: ("考试周", "exam"),
    19: ("考试周", "exam"),
}


def d(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def fmt(day: dt.date) -> str:
    return f"{day.year} 年 {day.month} 月 {day.day} 日"


def short(day: dt.date) -> str:
    return f"{day.month}/{day.day}"


def span(start: str, end: str | None) -> str:
    s = d(start)
    if not end:
        return f"{fmt(s)}（周{WEEKDAY_CN[s.weekday()]}）"
    e = d(end)
    if s.year == e.year and s.month == e.month:
        return f"{fmt(s)}—{e.day} 日"
    return f"{fmt(s)}—{fmt(e)}"


def weeks() -> list[dict]:
    out = []
    start = d(DATA["weeks_start"])
    exam_s, exam_e = d(DATA["exam_start"]), d(DATA["exam_end"])
    for i in range(DATA["weeks_total"]):
        ws = start + dt.timedelta(weeks=i)
        we = ws + dt.timedelta(days=6)
        note = ""
        if ws <= exam_e and we >= exam_s:
            note = "考试周"
        elif ws <= d("2026-11-15") and we >= d("2026-11-09"):
            note = "期中考试（不停课）"
        elif ws <= d("2026-10-07") and we >= d("2026-10-01"):
            note = "国庆节放假调休"
        elif ws <= d("2026-09-27") and we >= d("2026-09-25"):
            note = "中秋节放假调休"
        elif ws <= d("2026-10-31") and we >= d("2026-10-30"):
            note = "校运动会"
        out.append({"n": i + 1, "start": ws, "end": we, "note": note})
    return out


# ---------------------------------------------------------------- 网格辅助


def day_marks() -> dict[dt.date, tuple[str, str]]:
    """日期 -> (短标签, 类型)。"""
    marks: dict[dt.date, tuple[str, str]] = {}
    for start, end, label, kind in MARKS:
        cur = d(start)
        last = d(end) if end else cur
        while cur <= last:
            marks[cur] = (label, kind)
            cur += dt.timedelta(days=1)
    return marks


def grid_columns() -> list[dt.date]:
    """每一列的星期一。"""
    start, end = d(DATA["grid_start"]), d(DATA["grid_end"])
    n = (end - start).days // 7 + 1
    return [start + dt.timedelta(weeks=i) for i in range(n)]


def week_no(monday: dt.date) -> int | None:
    n = (monday - d(DATA["weeks_start"])).days // 7 + 1
    return n if 1 <= n <= DATA["weeks_total"] else None


def col_label(monday: dt.date) -> str:
    """不属于第 1—19 周的列，给个说法给悬停读数用。"""
    if monday < d(DATA["weeks_start"]):
        return "开学前"
    return "寒假"


# ---------------------------------------------------------------- 各区块


def build_stats() -> str:
    ws = d(DATA["weeks_start"])
    exam_s, exam_e = d(DATA["exam_start"]), d(DATA["exam_end"])
    teach = DATA["weeks_total"] - 2
    items = [
        ("is-key", "正式上课", short(ws), "第 1 周 · 周一"),
        ("", "教学周", f"{teach} 周", "另有 2 周停课考试"),
        ("", "考试周", short(exam_s), f"至 {short(exam_e)}，共 9 天"),
        ("", "寒假", short(d(DATA["winter_break"])), "春节 2 月 6 日"),
    ]
    cells = "".join(
        f'<div class="semester-stat {cls}"><span>{label}</span><b>{value}</b><i>{hint}</i></div>'.replace(
            'semester-stat "', 'semester-stat"'
        )
        for cls, label, value, hint in items
    )
    return f'<div class="semester-stats">{cells}</div>'


def build_rail() -> str:
    n = DATA["weeks_total"]
    exam_week = (d(DATA["exam_start"]) - d(DATA["weeks_start"])).days // 7 + 1
    segs = []
    for i in range(1, n + 1):
        cls = ' class="is-exam"' if i >= exam_week else ""
        segs.append(f"<i{cls}></i>")

    # 月份刻度：按教学周分组
    groups = [(1, 3, "9 月"), (4, 4, "10 月"), (8, 4, "11 月"), (12, 5, "12 月"), (17, 3, "1 月")]
    months = "".join(
        f'<span style="grid-column:{s} / span {w}">{t}</span>' for s, w, t in groups
    )

    attrs = (
        f'data-weeks-start="{DATA["weeks_start"]}" data-weeks-total="{n}" '
        f'data-exam-start="{DATA["exam_start"]}" data-winter-break="{DATA["winter_break"]}"'
    )
    return (
        f'<div class="semester-rail" {attrs}>'
        '<div class="semester-rail__top">'
        '<div class="semester-rail__now">'
        '<b data-sp="week">—</b><em data-sp="range">—</em>'
        f'<span>· 共 {n} 周</span>'
        "</div>"
        '<div class="semester-rail__facts">'
        '<div><span class="lab">距考试周</span><b><span data-sp="to-exam">—</span><small>天</small></b></div>'
        '<div><span class="lab">距寒假</span><b><span data-sp="to-break">—</span><small>天</small></b></div>'
        "</div>"
        "</div>"
        f'<div class="semester-bar">{"".join(segs)}</div>'
        f'<div class="semester-bar__months">{months}</div>'
        "</div>"
    )


def build_calendar() -> str:
    marks = day_marks()
    cols = grid_columns()
    total_cols = len(cols)
    first_day = d(DATA["grid_start"])
    last_day = d(DATA["grid_end"])

    # 月份分组：看每列的星期天落在哪个月
    groups: list[tuple[int, int, str]] = []
    i = 0
    while i < total_cols:
        sunday = cols[i] + dt.timedelta(days=6)
        j = i
        while j + 1 < total_cols and (cols[j + 1] + dt.timedelta(days=6)).month == sunday.month:
            j += 1
        label = f"{sunday.year} 年 {sunday.month} 月" if (i == 0 or sunday.month == 1) else f"{sunday.month} 月"
        groups.append((i, j - i + 1, label))
        i = j + 1

    months = "".join(
        f'<span style="grid-column:{s + 2} / span {w}">{t}</span>' for s, w, t in groups
    )

    head = ['<div class="sg-label"></div>']
    for k, monday in enumerate(cols, start=1):
        n = week_no(monday)
        head.append(f'<div class="sg-wn" data-col="{k}">{n or ""}</div>')

    body: list[str] = []
    for wd in range(7):
        body.append(f'<div class="sg-label">{WEEKDAY_CN[wd]}</div>')
        for k, monday in enumerate(cols, start=1):
            day = monday + dt.timedelta(days=wd)
            label, kind = marks.get(day, ("", ""))
            n = week_no(monday)
            cls = [f"is-{kind}"] if kind else []
            if wd >= 5 and kind not in ("hol", "exam", "mid"):
                cls.append("is-we")
            if day < d("2026-09-01") or day > last_day:
                cls.append("is-out")

            attrs = [f'data-col="{k}"', f'data-date="{day.isoformat()}"']
            if n:
                attrs.append(f'data-week="{n}"')
            else:
                attrs.append(f'data-col-label="{col_label(monday)}"')

            tip = f"{day.isoformat()} 周{WEEKDAY_CN[wd]}"
            if label:
                tip += f" · {label}"
            attrs.append(f'title="{tip}"')

            em = ""
            if label:
                long_cls = ' class="is-long"' if len(label) > 2 else ""
                em = f"<em{long_cls}>{label}</em>"
            klass = (" ".join(cls)).strip()
            body.append(
                f'<div class="sg-cd{(" " + klass) if klass else ""}" {" ".join(attrs)}>'
                f"<b>{day.day}</b>{em}</div>"
            )

    attrs = (
        f'data-weeks-start="{DATA["weeks_start"]}" data-weeks-total="{DATA["weeks_total"]}" '
        f'data-exam-start="{DATA["exam_start"]}" data-winter-break="{DATA["winter_break"]}"'
    )
    return (
        f'<div class="semester-cal" {attrs}>'
        '<div class="semester-cal__scroll"><div class="sg-wrap">'
        f'<div class="semester-grid" style="--cols:{total_cols}">'
        f'<div class="sg sg--months">{months}</div>'
        f'<div class="sg sg--head">{"".join(head)}</div>'
        f'<div class="sg sg--body">{"".join(body)}</div>'
        "</div></div></div>"
        '<div class="semester-cal__foot">'
        '<div class="semester-readout">—</div>'
        '<span class="semester-hint">左右滑动查看全部月份</span>'
        '<div class="semester-legend">'
        '<span><i class="sw-hol"></i>放假</span>'
        '<span><i class="sw-exam"></i>停课考试</span>'
        '<span><i class="sw-mid"></i>期中</span>'
        '<span><i class="sw-make"></i>补课</span>'
        '<span><i class="sw-we"></i>周末</span>'
        '<span><i class="sw-today"></i>今天</span>'
        "</div></div></div>"
    )


def build_events() -> str:
    rows = []
    for start, end, title, note in DATA["events"]:
        s = d(start)
        if end:
            e = d(end)
            date = f'{short(s)}<span class="dash">–</span>{short(e)}'
        else:
            date = f'{short(s)}<span class="wd">周{WEEKDAY_CN[s.weekday()]}</span>'
        n = f'<span class="note">{note}</span>' if note else ""
        rows.append(f"<li><time>{date}</time><p><b>{title}</b>{n}</p></li>")
    return f'<ul class="semester-events">{"".join(rows)}</ul>'


def build_lookup() -> str:
    rows = []
    for w in weeks():
        n = w["n"]
        note, kind = WEEK_NOTES.get(n, ("", ""))
        chip = f'<em class="tag-{kind}">{note}</em>' if note else ""
        rows.append(
            f'<tr data-row-week="{n}"><td>{n}</td>'
            f'<td>{short(w["start"])} — {short(w["end"])}</td><td>{chip}</td></tr>'
        )
    total = DATA["weeks_total"]
    return (
        '<details class="semester-lookup">'
        f"<summary>周次速查表<span>{total} 周，含考试周</span></summary>"
        "<table><thead><tr><th>周次</th><th>日期（周一 — 周日）</th><th>备注</th></tr></thead>"
        f'<tbody>{"".join(rows)}</tbody></table>'
        "</details>"
    )


def build_official() -> str:
    rel = "assets/semester/calendar-2026-2027-1.jpg"
    path = Path(__file__).resolve().parents[1] / "docs" / rel
    if path.exists():
        return (
            '<figure class="semester-figure">'
            f'<img src="../{rel}" alt="浙大城市学院 {DATA["academic_year"]} 学年校历原图" loading="lazy">'
            "<figcaption>教务处发布的校历原图（含作息时间表）</figcaption>"
            "</figure>"
        )
    return (
        '<p class="semester-todo">学校发布的校历原图还没补。把教务处的校历长图存成 '
        f"<code>docs/{rel}</code>（文件名别改）后重跑 "
        "<code>python scripts/gen_semester_schedule.py</code>，这里会自动换成图片。</p>"
    )


def build() -> str:
    lines: list[str] = []
    a = lines.append

    ws = d(DATA["weeks_start"])
    exam_s, exam_e = d(DATA["exam_start"]), d(DATA["exam_end"])
    teach_weeks = DATA["weeks_total"] - 2

    a("<!-- 本文件由 scripts/gen_semester_schedule.py 生成，改数据请改脚本后重跑 -->")
    a("")
    a("# 学期安排")
    a("")
    a(
        f"这一页把 {DATA['academic_year']} 学年{DATA['term']}的周次、假期和考试放在一起："
        "报到和军训什么时候结束、哪天正式上课、什么时候期中、考试周几号到几号、寒假从哪天开始。"
        "想知道某个日期是第几周，看中间的校历网格；想知道这学期还剩什么，看关键节点。"
    )
    a("")
    a(
        "> 日期来源为学校发布的学年校历，节假日调休以教务处的具体通知为准。"
        "如果这里和你的课表、学院通知对不上，以教务处和学院的通知为准。"
    )
    a("")

    # ---- 01 概览 ----
    a("## 学期概览 {: .sp-h2 }")
    a("")
    a(build_stats())
    a("")

    # ---- 02 进度 ----
    a("## 学期进度 {: .sp-h2 }")
    a("")
    a(build_rail())
    a("")

    # ---- 03 网格 ----
    a("## 校历网格 {: .sp-h2 }")
    a("")
    a(
        "每周一列、周一到周日为行，按整月排到 9/1—1/31；格子里的小字是当天的安排，"
        "底色只说明那天上不上课。"
    )
    a("")
    a(build_calendar())
    a("")

    # ---- 04 关键节点 ----
    a("## 关键节点 {: .sp-h2 }")
    a("")
    a(build_events())
    a("")

    # ---- 05 周次速查 ----
    a("## 周次速查 {: .sp-h2 }")
    a("")
    a(
        f"第 1 周从 {fmt(ws)}（星期一）算起，每周一到周日。"
        f"第 {teach_weeks} 周之后是考试周（{short(exam_s)}—{short(exam_e)}）。"
    )
    a("")
    a(build_lookup())
    a("")

    # ---- 学期节奏（原样保留） ----
    a("## 一学期大致怎么过 {: .sp-h2 .is-plain }")
    a("")
    a("| 阶段 | 时间 | 该做什么 |")
    a("| --- | --- | --- |")
    a(
        f"| 开课前的准备 | {short(d('2026-08-28'))} 前后 | 查课表、确认宿舍和缴费、把教材和证件备齐；新生按学院安排参加始业教育和军训。 |"
    )
    a(
        "| 前半学期 | 第 1—8 周 | 课程密度最大的时候，先跟上作业节奏；需要退课、改选的，注意教务处的选课窗口。 |"
    )
    a(
        f"| 期中 | 第 9 周（{short(d('2026-11-09'))}—{short(d('2026-11-15'))}） | 期中考试不停课，考试和正常上课会叠在一起，提前把复习塞进周末。 |"
    )
    a(
        f"| 后半学期 | 第 10—{teach_weeks} 周 | 大作业和课程设计集中交付；寒假前的实习、竞赛报名也在这段时间截止。 |"
    )
    a(
        f"| 考试周 | {short(exam_s)}—{short(exam_e)} | 全校停课考试，按考试安排表逐门确认时间地点，别只看课表。 |"
    )
    a(
        f"| 寒假 | {short(d(DATA['winter_break']))} 起 | 成绩一般在本学期结束后陆续出，补考安排看教务处通知。 |"
    )
    a("")

    # ---- 维护说明（原样保留） ----
    a("## 这一页怎么维护 {: .sp-h2 .is-plain }")
    a("")
    a("- 所有日期写在 `scripts/gen_semester_schedule.py` 顶部的 `DATA` 里，改完运行 `python scripts/gen_semester_schedule.py` 重新生成本页；")
    a("- 新增节点就往 `events` 里加一行 `(开始日期, 结束日期或 None, 事项, 说明)`，关键节点和周次速查会一起更新；格子里的短标签在 `MARKS` 里加一行 `(开始日期, 结束日期或 None, 标签, 类型)`；")
    a("- 下一学年开学后，把 `DATA` 换成新学年数据即可，页面结构不用动。")
    a("")
    a(build_official())
    a("")
    return "\n".join(lines)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "semester.md"
    target.write_text(build(), encoding="utf-8")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
