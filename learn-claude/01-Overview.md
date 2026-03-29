# 01 - Claude Code Overview 学习笔记

**学习时间**：2026-03-14 12:10  
**页面地址**：https://code.claude.com/docs/en/overview

---

## 📖 原文要点

### 核心定位
Claude Code 是一个 **AI 驱动的编程助手**，可以：
- 理解整个代码库
- 跨多个文件和工具工作
- 构建功能、修复 Bug、自动化开发任务

### 5 种使用方式

#### 1. **Terminal CLI** ⭐（推荐）
完整的命令行工具，直接在终端中编辑文件、运行命令、管理项目。

**安装方式**：
- **Native Install**（推荐）：自动后台更新
  - macOS/Linux/WSL: `curl -fsSL https://claude.ai/install.sh | bash`
  - Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`
- **Homebrew**: `brew install --cask claude-code`（需手动更新）
- **WinGet**: `winget install Anthropic.ClaudeCode`（需手动更新）

**启动**：
```bash
cd your-project
claude
```

#### 2. **VS Code 扩展**
提供内联差异对比、@提及、计划审查、对话历史。

**安装**：在扩展市场搜索 "Claude Code"

#### 3. **Desktop App**
独立应用，可视化查看差异、多会话并行、安排定期任务、启动云会话。

**特点**：需要付费订阅

#### 4. **Web**
浏览器中运行，无需本地设置。适合长期运行任务、处理不在本地的仓库、并行多任务。

**地址**：claude.ai/code

#### 5. **JetBrains 插件**
支持 IntelliJ IDEA、PyCharm、WebStorm 等，提供交互式差异查看和选择上下文共享。

---

## 🎯 Claude Code 能做什么？

### 1. **自动化重复性工作**
写测试、修复 lint 错误、解决合并冲突、更新依赖、写发布说明。

**示例**：
```bash
claude "write tests for the auth module, run them, and fix any failures"
```

### 2. **构建功能和修复 Bug**
用自然语言描述需求，Claude Code 会：
- 规划方法
- 跨多个文件编写代码
- 验证功能

**Bug 修复**：粘贴错误信息或描述症状，Claude Code 会：
- 追踪问题
- 识别根本原因
- 实现修复

### 3. **创建 Commits 和 Pull Requests**
直接与 git 交互，stage 更改、写提交信息、创建分支、打开 PR。

**示例**：
```bash
claude "commit my changes with a descriptive message"
```

### 4. **通过 MCP 连接工具**
Model Context Protocol (MCP) 是连接 AI 工具和外部数据源的开放标准。

**示例**：
- 读取 Google Drive 中的设计文档
- 更新 Jira 票据
- 从 Slack 拉取数据
- 使用自定义工具

### 5. **用 Instructions、Skills 和 Hooks 自定义**

#### **CLAUDE.md**
项目根目录的 Markdown 文件，每次会话开始时 Claude Code 会读取。
- 设置编码标准
- 记录架构决策
- 指定首选库
- 定义审查清单

#### **Auto Memory**
Claude Code 自动构建记忆，保存学习内容（如构建命令、调试见解）。

#### **自定义命令**
打包可重复的工作流，如 `/review-pr` 或 `/deploy-staging`。

#### **Hooks**
在 Claude Code 操作前后运行 shell 命令。
- 文件编辑后自动格式化
- 提交前运行 lint

### 6. **运行 Agent Teams 和构建自定义 Agents**

#### **Agent Teams**
生成多个 Claude Code agents，同时处理任务的不同部分。
- Lead agent 协调工作
- 分配子任务
- 合并结果

#### **Agent SDK**
构建自己的 agents，使用 Claude Code 的工具和能力。
- 完全控制编排
- 工具访问权限
- 权限管理

### 7. **Pipe、Script 和自动化 CLI**
遵循 Unix 哲学，可组合。

**示例**：
```bash
# 监控日志并告警
tail -f app.log | claude -p "Slack me if you see any anomalies"

# CI 中自动化翻译
claude -p "translate new strings into French and raise a PR for review"

# 跨文件批量操作
git diff main --name-only | claude -p "review these changed files for security issues"
```

### 8. **随处工作**
会话不绑定单一界面，可以跨环境移动工作：
- **Remote Control**：离开桌面，用手机或浏览器继续
- **/teleport**：在 web 或 iOS 应用启动长期任务，拉取到终端
- **/desktop**：将终端会话交给 Desktop app 进行可视化差异审查
- **Slack**：在 Slack 中 @Claude 提交 bug 报告，获得 PR

---

## 💡 学习感悟

### 1. **多模态设计哲学**
Claude Code 的设计理念是 **"随处可用"**：
- 同一个底层引擎
- CLAUDE.md、设置、MCP 服务器跨所有界面工作
- 会话可以跨设备迁移

这与 OpenClaw 的设计理念类似 - 让 AI Agent 无缝集成到工作流程中。

### 2. **Unix 哲学的体现**
"Pipe, script, and automate with the CLI" 这部分让我印象深刻：
- 可以用管道输入
- 可以在 CI 中运行
- 可以与其他工具链式组合

这符合 Unix 哲学："做一件事，并把它做好"。

### 3. **记忆系统的重要性**
**CLAUDE.md + Auto Memory** 的组合非常强大：
- CLAUDE.md 是显式指令（类似 OpenClaw 的 AGENTS.md）
- Auto Memory 是隐式学习（类似 OpenClaw 的 MEMORY.md）

这种 **显式 + 隐式** 的记忆系统设计，是 AI Agent 持续学习的关键。

### 4. **MCP 的开放性**
Model Context Protocol 作为开放标准，让 Claude Code 可以：
- 连接外部数据源
- 使用自定义工具
- 不被锁定在单一生态

这与 OpenClaw 的 Skills 系统类似 - 通过标准化接口扩展能力。

### 5. **Agent 编排能力**
**Subagents + Agent Teams + Agent SDK** 三层架构：
- Subagents：单会话内专业化处理
- Agent Teams：多 agent 并行协作
- Agent SDK：完全自定义编排

这为复杂工作流提供了强大的工具支持。

---

## 🎯 实践建议

### 1. **从 Terminal CLI 开始**
对于已有编程习惯的开发者，Terminal CLI 是最自然的入口：
```bash
# 安装（macOS）
curl -fsSL https://claude.ai/install.sh | bash

# 启动
cd my-project
claude
```

### 2. **创建项目的 CLAUDE.md**
立即为项目创建 CLAUDE.md，定义：
- 编码规范
- 架构决策
- 测试策略
- Git 工作流

示例：
```markdown
# Project Guidelines

## 编码规范
- 使用 TypeScript strict mode
- 函数必须有 JSDoc 注释
- 测试覆盖率 > 80%

## 架构
- 前端：React + Vite
- 后端：Node.js + Express
- 数据库：PostgreSQL

## Git 工作流
- 分支命名：feature/xxx, fix/xxx
- 提交信息：遵循 Conventional Commits
- PR 必须经过 code review
```

### 3. **尝试 Pipe 和自动化**
从简单的自动化开始：
```bash
# 查看最近的错误日志
tail -100 error.log | claude -p "summarize the errors and suggest fixes"

# 代码审查
git diff main | claude -p "review for security issues"
```

### 4. **探索 MCP 集成**
如果使用外部工具（如 Jira、Slack、Google Drive），配置 MCP 服务器让 Claude Code 访问这些数据。

### 5. **学习 Subagents**
后续深入学习 Subagents，创建专业化 agents：
- Code reviewer
- Test runner
- Documentation writer

---

## 📚 下一步学习

根据 Overview 的 "Next steps"，建议学习顺序：
1. ✅ **Overview**（当前页面）
2. ⏭️ **Quickstart** - 实际上手第一个任务
3. ⏭️ **Store instructions and memories** - 深入理解 CLAUDE.md 和 Auto Memory
4. ⏭️ **Common workflows** - 学习常见工作模式
5. ⏭️ **Best practices** - 掌握最佳实践

---

## 🏷️ 标签
`#getting-started` `#overview` `#installation` `#multi-platform` `#mcp` `#agents`
