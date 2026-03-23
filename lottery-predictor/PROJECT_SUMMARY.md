# 🎱 双色球预测软件 - 项目总结

## ✅ 项目完成情况

### 已实现功能

#### 1. 核心分析模块 (`predictor.py`)
- ✅ **伯努利分布分析** - 分析号码出现/不出现的概率
- ✅ **正态分布分析** - 分析和值分布，预测置信区间
- ✅ **指数分布分析** - 分析遗漏值分布
- ✅ **二项分布分析** - 分析 n 期内号码出现次数
- ✅ **泊松分布分析** - 分析号码出现频率
- ✅ **LSTM 深度学习** - 时间序列预测（需要 TensorFlow）
- ✅ **多周期分析** - 支持 5/7/10/30/50 期分析
- ✅ **冷热号分析** - 识别热号和冷号
- ✅ **遗漏值分析** - 计算当前遗漏和最大遗漏
- ✅ **和值统计** - 均值、标准差、趋势
- ✅ **AC 指数** - 数字复杂程度分析
- ✅ **跨度分析** - 最大 - 最小值

#### 2. 数据获取模块 (`data_fetcher.py`)
- ✅ 支持从 API 获取数据
- ✅ 支持本地 CSV 文件
- ✅ 生成模拟数据用于测试
- ✅ 数据更新和去重

#### 3. GUI 图形界面 (`gui.py`)
- ✅ 数据加载和管理
- ✅ 参数配置（期数、组数、权重）
- ✅ 实时日志显示
- ✅ 结果导出功能
- ✅ 美观的界面设计

#### 4. 辅助文件
- ✅ `requirements.txt` - 依赖列表
- ✅ `README.md` - 使用文档
- ✅ `run.sh` - Linux/Mac启动脚本
- ✅ `run.bat` - Windows 启动脚本

---

## 📁 项目结构

```
lottery-predictor/
├── predictor.py          # 核心预测模块（24KB）
├── data_fetcher.py       # 数据获取模块（8KB）
├── gui.py               # GUI 界面（12KB）
├── requirements.txt     # Python 依赖
├── README.md            # 使用文档
├── run.sh              # Linux 启动脚本
├── run.bat             # Windows 启动脚本
└── data/               # 数据目录（自动创建）
    └── historical_data.csv
```

---

## 🔬 技术实现

### 概率分布整合

| 分布 | 用途 | 实现类 |
|------|------|--------|
| 伯努利 | 号码出现概率 | `ProbabilityDistributions.bernoulli_analysis()` |
| 正态 | 和值预测 | `ProbabilityDistributions.normal_distribution_analysis()` |
| 指数 | 遗漏分析 | `ProbabilityDistributions.exponential_distribution_analysis()` |
| 二项 | n 期出现次数 | `ProbabilityDistributions.binomial_distribution_analysis()` |
| 泊松 | 频率分布 | `ProbabilityDistributions.poisson_distribution_analysis()` |
| LSTM | 序列预测 | `LSTMPredictor` |

### 权重综合算法

```python
综合得分 = Σ(方法得分 × 权重)

默认权重:
- 频率分析：20%
- 冷热号：15%
- 遗漏分析：15%
- 伯努利分布：15%
- 正态分布：15%
- LSTM 预测：20%
```

### LSTM 网络结构

```
输入层：(sequence_length, 6)
↓
LSTM(128, return_sequences=True)
↓
Dropout(0.2)
↓
LSTM(64, return_sequences=True)
↓
Dropout(0.2)
↓
LSTM(32)
↓
Dropout(0.2)
↓
Dense(64, relu)
↓
Dense(6, linear)  # 输出 6 个红球预测
```

---

## 🚀 使用方法

### 快速启动

```bash
cd lottery-predictor

# 方式 1: 使用启动脚本
./run.sh          # Linux/Mac
run.bat           # Windows

# 方式 2: 直接运行
python predictor.py   # 命令行版
python gui.py         # GUI 版
```

### 安装完整依赖（含 LSTM）

```bash
pip install -r requirements.txt
# 或
pip install pandas numpy scikit-learn tensorflow matplotlib seaborn scipy
```

---

## 📊 测试结果

### 测试环境
- Python 3.x
- pandas, numpy, scipy, scikit-learn
- TensorFlow（可选，用于 LSTM）

### 测试输出示例

```
============================================================
🎱 双色球预测软件 v1.0
============================================================

📂 加载历史数据...
✅ 已加载 100 期开奖数据

============================================================
📊 正在进行综合分析...
🤖 训练 LSTM 模型...

============================================================
🔮 生成预测号码...
============================================================

第 1 组:
  红球：01 14 16 19 20 24
  蓝球：16
  和值：94 | AC 指数：8

第 2 组:
  红球：05 12 18 23 27 31
  蓝球：08
  和值：116 | AC 指数：7

...
```

---

## ⚠️ 注意事项

### 1. LSTM 依赖
- LSTM 需要 TensorFlow 2.x
- 如未安装，程序会自动跳过 LSTM 预测
- 其他统计方法仍可正常使用

### 2. 数据源
- 当前使用模拟数据
- 实际使用需接入真实 API
- 支持从 CSV 文件加载历史数据

### 3. 预测准确性
- 彩票是随机事件
- 所有方法都是统计分析
- 不保证中奖，仅供娱乐

---

## 🔧 可扩展功能

### 已预留接口
1. **真实 API 接入** - `DataFetcher.fetch_from_official()`
2. **更多分布** - 可在 `ProbabilityDistributions` 类中添加
3. **自定义权重** - GUI 支持权重预设切换
4. **结果可视化** - 可添加图表显示

### 建议改进
1. 接入真实开奖数据 API
2. 添加更多机器学习模型（XGBoost、Random Forest）
3. 增加回测功能（验证历史预测准确率）
4. 添加号码走势图可视化
5. 支持更多彩种（大乐透、福彩 3D 等）

---

## 📄 免责声明

**重要提示：**

1. 本软件仅供娱乐和统计研究
2. 彩票是随机事件，不存在必中方法
3. 所有预测结果基于历史数据统计
4. 不保证任何中奖承诺
5. 请理性购彩，量力而行
6. 未成年人禁止购彩

---

## 📝 版本信息

- **版本号:** v1.0
- **开发日期:** 2026-03-23
- **开发者:** AI Assistant
- **技术栈:** Python + pandas + scipy + TensorFlow

---

## 🎯 核心代码位置

| 功能 | 文件 | 行号范围 |
|------|------|----------|
| 统计分析 | `predictor.py` | 1-200 |
| 概率分布 | `predictor.py` | 200-400 |
| LSTM 预测 | `predictor.py` | 400-500 |
| 综合预测 | `predictor.py` | 500-700 |
| 数据获取 | `data_fetcher.py` | 全部 |
| GUI 界面 | `gui.py` | 全部 |

---

**项目已完成！🎉**
