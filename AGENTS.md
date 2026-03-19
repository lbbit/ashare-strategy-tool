# AGENTS.md

## 项目目标
A 股策略选股、回测、每日交易计划、持仓分析、CLI、Web UI、Windows 打包与 GitHub Release 自动化工具。

长期目标：
1. 支持普通股民通过手工输入持仓完成分析、换仓建议和持仓同步
2. 后续支持量化 API / 券商 API 接入，实现账户读取与交易执行扩展
3. 支持免费数据源与付费/API Key 数据源并存
4. 支持用户自定义参数、策略模板和多种交互方式
5. CLI 对 AI Agent 友好，UI 对普通用户友好

## 当前架构
- `src/ashare_strategy/core/`：配置与基础模型
- `src/ashare_strategy/data/`：当前数据抓取与缓存层
- `src/ashare_strategy/accounts/`：账户/持仓抽象层，为手工持仓和 API 账户预留扩展点
- `src/ashare_strategy/strategies/`：策略筛选逻辑
- `src/ashare_strategy/backtest/`：回测与绩效分析
- `src/ashare_strategy/execution/`：当前交易服务与持仓持久化
- `src/ashare_strategy/planner.py`：每日交易计划与导出
- `src/ashare_strategy/reporting.py`：报告导出
- `src/ashare_strategy/services/`：筛选、回测、持仓、规划等服务拆分层
- `src/ashare_strategy/ui/`：Streamlit 界面
- `tests/`：单元测试
- `docs/`：开发计划、架构建议、功能状态、详细使用说明
- `.github/workflows/`：测试、构建、发布自动化

## 推荐演进方向
为避免后续难扩展，后续开发优先朝以下方向推进：
1. 抽象统一数据源接口，不将业务逻辑绑定在单一 `AkshareProvider`
2. 将当前 `TradingService` 拆分为更细的服务类
3. 逐步引入账户/持仓抽象层，兼容手工持仓和 API 账户
4. 将配置拆分为策略配置、数据源配置、应用配置
5. 保持 UI 与业务逻辑解耦，为未来更强的前端方案预留空间
6. 增强 CLI 的稳定 JSON 输出，方便 AI Agent 集成

## 开发约定
1. 每次新增功能后：
   - 更新 `docs/FEATURE_STATUS.md`
   - 更新 `docs/USER_GUIDE.md`
   - 如涉及架构变化，更新本文件
   - 如涉及路线变化，更新 `docs/DEVELOPMENT_PLAN.md`
2. 每完成一个较完整功能集：
   - 补测试
   - 更新 README 引用
   - 提交 tag
   - 编写 GitHub Release 说明
3. GitHub 操作优先使用 SSH remote。
4. 如果新增运行时产物，避免直接提交真实数据文件，优先提交 example 文件或 `.gitkeep`。
5. 文档必须兼顾两类用户：
   - 普通用户：关心怎么装、怎么用、能解决什么问题
   - AI/开发者：关心架构、约束、模块边界、扩展方式

## 当前阶段重点
- 架构升级：服务拆分、数据源抽象、账户抽象、配置分层
- 保持 CLI / UI 易用性
- 保持 Windows 发布链路稳定
- 提高对普通用户和 AI Agent 的可用性
