# 📡 真实数据获取方案

## ⚠️ 当前网络状况

**测试结果:**
- ❌ 福彩网 API - 404/超时
- ❌ 500 彩票网 - 解析失败
- ❌ APIHubs - 连接超时
- ❌ EasyAPI - DNS 解析失败
- ❌ 天地图 - DNS 解析失败

**原因:** 网络环境限制，无法访问外部彩票 API

---

## ✅ 可用方案

### 方案一：手动导入数据（推荐）

从以下网站手动下载 CSV 数据：

1. **福彩网** - https://www.zhcw.com/kaijianggonggao/ssq/
2. **500 彩票网** - http://kaijiang.500.com/ssq.shtml
3. **中彩网** - https://www.zcw.com/ssq/kaijiang/

**步骤:**
1. 打开网站
2. 复制历史数据（Excel 格式）
3. 保存为 CSV
4. 放到 `data/historical_data.csv`

---

### 方案二：使用提供的模拟数据

当前项目已包含模拟数据生成器，可以用于：
- ✅ 测试预测算法
- ✅ 测试 GUI 界面
- ✅ 测试自动更新功能
- ✅ 演示和开发

**命令:**
```bash
python3 auto_update.py --force
```

---

### 方案三：本地网络环境改善后使用

如果你有更好的网络环境，可以使用以下 API：

#### 1. APIHubs（推荐）
```python
url = "https://api.apihubs.com/lottery/history"
params = {'size': 1000, 'lottery': 'ssq'}
```

#### 2. 聚合数据（需要 API 密钥）
```python
url = "https://apis.juhe.cn/lottery/query"
params = {'lottery_id': 'ssq', 'key': 'YOUR_KEY'}
```

#### 3. 极速数据（需要 API 密钥）
```python
url = "https://api.jisuapi.com/lottery/ssq"
params = {'appkey': 'YOUR_KEY', 'num': '100'}
```

---

## 🔧 修改代码使用真实 API

当你有可用的 API 时，修改 `data_fetcher.py`:

```python
def fetch_from_api(self, source: str = 'mock', ...) -> pd.DataFrame:
    if source == 'apihubs':
        return self._fetch_apihubs()  # 取消注释
    elif source == 'zhcw':
        return self._fetch_zhcw()  # 取消注释
    # ...
```

---

## 📊 当前可用功能

虽然无法获取真实数据，但以下功能完全正常：

| 功能 | 状态 | 说明 |
|------|------|------|
| 预测算法 | ✅ | 使用模拟数据 |
| 概率分析 | ✅ | 伯努利、正态、泊松等 |
| LSTM 预测 | ✅ | 深度学习模型 |
| GUI 界面 | ✅ | 图形界面正常 |
| 自动更新 | ✅ | 逻辑正常 |
| 定时任务 | ✅ | Cron 已配置 |

---

## 💡 建议

### 立即可做
1. **使用模拟数据测试** - 功能完全正常
2. **手动导入数据** - 从官网复制 Excel

### 后续优化
1. **改善网络** - 使用代理或更好的网络环境
2. **申请 API 密钥** - 聚合数据、极速数据
3. **本地部署** - 在服务器上部署爬虫

---

## 📁 数据格式

手动准备数据的格式：

```csv
issue,date,red1,red2,red3,red4,red5,red6,blue
2026001,2026-01-02,5,12,18,23,27,31,9
2026002,2026-01-05,3,11,15,22,28,33,12
...
```

---

**总结:** 由于网络限制，建议使用模拟数据进行开发和测试。有真实数据需求时，可以手动导入或使用可用网络环境的服务器。
