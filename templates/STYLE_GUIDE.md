# 美股投研 · 「研究终端」风格规范 (STYLE GUIDE)

所有美股 / 半导体 / AI 基建研报统一用这套视觉与结构。**目标美学**：暖纸色 + 绿色 accent
的「投资研究终端」——克制、信息密度高、可排序、可搜索。参考样板：
`docs/research/ai-infra-dashboard/index.html`。

## 产出规范（最重要）
- 一篇研报 = **一个自包含单 HTML**：内联 `<style>`（整段复制 `docs/assets/theme.css`）+ 内联
  `<script>`（整段复制 `docs/assets/terminal.js`）。**不外链 CSS/JS**，这样它能作为子模块独立发布。
- **起手就复制** `templates/research-report.html`，按注释填内容，删掉用不到的 panel。
- 图片：要么 base64 内联，要么和 HTML 放同目录，发布时用 `--cover` 带上。

## 设计令牌（来自 :root，勿改）
- 背景 `--bg:#f6f4ef`｜卡面 `--surface:#fffdfa`｜墨 `--ink:#181916`｜次要 `--muted:#676b62`
- 描边 `--line:#d9d5ca` / `--line-strong:#bdb7aa`｜圆角 `--radius:8px`
- 强调：绿 `--accent:#0b6b57`（主）｜金 `--accent-2:#9a6500`（关注/警示）｜红 `--danger:#a33b2a`（风险）｜蓝 `--cool:#315f8a`
- 字体：Inter + PingFang SC 中文回退；数字一律 `font-variant-numeric: tabular-nums`

## 布局骨架
`app-shell`（侧栏 280px + 主区）→ 主区内：`topbar`(搜索) → `hero-panel`(定位语 + `metric-grid` 4 个 KPI) → 若干 `panel`。
- 侧栏 `.sidebar`：`.brand`(h1 标题 + p 副标题) + 多个 `.nav-group`（`.nav-group-title` + `.nav-link`：`<span>序号</span><strong>名</strong>`）。
- 每个 `panel`：`.panel-head`(`.eyebrow` 小标签 + `h2` 标题 + 可选 p 说明) + 内容区。

## 组件清单（按需取用）
| 组件 | class | 用途 |
|---|---|---|
| KPI 指标 | `.metric-grid > .metric`（`strong` 数字 + `span` 名） | Hero 关键数字 |
| 可排序表 | `table.sortable`，表头 `th > button.sort-button` | 玩家/数据排序表 |
| 数字列 | `td.num` | 右对齐等宽数字、参与数值排序 |
| 玩家档案卡 | `.player-grid > .player-card`（`header`+`h3`+`.ticker`，`dl/dt/dd`） | 个股要点 |
| 产业链图 | `.chain-map > .chain-row > .chain-cell`（`.bottleneck/.watch/.risk-node`） | 供应链/环节 |
| 正文 | `.markdown-body`（h2/h3/p/ul/blockquote/pre/table） | Markdown 转出的研究正文 |
| 时间线 | `.timeline > .timeline-item`（`time` + `div`） | 事件/催化 |
| 徽章 | `.badge`（`.accent` 绿 / `.warn` 金） | 风控规则、标签、状态 |
| 文档入口 | `.doc-map > .doc-chip`（`span` 小字 + `strong`） | 子文档导航 |
| 来源 | `.source-list > li > a` | 参考链接 |
| 图示 | 内联 `<svg class="diagram">`（`.node/.node-strong/.link…`） | 结构示意图 |

## 交互（已内置在 terminal.js）
- **搜索**：顶栏 `#searchInput` 实时过滤 → `table.sortable` 的行 + 任意 `.filter-item` 元素。给"希望被搜索过滤"的卡片/小节加 `class="filter-item"`。
- **排序**：`table.sortable` 表头点 `button.sort-button` 切换升降序；纯数字列按数值排，否则按拼音。
- 必备元素 id：`#searchInput #resetSearch #rowCount #emptyState`（模板已含）。

## 文案规范
- `.eyebrow` 用**英文短标签大写**（如 `Tradable Players`、`Supply Chain`、`Risk Rules`）。
- `h2` 用中文标题；说明文字进 `.muted` / `panel-head` 的 p。
- 数字（营收占比、点赞、提及）保留单位，放进 `td.num` 或 `.metric strong`。
- 结尾 footer 必含口径与免责：`仅供研究，非投资建议`。

## 发布
填好后：
```bash
cd ~/automation/us-stock-daily
python3 publish_research.py --src 你的报告.html --slug some-topic \
  --title "标题" --date YYYY-MM-DD --tags 硅光,CPO --tickers AVGO,MRVL --teaser "一句话"
```

## 可直接粘给 LLM 的 PROMPT
> 你是美股投研编辑。请把以下材料整理成**一个自包含 HTML 研报**，严格使用「研究终端」设计系统：
> 暖纸底 `#f6f4ef` + 绿色 accent `#0b6b57`，Inter/PingFang 字体，`app-shell`(侧栏+主区) 布局；
> 顶栏带全局搜索框，Hero 含 4 个 KPI 指标卡，正文用 `panel` 分区；可排序表用 `table.sortable`
> + 表头 `button.sort-button`，个股用 `.player-card`，产业链用 `.chain-map`，催化用 `.timeline`，
> 风控/标签用 `.badge`。内联整段 CSS 与 JS（见 theme.css / terminal.js），数字用 tabular-nums，
> 结尾注明"仅供研究，非投资建议"。直接输出完整 HTML，可基于 templates/research-report.html 起手。
> 材料如下：……
