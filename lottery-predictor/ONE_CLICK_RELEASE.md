# 🚀 双色球预测软件 - 一键 Release Windows EXE 指南

## 📦 完整打包流程

### 方式一：GitHub Actions 自动构建（推荐）

#### 步骤 1: 准备代码

```bash
cd /home/admin/openclaw/workspace/lottery-predictor

# 确保代码已提交
git add -A
git commit -m "准备发布 v1.0.0"
```

#### 步骤 2: 一键 Release

```bash
# 运行 Release 脚本
./release.sh v1.0.0
```

**或者手动操作：**

```bash
# 创建版本标签
git tag v1.0.0

# 推送到 GitHub
git push origin v1.0.0
```

#### 步骤 3: 等待构建完成

- GitHub Actions 会自动触发构建
- 构建时间：5-10 分钟
- 查看进度：https://github.com/lgffcb/excel-extractor/actions

#### 步骤 4: 下载 Release

- 访问：https://github.com/lgffcb/excel-extractor/releases
- 下载：`SSQ_Predictor_Windows.zip`

---

### 方式二：本地构建

#### Windows 系统

```bash
cd /home/admin/openclaw/workspace/lottery-predictor

# 运行打包脚本
build_exe.bat
```

#### Linux/Mac 系统

```bash
cd /home/admin/openclaw/workspace/lottery-predictor

# 运行打包脚本
./build_exe.sh
```

#### 输出文件

```
dist/
├── SSQ_Predictor.exe      # GUI 界面版
├── SSQ_CLI.exe            # 命令行版
├── SSQ_Update.exe         # 更新工具
└── SSQ_Fetch.exe          # 数据获取工具

release_package/           # 完整发布包
SSQ_Predictor_Windows.zip  # 压缩包
```

---

## 📋 完整文件清单

### GitHub 仓库文件

```
lottery-predictor/
├── .github/
│   └── workflows/
│       └── release.yml       # GitHub Actions 配置 🆕
├── predictor.py              # 预测核心
├── gui.py                    # GUI 界面
├── auto_update.py            # 自动更新
├── data_fetcher.py           # 数据获取
├── fetch_history_17500.py    # 17500 爬虫
├── data/
│   └── historical_data.csv   # 历史数据
├── build_exe.bat             # Windows 打包脚本 🆕
├── build_exe.sh              # Linux 打包脚本 🆕
├── release.sh                # Release 脚本 🆕
├── BUILD_EXE_GUIDE.md        # 打包指南 🆕
└── README.md                 # 使用说明
```

### Release 包内容

```
SSQ_Predictor_Windows.zip
├── SSQ_Predictor.exe      # GUI 界面版（推荐）
├── SSQ_CLI.exe            # 命令行版
├── SSQ_Update.exe         # 更新工具
├── SSQ_Fetch.exe          # 数据获取工具
├── data/
│   └── historical_data.csv
├── README.md
└── requirements.txt
```

---

## 🎯 使用方法

### 普通用户（下载 Release）

1. **下载**
   - 访问 GitHub Releases 页面
   - 下载 `SSQ_Predictor_Windows.zip`

2. **解压**
   - 解压到任意目录

3. **运行**
   ```
   双击 SSQ_Predictor.exe
   ```

4. **预测**
   - 点击"开始预测"
   - 查看预测结果

### 开发者（自行构建）

1. **克隆代码**
   ```bash
   git clone https://github.com/lgffcb/excel-extractor.git
   cd excel-extractor/lottery-predictor
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. **打包**
   ```bash
   ./build_exe.sh  # Linux/Mac
   build_exe.bat   # Windows
   ```

---

## 📊 构建统计

| 项目 | 数值 |
|------|------|
| Python 版本 | 3.10 |
| PyInstaller | 最新 |
| 构建时间 | 5-10 分钟 |
| EXE 大小 | ~50MB/个 |
| 总压缩包 | ~200MB |
| 历史数据 | 3428 期 |

---

## 🔧 高级配置

### 自定义版本号

```bash
# 编辑 release.yml
vi .github/workflows/release.yml

# 修改版本格式
- name: Get version from tag
  run: |
    $version = "${{ github.ref_name }}"
    echo "version=$version" >> $env:GITHUB_OUTPUT
```

### 添加更多工具

```yaml
# 在 release.yml 中添加新的打包步骤
- name: Build EXE - Custom Tool
  run: |
    pyinstaller --onefile --name Custom_Tool custom.py
```

### 修改 Release 说明

编辑 `release.yml` 中的 `body` 部分。

---

## ⚠️ 注意事项

### Windows 兼容性

- ✅ Windows 10/11
- ✅ 需要 .NET Framework 4.5+
- ✅ 64 位系统

### 杀毒软件

- PyInstaller 打包的 EXE 可能被误报
- 添加到杀毒软件白名单
- 或签名后发布

### 数据文件

- 确保 `data/historical_data.csv` 存在
- 与 EXE 在同一目录结构

### 权限问题

- 首次运行可能需要管理员权限
- 数据更新需要写入权限

---

## 🐛 故障排查

### 问题 1：GitHub Actions 未触发

```bash
# 检查标签是否推送
git push origin v1.0.0 --force
```

### 问题 2：构建失败

- 查看 Actions 日志
- 检查依赖版本
- 确保 Python 3.10

### 问题 3：EXE 无法运行

```bash
# 本地测试
python predictor.py

# 重新打包
pip install --upgrade pyinstaller
./build_exe.sh
```

### 问题 4：数据文件找不到

确保目录结构正确：
```
SSQ_Predictor.exe
data/
└── historical_data.csv
```

---

## 📞 快速参考

### 发布新版本

```bash
# 1. 更新代码
git add -A
git commit -m "更新内容"

# 2. 打标签
git tag v1.0.1

# 3. 推送
git push origin v1.0.1

# 4. 等待构建完成
# 5. 下载 Release
```

### 本地测试打包

```bash
# 快速打包测试
pyinstaller --onefile predictor.py

# 测试运行
./dist/predictor
```

---

## 📄 许可证

MIT License

---

**最后更新:** 2026-03-23  
**版本:** v1.0.0  
**构建:** GitHub Actions / 本地打包

🎉 **一键 Release 完成！**
