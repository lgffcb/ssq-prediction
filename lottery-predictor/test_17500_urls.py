#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 17500 不同 URL 格式
"""

import requests
from bs4 import BeautifulSoup
import re

urls_to_try = [
    "https://www.17500.cn/ssq/kaijiang.php",
    "https://www.17500.cn/ssq/kaijiang.htm",
    "https://www.17500.cn/ssq/",
    "https://m.17500.cn/ssq/kaijiang.php",
    "https://www.17500.cn/ssq/history.php",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

print("=" * 60)
print("🧪 测试 17500 网站 URL")
print("=" * 60)

for url in urls_to_try:
    print(f"\n测试：{url}")
    print("-" * 60)
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"状态码：{response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ 成功！页面大小：{len(response.text)} 字节")
            
            # 检查是否有数据
            if '双色球' in response.text or 'ssq' in response.text.lower():
                print("✅ 包含双色球数据")
                
                # 尝试提取期号
                issues = re.findall(r'(\d{7})', response.text)[:5]
                if issues:
                    print(f"找到期号：{issues}")
            
            # 保存 HTML 用于分析
            with open('test_17500.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("💾 HTML 已保存到：test_17500.html")
            
            break
        else:
            print(f"❌ 失败")
    
    except Exception as e:
        print(f"❌ 错误：{e}")

print("\n" + "=" * 60)
