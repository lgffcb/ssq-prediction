# GitHub Actions 自动打包 Windows EXE 指南

## 步骤 1：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`excel-extractor`（或你喜欢的名字）
3. 设为 **Public** 或 **Private**（Private 需要 GitHub Pro 才能使用 Actions）
4. 点击"Create repository"

## 步骤 2：上传代码到 GitHub

### 方法 A：使用 Git 命令行（推荐）

在终端执行以下命令：

```bash
# 替换为你的 GitHub 用户名
git remote add origin https://github.com/你的用户名/excel-extractor.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 方法 B：使用 GitHub Desktop

1. 下载：https://desktop.github.com/
2. 添加本地仓库：File → Add Local Repository
3. 选择 `/home/admin/openclaw/workspace` 文件夹
4. 点击"Publish repository"

### 方法 C：直接上传文件

1. 在 GitHub 仓库页面点击"uploading an existing file"
2. 拖拽以下文件：
   - `excel_search_extract.py`
   - `README.md`
   - `build-windows.bat`
   - `.gitignore`
   - `.github/workflows/build-windows.yml`（需要先创建 .github/workflows 文件夹）
3. 点击"Commit changes"

## 步骤 3：启用 GitHub Actions

1. 在 GitHub 仓库页面，点击 **Actions** 标签
2. 如果是第一次使用，点击 **I understand my workflows, go ahead and enable them**
3. 你会看到 "Build Windows EXE" 工作流

## 步骤 4：触发自动打包

### 方式 A：推送标签（推荐）

```bash
# 打标签
git tag v1.0.0

# 推送标签到 GitHub
git push origin v1.0.0
```

### 方式 B：手动触发

1. 在 Actions 页面选择 "Build Windows EXE"
2. 点击 "Run workflow"
3. 选择分支（main）
4. 点击 "Run workflow"

## 步骤 5：下载打包好的 EXE

### 从 Actions 下载

1. 在 Actions 页面点击正在运行或已完成的 workflow
2. 滚动到页面底部 "Artifacts" 部分
3. 点击 `ExcelExtractor-Windows` 下载
4. 解压得到 `ExcelExtractor.exe`

### 从 Releases 下载（如果推送了标签）

1. 在仓库页面右侧点击 "Releases"
2. 选择最新版本（如 v1.0.0）
3. 下载 `ExcelExtractor.exe`

## 常见问题

### Q: Actions 没有自动运行？
A: 检查 Settings → Actions → General，确保 "Allow all actions and reusable workflows" 已启用

### Q: 打包失败？
A: 点击失败的 job 查看日志，常见问题：
- 依赖安装失败 → 检查网络
- 内存不足 → GitHub Actions 免费额度有限

### Q: 如何修改 EXE 名称？
A: 编辑 `.github/workflows/build-windows.yml` 中的 `--name ExcelExtractor`

### Q: 如何添加图标？
A: 
1. 准备 `.ico` 图标文件
2. 上传到仓库
3. 修改 yml 文件：`pyinstaller --onefile --name ExcelExtractor --icon=your-icon.ico ...`

## 打包配置说明

`.github/workflows/build-windows.yml` 关键配置：

```yaml
runs-on: windows-latest  # 使用 Windows 最新系统
python-version: '3.10'   # Python 版本
pyinstaller --onefile    # 打包成单个 EXE
```

## 下一步

打包完成后，你可以：
1. 下载 EXE 直接使用
2. 在 Releases 页面分享给其他人
3. 继续开发新功能，推送新标签自动打包新版本

---

**提示**：GitHub Actions 免费额度：
- 公共仓库：无限免费
- 私有仓库：每月 2000 分钟
- 打包一次约 5-10 分钟
