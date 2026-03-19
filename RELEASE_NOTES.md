# Release Notes

## ✨ 本次更新亮点
- 修复 GitHub Release 工作流在 Windows runner 上未匹配到版本化 zip 的问题
- 新增上传前产物列表输出，方便直接从日志确认 Windows 安装包是否已生成
- 补充 AGENTS 与功能状态文档，明确“workflow success 不等于 release assets 已存在”的发布校验约束

## 📦 产物
- `ashare-strategy-windows-x86_64-v0.16.4.zip`
- 源码包

## 🙌 使用建议
- 发布完成后，除了看 Actions 成功，还应执行 `gh release view v0.16.4 --json assets,url` 确认附件真实存在
- Windows 用户下载后，建议优先验证 `version`、`--help`、`doctor-data`、`init-workspace`、`ui`
- 如果数据源异常，请先运行 `doctor-data`，必要时再尝试 `--offline`
