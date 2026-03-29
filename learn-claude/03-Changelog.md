# 03 - Claude Code Changelog 学习笔记

**学习时间**：2026-03-14 12:20  
**页面地址**：https://code.claude.com/docs/en/changelog

---

## 📖 原文要点

Changelog 记录了从 **0.2.125**（早期版本）到 **2.1.76**（最新版本）的所有更新。这里重点关注**最新 5 个版本**的关键更新。

### 🆕 最新版本：2.1.76（2026-03-14）

#### 新增功能
1. **MCP Elicitation Support**
   - MCP 服务器可以在任务中通过交互对话框请求结构化输入
   - 新增 Elicitation 和 ElicitationResult hooks

2. **Session Name Display**
   - 新增 `-n / --name <name>` CLI 标志，启动时设置会话显示名称
   - `/rename` 命令设置的名称会显示在提示栏

3. **Worktree Sparse Paths**
   - 新增 `worktree.sparsePaths` 设置
   - 在大型 monorepo 中，只检出需要的目录（git sparse-checkout）

4. **PostCompact Hook**
   - 在压缩完成后触发

5. **Session Quality Survey**
   - 企业管理员可通过 `feedbackSurveyRate` 配置采样率

6. **Effort Slash Command**
   - `/effort` 命令设置模型努力级别

#### 重要修复
- 修复延迟工具（通过 ToolSearch 加载）在对话压缩后丢失输入 schema
- 修复 slash 命令显示 "Unknown skill"
- 修复 plan mode 在计划已接受后再次请求批准
- 修复 voice mode 在权限对话框打开时吞掉按键
- 修复自动压缩在连续失败后无限重试（现在断路器在 3 次后停止）
- 改进 --worktree 启动性能
- 改进后台 agent 行为（杀死后台 agent 现在会保留部分结果）

---

### 🔥 2.1.75（2026-03-13）

#### 重大更新
1. **1M Context Window for Opus 4.6**
   - Max、Team 和 Enterprise 计划默认提供 1M 上下文窗口
   - 之前需要额外使用

2. **Color Command**
   - `/color` 命令为所有用户设置提示栏颜色

3. **Memory Timestamps**
   - 记忆文件添加最后修改时间戳
   - 帮助 Claude 推理哪些记忆是新鲜 vs 陈旧

#### 重要修复
- 修复 voice mode 在全新安装时无法正确激活
- 修复 Bash tool 在管道命令中破坏 `!`（如 `jq 'select(.x != .y)'`）
- 修复 token 估算过度计算 thinking 和 tool_use blocks，导致过早上下文压缩
- 改进 macOS 非 MDM 机器的启动性能

---

### ⚡ 2.1.74（2026-03-12）

#### 新增功能
1. **Actionable /context Suggestions**
   - `/context` 命令识别上下文重的工具、内存膨胀、容量警告
   - 提供具体优化建议

2. **Custom Auto-Memory Directory**
   - `autoMemoryDirectory` 设置配置自定义自动记忆存储目录

3. **Model Overrides**
   - `modelOverrides` 设置映射模型选择器条目到自定义提供商模型 ID
   - 例如 Bedrock 推理配置文件 ARN

#### 重要修复
- 修复内存泄漏：流式 API 响应缓冲区在生成器提前终止时未释放
- 修复托管策略 ask 规则被用户 allow 规则或 skill allowed-tools 绕过
- 修复完整模型 ID（如 `claude-opus-4-5`）在 agent frontmatter 中被忽略
- 修复 MCP OAuth 认证在回调端口已被使用时挂起

---

### 🛠️ 2.1.73（2026-03-11）

#### 新增功能
1. **Model Overrides Setting**
   - 映射模型选择器条目到自定义提供商模型 ID

2. **Improved Error Guidance**
   - OAuth 登录或连接检查因 SSL 证书错误失败时提供可操作指导

#### 重要修复
- 修复复杂 bash 命令的权限提示导致的冻结和 100% CPU 循环
- 修复许多 skill 文件同时更改时的死锁（如 git pull）
- 修复 Bash tool 输出在多个会话中丢失
- 修复子 agent 在 Bedrock/Vertex/Foundry 上被降级到旧模型版本
- 改进上箭头在中断 Claude 后的行为（恢复被中断的提示并倒回对话）

---

### 🎯 2.1.72（2026-03-10）

#### 新增功能
1. **/copy Write to File**
   - `/copy` 中 `w` 键将选中内容直接写入文件，绕过剪贴板
   - 适用于 SSH 场景

2. **/plan Description Argument**
   - `/plan fix the auth bug` 直接进入 plan mode 并开始

3. **ExitWorktree Tool**
   - 离开 EnterWorktree 会话

4. **Simplified Effort Levels**
   - 简化为 low/medium/high（移除 max）
   - 新符号：○ ◐ ●
   - `/effort auto` 重置为默认

#### 重要修复
- 修复退出时后台任务或 hooks 响应慢
- 修复 agent 任务进度卡在 "Initializing…"
- 修复 voice mode 问题：输入延迟、错误 "No speech detected"、陈旧转录
- 修复 --continue 在 --compact 后不从最近点恢复
- 修复 bash 安全解析边缘情况
- 改进长会话中的 CPU 利用率
- 修复 SDK query() 调用中的提示缓存失效（减少输入 token 成本最多 12x）

---

## 💡 关键功能演进分析

### 1. **上下文管理能力增强**

#### 1M Context Window（2.1.75）
- Opus 4.6 默认提供 1M 上下文
- 适用于 Max/Team/Enterprise

#### Sparse Worktree（2.1.76）
- 大型 monorepo 只检出需要的目录
- 减少启动时间和磁盘使用

#### Context Suggestions（2.1.74）
- `/context` 提供可操作优化建议
- 识别上下文重的工具和内存膨胀

**启示**：Claude Code 正在解决**上下文管理**这一 AI Agent 的核心挑战。

---

### 2. **记忆系统改进**

#### Memory Timestamps（2.1.75）
- 记忆文件添加最后修改时间
- 帮助 Claude 推理记忆新鲜度

#### Custom Auto-Memory Directory（2.1.74）
- 可配置自定义存储位置

**启示**：记忆系统从"静态存储"进化为"时间感知"系统。

---

### 3. **MCP 生态扩展**

#### MCP Elicitation（2.1.76）
- MCP 服务器可以在任务中请求输入
- 更强大的交互能力

#### OAuth Improvements（2.1.74）
- 修复 OAuth 认证挂起
- 改进 token 刷新

**启示**：MCP 作为开放标准，正在快速演进。

---

### 4. **性能优化**

#### Startup Performance（2.1.75）
- macOS 非 MDM 机器跳过不必要的子进程
- 改进启动速度

#### CPU Utilization（2.1.72）
- 改进长会话中的 CPU 利用率

#### Prompt Cache（2.1.72）
- 修复 SDK query() 中的缓存失效
- 减少输入 token 成本最多 12x

**启示**：性能优化是持续迭代的重要方向。

---

### 5. **Voice Mode 改进**

#### Multiple Fixes（2.1.72-2.1.76）
- 修复全新安装时的激活问题
- 修复权限对话框打开时吞掉按键
- 修复输入延迟和错误检测
- 修复 Windows 原生二进制的音频模块加载

**启示**：Voice mode 是一个复杂功能，需要大量边缘情况修复。

---

### 6. **Agent 协作能力**

#### Background Agent Behavior（2.1.76）
- 杀死后台 agent 现在保留部分结果
- 避免工作丢失

#### Agent Team Fixes（2.1.72）
- 修复 team agents 继承 leader 的模型
- 修复 agent 任务进度卡住

**启示**：Agent 协作系统正在变得更健壮。

---

## 🎯 版本演进趋势

### 从 Changelog 看到的趋势

1. **更智能的上下文管理**
   - 1M 上下文
   - Sparse checkout
   - 上下文优化建议

2. **更强大的记忆系统**
   - 时间戳感知
   - 自定义存储

3. **更开放的生态**
   - MCP 持续增强
   - OAuth 改进

4. **更稳定的性能**
   - 启动优化
   - CPU 优化
   - 缓存优化

5. **更好的用户体验**
   - Voice mode 修复
   - 权限改进
   - 错误提示优化

---

## 💡 学习感悟

### 1. **快速迭代的力量**
从 0.2.125 到 2.1.76，版本号跨越巨大，说明：
- **快速迭代**：几乎每天都有更新
- **持续改进**：大量 bug fixes 和性能优化
- **用户反馈驱动**：许多修复来自用户报告

### 2. **边缘情况的重要性**
Changelog 中大量修复都是**边缘情况**：
- SSH 连接慢时的行为
- 非标准模型字符串
- Windows 特定问题
- 长会话中的内存泄漏

**启示**：AI Agent 系统的复杂性在于**边缘情况**，需要大量测试和用户反馈。

### 3. **性能优化的持续性**
几乎每个版本都有性能优化：
- 启动时间
- CPU 利用率
- 内存泄漏
- Token 成本

**启示**：性能优化是一个**永无止境**的过程。

### 4. **MCP 作为战略重点**
MCP 相关更新频繁：
- 新功能（Elicitation）
- 修复（OAuth）
- 改进（连接恢复）

**启示**：Anthropic 将 MCP 视为**生态系统战略**的核心。

### 5. **Voice Mode 的复杂性**
Voice mode 有最多的修复：
- 不同平台的音频问题
- 权限问题
- 输入延迟
- 错误检测

**启示**：**跨平台音频**是最复杂的功能之一，需要大量工程投入。

---

## 🎯 实践建议

### 1. **保持更新**
Native Install 会自动更新，确保：
```bash
# 检查版本
claude --version

# 如果是 Homebrew/WinGet，定期更新
brew upgrade claude-code
winget upgrade Anthropic.ClaudeCode
```

### 2. **关注新功能**
定期查看 Changelog，重点关注：
- 新 slash 命令
- 性能优化
- 重要 bug fixes

### 3. **报告问题**
如果遇到问题，检查 Changelog：
- 可能已在最新版本修复
- 可以通过 GitHub Issues 报告

### 4. **利用新功能**
例如 2.1.76 的 sparse worktree：
```bash
# 大型 monorepo
claude --worktree --sparsePaths src/,tests/
```

### 5. **理解限制**
某些功能有平台限制：
- Voice mode 在某些平台不稳定
- 1M 上下文需要特定订阅

---

## 📚 与 OpenClaw 的对比

### 相似之处
1. **快速迭代** - 都在持续更新
2. **用户反馈驱动** - 根据用户报告修复问题
3. **性能优化** - 持续改进性能

### 差异之处
1. **更新频率** - Claude Code 几乎每天更新，OpenClaw 相对稳定
2. **版本号** - Claude Code 已经 2.1.x，OpenClaw 还在早期版本
3. **成熟度** - Claude Code 更成熟，边缘情况处理更好

### 可以借鉴
1. **Changelog 透明度** - 详细记录每个版本变化
2. **快速修复** - 用户报告的问题快速修复
3. **性能监控** - 持续关注性能指标

---

## 🏷️ 标签
`#changelog` `#version-history` `#performance` `#mcp` `#voice-mode` `#context-management`
