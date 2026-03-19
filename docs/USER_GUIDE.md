# 👶 新手详细使用说明

> 这份文档默认你是一个只会手动炒股、没有写过程序、也没接触过量化工具的新手。  
> 🎯 目标不是让你学会编程，而是让你一步一步把工具跑起来，先用起来，再慢慢理解里面的规则。

## 1️⃣ 先说清楚：这个工具到底是干什么的？
你可以把它理解成一个“炒股辅助小助手”，主要帮你做 4 件事：

1. 🔎 **每天找出值得关注的股票**
2. 💼 **检查你现在的持仓要不要重点盯一下**
3. 📉 **回头验证这套方法过去是否有效**
4. 📄 **把结果导出成表格，方便自己复盘**

它**不会替你自动下单**，也**不会保证赚钱**。  
它的作用是：
- ⏱️ 帮你减少手工翻股票的时间
- 📏 帮你把“凭感觉操作”变成“按规则检查”
- 🧠 帮你建立自己的复盘习惯

## 2️⃣ 如果你完全不懂这些名词，先这样理解
- **选股**：从很多股票里挑出符合条件的股票
- **回测**：拿过去的历史数据，看看这套方法以前表现怎样
- **持仓**：你现在手里持有的股票
- **调仓**：把原来的股票卖掉一部分，再买新的
- **均线**：过去一段时间平均价格的线，用来判断强弱
- **回撤**：账户从高点往下掉了多少
- **胜率**：赚钱的交易次数占总交易次数的比例

👉 你不需要一开始全懂，只要先会操作，后面再逐步理解就行。

## 3️⃣ 最推荐的新手使用方式
如果你只想最快上手，请按下面顺序做：

### 路线 A：只想先用最核心功能
1. 安装工具
2. 运行 `screen` 看今天候选股
3. 运行 `plan` 生成每日计划
4. 运行 `backtest` 看历史效果

### 路线 B：你手里已经有持仓
1. 安装工具
2. 先运行 `save-sample-positions` 生成一个示例持仓文件
3. 把里面的股票改成你自己的持仓
4. 运行 `positions` 检查是否读取成功
5. 运行 `plan` 生成每日计划

## 4️⃣ 安装步骤（一步一步来）

### 4.1 你需要准备什么？
至少准备：
- 💻 一台电脑
- 🐍 已安装 Python 3.11 或更高版本
- 🌐 能访问 GitHub
- 📋 基本的命令行操作能力（复制粘贴命令即可）

### 4.2 安装命令
在终端中依次运行：

```bash
git clone git@github.com:lbbit/ashare-strategy-tool.git
cd ashare-strategy-tool
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

如果你是 Windows 用户，虚拟环境激活一般类似：

```powershell
.venv\Scripts\activate
```

### 4.3 如果你不想折腾源码
可以优先去这里下载发布版：
- 📦 https://github.com/lbbit/ashare-strategy-tool/releases

> ⚠️ 注意：Windows 打包版现在会内置默认配置文件，正常情况下解压后可直接运行。
> 如果 Release 页面没有 zip 附件，通常是自动打包工作流失败了，需要补发或手动上传。

## 5️⃣ 先完成一次最简单的使用

### 第一步：查看今日候选股
如果你是源码安装用户，运行：
```bash
ashare-strategy screen
```
如果你是 Windows 压缩包用户，进入解压目录后运行：
```powershell
.\ashare-strategy.exe screen
```

意义：
- ✅ 确认工具已经装好
- ✅ 确认数据接口可用
- ✅ 看看策略今天挑出了哪些股票

### 第二步：生成每日交易计划
运行：
```bash
ashare-strategy plan --output-dir daily_plan
```

这个命令会帮你生成一个文件夹，例如 `daily_plan/`，里面通常有：
- `summary.csv`：📋 今天总体情况
- `buy_candidates.csv`：🛒 今天值得重点关注的候选股票
- `hold_positions.csv`：💼 当前持仓列表
- `sell_review.csv`：🚨 建议你重点复核的持仓

### 第三步：回测历史效果
运行：
```bash
ashare-strategy backtest --mode rolling --export-report-dir reports
```

意义：
- 📊 看看策略过去历史表现
- 🧪 不是看某一笔赚没赚，而是整体规则长期是否靠谱
- 📁 会导出交易记录和净值曲线，方便你自己复盘

## 6️⃣ 如果你已经有持仓，怎么录进去？

### 6.1 先生成一个示例文件
运行：
```bash
ashare-strategy save-sample-positions
```

### 6.2 再查看当前持仓
运行：
```bash
ashare-strategy positions
```

### 6.3 你应该怎么理解这个功能？
它不是自动读券商账户，而是让你先把自己的持仓记录在一个本地文件里。  
这样工具就知道：
- 你现在拿着哪些股票
- 今天有哪些股票需要重点复核
- 哪些候选股已经持有，不需要重复关注

## 7️⃣ 最重要：新手参数怎么设置？
默认配置文件在：
- `config/default_strategy.yaml`

如果你是新手，**建议先不要改参数**，先用默认值跑通一次。  
等你看懂结果后，再开始微调。

### 7.1 `hold_days`
意思：最多持有几天。  
建议新手：**先用默认值**。  
影响：值越小，换股越快；值越大，持股时间越长。

### 7.2 `rebalance_interval`
意思：隔几天检查一次是否换仓。  
建议新手：**先用默认值**。  
影响：数字小更频繁调整，数字大更少交易。

### 7.3 `commission_rate`
意思：佣金，也就是交易手续费。  
建议新手：**不要设为 0**，否则回测会太理想化。

### 7.4 `stamp_duty_rate`
意思：印花税。通常卖出时产生。  
建议：保持默认。

### 7.5 `slippage_rate`
意思：滑点。你看到的价格，不一定就是你实际成交的价格。  
建议新手：保持默认，不要先关掉。

### 7.6 `use_cache`
意思：是否使用本地缓存。  
建议：✅ **开着**。  
原因：更快、减少重复联网请求、网络不稳定时更有帮助。

## 8️⃣ 每个命令是干什么的？

### `ashare-strategy screen`
🔎 用途：看今天有哪些股票符合规则。

### `ashare-strategy plan --output-dir daily_plan`
📝 用途：生成你的日常执行计划。

### `ashare-strategy positions`
💼 用途：查看当前本地记录的持仓。

### `ashare-strategy save-sample-positions`
🧾 用途：生成一个示例持仓文件，方便你照着修改。

### `ashare-strategy backtest --mode rolling --export-report-dir reports`
📉 用途：回看历史上这套方法表现怎么样。

### `ashare-strategy ui`
🖥️ 用途：打开图形界面，适合不想总看命令行的人。

## 9️⃣ 建议你每天怎么用
最简单的日常流程：
1. `positions` 看当前持仓是否正确
2. `screen` 看今天候选股
3. `plan` 生成每日计划
4. 打开 `buy_candidates.csv` 和 `sell_review.csv`
5. 结合你自己的交易经验做最终决定

## 🔟 回测结果怎么看才不容易误解？
建议重点看：
- **年化收益**：长期平均下来赚得怎么样
- **最大回撤**：最糟糕的时候会亏到什么程度
- **胜率**：赚钱次数多不多
- **盈亏比**：赚的时候赚得是否比亏的时候更多

❗ 不要只盯收益，不看风险。

## 1️⃣1️⃣ 常见问题

### 为什么我运行失败？
常见原因：
- 网络不稳定
- AkShare 上游数据接口异常
- 本地 Python 环境没有装好

### 为什么没有结果？
可能是：
- 当天没有股票符合当前规则
- 持仓文件为空
- 数据接口没有返回有效数据

### 为什么 Release 没有 Windows 压缩包？
如果自动发布流程失败，Release 页面可能只有源码，没有 zip 附件。  
这种情况需要检查 GitHub Actions 的 release 工作流并重新上传附件。

## 1️⃣2️⃣ 图形界面怎么用？
运行：
```bash
ashare-strategy ui
```

打开后你可以：
- 调整参数
- 点击运行选股
- 点击运行回测
- 看净值曲线
- 看指标卡片

## 1️⃣3️⃣ 你现在最该做什么？
如果你今天第一次接触这个工具，请只做这 4 件事：

```bash
ashare-strategy screen
ashare-strategy save-sample-positions
ashare-strategy positions
ashare-strategy plan --output-dir daily_plan
```

🎉 先把流程跑通，再考虑改参数、做回测、研究细节。

## 1️⃣4️⃣ 给 AI 或自动化工具使用
如果你希望把 CLI 结果交给 AI Agent 或其他脚本处理，可以使用 JSON 输出：

```bash
ashare-strategy screen --output json
```

这样更适合自动化读取。

```bash
ashare-strategy plan --output json
ashare-strategy positions --output json
```
这适合给 AI Agent、脚本或自动化流程读取。
