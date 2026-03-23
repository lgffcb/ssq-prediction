#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 17500 网站爬取双色球数据
URL: https://www.17500.cn/ssq/kaijiang.php
"""

import requests
import pandas as pd
import re
from typing import Optional, List
import time


class Lottery17500Spider:
    """17500 彩票网爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.17500.cn/',
        })
    
    def fetch_current_year(self, year: int = None) -> Optional[pd.DataFrame]:
        """
        获取指定年份的数据
        
        URL: https://www.17500.cn/ssq/kaijiang.php?year={year}
        
        Args:
            year: 年份（如 2026）
            
        Returns:
            DataFrame 包含开奖数据
        """
        if year is None:
            year = 2026  # 当前年份
        
        url = f"https://www.17500.cn/ssq/kaijiang.php?year={year}"
        
        try:
            print(f"📡 正在爬取 17500 网站 {year} 年数据...")
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"❌ 请求失败：{response.status_code}")
                return None
            
            html = response.text
            
            # 解析表格数据
            records = self._parse_17500_html(html)
            
            if records:
                df = pd.DataFrame(records)
                print(f"✅ 从 17500 爬取 {len(df)} 期数据")
                return df
            else:
                print("⚠️  未找到数据")
                return None
                
        except Exception as e:
            print(f"❌ 爬取失败：{e}")
            return None
    
    def _parse_17500_html(self, html: str) -> List[dict]:
        """解析 17500 HTML"""
        records = []
        
        # 17500 的数据格式通常是表格
        # 查找所有 tr 标签
        tr_pattern = r'<tr[^>]*>(.*?)</tr>'
        trs = re.findall(tr_pattern, html, re.DOTALL | re.IGNORECASE)
        
        for tr in trs:
            # 提取 td 内容
            td_pattern = r'<td[^>]*>(.*?)</td>'
            tds = re.findall(td_pattern, tr, re.DOTALL | re.IGNORECASE)
            
            # 清理 HTML 标签
            clean_tds = []
            for td in tds:
                # 移除所有 HTML 标签
                text = re.sub(r'<[^>]+>', '', td).strip()
                # 移除空格和换行
                text = re.sub(r'\s+', ' ', text)
                clean_tds.append(text)
            
            # 17500 格式：期号 日期 红球 1-6 蓝球 其他列
            # 通常需要至少 8 列数据
            if len(clean_tds) >= 8:
                try:
                    # 尝试解析期号（格式：2026001）
                    issue = clean_tds[0].strip()
                    if not re.match(r'\d{7}', issue):
                        continue
                    
                    # 日期
                    date = clean_tds[1].strip()
                    
                    # 红球（通常是 6 个数字）
                    reds = []
                    for i in range(2, 8):
                        if i < len(clean_tds):
                            red_num = clean_tds[i].strip()
                            if red_num.isdigit():
                                reds.append(int(red_num))
                    
                    # 蓝球
                    blue = 0
                    if len(clean_tds) >= 8:
                        blue_str = clean_tds[7].strip()
                        if blue_str.isdigit():
                            blue = int(blue_str)
                    
                    # 验证数据
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
        
        return records
    
    def fetch_all_years(self, start_year: int = 2020, end_year: int = None) -> pd.DataFrame:
        """
        获取多年的数据
        
        Args:
            start_year: 开始年份
            end_year: 结束年份（默认当前年份）
            
        Returns:
            合并的 DataFrame
        """
        if end_year is None:
            end_year = 2026
        
        all_records = []
        
        for year in range(start_year, end_year + 1):
            print(f"\n{'='*60}")
            df = self.fetch_current_year(year)
            
            if df is not None and len(df) > 0:
                all_records.append(df)
            
            # 延迟，避免请求过快
            if year < end_year:
                time.sleep(1)
        
        if all_records:
            combined = pd.concat(all_records, ignore_index=True)
            # 去重
            combined = combined.drop_duplicates(subset=['issue'], keep='last')
            # 排序
            combined = combined.sort_values('issue').reset_index(drop=True)
            
            print(f"\n{'='*60}")
            print(f"✅ 总共获取 {len(combined)} 期数据 ({start_year}-{end_year}年)")
            return combined
        else:
            print("\n❌ 未获取到任何数据")
            return pd.DataFrame()
    
    def fetch_latest(self, count: int = 30) -> Optional[pd.DataFrame]:
        """
        获取最近 N 期数据
        
        Args:
            count: 获取期数
            
        Returns:
            DataFrame 包含最近 N 期数据
        """
        # 获取当前年份数据
        df = self.fetch_current_year()
        
        if df is not None and len(df) > 0:
            # 返回最近 N 期
            return df.tail(count).reset_index(drop=True)
        
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("🕷️  17500 彩票网爬虫")
    print("=" * 60)
    print()
    
    spider = Lottery17500Spider()
    
    # 测试 1：获取当前年份数据
    print("测试 1: 获取 2026 年数据")
    print("-" * 60)
    df_2026 = spider.fetch_current_year(2026)
    
    if df_2026 is not None and len(df_2026) > 0:
        print(f"\n✅ 成功获取 {len(df_2026)} 期数据")
        print(f"\n最近 5 期:")
        print(df_2026.tail(5).to_string(index=False))
        
        # 保存
        df_2026.to_csv('data/ssq_17500_2026.csv', index=False, encoding='utf-8-sig')
        print(f"\n💾 数据已保存到：data/ssq_17500_2026.csv")
    else:
        print("\n❌ 获取 2026 年数据失败")
    
    print()
    
    # 测试 2：获取多年数据
    print("测试 2: 获取 2023-2026 年数据")
    print("-" * 60)
    df_all = spider.fetch_all_years(2023, 2026)
    
    if df_all is not None and len(df_all) > 0:
        print(f"\n✅ 成功获取 {len(df_all)} 期数据")
        print(f"\n最近 5 期:")
        print(df_all.tail(5).to_string(index=False))
        
        # 保存
        df_all.to_csv('data/ssq_17500_all.csv', index=False, encoding='utf-8-sig')
        print(f"\n💾 数据已保存到：data/ssq_17500_all.csv")
    
    print()
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
