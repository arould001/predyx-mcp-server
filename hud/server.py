#!/usr/bin/env python3
"""Dia HUD - WebSocket Server"""

import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path
import websockets
from aiohttp import web

# 配置
STATUS_FILE = Path(__file__).parent.parent / "status.json"
PORT = 8888
HOST = "0.0.0.0"

# 状态
connected_clients = set()
status_cache = {}


async def read_status():
    """读取状态文件"""
    try:
        if STATUS_FILE.exists():
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"读取状态文件失败: {e}")
    return {}


async def broadcast_status():
    """广播状态更新"""
    if not connected_clients:
        return
    
    status = await read_status()
    message = json.dumps(status, ensure_ascii=False)
    
    # 广播给所有客户端
    disconnected = set()
    for client in connected_clients:
        try:
            await client.send(message)
        except:
            disconnected.add(client)
    
    # 移除断开的客户端
    connected_clients.difference_update(disconnected)


async def status_watcher():
    """监听状态文件变化"""
    last_mtime = 0
    
    while True:
        try:
            if STATUS_FILE.exists():
                mtime = STATUS_FILE.stat().st_mtime
                if mtime > last_mtime:
                    last_mtime = mtime
                    await broadcast_status()
        except Exception as e:
            print(f"监听状态失败: {e}")
        
        await asyncio.sleep(0.5)


async def websocket_handler(websocket):
    """WebSocket 处理器"""
    connected_clients.add(websocket)
    print(f"✓ 客户端连接 ({len(connected_clients)} 在线)")
    
    try:
        # 立即发送当前状态
        status = await read_status()
        await websocket.send(json.dumps(status, ensure_ascii=False))
        
        # 保持连接
        async for message in websocket:
            # 处理客户端消息（如果需要）
            pass
    
    except websockets.exceptions.ConnectionClosed:
        pass
    
    finally:
        connected_clients.discard(websocket)
        print(f"✗ 客户端断开 ({len(connected_clients)} 在线)")


async def http_handler(request):
    """HTTP 静态文件服务"""
    index_path = Path(__file__).parent / "index.html"
    
    if request.path == "/":
        return web.FileResponse(index_path)
    
    return web.Response(status=404)


async def start_server():
    """启动服务器"""
    # HTTP 服务器（用于静态文件）
    app = web.Application()
    app.router.add_get("/", http_handler)
    app.router.add_static("/", Path(__file__).parent)
    
    runner = web.AppRunner(app)
    await runner.setup()
    http_site = web.TCPSite(runner, HOST, PORT)
    await http_site.start()
    
    print(f"📊 Dia HUD 启动成功")
    print(f"   Web界面: http://localhost:{PORT}")
    print(f"   局域网: http://192.168.1.189:{PORT}")
    print()
    
    # WebSocket 服务器
    ws_server = await websockets.serve(websocket_handler, HOST, PORT + 1)
    print(f"   WebSocket: ws://localhost:{PORT + 1}")
    print()
    
    # 启动状态监听
    asyncio.create_task(status_watcher())
    
    # 保持运行
    await asyncio.Future()


if __name__ == "__main__":
    print("🚀 启动 Dia HUD...")
    print()
    asyncio.run(start_server())
