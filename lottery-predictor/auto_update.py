#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球数据自动更新脚本
支持定时任务、增量更新、通知提醒
"""

import sys
import os
from datetime import datetime
import argparse

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataFetcher


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='双色球数据自动更新工具')
    
    parser.add_argument('-f', '--file', 
                        default='data/historical_data.csv',
                        help='数据文件路径 (默认：data/historical_data.csv)')
    
    parser.add_argument('-s', '--source',
                        choices=['mock', '17500', 'kaijiang', '500wan'],
                        default='17500',
                        help='数据源 (默认：17500)')
    
    parser.add_argument('-i', '--interval',
                        choices=['always', 'daily', 'weekly'],
                        default='daily',
                        help='更新间隔 (默认：daily)')
    
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='静默模式（只输出错误）')
    
    parser.add_argument('--check-only',
                        action='store_true',
                        help='只检查，不更新')
    
    parser.add_argument('--force',
                        action='store_true',
                        help='强制更新（忽略间隔设置）')
    
    args = parser.parse_args()
    
    fetcher = DataFetcher()
    
    if not args.quiet:
        print("=" * 60)
        print("🔄 双色球数据自动更新")
        print("=" * 60)
        print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 文件：{args.file}")
        print(f"📡 数据源：{args.source}")
        print(f"⏳ 间隔：{args.interval}")
        print()
    
    try:
        # 检查是否有新数据
        if args.check_only:
            has_new = fetcher.check_for_new_draw(args.file, args.source)
            if has_new:
                print("✅ 有新数据可更新")
                return 0
            else:
                print("✅ 数据已是最新")
                return 0
        
        # 强制更新
        if args.force:
            if not args.quiet:
                print("⚡ 强制更新模式...")
            df = fetcher.update_data(args.file, args.source, auto=args.quiet)
            if not args.quiet:
                print(f"\n✅ 更新完成：共 {len(df)} 期")
            return 0
        
        # 自动更新
        df = fetcher.auto_update(args.file, args.source, args.interval)
        
        if not args.quiet:
            print()
            print("=" * 60)
            print(f"✅ 当前数据：{len(df)} 期")
            
            # 显示最近一期
            if len(df) > 0:
                last = df.iloc[-1]
                if 'issue' in last:
                    print(f"📊 最新期号：{last['issue']}")
                if 'date' in last:
                    print(f"📅 开奖日期：{last['date']}")
                if 'red1' in last:
                    reds = [last[f'red{i}'] for i in range(1, 7)]
                    print(f"🔴 红球：{' '.join(str(int(r)) for r in reds)}")
                    print(f"🔵 蓝球：{int(last['blue'])}")
            
            print("=" * 60)
        
        return 0
        
    except Exception as e:
        if not args.quiet:
            print(f"\n❌ 更新失败：{e}")
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
