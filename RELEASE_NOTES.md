# Release Notes

## ✨ 本次更新亮点
- `TushareProvider` 新增 SDK 后端切换能力，支持 `tushare` 与 `tinyshare`
- 已验证 Tinyshare 授权码可用，并以最小流量测试通过 `index_daily` / `daily` / `trade_cal`
- 配置文件新增 `data_source.tushare_sdk`，支持持久化保存 SDK 选择
- 文档补充 Tinyshare 与官方 Tushare token/权限差异说明

## 📦 产物
- `ashare-strategy-windows-x86_64.zip`
- 源码包

## 🙌 使用建议
- 如果你购买的是 Tinyshare 授权码，请配置 `data_source.provider: tushare`
- 同时设置 `data_source.tushare_sdk: tinyshare`
- 将授权码填写到 `data_source.tushare_token`
