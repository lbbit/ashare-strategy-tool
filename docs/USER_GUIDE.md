# 👶 A股策略工具新手使用说明

> 这是一份给普通股民和第一次使用本工具的用户准备的说明。  
> 目标不是让你先学会编程，而是让你先会用、先跑通、先看懂结果。

---

## 1️⃣ 这个工具能帮你做什么？
你可以把它理解成一个 **A 股选股 + 回测 + 持仓复核 + 每日计划辅助工具**。

它现在可以帮你做这些事：
- 🔎 从市场里筛选候选股票
- 📉 回看这套方法过去的历史表现
- 💼 保存你的持仓，方便每天复核
- 📝 自动生成每日交易计划
- 📊 导出候选股、交易记录、净值和指标
- 🖥️ 用图形界面查看结果

### 一句话理解
它不是自动替你下单的软件，
而是把你每天“看股票、记持仓、做复盘”的流程尽量标准化、自动化。

---

## 2️⃣ 最适合哪些人？
如果你属于下面这些情况，本工具会比较适合：
- 平时自己看盘、选股，但想减少凭感觉交易
- 想快速得到“今天重点看什么股票”的参考结果
- 想先用简单方式了解策略回测
- 想把自己的持仓记录下来，方便复核
- 想要一个既能命令行使用、又能图形界面使用的工具

---

## 3️⃣ 第一次使用，建议你按这个顺序来
建议第一次不要一上来就调很多参数，先按顺序跑通：

1. `init-workspace`：初始化工作目录
2. `screen`：看看今天筛出来什么股票
3. `positions`：看看持仓格式
4. `plan`：生成每日交易计划
5. `backtest`：查看历史效果
6. `ui`：打开图形界面

---

## 4️⃣ 安装方法

### 方式 A：源码安装（适合愿意折腾一点的用户）
```bash
git clone git@github.com:lbbit/ashare-strategy-tool.git
cd ashare-strategy-tool
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 方式 B：Windows 打包版
如果你不想自己装依赖，可以直接去 GitHub Release 下载 Windows 打包版：
- `ashare-strategy-windows-x86_64.zip`

解压后直接运行：
```powershell
.\ashare-strategy.exe screen
```

---

## 5️⃣ 最推荐的新手命令

### 先初始化工作目录
```bash
ashare-strategy init-workspace --output-dir my_workspace
```

初始化后通常会得到：
- `README.txt`
- `custom_strategy.yaml`
- `beginner_strategy.yaml`
- `conservative_strategy.yaml`
- `aggressive_strategy.yaml`
- `reports/`
- `daily_plan/`

这一步非常推荐，因为它能把第一次使用需要的目录和模板都准备好。

---

## 6️⃣ 看今天候选股
```bash
ashare-strategy screen
```

如果想看结构化 JSON：
```bash
ashare-strategy screen --output json
```

如果你是第一次用，还可以直接套模板：
```bash
ashare-strategy screen --template beginner
```

### 三种模板的直观理解
- `beginner`：适合第一次用，参数比较均衡
- `conservative`：偏稳健
- `aggressive`：偏激进

---

## 7️⃣ 查看或初始化持仓

### 查看当前持仓
```bash
ashare-strategy positions
```

### 写入示例持仓
```bash
ashare-strategy save-sample-positions
```

### 初始化账户/持仓模板
```bash
ashare-strategy init-account
```

如果你想接入自己的真实持仓，通常可以先用示例文件做参考，再改成自己的数据。

---

## 8️⃣ 生成每日交易计划
```bash
ashare-strategy plan --output-dir daily_plan
```

生成后通常会有这些文件：
- `summary.csv`：计划摘要
- `buy_candidates.csv`：可关注候选
- `hold_positions.csv`：当前持仓
- `sell_review.csv`：卖出复核建议

如果你想让 AI Agent 或脚本读取结果：
```bash
ashare-strategy plan --output json
```

---

## 9️⃣ 做历史回测
```bash
ashare-strategy backtest --mode rolling --export-report-dir reports
```

如果想导出交易 CSV：
```bash
ashare-strategy backtest --export-csv trades.csv
```

如果想输出 JSON：
```bash
ashare-strategy backtest --output json
```

### 你通常会看到这些关键结果
- 策略收益
- 基准收益
- 超额收益
- 最大回撤
- 胜率
- 夏普比率
- 净值曲线

---

## 🔟 打开图形界面
```bash
ashare-strategy ui
```

打开后你可以：
- 选择模板
- 调整参数
- 执行选股
- 执行回测
- 查看净值曲线和交易记录

### UI 里建议怎么用
- 新手先选 `beginner`
- 先用默认值跑通一次
- 先看结果，再逐步改参数

---

## 1️⃣1️⃣ 如果数据拉取失败，怎么办？
最近这部分能力已经增强了，建议按下面方法排查。

### 第一步：先诊断数据源
```bash
ashare-strategy doctor-data
```

如果你想让脚本读取结果：
```bash
ashare-strategy doctor-data --output json
```

它会告诉你：
- 当前用的是哪个数据源
- 如果是 Tushare 类，是哪个 SDK
- token/授权码是否有效
- 核心接口能不能访问
- 是否只能依赖缓存

---

## 1️⃣2️⃣ 离线/仅缓存模式
如果网络不稳定，或者你只想复用本地缓存，可用：

```bash
ashare-strategy screen --offline
ashare-strategy backtest --offline
ashare-strategy plan --offline
```

### 离线模式是什么意思？
- 不主动联网
- 只使用本地缓存数据
- 如果缓存不存在，会明确报“缓存缺失”

这在免费源波动时很有用。

---

## 1️⃣3️⃣ 数据源怎么选？
当前项目支持多种数据源路径：

### 1. 默认免费体验：AkShare
适合：
- 新手
- 免费体验
- 原型验证

特点：
- 不花钱
- 上手快
- 但稳定性容易受上游影响

### 2. 官方 Tushare
适合：
- 有 token 的用户
- 希望更规范接口的用户

### 3. Tinyshare 兼容模式
如果你购买的是 Tinyshare 授权码，请这样配：

```yaml
data_source:
  provider: tushare
  tushare_sdk: tinyshare
  tushare_token: "你的授权码"
```

这样程序内部会使用 `tinyshare` SDK，但外部仍然按 Tushare 风格工作。

---

## 1️⃣4️⃣ token 问题怎么理解？
这个很重要，很多用户第一次会混淆。

### 情况 1：提示“token 不对，请确认”
通常表示：
- token/授权码写错了
- token 已失效
- 用错了 SDK

### 情况 2：提示“没有接口访问权限”
通常表示：
- token 是有效的
- 但当前账号没有目标接口权限

也就是说：
> token 有效，不等于你对所有接口都有权限。

---

## 1️⃣5️⃣ 命令失败时为什么现在会带提示？
因为现在 `screen / backtest / plan` 在失败时会自动附带：
- `provider_diagnostics`
- `hint`

这可以帮助你快速判断到底是：
- 网络问题
- token 认证问题
- 权限不足
- 还是缓存不可用

如果你是开发者或 AI Agent 用户，这个结构化输出会很有用。

---

## 1️⃣6️⃣ 推荐给普通用户的使用方法
如果你只是普通股民，我建议这样用：

### 每天早上
1. 跑 `screen`
2. 跑 `plan`
3. 对照自己的持仓看 `sell_review.csv`

### 每周或每月
1. 调一下参数
2. 跑 `backtest`
3. 看看策略是否更适合你的风格

### 网络不好时
1. 先跑 `doctor-data`
2. 再尝试 `--offline`

---

## 1️⃣7️⃣ 常见问题

### Q1：我不会编程，也能用吗？
可以。建议先从 Windows 打包版开始，然后按本说明一步步操作。

### Q2：这个工具会自动下单吗？
不会。它当前主要是辅助决策、复盘、持仓分析和计划生成工具。

### Q3：为什么我今天拉不到数据？
常见原因：
- 免费数据源上游波动
- 网络问题
- token/授权码问题
- 接口权限不足

建议先执行：
```bash
ashare-strategy doctor-data
```

### Q4：离线模式为什么还会失败？
因为离线模式依赖本地缓存。如果之前没缓存过对应数据，就会提示缓存缺失。

---

## 1️⃣8️⃣ 文档导航
如果你还想继续深入：
- `README.md`：项目总览
- `docs/FEATURE_STATUS.md`：现在已经做到了哪些功能
- `docs/DEVELOPMENT_PLAN.md`：后续准备怎么继续演进
- `docs/DATA_PROVIDER_RESEARCH.md`：数据源调研与路线规划
- `AGENTS.md`：AI/开发协作约定

---

## 1️⃣9️⃣ 最后给新手一句建议
第一次使用时，不要急着调很多参数。

最好的路径是：
1. 先跑通
2. 先看懂输出
3. 再逐步调整
4. 最后再比较不同模板和参数

这样最不容易把自己绕晕。🙂
