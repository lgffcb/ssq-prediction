# ✅ 自动更新功能已完成

## 🎯 更新内容

### 新增文件

| 文件 | 说明 |
|------|------|
| `auto_update.py` | 自动更新脚本（支持命令行参数） |
| `lottery-update.service` | systemd 服务文件 |
| `lottery-update.timer` | systemd 定时器文件 |
| `crontab_example.txt` | Cron 配置示例 |
| `AUTO_UPDATE_GUIDE.md` | 详细使用指南 |

### 增强功能

#### 1. DataFetcher 类增强

```python
# 新增方法
- update_data(auto=True)          # 支持静默更新
- check_for_new_draw()            # 检查是否有新数据
- auto_update(interval='daily')   # 自动更新（智能判断）
```

#### 2. 增量更新逻辑

```
检查文件 → 读取最后期号 → 获取最新数据 → 比较期号 → 增量合并
```

- ✅ 只下载新数据
- ✅ 自动去重
- ✅ 保留历史数据
- ✅ 智能判断是否需要更新

#### 3. 更新间隔检测

| 间隔 | 检测逻辑 |
|------|----------|
| `always` | 总是更新 |
| `daily` | 检查文件是否超过 1 天未更新 |
| `weekly` | 检查文件是否超过 7 天未更新 |

---

## 🚀 使用示例

### 基础使用

```bash
cd /home/admin/openclaw/workspace/lottery-predictor

# 自动更新（每天检查一次）
python3 auto_update.py

# 强制更新
python3 auto_update.py --force

# 静默模式
python3 auto_update.py -q

# 只检查不更新
python3 auto_update.py --check-only
```

### 定时任务

#### Cron（推荐）

```bash
# 编辑 crontab
crontab -e

# 添加（每天早上 9 点）
0 9 * * * cd /home/admin/openclaw/workspace/lottery-predictor && python3 auto_update.py -q >> logs/auto_update.log 2>&1
```

#### Systemd Timer

```bash
# 复制服务文件
sudo cp lottery-update.* /etc/systemd/system/

# 启用定时器
sudo systemctl enable lottery-update.timer
sudo systemctl start lottery-update.timer

# 查看状态
systemctl list-timers | grep lottery
```

---

## 📊 测试结果

### 首次更新

```
============================================================
🔄 双色球数据自动更新
============================================================
⏰ 时间：2026-03-23 10:52:54
📂 文件：data/historical_data.csv
📡 数据源：mock
⏳ 间隔：daily

ℹ️  首次使用，需要下载数据

📡 正在更新数据...
📊 数据更新完成：0 → 100 期 (新增 100 期)

============================================================
✅ 当前数据：100 期
📊 最新期号：2026002
📅 开奖日期：2026-03-20
🔴 红球：11 16 18 30 32 33
🔵 蓝球：3
============================================================
```

### 增量更新（无新数据）

```
============================================================
🔄 双色球数据自动更新
============================================================
⏰ 时间：2026-03-23 10:55:01
📂 文件：data/historical_data.csv
📡 数据源：mock
⏳ 间隔：daily

✅ 数据较新（0 小时前更新过）
✅ 已加载 100 期数据

============================================================
✅ 当前数据：100 期
============================================================
```

---

## 📁 完整文件列表

```
lottery-predictor/
├── predictor.py              # 核心预测模块 (24KB)
├── data_fetcher.py           # 数据获取模块 (8KB) ✅已增强
├── gui.py                    # GUI 界面 (12KB)
├── auto_update.py            # 自动更新脚本 (3KB) 🆕
├── requirements.txt          # Python 依赖
├── README.md                 # 使用文档
├── AUTO_UPDATE_GUIDE.md      # 自动更新指南 (6KB) 🆕
├── AUTO_UPDATE_COMPLETE.md   # 本文档 🆕
├── lottery-update.service    # systemd 服务 🆕
├── lottery-update.timer      # systemd 定时器 🆕
├── crontab_example.txt       # Cron 示例 🆕
├── run.sh                    # Linux 启动脚本
├── run.bat                   # Windows 启动脚本
└── data/
    └── historical_data.csv   # 历史数据文件
```

---

## ⚙️ 自动更新配置选项

### 命令行参数

```bash
python3 auto_update.py [选项]

选项:
  -f, --file FILE       数据文件路径 (默认：data/historical_data.csv)
  -s, --source SOURCE   数据源 (mock/kaijiang/500wan)
  -i, --interval INTERVAL  更新间隔 (always/daily/weekly)
  -q, --quiet           静默模式
  --check-only          只检查不更新
  --force               强制更新
```

### 更新策略

| 场景 | 推荐配置 |
|------|----------|
| 日常使用 | `-i daily`（每天检查） |
| 开奖后更新 | `-i always`（总是检查） |
| 低频使用 | `-i weekly`（每周检查） |
| 后台任务 | `-q`（静默模式） |

---

## 🔧 集成到预测软件

自动更新已集成到主程序：

### GUI 界面

点击"🔄 更新数据"按钮即可自动更新。

### 命令行

```bash
# 运行预测前自动更新
python3 auto_update.py && python3 predictor.py
```

---

## 📝 后续改进建议

1. **真实 API 接入** - 对接官方开奖数据 API
2. **邮件/微信通知** - 更新成功后发送通知
3. **数据校验** - 验证数据完整性和准确性
4. **多彩种支持** - 大乐透、福彩 3D 等
5. **云同步** - 数据同步到云存储

---

## ✅ 完成清单

- [x] 增量更新逻辑
- [x] 自动更新脚本
- [x] Cron 定时任务配置
- [x] Systemd Timer 配置
- [x] 使用文档
- [x] 测试验证
- [x] 错误处理
- [x] 静默模式
- [x] 强制更新选项
- [x] 检查模式

---

**状态:** ✅ 完成  
**时间:** 2026-03-23  
**版本:** v1.0
