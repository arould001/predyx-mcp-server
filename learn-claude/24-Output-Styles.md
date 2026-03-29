# 24 - Output Styles 学习笔记

**学习时间**：2026-03-14 16:32
**页面地址**：https://code.claude.com/docs/en/output-styles

---

## 📖 核心概念

### 是什么
**Output styles** 让你将 Claude Code 适配为任何类型的 agent，同时保持其核心能力（运行本地脚本、读写文件、跟踪 TODOs）。

### 直接修改 System Prompt
**Output styles directly modify Claude Code's system prompt**。

---

## 🎯 Built-in Output Styles

### 1. Default
**Existing system prompt**, designed to help you complete software engineering tasks efficiently.

### 2. Explanatory
**Provides educational "Insights"** in between helping you complete software engineering tasks.

**Helps you understand**:
- Implementation choices
- Codebase patterns

### 3. Learning
**Collaborative, learn-by-doing mode**.

**Features**:
- Shares "Insights" while coding
- Asks you to contribute small, strategic pieces of code yourself
- Adds `TODO(human)` markers in your code for you to implement

---

## ⚙️ How Output Styles Work

### System Prompt Modifications

#### 1. All Output Styles
- **Exclude** instructions for efficient output (such as responding concisely)

#### 2. Custom Output Styles
- **Exclude** instructions for coding (such as verifying code with tests)
- **Unless** `keep-coding-instructions: true`

#### 3. All Output Styles
- Have their own custom instructions **added to end** of system prompt
- Trigger **reminders** for Claude to adhere to output style instructions during conversation

---

## 🔄 Change Your Output Style

### Interactive Menu
**Run `/config`** and select **Output style** to pick style from menu.

**Saved to**: `.claude/settings.local.json` at local project level.

### Direct Edit
**Edit `outputStyle` field** in settings file:

```json
{
  "outputStyle": "Explanatory"
}
```

### When Changes Take Effect
**Changes take effect next time you start new session**.

**Why**: System prompt set at session start → keeps system prompt stable throughout conversation → prompt caching can reduce latency and cost.

---

## 🎨 Create a Custom Output Style

### Structure
**Markdown files with frontmatter and text** that will be added to system prompt.

### Example
```markdown
---
name: My Custom Style
description: A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

### Save Locations

| Level | Path |
|-------|------|
| **User level** | `~/.claude/output-styles` |
| **Project level** | `.claude/output-styles` |

---

## 📋 Frontmatter Reference

| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Name of output style | Inherits from file name |
| `description` | Description of output style, shown in `/config` picker | None |
| `keep-coding-instructions` | Whether to keep parts of Claude Code's system prompt related to coding | `false` |

---

## 🆚 Comparisons to Related Features

### Output Styles vs. CLAUDE.md vs. --append-system-prompt

| Feature | What it Does |
|---------|-------------|
| **Output Styles** | **Completely "turn off"** parts of Claude Code's default system prompt specific to software engineering |
| **CLAUDE.md** | Adds contents as **user message** following Claude Code's default system prompt. **Does not edit** default system prompt. |
| **--append-system-prompt** | **Appends** content to system prompt. **Does not edit** default system prompt. |

**Key difference**: Output styles **modify** default system prompt; others **add to** it.

### Output Styles vs. Agents

| Feature | Scope | What it Affects |
|---------|-------|-----------------|
| **Output Styles** | Affects **main agent loop** | Only affects **system prompt** |
| **Agents** | **Invoked** to handle specific tasks | Can include **additional settings** (model, tools available, context about when to use) |

**Key difference**: Output styles modify main loop; agents are invoked for tasks.

### Output Styles vs. Skills

| Feature | When Active | What it Does |
|----------|-------------|--------------|
| **Output Styles** | **Always active** once selected | Modify how Claude responds (formatting, tone, structure) |
| **Skills** | **Invoked** with `/skill-name` or loaded automatically when relevant | Task-specific prompts |

**Use case**:
- **Output styles**: Consistent formatting preferences
- **Skills**: Reusable workflows and tasks

---

## 💡 学习感悟

### 1. **Output Styles 直接修改 System Prompt**
**核心能力**：将 Claude Code 适配为任何类型的 agent。

**修改规则**：
- All output styles: Exclude efficient output instructions
- Custom output styles: Exclude coding instructions (unless `keep-coding-instructions: true`)
- Add custom instructions to end of system prompt
- Trigger reminders to adhere to style during conversation

### 2. **Built-in Output Styles 覆盖不同场景**
**三种模式**：
- **Default**: 高效完成软件工程任务
- **Explanatory**: 提供 "Insights"（解释实现选择和代码库模式）
- **Learning**: 协作学习模式（Claude 分享 Insights + 让你贡献代码 + 添加 `TODO(human)` 标记）

### 3. **Changes Take Effect on Next Session**
**为什么**：
- System prompt set at session start
- Keeps system prompt stable → prompt caching reduces latency and cost

**Current session**: 不受影响。

### 4. **Custom Output Styles 是 Markdown + Frontmatter**
**结构**：
```markdown
---
name: My Custom Style
description: Description shown in /config picker
keep-coding-instructions: false
---

# Custom Instructions
...
```

**Save locations**: User level (`~/.claude/output-styles`) or Project level (`.claude/output-styles`).

### 5. **Frontmatter 有三个字段**
| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Output style name | File name |
| `description` | Shown in `/config` picker | None |
| `keep-coding-instructions` | Keep coding instructions? | `false` |

**`keep-coding-instructions: true`** → 保留 coding 相关指令（验证代码、测试等）。

### 6. **Output Styles vs CLAUDE.md vs --append-system-prompt**
**核心差异**：
- **Output styles**: **Modify** default system prompt（turn off software engineering parts）
- **CLAUDE.md**: **Add** user message after default system prompt（don't edit）
- **--append-system-prompt**: **Append** to system prompt（don't edit）

**Output styles 是唯一可以"关闭"default system prompt 部分** 的方式。

### 7. **Output Styles vs Agents**
**Output styles**:
- Affects **main agent loop**
- Only affects **system prompt**

**Agents**:
- **Invoked** to handle specific tasks
- Can include **additional settings** (model, tools, context)

**Use output styles** for global behavior modification; **use agents** for task delegation.

### 8. **Output Styles vs Skills**
**Output styles**:
- **Always active** once selected
- Modify how Claude responds (formatting, tone, structure)

**Skills**:
- **Invoked** with `/skill-name` or loaded automatically
- Task-specific prompts

**Use output styles** for consistent formatting; **use skills** for reusable workflows.

### 9. **Use /config to Change Output Style**
**Interactive menu**:
```
/config
```
→ Select "Output style"

**Saved to**: `.claude/settings.local.json` (local project level).

**Or edit directly**:
```json
{
  "outputStyle": "Explanatory"
}
```

### 10. **Output Styles Enable Non-Software-Engineering Uses**
**Core capabilities preserved**:
- Running local scripts
- Reading/writing files
- Tracking TODOs

**Only modify**: System prompt behavior (formatting, tone, structure).

**Can turn off**: Software engineering specific instructions.

---

## 🎯 实践建议

### 1. **Use Default for Efficient Software Engineering**
**Default output style**: Existing system prompt → complete software engineering tasks efficiently.

### 2. **Use Explanatory for Learning Codebase**
**Explanatory mode**:
- Provides "Insights" while coding
- Helps understand implementation choices
- Helps understand codebase patterns

**Good for**: New team members, new projects.

### 3. **Use Learning for Collaborative Learning**
**Learning mode**:
- Shares "Insights" while coding
- Asks you to contribute small pieces of code
- Adds `TODO(human)` markers for you to implement

**Good for**: Training, skill building.

### 4. **Create Custom Output Styles for Specific Needs**
**Example**: Documentation writer
```markdown
---
name: Documentation Writer
description: Focus on writing clear, comprehensive documentation
keep-coding-instructions: false
---

# Documentation Writer Mode

You are an interactive CLI tool that helps users create and maintain documentation...

## Specific Behaviors

- Focus on clarity and comprehensiveness
- Use examples and code snippets
- Structure documentation logically
- Keep documentation up-to-date with code changes
```

**Save to**: `~/.claude/output-styles/documentation-writer.md`

### 5. **Use /config to Switch Styles**
```
/config
```
→ Select "Output style" → Choose style

**Changes take effect next session**.

### 6. **Set keep-coding-instructions: true if Needed**
**If you want to keep coding instructions** (verify code with tests, etc.):
```markdown
---
keep-coding-instructions: true
---
```

**Default**: `false` (custom output styles exclude coding instructions).

### 7. **Use Output Styles for Formatting Preferences**
**Consistent formatting**:
- Response structure
- Tone
- Output format

**Use skills** for reusable workflows and tasks.

### 8. **Don't Confuse with CLAUDE.md or --append-system-prompt**
**Output styles**: Modify default system prompt
**CLAUDE.md**: Add user message after default system prompt
**--append-system-prompt**: Append to system prompt

**Choose based on what you need**:
- **Modify default behavior** → Output styles
- **Add context** → CLAUDE.md
- **Append instructions** → --append-system-prompt

### 9. **Project-Level vs User-Level**
**User-level** (`~/.claude/output-styles`): Available across all projects
**Project-level** (`.claude/output-styles`): Specific to project

**Choose based on scope**:
- Personal preferences → User-level
- Project-specific needs → Project-level

### 10. **Remember Changes Take Effect on Next Session**
**Current session**: Not affected
**Next session**: New output style applied

**Why**: Prompt caching → reduce latency and cost.

---

## 📚 Use Cases

### 1. Learning a New Codebase
**Use**: Explanatory output style
**Benefit**: Provides "Insights" about implementation choices and codebase patterns

### 2. Training Junior Developers
**Use**: Learning output style
**Benefit**: Collaborative learning + `TODO(human)` markers

### 3. Writing Documentation
**Use**: Custom output style (keep-coding-instructions: false)
**Benefit**: Focus on documentation, not coding

### 4. Code Review
**Use**: Custom output style focused on review
**Benefit**: Consistent review format and tone

### 5. API Development
**Use**: Custom output style for API design
**Benefit**: Consistent API documentation and response format

---

## 🔄 vs Related Features Summary

| Feature | Modifies Default System Prompt? | Always Active? | Use Case |
|---------|--------------------------------|----------------|----------|
| **Output Styles** | Yes (turn off SE parts) | Yes (once selected) | Formatting, tone, structure |
| **CLAUDE.md** | No (adds user message) | Yes | Project context |
| **--append-system-prompt** | No (appends to prompt) | Yes | Additional instructions |
| **Agents** | No (invoked for tasks) | No (task-specific) | Task delegation |
| **Skills** | No (task-specific prompts) | No (invoked or auto-loaded) | Reusable workflows |

**Choose based on needs**:
- **Modify behavior** → Output styles
- **Add context** → CLAUDE.md
- **Append instructions** → --append-system-prompt
- **Delegate tasks** → Agents
- **Reusable workflows** → Skills

---

## 🏷️ 标签
`#output-styles` `#system-prompt` `#customization` `#explanatory` `#learning` `#claude-md` `#agents` `#skills` `#formatting` `#tone`
