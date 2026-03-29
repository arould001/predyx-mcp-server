# 10 - Claude Code on the Web 学习笔记

**学习时间**：2026-03-14 14:35
**页面地址**：https://code.claude.com/docs/en/claude-code-on-the-web

---

## 📖 原文要点

### 核心概念

**Claude Code on the Web** 在安全的云基础设施上异步运行 Claude Code 任务。

**适用场景**：
- ✅ **回答问题** - 代码架构、功能实现
- ✅ **Bug 修复和常规任务** - 不需要频繁引导的定义良好任务
- ✅ **并行工作** - 同时处理多个 bug 修复
- ✅ **不在本地的仓库** - 处理没有本地克隆的代码
- ✅ **后端更改** - Claude 可以写测试然后写代码通过测试

**Research Preview** - 目前处于研究预览阶段。

---

## 👥 谁可以使用

**可用计划**：
- Pro 用户
- Max 用户
- Team 用户
- Enterprise 用户（需 premium seats 或 Chat + Claude Code seats）

---

## 🚀 Getting Started

**步骤**：
1. 访问 **claude.ai/code**
2. 连接 GitHub 账户
3. 在仓库中安装 Claude GitHub app
4. 选择默认环境
5. 提交编码任务
6. 在 diff view 中审查更改，迭代评论，然后创建 PR

---

## ⚙️ How It Works

**执行流程**：
1. **Repository cloning** - 仓库克隆到 Anthropic 管理的虚拟机
2. **Environment setup** - Claude 准备安全云环境，运行 setup script（如配置）
3. **Network configuration** - 根据设置配置网络访问
4. **Task execution** - Claude 分析代码、做更改、运行测试、检查工作
5. **Completion** - 完成后通知，可创建 PR
6. **Results** - 更改推送到分支，准备创建 PR

---

## 🔍 Review Changes with Diff View

**Diff View** 让你在创建 PR 前直接在 app 中查看更改：

**功能**：
- 📊 **Diff stats indicator** - 显示添加和删除行数（如 `+12 -1`）
- 📂 **File list** - 左侧文件列表
- 📝 **Changes view** - 右侧显示每个文件的更改

**操作**：
- 逐文件审查更改
- 对特定更改评论请求修改
- 基于 feedback 继续迭代

**优势**：无需创建 draft PR 或切换到 GitHub 即可多轮优化。

---

## 🔄 Moving Tasks Between Web and Terminal

### From Terminal to Web

**启动 Web 会话**：
```bash
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

**特点**：
- 在 claude.ai 创建新 Web 会话
- 任务在云端运行，本地继续工作
- 用 `/tasks` 检查进度
- 在 claude.ai 或 Claude mobile app 交互

### Tips for Remote Tasks

**Plan locally, execute remotely**：
```bash
# 本地计划
claude --permission-mode plan

# 远程执行
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

**Run tasks in parallel**：
```bash
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

用 `/tasks` 监控所有会话。

### From Web to Terminal

**Teleport** - 将 Web 会话拉到终端：

**方式**：
1. **`/teleport` 或 `/tp`** - 交互式选择器
2. **`claude --teleport`** - 命令行选择器
3. **`claude --teleport <session-id>`** - 直接恢复特定会话
4. **从 `/tasks`** - 按 `t` teleport
5. **从 Web 界面** - 点击 "Open in CLI"

**Teleport 做什么**：
- 验证在正确仓库
- 从远程会话 fetch 和 checkout 分支
- 加载完整对话历史到终端

**Requirements for Teleporting**：

| Requirement | Details |
|-------------|---------|
| **Clean git state** | 工作目录必须无未提交更改（会提示 stash） |
| **Correct repository** | 必须在相同仓库的 checkout（不是 fork） |
| **Branch available** | Web 会话分支必须已推送到远程 |
| **Same account** | 必须认证到 Web 会话使用的相同 Claude.ai 账户 |

---

## 🌐 Cloud Environment

### Default Image

**Universal Image** 包含：
- 流行编程语言和运行时
- 常见构建工具和包管理器
- 测试框架和 linters

**Check available tools**：
```bash
check-tools
```

**Language-specific setups**：
- Python 3.x with pip, poetry, scientific libraries
- Node.js LTS with npm, yarn, pnpm, bun
- Ruby 3.1.6, 3.2.6, 3.3.6
- PHP 8.4.14
- Java OpenJDK with Maven/Gradle
- Go latest stable
- Rust toolchain with cargo
- C++ GCC and Clang

**Databases**：
- PostgreSQL 16
- Redis 7.0

### Environment Configuration

**When session starts**：
1. **Environment preparation** - 克隆 repo，运行 setup script
2. **Network configuration** - 配置网络访问
3. **Claude Code execution** - Claude 运行完成任务
4. **Outcome** - 推送分支，可创建 PR

**Add/Update environments**：
- Add: Select current environment → "Add environment"
- Update: Select current environment → settings button
- Default from terminal: `/remote-env`

### Setup Scripts

**Setup script** - Bash 脚本在新云会话启动时运行（Claude Code 启动前）。

**用途**：
- 安装依赖
- 配置工具
- 准备云环境需要的任何东西

**Example**：
```bash
#!/bin/bash
apt update && apt install -y gh
```

**vs SessionStart hooks**：

| Setup Scripts | SessionStart Hooks |
|---------------|-------------------|
| Attached to cloud environment | Attached to repository |
| Configured in Cloud UI | Configured in `.claude/settings.json` |
| Before Claude Code launches | After Claude Code launches |
| New sessions only | Every session (including resumed) |
| Cloud only | Both local and cloud |

---

## 🔒 Network Access and Security

### GitHub Proxy

**All GitHub operations** 通过专用代理服务：
- 安全管理 GitHub 认证
- 限制 git push 到当前工作分支
- 在保持安全边界的同时启用无缝克隆、fetch、PR 操作

### Security Proxy

**Environments run behind** HTTP/HTTPS network proxy：
- 保护免受恶意请求
- 速率限制和滥用预防
- 内容过滤增强安全

### Access Levels

**Default**: Limited to allowlisted domains.

**Configurable**: Custom network access, including disabling.

### Default Allowed Domains

**Anthropic Services**:
- api.anthropic.com
- statsig.anthropic.com
- platform.claude.com
- code.claude.com
- claude.ai

**Version Control**:
- github.com, api.github.com, etc.
- gitlab.com, registry.gitlab.com
- bitbucket.org, api.bitbucket.org

**Container Registries**:
- registry-1.docker.io, hub.docker.com
- gcr.io, ghcr.io, mcr.microsoft.com

**Package Managers**:
- **JavaScript/Node**: registry.npmjs.org, yarnpkg.com
- **Python**: pypi.org, files.pythonhosted.org
- **Ruby**: rubygems.org
- **Rust**: crates.io, static.rust-lang.org
- **Go**: proxy.golang.org
- **JVM**: repo.maven.org, gradle.org
- **Other**: packagist.org (PHP), nuget.org (.NET), etc.

**Cloud Platforms**:
- Google Cloud, Azure, AWS, Oracle

---

## 💡 学习感悟

### 1. **云端 vs 本地的选择**

Claude Code on the Web vs Remote Control：

| Web | Remote Control |
|-----|----------------|
| 云端执行 | 本地执行，远程界面 |
| 无本地设置 | 需要本地环境 |
| Anthropic 管理 VM | 使用你的文件系统 |
| 适合无本地克隆 | 需要本地克隆 |
| 并行多任务 | 继续本地工作 |

**选择标准**：任务性质决定使用哪个。

### 2. **Teleport 的价值**

Teleport 解决了 **"云开始，本地继续"** 的问题：
- 在 Web 上开始（无需本地设置）
- 迭代和验证
- Teleport 到本地继续深度工作
- 无缝切换

### 3. **Setup Scripts 的分层设计**

Setup Scripts + SessionStart Hooks 的组合：
- **Setup Scripts** - 云端特定（安装云需要但本地有的）
- **SessionStart Hooks** - 通用（云端和本地都运行）

这种分层避免了重复配置。

### 4. **安全性的多层设计**

安全架构的多层：
- **GitHub Proxy** - 限制 push 到当前分支
- **Security Proxy** - 恶意请求保护、速率限制
- **Network Allowlist** - 限制网络访问
- **Scoped Credentials** - 单一目的的短期凭证

这种**Defense in Depth** 策略。

### 5. **Diff View 的交互式审查**

Diff View 的价值：
- 在创建 PR 前审查
- 多轮迭代
- 无需切换工具
- 减少噪音（避免 draft PR）

这符合 **"Review early, review often"** 原则。

### 6. **默认镜像的完整性**

Universal Image 包含：
- 主流语言和运行时
- 数据库（PostgreSQL, Redis）
- 包管理器
- 构建工具

这减少了 **Setup Script** 的需求，提高启动速度。

---

## 🎯 实践建议

### 1. **快速 Bug 修复用 Web**

```bash
# 无需本地克隆
claude --remote "Fix the authentication bug in src/auth/login.ts"

# 在手机上监控
# Claude mobile app

# 完成后创建 PR
```

### 2. **复杂任务先 Plan 后 Execute**

```bash
# 本地计划
claude --permission-mode plan

# 理解代码库，创建计划
# Ctrl+G 编辑计划

# 满意后远程执行
claude --remote "Execute the migration plan"
```

### 3. **并行处理多个任务**

```bash
# 启动多个并行任务
claude --remote "Fix test auth.spec.ts"
claude --remote "Update API docs"
claude --remote "Refactor logger"

# 用 /tasks 监控
/tasks
```

### 4. **Teleport 回本地继续**

```bash
# Web 上开始，迭代
# 需要深度工作时
claude --teleport

# 或会话中
/teleport

# 继续本地工作
```

### 5. **配置环境**

**Setup Script**（云特定）：
```bash
#!/bin/bash
# Install cloud-only tools
apt update && apt install -y gh
```

**SessionStart Hook**（通用）：
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "npm install"
          }
        ]
      }
    ]
  }
}
```

### 6. **审查 Diff View**

- 打开 claude.ai/code
- 点击 diff stats indicator（`+12 -1`）
- 逐文件审查
- 评论请求修改
- 迭代直到满意
- 创建 PR

---

## 📚 与 OpenClaw 的对比

### 相似之处

1. **云端执行** - 都可以在云端运行
2. **远程访问** - 都支持远程访问能力

### 差异之处

1. **Web 界面** - Claude Code 有专门的 Web 界面，OpenClaw 依赖第三方平台
2. **Teleport** - Claude Code 有 teleport 功能，OpenClaw 没有
3. **环境管理** - Claude Code 有完整的环境配置系统，OpenClaw 更依赖本地
4. **Diff View** - Claude Code 有内置 diff view，OpenClaw 需要外部工具

### 可以借鉴

1. **Teleport** - Web 会话拉回本地继续
2. **Diff View** - 内置代码审查界面
3. **Environment Profiles** - 环境配置系统
4. **Setup Scripts** - 云环境初始化脚本

---

## 🏷️ 标签
`#web` `#cloud` `#teleport` `#diff-view` `#setup-scripts` `#environment` `#security`
