#!/usr/bin/env python3
"""
Multi-Agent Orchestrator
40 人团队 Agent-Agile 协作编排器
"""

import json
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional
import fcntl

# ============================================================
# 配置
# ============================================================

STATE_FILE = Path.home() / ".openclaw" / "workspace" / "ideas" / "orchestrator" / "state.json"
LOCK_FILE = STATE_FILE.with_suffix(".lock")
HEARTBEAT_INTERVAL = 30  # seconds
MAX_RETRIES = 3


# ============================================================
# State Manager（线程安全）
# ============================================================

class StateManager:
    """共享状态管理器，使用文件锁保证线程安全"""
    
    def __init__(self, state_file: Path, lock_file: Path):
        self.state_file = state_file
        self.lock_file = lock_file
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化状态文件
        if not self.state_file.exists():
            self._write_state({
                "agents": {},
                "tasks": {},
                "history": [],
                "last_update": None
            })
    
    def _read_state(self) -> dict:
        with open(self.lock_file, 'w') as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    
    def _write_state(self, state: dict):
        with open(self.lock_file, 'w') as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                state["last_update"] = datetime.now().isoformat()
                with open(self.state_file, 'w') as f:
                    json.dump(state, f, indent=2, ensure_ascii=False)
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    
    def register_agent(self, agent_id: str, role: str):
        """注册 agent"""
        state = self._read_state()
        state["agents"][agent_id] = {
            "role": role,
            "status": "idle",
            "current_task": None,
            "last_heartbeat": datetime.now().isoformat(),
            "completed_tasks": 0,
            "failed_tasks": 0
        }
        self._write_state(state)
        print(f"[Orchestrator] Agent {agent_id} ({role}) registered")
    
    def update_agent_status(self, agent_id: str, status: str, task_id: Optional[str] = None):
        """更新 agent 状态"""
        state = self._read_state()
        if agent_id in state["agents"]:
            state["agents"][agent_id]["status"] = status
            state["agents"][agent_id]["current_task"] = task_id
            state["agents"][agent_id]["last_heartbeat"] = datetime.now().isoformat()
            
            if status == "completed":
                state["agents"][agent_id]["completed_tasks"] += 1
            elif status == "failed":
                state["agents"][agent_id]["failed_tasks"] += 1
            
            self._write_state(state)
    
    def add_task(self, task_id: str, agent_role: str, command: str, 
                 priority: int = 0, depends_on: list = None):
        """添加任务"""
        state = self._read_state()
        state["tasks"][task_id] = {
            "agent_role": agent_role,
            "command": command,
            "priority": priority,
            "depends_on": depends_on or [],
            "status": "pending",
            "assigned_to": None,
            "result": None,
            "error": None,
            "retries": 0,
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None
        }
        self._write_state(state)
        print(f"[Orchestrator] Task {task_id} added (priority={priority}, role={agent_role})")
    
    def get_next_task(self, agent_id: str) -> Optional[dict]:
        """获取下一个可用任务"""
        state = self._read_state()
        agent = state["agents"].get(agent_id)
        if not agent:
            return None
        
        agent_role = agent["role"]
        completed_tasks = {tid for tid, t in state["tasks"].items() 
                          if t["status"] == "completed"}
        
        # 找到匹配角色、依赖已满足、优先级最高的任务
        candidates = []
        for tid, task in state["tasks"].items():
            if task["status"] != "pending":
                continue
            if task["agent_role"] != agent_role:
                continue
            
            # 检查依赖
            deps_met = all(dep in completed_tasks for dep in task["depends_on"])
            if not deps_met:
                continue
            
            candidates.append((tid, task))
        
        if not candidates:
            return None
        
        # 按优先级排序（高优先级在前）
        candidates.sort(key=lambda x: x[1]["priority"], reverse=True)
        return {"task_id": candidates[0][0], **candidates[0][1]}
    
    def start_task(self, task_id: str, agent_id: str):
        """开始任务"""
        state = self._read_state()
        if task_id in state["tasks"]:
            state["tasks"][task_id]["status"] = "running"
            state["tasks"][task_id]["assigned_to"] = agent_id
            state["tasks"][task_id]["started_at"] = datetime.now().isoformat()
            self._write_state(state)
            print(f"[Orchestrator] Task {task_id} started by {agent_id}")
    
    def complete_task(self, task_id: str, result: str = None):
        """完成任务"""
        state = self._read_state()
        if task_id in state["tasks"]:
            state["tasks"][task_id]["status"] = "completed"
            state["tasks"][task_id]["result"] = result
            state["tasks"][task_id]["completed_at"] = datetime.now().isoformat()
            self._write_state(state)
            print(f"[Orchestrator] Task {task_id} completed")
    
    def fail_task(self, task_id: str, error: str):
        """任务失败"""
        state = self._read_state()
        if task_id in state["tasks"]:
            task = state["tasks"][task_id]
            task["retries"] += 1
            
            if task["retries"] < MAX_RETRIES:
                task["status"] = "pending"  # 重试
                print(f"[Orchestrator] Task {task_id} failed, retry {task['retries']}/{MAX_RETRIES}")
            else:
                task["status"] = "failed"
                task["error"] = error
                print(f"[Orchestrator] Task {task_id} failed permanently: {error}")
            
            task["error"] = error
            self._write_state(state)
    
    def get_status_report(self) -> dict:
        """获取状态报告"""
        state = self._read_state()
        
        agents_summary = {}
        for aid, agent in state["agents"].items():
            agents_summary[aid] = {
                "role": agent["role"],
                "status": agent["status"],
                "current_task": agent["current_task"],
                "completed": agent["completed_tasks"],
                "failed": agent["failed_tasks"]
            }
        
        tasks_summary = {
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0
        }
        for task in state["tasks"].values():
            tasks_summary[task["status"]] += 1
        
        return {
            "agents": agents_summary,
            "tasks": tasks_summary,
            "last_update": state["last_update"]
        }


# ============================================================
# Agent Worker
# ============================================================

class AgentWorker:
    """Agent 工作进程"""
    
    def __init__(self, agent_id: str, role: str, state_manager: StateManager):
        self.agent_id = agent_id
        self.role = role
        self.state = state_manager
        self.running = False
    
    def start(self):
        """启动 agent"""
        self.state.register_agent(self.agent_id, self.role)
        self.running = True
        
        print(f"[{self.agent_id}] Started ({self.role})")
        
        # 心跳线程
        heartbeat_thread = threading.Thread(target=self._heartbeat_loop)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
        
        # 工作循环
        self._work_loop()
    
    def _heartbeat_loop(self):
        """心跳循环"""
        while self.running:
            state = self.state._read_state()
            if self.agent_id in state["agents"]:
                state["agents"][self.agent_id]["last_heartbeat"] = datetime.now().isoformat()
                self.state._write_state(state)
            time.sleep(HEARTBEAT_INTERVAL)
    
    def _work_loop(self):
        """工作循环"""
        while self.running:
            # 获取下一个任务
            task = self.state.get_next_task(self.agent_id)
            
            if task:
                task_id = task["task_id"]
                command = task["command"]
                
                # 开始任务
                self.state.start_task(task_id, self.agent_id)
                self.state.update_agent_status(self.agent_id, "running", task_id)
                
                # 执行命令
                try:
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=300  # 5 分钟超时
                    )
                    
                    if result.returncode == 0:
                        self.state.complete_task(task_id, result.stdout)
                        self.state.update_agent_status(self.agent_id, "completed")
                    else:
                        self.state.fail_task(task_id, result.stderr)
                        self.state.update_agent_status(self.agent_id, "failed")
                
                except subprocess.TimeoutExpired:
                    self.state.fail_task(task_id, "Timeout")
                    self.state.update_agent_status(self.agent_id, "failed")
                except Exception as e:
                    self.state.fail_task(task_id, str(e))
                    self.state.update_agent_status(self.agent_id, "failed")
            else:
                # 没有任务，等待
                self.state.update_agent_status(self.agent_id, "idle")
                time.sleep(5)
    
    def stop(self):
        """停止 agent"""
        self.running = False
        print(f"[{self.agent_id}] Stopped")


# ============================================================
# Orchestrator（主进程）
# ============================================================

class Orchestrator:
    """编排器主进程"""
    
    def __init__(self):
        self.state = StateManager(STATE_FILE, LOCK_FILE)
        self.workers = []
    
    def add_task(self, task_id: str, agent_role: str, command: str,
                 priority: int = 0, depends_on: list = None):
        """添加任务"""
        self.state.add_task(task_id, agent_role, command, priority, depends_on)
    
    def spawn_agent(self, agent_id: str, role: str):
        """启动 agent"""
        worker = AgentWorker(agent_id, role, self.state)
        thread = threading.Thread(target=worker.start)
        thread.daemon = True
        thread.start()
        self.workers.append(worker)
        return worker
    
    def status(self) -> dict:
        """获取状态"""
        return self.state.get_status_report()
    
    def print_status(self):
        """打印状态"""
        report = self.status()
        
        print("\n" + "="*60)
        print("  AGENTS")
        print("="*60)
        for aid, info in report["agents"].items():
            print(f"  {aid} ({info['role']}): {info['status']}")
            if info['current_task']:
                print(f"    → Task: {info['current_task']}")
            print(f"    ✓ Completed: {info['completed']}  ✗ Failed: {info['failed']}")
        
        print("\n" + "="*60)
        print("  TASKS")
        print("="*60)
        for status, count in report["tasks"].items():
            print(f"  {status}: {count}")
        
        print(f"\n  Last update: {report['last_update']}")
        print("="*60 + "\n")


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-Agent Orchestrator")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--add-task", nargs=4, metavar=("TASK_ID", "ROLE", "COMMAND", "PRIORITY"),
                       help="Add a task")
    
    args = parser.parse_args()
    
    orchestrator = Orchestrator()
    
    if args.demo:
        # Demo：启动 3 个 agents，添加 5 个任务
        print("Starting demo...")
        
        # 启动 agents
        orchestrator.spawn_agent("pm-1", "pm")
        orchestrator.spawn_agent("dev-1", "dev")
        orchestrator.spawn_agent("qa-1", "qa")
        
        # 添加任务（带依赖）
        orchestrator.add_task("task-1", "pm", 'echo "Writing spec..."', priority=10)
        orchestrator.add_task("task-2", "dev", 'echo "Implementing feature..."', 
                            priority=8, depends_on=["task-1"])
        orchestrator.add_task("task-3", "qa", 'echo "Writing tests..."', 
                            priority=5, depends_on=["task-1"])
        orchestrator.add_task("task-4", "dev", 'echo "Refactoring..."', 
                            priority=3, depends_on=["task-2"])
        orchestrator.add_task("task-5", "qa", 'echo "Final testing..."', 
                            priority=1, depends_on=["task-3", "task-4"])
        
        # 运行 30 秒
        for i in range(6):
            time.sleep(5)
            orchestrator.print_status()
        
        print("Demo complete!")
    
    elif args.status:
        orchestrator.print_status()
    
    elif args.add_task:
        task_id, role, command, priority = args.add_task
        orchestrator.add_task(task_id, role, command, int(priority))
        print(f"Task {task_id} added")
