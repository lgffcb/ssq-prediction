#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易网页内容抓取工具
用法：python webcontentfetcher.py <URL>
"""

import sys
import requests
from bs4 import BeautifulSoup

def fetch_web(url):
    """抓取网页内容并提取正文"""
    try:
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 发送请求
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = response.apparent_encoding
        
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title = soup.find('title')
        title_text = title.get_text().strip() if title else '无标题'
        
        # 提取正文（尝试多种选择器）
        content_selectors = ['article', '.content', '.post-content', '#content', 'main', '.article-content']
        content = None
        
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                break
        
        # 如果没找到，提取所有段落
        if not content:
            paragraphs = soup.find_all('p')
            content = '\n'.join([p.get_text().strip() for p in paragraphs[:20]])
        else:
            content = content.get_text().strip()
        
        # 输出结果
        print(f"📄 标题：{title_text}")
        print(f"🔗 链接：{url}")
        print(f"📝 字数：{len(content)}")
        print("\n" + "="*60 + "\n")
        print(content[:3000])  # 限制输出长度
        
        return content
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python webcontentfetcher.py <URL>")
        print("示例：python webcontentfetcher.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    fetch_web(url)
