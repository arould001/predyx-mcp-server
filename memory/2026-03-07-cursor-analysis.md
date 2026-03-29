# Cursor 企业级高效使用深度分析

<!-- compounded: 2026-03-15 -->

> **分析时间**: 2026-03-07
> **分析人**: Dia
> **来源**: Cursor 官网 + 企业客户案例

---

## 📋 目录

1. [核心功能概览](#核心功能概览)
2. [企业级特性](#企业级特性)
3. [客户案例研究](#客户案例研究)
4. [企业级最佳实践](#企业级最佳实践)
5. [组织级推广策略](#组织级推广策略)
6. [定价与 ROI 分析](#定价与-roi-分析)
7. [风险与注意事项](#风险与注意事项)
8. [实施路线图](#实施路线图)

---

## 核心功能概览

### 1. Agents - 自主编码能力

**核心能力**：
- 自主在后台工作，开发者专注于决策
- 支持多模型并行（OpenAI, Anthropic, Gemini, xAI, Cursor 自研）
- Cloud Agents: 云端运行，支持 Web 和移动端
- Codebase Understanding: 深度理解代码库，语义搜索

**工作模式**：
- **Plan Mode**: 复杂任务先提问、建计划、再执行
- **Design Mode**: 可视化编辑页面元素
- **Debug Mode**: 插入代码，使用执行数据定位问题
- **Build Mode**: 自主构建功能

**能力范围**：
- Terminal: 运行 shell 命令（sandboxed）
- Git & Checkpoints: 版本控制，随时回滚
- @-mentions: 指向相关文件和上下文
- Image uploads: 上传参考图片

### 2. Team Rules - 团队规则定制

**功能**：
- 给 Cursor 提供代码库上下文和编码标准
- 团队可添加自定义规则
- 组织层面控制规则全面性

**示例规则**：
```yaml
---
description: Notion-inspired block architecture
globs: components/blocks/**/*
---
# Notion Block System
## Patterns
- Use Block components for all content types
- Keyboard navigation with ↑ ↓ to move between blocks
- Real-time collaboration via CRDT operations
- Animations use 150ms ease-out timing
- Spacing follows 4px grid: 4, 8, 12, 16, 24
- Command palette triggered with /
```

### 3. Bugbot - 自动代码审查

**功能**：
- 自动在 PR 上运行代码审查
- AI 标记复杂方法和风险文件
- Bugbot Autofix: 自动发现并修复问题
- 支持 GitHub 集成

**价值**（PlanetScale 案例）：
- 节省 2 个全职工程师的审查工作量
- 保护生产环境可靠性

### 4. MCP (Model Context Protocol)

**集成能力**：
- 连接外部工具和数据源
- GitHub, Figma, Linear, Slack, Notion, Datadog 等
- 自定义 MCP servers

**Cursor 内部使用**：
- 客户数据库（订阅、设置、隐私）
- 事件日志（遥测错误、网络问题）
- Slack（客户互动线程）
- 工程票据平台
- 内部文档服务
- 账户管理服务

### 5. Plugins & Skills

**Plugins**：
- Marketplace: 社区构建的插件
- Slack Messaging Kit, Figma Visual Editor, Notion Workspace Integration 等

**Skills**：
- 领域知识注入
- 专业 prompts 和代码
- 示例: /fix-merge-conflicts, /code-review, /apply-notion-styleguide, /pr, /test

### 6. 多平台支持

- **Desktop**: 主要 IDE
- **CLI**: 终端运行 agents
- **GitHub**: PR 审查
- **Slack**: 协作沟通
- **JetBrains IDEs**: IntelliJ IDEA, PyCharm, WebStorm 等
- **Web & Mobile**: 云端 agents

---

## 企业级特性

### 1. Dashboard & Analytics

**追踪数据**：
- Agent Requests: 总请求数
- Tabs: Tab completions 使用量
- Chats: 对话数
- Users: 活跃用户数
- Model usage: 各模型使用情况
- Diffs: 代码变更量
- Agent Lines: Agent 生成的代码行数

**价值**：
- 追踪 AI 工具采用率
- 识别 power users
- 优化模型选择
- ROI 计算

### 2. 企业级控制

**Total Control**：
- 全局配置模型访问
- MCP 控制权限
- 系统级 agent 规则
- 粒度化管理

**安全与合规**：
- Zero data retention: 不训练用户数据
- SAML/OIDC SSO: 单点登录
- SCIM seat management: 用户配置
- SOC 2 Type 2 certified
- GDPR/CCPA 合规
- AES-256 加密（静态）
- TLS 1.2+ 加密（传输）
- 年度渗透测试

**支持服务**：
- Dedicated guidance: 专属指导
- Premium support: 高级支持
- Priority support & account management（Enterprise）

### 3. 团队协作

**Teams 计划功能**：
- Shared chats, commands, rules: 共享资源
- Centralized billing: 集中计费
- Usage analytics: 使用分析
- Org-wide privacy controls: 组织级隐私控制
- Role-based access control: 角色权限控制

### 4. Enterprise 计划功能

**额外功能**：
- Pooled usage: 共享使用额度
- Invoice/PO billing: 发票/采购订单计费
- AI code tracking API: AI 代码追踪 API
- Audit logs: 审计日志
- Granular admin controls: 精细管理控制
- Priority support: 优先支持

---

## 客户案例研究

### 1. Stripe (3,000+ engineers)

#### 实施策略

**预安装策略**：
- VS Code, IntelliJ, Cursor 都预装在每台机器
- 通过 lab 教新员工如何使用开发环境
- 新人第一天就能提交 PR

**Cursor Rules**：
- 给 Cursor 提供代码库上下文和编码标准
- 团队可以添加自己的规则
- 组织层面控制规则的全面性

**推广策略**：
- Influencer system（意见领袖推广）
- Power users 在 lunch-and-learns 分享工作流
- 展示如何并行运行多个 agents、写更好的 prompts

#### 代码审查适应

**挑战**: AI 让工程师写更多代码，但不能牺牲质量

**解决方案**：
- 用 LLMs 帮助审查者更高效工作
- AI 标记复杂方法或风险文件
- 引导审查者注意力到最需要的地方
- 工程师更愿意拒绝不成熟的代码（无论是人还是 agent 产生的）

#### 反直觉发现

**预期**: 初级工程师受益最大（用 AI 补偿经验不足）

**实际**: **资深工程师收益最大**

**原因**：
- 资深工程师有上下文知识
- 能清晰表达目标并指导 agents
- 知道要达成什么，能明确方向

**新思考**：
- 考虑新员工先学习代码库再给 Cursor 访问权限
- 先建立上下文，再使用 AI 工具

#### 成果

- **5-year high in developer sentiment score for tooling**
- "People are really excited about the tools they're getting"
- 快速但谨慎地采用，不牺牲质量和稳定性

### 2. NVIDIA (40,000 engineers)

**引用**：
> "My favorite enterprise AI service is Cursor. Every one of our engineers, some 40,000, are now assisted by AI and our productivity has gone up incredibly."
> 
> — **Jensen Huang, President & CEO, NVIDIA**

### 3. Coinbase

**引用**：
> "By February 2025, every Coinbase engineer had utilized Cursor, which has become the preferred IDE for most of our developers. Single engineers are now refactoring, upgrading, or building new codebases in days instead of months."
> 
> — **Brian Armstrong, CEO, Coinbase**

**关键成果**：
- 所有工程师都在使用
- 单人几天完成原本几个月的工作

### 4. Rippling (500 engineers)

**引用**：
> "Cursor has transformed the way our engineering teams write and ship code, with adoption growing from 150 to over 500 engineers (~60% of our org!) in just a few weeks."
> 
> — **Albert Strasheim, CTO, Rippling**

**关键成果**：
- 几周内从 150 增长到 500 engineers（60% org）
- 快速采用

### 5. Upwork

**数据**：
- PR volume +25%
- PR size +100%
- 总体 shipping 50% more code

**引用**：
> "Across roles and levels, we're seeing an increase of over 25% in PR volume and over 100% in the average PR size. Together, that means we're shipping about 50% more code."
> 
> — **Anton Andreev, Principal Software Engineer, Upwork**

### 6. PlanetScale (Bugbot 案例)

**价值**: Bugbot 节省 2 个全职工程师的审查工作量

**引用**：
> "Bugbot saves PlanetScale the equivalent of two full-time engineers worth of review effort."
> 
> — PlanetScale 案例

### 7. Cursor 内部（技术支持）

#### 核心思路

**Collapse everything into one session**:
- Code + Logs + Team Knowledge + Past Conversations
- 移除上下文收集瓶颈

#### 成果

- **75%+ 支持交互**通过 Cursor 自身处理
- **效率提升 5-10x**
- 小团队支持大规模用户群

#### 技术栈

**Multi-root Workspaces**:
- 跨多个仓库（frontend, backend, docs, tooling）
- 单个线程回答跨仓库问题

**MCP 集成**:
- 客户数据库（订阅、设置、隐私）
- 事件日志（服务使用、遥测错误、网络问题）
- Slack（客户互动线程）
- 工程票据平台（多个团队）
- 内部文档服务（runbooks、故障排除指南）
- 账户管理服务（客户信息）

**调查流程**:
1. **从代码库开始**: Ask Mode，从症状追溯产品行为
2. **识别失败位置**: Datadog MCP 拉取日志和追踪
3. **追踪类似案例**: 搜索 Slack 和支持平台
4. **判断是否为 bug**: Notion MCP 拉取 runbook
5. **提交 bug 报告**: Linear MCP 创建票据
6. **更新文档**: Slack @Cursor，cloud agent 开 PR

#### 自动化工具

**Slash Commands**:
- `/create-support-ticket`
- `/draft-customer-reply`
- `/search-known-issues`
- `/search-logs`

**Rules & Skills**:
- Customer reply (safe + actionable)
- Draft a high-quality bug ticket
- Known-issue researcher (Slack + Notion)

**Subagents（并行执行）**:
- **LogInvestigator**: 搜索 Datadog
- **KnownIssueMiner**: 扫描 Slack 和 Notion
- **TicketWriter**: 格式化证据
- **CustomerReplyDrafter**: 撰写客户回复

**Subagent 设计原则**:
- Narrow scope（窄范围）
- Clear output（明确输出）
- Explicit constraints（显式约束）

---

## 企业级最佳实践

### 1. 预配置与标准化

**Stripe 模式**:
- ✅ 预安装所有工具（VS Code, IntelliJ, Cursor）
- ✅ 通过 lab 教新员工使用开发环境
- ✅ 使用 Cursor Rules 提供代码库上下文和编码标准
- ✅ 允许团队添加自定义规则，但组织层面控制

**价值**:
- 降低入门门槛
- 新人第一天就能提交 PR
- 统一开发体验
- 最佳实践自动应用

### 2. 代码审查适应

**问题**: AI 让代码量增加，如何保证质量？

**解决方案**:
- ✅ 用 LLMs 辅助代码审查
- ✅ AI 标记复杂方法和风险文件
- ✅ 引导审查者注意力
- ✅ 培养工程师拒绝不成熟代码的文化（无论来源）

**工具**:
- Bugbot: 自动 PR 审查
- AI code review: 智能标记
- Custom rules: 团队特定检查

### 3. 推广策略

**Influencer System**:
- ✅ 识别 power users
- ✅ Lunch-and-learns 分享工作流
- ✅ 展示高级技巧（并行 agents、better prompts）
- ✅ 社区驱动采用

**内部文档**:
- ✅ 团队工作流文档
- ✅ 最佳实践分享
- ✅ Case studies
- ✅ FAQ

### 4. 培训与赋能

**出人意料发现**: 资深工程师受益最大

**原因**:
- 有上下文知识
- 能清晰表达目标
- 知道要达成什么

**培训策略调整**:
- 🤔 新员工可能先学习代码库，再使用 Cursor
- ✅ 先建立上下文，再使用 AI
- ✅ 针对不同资历的工程师提供不同培训

### 5. MCP 集成策略

**Cursor 内部模式**:

**数据源集成**:
- 客户数据库 → 理解客户背景
- 事件日志 → 快速定位问题
- Slack → 查找历史讨论
- 工单平台 → 了解团队工作方式
- 文档服务 → Runbooks 和故障排除
- 账户管理 → 客户关键信息

**价值**:
- 不需要跨工具搜索
- 所有上下文在一个 session
- 大幅提升效率

### 6. 自动化工具开发

**Slash Commands**:
- 为常见流程创建命令
- `/create-ticket`, `/draft-reply`, `/search-logs`
- 降低重复工作

**Rules & Skills**:
- 封装团队最佳实践
- Customer reply 模板
- Bug ticket 格式
- Known-issue 搜索流程

**Subagents**:
- 并行执行独立任务
- LogInvestigator, KnownIssueMiner, TicketWriter, CustomerReplyDrafter
- 结果合并后人工审核

### 7. Dashboard 与数据驱动

**追踪指标**:
- Agent Requests: 工具使用量
- Tabs/Chats: 交互频率
- Users: 采用率
- Model usage: 模型选择
- Diffs/Agent Lines: 代码产出

**价值**:
- 追踪采用进度
- 识别 power users
- 优化模型选择
- 计算 ROI

---

## 组织级推广策略

### Phase 1: 试点阶段（1-2 个月）

**目标**: 验证价值，培养 power users

**步骤**:
1. **选择试点团队**:
   - 技术先进、乐于尝试的团队
   - 10-20 人规模
   - 有资深工程师

2. **预配置环境**:
   - 安装 Cursor
   - 设置 Cursor Rules（代码库上下文 + 编码标准）
   - 配置 MCP 集成（如适用）

3. **培训与支持**:
   - 基础使用培训
   - Lunch-and-learns 分享
   - 建立支持渠道（Slack channel）

4. **收集反馈**:
   - 使用数据追踪（Dashboard）
   - 定期反馈会
   - 识别最佳实践

### Phase 2: 扩展阶段（2-3 个月）

**目标**: 扩大采用，培养影响力

**步骤**:
1. **识别 power users**:
   - 从 Dashboard 识别高使用者
   - 邀请成为 influencer

2. **内部推广**:
   - Power users 在各团队分享
   - Lunch-and-learns 扩展到其他团队
   - 建立 internal champions community

3. **优化流程**:
   - 根据反馈调整 Cursor Rules
   - 开发团队特定 Skills
   - 优化 MCP 集成

4. **数据追踪**:
   - 采用率追踪
   - 生产力指标对比
   - ROI 初步计算

### Phase 3: 组织级推广（3-6 个月）

**目标**: 全员采用，深度整合

**步骤**:
1. **预安装标准化**:
   - 所有新员工机器预装 Cursor
   - 培训 lab 包含 Cursor 使用
   - 新人第一天就能使用

2. **代码审查适应**:
   - 部署 Bugbot
   - AI 辅助代码审查流程
   - 培养审查文化

3. **深度集成**:
   - 完整 MCP 集成（数据库、日志、Slack 等）
   - 自动化工具（Slash Commands, Subagents）
   - 团队 Skills 库

4. **持续优化**:
   - 定期回顾使用数据
   - 优化规则和工具
   - 分享最佳实践

### Phase 4: 优化与扩展（持续）

**目标**: 持续改进，扩大应用

**步骤**:
1. **新功能试用**:
   - 优先使用新功能
   - 反馈给 Cursor 团队

2. **跨部门扩展**:
   - 技术支持团队（Cursor 内部模式）
   - 产品团队
   - QA 团队

3. **文化建设**:
   - AI-first 开发文化
   - 持续学习分享
   - 数据驱动优化

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
| **Free** | $0 | Limited reviews + GitHub |
| **Pro** | $40/用户/月 | 200 PRs/月 + Bugbot rules |
| **Teams** | $40/用户/月 | Unlimited reviews + Analytics |
| **Enterprise** | Custom | 30-day trial + Priority support |

### ROI 计算

#### 生产力提升

**Upwork 案例**:
- PR volume +25%
- PR size +100%
- 总体 +50% more code

**简单计算**（假设 100 人团队，平均薪资 $100k/年）:
- 传统模式: 100 engineers × $100k = $10M/年
- Cursor 模式: 67 engineers × $100k + 33 × $40 × 12 = $6.7M + $15.84k ≈ $6.72M/年
- **节省**: $3.28M/年（32.8%）

**更现实的场景**（50% 生产力提升）:
- 同样产出，只需 67 人
- 或者，同样人数，产出 +50%

#### 代码审查效率

**PlanetScale 案例**:
- Bugbot 节省 2 个全职工程师
- 假设薪资 $150k/年
- **节省**: $300k/年
- Bugbot Teams: 10 users × $40 × 12 = $4.8k/年
- **ROI**: 62.5x

#### 技术支持效率

**Cursor 内部案例**:
- 效率提升 5-10x
- 假设 10 人支持团队，薪资 $100k/年 = $1M/年
- 提升后: 2 人 × $100k + 8 × $40 × 12 = $200k + $3.84k ≈ $204k/年
- **节省**: $796k/年（79.6%）

### 建议定价策略

**小团队（10-50 人）**:
- **计划**: Teams ($40/用户/月)
- **成本**: $4.8k - $24k/年
- **预期 ROI**: 5-10x

**中型团队（50-200 人）**:
- **计划**: Enterprise (Custom pricing)
- **成本**: 协商，可能有批量折扣
- **预期 ROI**: 10-20x

**大型团队（200+ 人）**:
- **计划**: Enterprise + Pooled usage
- **成本**: 协商，按使用量付费
- **预期 ROI**: 20-30x

---

## 风险与注意事项

### 1. 质量风险

**问题**: AI 生成代码可能不符合标准

**解决方案**:
- ✅ Cursor Rules 提供编码标准
- ✅ Bugbot 自动审查
- ✅ 培养工程师拒绝不成熟代码的文化
- ✅ AI 辅助人工审查

### 2. 上下文缺失

**问题**: 新员工可能缺乏上下文，无法有效指导 AI

**解决方案**（Stripe 思考）:
- 🤔 新员工先学习代码库，再使用 Cursor
- ✅ 建立上下文后再使用 AI
- ✅ 提供代码库文档和培训

### 3. 过度依赖

**问题**: 工程师可能过度依赖 AI，失去独立思考

**解决方案**:
- ✅ 培养审查 AI 代码的习惯
- ✅ 保留手动编码练习
- ✅ 强调 AI 是工具，不是替代

### 4. 数据安全

**问题**: 代码和数据可能泄露

**解决方案**:
- ✅ Zero data retention（Enterprise）
- ✅ SOC 2 certified
- ✅ GDPR/CCPA 合规
- ✅ 本地代码库，敏感数据不上传

### 5. 成本控制

**问题**: 使用量可能失控

**解决方案**:
- ✅ Dashboard 追踪使用量
- ✅ Pooled usage（Enterprise）
- ✅ 设置使用上限
- ✅ 优化模型选择

### 6. 组织阻力

**问题**: 工程师可能抵触新工具

**解决方案**:
- ✅ Influencer system
- ✅ Lunch-and-learns
- ✅ 展示实际价值
- ✅ 自愿采用，不强制

---

## 实施路线图

### 3 个月快速启动

#### Month 1: 试点

**Week 1-2: 准备**
- 选择试点团队（10-20 人）
- 安装 Cursor
- 配置 Cursor Rules
- 设置 Dashboard

**Week 3-4: 培训与试用**
- 基础使用培训
- Power users 识别
- 初步反馈收集

#### Month 2: 优化与扩展

**Week 5-6: 优化**
- 根据反馈调整 Rules
- 开发团队 Skills
- MCP 集成（如需要）

**Week 7-8: 扩展**
- 扩展到 50-100 人
- Lunch-and-learns
- 建立支持社区

#### Month 3: 组织级推广

**Week 9-10: 标准化**
- 预安装流程
- 培训 lab 集成
- 新员工第一天可用

**Week 11-12: 深度整合**
- Bugbot 部署
- 代码审查流程调整
- Dashboard 数据分析

### 6 个月深度整合

#### Month 4-5: 高级功能

- 完整 MCP 集成（数据库、日志、Slack）
- 自动化工具开发（Slash Commands, Subagents）
- 跨部门扩展（技术支持、产品、QA）

#### Month 6: 优化与扩展

- 持续优化 Rules 和 Skills
- 新功能试用
- 文化建设（AI-first）
- ROI 评估

---

## 总结

### 核心发现

1. **资深工程师受益最大**: 有上下文，能清晰指导 AI
2. **预配置是关键**: Stripe 模式，新人第一天就能用
3. **Cursor Rules 是核心**: 提供上下文和标准，统一开发体验
4. **代码审查需适应**: AI 辅助审查，但保持人工监督
5. **Influencer system 最有效**: Power users 推动采用
6. **MCP 集成放大价值**: 所有上下文在一个 session
7. **自动化工具提升效率**: Slash Commands, Skills, Subagents

### 最佳实践

1. **预配置标准化**: 新员工机器预装，培训 lab 包含
2. **Cursor Rules**: 代码库上下文 + 编码标准 + 团队自定义
3. **代码审查适应**: Bugbot + AI 辅助 + 文化培养
4. **Influencer system**: Power users 分享，lunch-and-learns
5. **MCP 集成**: 数据库 + 日志 + Slack + 工单 + 文档
6. **自动化工具**: Slash Commands + Skills + Subagents
7. **数据驱动**: Dashboard 追踪，持续优化

### ROI 潜力

- **生产力**: +50%（Upwork 案例）
- **代码审查**: 节省 2 FTE（PlanetScale 案例）
- **技术支持**: 5-10x 效率提升（Cursor 内部案例）
- **总体 ROI**: 5-30x（根据团队规模）

### 推荐计划

**小团队（10-50 人）**: Teams ($40/用户/月)
**中型团队（50-200 人）**: Enterprise (Custom)
**大型团队（200+ 人）**: Enterprise + Pooled usage

---

## 附录

### A. Cursor Rules 示例

```yaml
---
description: Team coding standards
globs: **/*.ts
---
# TypeScript Best Practices

## Code Style
- Use const over let
- Prefer interfaces over types
- Use async/await over .then()

## Architecture
- Follow hexagonal architecture
- Dependency injection for services
- Repository pattern for data access

## Testing
- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for critical paths

## Naming Conventions
- camelCase for variables and functions
- PascalCase for classes and interfaces
- UPPER_SNAKE_CASE for constants
```

### B. Subagent 配置示例

```json
{
  "subagents": [
    {
      "name": "LogInvestigator",
      "scope": "Search Datadog for failure point and supporting evidence",
      "output": "Structured log analysis with timestamps and error patterns",
      "constraints": [
        "Only search last 24 hours",
        "Focus on ERROR and WARN levels",
        "Extract request IDs and user IDs"
      ]
    },
    {
      "name": "KnownIssueMiner",
      "scope": "Scan Slack and Notion for prior threads and workarounds",
      "output": "Summary of similar issues with status and workarounds",
      "constraints": [
        "Search Slack #support and #engineering",
        "Look for newest threads first",
        "Include current status if available"
      ]
    },
    {
      "name": "TicketWriter",
      "scope": "Format evidence into complete escalation",
      "output": "Linear ticket with reproduction steps, evidence, and severity",
      "constraints": [
        "Use team ticket template",
        "Include all gathered evidence",
        "Assign to appropriate team"
      ]
    },
    {
      "name": "CustomerReplyDrafter",
      "scope": "Write customer response, stripping out internal details",
      "output": "Customer-friendly response with next steps",
      "constraints": [
        "No internal URLs or identifiers",
        "Include workaround if available",
        "Set appropriate expectations"
      ]
    }
  ]
}
```

### C. MCP 集成清单

**客户数据**:
- [ ] 订阅信息
- [ ] 团队设置
- [ ] 隐私设置
- [ ] 使用历史

**日志与监控**:
- [ ] Datadog logs
- [ ] 遥测错误
- [ ] 网络问题
- [ ] 性能指标

**沟通平台**:
- [ ] Slack threads
- [ ] 支持工单
- [ ] 客户反馈

**工程系统**:
- [ ] GitHub/GitLab
- [ ] Linear/Jira
- [ ] CI/CD pipelines

**文档**:
- [ ] Runbooks
- [ ] API 文档
- [ ] 架构文档
- [ ] FAQ

**账户管理**:
- [ ] 客户信息
- [ ] 服务等级
- [ ] 关键联系人

---

**文档生成时间**: 2026-03-07
**最后更新**: 2026-03-07
**版本**: 1.0
