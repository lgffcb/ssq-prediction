#!/usr/bin/env python3
# 快速测试 API

from data_fetcher import DataFetcher
import sys

print("=" * 60)
print("🧪 测试彩票 API")
print("=" * 60)

fetcher = DataFetcher()

# 测试 1: 福彩网
print("\n1️⃣ 福彩网 (zhcw)...")
try:
    df = fetcher.fetch_from_api('zhcw')
    if df is not None and len(df) > 0:
        print(f"   ✅ 成功：{len(df)} 期")
        print(f"   最新：{df.iloc[-1]['issue']} ({df.iloc[-1]['date']})")
    else:
        print(f"   ⚠️  空数据")
except Exception as e:
    print(f"   ❌ 失败：{e}")

# 测试 2: APIHubs
print("\n2️⃣ APIHubs (apihubs)...")
try:
    df = fetcher.fetch_from_api('apihubs')
    if df is not None and len(df) > 0:
        print(f"   ✅ 成功：{len(df)} 期")
        print(f"   最新：{df.iloc[-1]['issue']} ({df.iloc[-1]['date']})")
    else:
        print(f"   ⚠️  空数据")
except Exception as e:
    print(f"   ❌ 失败：{e}")

# 测试 3: 模拟数据
print("\n3️⃣ 模拟数据 (mock)...")
try:
    df = fetcher.fetch_from_api('mock')
    print(f"   ✅ 成功：{len(df)} 期")
except Exception as e:
    print(f"   ❌ 失败：{e}")

print("\n" + "=" * 60)
