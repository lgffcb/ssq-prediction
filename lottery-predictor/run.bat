@echo off
chcp 65001 >nul
echo ============================================================
echo 🎱 双色球预测软件 v1.0
echo ============================================================
echo.

echo 📌 检查 Python...
python --version 2>nul
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 选择运行模式:
echo   1^) 命令行版本
echo   2^) GUI 图形界面
echo   3^) 安装依赖
echo   4^) 退出
echo ============================================================
echo.

set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🚀 启动命令行版本...
    echo.
    python predictor.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo 🚀 启动 GUI 图形界面...
    echo.
    python gui.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo 📦 安装依赖...
    pip install -r requirements.txt
    pause
) else if "%choice%"=="4" (
    echo 👋 再见！
    exit /b 0
) else (
    echo ❌ 无效选项
    pause
    exit /b 1
)
