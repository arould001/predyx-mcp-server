# OpenClaw + Codex/Claude Code Agent Swarm 架构

> 来源: https://x.com/elvissun/status/2025920521871716562
> 作者: Elvis (@elvissun)
> 时间: 2026-02-23

## 核心架构

```
OpenClaw (Zoe) = Orchestration Layer
    ├── 持有所有业务上下文（会议记录、客户历史、过去决策）
    ├── 写 prompts 给 coding agents
    ├── 监控进度（cron 每 10 分钟检查）
    └── 通知 Telegram

Codex/Claude Code = Execution Layer
    ├── 只看代码
    ├── 每个 agent 有独立的 worktree + tmux session
    └── 专注执行，不关心业务上下文
```

## 关键数据

- **94 commits/day** 最高纪录
- **7 PRs in 30 mins** 从想法到上线
- **平均 50 commits/day**
- **成本**: ~$100/month Claude + $90/month Codex
- **186 万次浏览**

## 为什么需要两层？

**Context window 是零和的：**
- 填满代码 → 没空间放业务上下文
- 填满客户历史 → 没空间放代码库

## 8 步工作流

1. **客户请求 → Zoe scope**（自动从 Obsidian 读取会议记录）
2. **Spawn Agent**（git worktree + tmux session）
3. **Monitor Loop**（cron 每 10 分钟检查 tmux 状态、PR、CI）
4. **Agent 创建 PR**
5. **3 个 AI Reviewer**（Codex + Gemini + Claude Code）
6. **自动测试**（lint, unit, E2E, Playwright）
7. **Human Review**（Telegram 通知）
8. **Merge**

## Ralph Loop V2

失败时 Zoe 会根据业务上下文调整 prompt：
- "这个客户想要 X，不是 Y"
- "只关注这三个文件"

## Agent 选择策略

| Agent | 擅长 | 用途 |
|-------|------|------|
| **Codex** | 后端逻辑、复杂 bug、多文件重构 | 90% 任务 |
| **Claude Code** | 前端、git 操作 | 快速任务 |
| **Gemini** | 设计感强 | 生成 UI spec |

## 瓶颈

**RAM** - 每个 agent 需要独立的 worktree + node_modules：
- 16GB 最多 4-5 agents
- Mac Studio M4 Max 128GB ($3,500)

## 金句

> "I don't use Codex or Claude Code directly anymore."

> "My git history looks like I just hired a dev team."

## 对我们的启发

这和 "让 Dia 更真实" 的方向完全一致：
- Orchestrator 层持有上下文
- Spawn 专门的 agents 去执行
- 监控、重试、通知自动化

我们可以学习他的：
1. Task registry (active-tasks.json)
2. Monitor loop (cron + tmux 检查)
3. Definition of Done (CI + 3 reviewers + screenshots)
4. 失败时调整 prompt（而不是简单重试）
