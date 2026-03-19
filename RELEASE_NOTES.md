# Release Notes

## ✨ 本次更新亮点
- 新增 `doctor-data` 命令，可诊断当前数据源认证、接口可用性与缓存降级状态
- UI 新增数据源状态展示与一键健康检查
- AkShare / Tushare(Tinyshare) provider 增加健康检查输出结构，便于普通用户和 AI Agent 排查问题
- 错误分类更清晰：区分认证失败、权限不足、缓存降级、网络错误

## 📦 产物
- `ashare-strategy-windows-x86_64.zip`
- 源码包

## 🙌 使用建议
- 如果数据拉取失败，先执行 `ashare-strategy doctor-data --output json`
- 若使用 Tinyshare，请确认 `data_source.tushare_sdk: tinyshare`
- 若 AkShare 出现网络波动，诊断结果会提示是否已退回缓存或完全不可用
