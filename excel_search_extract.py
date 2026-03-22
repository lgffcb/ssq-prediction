#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel 数据提取工具 - GUI 版本 v4
- 支持 .xls 和 .xlsx 格式
- 自动提取包含查找文字的列
- 支持"分包明细表"等任何包含"明细"的 sheet 名
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from openpyxl import load_workbook
import xlrd  # 支持.xls 格式
import os
import threading

class ExcelExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel 数据提取工具 v4")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        self.file_path = tk.StringVar()
        self.search_term = tk.StringVar()
        self.result_file_path = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        
        # 标题
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        ttk.Label(title_frame, text="📊 Excel 数据提取工具 v4", font=("Microsoft YaHei UI", 16, "bold")).pack()
        ttk.Label(title_frame, text="支持.xls 和.xlsx 格式 - 自动提取包含查找文字的列", font=("Microsoft YaHei UI", 9)).pack()
        
        # 1. 文件选择
        file_frame = ttk.LabelFrame(self.root, text="1️⃣ 选择 Excel 文件", padding="10")
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        file_entry_frame = ttk.Frame(file_frame)
        file_entry_frame.pack(fill=tk.X)
        
        self.file_entry = ttk.Entry(file_entry_frame, textvariable=self.file_path, font=("Consolas", 10))
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.file_entry.bind('<Control-v>', self.on_paste)
        
        ttk.Button(file_entry_frame, text="📂 浏览", command=self.browse_file, width=10).pack(side=tk.RIGHT)
        
        # 2. 查找内容
        search_frame = ttk.LabelFrame(self.root, text="2️⃣ 输入查找内容", padding="10")
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        search_entry_frame = ttk.Frame(search_frame)
        search_entry_frame.pack(fill=tk.X)
        
        self.search_entry = ttk.Entry(search_entry_frame, textvariable=self.search_term, font=("Consolas", 11), width=50)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.start_extraction())
        
        ttk.Label(search_frame, text="💡 提示：支持.xls 和.xlsx 格式", foreground="gray").pack(anchor=tk.W, pady=(5, 0))
        
        # 3. 开始按钮
        btn_frame = ttk.Frame(self.root, padding="10")
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        self.start_btn = ttk.Button(btn_frame, text="🚀 开始提取", command=self.start_extraction, width=20)
        self.start_btn.pack()
        
        # 4. 日志区域
        log_frame = ttk.LabelFrame(self.root, text="📋 处理状态", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = tk.Text(log_frame, height=15, font=("Consolas", 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 5. 底部按钮
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.open_folder_btn = ttk.Button(bottom_frame, text="📁 打开结果文件夹", command=self.open_result_folder, state=tk.DISABLED)
        self.open_folder_btn.pack(side=tk.LEFT)
        ttk.Label(bottom_frame, text="Excel 数据提取工具 v4.0", foreground="gray", font=("Microsoft YaHei UI", 8)).pack(side=tk.RIGHT)
    
    def on_paste(self, event):
        """粘贴文件路径"""
        try:
            clipboard = self.root.clipboard_get()
            if os.path.exists(clipboard) and (clipboard.endswith('.xlsx') or clipboard.endswith('.xls')):
                self.file_path.set(clipboard)
                self.log("✅ 已粘贴文件路径")
                return 'break'
        except:
            pass
        return None
    
    def browse_file(self):
        """浏览文件"""
        file_path = filedialog.askopenfilename(
            title="选择 Excel 文件",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_path.set(file_path)
            self.log(f"✅ 已选择：{os.path.basename(file_path)}")
    
    def log(self, message):
        """添加日志"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def start_extraction(self):
        """开始提取"""
        if not self.file_path.get():
            messagebox.showerror("错误", "请选择 Excel 文件！")
            return
        
        if not os.path.exists(self.file_path.get()):
            messagebox.showerror("错误", "文件不存在！")
            return
        
        if not self.search_term.get():
            messagebox.showerror("错误", "请输入查找内容！")
            return
        
        self.start_btn.config(state=tk.DISABLED)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.run_extraction)
        thread.daemon = True
        thread.start()
    
    def run_extraction(self):
        """运行提取"""
        try:
            file_path = self.file_path.get()
            search_term = self.search_term.get()
            
            self.log("="*60)
            self.log("🔧 正在处理 Excel 文件...")
            self.root.update()
            
            # 判断文件类型
            is_xls = file_path.lower().endswith('.xls')
            self.log(f"📁 文件格式：{'.xls (Excel 97-2003)' if is_xls else '.xlsx (Excel 2007+)'}")
            self.root.update()
            
            # 1. 加载 Excel
            if is_xls:
                # .xls 文件用 xlrd 读取
                self.log("📖 使用 xlrd 读取.xls 文件...")
                self.root.update()
                
                wb = xlrd.open_workbook(file_path)
                all_sheet_names = wb.sheet_names()
                
                self.log(f"\n📊 文件包含 {len(all_sheet_names)} 个工作表:")
                for name in all_sheet_names:
                    self.log(f"   - {name}")
                
                # 查找明细表
                target_sheet = None
                target_idx = 0
                for i, sheet_name in enumerate(all_sheet_names):
                    if '明细' in sheet_name:
                        target_sheet = sheet_name
                        target_idx = i
                        break
                
                if not target_sheet:
                    self.log(f"\n⚠️  未找到包含'明细'的工作表，使用第一个工作表")
                    target_sheet = all_sheet_names[0]
                else:
                    self.log(f"\n✅ 找到明细工作表：【{target_sheet}】")
                
                # 读取数据
                sheet = wb.sheet_by_index(target_idx)
                self.log(f"📋 工作表大小：{sheet.nrows} 行 × {sheet.ncols} 列")
                
                # 转换为 DataFrame
                data = []
                for row_idx in range(sheet.nrows):
                    row = [sheet.cell(row_idx, col_idx).value for col_idx in range(sheet.ncols)]
                    data.append(row)
                
                df = pd.DataFrame(data)
                
            else:
                # .xlsx 文件用 openpyxl 读取
                self.log("📖 使用 openpyxl 读取.xlsx 文件...")
                self.root.update()
                
                wb = load_workbook(file_path, data_only=True)
                all_sheet_names = wb.sheet_names
                
                self.log(f"\n📊 文件包含 {len(all_sheet_names)} 个工作表:")
                for name in all_sheet_names:
                    self.log(f"   - {name}")
                
                # 查找明细表
                target_sheet = None
                for sheet_name in all_sheet_names:
                    if '明细' in sheet_name:
                        target_sheet = sheet_name
                        break
                
                if not target_sheet:
                    self.log(f"\n⚠️  未找到包含'明细'的工作表，使用第一个工作表")
                    target_sheet = all_sheet_names[0]
                else:
                    self.log(f"\n✅ 找到明细工作表：【{target_sheet}】")
                
                # 读取数据
                sheet = wb[target_sheet]
                self.log(f"📋 工作表大小：{sheet.max_row} 行 × {sheet.max_column} 列")
                
                # 转换为 DataFrame
                df = pd.read_excel(file_path, sheet_name=target_sheet)
            
            # 2. 找出包含查找内容的列
            self.log(f"\n🔍 正在分析包含'{search_term}'的列...")
            self.root.update()
            
            df_str = df.astype(str)
            columns_to_extract = []
            column_names = []
            
            for col_idx in range(len(df.columns)):
                col_data = df_str.iloc[:, col_idx]
                if col_data.str.contains(str(search_term), na=False, case=False).any():
                    col_letter = self.get_column_letter(col_idx)
                    col_name = str(df.columns[col_idx]) if col_idx < len(df.columns) else f"列{col_idx}"
                    columns_to_extract.append(col_idx)
                    column_names.append(f'{col_letter}列：{col_name}')
                    # 统计该列有多少行包含查找内容
                    match_count = col_data.str.contains(str(search_term), na=False, case=False).sum()
                    self.log(f"   ✅ {col_letter}列 ({str(col_name)[:40]}) - {match_count}行包含'{search_term}'")
            
            if not columns_to_extract:
                self.log(f"❌ 没有找到包含'{search_term}'的列")
                messagebox.showwarning("提示", f"未找到包含'{search_term}'的列")
                self.start_btn.config(state=tk.NORMAL)
                return
            
            self.log(f"\n✅ 共 {len(columns_to_extract)} 列包含查找内容")
            
            # 3. 提取数据 - 提取所有行的整列数据
            result = df.iloc[:, columns_to_extract].copy()
            result.columns = column_names
            
            # 5. 保存
            self.result_file_path = os.path.splitext(file_path)[0] + '_提取结果.xlsx'
            result.to_excel(self.result_file_path, index=False)
            
            self.log(f"\n{'='*60}")
            self.log("✅ 数据提取完成！")
            self.log(f"📁 结果已保存到：{self.result_file_path}")
            self.log(f"📊 提取结果：{len(result)} 行 × {len(result.columns)} 列")
            
            self.open_folder_btn.config(state=tk.NORMAL)
            messagebox.showinfo("成功", f"数据提取完成！\n\n提取 {len(columns_to_extract)} 列的完整数据\n共 {len(result)} 行\n\n结果已保存到:\n{self.result_file_path}")
            
        except Exception as e:
            self.log(f"\n❌ 错误：{str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("错误", f"提取失败:\n{str(e)}")
        
        finally:
            self.start_btn.config(state=tk.NORMAL)
    
    def get_column_letter(self, col_index):
        """列索引转字母"""
        result = ""
        while col_index >= 0:
            result = chr(ord('A') + (col_index % 26)) + result
            col_index = col_index // 26 - 1
        return result
    
    def open_result_folder(self):
        """打开结果文件夹"""
        if self.result_file_path and os.path.exists(self.result_file_path):
            os.startfile(os.path.dirname(self.result_file_path))

def main():
    root = tk.Tk()
    app = ExcelExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
