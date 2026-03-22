# 📐 CAD 地形图绘制技能卡

## 📋 技能信息

| 项目 | 内容 |
|------|------|
| **技能名称** | CAD 地形图绘制 |
| **学习时间** | 2026-03-22 |
| **应用场景** | 施工现场地形图、等高线图、场地平整图 |
| **工具** | ezdxf, cadquery |
| **熟练度** | ⭐⭐⭐ 入门 |

---

## 🛠️ 安装依赖

```bash
pip install ezdxf cadquery
```

**已安装版本：**
- ezdxf: 1.4.3
- cadquery: 2.7.0
- vtk: 9.3.1

---

## 🎯 标准操作流程

### 方式一：生成示例地形图

```bash
python3 tools/cad_terrain.py sample output/terrain.dxf
```

### 方式二：创建空白模板

```bash
python3 tools/cad_terrain.py create output/template.dxf
```

### 方式三：Python 代码调用

```python
from tools.cad_terrain import create_terrain_map

# 准备数据
contour_data = [
    {'elevation': 100, 'points': [(0,0), (10,0), (10,10), (0,10)]},
    {'elevation': 105, 'points': [(2,2), (8,2), (8,8), (2,8)]},
]
bounds = [(0, 0), (100, 100)]

# 创建地形图
create_terrain_map('output/terrain.dxf', contour_data, bounds, "施工地形图", "1:500")
```

---

## 📊 DXF 文件结构

### 图层设置

| 图层名 | 颜色 | 用途 |
|--------|------|------|
| CONTOUR | 绿色 (3) | 等高线 |
| TEXT | 红色 (1) | 文字标注 |
| BOUNDARY | 紫色 (6) | 边界框 |
| DIMENSION | 青色 (4) | 标注网格 |

### 单位设置

- **绘图单位**：米 (meters)
- **$INSUNITS**：6

---

## 🔧 核心功能

### 1️⃣ 等高线绘制

```python
def add_contour_line(msp, points, elevation, layer='CONTOUR'):
    """
    msp: 模型空间
    points: 等高线点坐标 [(x1,y1), (x2,y2), ...]
    elevation: 高程值
    layer: 图层名
    """
```

### 2️⃣ 边界框

```python
def add_boundary(msp, corners, layer='BOUNDARY'):
    """
    corners: 四个角点 [(min_x,min_y), (max_x,min_y), 
                       (max_x,max_y), (min_x,max_y)]
    """
```

### 3️⃣ 坐标网格

```python
def add_grid(msp, min_x, max_x, min_y, max_y, interval=10):
    """
    interval: 网格间距（米）
    """
```

### 4️⃣ 标题栏

```python
def add_title_block(msp, title, scale, date=None):
    """
    title: 图名
    scale: 比例尺
    date: 日期（默认当天）
    """
```

---

## 📝 输入数据格式

### 等高线数据

```python
contour_data = [
    {
        'elevation': 100,  # 高程（米）
        'points': [        # 等高线坐标点
            (x1, y1),
            (x2, y2),
            ...
        ]
    },
    ...
]
```

### 边界范围

```python
bounds = [
    (min_x, min_y),  # 左下角坐标
    (max_x, max_y)   # 右上角坐标
]
```

---

## 🗺️ 施工地形图应用

### 污水管网工程

**需要的地形信息：**
1. ✅ 原始地面高程
2. ✅ 道路中心线
3. ✅ 建筑物轮廓
4. ✅ 水系分布
5. ✅ 管线走向

**绘图步骤：**
```
1. 收集现场测量数据
2. 整理高程点坐标
3. 生成等高线
4. 添加建筑物和道路
5. 标注管线走向
6. 添加图框和标题栏
```

---

## ⚠️ 注意事项

### 1. 坐标准确性
- 使用统一坐标系
- 高程数据要核实
- 比例尺要匹配

### 2. 图层管理
- 不同要素用不同图层
- 颜色区分要明显
- 便于后续编辑

### 3. 文件兼容性
- 保存为 R2010 格式
- 兼容 AutoCAD 2010+
- 可用 CAD 软件打开

### 4. 数据备份
- 保留原始测量数据
- DXF 文件定期备份
- 版本管理

---

## 💡 常见问题

### Q1: 等高线不闭合？
**A:** 检查首尾点坐标是否一致，或手动闭合

### Q2: 高程标注位置不对？
**A:** 调整 points 数组，确保标注点在等高线上

### Q3: 比例尺如何设置？
**A:** 根据实际范围选择：
- 小区级：1:200 - 1:500
- 村庄级：1:1000 - 1:2000
- 乡镇级：1:5000 - 1:10000

### Q4: 如何导入测量数据？
**A:** 将测量数据整理为 [(x,y,elevation)] 格式，再生成等高线

---

## 🔗 相关文件

| 文件 | 用途 |
|------|------|
| `tools/cad_terrain.py` | CAD 地形图绘制工具 |
| `output/terrain_sample.dxf` | 示例地形图 |
| `memory/skills/cad-terrain.md` | 技能卡片 |

---

## 📚 扩展学习

### AutoCAD 基础
- 图层管理
- 块定义
- 尺寸标注
- 打印输出

### 地形图知识
- 等高线原理
- 高程系统
- 坐标系统
- 比例尺选择

### 施工应用
- 土方计算
- 场地平整
- 管线综合
- 工程量统计

---

> 📌 **学习日期：** 2026-03-22
> 📌 **下次复习：** 2026-03-29
> 📌 **掌握程度：** 可独立绘制简单地形图
