# 🤖 多智能体系统 - 使用指南

## 🎯 快速开始

### 查看系统状态

```bash
cd /home/admin/openclaw/workspace/ssq-pure

# 查看所有智能体状态
python3 agent_system.py --status
```

### 列出所有智能体

```bash
# 列出可用智能体
python3 agent_system.py --list
```

**输出:**
```
🤖 可用智能体:
  - coder: 代码开发智能体
  - data: 数据分析智能体
  - tester: 测试智能体
  - doc: 文档智能体
  - builder: 构建智能体
  - monitor: 监控智能体
```

---

## 📋 分配任务

### 基本用法

```bash
python3 agent_system.py --agent <智能体类型> --task "<任务描述>" --priority <优先级>
```

### 参数说明

| 参数 | 说明 | 选项 |
|------|------|------|
| `--agent, -a` | 智能体类型 | coder, data, tester, doc, builder, monitor |
| `--task, -t` | 任务描述 | 任意字符串 |
| `--priority, -p` | 优先级 | low, normal, high, urgent |

---

## 🤖 智能体任务示例

### 1️⃣ 代码开发智能体 (coder)

```bash
# 运行预测
python3 agent_system.py -a coder -t "运行预测"

# 优化代码
python3 agent_system.py -a coder -t "优化预测算法" -p high

# 代码审查
python3 agent_system.py -a coder -t "审查 ssq_predictor.py"

# 修复 bug
python3 agent_system.py -a coder -t "修复数据加载 bug" -p urgent
```

### 2️⃣ 数据分析智能体 (data)

```bash
# 更新数据
python3 agent_system.py -a data -t "更新历史数据" -p high

# 数据分析
python3 agent_system.py -a data -t "分析最近 100 期数据"

# 数据统计
python3 agent_system.py -a data -t "生成统计报表"

# 数据验证
python3 agent_system.py -a data -t "验证数据完整性"
```

### 3️⃣ 测试智能体 (tester)

```bash
# 运行测试
python3 agent_system.py -a tester -t "运行单元测试"

# 验证数据
python3 agent_system.py -a tester -t "验证历史数据"

# 代码审查
python3 agent_system.py -a tester -t "审查最新代码"

# 性能测试
python3 agent_system.py -a tester -t "性能测试" -p high
```

### 4️⃣ 文档智能体 (doc)

```bash
# 更新文档
python3 agent_system.py -a doc -t "更新 README.md"

# 生成文档
python3 agent_system.py -a doc -t "生成 API 文档"

# 更新使用说明
python3 agent_system.py -a doc -t "更新使用指南"
```

### 5️⃣ 构建智能体 (builder)

```bash
# 构建 EXE
python3 agent_system.py -a builder -t "构建 Windows EXE" -p high

# 创建 Release
python3 agent_system.py -a builder -t "创建 Release v1.0.1" -p urgent

# 检查构建状态
python3 agent_system.py -a builder -t "检查构建状态"
```

### 6️⃣ 监控智能体 (monitor)

```bash
# 检查系统状态
python3 agent_system.py -a monitor -t "检查系统状态"

# 查看日志
python3 agent_system.py -a monitor -t "查看错误日志"

# 持续监控
python3 agent_system.py -a monitor -t "持续监控系统"
```

---

## 📊 任务优先级

| 优先级 | 说明 | 使用场景 |
|--------|------|---------|
| `low` | 低优先级 | 日常维护、文档更新 |
| `normal` | 普通优先级 | 常规任务 |
| `high` | 高优先级 | 数据更新、Bug 修复 |
| `urgent` | 紧急 | 严重 Bug、Release 发布 |

---

## 🔄 多智能体协作

### 场景 1：发布新版本

```bash
# 1. Coder 完成最后的功能开发
python3 agent_system.py -a coder -t "完成新功能" -p high

# 2. Tester 执行测试
python3 agent_system.py -a tester -t "回归测试" -p high

# 3. Doc 更新文档
python3 agent_system.py -a doc -t "更新 Release Notes"

# 4. Builder 创建 Release
python3 agent_system.py -a builder -t "创建 Release v1.0.1" -p urgent
```

### 场景 2：数据更新流程

```bash
# 1. Data 获取最新数据
python3 agent_system.py -a data -t "更新历史数据" -p high

# 2. Tester 验证数据质量
python3 agent_system.py -a tester -t "验证新数据"

# 3. Monitor 监控数据更新
python3 agent_system.py -a monitor -t "监控数据更新状态"
```

### 场景 3：Bug 修复流程

```bash
# 1. Monitor 发现并报告 Bug
python3 agent_system.py -a monitor -t "报告错误：预测结果异常" -p urgent

# 2. Coder 分析并修复
python3 agent_system.py -a coder -t "修复预测算法 bug" -p urgent

# 3. Tester 验证修复
python3 agent_system.py -a tester -t "验证 bug 修复" -p high

# 4. Builder 发布热修复
python3 agent_system.py -a builder -t "发布热修复" -p high
```

---

## 📝 实际运行示例

### 示例 1：运行预测

```bash
$ python3 agent_system.py -a coder -t "运行预测"

✅ 任务已分配给 代码开发智能体
   任务：运行预测
   优先级：normal
   时间：2026-03-23 14:46:56

🚀 开始执行任务...
   智能体：代码开发智能体
   任务：运行预测
   🔮 正在运行预测...

============================================================
🎱 双色球预测软件 v1.0
============================================================

📂 加载历史数据...
✅ 已加载 3428 期开奖数据

🔮 生成预测号码...

第 1 组:
  红球：01 14 16 19 20 24
  蓝球：16
  和值：94 | AC 指数：8

✅ 任务完成！
   结果：预测完成
```

### 示例 2：更新数据

```bash
$ python3 agent_system.py -a data -t "更新历史数据" -p high

✅ 任务已分配给 数据分析智能体
   任务：更新历史数据
   优先级：high
   时间：2026-03-23 14:46:56

🚀 开始执行任务...
   智能体：数据分析智能体
   任务：更新历史数据
   📡 正在更新数据...
✅ 任务完成！
   结果：数据更新完成
```

### 示例 3：查看状态

```bash
$ python3 agent_system.py --status

============================================================
🤖 多智能体系统状态
============================================================

📋 智能体列表 (6 个):
  - coder: 代码开发智能体
  - data: 数据分析智能体
  - tester: 测试智能体
  - doc: 文档智能体
  - builder: 构建智能体
  - monitor: 监控智能体

⏳ 待执行任务：0

✅ 已完成任务：3
  ✅ [data] 更新历史数据
  ✅ [coder] 运行预测
  ✅ [monitor] 检查系统状态

============================================================
```

---

## ⚙️ 高级用法

### 批量分配任务

```bash
#!/bin/bash
# 批量分配任务

# 数据更新流程
python3 agent_system.py -a data -t "获取最新数据" -p high
python3 agent_system.py -a tester -t "验证数据" -p normal
python3 agent_system.py -a monitor -t "监控更新" -p low
```

### 任务队列管理

```python
# Python 脚本中批量分配
from agent_system import MultiAgentSystem

system = MultiAgentSystem()

# 分配多个任务
system.assign_task("data", "更新数据", "high")
system.assign_task("coder", "优化算法", "normal")
system.assign_task("tester", "运行测试", "normal")

# 显示状态
system.show_status()
```

---

## 📊 智能体状态

| 智能体 | 状态 | 职责 |
|--------|------|------|
| coder | 🟢 就绪 | 代码开发、优化、Bug 修复 |
| data | 🟢 就绪 | 数据获取、分析、统计 |
| tester | 🟢 就绪 | 测试、验证、审查 |
| doc | 🟢 就绪 | 文档编写、更新 |
| builder | 🟢 就绪 | 构建、打包、Release |
| monitor | 🟢 运行中 | 监控、日志、告警 |

---

## 🎯 最佳实践

### 1. 合理分配优先级

- 日常任务：`normal`
- 数据更新：`high`
- Bug 修复：`high` 或 `urgent`
- Release 发布：`urgent`

### 2. 明确任务描述

❌ 不好：`"修复问题"`
✅ 好：`"修复数据加载时的编码错误"`

### 3. 监控任务执行

```bash
# 定期检查系统状态
python3 agent_system.py --status

# 查看最近任务
python3 agent_system.py --status | grep "已完成"
```

### 4. 自动化流程

```bash
# 创建自动化脚本
cat > auto_tasks.sh << 'EOF'
#!/bin/bash
# 每日自动化任务

# 1. 更新数据
python3 agent_system.py -a data -t "更新历史数据" -p high

# 2. 验证数据
python3 agent_system.py -a tester -t "验证数据完整性"

# 3. 运行预测
python3 agent_system.py -a coder -t "运行每日预测"

# 4. 监控系统
python3 agent_system.py -a monitor -t "检查系统状态"
EOF

chmod +x auto_tasks.sh
```

---

## 📞 常见问题

### Q: 如何查看智能体执行日志？

A: 任务执行时会实时输出日志到终端，也可以查看系统状态。

### Q: 任务执行失败怎么办？

A: 系统会显示错误信息，根据错误调整任务描述或检查代码。

### Q: 可以自定义智能体吗？

A: 可以！编辑 `agent_system.py` 中的 `self.agents` 字典添加新智能体。

### Q: 如何并行执行多个任务？

A: 使用后台运行：
```bash
python3 agent_system.py -a coder -t "任务 1" &
python3 agent_system.py -a data -t "任务 2" &
wait
```

---

## 🎉 总结

多智能体系统让双色球预测软件的开发和维护更加高效！

**优势:**
- 🤖 6 个专业智能体分工
- ⚡ 快速分配和执行任务
- 📊 实时状态监控
- 🔧 灵活的任务优先级
- 📝 完整的任务记录

**开始使用:**
```bash
python3 agent_system.py --help
```

---

**版本:** v1.0.0  
**更新时间:** 2026-03-23  
**智能体数量:** 6 个
