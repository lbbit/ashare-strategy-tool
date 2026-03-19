# 架构梳理与扩展建议

## 1. 当前架构结论
当前项目已经具备“单策略 + 单数据源 + 本地持仓 + CLI/UI + 回测 + 发布自动化”的可运行闭环，适合作为第一版产品原型。

但如果目标是长期演进为：
- 面向普通股民的高可用工具
- 同时支持“纯分析模式”和“量化接入模式”
- 同时支持免费数据源和付费数据源
- 同时支持 CLI / 图形界面 / AI Agent 集成
- 参数、策略、执行、账户同步都可扩展

那么当前架构还需要进一步“解耦”和“分层”。否则后续新增券商、账户、数据源、多个策略、UI 高级交互时，`TradingService` 很容易变成一个过于臃肿的总入口。

## 2. 当前架构的优点
- 目录结构清晰，核心功能已有初步分层
- 配置、数据、策略、回测、执行、UI 已有独立目录
- CLI 与 UI 已可复用同一个服务层
- 缓存、报告导出、持仓持久化都已具备雏形
- 当前开发成本低，迭代速度快

## 3. 当前架构的主要扩展风险

### 3.1 `TradingService` 职责过多
当前 `TradingService` 同时承担：
- 数据提供者初始化
- 策略筛选入口
- 回测入口
- 持仓读写入口

未来一旦加入：
- 多数据源
- 多账户来源
- 多执行通道
- 多策略模板
- 实盘/模拟盘切换

这里会很快膨胀成“大总管类”。

### 3.2 数据源未抽象成统一接口
当前直接绑定 `AkshareProvider`。后续如果接入：
- Tushare
- 聚宽/米筐/JQData
- Wind / iFinD
- 自建 API

则会出现大量 `if provider == xxx` 分支。

### 3.3 账户/持仓模型还停留在本地 JSON 级别
当前只支持本地 JSON 持仓。
未来目标里包含：
- 用户手工录入持仓
- 持仓同步
- 券商/量化 API 读取账户
- 模拟账户和真实账户并存

这说明后续需要“账户适配层”。

### 3.4 策略参数是单一配置模型
目前 `StrategyConfig` 适合单策略。
但后续如果支持：
- 多策略模板
- 用户策略方案保存
- UI 中配置多个策略实例
- 不同数据源有不同认证参数

则需要拆成多个配置域。

### 3.5 UI 技术路线需要提前确定长期方案
当前 Streamlit 非常适合快速验证，但如果未来要实现：
- 更丰富的图标和卡片布局
- 更灵活的交互引导
- 更像桌面工具/产品化界面
- 多页面、多状态管理、多账户切换

那么需要尽早确定是否：
- 继续以 Streamlit 作为“轻量专业版 UI”
- 后续新增独立前端（例如 React/Tauri/Electron）作为“产品化 UI”

结论：**短期继续用 Streamlit，长期建议预留独立前端 API 层。**

### 3.6 CLI 输出尚未完全 Agent-friendly
CLI 当前适合人看，但后续如果要方便 AI Agent 集成，建议逐步增强：
- `--output json`
- `--output csv`
- 稳定字段结构
- 明确 exit code
- 错误信息可机读

## 4. 建议的目标架构
建议逐步演进为以下分层：

### 4.1 config 层
建议拆分为：
- `StrategyConfig`：策略参数
- `DataSourceConfig`：数据源参数、API Key、缓存配置
- `AccountConfig`：账户/持仓来源配置
- `AppConfig`：UI/CLI/默认路径/环境配置

### 4.2 data 层
建议拆成：
- `data/providers/base.py`：统一数据源接口
- `data/providers/akshare.py`：免费数据源实现
- `data/providers/tushare.py`：后续付费数据源实现
- `data/providers/router.py`：根据配置选择数据源
- `data/cache.py`：缓存抽象

这样可以保证数据源扩展时不影响策略层。

### 4.3 accounts 层
新增：
- `accounts/models.py`
- `accounts/repository.py`
- `accounts/providers/manual.py`
- `accounts/providers/json_store.py`
- `accounts/providers/broker_api.py`

目标：
- 普通用户可手工维护持仓
- 后续可无缝切换到真实账户同步

### 4.4 strategy 层
建议未来支持：
- `strategies/base.py`
- `strategies/selector.py`
- `strategies/rules/`
- `strategies/registry.py`

这样可以支持多个策略模板并行。

### 4.5 services 层
将当前 `TradingService` 拆为：
- `ScreeningService`
- `BacktestService`
- `PlanningService`
- `PortfolioService`
- `AccountSyncService`

优点：
- 单一职责
- CLI/UI 更容易按功能调用
- 便于测试

### 4.6 execution 层
建议区分：
- `execution/simulator.py`：模拟执行
- `execution/adapters/base.py`
- `execution/adapters/broker_api.py`

目标：
- 当前先支持建议和模拟
- 后续再接实盘 API，不污染当前逻辑

### 4.7 interface 层
建议未来拆为：
- `interfaces/cli/`
- `interfaces/ui_streamlit/`
- `interfaces/api/`（可选）

原因：
如果未来 UI 独立前后端，就不能继续把入口都堆在单文件里。

## 5. 推荐的近期架构优化动作
这些建议优先级较高，而且不会破坏现有可运行能力。

### P0：马上做
1. 引入“数据源接口抽象”而不是直接写死 `AkshareProvider`
2. 将 `TradingService` 拆分为更细的服务类
3. 将配置拆成多个配置域，至少区分“策略配置”和“数据源配置”
4. CLI 增加机器可读输出模式设计（哪怕先不完全实现）
5. 在 AGENTS.md 中写清长期扩展方向和模块边界

### P1：尽快做
1. 新增账户/持仓抽象层
2. 设计手工持仓与券商账户统一模型
3. 规划 API 层，为后续高级 UI 做准备
4. 统一错误模型与错误码

### P2：后续演进
1. 引入多策略注册机制
2. 增加多数据源优先级和回退机制
3. 增加更强的 UI 技术方案（如独立前端）
4. 增加任务调度、通知、日报推送

## 6. UI 方案建议

### 短期
继续使用 Streamlit，原因：
- 开发快
- 对数据类产品足够友好
- 图表展示方便
- 适合快速迭代参数界面

### 中长期
建议预留 API 化能力，再考虑：
- React + FastAPI + ECharts
- Tauri（桌面版）
- Electron（跨平台桌面）

结论：
- **当前不要急着推翻 Streamlit**
- **但要避免把业务逻辑写死在 Streamlit 页面里**

## 7. 结论
当前架构作为 MVP 是合格的，但如果要承接长期目标，建议尽快朝“接口抽象 + 服务拆分 + 配置拆分 + 账户分层 + API 预留”的方向优化。

最关键的不是立刻引入大量复杂代码，而是先把扩展点留出来，避免后续：
- 数据源难切换
- 券商接口难接
- UI 与业务逻辑耦合
- CLI 不适合 Agent 调用
- 用户配置越来越混乱
