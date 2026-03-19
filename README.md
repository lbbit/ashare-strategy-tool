# A股选股策略工具

支持 A 股板块筛选、个股形态筛选、回测、CLI 运行与 Streamlit 图形界面。

## 功能概览
- 自动抓取 A 股板块与个股行情数据（AkShare）
- 参数化策略配置
- 基于规则的选股、买入、卖出与持仓管理
- 逐日滚动回测、净值曲线、最大回撤与沪深300对比
- CLI 命令行工具
- Streamlit 可视化界面
- 项目开发计划与功能进度文档

## 快速开始
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
ashare-strategy backtest --mode rolling --export-csv trades.csv
ashare-strategy ui
```

## 目录结构
- `src/ashare_strategy/` 核心源码
- `docs/DEVELOPMENT_PLAN.md` 开发计划
- `docs/FEATURE_STATUS.md` 已完成功能表
- `config/default_strategy.yaml` 默认策略参数

## 说明
1. 默认数据源为 `akshare`，不同接口字段可能随上游变化而调整。
2. 板块成交量字段在不同数据源量纲可能不同，已参数化处理。
3. 实盘下单接口未直接接券商，当前提供信号与模拟持仓管理框架，便于后续扩展。

## CLI 示例
```bash
ashare-strategy screen
ashare-strategy backtest --mode rolling
ashare-strategy backtest --mode rolling --export-csv trades.csv
ashare-strategy ui
```

## 当前能力边界
- 当前实盘部分仍为模拟持仓/信号执行框架，未直连券商交易接口。
- 回测为规则型日线回测，暂未计入手续费、滑点、涨跌停成交限制。

## 新增能力
- 交易成本：支持佣金、印花税、滑点参数
- 绩效指标：年化收益、波动率、夏普、胜率、盈亏比、最大回撤
- 持仓持久化：支持本地 JSON 持仓文件读写
- CLI 持仓命令：查看/写入示例持仓

## 文档
- [详细使用说明](docs/USER_GUIDE.md)
- [开发计划](docs/DEVELOPMENT_PLAN.md)
- [功能状态](docs/FEATURE_STATUS.md)
- [AI 开发说明](AGENTS.md)
