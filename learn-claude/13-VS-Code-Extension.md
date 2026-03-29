# 13 - VS Code Extension 学习笔记

**学习时间**：2026-03-14 14:50
**页面地址**：https://code.claude.com/docs/en/vs-code

---

## 📖 核心要点

### 是什么
Claude Code 的 VS Code 原生扩展，提供图形界面直接集成到 IDE 中。

### Prerequisites
- VS Code 1.98.0+
- Anthropic 账户
- 扩展包含 CLI，可从 VS Code 终端访问

---

## 🚀 Get Started

### 安装

**方式 1：直接安装**
- VS Code：`vscode:extension/anthropic.claude-code`
- Cursor：`cursor:extension/anthropic.claude-code`

**方式 2：扩展市场**
- `Cmd+Shift+X` (Mac) / `Ctrl+Shift+X` (Windows/Linux)
- 搜索 "Claude Code"
- 点击 Install

### 打开 Claude Code

**Spark 图标位置**：
1. **Editor Toolbar** - 编辑器右上角（最常用，需打开文件）
2. **Activity Bar** - 左侧边栏的 Spark 图标
3. **Command Palette** - `Cmd+Shift+P` → "Claude Code"
4. **Status Bar** - 右下角 "✱ Claude Code"

### 第一次使用

**Learn Claude Code checklist**：
- 首次打开会显示学习清单
- 点击 "Show me" 逐步学习
- 可随时在设置中重新启用

---

## 💡 核心功能

### 1. Prompt Box

**Permission Modes**：
- **Normal** - 每次操作前询问
- **Plan Mode** - Claude 描述将要做什么，等待批准
- **Auto-accept** - Claude 自动编辑，不询问

**Command Menu**：
- 输入 `/` 打开
- 包含：附加文件、切换模型、extended thinking、查看使用情况
- Customize：MCP servers、hooks、memory、permissions、plugins

**Context Indicator**：
- 显示上下文窗口使用量
- Claude 自动压缩，或手动 `/compact`

**Extended Thinking**：
- 让 Claude 花更多时间推理复杂问题
- 通过命令菜单 (`/`) 切换

**Multi-line Input**：
- `Shift+Enter` 换行不发送

### 2. Reference Files and Folders

**@-mentions**：
- `@filename` - 引用文件
- `@folder/` - 引用文件夹（trailing slash）
- Fuzzy matching - 支持模糊匹配

**Selection**：
- 选中代码时 Claude 自动看到
- `Option+K` (Mac) / `Alt+K` (Windows/Linux) 插入 @-mention 引用
- 格式：`@app.ts#5-10`

**Large PDFs**：
- 可指定页面：单页、范围（1-10）、开放范围（3 onward）

**Attachments**：
- `Shift` + 拖放文件 → 附加
- 点击 X 移除

### 3. Resume Past Conversations

**Local Sessions**：
- 点击顶部下拉菜单访问历史
- 按时间浏览（Today、Yesterday、Last 7 days）
- Hover 显示 rename 和 remove 操作

**Remote Sessions**：
- 从 claude.ai 恢复远程会话
- 需要 Claude.ai Subscription（不是 Console）
- "Past Conversations" → "Remote" tab
- 下载并本地继续

### 4. Customize Your Workflow

**Choose Where Claude Lives**：
- **Secondary sidebar** - 右侧（推荐）
- **Primary sidebar** - 左侧
- **Editor area** - 作为标签页

**Run Multiple Conversations**：
- "Open in New Tab" / "Open in New Window"
- 每个会话独立历史和上下文
- 彩色点指示状态：蓝色（权限请求）、橙色（完成）

**Switch to Terminal Mode**：
- 设置：`claudeCode.useTerminal`
- CLI 风格界面

---

## 🎨 Manage Plugins

**`/plugins` 命令**：
- 打开图形化插件管理界面

**Plugins Tab**：
- Installed plugins - 顶部，带开关
- Available plugins - 下方，可搜索
- Install 按钮

**Installation Scope**：
- **Install for you** - 所有项目（user scope）
- **Install for this project** - 项目共享（project scope）
- **Install locally** - 仅本地（local scope）

**Marketplaces Tab**：
- 添加 GitHub repo、URL、本地路径
- 刷新插件列表
- 删除 marketplace

---

## 🌐 Automate Browser Tasks with Chrome

**要求**：Claude in Chrome extension v1.0.36+

**用法**：
```bash
@browser go to localhost:3000 and check the console for errors
```

**功能**：
- 测试 web apps
- 调试 console logs
- 自动化浏览器工作流
- 共享浏览器登录状态

---

## ⌨️ VS Code Commands and Shortcuts

| Command | Shortcut | Description |
|---------|----------|-------------|
| Focus Input | `Cmd+Esc` / `Ctrl+Esc` | 切换 editor 和 Claude 焦点 |
| Open in New Tab | `Cmd+Shift+Esc` / `Ctrl+Shift+Esc` | 新标签页打开新会话 |
| New Conversation | `Cmd+N` / `Ctrl+N` | 开始新会话（Claude focused） |
| Insert @-Mention | `Option+K` / `Alt+K` | 插入文件和选择引用（editor focused） |
| Open in Side Bar | - | 在左侧边栏打开 |
| Open in Terminal | - | 终端模式打开 |

---

## ⚙️ Configure Settings

### Extension Settings (VS Code)

**重要设置**：

| Setting | Default | Description |
|---------|---------|-------------|
| `selectedModel` | `default` | 新会话模型（可用 `/model` 更改） |
| `useTerminal` | `false` | 终端模式而非图形面板 |
| `initialPermissionMode` | `default` | 权限模式：default/plan/acceptEdits/bypassPermissions |
| `preferredLocation` | `panel` | 打开位置：sidebar/panel |
| `autosave` | `true` | Claude 读写前自动保存 |
| `useCtrlEnterToSend` | `false` | 用 Ctrl/Cmd+Enter 发送而非 Enter |
| `hideOnboarding` | `false` | 隐藏学习清单 |

### Claude Code Settings (~/.claude/settings.json)

**共享设置**：
- Extension 和 CLI 共享
- 包括：allowed commands、environment variables、hooks、MCP servers

**JSON Schema**：
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```

---

## 🔄 VS Code Extension vs CLI

| Feature | CLI | VS Code Extension |
|---------|-----|------------------|
| **Commands and skills** | All | Subset |
| **MCP server config** | Yes | Partial（CLI 添加，`/mcp` 管理） |
| **Checkpoints** | Yes | Yes |
| **`!` bash shortcut** | Yes | No |
| **Tab completion** | Yes | No |

### Rewind with Checkpoints

**Hover 任何消息显示 rewind 按钮**：
- **Fork conversation from here** - 从此消息开始新分支，保留代码更改
- **Rewind code to here** - 回退文件更改到此点，保留完整对话历史
- **Fork conversation and rewind code** - 新分支 + 回退代码

### Run CLI in VS Code

**Integrated Terminal**：
- `Ctrl+\`` (Windows/Linux) / `Cmd+\`` (Mac)
- 运行 `claude`
- 自动集成 IDE（diff viewing、diagnostic sharing）

**External Terminal**：
- 运行 `/ide` 连接到 VS Code

### Include Terminal Output

```bash
@terminal:name
```

- `name` 是终端标题
- 让 Claude 看到命令输出、错误消息、日志

---

## 🔌 Connect to External Tools with MCP

**添加 MCP Server**：
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

**管理**：
- 在 chat panel 输入 `/mcp`
- Enable/disable servers
- Reconnect
- Manage OAuth

---

## 🌳 Work with Git

### Create Commits and Pull Requests

```bash
commit my changes with a descriptive message
create a pr for this feature
summarize the changes I've made to the auth module
```

### Use Git Worktrees

**隔离任务**：
```bash
claude --worktree feature-auth
```

**优势**：
- 独立文件状态
- 共享 git history
- 避免任务间干扰

---

## 🔐 Use Third-Party Providers

**支持的提供商**：
- Amazon Bedrock
- Google Vertex AI
- Microsoft Foundry

**配置**：
1. Disable Login Prompt（设置中）
2. 配置 provider（`~/.claude/settings.json`）

---

## 💡 学习感悟

### 1. **IDE 集成的深度**

VS Code extension 不是简单的聊天窗口，而是**深度集成**：
- **@-mentions** - 文件和代码引用
- **Diff View** - 内置差异审查
- **Checkpoints** - 回退机制
- **Terminal Integration** - 终端输出引用
- **Git Integration** - Commits、PRs、Worktrees

这体现了 **"Context is King"** 原则。

### 2. **多会话并行**

**Multiple Conversations** 解决了并行工作问题：
- New Tab / New Window
- 独立历史和上下文
- 状态指示器

这符合 **"Divide and Conquer"** 策略。

### 3. **Permission Modes 的灵活性**

三种 Permission Modes：
- **Normal** - 安全（默认）
- **Plan** - 先理解再执行
- **Auto-accept** - 快速迭代

**用户可以根据任务性质选择**，平衡安全与效率。

### 4. **Checkpoints 的价值**

**Checkpoints 提供了"后悔药"**：
- Fork conversation - 尝试不同方法
- Rewind code - 回退错误更改
- Combined - 两者结合

这是 **"Safe Experimentation"** 的关键。

### 5. **CLI vs Extension 的互补**

**CLI 和 Extension 不是竞争，而是互补**：
- **CLI** - 快速、脚本化、完整功能
- **Extension** - 可视化、集成、易用

**用户可以根据场景切换**，甚至在同一项目中同时使用。

### 6. **Terminal Output Reference**

**`@terminal:name` 的巧妙**：
- 无需复制粘贴
- Claude 直接读取终端输出
- 减少上下文切换

这是 **"减少认知负担"** 的设计。

---

## 🎯 实践建议

### 1. **从 Onboarding Checklist 开始**

- 首次打开时完成学习清单
- 逐步了解所有功能
- 可随时在设置中重新启用

### 2. **调整 Claude Panel 位置**

**推荐**：
- **Secondary Sidebar**（右侧） - 编码时可见
- **Editor Tab** - 并行任务时

### 3. **使用 @-mentions 精确引用**

```bash
# 文件
@auth.js

# 文件夹
@src/components/

# 特定行
@app.ts#5-10
```

### 4. **根据任务选择 Permission Mode**

**Normal**：
- 新项目
- 关键功能
- 学习阶段

**Plan**：
- 大型重构
- 多文件更改
- 需要先理解

**Auto-accept**：
- 熟悉项目
- 快速迭代
- 小修改

### 5. **利用 Checkpoints 实验**

**Fork Conversation**：
```bash
# 尝试不同方法
# 不满意就 rewind，重新 fork
```

### 6. **用 Git Worktrees 并行工作**

```bash
# 任务 1
claude --worktree feature-auth

# 任务 2
claude --worktree bugfix-payment

# 互不干扰
```

### 7. **引用终端输出**

```bash
# 运行测试
npm test

# 在 Claude 中
@terminal:npm test analyze the failures
```

---

## 📚 与 OpenClaw 的对比

### 相似之处

1. **IDE 集成** - 都可以在 IDE 中工作
2. **上下文管理** - 都支持文件引用
3. **多会话** - 都支持并行工作

### 差异之处

1. **深度集成** - Claude Code extension 更深入（checkpoints、terminal reference、git worktrees）
2. **Permission Modes** - Claude Code 有三级模式，OpenClaw 更简单
3. **Diff View** - Claude Code 有内置差异审查，OpenClaw 需要外部工具
4. **Checkpoints** - Claude Code 有回退机制，OpenClaw 没有
5. **Terminal Integration** - Claude Code 可以引用终端输出，OpenClaw 不能

### 可以借鉴

1. **@-mentions** - 精确文件和行引用
2. **Permission Modes** - 三级权限控制
3. **Checkpoints** - 回退和分支机制
4. **Terminal Reference** - 终端输出引用
5. **Diff View** - 内置差异审查
6. **Git Worktrees** - 并行任务隔离

---

## 🏷️ 标签
`#vscode` `#ide-integration` `#diff-view` `#checkpoints` `#terminal` `#git-worktrees` `#permission-modes`
