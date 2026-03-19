# Release Notes

## ✨ 本次更新亮点
- 修复 Windows Release 工作流中安装包路径不明确导致的上传失败问题
- `build_windows.py` 现在显式输出版本化 zip 路径，并在未生成产物时直接报错
- Release workflow 改为基于 tag 名拼接固定文件名并用 `gh release upload` 显式上传

## 📦 产物
- `ashare-strategy-windows-x86_64-v0.16.7.zip`
- 源码包

## 🙌 使用建议
- 发布完成后，建议执行 `gh release view v0.16.7 --json assets,url` 确认附件真实存在
- Windows 用户下载后，建议优先验证 `version`、`--help`、`doctor-data`、`init-workspace`、`ui`
- 如果数据源异常，请先运行 `doctor-data`，必要时再尝试 `--offline`
