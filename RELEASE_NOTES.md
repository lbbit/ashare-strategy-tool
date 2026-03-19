# Release Notes

## ✨ 本次更新亮点
- 继续修复 Windows 打包版 UI 启动逻辑，改为使用独立的内置 Streamlit 启动器
- `screen` 失败时也会输出更友好的数据源诊断提示，不再直接抛出一大段异常
- 全面重写 `docs/USER_GUIDE.md`，补充：模板怎么选、配置怎么改、持仓文件怎么填、输出文件各代表什么
- README、功能状态、开发计划、AGENTS 文档同步更新

## 📦 产物
- `ashare-strategy-windows-x86_64-v0.16.3.zip`
- 源码包

## 🙌 使用建议
- 如果你购买的是 Tinyshare 授权码，请务必使用 `provider: tushare` + `tushare_sdk: tinyshare` 的配置文件运行
- 如果 `screen` 失败，请先执行 `doctor-data`，再确认是否仍在使用默认 `akshare` 配置
- Windows 用户升级后，请重新验证 `ui`、`screen`、`init-workspace`、`version`
