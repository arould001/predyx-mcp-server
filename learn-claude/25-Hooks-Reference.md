# 25 - Hooks Reference 学习笔记

**学习时间**：2026-03-14 17:05
**页面地址**：https://code.claude.com/docs/en/hooks

---

## 📖 核心概念

### 是什么
**Hooks** 是用户定义的 shell commands, HTTP endpoints, 或 LLM prompts，在 Claude Code 生命周期的特定点自动执行。

### Hook Lifecycle
**Hooks fire at specific points** during Claude Code session:
1. **Event fires** → Claude Code passes JSON context to hook handler
2. **Matcher checks** → Regex filter determines if hook runs
3. **Hook handler runs** → Command/HTTP/Prompt/Agent executes
4. **Claude Code acts** → Processes result (allow/block/modify)

### For Quickstart
**See** "Automate workflows with hooks" guide.

This is the **reference documentation** → look up event schemas, configuration options, JSON formats, advanced features.

---

## 📋 Hook Events Summary

| Event | When it Fires | Can Block? |
|-------|---------------|------------|
| **SessionStart** | Session begins or resumes | No |
| **UserPromptSubmit** | User submits prompt, before Claude processes | Yes |
| **PreToolUse** | Before tool call executes | Yes |
| **PermissionRequest** | Permission dialog appears | Yes |
| **PostToolUse** | After tool call succeeds | No (feedback only) |
| **PostToolUseFailure** | After tool call fails | No (feedback only) |
| **Notification** | Claude Code sends notification | No |
| **SubagentStart** | Subagent is spawned | No |
| **SubagentStop** | Subagent finishes | Yes |
| **Stop** | Claude finishes responding | Yes |
| **TeammateIdle** | Agent team teammate about to go idle | Yes |
| **TaskCompleted** | Task being marked as completed | Yes |
| **InstructionsLoaded** | CLAUDE.md or .claude/rules/*.md loaded | No |
| **ConfigChange** | Configuration file changes during session | Yes (except policy_settings) |
| **WorktreeCreate** | Worktree being created | Yes (via exit code) |
| **WorktreeRemove** | Worktree being removed | No |
| **PreCompact** | Before context compaction | No |
| **PostCompact** | After context compaction completes | No |
| **Elicitation** | MCP server requests user input | Yes |
| **ElicitationResult** | After user responds to MCP elicitation | Yes |
| **SessionEnd** | Session terminates | No |

---

## ⚙️ Configuration

### Three Levels of Nesting
1. **Hook event** → Choose lifecycle point (e.g., `PreToolUse`, `Stop`)
2. **Matcher group** → Filter when it fires (e.g., `"Bash"`)
3. **Hook handlers** → Define what runs (command/HTTP/prompt/agent)

### Example Structure
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

### Hook Locations

| Location | Scope | Shareable |
|----------|-------|-----------|
| `~/.claude/settings.json` | All your projects | No (local to machine) |
| `.claude/settings.json` | Single project | Yes (commit to repo) |
| `.claude/settings.local.json` | Single project | No (gitignored) |
| **Managed policy settings** | Organization-wide | Yes (admin-controlled) |
| **Plugin hooks/hooks.json** | When plugin enabled | Yes (bundled with plugin) |
| **Skill or agent frontmatter** | While component active | Yes (in component file) |

**Enterprise admins** can use `allowManagedHooksOnly` to block user/project/plugin hooks.

---

## 🎯 Matcher Patterns

### What Matcher Filters
**Regex string** that filters when hooks fire.

| Event | What matcher filters | Example values |
|-------|---------------------|----------------|
| **PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest** | tool name | `Bash`, `Edit|Write`, `mcp__.*` |
| **SessionStart** | how session started | `startup`, `resume`, `clear`, `compact` |
| **SessionEnd** | why session ended | `clear`, `logout`, `prompt_input_exit`, ... |
| **Notification** | notification type | `permission_prompt`, `idle_prompt`, `auth_success`, ... |
| **SubagentStart** | agent type | `Bash`, `Explore`, `Plan`, or custom names |
| **PreCompact** | what triggered compaction | `manual`, `auto` |
| **SubagentStop** | agent type | Same as SubagentStart |
| **ConfigChange** | configuration source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |

**No matcher support**:
- UserPromptSubmit
- Stop
- TeammateIdle
- TaskCompleted
- WorktreeCreate
- WorktreeRemove
- InstructionsLoaded

### Matcher Syntax
**Regex patterns**:
- `*` or `""` or omit → match all occurrences
- `Edit|Write` → match either
- `Notebook.*` → match any tool starting with "Notebook"
- `mcp__.*` → match all MCP tools

### Match MCP Tools
**MCP tool naming**: `mcp__<server>__<tool>`

**Examples**:
- `mcp__memory__create_entities`
- `mcp__filesystem__read_file`
- `mcp__github__search_repositories`

**Patterns**:
- `mcp__memory__.*` → all tools from memory server
- `mcp__.*__write.*` → any tool containing "write" from any server

---

## 🔧 Hook Handler Fields

### Four Types
1. **Command hooks** (`type: "command"`) → run shell command
2. **HTTP hooks** (`type: "http"`) → send POST request
3. **Prompt hooks** (`type: "prompt"`) → send to Claude model
4. **Agent hooks** (`type: "agent"`) → spawn subagent with tool access

### Common Fields (All Types)

| Field | Required | Description |
|-------|----------|-------------|
| `type` | yes | `"command"`, `"http"`, `"prompt"`, or `"agent"` |
| `timeout` | no | Seconds before canceling. Defaults: 600 (command), 30 (prompt), 60 (agent) |
| `statusMessage` | no | Custom spinner message while hook runs |
| `once` | no | If true, runs only once per session then removed. Skills only |

### Command Hook Fields

| Field | Required | Description |
|-------|----------|-------------|
| `command` | yes | Shell command to execute |
| `async` | no | If true, runs in background without blocking |

### HTTP Hook Fields

| Field | Required | Description |
|-------|----------|-------------|
| `url` | yes | URL to send POST request to |
| `headers` | no | Additional HTTP headers (key-value pairs). Supports env var interpolation `$VAR_NAME` or `${VAR_NAME}` |
| `allowedEnvVars` | no | List of env var names that may be interpolated into headers. Required for any interpolation to work |

**Error handling**: Non-2xx, connection failures, timeouts → non-blocking errors (execution continues).

**To block**: Return 2xx with JSON body containing decision.

### Prompt/Agent Hook Fields

| Field | Required | Description |
|-------|----------|-------------|
| `prompt` | yes | Prompt text. Use `$ARGUMENTS` as placeholder for hook input JSON |
| `model` | no | Model to use. Defaults to fast model |

---

## 🔑 Reference Scripts by Path

### Environment Variables
- `$CLAUDE_PROJECT_DIR` → project root (wrap in quotes for spaces)
- `${CLAUDE_PLUGIN_ROOT}` → plugin's root directory

### Example
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 🎓 Hooks in Skills and Agents

### Frontmatter Syntax
**Hooks can be defined directly in skills/agents using frontmatter**.

**Skill example**:
```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

**Scoped to component's lifecycle** → cleaned up when component finishes.

**Subagents**: Stop hooks automatically converted to SubagentStop.

---

## 📋 /hooks Menu

### Interactive Browser
**Type `/hooks`** → open read-only browser for configured hooks.

**Shows**:
- Every hook event with count of configured hooks
- Drill into matchers
- Full details of each handler
- Type prefix: `[command]`, `[prompt]`, `[agent]`, `[http]`
- Source label: `[User]`, `[Project]`, `[Local]`, `[Plugin]`, `[Session]`, `[Built-in]`

**Read-only** → edit settings JSON to modify.

---

## 🚫 Disable or Remove Hooks

### Remove
**Delete entry from settings JSON**.

### Disable All
**Set `"disableAllHooks": true`** in settings file.

**Hierarchy**:
- User/project/local `disableAllHooks` **cannot** disable managed hooks
- Only managed settings level can disable managed hooks

### Snapshot at Startup
**Claude Code captures hooks snapshot at startup** → prevents mid-session modifications.

**Warning** if hooks modified externally → require review in `/hooks` menu.

---

## 📥 Hook Input and Output

### Common Input Fields (All Events)
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "agent_id": "agent-abc123",      // Only in subagents
  "agent_type": "Explore"          // Only in subagents
}
```

### Exit Code Output

| Exit Code | Meaning | What Happens |
|-----------|---------|--------------|
| **0** | Success | Parse stdout for JSON output. Most events: shown in verbose mode. UserPromptSubmit/SessionStart: added as context |
| **2** | Blocking error | Ignore stdout. Feed stderr to Claude as error. Block tool call/prompt/etc. |
| **Other** | Non-blocking error | Show stderr in verbose mode. Continue execution. |

### Exit Code 2 Behavior Per Event

| Event | Can Block? | What Happens on Exit 2 |
|-------|------------|------------------------|
| PreToolUse | Yes | Blocks tool call |
| PermissionRequest | Yes | Denies permission |
| UserPromptSubmit | Yes | Blocks prompt processing, erases prompt |
| Stop | Yes | Prevents Claude from stopping |
| SubagentStop | Yes | Prevents subagent from stopping |
| TeammateIdle | Yes | Prevents teammate from going idle |
| TaskCompleted | Yes | Prevents task from being marked completed |
| ConfigChange | Yes | Blocks configuration change (except policy_settings) |
| PostToolUse | No | Shows stderr to Claude (tool already ran) |
| PostToolUseFailure | No | Shows stderr to Claude (tool already failed) |
| Notification | No | Shows stderr to user only |
| ... | No | Most other events: shows stderr only |

### HTTP Response Handling

| Response | Meaning |
|----------|---------|
| **2xx with empty body** | Success (exit code 0, no output) |
| **2xx with plain text** | Success, text added as context |
| **2xx with JSON** | Success, parsed using same schema as command hooks |
| **Non-2xx** | Non-blocking error, continue |
| **Connection failure/timeout** | Non-blocking error, continue |

**Cannot signal blocking error via status code** → must return 2xx with JSON body containing decision.

---

## 🎯 JSON Output

### Approach Choice
**Choose one per hook**:
- **Exit codes alone** → simple allow/block
- **Exit 0 + JSON** → structured control (finer-grained)

**Claude Code only processes JSON on exit 0**. Exit 2 ignores any JSON.

### JSON Structure

**Three kinds of fields**:
1. **Universal fields** → work across all events
2. **Top-level decision/reason** → used by some events
3. **hookSpecificOutput** → nested object for richer control

#### Universal Fields

| Field | Default | Description |
|-------|---------|-------------|
| `continue` | `true` | If false, Claude stops processing entirely |
| `stopReason` | none | Message shown to user when `continue: false` |
| `suppressOutput` | `false` | If true, hides stdout from verbose mode |
| `systemMessage` | none | Warning message shown to user |

**Example**:
```json
{
  "continue": false,
  "stopReason": "Build failed, fix errors before continuing"
}
```

### Decision Control Patterns

| Events | Decision Pattern | Key Fields |
|--------|------------------|------------|
| UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, ConfigChange | Top-level decision | `decision: "block"`, `reason` |
| TeammateIdle, TaskCompleted | Exit code or continue: false | Exit 2 blocks with stderr. JSON `{\"continue\": false}` stops entirely |
| PreToolUse | hookSpecificOutput | `permissionDecision` (allow/deny/ask), `permissionDecisionReason` |
| PermissionRequest | hookSpecificOutput | `decision.behavior` (allow/deny) |
| WorktreeCreate | stdout path | Print absolute path to created worktree |
| Elicitation | hookSpecificOutput | `action` (accept/decline/cancel), `content` |
| ElicitationResult | hookSpecificOutput | `action` (accept/decline/cancel), `content` (override) |
| WorktreeRemove, Notification, SessionEnd, PreCompact, PostCompact, InstructionsLoaded | None | No decision control. Side effects only |

---

## 📅 Hook Events (Detailed)

### SessionStart
**When**: Session begins or resumes

**Matcher values**: `startup`, `resume`, `clear`, `compact`

**Input**:
```json
{
  "source": "startup",
  "model": "claude-sonnet-4-6",
  "agent_type": "..."  // Optional, if --agent used
}
```

**Decision control**: Cannot block. Stdout added as context.

**Special**: `CLAUDE_ENV_FILE` environment variable available for persisting env vars.

**Example** (persist env vars):
```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

### InstructionsLoaded
**When**: CLAUDE.md or .claude/rules/*.md loaded

**No matcher support** → fires on every load.

**Input**:
```json
{
  "file_path": "/absolute/path/to/CLAUDE.md",
  "memory_type": "Project",  // User, Project, Local, or Managed
  "load_reason": "session_start",  // nested_traversal, path_glob_match, include
  "globs": [...],  // Only for path_glob_match
  "trigger_file_path": "...",  // For lazy loads
  "parent_file_path": "..."   // For include loads
}
```

**Decision control**: None. Audit/observability only.

### UserPromptSubmit
**When**: User submits prompt, before Claude processes

**Input**:
```json
{
  "prompt": "Write a function to calculate the factorial of a number"
}
```

**Decision control**:
- Plain stdout → added as context
- JSON with `additionalContext` → added discretely
- JSON with `decision: "block"` → prevents processing, erases prompt

**Example**:
```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

### PreToolUse
**When**: Before tool call executes

**Matcher**: tool name (Bash, Edit, Write, Read, Glob, Grep, Agent, WebFetch, WebSearch, MCP tools)

**Input** (example: Bash):
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite",
    "timeout": 120000,
    "run_in_background": false
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

**Decision control** (hookSpecificOutput):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",  // allow, deny, or ask
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

**Key fields**:
- `permissionDecision`: `allow` (bypass permission), `deny` (prevent), `ask` (prompt user)
- `permissionDecisionReason`: For allow/ask → shown to user. For deny → shown to Claude
- `updatedInput`: Modify tool input before execution

### PermissionRequest
**When**: Permission dialog appears (before PreToolUse if permissions needed)

**Matcher**: tool name (same as PreToolUse)

**Input**:
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules"
  },
  "permission_suggestions": [
    { "type": "toolAlwaysAllow", "tool": "Bash" }
  ]
}
```

**Decision control**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",  // allow or deny
      "updatedInput": {
        "command": "npm run lint"
      },
      "updatedPermissions": [...],  // Apply permission rules
      "message": "...",  // For deny only
      "interrupt": false  // For deny only
    }
  }
}
```

### PostToolUse
**When**: After tool completes successfully

**Matcher**: tool name

**Input**:
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

**Decision control**:
```json
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedMCPToolOutput": {...}  // For MCP tools only
  }
}
```

### PostToolUseFailure
**When**: Tool execution fails

**Matcher**: tool name

**Input**:
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

**Decision control**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### Notification
**When**: Claude Code sends notifications

**Matcher**: notification type (`permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`)

**Input**:
```json
{
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

**Decision control**: None. Can only add `additionalContext`.

### SubagentStart
**When**: Subagent spawned via Agent tool

**Matcher**: agent type (Bash, Explore, Plan, or custom names)

**Input**:
```json
{
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

**Decision control**: Cannot block, but can inject `additionalContext`.

### SubagentStop
**When**: Subagent finishes

**Matcher**: agent type (same as SubagentStart)

**Input**:
```json
{
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

**Decision control** (same as Stop):
```json
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### Stop
**When**: Main Claude Code agent finishes responding

**No matcher support** → fires on every stop.

**Input**:
```json
{
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

**Decision control**:
```json
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

**Check `stop_hook_active`** to prevent infinite loops.

### TeammateIdle
**When**: Agent team teammate about to go idle

**No matcher support** → fires on every occurrence.

**Input**:
```json
{
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

**Decision control**:
- **Exit 2** → teammate receives stderr as feedback, continues working
- **JSON `{"continue": false, "stopReason": "..."}`** → stops teammate entirely

### TaskCompleted
**When**: Task being marked as completed

**No matcher support** → fires on every occurrence.

**Input**:
```json
{
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

**Decision control**:
- **Exit 2** → task not marked completed, stderr fed back as feedback
- **JSON `{"continue": false, "stopReason": "..."}`** → stops teammate entirely

### ConfigChange
**When**: Configuration file changes during session

**Matcher**: configuration source (`user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`)

**Input**:
```json
{
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

**Decision control**:
```json
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

**Exception**: `policy_settings` changes cannot be blocked.

### WorktreeCreate
**When**: Worktree being created (`--worktree` or `isolation: "worktree"`)

**No matcher support**.

**Input**:
```json
{
  "name": "feature-auth"
}
```

**Output**: Must print **absolute path** to created worktree on stdout.

**Decision control**: Success/failure via exit code. Non-zero → creation fails.

**Only type: "command"** hooks supported.

### WorktreeRemove
**When**: Worktree being removed

**No matcher support**.

**Input**:
```json
{
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

**Decision control**: None. Cannot block. Cleanup tasks only.

**Only type: "command"** hooks supported.

### PreCompact
**When**: Before context compaction

**Matcher**: trigger (`manual`, `auto`)

**Input**:
```json
{
  "trigger": "manual",
  "custom_instructions": ""
}
```

**Decision control**: None. Observability only.

### PostCompact
**When**: After context compaction completes

**Matcher**: trigger (`manual`, `auto`)

**Input**:
```json
{
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

**Decision control**: None. Follow-up tasks only.

### SessionEnd
**When**: Session terminates

**Matcher**: reason (`clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`)

**Input**:
```json
{
  "reason": "other"
}
```

**Decision control**: None. Cleanup tasks only.

**Default timeout**: 1.5 seconds. Override via `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`.

### Elicitation
**When**: MCP server requests user input mid-task

**Matcher**: MCP server name

**Input (form-mode)**:
```json
{
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

**Input (URL-mode)**:
```json
{
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

**Decision control**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",  // accept, decline, or cancel
    "content": {
      "username": "alice"
    }
  }
}
```

**Exit 2** → denies elicitation, shows stderr to user.

### ElicitationResult
**When**: After user responds to MCP elicitation, before response sent back

**Matcher**: MCP server name

**Input**:
```json
{
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

**Decision control**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",  // Overrides user's action
    "content": {}
  }
}
```

**Exit 2** → blocks response, effective action becomes `decline`.

---

## 🤖 Prompt-Based Hooks

### Supported Events
**All four hook types** (command, http, prompt, agent):
- PermissionRequest
- PostToolUse
- PostToolUseFailure
- PreToolUse
- Stop
- SubagentStop
- TaskCompleted
- UserPromptSubmit

**Only type: "command"**:
- All other events (ConfigChange, SessionStart, etc.)

### How Prompt Hooks Work
1. Send hook input + your prompt to Claude model (Haiku default)
2. LLM responds with structured JSON decision
3. Claude Code processes decision automatically

### Configuration
```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete.",
  "model": "...",  // Optional, defaults to fast model
  "timeout": 30    // Optional
}
```

**$ARGUMENTS placeholder** → injects hook input JSON.

### Response Schema
```json
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

- `ok: true` → allow action
- `ok: false` → prevent action, `reason` shown to Claude

### Example (Multi-criteria Stop hook)
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

## 🕵️ Agent-Based Hooks

### How Agent Hooks Work
1. Spawn subagent with prompt + hook input JSON
2. Subagent can use tools (Read, Grep, Glob) to investigate
3. After up to 50 turns, return `{ "ok": true/false }` decision
4. Claude Code processes decision same as prompt hook

**Use case**: Verification requires inspecting actual files or test output.

### Configuration
```json
{
  "type": "agent",
  "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
  "model": "...",  // Optional
  "timeout": 60    // Optional, default 60s
}
```

**Response schema**: Same as prompt hooks (`{ "ok": true/false, "reason": "..." }`).

### Example (Verify tests pass before stopping)
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

---

## 🚀 Run Hooks in the Background (async)

### Configuration
**Add `"async": true`** to command hook.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### How Async Hooks Execute
1. Claude Code starts hook process
2. **Immediately continues** without waiting
3. Hook receives same JSON input via stdin
4. When process exits, `systemMessage` or `additionalContext` delivered on next turn

**Notifications suppressed by default** → enable verbose mode (`Ctrl+O` or `--verbose`).

### Limitations
- **Only type: "command"** hooks support async
- **Cannot block** or return decisions (action already completed)
- Output delivered on **next conversation turn**
- **No deduplication** across multiple firings

### Example (Run tests after file changes)
**Script** (`.claude/hooks/run-tests-async.sh`):
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only run tests for source files
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Run tests and report results
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

**Configuration**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

---

## 🔒 Security Considerations

### Disclaimer
**Command hooks run with your system user's full permissions**. Can modify/delete/access any files your account can.

### Security Best Practices
1. ✅ **Validate and sanitize inputs** → never trust blindly
2. ✅ **Always quote shell variables** → use `"$VAR"` not `$VAR`
3. ✅ **Block path traversal** → check for `..` in file paths
4. ✅ **Use absolute paths** → specify full paths, use `$CLAUDE_PROJECT_DIR`
5. ✅ **Skip sensitive files** → avoid `.env`, `.git/`, keys, etc.

---

## 🐛 Debug Hooks

### Enable Debug Mode
**Run `claude --debug`** to see hook execution details:
- Which hooks matched
- Exit codes
- Output

**Toggle verbose mode**: `Ctrl+O` → see hook progress in transcript.

### Debug Output Example
```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

---

## 💡 学习感悟

### 1. **Hooks 是 Claude Code 的自动化核心**
**生命周期钩子** → 在关键节点注入自定义逻辑。

**四种类型**:
- **Command**: Shell commands（最灵活）
- **HTTP**: POST requests（远程集成）
- **Prompt**: LLM evaluation（智能决策）
- **Agent**: Subagent verification（深度检查）

### 2. **Decision Control 是核心能力**
**三种模式**:
- **Exit codes**: 简单允许/阻止（0 = allow, 2 = block）
- **JSON output**: 结构化控制（更细粒度）
- **hookSpecificOutput**: 事件特定控制（最丰富）

**关键**：Exit 0 + JSON vs Exit 2（二选一）。

### 3. **Matcher 是强大的过滤机制**
**Regex patterns**:
- `*` or omit → match all
- `Edit|Write` → either
- `mcp__.*` → all MCP tools
- `mcp__memory__.*` → specific server

**No matcher support**: UserPromptSubmit, Stop, TeammateIdle, TaskCompleted, WorktreeCreate/Remove, InstructionsLoaded.

### 4. **PreToolUse 是最强大的钩子**
**三重控制**:
- `permissionDecision`: `allow` (bypass), `deny` (block), `ask` (prompt)
- `permissionDecisionReason`: 反馈原因
- `updatedInput`: **修改 tool input before execution**

**可以动态修改参数** → 非常强大。

### 5. **Prompt/Agent Hooks 启用智能决策**
**Prompt hooks**: LLM evaluation（fast model）
**Agent hooks**: Subagent verification（tool access, up to 50 turns）

**Response schema**: `{ "ok": true/false, "reason": "..." }`

**Use case**:
- Prompt: Simple evaluation
- Agent: Need to inspect files/tests

### 6. **Async Hooks 解耦执行和响应**
**`async: true`**:
- Start process → immediately continue
- Output delivered on next turn
- Cannot block or return decisions

**Use case**: Long-running tasks (tests, deployments, API calls).

### 7. **SessionStart 可以持久化环境变量**
**`CLAUDE_ENV_FILE`** → write export statements to file.

**Available in all subsequent Bash commands**.

**Only SessionStart hooks** have access to this variable.

### 8. **Stop Hook 需要防止无限循环**
**Check `stop_hook_active`**:
```json
{
  "stop_hook_active": true
}
```

**If true** → already continuing as result of stop hook.

**Process transcript or check flag** to prevent infinite loop.

### 9. **TeammateIdle 和 TaskCompleted 是质量门**
**Exit 2**:
- TeammateIdle → teammate continues with stderr feedback
- TaskCompleted → task not completed, stderr fed back

**JSON `{"continue": false}`**:
- Stops teammate entirely

**Use case**: Enforce passing tests/lint before stopping/completing.

### 10. **WorktreeCreate/Remove 支持非 Git VCS**
**WorktreeCreate**:
- Replaces default git behavior
- Must print absolute path on stdout
- Non-zero exit → creation fails

**WorktreeRemove**:
- Cleanup tasks
- Cannot block

**Use case**: SVN, Perforce, Mercurial.

---

## 🎯 实践建议

### 1. **Start with Command Hooks**
**Simplest** → Shell scripts with exit codes.

**Example** (Block rm -rf):
```bash
#!/bin/bash
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0
fi
```

### 2. **Use JSON Output for Fine-Grained Control**
**Exit 0 + JSON**:
```json
{
  "decision": "block",
  "reason": "Test suite must pass before proceeding"
}
```

**vs Exit 2**: JSON provides structured feedback, exit 2 is simpler.

### 3. **Leverage PreToolUse UpdatedInput**
**Modify tool input**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "command": "npm run lint:fix"
    }
  }
}
```

**Use case**: Auto-fix, parameter normalization.

### 4. **Use Prompt Hooks for Intelligent Decisions**
**Example** (Stop hook):
```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
}
```

**LLM decides** based on context.

### 5. **Use Agent Hooks for File Inspection**
**Example** (Verify tests):
```json
{
  "type": "agent",
  "prompt": "Verify that all unit tests pass. Run the test suite. $ARGUMENTS",
  "timeout": 120
}
```

**Agent can read files, run tests** → more powerful than prompt.

### 6. **Use Async Hooks for Long-Running Tasks**
**Example** (Background tests):
```json
{
  "type": "command",
  "command": "run-tests.sh",
  "async": true,
  "timeout": 300
}
```

**Non-blocking**, results on next turn.

### 7. **Persist Env Vars in SessionStart**
**Example**:
```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

**Available in all subsequent Bash commands**.

### 8. **Enforce Quality Gates with TeammateIdle/TaskCompleted**
**Example** (Block if tests fail):
```bash
#!/bin/bash
if ! npm test 2>&1; then
  echo "Tests not passing. Fix before completing." >&2
  exit 2
fi
exit 0
```

**Exit 2** → continue working with feedback.

### 9. **Use /hooks Menu for Verification**
**Type `/hooks`** → browse configured hooks.

**Check**:
- Which hooks are active
- Configuration sources
- Match patterns

**Read-only** → edit JSON to modify.

### 10. **Debug with --debug and Ctrl+O**
**`claude --debug`** → detailed execution logs.

**`Ctrl+O`** → verbose mode in transcript.

**See**: Matched hooks, exit codes, output.

---

## 🏷️ 标签
`#hooks` `#automation` `#lifecycle` `#decision-control` `#matcher` `#prompt-hooks` `#agent-hooks` `#async-hooks` `#security` `#debugging`
