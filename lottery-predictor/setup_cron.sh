#!/bin/bash
# 双色球自动更新 - 一键安装脚本

echo "============================================================"
echo "🔄 双色球数据自动更新 - 一键配置"
echo "============================================================"
echo ""

PROJECT_DIR="/home/admin/openclaw/workspace/lottery-predictor"
PYTHON="/usr/bin/python3"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/auto_update.log"

# 检查目录
echo "📂 检查目录..."
mkdir -p "$LOG_DIR"
echo "  ✅ 日志目录：$LOG_DIR"

# 检查 Python
echo ""
echo "🐍 检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON=$(which python3)
    echo "  ✅ Python: $PYTHON"
else
    echo "  ❌ 未找到 Python3"
    exit 1
fi

# 选择定时方式
echo ""
echo "============================================================"
echo "选择定时任务类型:"
echo "  1) Cron (推荐 - Linux/Mac)"
echo "  2) Systemd Timer (Linux)"
echo "  3) 手动运行（不自动更新）"
echo "============================================================"
echo ""

if [ -n "$1" ]; then
    choice=$1
else
    read -p "请输入选项 (1-3): " choice
fi

case $choice in
    1)
        echo ""
        echo "📋 配置 Cron 定时任务..."
        
        # 创建临时 crontab 文件
        TEMP_CRON=$(mktemp)
        
        # 读取现有 crontab
        crontab -l 2>/dev/null > "$TEMP_CRON" || true
        
        # 添加新任务（每天早上 9 点）
        echo "" >> "$TEMP_CRON"
        echo "# 双色球数据自动更新（每天 9:00）" >> "$TEMP_CRON"
        echo "0 9 * * * cd $PROJECT_DIR && $PYTHON auto_update.py -f data/historical_data.csv -s mock -i daily >> $LOG_FILE 2>&1" >> "$TEMP_CRON"
        
        # 可选：开奖日晚上 9 点检查（周二、四、日）
        echo "# 双色球开奖日检查（周二、四、日 21:00）" >> "$TEMP_CRON"
        echo "0 21 * * 2,4,0 cd $PROJECT_DIR && $PYTHON auto_update.py -f data/historical_data.csv -s mock -i always >> $LOG_FILE 2>&1" >> "$TEMP_CRON"
        
        # 安装 crontab
        crontab "$TEMP_CRON"
        rm -f "$TEMP_CRON"
        
        echo ""
        echo "✅ Cron 配置完成！"
        echo ""
        echo "📋 已添加的任务:"
        crontab -l | grep lottery
        echo ""
        echo "📝 查看日志：tail -f $LOG_FILE"
        echo ""
        ;;
    
    2)
        echo ""
        echo "⚙️  配置 Systemd Timer..."
        
        # 检查是否需要 sudo
        if [ "$EUID" -ne 0 ]; then
            echo "  ⚠️  需要 sudo 权限，请输入密码"
        fi
        
        # 复制服务文件
        sudo cp "$PROJECT_DIR/lottery-update.service" /etc/systemd/system/
        sudo cp "$PROJECT_DIR/lottery-update.timer" /etc/systemd/system/
        
        # 重新加载 systemd
        sudo systemctl daemon-reload
        
        # 启用并启动定时器
        sudo systemctl enable lottery-update.timer
        sudo systemctl start lottery-update.timer
        
        echo ""
        echo "✅ Systemd Timer 配置完成！"
        echo ""
        echo "📊 查看状态：sudo systemctl status lottery-update.timer"
        echo "📋 查看所有定时器：sudo systemctl list-timers"
        echo "📝 查看日志：sudo journalctl -u lottery-update.service -f"
        echo ""
        ;;
    
    3)
        echo ""
        echo "ℹ️  手动模式已选择"
        echo ""
        echo "运行更新命令:"
        echo "  cd $PROJECT_DIR"
        echo "  python3 auto_update.py"
        echo ""
        ;;
    
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo "============================================================"
echo "✅ 配置完成！"
echo "============================================================"
echo ""
echo "📂 项目目录：$PROJECT_DIR"
echo "📝 日志文件：$LOG_FILE"
echo ""
echo "常用命令:"
echo "  手动更新：cd $PROJECT_DIR && python3 auto_update.py"
echo "  查看日志：tail -f $LOG_FILE"
echo "  强制更新：python3 auto_update.py --force"
echo ""
