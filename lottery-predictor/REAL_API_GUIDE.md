# 📡 真实 API 接入指南

## 🎯 可用的彩票 API 数据源

### 方式一：官方 API（推荐）

#### 1. 中国福彩网 - 双色球

**API 地址:**
```
https://m.zhcw.com/pchtml/kajianggonggao/ssq/list_1.html
```

**数据格式:** HTML 页面，需要解析

**示例代码:**
```python
def fetch_from_zhcw(self, page=1, page_size=30):
    """从中国福彩网获取数据"""
    import requests
    from bs4 import BeautifulSoup
    
    url = f"https://m.zhcw.com/pchtml/kajianggonggao/ssq/list_{page}.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    records = []
    for item in soup.select('.lottery-item'):
        issue = item.select_one('.issue').text.strip()
        date = item.select_one('.date').text.strip()
        reds = [int(r.text) for r in item.select('.red-ball')]
        blue = int(item.select_one('.blue-ball').text)
        
        records.append({
            'issue': issue,
            'date': date,
            'red1': reds[0], 'red2': reds[1], 'red3': reds[2],
            'red4': reds[3], 'red5': reds[4], 'red6': reds[5],
            'blue': blue
        })
    
    return pd.DataFrame(records)
```

---

### 方式二：第三方 API（免费）

#### 1. 聚合数据 API

**API 地址:**
```
https://apis.juhe.cn/lottery/query
```

**参数:**
- `lottery_id`: ssq (双色球)
- `page`: 页码
- `page_size`: 每页数量
- `key`: API 密钥（需要注册）

**请求示例:**
```python
def fetch_from_juhe(self, page=1, page_size=30):
    """从聚合数据获取"""
    import requests
    
    url = "https://apis.juhe.cn/lottery/query"
    params = {
        "lottery_id": "ssq",
        "page": page,
        "page_size": page_size,
        "key": "YOUR_API_KEY"  # 需要申请
    }
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    if data.get('error_code') == 0:
        records = []
        for item in data.get('result', {}).get('data', []):
            reds = [int(x) for x in item.get('num').split(',')[:-1]]
            blue = int(item.get('num').split(',')[-1])
            
            records.append({
                'issue': item.get('issue'),
                'date': item.get('opentime'),
                'red1': reds[0], 'red2': reds[1], 'red3': reds[2],
                'red4': reds[3], 'red5': reds[4], 'red6': reds[5],
                'blue': blue
            })
        
        return pd.DataFrame(records)
    
    return None
```

**获取 API 密钥:**
- 网站：https://www.juhe.cn/docs/api/id/1
- 免费额度：每天 100 次

---

#### 2. 阿里云 API 市场

**API 地址:**
```
https://aliapi.market.alicloud.com/api/lottery/ssq
```

**价格:** 免费或低价套餐

**示例:**
```python
def fetch_from_aliyun(self, page=1):
    """从阿里云 API 市场获取"""
    import requests
    
    url = "https://aliapi.market.alicloud.com/api/lottery/ssq"
    headers = {
        'Authorization': 'APPCODE YOUR_APP_CODE',
        'Content-Type': 'application/json'
    }
    params = {
        'page': page,
        'size': 30
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    data = response.json()
    
    # 解析数据...
    return df
```

**获取 APPCODE:**
- 网站：https://market.aliyun.com
- 搜索：彩票 API

---

#### 3. 历史数据 API（推荐用于初始化）

**API 地址:**
```
https://api.apihubs.com/lottery/history?size=1000&lottery=ssq
```

**特点:**
- ✅ 免费
- ✅ 无需 API 密钥
- ✅ 返回历史数据
- ❌ 可能不稳定

**示例代码:**
```python
def fetch_from_apihubs(self):
    """从 APIHubs 获取历史数据"""
    import requests
    
    url = "https://api.apihubs.com/lottery/history"
    params = {
        'size': 1000,  # 最多 1000 条
        'lottery': 'ssq'
    }
    
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    records = []
    for item in data.get('data', []):
        reds = [int(item[f'red{i}']) for i in range(1, 7)]
        blue = int(item['blue'])
        
        records.append({
            'issue': item.get('issue'),
            'date': item.get('date'),
            'red1': reds[0], 'red2': reds[1], 'red3': reds[2],
            'red4': reds[3], 'red5': reds[4], 'red6': reds[5],
            'blue': blue
        })
    
    return pd.DataFrame(records)
```

---

### 方式三：网页爬虫（备选）

#### 1. 500 彩票网

**URL:**
```
http://kaijiang.500.com/ssq.shtml
```

**示例代码:**
```python
def fetch_from_500wan(self):
    """从 500 彩票网爬取"""
    import requests
    from bs4 import BeautifulSoup
    
    url = "http://kaijiang.500.com/ssq.shtml"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'gb2312'
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    records = []
    table = soup.find('table', {'id': 'tdata'})
    
    for row in table.find_all('tr')[1:]:  # 跳过表头
        cols = row.find_all('td')
        if len(cols) >= 9:
            issue = cols[0].text.strip()
            date = cols[1].text.strip()
            reds = [int(cols[i].text) for i in range(2, 8)]
            blue = int(cols[8].text)
            
            records.append({
                'issue': issue,
                'date': date,
                'red1': reds[0], 'red2': reds[1], 'red3': reds[2],
                'red4': reds[3], 'red5': reds[4], 'red6': reds[5],
                'blue': blue
            })
    
    return pd.DataFrame(records)
```

---

## 🔧 集成到项目

### 修改 data_fetcher.py

在 `DataFetcher` 类中添加真实 API 方法：

```python
class DataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        })
    
    def fetch_from_api(self, source: str = 'zhcw', **kwargs):
        """统一 API 接口"""
        if source == 'zhcw':
            return self.fetch_from_zhcw(**kwargs)
        elif source == 'juhe':
            return self.fetch_from_juhe(**kwargs)
        elif source == 'apihubs':
            return self.fetch_from_apihubs(**kwargs)
        elif source == '500wan':
            return self.fetch_from_500wan(**kwargs)
        else:
            return self._generate_mock_data(100)
    
    def fetch_from_zhcw(self, page=1, page_size=30):
        """中国福彩网"""
        # 实现上面的代码
        pass
    
    def fetch_from_juhe(self, api_key=None, **kwargs):
        """聚合数据"""
        if api_key is None:
            api_key = os.getenv('JUHE_API_KEY', 'YOUR_DEFAULT_KEY')
        # 实现上面的代码
        pass
    
    def fetch_from_apihubs(self, **kwargs):
        """APIHubs 历史数据"""
        # 实现上面的代码
        pass
    
    def fetch_from_500wan(self, **kwargs):
        """500 彩票网"""
        # 实现上面的代码
        pass
```

---

## 📝 使用示例

### 1. 首次获取历史数据

```bash
# 使用 APIHubs 获取 1000 期历史数据
python3 auto_update.py -f data/historical_data.csv -s apihubs --force
```

### 2. 日常更新（福彩网）

```bash
# 每天从福彩网检查更新
python3 auto_update.py -f data/historical_data.csv -s zhcw -i daily
```

### 3. 使用聚合数据

```bash
# 需要 API 密钥
export JUHE_API_KEY="your_api_key_here"
python3 auto_update.py -f data/historical_data.csv -s juhe -i daily
```

---

## 🔑 API 密钥管理

### 方式一：环境变量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export JUHE_API_KEY="your_api_key"
export ALIYUN_APPCODE="your_appcode"

# 生效
source ~/.bashrc
```

### 方式二：配置文件

创建 `config.ini`:

```ini
[api]
juhe_key = your_api_key
aliyun_appcode = your_appcode
```

在代码中读取:

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

JUHE_KEY = config.get('api', 'juhe_key')
```

---

## 📊 API 对比

| API | 免费 | 需要密钥 | 稳定性 | 推荐度 |
|-----|------|----------|--------|--------|
| 福彩网 | ✅ | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| APIHubs | ✅ | ❌ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 聚合数据 | ⚠️ (限额) | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 阿里云 | ⚠️ (付费) | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 500 万 | ✅ | ❌ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## ⚠️ 注意事项

1. **请求频率** - 避免频繁请求，建议每天更新 1-2 次
2. **User-Agent** - 设置合适的 User-Agent 避免被屏蔽
3. **错误处理** - 添加重试机制和错误处理
4. **数据校验** - 验证返回数据的完整性
5. **遵守规则** - 遵守 API 提供商的使用条款

---

## 🔍 推荐方案

### 最佳实践

```python
# 1. 首次获取：使用 APIHubs（大量历史数据）
fetcher.fetch_from_api(source='apihubs')

# 2. 日常更新：使用福彩网（官方数据）
fetcher.fetch_from_api(source='zhcw')

# 3. 备用方案：500 彩票网
fetcher.fetch_from_api(source='500wan')
```

### 自动切换

```python
def fetch_with_fallback(self):
    """带降级策略的获取"""
    sources = ['zhcw', 'apihubs', '500wan']
    
    for source in sources:
        try:
            df = self.fetch_from_api(source)
            if df is not None and len(df) > 0:
                return df
        except Exception as e:
            print(f"❌ {source} 失败：{e}")
            continue
    
    # 所有源都失败，返回模拟数据
    return self._generate_mock_data(100)
```

---

**最后更新:** 2026-03-23  
**版本:** v1.0
