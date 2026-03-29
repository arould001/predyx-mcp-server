# 20 - Plugins 学习笔记

**学习时间**：2026-03-14 15:28
**页面地址**：https://code.claude.com/docs/en/plugins

---

## 📖 核心概念

### 是什么
**Plugins** 是可共享的 Claude Code 扩展，包含 skills, agents, hooks, MCP servers, LSP servers。通过 marketplace 分发，跨项目复用。

### vs Standalone Configuration

| 方面 | Standalone (.claude/) | Plugin (.claude-plugin/) |
|------|----------------------|--------------------------|
| **Skill names** | `/hello` | `/plugin-name:hello` |
| **Scope** | 单项目 | 跨项目共享 |
| **Distribution** | 手动复制 | Marketplace 安装 |
| **Versioning** | 无 | Semantic versioning |
| **Best for** | Personal workflows, experiments | Team sharing, community distribution |

**选择建议**：
- **Standalone**：单项目定制、个人工作流、快速实验
- **Plugin**：团队共享、跨项目复用、版本控制、marketplace 分发

**Workflow**：Start with `.claude/` → Convert to plugin when ready to share.

---

## 🚀 Quickstart（5 步创建第一个 Plugin）

### Prerequisites
- Claude Code v1.0.33+
- Authenticated

### Step 1: Create Plugin Directory
```bash
mkdir my-first-plugin
```

### Step 2: Create Plugin Manifest
```bash
mkdir my-first-plugin/.claude-plugin
```

**my-first-plugin/.claude-plugin/plugin.json**:
```json
{
  "name": "my-first-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

**Manifest Fields**:

| Field | Purpose |
|-------|---------|
| `name` | Unique identifier + skill namespace (`/my-first-plugin:hello`) |
| `description` | Shown in plugin manager |
| `version` | Semantic versioning for releases |
| `author` | Optional, for attribution |

### Step 3: Add a Skill
```bash
mkdir -p my-first-plugin/skills/hello
```

**my-first-plugin/skills/hello/SKILL.md**:
```markdown
---
description: Greet the user with a friendly message
disable-model-invocation: true
---

Greet the user warmly and ask how you can help them today.
```

### Step 4: Test Your Plugin
```bash
claude --plugin-dir ./my-first-plugin
```

**Test skill**:
```
/my-first-plugin:hello
```

**Why namespacing?**
- Plugin skills are **always namespaced** (`/greet:hello`)
- Prevents conflicts when multiple plugins have skills with the same name
- To change namespace prefix → update `name` in `plugin.json`

### Step 5: Add Skill Arguments
**Update SKILL.md**:
```markdown
---
description: Greet the user with a personalized message
---

# Hello Skill

Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
```

**Test with argument**:
```
/my-first-plugin:hello Alex
```

**Reload changes**:
```
/reload-plugins
```

**Key Components Created**:
- Plugin manifest (`.claude-plugin/plugin.json`)
- Skills directory (`skills/`)
- Skill arguments (`$ARGUMENTS`)

---

## 📁 Plugin Structure Overview

### ⚠️ Common Mistake
**Don't put these inside `.claude-plugin/`**:
- `commands/`
- `agents/`
- `skills/`
- `hooks/`

**Only `plugin.json` goes inside `.claude-plugin/`**. All other directories must be at **plugin root level**.

### Directory Structure

| Directory | Location | Purpose |
|-----------|----------|---------|
| `.claude-plugin/` | Plugin root | Contains `plugin.json` manifest |
| `commands/` | Plugin root | Skills as Markdown files |
| `agents/` | Plugin root | Custom agent definitions |
| `skills/` | Plugin root | Agent Skills with `SKILL.md` files |
| `hooks/` | Plugin root | Event handlers in `hooks.json` |
| `.mcp.json` | Plugin root | MCP server configurations |
| `.lsp.json` | Plugin root | LSP server configurations for code intelligence |
| `settings.json` | Plugin root | Default settings applied when plugin is enabled |

---

## 🛠️ Develop More Complex Plugins

### Add Skills to Your Plugin

**Structure**:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

**SKILL.md Example**:
```markdown
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

**After installing**:
```
/reload-plugins
```

**For complete Skill authoring** → see [Agent Skills](#agent-skills)

### Add LSP Servers to Your Plugin

**Recommendation**: For common languages (TypeScript, Python, Rust), **install pre-built LSP plugins from official marketplace**. Create custom LSP plugins only for languages not covered.

**.lsp.json**:
```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Note**: Users must have the language server binary installed.

**For complete LSP configuration** → see [LSP servers](#lsp-servers)

### Ship Default Settings with Your Plugin

**settings.json** (plugin root):
```json
{
  "agent": "security-reviewer"
}
```

**Supported key**: Currently only `agent` is supported.

**What it does**:
- Activates one of the plugin's custom agents as the main thread
- Applies its system prompt, tool restrictions, and model
- Lets plugin change how Claude Code behaves by default when enabled

**Priority**: Settings from `settings.json` **take priority over** settings declared in `plugin.json`. Unknown keys are silently ignored.

### Organize Complex Plugins

For plugins with many components, organize directory structure by functionality.

**For complete directory layouts** → see [Plugin directory structure](#plugin-directory-structure)

---

## 🧪 Test Your Plugins Locally

### Use --plugin-dir Flag
```bash
claude --plugin-dir ./my-plugin
```

**What it does**:
- Loads plugin directly **without requiring installation**
- Local copy takes precedence over installed marketplace plugin with same name
- Lets you test changes without uninstalling first

**Exception**: Marketplace plugins **force-enabled by managed settings** cannot be overridden.

### Reload Changes
```
/reload-plugins
```

**What it does**:
- Picks up updates without restarting
- **Exception**: Changes to LSP server configuration still require full restart

### Test Plugin Components
- ✅ Try skills: `/plugin-name:skill-name`
- ✅ Check agents: `/agents`
- ✅ Verify hooks: trigger expected events

### Load Multiple Plugins
```bash
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

---

## 🐛 Debug Plugin Issues

### Troubleshooting Checklist
1. ✅ **Check structure**: Ensure directories are at plugin root, **not inside** `.claude-plugin/`
2. ✅ **Test components individually**: Check each command, agent, and hook separately
3. ✅ **Use validation and debugging tools**: See [Debugging and development tools](#debugging-and-development-tools)

---

## 📤 Share Your Plugins

### When Your Plugin is Ready
1. ✅ **Add documentation**: Include `README.md` with installation and usage instructions
2. ✅ **Version your plugin**: Use semantic versioning in `plugin.json`
3. ✅ **Create or use a marketplace**: Distribute through plugin marketplaces
4. ✅ **Test with others**: Have team members test before wider distribution

**Once in marketplace** → others can install via [Discover and install plugins](#discover-and-install-plugins)

### Submit to Official Marketplace

**In-app submission forms**:
- **Claude.ai**: `claude.ai/settings/plugins/submit`
- **Console**: `platform.claude.com/plugins/submit`

**For complete specs, debugging, distribution** → see [Plugins reference](#plugins-reference)

---

## 🔄 Convert Existing Configurations to Plugins

### Migration Steps

#### 1. Create Plugin Structure
```bash
mkdir -p my-plugin/.claude-plugin
```

**my-plugin/.claude-plugin/plugin.json**:
```json
{
  "name": "my-plugin",
  "description": "Migrated from standalone configuration",
  "version": "1.0.0"
}
```

#### 2. Copy Existing Files
```bash
# Copy commands
cp -r .claude/commands my-plugin/

# Copy agents (if any)
cp -r .claude/agents my-plugin/

# Copy skills (if any)
cp -r .claude/skills my-plugin/
```

#### 3. Migrate Hooks
```bash
mkdir my-plugin/hooks
```

**my-plugin/hooks/hooks.json**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
      }
    ]
  }
}
```

**Note**:
- Copy `hooks` object from `.claude/settings.json` or `settings.local.json`
- Format is the same
- Hook command receives input as JSON on stdin (use `jq` to extract)

#### 4. Test Migrated Plugin
```bash
claude --plugin-dir ./my-plugin
```

**Test each component**:
- Run commands
- Check agents in `/agents`
- Verify hooks trigger correctly

### What Changes When Migrating

| Aspect | Standalone (.claude/) | Plugin |
|--------|----------------------|--------|
| **Availability** | Only one project | Can be shared via marketplaces |
| **File location** | `.claude/commands/` | `plugin-name/commands/` |
| **Hooks location** | `settings.json` | `hooks/hooks.json` |
| **Distribution** | Must manually copy | Install with `/plugin install` |

**After migrating** → remove original files from `.claude/` to avoid duplicates. Plugin version takes precedence when loaded.

---

## 💡 学习感悟

### 1. **Plugin 是 Claude Code 的核心扩展机制**
**Plugin vs Standalone**:
- **Standalone** (`.claude/`): 单项目、个人工作流、快速实验
- **Plugin** (`.claude-plugin/`): 团队共享、跨项目、版本控制、marketplace 分发

**核心差异**：
- Skill namespacing（`/plugin:skill`）
- Marketplace 安装（`/plugin install`）
- Semantic versioning
- 可共享性

**工作流**：Start with `.claude/` → Convert to plugin when ready to share.

### 2. **Plugin Manifest 是核心配置**
**plugin.json 定义了**：
- `name`: Unique identifier + skill namespace
- `description`: Shown in plugin manager
- `version`: Semantic versioning for releases
- `author`: Optional, for attribution

**关键**：`name` 字段决定 skill namespace (`/my-plugin:hello`).

### 3. **Plugin Structure 的常见错误**
**不要把子目录放在 `.claude-plugin/` 里面**：
- ❌ `.claude-plugin/commands/`
- ❌ `.claude-plugin/skills/`
- ❌ `.claude-plugin/agents/`

**正确位置**：Plugin root level.
- ✅ `my-plugin/commands/`
- ✅ `my-plugin/skills/`
- ✅ `my-plugin/agents/`

**只有 `plugin.json` 在 `.claude-plugin/` 里**。

### 4. **--plugin-dir 是开发和测试的关键**
**Test locally without installation**:
```bash
claude --plugin-dir ./my-plugin
```

**优势**：
- Local copy takes precedence over installed marketplace plugin
- Test changes without uninstalling
- `/reload-plugins` picks up updates without restart

**Exception**: Managed settings force-enabled plugins cannot be overridden.

### 5. **Migration from Standalone is Straightforward**
**Convert `.claude/` to plugin**:
1. Create plugin structure (`mkdir -p my-plugin/.claude-plugin`)
2. Create manifest (`plugin.json`)
3. Copy files (`cp -r .claude/commands my-plugin/`)
4. Migrate hooks (`hooks/hooks.json`)
5. Test (`claude --plugin-dir ./my-plugin`)

**After migrating** → remove original files from `.claude/`.

### 6. **Official Marketplace Submission**
**Two submission forms**:
- **Claude.ai**: `claude.ai/settings/plugins/submit`
- **Console**: `platform.claude.com/plugins/submit`

**Requirement**: Semantic versioning, `README.md`, tested by team members.

---

## 🎯 实践建议

### 1. **Start with Standalone, Convert to Plugin**
```bash
# Quick experiment in .claude/
mkdir -p .claude/commands
# ... create skills ...

# When ready to share, convert to plugin
mkdir -p my-plugin/.claude-plugin
cp -r .claude/commands my-plugin/
# ... create plugin.json ...
```

### 2. **Use Semantic Versioning**
```json
{
  "name": "my-plugin",
  "version": "1.0.0"  // major.minor.patch
}
```

**Versioning strategy**:
- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes

### 3. **Test Components Individually**
```bash
# Test skills
/my-plugin:skill-name

# Check agents
/agents

# Verify hooks
# Trigger expected events
```

### 4. **Add README.md**
```markdown
# My Plugin

## Installation
/plugin install my-plugin

## Usage
/my-plugin:hello

## Skills
- `hello`: Greet the user

## License
MIT
```

### 5. **Organize Complex Plugins by Functionality**
```
my-complex-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── code-review/
│   └── test-generator/
├── agents/
│   ├── security-reviewer/
│   └── performance-analyzer/
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
└── settings.json
```

### 6. **Ship Default Settings**
**settings.json**:
```json
{
  "agent": "security-reviewer"  // Activate custom agent by default
}
```

**Use case**: Plugin that changes Claude Code's default behavior.

---

## 📚 Next Steps

### For Plugin Users
- **Discover and install plugins**: browse marketplaces and install
- **Configure team marketplaces**: set up repository-level plugins

### For Plugin Developers
- **Create and distribute a marketplace**: package and share
- **Plugins reference**: complete technical specifications

### Dive Deeper into Components
- **Skills**: skill development details
- **Subagents**: agent configuration and capabilities
- **Hooks**: event handling and automation
- **MCP**: external tool integration

---

## 🏷️ 标签
`#plugins` `#extension-system` `#marketplace` `#skills` `#agents` `#hooks` `#lsp` `#distribution` `#semantic-versioning`
