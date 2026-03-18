# A股选股策略工具

支持 A 股板块筛选、个股形态筛选、回测、CLI 运行与 Streamlit 图形界面。

## 功能概览
- 自动抓取 A 股板块与个股行情数据（AkShare）
- 参数化策略配置
- 基于规则的选股、买入、卖出与持仓管理
- 1 年期回测与沪深300对比
- CLI 命令行工具
- Streamlit 可视化界面
- 项目开发计划与功能进度文档

## 快速开始
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
ashare-strategy backtest --days 250
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
