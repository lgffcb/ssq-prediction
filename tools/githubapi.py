#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub API 工具 - 调用 GitHub API
"""

import os
import sys
import requests
from datetime import datetime

# GitHub API 基础 URL
GITHUB_API = "https://api.github.com"

def search_repos(query, limit=5):
    """搜索仓库"""
    url = f"{GITHUB_API}/search/repositories"
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': limit
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"🔍 搜索：{query}")
        print(f"📊 结果数：{data['total_count']}\n")
        
        for i, repo in enumerate(data['items'][:limit], start=1):
            print(f"{i}. ⭐ {repo['full_name']}")
            print(f"   📝 {repo['description'] or '无描述'}")
            print(f"   ⭐ Stars: {repo['stargazers_count']:,}")
            print(f"   🍴 Forks: {repo['forks_count']:,}")
            print(f"   📅 更新：{repo['updated_at'][:10]}")
            print(f"   🔗 {repo['html_url']}\n")
    else:
        print(f"❌ 错误：{response.status_code}")
        print(response.json())

def get_user_info(username):
    """获取用户信息"""
    url = f"{GITHUB_API}/users/{username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        user = response.json()
        print(f"👤 GitHub 用户：{user['login']}")
        print(f"   📛 姓名：{user.get('name', '未设置')}")
        print(f"   📍 位置：{user.get('location', '未设置')}")
        print(f"   📦 公开仓库：{user['public_repos']}")
        print(f"   👥 关注者：{user['followers']:,}")
        print(f"   📅 加入：{user['created_at'][:10]}")
        print(f"   🔗 {user['html_url']}")
    else:
        print(f"❌ 未找到用户：{username}")

def get_trending(limit=5):
    """获取热门仓库（通过搜索）"""
    # 搜索今天热门的仓库
    today = datetime.now().strftime('%Y-%m-%d')
    query = f"created:>{today} sort:stars"
    
    url = f"{GITHUB_API}/search/repositories"
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': limit
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"🔥 今日热门仓库 ({today})\n")
        
        for i, repo in enumerate(data['items'][:limit], start=1):
            print(f"{i}. ⭐ {repo['full_name']}")
            print(f"   📝 {repo['description'] or '无描述'}")
            print(f"   ⭐ Stars: {repo['stargazers_count']:,}")
            print(f"   🔗 {repo['html_url']}\n")
    else:
        print(f"❌ 错误：{response.status_code}")

def get_repo_info(owner, repo):
    """获取仓库信息"""
    url = f"{GITHUB_API}/repos/{owner}/{repo}"
    response = requests.get(url)
    
    if response.status_code == 200:
        repo = response.json()
        print(f"📦 仓库：{repo['full_name']}")
        print(f"   📝 {repo['description'] or '无描述'}")
        print(f"   ⭐ Stars: {repo['stargazers_count']:,}")
        print(f"   🍴 Forks: {repo['forks_count']:,}")
        print(f"   📎 主分支：{repo['default_branch']}")
        print(f"   📄 License: {repo['license']['name'] if repo['license'] else '无'}")
        print(f"   🔗 {repo['html_url']}")
    else:
        print(f"❌ 未找到仓库：{owner}/{repo}")

def main():
    if len(sys.argv) < 2:
        print("GitHub API 工具")
        print("\n用法:")
        print("  python githubapi.py search <关键词>     - 搜索仓库")
        print("  python githubapi.py user <用户名>       - 获取用户信息")
        print("  python githubapi.py trending            - 热门仓库")
        print("  python githubapi.py repo <所有者/仓库>  - 仓库详情")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'search':
        query = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'AI'
        search_repos(query)
    elif command == 'user':
        username = sys.argv[2] if len(sys.argv) > 2 else 'torvalds'
        get_user_info(username)
    elif command == 'trending':
        get_trending()
    elif command == 'repo':
        if len(sys.argv) < 3:
            print("❌ 请提供仓库路径，如：microsoft/vscode")
            sys.exit(1)
        owner_repo = sys.argv[2]
        if '/' in owner_repo:
            owner, repo = owner_repo.split('/', 1)
            get_repo_info(owner, repo)
        else:
            print("❌ 格式错误，应为：所有者/仓库")
    else:
        print(f"❌ 未知命令：{command}")

if __name__ == '__main__':
    main()
