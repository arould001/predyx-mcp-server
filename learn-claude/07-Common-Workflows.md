# 07 - Common Workflows 学习笔记

**学习时间**：2026-03-14 14:02  
**页面地址**：https://code.claude.com/docs/en/common-workflows

---

## 📖 原文要点

本页面涵盖日常开发的实用工作流程：探索不熟悉的代码、调试、重构、写测试、创建 PR、管理会话。每个章节包含可适配到你自己项目的示例提示。

---

## 🔍 理解新代码库

### 快速获取代码库概览

**场景**：刚加入新项目，需要快速理解结构。

**步骤**：
```bash
cd /path/to/project
claude
```

**提示词**：
```bash
# 高层概览
give me an overview of this codebase

# 深入特定组件
explain the main architecture patterns used here
what are the key data models?
how is authentication handled?
```

**技巧**：
- 从广泛问题开始，然后缩小到特定区域
- 询问编码约定和模式
- 请求项目特定术语词汇表

### 查找相关代码

**场景**：需要定位与特定功能相关的代码。

**提示词**：
```bash
# 查找相关文件
find the files that handle user authentication

# 理解组件交互
how do these authentication files work together?

# 追踪执行流程
trace the login process from front-end to database
```

**技巧**：
- 具体描述你在找什么
- 使用项目领域语言
- 安装代码智能插件获得精确的"跳转到定义"和"查找引用"导航

---

## 🐛 高效修复 Bug

**场景**：遇到错误消息，需要找到并修复源头。

**提示词**：
```bash
# 分享错误
I'm seeing an error when I run npm test

# 请求修复建议
suggest a few ways to fix the @ts-ignore in user.ts

# 应用修复
update user.ts to add the null check you suggested
```

**技巧**：
- 告诉 Claude 重现问题的命令和堆栈跟踪
- 提及重现错误的步骤
- 说明错误是间歇性还是持续性

---

## 🔧 重构代码

**场景**：需要更新旧代码使用现代模式和实践。

**提示词**：
```bash
# 识别遗留代码
find deprecated API usage in our codebase

# 获取重构建议
suggest how to refactor utils.js to use modern JavaScript features

# 安全应用更改
refactor utils.js to use ES2024 features while maintaining the same behavior

# 验证重构
run tests for the refactored code
```

**技巧**：
- 让 Claude 解释现代方法的好处
- 请求更改在需要时保持向后兼容
- 小的、可测试的增量重构

---

## 🤖 使用专业化 Subagents

**场景**：用专业化 AI subagents 更有效地处理特定任务。

### 查看可用 subagents
```bash
/agents
```

### 自动使用
Claude Code 自动委派适当任务给专业化 subagents：
```bash
review my recent code changes for security issues
run all tests and fix any failures
```

### 显式请求特定 subagents
```bash
use the code-reviewer subagent to check the auth module
have the debugger subagent investigate why users can't log in
```

### 创建自定义 subagents
```bash
/agents
```

然后选择 "Create New subagent"，定义：
- 描述 subagent 目的的唯一标识符（如 code-reviewer, api-designer）
- Claude 何时应该使用此 agent
- 它可以访问哪些工具
- 描述 agent 角色和行为的系统提示

**技巧**：
- 在 `.claude/agents/` 创建项目特定 subagents 供团队共享
- 使用描述性 description 字段启用自动委派
- 限制工具访问到每个 subagent 实际需要的
- 查看 subagents 文档获取详细示例

---

## 📋 使用 Plan Mode 安全分析代码

Plan Mode 指示 Claude 通过只读操作分析代码库创建计划，非常适合探索代码库、规划复杂更改或安全审查代码。

### 何时使用 Plan Mode

- **Multi-step implementation**：功能需要编辑多个文件
- **Code exploration**：在更改前彻底研究代码库
- **Interactive development**：与 Claude 迭代方向

### 如何使用 Plan Mode

**会话中切换**：
- Shift+Tab 循环权限模式
- Normal → Auto-Accept（⏵⏵ accept edits on）→ Plan Mode（⏸ plan mode on）

**启动新会话**：
```bash
claude --permission-mode plan
```

**Headless 查询**：
```bash
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### 示例：规划复杂重构

```bash
claude --permission-mode plan

I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.
```

Claude 分析当前实现并创建综合计划。用后续问题优化：
```bash
What about backward compatibility?
How should we handle database migration?
```

**Ctrl+G** 在默认文本编辑器中打开计划，可直接编辑。

### 配置 Plan Mode 为默认

```json
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

---

## 🧪 处理测试

**场景**：需要为未覆盖代码添加测试。

**提示词**：
```bash
# 识别未测试代码
find functions in NotificationsService.swift that are not covered by tests

# 生成测试脚手架
add tests for the notification service

# 添加有意义的测试用例
add test cases for edge conditions in the notification service

# 运行并验证测试
run the new tests and fix any failures
```

**特点**：
- Claude 生成遵循项目现有模式和约定的测试
- 具体描述要验证的行为
- Claude 检查现有测试文件匹配已使用的风格、框架、断言模式

**全面覆盖**：
- 要求 Claude 识别可能遗漏的边缘情况
- Claude 分析代码路径并建议错误条件、边界值、意外输入的测试

---

## 🔀 创建 Pull Requests

可以直接要求 Claude（"create a pr for my changes"），或逐步引导：

**提示词**：
```bash
# 总结更改
summarize the changes I've made to the authentication module

# 生成 PR
create a pr

# 审查和优化
enhance the PR description with more context about the security improvements
```

**会话链接**：
- 用 `gh pr create` 创建 PR 时，会话自动链接到该 PR
- 可稍后用 `claude --from-pr <number>` 恢复

**建议**：提交前审查 Claude 生成的 PR，要求 Claude 强调潜在风险或考虑。

---

## 📄 处理文档

**场景**：需要为代码添加或更新文档。

**提示词**：
```bash
# 识别未文档化代码
find functions without proper JSDoc comments in the auth module

# 生成文档
add JSDoc comments to the undocumented functions in auth.js

# 审查和增强
improve the generated documentation with more context and examples

# 验证文档
check if the documentation follows our project standards
```

**技巧**：
- 指定文档风格（JSDoc、docstrings 等）
- 要求文档中的示例
- 请求公共 API、接口、复杂逻辑的文档

---

## 🖼️ 处理图像

**场景**：需要在代码库中处理图像，希望 Claude 帮助分析图像内容。

### 添加图像到对话

**方法**：
1. 拖放图像到 Claude Code 窗口
2. 复制图像并粘贴到 CLI（**ctrl+v**，**不要用 cmd+v**）
3. 提供图像路径给 Claude："Analyze this image: /path/to/your/image.png"

### 分析图像

**提示词**：
```bash
What does this image show?
Describe the UI elements in this screenshot
Are there any problematic elements in this diagram?
```

### 用图像提供上下文

```bash
Here's a screenshot of the error. What's causing it?
This is our current database schema. How should we modify it for the new feature?
```

### 从视觉内容获取代码建议

```bash
Generate CSS to match this design mockup
What HTML structure would recreate this component?
```

**技巧**：
- 文本描述不清楚或繁琐时用图像
- 包含错误、UI 设计、图表截图获得更好上下文
- 可在对话中处理多个图像
- 图像分析适用于图表、截图、模型等
- Claude 引用图像时（如 [Image #1]），Cmd+Click（Mac）或 Ctrl+Click（Windows/Linux）链接在默认查看器中打开图像

---

## 📂 引用文件和目录

用 `@` 快速包含文件或目录，无需等待 Claude 读取。

### 引用单个文件

```bash
Explain the logic in @src/utils/auth.js
```
**包含文件完整内容到对话**。

### 引用目录

```bash
What's the structure of @src/components?
```
**提供带文件信息的目录列表**。

### 引用 MCP 资源

```bash
Show me the data from @github:repos/owner/repo/issues
```
**用格式 `@server:resource` 从连接的 MCP servers 获取数据**。

**技巧**：
- 文件路径可相对或绝对
- `@` 文件引用添加文件目录和父目录的 CLAUDE.md 到上下文
- 目录引用显示文件列表，不是内容
- 可在单条消息中引用多个文件（如 "@file1.js and @file2.js"）

---

## 🧠 使用 Extended Thinking（思考模式）

Extended thinking 默认启用，给 Claude 空间在响应前逐步推理复杂问题。推理在 verbose mode 可见，用 Ctrl+O 切换。

**Opus 4.6 和 Sonnet 4.6 支持自适应推理**：模型根据你的 effort level 设置动态分配思考，而不是固定思考 token 预算。

### 配置思考模式

| 范围 | 如何配置 | 详情 |
|------|---------|------|
| **Effort level** | 运行 `/effort`，在 `/model` 调整，或设置 `CLAUDE_CODE_EFFORT_LEVEL` | 控制 Opus 4.6 和 Sonnet 4.6 的思考深度 |
| **ultrathink 关键字** | 在提示中包含 "ultrathink" | 为该轮在 Opus 4.6 和 Sonnet 4.6 上设置 effort 为 high |
| **Toggle 快捷键** | 按 Option+T（macOS）或 Alt+T（Windows/Linux） | 为当前会话切换思考开/关（所有模型） |
| **全局默认** | 用 `/config` 切换思考模式 | 设置跨所有项目的默认（所有模型）<br>保存为 `~/.claude/settings.json` 中的 `alwaysThinkingEnabled` |
| **限制 token 预算** | 设置 `MAX_THINKING_TOKENS` 环境变量 | 限制思考预算到特定 token 数（Opus 4.6 和 Sonnet 4.6 除非设为 0 否则忽略） |

**查看思考过程**：按 Ctrl+O 切换 verbose mode，看到显示为灰色斜体文本的内部推理。

### Extended Thinking 如何工作

**Opus 4.6 和 Sonnet 4.6**：
- 使用自适应推理
- 模型根据选择的 effort level 动态分配思考 tokens
- 这是调整速度和推理深度权衡的推荐方式

**旧模型**：
- 使用固定预算最多 31,999 tokens 从输出预算
- 可用 `MAX_THINKING_TOKENS` 环境变量限制
- 或通过 `/config` 或 Option+T/Alt+T 切换完全禁用

**禁用自适应思考**：设置 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`。

**收费**：所有使用的思考 tokens 都收费，即使 Claude 4 模型显示总结思考。

---

## 🔄 恢复之前的对话

**启动时恢复**：
```bash
# 继续当前目录最近对话
claude --continue

# 打开对话选择器或按名称恢复
claude --resume

# 恢复链接到特定 PR 的会话
claude --from-pr 123
```

**会话内**：用 `/resume` 切换到不同对话。

**会话存储**：每个项目目录。`/resume` 选择器显示来自同一 git 仓库的会话，包括 worktrees。

---

## 📛 命名你的会话

给会话描述性名称，稍后查找。这是同时处理多个任务或功能时的最佳实践。

### 命名会话

**启动时**：
```bash
claude -n auth-refactor
```

**会话中**：
```bash
/rename auth-refactor
```
**也显示名称在提示栏**。

**从选择器**：运行 `/resume`，导航到会话，按 R。

### 按名称恢复

**命令行**：
```bash
claude --resume auth-refactor
```

**会话内**：
```bash
/resume auth-refactor
```

---

## 🎯 使用会话选择器

`/resume` 命令（或 `claude --resume` 无参数）打开交互式会话选择器。

### 键盘快捷键

| 快捷键 | 动作 |
|--------|------|
| `↑` / `↓` | 在会话间导航 |
| `→` / `←` | 展开或折叠分组会话 |
| `Enter` | 选择并恢复高亮会话 |
| `P` | 预览会话内容 |
| `R` | 重命名高亮会话 |
| `/` | 搜索过滤会话 |
| `A` | 在当前目录和所有项目间切换 |
| `B` | 过滤到当前 git 分支的会话 |
| `Esc` | 退出选择器或搜索模式 |

### 会话组织

选择器显示带帮助性元数据的会话：
- 会话名称或初始提示
- 自上次活动以来经过的时间
- 消息计数
- Git 分支（如适用）

**Forked 会话**（用 `/rewind` 或 `--fork-session` 创建）在其根会话下分组，更容易找到相关对话。

### 技巧

- **早期命名会话**：在开始独特任务时用 `/rename` — 稍后找 "payment-integration" 比 "explain this function" 容易得多
- **用 `--continue`** 快速访问当前目录最近对话
- **用 `--resume session-name`** 当你知道需要哪个会话时
- **用 `--resume`**（无名称）当需要浏览和选择时
- **脚本用 `claude --continue --print "prompt"`** 在非交互模式恢复
- **在选择器按 P** 恢复前预览会话
- **恢复的对话** 以与原始相同的模型和配置开始

---

## 🌳 用 Git Worktrees 运行并行会话

**场景**：同时处理多个任务，需要每个 Claude 会话有自己的代码库副本，以便更改不冲突。

Git worktrees 通过创建各自有自己文件和分支的独立工作目录来解决这个问题，同时共享相同的仓库历史和远程连接。

### 使用 --worktree 标志

```bash
# 在名为 "feature-auth" 的 worktree 启动 Claude
# 创建 .claude/worktrees/feature-auth/ 带新分支
claude --worktree feature-auth

# 在单独 worktree 启动另一会话
claude --worktree bugfix-123
```

**省略名称**：Claude 自动生成随机名称：
```bash
# 自动生成名称如 "bright-running-fox"
claude --worktree
```

**Worktree 位置**：`<repo>/.claude/worktrees/<name>`，从默认远程分支分支。Worktree 分支命名为 `worktree-<name>`。

**会话中**：也可要求 Claude "work in a worktree" 或 "start a worktree"，它会自动创建一个。

### Subagent Worktrees

Subagents 也可用 worktree 隔离并行工作无冲突。

**配置**：
- 要求 Claude "use worktrees for your agents"
- 或在自定义 subagent 的 frontmatter 添加 `isolation: worktree`

每个 subagent 获得自己的 worktree，在 subagent 完成无更改时自动清理。

### Worktree 清理

**退出 worktree 会话时**，Claude 根据是否做了更改处理清理：

- **无更改**：worktree 及其分支自动移除
- **存在更改或提交**：Claude 提示你保留或移除 worktree
  - **保留**：保留目录和分支，可稍后返回
  - **移除**：删除 worktree 目录及其分支，丢弃所有未提交更改和提交

**手动清理**：在 Claude 会话外，用手动 worktree 管理。

**.gitignore**：添加 `.claude/worktrees/` 到 `.gitignore` 防止 worktree 内容在主仓库中显示为未跟踪文件。

### 手动管理 Worktrees

**更多控制**：用 Git 直接创建 worktrees。

```bash
# 用新分支创建 worktree
git worktree add ../project-feature-a -b feature-a

# 用现有分支创建 worktree
git worktree add ../project-bugfix bugfix-123

# 在 worktree 启动 Claude
cd ../project-feature-a && claude

# 完成后清理
git worktree list
git worktree remove ../project-feature-a
```

**初始化开发环境**：记住在每个新 worktree 中根据项目设置初始化开发环境。可能包括运行依赖安装（npm install, yarn）、设置虚拟环境或遵循项目标准设置流程。

### 非 Git 版本控制

Worktree 隔离默认与 git 工作。对于其他版本控制系统（SVN、Perforce、Mercurial），配置 `WorktreeCreate` 和 `WorktreeRemove` hooks 提供自定义 worktree 创建和清理逻辑。

---

## 🔔 获得当 Claude 需要注意时的通知

**场景**：启动长期运行任务并切换到另一窗口，设置桌面通知以便知道 Claude 何时完成或需要输入。

**使用 Notification hook 事件**：每当 Claude 等待权限、空闲等待新提示或完成认证时触发。

### 添加 hook 到设置

**macOS**：
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

**Linux**：
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
          }
        ]
      }
    ]
  }
}
```

**Windows**：
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
          }
        ]
      }
    ]
  }
}
```

### 可选缩小 matcher

默认 hook 在所有通知类型触发。只为特定事件触发，设置 `matcher` 字段为这些值之一：

| Matcher | 触发时机 |
|---------|---------|
| `permission_prompt` | Claude 需要你批准工具使用 |
| `idle_prompt` | Claude 完成并等待下一个提示 |
| `auth_success` | 认证完成 |
| `elicitation_dialog` | Claude 问你问题 |

### 验证 hook

运行 `/hooks` 选择 Notification 确认 hook 出现。选择它显示将运行的命令。

---

## 🛠️ 将 Claude 用作 Unix 风格工具

### 添加 Claude 到验证流程

**场景**：将 Claude Code 用作 linter 或代码审查器。

**添加到构建脚本**：
```json
// package.json
{
  "scripts": {
    "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
  }
}
```

**技巧**：
- 在 CI/CD 管道用 Claude 自动代码审查
- 自定义提示检查与你项目相关的特定问题
- 考虑为不同类型的验证创建多个脚本

### Pipe in, pipe out

**场景**：管道数据进入 Claude，以结构化格式获取数据。

```bash
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

**技巧**：
- 用管道将 Claude 集成到现有 shell 脚本
- 与其他 Unix 工具组合获得强大工作流
- 考虑用 `--output-format` 获得结构化输出

### 控制输出格式

**场景**：需要 Claude 输出为特定格式，特别是集成 Claude Code 到脚本或其他工具时。

#### 1. Text format（默认）

```bash
cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
```
**只输出 Claude 纯文本响应**（默认行为）。

#### 2. JSON format

```bash
cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
```
**输出带元数据（包括成本和持续时间）的消息 JSON 数组**。

#### 3. Streaming JSON format

```bash
cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
```
**实时输出一系列 JSON 对象**。每条消息是有效 JSON 对象，但整个输出如果连接不是有效 JSON。

**技巧**：
- **`--output-format text`** 用于简单集成，只需 Claude 响应
- **`--output-format json`** 当需要完整对话日志
- **`--output-format stream-json`** 用于每个对话轮次的实时输出

---

## ❓ 询问 Claude 关于其能力

Claude 内置访问其文档，可回答关于自身功能和限制的问题。

### 示例问题

```bash
can Claude Code create pull requests?
how does Claude Code handle permissions?
what skills are available?
how do I use MCP with Claude Code?
how do I configure Claude Code for Amazon Bedrock?
what are the limitations of Claude Code?
```

**Claude 提供基于文档的答案**。对于可执行示例和动手演示，参考上面的特定工作流部分。

**技巧**：
- Claude 总是可访问最新 Claude Code 文档，无论你使用的版本
- 问具体问题获得详细答案
- Claude 可解释复杂功能如 MCP 集成、企业配置、高级工作流

---

## 💡 学习感悟

### 1. **工作流的完整性**

这个页面涵盖了**从探索到提交**的完整开发周期：
1. 理解新代码库
2. 修复 Bug
3. 重构代码
4. 写测试
5. 创建 PR
6. 处理文档

每个环节都有具体的提示词和技巧。

### 2. **Plan Mode 的价值**

Plan Mode 是一个重要的**安全机制**：
- 在修改前先分析
- 创建可审查的计划
- 减少错误风险

这符合 **"Measure twice, cut once"** 原则。

### 3. **并行工作的能力**

Git Worktrees + Sessions 的组合：
- **Worktrees** - 代码隔离
- **Sessions** - 会话隔离
- **命名** - 易于管理

这解决了**多任务并行**的问题。

### 4. **Unix 哲学的体现**

"Pipe in, pipe out" 部分体现了 Unix 哲学：
- **可组合** - 与其他工具链式组合
- **文本流** - 用管道处理数据
- **结构化输出** - JSON/stream-json

这使 Claude Code 可以集成到现有工作流中。

### 5. **通知系统的重要性**

Notification hooks 解决了**长期运行任务**的问题：
- 启动任务
- 切换到其他工作
- 获得通知当完成或需要输入

这是**异步工作**的关键。

### 6. **Extended Thinking 的智能**

Extended Thinking + Adaptive Reasoning：
- **默认启用** - 自动推理
- **自适应** - 根据 effort level 动态分配
- **可控** - 可配置或禁用

这是 **"思考时间 vs 响应速度"** 的权衡。

---

## 🎯 实践建议

### 1. **建立命名习惯**

```bash
# 启动时命名
claude -n auth-refactor

# 或会话中
/rename auth-refactor
```

### 2. **用 Plan Mode 处理复杂任务**

```bash
# 启动 plan mode
claude --permission-mode plan

# 分析后创建计划
# Ctrl+G 编辑计划
# 审查后执行
```

### 3. **设置通知**

**macOS**：
```bash
# 添加到 ~/.claude/settings.json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### 4. **用 Worktrees 并行工作**

```bash
# 功能开发
claude --worktree feature-auth

# Bug 修复
claude --worktree bugfix-123
```

### 5. **集成到 CI/CD**

```json
// package.json
{
  "scripts": {
    "lint:claude": "claude -p 'review code for typos and issues'",
    "review:pr": "claude -p 'review this PR for security issues'"
  }
}
```

### 6. **用 @ 引用文件**

```bash
# 快速引用
Explain the logic in @src/utils/auth.js

# 目录结构
What's the structure of @src/components?

# MCP 资源
Show me the data from @github:repos/owner/repo/issues
```

### 7. **控制思考模式**

```bash
# 切换 verbose mode（看推理）
Ctrl+O

# 调整 effort level
/effort

# 单次深度思考
ultrathink analyze this complex algorithm
```

---

## 📚 与 OpenClaw 的对比

### 相似之处

1. **会话管理** - 都支持 resume/rename
2. **并行工作** - OpenClaw 用不同目录，Claude Code 用 worktrees
3. **工作流** - 都支持探索、修改、测试、提交

### 差异之处

1. **Plan Mode** - Claude Code 有明确的 plan mode，OpenClaw 没有
2. **Worktrees** - Claude Code 自动管理，OpenClaw 手动
3. **通知系统** - Claude Code 有 hooks，OpenClaw 没有
4. **Extended Thinking** - Claude Code 有，OpenClaw 依赖模型

### 可以借鉴

1. **Plan Mode** - 在执行前强制分析
2. **Notification Hooks** - 长期任务通知
3. **Session Picker** - 可视化选择器（快捷键、预览）
4. **Worktree 自动化** - 自动创建和清理

---

## 🏷️ 标签
`#workflows` `#plan-mode` `#worktrees` `#sessions` `#thinking` `#unix` `#notifications`
