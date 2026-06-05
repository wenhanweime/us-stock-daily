# -*- coding: utf-8 -*-
"""股市观察日报 — grok 检索查询定义。

改这里就能调整每日抓取的角度 / 措辞。`build_queries(date_str)` 返回：
  (summary_query, [(label, query), ...])
- summary_query: 一条综合查询，让 grok 直接产出可发布的「今日导读」。
- angle 列表: 6 个分板块深挖，作为子页的「分板块详情」。
"""
from __future__ import annotations
from typing import List, Tuple


def build_queries(date_str: str) -> Tuple[str, List[Tuple[str, str]]]:
    d = date_str  # 北京时间日期，如 2026-06-06

    summary_query = (
        f"今天（北京时间 {d}，覆盖最近一个美股交易日及盘后/隔夜讨论）X (Twitter) 上关于"
        "「美股 / 美国股市」点赞最高(most-liked)的讨论。请用 Top 模式按互动排序检索，产出一份"
        "可直接发布的中文「美股观察日报·今日导读」，包含以下五部分并用 Markdown 小标题分隔：\n"
        "### 一句话总结\n（今天美股圈在 X 上最核心的情绪/事件，1-2 句）\n"
        "### 讨论最多的话题排名\n（5-8 条，按热度排序，每条注明为什么热）\n"
        "### 最热个股 / Ticker\n（按提及量列出 $代码 及一句话原因）\n"
        "### 点赞最高的帖子 TOP15\n（每条：@handle、近似点赞数、核心观点、推文URL，按赞降序）\n"
        "### 整体情绪\n（多空对比 + 下一个市场关注的催化剂/事件）"
    )

    angle_queries: List[Tuple[str, str]] = [
        ("大盘 / 指数",
         f"今天（北京时间 {d}，最近24-48小时）X 上关于美股大盘的最高赞讨论：S&P 500 / Nasdaq / "
         "Dow / $SPY / $QQQ 的今日行情、创新高或回调、市场宽度(breadth)。Top 模式按互动排序，"
         "列尽量多(30条以上)高赞推文，每条给 @handle、点赞数、核心观点、推文URL。"),
        ("AI / 算力个股",
         f"今天（北京时间 {d}，最近24-48小时）X 上关于美股 AI/半导体龙头个股的最高赞讨论："
         "$NVDA 黄仁勋言论、$MRVL、$AMD、$AVGO、$TSLA、$MU、光模块/CPO、数据中心、电源/散热。"
         "列尽量多(30条以上)高互动推文：@handle、点赞数、观点、URL。"),
        ("中文美股圈",
         f"今天（北京时间 {d}，最近24-48小时）X 上中文/华人投资圈讨论美股最高赞的帖子。"
         "列尽量多(30条以上)：@handle、点赞数、观点、URL；侧重供应链龙头、个股选择、大盘判断、"
         "抄底/看空情绪。"),
        ("宏观 / 事件",
         f"今天（北京时间 {d}，最近24-48小时）X 上影响美股的宏观与事件最高赞讨论：美联储/利率/"
         "CPI/PCE/就业数据、地缘(伊朗/油价/中东)、关税与政策、议员内幕交易(Pelosi/NVDA)。"
         "列尽量多(30条以上)：@handle、点赞数、观点、URL。"),
        ("看空 / 风险",
         f"今天（北京时间 {d}，最近24-48小时）X 上对美股看空、风险与泡沫警告的最高赞讨论："
         "crash、bubble、估值过高、short interest、Michael Burry、回调/崩盘预警、1987/1999对比。"
         "列尽量多(30条以上)：@handle、点赞数、观点、URL。"),
        ("板块轮动 / 期权",
         f"今天（北京时间 {d}，最近24-48小时）X 上美股板块轮动、期权异动(unusual options)、IPO、"
         "加密与美股交叉、散户(retail)热门标的的最高赞讨论。列尽量多(30条以上)：@handle、点赞数、"
         "观点、URL。"),
    ]
    return summary_query, angle_queries
