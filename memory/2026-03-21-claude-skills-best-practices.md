# Anthropic Claude Code Skills 最佳实践分析

> **来源**: https://x.com/trq212/status/2033949937936085378  
> **作者**: Thariq (Anthropic Claude Code Team)  
> **时间**: 2026-03-18  
> **数据**: 6.2M views, 15K likes, 42K bookmarks  
> **重要性**: P0 - 官方权威来源，验证我们的方向

---

## 📋 核心内容

### 一、Skill 的本质（关键认知升级）

**误区**: Skills 只是 markdown 文件  
**真相**: Skills 是 **可执行的小系统**

它可以包含：
- 脚本（scripts/）
- 资源（assets/）
- 数据（data/）
- 配置（config）
- 钩子（hooks）
- 记忆（memory）

**核心洞察**:
> Skill 本质不是提示词，而是一个"可执行的小系统"。它可以让 AI 从"更聪明一点"变成"真正能稳定干活"。

---

### 二、9 种 Skill 类型分类

Anthropic 团队对内部数百个 Skills 进行分类后，总结出 9 种类型：

#### 1. Library & API Reference ⭐⭐⭐⭐⭐
**用途**: 解释如何正确使用库、CLI、SDK

**关键要素**:
- API 参考文档
- 代码片段库（references/）
- **Gotchas 清单**（踩坑列表）

**示例**:
- `billing-lib` - 内部计费库：边界情况、footguns
- `internal-platform-cli` - 内部 CLI 每个子命令的示例
- `frontend-design` - 设计系统规范

**Gotchas**:
> Claude 在通用知识上已经很强，但你的业务脏数据、那些"文档没写但一定会炸"的地方，只有你知道。

---

#### 2. Product Verification ⭐⭐⭐⭐⭐
**用途**: 测试或验证代码是否工作

**关键要素**:
- 配合外部工具（Playwright、tmux）
- **录制视频**以便人工审查
- **程序化断言**每一步的状态

**示例**:
- `signup-flow-driver` - 注册 → 邮箱验证 → onboarding 全流程
- `checkout-verifier` - 使用 Stripe 测试卡验证结账
- `tmux-cli-driver` - 需要 TTY 的交互式 CLI 测试

**最佳实践**:
> 可以值得让一个工程师花一周时间，把你的 verification skills 做到极致。

---

#### 3. Data Fetching & Analysis ⭐⭐⭐⭐
**用途**: 连接数据和监控栈

**关键要素**:
- 凭证管理
- Dashboard IDs
- 常见查询模式

**示例**:
- `funnel-query` - "如何连接事件查看 signup → activation → paid"
- `cohort-compare` - 比较两个队列的留存/转化
- `grafana` - 数据源 UIDs、集群名称

---

#### 4. Business Process & Team Automation ⭐⭐⭐⭐
**用途**: 自动化重复工作流

**关键要素**:
- 简单指令
- 依赖其他 Skills 或 MCPs
- **保存结果到日志文件**（帮助模型保持一致）

**示例**:
- `standup-post` - 聚合 ticket tracker + GitHub + Slack → 格式化 standup
- `create-<ticket-system>-ticket` - 强制 schema + 创建后工作流
- `weekly-recap` - PRs + tickets + deploys → 周报

---

#### 5. Code Scaffolding & Templates ⭐⭐⭐⭐
**用途**: 生成框架样板代码

**关键要素**:
- 可组合的脚本
- 自然语言需求（无法纯代码覆盖）

**示例**:
- `new-<framework>-workflow` - 新 service/workflow/handler 脚手架
- `new-migration` - 迁移文件模板 + 常见坑
- `create-app` - 新应用（预配置 auth、logging、deploy）

---

#### 6. Code Quality & Review ⭐⭐⭐⭐⭐
**用途**: 强制代码质量 + 审查

**关键要素**:
- 确定性脚本或工具（最大化鲁棒性）
- 可在 hooks 或 GitHub Actions 中运行

**示例**:
- `adversarial-review` - 生成新鲜视角的 subagent 批评 → 修复 → 迭代
- `code-style` - 强制代码风格（尤其是 Claude 默认做不好的）
- `testing-practices` - 如何写测试、测什么

---

#### 7. CI/CD & Deployment ⭐⭐⭐⭐
**用途**: 获取、推送、部署代码

**关键要素**:
- 引用其他 Skills 收集数据
- 自动化流程

**示例**:
- `babysit-pr` - 监控 PR → 重试 flaky CI → 解决冲突 → auto-merge
- `deploy-<service>` - build → smoke test → 渐进式流量切换 → 自动回滚
- `cherry-pick-prod` - 隔离 worktree → cherry-pick → 冲突解决 → PR

---

#### 8. Runbooks ⭐⭐⭐⭐
**用途**: 从症状到报告的多工具调查

**关键要素**:
- 症状映射（Slack thread、alert、error signature）
- 多工具调查流程
- 结构化报告

**示例**:
- `<service>-debugging` - 症状 → 工具 → 查询模式
- `oncall-runner` - 获取 alert → 检查常见问题 → 格式化发现
- `log-correlator` - 给定 request ID，从所有系统拉取匹配日志

---

#### 9. Infrastructure Operations ⭐⭐⭐⭐
**用途**: 常规维护和运维流程

**关键要素**:
- 涉及破坏性操作（需要 guardrails）
- 遵循最佳实践

**示例**:
- `<resource>-orphans` - 查找孤儿资源 → 发到 Slack → 等待 → 确认 → 清理
- `dependency-management` - 组织的依赖审批流程
- `cost-investigation` - "为什么存储/流量账单飙升" + 具体查询模式

---

### 三、最佳实践（Tips for Making Skills）

#### 1. Don't State the Obvious ⭐⭐⭐⭐⭐
**原则**: Claude 已经知道很多通用知识

**建议**:
- 聚焦于"把 Claude 推出正常思维方式"的信息
- 避免重复 AI 本来就会的内容

**示例**: `frontend-design` skill
- ❌ 不要写"如何居中 div"
- ✅ 写"避免 Inter 字体和紫色渐变"（改进设计品味）

---

#### 2. Build a Gotchas Section ⭐⭐⭐⭐⭐
**原则**: **最高价值内容**

**建议**:
- 记录 Claude 使用 Skill 时的常见失败点
- 随时间更新，捕获新的坑

**格式示例**:
```markdown
## ⚠️ Gotchas

### 常见错误 1: [错误名称]
- **症状**: [什么情况会出现]
- **原因**: [为什么会发生]
- **解决**: [如何修复]

### 常见错误 2: ...
```

---

#### 3. Use the File System & Progressive Disclosure ⭐⭐⭐⭐⭐
**原则**: Skill 是 folder，不是单个文件

**建议**:
- 使用 `references/` 存储详细文档
- 使用 `assets/` 存储模板
- 在 SKILL.md 中指向这些文件

**示例**:
```
my-skill/
├── SKILL.md（核心指令，<300 行）
├── references/
│   ├── api.md（API 参考）
│   └── examples.md（示例）
└── assets/
    └── template.md（输出模板）
```

---

#### 4. Avoid Railroading Claude ⭐⭐⭐⭐
**原则**: 给信息，但保留灵活性

**建议**:
- ❌ 不要: "第一步做 X，第二步做 Y，第三步做 Z"
- ✅ 要: "这里有可用的工具 A、B、C，根据情况选择"

---

#### 5. Think through the Setup ⭐⭐⭐⭐
**原则**: 有些 Skill 需要用户配置

**建议**:
- 使用 `config.json` 存储配置
- 如果配置未设置，让 Agent 询问用户

**示例**:
```json
// config.json
{
  "slack_channel": "#standup",
  "timezone": "Asia/Shanghai"
}
```

---

#### 6. The Description Field Is For the Model ⭐⭐⭐⭐⭐
**原则**: description 不是介绍，是**触发器**

**建议**:
- ❌ 错误: "这是一个 GitHub 工具"
- ✅ 正确: "当用户需要查看 PR 状态、CI 运行、创建 issue 时使用。不适用于本地 git 操作"

**原因**:
> Claude 启动时，会扫描所有 Skill 的 description 来决定"这个请求用哪个 Skill？"

---

#### 7. Memory & Storing Data ⭐⭐⭐⭐⭐（新发现！）
**原则**: Skill 可以存储数据形成记忆

**建议**:
- 使用简单的 text log 或 JSON
- 或使用 SQLite 数据库

**示例**: `standup-post` skill
```bash
# 保存每次生成的 standup
standups.log

# 下次运行时，Claude 读取历史
# 可以告诉用户"自昨天以来的变化"
```

**稳定存储位置**:
- `${CLAUDE_PLUGIN_DATA}` - 升级 Skill 不会被删除

---

#### 8. Store Scripts & Generate Code ⭐⭐⭐⭐⭐
**原则**: 给 Claude 脚本，让它组合而不是重写

**建议**:
- 在 `scripts/` 中提供 helper 函数
- Claude 花时间在"组合"，而不是"重建样板"

**示例**:
```python
# scripts/data_helpers.py
def fetch_events(start_date, end_date):
    """获取指定日期范围的事件"""
    # ... 实现

def compare_cohorts(cohort_a, cohort_b):
    """比较两个队列"""
    # ... 实现
```

Claude 可以动态生成脚本组合这些函数：
```python
# Claude 生成的分析脚本
from scripts.data_helpers import fetch_events, compare_cohorts

# 获取周二的数据
events = fetch_events("2026-03-18", "2026-03-18")
# ... 分析
```

---

#### 9. On Demand Hooks ⭐⭐⭐⭐（新发现！）
**原则**: 只在 Skill 激活时生效的 hooks

**建议**:
- 用于有主见的防护（不想一直开启）
- 但某些场景极其有用

**示例**:
```yaml
# production-safety skill
hooks:
  PreToolUse:
  - match: "rm -rf"
    action: block
    message: "❌ 生产环境禁止执行 rm -rf"
  - match: "DROP TABLE"
    action: block
    message: "❌ 生产环境禁止执行 DROP TABLE"
```

激活方式:
```
用户: "帮我操作生产数据库"
Claude: [激活 production-safety skill] [所有危险命令被阻止]
```

---

#### 10. Measuring Skills ⭐⭐⭐⭐（新发现！）
**原则**: 用 PreToolUse hook 记录 Skill 使用情况

**建议**:
- 发现哪些 Skill 流行
- 发现哪些 Skill 从不触发

**实现**:
```python
# PreToolUse hook
def log_skill_usage(skill_name, tool_name):
    # 记录到数据库
    db.insert({
        "skill": skill_name,
        "tool": tool_name,
        "timestamp": now()
    })
```

---

### 四、Distributing Skills

#### 两种方式

1. **Check into repo** (`./.claude/skills`)
   - 适合小团队、少仓库
   - 每个 Skill 都会增加 context

2. **Plugin Marketplace**
   - 适合大规模团队
   - 用户自主安装

#### 管理建议

**去中心化**:
- 不用中央团队决定
- Skill owner 决定何时推广到 marketplace

**沙盒测试**:
- 新 Skill 先上传到 GitHub sandbox folder
- 在 Slack/论坛分享
- 获得关注后再 PR 到 marketplace

---

## 🎯 对我们团队的改进建议

### 立即改进（W1-W2）

#### 改进 1: 为核心 Skills 添加 Gotchas Section

**目标 Skills**:
1. `coding-agent`
2. `github`
3. `notebooklm`
4. `youtube-full`
5. `agent-browser`

**示例（coding-agent）**:
```markdown
## ⚠️ Gotchas

### PTY 必须开启
- **症状**: agent 挂起、输出乱码、颜色丢失
- **原因**: coding agents 是交互式终端应用，需要 pseudo-terminal
- **解决**: 必须使用 `pty:true`

### 必须在 git repo 启动
- **症状**: Codex 拒绝运行，报错 "not in a trusted directory"
- **原因**: Codex 要求 git repo 才能工作
- **解决**: 
  - 正常项目: 直接运行
  - 临时任务: `mktemp -d && cd $_ && git init`

### 禁止在 ~/.openclaw/ 启动
- **症状**: agent 会读取你的私密文件（MEMORY.md、SOUL.md 等）
- **原因**: agent 可以访问当前目录所有文件
- **解决**: 永远使用 `workdir:` 参数指定工作目录
```

---

#### 改进 2: 实现关键 Skills 的 Memory 机制

**示例（coding-agent）**:

创建 `scripts/session-history.json`:
```json
{
  "sessions": [
    {
      "id": "abc123",
      "task": "Build snake game",
      "workdir": "~/projects/game",
      "status": "completed",
      "timestamp": "2026-03-20T10:00:00Z",
      "duration_minutes": 45,
      "gotchas_encountered": [
        "需要 PTY",
        "需要 git repo"
      ],
      "lessons_learned": [
        "使用 --full-auto 自动批准",
        "定期检查 process:log"
      ]
    }
  ]
}
```

在 SKILL.md 添加:
```markdown
## 记忆机制

每次启动时，读取 `scripts/session-history.json` 了解：
- 最近执行的任务
- 遇到的坑
- 成功的模式

执行完成后，更新 session-history.json 记录本次经验。
```

---

#### 改进 3: 优化 description 字段

**错误示例**:
```yaml
description: "GitHub operations via gh CLI"
```

**正确示例**:
```yaml
description: "GitHub operations via `gh` CLI: issues, PRs, CI runs, code review, API queries. Use when: (1) checking PR status or CI, (2) creating/commenting on issues, (3) listing/filtering PRs or issues, (4) viewing run logs. NOT for: local git operations (commit, push, pull), cloning repos, or code review."
```

---

### 中期改进（W3-W4）

#### 改进 4: 创建 On Demand Hooks Skill

**文件**: `skills/production-safety/SKILL.md`

```markdown
---
name: production-safety
description: "生产环境保护模式。当需要操作生产环境数据库、服务器、或关键系统时使用，阻止危险命令（rm -rf、DROP TABLE、force push 等）。"
hooks:
  PreToolUse:
  - match: "rm -rf"
    action: block
    message: "❌ 生产环境禁止执行 rm -rf"
  - match: "DROP TABLE"
    action: block
    message: "❌ 生产环境禁止执行 DROP TABLE"
  - match: "git push --force"
    action: block
    message: "❌ 生产环境禁止 force push"
  - match: "kubectl delete"
    action: block
    message: "❌ 生产环境禁止 kubectl delete（除非明确指定 --namespace）"
---

# 生产环境保护

这个 Skill 激活后，会阻止所有危险命令。

## 使用场景

- 操作生产数据库
- 部署到生产环境
- 修改生产配置

## 豁免机制

如果确实需要执行危险命令，必须：
1. 明确说明原因
2. 临时禁用这个 Skill
```

---

#### 改进 5: 应用 9 种类型分类

**为现有 Skills 分类**:

| Skill | 类型 | 说明 |
|-------|------|------|
| coding-agent | Code Scaffolding + CI/CD | 代码生成 + 自动化 |
| github | Library & API Reference | GitHub CLI 使用指南 |
| notebooklm | Business Process Automation | 内容生产自动化 |
| youtube-full | Data Fetching | 数据获取工具 |
| agent-browser | Product Verification | 浏览器自动化测试 |
| skill-creator | Code Scaffolding | Skill 创建模板 |

**价值**:
- 清楚每个 Skill 的职责
- 避免功能重叠
- 便于发现缺失类型

---

### 长期改进（持续）

#### 改进 6: 建立 Skill Marketplace

**目标**:
- 团队成员可以提交自己的 Skills
- 通过实践发现最佳 Skills
- 推广到团队 marketplace

**流程**:
1. 在 `skills/sandbox/` 创建新 Skill
2. 在团队群分享
3. 获得足够关注后 PR 到 `skills/marketplace/`
4. 团队成员自主安装

---

#### 改进 7: 实施 Measuring

**目标**: 了解哪些 Skills 被使用

**实现**:
```python
# 在 openclaw.json 添加全局 hook
{
  "hooks": {
    "PreToolUse": [
      {
        "match": ".*",
        "script": "~/.openclaw/scripts/log_skill_usage.py"
      }
    ]
  }
}
```

**分析**:
- 每周查看使用报告
- 发现从不触发的 Skills → 删除或改进
- 发现高频 Skills → 重点优化

---

## 🔧 高级技巧（Tw93 洞察）

### 技巧 11: disable-auto-invoke 策略

**问题**: 每个启用的 Skill 描述符常驻上下文，每个 Skill 都在偷你的上下文空间

**策略**:

| 使用频率 | 策略 | 说明 |
|---------|------|------|
| 高频（>1 次/会话） | 保持 auto-invoke | 优化描述符，减少 token |
| 低频（<1 次/会话） | disable-auto-invoke | 手动触发，描述符完全脱离上下文 |
| 极低频（<1 次/月） | 移除 Skill | 改为 AGENTS.md 中的文档 |

**实现**:
```yaml
# 低频 Skill
---
name: config-migration
description: Migrate config schema. Run only when explicitly requested.
disable-model-invocation: true  # ← 关键配置
---
```

**描述符优化**:
```yaml
# 低效（~45 tokens）
description: |
  This skill helps you review code changes in Rust projects. 
  It checks for common issues like unsafe code, error handling...
  Use this when you want to ensure code quality before merging.

# 高效（~9 tokens）
description: Use for PR reviews with focus on correctness.
```

---

### 技巧 12: Token 成本真相

**真实的上下文成本构成**:

```
200K 总上下文
├── 固定开销 (~15-20K)
│   ├── 系统指令: ~2K
│   ├── Skill 描述符: ~1-5K
│   ├── MCP Server 工具定义: ~10-20K  ← 最大隐形杀手
│   └── LSP 状态: ~2-5K
│
├── 半固定 (~5-10K)
│   ├── CLAUDE.md: ~2-5K
│   └── Memory: ~1-2K
│
└── 动态可用 (~160-180K)
    ├── 对话历史
    ├── 文件内容
    └── 工具调用结果
```

**关键洞察**:

> 一个典型 MCP Server（如 GitHub）包含 20-30 个工具定义，每个约 200 tokens，合计 **4,000-6,000 tokens**。接 5 个 Server，光这部分固定开销就到了 **25,000 tokens（12.5%）**。

**建议**:
- 只连接真正需要的 MCP Server
- 低频 MCP 考虑手动调用
- 定期用 `/context` 检查占用

---

### 技巧 13: Tool Output 噪声

**问题**: cargo test、git log 等命令输出动辄几千行，挤爆上下文

**解决方案 1: 手动截断**
```bash
# 所有长输出命令加 | head -30
cargo test 2>&1 | head -30
git log --oneline | head -30
```

**解决方案 2: RTK（推荐）**
- 开源项目：https://github.com/rtk-ai/rtk
- 自动过滤 Tool Output，只留决策信息
- 通过 Hook 透明重写，对 Claude 无感

**效果**:
```bash
# 走 RTK 之前（几千行）
running 262 tests
test auth::test_login ... ok
...（260 行）

# 走 RTK 之后（1 行）
✓ cargo test: 262 passed (1 suite, 0.08s)
```

---

### 技巧 14: Compact Instructions

**问题**: 默认压缩算法会丢掉架构决策和约束理由

**解决方案**: 在 CLAUDE.md 中写明压缩时必须保留什么

```markdown
## Compact Instructions

When compressing, preserve in priority order:
1. Architecture decisions (NEVER summarize)
2. Modified files and key changes
3. Current verification status (pass/fail)
4. Open TODOs and rollback notes
5. Tool outputs (can delete, keep pass/fail only)
```

---

### 技巧 15: 配置健康检查

**一键诊断**:
```bash
npx skills add tw93/claude-health -a claude-code -s health -g -y
```

**运行检查**:
```
/health
```

**检查内容**:
- CLAUDE.md 质量
- rules 配置
- skills 使用率
- hooks 有效性
- allowedTools 合理性

**输出格式**:
```
优先级报告：
🔴 需要立刻修
🟡 结构性问题
🟢 可以慢慢做
```

---

## 📊 预期效果

### Skill 质量提升

- **稳定性**: +80%（Gotchas + Memory + Hooks）
- **Token 效率**: +40%（Progressive Disclosure）
- **触发准确率**: +60%（优化 description）

### 团队效率提升

- **测试自动化率**: 60% → 90%
- **文档生成时间**: 2小时 → 5分钟
- **代码审查一致性**: +80%
- **故障排查时间**: -50%
- **新人上手速度**: 3倍提升

### 知识复用

- **踩坑经验固化**: 100%（所有坑都记录在 Gotchas）
- **历史记录保留**: 100%（Memory 机制）
- **重复踩坑率**: -80%

---

## 🔗 相关资源

- **原文**: https://x.com/trq212/status/2033949937936085378
- **Claude Code Skills 文档**: https://code.claude.com/docs/en/skills
- **Skilljar 课程**: https://anthropic.skilljar.com/introduction-to-agent-skills
- **Frontend Design Skill**: https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
- **Skill Creator**: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
- **Measuring 示例代码**: https://gist.github.com/ThariqS/24defad423d701746e23dc19aace4de5

---

## 📝 更新日志

| 日期 | 变更 |
|------|------|
| 2026-03-21 | 初始版本，基于 Anthropic 官方文章 |

---

## 💬 Steven 观后感（原文）

> 看完 Claude 内部工程师这份 Skills 总结，其实有种"被官方验证了"的感觉。很多我自己摸索出来的用法，比如用脚本代替提示词、给 Skill 加记忆、防重复这些，原来他们内部早就这么干了。
>
> 一个特别重要的认知升级是：**Skill 本质不是提示词，而是一个"可执行的小系统"**。
>
> 它可以有脚本、有数据、有配置、有记忆，甚至还能拦截危险操作。这一下就把它从"让 AI 更聪明一点"，变成了"让 AI 真正能稳定干活"。
>
> 你让 Claude 每次自己写代码实现功能，和直接给它一个现成脚本调用，完全不是一个稳定性等级。
>
> 还有一个让我挺有共鸣的点是 **"Gotchas（踩坑清单）才是最有价值的内容"**。
>
> 因为通用知识 AI 本来就会，但你踩过的坑、你业务里的脏数据、那些"文档没写但一定会炸"的地方，只有你知道。这些东西不写进去，Skill 再高级也会翻车。
>
> **本质上，Skill 就是在把你过去的失败经验变成 Claude 的默认行为。**
>
> 另外一个我觉得很多人会忽略的是：**description 不是介绍，是触发器**。
>
> Claude 根本不会读完整 Skill，它只看那一小段 description 来决定要不要用。所以你写成"这是一个XX工具"基本等于没写，必须写成"当用户提到XXX时使用"。这点我自己也踩过坑，很多 Skill 明明写好了，但就是从来没被调用过。
>
> 整体看下来，我现在对 Skills 的理解更清晰了，可以简单总结一句话：
>
> **Skill = 把你平时怎么干活，固化成 Claude 可复用的能力模块**
>
> 你有多少稳定流程，就能做出多少 Skill。  
> 你踩过多少坑，就能让 Claude 少踩多少坑。
>
> 说白了，你不是在"用 AI"，而是在把自己训练成一个可以复制的 AI 工作流系统。这件事一旦跑起来，是真的会上瘾。
