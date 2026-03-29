# 18 - Create Custom Subagents 学习笔记

**学习时间**：2026-03-14 15:10
**页面地址**：https://code.claude.com/docs/en/sub-agents

---

## 📖 核心概念

### 是什么
**Subagents** 是专业化 AI 助手，在独立上下文窗口中运行，处理特定类型的任务。

### 为什么用 Subagents
- **Preserve context** - 保持探索和实现远离主对话
- **Enforce constraints** - 限制工具访问
- **Reuse configurations** - 跨项目复用
- **Specialize behavior** - 针对特定领域的系统提示
- **Control costs** - 路由任务到更快、更便宜的模型（如 Haiku）

### Built-in Subagents

**Explore**:
- Model: Haiku（快速、低延迟）
- Tools: 只读工具（无 Write/Edit）
- Purpose: 文件发现、代码搜索、代码库探索

**Plan**:
- 创建详细实施计划

**General-purpose**:
- 通用助手

---

## 🚀 Quickstart: Create Your First Subagent

### 步骤

**1. Open the subagents interface**
```bash
/agents
```

**2. Create a new user-level agent**
- Select "Create new agent" → "User-level"
- Saves to `~/.claude/agents/`

**3. Generate with Claude**
```bash
A code improvement agent that scans files and suggests improvements for readability, performance, and best practices. It should explain each issue, show the current code, and provide an improved version.
```

**4. Select tools**
- For read-only reviewer: deselect all except "Read-only tools"

**5. Select model**
- Sonnet: 平衡能力和速度
- Opus: 最强推理
- Haiku: 最快、最便宜

**6. Choose a color**
- Background color to identify subagent in UI

**7. Save and try it out**
```bash
Use the code-improver agent to suggest improvements in this project
```

---

## ⚙️ Configure Subagents

### Choose the Subagent Scope

| Location | Scope | Priority | How to create |
|----------|-------|----------|---------------|
| `--agents` CLI flag | Current session | 1 (highest) | Pass JSON when launching |
| `.claude/agents/` | Current project | 2 | Interactive or manual |
| `~/.claude/agents/` | All your projects | 3 | Interactive or manual |
| Plugin's `agents/` | Where plugin enabled | 4 (lowest) | Installed with plugins |

### Write Subagent Files

**Markdown with YAML frontmatter**:
```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide specific, actionable feedback on quality, security, and best practices.
```

---

## 🔧 Supported Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase letters and hyphens) |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | Tools the subagent can use (inherits all if omitted) |
| `disallowedTools` | No | Tools to deny |
| `model` | No | `sonnet`, `opus`, `haiku`, full model ID, or `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | Maximum agentic turns |
| `skills` | No | Skills to preload |
| `mcpServers` | No | MCP servers available to subagent |
| `hooks` | No | Lifecycle hooks scoped to subagent |
| `memory` | No | Persistent memory scope: `user`, `project`, `local` |
| `background` | No | Run as background task (default: false) |
| `isolation` | No | `worktree` to run in isolated git worktree |

---

## 🎯 Control Subagent Capabilities

### Available Tools
- **Allowlist**: `tools: Read, Grep, Glob, Bash`
- **Denylist**: `disallowedTools: Write, Edit`

### Restrict Subagent Spawning
```yaml
# Only allow worker and researcher subagents
tools: Agent(worker, researcher), Read, Bash
```

### Scope MCP Servers
```yaml
mcpServers:
  # Inline definition
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name
  - github
```

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Standard permission checking with prompts |
| `acceptEdits` | Auto-accept file edits |
| `dontAsk` | Auto-deny permission prompts |
| `bypassPermissions` | Skip all permission checks |
| `plan` | Plan mode (read-only exploration) |

### Preload Skills
```yaml
skills:
  - api-conventions
  - error-handling-patterns
```

### Enable Persistent Memory
```yaml
memory: user  # or project, local
```

**Scope locations**:
- `user`: `~/.claude/agent-memory/<name>/` (across all projects)
- `project`: `.claude/agent-memory/<name>/` (project-specific, shareable)
- `local`: `.claude/agent-memory-local/<name>/` (project-specific, not in VCS)

---

## 🎣 Define Hooks for Subagents

### Hooks in Frontmatter
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
```

### Project-Level Hooks
```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/setup-db-connection.sh"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/cleanup-db-connection.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 💡 Work with Subagents

### Automatic Delegation
Claude 自动委托基于：
- 任务描述
- Subagent description field
- 当前上下文

**Explicit request**:
```bash
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

### Foreground vs Background

**Foreground (blocking)**:
- 阻塞主对话直到完成
- Permission prompts 传递给你
- Clarifying questions 传递给你

**Background (concurrent)**:
- 并发运行，你可继续工作
- 预先批准权限
- Auto-denies 未预批准的请求
- Clarifying questions 失败但继续运行

**Ctrl+B** - background a running task

### Common Patterns

**Isolate high-volume operations**:
```bash
Use a subagent to run the test suite and report only the failing tests
```

**Run parallel research**:
```bash
Research the authentication, database, and API modules in parallel using separate subagents
```

**Chain subagents**:
```bash
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Resume Subagents
```bash
# First invocation
Use the code-reviewer subagent to review the authentication module

# Resume
Continue that code review and now analyze the authorization logic
```

---

## 📚 Example Subagents

### Code Reviewer
```yaml
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger
```yaml
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Database Query Validator
```yaml
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

**Validation script**:
```bash
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

---

## 💡 学习感悟

### 1. **Subagent 的核心价值**
**上下文隔离** - 最大的价值：
- 高容量操作（测试、日志）不会污染主对话
- 只返回摘要给主对话

这是"分而治之"策略。

### 2. **Tool Restrictions 的精细化**
**两级控制**：
- **Allowlist** (`tools`) - 只允许特定工具
- **Denylist** (`disallowedTools`) - 排除特定工具

**Hooks for conditional validation**:
- `PreToolUse` hooks 可以基于内容决定是否允许
- 例如：只读 SQL 查询验证

这是"最小权限原则"的实现。

### 3. **Persistent Memory 的威力**
**跨会话学习**：
- `memory: user` - 跨所有项目
- `memory: project` - 项目特定
- `memory: local` - 项目特定但不进入 VCS

**让 subagent 越用越聪明**。

### 4. **Foreground vs Background 的智能**
**Foreground**: 需要交互（permission prompts, clarifying questions）
**Background**: 预先批准权限，独立运行

**Ctrl+B 随时切换**。

### 5. **Resume Subagents 的连续性**
**Subagent transcripts 独立持久化**：
- 主对话压缩不影响 subagent transcripts
- 可以恢复 subagent 继续工作
- 保留完整历史

**这实现了"会话连续性"**。

### 6. **Subagents vs Skills vs Agent Teams**

| Feature | Subagents | Skills | Agent Teams |
|---------|-----------|--------|-------------|
| **Context** | Isolated | Main conversation | Separate sessions |
| **Can spawn others** | No | Can invoke subagents | Yes (P2P communication) |
| **Best for** | Isolate verbose output | Reusable prompts in main context | Parallel work, sustained |

---

## 🎯 实践建议

### 1. **创建 Read-Only Code Reviewer**
```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Proactively reviews code for quality, security, and maintainability
tools: Read, Grep, Glob, Bash
model: sonnet
memory: user
---
```

### 2. **创建 Debugger with Edit Access**
```yaml
# .claude/agents/debugger.md
---
name: debugger
description: Debugging specialist for errors and test failures
tools: Read, Edit, Bash, Grep, Glob
model: sonnet
---
```

### 3. **使用 PreToolUse Hooks 限制操作**
```yaml
# Only allow SELECT queries
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
```

### 4. **用 Background Subagents 并行工作**
```bash
# 启动多个 subagents
Research the authentication, database, and API modules in parallel
```

### 5. **Resume Subagents 继续工作**
```bash
# First
Use the code-reviewer subagent to review the auth module

# Resume
Continue that code review and now analyze the authorization logic
```

### 6. **监控 Auto-Compaction**
```bash
# Check transcript files
~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl

# Look for compaction events
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

---

## 📚 与 OpenClaw 的对比

### 相似之处
1. **Isolation** - 都支持隔离上下文
2. **Tool restrictions** - 都支持工具限制
3. **Hooks** - 都支持生命周期 hooks

### 差异之处
1. **Subagents** - Claude Code 有明确的 subagent 概念，OpenClaw 没有
2. **Persistent memory** - Claude Code subagents 可以有持久记忆，OpenClaw 没有
3. **Background tasks** - Claude Code 支持 background subagents，OpenClaw 没有
4. **Transcript persistence** - Claude Code subagent transcripts 独立持久化，OpenClaw 没有

### 可以借鉴
1. **Subagent System** - 专业化 agents 系统
2. **Persistent Memory** - 跨会话学习
3. **Background Tasks** - 后台任务
4. **Resume Mechanism** - 恢复机制
5. **Tool Restrictions** - 精细化工具控制

---

## 🏷️ 标签
`#subagents` `#isolation` `#tool-restrictions` `#persistent-memory` `#hooks` `#foreground-background`
