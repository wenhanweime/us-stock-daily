# AAOI（Applied Optoelectronics）深度研究报告

日期：2026-06-09  
标的：Applied Optoelectronics, Inc.（NASDAQ: AAOI）  
货币：USD  
研究类型：AI 数据中心光模块高弹性执行型标的研究  
结论属性：研究分析，不构成投资建议

## 核心结论

**AAOI 不是便宜股，而是 AI 光模块供需紧张下的高 beta 执行股。** 市场正在买三个连续兑现：800G 从首批量产进入爬坡、1.6T 从订单进入发货、产能从十万只/月级别扩到五十万只/月以上。若这些节点顺利兑现，2026 年收入可能从 2025 年的 4.557 亿美元跃升到管理层框架的 11 亿美元以上；若任一环节延迟，当前估值没有多少容错率。

我的判断是：**中性偏积极观察，适合高风险小仓位跟踪，不适合把它当成低估值核心仓位。**  
综合评分：**6.5/10**。成长弹性 8.5/10，订单与产能可见度 7/10，财务质量 5/10，竞争壁垒 6/10，估值安全边际 3/10。

最关键的投资问题不是“AI 光模块需求是否真实”，而是：**AAOI 能否在 2026 下半年把 800G/1.6T 订单转成收入、毛利率和经营现金流。** 现在证据支持收入拐点，但还没有充分证明现金流和利润质量。

## 基础数据快照

| 项目 | 最新可核查信息 | 解释 |
|---|---:|---|
| 交易所 / 代码 | NASDAQ: AAOI | Applied Optoelectronics, Inc. |
| 主营 | 光模块、激光器/光组件、CATV/HFC 宽带设备、少量 Telecom/FTTH | 数据中心与 CATV 双主线 |
| 最新正式季报 | Q1 2026，2026-05-07 发布 | Q2 2026 尚未发布 |
| Q1 2026 收入 | 1.511 亿美元 | 同比 +51%，连续第四个季度创收入纪录 |
| Q1 2026 Data Center 收入 | 8,140 万美元 | 同比 +154%，约占收入 54% |
| Q1 2026 Non-GAAP GM | 29.2% | 仍未体现高端 AI 光模块公司应有的毛利率杠杆 |
| Q2 2026 指引 | 收入 1.80-1.98 亿美元；Non-GAAP GM 29-30% | Q2 是 800G 爬坡第一道验证 |
| FY2026 管理层框架 | 收入 >11 亿美元；Non-GAAP operating income >1.40 亿美元 | 来自 Q1 2026 电话会摘要 |
| 最新可交叉验证股价 | 2026-06-05 收盘 177.00 美元；2026-06-08 盘中约 195-201 美元 | 实时行情不可得，采用公开聚合页快照 |
| 市值 / EV | 约 142-163 亿美元市值区间；EV 约 140-161 亿美元区间 | 随股价剧烈波动 |
| 估值 | TTM P/S 约 26.7x；EV/FY2026 sales 约 13-15x | 用管理层 >11 亿美元收入框架估算 |

来源：AAOI [Q1 2026 results](https://investors.ao-inc.com/news-releases/news-release-details/applied-optoelectronics-reports-first-quarter-2026-results)、[2025 10-K](https://www.sec.gov/Archives/edgar/data/1158114/000143774926005875/aaoi20251231_10k.htm)、[Q1 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1158114/000143774926015620/aaoi20260331_10q.htm)、Yahoo Finance quote/key statistics、`evidence/AAOI_20260609/company_latest.json`、`valuation_quote.json`。

## 1. 光模块业务模式和产品线

**AAOI 的商业模式是高固定成本、垂直整合、客户高度集中的光通信制造商模式。** 公司自己设计/制造激光器、光组件和 transceiver（光模块，用于电信号与光信号转换），再向 hyperscaler（超大规模云厂商）、CATV 客户/渠道商和少量电信客户销售。垂直整合的好处是激光器供应、成本、定制和美国制造叙事；坏处是产能、良率和订单波动会直接冲击毛利率和现金流。

2025 年公司还不是纯 AI 数据中心公司。收入结构显示 CATV 仍是最大来源：

| 2025 收入来源 | 金额 / 占比 | 投资含义 |
|---|---:|---|
| CATV | 约 2.451 亿美元 / 53.8% | 主要受北美 cable/MSO 升级、1.8GHz amplifier、DOCSIS 升级驱动 |
| Internet Data Center | 约 1.957 亿美元 / 42.9% | AI 数据中心叙事的核心，但 2025 仍未超过 CATV |
| Telecom | 约 1,370 万美元 / 3.0% | 小业务 |
| FTTH/Other | 约 120 万美元 / 0.3% | 可忽略 |

到 Q1 2026，结构发生明显变化：Data Center 收入 8,140 万美元，已经超过 CATV 的 6,684 万美元，并成为增长主线。这个变化比全年 2025 结构更重要，因为它说明 AAOI 已经从“AI 光模块预期”进入“收入 mix 转向”的阶段。

产品线可以分成四层：

| 产品 / 业务 | 内容 | 关键判断 |
|---|---|---|
| Data Center optical transceivers | 100G/400G/800G/1.6T，重点是 800G OSFP DR8、1.6T 下一代模块 | 估值弹性的核心 |
| CPO/NPO/OBO/ELSFP | CPO/NPO 指把光学引擎与交换 ASIC 更近集成，OBO 是 on-board optics，ELSFP 是外置激光源形态 | 更长期技术路线，短期贡献不如 800G/1.6T pluggable 明确 |
| Lasers / chips / components | 内部激光器、CW DFB、pump laser 等 | 垂直整合的基础，也决定良率和成本 |
| CATV / HFC broadband | 放大器、发射机、节点等 | 现金流稳定性潜在来源，但客户集中度极高 |

来源：AAOI [optical transceivers product page](https://ao-inc.com/products/optical-transceivers/)、`evidence/AAOI_20260609/product_extract.json`、`tenk_customer_extract.json`。

## 2. AI 数据中心布局：订单真实，但客户集中极高

**AI 数据中心是 AAOI 估值重估的主因。** Q1 2026 Data Center 收入同比增长 154%，管理层称 Q1 已向一家大型 hyperscale customer 完成首批 800G volume shipment，并预计 Q2 开始强爬坡、Q3 随新增产能上线进一步加速。

关键订单证据：

| 时间 | 产品 | 订单 / 进度 | 重要性 |
|---|---|---|---|
| 2026-03-09 | 1.6T data center transceivers | 首个 volume order，金额超过 2 亿美元；预计 Q3 初开始发货，Q4 完成 | 证明 AAOI 不是只停留在 800G；进入下一代 AI fabric 供应链 |
| 2026-03-23 / 2026-04-02 | 800G single-mode transceivers | 一个 major hyperscale customer 的 800G 订单从超过 5,300 万美元扩大；近期合计约 1.24 亿美元 | 为 Q2-H2 2026 收入爬坡提供可观察支撑 |
| Q1 2026 | 800G 首批 volume shipment | 已向大型 hyperscale customer 出货 | 从 qualification 转向 production 的证据 |

但订单质量必须和客户集中度一起看。2025 年前十大客户贡献 96.6% 收入，前五大客户约 95.2%；Digicomm 占 53.1%，Microsoft 占 28.8%。Q1 2026 电话会/摘要显示前三大客户分别约占 44%、26%、25%，前十大客户约 98%。这意味着 AAOI 的增长是“少数客户决定曲线”的增长，客户推迟订单、压价、切换供应商或认证延迟都会直接影响季度收入。

Amazon 是战略变量而不是已经完全兑现的收入事实。2025 年公司向 Amazon.com 子公司发行 customer warrant，最多可购买 7,945,399 股，行权价 23.6956 美元，剩余 vesting 与 Amazon 及关联方最高 40 亿美元累计采购挂钩。这个安排强化了长期客户关系，但也意味着未来存在稀释和收入抵减会计处理。

来源：AAOI [1.6T order](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers)、[800G upsized order](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-new-upsized-order-800g-data-center-transceivers)、[2025 10-K](https://www.sec.gov/Archives/edgar/data/1158114/000143774926005875/aaoi20251231_10k.htm)、[Q1 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1158114/000143774926015620/aaoi20260331_10q.htm)、`order_extract.json`、`cashflow_balance_dilution.json`。

## 3. 800G / 1.6T 技术进展：短期看 800G 放量，长期看 1.6T 与 CPO/NPO

**800G 是 2026 年收入兑现核心，1.6T 是 2026 下半年到 2027 年的估值延续点。** 对 AI 集群来说，GPU/accelerator 数量扩大带来高强度 east-west traffic（服务器之间横向通信），铜互联在带宽、距离、功耗上受限，推动 400G 向 800G、1.6T 升级。

AAOI 的 800G 证据链相对更强：

- 产品层面：官网和 datasheet 体系覆盖 800G OSFP DR8，面向 single-mode fiber，典型用于高带宽数据中心互联。
- 商业层面：2026 年已公告多个 hyperscaler 订单，合计超过 1 亿美元级别。
- 经营层面：Q1 已完成首批 volume shipment，Q2 指引隐含 800G 爬坡。

1.6T 的证据链仍处于“订单明确、交付待验证”：

- 官方公告显示首个超过 2 亿美元 volume order。
- 预计 Q3 2026 初开始发货，Q4 完成。
- 技术上用于下一代 102.4T switching architecture 和更高密度 AI 数据中心 fabric。
- 关键验证点是 Q3 是否真的进入发货、良率是否稳定、毛利率是否随产品代际提升。

产能是投资变量的中心。公司在 Q1 2026 新闻稿中称退出 Q1 时 800G 月产能接近 10 万只；3 月 1.6T 订单公告称预计到 2026 年底 combined 800G + 1.6T 月产能超过 50 万只。Q1 电话会摘要进一步提到 Q2 约 15 万只/月、年底目标提高到 65 万只/月以上、2027 年底超过 93 万只/月。由于我无法抓取完整电话会原文，报告将“年底 >50 万只/月”视为更硬的官方 PR 口径，把“>65 万只/月”视为电话会摘要口径，需要下季继续核实。

这条产能路径的难点不只是买设备，还包括：

- 激光器和光组件供应；
- 800G/1.6T 良率和 reliability qualification；
- hyperscaler 多供应商认证；
- 美国 Texas、Taiwan 和 China 多地制造协同；
- 扩产带来的库存、应收账款和现金消耗。

因此，**收入放量本身不是终点，毛利率和经营现金流才是高质量兑现。**

来源：AAOI [Q1 2026 results](https://investors.ao-inc.com/news-releases/news-release-details/applied-optoelectronics-reports-first-quarter-2026-results)、[1.6T order](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers)、`products_800g_16t.json`、`product_extract.json`。

## 4. 最新财务数据和经营状况

**财务报表呈现的是典型扩产拐点：收入明显加速，利润仍弱，现金来自融资而不是经营。**

| 指标 | FY2025 | Q1 2026 | 解释 |
|---|---:|---:|---|
| 收入 | 4.557 亿美元 | 1.511 亿美元 | Q1 同比 +51%，环比 +13% |
| GAAP gross margin | 约 30.0% | 29.1% | 尚未出现高端产品带来的明显 margin expansion |
| Non-GAAP gross margin | 未在此表展开 | 29.2% | Q2 指引仍为 29-30% |
| GAAP net loss | -3,820 万美元 | -1,430 万美元 | 仍亏损 |
| Non-GAAP net loss | 未在此表展开 | -490 万美元 | 接近 breakeven，但还不是盈利质量证明 |
| Q2 2026 指引 | 不适用 | 收入 1.80-1.98 亿美元 | Q2 是关键验证点 |
| FY2026 管理层框架 | 不适用 | 收入 >11 亿美元；Non-GAAP operating income >1.40 亿美元 | 隐含下半年大幅加速 |

现金流更值得警惕：

| Q1 2026 现金流 | 金额 | 含义 |
|---|---:|---|
| Operating cash flow | -8,535 万美元 | 收入增长伴随应收和库存消耗现金 |
| Investing cash flow | -6,809 万美元 | 主要是扩产资本开支 |
| Financing cash flow | +3.893 亿美元 | 主要来自股权融资 |
| 期末现金、现金等价物和 restricted cash | 4.494 亿美元 | 账面流动性强，但来源主要是融资 |
| Q1 股权融资净额 | 约 3.82 亿美元 | 稀释换扩产资金 |

资产负债表目前能支撑扩产。Q1 2026 现金显著高于 2025 年底的约 2.160 亿美元；2.75% convertible senior notes due 2030 约 1.25 亿美元本金，账面值约 1.295 亿美元。问题不是短期偿债，而是：**公司能否把融资换来的产能转成正经营现金流，而不是继续靠股权市场补血。**

财务质量的正面证据：

- 收入加速是真实的，Q1 创纪录且 Q2 指引继续强增长。
- Data Center 收入占比已超过 CATV，AI 业务不再只是叙事。
- 现金储备足以支持短期扩产。
- Non-GAAP 盈亏已接近 breakeven。

财务质量的负面证据：

- GAAP 仍亏损。
- Non-GAAP gross margin 仍约 29-30%，低于 Lumentum/Coherent/Ciena 等更高质量光通信资产。
- Q1 经营现金流显著为负，应收账款和库存增长消耗现金。
- 2026 年扩产依赖融资和股本稀释。

来源：AAOI [Q1 2026 results](https://investors.ao-inc.com/news-releases/news-release-details/applied-optoelectronics-reports-first-quarter-2026-results)、[Q1 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1158114/000143774926015620/aaoi20260331_10q.htm)、`q1_release_extract.json`、`cashflow_balance_dilution.json`。

## 5. 行业竞争地位

**AAOI 的位置不是行业绝对龙头，而是小基数、高弹性、美国/台湾产能稀缺性的受益者。** AI 光模块竞争不是赢家通吃，hyperscaler 通常会多供应商认证，因此 AAOI 不需要成为最大玩家也能实现收入翻倍。但它面对的是规模、成本、技术和客户关系都很强的竞争对手。

| 公司 | 角色 | 相对 AAOI 的含义 |
|---|---|---|
| Innolight / Eoptolink | 中国 800G/1.6T 光模块量产强者，成本和交付速度优势明显 | AAOI 很难在成本/规模上取胜，主要靠客户多元化和美国供应链价值 |
| Coherent | 激光器、InP、模块、SiPh 平台型 photonics 公司 | 技术/规模/客户广度更强，毛利率高于 AAOI |
| Lumentum | 高端 laser/optical components 强者，也参与 AI 光链条 | 上游关键部件和毛利率优势更明显 |
| Fabrinet | 光模块/精密制造 EMS，不是直接品牌竞争者 | 是行业产量代理；低毛利但执行稳定 |
| Ciena | 光传输/DCF/DCI 系统商，不是短距 800G pluggable 直接竞品 | 更稳健地受益于 AI 数据中心互联和云网络扩容 |
| Broadcom 等 DSP/SiPh 生态 | DSP、switch/ASIC/SiPh 关键环节 | 决定模块 BOM、功耗和下一代架构方向 |

最新同业财务也说明 AAOI 的质量差距：

| 公司 | 最新季度收入 | Non-GAAP / adjusted GM | 业务质量信号 |
|---|---:|---:|---|
| AAOI | 1.511 亿美元 | 29.2% | 弹性高，但规模小、毛利率低、仍亏损 |
| Lumentum | 8.084 亿美元 | 47.9% | AI 光组件拉动，利润杠杆强 |
| Coherent | 18.1 亿美元 | 39.6% | 规模和垂直整合更强 |
| Fabrinet | 12.14 亿美元 | 约 12.1% | EMS 模式，低毛利高周转 |
| Ciena | 15.7 亿美元 | 44.9% | 系统侧稳健，backlog 强 |

AAOI 的相对优势：

- 小基数，2026 收入翻倍弹性更高；
- 已有明确 800G/1.6T hyperscaler 订单；
- 内部激光器和美国/Taiwan 扩产对客户供应链多元化有价值；
- Data Center mix 正在快速提高。

AAOI 的相对劣势：

- 规模远小于 Coherent、Lumentum、Fabrinet、Ciena；
- 毛利率明显低；
- 客户集中度极端；
- 仍未证明自由现金流；
- 1.6T 量产尚未通过财报验证。

来源：`peers_competition.json`、`peer_financials.json`、Lumentum [Q3 FY2026 results](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx)、Coherent [Q3 FY2026 results](https://www.coherent.com/news/press-releases/third-quarter-fiscal-year-2026-results)、Fabrinet [Q3 FY2026 results](https://investor.fabrinet.com/news-releases/news-release-details/fabrinet-announces-third-quarter-fiscal-year-2026-financial)、Ciena [Q2 FY2026 results](https://investor.ciena.com/news/news-details/2026/Ciena-Reports-Fiscal-Second-Quarter-2026-Financial-Results/default.aspx)。

## 6. 投资价值评估

**当前估值已经在要求 AAOI 连续兑现。** 以 2026 年 6 月初公开 quote/key-stat 快照看，AAOI 市值大约在 142-163 亿美元区间波动，EV 大约 140-161 亿美元。用管理层 FY2026 收入 >11 亿美元框架估算，EV/FY2026 sales 大约 13-15x；若用 TTM 收入口径，P/S 约 26.7x。

这个估值可以被解释，但很难说便宜：

- 如果 2026 年收入真的超过 11 亿美元，2027 年继续向 15-20 亿美元收入迈进，且 Non-GAAP gross margin 从 29-30% 向 35-40% 提升，当前估值有支撑。
- 如果公司只是收入增长、但毛利率不升、经营现金流持续为负，当前估值会快速显得过高。
- 如果 1.6T 发货延迟或客户订单不连续，估值压缩会很剧烈。

### 情景框架

| 情景 | 关键假设 | 估值含义 |
|---|---|---|
| Bull case | FY2026 收入 >11 亿美元，Q3/Q4 1.6T 顺利发货；2027 收入向 18-20 亿美元推进；Non-GAAP GM 接近或超过 38%；经营现金流转正 | 当前 EV 可被高成长逻辑支撑；股价继续上行依赖 2027 上修 |
| Base case | FY2026 收入接近 11 亿美元；GM 缓慢改善到 32-35%；客户订单延续但现金流改善有限 | 当前价格大体反映未来 12-18 个月乐观预期，风险回报一般 |
| Bear case | Q2/Q3 收入低于指引或 1.6T 延迟；GM 维持 29-30%；库存/应收继续消耗现金；客户集中风险暴露 | EV/S 可能从十几倍压缩到中个位数，股价回撤幅度可能很大 |

### 操作判断

更合理的策略不是追逐叙事，而是等财报验证：

- **可观察，不急于重仓。** 当前价格已经反映大量 2026-2027 预期。
- **小仓试错条件**：Q2 收入接近指引高端、800G 出货强、Non-GAAP GM 至少守住 29-30%、订单继续增加。
- **加仓条件**：Q3 确认 1.6T 发货，H2 毛利率上行，经营现金流改善，客户结构不再过度依赖单一 CATV/数据中心客户。
- **减仓/回避条件**：Q2 低于指引、GM 低于 29%、1.6T 推迟、经营现金流继续显著为负、股权融资继续放大、客户订单取消或转单。

## 7. 未来催化剂和验证清单

下一步最重要的不是听管理层再讲 TAM，而是用财报验证执行：

1. Q2 2026 收入是否落在 1.80-1.98 亿美元高端。
2. Non-GAAP gross margin 是否守住 29-30%，并在 H2 出现上行。
3. 800G 是否从首批出货变成数据中心收入主力。
4. 1.6T 是否按计划 Q3 初开始发货、Q4 完成首个超过 2 亿美元订单。
5. 800G/1.6T 月产能是否按 Q2、年底节点推进。
6. 经营现金流是否从 Q1 的 -8,535 万美元改善。
7. 库存、应收账款是否继续大幅占用现金。
8. Amazon warrant 相关采购和收入抵减是否扩大。
9. 前五/前十大客户集中度是否下降。
10. Lumentum、Coherent、Fabrinet、Ciena 财报是否继续确认 AI 光互联强需求。

## 8. 主要风险

**客户集中风险是第一风险。** FY2025 Digicomm 和 Microsoft 合计超过 80% 收入，Q1 2026 前三大客户约 95%。这不是普通集中度，而是几个客户就能决定全年曲线。

**扩产执行风险是第二风险。** 从 10 万只/月级别扩到 50 万只/月以上，需要设备、人员、良率、供应链、客户认证同时配合。任何一个环节延误都会影响收入和毛利率。

**毛利率风险是第三风险。** AI 光模块收入增长并不自动等于高利润。若 800G/1.6T 以低价换订单，或者扩产折旧、良率、供应链成本抵消产品代际提升，估值会被重新定价。

**现金流和稀释风险不可忽视。** Q1 2026 现金增加主要来自股权融资，经营现金流仍为负。Amazon customer warrant 也可能带来未来稀释。

**竞争风险持续存在。** Innolight/Eoptolink 有规模和成本优势，Coherent/Lumentum 有部件和技术优势，Fabrinet 有制造执行优势。AAOI 的窗口期来自供需紧张和客户多元化需求，但这不等于永久护城河。

**技术替代风险。** CPO/NPO、LPO、SiPh、DSP 功耗路线、switch architecture 变化都可能改变传统 pluggable transceiver 的价值分配。

## 最终判断

AAOI 是 AI 光通信链条里最有弹性的中小市值标的之一，但它的投资质量还没有达到“无脑配置”的程度。多头要押的是：800G 放量、1.6T 准时交付、产能快速扩张、毛利率上升、现金流改善同时发生。空头要押的是：市场把这些事提前全计入了价格，而财务报表还没证明利润和现金流质量。

我的结论是：**放在核心观察名单，等待 Q2/Q3 兑现；若已持有，应围绕财报节点和产能/毛利/现金流设置明确止盈止损；若未持有，不宜在高波动上涨后用大仓位追入。** 这是一只可以交易趋势和业绩斜率的股票，但在当前估值下，不是安全边际充分的长期价值股。

## 数据缺口与证据说明

- 本机 `smart-search doctor` 显示主搜索、web search/fetch、Exa 可用；研究主要通过 `smart-search search` 获取并保存证据。
- 直接 `smart-search fetch` 官方 IR、SEC、产品页时生成了 0 字节文件，因此报告引用官方 URL，并使用定向搜索抽取文件交叉验证。
- 本机没有 `yfinance` 和 OpenBB，直接 `curl` 到 Yahoo chart 接口 DNS 失败。因此没有获得完整 raw OHLCV CSV。`evidence/AAOI_20260609/aaoi_recent_ohlcv_search_derived.csv` 和 PNG 图是基于 `smart-search` 返回的 May 1-Jun 5 公开历史表整理，不能替代券商/API 原始行情。
- 旧证据目录 `evidence/AAOI_20260608/` 中的非空严格核查文件与本次新证据方向一致，但本报告以 `evidence/AAOI_20260609/` 为主证据包。

## 主要来源

- AAOI Q1 2026 results: https://investors.ao-inc.com/news-releases/news-release-details/applied-optoelectronics-reports-first-quarter-2026-results
- AAOI Q1 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1158114/000143774926015620/aaoi20260331_10q.htm
- AAOI 2025 10-K: https://www.sec.gov/Archives/edgar/data/1158114/000143774926005875/aaoi20251231_10k.htm
- AAOI 1.6T volume order: https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers
- AAOI 800G upsized order: https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-new-upsized-order-800g-data-center-transceivers
- AAOI optical transceivers: https://ao-inc.com/products/optical-transceivers/
- Yahoo Finance AAOI quote/history/key statistics: https://finance.yahoo.com/quote/AAOI/
- Lumentum Q3 FY2026 results: https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx
- Coherent Q3 FY2026 results: https://www.coherent.com/news/press-releases/third-quarter-fiscal-year-2026-results
- Fabrinet Q3 FY2026 results: https://investor.fabrinet.com/news-releases/news-release-details/fabrinet-announces-third-quarter-fiscal-year-2026-financial
- Ciena Q2 FY2026 results: https://investor.ciena.com/news/news-details/2026/Ciena-Reports-Fiscal-Second-Quarter-2026-Financial-Results/default.aspx
- Local source manifest: `evidence/AAOI_20260609/source_manifest.md`
