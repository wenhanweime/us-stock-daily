#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""monitor.py — 关键词放量监控（美股投研站第三条内容线，launchd 每小时调用）。

每小时：对每个簇跑一次 grok Latest 检索 → 解析原始推文 → 按推文 ID【跨小时去重】得每桶
「本轮新增」→ 跟该桶基线比做放量告警 → 写仪表盘 docs/monitor/index.html + 状态 docs/monitor.json
→ 调 research.render_home() 刷新统一首页（与每日观察/深度研究互不覆盖）→ 健壮 git push。

ID 去重绕开 grok 时间戳不准；新增数是采样代理（低频准、高频偏保守，页面已标注）。
手动： python3 monitor.py          正常跑
       python3 monitor.py --render  用上轮数据重渲染+刷首页+push（改样式时用，不调 grok）
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
from typing import Dict, List, Optional

import research
from keywords import CLUSTERS, ALL_BUCKETS, build_cluster_query

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
MONITOR_DIR = DOCS_DIR / "monitor"
MONITOR_INDEX = MONITOR_DIR / "index.html"
MONITOR_JSON = DOCS_DIR / "monitor.json"
STATE_PATH = BASE_DIR / "data" / "monitor_state.json"
RAW_DIR = BASE_DIR / "data" / "monitor_raw"

SMART_SEARCH = os.environ.get("SMART_SEARCH_BIN", "/opt/homebrew/bin/smart-search")
SEARCH_TIMEOUT = 160
SUBPROC_TIMEOUT = 220
SITE_TITLE = "关键词放量监控"
CST = timezone(timedelta(hours=8))

SEEN_CAP = 3000
HIST_CAP = 168
SPARK_N = 24
SPIKE_MIN = 4
SPIKE_MULT = 2.5

TWEET_RE = re.compile(r"https://(?:x|twitter)\.com/([A-Za-z0-9_]+)/status/(\d+)")
TIME_RE = re.compile(r"\b([0-2]?\d:[0-5]\d)\b")

MONITOR_CSS = """
:root{--bg:#f6f4ef;--surface:#fffdf8;--ink:#22201c;--muted:#6b665d;--accent:#0b6b57;
--accent-soft:#e3efe9;--line:#e6e1d6;--hot:#c2410c;--hot-soft:#fbe6d8;--radius:14px;--maxw:1000px;
--font:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
@media(prefers-color-scheme:dark){:root{--bg:#1a1916;--surface:#23211d;--ink:#ece8df;--muted:#a39d90;
--accent:#4cc2a3;--accent-soft:#21302b;--line:#33302a;--hot:#f0875a;--hot-soft:#3a2418;}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);line-height:1.7;font-size:16px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.site-header{max-width:var(--maxw);margin:0 auto;padding:22px 20px 4px}
.site-header b{font-size:21px}.site-header .upd{color:var(--muted);font-size:13px;margin-left:10px;font-variant-numeric:tabular-nums}
.back{display:inline-block;margin:2px 0 0;color:var(--muted);font-size:13px}
main{max-width:var(--maxw);margin:0 auto;padding:6px 20px 60px}
.lede{color:var(--muted);font-size:13.5px;border-left:3px solid var(--accent);padding:4px 0 4px 14px;margin:12px 0 20px}
.alert{background:var(--hot-soft);border:1px solid var(--hot);border-radius:var(--radius);padding:10px 18px;margin:0 0 20px}
.alert h2{font-size:15px;margin:6px 0 6px;color:var(--hot)}.alert.quiet{background:var(--surface);border-color:var(--line)}
.alert.quiet p{margin:6px 0;color:var(--muted);font-size:14px}.alert strong{color:var(--hot)}
ul.sigs{list-style:none;padding:0;margin:2px 0 4px}ul.sigs li{margin:8px 0;font-size:14px;line-height:1.65}
.sg-k{font-weight:700;color:var(--hot);margin-right:8px}.sg-t{color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}@media(max-width:680px){.grid{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px}
.card.spk{border-color:var(--hot);box-shadow:0 0 0 1px var(--hot) inset}
.chead{display:flex;align-items:center;justify-content:space-between;margin-bottom:4px}.cname{font-weight:700;font-size:16px}
.badge.hot{background:var(--hot);color:#fff;font-size:12px;padding:2px 8px;border-radius:8px}
.cnum{font-size:30px;font-weight:800;line-height:1.1;font-variant-numeric:tabular-nums;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.cunit{font-size:12px;font-weight:600;color:var(--muted)}.csamp{font-size:11.5px;font-weight:500;color:var(--muted);margin-left:auto}.cap{color:var(--hot)}
svg.spark{width:100%;height:34px;display:block;margin:8px 0 2px}
details{margin-top:6px}details summary{cursor:pointer;font-size:13px;color:var(--muted);list-style:none}
details summary::-webkit-details-marker{display:none}details summary::before{content:"▸ ";color:var(--accent)}details[open] summary::before{content:"▾ "}
ul.posts{list-style:none;padding:0;margin:8px 0 2px;max-height:300px;overflow:auto}
ul.posts li{padding:5px 0;border-bottom:1px solid var(--line);font-size:13px;line-height:1.5}
ul.posts .pt{color:var(--muted);font-variant-numeric:tabular-nums;font-size:12px}ul.posts .none{color:var(--muted)}
footer{margin-top:30px;color:var(--muted);font-size:12px;text-align:center}
"""


# --------------------------------------------------------------------------
def load_state() -> Dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            print("警告：monitor_state.json 解析失败，重建。")
    return {"buckets": {}, "last_run": ""}


def save_state(state: Dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")


def run_search(query: str, out_path: Path) -> Optional[dict]:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [SMART_SEARCH, "search", "--format", "json",
           "--output", str(out_path), "--timeout", str(SEARCH_TIMEOUT), query]
    try:
        subprocess.run(cmd, text=True, capture_output=True, timeout=SUBPROC_TIMEOUT)
    except subprocess.TimeoutExpired:
        print(f"  ! 超时 {out_path.name}")
    except FileNotFoundError:
        print(f"  ! 找不到 smart-search: {SMART_SEARCH}"); return None
    if not out_path.exists():
        return None
    try:
        d = json.loads(out_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"  ! 解析失败 {out_path.name}: {exc}"); return None
    if not d.get("ok"):
        print(f"  ! ok=false {out_path.name}"); return None
    return d


def parse_posts(content: str) -> List[Dict]:
    posts = []
    for line in (content or "").splitlines():
        m = TWEET_RE.search(line)
        if not m:
            continue
        url, handle, tid = m.group(0), m.group(1), m.group(2)
        tm = TIME_RE.search(line)
        text = TWEET_RE.sub("", line).strip(" |-—·*`")
        posts.append({"id": tid, "handle": handle, "url": url,
                      "time": tm.group(1) if tm else "", "text": text})
    return posts


def extract_signal(content: str) -> str:
    for line in (content or "").splitlines():
        s = line.strip(" *`-")
        if s.startswith("信号"):
            return re.sub(r"^信号[:：]?\s*", "", s)[:240]
    return ""


def inline_md(s: str) -> str:
    s = _html.escape(s or "", quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w])\*(?!\s)(.+?)(?<!\s)\*(?![\w])", r"<em>\1</em>", s)
    s = s.replace("**", "").replace("`", "")
    return s


def spark_svg(values: List[int]) -> str:
    vals = values[-SPARK_N:] or [0]
    w, h, pad = 180, 34, 3
    mx = max(vals + [1]); n = len(vals)
    bw = (w - pad * 2) / max(n, 1)
    bars = []
    for i, v in enumerate(vals):
        bh = (h - pad * 2) * (v / mx)
        x = pad + i * bw; y = h - pad - bh
        col = "var(--hot)" if i == n - 1 else "var(--accent)"
        bars.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(bw-1.5,1):.1f}" '
                    f'height="{max(bh,0.6):.1f}" rx="1" fill="{col}"/>')
    return (f'<svg class="spark" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'preserveAspectRatio="none">{"".join(bars)}</svg>')


def detect_spike(history: List[Dict], current_new: int) -> bool:
    prev = [h.get("new", 0) for h in history]
    if len(prev) < 3:
        return False
    base = sum(prev[-24:]) / len(prev[-24:])
    return current_new >= SPIKE_MIN and current_new >= SPIKE_MULT * max(base, 1.0)


# --------------------------------------------------------------------------
def render_dashboard(state: Dict, now: datetime, run_new: Dict[str, List[Dict]],
                     spikes: Dict[str, bool], signals: List) -> str:
    spiked = [b for b in ALL_BUCKETS if spikes.get(b)]
    has_sig = any((t for _, t in signals))
    if spiked or has_sig:
        items = "".join(f"<li>🔺 <b>{_html.escape(b)}</b> 放量"
                        f"（本轮新增 {len(run_new.get(b, []))} 条）</li>" for b in spiked)
        sig = "".join(f'<li><span class="sg-k">📡 {_html.escape(c)}</span>'
                      f'<span class="sg-t">{inline_md(t)}</span></li>'
                      for c, t in signals if t)
        banner = f'<section class="alert"><h2>本轮信号</h2><ul class="sigs">{items}{sig}</ul></section>'
    else:
        banner = '<section class="alert quiet"><p>本轮无放量告警，市场平静。</p></section>'

    cards = []
    for b in ALL_BUCKETS:
        bs = state["buckets"].get(b, {})
        hist = bs.get("history", [])
        cur = hist[-1]["new"] if hist else 0
        sampled = hist[-1].get("sampled", 0) if hist else 0
        spark = spark_svg([h.get("new", 0) for h in hist])
        badge = '<span class="badge hot">🔺放量</span>' if spikes.get(b) else ""
        capnote = ' <span class="cap">采样上限·可能偏低</span>' if sampled >= 38 else ""
        posts = run_new.get(b, [])[:15]
        plist = "".join(
            f'<li><span class="pt">{_html.escape(p.get("time") or "—")}</span> '
            f'<a href="{_html.escape(p.get("url",""))}" target="_blank" rel="noopener">@{_html.escape(p.get("handle",""))}</a> '
            f'<span class="px">{inline_md(p.get("text","")[:90])}</span></li>'
            for p in posts) or "<li class='none'>本轮无新帖</li>"
        cards.append(
            f'<div class="card{" spk" if spikes.get(b) else ""}">'
            f'<div class="chead"><span class="cname">{_html.escape(b)}</span>{badge}</div>'
            f'<div class="cnum">{cur}<span class="cunit">新增/本轮</span>'
            f'<span class="csamp">采样 {sampled}{capnote}</span></div>{spark}'
            f'<details><summary>本轮新帖 {len(posts)}</summary><ul class="posts">{plist}</ul></details></div>')

    return f"""<!doctype html>
<html lang="zh-Hans"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="900"><title>{SITE_TITLE} · 美股投研</title>
<style>{MONITOR_CSS}</style></head><body>
<header class="site-header"><b>{SITE_TITLE}</b>
  <span class="upd">更新 {now:%Y-%m-%d %H:%M} (北京时间) · 每小时自动刷新</span>
  <div><a class="back" href="../index.html">← 返回美股投研站</a></div></header>
<main>
  <p class="lede">每小时检索 X 上存储/光模块关键词的最新内容，按推文 ID 去重统计「本轮新增」，
   突然放量或出现异常信号时高亮。新增数为采样代理：低频词准，高频词偏保守。</p>
  {banner}
  <div class="grid">{''.join(cards)}</div>
  <footer>grok 原生 X 检索（Latest 模式，采样去重）· 数字为指示性非精确计数 · 仅供研究，非投资建议</footer>
</main></body></html>"""


def write_monitor_json(state: Dict, spikes: Dict[str, bool], now: datetime) -> None:
    buckets = []
    for b in ALL_BUCKETS:
        hist = state["buckets"].get(b, {}).get("history", [])
        last = hist[-1] if hist else {}
        buckets.append({"name": b, "new": last.get("new", 0),
                        "sampled": last.get("sampled", 0), "spike": bool(spikes.get(b))})
    data = {"last_updated": now.strftime("%Y-%m-%d %H:%M"),
            "keywords": len(ALL_BUCKETS),
            "spiked": [b for b in ALL_BUCKETS if spikes.get(b)],
            "buckets": buckets}
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    MONITOR_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def publish(stamp: str) -> None:
    """健壮 push：与每日 job 共用一个仓库，push 被拒时 rebase 远端后重试。"""
    def git(args):
        return subprocess.run(["git", "-C", str(BASE_DIR), *args], text=True, capture_output=True)
    try:
        git(["add", "docs"])
        if git(["diff", "--cached", "--quiet", "--", "docs"]).returncode == 0:
            print("docs 无变化，跳过。"); return
        if git(["commit", "-m", f"monitor {stamp}"]).returncode != 0:
            print("发布失败：git commit"); return
        for i in range(2):
            if git(["push"]).returncode == 0:
                print("已 push。"); return
            print(f"push 被拒，rebase 远端后重试（{i+1}）...")
            git(["pull", "--rebase", "--autostash"])
        print("发布失败：rebase 重试后 push 仍失败。")
    except Exception as exc:
        print(f"发布异常：{exc}")


def emit(state: Dict, now: datetime, run_new, spikes, signals, stamp: str) -> None:
    """写监控子页 + monitor.json + 刷新统一首页 + push。"""
    MONITOR_DIR.mkdir(parents=True, exist_ok=True)
    MONITOR_INDEX.write_text(render_dashboard(state, now, run_new, spikes, signals), encoding="utf-8")
    write_monitor_json(state, spikes, now)
    try:
        research.render_home()           # 刷新统一首页（每日观察+深度研究+关键词监控）
    except Exception as exc:
        print(f"刷新首页失败（不阻断）：{exc}")
    publish(stamp)


# --------------------------------------------------------------------------
def main() -> int:
    if "--render" in sys.argv:
        state = load_state()
        last = state.get("last")
        if not last:
            print("无 last 渲染数据，先正常跑一次 monitor.py。"); return 1
        now = datetime.fromisoformat(last["ts"])
        signals = [tuple(x) for x in last.get("signals", [])]
        emit(state, now, last.get("run_new", {}), last.get("spikes", {}),
             signals, now.strftime("%Y-%m-%d %H:%M") + " (render)")
        print("仅重渲染完成。"); return 0

    now = datetime.now(CST)
    hour_key = now.strftime("%Y-%m-%d %H:%M")
    print(f"== 关键词监控 {hour_key} ==")
    state = load_state(); state.setdefault("buckets", {})

    all_posts: Dict[str, Dict] = {}
    signals: List = []
    ok_any = False
    for ci, cluster in enumerate(CLUSTERS):
        print(f"[{ci+1}/{len(CLUSTERS)}] 簇「{cluster['name']}」...")
        d = run_search(build_cluster_query(cluster, hour_key),
                       RAW_DIR / now.strftime("%Y%m%d_%H") / f"c{ci}.json")
        if not d:
            continue
        ok_any = True
        content = d.get("content", "")
        sig = extract_signal(content)
        if sig:
            signals.append((cluster["name"], sig))
        for p in parse_posts(content):
            all_posts.setdefault(p["id"], p)

    if not ok_any:
        print("全部簇查询失败，放弃本轮（不提交）。"); return 1

    run_new: Dict[str, List[Dict]] = {b: [] for b in ALL_BUCKETS}
    spikes: Dict[str, bool] = {}
    for name, rx in [(n, rx) for c in CLUSTERS for (n, rx) in c["buckets"]]:
        bs = state["buckets"].setdefault(name, {"seen": [], "history": []})
        seen = set(bs["seen"]); sampled = 0
        for p in all_posts.values():
            if rx.search(p["text"]) or rx.search("@" + p["handle"]):
                sampled += 1
                if p["id"] not in seen:
                    seen.add(p["id"]); run_new[name].append(p)
        new_n = len(run_new[name])
        spikes[name] = detect_spike(bs["history"], new_n)
        bs["seen"] = list(seen)[-SEEN_CAP:]
        bs["history"] = (bs["history"] + [{"hour": hour_key, "new": new_n,
                          "sampled": sampled, "spike": spikes[name]}])[-HIST_CAP:]
        print(f"   {name}: 新增 {new_n} / 采样 {sampled}{' 🔺放量' if spikes[name] else ''}")

    state["last_run"] = hour_key
    state["last"] = {"ts": now.isoformat(), "signals": signals, "spikes": spikes,
                     "run_new": {b: run_new[b][:15] for b in ALL_BUCKETS}}
    save_state(state)
    emit(state, now, run_new, spikes, signals, hour_key)
    print("完成。" + ("　告警：" + ", ".join(b for b in ALL_BUCKETS if spikes.get(b))
                       if any(spikes.values()) else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
