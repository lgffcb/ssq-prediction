#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 17500 获取双色球历史数据
URL: http://www.17500.cn/getData/ssq.TXT
数据格式：期号，日期，红球 1-6，蓝球，其他字段
"""

import requests
import pandas as pd
import io
from typing import Optional


def fetch_from_17500_txt() -> Optional[pd.DataFrame]:
    """
    从 17500 TXT 接口获取历史数据
    
    Returns:
        DataFrame 包含开奖数据
    """
    url = "http://www.17500.cn/getData/ssq.TXT"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
    }
    
    try:
        print("📡 正在从 17500 获取历史数据...")
        print(f"URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"❌ 请求失败：{response.status_code}")
            return None
        
        text = response.text
        print(f"✅ 获取到数据：{len(text)} 字节")
        
        # 显示前几行看看格式
        lines = text.strip().split('\n')
        print(f"\n📋 数据格式预览（前 3 行）:")
        for i, line in enumerate(lines[:3]):
            print(f"  {i+1}: {line}")
        
        # 解析 CSV 格式数据
        # 使用 pandas 读取
        df = pd.read_csv(
            io.StringIO(text),
            sep=' ',
            header=None,
            dtype=str
        )
        
        print(f"📊 原始数据：{len(df)} 行 × {len(df.columns)} 列")
        
        # 只保留前 9 列（期号、日期、6 红、1 蓝）
        df = df.iloc[:, :9]
        df.columns = ['issue', 'date', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']
        
        # 转换数据类型
        df['issue'] = df['issue'].astype(str)
        df['date'] = df['date'].astype(str)
        
        # 转换数字列，处理可能的空值
        for col in ['red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
        # 排序
        df = df.sort_values('issue', ascending=False).reset_index(drop=True)
        
        print(f"\n✅ 成功解析 {len(df)} 期数据")
        return df
        
    except Exception as e:
        print(f"❌ 获取失败：{e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("📡 17500 双色球历史数据获取")
    print("=" * 60)
    print()
    
    df = fetch_from_17500_txt()
    
    if df is not None and len(df) > 0:
        print(f"\n{'='*60}")
        print(f"✅ 成功获取 {len(df)} 期历史数据")
        print(f"{'='*60}")
        
        print(f"\n最近 10 期:")
        print(df.head(10).to_string(index=False))
        
        print(f"\n最早 10 期:")
        print(df.tail(10).to_string(index=False))
        
        # 统计信息
        print(f"\n📊 统计信息:")
        print(f"  期号范围：{df.iloc[-1]['issue']} - {df.iloc[0]['issue']}")
        print(f"  日期范围：{df.iloc[-1]['date']} - {df.iloc[0]['date']}")
        print(f"  总期数：{len(df)}")
        
        # 保存
        df.to_csv('data/ssq_history.csv', index=False, encoding='utf-8-sig')
        print(f"\n💾 数据已保存到：data/ssq_history.csv")
        
        # 更新历史数据文件
        df.to_csv('data/historical_data.csv', index=False, encoding='utf-8-sig')
        print(f"💾 已更新：data/historical_data.csv")
        
        # 显示文件大小
        import os
        file_size = os.path.getsize('data/ssq_history.csv')
        print(f"📦 文件大小：{file_size / 1024:.2f} KB")
    else:
        print("\n❌ 获取数据失败")
    
    print()
    print("=" * 60)


if __name__ == '__main__':
    main()
