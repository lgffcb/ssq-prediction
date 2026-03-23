@echo off
chcp 65001 >nul
echo ============================================================
echo 🎱 双色球预测软件 - Windows EXE 打包工具
echo ============================================================
echo.

echo 📌 检查 Python...
python --version 2>nul
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.10
    pause
    exit /b 1
)

echo.
echo 📦 安装依赖...
pip install pyinstaller pandas numpy scikit-learn scipy matplotlib seaborn -q
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 开始打包...
echo ============================================================
echo.

REM 创建输出目录
if not exist "dist" mkdir dist
if not exist "release_package" mkdir release_package
if not exist "release_package\data" mkdir release_package\data

echo 1️⃣ 打包 GUI 界面版...
pyinstaller --onefile --windowed --name SSQ_Predictor --icon=NONE predictor.py
if errorlevel 1 (
    echo ❌ GUI 版打包失败
    pause
    exit /b 1
)

echo.
echo 2️⃣ 打包命令行版...
pyinstaller --onefile --name SSQ_CLI predictor.py
if errorlevel 1 (
    echo ❌ 命令行版打包失败
    pause
    exit /b 1
)

echo.
echo 3️⃣ 打包更新工具...
pyinstaller --onefile --name SSQ_Update auto_update.py
if errorlevel 1 (
    echo ❌ 更新工具打包失败
    pause
    exit /b 1
)

echo.
echo 4️⃣ 打包数据获取工具...
pyinstaller --onefile --name SSQ_Fetch fetch_history_17500.py
if errorlevel 1 (
    echo ❌ 数据获取工具打包失败
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 创建 Release 包...
echo ============================================================
echo.

copy dist\SSQ_Predictor.exe release_package\ >nul
copy dist\SSQ_CLI.exe release_package\ >nul
copy dist\SSQ_Update.exe release_package\ >nul
copy dist\SSQ_Fetch.exe release_package\ >nul
copy README.md release_package\ >nul
copy requirements.txt release_package\ >nul

if exist "data\historical_data.csv" (
    copy data\historical_data.csv release_package\data\ >nul
    echo ✅ 数据文件已复制
) else (
    echo ⚠️  数据文件不存在，跳过
)

echo.
echo 📦 压缩文件...
powershell -Command "Compress-Archive -Path 'release_package\*' -DestinationPath 'SSQ_Predictor_Windows.zip' -Force"

echo.
echo ============================================================
echo ✅ 打包完成！
echo ============================================================
echo.
echo 📂 输出目录:
echo   - dist\              (单个 EXE 文件)
echo   - release_package\   (完整发布包)
echo   - SSQ_Predictor_Windows.zip (压缩包)
echo.
echo 📊 文件大小:
dir /S dist\*.exe | find "EXE"
echo.
echo 🎉 成功！
echo.
pause
