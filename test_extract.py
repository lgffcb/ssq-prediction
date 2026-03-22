#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Excel 数据提取工具 - 命令行测试版 v3 (支持 xls)"""

import pandas as pd
import xlrd
import os
import sys
import glob

def get_column_letter(col_index):
    """列索引转字母"""
    result = ""
    while col_index >= 0:
        result = chr(ord('A') + (col_index % 26)) + result
        col_index = col_index // 26 - 1
    return result

def extract_data(file_path, search_term):
    """提取数据"""
    print("="*60)
    print("🔧 正在处理 Excel 文件...")
    
    # 判断文件类型
    is_xls = file_path.endswith('.xls')
    
    if is_xls:
        # xls 文件用 xlrd 读取
        wb = xlrd.open_workbook(file_path)
        all_sheet_names = wb.sheet_names()
        print(f"\n📊 文件包含 {len(all_sheet_names)} 个工作表:")
        for name in all_sheet_names:
            print(f"   - {name}")
        
        # 查找明细表
        target_sheet = None
        target_idx = 0
        for i, sheet_name in enumerate(all_sheet_names):
            if '明细' in sheet_name:
                target_sheet = sheet_name
                target_idx = i
                break
        
        if not target_sheet:
            print(f"\n⚠️  未找到包含'明细'的工作表，使用第一个工作表")
            target_sheet = all_sheet_names[0]
        else:
            print(f"\n✅ 找到明细工作表：【{target_sheet}】(索引 {target_idx})")
        
        # 读取数据
        sheet = wb.sheet_by_index(target_idx)
        print(f"📋 工作表大小：{sheet.nrows} 行 × {sheet.ncols} 列")
        
        # 转换为 DataFrame
        data = []
        for row_idx in range(sheet.nrows):
            row = [sheet.cell(row_idx, col_idx).value for col_idx in range(sheet.ncols)]
            data.append(row)
        
        df = pd.DataFrame(data)
        
    else:
        # xlsx 文件
        wb = pd.ExcelFile(file_path)
        all_sheet_names = wb.sheet_names
        print(f"\n📊 文件包含 {len(all_sheet_names)} 个工作表:")
        for name in all_sheet_names:
            print(f"   - {name}")
        
        # 查找明细表
        target_sheet = None
        for sheet_name in all_sheet_names:
            if '明细' in sheet_name:
                target_sheet = sheet_name
                break
        
        if not target_sheet:
            print(f"\n⚠️  未找到包含'明细'的工作表，使用第一个工作表")
            target_sheet = all_sheet_names[0]
        else:
            print(f"\n✅ 找到明细工作表：【{target_sheet}】")
        
        df = pd.read_excel(file_path, sheet_name=target_sheet)
    
    # 搜索
    print(f"\n🔍 正在搜索包含'{search_term}'的行...")
    df_str = df.astype(str)
    mask = df_str.apply(lambda col: col.str.contains(str(search_term), na=False, case=False)).any(axis=1)
    matched_rows = df[mask]
    
    if len(matched_rows) == 0:
        print(f"❌ 未找到包含'{search_term}'的行")
        return None
    
    print(f"✅ 找到 {len(matched_rows)} 条匹配记录")
    
    # 找出包含查找内容的列
    print(f"\n📊 正在分析包含'{search_term}'的列...")
    columns_to_extract = []
    column_names = []
    
    for col_idx in range(len(df.columns)):
        col_data = df_str.iloc[:, col_idx]
        if col_data.str.contains(str(search_term), na=False, case=False).any():
            col_letter = get_column_letter(col_idx)
            col_name = str(df.columns[col_idx]) if col_idx < len(df.columns) else f"列{col_idx}"
            columns_to_extract.append(col_idx)
            column_names.append(f'{col_letter}列')
            # 显示列名和示例值
            sample_val = col_data[col_data.str.contains(str(search_term), na=False, case=False)].iloc[0] if len(col_data[col_data.str.contains(str(search_term), na=False, case=False)]) > 0 else ''
            print(f"   ✅ {col_letter}列 ({col_name[:50]}) - 示例：{str(sample_val)[:50]}")
    
    if not columns_to_extract:
        print("❌ 没有找到包含查找内容的列")
        return None
    
    print(f"\n✅ 共 {len(columns_to_extract)} 列包含查找内容")
    
    # 提取数据
    result = matched_rows.iloc[:, columns_to_extract].copy()
    result.columns = column_names
    
    # 保存
    output_file = os.path.splitext(file_path)[0] + '_提取结果.xlsx'
    result.to_excel(output_file, index=False)
    
    print(f"\n{'='*60}")
    print("✅ 数据提取完成！")
    print(f"📁 结果已保存到：{output_file}")
    print(f"📊 提取结果：{len(result)} 行 × {len(result.columns)} 列")
    
    # 显示前 5 行
    print("\n前 5 行数据预览:")
    print(result.head().to_string(index=False))
    
    return output_file

if __name__ == "__main__":
    # 查找 Downloads 目录下的 Excel 文件
    download_dir = "/home/admin/Downloads"
    
    if not os.path.exists(download_dir):
        print(f"❌ 目录不存在：{download_dir}")
        sys.exit(1)
    
    # 查找 Excel 文件
    excel_files = glob.glob(os.path.join(download_dir, "*.xlsx"))
    excel_files.extend(glob.glob(os.path.join(download_dir, "*.xls")))
    
    if not excel_files:
        print(f"❌ 目录中没有 Excel 文件：{download_dir}")
        sys.exit(1)
    
    print(f"📂 找到 {len(excel_files)} 个 Excel 文件:")
    for i, f in enumerate(excel_files, 1):
        size_mb = os.path.getsize(f) / 1024 / 1024
        print(f"   {i}. {os.path.basename(f)} ({size_mb:.2f} MB)")
    
    # 使用第一个文件
    test_file = excel_files[0]
    print(f"\n📋 使用文件：{os.path.basename(test_file)}")
    
    # 输入查找内容
    if len(sys.argv) > 1:
        search_term = sys.argv[1]
    else:
        search_term = input("\n🔍 请输入要查找的内容：").strip()
        if not search_term:
            print("❌ 未输入查找内容")
            sys.exit(1)
    
    print(f"查找内容：{search_term}")
    print()
    
    result = extract_data(test_file, search_term)
    
    if result:
        print("\n✅ 测试成功！")
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)
