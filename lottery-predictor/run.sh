#!/bin/bash
# 双色球预测软件 - 启动脚本

echo "============================================================"
echo "🎱 双色球预测软件 v1.0"
echo "============================================================"
echo ""

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📌 Python 版本：$python_version"

# 检查依赖
echo ""
echo "📦 检查依赖..."
python3 -c "import pandas" 2>/dev/null && echo "  ✅ pandas" || echo "  ❌ pandas (需要安装)"
python3 -c "import numpy" 2>/dev/null && echo "  ✅ numpy" || echo "  ❌ numpy (需要安装)"
python3 -c "import sklearn" 2>/dev/null && echo "  ✅ scikit-learn" || echo "  ❌ scikit-learn (需要安装)"
python3 -c "import tensorflow" 2>/dev/null && echo "  ✅ tensorflow" || echo "  ⚠️  tensorflow (可选，用于 LSTM)"
python3 -c "import tkinter" 2>/dev/null && echo "  ✅ tkinter" || echo "  ❌ tkinter (GUI 需要)"

echo ""
echo "============================================================"
echo "选择运行模式:"
echo "  1) 命令行版本"
echo "  2) GUI 图形界面"
echo "  3) 安装依赖"
echo "  4) 退出"
echo "============================================================"
echo ""

read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚀 启动命令行版本..."
        echo ""
        python3 predictor.py
        ;;
    2)
        echo ""
        echo "🚀 启动 GUI 图形界面..."
        echo ""
        python3 gui.py
        ;;
    3)
        echo ""
        echo "📦 安装依赖..."
        pip3 install -r requirements.txt
        ;;
    4)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac
