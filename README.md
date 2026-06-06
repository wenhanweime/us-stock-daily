# 美股投研 (us-stock-daily)

一个统一的美股 / 半导体 / AI 基建投研站，三条内容线：

- **每日观察**（自动）：每天抓取 X 上美股高赞讨论，grok 原生检索聚合当日热点 / 个股 / 情绪。
- **深度研究**（手动）：不定期产出的个股 / 产业链 / 主题研报，每篇作为一个自包含「子模块」收纳进站点。
- **关键词监控**（自动）：每小时检索存储 / 光模块关键词，按推文 ID 去重统计「放量」并告警。

三线共用一个首页（`docs/index.html`，自动重渲染，互不覆盖）。

**站点**：https://wenhanweime.github.io/us-stock-daily/

## 工作原理
`launchd`（每天北京时间 12:00）→ `generate_report.py`：
1. 串行调用本地 `smart-search`（1 条综合导读 + 6 条分板块查询，`grok-4.20-multi-agent-xhigh`，Top 模式）。
2. 机械聚合：跨结果去重唯一推文数、`$ticker` 提及排名、高产账号。
3. 渲染当日子页 `docs/reports/YYYY-MM-DD.html`，更新 `docs/feed.json`（滚动封顶 90 期），重生成首页 `docs/index.html`。
4. `git add docs/ && commit && push` → GitHub Pages 自动刷新。

> 串行调用是有意为之：grok 网关并发会限流（见个人记忆）。整期约 10–12 分钟。

## 深度研究：发布一篇研报（手动）
把一篇**自包含的研报 HTML** 收纳为站点子模块并发布：
```bash
cd ~/Documents/us-stock-daily
python3 publish_research.py --src <报告.html> \
  --slug silicon-photonics-cpo-2026 --title "硅光 / CPO 产业全景 2026" \
  --date 2026-05-31 --tags 硅光,CPO,光互联 --tickers AVGO,MRVL \
  --teaser "一句话摘要"           # 省略的字段会自动从 HTML 推断；加 --no-push 只收纳不发布
```
脚本会拷贝到 `docs/research/<slug>/index.html` → 写 `meta.json` → 更新 `research.json`
→ 重渲染首页 → `git push`。同 slug 再发=覆盖更新。**公开站，勿发未脱敏内容。**

> 对应 Claude skill：`~/.claude/skills/us-stock-research-publish/`（产出研报后让 agent 自动走这条流程）。

## 关键词监控（自动）
`launchd com.pot.us-stock-monitor`（每小时 :17）→ `monitor.py`：每个簇跑一次 grok Latest 检索 →
按**推文 ID 跨小时去重**得每桶「本轮新增」→ 放量告警（≥4 且 ≥2.5× 近 24 轮基线）→ 写
`docs/monitor/index.html` + `docs/monitor.json` → 调 `research.render_home()` 刷新统一首页 → push。
- 监控对象（桶）改 `keywords.py`；当前：存储簇=美光$MU / 闪迪$SNDK / 海力士Hynix / 存储HBM，光簇=光模块 / CPO硅光 / $SIVE。
- 新增数是**采样代理**：grok 每簇约 40 条上限，低频词准、高频词偏保守（页面标「采样上限」）；要精确计数需 Apify / X API。
- 只改样式不调 grok：`python3 monitor.py --render`（用上轮数据重渲染 + 刷首页 + push）。

## 风格固化（「研究终端」）
全站统一视觉：暖纸底 `#f6f4ef` + 绿 accent `#0b6b57` + Inter 字体 + 侧栏导航 + 顶栏全局搜索 + KPI 指标卡 + 可排序表（样板：`docs/research/ai-infra-dashboard/`）。
- `docs/assets/theme.css` — 共享设计系统（首页 + 日报用，研报内联同款）
- `docs/assets/terminal.js` — 共享交互（搜索过滤 + 表头排序）
- `templates/research-report.html` — 研报模板（自包含，复制即用）
- `templates/STYLE_GUIDE.md` — 设计令牌 / 组件清单 / 可粘 LLM 的 prompt

## 目录
- `generate_report.py` — 每日观察主入口（launchd 自动）
- `queries.py` — 抓取的查询措辞（**改这里调整角度/口径**）
- `monitor.py` — 关键词监控主入口（launchd 每小时自动） · `keywords.py` — 监控桶配置（**改这里增删关键词**）
- `research.py` — 子模块管理 + 首页统一渲染（每日观察/深度研究/关键词监控三区共用）
- `publish_research.py` — 深度研究发布 CLI
- `docs/` — GitHub Pages 根（`/docs` on `main`）：`index.html` / `feed.json` / `research.json` / `monitor.json` / `assets/` / `reports/*.html` / `research/<slug>/` / `monitor/`
- `data/` — 原始 grok JSON、监控去重 state（`monitor_state.json`）等本地留档，不入库
- `logs/` — launchd 运行日志（不入库）

## 手动运行
```bash
cd ~/Documents/us-stock-daily
python3 generate_report.py
```

## 改每日时间
编辑 `~/Library/LaunchAgents/com.pot.us-stock-daily.plist` 的 `StartCalendarInterval`，然后：
```bash
launchctl bootout gui/$(id -u)/com.pot.us-stock-daily 2>/dev/null
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.pot.us-stock-daily.plist
```

## 依赖
- 本地 `smart-search`（`/opt/homebrew/bin/smart-search`，配置在 `~/.config/smart-search/`）
- Python 3（标准库 + 可选 `markdown`：`pip3 install --user markdown`，缺失时脚本用内置兜底渲染）
- `gh` 已登录、`git` 已配置

## 注意
- launchd 仅在 Mac 唤醒时运行；中午关机则当天缺期。
- 点赞数为 grok 检索时近似值。仅供研究，非投资建议。
