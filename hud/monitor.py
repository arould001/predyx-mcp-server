#!/usr/bin/env python3
"""OpenClaw 状态监控器 - 简化版（无需外部依赖）"""

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

STATUS_FILE = Path(__file__).parent.parent / "status.json"
GATEWAY_PORT = 18789

def check_gateway_status():
    """检查 Gateway 进程状态（使用系统命令）"""
    try:
        # 使用 lsof 检查端口
        result = subprocess.run(
            ["/usr/sbin/lsof", "-i", f":{GATEWAY_PORT}", "-P"],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        if "LISTEN" in result.stdout:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                # 解析 PID
                parts = lines[1].split()
                pid = int(parts[1])
                
                # 使用 ps 获取进程信息
                ps_result = subprocess.run(
                    ["ps", "-p", str(pid), "-o", "etime,pcpu,rss"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                if ps_result.returncode == 0:
                    ps_lines = ps_result.stdout.strip().split('\n')
                    if len(ps_lines) > 1:
                        ps_parts = ps_lines[1].split()
                        uptime_str = ps_parts[0]
                        cpu_percent = float(ps_parts[1])
                        memory_kb = int(ps_parts[2])
                        
                        return {
                            "running": True,
                            "pid": pid,
                            "uptime_str": uptime_str,
                            "cpu_percent": cpu_percent,
                            "memory_mb": memory_kb / 1024
                        }
        
        return {"running": False}
        
    except Exception as e:
        print(f"检查失败: {e}")
        return {"running": False}

def get_openclaw_sessions():
    """读取 OpenClaw 会话数据"""
    sessions_file = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"
    
    if not sessions_file.exists():
        return []
    
    try:
        with open(sessions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        sessions = []
        for session_key, session_data in data.items():
            # 提取关键信息
            session_info = {
                "key": session_key,
                "id": session_data.get("sessionId", "unknown"),
                "updated": session_data.get("updatedAt", 0),
                "chat_type": session_data.get("chatType", "unknown"),
                "channel": session_data.get("lastChannel", "unknown"),
                "model": session_data.get("model", "unknown"),
                "tokens": {
                    "input": session_data.get("inputTokens", 0),
                    "output": session_data.get("outputTokens", 0),
                    "total": session_data.get("totalTokens", 0)
                }
            }
            sessions.append(session_info)
        
        # 按更新时间排序（最新的在前）
        sessions.sort(key=lambda x: x["updated"], reverse=True)
        return sessions[:5]  # 只返回最近5个
        
    except Exception as e:
        print(f"读取会话失败: {e}")
        return []

def update_status():
    """更新状态文件"""
    # 读取现有状态
    if STATUS_FILE.exists():
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            status = json.load(f)
    else:
        status = {
            "agent": {"name": "Dia", "status": "offline", "model": "zai/glm-5"},
            "session": {},
            "context": {"used_tokens": 0, "max_tokens": 128000},
            "tools": {"calls_today": 0, "recent_calls": []},
            "tasks": {"completed": 0, "pending": 0}
        }
    
    # 检查 Gateway 状态
    gateway = check_gateway_status()
    
    if gateway["running"]:
        status["agent"]["status"] = "idle"
        status["session"]["running"] = True
        status["session"]["uptime"] = gateway["uptime_str"]
        status["session"]["gateway_pid"] = gateway["pid"]
        status["session"]["cpu_percent"] = round(gateway["cpu_percent"], 1)
        status["session"]["memory_mb"] = round(gateway["memory_mb"], 1)
        status["session"]["duration"] = gateway["uptime_str"]
        
        # 获取会话数据
        sessions = get_openclaw_sessions()
        if sessions:
            status["tasks"]["active_sessions"] = len(sessions)
            
            # 计算总 Token 使用
            total_tokens = sum(s["tokens"]["total"] for s in sessions)
            status["context"]["used_tokens"] = total_tokens
            status["context"]["usage_percent"] = round(total_tokens / 128000 * 100, 1)
            
            # 任务队列：显示活跃会话
            status["tasks"]["queue"] = [
                {
                    "name": f"{s['channel']}:{s['chat_type']}",
                    "tokens": s["tokens"]["total"]
                }
                for s in sessions[:3]
            ]
    else:
        status["agent"]["status"] = "offline"
        status["session"]["running"] = False
        status["session"]["uptime"] = "0:00"
        status["session"]["duration"] = "0:00"
    
    # 保存状态
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    
    return status

def main():
    """主循环"""
    print("🔍 OpenClaw 状态监控器启动")
    print(f"   监控端口: {GATEWAY_PORT}")
    print(f"   状态文件: {STATUS_FILE}")
    print()
    
    while True:
        try:
            status = update_status()
            if status["session"]["running"]:
                print(f"✓ Gateway 运行中 (PID: {status['session']['gateway_pid']}, "
                      f"时长: {status['session']['duration']}, "
                      f"CPU: {status['session']['cpu_percent']}%, "
                      f"内存: {status['session']['memory_mb']:.1f}MB)", flush=True)
            else:
                print("⚠️  Gateway 未运行", flush=True)
            
            time.sleep(5)  # 每5秒更新一次
            
        except KeyboardInterrupt:
            print("\n👋 监控器已停止")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
