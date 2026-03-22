@echo off
chcp 65001 >nul
echo ============================================================
echo Excel 数据提取工具 - 一键打包脚本
echo ============================================================
echo.

echo [1/4] 检查 Python 安装...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python
    echo.
    echo 请先安装 Python: https://www.python.org/downloads/
    echo 安装时勾选 "Add Python to PATH"
    pause
    exit /b 1
)
echo ✅ Python 已安装

echo.
echo [2/4] 安装依赖库...
pip install pandas openpyxl pyinstaller -q
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装完成

echo.
echo [3/4] 打包 EXE 文件...
pyinstaller --onefile --name ExcelExtractor --icon=NONE --clean excel_search_extract.py
if errorlevel 1 (
    echo ❌ 打包失败
    pause
    exit /b 1
)
echo ✅ 打包完成

echo.
echo [4/4] 检查输出文件...
if exist "dist\ExcelExtractor.exe" (
    echo ✅ EXE 文件已生成：dist\ExcelExtractor.exe
    echo.
    echo ============================================================
    echo 打包成功！
    echo EXE 文件位置：%CD%\dist\ExcelExtractor.exe
    echo ============================================================
) else (
    echo ❌ EXE 文件未找到
)

echo.
pause
