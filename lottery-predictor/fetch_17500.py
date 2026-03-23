#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 17500 网站爬取双色球数据 - 可用版本
URL: https://www.17500.cn/ssq/
"""

import requests
import pandas as pd
import re
from typing import Optional, List


def fetch_from_17500() -> Optional[pd.DataFrame]:
    """
    从 17500 网站爬取双色球数据
    
    Returns:
        DataFrame 包含开奖数据
    """
    url = "https://www.17500.cn/ssq/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    try:
        print("📡 正在爬取 17500 网站...")
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"❌ 请求失败：{response.status_code}")
            return None
        
        html = response.text
        
        # 解析数据
        records = []
        
        # 查找所有期号（更宽松的匹配）
        issue_pattern = r'href="/kj/list-ssq\.html">(\d{7})<'
        all_issues = re.findall(issue_pattern, html)
        
        # 查找所有日期
        date_pattern = r'>(\d{4}-\d{2}-\d{2})<'
        all_dates = re.findall(date_pattern, html)
        
        # 查找所有红球
        red_pattern = r'class="fred">([\d\s]+)</b>'
        all_reds = re.findall(red_pattern, html)
        
        # 查找所有蓝球
        blue_pattern = r'class="fblue">(\d+)</b>'
        all_blues = re.findall(blue_pattern, html)
        
        print(f"找到：{len(all_issues)} 期，{len(all_dates)} 日期，{len(all_reds)} 红球，{len(all_blues)} 蓝球")
        
        # 组合数据
        min_len = min(len(all_issues), len(all_reds), len(all_blues))
        
        for i in range(min_len):
            try:
                issue = all_issues[i]
                date = all_dates[i] if i < len(all_dates) else ''
                red_str = all_reds[i].strip()
                reds = [int(x) for x in red_str.split()]
                blue = int(all_blues[i])
                
                if len(reds) == 6 and 1 <= blue <= 16:
                    records.append({
                        'issue': issue,
                        'date': date,
                        'red1': reds[0],
                        'red2': reds[1],
                        'red3': reds[2],
                        'red4': reds[3],
                        'red5': reds[4],
                        'red6': reds[5],
                        'blue': blue
                    })
            except Exception as e:
                continue
        
        if records:
            df = pd.DataFrame(records)
            # 去重
            df = df.drop_duplicates(subset=['issue'], keep='last')
            # 排序
            df = df.sort_values('issue', ascending=False).reset_index(drop=True)
            
            print(f"✅ 成功爬取 {len(df)} 期数据")
            return df
        else:
            print("⚠️  未找到数据")
            return None
            
    except Exception as e:
        print(f"❌ 爬取失败：{e}")
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("🕷️  17500 双色球爬虫 - 可用版本")
    print("=" * 60)
    print()
    
    df = fetch_from_17500()
    
    if df is not None and len(df) > 0:
        print(f"\n{'='*60}")
        print(f"✅ 成功获取 {len(df)} 期数据")
        print(f"{'='*60}")
        
        print(f"\n最近 10 期:")
        print(df.head(10).to_string(index=False))
        
        # 统计信息
        print(f"\n数据范围：{df.iloc[-1]['issue']} - {df.iloc[0]['issue']}")
        print(f"日期范围：{df.iloc[-1]['date']} - {df.iloc[0]['date']}")
        
        # 保存
        df.to_csv('data/ssq_17500.csv', index=False, encoding='utf-8-sig')
        print(f"\n💾 数据已保存到：data/ssq_17500.csv")
        
        # 更新历史数据文件
        df.to_csv('data/historical_data.csv', index=False, encoding='utf-8-sig')
        print(f"💾 已更新：data/historical_data.csv")
    else:
        print("\n❌ 获取数据失败")
    
    print()
    print("=" * 60)


if __name__ == '__main__':
    main()
