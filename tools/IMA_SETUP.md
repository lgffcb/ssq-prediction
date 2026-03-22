# IMA 笔记技能配置指南

## ✅ 安装状态

| 项目 | 状态 |
|------|------|
| 技能文件 | ✅ 已安装 |
| 安装路径 | `~/.openclaw/skills/ima-note/` |
| API 凭证 | ⏳ 待配置 |

---

## 🔑 获取 API Key 步骤

### 1️⃣ 打开 IMA 官网
访问：https://ima.qq.com/agent-interface

### 2️⃣ 登录/注册
- 使用 QQ 或微信扫码登录
- 如果没有账号，先注册

### 3️⃣ 创建应用
- 进入"应用管理"
- 点击"创建新应用"
- 填写应用名称（如：OpenClaw 助手）
- 选择应用类型：AI Agent

### 4️⃣ 获取凭证
创建成功后，你会获得：
- **Client ID** （客户端 ID）
- **API Key** （API 密钥）

---

## ⚙️ 配置环境变量

### 方式一：临时配置（当前会话有效）

```bash
export IMA_OPENAPI_CLIENTID="你的 Client ID"
export IMA_OPENAPI_APIKEY="你的 API Key"
```

### 方式二：永久配置（推荐）

编辑 `~/.bashrc` 或 `~/.zshrc`：

```bash
echo 'export IMA_OPENAPI_CLIENTID="你的 Client ID"' >> ~/.bashrc
echo 'export IMA_OPENAPI_APIKEY="你的 API Key"' >> ~/.bashrc
source ~/.bashrc
```

### 方式三：写入 .env 文件

在 workspace 创建 `.env` 文件：

```bash
IMA_OPENAPI_CLIENTID=你的 Client ID
IMA_OPENAPI_APIKEY=你的 API Key
```

---

## 🧪 测试配置

配置完成后，运行以下命令测试：

```bash
# 检查环境变量是否设置
echo $IMA_OPENAPI_CLIENTID
echo $IMA_OPENAPI_APIKEY

# 测试 API 调用
curl -X POST "https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"cursor": "0", "limit": 5}'
```

---

## 📝 可用功能

配置成功后，你可以让我：

| 功能 | 示例 |
|------|------|
| 📖 **搜索笔记** | "帮我找一下关于项目会议的笔记" |
| 📚 **浏览笔记本** | "看看我有哪些笔记本" |
| 📄 **读取笔记** | "打开上周的工作总结" |
| ✍️ **新建笔记** | "帮我记一下今天的待办事项" |
| ➕ **追加内容** | "给刚才的笔记补充一点内容" |
| 🗂️ **整理笔记** | "把这篇笔记移到工作笔记本" |

---

## 🔒 隐私说明

- 笔记内容属于个人隐私
- 在群聊场景中只展示标题和摘要
- 不会主动展示笔记正文
- API 调用使用 HTTPS 加密传输

---

## ⚠️ 注意事项

1. **API Key 保密** - 不要分享给他人
2. **调用频率** - 避免短时间内大量请求
3. **内容大小** - 单篇笔记有大小限制，超长需拆分
4. **编码格式** - 确保内容 UTF-8 编码

---

## 🆘 常见问题

### Q: 提示"缺少 IMA 凭证"
A: 请按上述步骤配置环境变量

### Q: API 调用失败
A: 检查 Client ID 和 API Key 是否正确，确认未过期

### Q: 笔记内容乱码
A: 确保内容 UTF-8 编码，中文内容注意转码

---

## 📞 获取帮助

- IMA 官网：https://ima.qq.com
- API 文档：`~/.openclaw/skills/ima-note/references/api.md`
- 技能文件：`~/.openclaw/skills/ima-note/SKILL.md`

---

**下一步：** 请获取 API Key 后告诉我，我帮你验证配置！🔑
