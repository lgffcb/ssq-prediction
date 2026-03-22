# Excel 数据提取工具

自动提取 Excel 明细表数据的工具。

## 功能

- ✅ 自动显示隐藏的 Excel 工作表
- ✅ 取消隐藏的行和列
- ✅ 将公式转换为数值
- ✅ 自动查找包含"明细"的工作表
- ✅ 搜索匹配内容并动态提取相关列

## 使用方法

### 方式 1：直接运行 Python 脚本

```bash
# 安装依赖
pip install pandas openpyxl

# 运行脚本
python excel_search_extract.py
```

### 方式 2：下载打包好的 EXE（Windows）

1. 访问 [Releases](https://github.com/你的用户名/excel-extractor/releases)
2. 下载最新版本的 `ExcelExtractor.exe`
3. 双击运行

### 方式 3：自己打包 EXE

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --name ExcelExtractor excel_search_extract.py

# EXE 文件在 dist/ExcelExtractor.exe
```

## 自动打包

本项目配置了 GitHub Actions，每次推送标签时会自动打包 Windows EXE：

```bash
# 打标签触发打包
git tag v1.0.0
git push origin v1.0.0
```

打包完成后在 [Releases](https://github.com/你的用户名/excel-extractor/releases) 下载。

## 使用示例

```
============================================================
Excel 数据提取工具 - 明细表专用 (命令行版)
============================================================

📂 请输入 Excel 文件路径：C:\Users\你的用户名\Downloads\你的文件.xlsx

🔧 正在处理 Excel 文件...
   ✅ 显示了 1 个隐藏的工作表
   ✅ 取消了 2 个隐藏行
   ✅ 取消了 2 个隐藏列
   ✅ 公式已转换为数值

🔍 请输入要查找的内容：张三

✅ 找到 2 条匹配记录

================================================================================
查找内容：张三
明细工作表：明细表
匹配行数：2
================================================================================
 B 列  O 列
 张三 NaN
NaN  张三
================================================================================

✅ 结果已保存到：你的文件_提取结果.xlsx
```

## 输出说明

- 动态提取包含查找内容的列
- 结果保存为 `原文件名_提取结果.xlsx`
- 同时生成处理后的文件 `原文件名_processed.xlsx`

## 许可证

MIT License
