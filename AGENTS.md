# AGENTS.md

## 项目目标
A 股策略选股、回测、信号执行、CLI、Web UI、Windows 打包与 GitHub Release 自动化工具。

## 当前架构
- `src/ashare_strategy/core/`：配置与基础模型
- `src/ashare_strategy/data/`：AkShare 数据抓取与 CSV 缓存
- `src/ashare_strategy/strategies/`：板块/个股筛选逻辑
- `src/ashare_strategy/backtest/`：简化回测、滚动回测、绩效分析
- `src/ashare_strategy/execution/`：交易服务与持仓持久化
- `src/ashare_strategy/ui/`：Streamlit 界面
- `tests/`：单元测试
- `docs/`：开发计划、功能状态、详细使用说明
- `.github/workflows/`：测试、构建、发布自动化

## 开发约定
1. 每次新增功能后：
   - 更新 `docs/FEATURE_STATUS.md`
   - 更新 `docs/USER_GUIDE.md`
   - 如涉及架构变化，更新本文件
2. 每完成一个较完整功能集：
   - 补测试
   - 更新 README 引用
   - 提交 tag
   - 编写 GitHub Release 说明
3. GitHub 操作优先使用 SSH remote。
4. 如果新增运行时产物，避免直接提交真实数据文件，优先提交 example 文件或 `.gitkeep`。

## 下一步重点
- 更真实的交易制度约束
- 报告导出
- Windows 可执行包
- Release 自动化
