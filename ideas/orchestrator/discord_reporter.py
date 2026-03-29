#!/usr/bin/env python3
"""
Discord 集成 - 定期汇报 agents 进度到 Discord
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import Orchestrator


def send_to_discord(message: str):
    """发送消息到 Discord（通过 OpenClaw message 工具）"""
    # 这里可以调用 OpenClaw 的 message tool
    # 或者直接用 Discord webhook
    print(f"[Discord] {message}")


def monitor_loop(orchestrator: Orchestrator, interval: int = 60):
    """定期监控并发送汇报"""
    
    last_report = None
    
    while True:
        report = orchestrator.status()
        
        # 检查是否有变化
        if report != last_report:
            # 格式化消息
            msg_lines = ["🤖 Agent-Agile 进度汇报\n"]
            
            # Agents 状态
            msg_lines.append("**Agents:**")
            for aid, info in report["agents"].items():
                emoji = {"idle": "😴", "running": "🔄", "completed": "✅"}.get(info["status"], "❓")
                msg_lines.append(f"  {emoji} {aid}: {info['status']}")
            
            # Tasks 统计
            msg_lines.append(f"\n**Tasks:**")
            msg_lines.append(f"  Pending: {report['tasks']['pending']}")
            msg_lines.append(f"  Running: {report['tasks']['running']}")
            msg_lines.append(f"  Completed: {report['tasks']['completed']}")
            msg_lines.append(f"  Failed: {report['tasks']['failed']}")
            
            # 发送
            send_to_discord("\n".join(msg_lines))
            last_report = report
        
        time.sleep(interval)


if __name__ == "__main__":
    orchestrator = Orchestrator()
    monitor_loop(orchestrator)
