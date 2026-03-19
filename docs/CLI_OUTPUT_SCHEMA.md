# CLI 输出字段说明

## 统一 JSON 包装结构
当命令使用 `--output json` 时，优先返回以下结构：

```json
{
  "status": "success",
  "message": "...",
  "data": ...
}
```

错误时：

```json
{
  "status": "error",
  "message": "错误说明",
  "data": null
}
```

## 各命令说明

### `screen --output json`
- `data`: 候选股票数组
- 每个元素通常包含：
  - `stock_code`
  - `stock_name`
  - 其他筛选结果字段

### `positions --output json`
- `data`: 当前持仓数组
- 每个元素通常包含：
  - `stock_code`
  - `stock_name`
  - `buy_date`
  - `buy_price`
  - `shares`

### `plan --output json`
- `data.summary`: 计划摘要
- `data.buy_candidates`: 候选买入清单
- `data.hold_positions`: 当前持仓
- `data.sell_review`: 卖出复核清单

### `backtest --output json`
- `data.strategy_return`
- `data.benchmark_return`
- `data.excess_return`
- `data.max_drawdown`
- `data.trades`
- `data.equity_curve`
- `data.metrics`

### `init-account --output json`
- `data`: 初始化后的示例持仓列表

### `init-workspace --output json`
- `data.positions_initialized`: 是否已初始化持仓
- `data.output_dir`: 初始化的工作目录
- `data.files`: 新生成的文件列表
