# 美股投研 (us-stock-daily)

一个统一的美股 / 半导体 / AI 基建投研站，两条内容线：

- **每日观察**（自动）：每天抓取 X 上美股高赞讨论，grok 原生检索聚合当日热点 / 个股 / 情绪。
- **深度研究**（手动）：不定期产出的个股 / 产业链 / 主题研报，每篇作为一个自包含「子模块」收纳进站点。

两线共用一个首页（`docs/index.html`，自动重渲染，互不覆盖）。

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

## 目录
- `generate_report.py` — 每日观察主入口（launchd 自动）
- `queries.py` — 抓取的查询措辞（**改这里调整角度/口径**）
- `research.py` — 深度研究子模块管理 + 首页统一渲染（被上面两者共用）
- `publish_research.py` — 深度研究发布 CLI
- `docs/` — GitHub Pages 根（`/docs` on `main`）：`index.html` / `feed.json` / `research.json` / `assets/style.css` / `reports/*.html` / `research/<slug>/`
- `data/raw/<date>/` — 每期原始 grok JSON（本地留档，不入库）
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
