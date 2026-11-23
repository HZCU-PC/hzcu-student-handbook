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


def build() -> str:
    ws = d(DATA["weeks_start"])
    exam_s, exam_e = d(DATA["exam_start"]), d(DATA["exam_end"])
    teach_weeks = DATA["weeks_total"] - 2
    lines: list[str] = []
    a = lines.append

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

    # ---- 校历原图 ----
    a("## 校历原图")
    a("")
    a(
        "学校发的校历长图（含作息时间表）体积大、字小，手机上不好看清，"
        "所以这里用上面的表格做常规查询；要对照原图时看下面这张。"
    )
    a("")
    img_rel = "assets/semester/calendar-2026-2027-1.jpg"
    img_path = Path(__file__).resolve().parents[1] / "docs" / img_rel
    if img_path.exists():
        a('<figure class="semester-figure">')
        a(
            f'  <img src="../{img_rel}" '
            'alt="浙大城市学院 2026—2027 学年第一学期校历" loading="lazy">'
        )
        a("  <figcaption>浙大城市学院 2026—2027 学年第一学期校历</figcaption>")
        a("</figure>")
    else:
        a('<figure class="semester-figure semester-figure--empty">')
        a("  <b>校历原图待补。</b>")
        a(
            f"  把校历长图存为 <code>docs/{img_rel}</code> 后重新运行 "
            "<code>python scripts/gen_semester_schedule.py</code>，这里会自动换成图片；"
            "图片缺失时页面只显示这一块说明，不影响其余内容。"
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


if __name__ == "__main__":
    main()
