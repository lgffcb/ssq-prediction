# 🎱 双色球预测软件 - 快速参考卡

## 📋 常用命令

### 预测号码
```bash
cd /home/admin/openclaw/workspace/lottery-predictor

# 命令行预测
python3 predictor.py

# GUI 界面
python3 gui.py
```

### 数据更新
```bash
# 自动更新（推荐）
python3 auto_update.py

# 强制更新
python3 auto_update.py --force

# 静默模式
python3 auto_update.py -q

# 只检查
python3 auto_update.py --check-only
```

### 查看日志
```bash
# 实时更新日志
tail -f logs/auto_update.log

# 查看最近 10 条
tail -n 10 logs/auto_update.log
```

---

## ⏰ 定时任务

### 查看配置
```bash
# 查看 crontab
crontab -l

# 查看 systemd 定时器
systemctl list-timers | grep lottery
```

### 管理任务
```bash
# 编辑 crontab
crontab -e

# 重启 systemd 定时器
sudo systemctl restart lottery-update.timer

# 查看日志
sudo journalctl -u lottery-update.service -f
```

---

## 📡 API 数据源

| 代码 | 数据源 | 说明 |
|------|--------|------|
| `mock` | 模拟数据 | 测试用 |
| `zhcw` | 福彩网 | 官方数据（推荐） |
| `apihubs` | APIHubs | 历史数据 |
| `juhe` | 聚合数据 | 需要 API 密钥 |
| `500wan` | 500 彩票网 | 备选方案 |

### 使用示例
```bash
# 使用福彩网
python3 auto_update.py -s zhcw

# 使用 APIHubs
python3 auto_update.py -s apihubs --force
```

---

## 🔧 故障排查

### 问题 1：权限错误
```bash
chmod +x run.sh setup_cron.sh
chmod +x *.py
```

### 问题 2：依赖缺失
```bash
pip install pandas numpy scikit-learn scipy matplotlib seaborn
```

### 问题 3：数据文件不存在
```bash
mkdir -p data
python3 auto_update.py --force
```

### 问题 4：Cron 不执行
```bash
# 检查 cron 服务
sudo systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog
```

---

## 📊 文件结构

```
lottery-predictor/
├── predictor.py          # 预测核心
├── gui.py                # 图形界面
├── auto_update.py        # 自动更新
├── data_fetcher.py       # 数据获取
├── data/                 # 数据目录
│   └── historical_data.csv
├── logs/                 # 日志目录
│   └── auto_update.log
└── docs/                 # 文档
    ├── README.md
    ├── AUTO_UPDATE_GUIDE.md
    └── REAL_API_GUIDE.md
```

---

## 🎯 权重配置

| 预设 | 频率 | 冷热 | 遗漏 | 伯努利 | 正态 | LSTM |
|------|------|------|------|--------|------|------|
| 均衡 | 20% | 15% | 15% | 15% | 15% | 20% |
| 偏重频率 | 35% | 20% | 10% | 15% | 10% | 10% |
| 偏重遗漏 | 15% | 10% | 35% | 15% | 15% | 10% |
| 偏重 LSTM | 15% | 10% | 10% | 15% | 10% | 40% |

---

## 📞 快速帮助

```bash
# 查看帮助
python3 auto_update.py --help

# 查看版本
cat PROJECT_SUMMARY.md | head -20

# 重新配置定时任务
./setup_cron.sh
```

---

## 🔗 相关文档

- `README.md` - 基础使用
- `AUTO_UPDATE_GUIDE.md` - 自动更新详解
- `REAL_API_GUIDE.md` - 真实 API 接入
- `PROJECT_SUMMARY.md` - 项目总结

---

**打印此卡片作为快速参考！**
