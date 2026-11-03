"""Resolve paper PDF URLs and render page-one JPEG thumbnails."""
from __future__ import annotations

import os
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THUMB_DIR = ROOT / "docs" / "assets" / "paper-thumbs"
THUMB_WIDTH = 600
THUMB_ASPECT = 424 / 300
USER_AGENT = "HZCU-student-handbook/1.0 (paper thumb capture; academic mirror)"

ARXIV_ABS = re.compile(
    r"https?://(?:www\.)?arxiv\.org/abs/([\d.]+(?:v\d+)?)", re.I
)
ARXIV_PDF = re.compile(
    r"https?://(?:www\.)?arxiv\.org/pdf/([\d.]+(?:v\d+)?)", re.I
)
NATURE_ART = re.compile(
    r"https?://(?:www\.)?nature\.com/articles/([a-z0-9-]+)", re.I
)
SCIENCE_DOI = re.compile(
    r"https?://(?:www\.)?science\.org/doi/(10\.\d+/science\.[a-z0-9]+)", re.I
)
PNAS_DOI = re.compile(
    r"https?://(?:www\.)?pnas\.org/doi/(10\.\d+/pnas\.[\d.]+)", re.I
)
OPENREVIEW = re.compile(
    r"https?://openreview\.net/(?:forum|pdf)\?id=([^&\s\"]+)", re.I
)
ACL_ANTH = re.compile(
    r"https?://aclanthology\.org/([\d.]+(?:\.\d+)?(?:\.\d+)?)", re.I
)


MANUAL_PDF: dict[str, str] = {
    "WB-A11": "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf",
}


def _load_evidence() -> dict:
    import ast

    src = (ROOT / "scripts" / "expand_papers_from_workbook.py").read_text(encoding="utf-8")
    m = re.search(r"^evidence = (\{.*?\n\})\nhooks=", src, re.M | re.S)
    if not m:
        return {}
    return ast.literal_eval(m.group(1))


_EVIDENCE: dict | None = None


def pdf_from_evidence(zh: str) -> str | None:
    global _EVIDENCE
    if _EVIDENCE is None:
        _EVIDENCE = _load_evidence()
    if not zh or zh not in _EVIDENCE:
        return None
    link = _EVIDENCE[zh][0]
    return resolve_pdf_url(link)


def resolve_pdf_for_paper(paper: dict) -> str | None:
    pid = paper.get("id") or ""
    if pid in MANUAL_PDF:
        return MANUAL_PDF[pid]
    url = resolve_pdf_url(paper.get("link") or "")
    if url:
        return url
    return pdf_from_evidence(paper.get("zh") or "")


def resolve_pdf_url(link: str) -> str | None:
    """Best-effort PDF URL for a paper landing page."""
    link = (link or "").strip()
    if not link:
        return None
    if link.lower().endswith(".pdf"):
        return link

    m = ARXIV_PDF.search(link)
    if m:
        return f"https://arxiv.org/pdf/{m.group(1)}.pdf"
    m = ARXIV_ABS.search(link)
    if m:
        return f"https://arxiv.org/pdf/{m.group(1)}.pdf"

    m = NATURE_ART.search(link)
    if m:
        return f"https://www.nature.com/articles/{m.group(1)}.pdf"

    m = SCIENCE_DOI.search(link)
    if m:
        return f"https://www.science.org/doi/pdf/{m.group(1)}?download=true"

    m = PNAS_DOI.search(link)
    if m:
        return f"https://www.pnas.org/doi/pdf/{m.group(1)}"

    m = OPENREVIEW.search(link)
    if m:
        return f"https://openreview.net/pdf?id={m.group(1)}"

    m = ACL_ANTH.search(link)
    if m:
        slug = m.group(1).rstrip("/")
        if not slug.endswith(".pdf"):
            slug += ".pdf"
        return f"https://aclanthology.org/{slug}"

    if "doi.org/" in link.lower():
        return None

    return None


def fetch_bytes(url: str, timeout: float = 90.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if proxy:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": proxy, "https": proxy})
        )
        resp = opener.open(req, timeout=timeout)
    else:
        resp = urllib.request.urlopen(req, timeout=timeout)
    with resp:
        data = resp.read()
    if not data.startswith(b"%PDF"):
        raise ValueError("response is not a PDF")
    return data


def render_first_page_jpeg(pdf_bytes: bytes, quality: int = 82) -> bytes:
    import pymupdf

    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    try:
        page = doc[0]
        page_w = page.rect.width
        clip_h = min(page.rect.height, page_w * THUMB_ASPECT)
        clip = pymupdf.Rect(
            page.rect.x0, page.rect.y0, page.rect.x0 + page_w, page.rect.y0 + clip_h
        )
        zoom = THUMB_WIDTH / page_w
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
        return pix.tobytes("jpeg", jpg_quality=quality)
    finally:
        doc.close()


def thumb_path(paper_id: str) -> Path:
    return THUMB_DIR / f"{paper_id}.jpg"


def thumb_src(paper_id: str) -> str:
    return f"../assets/paper-thumbs/{paper_id}.jpg"
