# 17 - Claude Code in Slack 学习笔记

**学习时间**：2026-03-14 15:05
**页面地址**：https://code.claude.com/docs/en/slack

---

## 📖 核心概念

### 是什么
在 Slack 中用 `@Claude` mention 触发 Claude Code session，自动路由到 Claude Code on the web 处理编码任务。

### Use Cases
- **Bug investigation and fixes** - 在 Slack 中报告 bug，Claude 调查修复
- **Quick code reviews and modifications** - 小功能实现或重构
- **Collaborative debugging** - 利用 Slack 讨论的上下文调试
- **Parallel task execution** - 异步启动任务，继续其他工作

---

## 🎯 Prerequisites

| Requirement | Details |
|-------------|---------|
| **Claude Plan** | Pro, Max, Teams, or Enterprise with Claude Code access (premium seats) |
| **Claude Code on the web** | Access enabled |
| **GitHub Account** | Connected to Claude Code on the web, at least one repo authenticated |
| **Slack Authentication** | Slack account linked to Claude account |

---

## 🚀 Setting Up

### 1. Install Claude App in Slack
- Workspace admin 从 Slack App Marketplace 安装
- https://slack.com/marketplace/A08SF47R6P4

### 2. Connect Claude Account
- Open Claude app in Slack
- Go to App Home tab
- Click "Connect"
- Complete authentication flow

### 3. Configure Claude Code on the Web
- Visit claude.ai/code
- Sign in with same account as Slack
- Connect GitHub account
- Authenticate at least one repository

### 4. Choose Routing Mode

**Two modes**:

| Mode | Behavior |
|------|----------|
| **Code only** | All @mentions route to Claude Code sessions. Best for dev-only teams. |
| **Code + Chat** | Intelligent routing between Claude Code (coding) and Claude Chat (writing/analysis). Best for all-in-one teams. |

**Retry as Code**: In Code + Chat mode, can retry a Chat response as Code session.

### 5. Add Claude to Channels
```bash
/invite @Claude
```

- Claude NOT auto-added to any channels
- Must explicitly invite
- Only responds to @mentions in channels where added

---

## 🔄 How It Works

### Automatic Detection
- Claude analyzes message to detect coding intent
- Routes to Claude Code on the web if coding task
- Can explicitly tell Claude to handle as coding task

**Important**:
- Only works in **channels** (public or private)
- **NOT** in DMs

### Context Gathering

**From threads**:
- Gathers context from all messages in thread

**From channels**:
- Looks at recent channel messages

**Purpose**:
- Understand problem
- Select appropriate repository
- Inform approach to task

**Security Note**: Claude may follow directions from context, only use in trusted conversations.

### Session Flow
1. **Initiation** - You @mention Claude with coding request
2. **Detection** - Claude analyzes and detects coding intent
3. **Session creation** - New Claude Code session on claude.ai/code
4. **Progress updates** - Status updates in Slack thread
5. **Completion** - @mention you with summary and action buttons
6. **Review** - "View Session" or "Create PR"

---

## 🎨 User Interface Elements

### App Home
- Connection status
- Connect/disconnect Claude account

### Message Actions
- **View Session** - Open full session in browser
- **Create PR** - Create PR from session changes
- **Retry as Code** - Retry Chat response as Code session
- **Change Repo** - Select different repository

### Repository Selection
- Claude auto-selects based on context
- May show dropdown if multiple repos could apply

---

## 🔐 Access and Permissions

### User-Level Access

| Access Type | Requirement |
|-------------|-------------|
| **Claude Code Sessions** | Each user runs under own account |
| **Usage & Rate Limits** | Counts against individual plan |
| **Repository Access** | Only repos personally connected |
| **Session History** | Appears in claude.ai/code history |

### Workspace-Level Access
- **App installation** - Workspace admins control
- **Enterprise Grid** - Org admins control which workspaces
- **App removal** - Immediately revokes access for all users

### Channel-Based Access Control
- **Invite required** - `/invite @Claude`
- **Channel membership controls access**
- **Access gating through channels**
- **Private channel support**

---

## 📋 Best Practices

### Writing Effective Requests

**Be specific**:
```bash
# ✅ Good
@Claude fix the TypeError in src/auth/login.ts line 42

# ❌ Bad
@Claude fix the bug
```

**Provide context**:
- Mention repository or project
- Include file names, function names, error messages

**Define success**:
- Should Claude write tests?
- Update documentation?
- Create PR?

**Use threads**:
- Reply in threads for bugs/features
- Claude gathers full context

### When to Use Slack vs Web

**Use Slack when**:
- Context exists in Slack discussion
- Want to kick off task asynchronously
- Collaborating with teammates who need visibility

**Use the web directly when**:
- Need to upload files
- Want real-time interaction
- Working on longer, complex tasks

---

## 🛠️ Troubleshooting

### Sessions Not Starting
- Verify Claude account connected in App Home
- Check Claude Code on the web access enabled
- Ensure at least one GitHub repo connected

### Repository Not Showing
- Connect repo in claude.ai/code
- Verify GitHub permissions
- Try disconnecting/reconnecting GitHub

### Wrong Repository Selected
- Click "Change Repo" button
- Include repo name in request

### Authentication Errors
- Disconnect/reconnect Claude account in App Home
- Ensure signed into correct Claude account
- Check plan includes Claude Code access

### Session Expiration
- Sessions remain accessible in claude.ai/code history
- Can continue or reference past sessions

---

## ⚠️ Current Limitations

- **GitHub only** - Currently supports only GitHub repositories
- **One PR at a time** - Each session can create one pull request
- **Rate limits apply** - Uses individual Claude plan limits
- **Web access required** - Must have Claude Code on the web access

---

## 💡 学习感悟

### 1. **Slack 作为 AI 编程入口**

这是**"ChatOps"** 的进化：
- 传统 ChatOps：脚本命令
- Claude Code in Slack：自然语言 + AI 编程

**"在对话中编程"**。

### 2. **Intelligent Routing 的智能**

**Code + Chat mode** 智能路由：
- 分析消息意图
- 自动路由到 Code 或 Chat
- 可手动 retry

**这体现了"AI 理解用户意图"**。

### 3. **Channel-Based Access Control**

**通道级权限控制**：
- 必须显式 invite Claude
- 只在 invited channels 响应
- 可用于限制使用范围

**这是"最小权限原则"**。

### 4. **Context from Slack Discussions**

**利用 Slack 讨论的上下文**：
- Thread context
- Recent channel messages

**这解决了"AI 不知道背景"的问题**。

### 5. **Async + Parallel Work**

**异步并行工作**：
- 在 Slack 启动任务
- 继续其他工作
- 收到通知时查看结果

**这符合"异步协作"趋势**。

### 6. **User-Level vs Workspace-Level**

**双层权限模型**：
- **User-level** - 个人账户、个人 repos、个人 limits
- **Workspace-level** - 管理员控制安装和访问

**平衡了灵活性和控制**。

---

## 🎯 实践建议

### 1. **设置 Code + Chat Mode**

推荐大多数团队使用 Code + Chat mode：
- 单一入口 `@Claude`
- 智能路由
- 可手动切换

### 2. **在专用 Channel 使用**

创建专用 channel：
```bash
#create-dev-channel
/invite @Claude
```

**好处**：
- 集中开发讨论
- 方便 Claude 理解上下文
- 减少噪音

### 3. **用 Thread 提供上下文**

```bash
# Channel
User1: We're seeing TypeError in production

# Thread
User2: I think it's in auth.js
User1: Let me check the logs... it's line 42
User2: @Claude fix the TypeError in auth.js line 42
```

**Claude 看到完整上下文**。

### 4. **明确指定 Repository**

```bash
# ✅ Good
@Claude in the payments-service repo, implement fraud detection

# ❌ Bad
@Claude implement fraud detection
```

### 5. **Review 后再 Create PR**

- 先 "View Session" 检查代码
- 确认正确后再 "Create PR"

### 6. **监控 Rate Limits**

- Sessions 使用个人 plan limits
- 大量用户时考虑 Enterprise plan

---

## 📚 与 OpenClaw Discord 的对比

### 相似之处
1. **Chat platform integration** - 都在聊天平台集成
2. **@mention trigger** - 都用 mention 触发
3. **Context from discussions** - 都利用讨论上下文

### 差异之处
1. **Routing** - Claude Code 有智能路由（Code vs Chat），OpenClaw 没有
2. **Session creation** - Claude Code 创建 Web session，OpenClaw 在本地运行
3. **Channel-based access** - Claude Code 需要显式 invite，OpenClaw 自动响应
4. **Multi-repo** - Claude Code 支持多 repo 选择，OpenClaw 通常单项目

### 可以借鉴
1. **Intelligent Routing** - Code vs Chat 智能路由
2. **Channel-based Access Control** - 通道级权限
3. **Thread Context** - 利用 thread 上下文
4. **Async Notifications** - 完成后 @mention 通知
5. **Retry Mechanism** - Retry as Code/Chat 机制

---

## 🏷️ 标签
`#slack` `#chatops` `#async` `#intelligent-routing` `#channel-access` `#collaboration`
