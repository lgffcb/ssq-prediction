# 🚀 双色球预测软件 - Windows EXE 打包指南

## 📦 一键构建 Release

### 方式一：GitHub Actions（推荐）

1. **打标签并推送**
   ```bash
   cd /home/admin/openclaw/workspace/lottery-predictor
   
   # 创建版本标签
   git tag v1.0.0
   
   # 推送到 GitHub
   git push origin v1.0.0
   ```

2. **自动构建**
   - GitHub Actions 会自动触发构建
   - 约 5-10 分钟后完成
   - 查看进度：https://github.com/lgffcb/excel-extractor/actions

3. **下载 Release**
   - 访问：https://github.com/lgffcb/excel-extractor/releases
   - 下载 `SSQ_Predictor_Windows.zip`

---

### 方式二：本地构建

#### 1. 安装依赖

```bash
# 安装 PyInstaller
pip install pyinstaller pandas numpy scikit-learn scipy matplotlib seaborn
```

#### 2. 运行打包脚本

```bash
cd /home/admin/openclaw/workspace/lottery-predictor

# Windows
build_exe.bat

# Linux/Mac
./build_exe.sh
```

#### 3. 查看输出

```
dist/
├── SSQ_Predictor.exe      # GUI 界面版
├── SSQ_CLI.exe            # 命令行版
├── SSQ_Update.exe         # 更新工具
└── SSQ_Fetch.exe          # 数据获取工具
```

---

## 📁 打包内容

### 包含文件

| 文件 | 说明 | 大小 |
|------|------|------|
| `SSQ_Predictor.exe` | GUI 图形界面版 | ~50MB |
| `SSQ_CLI.exe` | 命令行预测版 | ~50MB |
| `SSQ_Update.exe` | 数据自动更新 | ~50MB |
| `SSQ_Fetch.exe` | 数据获取工具 | ~50MB |
| `data/historical_data.csv` | 历史数据 | 126KB |
| `README.md` | 使用说明 | 5KB |

### 打包后结构

```
SSQ_Predictor_Windows/
├── SSQ_Predictor.exe      # 主程序（GUI）
├── SSQ_CLI.exe            # 命令行版
├── SSQ_Update.exe         # 更新工具
├── SSQ_Fetch.exe          # 数据获取
├── data/
│   └── historical_data.csv
├── README.md
└── requirements.txt
```

---

## 🎯 使用方法

### GUI 界面版（推荐）

1. 双击运行 `SSQ_Predictor.exe`
2. 点击"开始预测"
3. 查看预测结果

### 命令行版

```bash
# 预测号码
SSQ_CLI.exe

# 更新数据
SSQ_Update.exe

# 获取数据
SSQ_Fetch.exe
```

---

## 🔧 自定义版本

### 修改版本号

编辑 `.github/workflows/release.yml`:

```yaml
- name: Get version from tag
  id: get_version
  run: |
    $version = "${{ github.ref_name }}"
    echo "version=$version" >> $env:GITHUB_OUTPUT
```

### 修改 Release 说明

编辑 `release.yml` 中的 `body` 部分。

---

## 📊 构建统计

| 项目 | 数值 |
|------|------|
| Python 版本 | 3.10 |
| PyInstaller 版本 | 最新 |
| 构建时间 | 5-10 分钟 |
| EXE 大小 | ~50MB 每个 |
| 总压缩包大小 | ~200MB |

---

## ⚠️ 注意事项

1. **Windows 兼容性**
   - 支持 Windows 10/11
   - 需要 .NET Framework 4.5+

2. **杀毒软件**
   - 可能误报（PyInstaller 打包常见问题）
   - 添加到白名单即可

3. **数据文件**
   - 确保 `data/historical_data.csv` 存在
   - 与 EXE 在同一目录或子目录

4. **权限问题**
   - 首次运行可能需要管理员权限
   - 数据更新需要写入权限

---

## 🐛 故障排查

### 问题 1：EXE 无法运行

```bash
# 检查依赖
python -m PyInstaller --version

# 重新打包
pip install --upgrade pyinstaller
```

### 问题 2：缺少 DLL

```bash
# 添加隐藏导入
pyinstaller --hidden-import=sklearn.utils.murmurhash ...
```

### 问题 3：数据文件找不到

```python
# 在代码中添加
import sys
import os

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
```

---

## 📞 常用命令

### 本地测试打包

```bash
# 测试单个文件
pyinstaller --onefile predictor.py

# 测试带数据文件
pyinstaller --onefile --add-data "data/historical_data.csv;data" predictor.py
```

### 创建 Release

```bash
# 打标签
git tag v1.0.0

# 推送标签
git push origin v1.0.0

# 查看标签
git tag -l
```

---

## 📄 许可证

MIT License

---

**最后更新:** 2026-03-23  
**版本:** v1.0.0  
**构建:** GitHub Actions
