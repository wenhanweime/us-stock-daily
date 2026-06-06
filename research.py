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
MONITOR_JSON = DOCS_DIR / "monitor.json"

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


def load_monitor() -> dict:
    """关键词监控状态（由 monitor.py 写 docs/monitor.json）；缺失安全降级。"""
    if MONITOR_JSON.exists():
        try:
            return json.loads(MONITOR_JSON.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


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
    rentries = research.get("entries", [])
    dentries = feed.get("entries", [])
    last = (feed.get("last_updated", "") or "")[:10]

    # 侧栏：深度研究导航
    rnav = []
    for i, e in enumerate(rentries):
        rnav.append('<a class="nav-link" href="#r-%s"><span>%02d</span>'
                    '<strong>%s</strong></a>'
                    % (_esc(e.get("slug")), i + 1, _esc(e.get("title"))))
    rnav_html = "".join(rnav) or '<p class="nav-group-title">暂无</p>'

    # 深度研究卡片
    rcards = []
    for e in rentries:
        tks = " ".join("$" + t for t in (e.get("tickers") or [])[:4])
        badges = "".join('<span class="badge">%s</span>' % _esc(t)
                         for t in (e.get("tags") or [])[:5])
        rcards.append(
            '<article class="player-card filter-item" id="r-%s">'
            '<header><h3><a href="%s">%s</a></h3>'
            '<span class="ticker">%s</span></header>'
            '<p class="muted" style="margin:0 0 10px;font-size:13px;line-height:1.55">%s</p>'
            '<div class="tag-row">%s<span class="badge accent">%s</span></div>'
            '</article>'
            % (_esc(e.get("slug")), _esc(e.get("path")), _esc(e.get("title")),
               _esc(tks), _esc(e.get("teaser")), badges, _esc(e.get("date"))))
    rcards_html = "".join(rcards) or '<p class="empty-state visible">暂无深度研究。</p>'

    # 每日观察 chips
    dchips = []
    for e in dentries:
        path = e.get("report_path") or ("reports/%s.html" % e.get("date"))
        tks = " ".join(t for t, _ in (e.get("tickers") or [])[:5])
        dchips.append(
            '<a class="doc-chip filter-item" href="%s">'
            '<span>%s · %s 高赞</span><strong>%s</strong></a>'
            % (_esc(path), _esc(e.get("date")), e.get("unique_tweets", 0),
               _esc(e.get("teaser", "") or tks)))
    dchips_html = "".join(dchips) or '<p class="empty-state visible">暂无日报。</p>'

    # 关键词监控（第三条线）
    mon = load_monitor()
    mon_buckets = mon.get("buckets", [])
    mon_kw = mon.get("keywords", len(mon_buckets))
    mon_spiked = mon.get("spiked", [])
    mon_updated = ("最后更新 %s。" % _esc(mon.get("last_updated"))) if mon.get("last_updated") else ""
    if mon_buckets:
        mchips = []
        for b in mon_buckets:
            flag = " 🔺放量" if b.get("spike") else ""
            mchips.append(
                '<a class="doc-chip filter-item" href="monitor/index.html">'
                '<span>新增 %s · 采样 %s%s</span><strong>%s</strong></a>'
                % (b.get("new", 0), b.get("sampled", 0), flag, _esc(b.get("name"))))
        mon_chips_html = "".join(mchips)
    else:
        mon_chips_html = '<p class="empty-state visible">监控未启动。</p>'

    # 指标
    tickers_cov = len({t for e in rentries for t in (e.get("tickers") or [])})
    metrics = [(len(rentries), "深度研究"), (tickers_cov, "覆盖个股标的"),
               (len(dentries), "每日观察期数"), (mon_kw or "—", "监控关键词"),
               (len(mon_spiked) if mon_buckets else "—", "放量告警"),
               (last or "—", "最新更新")]
    metric_html = "".join(
        '<div class="metric"><strong>%s</strong><span>%s</span></div>'
        % (_esc(v), _esc(l)) for v, l in metrics)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "index.html").write_text(f"""<!doctype html>
<html lang="zh-Hans"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f6f4ef">
<title>{_esc(SITE_NAME)}</title>
<link rel="stylesheet" href="assets/theme.css">
</head><body>
<a class="skip-link" href="#main">跳到主内容</a>
<div class="app-shell">
  <aside class="sidebar" aria-label="导航">
    <div class="brand"><h1>{_esc(SITE_NAME)}</h1>
      <p>美股 · 半导体 · AI 基建 · 投资研究终端</p></div>
    <nav class="nav-group" aria-label="板块">
      <p class="nav-group-title">Sections</p>
      <a class="nav-link" href="#research"><span>RS</span><strong>深度研究</strong></a>
      <a class="nav-link" href="#daily"><span>DAY</span><strong>每日观察</strong></a>
      <a class="nav-link" href="#monitor"><span>MON</span><strong>关键词监控</strong></a>
    </nav>
    <nav class="nav-group" aria-label="深度研究">
      <p class="nav-group-title">Research</p>
      {rnav_html}
    </nav>
  </aside>
  <main class="main" id="main">
    <div class="topbar" role="search">
      <div class="search-wrap"><label for="searchInput">搜索研报 / 个股 / 主题</label>
        <div class="search-row">
          <input id="searchInput" type="search" autocomplete="off" placeholder="例如 硅光、HBM、MU、CPO…" aria-describedby="rowCount">
          <span class="badge" id="rowCount" aria-live="polite">—</span>
        </div></div>
      <div class="tool-buttons">
        <button type="button" id="resetSearch">重置</button>
        <a class="source-link" href="https://github.com/wenhanweime/us-stock-daily" target="_blank" rel="noopener">GitHub</a>
      </div>
    </div>
    <section class="hero-panel" id="overview">
      <div class="overview-copy">
        <p class="eyebrow">Investment Research Terminal</p>
        <h2>把美股投研沉淀成可检索、可追踪、可复盘的研究终端</h2>
        <p>「每日观察」自动聚合 X 高赞讨论，「深度研究」沉淀个股与产业链深挖。顶部搜索可同时过滤研报与日报。仅供研究，非投资建议。</p>
      </div>
      <div class="metric-grid">{metric_html}</div>
    </section>
    <section class="panel" id="research">
      <div class="panel-head"><div><p class="eyebrow">Deep Dives</p>
        <h2>深度研究</h2><p>个股 / 产业链 / 主题研报，每篇为自包含子模块。</p></div></div>
      <div class="player-grid">{rcards_html}</div>
    </section>
    <section class="panel" id="daily">
      <div class="panel-head"><div><p class="eyebrow">Daily Market Watch</p>
        <h2>每日观察</h2><p>每天北京时间约 12:00 自动更新。最后更新：{_esc(last)}。</p></div></div>
      <div class="doc-map">{dchips_html}</div>
    </section>
    <section class="panel" id="monitor">
      <div class="panel-head"><div><p class="eyebrow">Keyword Velocity Monitor</p>
        <h2>关键词监控</h2><p>每小时检索存储 / 光模块关键词，按推文 ID 去重统计放量。{mon_updated}</p></div></div>
      <div class="doc-map">{mon_chips_html}</div>
      <p style="margin:12px 0 0"><a class="source-link" href="monitor/index.html">查看完整监控看板 →</a></p>
    </section>
    <p class="empty-state" id="emptyState">没有匹配的内容。</p>
    <footer class="footer">grok 原生 X 检索 · 内容由 AI 聚合可能有误 · 仅供研究，非投资建议</footer>
  </main>
</div>
<script src="assets/terminal.js"></script>
</body></html>""", encoding="utf-8")


if __name__ == "__main__":
    render_home()
    print("已重渲染 docs/index.html")
