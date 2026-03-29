# 21 - Discover and Install Plugins 学习笔记

**学习时间**：2026-03-14 15:42
**页面地址**：https://code.claude.com/docs/en/discover-plugins

---

## 📖 核心概念

### 是什么
**Plugin Marketplaces** 是插件目录，帮助发现和安装 Claude Code 扩展，无需自己构建。

### 工作流程（2步）
1. **Add the marketplace** → 注册目录到 Claude Code（不安装任何插件）
2. **Install individual plugins** → 浏览目录并安装需要的插件

**比喻**：像添加应用商店 → 可以浏览收藏，但仍需选择下载哪些应用。

---

## 🏢 Official Anthropic Marketplace

### 自动可用
- **claude-plugins-official** 在启动 Claude Code 时自动可用
- 运行 `/plugin` → Discover tab 浏览

### 安装插件
```
/plugin install plugin-name@claude-plugins-official
```

### 提交插件
**In-app submission forms**:
- **Claude.ai**: `claude.ai/settings/plugins/submit`
- **Console**: `platform.claude.com/plugins/submit`

**独立分发** → 创建自己的 marketplace。

### 官方插件分类

#### 1. Code Intelligence（LSP 插件）
**功能**：启用 Claude Code 的内置 LSP 工具，实时跳转到定义、查找引用、查看类型错误。

**原理**：配置 Language Server Protocol 连接（与 VS Code 相同技术）。

**要求**：语言服务器二进制文件必须安装在系统上。

**支持语言**：

| Language | Plugin | Binary Required |
|----------|--------|-----------------|
| C/C++ | `clangd-lsp` | `clangd` |
| C# | `csharp-lsp` | `csharp-ls` |
| Go | `gopls-lsp` | `gopls` |
| Java | `jdtls-lsp` | `jdtls` |
| Kotlin | `kotlin-lsp` | `kotlin-language-server` |
| Lua | `lua-lsp` | `lua-language-server` |
| PHP | `php-lsp` | `intelephense` |
| Python | `pyright-lsp` | `pyright-langserver` |
| Rust | `rust-analyzer-lsp` | `rust-analyzer` |
| Swift | `swift-lsp` | `sourcekit-lsp` |
| TypeScript | `typescript-lsp` | `typescript-language-server` |

**错误提示**：`Executable not found in $PATH` → 安装所需二进制文件。

#### Claude 从 Code Intelligence 插件获得的能力

**1. Automatic diagnostics**:
- 每次文件编辑后，语言服务器自动分析更改并报告错误和警告
- Claude 看到类型错误、缺失导入、语法问题（无需运行编译器或 linter）
- 如果 Claude 引入错误，它会在同一 turn 中注意到并修复
- **零配置**（只需安装插件）
- 按 `Ctrl+O` 查看 "diagnostics found" 指示器时可以看到诊断

**2. Code navigation**:
- Jump to definitions
- Find references
- Get type info on hover
- List symbols
- Find implementations
- Trace call hierarchies

**比基于 grep 的搜索更精确**（可用性因语言和环境而异）。

**遇到问题** → see [Code intelligence troubleshooting](#code-intelligence-troubleshooting)

#### 2. External Integrations（MCP 插件）
**功能**：捆绑预配置的 MCP servers，无需手动设置即可连接外部服务。

**支持服务**：
- **Source control**: `github`, `gitlab`
- **Project management**: `atlassian` (Jira/Confluence), `asana`, `linear`, `notion`
- **Design**: `figma`
- **Infrastructure**: `vercel`, `firebase`, `supabase`
- **Communication**: `slack`
- **Monitoring**: `sentry`

#### 3. Development Workflows
**功能**：为常见开发任务添加命令和 agents。

**插件**：
- `commit-commands`: Git commit workflows（commit, push, PR creation）
- `pr-review-toolkit`: Specialized agents for reviewing pull requests
- `agent-sdk-dev`: Tools for building with Claude Agent SDK
- `plugin-dev`: Toolkit for creating your own plugins

#### 4. Output Styles
**功能**：自定义 Claude 的响应方式。

**插件**：
- `explanatory-output-style`: Educational insights about implementation choices
- `learning-output-style`: Interactive learning mode for skill building

---

## 🎓 Try It: Add Demo Marketplace

### Anthropic Demo Marketplace
**claude-code-plugins** - 展示插件系统可能性的示例插件。

**需要手动添加**（不像官方 marketplace 自动可用）。

### Step 1: Add Marketplace
```
/plugin marketplace add anthropics/claude-code
```

下载 marketplace 目录，插件变为可用。

### Step 2: Browse Available Plugins
```
/plugin
```

**Plugin Manager 界面（4个标签）**：
- **Discover**: 浏览所有 marketplaces 的可用插件
- **Installed**: 查看和管理已安装插件
- **Marketplaces**: 添加、移除或更新 marketplaces
- **Errors**: 查看插件加载错误

**导航**：`Tab` 循环（`Shift+Tab` 向后）。

**Discover tab** → 查看刚添加的 marketplace 插件。

### Step 3: Install a Plugin
**选择插件 → 选择安装 scope**：
- **User scope**: 为自己跨所有项目安装
- **Project scope**: 为此仓库的所有协作者安装
- **Local scope**: 为自己在此仓库安装（不与协作者共享）

**Example**: 安装 `commit-commands`（添加 git workflow 命令）→ User scope。

**CLI 安装**:
```
/plugin install commit-commands@anthropics-claude-code
```

**更多信息** → see [Configuration scopes](#configuration-scopes)

### Step 4: Use Your New Plugin
**插件命令立即可用**（命名空间为插件名称）。

**commit-commands 提供的命令**:
```
/commit-commands:commit
```

**功能**：stage 更改、生成 commit 消息、创建 commit。

**每个插件工作方式不同** → 查看 Discover tab 描述或 homepage 了解提供的命令和能力。

---

## 📦 Add Marketplaces

### Shortcut
- `/plugin market` instead of `/plugin marketplace`
- `rm` instead of `remove`

### 支持的来源

| Source | Format | Example |
|--------|--------|---------|
| GitHub repositories | `owner/repo` | `anthropics/claude-code` |
| Git URLs | Any git repository URL | GitLab, Bitbucket, self-hosted |
| Local paths | Directories or paths to `marketplace.json` | `./my-marketplace` |
| Remote URLs | Direct URLs to hosted `marketplace.json` | `https://example.com/marketplace.json` |

### Add from GitHub
**要求**：GitHub repo 包含 `.claude-plugin/marketplace.json`

**Format**: `owner/repo` (owner = GitHub username/org, repo = repository name)

```
/plugin marketplace add anthropics/claude-code
```

### Add from Other Git Hosts
**支持**：GitLab, Bitbucket, self-hosted servers

**HTTPS**:
```
/plugin marketplace add https://gitlab.com/company/plugins.git
```

**SSH**:
```
/plugin marketplace add git@gitlab.com:company/plugins.git
```

**Specific branch/tag**（附加 `#` + ref）:
```
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Add from Local Paths
**要求**：目录包含 `.claude-plugin/marketplace.json`

**Directory**:
```
/plugin marketplace add ./my-marketplace
```

**Direct path to marketplace.json**:
```
/plugin marketplace add ./path/to/marketplace.json
```

### Add from Remote URLs
**Direct URL to marketplace.json**:
```
/plugin marketplace add https://example.com/marketplace.json
```

**Limitations**: URL-based marketplaces 有一些限制（vs Git-based）。如果遇到 "path not found" 错误 → see [Troubleshooting](#troubleshooting)

---

## 🔧 Install Plugins

### Default Installation (User Scope)
```
/plugin install plugin-name@marketplace-name
```

### Choose Different Scope
**Interactive UI**:
1. Run `/plugin`
2. Go to **Discover tab**
3. Press `Enter` on a plugin
4. Choose scope:
   - **User scope** (default): 为自己跨所有项目安装
   - **Project scope**: 为此仓库所有协作者安装（添加到 `.claude/settings.json`）
   - **Local scope**: 为自己在此仓库安装（不与协作者共享）

**Managed scope**: 管理员通过 managed settings 安装，无法修改。

**View installed plugins**:
```
/plugin
```
→ **Installed tab** (grouped by scope)

### ⚠️ Security Warning
**在安装前确保信任插件**。

Anthropic **不控制** 插件包含的 MCP servers、文件或其他软件，**无法验证** 它们是否按预期工作。

**检查每个插件的 homepage 了解更多信息**。

---

## 🛠️ Manage Installed Plugins

### Interactive UI
**Run `/plugin` → Installed tab**:
- View
- Enable
- Disable
- Uninstall

**Type to filter** by plugin name or description.

### CLI Commands

**Disable (without uninstalling)**:
```
/plugin disable plugin-name@marketplace-name
```

**Re-enable**:
```
/plugin enable plugin-name@marketplace-name
```

**Completely remove**:
```
/plugin uninstall plugin-name@marketplace-name
```

**Target specific scope**:
```bash
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

---

## 🔄 Apply Plugin Changes Without Restarting

### When Changes Take Effect
- **Immediately**: New commands and hooks
- **Require restart**: LSP server updates

### Reload All Active Plugins
```
/reload-plugins
```

**What it does**:
- Reloads all active plugins
- Reports what was loaded
- Notifies if LSP servers were added/updated (require restart)

---

## 📋 Manage Marketplaces

### Interactive Interface
**Run `/plugin` → Marketplaces tab**:
- View all added marketplaces with sources and status
- Add new marketplaces
- Update marketplace listings (fetch latest plugins)
- Remove marketplaces no longer needed

### CLI Commands

**List all configured marketplaces**:
```
/plugin marketplace list
```

**Refresh plugin listings**:
```
/plugin marketplace update marketplace-name
```

**Remove a marketplace**:
```
/plugin marketplace remove marketplace-name
```

**Warning**: Removing marketplace will **uninstall** any plugins you installed from it.

---

## 🔄 Configure Auto-Updates

### What Auto-Update Does
- **Refreshes marketplace data** at startup
- **Updates installed plugins** to latest versions
- **Notifies** if plugins were updated → prompt to run `/reload-plugins`

### Toggle Auto-Update (Interactive UI)
1. Run `/plugin`
2. Select **Marketplaces**
3. Choose a marketplace
4. Select **Enable auto-update** or **Disable auto-update**

### Default Behavior
- **Official Anthropic marketplaces**: Auto-update enabled by default
- **Third-party and local development marketplaces**: Auto-update disabled by default

### Disable All Auto-Updates
**Environment variable**:
```bash
export DISABLE_AUTOUPDATER=true
```

**See** [Auto updates](#auto-updates) for details.

### Keep Plugin Auto-Updates, Disable Claude Code Auto-Updates
```bash
export DISABLE_AUTOUPDATER=true
export FORCE_AUTOUPDATE_PLUGINS=true
```

**Use case**: 手动管理 Claude Code 更新，但仍接收自动插件更新。

---

## 👥 Configure Team Marketplaces

### Team Admin Setup
**Add marketplace configuration to `.claude/settings.json`**:

```json
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

### How It Works
- Team members trust the repository folder
- Claude Code prompts to install these marketplaces and plugins

**Full configuration options** → see [Plugin settings](#plugin-settings) (includes `extraKnownMarketplaces` and `enabledPlugins`)

---

## 🛡️ Security

### ⚠️ High Trust Components
**Plugins and marketplaces are highly trusted**:
- Can execute **arbitrary code** on your machine
- With **your user privileges**

### Only Install from Trusted Sources
**Before installing**:
- ✅ Trust the source
- ✅ Check plugin's homepage
- ✅ Understand what it does

**Organizations** can restrict which marketplaces users are allowed to add using **managed marketplace restrictions**.

---

## 🐛 Troubleshooting

### /plugin Command Not Recognized
**Symptoms**: "unknown command" or `/plugin` doesn't appear

**Check version**:
```bash
claude --version
```
**Requires**: v1.0.33 or later

**Update Claude Code**:
```bash
# Homebrew
brew upgrade claude-code

# npm
npm update -g @anthropic-ai/claude-code

# Native installer
# Re-run install command from Setup
```

**Restart**:
- After updating, restart terminal
- Run `claude` again

### Common Issues

**Marketplace not loading**:
- Verify URL is accessible
- Check `.claude-plugin/marketplace.json` exists at the path

**Plugin installation failures**:
- Check plugin source URLs are accessible
- Verify repositories are public (or you have access)

**Files not found after installation**:
- Plugins are copied to cache
- Paths referencing files outside plugin directory won't work

**Plugin skills not appearing**:
```bash
rm -rf ~/.claude/plugins/cache
# Restart Claude Code
# Reinstall plugin
```

**Detailed troubleshooting** → see [Troubleshooting](#troubleshooting) in marketplace guide

**Debugging tools** → see [Debugging and development tools](#debugging-and-development-tools)

### Code Intelligence Issues

**Language server not starting**:
- Verify binary is installed and in `$PATH`
- Check `/plugin` Errors tab for details

**High memory usage**:
- Language servers like `rust-analyzer` and `pyright` can consume significant memory on large projects
- If memory issues: `/plugin disable <plugin-name>`
- Rely on Claude's built-in search tools instead

**False positive diagnostics in monorepos**:
- Language servers may report unresolved import errors for internal packages if workspace isn't configured correctly
- These don't affect Claude's ability to edit code

---

## 💡 学习感悟

### 1. **Marketplace 是 Plugin 分发的核心**
**2步流程**：
1. Add marketplace（注册目录）
2. Install individual plugins（按需安装）

**比喻**：像应用商店 → 可以浏览收藏，但仍需选择下载哪些应用。

**关键**：Adding marketplace ≠ Installing plugins.

### 2. **Official Anthropic Marketplace 自动可用**
**claude-plugins-official**:
- 启动时自动可用
- 包含 LSP plugins, MCP integrations, development workflows, output styles
- Maintained by Anthropic

**安装**:
```
/plugin install plugin-name@claude-plugins-official
```

**提交插件到官方 marketplace**:
- Claude.ai: `claude.ai/settings/plugins/submit`
- Console: `platform.claude.com/plugins/submit`

### 3. **Code Intelligence 是 LSP 插件的核心能力**
**Language Server Protocol**:
- 与 VS Code 相同技术
- 支持 11 种语言（C/C++, C#, Go, Java, Kotlin, Lua, PHP, Python, Rust, Swift, TypeScript）

**Claude 获得的能力**：
1. **Automatic diagnostics**: 每次编辑后自动报告错误和警告
2. **Code navigation**: Jump to definitions, find references, type info, etc.

**要求**：语言服务器二进制文件必须安装在系统上。

**错误提示**：`Executable not found in $PATH` → 安装所需二进制。

### 4. **Installation Scopes 是关键概念**
**3种 scopes**:
- **User scope**: 跨所有项目（自己）
- **Project scope**: 此仓库所有协作者（添加到 `.claude/settings.json`）
- **Local scope**: 此仓库（自己，不共享）

**Managed scope**: 管理员通过 managed settings 安装，无法修改。

**View by scope**: `/plugin` → Installed tab (grouped by scope)

### 5. **Auto-Updates 可配置**
**默认行为**:
- Official Anthropic marketplaces: Auto-update enabled
- Third-party/local: Auto-update disabled

**Toggle via UI**: `/plugin` → Marketplaces → Enable/Disable auto-update

**Environment variables**:
```bash
# Disable all auto-updates
export DISABLE_AUTOUPDATER=true

# Keep plugin updates, disable Claude Code updates
export DISABLE_AUTOUPDATER=true
export FORCE_AUTOUPDATE_PLUGINS=true
```

### 6. **Security 是首要考虑**
**Plugins are highly trusted**:
- Can execute arbitrary code
- With your user privileges

**最佳实践**：
- ✅ Only install from trusted sources
- ✅ Check plugin's homepage
- ✅ Understand what it does

**Organizations**: 可以限制允许的 marketplaces。

### 7. **/reload-plugins 是关键命令**
**应用更改而无需重启**:
```
/reload-plugins
```

**What it does**:
- Reloads all active plugins
- Reports what was loaded
- Notifies if LSP servers updated (require restart)

**Exception**: LSP server updates still require restart.

### 8. **Team Marketplaces 支持团队协作**
**Team admin setup**:
```json
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

**Flow**: Team members trust repo → Claude Code prompts to install.

---

## 🎯 实践建议

### 1. **Start with Official Marketplace**
```
/plugin
```
→ Discover tab → Browse official plugins

### 2. **Install LSP Plugins for Your Languages**
```
# Python
/plugin install pyright-lsp@claude-plugins-official

# TypeScript
/plugin install typescript-lsp@claude-plugins-official

# Rust
/plugin install rust-analyzer-lsp@claude-plugins-official
```

**Verify binary installed**:
```bash
pyright-langserver --version
typescript-language-server --version
rust-analyzer --version
```

### 3. **Try Demo Marketplace**
```
/plugin marketplace add anthropics/claude-code
/plugin install commit-commands@anthropics-claude-code
/commit-commands:commit
```

### 4. **Use Interactive UI for Scopes**
```
/plugin
```
→ Discover tab → Enter on plugin → Choose scope

### 5. **Configure Auto-Updates**
```
/plugin
```
→ Marketplaces → Enable/Disable auto-update

### 6. **Set Up Team Marketplaces**
**Project `.claude/settings.json`**:
```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

### 7. **Troubleshoot Issues**
```bash
# Check version
claude --version

# Clear cache if skills not appearing
rm -rf ~/.claude/plugins/cache

# Reload plugins
/reload-plugins
```

### 8. **Disable High-Memory LSP Plugins**
```
/plugin disable rust-analyzer-lsp@claude-plugins-official
```

**Use Claude's built-in search instead**.

---

## 📚 Next Steps

### Build Your Own Plugins
- See [Plugins](#plugins) to create skills, agents, hooks

### Create a Marketplace
- See [Create a plugin marketplace](#create-a-plugin-marketplace) to distribute plugins to team or community

### Technical Reference
- See [Plugins reference](#plugins-reference) for complete specifications

---

## 🏷️ 标签
`#marketplaces` `#plugin-installation` `#lsp` `#code-intelligence` `#mcp` `#scopes` `#auto-updates` `#team-configuration` `#security` `#troubleshooting`
