#!/usr/bin/env python3
"""publish_research.py — 把一篇自包含研报 HTML 收纳为站点「子模块」并发布。

用法:
  python3 publish_research.py --src 报告.html \
      [--slug silicon-photonics-cpo] [--title "..."] [--date 2026-06-06] \
      [--tags 硅光,CPO] [--tickers AVGO,MRVL] [--teaser "..."] \
      [--cover cover.jpg] [--no-push]

省略字段会自动推断：title 取 <title>，date 取文件 mtime，
teaser 取 meta description / 首个 <h1>，slug 由标题派生。
"""
from __future__ import annotations
import argparse, subprocess, sys
import research


def _split(s):
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def _git(*args):
    return subprocess.run(["git", "-C", str(research.BASE_DIR), *args],
                          text=True, capture_output=True)


def publish_git(msg: str) -> None:
    if _git("add", "docs").returncode != 0:
        print("发布失败：git add"); return
    if _git("diff", "--cached", "--quiet", "--", "docs").returncode == 0:
        print("docs 无变化，跳过发布。"); return
    if _git("commit", "-m", msg).returncode != 0:
        print("发布失败：git commit"); return
    p = _git("push")
    print("已 push，GitHub Pages 将刷新。" if p.returncode == 0
          else f"发布失败：git push {p.stderr.strip()}")


def main() -> int:
    ap = argparse.ArgumentParser(description="收纳并发布一篇深度研究 HTML")
    ap.add_argument("--src", required=True, help="源 HTML 路径（自包含单文件）")
    ap.add_argument("--slug", help="英文短横线 slug（缺省由标题派生；同 slug=覆盖更新）")
    ap.add_argument("--title", help="标题（缺省取 <title>）")
    ap.add_argument("--date", help="日期 YYYY-MM-DD（缺省取文件 mtime）")
    ap.add_argument("--tags", help="标签，逗号分隔，如 硅光,CPO,光互联")
    ap.add_argument("--tickers", help="个股代码，逗号分隔，如 AVGO,MRVL")
    ap.add_argument("--teaser", help="一句话摘要（缺省自动提取）")
    ap.add_argument("--cover", help="封面图路径（可选，复制进子模块目录）")
    ap.add_argument("--no-push", action="store_true", help="只本地收纳，不 git push")
    a = ap.parse_args()

    entry = research.add_research(
        a.src, slug=a.slug, title=a.title, date=a.date,
        tags=_split(a.tags), tickers=_split(a.tickers),
        teaser=a.teaser, cover=a.cover)
    research.render_home()
    print(f"已收纳：{entry['title']}  →  docs/{entry['path']}  (slug={entry['slug']})")
    if a.no_push:
        print("（--no-push：未发布，记得稍后 git push）")
        return 0
    publish_git(f"研究上线：{entry['title']} ({entry['slug']})")
    print(f"线上：https://wenhanweime.github.io/us-stock-daily/{entry['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
