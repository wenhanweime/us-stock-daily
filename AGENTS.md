# AGENTS.md — 美股投研 唯一归集地

> 适用于在本仓库工作的所有 agent（Codex / Claude Code / Amp / Augment 等）。
> 这是「美股 / 半导体 / AI 基建 / 个股 / 投资研究」产出的**唯一归集仓库**。

## 铁律
- **任何**股票 / 投资 / 半导体 / AI 基建研究的产出，都必须落在本仓库，**不要**散落到
  `~/Downloads`、桌面或其它目录。
- 本仓库公开发布在 GitHub Pages（https://wenhanweime.github.io/us-stock-daily/）：
  **涉密 / 未脱敏 / 含个人隐私的内容禁止发布。**

## 三条内容线
- **每日观察**（自动）：`docs/reports/<date>.html`，由 `generate_report.py` + launchd 每天约 12:00 生成，**勿手改**。
- **深度研究**（手动）：`docs/research/<slug>/index.html`，每篇为自包含子模块，由 `publish_research.py` 收纳发布。
- **关键词监控**（自动）：`docs/monitor/index.html` + `docs/monitor.json`，由 `monitor.py`（桶配置在 `keywords.py`）+ launchd `com.pot.us-stock-monitor` 每小时 :17 生成，**勿手改**。盯存储/光模块关键词放量，按推文 ID 去重计数 + 放量告警。

## 发布一篇深度研究
```bash
cd ~/Documents/us-stock-daily
python3 publish_research.py --src <报告.html> --slug <英文短横线> \
  --title "<标题>" --date YYYY-MM-DD --tags 硅光,CPO --tickers AVGO,MRVL --teaser "<一句话>"
```
脚本自动：拷到 `docs/research/<slug>/` → 写 `meta.json` → 更新 `docs/research.json` → 重渲染首页 → `git push`。
省略字段会从 HTML 推断；`--no-push` 只本地收纳。**同 slug 再发 = 覆盖更新。**

## 风格（统一「研究终端」）
- 暖纸底 `#f6f4ef` + 绿 accent `#0b6b57` + Inter 字体 + 侧栏导航 + 顶栏搜索 + KPI 指标卡 + 可排序表。
- 新研报**复制** `templates/research-report.html`（自包含，内联 CSS+JS）起手；规范与可粘 LLM 的 prompt 见 `templates/STYLE_GUIDE.md`；样板 `docs/research/ai-infra-dashboard/`。

## 约定
- slug 用英文短横线（如 `silicon-photonics-cpo-2026`）。
- tickers 只写代码不带 `$`（`MU`、`000660.KS`），逗号分隔。
- 研报必须是**自包含单 HTML**（内联 CSS/JS），配图同目录或 base64 内联。

## 关键文件
- `generate_report.py` 每日观察 · `queries.py` 抓取口径
- `monitor.py` 关键词监控 · `keywords.py` 监控桶配置（改这里增删关键词）
- `research.py` 子模块管理 + 首页统一渲染（每日观察/深度研究/关键词监控三区） · `publish_research.py` 发布 CLI
- `docs/assets/theme.css` + `terminal.js` 共享设计系统 · `templates/` 模板与规范
- Claude Code 用户另有 skill：`us-stock-research-publish`（封装上述流程）
