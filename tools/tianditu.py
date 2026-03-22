#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天地图 API 工具
支持：地理编码、逆地理编码、搜索、路线规划等
"""

import os
import sys
import requests
import webbrowser

API_KEY = "55362d559694da0d42206960bd48e98c"
BASE_URL = "http://api.tianditu.gov.cn"

def search(keyword, types=None, count=10):
    """搜索地点"""
    url = f"{BASE_URL}/search/v2"
    params = {
        'ds': 'map',
        'keyWord': keyword,
        'count': count,
        'tk': API_KEY
    }
    if types:
        params['types'] = types
    
    response = requests.get(url, params=params)
    result = response.json()
    
    if result.get('status') == 1:
        print(f"\n✅ 找到 {len(result.get('data', []))} 个结果")
        for i, item in enumerate(result.get('data', []), start=1):
            print(f"\n{i}. {item.get('title', '未知')}")
            print(f"   地址：{item.get('address', '无')}")
            print(f"   坐标：{item.get('lon', '?')}, {item.get('lat', '?')}")
            if item.get('tel'):
                print(f"   电话：{item.get('tel')}")
    else:
        print(f"❌ 搜索失败：{result.get('msg', '未知错误')}")
    
    return result

def geocode(address):
    """地理编码：地址转坐标"""
    url = f"{BASE_URL}/geocoding/v2"
    params = {
        'ds': 'map',
        'address': address,
        'tk': API_KEY
    }
    
    response = requests.get(url, params=params)
    result = response.json()
    
    if result.get('status') == 1:
        location = result.get('location', {})
        print(f"\n✅ 地理编码成功")
        print(f"   地址：{address}")
        print(f"   经度：{location.get('lon', '?')}")
        print(f"   纬度：{location.get('lat', '?')}")
    else:
        print(f"❌ 地理编码失败：{result.get('msg', '未知错误')}")
    
    return result

def reverse_geocode(lon, lat):
    """逆地理编码：坐标转地址"""
    url = f"{BASE_URL}/geocoding/v2"
    params = {
        'ds': 'map',
        'location': f"{lon},{lat}",
        'tk': API_KEY
    }
    
    response = requests.get(url, params=params)
    result = response.json()
    
    if result.get('status') == 1:
        print(f"\n✅ 逆地理编码成功")
        print(f"   坐标：{lon}, {lat}")
        print(f"   地址：{result.get('address', '无')}")
        print(f"   语义：{result.get('semantic', '无')}")
    else:
        print(f"❌ 逆地理编码失败：{result.get('msg', '未知错误')}")
    
    return result

def open_map(lon, lat, zoom=15):
    """在浏览器中打开天地图"""
    url = f"https://map.tianditu.gov.cn/?lon={lon}&lat={lat}&level={zoom}&mapmode=2d"
    webbrowser.open(url)
    print(f"\n🗺️ 已在浏览器中打开天地图")
    print(f"   位置：{lon}, {lat}")
    print(f"   缩放级别：{zoom}")

def main():
    print("🌍 天地图 API 工具\n")
    print("=" * 50)
    print(f"API Key: {API_KEY[:20]}...")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("\n用法:")
        print("  python tianditu.py search <关键词>     - 搜索地点")
        print("  python tianditu.py geocode <地址>      - 地址转坐标")
        print("  python tianditu.py reverse <经度> <纬度> - 坐标转地址")
        print("  python tianditu.py open <经度> <纬度>  - 打开地图")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'search':
        keyword = ' '.join(sys.argv[2:])
        search(keyword)
    elif command == 'geocode':
        address = ' '.join(sys.argv[2:])
        geocode(address)
    elif command == 'reverse':
        if len(sys.argv) < 4:
            print("❌ 请提供经度和纬度")
            sys.exit(1)
        lon, lat = sys.argv[2], sys.argv[3]
        reverse_geocode(lon, lat)
    elif command == 'open':
        if len(sys.argv) < 4:
            print("❌ 请提供经度和纬度")
            sys.exit(1)
        lon, lat = sys.argv[2], sys.argv[3]
        open_map(lon, lat)
    else:
        print(f"❌ 未知命令：{command}")

if __name__ == '__main__':
    main()
