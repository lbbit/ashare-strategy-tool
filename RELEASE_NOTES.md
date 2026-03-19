# Release Notes

## ✨ 本次更新亮点
- 为 `Tinyshare/Tushare` 增加 capability-aware 的轻量筛选降级路径，不再强依赖 AkShare 的板块/实时接口
- 补强账户快照与计划建议链路，`positions` / `plan` 能更好反映现金、持仓市值、可卖数量与预算信息
- 修复 Windows 打包版 UI 启动器定位问题，并补充 `tinyshare` 打包依赖，提升实机可用性
- 同步更新 README、新手指南、功能状态与开发计划，明确 AkShare 与 Tinyshare 的推荐使用姿势

## 📦 产物
- `ashare-strategy-windows-x86_64-v0.16.8.zip`
- 源码包

## 🙌 使用建议
- 推荐优先使用 Tinyshare 作为稳定模式：先执行 `doctor-data`，再使用 `screen` / `plan` / `backtest`
- 发布完成后，执行 `gh release view v0.16.8 --json assets,url` 确认附件真实存在
- Windows 用户下载后，建议重点验证 `version`、`--help`、`ui`、`doctor-data --config ...`、`screen --config ...`
