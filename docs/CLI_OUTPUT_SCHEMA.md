# CLI 输出字段说明

## 统一 JSON 包装结构
当命令使用 `--output json` 时，优先返回以下结构：

```json
{
  "schema_version": "1.0",
  "status": "success",
  "message": "...",
  "data": ...
}
```

错误时：

```json
{
  "schema_version": "1.0",
  "status": "error",
  "message": "错误说明",
  "data": null
}
```

## 稳定性约定
1. `schema_version` / `status` / `message` / `data` 为统一外层字段，后续应尽量保持稳定
2. 已文档化字段如无必要不要随意改名
3. 新增字段尽量采用向后兼容方式扩展，不破坏既有 Agent / 脚本解析
4. 如需破坏性修改，应同步更新本文件、README、USER_GUIDE、AGENTS.md

## 各命令说明

### `screen --output json`
- `data`: 候选股票数组

### `positions --output json`
- `data`: 当前持仓数组

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
- `data.directories`: 新生成的目录列表
