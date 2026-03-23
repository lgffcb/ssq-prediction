# 🎱 双色球预测软件

基于概率统计和机器学习的双色球预测分析工具

## ✨ 功能特性

- ✅ **3428 期真实历史数据** (2003-2026)
- ✅ **6 种概率分布分析** (伯努利、正态、指数、二项、泊松、LSTM)
- ✅ **GUI 图形界面** - 一键预测
- ✅ **自动更新数据** - 每天从 17500 获取最新数据
- ✅ **命令行工具** - 支持批量预测
- ✅ **Windows EXE** - 无需安装 Python

## 🚀 快速开始

### 方式一：下载 Release（推荐）

1. 访问 [Releases](https://github.com/lgffcb/ssq-prediction/releases)
2. 下载 `SSQ_Predictor_Windows.zip`
3. 解压后双击运行 `SSQ_Predictor.exe`
4. 点击"开始预测"

### 方式二：源码运行

```bash
# 安装依赖
pip install -r requirements.txt

# 获取数据
python fetch_history_17500.py

# 运行预测
python predictor.py

# GUI 界面
python gui.py
```

## 📦 文件说明

| 文件 | 说明 |
|------|------|
| `predictor.py` | 预测核心程序 |
| `gui.py` | GUI 图形界面 |
| `auto_update.py` | 自动更新工具 |
| `data_fetcher.py` | 数据获取模块 |
| `fetch_history_17500.py` | 17500 网站爬虫 |
| `data/historical_data.csv` | 3428 期历史数据 |

## 📊 数据来源

- **数据源:** 17500 彩票网
- **接口:** http://www.17500.cn/getData/ssq.TXT
- **数据量:** 3428 期（2003-2026）
- **更新频率:** 每天自动更新

## 🔮 预测方法

### 概率分布分析
- **伯努利分布** - 号码出现概率
- **正态分布** - 和值分析
- **指数分布** - 遗漏分析
- **二项分布** - n 期出现次数
- **泊松分布** - 频率分布

### 深度学习
- **LSTM** - 时间序列预测

## 🛠️ 打包 EXE

### Windows
```bash
build_exe.bat
```

### Linux/Mac
```bash
./build_exe.sh
```

输出目录：`dist/`

## 📋 使用示例

### 预测号码
```bash
python predictor.py
```

### 更新数据
```bash
python auto_update.py
```

### 获取历史数据
```bash
python fetch_history_17500.py
```

## 📄 文档

- [QUICK_START.md](QUICK_START.md) - 快速参考
- [GitHub Actions](https://github.com/lgffcb/ssq-prediction/actions) - 自动构建
- [Releases](https://github.com/lgffcb/ssq-prediction/releases) - 下载 EXE

## ⚠️ 免责声明

本软件仅供娱乐和统计研究，不保证中奖！
- 彩票是随机事件，不存在必中方法
- 所有预测基于历史数据统计
- 请理性购彩，量力而行
- 未成年人禁止购彩

## 📊 统计信息

| 项目 | 数值 |
|------|------|
| 历史数据 | 3428 期 |
| 时间跨度 | 23 年 (2003-2026) |
| 数据源 | 17500 彩票网 |
| 预测方法 | 6 种 |
| 代码语言 | Python 3.10+ |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**版本:** v1.0.0  
**最后更新:** 2026-03-23  
**GitHub:** https://github.com/lgffcb/ssq-prediction
