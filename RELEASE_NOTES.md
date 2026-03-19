# Release Notes

## ✨ 本次更新亮点
- 提升 AkShare 免费数据源可靠性：增加重试与缓存降级能力
- 新增 `TushareProvider` 与配置化 token 支持，为更稳定数据源接入打基础
- 默认配置支持持久化保存数据源认证信息与重试参数
- 文档新增 Tushare 权限说明与数据源适配建议

## 📦 产物
- `ashare-strategy-windows-x86_64.zip`
- 源码包

## 🙌 使用建议
- 默认继续使用 AkShare 体验，但若网络波动可受益于缓存与重试增强
- 如果切换到 Tushare Pro，请在配置中填写 `data_source.tushare_token`
- 注意：Tushare token 有效不代表所有接口都有权限，需结合账号权限等级判断
