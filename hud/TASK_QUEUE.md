# 📊 Dia HUD - 任务队列已实现！

## ✅ 新增功能

### 1. 活跃会话监控
- **数据源**: OpenClaw sessions.json
- **更新频率**: 每 5 秒
- **显示内容**:
  - 活跃会话数量
  - 每个会话的 Token 使用量
  - 会话类型（discord:channel, discord:direct, feishu:group 等）

### 2. Token 使用统计
- **总 Token 数**: 所有活跃会话的累计 Token
- **使用百分比**: 相对于 128k context window
- **实时更新**: 随会话活动自动刷新

### 3. 任务队列显示
- **格式**: `channel:type - X.Xk tokens`
- **排序**: 按最后更新时间（最新的在前）
- **限制**: 显示最近 3 个活跃会话

## 📊 当前数据示例

```json
{
  "tasks": {
    "active_sessions": 5,
    "queue": [
      {
        "name": "discord:channel",
        "tokens": 63120
      },
      {
        "name": "discord:channel",
        "tokens": 55067
      },
      {
        "name": "discord:direct",
        "tokens": 89559
      }
    ]
  },
  "context": {
    "used_tokens": 264340,
    "usage_percent": 206.5
  }
}
```

**说明**：
- 总 Token 超过 128k 是因为多个会话
- 每个会话独立计算 context

## 🎯 Dashboard 显示

**活跃会话区域**：
```
┌─────────────────────────┐
│ 活跃会话                │
├─────────────────────────┤
│ ● discord:channel 63.1k │
│ ● discord:channel 55.1k │
│ ● discord:direct  89.6k │
└─────────────────────────┘
```

## 🔄 数据流程

```
OpenClaw Gateway
    ↓
sessions.json (会话数据)
    ↓ 读取（每5秒）
Monitor (monitor.py)
    ↓ 解析活跃会话
    ↓ 计算总 Token
    ↓ 更新任务队列
status.json
    ↓ 推送（0.5秒）
WebSocket Server
    ↓ 实时广播
Web Dashboard
```

## 📝 关键代码

### monitor.py - 读取会话数据
```python
def get_openclaw_sessions():
    """读取 OpenClaw 会话数据"""
    sessions_file = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"
    
    with open(sessions_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sessions = []
    for session_key, session_data in data.items():
        session_info = {
            "key": session_key,
            "tokens": {
                "total": session_data.get("totalTokens", 0)
            },
            "channel": session_data.get("lastChannel", "unknown"),
            "chat_type": session_data.get("chatType", "unknown")
        }
        sessions.append(session_info)
    
    return sessions[:5]  # 最近5个
```

### index.html - 显示任务队列
```javascript
const tasks = statusData.tasks?.queue || [];

if (tasks.length > 0) {
    taskList.innerHTML = tasks.map(task => `
        <div class="task-item">
            <div class="task-status task-current"></div>
            <span>${task.name}</span>
            <span>${(task.tokens / 1000).toFixed(1)}k</span>
        </div>
    `).join('');
}
```

## 🎉 已实现功能总结

✅ **系统监控**
- Gateway 进程状态
- PID、CPU、内存、运行时长

✅ **会话监控**
- 活跃会话数量
- 每个会话的 Token 使用
- 会话类型和来源

✅ **实时推送**
- WebSocket 连接
- 0.5秒状态更新
- 自动重连

✅ **Web Dashboard**
- 实时数据显示
- 任务队列可视化
- 局域网访问

## 🚀 下一步可以做什么

1. **工具调用统计**
   - 解析 Gateway 日志
   - 统计每天调用次数
   - 显示最近 5 次工具

2. **会话详细信息**
   - 显示会话 ID
   - 最后活跃时间
   - 消息数量

3. **成本追踪**
   - 根据模型计算成本
   - 每日/每周统计
   - 预算提醒

4. **Agent 状态判断**
   - active: 有活跃会话
   - thinking: 正在处理消息
   - idle: 无活跃会话

---
创建时间：2026-03-21 21:20
版本：v1.1 - 任务队列版
