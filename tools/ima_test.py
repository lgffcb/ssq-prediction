#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMA API 测试工具
"""

import os
import sys
import requests

BASE_URL = "https://ima.qq.com/openapi/note/v1"

def check_env():
    """检查环境变量"""
    client_id = os.environ.get('IMA_OPENAPI_CLIENTID')
    api_key = os.environ.get('IMA_OPENAPI_APIKEY')
    
    if not client_id:
        print("❌ 缺少 IMA_OPENAPI_CLIENTID 环境变量")
        return None, None
    if not api_key:
        print("❌ 缺少 IMA_OPENAPI_APIKEY 环境变量")
        return None, None
    
    print("✅ 环境变量配置正确")
    return client_id, api_key

def list_folders(client_id, api_key):
    """列出笔记本"""
    url = f"{BASE_URL}/list_note_folder_by_cursor"
    headers = {
        'ima-openapi-clientid': client_id,
        'ima-openapi-apikey': api_key,
        'Content-Type': 'application/json'
    }
    data = {"cursor": "0", "limit": 10}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if result.get('code', -1) == 0:
            print(f"\n✅ 找到 {len(result.get('note_book_folders', []))} 个笔记本")
            for folder in result.get('note_book_folders', []):
                basic = folder.get('folder', {}).get('basic_info', {})
                print(f"   📚 {basic.get('name')} ({basic.get('note_number')} 篇笔记)")
        else:
            print(f"❌ API 错误：{result.get('code')} - {result.get('msg', '未知错误')}")
    except Exception as e:
        print(f"❌ 请求失败：{e}")

def main():
    print("📝 IMA API 测试工具\n")
    print("=" * 50)
    
    client_id, api_key = check_env()
    if not client_id:
        print("\n📖 配置指南：")
        print("   1. 访问 https://ima.qq.com/agent-interface")
        print("   2. 获取 Client ID 和 API Key")
        print("   3. 设置环境变量:")
        print("      export IMA_OPENAPI_CLIENTID=\"your_id\"")
        print("      export IMA_OPENAPI_APIKEY=\"your_key\"")
        sys.exit(1)
    
    print("=" * 50)
    print("\n🧪 测试笔记本列表...\n")
    list_folders(client_id, api_key)
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")

if __name__ == '__main__':
    main()
