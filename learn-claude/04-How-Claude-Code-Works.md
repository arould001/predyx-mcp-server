# 04 - How Claude Code Works 学习笔记

**学习时间**：2026-03-14 12:25  
**页面地址**：https://code.claude.com/docs/en/how-claude-code-works

---

## 📖 原文要点

### 核心概念：Agentic Loop（代理循环）

Claude Code 是一个 **agentic assistant**，通过三阶段循环工作：

```
1. Gather Context（收集上下文）
2. Take Action（执行操作）
3. Verify Results（验证结果）
```

**关键特点**：
- **自适应**：根据任务调整（问题只需收集上下文，Bug 修复需要完整循环）
- **链式行动**：链接数十个操作，中途纠错
- **人类参与**：可随时中断、提供额外上下文、尝试不同方法

**Agentic Loop 的两个组件**：
1. **Models** - 推理（Claude models）
2. **Tools** - 行动（Claude Code 提供）

---

### Models（模型）

Claude Code 使用 Claude models 来：
- 理解代码（任何语言）
- 理解组件连接
- 推理需要改变什么

**多模型选择**：
- **Sonnet** - 大多数编码任务
- **Opus** - 复杂架构决策的更强推理

**切换模型**：
```bash
# 会话中切换
/model

# 启动时指定
claude --model opus
```

---

### Tools（工具）

**工具让 Claude Code 变成 agentic**：
- 没有工具：只能返回文本
- 有工具：可以读取代码、编辑文件、运行命令、搜索网页、与外部服务交互

#### 5 大工具类别

| 类别 | 能力 |
|------|------|
| **File operations** | 读取文件、编辑代码、创建新文件、重命名和重组 |
| **Search** | 按模式查找文件、用 regex 搜索内容、探索代码库 |
| **Execution** | 运行 shell 命令、启动服务器、运行测试、使用 git |
| **Web** | 搜索网页、获取文档、查找错误消息 |
| **Code intelligence** | 查看类型错误和警告、跳转定义、查找引用（需要 code intelligence plugins） |

#### 示例：修复失败测试的流程

当你说 "fix the failing tests" 时，Claude 会：
1. **Run tests** - 运行测试套件查看失败
2. **Read error output** - 读取错误输出
3. **Search files** - 搜索相关源文件
4. **Read files** - 读取文件理解代码
5. **Edit files** - 编辑文件修复问题
6. **Run tests again** - 再次运行测试验证

**每个工具使用都给 Claude 新信息，指导下一步。**

#### 扩展能力

基础工具之上，可以添加：
- **Skills** - 扩展知识
- **MCP** - 连接外部服务
- **Hooks** - 自动化工作流
- **Subagents** - 委派任务

---

### What Claude Can Access（访问权限）

当你在目录运行 `claude` 时，Claude Code 获得：

1. **Your project** - 目录和子目录中的文件，以及你允许的其他位置文件
2. **Your terminal** - 你能运行的任何命令：构建工具、git、包管理器、系统工具、脚本
3. **Your git state** - 当前分支、未提交更改、最近提交历史
4. **Your CLAUDE.md** - 项目特定指令、约定、上下文
5. **Auto memory** - Claude 自动保存的学习内容（前 200 行 MEMORY.md）
6. **Extensions** - MCP servers、skills、subagents、Chrome 集成

**关键优势**：Claude 能看到整个项目，可以跨文件工作，这与只看当前文件的内联代码助手不同。

---

### Environments and Interfaces（环境和界面）

#### 3 种执行环境

| 环境 | 代码运行位置 | 用例 |
|------|-------------|------|
| **Local** | 你的机器 | 默认。完整访问文件、工具、环境 |
| **Cloud** | Anthropic 管理的 VMs | 卸载任务、处理不在本地的仓库 |
| **Remote Control** | 你的机器，从浏览器控制 | 使用 Web UI 但保持本地 |

#### 多种界面

Terminal、Desktop app、IDE 扩展、claude.ai/code、Remote Control、Slack、CI/CD pipelines。

**界面决定你如何交互，但底层 agentic loop 相同。**

---

### Work with Sessions（会话管理）

#### 会话特性

1. **本地保存** - 每条消息、工具使用、结果都存储
2. **支持回退、恢复、分叉**
3. **修改前快照** - 文件修改前创建快照，可以恢复

#### 会话独立性

每个新会话：
- 从**全新的上下文窗口**开始
- **没有之前会话的对话历史**
- 可以通过 **auto memory** 跨会话持久化学习
- 可以在 **CLAUDE.md** 添加持久指令

#### 跨分支工作

- 会话绑定到**当前目录**
- Claude 看到**当前分支的文件**
- 切换分支后，会话历史保持不变
- 可以用 **git worktrees** 并行运行多个会话

#### Resume or Fork Sessions（恢复或分叉会话）

**Resume（恢复）**：
```bash
claude --continue
# 或
claude --resume
```
- 使用**相同 session ID**
- 新消息追加到现有对话
- 完整对话历史恢复
- **会话级权限不恢复**（需重新批准）

**Fork（分叉）**：
```bash
claude --continue --fork-session
```
- 创建**新 session ID**
- 保留到该点的对话历史
- 原始会话保持不变
- 会话级权限不继承

**⚠️ 同一会话在多个终端**：
- 都写入同一会话文件
- 消息会交错
- 每个终端只看到自己的消息
- 恢复会话时看到所有交错的消息

**建议**：并行工作用 `--fork-session` 给每个终端干净的会话。

---

### The Context Window（上下文窗口）

#### 包含内容

Claude 的上下文窗口包含：
- 对话历史
- 文件内容
- 命令输出
- CLAUDE.md
- 加载的 skills
- 系统指令

#### 上下文管理

**自动压缩**：
- 接近限制时自动管理
- 先清除旧的工具输出
- 如需则总结对话
- 保留你的请求和关键代码片段
- 早期对话的详细指令可能丢失

**手动控制**：
```bash
# 查看什么占用空间
/context

# 控制压缩时保留什么
/compact focus on the API changes
```

**持久化规则**：放在 CLAUDE.md，不要依赖对话历史。

#### 用 Skills 和 Subagents 管理上下文

**Skills**：
- 按需加载
- 会话开始时 Claude 只看到描述
- 使用时才加载完整内容
- 手动调用的 skills 可设置 `disable-model-invocation: true` 保持在上下文外

**Subagents**：
- 获得全新上下文
- 与主对话完全分离
- 工作不会膨胀你的上下文
- 完成后返回摘要

---

### Stay Safe with Checkpoints and Permissions（安全机制）

#### Checkpoints（检查点）

**每个文件编辑可逆**：
- 编辑前快照当前内容
- 出问题时按 **Esc 两次** 回退到之前状态
- 或让 Claude undo

**限制**：
- 本地会话，与 git 分离
- 只覆盖文件更改
- 影响远程系统的操作（数据库、APIs、部署）无法检查点

#### Permissions（权限）

**3 种权限模式**（Shift+Tab 切换）：

1. **Default** - 文件编辑和 shell 命令前询问
2. **Auto-accept edits** - 编辑文件不问，命令仍问
3. **Plan mode** - 只用只读工具，创建计划供批准后执行

**允许特定命令**：
在 `.claude/settings.json` 中允许特定命令，Claude 不再每次询问。
```json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(git status)"
    ]
  }
}
```

**作用域**：从组织策略到个人偏好。详见 Permissions 文档。

---

### Work Effectively with Claude Code（使用技巧）

#### 1. **Ask Claude Code for help**

```bash
# 询问如何使用
how do I set up hooks?
what's the best way to structure my CLAUDE.md?

# 内置命令
/init     # 创建 CLAUDE.md
/agents   # 配置自定义 subagents
/doctor   # 诊断常见问题
```

#### 2. **It's a conversation**

**不需要完美提示**：
```bash
Fix the login bug

# [Claude 调查，尝试]
That's not quite right. The issue is in the session handling.

# [Claude 调整方法]
```

**迭代，不要重新开始。**

#### 3. **Interrupt and steer**

**随时中断**：
- 走错路径时，直接输入纠正
- 按 Enter，Claude 会停止并调整
- 不需要等待完成或重新开始

#### 4. **Be specific upfront**

**越精确，越少纠正**：
```bash
# ❌ 不好
Fix the bug

# ✅ 好
The checkout flow is broken for users with expired cards.
Check src/payments/ for the issue, especially token refresh.
Write a failing test first, then fix it.
```

**模糊提示可行，但需要更多引导。**

#### 5. **Give Claude something to verify against**

**包含验证内容**：
- 测试用例
- 预期 UI 的截图
- 定义的输出

**示例**：
```bash
Implement validateEmail. Test cases: 'user@example.com' → true,
'invalid' → false, 'user@.com' → false. Run the tests after.
```

**视觉工作**：粘贴设计截图，让 Claude 比较实现。

#### 6. **Explore before implementing**

**复杂问题：分离研究和编码**。

**Plan mode**（Shift+Tab 两次）：
```bash
Read src/auth/ and understand how we handle sessions.
Then create a plan for adding OAuth support.
```

**两阶段方法**：
1. 分析代码库
2. 审查计划，通过对话优化
3. 让 Claude 实现

**比直接编码产生更好结果。**

#### 7. **Delegate, don't dictate**

**像委托给有能力的同事**：
- 给上下文和方向
- 信任 Claude 解决细节

```bash
# ✅ 好
The checkout flow is broken for users with expired cards.
The relevant code is in src/payments/. Can you investigate and fix it?
```

**不需要指定读哪些文件或运行什么命令。Claude 会解决。**

---

## 💡 学习感悟

### 1. **Agentic Loop 的优雅**

三阶段循环（Context → Action → Verify）简单但强大：
- **自适应**：根据任务调整
- **链式**：数十个操作链接
- **纠错**：中途调整

这与 OpenClaw 的工作方式类似，但 Claude Code 更强调**自主性**和**循环迭代**。

### 2. **工具分类的清晰性**

5 大类别清晰定义了 AI Agent 的能力边界：
- **File operations** - 文件系统
- **Search** - 信息检索
- **Execution** - 命令执行
- **Web** - 网络访问
- **Code intelligence** - 代码理解

这是设计 AI Agent 系统的好参考。

### 3. **上下文管理的策略**

Claude Code 的上下文管理策略很成熟：
- **自动压缩** - 接近限制时自动管理
- **持久化规则** - CLAUDE.md 而非对话历史
- **Skills 按需加载** - 只在使用时加载完整内容
- **Subagents 隔离** - 独立上下文

这些策略可以借鉴到 OpenClaw。

### 4. **会话管理的灵活性**

**Resume vs Fork** 的设计很巧妙：
- **Resume** - 继续工作，相同 session ID
- **Fork** - 尝试不同方法，新 session ID

这解决了"想尝试不同方法但不想影响原会话"的需求。

### 5. **安全机制的平衡**

**Checkpoints + Permissions** 的组合：
- **Checkpoints** - 文件修改可逆（本地）
- **Permissions** - 控制能力（三级模式）

平衡了**安全性**和**效率**。

### 6. **"Delegate, don't dictate" 的哲学**

这是 AI Agent 使用的核心原则：
- 给上下文和方向
- 信任 AI 解决细节
- 不需要微管理

这符合 **"AI as colleague"** 而非 "AI as tool" 的理念。

---

## 🎯 实践建议

### 1. **理解 Agentic Loop**

在实践中观察这个循环：
```bash
# 观察 Claude 的工作流程
fix the failing tests

# Claude 会：
# 1. Run tests（收集上下文）
# 2. Read errors（收集上下文）
# 3. Search files（收集上下文）
# 4. Edit files（执行操作）
# 5. Run tests again（验证结果）
```

### 2. **使用 Plan Mode**

复杂问题先用 Plan Mode：
```bash
# Shift+Tab 两次进入 Plan Mode
analyze the authentication flow and create a plan for adding OAuth
```

### 3. **管理上下文**

定期检查上下文使用：
```bash
/context  # 查看什么占用空间
/compact  # 手动压缩
```

**持久化规则放在 CLAUDE.md**。

### 4. **使用 Fork 探索不同方法**

```bash
# 当前方法不满意
claude --continue --fork-session

# 尝试不同方法，不影响原会话
```

### 5. **给 Claude 验证标准**

```bash
# 提供测试用例
Implement formatDate(date). Test cases:
- formatDate('2026-03-14') → 'March 14, 2026'
- formatDate('invalid') → null

# 提供截图
# [粘贴 UI 设计截图]
Implement this design
```

### 6. **委托而非指挥**

```bash
# ❌ 不好（微管理）
Read src/auth/login.js, find the validateUser function, add a check for expired tokens, then run npm test

# ✅ 好（委托）
Users with expired tokens can still log in. Fix the authentication flow and verify with tests.
```

---

## 📚 与 OpenClaw 的对比

### 相似之处

1. **Agentic Loop** - 都是 Context → Action → Verify
2. **Tools** - 都有工具系统扩展能力
3. **Memory** - CLAUDE.md vs AGENTS.md，Auto Memory vs MEMORY.md
4. **Sessions** - 都有会话管理

### 差异之处

1. **权限模式** - Claude Code 有三级模式，OpenClaw 相对简单
2. **Checkpoints** - Claude Code 自动快照，OpenClaw 依赖 git
3. **上下文管理** - Claude Code 更成熟（自动压缩、Skills 按需加载）
4. **Fork Sessions** - Claude Code 有 fork 概念，OpenClaw 没有

### 可以借鉴

1. **三级权限模式** - Default / Auto-accept / Plan
2. **Fork Sessions** - 尝试不同方法但不影响原会话
3. **Checkpoints** - 文件修改前自动快照
4. **Context 命令** - 查看上下文使用情况

---

## 🏷️ 标签
`#agentic-loop` `#tools` `#context-management` `#sessions` `#permissions` `#best-practices`
