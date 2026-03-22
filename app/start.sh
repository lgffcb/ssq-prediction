#!/bin/bash
# 管网计量助手 启动脚本

echo "🚀 启动管网计量助手..."
echo ""
echo "📐 管网计量助手 v1.0"
echo "================================"
echo ""
echo "访问地址：http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

cd /home/admin/openclaw/workspace
streamlit run app/main.py --server.address localhost --server.port 8501
