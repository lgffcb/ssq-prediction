#!/bin/bash
# 数据提取汇总助手 启动脚本

echo "🚀 启动数据提取汇总助手..."
echo ""
echo "📊 数据提取汇总助手 v1.0"
echo "================================"
echo ""
echo "访问地址：http://localhost:8502"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

cd /home/admin/openclaw/workspace
streamlit run skills/data_extractor/main.py --server.address localhost --server.port 8502
