#!/bin/bash
# 双色球预测软件 - Linux/Mac 打包脚本

echo "============================================================"
echo "🎱 双色球预测软件 - EXE 打包工具"
echo "============================================================"
echo ""

# 检查 Python
echo "📌 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3"
    exit 1
fi

python3 --version
echo "  ✅ Python 已安装"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install pyinstaller pandas numpy scikit-learn scipy matplotlib seaborn -q
echo "  ✅ 依赖已安装"

echo ""
echo "============================================================"
echo "开始打包..."
echo "============================================================"
echo ""

# 创建目录
mkdir -p dist release_package release_package/data

# 打包 GUI 版（需要 tkinter）
echo "1️⃣ 打包 GUI 界面版..."
pyinstaller --onefile --windowed --name SSQ_Predictor predictor.py
if [ $? -ne 0 ]; then
    echo "❌ GUI 版打包失败"
    exit 1
fi

echo ""
echo "2️⃣ 打包命令行版..."
pyinstaller --onefile --name SSQ_CLI predictor.py
if [ $? -ne 0 ]; then
    echo "❌ 命令行版打包失败"
    exit 1
fi

echo ""
echo "3️⃣ 打包更新工具..."
pyinstaller --onefile --name SSQ_Update auto_update.py
if [ $? -ne 0 ]; then
    echo "❌ 更新工具打包失败"
    exit 1
fi

echo ""
echo "4️⃣ 打包数据获取工具..."
pyinstaller --onefile --name SSQ_Fetch fetch_history_17500.py
if [ $? -ne 0 ]; then
    echo "❌ 数据获取工具打包失败"
    exit 1
fi

echo ""
echo "============================================================"
echo "创建 Release 包..."
echo "============================================================"
echo ""

cp dist/SSQ_Predictor* release_package/ 2>/dev/null
cp dist/SSQ_CLI* release_package/ 2>/dev/null
cp dist/SSQ_Update* release_package/ 2>/dev/null
cp dist/SSQ_Fetch* release_package/ 2>/dev/null
cp README.md release_package/
cp requirements.txt release_package/

if [ -f "data/historical_data.csv" ]; then
    cp data/historical_data.csv release_package/data/
    echo "✅ 数据文件已复制"
else
    echo "⚠️  数据文件不存在，跳过"
fi

echo ""
echo "📦 压缩文件..."
cd release_package
zip -r ../SSQ_Predictor_Windows.zip *
cd ..

echo ""
echo "============================================================"
echo "✅ 打包完成！"
echo "============================================================"
echo ""
echo "📂 输出目录:"
echo "  - dist/              (单个 EXE 文件)"
echo "  - release_package/   (完整发布包)"
echo "  - SSQ_Predictor_Windows.zip (压缩包)"
echo ""
echo "📊 文件大小:"
ls -lh dist/*.exe 2>/dev/null || ls -lh dist/SSQ_* 2>/dev/null
echo ""
echo "🎉 成功！"
echo ""
