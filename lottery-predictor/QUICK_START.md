# 🎱 双色球预测 - 快速参考卡

## 🚀 一键 Release

```bash
cd /home/admin/openclaw/workspace/lottery-predictor

# 方式 1: 一键脚本
./release.sh v1.0.0

# 方式 2: 手动
git tag v1.0.0
git push origin v1.0.0
```

**然后:**
- 查看构建：https://github.com/lgffcb/excel-extractor/actions
- 下载 Release: https://github.com/lgffcb/excel-extractor/releases

---

## 📦 本地打包

```bash
# Windows
build_exe.bat

# Linux/Mac
./build_exe.sh
```

**输出:**
```
dist/SSQ_Predictor.exe
dist/SSQ_CLI.exe
dist/SSQ_Update.exe
dist/SSQ_Fetch.exe
```

---

## 🎯 用户使用

### GUI 版
```
双击 SSQ_Predictor.exe → 点击"开始预测"
```

### 命令行版
```bash
SSQ_CLI.exe
```

### 更新数据
```bash
SSQ_Update.exe
```

---

## 📊 数据概况

- **数据源:** 17500 彩票网
- **总期数:** 3428 期
- **时间跨度:** 2003-2026 (23 年)
- **文件大小:** 126KB

---

## 🔮 预测方法

- ✅ 伯努利分布
- ✅ 正态分布
- ✅ 指数分布
- ✅ 二项分布
- ✅ 泊松分布
- ✅ LSTM 深度学习

---

## 📁 重要文件

| 文件 | 用途 |
|------|------|
| `predictor.py` | 预测核心 |
| `gui.py` | GUI 界面 |
| `auto_update.py` | 自动更新 |
| `fetch_history_17500.py` | 数据获取 |
| `data/historical_data.csv` | 历史数据 |

---

## 🔧 常用命令

```bash
# 获取数据
python3 fetch_history_17500.py

# 预测号码
python3 predictor.py

# GUI 界面
python3 gui.py

# 自动更新
python3 auto_update.py

# 查看日志
tail -f logs/auto_update.log

# 查看定时任务
crontab -l
```

---

## 📞 相关链接

- **GitHub:** https://github.com/lgffcb/excel-extractor
- **Actions:** https://github.com/lgffcb/excel-extractor/actions
- **Releases:** https://github.com/lgffcb/excel-extractor/releases

---

## ⚠️ 免责声明

本软件仅供娱乐和统计研究，不保证中奖！
请理性购彩，量力而行！

---

**版本:** v1.0.0  
**更新:** 2026-03-23
