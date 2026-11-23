#!/usr/bin/env python3
"""生成 docs/semester.md 的学期安排正文。

所有日期数据集中在 DATA 里，改日期只改这一处，重新运行本脚本即可：

    python scripts/gen_semester_schedule.py

数据来源：浙大城市学院 2026—2027 学年校历（第一学期 / 秋冬学期）。
官方原文由学校公众号发布，本页只做搬运与整理；日期以教务处最新通知为准。
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

# SVG 里用的颜色（与 palette.css 同族，但写死，保证图片单独打开也正确）
C_BG = "#ffffff"
C_FRAME = "#f7f8fb"
C_LINE = "#e6eaf2"
C_TEXT = "#15171f"
C_MUTED = "#5b6272"
C_DIM = "#6e7587"
C_ACCENT = "#3f6fe4"
C_ACCENT_SOFT = "#eaefff"
C_WARN = "#a8760a"
C_WARN_SOFT = "#fdf3dc"
C_WEEKEND = "#f2f4f9"


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


def day_marks() -> dict[dt.date, tuple[str, str]]:
    """日期 -> (短标签, 类型)。类型：holiday / make / exam / break / event"""
    marks: dict[dt.date, tuple[str, str]] = {}
    for start, end, title, _note in DATA["events"]:
        s = d(start)
        e = d(end) if end else s
        if "军训" in title or "报到" in title:
            label, kind = "军训", "event"
        elif "中秋" in title:
            label, kind = "中秋", "holiday"
        elif "国庆" in title:
            label, kind = "国庆", "holiday"
        elif "元旦" in title:
            label, kind = "元旦", "holiday"
        elif "运动会" in title:
            label, kind = "运动会", "event"
        elif "期中" in title:
            label, kind = "期中", "exam"
        elif "停课考试" in title:
            label, kind = "考试", "exam"
        elif "寒假" in title:
            label, kind = "寒假", "break"
        elif "上双周" in title or "上单周" in title:
            label, kind = "补课", "make"
        else:
            continue
        cur = s
        while cur <= e:
            marks[cur] = (label, kind)
            cur += dt.timedelta(days=1)
    return marks


def build_svg() -> str:
    """把校历画成 SVG：横轴 19 个教学周，纵轴周一到周日。"""
    cell_w, cell_h = 54, 38
    lab_w, month_h, head_h = 78, 24, 30
    n = DATA["weeks_total"]
    width = lab_w + n * cell_w
    height = month_h + head_h + 7 * cell_h + 30
    start = d(DATA["weeks_start"])
    marks = day_marks()
    exam_s, exam_e = d(DATA["exam_start"]), d(DATA["exam_end"])

    out: list[str] = []
    add = out.append
    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Segoe UI, PingFang SC, Microsoft YaHei, sans-serif">'
    )
    add(f'<rect width="{width}" height="{height}" fill="{C_BG}"/>')
    add(
        f'<text x="12" y="16" font-size="11" fill="{C_MUTED}" letter-spacing="1">'
        f'浙大城市学院 {DATA["academic_year"]} 学年{DATA["term"]} · 第 1—{n} 周</text>'
    )

    # 月份分组
    monday_months = []
    for i in range(n):
        ws = start + dt.timedelta(weeks=i)
        monday_months.append(ws.month)
    group_start = 0
    for i in range(1, n + 1):
        if i == n or monday_months[i] != monday_months[group_start]:
            x = lab_w + group_start * cell_w
            w = (i - group_start) * cell_w
            year = (start + dt.timedelta(weeks=group_start)).year
            add(
                f'<text x="{x + w / 2:.1f}" y="19" font-size="11" fill="{C_DIM}" '
                f'text-anchor="middle">{year} 年 {monday_months[group_start]} 月</text>'
            )
            if group_start:
                add(
                    f'<line x1="{x}" y1="4" x2="{x}" y2="{month_h - 4}" '
                    f'stroke="{C_LINE}" stroke-width="1"/>'
                )
            group_start = i

    top = month_h
    # 周次表头
    add(
        f'<rect x="{lab_w}" y="{top}" width="{n * cell_w}" height="{head_h}" fill="{C_FRAME}"/>'
    )
    for i in range(n):
        x = lab_w + i * cell_w
        add(
            f'<text x="{x + cell_w / 2:.1f}" y="{top + head_h / 2 + 4:.1f}" font-size="11" '
            f'fill="{C_MUTED}" text-anchor="middle">{i + 1}</text>'
        )
    add(
        f'<text x="{lab_w - 10}" y="{top + head_h / 2 + 4:.1f}" font-size="10" fill="{C_DIM}" '
        f'text-anchor="end">周次</text>'
    )

    body_top = top + head_h
    for row, wd in enumerate("一二三四五六日"):
        y = body_top + row * cell_h
        add(
            f'<text x="{lab_w - 10}" y="{y + cell_h / 2 + 4:.1f}" font-size="11" fill="{C_MUTED}" '
            f'text-anchor="end">周{WEEKDAY_CN[row]}</text>'
        )
        for i in range(n):
            x = lab_w + i * cell_w
            day = start + dt.timedelta(weeks=i, days=row)
            label, kind = marks.get(day, ("", ""))
            fill = C_BG
            if kind in ("holiday", "break"):
                fill = C_ACCENT_SOFT
            elif kind == "exam":
                fill = C_WARN_SOFT
            elif row >= 5:
                fill = C_WEEKEND
            add(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="{fill}" '
                f'stroke="{C_LINE}" stroke-width="1"/>'
            )
            add(
                f'<text x="{x + cell_w / 2:.1f}" y="{y + 15:.1f}" font-size="10.5" fill="{C_TEXT}" '
                f'text-anchor="middle">{day.day}</text>'
            )
            if label:
                color = C_WARN if kind in ("exam", "make") else C_ACCENT
                add(
                    f'<text x="{x + cell_w / 2:.1f}" y="{y + 29:.1f}" font-size="9" fill="{color}" '
                    f'text-anchor="middle">{label}</text>'
                )

    # 图例
    ly = body_top + 7 * cell_h + 20
    items = [
        (C_ACCENT_SOFT, C_ACCENT, "放假 / 寒假"),
        (C_WARN_SOFT, C_WARN, f"考试（{short(exam_s)}—{short(exam_e)}）"),
        (C_WEEKEND, C_MUTED, "周末"),
    ]
    lx = lab_w
    for fill, color, text in items:
        add(f'<rect x="{lx}" y="{ly - 9}" width="12" height="12" fill="{fill}" stroke="{C_LINE}"/>')
        add(f'<text x="{lx + 18}" y="{ly + 1}" font-size="10" fill="{color}">{text}</text>')
        lx += 24 + len(text) * 10

    add("</svg>")
    return "\n".join(out)


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
        f"这一页把 {DATA['academic_year']} 学年{DATA['term']}的关键时间点、周次对照和校历原图"
        "放在一起：报到和军训什么时候结束、哪天正式上课、什么时候期中、考试周几号到几号、"
        "寒假从哪天开始——需要快速查某个日期属于第几周，看中间那张周次表就行。"
    )
    a("")
    a(
        "> 日期来源为学校发布的学年校历，节假日调休以教务处的具体通知为准。"
        "如果这里和你的课表、学院通知对不上，以教务处和学院的通知为准。"
    )
    a("")

    # ---- 概览卡片 ----
    a("## 一眼看懂")
    a("")
    a('<div class="semester-cards" markdown>')
    a("")
    a(f'<div class="semester-card">')
    a(f'<span class="semester-card__label">学期起止</span>')
    a(f'<span class="semester-card__value">{short(ws)} — {short(exam_e)}</span>')
    a(f'<span class="semester-card__hint">共 {DATA["weeks_total"]} 周，含考试周</span>')
    a("</div>")
    a("")
    a(f'<div class="semester-card">')
    a(f'<span class="semester-card__label">正式上课</span>')
    a(f'<span class="semester-card__value">{short(ws)}</span>')
    a(f'<span class="semester-card__hint">第 1 周星期一</span>')
    a("</div>")
    a("")
    a(f'<div class="semester-card">')
    a(f'<span class="semester-card__label">教学 / 考试</span>')
    a(f'<span class="semester-card__value">{teach_weeks} + 2 周</span>')
    a(f'<span class="semester-card__hint">前 {teach_weeks} 周上课，最后 2 周停课考试</span>')
    a("</div>")
    a("")
    a(f'<div class="semester-card">')
    a(f'<span class="semester-card__label">寒假开始</span>')
    a(f'<span class="semester-card__value">{short(d(DATA["winter_break"]))}</span>')
    a(f'<span class="semester-card__hint">春节 {fmt(d("2027-02-06")).replace(" ", "")}</span>')
    a("</div>")
    a("")
    a("</div>")
    a("")

    # ---- 当前进度 ----
    a("## 现在第几周")
    a("")
    a(
        f'<div class="semester-progress" data-weeks-start="{DATA["weeks_start"]}" '
        f'data-weeks-total="{DATA["weeks_total"]}" data-exam-start="{DATA["exam_start"]}" '
        f'data-winter-break="{DATA["winter_break"]}">'
    )
    a('<span>本周是第 <b class="sp-week">—</b> 周</span>')
    a('<span>距考试周开始还有 <b class="sp-exam">—</b> 天</span>')
    a('<span>距寒假还有 <b class="sp-break">—</b> 天</span>')
    a("</div>")
    a("")
    a("（上面三个数字由浏览器按本机日期算，学期结束后会显示为已结束。）")
    a("")

    # ---- 关键节点 ----
    a("## 关键节点")
    a("")
    a("| 日期 | 事项 | 说明 |")
    a("| --- | --- | --- |")
    for start, end, title, note in DATA["events"]:
        a(f"| {span(start, end)} | {title} | {note or '—'} |")
    a("")

    # ---- 周次表 ----
    a("## 周次对照表")
    a("")
    a(
        f"第 1 周从 {fmt(ws)}（星期一）算起，每周一到周日。"
        f"第 {teach_weeks} 周之后是考试周（{short(exam_s)}—{short(exam_e)}）。"
    )
    a("")
    a("| 周次 | 开始 | 结束 | 备注 |")
    a("| --- | --- | --- | --- |")
    for w in weeks():
        a(
            f"| 第 {w['n']} 周 | {fmt(w['start'])} | {fmt(w['end'])} | {w['note'] or '—'} |"
        )
    a("")

    # ---- 校历图 ----
    a("## 校历图")
    a("")
    a(
        "下面这张是按本页数据画出来的：横轴是教学周，纵轴是周一到周日，"
        "放假的格子、考试周的格子都自带底色，比翻长图快。"
    )
    a("")
    a('<figure class="semester-figure">')
    a(
        '  <img src="../assets/semester/calendar-2026-2027-1.svg" '
        'alt="浙大城市学院 2026—2027 学年第一学期校历（教学周网格）" loading="lazy">'
    )
    a("  <figcaption>2026—2027 学年第一学期教学周网格（由 scripts/gen_semester_schedule.py 生成）</figcaption>")
    a("</figure>")
    a("")

    official_rel = "assets/semester/calendar-2026-2027-1.jpg"
    official_path = Path(__file__).resolve().parents[1] / "docs" / official_rel
    a("### 学校发布的原图")
    a("")
    if official_path.exists():
        a('<figure class="semester-figure">')
        a(
            f'  <img src="../{official_rel}" '
            'alt="浙大城市学院 2026—2027 学年第一学期校历原图" loading="lazy">'
        )
        a("  <figcaption>教务处发布的校历原图（含作息时间表）</figcaption>")
        a("</figure>")
    else:
        a('<figure class="semester-figure semester-figure--empty">')
        a("  <b>原图待补。</b>")
        a(
            f"  把教务处的校历长图存成 <code>docs/{official_rel}</code>"
            "（文件名别改）后重跑 <code>python scripts/gen_semester_schedule.py</code>，"
            "这里会自动换成图片。"
        )
        a("</figure>")
    a("")

    # ---- 节奏建议 ----
    a("## 一学期大致怎么过")
    a("")
    a("| 阶段 | 时间 | 该做什么 |")
    a("| --- | --- | --- |")
    a(
        f"| 开课前的准备 | {short(d('2026-08-28'))} 前后 | 查课表、确认宿舍和缴费、把教材和证件备齐；新生按学院安排参加始业教育和军训。 |"
    )
    a(
        f"| 前半学期 | 第 1—8 周 | 课程密度最大的时候，先跟上作业节奏；需要退课、改选的，注意教务处的选课窗口。 |"
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

    # ---- 维护说明 ----
    a("## 这一页怎么维护")
    a("")
    a("- 所有日期写在 `scripts/gen_semester_schedule.py` 顶部的 `DATA` 里，改完运行 `python scripts/gen_semester_schedule.py` 重新生成本页；")
    a("- 新增节点就往 `events` 里加一行 `(开始日期, 结束日期或 None, 事项, 说明)`，周次表和「关键节点」会一起更新；")
    a("- 下一学年开学后，把 `DATA` 换成新学年数据即可，页面结构不用动。")
    a("")
    return "\n".join(lines)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    target = root / "docs" / "semester.md"
    target.write_text(build(), encoding="utf-8")
    print(f"wrote {target} ({target.stat().st_size} bytes)")

    svg = root / "docs" / "assets" / "semester" / "calendar-2026-2027-1.svg"
    svg.parent.mkdir(parents=True, exist_ok=True)
    svg.write_text(build_svg(), encoding="utf-8")
    print(f"wrote {svg} ({svg.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
