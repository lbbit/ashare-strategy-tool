# 👶 A股策略工具完整新手指南

> 如果你是第一次接触这个工具，请把它理解成：
> **一个帮你做选股、回测、持仓记录、每日复盘和交易计划整理的辅助工具。**
>
> 它不是自动下单软件，而是帮助你把“每天看盘、记笔记、盯持仓”的过程标准化。

---

# 1. 你到底应该怎么用这个工具？

最简单的理解：

| 你想做什么 | 该用什么命令 |
|---|---|
| 看今天有哪些候选股 | `screen` |
| 看我的持仓文件长什么样 | `positions` |
| 先生成一个可修改的持仓样例 | `init-account` |
| 初始化整个工作目录 | `init-workspace` |
| 生成今天的交易计划 | `plan` |
| 看历史回测表现 | `backtest` |
| 用图形界面操作 | `ui` |
| 检查数据源是否正常 | `doctor-data` |
| 看当前软件版本 | `version` |

### 推荐新手使用顺序
第一次建议按这个顺序：

1. `version`
2. `init-workspace`
3. `init-account`
4. 修改持仓文件
5. `positions`
6. `screen`
7. `plan`
8. `backtest`
9. `ui`

---

# 2. 第一步：先确认你运行的是哪个版本

```bash
ashare-strategy version
```

Windows 打包版：
```powershell
.\ashare-strategy.exe version
```

用途：
- 确认你是不是最新版本
- 排查“为什么我这里命令不一样”
- 方便和 Release 页面对应

---

# 3. 第二步：初始化工作目录

```bash
ashare-strategy init-workspace
```

执行后默认会生成一个目录：
- `workspace_init/`

里面通常会有这些内容：

| 文件/目录 | 作用 | 你是否需要修改 |
|---|---|---|
| `README.txt` | 初始化目录的简短说明 | 一般不用 |
| `custom_strategy.yaml` | 当前基础配置副本 | 建议按需修改 |
| `beginner_strategy.yaml` | 新手模板配置 | 可直接使用/微调 |
| `conservative_strategy.yaml` | 稳健模板配置 | 可直接使用/微调 |
| `aggressive_strategy.yaml` | 激进模板配置 | 可直接使用/微调 |
| `reports/` | 回测报告输出目录 | 不用手动建 |
| `daily_plan/` | 每日计划输出目录 | 不用手动建 |

### 你应该怎么理解这些模板文件？

| 模板文件 | 风格 | 适合谁 |
|---|---|---|
| `beginner_strategy.yaml` | 参数均衡 | 第一次使用的新手 |
| `conservative_strategy.yaml` | 偏稳健 | 更看重控制波动的用户 |
| `aggressive_strategy.yaml` | 偏激进 | 能接受更大波动的用户 |
| `custom_strategy.yaml` | 当前基础配置副本 | 想自己长期维护一套配置的人 |

---

# 4. 模板到底怎么用？

## 方法 A：命令行里直接指定模板名

```bash
ashare-strategy screen --template beginner
ashare-strategy plan --template conservative
ashare-strategy backtest --template aggressive
```

### `--template` 可选值

| 值 | 含义 |
|---|---|
| `beginner` | 新手均衡模板 |
| `conservative` | 稳健模板 |
| `aggressive` | 激进模板 |
| `custom` | 不额外套模板，完全按配置文件本身运行 |

> 注意：`screen custom` 这种写法是错的。  
> 正确写法是：
> ```bash
> ashare-strategy screen --template custom
> ```

## 方法 B：直接指定某个模板配置文件

如果你已经初始化了工作目录，也可以直接用某个 yaml 文件：

```bash
ashare-strategy screen --config workspace_init/beginner_strategy.yaml
ashare-strategy plan --config workspace_init/conservative_strategy.yaml
ashare-strategy backtest --config workspace_init/aggressive_strategy.yaml
```

## 方法 C：图形界面里选择模板
在 UI 左侧边栏选择：
- `beginner`
- `conservative`
- `aggressive`

---

# 5. 第三步：初始化持仓文件

```bash
ashare-strategy init-account
```

执行后，会在默认位置生成持仓文件：
- `data/positions.json`

## 这个文件是干什么的？
它是你当前持仓的本地记录。

程序会用它来：
- 展示你的持仓
- 生成每日计划里的持仓部分
- 帮你区分哪些票已持有、哪些是新的候选股

---

# 6. 持仓文件应该怎么改？

默认示例内容大致像这样：

```json
[
  {
    "stock_code": "000001",
    "stock_name": "示例股票",
    "buy_date": "2026-03-18",
    "buy_price": 12.34,
    "shares": 1000
  }
]
```

## 每个字段是什么意思？

| 字段 | 含义 | 示例 | 必填 | 说明 |
|---|---|---|---|---|
| `stock_code` | 股票代码 | `000001` | 是 | 不带 `.SZ/.SH` |
| `stock_name` | 股票名称 | `平安银行` | 建议填 | 便于你自己看懂 |
| `buy_date` | 买入日期 | `2026-03-18` | 建议填 | 格式建议 `YYYY-MM-DD` |
| `buy_price` | 买入价格 | `12.34` | 建议填 | 用于参考 |
| `shares` | 持股数量 | `1000` | 是 | 持仓股数 |

## 一个更真实的例子

```json
[
  {
    "stock_code": "000001",
    "stock_name": "平安银行",
    "buy_date": "2026-03-10",
    "buy_price": 11.82,
    "shares": 2000
  },
  {
    "stock_code": "600519",
    "stock_name": "贵州茅台",
    "buy_date": "2026-03-15",
    "buy_price": 1688.50,
    "shares": 100
  }
]
```

## 修改后如何检查？

```bash
ashare-strategy positions
```

如果想看 JSON 格式输出：

```bash
ashare-strategy positions --output json
```

---

# 7. 第四步：看今天候选股

```bash
ashare-strategy screen
```

如果你想直接套模板：

```bash
ashare-strategy screen --template beginner
```

如果你想使用某个具体配置文件：

```bash
ashare-strategy screen --config workspace_init/beginner_strategy.yaml
```

## 如果失败怎么办？
现在 `screen` 失败时会自动提示：
- 当前数据源状态
- 建议执行 `doctor-data`

---

# 8. 第五步：生成每日交易计划

```bash
ashare-strategy plan --output-dir daily_plan
```

运行后通常会生成这些文件：

| 文件名 | 作用 |
|---|---|
| `summary.csv` | 今日计划摘要 |
| `buy_candidates.csv` | 今日可关注的候选股 |
| `hold_positions.csv` | 当前持仓清单 |
| `sell_review.csv` | 今日需要复核的卖出清单 |

## 这些文件怎么理解？

### `summary.csv`
告诉你今天大概有：
- 几个候选股
- 几个可买入关注对象
- 几个持仓
- 几个需要卖出复核的项目

### `buy_candidates.csv`
表示：
- 今天值得重点看的候选票
- 不等于必须买
- 是待你进一步判断的名单

### `hold_positions.csv`
表示：
- 当前持仓列表
- 来自你的 `positions.json`

### `sell_review.csv`
表示：
- 需要你人工复核是否应该卖出的项目
- 不等于程序已经帮你做出最终决定

---

# 9. 第六步：做历史回测

```bash
ashare-strategy backtest --mode rolling --export-report-dir reports
```

执行后通常会导出：

| 文件名 | 作用 |
|---|---|
| `candidates.csv` | 回测过程中出现的候选股 |
| `trades.csv` | 交易记录 |
| `equity_curve.csv` | 净值曲线 |
| `metrics.csv` | 绩效指标 |

## 常见指标怎么理解？

| 指标 | 含义 |
|---|---|
| `annualized_return` | 年化收益 |
| `volatility` | 波动率 |
| `sharpe_ratio` | 夏普比率 |
| `max_drawdown` | 最大回撤 |
| `win_rate` | 胜率 |
| `profit_loss_ratio` | 盈亏比 |

---

# 10. 配置文件到底该怎么改？

默认配置文件示例：
- `config/default_strategy.yaml`
- 或初始化后的 `workspace_init/*.yaml`

## 最关键参数说明

| 参数 | 含义 | 常见值建议 | 可选说明 |
|---|---|---|---|
| `data_source.provider` | 数据源类型 | `akshare` / `tushare` | 免费默认用 `akshare` |
| `data_source.tushare_sdk` | Tushare 后端 SDK | `tushare` / `tinyshare` | 用 Tinyshare 授权码时改成 `tinyshare` |
| `data_source.tushare_token` | token/授权码 | 字符串 | 官方 Tushare token 或 Tinyshare 授权码 |
| `data_source.use_cache` | 是否启用缓存 | `true` | 建议保持开启 |
| `data_source.offline_mode` | 是否离线模式 | `false` / `true` | `true` 时仅走缓存 |
| `lookback_days` | 回看历史天数 | `240~500` | 越大历史越长 |
| `rebalance_interval` | 调仓周期 | `5/7/10` | 越小调仓越频繁 |
| `max_positions` | 最多持股数 | `2/3/5` | 越大越分散 |
| `hold_days` | 最大持有天数 | `3/5/7` | 越小越偏短线 |
| `first_day_gain_pct` | 首日涨幅阈值 | `5~8` | 越大筛选越严格 |

---

# 11. 如果你使用的是 Tinyshare，应该怎么配？

```yaml
data_source:
  provider: tushare
  tushare_sdk: tinyshare
  tushare_token: "你的授权码"
```

### 很重要
如果你已经买了 Tinyshare，但仍然使用默认 `akshare` 配置，
那程序当然还是会去访问 AkShare，而不是 Tinyshare。

也就是说：
> 你要想用 Tinyshare，必须显式改配置文件，或者指定一个使用 Tinyshare 的配置文件。

---

# 12. 我明明买了 Tinyshare，为什么 `screen` 还是失败？
因为你当前可能还是：
- 用的默认配置
- 默认配置里的 `data_source.provider: akshare`

### 正确做法
先准备一个配置文件，例如：

```yaml
data_source:
  provider: tushare
  tushare_sdk: tinyshare
  tushare_token: "你的授权码"
  use_cache: true
  offline_mode: false
```

然后运行：

```bash
ashare-strategy doctor-data --config your_tinyshare.yaml
ashare-strategy screen --config your_tinyshare.yaml
```

---

# 13. 第七步：数据源检查

```bash
ashare-strategy doctor-data
```

它会告诉你：
- 当前数据源是谁
- 当前 SDK 是什么
- token/授权码是否有效
- 核心接口能不能访问
- 是否已经退回缓存

这是排查问题时最推荐先跑的命令。

---

# 14. 第八步：离线模式

如果免费源不稳定，或者你只想用本地缓存：

```bash
ashare-strategy screen --offline
ashare-strategy plan --offline
ashare-strategy backtest --offline
```

### 注意
离线模式只会读缓存。
如果缓存本来就没有，对应命令还是会失败，但会明确告诉你“缓存缺失”。

---

# 15. 第九步：图形界面怎么用？

```bash
ashare-strategy ui
```

UI 里建议这样操作：
1. 先选模板
2. 看左侧参数说明
3. 先执行选股
4. 再执行回测
5. 遇到问题先看数据源状态

---

# 16. 常见错误与含义

| 提示 | 含义 | 你该怎么做 |
|---|---|---|
| `token 不对，请确认` | token/授权码无效 | 检查 token 或 SDK 是否正确 |
| `没有接口访问权限` | token 有效但权限不足 | 换有权限的接口或账号 |
| `RemoteDisconnected` | 网络/上游中断 | 先跑 `doctor-data` |
| `ProxyError` | 代理/网络配置异常 | 检查本机代理设置 |
| `离线模式已启用，且本地缓存缺失` | 你开了离线模式，但没缓存 | 先联网成功跑一次再离线 |

---

# 17. 给普通用户的最终建议

如果你是普通用户，最推荐这样用：

### 第一次
1. `version`
2. `init-workspace`
3. `init-account`
4. 改好持仓文件
5. `positions`
6. `screen`

### 日常使用
1. `screen`
2. `plan`
3. 必要时 `backtest`

### 数据源出问题时
1. `doctor-data`
2. 如果已有缓存，再尝试 `--offline`

---

# 18. 文档导航
- `README.md`：项目总览
- `docs/FEATURE_STATUS.md`：已实现功能总表
- `docs/DEVELOPMENT_PLAN.md`：后续路线
- `docs/DATA_PROVIDER_RESEARCH.md`：数据源方案调研
- `AGENTS.md`：AI/开发协作说明
