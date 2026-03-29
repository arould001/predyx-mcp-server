# 22 - Extend Claude with Skills 学习笔记

**学习时间**：2026-03-14 16:06
**页面地址**：https://code.claude.com/docs/en/skills

---

## 📖 核心概念

### 是什么
**Skills** 扩展 Claude 的能力。创建 `SKILL.md` 文件，Claude 将其添加到工具包。Claude 在相关时自动使用，或通过 `/skill-name` 直接调用。

### Agent Skills 开放标准
Claude Code skills 遵循 **Agent Skills 开放标准**（跨多个 AI 工具工作）。Claude Code 扩展标准，增加了：
- Invocation control
- Subagent execution
- Dynamic context injection

### Custom Commands → Skills
**已合并**：
- `.claude/commands/deploy.md` 和 `.claude/skills/deploy/SKILL.md` 都创建 `/deploy`，工作方式相同
- 现有 `.claude/commands/` 文件继续工作
- Skills 增加可选特性：
  - 支持文件的目录
  - Frontmatter 控制调用方式
  - Claude 自动加载（当相关时）

---

## 🎁 Bundled Skills

### 是什么
**Bundled skills** 随 Claude Code 一起发布，每个会话都可用。

### vs Built-in Commands
- **Built-in commands**: 执行固定逻辑
- **Bundled skills**: 基于 prompt，给 Claude 详细的 playbook，让其编排工作（可 spawn parallel agents, read files, adapt to codebase）

### Available Bundled Skills

| Skill | Purpose |
|-------|---------|
| `/batch <instruction>` | Orchestrate large-scale changes across codebase in parallel. Researches codebase, decomposes work into 5-30 independent units, presents plan. Once approved, spawns one background agent per unit in isolated git worktree. Each agent implements unit, runs tests, opens PR. **Requires git repository**. Example: `/batch migrate src/ from Solid to React` |
| `/claude-api` | Load Claude API reference material for project's language (Python, TypeScript, Java, Go, Ruby, C#, PHP, or cURL) and Agent SDK reference for Python and TypeScript. Covers tool use, streaming, batches, structured outputs, common pitfalls. Also activates automatically when code imports `anthropic`, `@anthropic-ai/sdk`, or `claude_agent_sdk` |
| `/debug [description]` | Troubleshoot current Claude Code session by reading session debug log. Optionally describe issue to focus analysis |
| `/loop [interval] <prompt>` | Run prompt repeatedly on interval while session stays open. Useful for polling deployment, babysitting PR, or periodically re-running another skill. Example: `/loop 5m check if deploy finished`. See [Run prompts on a schedule](#run-prompts-on-a-schedule) |
| `/simplify [focus]` | Review recently changed files for code reuse, quality, efficiency issues, then fix. Spawns three review agents in parallel, aggregates findings, applies fixes. Pass text to focus on specific concerns: `/simplify focus on memory efficiency` |

---

## 🚀 Getting Started

### Create Your First Skill
**Example**: 创建解释代码的 skill（使用 visual diagrams 和 analogies）

#### Step 1: Create Skill Directory
```bash
mkdir -p ~/.claude/skills/explain-code
```

**Personal skills** → 所有项目可用。

#### Step 2: Write SKILL.md
**Two parts**:
1. **YAML frontmatter** (between `---` markers) - tells Claude when to use skill
2. **Markdown content** - instructions Claude follows when skill invoked

**~/.claude/skills/explain-code/SKILL.md**:
```markdown
---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.
```

#### Step 3: Test the Skill
**Two ways**:

**1. Automatic invocation** (matches description):
```
How does this code work?
```

**2. Direct invocation**:
```
/explain-code src/auth/login.ts
```

**Expected behavior**: Claude should include an analogy and ASCII diagram in explanation.

---

## 📂 Where Skills Live

### Location Determines Scope

| Location | Path | Applies to |
|----------|------|------------|
| **Enterprise** | See managed settings | All users in organization |
| **Personal** | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| **Project** | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| **Plugin** | `<plugin>/skills/<skill-name>/SKILL.md` | Where plugin is enabled |

### Priority
**When skills share same name**:
- Enterprise > Personal > Project
- **Plugin skills** use `plugin-name:skill-name` namespace → cannot conflict

**If skill and command share same name** → skill takes precedence.

### Automatic Discovery from Nested Directories
**Monorepo support**: When working with files in subdirectories, Claude Code automatically discovers skills from nested `.claude/skills/` directories.

**Example**: Editing file in `packages/frontend/` → Claude Code looks for skills in `packages/frontend/.claude/skills/`.

### Skill Directory Structure
```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

**SKILL.md is required**. Other files are optional:
- Templates for Claude to fill in
- Example outputs showing expected format
- Scripts Claude can execute
- Detailed reference documentation

**Reference these files from SKILL.md** so Claude knows what they contain and when to load them.

**Files in `.claude/commands/` still work** and support same frontmatter. Skills recommended since they support additional features.

### Skills from Additional Directories
**--add-dir**: Skills defined in `.claude/skills/` within directories added via `--add-dir` are loaded automatically and picked up by live change detection.

**Edit during session without restarting**.

**CLAUDE.md files** from `--add-dir` directories are **not loaded by default**. To load, set `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`.

---

## ⚙️ Configure Skills

### Two Parts
1. **YAML frontmatter** (top of `SKILL.md`)
2. **Markdown content** (follows frontmatter)

### Types of Skill Content

#### 1. Reference Content
**Adds knowledge** Claude applies to current work. Conventions, patterns, style guides, domain knowledge.

**Runs inline** so Claude can use it alongside conversation context.

**Example**:
```markdown
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

#### 2. Task Content
**Step-by-step instructions** for specific action (deployments, commits, code generation).

**Often actions you want to invoke directly** with `/skill-name` rather than letting Claude decide when to run.

**Add `disable-model-invocation: true`** to prevent Claude from triggering automatically.

**Example**:
```markdown
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

**Thinking through invocation** (by you, by Claude, or both) and execution context (inline or subagent) helps guide what to include.

---

## 📋 Frontmatter Reference

### Example
```yaml
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read, Grep
---

Your skill instructions here...
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name. If omitted, uses directory name. Lowercase letters, numbers, hyphens only (max 64 chars). |
| `description` | **Recommended** | What skill does and when to use it. Claude uses this to decide when to apply skill. If omitted, uses first paragraph of markdown content. |
| `argument-hint` | No | Hint shown during autocomplete. Example: `[issue-number]` or `[filename] [format]`. |
| `disable-model-invocation` | No | Set to `true` to prevent Claude from automatically loading. Use for workflows you want to trigger manually with `/name`. Default: `false`. |
| `user-invocable` | No | Set to `false` to hide from `/` menu. Use for background knowledge users shouldn't invoke directly. Default: `true`. |
| `allowed-tools` | No | Tools Claude can use **without asking permission** when skill is active. |
| `model` | No | Model to use when skill is active. |
| `context` | No | Set to `fork` to run in forked subagent context. |
| `agent` | No | Which subagent type to use when `context: fork` is set. |
| `hooks` | No | Hooks scoped to skill's lifecycle. See [Hooks in skills and agents](#hooks-in-skills-and-agents). |

**All fields optional**. Only `description` recommended so Claude knows when to use skill.

---

## 🔤 Available String Substitutions

### Variables

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking skill. If not present in content, arguments are appended as `ARGUMENTS: <value>`. |
| `$ARGUMENTS[N]` | Access specific argument by 0-based index (e.g., `$ARGUMENTS[0]` for first argument). |
| `$N` | Shorthand for `$ARGUMENTS[N]` (e.g., `$0` for first argument, `$1` for second). |
| `${CLAUDE_SESSION_ID}` | Current session ID. Useful for logging, creating session-specific files, or correlating skill output with sessions. |
| `${CLAUDE_SKILL_DIR}` | Directory containing skill's `SKILL.md` file. For plugin skills, this is skill's subdirectory within plugin, not plugin root. Use in bash injection commands to reference scripts or files bundled with skill, regardless of current working directory. |

### Example
```markdown
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

---

## 📁 Add Supporting Files

### Why
**Keep SKILL.md focused on essentials** while letting Claude access detailed reference material only when needed.

**Large reference docs, API specifications, example collections** don't need to load into context every time skill runs.

### Structure
```
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

### Reference from SKILL.md
```markdown
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

**Keep SKILL.md under 500 lines**. Move detailed reference material to separate files.

---

## 🎮 Control Who Invokes a Skill

### Default Behavior
**Both you and Claude can invoke any skill**:
- You: `/skill-name` to invoke directly
- Claude: Load automatically when relevant to conversation

### Two Frontmatter Fields to Restrict

#### 1. disable-model-invocation: true
**Only you can invoke**. Use for workflows with side effects or that you want to control timing.

**Examples**: `/commit`, `/deploy`, `/send-slack-message`

**You don't want Claude deciding to deploy because your code looks ready**.

```markdown
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

#### 2. user-invocable: false
**Only Claude can invoke**. Use for background knowledge that isn't actionable as command.

**Example**: `legacy-system-context` skill explains how old system works. Claude should know this when relevant, but `/legacy-system-context` isn't a meaningful action for users to take.

### Invocation Matrix

| Frontmatter | You can invoke | Claude can invoke | When loaded into context |
|-------------|----------------|-------------------|--------------------------|
| (default) | Yes | Yes | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description not in context, full skill loads when you invoke |
| `user-invocable: false` | No | Yes | Description always in context, full skill loads when invoked |

**In regular session**: Skill descriptions loaded into context so Claude knows what's available, but **full skill content only loads when invoked**.

**Subagents with preloaded skills**: Full skill content is injected at startup.

---

## 🔒 Restrict Tool Access

### allowed-tools Field
**Limit which tools Claude can use** when skill is active.

**Example**: Read-only mode - Claude can explore files but not modify them.

```markdown
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

---

## 📝 Pass Arguments to Skills

### $ARGUMENTS Placeholder
**Both you and Claude can pass arguments** when invoking skill. Arguments available via `$ARGUMENTS` placeholder.

**Example**: Fix GitHub issue by number.

```markdown
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

**When you run `/fix-issue 123`**: Claude receives "Fix GitHub issue 123 following our coding standards…"

**If skill doesn't include `$ARGUMENTS`**: Claude Code appends `ARGUMENTS: <your input>` to end of skill content so Claude still sees what you typed.

### Access Individual Arguments

#### $ARGUMENTS[N]
```markdown
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

**Running `/migrate-component SearchBar React Vue`**: Replaces `$ARGUMENTS[0]` with `SearchBar`, `$ARGUMENTS[1]` with `React`, `$ARGUMENTS[2]` with `Vue`.

#### $N Shorthand
```markdown
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

**Same result, shorter syntax**.

---

## 🚀 Advanced Patterns

### 1. Inject Dynamic Context

#### !command Syntax
**Runs shell commands before skill content sent to Claude**. Command output replaces placeholder, so Claude receives actual data, not command itself.

**Example**: Summarize PR by fetching live PR data with GitHub CLI.

```markdown
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

**When this skill runs**:
1. Each `!command` executes immediately (before Claude sees anything)
2. Output replaces placeholder in skill content
3. Claude receives fully-rendered prompt with actual PR data

**This is preprocessing, not something Claude executes**. Claude only sees final result.

**Extended thinking**: To enable in skill, include word "ultrathink" anywhere in skill content.

### 2. Run Skills in a Subagent

#### context: fork
**Add to frontmatter when you want skill to run in isolation**. Skill content becomes prompt that drives subagent. **Won't have access to your conversation history**.

**Only makes sense for skills with explicit instructions**. If skill contains guidelines like "use these API conventions" without a task, subagent receives guidelines but no actionable prompt, and returns without meaningful output.

#### Skills vs Subagents

| Approach | System prompt | Task | Also loads |
|----------|--------------|------|------------|
| **Skill with `context: fork`** | From agent type (Explore, Plan, etc.) | SKILL.md content | CLAUDE.md |
| **Subagent with skills field** | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md |

**With `context: fork`**: You write task in skill and pick agent type to execute it.

**Inverse** (defining custom subagent that uses skills as reference material): See [Subagents](#subagents).

#### Example: Research Skill Using Explore Agent
```markdown
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

**When this skill runs**:
1. New isolated context created
2. Subagent receives skill content as prompt ("Research $ARGUMENTS thoroughly…")
3. Agent field determines execution environment (model, tools, permissions)
4. Results summarized and returned to main conversation

**Agent field options**:
- Built-in agents: `Explore`, `Plan`, `general-purpose`
- Custom subagents from `.claude/agents/`
- If omitted: uses `general-purpose`

---

## 🔐 Restrict Claude's Skill Access

### Default Behavior
**Claude can invoke any skill without `disable-model-invocation: true`**.

**Skills with `allowed-tools` grant Claude access to those tools without per-use approval when skill is active**.

**Permission settings still govern baseline approval behavior** for all other tools.

**Built-in commands** like `/compact` and `/init` are **not available** through Skill tool.

### Three Ways to Control

#### 1. Disable All Skills
**Deny Skill tool in `/permissions`**:
```markdown
# Add to deny rules:
Skill
```

#### 2. Allow/Deny Specific Skills
```markdown
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

**Permission syntax**:
- `Skill(name)` for exact match
- `Skill(name *)` for prefix match with any arguments

#### 3. Hide Individual Skills
**Add `disable-model-invocation: true`** to frontmatter. Removes skill from Claude's context entirely.

**Note**: `user-invocable` field only controls menu visibility, not Skill tool access. Use `disable-model-invocation: true` to block programmatic invocation.

---

## 📤 Share Skills

### Distribution Scopes

| Scope | How |
|-------|-----|
| **Project skills** | Commit `.claude/skills/` to version control |
| **Plugins** | Create `skills/` directory in plugin |
| **Managed** | Deploy organization-wide through managed settings |

---

## 🎨 Generate Visual Output

### Pattern
**Skills can bundle and run scripts in any language**, giving Claude capabilities beyond what's possible in single prompt.

**Powerful pattern**: Generating visual output - interactive HTML files that open in browser for exploring data, debugging, or creating reports.

### Example: Codebase Explorer

**Interactive tree view**:
- Expand and collapse directories
- See file sizes at glance
- Identify file types by color

#### Step 1: Create Skill Directory
```bash
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

#### Step 2: Create SKILL.md
**~/.claude/skills/codebase-visualizer/SKILL.md**:
```markdown
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` in current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
```

#### Step 3: Create visualize.py Script
**~/.claude/skills/codebase-visualizer/scripts/visualize.py**:

**Key features**:
- Scans directory tree
- Generates self-contained HTML file
- Summary sidebar (file count, directory count, total size, file types)
- Bar chart by file type (top 8 by size)
- Collapsible tree with color-coded file type indicators
- Uses only Python built-in libraries (no packages to install)

**Full script**: 131 lines (see page for complete code)

#### Step 4: Test
**In Claude Code**:
```
Visualize this codebase.
```

**What happens**:
1. Claude runs script
2. Generates `codebase-map.html`
3. Opens in browser

**Pattern works for any visual output**: dependency graphs, test coverage reports, API documentation, database schema visualizations.

**Bundled script does heavy lifting** while Claude handles orchestration.

---

## 🐛 Troubleshooting

### Skill Not Triggering
**If Claude doesn't use skill when expected**:
1. ✅ Check description includes keywords users would naturally say
2. ✅ Verify skill appears in "What skills are available?"
3. ✅ Try rephrasing request to match description more closely
4. ✅ Invoke directly with `/skill-name` if skill is user-invocable

### Skill Triggers Too Often
**If Claude uses skill when you don't want it**:
1. ✅ Make description more specific
2. ✅ Add `disable-model-invocation: true` if you only want manual invocation

### Claude Doesn't See All My Skills
**Skill descriptions loaded into context** so Claude knows what's available.

**If you have many skills**, they may exceed character budget:
- Budget scales dynamically at **2% of context window**
- Fallback of **16,000 characters**
- Run `/context` to check for warning about excluded skills

**To override limit**:
```bash
export SLASH_COMMAND_TOOL_CHAR_BUDGET=<number>
```

---

## 💡 学习感悟

### 1. **Skills 是 Claude Code 的核心扩展机制**
**Two-part structure**:
- **YAML frontmatter**: Controls when/how to use
- **Markdown content**: Instructions to follow

**Agent Skills 开放标准** → 跨多个 AI 工具工作。

**Custom commands 已合并** → `.claude/commands/` 和 `.claude/skills/` 都创建 `/command`，工作方式相同。

### 2. **Bundled Skills 是 Prompt-Based，Not Fixed Logic**
**vs Built-in commands**:
- **Built-in**: Fixed logic
- **Bundled**: Prompt-based, give Claude playbook, orchestrate work with tools

**Available**:
- `/batch`: Large-scale parallel changes (5-30 units, git worktrees, PRs)
- `/claude-api`: Load API reference (auto-activates on imports)
- `/debug`: Troubleshoot session
- `/loop`: Run prompt repeatedly
- `/simplify`: Review and fix recently changed files

### 3. **Skill Location Determines Scope**
**Priority**: Enterprise > Personal > Project

**Plugin skills**: Namespaced (`plugin:skill`) → no conflict

**Monorepo support**: Automatic discovery from nested `.claude/skills/` directories.

### 4. **Two Types of Skill Content**
**Reference content**:
- Adds knowledge (conventions, patterns, style guides)
- Runs inline alongside conversation

**Task content**:
- Step-by-step instructions (deployments, commits)
- Often want direct invocation (`/skill-name`)
- Add `disable-model-invocation: true` to prevent auto-trigger

**Think through invocation and execution context**.

### 5. **Frontmatter Control is Powerful**
**Key fields**:
- `description`: When to use (recommended)
- `disable-model-invocation`: Prevent auto-load (for workflows with side effects)
- `user-invocable`: Hide from menu (for background knowledge)
- `allowed-tools`: Restrict tool access (read-only mode)
- `context: fork`: Run in subagent
- `agent`: Subagent type (Explore, Plan, etc.)

**All optional**, but `description` recommended.

### 6. **String Substitutions Enable Dynamic Skills**
**Variables**:
- `$ARGUMENTS`: All arguments
- `$ARGUMENTS[N]` or `$N`: Specific argument by index
- `${CLAUDE_SESSION_ID}`: Session ID
- `${CLAUDE_SKILL_DIR}`: Skill directory (for scripts/files)

**Use cases**: Logging, session-specific files, referencing bundled resources.

### 7. **Supporting Files Keep SKILL.md Focused**
**Structure**:
```
my-skill/
├── SKILL.md (required - overview)
├── reference.md (detailed docs)
├── examples.md (examples)
└── scripts/
    └── helper.py (utility script)
```

**Keep SKILL.md under 500 lines**. Move detailed reference material to separate files.

**Reference from SKILL.md** so Claude knows what each file contains.

### 8. **Control Invocation is Critical**
**Two fields**:
- `disable-model-invocation: true`: Only you can invoke (deploy, commit)
- `user-invocable: false`: Only Claude can invoke (background knowledge)

**Invocation matrix**:
- Default: Both can invoke
- `disable-model-invocation: true`: You only
- `user-invocable: false`: Claude only

**In regular session**: Descriptions always in context, full content loads when invoked.

**Subagents with preloaded skills**: Full content injected at startup.

### 9. **Advanced Patterns Enable Powerful Skills**
**Inject dynamic context**:
- `!command` syntax runs shell commands before skill sent to Claude
- Output replaces placeholder
- Claude receives actual data, not command

**Run in subagent**:
- `context: fork` runs skill in isolation
- Skill content becomes subagent prompt
- No access to conversation history

**Agent field**: Determines execution environment (Explore, Plan, etc.)

### 10. **Visual Output Pattern is Game-Changer**
**Bundled scripts** in any language → capabilities beyond single prompt.

**Codebase explorer example**:
- Interactive HTML tree view
- Collapsible directories
- File sizes and colors
- Summary sidebar and bar chart

**Pattern works for**: dependency graphs, test coverage, API docs, DB schemas.

**Script does heavy lifting**, Claude handles orchestration.

---

## 🎯 实践建议

### 1. **Start with Personal Skills**
```bash
mkdir -p ~/.claude/skills/my-skill
```

**Available across all projects**.

### 2. **Write Clear Descriptions**
```markdown
---
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---
```

**Include keywords users would naturally say**.

### 3. **Use disable-model-invocation for Workflows with Side Effects**
```markdown
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---
```

**Prevent Claude from auto-deploying**.

### 4. **Keep SKILL.md Under 500 Lines**
**Move detailed reference material** to supporting files:
- `reference.md`
- `examples.md`
- `scripts/`

**Reference from SKILL.md**.

### 5. **Use Supporting Files for Complex Skills**
```
my-skill/
├── SKILL.md (overview and navigation)
├── reference.md (detailed docs)
└── scripts/
    └── helper.py
```

**Keeps SKILL.md focused**.

### 6. **Inject Dynamic Context with !command**
```markdown
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
```

**Claude receives actual data**, not command.

### 7. **Run Skills in Subagents for Isolation**
```markdown
---
context: fork
agent: Explore
---
```

**Skill content becomes subagent prompt**. No access to conversation history.

### 8. **Restrict Tool Access for Read-Only Skills**
```markdown
---
allowed-tools: Read, Grep, Glob
---
```

**Claude can explore but not modify**.

### 9. **Generate Visual Output with Bundled Scripts**
**Pattern**:
1. Create skill directory + `scripts/` subdirectory
2. SKILL.md describes what script does and how to run
3. Script generates HTML and opens in browser

**Works for any visual output**.

### 10. **Share at Appropriate Scope**
- **Project skills**: Commit `.claude/skills/` to VCS
- **Team**: Create plugin with `skills/` directory
- **Organization**: Deploy via managed settings

---

## 📚 Related Resources

- **Subagents**: Delegate tasks to specialized agents
- **Plugins**: Package and distribute skills with other extensions
- **Hooks**: Automate workflows around tool events
- **Memory**: Manage `CLAUDE.md` files for persistent context
- **Built-in commands**: Reference for built-in `/` commands
- **Permissions**: Control tool and skill access

---

## 🏷️ 标签
`#skills` `#agent-skills` `#extension` `#frontmatter` `#subagents` `#dynamic-context` `#visual-output` `#supporting-files` `#invocation-control` `#tool-restrictions`
