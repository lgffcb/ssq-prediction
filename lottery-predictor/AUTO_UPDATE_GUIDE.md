# 🔄 双色球数据自动更新指南

## 📋 功能概述

支持三种自动更新方式：

1. **命令行自动更新** - 手动运行自动更新脚本
2. **Cron 定时任务** - Linux/Mac 定时更新
3. **Systemd Timer** - Linux 系统服务定时更新
4. **Windows 任务计划** - Windows 定时更新

---

## 🚀 使用方法

### 方式一：命令行自动更新

```bash
cd /home/admin/openclaw/workspace/lottery-predictor

# 基本用法（每天检查一次）
python3 auto_update.py

# 指定数据文件
python3 auto_update.py -f data/historical_data.csv

# 强制更新（忽略间隔）
python3 auto_update.py --force

# 静默模式（只输出错误）
python3 auto_update.py -q

# 只检查，不更新
python3 auto_update.py --check-only

# 每周检查一次
python3 auto_update.py -i weekly

# 总是更新
python3 auto_update.py -i always
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-f, --file` | 数据文件路径 | `data/historical_data.csv` |
| `-s, --source` | 数据源 (mock/kaijiang/500wan) | `mock` |
| `-i, --interval` | 更新间隔 (always/daily/weekly) | `daily` |
| `-q, --quiet` | 静默模式 | `False` |
| `--check-only` | 只检查不更新 | `False` |
| `--force` | 强制更新 | `False` |

---

### 方式二：Cron 定时任务（Linux/Mac）

#### 1. 创建日志目录

```bash
mkdir -p /home/admin/openclaw/workspace/lottery-predictor/logs
```

#### 2. 编辑 crontab

```bash
crontab -e
```

#### 3. 添加配置

选择以下一行添加到 crontab：

```bash
# 每天早上 9 点检查更新
0 9 * * * cd /home/admin/openclaw/workspace/lottery-predictor && /usr/bin/python3 auto_update.py -f data/historical_data.csv -s mock -i daily >> logs/auto_update.log 2>&1

# 开奖日晚上 9 点检查（周二、四、日）
0 21 * * 2,4,0 cd /home/admin/openclaw/workspace/lottery-predictor && /usr/bin/python3 auto_update.py -f data/historical_data.csv -s mock -i always >> logs/auto_update.log 2>&1

# 静默模式（只在有更新时输出）
0 9 * * * cd /home/admin/openclaw/workspace/lottery-predictor && /usr/bin/python3 auto_update.py -f data/historical_data.csv -s mock -i daily -q >> logs/auto_update.log 2>&1
```

#### 4. 验证配置

```bash
# 查看 crontab
crontab -l

# 查看日志
tail -f logs/auto_update.log
```

---

### 方式三：Systemd Timer（Linux）

#### 1. 复制服务文件

```bash
cd /home/admin/openclaw/workspace/lottery-predictor

# 复制到 systemd 目录（需要 sudo）
sudo cp lottery-update.service /etc/systemd/system/
sudo cp lottery-update.timer /etc/systemd/system/
```

#### 2. 启用服务

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启用定时器
sudo systemctl enable lottery-update.timer

# 启动定时器
sudo systemctl start lottery-update.timer

# 查看状态
sudo systemctl status lottery-update.timer
sudo systemctl list-timers
```

#### 3. 查看日志

```bash
# 查看服务日志
journalctl -u lottery-update.service

# 实时查看
journalctl -u lottery-update.service -f
```

---

### 方式四：Windows 任务计划程序

#### 1. 打开任务计划程序

```
Win + R → taskschd.msc → 确定
```

#### 2. 创建基本任务

1. 点击"创建基本任务"
2. 名称：双色球数据更新
3. 触发器：每天 9:00
4. 操作：启动程序
5. 程序/脚本：`python.exe`
6. 添加参数：`auto_update.py -f data\historical_data.csv -s mock -i daily`
7. 起始于：`C:\path\to\lottery-predictor`

#### 3. 使用批处理文件

或者使用提供的 `auto_update.bat`：

```batch
@echo off
cd /d "%~dp0"
python auto_update.py -f data\historical_data.csv -s mock -i daily
pause
```

---

## 📊 增量更新逻辑

自动更新会智能判断是否需要更新：

### 检查流程

```
1. 检查数据文件是否存在
   ↓
2. 读取最后一期信息（期号/日期）
   ↓
3. 获取最新数据
   ↓
4. 比较期号/日期
   ↓
5. 如果有新数据 → 增量下载并合并
   如果无新数据 → 跳过更新
```

### 增量更新优势

- ✅ 只下载新数据，节省流量
- ✅ 保留历史数据，不重复
- ✅ 自动去重，保证数据准确
- ✅ 按期号/日期排序

---

## 🔧 更新间隔说明

| 间隔 | 说明 | 适用场景 |
|------|------|----------|
| `always` | 总是更新 | 开奖后立即检查 |
| `daily` | 每天检查一次 | 日常使用（推荐） |
| `weekly` | 每周检查一次 | 低频使用 |

---

## 📝 日志示例

### 有新数据时

```
============================================================
🔄 双色球数据自动更新
============================================================
⏰ 时间：2026-03-23 09:00:00
📂 文件：data/historical_data.csv
📡 数据源：mock
⏳ 间隔：daily

ℹ️  数据已 1 天未更新

📡 正在更新数据...
📊 数据更新完成：100 → 101 期 (新增 1 期)

============================================================
✅ 当前数据：101 期
📊 最新期号：2026015
📅 开奖日期：2026-03-22
🔴 红球：5 12 18 23 27 31
🔵 蓝球：9
============================================================
```

### 无新数据时

```
============================================================
🔄 双色球数据自动更新
============================================================
⏰ 时间：2026-03-23 09:00:00
📂 文件：data/historical_data.csv
📡 数据源：mock
⏳ 间隔：daily

✅ 数据较新（5 小时前更新过）

============================================================
✅ 当前数据：100 期
============================================================
```

---

## ⚙️ 高级配置

### 自定义数据源

修改 `data_fetcher.py` 中的 `fetch_from_official()` 方法，接入真实 API：

```python
def fetch_from_official(self, page: int = 1, page_size: int = 30):
    # 替换为真实 API
    url = "https://api.example.com/lottery/ssq"
    params = {'page': page, 'page_size': page_size}
    
    response = self.session.get(url, params=params, timeout=10)
    data = response.json()
    
    # 解析数据...
    return df
```

### 邮件通知

在 `auto_update.py` 中添加邮件通知：

```python
def send_notification(new_count: int):
    import smtplib
    from email.message import EmailMessage
    
    msg = EmailMessage()
    msg['Subject'] = f'双色球更新通知 - 新增 {new_count} 期'
    msg['From'] = 'lottery@example.com'
    msg['To'] = 'user@example.com'
    msg.set_content(f'双色球数据已更新，新增 {new_count} 期')
    
    # 发送邮件...
```

---

## 🐛 故障排查

### 问题 1：权限错误

```bash
# 确保有执行权限
chmod +x auto_update.py
chmod +x run.sh

# 或使用 python 直接运行
python3 auto_update.py
```

### 问题 2：文件不存在

```bash
# 创建数据目录
mkdir -p data

# 首次下载数据
python3 auto_update.py --force
```

### 问题 3：Cron 不执行

```bash
# 检查 cron 服务
sudo systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog

# 确保路径正确（使用绝对路径）
```

### 问题 4：Systemd 不执行

```bash
# 查看服务状态
sudo systemctl status lottery-update.timer

# 查看日志
journalctl -u lottery-update.service

# 重新加载配置
sudo systemctl daemon-reload
sudo systemctl restart lottery-update.timer
```

---

## 📞 技术支持

如有问题，请检查：

1. ✅ Python 环境是否正常
2. ✅ 依赖包是否安装
3. ✅ 文件路径是否正确
4. ✅ 网络连接是否正常
5. ✅ 日志文件中的错误信息

---

**最后更新:** 2026-03-23  
**版本:** v1.0
