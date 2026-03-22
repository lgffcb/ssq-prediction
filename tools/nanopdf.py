#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易 PDF 处理工具 - NanoPDF 风格
支持：创建、读取、合并、转换 PDF
"""

import sys
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_pdf(output, text="Hello PDF"):
    """创建简单 PDF"""
    c = canvas.Canvas(output, pagesize=A4)
    c.drawString(100, 750, text)
    c.save()
    print(f"✅ PDF 已创建：{output}")

def read_pdf(path):
    """读取 PDF 内容"""
    try:
        reader = PdfReader(path)
        print(f"📄 文件：{path}")
        print(f"📊 页数：{len(reader.pages)}")
        
        for i, page in enumerate(reader.pages[:3], start=1):
            text = page.extract_text()
            print(f"\n--- 第{i}页 ---")
            print(text[:500] if text else "无法提取文字")
    except Exception as e:
        print(f"❌ 错误：{e}")

def merge_pdfs(paths, output):
    """合并多个 PDF"""
    merger = PdfMerger()
    for path in paths:
        merger.append(path)
    merger.write(output)
    merger.close()
    print(f"✅ 已合并 {len(paths)} 个 PDF -> {output}")

def split_pdf(path, output_dir):
    """拆分 PDF"""
    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(path)
    
    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        output = f"{output_dir}/page_{i}.pdf"
        with open(output, 'wb') as f:
            writer.write(f)
    
    print(f"✅ 已拆分 {len(reader.pages)} 页 -> {output_dir}/")

def main():
    if len(sys.argv) < 2:
        print("NanoPDF - 简易 PDF 工具")
        print("\n用法:")
        print("  python nanopdf.py create <输出文件> [文字]")
        print("  python nanopdf.py read <PDF 文件>")
        print("  python nanopdf.py merge <输出> <PDF1> <PDF2> ...")
        print("  python nanopdf.py split <PDF 文件> <输出目录>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create':
        output = sys.argv[2] if len(sys.argv) > 2 else 'output.pdf'
        text = sys.argv[3] if len(sys.argv) > 3 else 'Hello PDF'
        create_pdf(output, text)
    
    elif command == 'read':
        path = sys.argv[2] if len(sys.argv) > 2 else None
        if path:
            read_pdf(path)
        else:
            print("❌ 请提供 PDF 文件路径")
    
    elif command == 'merge':
        if len(sys.argv) < 4:
            print("❌ 至少需要 2 个 PDF 文件")
            sys.exit(1)
        output = sys.argv[2]
        paths = sys.argv[3:]
        merge_pdfs(paths, output)
    
    elif command == 'split':
        if len(sys.argv) < 4:
            print("❌ 请提供 PDF 文件和输出目录")
            sys.exit(1)
        path = sys.argv[2]
        output_dir = sys.argv[3]
        split_pdf(path, output_dir)
    
    else:
        print(f"❌ 未知命令：{command}")

if __name__ == '__main__':
    main()
