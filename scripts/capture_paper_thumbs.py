"""Download paper PDFs and save first-page JPEG thumbnails under docs/assets/paper-thumbs/."""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
PAGE = ROOT / "docs" / "papers.md"
PROGRESS = ROOT / "scripts" / ".paper_thumb_progress.json"
JSON_RE = re.compile(
    r'(<script id="papers-json" type="application/json">)(.*?)(</script>)', re.S
)

from paper_thumb_utils import (  # noqa: E402
    THUMB_DIR,
    fetch_bytes,
    render_first_page_jpeg,
    resolve_pdf_for_paper,
    thumb_path,
)


CARD_INLINE_RE = re.compile(
    r'<article class="card" data-id="(?P<id>[^"]+)".*?</article>', re.S
)


def inline_shotimg_ids(page_text: str) -> set[str]:
    ids: set[str] = set()
    for m in CARD_INLINE_RE.finditer(page_text):
        chunk = m.group(0)
        if "shotimg" in chunk and "data:image" in chunk:
            ids.add(m.group("id"))
    return ids


def load_papers() -> list[dict]:
    text = PAGE.read_text(encoding="utf-8")
    m = JSON_RE.search(text)
    if not m:
        raise SystemExit("papers-json not found")
    return json.loads(m.group(2)), text


def load_progress() -> dict:
    if PROGRESS.is_file():
        return json.loads(PROGRESS.read_text(encoding="utf-8"))
    return {"ok": {}, "fail": {}}


def save_progress(state: dict) -> None:
    PROGRESS.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def capture_one(paper: dict, force: bool) -> tuple[str, str | None]:
    pid = paper["id"]
    out = thumb_path(pid)
    if out.is_file() and not force:
        return "skip", "exists"
    pdf_url = resolve_pdf_for_paper(paper)
    if not pdf_url:
        return "fail", f"no PDF URL for link={paper.get('link')!r}"
    try:
        pdf = fetch_bytes(pdf_url)
        jpeg = render_first_page_jpeg(pdf)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
        return "fail", str(e)
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    out.write_bytes(jpeg)
    return "ok", pdf_url


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", action="append", help="only these WB ids")
    parser.add_argument("--limit", type=int, default=0, help="max captures this run")
    parser.add_argument("--force", action="store_true", help="overwrite existing JPEG")
    parser.add_argument("--sleep", type=float, default=1.2, help="seconds between downloads")
    parser.add_argument(
        "--skip-inline",
        action="store_true",
        default=True,
        help="skip papers that already have inline base64 shotimg (default: true)",
    )
    parser.add_argument(
        "--include-inline",
        action="store_true",
        help="also re-capture papers with inline shotimg",
    )
    args = parser.parse_args()
    skip_inline = args.skip_inline and not args.include_inline

    papers, page_text = load_papers()
    inline_ids = inline_shotimg_ids(page_text) if skip_inline else set()
    if args.id:
        want = set(args.id)
        papers = [p for p in papers if p["id"] in want]
    state = load_progress()
    stats = {"ok": 0, "skip": 0, "fail": 0}
    done = 0

    for paper in papers:
        if args.limit and done >= args.limit:
            break
        pid = paper["id"]
        if skip_inline and pid in inline_ids:
            stats["skip"] += 1
            continue
        status, detail = capture_one(paper, args.force)
        stats[status] += 1
        if status == "ok":
            state["ok"][pid] = detail
            state["fail"].pop(pid, None)
            done += 1
            print(f"OK {pid} <- {detail}")
        elif status == "skip":
            print(f"SKIP {pid} ({detail})")
        else:
            state["fail"][pid] = detail
            print(f"FAIL {pid}: {detail}", file=sys.stderr)
        save_progress(state)
        if status == "ok" and args.sleep:
            time.sleep(args.sleep)

    print(
        f"done: ok={stats['ok']} skip={stats['skip']} fail={stats['fail']}; "
        f"thumbs dir={THUMB_DIR}"
    )


if __name__ == "__main__":
    main()
