# 🚀 A股选股策略工具

> 📈 给普通股民也能上手的 A 股辅助决策工具：帮你每天找股票、看持仓、做回测、生成交易计划。  
> 🙌 不要求你会编程，不要求你懂量化，只要跟着步骤操作，就能快速用起来。

[![Release](https://img.shields.io/github/v/release/lbbit/ashare-strategy-tool)](https://github.com/lbbit/ashare-strategy-tool/releases)
[![Stars](https://img.shields.io/github/stars/lbbit/ashare-strategy-tool?style=social)](https://github.com/lbbit/ashare-strategy-tool/stargazers)
[![License](https://img.shields.io/github/license/lbbit/ashare-strategy-tool)](LICENSE)

## ✨ 这是一个适合谁的工具？
如果你属于下面任意一种，这个工具就适合你：
- 👀 平时手动看盘、选股，但觉得太花时间
- 🧠 想减少“凭感觉买卖”，希望有一套明确规则
- 📊 想知道一个策略过去表现如何，但不会写量化代码
- 🗂️ 想每天快速得到“今日可关注股票”和“持仓复核建议”
- 🪜 想要一个能逐步进阶的工具：先命令行用，再慢慢用图形界面

## 💡 它能为你做什么？
这个工具现在已经可以帮你完成：
- ✅ **自动选股**：从 A 股市场中筛出符合规则的候选股
- ✅ **每日交易计划**：自动生成“今天重点看什么、当前持仓怎么复核”
- ✅ **历史回测**：看看策略过去一段时间收益、回撤、胜率如何
- ✅ **持仓管理**：保存你当前持仓，方便每天复核
- ✅ **结果导出**：把候选股、交易记录、净值曲线导出成 CSV
- ✅ **可视化查看**：通过 Web UI 查看回测结果和指标

一句话理解：
> 🛠️ 它不是替你自动下单，而是把你每天手工做的“翻股票、记持仓、做复盘”流程尽量自动化。

## 🌟 为什么普通股民也容易上手？
因为你不需要先学编程，只需要先会这 3 个命令：

```bash
ashare-strategy screen
ashare-strategy plan --output-dir daily_plan
ashare-strategy backtest --mode rolling --export-report-dir reports
```

它们分别对应：
- `screen`：🔎 今天有哪些股票符合规则
- `plan`：📝 今天该重点看什么、持仓要不要复核
- `backtest`：📉 这套方法过去效果如何

## ⚡ 快速开始：3 步跑起来

### 1️⃣ 第 1 步：安装
```bash
git clone git@github.com:lbbit/ashare-strategy-tool.git
cd ashare-strategy-tool
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

如果你是普通用户，不想看源码，也可以直接去 Release 页面下载 Windows 打包版本：
- 📦 [下载发布版本](https://github.com/lbbit/ashare-strategy-tool/releases)

### 2️⃣ 第 2 步：先看今天候选股
如果你使用的是源码安装版：
```bash
ashare-strategy screen
```
如果你使用的是 Windows 打包版：
```powershell
.\ashare-strategy.exe screen
```

### 3️⃣ 第 3 步：生成每日计划
```bash
ashare-strategy plan --output-dir daily_plan
```
运行后会生成：
- `summary.csv`：📋 今天计划摘要
- `buy_candidates.csv`：🛒 今日可关注买入候选
- `hold_positions.csv`：💼 当前持仓
- `sell_review.csv`：🚨 今日待复核卖出清单

如果你想先看看策略历史效果，再运行：
```bash
ashare-strategy backtest --mode rolling --export-report-dir reports
```

## 🧭 最推荐的新手使用路径
如果你是第一次用，建议按下面顺序：
1. `screen`：先看候选股输出长什么样
2. `save-sample-positions`：生成一个示例持仓
3. `positions`：看持仓格式
4. `plan`：生成每日计划
5. `backtest`：看历史效果
6. `ui`：打开图形界面

## 🧰 功能总览
- 板块筛选
- 个股筛选
- 买卖规则模拟
- 持仓持久化
- 逐日滚动回测
- 年化收益 / 回撤 / 夏普 / 胜率 / 盈亏比
- 报告导出
- 每日交易计划导出
- Windows 自动打包发布

## 📈 Star 趋势
[![Stargazers over time](https://starchart.cc/lbbit/ashare-strategy-tool.svg?variant=adaptive)](https://starchart.cc/lbbit/ashare-strategy-tool)

## 🧪 常用命令
```bash
ashare-strategy screen
ashare-strategy plan --output-dir daily_plan
ashare-strategy positions
ashare-strategy save-sample-positions
ashare-strategy backtest --mode rolling --export-report-dir reports
ashare-strategy ui
```

## ⚠️ 当前能力边界
- 当前不直接连接券商自动下单
- 当前更适合“辅助决策 + 模拟复盘 + 持仓管理”
- 实时数据依赖 AkShare 与上游接口，若网络波动可能导致请求失败

## 📚 文档导航
- [👶 新手详细使用说明](docs/USER_GUIDE.md)
- [🗺️ 开发计划](docs/DEVELOPMENT_PLAN.md)
- [📌 功能状态](docs/FEATURE_STATUS.md)
- [🤖 AI 开发说明](AGENTS.md)
- [📝 Release 说明](RELEASE_NOTES.md)
- [🛰️ 数据源调研与适配计划](docs/DATA_PROVIDER_RESEARCH.md)

## 📦 下载与发布
- GitHub Release 页面提供源码包和 Windows 打包版
- Windows 打包版已内置默认配置文件，解压后可直接运行 `ashare-strategy.exe screen`
- Tag 发布后会自动触发 Windows x86_64 打包上传
- 如果自动上传失败，可手动补传 zip 附件

## 🎯 适合你的使用方式
- **只想看信号**：用 `screen`
- **想做日常复盘**：用 `plan`
- **想验证策略过去是否有效**：用 `backtest`
- **不想总看命令行**：用 `ui`

> ❤️ 如果你愿意，这个工具可以把“手工选股”变成“半自动执行流程”。

## 🧱 首次初始化后会得到什么？
运行 `ashare-strategy init-workspace` 后，通常会得到：
- 示例持仓
- `reports/` 报告目录
- `daily_plan/` 计划目录
- `custom_strategy.yaml` 配置副本
- `README.txt` 使用说明文件

## 🧪 策略模板
现在支持三种模板：
- `beginner`：新手默认推荐
- `conservative`：偏稳健
- `aggressive`：偏激进

例如：
```bash
ashare-strategy screen --template conservative
ashare-strategy backtest --template aggressive --output json
```


## 数据源补充说明
- 默认免费体验可使用 `akshare`
- 若你购买的是 Tinyshare 授权码，可继续选择 `provider: tushare`，并把 `data_source.tushare_sdk` 设为 `tinyshare`，把授权码填写到 `data_source.tushare_token`

- 新增 `doctor-data` 命令，可快速检查当前数据源是否可认证、核心接口是否可访问、是否只能回退缓存。
