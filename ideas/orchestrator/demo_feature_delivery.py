#!/usr/bin/env python3
"""
Orchestrator Demo - 40 人团队场景示例

场景：
- 产品经理（PM）：写需求文档、验收标准
- 开发（Dev）：实现功能、代码重构
- 测试（QA）：写测试用例、执行测试

依赖关系：
  PM 任务 → Dev 任务 + QA 任务 → 最终验收
"""

import sys
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator import Orchestrator
import time


def demo_feature_delivery():
    """演示一个完整的 feature 交付流程"""
    
    orchestrator = Orchestrator()
    
    print("="*60)
    print("  Agent-Agile Feature Delivery Demo")
    print("  场景：实现「用户登录」功能")
    print("="*60 + "\n")
    
    # 1. 启动 agents
    print(">>> 启动 Agents...")
    orchestrator.spawn_agent("pm-steven", "pm")
    orchestrator.spawn_agent("dev-1", "dev")
    orchestrator.spawn_agent("dev-2", "dev")
    orchestrator.spawn_agent("qa-1", "qa")
    
    time.sleep(2)
    
    # 2. 添加任务（DAG 依赖）
    print("\n>>> 添加任务...")
    
    # Phase 1: PM 活儿
    orchestrator.add_task(
        task_id="spec-login",
        agent_role="pm",
        command='echo "✍️ 写需求文档：用户登录流程" && sleep 3',
        priority=10
    )
    
    orchestrator.add_task(
        task_id="acceptance-criteria",
        agent_role="pm",
        command='echo "✍️ 写验收标准：登录成功/失败场景" && sleep 2',
        priority=9,
        depends_on=["spec-login"]
    )
    
    # Phase 2: Dev 并行开发
    orchestrator.add_task(
        task_id="dev-frontend",
        agent_role="dev",
        command='echo "💻 前端：实现登录表单 UI" && sleep 4',
        priority=8,
        depends_on=["spec-login"]
    )
    
    orchestrator.add_task(
        task_id="dev-backend",
        agent_role="dev",
        command='echo "💻 后端：实现认证 API" && sleep 5',
        priority=8,
        depends_on=["spec-login"]
    )
    
    orchestrator.add_task(
        task_id="dev-integration",
        agent_role="dev",
        command='echo "💻 集成：前后端联调" && sleep 3',
        priority=7,
        depends_on=["dev-frontend", "dev-backend"]
    )
    
    # Phase 3: QA 测试
    orchestrator.add_task(
        task_id="qa-testcases",
        agent_role="qa",
        command='echo "🧪 写测试用例：覆盖所有场景" && sleep 3',
        priority=6,
        depends_on=["acceptance-criteria"]
    )
    
    orchestrator.add_task(
        task_id="qa-automation",
        agent_role="qa",
        command='echo "🧪 自动化测试：Selenium 跑一遍" && sleep 4',
        priority=5,
        depends_on=["qa-testcases", "dev-integration"]
    )
    
    orchestrator.add_task(
        task_id="qa-final",
        agent_role="qa",
        command='echo "✅ 最终验收：所有测试通过" && sleep 2',
        priority=4,
        depends_on=["qa-automation"]
    )
    
    # 3. 监控进度
    print("\n>>> 开始执行...\n")
    
    for i in range(20):
        time.sleep(2)
        report = orchestrator.status()
        
        # 清屏 + 打印状态
        print("\033[2J\033[H")  # ANSI clear screen
        print("="*60)
        print(f"  Agent-Agile 进度 [{i*2}s]")
        print("="*60)
        
        for aid, info in report["agents"].items():
            status_emoji = {
                "idle": "😴",
                "running": "🔄",
                "completed": "✅",
                "failed": "❌"
            }.get(info["status"], "❓")
            
            print(f"{status_emoji} {aid} ({info['role']}): {info['status']}")
            if info["current_task"]:
                print(f"   → {info['current_task']}")
        
        print("\n" + "-"*60)
        print(f"Tasks: {report['tasks']}")
        print("-"*60)
        
        # 检查是否全部完成
        if report["tasks"]["pending"] == 0 and report["tasks"]["running"] == 0:
            print("\n🎉 所有任务完成！")
            break
    
    print("\n" + "="*60)
    print("  Final Report")
    print("="*60)
    orchestrator.print_status()


if __name__ == "__main__":
    demo_feature_delivery()
