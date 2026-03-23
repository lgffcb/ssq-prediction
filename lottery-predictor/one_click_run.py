#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球预测 - 一键运行完整版
获取最新数据 + 运行预测
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print('='*60)
    
    result = subprocess.run(
        cmd, 
        shell=True, 
        capture_output=True, 
        text=True,
        cwd='/home/admin/openclaw/workspace/lottery-predictor'
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return result.returncode == 0


def main():
    """主函数"""
    print("="*60)
    print("🎱 双色球预测软件 - 一键运行")
    print("="*60)
    
    os.chdir('/home/admin/openclaw/workspace/lottery-predictor')
    
    # 1. 获取最新数据
    success = run_command(
        "python3 fetch_history_17500.py 2>&1 | grep -E '(成功 | 最近 | 统计|💾)'",
        "步骤 1: 获取最新历史数据"
    )
    
    if not success:
        print("⚠️  获取数据失败，使用现有数据")
    
    # 2. 显示数据概况
    run_command(
        "head -5 data/historical_data.csv && echo '...' && tail -3 data/historical_data.csv",
        "步骤 2: 数据概况"
    )
    
    # 3. 运行预测
    success = run_command(
        "python3 predictor.py 2>&1",
        "步骤 3: 运行预测"
    )
    
    if success:
        print("\n" + "="*60)
        print("✅ 完成！")
        print("="*60)
        print("\n💡 提示:")
        print("  - 数据文件：data/historical_data.csv")
        print("  - 预测结果：已显示在上方")
        print("  - 日志文件：logs/auto_update.log")
        print()


if __name__ == '__main__':
    main()
