# 详细使用说明

## 1. 项目简介
本工具用于实现 A 股板块筛选、个股筛选、回测分析、持仓持久化、CLI 与 Web UI 操作。

## 2. 安装方式
### 2.1 源码安装
```bash
git clone git@github.com:lbbit/ashare-strategy-tool.git
cd ashare-strategy-tool
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 2.2 Windows 打包版本
在 GitHub Releases 中下载 `ashare-strategy-tool-windows-x86_64.zip`，解压后运行可执行文件。

## 3. 配置说明
默认配置文件：`config/default_strategy.yaml`

主要参数：
- `board_ma_window`：板块均线窗口
- `board_min_volume`：板块成交量阈值
- `stock_float_cap_max`：流通股上限
- `first_day_gain_pct`：首日阳线涨幅阈值
- `buy_ma_window` / `sell_ma_window`：买卖均线参数
- `hold_days`：最大持有天数
- `rebalance_interval`：调仓周期
- `commission_rate` / `stamp_duty_rate` / `slippage_rate`：交易成本
- `position_store_path`：持仓文件路径
- `use_cache`：是否启用缓存

## 4. CLI 使用
### 4.1 选股
```bash
ashare-strategy screen
```

### 4.2 回测
```bash
ashare-strategy backtest --mode rolling
ashare-strategy backtest --mode rolling --export-csv trades.csv
```

### 4.3 持仓管理
```bash
ashare-strategy positions
ashare-strategy save-sample-positions
```

### 4.4 启动 Web UI
```bash
ashare-strategy ui
```

## 5. Web UI 功能
- 策略参数调整
- 一键选股
- 一键回测
- 指标卡片展示
- 净值曲线展示
- 候选股与交易记录展示

## 6. 回测指标说明
- 策略收益
- 基准收益
- 超额收益
- 最大回撤
- 年化收益
- 波动率
- 夏普比率
- 胜率
- 盈亏比

## 7. 持仓文件
默认位置：`data/positions.json`
可用于保存外部调仓结果或模拟盘持仓。

## 8. 发布与下载
- Release 页面提供源码包和 Windows x86_64 打包包
- 每次 tag 发布都会自动触发 GitHub Actions 构建与上传

## 9. 报告导出
```bash
ashare-strategy backtest --mode rolling --export-report-dir reports
```
导出内容包括：
- candidates.csv
- trades.csv
- equity_curve.csv
- metrics.csv

## 10. Windows 打包说明
项目在 GitHub tag 发布后，会自动通过 GitHub Actions 构建 Windows x86_64 包并上传到 Release。

## 11. 注意事项
- 实时数据依赖 AkShare 与上游数据接口，若网络异常或接口限流，CLI/回测可能失败。
- 建议开启缓存，并在网络稳定时先预热数据。
