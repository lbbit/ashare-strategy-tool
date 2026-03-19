# Release Notes

## ✨ 本次更新亮点
- 新增账户/持仓抽象层，为手工持仓、JSON 持仓、未来 API 账户接入打基础
- `plan` 与 `positions` 命令增强结构化输出能力，更适合 AI Agent 和自动化脚本集成
- 配置中增加账户提供者字段，为后续多账户来源扩展预留接口
- 同步更新功能状态、使用说明、AI 开发文档

## 📦 产物
- `ashare-strategy-windows-x86_64.zip`
- 源码包

## 🙌 使用建议
- 普通用户继续使用默认文本输出
- 自动化用户可使用 `plan --output json` 和 `positions --output json`
- 后续版本将继续推进配置分层和账户同步能力
