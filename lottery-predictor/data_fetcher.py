#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球历史数据获取模块
支持从多个数据源获取开奖数据
"""

import requests
import pandas as pd
import json
from datetime import datetime
from typing import Optional, List
import time


class DataFetcher:
    """双色球数据获取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_from_official(self, page: int = 1, page_size: int = 30) -> Optional[pd.DataFrame]:
        """
        从官方网站获取数据（需要实际 API）
        
        Args:
            page: 页码
            page_size: 每页数量
            
        Returns:
            DataFrame 包含开奖数据
        """
        # 这里使用模拟数据，实际使用时需要替换为真实 API
        # 官方 API 示例：https://m.zhcw.com/pchtml/kajianggonggao/ssq/list_1.html
        
        print("⚠️  官方 API 需要实际接入，使用模拟数据...")
        return self._generate_mock_data(page_size * page)
    
    def fetch_from_api(self, source: str = '17500', 
                       start_date: str = None,
                       end_date: str = None) -> pd.DataFrame:
        """
        从第三方 API 获取数据
        
        Args:
            source: 数据源 ('17500', 'zhcw', 'apihubs', '500wan', 'mock')
            start_date: 开始日期 'YYYY-MM-DD'
            end_date: 结束日期 'YYYY-MM-DD'
            
        Returns:
            DataFrame 包含开奖数据
        """
        if source == '17500':
            return self._fetch_17500_history()
        elif source == 'zhcw':
            return self._fetch_zhcw()
        elif source == 'apihubs':
            return self._fetch_apihubs()
        elif source == '500wan':
            return self._fetch_500wan()
        elif source == 'mock':
            return self._generate_mock_data(100)
        else:
            print(f"⚠️  未知数据源：{source}，使用模拟数据")
            return self._generate_mock_data(100)
    
    def _fetch_17500_history(self) -> pd.DataFrame:
        """
        从 17500 获取历史数据（TXT 接口）
        
        URL: http://www.17500.cn/getData/ssq.TXT
        
        Returns:
            DataFrame 包含历史开奖数据
        """
        import io
        
        url = "http://www.17500.cn/getData/ssq.TXT"
        
        try:
            print("📡 正在从 17500 获取历史数据...")
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"❌ 请求失败：{response.status_code}")
                return self._generate_mock_data(100)
            
            text = response.text
            print(f"✅ 获取到 {len(text)} 字节数据")
            
            # 解析 CSV 格式（空格分隔）
            df = pd.read_csv(
                io.StringIO(text),
                sep=' ',
                header=None,
                dtype=str
            )
            
            # 只保留前 9 列
            df = df.iloc[:, :9]
            df.columns = ['issue', 'date', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']
            
            # 转换数据类型
            df['issue'] = df['issue'].astype(str)
            df['date'] = df['date'].astype(str)
            
            for col in ['red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
            # 排序
            df = df.sort_values('issue', ascending=False).reset_index(drop=True)
            
            print(f"✅ 成功获取 {len(df)} 期历史数据")
            return df
            
        except Exception as e:
            print(f"❌ 17500 获取失败：{e}")
            return self._generate_mock_data(100)
    
    def _fetch_zhcw(self) -> pd.DataFrame:
        """
        从中国福彩网获取数据
        
        API: https://m.zhcw.com/pchtml/kajianggonggao/ssq/list_1.html
        """
        try:
            # 使用第三方 API（更稳定）
            url = "https://api.apihubs.com/lottery/history"
            params = {
                'size': 100,  # 获取最近 100 期
                'lottery': 'ssq'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' not in data:
                print("⚠️  API 返回数据格式异常")
                return self._generate_mock_data(100)
            
            records = []
            for item in data.get('data', []):
                # 解析红球和蓝球
                reds = [int(item.get(f'red{i}', 0)) for i in range(1, 7)]
                blue = int(item.get('blue', 0))
                
                record = {
                    'issue': item.get('issue', ''),
                    'date': item.get('date', ''),
                    'red1': reds[0],
                    'red2': reds[1],
                    'red3': reds[2],
                    'red4': reds[3],
                    'red5': reds[4],
                    'red6': reds[5],
                    'blue': blue
                }
                records.append(record)
            
            df = pd.DataFrame(records)
            
            if len(df) > 0:
                print(f"✅ 从福彩网 API 获取到 {len(df)} 期数据")
                return df
            else:
                print("⚠️  API 返回空数据，使用模拟数据")
                return self._generate_mock_data(100)
                
        except Exception as e:
            print(f"⚠️  福彩网 API 请求失败：{e}")
            print("   使用模拟数据...")
            return self._generate_mock_data(100)
    
    def _fetch_apihubs(self) -> pd.DataFrame:
        """
        从 APIHubs 获取历史数据（最多 1000 期）
        
        API: https://api.apihubs.com/lottery/history
        """
        try:
            url = "https://api.apihubs.com/lottery/history"
            params = {
                'size': 1000,
                'lottery': 'ssq'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' not in data:
                return self._generate_mock_data(100)
            
            records = []
            for item in data.get('data', []):
                reds = [int(item.get(f'red{i}', 0)) for i in range(1, 7)]
                blue = int(item.get('blue', 0))
                
                records.append({
                    'issue': item.get('issue', ''),
                    'date': item.get('date', ''),
                    'red1': reds[0], 'red2': reds[1], 'red3': reds[2],
                    'red4': reds[3], 'red5': reds[4], 'red6': reds[5],
                    'blue': blue
                })
            
            df = pd.DataFrame(records)
            print(f"✅ 从 APIHubs 获取到 {len(df)} 期历史数据")
            return df
            
        except Exception as e:
            print(f"⚠️  APIHubs 请求失败：{e}")
            return self._generate_mock_data(100)
    
    def _fetch_500wan(self) -> pd.DataFrame:
        """
        从 500 彩票网获取数据（网页爬虫）
        
        URL: http://kaijiang.500.com/ssq.shtml
        """
        try:
            from bs4 import BeautifulSoup
            
            url = "http://kaijiang.500.com/ssq.shtml"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            response.encoding = 'gb2312'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id': 'tdata'})
            
            if not table:
                return self._generate_mock_data(100)
            
            records = []
            for row in table.find_all('tr')[1:]:  # 跳过表头
                cols = row.find_all('td')
                if len(cols) >= 9:
                    issue = cols[0].text.strip()
                    date = cols[1].text.strip()
                    reds = [int(cols[i].text) for i in range(2, 8)]
                    blue = int(cols[8].text)
                    
                    records.append({
                        'issue': issue,
                        'date': date,
                        'red1': reds[0], 'red2': reds[1], 'red3': reds[2],
                        'red4': reds[3], 'red5': reds[4], 'red6': reds[5],
                        'blue': blue
                    })
            
            df = pd.DataFrame(records)
            print(f"✅ 从 500 彩票网获取到 {len(df)} 期数据")
            return df
            
        except ImportError:
            print("⚠️  BeautifulSoup 未安装，无法爬取 500 彩票网")
            return self._generate_mock_data(100)
        except Exception as e:
            print(f"⚠️  500 彩票网爬取失败：{e}")
            return self._generate_mock_data(100)
    
    def _fetch_kaijiang_api(self, start_date: str = None, 
                            end_date: str = None) -> pd.DataFrame:
        """
        从开奖网 API 获取数据（保留向后兼容）
        """
        return self._fetch_zhcw()
    
    def _generate_mock_data(self, n_draws: int = 100) -> pd.DataFrame:
        """
        生成模拟历史数据
        
        Args:
            n_draws: 生成多少期数据
            
        Returns:
            DataFrame 包含模拟数据
        """
        import numpy as np
        np.random.seed(int(time.time()))
        
        data = []
        base_date = datetime.now()
        
        for i in range(n_draws):
            # 生成红球（1-33 选 6）
            reds = sorted(np.random.choice(33, 6, replace=False) + 1)
            # 生成蓝球（1-16 选 1）
            blue = np.random.randint(1, 17)
            
            # 期号（模拟）
            issue = f"2026{((n_draws - i) % 100) + 1:03d}"
            
            # 日期（每 3 天一期）
            draw_date = base_date - pd.Timedelta(days=(n_draws - i) * 3)
            
            data.append({
                'issue': issue,
                'date': draw_date.strftime('%Y-%m-%d'),
                'red1': reds[0],
                'red2': reds[1],
                'red3': reds[2],
                'red4': reds[3],
                'red5': reds[4],
                'red6': reds[5],
                'blue': blue
            })
        
        df = pd.DataFrame(data)
        return df
    
    def save_to_csv(self, df: pd.DataFrame, file_path: str):
        """保存数据到 CSV"""
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"✅ 数据已保存到：{file_path}")
    
    def load_from_csv(self, file_path: str) -> pd.DataFrame:
        """从 CSV 加载数据"""
        import os
        
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在：{file_path}")
            return None
        
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        print(f"✅ 已加载 {len(df)} 期数据")
        return df
    
    def update_data(self, file_path: str = 'data/historical_data.csv',
                    source: str = 'mock',
                    auto: bool = False) -> pd.DataFrame:
        """
        更新数据
        
        Args:
            file_path: 数据文件路径
            source: 数据源
            auto: 是否自动模式（静默更新）
            
        Returns:
            更新后的 DataFrame
        """
        import os
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 加载现有数据
        if os.path.exists(file_path):
            existing_df = self.load_from_csv(file_path)
            existing_count = len(existing_df)
            
            # 获取最后一期信息
            if 'issue' in existing_df.columns:
                last_issue = existing_df.iloc[-1]['issue']
                last_date = existing_df.iloc[-1]['date'] if 'date' in existing_df.columns else None
            else:
                last_issue = None
                last_date = None
        else:
            existing_df = None
            existing_count = 0
            last_issue = None
            last_date = None
        
        if not auto:
            print("📡 获取最新数据...")
        
        # 获取新数据
        new_df = self.fetch_from_api(source, start_date=last_date)
        
        # 如果有期号，进行增量更新
        if existing_df is not None and 'issue' in existing_df.columns and 'issue' in new_df.columns:
            # 只保留新期号
            if last_issue:
                new_df = new_df[~new_df['issue'].isin(existing_df['issue'])]
        
        # 如果有新数据
        if len(new_df) > 0:
            # 合并数据（先去重）
            if existing_df is not None and len(existing_df) > 0:
                # 移除 existing_df 中已经存在的期号
                if 'issue' in new_df.columns and 'issue' in existing_df.columns:
                    new_df = new_df[~new_df['issue'].isin(existing_df['issue'])]
                
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                combined_df = new_df
            
            # 去重
            combined_df = combined_df.drop_duplicates(
                subset=['issue'] if 'issue' in combined_df.columns else ['red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue'],
                keep='last'
            )
            
            # 排序
            if 'date' in combined_df.columns:
                combined_df = combined_df.sort_values('date').reset_index(drop=True)
            elif 'issue' in combined_df.columns:
                combined_df = combined_df.sort_values('issue').reset_index(drop=True)
            
            # 保存
            self.save_to_csv(combined_df, file_path)
            
            new_count = len(combined_df)
            added_count = new_count - existing_count
            
            if not auto:
                print(f"📊 数据更新完成：{existing_count} → {new_count} 期 (新增 {added_count} 期)")
            
            return combined_df
        else:
            if not auto:
                print(f"✅ 数据已是最新（共 {existing_count} 期）")
            return existing_df
    
    def check_for_new_draw(self, file_path: str = 'data/historical_data.csv',
                           source: str = 'mock') -> bool:
        """
        检查是否有新开奖数据
        
        Args:
            file_path: 数据文件路径
            source: 数据源
            
        Returns:
            True 如果有新数据，False 如果已是最新
        """
        import os
        
        if not os.path.exists(file_path):
            return True  # 没有文件，需要下载
        
        # 加载现有数据
        existing_df = self.load_from_csv(file_path)
        
        if len(existing_df) == 0:
            return True
        
        # 获取最新一期
        if 'issue' in existing_df.columns:
            last_issue = existing_df.iloc[-1]['issue']
        else:
            last_issue = None
        
        # 获取最新数据（只获取最近几期）
        print("🔍 检查最新开奖...")
        latest_df = self.fetch_from_api(source)
        
        if len(latest_df) == 0:
            return False
        
        # 检查是否有新期号
        if last_issue and 'issue' in latest_df.columns:
            latest_issue = latest_df.iloc[-1]['issue']
            return latest_issue != last_issue
        
        # 检查日期
        if 'date' in existing_df.columns and 'date' in latest_df.columns:
            last_date = existing_df.iloc[-1]['date']
            latest_date = latest_df.iloc[-1]['date']
            return latest_date != last_date
        
        return True
    
    def auto_update(self, file_path: str = 'data/historical_data.csv',
                    source: str = 'mock',
                    check_interval: str = 'daily') -> pd.DataFrame:
        """
        自动更新数据
        
        Args:
            file_path: 数据文件路径
            source: 数据源
            check_interval: 检查间隔 ('daily', 'weekly', 'always')
            
        Returns:
            更新后的 DataFrame
        """
        import os
        from datetime import datetime, timedelta
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        print("=" * 60)
        print("🔄 双色球数据自动更新")
        print("=" * 60)
        print(f"\n📂 数据文件：{file_path}")
        print(f"📡 数据源：{source}")
        print(f"⏰ 检查间隔：{check_interval}")
        print()
        
        # 检查是否需要更新
        should_update = False
        
        if check_interval == 'always':
            should_update = True
            print("ℹ️  模式：总是更新")
        elif os.path.exists(file_path):
            # 检查文件最后修改时间
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            file_age = datetime.now() - file_mtime
            
            if check_interval == 'daily':
                if file_age >= timedelta(days=1):
                    should_update = True
                    print(f"ℹ️  数据已 {file_age.days} 天未更新")
                else:
                    print(f"✅ 数据较新（{file_age.seconds // 3600} 小时前更新过）")
            elif check_interval == 'weekly':
                if file_age >= timedelta(days=7):
                    should_update = True
                    print(f"ℹ️  数据已 {file_age.days} 天未更新")
                else:
                    print(f"✅ 数据较新（{file_age.days} 天前更新过）")
        else:
            should_update = True
            print("ℹ️  首次使用，需要下载数据")
        
        if should_update:
            print("\n📡 正在更新数据...")
            return self.update_data(file_path, source, auto=False)
        else:
            # 加载现有数据
            return self.load_from_csv(file_path)


def download_sample_data():
    """下载示例数据"""
    fetcher = DataFetcher()
    df = fetcher.fetch_from_api(source='mock')
    fetcher.save_to_csv(df, 'data/historical_data.csv')
    return df


if __name__ == '__main__':
    import os
    
    print("=" * 60)
    print("📡 双色球数据获取工具")
    print("=" * 60)
    
    fetcher = DataFetcher()
    
    # 获取数据
    print("\n📡 正在获取数据...")
    df = fetcher.fetch_from_api(source='mock')
    
    print(f"\n✅ 获取到 {len(df)} 期数据")
    print("\n最近 5 期开奖:")
    print(df.tail(5).to_string(index=False))
    
    # 保存数据
    os.makedirs('data', exist_ok=True)
    fetcher.save_to_csv(df, 'data/historical_data.csv')
    
    print("\n" + "=" * 60)
