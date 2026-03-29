# 09 - Remote Control 学习笔记

**学习时间**：2026-03-14 14:15
**页面地址**：https://code.claude.com/docs/en/remote-control

---

## 📖 原文要点

### 核心概念

**Remote Control** 让你从任何设备继续本地 Claude Code 会话：
- 📱 **手机/平板**
- 💻 **任何浏览器**
- 🔄 **与 claude.ai/code 和 Claude 移动应用配合使用**

**关键特点**：
- ✅ **完全本地** - Claude 在本地运行，不移动到云端
- ✅ **全环境访问** - 文件系统、MCP servers、工具、项目配置都可用
- ✅ **多设备同步** - 对话在所有连接设备间保持同步
- ✅ **自动重连** - 笔记本睡眠或网络断开后自动重连

---

## 🎯 Requirements

### 1. **订阅要求**
- Pro、Max、Team、Enterprise 计划可用
- Team 和 Enterprise 管理员必须先在 admin settings 启用 Claude Code
- **不支持 API keys**

### 2. **认证**
```bash
claude
/login  # 通过 claude.ai 登录
```

### 3. **工作区信任**
```bash
# 至少在项目目录运行一次以接受工作区信任对话框
cd your-project
claude
```

### 4. **版本要求**
- Claude Code v2.1.51 或更高
- 检查版本：`claude --version`

---

## 🚀 启动 Remote Control 会话

### 方法 1：Server Mode（推荐）

```bash
cd your-project
claude remote-control
```

**特点**：
- 进程在终端中保持运行，等待远程连接
- 显示会话 URL
- 按空格键显示 QR 码（手机快速访问）
- 显示连接状态和工具活动

**可用标志**：

| Flag | 描述 |
|------|------|
| `--name "My Project"` | 设置在 claude.ai/code 会话列表中可见的自定义会话标题 |
| `--spawn <mode>` | 并发会话创建方式（same-dir 或 worktree） |
| `--capacity <N>` | 最大并发会话数（默认 32） |
| `--verbose` | 显示详细连接和会话日志 |
| `--sandbox / --no-sandbox` | 启用/禁用文件系统和网络隔离的沙箱 |

**`--spawn` 模式**：
- **same-dir（默认）**：所有会话共享当前工作目录，可能冲突
- **worktree**：每个按需会话获得自己的 git worktree（需要 git repo）

### 方法 2：Interactive Session

```bash
claude --remote-control
```

或会话内：
```bash
/remote-control
```

### 方法 3：From Existing Session

如果会话已在运行，使用 `/remote-control` 启用远程控制。

---

## 📲 从另一设备连接

### 1. **打开会话 URL**
- 在任何浏览器中打开
- 直接跳转到 claude.ai/code 的会话
- 终端显示 URL

### 2. **扫描 QR 码**
- QR 码与会话 URL 一起显示
- 扫描直接在 Claude app 中打开
- `claude remote-control` 模式下按空格键切换 QR 码显示

### 3. **在 claude.ai/code 或 Claude App 中查找**
- 按名称在会话列表中找到会话
- Remote Control 会话显示带绿色状态点的电脑图标

**会话命名来源**（优先级）：
1. `--name` 参数（或 `/remote-control` 传递的名称）
2. 你的最后一条消息
3. `/rename` 值
4. "Remote Control session"（无对话历史时）

---

## ⚙️ 为所有会话启用 Remote Control

**默认**：只在显式运行时激活。

**启用自动 Remote Control**：
```bash
claude
/config
# 设置 "Enable Remote Control for all sessions" 为 true
```

**效果**：
- 每个交互式 Claude Code 进程注册一个远程会话
- 运行多个实例时，每个都有自己的环境和会话
- 要从单个进程运行多个并发会话，用 server mode + `--spawn`

---

## 🔒 Connection and Security

### 连接机制

1. **出站 HTTPS only** - 本地会话只发出站 HTTPS 请求，从不打开入站端口
2. **注册和轮询** - 启动 Remote Control 时，向 Anthropic API 注册并轮询工作
3. **消息路由** - 从另一设备连接时，服务器通过流连接在 web/mobile 客户端和本地会话间路由消息

### 安全机制

- **所有流量通过 TLS** - 与任何 Claude Code 会话相同的传输安全
- **多个短期凭证** - 每个凭证单一用途，独立过期
- **通过 Anthropic API** - 所有通信经过 Anthropic API

---

## 🆚 Remote Control vs Claude Code on the Web

| 方面 | Remote Control | Claude Code on the Web |
|------|---------------|----------------------|
| **执行位置** | 你的机器 | Anthropic 管理的云基础设施 |
| **环境** | 本地 MCP servers、工具、配置 | 云环境 |
| **用途** | 中途本地工作，从另一设备继续 | 无需本地设置启动任务、处理未克隆的 repo、并行运行多个任务 |
| **数据** | 保持在本地 | 在云端 |

**何时用 Remote Control**：
- 本地工作中途想从另一设备继续
- 需要本地 MCP servers 和工具
- 项目配置重要

**何时用 Claude Code on the Web**：
- 无本地设置启动任务
- 处理没有克隆的 repo
- 并行运行多个任务

---

## ⚠️ Limitations

### 1. **一个远程会话 per 交互进程**
- Server mode 外，每个 Claude Code 实例一次支持一个远程会话
- 用 server mode + `--spawn` 从单个进程运行多个并发会话

### 2. **终端必须保持打开**
- Remote Control 作为本地进程运行
- 关闭终端或停止 `claude` 进程 → 会话结束
- 重新运行 `claude remote-control` 启动新的

### 3. **扩展网络中断**
- 机器唤醒但无法访问网络超过约 10 分钟 → 会话超时，进程退出
- 重新运行 `claude remote-control` 启动新会话

---

## 💡 学习感悟

### 1. **本地优先的哲学**

Remote Control 体现了 **"Local-First"** 哲学：
- **数据留在本地** - 不移动到云端
- **完全控制** - 本地文件系统、MCP servers、工具
- **云作为管道** - 云只是消息路由，不是执行环境

这与很多"云优先"的 AI 工具形成对比。

### 2. **无缝跨设备体验**

Remote Control 解决了**跨设备工作流**问题：
- 桌面开始
- 手机继续
- 浏览器切换

所有设备看到**相同对话**，无缝切换。

### 3. **安全的架构设计**

安全设计很巧妙：
- **无入站端口** - 只出站 HTTPS
- **轮询机制** - 不需要打开防火墙
- **短期凭证** - 限制泄露影响
- **TLS 加密** - 传输安全

这避免了传统远程桌面的安全问题。

### 4. **Server Mode 的扩展性**

Server Mode + `--spawn` 提供了**水平扩展**能力：
- 单个进程支持最多 32 个并发会话
- `worktree` 模式避免文件冲突
- 适合团队或高并发场景

### 5. **与 Claude Code on the Web 的互补**

两个功能不是竞争，而是**互补**：
- **Remote Control** - 本地工作延续
- **Web** - 无本地设置开始

根据场景选择，不是二选一。

---

## 🎯 实践建议

### 1. **日常使用场景**

**场景 1：桌面到手机**
```bash
# 桌面
cd my-project
claude remote-control
# 按空格显示 QR 码
# 手机扫描继续工作
```

**场景 2：多设备协作**
```bash
# 启动
claude remote-control --name "API Refactor"

# 从不同设备连接：
# - 桌面浏览器：claude.ai/code
# - 手机：Claude app
# - 平板：Claude app
# 所有设备看到相同对话
```

### 2. **团队使用**

**Server Mode 支持多会话**：
```bash
# 管理员启动
claude remote-control --spawn worktree --capacity 10

# 团队成员连接不同会话
# 每个会话有自己的 worktree
```

### 3. **自动化场景**

**CI/CD 集成**：
```bash
# 在服务器上启动
claude remote-control --name "CI Debug"

# 开发者从手机连接查看和干预
```

### 4. **安全实践**

**沙箱隔离**：
```bash
# 不信任的代码库
claude remote-control --sandbox

# 限制文件系统和网络访问
```

### 5. **会话管理**

**命名最佳实践**：
```bash
# 使用描述性名称
claude remote-control --name "Feature: User Authentication"
claude remote-control --name "Bugfix: Payment Gateway"
claude remote-control --name "Refactor: Database Schema"
```

---

## 📚 与 OpenClaw 的对比

### 相似之处

1. **跨设备** - 都支持跨设备工作
2. **本地优先** - OpenClaw 通过 Discord 等渠道访问本地能力

### 差异之处

1. **Remote Control** - Claude Code 有专门的远程控制功能，OpenClaw 没有
2. **移动应用** - Claude Code 有专门的移动应用，OpenClaw 通过第三方客户端
3. **Server Mode** - Claude Code 有 server mode 支持多会话，OpenClaw 通过多个 gateway

### 可以借鉴

1. **Server Mode** - 支持 `--spawn` 和 `--capacity` 的多会话架构
2. **QR 码连接** - 快速从移动设备连接
3. **会话命名** - 更好的会话识别和管理
4. **自动重连** - 网络中断后的自动恢复机制

---

## 🏷️ 标签
`#remote-control` `#mobile` `#cross-device` `#security` `#server-mode` `#worktree`
