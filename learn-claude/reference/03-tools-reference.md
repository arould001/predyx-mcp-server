# Tools Reference

> **来源**: https://code.claude.com/docs/en/tools-reference
> **抓取时间**: 2026-03-14

Complete reference for the tools Claude Code can use, including permission requirements.

---

## Tool List

Claude Code has access to a set of tools that help it understand and modify your codebase. The tool names below are the exact strings you use in permission rules, subagent tool lists, and hook matchers.

| Tool | Description | Permission Required |
|------|-------------|---------------------|
| `Agent` | Spawns a subagent with its own context window to handle a task | No |
| `AskUserQuestion` | Asks multiple-choice questions to gather requirements or clarify ambiguity | No |
| `Bash` | Executes shell commands in your environment. See Bash tool behavior | Yes |
| `CronCreate` | Schedules a recurring or one-shot prompt within the current session (gone when Claude exits). See scheduled tasks | No |
| `CronDelete` | Cancels a scheduled task by ID | No |
| `CronList` | Lists all scheduled tasks in the session | No |
| `Edit` | Makes targeted edits to specific files | Yes |
| `EnterPlanMode` | Switches to plan mode to design an approach before coding | No |
| `EnterWorktree` | Creates an isolated git worktree and switches into it | No |
| `ExitPlanMode` | Presents a plan for approval and exits plan mode | Yes |
| `ExitWorktree` | Exits a worktree session and returns to the original directory | No |
| `Glob` | Finds files based on pattern matching | No |
| `Grep` | Searches for patterns in file contents | No |
| `ListMcpResourcesTool` | Lists resources exposed by connected MCP servers | No |
| `LSP` | Code intelligence via language servers. Reports type errors and warnings automatically after file edits. Also supports navigation operations: jump to definitions, find references, get type info, list symbols, find implementations, trace call hierarchies. Requires a code intelligence plugin and its language server binary | No |
| `NotebookEdit` | Modifies Jupyter notebook cells | Yes |
| `Read` | Reads the contents of files | No |
| `ReadMcpResourceTool` | Reads a specific MCP resource by URI | No |
| `Skill` | Executes a skill within the main conversation | Yes |
| `TaskCreate` | Creates a new task in the task list | No |
| `TaskGet` | Retrieves full details for a specific task | No |
| `TaskList` | Lists all tasks with their current status | No |
| `TaskOutput` | Retrieves output from a background task | No |
| `TaskStop` | Kills a running background task by ID | No |
| `TaskUpdate` | Updates task status, dependencies, details, or deletes tasks | No |
| `TodoWrite` | Manages the session task checklist. Available in non-interactive mode and the Agent SDK; interactive sessions use TaskCreate, TaskGet, TaskList, and TaskUpdate instead | No |
| `ToolSearch` | Searches for and loads deferred tools when tool search is enabled | No |
| `WebFetch` | Fetches content from a specified URL | Yes |
| `WebSearch` | Performs web searches | Yes |
| `Write` | Creates or overwrites files | Yes |

Permission rules can be configured using `/permissions` or in permission settings. Also see Tool-specific permission rules.

---

## Bash Tool Behavior

The Bash tool runs each command in a separate process with the following persistence behavior:

1. **Working directory persists across commands**. Set `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` to reset to the project directory after each command.

2. **Environment variables do not persist**. An export in one command will not be available in the next.

3. **Activate your virtualenv or conda environment before launching Claude Code**. To make environment variables persist across Bash commands, set `CLAUDE_ENV_FILE` to a shell script before launching Claude Code, or use a SessionStart hook to populate it dynamically.

---

## Tool Categories

### 📁 File Operations
- `Read` - Read files
- `Edit` - Edit files (targeted changes)
- `Write` - Create/overwrite files
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `NotebookEdit` - Edit Jupyter notebooks

### 🖥️ System Operations
- `Bash` - Execute shell commands
- `EnterWorktree` / `ExitWorktree` - Git worktree isolation
- `LSP` - Code intelligence

### 🤖 Agent Operations
- `Agent` - Spawn subagents
- `Skill` - Execute skills

### 📋 Task Management
- `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` - Task tracking
- `TaskOutput` / `TaskStop` - Background task management
- `TodoWrite` - Non-interactive task checklist

### ⏰ Scheduling
- `CronCreate` / `CronDelete` / `CronList` - Scheduled tasks

### 🌐 Web Operations
- `WebFetch` - Fetch URLs
- `WebSearch` - Web search

### 🔌 MCP Operations
- `ListMcpResourcesTool` - List MCP resources
- `ReadMcpResourceTool` - Read MCP resource

### 💬 User Interaction
- `AskUserQuestion` - Ask questions
- `EnterPlanMode` / `ExitPlanMode` - Planning mode

### 🔍 Tool Discovery
- `ToolSearch` - Search and load deferred tools

---

## Permission Patterns

### Tools Requiring Permission (High Risk)
- `Bash` - System commands
- `Edit` - Modify files
- `ExitPlanMode` - Present plan
- `NotebookEdit` - Modify notebooks
- `Skill` - Execute skills
- `WebFetch` - Fetch external content
- `WebSearch` - Search web
- `Write` - Create/overwrite files

### Tools Not Requiring Permission (Low Risk)
- `Agent` - Spawn subagents
- `AskUserQuestion` - Ask questions
- `CronCreate` / `CronDelete` / `CronList` - Scheduling
- `EnterPlanMode` / `EnterWorktree` / `ExitWorktree` - Mode switching
- `Glob` / `Grep` - Search
- `ListMcpResourcesTool` / `ReadMcpResourceTool` - MCP access
- `LSP` - Code intelligence
- `Read` - Read files
- `TaskCreate` / `TaskGet` / `TaskList` / `TaskOutput` / `TaskStop` / `TaskUpdate` - Task management
- `TodoWrite` - Task checklist
- `ToolSearch` - Tool discovery

---

## See Also

- Permissions: permission system, rule syntax, and tool-specific patterns
- Subagents: configure tool access for subagents
- Hooks: run custom commands before or after tool execution
