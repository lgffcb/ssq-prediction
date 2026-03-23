#!/bin/bash
# 双色球预测 - 一键运行脚本

echo "============================================================"
echo "🎱 双色球预测软件 - 一键运行"
echo "============================================================"
echo ""

cd /home/admin/openclaw/workspace/lottery-predictor

# 1. 检查数据
echo "📂 检查数据文件..."
if [ -f "data/historical_data.csv" ]; then
    LINES=$(wc -l < data/historical_data.csv)
    echo "✅ 历史数据：$((LINES-1)) 期"
else
    echo "❌ 数据文件不存在，正在获取..."
    python3 fetch_history_17500.py
fi

echo ""
echo "========================================"
echo "🔮 开始预测..."
echo "========================================"
echo ""

# 2. 运行预测
python3 predictor.py

echo ""
echo "========================================"
echo "✅ 完成！"
echo "========================================"
