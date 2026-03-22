#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CAD 地形图绘制工具
支持：DXF 文件创建、等高线绘制、地形图生成
"""

import ezdxf
from ezdxf import units
from datetime import datetime
import math

def create_dxf_template(filename, title="地形图"):
    """创建 DXF 模板文件"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # 设置单位为米
    doc.header['$INSUNITS'] = 6  # 6 = meters
    
    # 添加图层
    doc.layers.add('CONTOUR', color=3)  # 等高线 - 绿色
    doc.layers.add('TEXT', color=1)     # 文字 - 红色
    doc.layers.add('BOUNDARY', color=6) # 边界 - 紫色
    doc.layers.add('DIMENSION', color=4)# 标注 - 青色
    
    return doc, msp

def add_contour_line(msp, points, elevation, layer='CONTOUR'):
    """添加等高线"""
    if len(points) < 2:
        return
    
    # 创建多段线
    msp.add_lwpolyline(points, dxfattribs={'layer': layer, 'elevation': elevation})
    
    # 添加高程标注
    if points:
        label_pos = points[len(points)//2]
        text = msp.add_text(f"{elevation}m", dxfattribs={'layer': 'TEXT', 'height': 0.5})
        text.set_placement(label_pos)

def add_boundary(msp, corners, layer='BOUNDARY'):
    """添加边界框"""
    if len(corners) == 4:
        corners.append(corners[0])  # 闭合
        msp.add_lwpolyline(corners, dxfattribs={'layer': layer, 'linetype': 'DASHED'})

def add_grid(msp, min_x, max_x, min_y, max_y, interval=10, layer='DIMENSION'):
    """添加坐标网格"""
    # 纵向线
    x = min_x
    while x <= max_x:
        msp.add_line((x, min_y), (x, max_y), dxfattribs={'layer': layer, 'lineweight': 18})
        x += interval
    
    # 横向线
    y = min_y
    while y <= max_y:
        msp.add_line((min_x, y), (max_x, y), dxfattribs={'layer': layer, 'lineweight': 18})
        y += interval

def add_title_block(msp, title, scale, date=None):
    """添加标题栏"""
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # 标题栏框
    msp.add_lwpolyline([(0, 0), (100, 0), (100, 20), (0, 20), (0, 0)], 
                       dxfattribs={'layer': 'BOUNDARY'})
    
    # 标题文字
    text = msp.add_text(title, dxfattribs={'layer': 'TEXT', 'height': 2.5})
    text.set_placement((50, 15))
    text = msp.add_text(f"比例：{scale}", dxfattribs={'layer': 'TEXT', 'height': 1.5})
    text.set_placement((10, 10))
    text = msp.add_text(f"日期：{date}", dxfattribs={'layer': 'TEXT', 'height': 1.5})
    text.set_placement((10, 5))

def create_terrain_map(output_file, contour_data, bounds, title="地形图", scale="1:500"):
    """
    创建地形图
    
    参数:
        output_file: 输出 DXF 文件路径
        contour_data: 等高线数据 [{elevation: 高程，points: [(x1,y1), (x2,y2), ...]}]
        bounds: 边界 [(min_x, min_y), (max_x, max_y)]
        title: 图名
        scale: 比例尺
    """
    doc, msp = create_dxf_template(output_file, title)
    
    # 添加边界
    min_x, min_y = bounds[0]
    max_x, max_y = bounds[1]
    add_boundary(msp, [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])
    
    # 添加网格
    add_grid(msp, min_x, max_x, min_y, max_y, interval=10)
    
    # 添加等高线
    for contour in contour_data:
        elevation = contour.get('elevation', 0)
        points = contour.get('points', [])
        if points:
            add_contour_line(msp, points, elevation)
    
    # 添加标题栏
    add_title_block(msp, title, scale)
    
    # 保存文件
    doc.saveas(output_file)
    print(f"✅ DXF 文件已创建：{output_file}")
    print(f"   等高线数量：{len(contour_data)}")
    print(f"   范围：({min_x}, {min_y}) - ({max_x}, {max_y})")
    
    return output_file

def generate_sample_contour_data():
    """生成示例等高线数据（圆形山丘）"""
    contours = []
    center = (50, 50)
    
    for elevation in range(100, 150, 5):
        radius = 50 - (elevation - 100) * 0.8
        points = []
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            x = center[0] + radius * math.cos(rad)
            y = center[1] + radius * math.sin(rad)
            points.append((x, y))
        contours.append({'elevation': elevation, 'points': points})
    
    return contours

def main():
    import sys
    
    print("📐 CAD 地形图绘制工具\n")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python cad_terrain.py sample    - 生成示例地形图")
        print("  python cad_terrain.py create <输出文件> - 创建空白模板")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'sample':
        # 生成示例地形图
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'terrain_sample.dxf'
        contour_data = generate_sample_contour_data()
        bounds = [(0, 0), (100, 100)]
        create_terrain_map(output_file, contour_data, bounds, "示例地形图", "1:500")
    
    elif command == 'create':
        # 创建空白模板
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'template.dxf'
        doc, msp = create_dxf_template(output_file)
        doc.saveas(output_file)
        print(f"✅ 模板文件已创建：{output_file}")
    
    else:
        print(f"❌ 未知命令：{command}")

if __name__ == '__main__':
    main()
