#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tavily Search - AI 优化搜索引擎
"""

import os
import sys
from tavily import TavilyClient

def search(query, api_key=None, max_results=5):
    """搜索"""
    if not api_key:
        api_key = os.environ.get('TAVILY_API_KEY')
    
    if not api_key:
        print("❌ 请设置 TAVILY_API_KEY 环境变量")
        return None
    
    client = TavilyClient(api_key=api_key)
    response = client.search(query, max_results=max_results)
    
    print(f"🔍 搜索：{query}")
    print(f"📊 结果数：{len(response.get('results', []))}\n")
    
    for i, result in enumerate(response.get('results', [])[:max_results], start=1):
        print(f"{i}. {result.get('title', '无标题')}")
        print(f"   {result.get('content', '无摘要')}")
        print(f"   🔗 {result.get('url', '')}\n")
    
    return response

def main():
    if len(sys.argv) < 2:
        print("Tavily Search - AI 优化搜索引擎")
        print("\n用法:")
        print("  python tavilysearch.py <搜索关键词>")
        print("\n需要设置环境变量：TAVILY_API_KEY")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    search(query)

if __name__ == '__main__':
    main()
