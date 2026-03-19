# Release Notes

## ✨ 本次更新亮点
- 修复 Windows 打包版 `init-workspace` 仍读取外部 `config/default_strategy.yaml` 导致报错的问题
- 修复 Windows 打包版 `ui` 启动时报 `No such option: -m` 的问题
- 新增运行时路径工具与内置 Streamlit 启动脚本，提升打包版稳定性
- 文档补充 Windows 打包版常见问题与排查建议

## 📦 产物
- `ashare-strategy-windows-x86_64.zip`
- 源码包

## 🙌 使用建议
- Windows 用户升级到本版本后，再重新测试 `init-workspace` 和 `ui`
- 若 `screen` 仍受网络/代理影响，建议先执行 `doctor-data`
- 如本地已有缓存，也可以尝试 `screen --offline`
