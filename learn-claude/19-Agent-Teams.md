# 19 - Agent Teams 学习笔记

**学习时间**：2026-03-14 15:25
**页面地址**：https://code.claude.com/docs/en/agent-teams

---

## 📖 核心概念

### 是什么
**Agent Teams** 协调多个 Claude Code 实例作为团队工作，有共享任务列表、agent 间消息传递和集中管理。

### 实验性功能
- **默认禁用**
- 需要 v2.1.32+
- 有已知限制（会话恢复、任务协调、关闭行为）

### vs Subagents

| 方面 | Subagents | Agent Teams |
|------|-----------|-------------|
| **Context** | Own context window; results return to caller | Own context window; fully independent |
| **Communication** | Report results back to main agent only | Teammates message each other directly |
| **Coordination** | Main agent manages all work | Shared task list with self-coordination |
| **Best for** | Focused tasks where only result matters | Complex work requiring discussion and collaboration |
| **Token cost** | Lower: results summarized back | Higher: each teammate is separate Claude instance |

**关键差异**：Teammates 可以**直接互相通信**，不需要通过 lead。

---

## 🎯 When to Use

### Best Use Cases
- **Research and review** - 多角度同时调查
- **New modules or features** - 各自拥有独立部分
- **Debugging with competing hypotheses** - 并行测试不同理论
- **Cross-layer coordination** - frontend/backend/tests 各有不同 teammate

### NOT Good For
- Sequential tasks
- Same-file edits
- Work with many dependencies

**Use single session or subagents instead**.

---

## 🚀 Enable Agent Teams

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## 🏗️ Architecture

### Components

| Component | Role |
|-----------|------|
| **Team lead** | Main Claude Code session, creates team, spawns teammates, coordinates work |
| **Teammates** | Separate Claude Code instances, work on assigned tasks |
| **Task list** | Shared list of work items, teammates claim and complete |
| **Mailbox** | Messaging system for inter-agent communication |

### Storage
- **Team config**: `~/.claude/teams/{team-name}/config.json`
- **Task list**: `~/.claude/tasks/{team-name}/`

---

## 💡 Start Your First Agent Team

### Natural Language Prompt
```bash
I'm designing a CLI tool that helps developers track TODO comments across their codebase. Create an agent team to explore this from different angles: one teammate on UX, one on technical architecture, one playing devil's advocate.
```

Claude 会：
1. 创建带 shared task list 的团队
2. 为每个视角 spawn teammates
3. 让他们探索问题
4. 综合发现
5. 完成后清理团队

---

## 🎮 Control Your Agent Team

### Display Modes

**In-process**（默认）:
- 所有 teammates 运行在主终端
- `Shift+Down` 循环 teammates
- 任何终端可用

**Split panes**:
- 每个 teammate 有自己的 pane
- 可同时看到所有输出
- 点击 pane 直接交互
- Requires tmux or iTerm2

```json
// settings.json
{
  "teammateMode": "in-process"  // or "tmux"
}
```

**Flag**:
```bash
claude --teammate-mode in-process
```

### Specify Teammates and Models
```bash
Create a team with 4 teammates to refactor these modules in parallel. Use Sonnet for each teammate.
```

### Require Plan Approval
```bash
Spawn an architect teammate to refactor the authentication module. Require plan approval before they make any changes.
```

**Flow**:
1. Teammate plans (read-only)
2. Sends plan approval request to lead
3. Lead reviews and approves/rejects
4. If approved → teammate exits plan mode and implements
5. If rejected → teammate revises and resubmits

### Talk to Teammates Directly

**In-process mode**:
- `Shift+Down` - cycle through teammates
- Type to send message
- `Enter` - view teammate's session
- `Escape` - interrupt current turn
- `Ctrl+T` - toggle task list

**Split-pane mode**:
- Click into teammate's pane

### Assign and Claim Tasks

**Lead assigns**: tell lead which task to give to which teammate
**Self-claim**: teammate picks up next unassigned, unblocked task

**Task states**: pending, in progress, completed
**Task dependencies**: pending task with unresolved dependencies cannot be claimed

### Shut Down Teammates
```bash
Ask the researcher teammate to shut down
```

Teammate can approve (exit gracefully) or reject with explanation.

### Clean Up the Team
```bash
Clean up the team
```

Removes shared team resources. Fails if teammates still running.

### Enforce Quality Gates with Hooks

**TeammateIdle**: runs when teammate about to go idle. Exit code 2 to send feedback and keep working.
**TaskCompleted**: runs when task being marked complete. Exit code 2 to prevent completion and send feedback.

---

## 🔄 How Agent Teams Work

### Starting Mechanisms

**You request a team**: explicitly ask for agent team
**Claude proposes a team**: if Claude determines task benefits from parallel work

**Claude won't create team without your approval**.

### Context and Communication

**Teammate context**:
- Loads same project context as regular session (CLAUDE.md, MCP servers, skills)
- Receives spawn prompt from lead
- **Lead's conversation history does not carry over**

**Information sharing**:
- **Automatic message delivery**: messages delivered automatically
- **Idle notifications**: teammate notifies lead when finished
- **Shared task list**: all agents see task status

**Teammate messaging**:
- **message**: send to one specific teammate
- **broadcast**: send to all teammates (use sparingly, costs scale)

### Token Usage

**Significantly more tokens than single session**:
- Each teammate has own context window
- Token usage scales with number of active teammates

**Worthwhile for**: research, review, new feature work
**NOT cost-effective for**: routine tasks

---

## 📚 Use Case Examples

### Parallel Code Review
```bash
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage

Have them each review and report findings.
```

Each reviewer applies different filter. Lead synthesizes findings.

### Competing Hypotheses Investigation
```bash
Users report the app exits after one message instead of staying connected. Spawn 5 agent teammates to investigate different hypotheses. Have them talk to each other to try to disprove each other's theories, like a scientific debate. Update the findings doc with whatever consensus emerges.
```

**Debate structure is key**: sequential investigation suffers from anchoring. Multiple independent investigators actively disproving each other → theory that survives is more likely actual root cause.

---

## 🎯 Best Practices

### Give Teammates Enough Context
```bash
Spawn a security reviewer teammate with the prompt: "Review the authentication module at src/auth/ for security vulnerabilities. Focus on token handling, session management, and input validation. The app uses JWT tokens stored in httpOnly cookies. Report any issues with severity ratings."
```

### Choose Appropriate Team Size

**Constraints**:
- Token costs scale linearly
- Coordination overhead increases
- Diminishing returns

**Recommendation**:
- **Start with 3-5 teammates** for most workflows
- **5-6 tasks per teammate** keeps everyone productive
- 15 independent tasks → 3 teammates good starting point

**3 focused teammates often outperform 5 scattered ones**.

### Size Tasks Appropriately

- **Too small**: coordination overhead exceeds benefit
- **Too large**: teammates work too long without check-ins
- **Just right**: self-contained units producing clear deliverable

### Wait for Teammates to Finish
```bash
Wait for your teammates to complete their tasks before proceeding
```

Lead sometimes starts implementing instead of waiting.

### Start with Research and Review

New to agent teams → start with tasks with clear boundaries and don't require writing code:
- Reviewing PR
- Researching library
- Investigating bug

### Avoid File Conflicts

Two teammates editing same file → overwrites. Break work so each teammate owns different files.

### Monitor and Steer

Check progress, redirect approaches not working, synthesize findings. Unattended teams increase wasted effort risk.

---

## 🛠️ Troubleshooting

### Teammates Not Appearing
- In-process: press `Shift+Down` to cycle
- Check task complexity
- Split panes: `which tmux` or iTerm2 it2 CLI

### Too Many Permission Prompts
Pre-approve common operations in permission settings.

### Teammates Stopping on Errors
- Check output (Shift+Down or click pane)
- Give additional instructions
- Spawn replacement teammate

### Lead Shuts Down Before Work Done
Tell it to keep going. Tell lead to wait for teammates.

### Orphaned tmux Sessions
```bash
tmux ls
tmux kill-session -t <session-name>
```

---

## ⚠️ Limitations

**Experimental, current limitations**:

1. **No session resumption with in-process teammates**: `/resume` and `/rewind` do not restore in-process teammates
2. **Task status can lag**: teammates sometimes fail to mark tasks completed
3. **Shutdown can be slow**: teammates finish current request/tool call before shutting down
4. **One team per session**: lead can only manage one team at a time
5. **No nested teams**: teammates cannot spawn their own teams
6. **Lead is fixed**: can't promote teammate to lead or transfer leadership
7. **Permissions set at spawn**: all teammates start with lead's permission mode
8. **Split panes require tmux or iTerm2**: NOT supported in VS Code integrated terminal, Windows Terminal, Ghostty

**CLAUDE.md works normally**: teammates read CLAUDE.md files from working directory.

---

## 💡 学习感悟

### 1. **P2P Communication 的突破**
**Agent Teams 的核心价值**：
- Teammates **直接互相通信**（不需要通过 lead）
- Shared task list with **self-coordination**
- Lead 不需要轮询更新（automatic message delivery）

**这是真正的多 Agent 协作**，而不是 hierarchical delegation。

### 2. **Display Modes 的灵活性**
**In-process vs Split panes**:
- **In-process**: 任何终端可用，简单
- **Split panes**: 可视化所有 teammates，但需要 tmux/iTerm2

**选择取决于场景**。

### 3. **Plan Approval 的安全机制**
**Require plan approval for teammates**:
- Teammate 先 plan（read-only）
- Lead 审查并批准/拒绝
- 批准后才实施

**这是"Trust but Verify"原则**。

### 4. **Competing Hypotheses 的科学方法**
**Investigation with competing hypotheses**:
- 5 个 teammates 各自调查不同假设
- 互相挑战，像科学辩论
- 共识更新到 findings doc

**这是"科学方法"的 AI Agent 版本**。

### 5. **Token Cost 的权衡**
**Agent teams use significantly more tokens**:
- Each teammate = separate Claude instance
- Token usage scales linearly with team size

**权衡**：并行加速 vs Token 成本。

### 6. **Experimental Status 的现实**
**Known limitations**:
- No session resumption with in-process teammates
- Task status can lag
- One team per session
- No nested teams

**这是实验性功能，生产使用需谨慎**。

---

## 🎯 实践建议

### 1. **Start with Research and Review**
```bash
# New to agent teams
Create an agent team to review this PR from security, performance, and test coverage perspectives.
```

### 2. **Use 3-5 Teammates**
```bash
# Optimal team size
Create a team with 4 teammates to investigate this bug from different angles.
```

### 3. **Require Plan Approval for Complex Tasks**
```bash
# Safety mechanism
Spawn an architect teammate to refactor the auth module. Require plan approval before implementation.
```

### 4. **Size Tasks Appropriately**
- 5-6 tasks per teammate
- Self-contained units
- Clear deliverables

### 5. **Monitor and Steer**
- Check progress regularly
- Redirect approaches not working
- Synthesize findings as they come in

### 6. **Use Hooks for Quality Gates**
```json
{
  "hooks": {
    "TeammateIdle": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/check-quality.sh"
          }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/verify-task.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 📚 与 Subagents 的对比总结

### Subagents
- **Context**: Isolated, results return to caller
- **Communication**: Only to main agent
- **Coordination**: Main agent manages
- **Best for**: Focused tasks, only result matters
- **Token cost**: Lower

### Agent Teams
- **Context**: Independent, separate sessions
- **Communication**: P2P between teammates
- **Coordination**: Self-coordinating via shared task list
- **Best for**: Complex work needing discussion/collaboration
- **Token cost**: Higher

**选择标准**：Teammates need to communicate with each other?

---

## 🏷️ 标签
`#agent-teams` `#multi-agent` `#p2p-communication` `#parallel-work` `#experimental` `#coordination`
