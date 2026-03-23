#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球数据爬虫 - 直接从官方网站爬取
支持：福彩网、500 彩票网、第一彩票网
"""

import requests
import pandas as pd
import re
import time
from datetime import datetime
from typing import List, Dict, Optional
import random


class LotterySpider:
    """彩票数据爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        })
    
    def fetch_from_zhcw_official(self, page: int = 1, page_size: int = 30) -> Optional[pd.DataFrame]:
        """
        从中国福彩网官方网站爬取
        
        URL: https://m.zhcw.com/pchtml/kajianggonggao/ssq/list_{page}.html
        
        Args:
            page: 页码
            page_size: 每页数量
            
        Returns:
            DataFrame 包含开奖数据
        """
        try:
            url = f"https://m.zhcw.com/pchtml/kajianggonggao/ssq/list_{page}.html"
            
            print(f"📡 正在爬取福彩网第 {page} 页...")
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"❌ 请求失败：{response.status_code}")
                return None
            
            html = response.text
            
            # 使用正则表达式提取数据
            # 匹配格式：期号、日期、红球、蓝球
            pattern = r'<li[^>]*>.*?第\s*(\d{4})\s*期.*?(\d{4}-\d{2}-\d{2}).*?red">(\d+).*?red">(\d+).*?red">(\d+).*?red">(\d+).*?red">(\d+).*?red">(\d+).*?blue">(\d+)'
            
            matches = re.findall(pattern, html, re.DOTALL)
            
            if not matches:
                # 尝试另一种格式
                pattern = r'(\d{8})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)'
                matches = re.findall(pattern, html)
            
            if not matches:
                print("⚠️  未找到数据，尝试其他格式...")
                return self._parse_zhcw_alternative(html)
            
            records = []
            for match in matches:
                try:
                    if len(match) == 8:  # 期号 + 日期 + 6 红 +1 蓝
                        issue = match[0]
                        date = match[1] if len(match[1]) > 4 else f"20{match[0][:2]}-{match[0][2:4]}-{match[0][4:6]}"
                        reds = [int(match[i]) for i in range(2, 8)]
                        blue = int(match[8]) if len(match) > 8 else int(match[7])
                    else:
                        continue
                    
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
                    print(f"⚠️  解析失败：{e}")
                    continue
            
            if records:
                df = pd.DataFrame(records)
                print(f"✅ 成功爬取 {len(df)} 期数据")
                return df
            else:
                print("⚠️  未解析到有效数据")
                return None
                
        except Exception as e:
            print(f"❌ 爬取失败：{e}")
            return None
    
    def _parse_zhcw_alternative(self, html: str) -> Optional[pd.DataFrame]:
        """备用解析方法"""
        try:
            # 查找所有包含数字的段落
            lines = html.split('\n')
            records = []
            
            for line in lines:
                # 匹配期号格式
                if '第' in line and '期' in line:
                    # 提取期号
                    issue_match = re.search(r'第\s*(\d+)\s*期', line)
                    if issue_match:
                        issue = issue_match.group(1)
                        
                        # 提取红球
                        reds = re.findall(r'red[^>]*>(\d+)', line)
                        # 提取蓝球
                        blues = re.findall(r'blue[^>]*>(\d+)', line)
                        
                        if len(reds) >= 6 and len(blues) >= 1:
                            records.append({
                                'issue': issue,
                                'date': '',
                                'red1': int(reds[0]),
                                'red2': int(reds[1]),
                                'red3': int(reds[2]),
                                'red4': int(reds[3]),
                                'red5': int(reds[4]),
                                'red6': int(reds[5]),
                                'blue': int(blues[0])
                            })
            
            if records:
                df = pd.DataFrame(records)
                print(f"✅ 备用方法爬取 {len(df)} 期数据")
                return df
            
            return None
        except Exception as e:
            print(f"❌ 备用解析失败：{e}")
            return None
    
    def fetch_from_500wan(self, page: int = 1) -> Optional[pd.DataFrame]:
        """
        从 500 彩票网爬取
        
        URL: http://kaijiang.500.com/ssq.shtml
        
        Returns:
            DataFrame 包含开奖数据
        """
        try:
            url = "http://kaijiang.500.com/ssq.shtml"
            
            print(f"📡 正在爬取 500 彩票网...")
            response = self.session.get(url, timeout=15)
            response.encoding = 'gb2312'
            
            if response.status_code != 200:
                print(f"❌ 请求失败：{response.status_code}")
                return None
            
            html = response.text
            
            # 查找表格数据
            records = []
            
            # 匹配 tr 标签中的 td
            tr_pattern = r'<tr[^>]*>(.*?)</tr>'
            td_pattern = r'<td[^>]*>(.*?)</td>'
            
            trs = re.findall(tr_pattern, html, re.DOTALL | re.IGNORECASE)
            
            for tr in trs[1:]:  # 跳过表头
                tds = re.findall(td_pattern, tr, re.DOTALL | re.IGNORECASE)
                
                if len(tds) >= 9:
                    try:
                        # 清理 HTML 标签
                        clean_tds = [re.sub(r'<[^>]+>', '', td).strip() for td in tds]
                        
                        issue = clean_tds[0]
                        date = clean_tds[1]
                        reds = [int(clean_tds[i]) for i in range(2, 8)]
                        blue = int(clean_tds[8])
                        
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
                print(f"✅ 从 500 彩票网爬取 {len(df)} 期数据")
                return df
            else:
                print("⚠️  未找到数据")
                return None
                
        except Exception as e:
            print(f"❌ 爬取失败：{e}")
            return None
    
    def fetch_from_dcp(self, page: int = 1) -> Optional[pd.DataFrame]:
        """
        从第一彩票网爬取
        
        URL: http://www.dcp777.com/kaijiang/ssq/
        
        Returns:
            DataFrame 包含开奖数据
        """
        try:
            url = f"http://www.dcp777.com/kaijiang/ssq/index_{page}.html"
            
            print(f"📡 正在爬取第一彩票网第 {page} 页...")
            response = self.session.get(url, timeout=15)
            response.encoding = 'gb2312'
            
            if response.status_code != 200:
                return None
            
            html = response.text
            
            # 解析数据（类似 500 万）
            records = []
            tr_pattern = r'<tr[^>]*>(.*?)</tr>'
            td_pattern = r'<td[^>]*>(.*?)</td>'
            
            trs = re.findall(tr_pattern, html, re.DOTALL | re.IGNORECASE)
            
            for tr in trs[1:]:
                tds = re.findall(td_pattern, tr, re.DOTALL | re.IGNORECASE)
                
                if len(tds) >= 8:
                    try:
                        clean_tds = [re.sub(r'<[^>]+>', '', td).strip() for td in tds]
                        
                        issue = clean_tds[0]
                        date = clean_tds[1]
                        reds_str = clean_tds[2].split(',')
                        reds = [int(r) for r in reds_str if r.isdigit()]
                        blue = int(clean_tds[3]) if clean_tds[3].isdigit() else 0
                        
                        if len(reds) == 6:
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
                    except:
                        continue
            
            if records:
                df = pd.DataFrame(records)
                print(f"✅ 从第一彩票网爬取 {len(df)} 期数据")
                return df
            
            return None
            
        except Exception as e:
            print(f"❌ 爬取失败：{e}")
            return None
    
    def fetch_multiple_pages(self, source: str = '500wan', 
                            pages: int = 3, 
                            delay: float = 1.0) -> pd.DataFrame:
        """
        爬取多页数据
        
        Args:
            source: 数据源 ('500wan', 'zhcw', 'dcp')
            pages: 爬取页数
            delay: 页间延迟（秒）
            
        Returns:
            合并的 DataFrame
        """
        all_records = []
        
        for page in range(1, pages + 1):
            if source == '500wan':
                df = self.fetch_from_500wan(page)
            elif source == 'zhcw':
                df = self.fetch_from_zhcw_official(page)
            elif source == 'dcp':
                df = self.fetch_from_dcp(page)
            else:
                print(f"⚠️  未知数据源：{source}")
                break
            
            if df is not None and len(df) > 0:
                all_records.append(df)
            
            # 延迟，避免请求过快
            if page < pages:
                time.sleep(delay + random.uniform(0, 0.5))
        
        if all_records:
            combined = pd.concat(all_records, ignore_index=True)
            # 去重
            combined = combined.drop_duplicates(subset=['issue'], keep='last')
            # 排序
            if 'date' in combined.columns:
                combined = combined.sort_values('date').reset_index(drop=True)
            
            print(f"\n✅ 总共爬取 {len(combined)} 期数据")
            return combined
        else:
            print("❌ 未获取到任何数据")
            return pd.DataFrame()
    
    def fetch_latest(self, source: str = '500wan') -> Optional[pd.DataFrame]:
        """
        只获取最新一期数据
        
        Args:
            source: 数据源
            
        Returns:
            最新一期数据
        """
        if source == '500wan':
            df = self.fetch_from_500wan()
        elif source == 'zhcw':
            df = self.fetch_from_zhcw_official()
        else:
            df = self.fetch_from_500wan()
        
        if df is not None and len(df) > 0:
            return df.iloc[-1:]
        return None


def main():
    """主函数"""
    print("=" * 60)
    print("🕷️  双色球数据爬虫")
    print("=" * 60)
    print()
    
    spider = LotterySpider()
    
    # 测试不同数据源
    sources = ['500wan', 'zhcw', 'dcp']
    
    for source in sources:
        print(f"\n{'='*60}")
        print(f"测试数据源：{source}")
        print('='*60)
        
        try:
            df = spider.fetch_latest(source)
            
            if df is not None and len(df) > 0:
                print(f"\n✅ {source} 成功!")
                print(f"最新一期：{df.iloc[0]['issue']}")
                print(f"开奖日期：{df.iloc[0]['date']}")
                reds = [df.iloc[0][f'red{i}'] for i in range(1, 7)]
                print(f"红球：{' '.join(str(int(r)) for r in reds)}")
                print(f"蓝球：{int(df.iloc[0]['blue'])}")
            else:
                print(f"⚠️  {source} 返回空数据")
        except Exception as e:
            print(f"❌ {source} 失败：{e}")
        
        print()
        time.sleep(1)
    
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
