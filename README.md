# 股市观察日报 (us-stock-daily)

每日自动抓取 X (Twitter) 上**美股高赞讨论**，用 grok 原生检索聚合当日最热话题 / 个股 / 情绪，
生成静态网页并推送到 GitHub Pages。

**站点**：https://wenhanweime.github.io/us-stock-daily/

## 工作原理
`launchd`（每天北京时间 12:00）→ `generate_report.py`：
1. 串行调用本地 `smart-search`（1 条综合导读 + 6 条分板块查询，`grok-4.20-multi-agent-xhigh`，Top 模式）。
2. 机械聚合：跨结果去重唯一推文数、`$ticker` 提及排名、高产账号。
3. 渲染当日子页 `docs/reports/YYYY-MM-DD.html`，更新 `docs/feed.json`（滚动封顶 90 期），重生成首页 `docs/index.html`。
4. `git add docs/ && commit && push` → GitHub Pages 自动刷新。

> 串行调用是有意为之：grok 网关并发会限流（见个人记忆）。整期约 10–12 分钟。

## 目录
- `generate_report.py` — 主入口
- `queries.py` — 抓取的查询措辞（**改这里调整角度/口径**）
- `docs/` — GitHub Pages 根（`/docs` on `main`）：`index.html` / `feed.json` / `assets/style.css` / `reports/*.html`
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
