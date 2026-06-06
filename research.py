#!/usr/bin/env python3
"""research.py — 深度研究「子模块」管理 + 统一首页渲染。

与 generate_report.py（每日观察）解耦：本模块独立计算路径，被
generate_report.py 与 publish_research.py 共同调用，确保每日 cron
重写 index.html 时不会覆盖「深度研究」板块。
"""
from __future__ import annotations
import json, re, shutil, html as _html
from datetime import datetime
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
RESEARCH_DIR = DOCS_DIR / "research"
RESEARCH_JSON = DOCS_DIR / "research.json"
FEED_JSON = DOCS_DIR / "feed.json"

SITE_NAME = "美股投研"


def _esc(s) -> str:
    return _html.escape(str(s if s is not None else ""), quote=True)


def slugify(text: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", (text or "").strip().lower()).strip("-")
    return s or datetime.now().strftime("r%Y%m%d%H%M%S")


def _load(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"entries": [], "last_updated": ""}


def load_research() -> dict:
    return _load(RESEARCH_JSON)


def load_feed() -> dict:
    return _load(FEED_JSON)


def save_research(data: dict) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    RESEARCH_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                             encoding="utf-8")


def add_research(src, slug=None, title=None, date=None, tags=None,
                 tickers=None, teaser=None, cover=None) -> dict:
    src = Path(src).expanduser()
    if not src.is_file():
        raise FileNotFoundError(src)
    text = src.read_text(encoding="utf-8", errors="ignore")
    if not title:
        m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
        title = (m.group(1).strip() if m else src.stem)
    if not slug:
        slug = slugify(title if re.search(r"[A-Za-z0-9]", title) else src.stem)
    if not date:
        date = datetime.fromtimestamp(src.stat().st_mtime).strftime("%Y-%m-%d")
    tags = list(tags or [])
    tickers = list(tickers or [])
    if not teaser:
        m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
                      text, re.I | re.S)
        if m:
            teaser = re.sub(r"\s+", " ", m.group(1)).strip()[:90]
        else:
            m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
            teaser = re.sub(r"<[^>]+>", "", m.group(1)).strip()[:90] if m else ""
    dest = RESEARCH_DIR / slug
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest / "index.html")
    cover_name = None
    if cover:
        cp = Path(cover).expanduser()
        if cp.is_file():
            cover_name = cp.name
            shutil.copyfile(cp, dest / cover_name)
    entry = {"slug": slug, "title": title, "date": date, "tags": tags,
             "tickers": tickers, "teaser": teaser, "cover": cover_name,
             "path": f"research/{slug}/index.html",
             "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    data = load_research()
    data["entries"] = [e for e in data.get("entries", []) if e.get("slug") != slug]
    data["entries"].append(entry)
    data["entries"].sort(key=lambda e: e.get("date", ""), reverse=True)
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_research(data)
    (dest / "meta.json").write_text(json.dumps(entry, ensure_ascii=False, indent=2),
                                    encoding="utf-8")
    return entry


def _research_cards(research: dict) -> str:
    cards = []
    for e in research.get("entries", []):
        tags = "".join(f'<span class="tag">{_esc(t)}</span>'
                       for t in (e.get("tags") or [])[:5])
        tks = " ".join(f"${_esc(t)}" for t in (e.get("tickers") or [])[:6])
        meta = " · ".join(x for x in [_esc(e.get("date", "")), tks] if x)
        cards.append(
            f'<a class="rcard" href="{_esc(e.get("path"))}">'
            f'<div class="rtitle">{_esc(e.get("title"))}</div>'
            f'<div class="rmeta">{meta}</div>'
            f'<div class="rteaser">{_esc(e.get("teaser"))}</div>'
            f'<div class="rtags">{tags}</div></a>')
    return "".join(cards)


def _daily_items(feed: dict) -> str:
    items = []
    for e in feed.get("entries", []):
        tks = " ".join(t for t, _ in (e.get("tickers") or [])[:6])
        path = e.get("report_path") or f'reports/{e.get("date")}.html'
        items.append(
            f'<li><a class="d" href="{_esc(path)}">{_esc(e.get("date"))}</a>'
            f'<div class="t">{_esc(e.get("teaser", ""))}</div>'
            f'<div class="s">{e.get("unique_tweets", 0)} 条高赞 · {_esc(tks)}</div></li>')
    return "".join(items)


def render_home(feed: Optional[dict] = None) -> None:
    feed = feed if feed is not None else load_feed()
    research = load_research()
    cards = _research_cards(research)
    items = _daily_items(feed)
    last = feed.get("last_updated", "")
    research_section = (
        f'<section class="block"><h2 class="sec">深度研究</h2>'
        f'<div class="rgrid">{cards}</div></section>') if cards else ""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "index.html").write_text(f"""<!doctype html>
<html lang="zh-Hans"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(SITE_NAME)}</title>
<link rel="stylesheet" href="assets/style.css">
</head><body>
<header class="site-header"><b>{_esc(SITE_NAME)}</b></header>
<main class="home">
  <p class="lede">美股 / 半导体 / AI 基建投研：每日抓取 X 高赞讨论的「观察日报」，
   以及不定期产出的「深度研究」。仅供研究，非投资建议。</p>
  {research_section}
  <section class="block"><h2 class="sec">每日观察</h2>
  <p class="sub">每天北京时间约 12:00 自动更新。最后更新：{_esc(last)}</p>
  <ul class="archive">{items or '<li>暂无数据</li>'}</ul></section>
  <footer>grok 原生 X 检索 · 仅供研究，非投资建议</footer>
</main></body></html>""", encoding="utf-8")


if __name__ == "__main__":
    render_home()
    print("已重渲染 docs/index.html")
