# 02 - Claude Code Quickstart 学习笔记

**学习时间**：2026-03-14 12:15  
**页面地址**：https://code.claude.com/docs/en/quickstart

---

## 📖 原文要点

### 准备工作
- ✅ 终端或命令提示符
- ✅ 一个代码项目
- ✅ Claude 订阅（Pro/Max/Teams/Enterprise）或 Console 账户或云提供商

### 8 步快速上手

#### **Step 1: 安装 Claude Code**

**Native Install**（推荐，自动更新）：
```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Windows CMD
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**Homebrew**（需手动更新）：
```bash
brew install --cask claude-code
```

**WinGet**（需手动更新）：
```bash
winget install Anthropic.ClaudeCode
```

**Windows 要求**：必须先安装 Git for Windows。

#### **Step 2: 登录账户**

```bash
claude
# 首次使用会提示登录

/login
# 跟随提示登录
```

**支持的账户类型**：
1. Claude Pro/Max/Teams/Enterprise（推荐）
2. Claude Console（API 预付费，自动创建 "Claude Code" workspace 用于成本追踪）
3. Amazon Bedrock、Google Vertex AI、Microsoft Foundry（企业云）

登录后凭据会保存，切换账户用 `/login`。

#### **Step 3: 启动第一个会话**

```bash
cd /path/to/your/project
claude
```

会看到欢迎界面，显示：
- 会话信息
- 最近对话
- 最新更新

**命令**：
- `/help` - 查看可用命令
- `/resume` - 继续之前的对话

#### **Step 4: 提第一个问题**

**理解代码库**：
```bash
what does this project do?
```

**更具体的问题**：
```bash
what technologies does this project use?
where is the main entry point?
explain the folder structure
```

**询问 Claude Code 能力**：
```bash
what can Claude Code do?
how do I create custom skills in Claude Code?
can Claude Code work with Docker?
```

**关键**：Claude Code 会根据需要读取项目文件，你不需要手动添加上下文。

#### **Step 5: 做第一次代码修改**

```bash
add a hello world function to the main file
```

**Claude Code 的流程**：
1. 找到合适的文件
2. 显示提议的更改
3. 请求你的批准
4. 执行编辑

**权限**：Claude Code 总是在修改文件前请求许可。你可以：
- 批准单个更改
- 为会话启用 "Accept all" 模式

#### **Step 6: 使用 Git**

**基本操作**：
```bash
what files have I changed?
commit my changes with a descriptive message
```

**复杂操作**：
```bash
create a new branch called feature/quickstart
show me the last 5 commits
help me resolve merge conflicts
```

#### **Step 7: 修复 Bug 或添加功能**

**添加功能**：
```bash
add input validation to the user registration form
```

**修复 Bug**：
```bash
there's a bug where users can submit empty forms - fix it
```

**Claude Code 会**：
1. 定位相关代码
2. 理解上下文
3. 实现解决方案
4. 运行测试（如果有）

#### **Step 8: 测试其他常见工作流**

**重构代码**：
```bash
refactor the authentication module to use async/await instead of callbacks
```

**写测试**：
```bash
write unit tests for the calculator functions
```

**更新文档**：
```bash
update the README with installation instructions
```

**代码审查**：
```bash
review my changes and suggest improvements
```

**关键**：像与有帮助的同事交谈一样与 Claude 对话。描述你想实现什么，它会帮你达成。

---

## 📋 常用命令速查表

| 命令 | 作用 | 示例 |
|------|------|------|
| `claude` | 启动交互模式 | `claude` |
| `claude "task"` | 运行一次性任务 | `claude "fix the build error"` |
| `claude -p "query"` | 单次查询后退出 | `claude -p "explain this function"` |
| `claude -c` | 继续最近对话 | `claude -c` |
| `claude -r` | 恢复之前的对话 | `claude -r` |
| `claude commit` | 创建 Git 提交 | `claude commit` |
| `/clear` | 清除对话历史 | `/clear` |
| `/help` | 显示可用命令 | `/help` |
| `exit` 或 `Ctrl+C` | 退出 Claude Code | `exit` |

---

## 💡 新手专业技巧

### 1. **请求要具体**

❌ **不好**：
```bash
fix the bug
```

✅ **好**：
```bash
fix the login bug where users see a blank screen after entering wrong credentials
```

### 2. **使用逐步指令**

将复杂任务分解为步骤：
```bash
1. create a new database table for user profiles
2. create an API endpoint to get and update user profiles
3. build a webpage that allows users to see and edit their information
```

### 3. **让 Claude 先探索**

在修改前，先让 Claude 理解代码：
```bash
analyze the database schema
build a dashboard showing products that are most frequently returned by our UK customers
```

### 4. **节省时间的快捷键**

- 按 `?` - 查看所有键盘快捷键
- 按 `Tab` - 命令补全
- 按 `↑` - 命令历史
- 输入 `/` - 查看所有命令和 skills

---

## 🎯 下一步学习

1. **How Claude Code works** - 理解 agent loop、内置工具、项目交互
2. **Best practices** - 有效提示和项目设置
3. **Common workflows** - 常见任务的分步指南
4. **Extend Claude Code** - 用 CLAUDE.md、skills、hooks、MCP 自定义

---

## 💡 学习感悟

### 1. **对话式编程的威力**
Quickstart 强调的核心思想是：**像与同事交谈一样与 Claude 对话**。

这打破了传统编程的"工具-命令"模式，变成"意图-协作"模式。

**对比**：
- **传统**：学习命令 → 查文档 → 写脚本 → 调试
- **Claude Code**：描述意图 → Claude 执行 → 验证结果

### 2. **渐进式引导设计**
8 步设计非常合理：
1. 安装（基础）
2. 登录（账户）
3. 启动（环境）
4. 提问（理解）
5. 改代码（修改）
6. Git（版本控制）
7. 修 Bug（实战）
8. 工作流（进阶）

每一步都建立在前一步基础上，符合学习曲线。

### 3. **自动上下文管理**
"Claude Code reads your project files as needed. You don't have to manually add context."

这是一个关键设计 - **隐式上下文管理**：
- 用户不需要手动指定文件
- Claude Code 自动分析代码库
- 减少认知负担

这与 OpenClaw 的 memory_search 类似 - 自动检索相关内容。

### 4. **权限与安全**
"Claude Code always asks for permission before modifying files."

这是 AI Agent 安全的重要原则：
- **最小权限原则**
- **显式确认**
- **可预测行为**

但提供了 "Accept all" 模式用于信任场景 - 灵活性与安全性平衡。

### 5. **命令行哲学**
Quickstart 展示的命令行用法：
- **一次性任务**：`claude "fix the build error"`
- **交互模式**：`claude`
- **查询模式**：`claude -p "explain this function"`

这体现了 Unix 哲学的"可组合性" - 可以用在脚本、CI/CD、日常开发中。

### 6. **提示工程的教学**
新手技巧实际上是在教**提示工程**：
- 具体化（Specific）
- 分步骤（Step-by-step）
- 探索先行（Explore first）

这些是有效使用 AI Agent 的通用原则。

---

## 🎯 实践建议

### 1. **立即实践**
完成 Quickstart 后，立即在真实项目中尝试：
```bash
# 在你的项目中
cd your-real-project
claude

# 尝试提问
what does this project do?
where is the main entry point?

# 尝试修改
add a comment explaining what this function does
```

### 2. **创建 CLAUDE.md**
学习完 Quickstart 后，立即创建项目的 CLAUDE.md：
```markdown
# 项目指南

## 技术栈
- 前端：React
- 后端：Node.js
- 数据库：PostgreSQL

## 代码规范
- 使用 ESLint
- 测试覆盖率 > 70%

## Git 工作流
- 分支命名：feature/xxx, fix/xxx
- 提交信息遵循 Conventional Commits
```

### 3. **逐步进阶**
不要急于使用高级功能，按照学习路径：
1. ✅ Quickstart（当前）
2. ⏭️ Common workflows（学习常见模式）
3. ⏭️ Best practices（优化提示技巧）
4. ⏭️ Extend Claude Code（自定义能力）

### 4. **建立工作流**
将 Claude Code 集成到日常工作中：
- 代码审查：`review my changes`
- 提交代码：`claude commit`
- 写测试：`write tests for ...`
- 重构：`refactor ...`

### 5. **学习提示技巧**
新手技巧中的"具体化"和"分步骤"是关键：
- ❌ "fix the bug"
- ✅ "fix the login bug where users see a blank screen after entering wrong credentials"

**练习**：用这个模式改写你的常见请求。

---

## 📚 与 OpenClaw 的对比

### 相似之处
1. **对话式交互** - 自然语言描述意图
2. **上下文管理** - 自动读取项目文件
3. **技能系统** - Claude Code 的 Skills vs OpenClaw 的 Skills
4. **记忆系统** - CLAUDE.md vs AGENTS.md

### 差异之处
1. **界面** - Claude Code 专注 IDE/终端，OpenClaw 专注聊天平台
2. **自动化程度** - Claude Code 更激进（自动修改文件），OpenClaw 更保守（需确认）
3. **生态** - Claude Code 有 MCP，OpenClaw 有 Skills 系统

### 可以借鉴
1. **权限模式** - "Accept all" vs 逐个确认的灵活切换
2. **命令速查表** - 清晰的命令分类和示例
3. **渐进式引导** - 8 步快速上手的结构

---

## 🏷️ 标签
`#quickstart` `#getting-started` `#installation` `#git` `#prompting` `#best-practices`
