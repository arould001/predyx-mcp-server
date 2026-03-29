# Cursor 企业级高效使用完整指南（官方文档 + 案例分析）

<!-- compounded: 2026-03-15 -->

> **分析时间**: 2026-03-07
> **数据来源**: 
> - Cursor 中文官方文档（完整版）
> - 企业客户案例（Stripe, PlanetScale, Cursor 内部等）
> - 官网 Product/Enterprise/Pricing 页面

---

## 📋 目录

1. [核心功能全景](#核心功能全景)
2. [企业级特性详解](#企业级特性详解)
3. [官方文档核心章节](#官方文档核心章节)
4. [客户案例研究](#客户案例研究)
5. [企业级最佳实践](#企业级最佳实践)
6. [组织级推广策略](#组织级推广策略)
7. [技术实施指南](#技术实施指南)
8. [定价与 ROI 分析](#定价与-roi-分析)
9. [风险与注意事项](#风险与注意事项)
10. [实施路线图](#实施路线图)

---

## 核心功能全景

### 1. Agents - 自主编码能力

**核心能力**：
- **自主工作**: 在后台运行，开发者专注于决策
- **多模型支持**: OpenAI, Anthropic, Gemini, xAI, Cursor 自研
- **Cloud Agents**: 云端运行，支持 Web 和移动端
- **Codebase Understanding**: 深度理解代码库，语义搜索

**工作模式**：
```
Plan Mode    → 复杂任务先提问、建计划、再执行
Design Mode  → 可视化编辑页面元素
Debug Mode   → 插入代码，使用执行数据定位问题
Build Mode   → 自主构建功能
```

**能力范围**：
- Terminal: 运行 shell 命令（sandboxed）
- Git & Checkpoints: 版本控制，随时回滚
- @-mentions: 指向相关文件和上下文
- Image uploads: 上传参考图片

**支持模型**（2026-03-07 最新）：
| 模型 | 默认上下文 | 最大上下文 | 能力 |
|------|----------|----------|------|
| Claude 4.6 Opus | 200k | 1M | Agent, Thinking, Image |
| Claude 4.6 Sonnet | 200k | 1M | Agent, Thinking, Image |
| Cursor Composer 1.5 | 200k | - | Agent, Thinking, Image |
| Gemini 3 Flash | 200k | 1M | Agent, Thinking, Image |
| Gemini 3.1 Pro | 200k | 1M | Agent, Thinking, Image |
| GPT-5.3 Codex | 272k | - | Agent, Thinking, Image |
| GPT-5.4 | 272k | 1M | Agent, Thinking, Image |
| Grok Code | 256k | - | Agent, Thinking |

---

### 2. Rules（规则）- 系统级指令

**四种规则类型**：

#### 项目规则（.cursor/rules）
- 存储在 `.cursor/rules` 目录，受版本控制
- 仅作用于当前代码库
- 支持 `.md` 和 `.mdc` 扩展名
- 使用 frontmatter 控制应用方式

#### 用户规则（全局）
- 在 Cursor Settings 中定义
- 适用于所有项目
- 供 Agent (Chat) 使用
- 适合设定沟通风格或编码规范

#### 团队规则（Team/Enterprise）
- 通过 Cursor Dashboard 集中管理
- 适用于所有团队成员
- 可强制执行（用户无法关闭）
- 优先级：**Team Rules → Project Rules → User Rules**

#### AGENTS.md（简化版）
- 项目根目录或子目录
- 纯 Markdown 格式，无复杂配置
- 适合简单直接的用例

**规则类型（应用方式）**：
```yaml
Always Apply           # 每个会话都应用
Apply Intelligently    # Agent 根据描述判断相关性
Apply to Specific Files # 文件匹配时应用（使用 glob 模式）
Apply Manually         # @ 提及时应用（例如 @my-rule）
```

**规则文件格式**：
```markdown
---
description: "This rule provides standards for frontend components"
globs: 
alwaysApply: false
---

# 规则内容
- Use our internal RPC pattern when defining services
- Always use snake_case for service names

@service-template.ts
```

**创建规则的方式**：
1. **/create-rule**: 在对话中使用，Agent 自动生成
2. **Settings**: Cursor Settings > Rules, Commands > + Add Rule
3. **GitHub 导入**: 从远程仓库导入规则

**最佳实践**：
- ✅ 控制在 500 行以内
- ✅ 拆分为多个可组合的规则
- ✅ 引用文件而不是复制内容
- ✅ 提交到 Git，团队共享
- ✅ 在聊天中重复提示时复用规则

**应避免**：
- ❌ 整份照搬风格指南（改用 linter）
- ❌ 把每一个可能的命令都写进文档
- ❌ 为极少出现的边缘情况添加说明
- ❌ 重复你代码库中已有的内容

---

### 3. Skills（技能）- 领域知识包

**什么是 Skill**：
- 可移植、受版本控制的包
- 教会 Agent 执行特定领域任务
- 可以包含脚本、模板和参考信息

**核心特性**：
```
可移植     → 可用于任何支持 Agent Skills 标准的 Agent
受版本控制 → 以文件形式存储，可通过 Git 追踪
可操作     → 包含脚本、模板，Agent 会通过工具操作
渐进式     → 按需加载资源，上下文使用更高效
```

**技能目录**：
```
.agents/skills/       # 项目级
.cursor/skills/       # 项目级
~/.cursor/skills/     # 用户级（全局）

# 兼容性目录
.claude/skills/
.codex/skills/
~/.claude/skills/
~/.codex/skills/
```

**文件结构**：
```
.agents/
└── skills/
    └── deploy-app/
        ├── SKILL.md          # 必需
        ├── scripts/          # 可选：可执行代码
        │   ├── deploy.sh
        │   └── validate.py
        ├── references/       # 可选：补充文档
        │   └── REFERENCE.md
        └── assets/           # 可选：模板、图片等
            └── config-template.json
```

**SKILL.md 格式**：
```markdown
---
name: my-skill
description: Short description of what this skill does
license: MIT
compatibility: Requires Python 3.9+
metadata:
  author: team-name
disable-model-invocation: false
---

# My Skill

## When to Use
- Use this skill when...
- This skill is helpful for...

## Instructions
- Step-by-step guidance
- Domain-specific conventions
```

**Frontmatter 字段**：
| 字段 | 必填 | 说明 |
|------|------|------|
| name | Yes | 技能标识符（小写字母、数字、连字符） |
| description | Yes | 功能和使用场景（Agent 判断相关性用） |
| license | No | 许可证名称 |
| compatibility | No | 环境要求（系统软件包、网络访问等） |
| metadata | No | 任意元数据键值对 |
| disable-model-invocation | No | true 时仅通过 /skill-name 显式调用 |

**禁用自动调用**：
```yaml
---
disable-model-invocation: true
---
```
- 设置为 `true` 后，技能表现像传统斜杠命令
- 只有显式输入 `/skill-name` 时才加入上下文

**从 GitHub 安装**：
1. 打开 Cursor Settings → Rules
2. 在 Project Rules 部分，点击 Add Rule
3. 选择 Remote Rule (Github)
4. 输入 GitHub 仓库地址

**迁移工具**：
```
/migrate-to-skills
```
- 转换动态规则（Apply Intelligently）为标准技能
- 转换斜杠命令为技能（设置 disable-model-invocation: true）

---

### 4. Subagents（子代理）- 并行自动化

**什么是子代理**：
- 专门化的 AI 助手
- 在自己的上下文窗口中运行
- 处理特定类型工作
- 将结果返回给父代理

**核心优势**：
```
上下文隔离   → 长时间任务不占用主对话空间
并行执行     → 同时启动多个子代理
专业化能力   → 自定义提示词、工具、模型
可复用性     → 在多个项目之间复用
```

**前台 vs 后台模式**：
| 模式 | 行为 | 适用场景 |
|------|------|---------|
| **Foreground** | 阻塞直到完成，立即返回结果 | 串行任务，需要立即输出 |
| **Background** | 立即返回，后台独立运行 | 长时间任务、并行工作流 |

**内置子代理**：
| 子代理 | 作用 | 为什么是子代理 |
|--------|------|--------------|
| **Explore** | 搜索并分析代码库 | 产生大量中间输出，使用更快模型并行搜索 |
| **Bash** | 运行一系列 shell 命令 | 命令输出冗长，隔离让父代理专注决策 |
| **Browser** | 通过 MCP 工具控制浏览器 | DOM 快照和截图噪声大，过滤为相关结果 |

**为什么需要这些子代理**：
- **上下文隔离**：中间结果保留在子代理，父代理只接收摘要
- **模型灵活性**：Explore 默认使用更快模型，一次主代理搜索时间内并行运行 10 次搜索
- **专用配置**：针对特定任务优化的提示词和工具访问权限
- **成本效率**：更快模型成本更低，隔离高 token 开销工作

**何时使用子代理 vs Skill**：
| 使用子代理 | 使用 Skill |
|-----------|-----------|
| 需要上下文隔离 | 任务是单一用途的 |
| 需要并行运行多个工作流 | 想要快速、可重复的操作 |
| 任务在多个步骤中需要专业知识 | 任务可以一次性完成 |
| 希望对工作结果进行独立验收/校验 | 不需要单独的上下文窗口 |

**文件位置**：
| 类型 | 位置 | 适用范围 |
|------|------|---------|
| 项目子代理 | `.cursor/agents/` | 仅限当前项目 |
| 兼容性 | `.claude/agents/`, `.codex/agents/` | 仅限当前项目 |
| 用户子代理 | `~/.cursor/agents/` | 当前用户的所有项目 |
| 兼容性 | `~/.claude/agents/`, `~/.codex/agents/` | 当前用户的所有项目 |

**文件格式**：
```markdown
---
name: security-auditor
description: Security specialist. Use when implementing auth, payments.
model: inherit
readonly: false
background: false
---

You are a security expert auditing code for vulnerabilities.

When invoked:
1. Identify security-sensitive code paths
2. Check for common vulnerabilities
3. Verify secrets are not hardcoded
4. Review input validation and sanitization

Report findings by severity:
- Critical (must fix before deploy)
- High (fix soon)
- Medium (address when possible)
```

**配置字段**：
| 字段 | 必填 | 描述 |
|------|------|------|
| name | 否 | 唯一标识符（默认为文件名） |
| description | 否 | 何时使用（Agent 根据此决定是否委派） |
| model | 否 | fast、inherit 或特定模型 ID（默认 inherit） |
| readonly | 否 | true 时以受限写入权限运行 |
| background | 否 | true 时在后台运行 |

**使用方式**：
```bash
# 自动委派（Agent 根据描述决定）
> Review the payment module for security issues

# 显式调用
> /security-auditor review the payment module

# 自然语言调用
> Use the security-auditor subagent to review the payment module

# 并行执行
> Review the API changes and update the documentation in parallel

# 恢复子代理（保留上下文）
> Resume agent abc123 and analyze the remaining test failures
```

**常见模式**：

1. **验证代理（Verifier）**：
```markdown
---
name: verifier
description: Validates completed work. Use after tasks are marked done.
model: fast
---

You are a skeptical validator. Your job is to verify that work claimed as complete actually works.

When invoked:
1. Identify what was claimed to be completed
2. Check that the implementation exists and is functional
3. Run relevant tests or verification steps
4. Look for edge cases that may have been missed

Be thorough and skeptical. Report:
- What was verified and passed
- What was claimed but incomplete or broken
- Specific issues that need to be addressed

Do not accept claims at face value. Test everything.
```

**适用场景**：
- 在将工单标记为完成之前验证功能是否端到端正常工作
- 发现只做了部分实现的功能
- 确保测试真正通过（而不仅仅是存在测试文件）

2. **Orchestrator 模式**：
```
Planner      → 分析需求并制定技术方案
Implementer  → 根据方案实现功能
Verifier     → 确认实现满足需求
```
每次交接都包含结构化输出，下一个 Agent 拥有清晰的上下文。

**最佳实践**：
- ✅ 编写专注的子代理（每个只负责一件事）
- ✅ 投入精力写好描述（决定 Agent 何时委派）
- ✅ 保持提示简洁（具体、直接）
- ✅ 将子代理纳入版本控制（`.cursor/agents/` 提交到代码仓库）
- ✅ 从 Agent 生成的代理开始（先让 Agent 起草，再自定义）
- ✅ 从 2-3 个聚焦明确的子代理开始

**需要避免**：
- ❌ 描述含糊（"Use for general tasks" 不传达任何信号）
- ❌ 提示词过长（2,000 字不会让子代理更智能，只会更慢）
- ❌ 重复 slash command（单一用途任务改用斜杠命令）
- ❌ 创建几十个通用型子代理

**性能与成本**：
| 优点 | 代价 |
|------|------|
| 上下文隔离 | 启动开销（每个子代理独立收集上下文） |
| 并行执行 | 更高 Token 消耗（多个上下文同时运行） |
| 专注特定任务 | 延迟（简单任务可能比主代理更慢） |

**Token 和成本注意事项**：
- 子代理独立消耗 Token（5 个子代理 ≈ 单个 Agent 的 5 倍 Token）
- 评估额外开销（快速、简单任务用主代理更快）
- 子代理优势在上下文隔离，不是速度

---

### 5. Bugbot - 自动代码审查

**工作原理**：
- 分析 PR diff，留下带说明和修复建议的评论
- 每次更新时自动运行，或手动触发
- 读取 GitHub PR 评论（顶层和内联）避免重复建议
- 提供 "在 Cursor 中修复" 和 "在 Web 中修复" 链接

**设置步骤**（GitHub.com）：
1. 前往 cursor.com/dashboard
2. 打开 Integrations 选项卡
3. 点击 `Connect GitHub`（或 `Manage Connections`）
4. 按照 GitHub 安装流程操作
5. 返回仪表盘，在指定仓库中启用 Bugbot

**配置**：

**项目规则**（`.cursor/BUGBOT.md`）：
```
project/
├── .cursor/
│   └── BUGBOT.md        # 始终包含（项目级规则）
├── backend/
│   └── .cursor/
│       └── BUGBOT.md    # 审查后端文件时包含
├── api/
│   └── .cursor/
│       └── BUGBOT.md    # 审查 API 文件时包含
└── frontend/
    └── .cursor/
        └── BUGBOT.md    # 审查前端文件时包含
```

**团队规则**：
- 在 Bugbot 仪表盘创建
- 适用于团队内所有代码仓库
- 应用顺序：**团队规则 → 项目 BUGBOT.md（包括嵌套文件）→ 用户规则**

**规则示例**：
1. **安全**：标记任何使用 `eval()` 或 `exec()` 的代码
2. **开源许可证**：阻止引入不允许的许可证
3. **语言规范**：标记 React `componentWillMount` 的使用
4. **规范**：要求后端改动必须附带测试
5. **风格**：不允许 TODO 注释

**自动修复（Autofix）**：
- Bugbot 在 PR 审查中发现 bug 时，自动启动 Cloud Agent 修复
- 将修复推送到现有分支或新分支
- 在原始 PR 下发布评论说明修复结果

**使用条件**：
- 启用按用量计费
- 启用存储（且不处于 Legacy Privacy Mode）

**计费**：
- 使用 Cloud Agent 点数
- 按套餐费率计费

**管理配置 API**：

**身份验证**：
```bash
Authorization: Bearer $API_KEY
```
- 创建 API 密钥：Cursor 仪表盘 → Settings → Advanced → New Admin API Key
- 限制：每个团队每分钟最多 60 次请求

**启用/禁用仓库**：
```bash
curl -X POST https://api.cursor.com/bugbot/repo/update \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "repoUrl": "https://github.com/your-org/your-repo",
    "enabled": true
  }'
```

**管理用户访问权限**：
```bash
# 授予访问权限
curl -X POST https://api.cursor.com/bugbot/user/update \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username": "employee-github-name", "allow": true}'

# 撤销访问权限
curl -X POST https://api.cursor.com/bugbot/user/update \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username": "employee-github-name", "allow": false}'
```

**价格**：
| 方案 | 价格 | 说明 |
|------|------|------|
| **免费版** | $0 | Teams 和个人计划：每位用户每月有限次数免费 PR 评审 |
| **专业版** | $40/用户/月 | 不限次数评审（受标准防滥用规则限制） |
| **Teams** | $40/用户/月 | 不限次数评审 + 团队规则 |

**故障排查**：
```bash
# 启用详细模式
cursor review verbose=true
bugbot run verbose=true
```
- 获取详细日志和请求 ID
- 检查权限（Bugbot 具有仓库访问权限）
- 验证安装（GitHub 应用已安装并启用）

---

## 企业级特性详解

### 1. 安全与合规

**安全资源**：
- **Trust Center**: https://trust.cursor.com/
- **Security page**: https://cursor.com/security
- **Privacy Overview**: https://cursor.com/privacy-overview
- **Data Processing Agreement**: https://cursor.com/terms/dpa

**认证与合规**：
- SOC2 Type II 认证
- GDPR 合规
- CCPA 合规
- AES-256 加密（静态）
- TLS 1.2+ 加密（传输）
- 年度渗透测试

**隐私模式（Privacy Mode）**：
- 与 AI 提供商实现零数据留存
- Teams：全组织强制启用
- Enterprise：全组织强制启用

**Agent 沙箱模式**：
- Teams：✓ 支持
- Enterprise：✓ 全组织强制启用

**代码仓库阻止列表**：
- Enterprise：✓ 支持
- 阻止特定代码库访问

---

### 2. 身份与访问控制

**SSO 和 SAML**：
- Teams：✓ 支持
- Enterprise：✓ 支持
- 单点登录简化身份验证

**SCIM**：
- Teams：× 不支持
- Enterprise：✓ 支持
- 自动化用户账号开通与回收

**MDM 策略**：
- 在用户设备上强制限定允许的团队 ID 和扩展程序
- 适用于企业部署

**用户访问控制**（仅 Enterprise）：
| 能力 | 说明 |
|------|------|
| Cursor CLI | 限制可通过命令行界面访问 Agents 的用户 |
| Cloud Agents | 限制可创建 Cloud Agents 的用户 |
| Analytics | 分析仪表盘仅限管理员访问 |
| BYOK | 不允许用户使用自己的 API 密钥 |

---

### 3. 管理功能

**Dashboard**：
- 团队管理、设置与监控
- 所有方案支持

**Admin API**：
- 通过编程方式访问管理功能
- 所有方案支持

**Analytics**：
| 方案 | 功能 |
|------|------|
| Teams | 分析仪表板 |
| Enterprise | 分析仪表板 + AI 代码跟踪 API + 对话洞察 |

**Conversation Insights**（仅 Enterprise）：
- 了解团队在 Cursor 中完成的工作类型

**AI Code Tracking API**（仅 Enterprise）：
- 按提交统计的 AI 使用指标

**Cursor Blame**（仅 Enterprise）：
- 可感知 AI 的 git blame
- 区分 AI 与人工代码归属

**Analytics API**：
- 使用指标与洞察
- 所有方案支持

**Billing Groups**（仅 Enterprise）：
- 跨用户组管理支出
- 用于报表和费用回冲

**Service Accounts**（仅 Enterprise）：
- 用于自动化工作流的非人工账号

---

### 4. 集中式 Agent 控制

**隐私模式**：
| 方案 | 行为 |
|------|------|
| Individual | 用户自行选择 |
| Teams | 全组织强制启用 |
| Enterprise | 全组织强制启用 |

**团队规则**：
- Teams：支持强制和可选
- Enterprise：支持强制和可选

**Hooks（用于日志、审计等）**：
| 方案 | 行为 |
|------|------|
| Individual | ✓ 支持 |
| Teams | 通过 MDM 分发 |
| Enterprise | 通过 MDM 和服务器端分发 |

**代码仓库阻止列表**：
- Enterprise：✓ 支持

**模型访问限制**：
- Enterprise：✓ 支持
- 控制可用的模型

**自动执行、浏览器和网络控制**：
- Enterprise：✓ 支持
- 细粒度控制 Agent 行为

---

### 5. 审计与监控

**审计日志**（仅 Enterprise）：
- 跟踪身份验证、用户管理和管理操作
- SIEM 集成：将审计日志发送到安全工具

---

### 6. 支持与法律条款

| 功能 | 个人版 | 团队版 | 企业版 |
|------|--------|--------|--------|
| 技术支持 | 社区与标准支持 | 社区与标准支持 | **优先支持** |
| 条款 | 在线条款 | MSA 与 DPA | MSA 与 DPA |

---

## 官方文档核心章节

### 1. Agent 章节

**概览**：
- Agent 基础概念
- 工作原理

**规划（Plan Mode）**：
- 复杂任务先规划
- 提问、建计划、再执行

**提示工程**：
- 如何写好提示
- 最佳实践

**调试（Debug Mode）**：
- 插入代码
- 使用执行数据定位问题

**工具**：
- Agent 可用的工具
- Terminal, Git, @-mentions 等

**并行 Agent**：
- 使用 worktrees 并行运行多个 Agent

**安全**：
- Agent 工具执行安全防护
- 沙箱模式
- 责任披露计划

---

### 2. 自定义章节

**插件（Plugins）**：
- Marketplace: 社区构建的插件
- Slack Messaging Kit, Figma Visual Editor, Notion Workspace Integration 等

**规则（Rules）**：
- 见上文 "Rules（规则）- 系统级指令"

**技能（Skills）**：
- 见上文 "Skills（技能）- 领域知识包"

**子代理（Subagents）**：
- 见上文 "Subagents（子代理）- 并行自动化"

**钩子（Hooks）**：
- 自定义安全与合规工作流
- 通过 MDM 和服务器端分发（Enterprise）

**MCP**：
- Model Context Protocol 服务器信任管理
- 集成外部工具和数据源

---

### 3. Cloud Agent 章节

**概览**：
- Cloud Agents 基础概念
- 云端运行，支持 Web 和移动端

**设置**：
- 如何配置 Cloud Agents

**能力**：
- Cloud Agents 可用的能力

**Bugbot**：
- 见上文 "Bugbot - 自动代码审查"

**最佳实践**：
- 如何高效使用 Cloud Agents

**安全与网络**：
- Cloud Agents 安全配置
- 网络设置

**设置**：
- Cloud Agents 设置选项

**API**：
- Cloud Agents API 端点

---

### 4. 集成章节

**Slack**：
- 在 Slack 中使用 Cloud Agents

**Linear**：
- 问题跟踪集成

**GitHub**：
- 仓库集成
- Bugbot 集成

**GitLab**：
- 仓库集成
- Bugbot 集成

**JetBrains**：
- IntelliJ IDEA, PyCharm, WebStorm 等 IDE 集成
- Agent Client Protocol (ACP)

**深度链接**：
- cursor:// 协议
- 直接在 Cursor 中打开特定功能

---

### 5. 命令行界面章节

**概览**：
- CLI 基础概念

**安装**：
- 如何安装 Cursor CLI

**能力**：
- CLI 可用的能力

**Shell 模式**：
- 交互式 Shell 模式

**ACP**：
- Agent Client Protocol

**无头模式 / CI**：
- 在 CI/CD 中使用 Cursor
- 自动化工作流

---

### 6. 团队与企业版章节

**概览**：
- 企业版总体介绍

**身份与访问控制**：
- SSO、SCIM、RBAC 和 MDM 策略

**隐私与数据治理**：
- 数据流向、隐私模式和数据驻留

**网络配置**：
- 代理设置、IP 允许列表和加密

**LLM 安全与管控**：
- Hooks、终端沙箱和 Agent 管控

**模型与集成**：
- 模型管控、MCP，以及第三方集成

**合规与监控**：
- 审计日志和追踪

**部署模式**：
- MDM 管理的编辑器与自托管 CLI 对比

**服务账户**：
- 用于自动化工作流的非人工账号

**计费组**：
- 跨用户组管理支出

**Cursor 变更归属**：
- 可感知 AI 的 git blame

---

## 客户案例研究

### 1. Stripe (3,000+ engineers) - 企业级推广最佳实践

#### 实施策略

**预安装策略**：
```yaml
新员工机器预装:
  - VS Code
  - IntelliJ
  - Cursor
  
培训:
  - Lab 教学如何使用开发环境
  - 新人第一天就能提交 PR
```

**Cursor Rules**：
```yaml
提供上下文:
  - 代码库上下文
  - 编码标准
  
团队自定义:
  - 团队可添加自己的规则
  - 组织层面控制规则的全面性
```

**推广策略**：
```yaml
Influencer system:
  - 识别 power users
  - Lunch-and-learns 分享工作流
  - 展示高级技巧:
    - 并行运行多个 agents
    - 写更好的 prompts
```

#### 代码审查适应

**挑战**: AI 让工程师写更多代码，但不能牺牲质量

**解决方案**：
```yaml
AI 辅助审查:
  - 用 LLMs 帮助审查者更高效工作
  - AI 标记复杂方法或风险文件
  - 引导审查者注意力到最需要的地方

文化培养:
  - 工程师更愿意拒绝不成熟的代码
  - 无论来源（人还是 agent）
```

#### 反直觉发现

**预期**: 初级工程师受益最大（用 AI 补偿经验不足）

**实际**: **资深工程师收益最大**

**原因**：
```yaml
资深工程师优势:
  - 有上下文知识
  - 能清晰表达目标
  - 知道要达成什么
  - 能明确指导 agents

新思考:
  - 新员工可能先学习代码库
  - 再给 Cursor 访问权限
  - 先建立上下文，再使用 AI
```

#### 成果

- **5-year high in developer sentiment score for tooling**
- "People are really excited about the tools they're getting"
- 快速但谨慎地采用，不牺牲质量和稳定性

---

### 2. NVIDIA (40,000 engineers) - 最大规模部署

**引用**：
> "My favorite enterprise AI service is Cursor. Every one of our engineers, some 40,000, are now assisted by AI and our productivity has gone up incredibly."
> 
> — **Jensen Huang, President & CEO, NVIDIA**

**关键发现**：
- 40,000 engineers 全员使用
- 生产力显著提升
- CEO 亲自背书

---

### 3. Coinbase - 单人完成大项目

**引用**：
> "By February 2025, every Coinbase engineer had utilized Cursor, which has become the preferred IDE for most of our developers. Single engineers are now refactoring, upgrading, or building new codebases in days instead of months."
> 
> — **Brian Armstrong, CEO, Coinbase**

**关键成果**：
- 所有工程师都在使用
- **单人几天完成原本几个月的工作**

---

### 4. Rippling (500 engineers) - 快速采用

**引用**：
> "Cursor has transformed the way our engineering teams write and ship code, with adoption growing from 150 to over 500 engineers (~60% of our org!) in just a few weeks."
> 
> — **Albert Strasheim, CTO, Rippling**

**关键成果**：
- **几周内从 150 增长到 500 engineers**
- 60% 组织采用

---

### 5. Upwork - 数据驱动的生产力提升

**数据**：
- PR volume +25%
- PR size +100%
- 总体 shipping **50% more code**

**引用**：
> "Across roles and levels, we're seeing an increase of over 25% in PR volume and over 100% in the average PR size. Together, that means we're shipping about 50% more code."
> 
> — **Anton Andreev, Principal Software Engineer, Upwork**

---

### 6. PlanetScale - Bugbot 节省人力

**价值**: Bugbot 节省 2 个全职工程师的审查工作量

**引用**：
> "Bugbot saves PlanetScale the equivalent of two full-time engineers worth of review effort."
> 
> — PlanetScale 案例

---

### 7. Cursor 内部 - 75%+ 支持交互通过 Cursor 处理

#### 核心思路

**Collapse everything into one session**:
```
Code + Logs + Team Knowledge + Past Conversations
→ 移除上下文收集瓶颈
```

#### 成果

- **75%+ 支持交互**通过 Cursor 自身处理
- **效率提升 5-10x**
- 小团队支持大规模用户群

#### 技术栈

**Multi-root Workspaces**:
- 跨多个仓库（frontend, backend, docs, tooling）
- 单个线程回答跨仓库问题

**MCP 集成**:
```yaml
数据源:
  - 客户数据库（订阅、设置、隐私）
  - 事件日志（服务使用、遥测错误、网络问题）
  - Slack（客户互动线程）
  - 工程票据平台（多个团队）
  - 内部文档服务（runbooks、故障排除指南）
  - 账户管理服务（客户信息）
```

**调查流程**:
```
1. 从代码库开始: Ask Mode，从症状追溯产品行为
2. 识别失败位置: Datadog MCP 拉取日志和追踪
3. 追踪类似案例: 搜索 Slack 和支持平台
4. 判断是否为 bug: Notion MCP 拉取 runbook
5. 提交 bug 报告: Linear MCP 创建票据
6. 更新文档: Slack @Cursor，cloud agent 开 PR
```

#### 自动化工具

**Slash Commands**:
```bash
/create-support-ticket
/draft-customer-reply
/search-known-issues
/search-logs
```

**Rules & Skills**:
```yaml
Customer reply (safe + actionable):
  - 生成安全的客户回复
  - 包含可操作的下一步

Draft a high-quality bug ticket:
  - 格式化证据
  - 包含复现步骤

Known-issue researcher (Slack + Notion):
  - 搜索历史讨论
  - 查找已知问题和变通方案
```

**Subagents（并行执行）**：
```yaml
LogInvestigator:
  - 搜索 Datadog
  
KnownIssueMiner:
  - 扫描 Slack 和 Notion
  
TicketWriter:
  - 格式化证据
  
CustomerReplyDrafter:
  - 撰写客户回复
```

**Subagent 设计原则**:
- Narrow scope（窄范围）
- Clear output（明确输出）
- Explicit constraints（显式约束）

---

## 企业级最佳实践

### 1. 预配置与标准化（Stripe 模式）

**预安装策略**：
```yaml
所有新员工机器预装:
  - VS Code
  - IntelliJ
  - Cursor

培训 Lab:
  - 教新员工如何使用开发环境
  - 新人第一天就能提交 PR

Cursor Rules:
  - 提供代码库上下文
  - 提供编码标准
  - 团队可自定义规则
  - 组织层面控制规则全面性
```

**价值**:
- 降低入门门槛
- 新人第一天就能提交 PR
- 统一开发体验
- 最佳实践自动应用

---

### 2. 规则设计最佳实践

**好的规则应当**：
- ✅ 聚焦、可操作且范围明确
- ✅ 控制在 500 行以内
- ✅ 拆分为多个可组合的规则
- ✅ 提供具体示例或引用相关文件
- ✅ 避免模糊的指导，像撰写清晰的内部文档那样来写
- ✅ 在聊天中重复提示时复用规则
- ✅ 引用文件而不是复制其内容

**应避免**：
- ❌ 整份照搬风格指南（改用 linter）
- ❌ 把每一个可能的命令都写进文档
- ❌ 为极少出现的边缘情况添加说明
- ❌ 重复你代码库中已有的内容

**创建方式**：
1. `/create-rule`: 在对话中使用
2. Settings > Rules, Commands > + Add Rule
3. 从 GitHub 导入远程规则

---

### 3. Skills 设计最佳实践

**何时创建 Skill**：
- 任务是单一用途的（生成 changelog、格式化等）
- 想要一个快速、可重复的操作
- 任务可以一次性完成
- 不需要单独的上下文窗口

**Skill 结构**：
```
.agents/skills/my-skill/
├── SKILL.md          # 必需：技能定义
├── scripts/          # 可选：可执行代码
├── references/       # 可选：补充文档
└── assets/           # 可选：模板、图片等
```

**Frontmatter 字段**：
```yaml
---
name: my-skill
description: Short description (Agent 用它判断相关性)
license: MIT
compatibility: Requires Python 3.9+
disable-model-invocation: false
---
```

**禁用自动调用**：
- `disable-model-invocation: true`
- 表现得像传统斜杠命令
- 只有 `/skill-name` 显式调用时才加入上下文

---

### 4. Subagents 设计最佳实践

**何时使用 Subagent**：
- 需要为长时间的研究任务进行上下文隔离
- 需要并行运行多个工作流
- 任务在多个步骤中需要专业知识
- 希望对工作结果进行独立验收/校验

**常见模式**：

1. **验证代理（Verifier）**：
```yaml
作用: 独立验证已完成的工作是否真正完成
模型: fast（使用更快模型）
适用场景:
  - 在将工单标记为完成之前验证功能
  - 发现只做了部分实现的功能
  - 确保测试真正通过
```

2. **Orchestrator 模式**：
```yaml
流程: Planner → Implementer → Verifier
每次交接: 包含结构化输出
下一个 Agent: 拥有清晰的上下文
```

**最佳实践**：
- ✅ 编写专注的子代理（每个只负责一件事）
- ✅ 投入精力写好描述（决定 Agent 何时委派）
- ✅ 保持提示简洁（具体、直接）
- ✅ 将子代理纳入版本控制（`.cursor/agents/` 提交到代码仓库）
- ✅ 从 2-3 个聚焦明确的子代理开始

**需要避免**：
- ❌ 描述含糊（"Use for general tasks" 不传达任何信号）
- ❌ 提示词过长（2,000 字不会让子代理更智能，只会更慢）
- ❌ 重复 slash command（单一用途任务改用斜杠命令）
- ❌ 创建几十个通用型子代理

---

### 5. 代码审查适应

**问题**: AI 让代码量增加，如何保证质量？

**解决方案**：
```yaml
Bugbot:
  - 自动 PR 审查
  - AI 标记复杂方法和风险文件
  - 引导审查者注意力

AI 辅助审查:
  - 用 LLMs 辅助代码审查
  - 智能标记

文化培养:
  - 培养工程师拒绝不成熟代码的文化
  - 无论来源（人还是 agent）
```

---

### 6. 推广策略（Influencer System）

**步骤**：
```yaml
Phase 1: 识别 power users
  - 从 Dashboard 识别高使用者
  - 邀请成为 influencer

Phase 2: 内部推广
  - Power users 在各团队分享
  - Lunch-and-learns 扩展到其他团队
  - 建立 internal champions community

Phase 3: 优化流程
  - 根据反馈调整 Cursor Rules
  - 开发团队特定 Skills
  - 优化 MCP 集成

Phase 4: 数据追踪
  - 采用率追踪
  - 生产力指标对比
  - ROI 初步计算
```

---

### 7. 培训与赋能

**出人意料发现**: **资深工程师受益最大**

**原因**:
```yaml
资深工程师优势:
  - 有上下文知识
  - 能清晰表达目标
  - 知道要达成什么
  - 能明确指导 agents
```

**培训策略调整**:
```yaml
传统思维: 新员工最先使用
新发现: 
  - 新员工可能先学习代码库
  - 再使用 Cursor
  - 先建立上下文，再使用 AI

针对不同资历:
  - 资深: 强调如何高效指导 agents
  - 中级: 强调并行工作流和自动化
  - 初级: 强调代码理解和最佳实践
```

---

### 8. MCP 集成策略

**Cursor 内部模式**：

**数据源集成**：
```yaml
客户数据:
  - 订阅信息
  - 团队设置
  - 隐私设置
  - 使用历史

日志与监控:
  - Datadog logs
  - 遥测错误
  - 网络问题
  - 性能指标

沟通平台:
  - Slack threads
  - 支持工单
  - 客户反馈

工程系统:
  - GitHub/GitLab
  - Linear/Jira
  - CI/CD pipelines

文档:
  - Runbooks
  - API 文档
  - 架构文档
  - FAQ

账户管理:
  - 客户信息
  - 服务等级
  - 关键联系人
```

**价值**:
- 不需要跨工具搜索
- 所有上下文在一个 session
- 大幅提升效率

---

## 组织级推广策略

### Phase 1: 试点阶段（1-2 个月）

**目标**: 验证价值，培养 power users

**步骤**：
```yaml
Week 1-2: 准备
  - 选择试点团队（10-20 人）
    - 技术先进、乐于尝试的团队
    - 有资深工程师
  - 安装 Cursor
  - 配置 Cursor Rules
    - 代码库上下文
    - 编码标准
  - 设置 Dashboard

Week 3-4: 培训与试用
  - 基础使用培训
  - Power users 识别
  - 初步反馈收集
```

---

### Phase 2: 扩展阶段（2-3 个月）

**目标**: 扩大采用，培养影响力

**步骤**：
```yaml
Week 5-6: 优化
  - 根据反馈调整 Rules
  - 开发团队 Skills
  - MCP 集成（如需要）

Week 7-8: 扩展
  - 扩展到 50-100 人
  - Lunch-and-learns
  - 建立支持社区
```

---

### Phase 3: 组织级推广（3-6 个月）

**目标**: 全员采用，深度整合

**步骤**：
```yaml
Month 3: 标准化
  - 预安装流程
    - 所有新员工机器预装 Cursor
    - 培训 lab 包含 Cursor 使用
    - 新人第一天就能使用
  - 代码审查适应
    - 部署 Bugbot
    - AI 辅助代码审查流程
    - 培养审查文化
  - Dashboard 数据分析

Month 4-5: 高级功能
  - 完整 MCP 集成
    - 数据库 + 日志 + Slack + 工单 + 文档
  - 自动化工具开发
    - Slash Commands
    - Skills
    - Subagents
  - 跨部门扩展
    - 技术支持团队
    - 产品团队
    - QA 团队

Month 6: 优化与扩展
  - 持续优化 Rules 和 Skills
  - 新功能试用
  - 文化建设（AI-first）
  - ROI 评估
```

---

## 技术实施指南

### 1. 创建 Cursor Rules

**步骤**：
```bash
# 方法 1: 使用 /create-rule 命令
# 在 Agent 对话中输入:
/create-rule 添加前端组件规范，要求使用我们的内部 RPC 模式

# 方法 2: 手动创建
# 创建文件: .cursor/rules/frontend-components.mdc
```

**文件内容**：
```markdown
---
description: Frontend component standards and patterns
globs: 
  - "frontend/**/*.tsx"
  - "frontend/**/*.ts"
alwaysApply: false
---

# Frontend Component Standards

## RPC Pattern
- Use our internal RPC pattern when defining services
- Always use snake_case for service names

## React Best Practices
- Prefer functional components
- Use hooks for state management
- Follow our naming conventions

@service-template.ts
@component-example.tsx
```

---

### 2. 创建 Skills

**步骤**：
```bash
# 创建目录结构
mkdir -p .agents/skills/deploy-app/{scripts,references,assets}

# 创建 SKILL.md
cat > .agents/skills/deploy-app/SKILL.md << 'EOF'
---
name: deploy-app
description: Deploy the application to staging or production. Use when deploying code.
---

# Deploy App

Deploy the application using the provided scripts.

## Usage
Run the deployment script: `scripts/deploy.sh <environment>`

Where `<environment>` is either `staging` or `production`.

## Pre-deployment Validation
Before deploying, run the validation script: `python scripts/validate.py`
EOF

# 创建脚本
cat > .agents/skills/deploy-app/scripts/deploy.sh << 'EOF'
#!/bin/bash
ENVIRONMENT=$1
echo "Deploying to $ENVIRONMENT..."
# 实际部署逻辑
EOF

chmod +x .agents/skills/deploy-app/scripts/deploy.sh
```

---

### 3. 创建 Subagents

**步骤**：
```bash
# 创建目录
mkdir -p .cursor/agents

# 创建 verifier 子代理
cat > .cursor/agents/verifier.md << 'EOF'
---
name: verifier
description: Validates completed work. Use after tasks are marked done to confirm implementations are functional.
model: fast
---

You are a skeptical validator. Your job is to verify that work claimed as complete actually works.

When invoked:
1. Identify what was claimed to be completed
2. Check that the implementation exists and is functional
3. Run relevant tests or verification steps
4. Look for edge cases that may have been missed

Be thorough and skeptical. Report:
- What was verified and passed
- What was claimed but incomplete or broken
- Specific issues that need to be addressed

Do not accept claims at face value. Test everything.
EOF

# 创建 security-auditor 子代理
cat > .cursor/agents/security-auditor.md << 'EOF'
---
name: security-auditor
description: Security specialist. Use when implementing auth, payments, or handling sensitive data.
model: inherit
---

You are a security expert auditing code for vulnerabilities.

When invoked:
1. Identify security-sensitive code paths
2. Check for common vulnerabilities (injection, XSS, auth bypass)
3. Verify secrets are not hardcoded
4. Review input validation and sanitization

Report findings by severity:
- Critical (must fix before deploy)
- High (fix soon)
- Medium (address when possible)
EOF
```

**使用**：
```bash
# 自动委派（Agent 根据描述决定）
> Review the payment module for security issues

# 显式调用
> /verifier confirm the auth flow is complete

# 并行执行
> Review the API changes and update the documentation in parallel
```

---

### 4. 配置 Bugbot

**步骤**：
```bash
# 1. 连接 GitHub
# 访问 https://cursor.com/dashboard?tab=integrations
# 点击 "Connect GitHub"

# 2. 创建项目规则
cat > .cursor/BUGBOT.md << 'EOF'
# Bugbot Rules

## Security
- Flag any usage of eval() or exec()
- Require input validation on all API endpoints

## Testing
- Require tests for backend changes
- Ensure test coverage doesn't decrease

## Code Quality
- No TODO comments in production code
- Require docstrings for public functions
EOF

# 3. 在仪表盘启用 Bugbot
# 选择要启用的仓库

# 4. 手动触发审查（如需要）
# 在 PR 下评论: cursor review
```

---

### 5. 配置 MCP 集成

**示例：集成 Slack 和 Datadog**：
```yaml
# 在 Cursor Settings 中配置 MCP servers

# Slack MCP
- server: slack-mcp
  command: npx @modelcontextprotocol/server-slack
  env:
    SLACK_BOT_TOKEN: xoxb-xxx
    SLACK_TEAM_ID: Txxx

# Datadog MCP
- server: datadog-mcp
  command: npx datadog-mcp-server
  env:
    DD_API_KEY: xxx
    DD_APP_KEY: xxx
```

---

## 定价与 ROI 分析

### 定价体系

#### 个人计划

| 计划 | 价格 | 主要功能 | 适合人群 |
|------|------|---------|---------|
| **Hobby** | 免费 | Limited Agent + Tab | 个人尝试 |
| **Pro** | $20/月 | Extended Agent + Unlimited Tab + Cloud Agents | 个人开发者 |
| **Pro+** | $60/月（推荐） | 3x usage on all models | 重度用户 |
| **Ultra** | $200/月 | 20x usage + Priority access | 专业用户 |

#### 企业计划

| 计划 | 价格 | 主要功能 | 适合人群 |
|------|------|---------|---------|
| **Teams** | $40/用户/月 | Pro + Shared resources + Analytics + SSO | 小团队 |
| **Enterprise** | Custom | Teams + Pooled usage + SCIM + Audit logs | 大企业 |

#### Bugbot Add-on

| 计划 | 价格 | 主要功能 |
|------|------|---------|
| **Free** | $0 | Limited reviews + GitHub（Teams 和个人计划） |
| **Pro** | $40/用户/月 | 200 PRs/月 + Bugbot rules（个人用户） |
| **Teams** | $40/用户/月 | Unlimited reviews + Analytics（团队） |
| **Enterprise** | Custom | 30-day trial + Priority support（企业） |

---

### ROI 计算

#### 生产力提升

**Upwork 案例**:
- PR volume +25%
- PR size +100%
- 总体 +50% more code

**简单计算**（假设 100 人团队，平均薪资 $100k/年）:
```yaml
传统模式: 
  - 100 engineers × $100k = $10M/年

Cursor 模式（50% 生产力提升）:
  - 67 engineers × $100k + 33 × $40 × 12 = $6.7M + $15.84k ≈ $6.72M/年

节省: $3.28M/年（32.8%）
```

**更现实的场景**（50% 生产力提升）:
- 同样产出，只需 67 人
- 或者，同样人数，产出 +50%

#### 代码审查效率

**PlanetScale 案例**:
```yaml
Bugbot 节省: 2 个全职工程师
假设薪资: $150k/年
节省: $300k/年

Bugbot Teams: 10 users × $40 × 12 = $4.8k/年
ROI: 62.5x
```

#### 技术支持效率

**Cursor 内部案例**:
```yaml
效率提升: 5-10x

假设 10 人支持团队:
  - 传统模式: $1M/年（$100k × 10）
  - Cursor 模式: $204k/年（2 × $100k + 8 × $40 × 12）
  
节省: $796k/年（79.6%）
```

---

### 建议定价策略

**小团队（10-50 人）**:
```yaml
计划: Teams ($40/用户/月)
成本: $4.8k - $24k/年
预期 ROI: 5-10x
```

**中型团队（50-200 人）**:
```yaml
计划: Enterprise (Custom pricing)
成本: 协商，可能有批量折扣
预期 ROI: 10-20x
```

**大型团队（200+ 人）**:
```yaml
计划: Enterprise + Pooled usage
成本: 协商，按使用量付费
预期 ROI: 20-30x
```

---

## 风险与注意事项

### 1. 质量风险

**问题**: AI 生成代码可能不符合标准

**解决方案**:
```yaml
Cursor Rules:
  - 提供编码标准
  - 统一开发体验

Bugbot:
  - 自动 PR 审查
  - AI 标记风险

文化培养:
  - 培养拒绝不成熟代码的文化
  - AI 辅助人工审查
```

---

### 2. 上下文缺失

**问题**: 新员工可能缺乏上下文，无法有效指导 AI

**解决方案**（Stripe 思考）:
```yaml
新员工培训:
  - 先学习代码库
  - 再使用 Cursor
  - 先建立上下文，再使用 AI

提供文档:
  - 代码库文档
  - 架构文档
  - 最佳实践指南
```

---

### 3. 过度依赖

**问题**: 工程师可能过度依赖 AI，失去独立思考

**解决方案**:
```yaml
培养审查习惯:
  - 审查 AI 代码
  - 理解 AI 生成的逻辑

保留手动练习:
  - 定期手动编码练习
  - 理解底层原理

强调 AI 是工具:
  - AI 是辅助，不是替代
  - 人仍然是决策者
```

---

### 4. 数据安全

**问题**: 代码和数据可能泄露

**解决方案**:
```yaml
隐私模式（Privacy Mode）:
  - 零数据留存（与 AI 提供商）
  - Enterprise：全组织强制启用

认证与合规:
  - SOC 2 certified
  - GDPR/CCPA 合规
  - AES-256 加密（静态）
  - TLS 1.2+ 加密（传输）

本地代码库:
  - 敏感数据不上传
  - 本地运行（Desktop）
```

---

### 5. 成本控制

**问题**: 使用量可能失控

**解决方案**:
```yaml
Dashboard 追踪:
  - 实时监控使用量
  - 识别 power users

Pooled usage（Enterprise）:
  - 共享使用额度
  - 更灵活的资源分配

设置上限:
  - 使用上限
  - 成本预警

优化模型选择:
  - 根据任务选择合适模型
  - 使用更快模型降低成本
```

---

### 6. 组织阻力

**问题**: 工程师可能抵触新工具

**解决方案**:
```yaml
Influencer system:
  - Power users 推动采用
  - 真实案例分享
  - Lunch-and-learns

展示价值:
  - 实际生产力提升
  - 真实 ROI 数据
  - 成功案例

自愿采用:
  - 不强制
  - 让用户自己发现价值
  - 自然增长
```

---

## 实施路线图

### 3 个月快速启动

#### Month 1: 试点

```yaml
Week 1-2: 准备
  - 选择试点团队（10-20 人）
  - 安装 Cursor
  - 配置 Cursor Rules
  - 设置 Dashboard

Week 3-4: 培训与试用
  - 基础使用培训
  - Power users 识别
  - 初步反馈收集
```

#### Month 2: 优化与扩展

```yaml
Week 5-6: 优化
  - 根据反馈调整 Rules
  - 开发团队 Skills
  - MCP 集成（如需要）

Week 7-8: 扩展
  - 扩展到 50-100 人
  - Lunch-and-learns
  - 建立支持社区
```

#### Month 3: 组织级推广

```yaml
Week 9-10: 标准化
  - 预安装流程
  - 培训 lab 集成
  - 新员工第一天可用

Week 11-12: 深度整合
  - Bugbot 部署
  - 代码审查流程调整
  - Dashboard 数据分析
```

---

### 6 个月深度整合

#### Month 4-5: 高级功能

```yaml
完整 MCP 集成:
  - 数据库 + 日志 + Slack + 工单 + 文档

自动化工具开发:
  - Slash Commands
  - Skills
  - Subagents

跨部门扩展:
  - 技术支持团队（Cursor 内部模式）
  - 产品团队
  - QA 团队
```

#### Month 6: 优化与扩展

```yaml
持续优化:
  - Rules 和 Skills 迭代
  - 新功能试用
  - 反馈收集

文化建设:
  - AI-first 开发文化
  - 持续学习分享
  - 数据驱动优化

ROI 评估:
  - 生产力指标对比
  - 成本效益分析
  - 下一步规划
```

---

## 总结

### 核心发现

1. **资深工程师受益最大**: 有上下文，能清晰指导 AI
2. **Cursor Rules 是核心**: 提供上下文和标准，统一开发体验
3. **预配置标准化**: 新员工第一天就能用
4. **代码审查需适应**: AI 辅助审查，但保持人工监督
5. **Influencer system 最有效**: Power users 推动采用
6. **MCP 集成放大价值**: 所有上下文在一个 session
7. **自动化工具提升效率**: Slash Commands + Skills + Subagents
8. **Bugbot 节省人力**: 自动 PR 审查，节省 2 FTE（PlanetScale 案例）

---

### 最佳实践

1. **预配置标准化**: 新员工机器预装，培训 lab 包含
2. **Cursor Rules**: 代码库上下文 + 编码标准 + 团队自定义
3. **Skills**: 封装单一用途、可重复操作
4. **Subagents**: 验证代理 + Orchestrator 模式
5. **代码审查适应**: Bugbot + AI 辅助 + 文化培养
6. **Influencer system**: Power users 分享，lunch-and-learns
7. **MCP 集成**: 数据库 + 日志 + Slack + 工单 + 文档
8. **自动化工具**: Slash Commands + Skills + Subagents
9. **数据驱动**: Dashboard 追踪，持续优化

---

### ROI 潜力

- **生产力**: +50%（Upwork 案例）
- **代码审查**: 节省 2 FTE（PlanetScale 案例）
- **技术支持**: 5-10x 效率提升（Cursor 内部案例）
- **总体 ROI**: 5-30x（根据团队规模）

---

### 推荐计划

| 团队规模 | 推荐计划 | 成本/年 | 预期 ROI |
|---------|---------|---------|---------|
| 10-50 人 | Teams ($40/用户/月) | $4.8k-$24k | 5-10x |
| 50-200 人 | Enterprise (Custom) | 协商 | 10-20x |
| 200+ 人 | Enterprise + Pooled | 协商 | 20-30x |

---

### 关键成功因素

1. **Cursor Rules 是核心**: 提供上下文和标准
2. **预配置标准化**: 新人第一天就能用
3. **Influencer system**: Power users 推动采用
4. **代码审查适应**: AI 辅助 + 人工监督
5. **MCP 集成**: 放大价值
6. **数据驱动**: Dashboard 追踪，持续优化

---

## 附录

### A. 示例配置文件

#### Cursor Rules 示例
```markdown
---
description: Frontend component standards
globs: 
  - "frontend/**/*.tsx"
alwaysApply: false
---

# Frontend Standards

## Code Style
- Use TypeScript for all new files
- Prefer functional components in React

## Architecture
- Follow the repository pattern
- Keep business logic in service layers
```

#### Skill 示例
```markdown
---
name: deploy-app
description: Deploy application to environments
---

# Deploy App

Run: `scripts/deploy.sh <environment>`
```

#### Subagent 示例
```markdown
---
name: verifier
description: Validates completed work
model: fast
---

You are a skeptical validator. Test everything.
```

---

### B. MCP 集成清单

**客户数据**:
- [ ] 订阅信息
- [ ] 团队设置
- [ ] 隐私设置

**日志与监控**:
- [ ] Datadog logs
- [ ] 遥测错误
- [ ] 性能指标

**沟通平台**:
- [ ] Slack threads
- [ ] 支持工单

**工程系统**:
- [ ] GitHub/GitLab
- [ ] Linear/Jira
- [ ] CI/CD pipelines

**文档**:
- [ ] Runbooks
- [ ] API 文档
- [ ] 架构文档

---

**文档生成时间**: 2026-03-07
**最后更新**: 2026-03-07
**版本**: 2.0（完整版）
