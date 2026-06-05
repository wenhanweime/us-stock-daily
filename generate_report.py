#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""股市观察日报 — 主入口（由 launchd 每日 12:00 北京时间调用）。

流程：串行跑 smart-search（1 综合导读 + 6 分板块）→ 机械聚合(去重推文/ticker/作者)
     → 渲染当日子页 docs/reports/<date>.html → 更新 docs/feed.json → 重生成 docs/index.html
     → git add docs/ + commit + push（GitHub Pages 自动刷新）。

设计参考用户既有项目 ~/Documents/TwitterMessage/summarize_tweets.py 的
load_local_env / update_static_feed / auto_publish_to_pages 模式。
手动运行：  python3 generate_report.py
"""
from __future__ import annotations

import html as _html
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from queries import build_queries

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
REPORTS_DIR = DOCS_DIR / "reports"
FEED_JSON_PATH = DOCS_DIR / "feed.json"
RAW_ROOT = BASE_DIR / "data" / "raw"

SMART_SEARCH = os.environ.get("SMART_SEARCH_BIN", "/opt/homebrew/bin/smart-search")
SEARCH_TIMEOUT = 240          # 传给 smart-search 的 --timeout
SUBPROC_TIMEOUT = 320         # 子进程硬超时（留余量）
FEED_MAX_ENTRIES = 90         # feed.json 保留期数上限
SITE_TITLE = "股市观察日报"
CST = timezone(timedelta(hours=8))

TWEET_RE = re.compile(r"https://(?:x|twitter)\.com/([A-Za-z0-9_]+)/status/(\d+)")
TICKER_RE = re.compile(r"\$[A-Z]{1,5}\b")


# ---------------------------------------------------------------------------
# env（照搬 TwitterMessage 模式：项目内可放 .env 覆盖配置）
# ---------------------------------------------------------------------------
def load_local_env() -> None:
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        if k and k not in os.environ:
            os.environ[k] = v.strip().strip('"').strip("'")


# ---------------------------------------------------------------------------
# markdown → html（优先 markdown 库，缺失时退化为内置极简转换，保证永不硬崩）
# ---------------------------------------------------------------------------
def md_to_html(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    try:
        import markdown  # type: ignore
        return markdown.markdown(text, extensions=["tables", "sane_lists", "nl2br"])
    except Exception:
        return _fallback_md(text)


def _inline(s: str) -> str:
    s = _html.escape(s, quote=False)
    s = re.sub(r"\[\[?(\d+)\]?\]\((https?://[^\s)]+)\)",
               r'<sup><a href="\2" target="_blank" rel="noopener">\1</a></sup>', s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"(https?://[^\s<]+)", r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def _fallback_md(text: str) -> str:
    out: List[str] = []
    list_mode: Optional[str] = None  # 'ul' | 'ol'

    def close_list():
        nonlocal list_mode
        if list_mode:
            out.append(f"</{list_mode}>")
            list_mode = None

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            close_list()
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_list()
            lvl = min(len(m.group(1)) + 1, 6)
            out.append(f"<h{lvl}>{_inline(m.group(2))}</h{lvl}>")
            continue
        m = re.match(r"^\d+[.)]\s+(.*)$", line)
        if m:
            if list_mode != "ol":
                close_list(); out.append("<ol>"); list_mode = "ol"
            out.append(f"<li>{_inline(m.group(1))}</li>")
            continue
        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            if list_mode != "ul":
                close_list(); out.append("<ul>"); list_mode = "ul"
            out.append(f"<li>{_inline(m.group(1))}</li>")
            continue
        close_list()
        out.append(f"<p>{_inline(line)}</p>")
    close_list()
    return "\n".join(out)


# ---------------------------------------------------------------------------
# smart-search 调用 + 解析
# ---------------------------------------------------------------------------
def run_search(query: str, out_path: Path) -> Optional[dict]:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [SMART_SEARCH, "search", "--format", "json",
           "--output", str(out_path), "--timeout", str(SEARCH_TIMEOUT), query]
    try:
        subprocess.run(cmd, text=True, capture_output=True, timeout=SUBPROC_TIMEOUT)
    except subprocess.TimeoutExpired:
        print(f"  ! 超时：{out_path.name}")
    except FileNotFoundError:
        print(f"  ! 找不到 smart-search：{SMART_SEARCH}")
        return None
    if not out_path.exists():
        return None
    try:
        data = json.loads(out_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"  ! 解析失败 {out_path.name}: {exc}")
        return None
    if not data.get("ok"):
        print(f"  ! ok=false {out_path.name}: {data.get('error', '')[:80]}")
        return None
    return data


def aggregate(contents: Sequence[str]) -> Dict:
    blob = "\n".join(contents)
    tweets = set()
    authors: Dict[str, int] = {}
    for handle, sid in TWEET_RE.findall(blob):
        key = f"{handle}/{sid}"
        if key not in tweets:
            tweets.add(key)
            authors[handle] = authors.get(handle, 0) + 1
    tickers: Dict[str, int] = {}
    for t in TICKER_RE.findall(blob):
        tickers[t] = tickers.get(t, 0) + 1
    return {
        "unique_tweets": len(tweets),
        "tickers": sorted(tickers.items(), key=lambda x: -x[1])[:15],
        "authors": sorted(authors.items(), key=lambda x: -x[1])[:12],
    }


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
def _us_trading_hint(now_cst: datetime) -> str:
    try:
        from zoneinfo import ZoneInfo
        et = now_cst.astimezone(ZoneInfo("America/New_York"))
        return f"覆盖美东 {et:%Y-%m-%d} 前后的盘后/隔夜讨论"
    except Exception:
        return "覆盖最近一个美股交易日的盘后/隔夜讨论"


def render_report_page(date_str: str, now_cst: datetime, model: str,
                       summary_md: str, angles: List[Tuple[str, dict]],
                       agg: Dict) -> str:
    ticker_html = "".join(
        f"<tr><td>{i+1}</td><td class='tk'>{_html.escape(t)}</td>"
        f"<td>{n}</td></tr>"
        for i, (t, n) in enumerate(agg["tickers"]))
    author_html = "".join(
        f"<li><span class='at'>@{_html.escape(a)}</span> · {n} 帖</li>"
        for a, n in agg["authors"])

    sections = []
    for label, data in angles:
        if not data:
            continue
        body = md_to_html(data.get("content", ""))
        srcs = data.get("sources") or []
        src_links = "".join(
            f'<a href="{_html.escape(s.get("url",""))}" target="_blank" '
            f'rel="noopener">{i+1}</a> '
            for i, s in enumerate(srcs) if s.get("url"))
        src_block = f'<div class="sources">来源：{src_links}</div>' if src_links else ""
        sections.append(
            f'<details><summary>{_html.escape(label)}</summary>'
            f'<div class="md">{body}</div>{src_block}</details>')

    summary_html = md_to_html(summary_md) if summary_md else \
        '<p class="warn">今日导读综合查询未成功，请见下方分板块详情。</p>'

    return f"""<!doctype html>
<html lang="zh-Hans"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{SITE_TITLE} · {date_str}</title>
<link rel="stylesheet" href="../assets/style.css">
</head><body>
<header class="site-header"><a href="../index.html">← {SITE_TITLE}</a></header>
<main class="report">
  <h1>{date_str} 美股观察日报</h1>
  <div class="meta">生成于 {now_cst:%Y-%m-%d %H:%M} (北京时间) · 模型 {_html.escape(model or 'grok')}
   · 去重唯一高赞推文 <b>{agg['unique_tweets']}</b> 条 · {_us_trading_hint(now_cst)}</div>
  <section class="hero md">{summary_html}</section>
  <section class="stats">
    <div class="card"><h3>最热个股 / Ticker</h3>
      <table class="ticker"><thead><tr><th>#</th><th>代码</th><th>提及</th></tr></thead>
      <tbody>{ticker_html or '<tr><td colspan=3>—</td></tr>'}</tbody></table></div>
    <div class="card"><h3>高产账号</h3><ul class="authors">{author_html or '<li>—</li>'}</ul></div>
  </section>
  <h2>分板块详情</h2>
  {''.join(sections) or '<p class="warn">分板块查询均未成功。</p>'}
  <footer>数据来源：grok 原生 X 检索（Top 模式）· 点赞为检索时近似值 · 仅供研究，非投资建议</footer>
</main></body></html>"""


def update_feed(entry: Dict) -> Dict:
    data = {"entries": []}
    if FEED_JSON_PATH.exists():
        try:
            loaded = json.loads(FEED_JSON_PATH.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                data = loaded
        except json.JSONDecodeError:
            print("警告：feed.json 解析失败，将重建。")
    entries = [e for e in data.get("entries", []) if e.get("date") != entry["date"]]
    entries.insert(0, entry)
    data["entries"] = entries[:FEED_MAX_ENTRIES]
    data["last_updated"] = entry["generated_at"]
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    FEED_JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                              encoding="utf-8")
    return data


def render_index(feed: Dict) -> None:
    items = []
    for e in feed.get("entries", []):
        tks = " ".join(t for t, _ in (e.get("tickers") or [])[:6])
        items.append(
            f'<li><a class="d" href="reports/{e["date"]}.html">{e["date"]}</a>'
            f'<div class="t">{_html.escape(e.get("teaser",""))}</div>'
            f'<div class="s">{e.get("unique_tweets",0)} 条高赞 · {_html.escape(tks)}</div></li>')
    last = feed.get("last_updated", "")
    (DOCS_DIR / "index.html").write_text(f"""<!doctype html>
<html lang="zh-Hans"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{SITE_TITLE}</title>
<link rel="stylesheet" href="assets/style.css">
</head><body>
<header class="site-header"><b>{SITE_TITLE}</b></header>
<main class="home">
  <p class="lede">每日自动抓取 X (Twitter) 上美股高赞讨论，聚合当日最热话题、个股与情绪。
   每天北京时间约 12:00 更新。最后更新：{_html.escape(last)}</p>
  <ul class="archive">{''.join(items) or '<li>暂无数据</li>'}</ul>
  <footer>grok 原生 X 检索 · 仅供研究，非投资建议</footer>
</main></body></html>""", encoding="utf-8")


# ---------------------------------------------------------------------------
# git 发布（照搬 TwitterMessage：无变化跳过、有变化 commit+push，不抛异常）
# ---------------------------------------------------------------------------
def publish(generated_at: str) -> None:
    def git(args):
        return subprocess.run(["git", "-C", str(BASE_DIR), *args],
                              text=True, capture_output=True)
    try:
        if git(["add", "docs"]).returncode != 0:
            print("发布失败：git add"); return
        if git(["diff", "--cached", "--quiet", "--", "docs"]).returncode == 0:
            print("docs 无变化，跳过发布。"); return
        c = git(["commit", "-m", f"日报更新 {generated_at}"])
        if c.returncode != 0:
            print(f"发布失败：git commit {c.stderr.strip()}"); return
        p = git(["push"])
        if p.returncode != 0:
            print(f"发布失败：git push {p.stderr.strip()}"); return
        print("已 push，GitHub Pages 将刷新。")
    except FileNotFoundError:
        print("发布失败：未找到 git。")
    except Exception as exc:
        print(f"发布失败：{exc}")


# ---------------------------------------------------------------------------
def main() -> int:
    load_local_env()
    now = datetime.now(CST)
    date_str = now.strftime("%Y-%m-%d")
    raw_dir = RAW_ROOT / date_str
    print(f"== 股市观察日报 {date_str} ==")

    summary_q, angle_qs = build_queries(date_str)

    print("[0/6] 综合导读 ...")
    summary_data = run_search(summary_q, raw_dir / "g0_summary.json")

    angles: List[Tuple[str, dict]] = []
    for i, (label, q) in enumerate(angle_qs, 1):
        print(f"[{i}/{len(angle_qs)}] {label} ...")
        angles.append((label, run_search(q, raw_dir / f"g{i}.json")))

    contents = ([summary_data["content"]] if summary_data else []) + \
               [d.get("content", "") for _, d in angles if d]
    if not contents:
        print("全部查询失败，放弃本期（不提交）。")
        return 1

    agg = aggregate(contents)
    model = (summary_data or next((d for _, d in angles if d), {})).get("model", "grok")
    summary_md = summary_data["content"] if summary_data else ""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / f"{date_str}.html").write_text(
        render_report_page(date_str, now, model, summary_md, angles, agg),
        encoding="utf-8")
    print(f"已生成子页 reports/{date_str}.html（唯一推文 {agg['unique_tweets']} 条）")

    teaser = ""
    if summary_md:
        for ln in summary_md.splitlines():
            t = re.sub(r"[#*`>]", "", ln).strip()
            if len(t) > 8 and not t.startswith("一句话"):
                teaser = t[:80]; break
    generated_at = now.strftime("%Y-%m-%d %H:%M:%S %z")
    feed = update_feed({
        "date": date_str,
        "generated_at": generated_at,
        "model": model,
        "unique_tweets": agg["unique_tweets"],
        "tickers": agg["tickers"][:8],
        "teaser": teaser or f"{agg['unique_tweets']} 条美股高赞讨论聚合",
        "report_path": f"reports/{date_str}.html",
    })
    render_index(feed)
    publish(generated_at)
    print("完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
