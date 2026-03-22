#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel 数据提取工具 - 命令行版本
- 命令行输入查找内容
- 先处理 Excel：显示所有隐藏表格、取消行列隐藏、公式转数值
- 自动查找 sheet 名包含"明细"的工作表
- 在该表中搜索匹配内容
- 动态提取匹配行中包含查找内容的列及其数据
"""

import pandas as pd
from openpyxl import load_workbook
import os
import sys

def get_column_letter(col_index):
    """将列索引转换为 Excel 列字母 (0=A, 1=B, ..., 9=J, 15=P, etc.)"""
    result = ""
    while col_index >= 0:
        result = chr(ord('A') + (col_index % 26)) + result
        col_index = col_index // 26 - 1
    return result

def unhide_and_convert_values(file_path):
    """
    处理 Excel 文件：
    1. 显示所有隐藏的工作表
    2. 取消所有隐藏的行和列
    3. 将所有公式转换为数值
    返回处理后的临时文件路径
    """
    try:
        print("\n🔧 正在处理 Excel 文件...")
        
        # 加载工作簿
        wb = load_workbook(file_path)
        
        # 1. 显示所有隐藏的工作表
        hidden_sheets = []
        for sheet in wb.worksheets:
            if sheet.sheet_state == 'hidden':
                sheet.sheet_state = 'visible'
                hidden_sheets.append(sheet.title)
        
        if hidden_sheets:
            print(f"   ✅ 显示了 {len(hidden_sheets)} 个隐藏的工作表：{hidden_sheets}")
        else:
            print("   ✅ 没有隐藏的工作表")
        
        # 2 & 3. 对每个工作表：取消行列隐藏 + 公式转数值
        total_hidden_rows = 0
        total_hidden_cols = 0
        
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            
            # 取消行隐藏
            hidden_rows = 0
            for row_dim in sheet.row_dimensions.values():
                if row_dim.hidden:
                    row_dim.hidden = False
                    hidden_rows += 1
            total_hidden_rows += hidden_rows
            
            # 取消列隐藏
            hidden_cols = 0
            for col_dim in sheet.column_dimensions.values():
                if col_dim.hidden:
                    col_dim.hidden = False
                    hidden_cols += 1
            total_hidden_cols += hidden_cols
        
        print(f"   ✅ 取消了 {total_hidden_rows} 个隐藏行")
        print(f"   ✅ 取消了 {total_hidden_cols} 个隐藏列")
        
        # 保存为临时文件（公式已转为数值）
        temp_file = os.path.splitext(file_path)[0] + '_processed.xlsx'
        
        # 创建新工作簿，只保留数值
        from openpyxl import Workbook
        wb_new = Workbook()
        wb_new.remove(wb_new.active)  # 移除默认 sheet
        
        for sheet_name in wb.sheetnames:
            old_sheet = wb[sheet_name]
            new_sheet = wb_new.create_sheet(title=sheet_name)
            
            # 复制数据（只复制值，不复制公式）
            for row in old_sheet.iter_rows(values_only=True):
                if any(cell is not None for cell in row):  # 跳过空行
                    new_sheet.append(row)
            
            # 复制列宽
            for col_letter, col_dim in old_sheet.column_dimensions.items():
                if col_dim.width:
                    new_sheet.column_dimensions[col_letter].width = col_dim.width
        
        wb_new.save(temp_file)
        
        print(f"   ✅ 公式已转换为数值")
        print(f"   📁 处理后的文件：{temp_file}")
        
        return temp_file
        
    except Exception as e:
        print(f"   ❌ 处理失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return None

def find_detail_sheet(sheet_names):
    """查找包含"明细"的工作表"""
    for sheet_name in sheet_names:
        if '明细' in sheet_name:
            return sheet_name
    return None

def search_and_extract(file_path, search_term):
    """在 Excel 文件的明细表中搜索并动态提取数据"""
    try:
        # 读取所有 sheet
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        
        sheet_names = list(all_sheets.keys())
        print(f"\n📊 文件包含 {len(sheet_names)} 个工作表：{sheet_names}")
        
        # 查找"明细表"
        target_sheet = find_detail_sheet(sheet_names)
        
        if not target_sheet:
            print(f"\n❌ 未找到包含'明细'的工作表")
            print(f"可用的工作表：{', '.join(sheet_names)}")
            return None
        
        print(f"\n✅ 找到明细工作表：【{target_sheet}】")
        
        df = all_sheets[target_sheet]
        print(f"工作表大小：{len(df)} 行 × {len(df.columns)} 列")
        
        # 将搜索列转换为字符串以便搜索
        df_str = df.astype(str)
        
        # 搜索包含查找内容的行
        mask = df_str.apply(lambda col: col.str.contains(str(search_term), na=False, case=False)).any(axis=1)
        matched_rows = df[mask]
        
        if len(matched_rows) == 0:
            print(f"\n❌ 未找到包含'{search_term}'的行")
            return None
        
        print(f"\n✅ 找到 {len(matched_rows)} 条匹配记录")
        
        # 对于每个匹配的行，找出哪些列包含查找内容
        all_results = []
        
        for idx, row in matched_rows.iterrows():
            row_data = {}
            row_str = df_str.loc[idx].astype(str)
            
            # 找出该行中包含查找内容的所有列
            matching_cols = row_str[row_str.str.contains(str(search_term), na=False, case=False)].index.tolist()
            
            # 提取这些列的数据，加上列字母标识
            for col in matching_cols:
                col_idx = df.columns.get_loc(col)
                col_letter = get_column_letter(col_idx)
                row_data[f'{col_letter}列'] = row[col]
            
            if row_data:
                all_results.append(row_data)
        
        if not all_results:
            print("未找到匹配的列数据")
            return None
        
        # 转换为 DataFrame
        result = pd.DataFrame(all_results)
        
        # 打印结果
        print("\n" + "="*80)
        print(f"查找内容：{search_term}")
        print(f"明细工作表：{target_sheet}")
        print(f"匹配行数：{len(result)}")
        print("="*80)
        print(result.to_string(index=False))
        print("="*80)
        
        # 保存结果到新 Excel 文件
        output_file = os.path.splitext(file_path)[0] + '_提取结果.xlsx'
        result.to_excel(output_file, index=False)
        print(f"\n✅ 结果已保存到：{output_file}")
        
        return result
        
    except Exception as e:
        print(f"❌ 错误：{str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """主函数"""
    print("="*60)
    print("Excel 数据提取工具 - 明细表专用 (命令行版)")
    print("="*60)
    
    # 获取文件路径
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("\n📂 请输入 Excel 文件路径：").strip()
    
    if not file_path:
        print("未输入文件路径，程序退出")
        return
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在：{file_path}")
        return
    
    print(f"已选择文件：{file_path}")
    
    # 先处理 Excel：显示隐藏表格、取消行列隐藏、公式转数值
    processed_file = unhide_and_convert_values(file_path)
    if not processed_file:
        print("❌ Excel 文件处理失败，程序退出")
        return
    
    # 获取查找内容
    search_term = input("\n🔍 请输入要查找的内容：").strip()
    if not search_term:
        print("未输入查找内容，程序退出")
        return
    
    print(f"查找内容：{search_term}")
    
    # 搜索并提取
    result = search_and_extract(processed_file, search_term)
    
    if result is not None:
        print("\n✅ 数据提取完成！")
        print(f"📋 结果已保存到：{os.path.splitext(file_path)[0] + '_提取结果.xlsx'}")
    else:
        print("\n❌ 数据提取失败")

if __name__ == "__main__":
    main()
