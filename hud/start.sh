#!/bin/bash
# 启动 Dia HUD 完整服务

echo "🚀 启动 Dia HUD 完整服务..."
echo ""

# 停止旧进程
echo "停止旧进程..."
pkill -f "server.py" 2>/dev/null
pkill -f "monitor.py" 2>/dev/null
sleep 2

# 启动 WebSocket Server
echo "启动 WebSocket Server..."
cd ~/.openclaw/workspace/hud
python3 server.py > /tmp/hud_server.log 2>&1 &
SERVER_PID=$!
sleep 2

# 检查是否启动成功
if ps -p $SERVER_PID > /dev/null; then
    echo "✓ WebSocket Server 已启动 (PID: $SERVER_PID)"
else
    echo "✗ WebSocket Server 启动失败"
    cat /tmp/hud_server.log
    exit 1
fi

# 启动状态监控器
echo "启动状态监控器..."
python3 monitor.py > /tmp/monitor.log 2>&1 &
MONITOR_PID=$!
sleep 2

# 检查是否启动成功
if ps -p $MONITOR_PID > /dev/null; then
    echo "✓ 状态监控器已启动 (PID: $MONITOR_PID)"
else
    echo "✗ 状态监控器启动失败"
    cat /tmp/monitor.log
    exit 1
fi

echo ""
echo "📊 Dia HUD 启动成功！"
echo ""
echo "访问地址："
echo "  本机:   http://localhost:8888"
echo "  局域网: http://192.168.1.189:8888"
echo ""
echo "日志文件："
echo "  Server:  /tmp/hud_server.log"
echo "  Monitor: /tmp/monitor.log"
echo ""
echo "停止服务: pkill -f 'server.py|monitor.py'"
