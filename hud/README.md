# 📊 Dia HUD - OpenClaw Agent 实时监控系统

## 系统架构

```
┌─────────────────────┐
│  OpenClaw Gateway   │
│   (Port 18789)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Monitor (监控器)   │ ← 每5秒检查一次
│  - 进程状态          │
│  - CPU/内存          │
│  - 运行时长          │
└──────────┬──────────┘
           │
           ▼ 更新
┌─────────────────────┐
│   status.json       │
│  (状态文件)          │
└──────────┬──────────┘
           │
           ▼ 监听（0.5秒）
┌─────────────────────┐
│  WebSocket Server   │
│   (Port 8889)       │
└──────────┬──────────┘
           │
           ▼ 推送
┌─────────────────────┐
│   Web Dashboard     │
│   (Port 8888)       │
└─────────────────────┘
```

## 组件说明

### 1. monitor.py - 状态监控器
**功能**：
- 每5秒检查 Gateway 进程状态
- 使用系统命令（lsof + ps）获取进程信息
- 更新 status.json 文件

**监控指标**：
- 进程运行状态（运行中/未运行）
- Gateway PID
- 运行时长
- CPU 使用率
- 内存占用

### 2. server.py - WebSocket 服务器
**功能**：
- 提供 WebSocket 连接（端口 8889）
- 监听 status.json 文件变化（0.5秒轮询）
- 实时广播状态更新给所有客户端
- 提供 HTTP 静态文件服务（端口 8888）

### 3. index.html - Web Dashboard
**功能**：
- 实时显示 Agent 状态
- WebSocket 连接状态指示
- 可视化展示监控数据

**显示内容**：
- Agent 状态（空闲/工作中/思考中/离线）
- Gateway PID
- 运行时长
- CPU 使用率
- 内存占用
- Context Token 使用情况（预留）
- 工具调用统计（预留）
- 任务队列（预留）

## 使用方法

### 启动服务
```bash
~/.openclaw/workspace/hud/start.sh
```

### 访问 Dashboard
- 本机：http://localhost:8888
- 局域网：http://192.168.1.189:8888

### 停止服务
```bash
pkill -f "server.py|monitor.py"
```

### 查看日志
```bash
# Server 日志
tail -f /tmp/hud_server.log

# Monitor 日志
tail -f /tmp/monitor.log
```

## 状态文件格式 (status.json)

```json
{
  "agent": {
    "name": "Dia",
    "status": "idle|active|thinking|offline",
    "current_task": null,
    "model": "zai/glm-5"
  },
  "session": {
    "running": true,
    "gateway_pid": 38919,
    "uptime": "03:34:41",
    "duration": "03:34:41",
    "cpu_percent": 6.8,
    "memory_mb": 707.1
  },
  "context": {
    "used_tokens": 0,
    "max_tokens": 128000,
    "usage_percent": 0
  },
  "tools": {
    "calls_today": 0,
    "recent_calls": []
  },
  "tasks": {
    "completed": 0,
    "pending": 0,
    "current": null
  }
}
```

## 已实现功能

✅ WebSocket 实时推送
✅ 进程状态监控（PID、CPU、内存、时长）
✅ Web Dashboard 显示
✅ 局域网访问
✅ 状态文件自动更新（5秒间隔）
✅ WebSocket 自动重连
✅ 连接状态指示

## 待实现功能

🔄 Context Token 实时监控（需要 OpenClaw API 支持）
🔄 工具调用统计（需要日志解析或 API）
🔄 任务队列显示（需要 OpenClaw 任务系统）
🔄 消息数量统计（需要会话 API）
🔄 成本累计（需要 API 调用成本数据）
🔄 Agent 状态判断（active/thinking 状态检测）

## 技术栈

- **Python 3.14**：监控器 + WebSocket 服务器
- **aiohttp**：HTTP 服务器
- **websockets**：WebSocket 库
- **原生 JavaScript**：前端展示
- **系统命令**：lsof + ps（无需外部 Python 依赖）

## 优势

1. **轻量级**：使用系统命令，无需安装 psutil 等依赖
2. **非侵入式**：不修改 OpenClaw 主程序
3. **可扩展**：status.json 格式易于扩展新字段
4. **实时性**：0.5秒 WebSocket 推送 + 5秒状态更新

## 故障排除

### Dashboard 显示"未连接"
1. 检查 WebSocket Server 是否运行：`ps aux | grep server.py`
2. 检查端口是否监听：`lsof -i :8889`
3. 查看日志：`cat /tmp/hud_server.log`

### 数据不更新
1. 检查 Monitor 是否运行：`ps aux | grep monitor.py`
2. 查看 status.json 是否更新：`cat ~/.openclaw/workspace/status.json`
3. 查看日志：`cat /tmp/monitor.log`

### 端口被占用
```bash
# 查看端口占用
lsof -i :8888
lsof -i :8889

# 停止所有旧进程
pkill -f "server.py|monitor.py"
```

---
创建时间：2026-03-21
版本：v1.0
