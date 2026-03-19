# Release Notes

## ✨ 本次更新亮点
- `screen` / `backtest` / `plan` 新增 `--offline` 仅缓存模式，网络不稳定时可避免主动联网
- 业务命令失败时会自动附带数据源诊断信息与友好提示，帮助快速区分网络、认证、权限、缓存问题
- 新增 `provider_diagnostics` 与 `hint` 结构化错误输出，方便 AI Agent 和脚本集成
- 配置文件支持持久化 `data_source.offline_mode`

## 📦 产物
- `ashare-strategy-windows-x86_64.zip`
- 源码包

## 🙌 使用建议
- 如果当天网络差，可优先尝试 `ashare-strategy backtest --offline`
- 若命令失败，请查看返回中的 `provider_diagnostics` 和 `hint`
- 建议结合 `ashare-strategy doctor-data` 一起排查数据源问题
