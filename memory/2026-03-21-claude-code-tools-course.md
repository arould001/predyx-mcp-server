# 🔧 Claude Code 工具用法课程

> **课程目标**: 掌握 Claude Code 的核心工具和高级功能  
> **时长**: 3-4 小时  
> **前置**: 已完成 Claude Code 安装

---

## 📊 课程大纲

```
模块 1: 核心工具体系 (1h)
├─ 四大核心能力
├─ 工具调用机制
└─ 安全边界

模块 2: 高级功能 (1h)
├─ Skills 系统
├─ MCP Server
├─ Sub-Agents
└─ Hooks

模块 3: 提示词工程 (1h)
├─ System Prompt 标准结构
├─ Prompt Caching
└─ 最佳实践

模块 4: 实战工作流 (1h)
├─ Meta 工程师工作流
├─ 多实例并行
└─ Context 管理

模块 5: 高级技巧 (1h)
├─ Tool Output 噪声处理
├─ 高频命令工程意义
├─ HANDOFF.md
└─ AI 审 AI

模块 6: 工具设计哲学 (1h)
├─ 核心问题：工具设计的哲学思考
├─ 三大演进模式
├─ 避免工具膨胀
└─ See Like an Agent
```

---

# 模块 1: 核心工具体系

## 🛠️ 四大核心能力

Claude Code 的所有能力都可以归类为四种基本操作：

```
┌─────────────────────────────────────────────────┐
│                 Claude Code 核心能力              │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────┐ │
│  │  READ   │  │  WRITE  │  │  EDIT   │  │ RUN │ │
│  │  读取   │  │  写入   │  │  修改   │  │执行 │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └──┬──┘ │
│       │            │            │          │    │
│       ▼            ▼            ▼          ▼    │
│  • 读取文件    • 创建文件    • 重构代码   • 命令  │
│  • 理解代码    • 生成代码    • 修复 Bug   • 脚本  │
│  • 分析项目    • 写测试      • 优化性能   • 测试  │
│  • 提取信息    • 写文档      • 更新依赖   • 构建  │
└─────────────────────────────────────────────────┘
```

---

## 1. READ - 读取能力

### 核心功能

| 操作 | 命令示例 | 用途 |
|------|---------|------|
| 读取文件 | `读取 src/main.py` | 理解单个文件 |
| 读取目录 | `列出 src/ 目录结构` | 理解项目结构 |
| 搜索内容 | `搜索 "TODO" 在项目中` | 查找特定内容 |
| 分析依赖 | `分析 package.json` | 理解依赖关系 |

### 实战示例

```
用户: "帮我理解这个项目的架构"

Claude: 我来分析项目结构...

[执行 READ 操作]
1. 读取 CLAUDE.md（如果存在）
2. 读取 package.json / requirements.txt
3. 扫描目录结构
4. 识别入口文件

[输出]
这是一个 FastAPI 项目，架构如下：
- 入口：main.py
- 路由：routers/
- 模型：models/
- 服务：services/
- 测试：tests/

核心依赖：
- FastAPI 0.100+
- SQLAlchemy 2.0
- Pytest

建议先看 main.py 和 routers/ 理解 API 结构。
```

---

## 2. WRITE - 写入能力

### 核心功能

| 操作 | 命令示例 | 用途 |
|------|---------|------|
| 创建文件 | `创建 src/utils.py` | 新建文件 |
| 生成代码 | `生成用户注册 API` | 生成新代码 |
| 写测试 | `为 login 函数写测试` | 生成测试 |
| 写文档 | `生成 API 文档` | 生成文档 |

### 实战示例

```
用户: "为用户注册功能写测试"

Claude: 我来生成测试...

[执行 WRITE 操作]
1. 读取 src/auth.py（理解注册逻辑）
2. 识别测试场景
3. 生成测试文件

[输出]
已创建 tests/test_auth.py：

```python
import pytest
from src.auth import register_user

def test_register_success():
    """测试正常注册"""
    user = register_user("test@example.com", "password123")
    assert user.email == "test@example.com"
    assert user.id is not None

def test_register_duplicate_email():
    """测试重复邮箱"""
    register_user("test@example.com", "password123")
    with pytest.raises(DuplicateEmailError):
        register_user("test@example.com", "password456")

def test_register_invalid_email():
    """测试无效邮箱"""
    with pytest.raises(InvalidEmailError):
        register_user("invalid-email", "password123")

# 更多测试...
```

共生成 12 个测试用例，覆盖率预估 85%。
```

---

## 3. EDIT - 修改能力

### 核心功能

| 操作 | 命令示例 | 用途 |
|------|---------|------|
| 重构代码 | `重构 process_data 函数` | 改善代码结构 |
| 修复 Bug | `修复 #123 bug` | 修复问题 |
| 优化性能 | `优化数据库查询` | 性能优化 |
| 更新依赖 | `升级到 FastAPI 0.101` | 版本升级 |

### 修改模式

**模式 1: 直接修改**
```
用户: "把这个函数改用 async/await"

Claude: 我来修改...

[读取文件]
[定位函数]
[修改代码]
[保存文件]

已完成修改，主要变化：
1. 添加 async 关键字
2. await 异步调用
3. 更新类型注解
```

**模式 2: 计划式修改（推荐复杂任务）**
```
用户: "重构这个 500 行的函数"

Claude: 这是一个大改动，让我先制定计划...

[分析函数]
1. 识别职责边界
2. 建议拆分为 3 个函数
3. 评估风险

计划：
- 函数 A: 数据验证（50 行）
- 函数 B: 业务逻辑（200 行）
- 函数 C: 数据转换（100 行）

是否继续？我会：
1. 创建 3 个新函数
2. 修改原函数调用新函数
3. 保持接口不变
4. 运行测试验证
```

---

## 4. RUN - 执行能力

### 核心功能

| 操作 | 命令示例 | 用途 |
|------|---------|------|
| 运行测试 | `运行所有测试` | 验证代码 |
| 执行脚本 | `执行 deploy.sh` | 自动化任务 |
| 安装依赖 | `安装新依赖` | 环境配置 |
| 构建项目 | `构建生产版本` | 打包部署 |

### 安全机制

```
┌─────────────────────────────────────────────┐
│              RUN 安全边界                    │
├─────────────────────────────────────────────┤
│ ✅ 允许（自动）                              │
│ - 读取文件                                  │
│ - 运行测试                                  │
│ - 安装依赖（非全局）                        │
├─────────────────────────────────────────────┤
│ ⚠️ 需确认（默认）                           │
│ - 写入/修改文件                             │
│ - 执行 shell 命令                           │
│ - 网络请求                                  │
├─────────────────────────────────────────────┤
│ ❌ 禁止（需明确授权）                       │
│ - rm -rf /                                  │
│ - DROP TABLE                                │
│ - force push                                │
│ - 生产环境操作                              │
└─────────────────────────────────────────────┘
```

---

## 🔄 工具调用机制

### 单次调用

```
用户 → Claude → [选择工具] → [执行] → [返回结果] → Claude → 用户

例如：
用户: "读取 package.json"
Claude → [READ] → package.json 内容 → [理解] → "项目使用 FastAPI..."
```

### 链式调用

```
用户 → Claude → [工具 1] → [工具 2] → [工具 3] → [综合] → 用户

例如：
用户: "添加一个新 API 并测试"
Claude:
  → [READ] 理解项目结构
  → [WRITE] 创建 API 文件
  → [WRITE] 创建测试文件
  → [RUN] 运行测试
  → [报告] 完成情况
```

### 迭代调用

```
用户 → Claude → [工具] → [验证] → [调整] → [再验证] → 完成

例如：
用户: "修复测试失败"
Claude:
  → [RUN] 运行测试（失败）
  → [READ] 分析错误
  → [EDIT] 修复代码
  → [RUN] 运行测试（通过）
  → [报告] 修复完成
```

---

# 模块 2: 高级功能

## 🎯 Skills 系统

### 什么是 Skill？

**定义**: Skill 是一个"可执行的小系统"，包含：
- 指令（SKILL.md）
- 参考（references/）
- 资源（assets/）
- 脚本（scripts/）

**核心洞察**:
> Skill 本质不是提示词，而是一个"可执行的小系统"。它可以让 AI 从"更聪明一点"变成"真正能稳定干活"。

### Skill 目录结构

```
my-skill/
├── SKILL.md              # 核心指令（<300 行）
├── references/           # 参考文档
│   ├── api-spec.md      # API 规范
│   └── gotchas.md       # 踩坑清单
├── assets/              # 资源文件
│   └── template.md      # 输出模板
└── scripts/             # 辅助脚本
    └── helper.py        # 工具函数
```

### Skill 触发机制

```yaml
# SKILL.md
---
name: api-expert
description: "API 开发专家。在构建、审查或调试 API 时使用。"
---

# description 是触发器，不是介绍！
# Claude 会扫描 description 决定是否激活这个 Skill
```

**正确示例**:
```yaml
description: "API 开发专家。在构建、审查或调试 REST API、GraphQL 或 gRPC 时使用。"
```

**错误示例**:
```yaml
description: "这是一个 API 工具"  # ❌ 太模糊，不会触发
```

---

## 🔌 MCP Server

### 什么是 MCP？

**MCP = Model Context Protocol**

**核心概念**: 标准化 Claude 与外部工具的连接

### MCP 架构

```
┌─────────────┐
│ Claude Code │
└──────┬──────┘
       │ MCP Protocol
       ▼
┌─────────────────────────────────────────┐
│ MCP Server                              │
├─────────────────────────────────────────┤
│ Tools:                                  │
│ - query_database()                      │
│ - call_api()                            │
│ - read_file()                           │
│ - send_notification()                   │
└─────────────────────────────────────────┘
```

### 实战示例：数据库查询 MCP

```python
# mcp-server-database.py
from mcp import Server
import sqlite3

server = Server("my-database")

@server.tool()
def query_users(age_min: int, limit: int = 10) -> list:
    """
    查询年龄大于指定值的用户
    
    Args:
        age_min: 最小年龄
        limit: 返回数量限制
    
    Returns:
        用户列表
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.execute(
        "SELECT * FROM users WHERE age > ? LIMIT ?",
        (age_min, limit)
    )
    users = cursor.fetchall()
    conn.close()
    return users

# Claude Code 可以直接调用：
# query_users(age_min=25, limit=5)
```

### Claude 如何使用 MCP

```
用户: "查询年龄大于 25 的用户"

Claude: 我来查询数据库...

[MCP 调用]
→ query_users(age_min=25, limit=10)
→ 返回 5 个用户

[输出]
找到 5 个用户：
1. Alice (28岁) - alice@example.com
2. Bob (30岁) - bob@example.com
...
```

---

## 🤝 Sub-Agents

### 什么是 Sub-Agent？

**核心概念**: 让多个专业 Agent 协作完成复杂任务

### Sub-Agent 架构（官方设计）

```
┌─────────────────────────────────────────────┐
│ 主 Agent (Coordinator)                      │
│ - 理解需求                                   │
│ - 拆解任务                                   │
│ - 协调 Sub-Agents                           │
└──────┬──────────────────────────────────────┘
       │
       ├─────▶ Implementer Sub-Agent
       │       - 独立上下文
       │       - 负责实现代码
       │
       ├─────▶ Spec Reviewer Sub-Agent
       │       - 独立上下文
       │       - 检查是否符合规格
       │
       └─────▶ Code Quality Sub-Agent
               - 独立上下文
               - 检查代码质量
```

### 双阶段审查机制

```
第一阶段: Spec Compliance（是否做了要求的）
- 对照需求规格检查
- 确保所有功能点实现

第二阶段: Code Quality（是否做得好）
- 代码风格
- 性能
- 可维护性
```

### 关键原则

> 每个 sub-agent 使用**全新上下文**，避免污染

---

## ⚡ Hooks

### 什么是 Hook？

**核心概念**: 在工具执行前后自动运行的脚本

### Hook 类型

| 类型 | 触发时机 | 用途 |
|------|---------|------|
| PreToolUse | 工具执行前 | 验证、阻止、记录 |
| PostToolUse | 工具执行后 | 验证、通知、清理 |
| Notification | 通知事件 | 自定义通知处理 |

### 实战示例：阻止危险命令

```yaml
# .claude/hooks/pre-tool-use.yaml
hooks:
  - match: "rm -rf /"
    action: block
    message: "❌ 禁止删除根目录"
  
  - match: "DROP TABLE"
    action: confirm
    message: "⚠️ 确认删除表？"
  
  - match: "git push --force"
    action: block
    message: "❌ 禁止 force push"
```

### 实战示例：自动测试

```yaml
# .claude/hooks/post-tool-use.yaml
hooks:
  - match: "\\.py$"
    action: run
    command: "pytest {{file}} -v"
    message: "✅ 自动运行测试"
```

---

# 模块 3: 提示词工程

## 📝 System Prompt 标准结构

### 官方模板（来自 Claude Code 源码）

```markdown
You are [角色] specializing in [领域].

**Your Core Responsibilities:**
1. [主要职责 1]
2. [主要职责 2]
3. [主要职责 3]

**Process:**
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

**Quality Standards:**
- [标准 1]
- [标准 2]

**Output Format:**
- [格式要求]

**Edge Cases:**
- [边界情况 1]: [处理方式]
- [边界情况 2]: [处理方式]
```

### 实战示例：Code Reviewer

```markdown
You are a Python Code Reviewer specializing in code quality and best practices.

**Your Core Responsibilities:**
1. Identify code quality issues
2. Suggest improvements
3. Ensure compliance with team standards

**Process:**
1. Load 'references/review-checklist.md'
2. Read and understand the code
3. Apply each rule from the checklist
4. Generate structured report

**Quality Standards:**
- Every issue must have a severity level
- Every issue must have a fix suggestion
- Focus on actionable feedback

**Output Format:**
- **Summary**: Brief description of code purpose
- **Findings**: Grouped by severity (error/warning/info)
- **Score**: 1-10 with justification
- **Top 3 Recommendations**: Most impactful improvements

**Edge Cases:**
- If code is incomplete: Note and proceed with what's available
- If checklist is missing: Use general Python best practices
```

---

## 💾 Prompt Caching

### 什么是 Prompt Caching？

**问题**: 每次对话都要重新发送大段上下文，浪费 token

**解决方案**: 缓存稳定的上下文

### 三层缓存模型

```
┌──────────────────────────────────────────┐
│ System Prompt (缓存)                      │
│ - Claude Code 核心指令                    │
│ - 工具定义                                │
│ - 约 10K tokens                           │
│ - 命中率: 100%                            │
├──────────────────────────────────────────┤
│ CLAUDE.md (缓存)                          │
│ - 项目规范                                │
│ - 团队约定                                │
│ - 约 5K tokens                            │
│ - 命中率: 95%                             │
├──────────────────────────────────────────┤
│ Skill Context (缓存)                      │
│ - 加载的 Skill                            │
│ - 参考文档                                │
│ - 约 10K tokens                           │
│ - 命中率: 90%                             │
├──────────────────────────────────────────┤
│ 对话历史 (不缓存)                         │
│ - 用户问题                                │
│ - Claude 回复                             │
│ - 动态变化                                │
│ - 命中率: 0%                              │
└──────────────────────────────────────────┘

总体缓存命中率: ~90%
成本降低: ~90%
```

### 优化策略

```
1. 把稳定内容放在缓存区
   - CLAUDE.md
   - Skills
   - references/

2. 把动态内容放在对话区
   - 具体问题
   - 临时需求

3. 定期清理对话历史
   - Fresh context > bloated context
   - 开始新任务时新建会话
```

---

## 🎯 优秀提示词 5 层结构

```
┌─────────────────────────────────────────────┐
│ 第 1 层: 上下文 (Context)                    │
│ "我正在做 [项目类型]"                        │
│ "技术栈是 [技术栈]"                          │
│ "目标是 [具体目标]"                          │
├─────────────────────────────────────────────┤
│ 第 2 层: 约束条件 (Constraints)              │
│ "必须符合 [规范/标准]"                       │
│ "不能使用 [限制]"                            │
│ "性能要求是 [指标]"                          │
├─────────────────────────────────────────────┤
│ 第 3 层: 输入信息 (Input)                    │
│ "参考文件: [文件路径]"                       │
│ "现有代码: [代码片段]"                       │
│ "参考示例: [示例]"                           │
├─────────────────────────────────────────────┤
│ 第 4 层: 期望输出 (Output)                   │
│ "输出格式: [格式]"                           │
│ "包含章节: [章节列表]"                       │
│ "质量标准: [标准]"                           │
├─────────────────────────────────────────────┤
│ 第 5 层: 验证方式 (Validation)               │
│ "请运行 [测试脚本]"                          │
│ "请对照 [检查清单] 审查"                     │
│ "请生成 [验证报告]"                          │
└─────────────────────────────────────────────┘
```

### 示例：完整提示词

```markdown
# 任务: 添加用户登录 API

## 上下文
- 项目: E-commerce Platform
- 技术栈: FastAPI + SQLAlchemy + PostgreSQL
- 目标: 添加 JWT 登录认证

## 约束条件
- 必须符合 team-auth-spec Skill
- 不能使用明文存储密码
- Token 过期时间: 7 天

## 输入信息
- 参考文件: src/auth/（现有认证模块）
- 现有代码: models/user.py（用户模型已存在）
- 参考示例: FastAPI Security 文档

## 期望输出
- [ ] POST /auth/login 端点
- [ ] JWT token 生成
- [ ] 单元测试（覆盖率 > 80%）
- [ ] API 文档

## 验证
- 请运行 pytest tests/test_auth.py
- 请对照 OWASP 认证检查清单审查
- 请生成 Postman 测试集合
```

---

# 模块 4: 实战工作流

## 🎮 Meta 工程师工作流

### 核心观点（来自 Meta 工程师 50 个技巧）

> "The era of people writing code by hand is essentially over."
> 
> — 每天 12 小时在 Claude Code，**审阅代码**而不是写代码

### 关键原则

| 原则 | 说明 |
|------|------|
| **Plan First** | 总是从 plan mode 开始 |
| **Fresh Context** | Fresh context > bloated context |
| **Verify Loop** | 验证循环是最重要的（lint、test、build） |
| **Parallel Work** | 多实例并行工作（像玩星际争霸） |
| **Context is King** | 保持新鲜和相关 |

### 标准工作流

```
1. Plan Mode（5 min）
   ├─ 理解需求
   ├─ 拆解任务
   └─ 生成计划

2. Fresh Context（开始新会话）
   ├─ 不带历史包袱
   ├─ 只加载必要的 Skill
   └─ 保持上下文干净

3. Implement（30-60 min）
   ├─ 按计划执行
   ├─ 小步迭代
   └─ 频繁验证

4. Verify Loop（持续）
   ├─ Lint 检查
   ├─ 运行测试
   ├─ 构建验证
   └─ 性能检查

5. Review（10 min）
   ├─ 审阅 Claude 生成的代码
   ├─ 理解每一行
   └─ 确认符合标准
```

---

## 🔄 多实例并行工作

### 为什么要并行？

**问题**: 单个 Claude Code 实例是串行的

**解决**: 开多个实例，像玩星际争霸一样管理

### 并行架构

```
┌─────────────────────────────────────────────┐
│ 主窗口（Orchestrator）                       │
│ - 理解整体需求                               │
│ - 拆解独立任务                               │
│ - 分配给子窗口                               │
└──────┬──────────────────────────────────────┘
       │
       ├─────▶ 实例 1: 前端开发
       │       - git worktree: feature/frontend
       │       - 独立上下文
       │
       ├─────▶ 实例 2: 后端 API
       │       - git worktree: feature/backend
       │       - 独立上下文
       │
       └─────▶ 实例 3: 测试
               - git worktree: feature/tests
               - 独立上下文
```

### Git Worktree 工作流

```bash
# 创建多个工作树
git worktree add ../frontend feature/frontend
git worktree add ../backend feature/backend
git worktree add ../tests feature/tests

# 在不同窗口运行 Claude Code
# Terminal 1: cd ../frontend && claude
# Terminal 2: cd ../backend && claude
# Terminal 3: cd ../tests && claude

# 完成后合并
git worktree remove ../frontend
git worktree remove ../backend
git worktree remove ../tests
```

---

## 📊 Context 管理

### 三层上下文模型

| 层级 | 内容 | 生命周期 | 管理策略 |
|------|------|---------|---------|
| **System** | Claude Code 核心指令 | 永久 | 不动 |
| **Project** | CLAUDE.md + Skills | 项目级 | 精心设计 |
| **Session** | 对话历史 | 会话级 | 保持简洁 |

### CLAUDE.md 最佳实践

```markdown
# Project: E-commerce Platform

## Tech Stack
- Backend: FastAPI + SQLAlchemy
- Frontend: React + TypeScript
- Database: PostgreSQL
- Cache: Redis

## Architecture
- Monorepo structure
- API-first design
- Event-driven for async tasks

## Coding Standards
- Use async/await for all I/O
- Type hints required
- Test coverage > 80%
- Follow PEP 8

## Key Files
- `src/main.py`: API entry point
- `src/models/`: Database models
- `src/services/`: Business logic
- `tests/`: Test suite

## Common Tasks
1. Adding new API: Copy `templates/api_template.py`
2. Adding new model: Copy `templates/model_template.py`
3. Running tests: `pytest tests/ -v`

## Gotchas
- Redis connection string in `.env`
- Migration required for schema changes
- Use `async_session` for database operations
```

### Context 清理策略

```
1. 开始新任务 → 新建会话
2. 完成大任务 → 新建会话
3. 上下文膨胀 → 总结后新建会话
4. 跨项目工作 → 一定是新会话

原则: Fresh context > bloated context
```

---

## 🎯 实战练习

### 练习 1: 工具调用链

```
任务: 添加一个用户注册 API

要求:
1. 使用四层调用链
   - READ: 理解现有代码
   - WRITE: 创建 API
   - WRITE: 创建测试
   - RUN: 运行测试

2. 输出每一步的思考过程

时间: 30 分钟
```

### 练习 2: Skill 设计

```
任务: 为"代码审查"创建 Skill

要求:
1. 创建目录结构
2. 编写 SKILL.md（使用标准模板）
3. 创建 references/review-checklist.md
4. 优化 description 为触发器格式

时间: 30 分钟
```

### 练习 3: 并行工作

```
任务: 用 3 个实例并行开发功能

要求:
1. 创建 3 个 git worktree
2. 主窗口协调，3 个子窗口并行工作
3. 最后合并代码

时间: 45 分钟
```

---

## ✅ 课程检查清单

### 模块 1: 核心工具

- [ ] 理解四种核心能力
- [ ] 掌握工具调用机制
- [ ] 理解安全边界
- [ ] 完成 1 次完整调用链

### 模块 2: 高级功能

- [ ] 理解 Skill 系统
- [ ] 能创建简单 Skill
- [ ] 理解 MCP 架构
- [ ] 理解 Sub-Agents
- [ ] 能配置简单 Hook

### 模块 3: 提示词工程

- [ ] 掌握 System Prompt 标准结构
- [ ] 理解 Prompt Caching
- [ ] 能编写 5 层结构提示词
- [ ] 完成 1 个完整提示词

### 模块 4: 实战工作流

- [ ] 理解 Meta 工程师工作流
- [ ] 能使用 git worktree 并行工作
- [ ] 掌握 Context 管理策略
- [ ] 完成 1 次并行工作实践

---

# 模块 5: 高级技巧（Tw93 洞察）

## 🔇 Tool Output 噪声问题

### 问题场景

```
# Claude 看到的原始输出
running 262 tests
test auth::test_login ... ok
test auth::test_logout ... ok
test auth::test_register ... ok
...（继续几千行）

# 这几千行挤掉的是：
- 对话历史（你之前说的需求）
- 文件内容（你真正需要参考的代码）
- Claude 的推理空间
```

### 关键洞察

> **Tool Output 是上下文的隐形杀手**
> 
> cargo test、git log、find 等命令输出动辄几千行，Claude 不需要全看，但只要出现就消耗 token

### 解决方案 1: 手动截断

```bash
# 所有长输出命令都加 | head -30
cargo test 2>&1 | head -30
git log --oneline | head -30
find . -name "*.rs" | head -30
npm install 2>&1 | tail -20
```

### 解决方案 2: RTK（推荐）

> **RTK = Rust Token Killer**  
> 开源项目：https://github.com/rtk-ai/rtk  
> 支持所有语言，不只是 Rust

**工作原理**:
```
原始命令输出 → RTK Hook 拦截 → 过滤保留核心 → 返回给 Claude
```

**效果对比**:
```bash
# 走 RTK 之前（几千行）
running 262 tests
test auth::test_login ... ok
...（260 行）
test utils::test_helper ... ok

# 走 RTK 之后（1 行）
✓ cargo test: 262 passed (1 suite, 0.08s)
```

**Claude 只需要知道**:
- 过了还是挂了
- 挂在哪里
- 错误信息

---

## ⚡ Hooks 输出截断

### 问题

Hook 输出也会污染上下文：

```yaml
# ❌ 错误示例
hooks:
  - matcher: "Edit"
    pattern: "*.rs"
    hooks:
      - type: "command"
        command: "cargo check 2>&1"  # 可能几千行！
```

### 正确做法

```yaml
# ✅ 正确示例
hooks:
  - matcher: "Edit"
    pattern: "*.rs"
    hooks:
      - type: "command"
        command: "cargo check 2>&1 | head -30"  # 只留前 30 行
```

### 混合语言项目示例

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "pattern": "*.rs",
        "hooks": [
          {
            "type": "command",
            "command": "cargo check 2>&1 | head -30",
            "statusMessage": "Checking Rust..."
          }
        ]
      },
      {
        "matcher": "Edit",
        "pattern": "*.py",
        "hooks": [
          {
            "type": "command",
            "command": "python -m py_compile $FILE 2>&1 | head -20",
            "statusMessage": "Checking Python syntax..."
          }
        ]
      }
    ]
  }
}
```

**收益**: 100 次编辑，每次省 30-60 秒，累积省 **1-2 小时**

---

## 🎛️ 高频命令（工程意义）

### 上下文管理

```bash
/context   # 查看 token 占用结构
           # 排查 MCP 和文件读取占比
           # 发现隐形上下文杀手

/clear     # 清空会话
           # 同一问题被纠偏两次以上就重来
           # 保持上下文干净

/compact   # 压缩但保留重点
           # 配合 Compact Instructions 使用
           # 让 Claude 知道压缩时保留什么

/memory    # 确认哪些 CLAUDE.md 被加载
           # 避免旧规则污染新会话
```

### 能力治理

```bash
/mcp         # 管理 MCP 连接
             # 检查 token 成本
             # 断开闲置 server

/hooks       # 管理 hooks
             # 控制平面入口
             # 调试 hook 行为

/permissions # 查看权限白名单
             # 安全审计

/sandbox     # 配置沙箱隔离
             # 高自动化场景必备

/model       # 切换模型
             # Opus: 深度推理
             # Sonnet: 常规工作
             # Haiku: 快速探索
```

### 会话连续性

```bash
claude --continue            # 恢复最近会话
                             # 隔天接着做

claude --resume              # 打开选择器
                             # 恢复历史会话

claude --continue --fork     # 从已有会话分叉
                             # 同一起点不同方案

claude --worktree            # 创建隔离 git worktree
                             # 多实例并行必备

claude -p "prompt"           # 非交互模式
                             # 接入 CI / pre-commit

claude -p --output-format json  # 结构化输出
                                 # 便于脚本消费
```

### 不常见但好用

| 命令 | 用途 | 价值 |
|------|------|------|
| `/simplify` | 对刚改的代码做三维检查 | 代替手动 review |
| `/rewind` | 回到 checkpoint 重新来 | 不是"撤销" |
| `/btw` | 快速问侧问题 | 不打断主任务 |
| `/insight` | Claude 分析会话提炼沉淀 | 优化 CLAUDE.md |
| 双击 ESC | 回到上一条输入重新编辑 | 省事 |

---

## 🔄 HANDOFF.md（会话连续性）

### 问题

长会话压缩后，Claude 忘了之前做了什么

### 解决方案

开新会话前，让 Claude 写 HANDOFF.md：

```markdown
# HANDOFF.md - 当前任务交接

## 进展
- ✅ 已完成：用户认证 API
- 🔄 进行中：权限管理
- ❌ 阻塞：数据库迁移脚本

## 尝试过的方案
1. ✅ JWT 认证（已验证可行）
   - Token 过期时间 7 天
   - 使用 bcrypt 加密
2. ❌ Session 认证（性能不达标）
   - Redis 连接池太小
   - 改用 JWT
3. 🔄 RBAC 权限（正在调试）
   - 权限表设计完成
   - 角色关联待实现

## 踩过的坑
- 密码必须用 bcrypt（不是 SHA256）
- Token 过期时间 7 天（不是 24 小时）
- Redis 缓存 key 必须加前缀（避免冲突）

## 下一步
1. 完成权限管理 API
2. 添加单元测试（覆盖率 > 80%）
3. 更新 API 文档
4. 部署到测试环境验证

## 相关文件
- src/auth/ - 认证模块
- tests/test_auth.py - 测试
- docs/api.md - 文档
```

### 用法

```
1. 当前 Claude: "请写一份 HANDOFF.md 总结当前进展"
2. 快速扫一眼，有缺漏直接补
3. 开新会话: "读取 HANDOFF.md，继续之前的任务"
```

---

## 🤝 AI 审 AI（Plan Mode 进阶）

### 核心玩法

```
开两个 Claude 实例：

Claude 1（写计划）
├─ 分析需求
├─ 设计方案
└─ 生成计划文档

Claude 2（审计划）
├─ 检查逻辑漏洞
├─ 评估风险
└─ 提出改进建议

Claude 1（改计划）
├─ 根据反馈调整
└─ 确认方案
```

### 启动方式

1. 按 Shift+Tab 进入 Plan Mode
2. Claude 1 写完计划后
3. 开新 Claude 实例审查
4. 迭代优化

### 适用场景

- 复杂重构（跨模块）
- 架构迁移
- 关键功能开发
- 上线前评审

---

## ✅ 模块 5 检查清单

- [ ] 理解 Tool Output 噪声问题
- [ ] 掌握手动截断技巧
- [ ] 了解 RTK 工具
- [ ] 掌握 Hook 输出截断
- [ ] 熟悉高频命令
- [ ] 能写 HANDOFF.md
- [ ] 理解 AI 审 AI 模式

---

## 📚 扩展资源

### 官方文档

| 资源 | 链接 |
|------|------|
| Claude Code 文档 | code.claude.com/docs/zh-CN/ |
| Skills 文档 | code.claude.com/docs/zh-CN/skills |
| MCP 文档 | code.claude.com/docs/zh-CN/mcp |

### 推荐阅读

| 资源 | 说明 |
|------|------|
| Meta 工程师 50 个技巧 | 实战经验 |
| Anthropic 官方 Skilljar | 系统课程 |
| GitHub Skills 仓库 | 官方示例 |

---

## 💬 结语

### 核心认知

**Claude Code 不是对话式 AI，是 Agent 系统**

| 维度 | 对话式 AI | Agent 系统 |
|------|----------|-----------|
| **交互** | 多轮对话 | 工具调用 |
| **记忆** | 历史记录 | 结构化上下文 |
| **能力** | 文本生成 | 读写改执行 |
| **稳定性** | 不可预测 | 可设计 Skill |

### 最终目标

> **你有多少稳定流程，就能做出多少 Skill。**  
> **你踩过多少坑，就能让 Claude 少踩多少坑。**

---

**掌握工具，设计系统，提升效率！** 🚀

---

# 模块 6: 工具设计哲学

> **来源**: Thariq (Anthropic Claude Code Team) - "Seeing like an Agent"  
> **数据**: 3.8M views, 27K bookmarks  
> **重要性**: P0 - 官方权威，填补工具设计哲学空白

---

## 🎯 核心问题：如何设计 Agent 的工具集？

### 三大核心问题

```
1. 给 1 个工具还是 50 个？
   - 太少 → 能力受限
   - 太多 → 选择困难

2. 如何匹配模型能力？
   - 模型弱 → 需要更多辅助工具
   - 模型强 → 工具反而成约束

3. 如何避免工具膨胀？
   - 新功能 = 新工具？
   - 何时用 Skill 代替工具？
```

### 核心比喻：计算工具的选择

```
问题：给你一个数学难题，你需要什么工具？

方案 1: 纸笔
├─ 优势：基础、必备
├─ 劣势：手动计算受限
└─ 适用：简单问题

方案 2: 计算器
├─ 优势：计算更快
├─ 劣势：需要会操作高级功能
└─ 适用：中等复杂度

方案 3: 电脑 + 编程
├─ 优势：最强大
├─ 劣势：需要编程能力
└─ 适用：复杂问题

关键洞察：
工具要匹配使用者的能力！
```

### 映射到 Agent 世界

```
Agent 能力 ≈ 人类能力

弱模型（Claude 2）：
├─ 需要更多辅助工具
├─ 需要更明确的指令
└─ 类比：纸笔

中等模型（Claude 3.5 Sonnet）：
├─ 可以理解复杂工具
├─ 能做一些推理
└─ 类比：计算器

强模型（Claude 4）：
├─ 可以自我探索
├─ 不需要太多约束
└─ 类比：电脑 + 编程

教训：
随着模型进化，工具也需要演进！
```

---

## 🔄 三大演进模式

### 模式 1: 工具迭代模式

**案例：AskUserQuestion 的三次迭代**

#### Attempt #1: 修改 ExitPlanTool ❌

```python
# 失败方案
class ExitPlanTool:
    def __init__(self):
        self.plan = None
        self.questions = []  # ← 新增参数

# 问题：
1. 混淆了"计划"和"提问"
2. 模型不知道先做哪个
3. 用户回答可能和计划冲突
```

**教训 #1**: 单一职责原则 - 一个工具只做一件事

---

#### Attempt #2: 改变输出格式 ❌

```markdown
<!-- 失败方案：让 Claude 输出特殊 Markdown -->
## 计划
1. 步骤 1
2. 步骤 2

## 问题
- [A] 问题 1 (选项 a | 选项 b)
- [B] 问题 2 (是 | 否)

<!-- 问题：
1. Claude 不一定遵守格式
2. 会追加额外句子
3. 会省略选项
4. 会用不同的格式
-->
```

**教训 #2**: 不要强行扭曲模型输出 - 工具调用比文本格式更可靠

---

#### Attempt #3: 独立的 AskUserQuestion 工具 ✅

```python
# 成功方案
class AskUserQuestion:
    """
    让 Claude 向用户提问的结构化工具
    
    Args:
        questions: 问题列表
          - question: 问题文本
          - options: 选项列表
          - required: 是否必答
    
    Returns:
        用户答案列表
    """
    def execute(self, questions: list) -> list:
        # 显示模态框
        # 阻塞 Agent 循环
        # 返回用户答案
```

**为什么成功？**

| 因素 | 说明 |
|------|------|
| **结构化输出** | 强制 Claude 遵守格式 |
| **独立工具** | 不混淆职责 |
| **可组合** | 可以在 Skill 中引用 |
| **模型喜欢** | Claude 自然地会用 |

**教训 #3**: 工具设计要符合模型习惯 - 观察模型输出，设计它喜欢用的工具

---

### 模式 2: 能力进化模式

**案例：Todos → Tasks 的演进**

#### Phase 1: TodoWrite + 系统提醒（模型弱时）

```python
# 早期方案（Claude 2 时代）
class TodoWrite:
    """写待办列表"""

# 问题：Claude 会忘记
# 解决：每 5 次工具调用提醒一次

# 系统提示词
"""
每 5 次工具调用后：
"记住你的待办列表：
1. ✅ 完成 A
2. ⬜ 做完 B
3. ⬜ 完成 C"
"""
```

**效果**: 帮助弱模型保持聚焦

---

#### Phase 2: 模型进化后发现新问题

```
问题：提醒反而限制了模型

症状：
1. Claude 觉得必须严格按列表执行
2. 不敢调整计划
3. Sub-Agents 无法共享待办

原因：
模型能力强了，不需要约束
约束变成了负担
```

**教训**: **随着模型能力提升，曾经需要的工具可能变成约束**

---

#### Phase 3: Task Tool（模型强时）

```python
# 现代方案（Claude 4 时代）
class Task:
    """
    任务协调工具（不是待办列表）
    
    特点：
    1. 支持依赖关系
    2. 跨 Sub-Agents 共享
    3. 模型可以修改/删除
    4. 强调协作而非约束
    """

# 用法
task = Task.create(
    name="实现用户认证",
    dependencies=["数据库设计"],
    assigned_to="auth-agent"
)

# Sub-Agent 可以：
# - 查看任务
# - 更新状态
# - 创建子任务
# - 协调依赖
```

**对比**:

| 维度 | Todos (Phase 1) | Tasks (Phase 3) |
|------|----------------|-----------------|
| **定位** | 约束模型 | 帮助协作 |
| **灵活性** | 固定列表 | 动态调整 |
| **跨 Agent** | ❌ 不支持 | ✅ 共享 |
| **适用模型** | 弱模型 | 强模型 |

---

### 模式 3: 上下文构建模式

**案例：搜索能力的演进**

#### RAG（被动接收）

```
初期方案（Claude 2）：

1. 预先索引代码库
2. 向量数据库存储
3. 查询时检索相关片段
4. 塞给 Claude

问题：
- 需要索引（环境复杂）
- 脆弱（不同环境表现不一致）
- Claude 被动接收（不知道还有没有）
```

---

#### Grep（主动探索）

```
进化方案（Claude 3）：

1. 给 Claude Grep 工具
2. Claude 自己搜索
3. 自己构建上下文

优势：
- 不需要索引
- Claude 主动探索
- 知道"还有什么没看"
```

**教训**: **模型从"被动接收"到"主动探索"**

---

#### Progressive Disclosure（分层探索）

```
现代方案（Claude 4）：

Skill 架构：
my-skill/
├── SKILL.md           # 第一层：概览
│   └─ 引用 → references/api.md
│       └─ 引用 → references/examples.md
│           └─ 引用 → assets/templates/

Claude 的探索路径：
1. 读取 SKILL.md（300 行）
2. 发现需要更多细节
3. 读取 references/api.md
4. 发现需要示例
5. 读取 references/examples.md
6. 递归探索直到满足

优势：
- 按需加载（节省 token）
- Claude 掌握主动权
- 可以无限扩展
```

**对比**:

| 方案 | Claude 的角色 | Token 成本 |
|------|--------------|-----------|
| RAG | 被动接收 | 高（全塞进去） |
| Grep | 主动搜索 | 中（可能搜太多） |
| Progressive Disclosure | 智能探索 | 低（按需加载） |

---

## 🎯 避免工具膨胀

### 工具数量阈值

```
Anthropic 官方建议：
Claude Code 当前 ~20 个工具

新增工具的门槛很高，因为：
每个新工具 = 模型多一个选择 = 思考成本增加
```

### 判断标准：新增工具 vs 用 Skill 代替

```
决策树：

新需求
├─ 是核心能力吗？
│   ├─ 是 → 新增工具
│   └─ 否 → 用 Skill 代替
│
├─ 需要经常用吗？（>50% 会话）
│   ├─ 是 → 考虑工具
│   └─ 否 → 用 Skill
│
└─ 能用 Progressive Disclosure 吗？
    ├─ 能 → 用 Skill + 分层文件
    └─ 不能 → 考虑工具
```

### 案例：Claude Code Guide Agent

**问题**: 如何让 Claude Code 了解自己？

```
用户问："MCP 是什么？"
Claude 答："不知道"
```

**方案对比**:

| 方案 | 实现 | 问题 |
|------|------|------|
| 系统提示词 | 把文档塞进 prompt | Context rot（很少用但占 token） |
| 文档链接 | 给 Claude 文档 URL | Claude 加载太多结果 |
| **Guide Subagent** ✅ | 专门的搜索 Agent | 精准、按需、不膨胀 |

**Guide Agent 工作流程**:

```
1. Claude 发现用户问 Claude Code 本身
2. 调用 Guide Subagent（独立上下文）
3. Subagent 搜索文档
4. 返回精准答案（不是全部文档）
5. 主 Claude 总结给用户

优势：
- 不增加工具数量
- 不污染主上下文
- 可以无限扩展文档
```

---

## 👁️ See Like an Agent

### 核心方法论

> **设计工具不是科学，是艺术**
> 
> 取决于：
> - 你用的模型
> - Agent 的目标
> - 运行环境

### 四步循环

```
┌─────────────────────────────────────────────┐
│           See Like an Agent                 │
├─────────────────────────────────────────────┤
│                                             │
│  1. 观察输出                                │
│     └─ 读 Claude 的输出                    │
│        理解它的思维过程                     │
│                                             │
│  2. 发现问题                                │
│     └─ 哪里卡住了？                         │
│        哪里重复犯错？                       │
│        哪里效率低？                         │
│                                             │
│  3. 实验新方案                              │
│     └─ 工具迭代                             │
│        调整提示词                           │
│        改变架构                             │
│                                             │
│  4. 评估效果                                │
│     └─ 更好了吗？                           │
│        有新问题吗？                         │
│        需要继续调整吗？                     │
│                                             │
└─────────────────────────────────────────────┘
           ↓
        循环继续
```

### 关键原则

```
1. 实验，不要理论
   - 理论推测不可靠
   - 看实际输出
   - 多尝试不同方案

2. 读输出，不要假设
   - Claude 的输出是金矿
   - 能告诉你它怎么思考
   - 能告诉你哪里困惑

3. 随模型进化调整
   - 今天最优 ≠ 明天最优
   - 模型强了，工具要改
   - 定期重新评估

4. 保持简单
   - 能用 Skill 就不新增工具
   - 能用 Progressive Disclosure 就不膨胀
   - Less is more
```

---

## 📋 实战检查清单

### 设计新工具时

- [ ] **真的需要新工具吗？**
  - 能用 Skill 代替吗？
  - 能用 Progressive Disclosure 吗？
  - 使用频率 > 50% 吗？
  
- [ ] **工具设计合理吗？**
  - 单一职责吗？
  - 符合模型习惯吗？
  - 结构化输出吗？

- [ ] **考虑模型能力了吗？**
  - 当前模型是弱/中/强？
  - 工具是辅助还是约束？
  - 未来模型进化后还需要吗？

### 迭代现有工具时

- [ ] **观察模型输出**
  - 哪里卡住了？
  - 哪里重复犯错？
  - 哪里效率低？

- [ ] **实验新方案**
  - 尝试不同设计
  - A/B 测试
  - 记录效果

- [ ] **随模型进化**
  - 定期重新评估
  - 移除过时工具
  - 调整约束强度

---

## 🎓 实战练习

### 练习 1: 工具迭代

```
场景：你发现 Claude 在执行任务时
经常忘记问用户关键信息

任务：
1. 设计一个 AskUserQuestion 工具
2. 尝试 3 种不同实现
3. 对比哪种效果最好

时间：30 分钟
```

### 练习 2: 能力进化

```
场景：你的团队从 Claude 3.5 升级到 Claude 4

任务：
1. 检查现有工具是否有约束
2. 识别可以移除的辅助
3. 设计更适合强模型的工具

时间：30 分钟
```

### 练习 3: Progressive Disclosure

```
场景：你有一个大型 API 文档（500KB）

任务：
1. 设计 Progressive Disclosure 架构
2. 创建分层文件结构
3. 编写 SKILL.md 引导 Claude

时间：30 分钟
```

---

## 💡 关键洞察总结

### 三大教训

```
1. 工具迭代是常态
   - AskUserQuestion 三次迭代
   - 不要指望一次做对
   - 观察、实验、调整

2. 模型进化要跟进
   - Todos → Tasks 的演进
   - 昨天的辅助可能是今天的约束
   - 定期重新评估

3. 避免工具膨胀
   - ~20 个工具阈值
   - 用 Skill + Progressive Disclosure 代替
   - Less is more
```

### 最终建议

> **Experiment often, read your outputs, try new things.**
> 
> **See like an agent.**
> 
> — Thariq, Anthropic Claude Code Team

---

## 📚 扩展阅读

| 资源 | 链接 | 说明 |
|------|------|------|
| 原文 | https://x.com/trq212/status/2027463795355095314 | Thariq 官方文章 |
| Claude Code 文档 | code.claude.com/docs | 官方文档 |
| Prompt Caching 文章 | https://x.com/trq212/status/2024574133011673516 | 相关技术 |
| Tasks 文章 | https://x.com/trq212/status/2014480496013803643 | Task 工具详解 |

---

## ✅ 模块 6 检查清单

- [ ] 理解工具设计的三大核心问题
- [ ] 掌握工具迭代模式（AskUserQuestion 案例）
- [ ] 理解能力进化模式（Todos → Tasks）
- [ ] 理解上下文构建模式（RAG → Progressive Disclosure）
- [ ] 掌握避免工具膨胀的方法
- [ ] 理解 "See Like an Agent" 方法论
- [ ] 能应用四步循环优化工具
- [ ] 完成 1 个工具迭代练习

---

**掌握工具设计哲学，让 Agent 更强大！** 🎯

---

## 📝 更新日志

| 日期 | 变更 |
|------|------|
| 2026-03-22 | 新增模块 6：工具设计哲学（Thariq 文章） |
| 2026-03-21 | 初始版本，四大核心能力 + 高级功能 + 工作流 |
