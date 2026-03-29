# 11 - Claude Code Desktop Get Started 学习笔记

**学习时间**：2026-03-14 14:40
**页面地址**：https://code.claude.com/docs/en/desktop-quickstart

---

## 📖 原文要点

### Desktop App 简介

**Claude Code Desktop** 提供 Claude Code 的图形界面，无需终端。

**核心功能**：
- 🎨 **Visual diff review** - 可视化差异审查
- 🖥️ **Live app preview** - 实时应用预览
- 🔄 **GitHub PR monitoring with auto-merge** - GitHub PR 监控与自动合并
- 🌳 **Parallel sessions with Git worktree isolation** - 并行会话与 Git worktree 隔离
- ⏰ **Scheduled tasks** - 定时任务
- ☁️ **Run tasks remotely** - 远程运行任务

**三个标签页**：

| Tab | 功能 |
|-----|------|
| **Chat** | 通用对话，无文件访问（类似 claude.ai） |
| **Cowork** | 自主后台 agent，在云 VM 中工作，独立运行 |
| **Code** | 交互式编码助手，直接访问本地文件，实时审查和批准每个更改 |

**本页重点**：Code 标签。

**要求**：Pro、Max、Teams 或 Enterprise 订阅。

---

## 🚀 Install

### 步骤

**1. Download the app**

**macOS**：Universal build for Intel and Apple Silicon
- 下载链接：claude.ai/api/desktop/darwin/universal/dmg/latest/redirect

**Windows**：
- x64：claude.ai/api/desktop/win32/x64/exe/latest/redirect
- ARM64：claude.ai/api/desktop/win32/arm64/exe/latest/redirect

**Linux**：目前不支持

**2. Sign in**

- macOS：Applications 文件夹启动
- Windows：Start 菜单启动
- 使用 Anthropic 账户登录

**3. Open the Code tab**

- 点击顶部中心的 **Code** 标签
- 如果提示升级 → 需要订阅付费计划
- 如果提示在线登录 → 完成登录并重启应用
- 如果看到 403 错误 → 查看认证故障排除

**重要**：
- Desktop app 包含 Claude Code
- **不需要**单独安装 Node.js 或 CLI
- 要从终端使用 `claude`，需要单独安装 CLI

---

## 🎯 Start Your First Session

### 1. Choose an environment and folder

**Local**（本地）：
- 在你的机器上运行 Claude
- 直接使用你的文件
- 点击 **Select folder** 选择项目目录

**Remote**（远程）：
- 在 Anthropic 云基础设施上运行会话
- 即使关闭应用也继续运行
- 使用与 Claude Code on the Web 相同的基础设施

**SSH**：
- 通过 SSH 连接到远程机器（你的服务器、云 VM、dev containers）
- Claude Code 必须安装在远程机器上

**建议**：从小项目开始，你知道最好的项目，这是最快看到 Claude Code 能力的方式。

**Windows 要求**：必须安装 Git（大多数 Mac 默认包含）。

### 2. Choose a model

- 从发送按钮旁边的下拉菜单选择模型
- 比较 Opus、Sonnet 和 Haiku
- **会话开始后不能更改模型**

### 3. Tell Claude what to do

**示例提示词**：
```bash
Find a TODO comment and fix it
Add tests for the main function
Create a CLAUDE.md with instructions for this codebase
```

**Session 概念**：
- Session 是与 Claude 关于代码的对话
- 每个会话跟踪自己的上下文和更改
- 可以同时处理多个任务而不互相干扰

### 4. Review and accept changes

**默认**：Code 标签以 **Ask permissions mode** 启动
- Claude 提议更改
- 等待你的批准
- 然后应用更改

**你会看到**：
- **Diff view** - 显示每个文件将更改的确切内容
- **Accept/Reject 按钮** - 批准或拒绝每个更改
- **Real-time updates** - Claude 处理请求时的实时更新

**如果拒绝更改**：
- Claude 会问你想如何不同地进行
- 文件在你接受前不会被修改

---

## 🎓 Now What?

### Interrupt and Steer

- 可以在任何时候中断 Claude
- 如果走错路径，点击停止按钮或输入修正并按 **Enter**
- Claude 停止当前工作并根据你的输入调整
- **不需要**等待完成或重新开始

### Give Claude More Context

**提供上下文的方式**：
- 输入 `@filename` 在提示框中拉取特定文件
- 使用附件按钮附加图像和 PDF
- 直接拖放文件到提示框

**更多上下文 = 更好结果**

### Use Skills for Repeatable Tasks

**访问方式**：
- 输入 `/` 或点击 **+** → **Slash commands**

**包含**：
- Built-in commands
- Custom skills
- Plugin skills

**Skills 是可重用提示**，可以在需要时调用，如代码审查清单或部署步骤。

### Review Changes Before Committing

**Diff View 流程**：
1. Claude 编辑文件后，出现 `+12 -1` 指示器
2. 点击打开 diff view
3. 逐文件审查修改
4. 对特定行评论
5. Claude 阅读评论并修订
6. 点击 **Review code** 让 Claude 自己评估差异并留下内联建议

### Adjust How Much Control You Have

**Permission Mode** 控制平衡：

| Mode | 描述 |
|------|------|
| **Ask permissions**（默认） | 每次编辑前需要批准 |
| **Auto accept edits** | 自动接受文件编辑，更快迭代 |
| **Plan mode** | 让 Claude 规划方法而不触摸任何文件，适合大型重构前 |

### Add Plugins for More Capabilities

**步骤**：
1. 点击提示框旁边的 **+** 按钮
2. 选择 **Plugins**
3. 浏览和安装插件

**Plugins 添加**：
- Skills
- Agents
- MCP servers
- 更多

### Preview Your App

**Preview 下拉菜单**：
- 在 desktop 中直接运行 dev server
- Claude 可以查看运行的应用
- 测试端点
- 检查日志
- 迭代看到的内容

### Track Your Pull Request

**PR 监控功能**：
- Claude Code 监控 CI 检查结果
- 可以自动修复失败
- 所有检查通过后自动合并 PR

### Put Claude on a Schedule

**Scheduled Tasks**：
- 自动按循环运行 Claude
- 每日代码审查（每天早上）
- 每周依赖审计
- 从连接工具提取的简报

### Scale Up When You're Ready

**Parallel Sessions**：
- 从侧边栏打开并行会话
- 一次处理多个任务
- 每个在自己的 Git worktree

**Long-running Work**：
- 发送到云端
- 即使关闭应用也继续运行

**Continue in Another Surface**：
- 如果任务需要更长时间
- 在 web 或 IDE 中继续会话

**Connect External Tools**：
- GitHub
- Slack
- Linear
- 将工作流整合在一起

---

## 💡 Learning Insights

### 1. **GUI 的价值**

Desktop App 提供了 GUI，这对**不熟悉终端的用户**友好：
- **Visual Diff View** - 比终端 diff 更直观
- **Preview** - 内置应用预览，无需外部工具
- **PR Monitoring** - 自动化 PR 跟踪

这降低了**入门门槛**。

### 2. **三个 Tab 的分工**

**三个 Tab 的设计很清晰**：
- **Chat** - 通用对话（类似 ChatGPT）
- **Cowork** - 自主后台工作（类似 Async Agent）
- **Code** - 交互式编码（类似 Terminal CLI）

**用户可以根据需求选择**：
- 快速问题 → Chat
- 后台任务 → Cowork
- 编码工作 → Code

### 3. **Permission Mode 的平衡**

**三种 Permission Mode**：
- **Ask permissions** - 安全但慢
- **Auto accept edits** - 快但有风险
- **Plan mode** - 先理解再执行

**这平衡了**：
- **安全性** vs **效率**
- **控制** vs **自主**

**用户可以根据任务性质选择**。

### 4. **Parallel Sessions 的扩展性**

**Parallel Sessions + Git Worktrees**：
- 每个会话有自己的 Git worktree
- 避免文件冲突
- 可以同时处理多个任务

**这解决了** **多任务并行** 的问题。

### 5. **Scheduled Tasks 的自动化**

**Scheduled Tasks 提供了自动化能力**：
- 每日代码审查
- 每周依赖审计
- 定期简报

**这实现了** **主动工作**，而不是被动响应。

### 6. **与 CLI 的互操作性**

**Desktop 和 CLI 可以同时运行**：
- 共享配置（CLAUDE.md、MCP servers、hooks、skills、settings）
- 可以在同一个项目上工作

**这提供了** **灵活性** - 根据场景选择工具。

---

## 🎯 Practical Recommendations

### 1. **从小项目开始**

```bash
# 选择你熟悉的小项目
# 理解 Claude Code 的能力
# 逐步扩展到更大项目
```

### 2. **根据任务选择 Permission Mode**

**Ask permissions**：
- 不熟悉的代码库
- 关键功能
- 学习阶段

**Auto accept edits**：
- 信任的代码库
- 快速迭代
- 小修改

**Plan mode**：
- 大型重构
- 多文件更改
- 需要先理解方法

### 3. **利用 Visual Diff View**

**工作流**：
1. 让 Claude 做更改
2. 点击 `+12 -1` 指示器
3. 逐文件审查
4. 对可疑更改评论
5. Claude 修订
6. 满意后接受

### 4. **使用 Skills 简化重复任务**

**创建 Skills**：
```markdown
# .claude/skills/review/SKILL.md
---
name: review
description: Code review checklist
---

Review code for:
1. Security issues
2. Performance problems
3. Code style
4. Test coverage
```

**调用**：`/review`

### 5. **设置定时任务**

**每日审查**：
- Schedule: Daily 9:00 AM
- Task: Review yesterday's code

**每周审计**：
- Schedule: Weekly Monday 10:00 AM
- Task: Check dependencies

### 6. **并行会话处理多任务**

**场景**：同时修复多个 bug

**流程**：
1. Session 1 → Bug #1
2. Session 2 → Bug #2
3. 每个有自己的 worktree
4. 不会冲突

---

## 📚 与 OpenClaw 的对比

### 相似之处

1. **多平台** - 都支持不同界面
2. **Skills** - 都有可重用提示
3. **权限控制** - 都有权限管理
4. **会话管理** - 都支持多会话

### 差异之处

1. **GUI** - Desktop 有完整 GUI，OpenClaw 依赖聊天平台
2. **Preview** - Desktop 有内置预览，OpenClaw 需要外部工具
3. **PR 监控** - Desktop 有自动监控和合并，OpenClaw 没有
4. **定时任务** - Desktop 有定时任务，OpenClaw 依赖 cron
5. **三个 Tab** - Desktop 有 Chat/Cowork/Code，OpenClaw 单一模式

### 可以借鉴

1. **Visual Diff View** - 内置代码审查界面
2. **Permission Mode** - 三级权限控制
3. **PR Monitoring** - 自动 PR 跟踪和合并
4. **Scheduled Tasks** - 内置定时任务系统
5. **Preview Integration** - 应用预览集成
6. **Three-Tab Design** - 不同工作模式的清晰分离

---

## 🏷️ 标签
`#desktop` `#gui` `#visual-diff` `#parallel-sessions` `#scheduled-tasks` `#permission-modes` `#preview`
