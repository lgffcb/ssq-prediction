# 📊 数据格式说明

## ✅ 本项目使用的数据格式

### CSV 格式（唯一数据格式）

**本项目只使用 CSV 格式的数据文件，不涉及任何 Excel 文件操作。**

#### 数据文件

| 文件 | 格式 | 说明 |
|------|------|------|
| `data/historical_data.csv` | CSV | 历史开奖数据（3428 期） |

#### CSV 数据结构

```csv
issue,date,red1,red2,red3,red4,red5,red6,blue
2026031,2026-03-22,3,10,12,13,18,33,8
2026030,2026-03-19,10,11,14,19,22,24,4
2026029,2026-03-17,6,19,22,23,28,31,5
```

**字段说明：**
- `issue` - 期号（7 位数字）
- `date` - 开奖日期（YYYY-MM-DD）
- `red1-red6` - 红球号码（1-33）
- `blue` - 蓝球号码（1-16）

---

## ❌ 不使用的格式

本项目**不使用**以下格式：

- ❌ Excel 文件（.xlsx, .xls, .xlsm）
- ❌ Excel 相关库（openpyxl, xlrd, xlsxwriter）
- ❌ Excel 导出功能

---

## 🔧 数据处理

### 数据获取

```python
# 从 17500 网站获取 TXT 格式数据
url = "http://www.17500.cn/getData/ssq.TXT"

# 使用 pandas 读取（空格分隔）
df = pd.read_csv(io.StringIO(text), sep=' ', header=None, dtype=str)
```

### 数据保存

```python
# 保存为 CSV 格式
df.to_csv('data/historical_data.csv', index=False, encoding='utf-8-sig')
```

### 数据加载

```python
# 从 CSV 加载
df = pd.read_csv('data/historical_data.csv', encoding='utf-8-sig')
```

---

## 📦 依赖说明

### 核心依赖

```txt
pandas>=2.0.0          # 数据处理（CSV）
numpy>=1.24.0          # 数值计算
scikit-learn>=1.3.0    # 机器学习
tensorflow>=2.13.0     # 深度学习
matplotlib>=3.7.0      # 数据可视化
seaborn>=0.12.0        # 统计图表
scipy>=1.11.0          # 统计分析
requests>=2.31.0       # HTTP 请求
```

### 不需要的依赖

以下依赖**不需要安装**：

```txt
❌ openpyxl    # Excel 读写
❌ xlrd        # Excel 读取
❌ xlsxwriter  # Excel 写入
❌ pyxlsb      # Excel 二进制格式
```

---

## 🎯 项目定位

**双色球预测软件** 是一个纯粹的彩票数据分析工具：

- ✅ 只处理 CSV 格式数据
- ✅ 只使用标准数据科学库
- ✅ 不涉及任何 Excel 操作
- ✅ 专注于概率统计和预测

---

## 📝 常见误解

### 误解 1：需要 Excel 才能使用

**事实：** 不需要！只需要 Python 和 CSV 文件。

### 误解 2：可以导出 Excel 报表

**事实：** 不支持 Excel 导出，只支持 CSV 格式。

### 误解 3：可以读取 Excel 格式的历史数据

**事实：** 只支持 CSV 格式，Excel 数据需要先转换为 CSV。

---

## 🔄 Excel 数据转换

如果你有 Excel 格式的双色球数据，可以：

### 方法 1：使用 Excel 软件

1. 用 Excel 打开文件
2. 另存为 → 选择 "CSV (逗号分隔) (*.csv)"
3. 保存到 `data/historical_data.csv`

### 方法 2：使用 Python 转换

```python
import pandas as pd

# 读取 Excel
df = pd.read_excel('data.xlsx')

# 保存为 CSV
df.to_csv('data/historical_data.csv', index=False, encoding='utf-8-sig')
```

---

## 📊 数据源

**官方数据源：**
- 17500 彩票网
- URL: http://www.17500.cn/getData/ssq.TXT
- 格式：TXT（空格分隔）
- 自动转换为 CSV 存储

---

## ✅ 总结

| 项目 | 说明 |
|------|------|
| 数据格式 | CSV（唯一） |
| Excel 支持 | ❌ 不支持 |
| 依赖库 | 标准数据科学库 |
| 数据源 | 17500 彩票网 |
| 编码 | UTF-8 with BOM |

---

**本说明文档澄清：双色球预测软件不涉及任何 Excel 表格提取功能，只处理 CSV 格式数据。**
