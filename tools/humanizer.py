#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Humanizer - 文本人性化处理工具
"""

import humanize
import sys

def humanize_number(num):
    """数字人性化"""
    return humanize.intword(num)

def humanize_time(seconds):
    """时间人性化"""
    return humanize.naturaltime(seconds)

def humanize_filesize(bytes):
    """文件大小人性化"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(bytes) < 1024.0:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024.0
    return f"{bytes:.1f}PB"

def main():
    if len(sys.argv) < 2:
        print("Humanizer - 文本人性化处理")
        print("\n用法:")
        print("  python humanizer.py number <数字>")
        print("  python humanizer.py time <秒数>")
        print("  python humanizer.py filesize <字节数>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'number':
        num = sys.argv[2]
        print(f"{num} = {humanize_number(int(num))}")
    
    elif command == 'time':
        seconds = sys.argv[2]
        print(f"{seconds}秒 = {humanize_time(int(seconds))}")
    
    elif command == 'filesize':
        bytes = sys.argv[2]
        print(f"{bytes}字节 = {humanize_filesize(int(bytes))}")
    
    else:
        print(f"❌ 未知命令：{command}")

if __name__ == '__main__':
    main()
