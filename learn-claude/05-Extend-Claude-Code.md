# 05 - Extend Claude Code 学习笔记

**学习时间**：2026-03-14 13:52  
**页面地址**：https://code.claude.com/docs/en/features-overview

---

## 📖 原文要点

### 核心概念

Claude Code = **Model（推理） + Built-in Tools（基础能力） + Extensions（扩展层）**

**Built-in Tools** 覆盖大多数编码任务：
- File operations（文件操作）
- Search（搜索）
- Execution（执行）
- Web access（网页访问）

**Extensions** 用于自定义：
- Claude 知道什么
- 连接外部服务
- 自动化工作流

---

## 🎯 扩展功能概览

### 6 大扩展机制

| 功能 | 作用 | 何时使用 | 示例 |
|------|------|---------|------|
| **CLAUDE.md** | 每个会话加载的持久上下文 | 项目约定、"总是做 X"规则 | "Use pnpm, not npm. Run tests before committing." |
| **Skills** | Claude 可用的指令、知识、工作流 | 可复用内容、参考文档、可重复任务 | /deploy 运行部署清单；API 文档 skill |
| **Subagent** | 返回摘要结果的隔离执行上下文 | 上下文隔离、并行任务、专业化 worker | 读取大量文件但只返回关键发现的研究任务 |
| **Agent teams** | 协调多个独立的 Claude Code 会话 | 并行研究、新功能开发、竞争假设调试 | 同时生成 reviewers 检查安全、性能、测试 |
| **MCP** | 连接外部服务 | 外部数据或操作 | 查询数据库、发 Slack、控制浏览器 |
| **Hook** | 事件触发的确定性脚本 | 可预测自动化、不涉及 LLM | 每次文件编辑后运行 ESLint |

**Plugins** 是打包层：将 skills、hooks、subagents、MCP servers 打包成单个可安装单元。

---

## 🔍 功能对比

### 1. **Skill vs Subagent**

| 方面 | Skill | Subagent |
|------|-------|----------|
| **是什么** | 可复用的指令、知识、工作流 | 有自己上下文的隔离 worker |
| **关键优势** | 跨上下文共享内容 | 上下文隔离。工作分离，只返回摘要 |
| **最适合** | 参考资料、可调用工作流 | 读取大量文件、并行工作、专业化 worker |

**Skills** 可以是：
- **Reference** - 提供知识（如 API style guide）
- **Action** - 做特定事情（如 /deploy 运行部署工作流）

**Subagents** 用于：
- 上下文隔离
- 上下文窗口满时
- 不需要中间工作可见时

**可以组合**：
- Subagent 可以预加载特定 skills
- Skill 可以用 `context: fork` 在隔离上下文运行

---

### 2. **CLAUDE.md vs Skill**

| 方面 | CLAUDE.md | Skill |
|------|-----------|-------|
| **加载时机** | 每个会话，自动 | 按需 |
| **可包含文件** | 是（@path imports） | 是（@path imports） |
| **可触发工作流** | 否 | 是（/<name>） |
| **最适合** | "总是做 X"规则 | 参考资料、可调用工作流 |

**经验法则**：
- **CLAUDE.md** < 200 行
- 如果增长，移参考资料到 skills 或拆分到 `.claude/rules/`

---

### 3. **CLAUDE.md vs Rules vs Skills**

| 方面 | CLAUDE.md | .claude/rules/ | Skill |
|------|-----------|----------------|-------|
| **加载时机** | 每个会话 | 每个会话，或打开匹配文件时 | 按需，调用或相关时 |
| **作用域** | 整个项目 | 可限定到文件路径 | 任务特定 |
| **最适合** | 核心约定和构建命令 | 语言特定或目录特定指南 | 参考资料、可重复工作流 |

**使用场景**：
- **CLAUDE.md** - 每个会话都需要：构建命令、测试约定、项目架构
- **Rules** - 保持 CLAUDE.md 聚焦。带 paths frontmatter 的 rules 只在处理匹配文件时加载
- **Skills** - Claude 只有时需要的内容，如 API 文档或用 /<name> 触发的部署清单

---

### 4. **Subagent vs Agent Team**

| 方面 | Subagent | Agent Team |
|------|----------|------------|
| **上下文** | 自己的上下文窗口；结果返回调用者 | 自己的上下文窗口；完全独立 |
| **通信** | 只向 main agent 报告结果 | Teammates 直接互相消息 |
| **协调** | Main agent 管理所有工作 | 共享任务列表自我协调 |
| **最适合** | 只关注结果的聚焦任务 | 需要讨论和协作的复杂工作 |
| **Token 成本** | 较低：结果摘要回主上下文 | 较高：每个 teammate 是独立的 Claude 实例 |

**何时用 Subagent**：
- 快速、聚焦的 worker
- 研究问题、验证声明、审查文件
- 主对话保持干净

**何时用 Agent Team**：
- Teammates 需要共享发现、互相挑战、独立协调
- 竞争假设研究、并行代码审查、新功能开发

**过渡点**：
- 如果并行运行 subagents 但遇到上下文限制
- 或 subagents 需要互相通信
- → Agent teams 是自然的下一步

---

### 5. **MCP vs Skill**

| 方面 | MCP | Skill |
|------|-----|-------|
| **是什么** | 连接外部服务的协议 | 知识、工作流、参考资料 |
| **提供** | 工具和数据访问 | 知识、工作流、参考资料 |
| **示例** | Slack 集成、数据库查询、浏览器控制 | 代码审查清单、部署工作流、API style guide |

**解决不同问题，可以协同工作**：
- **MCP** 给 Claude 与外部系统交互的能力
- **Skill** 给 Claude 如何有效使用这些工具的知识

**示例**：
- MCP server 连接 Claude 到数据库
- Skill 教 Claude 数据模型、常见查询模式、不同任务用哪些表

---

## 🏗️ 功能分层

### 优先级规则

1. **CLAUDE.md files are additive**
   - 所有级别同时贡献内容
   - 工作目录及以上在启动时加载
   - 子目录在访问时加载
   - 冲突时 Claude 用判断力协调，更具体的指令通常优先

2. **Skills and subagents override by name**
   - 相同名称存在时，一个定义获胜
   - Skills: managed > user > project
   - Subagents: managed > CLI flag > project > user > plugin
   - Plugin skills 命名空间化避免冲突

3. **MCP servers override by name**
   - local > project > user

4. **Hooks merge**
   - 所有注册的 hooks 为匹配事件触发，无论来源

---

## 🔄 组合功能

每个扩展解决不同问题：
- **CLAUDE.md** - always-on context
- **Skills** - on-demand knowledge & workflows
- **MCP** - external connections
- **Subagents** - isolation
- **Hooks** - automation

**真实设置根据工作流组合它们**。

### 组合模式

| 模式 | 工作原理 | 示例 |
|------|---------|------|
| **Skill + MCP** | MCP 提供连接；skill 教 Claude 如何使用 | MCP 连接数据库，skill 文档化 schema 和查询模式 |
| **Skill + Subagent** | Skill 为并行工作生成 subagents | /audit skill 启动安全、性能、风格 subagents 在隔离上下文工作 |
| **CLAUDE.md + Skills** | CLAUDE.md 持有 always-on 规则；skills 持有按需参考资料 | CLAUDE.md 说"遵循 API 约定"，skill 包含完整 API style guide |
| **Hook + MCP** | Hook 通过 MCP 触发外部动作 | Post-edit hook 在 Claude 修改关键文件时发送 Slack 通知 |

---

## 💰 上下文成本

### 上下文成本按功能

| 功能 | 加载时机 | 加载内容 | 上下文成本 |
|------|---------|---------|-----------|
| **CLAUDE.md** | 会话开始 | 完整内容 | 每次请求 |
| **Skills** | 会话开始 + 使用时 | 开始时描述，使用时完整内容 | 低（每次请求描述）* |
| **MCP servers** | 会话开始 | 所有工具定义和 schemas | 每次请求 |
| **Subagents** | 生成时 | 带指定 skills 的新鲜隔离上下文 | 与主会话隔离 |
| **Hooks** | 触发时 | 无（外部运行） | 零，除非 hook 返回额外上下文 |

*默认：skill 描述在会话开始时加载，Claude 决定何时使用。
设置 `disable-model-invocation: true` 完全隐藏，直到手动调用。

---

## 🔄 功能加载机制

### CLAUDE.md
- **When**: 会话开始
- **What**: 所有 CLAUDE.md 文件（managed、user、project 级别）完整内容
- **Inheritance**: 从工作目录读到根，子目录在访问时发现
- **建议**: 保持 < 500 行，移参考资料到 skills

### Skills
- **When**: 取决于配置
  - 默认：会话开始加载描述，使用时加载完整内容
  - User-only skills（`disable-model-invocation: true`）：调用前不加载
- **What**: 
  - Model-invocable skills：每次请求看到名称和描述
  - 调用时完整内容加载到对话
- **How Claude chooses**: 匹配任务与 skill 描述
- **In subagents**: 完全预加载，不继承主会话 skills
- **建议**: 有副作用的 skills 用 `disable-model-invocation: true`

### MCP Servers
- **When**: 会话开始
- **What**: 所有工具定义和 JSON schemas
- **Context cost**: Tool search 加载最多 10% 上下文，其余延迟到需要时
- **注意**: 连接可能静默失败，用 `/mcp` 检查

### Subagents
- **When**: 按需
- **What**: 新鲜隔离上下文：
  - 系统提示（与父共享以缓存效率）
  - skills: 字段列出的 skills 完整内容
  - CLAUDE.md 和 git status（从父继承）
  - Lead agent 在提示中传递的任何上下文
- **Context cost**: 与主会话隔离

### Hooks
- **When**: 触发时
- **What**: 无（外部脚本）
- **Context cost**: 零，除非 hook 返回输出添加到对话

---

## 💡 学习感悟

### 1. **分层设计的优雅**

Claude Code 的扩展系统采用**分层设计**：
- **核心层**：Model + Built-in Tools（覆盖 80% 场景）
- **扩展层**：6 大机制（解决剩余 20% 场景）

这种设计符合 **Pareto Principle（80/20 法则）**。

### 2. **功能定位的清晰性**

每个扩展有明确的定位：
- **CLAUDE.md** - Always-on context（"总是做 X"）
- **Skills** - On-demand knowledge（"有时需要 Y"）
- **MCP** - External connections（"连接外部 Z"）
- **Subagents** - Isolation（"隔离工作 W"）
- **Hooks** - Automation（"自动执行 V"）

这种清晰的**单一职责原则**避免了功能重叠。

### 3. **上下文成本意识**

文档非常强调**上下文成本**：
- 每个功能都有上下文成本分析
- 提供减少成本的策略
- 用 `/context` 监控使用

这体现了 **"Context is precious"** 的核心原则。

### 4. **组合而非堆砌**

文档强调**组合功能**：
- 不是用一个大功能解决所有问题
- 而是用多个小功能组合
- 每个功能解决擅长的问题

这符合 **Unix 哲学**："Do one thing well"。

### 5. **Skill vs Subagent 的精妙区分**

这个对比让我理解了：
- **Skill** - 在主上下文中工作，适合参考资料
- **Subagent** - 在隔离上下文工作，适合大量文件操作

关键是：**Context isolation vs Context sharing**。

### 6. **Agent Teams 的未来**

Agent Teams 被标记为 "experimental"，但展现了：
- **多 Agent 协作**的方向
- **P2P 通信**的能力
- **自我协调**的架构

这可能是 AI Agent 系统的未来 - 从单 agent 到多 agent。

---

## 🎯 实践建议

### 1. **从简单开始**

按照顺序添加扩展：
1. **CLAUDE.md** - 项目约定
2. **Skills** - 参考资料、工作流
3. **MCP** - 外部连接
4. **Hooks** - 自动化
5. **Subagents** - 隔离任务
6. **Agent Teams** - 协作任务

### 2. **管理 CLAUDE.md 大小**

```markdown
# 项目约定（CLAUDE.md）

## 核心规则（保持在 200 行内）
- Use pnpm, not npm
- Run tests before committing

## 移动内容到 Skills
- API 文档 → skills/api-guide.md
- 部署清单 → skills/deploy.md
- 代码审查清单 → skills/review.md
```

### 3. **用 disable-model-invocation 节省上下文**

```yaml
---
name: deploy
description: Deploy to production
disable-model-invocation: true  # 只在你调用 /deploy 时加载
---

# Deployment Checklist
...
```

### 4. **监控上下文使用**

```bash
# 定期检查
/context

# MCP servers 成本
/mcp

# 压缩时控制保留内容
/compact focus on the API changes
```

### 5. **组合使用**

```bash
# Skill + MCP
# MCP 连接数据库
# Skill 教 Claude 如何使用
"Query the users table to find inactive accounts"

# Skill + Subagent
# /audit skill 启动多个 subagents
/audit

# Hook + MCP
# Post-edit hook 发送 Slack 通知
# 在 hooks 配置中：
# PostToolUse:
#   - matcher: Edit|Write
#     hooks:
#       - type: command
#         command: ./scripts/notify-slack.sh
```

### 6. **选择 Subagent vs Agent Team**

**用 Subagent**：
```bash
# 快速、聚焦的任务
"Research the authentication flow"
"Review this file for security issues"
```

**用 Agent Team**：
```bash
# 需要协作的任务
"Spawn reviewers to check security, performance, and tests simultaneously"
```

---

## 📚 与 OpenClaw 的对比

### 相似之处

1. **Skills 系统** - 都是 Markdown 文件
2. **记忆系统** - CLAUDE.md vs AGENTS.md
3. **Hooks** - 都支持生命周期 hooks
4. **MCP** - 都支持 MCP 协议

### 差异之处

1. **Subagents** - Claude Code 有明确概念，OpenClaw 用 sessions_spawn
2. **Agent Teams** - Claude Code 有 P2P 协作，OpenClaw 没有
3. **上下文管理** - Claude Code 更成熟（监控、压缩、成本分析）
4. **分层机制** - Claude Code 有 managed/user/project/plugin 四层

### 可以借鉴

1. **disable-model-invocation** - Skills 按需加载
2. **Context monitoring** - `/context` 命令
3. **Agent Teams** - 多 agent 协作架构
4. **成本分析** - 每个功能的上下文成本

---

## 🏷️ 标签
`#extensions` `#skills` `#subagents` `#mcp` `#hooks` `#context-management` `#layering`
