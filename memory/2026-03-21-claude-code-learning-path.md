# 🎓 Claude Code 完整学习路线设计

> **目标**: 从零基础到团队落地，打造完整的学习体系  
> **总时长**: 4-6 周（根据团队节奏调整）  
> **受众**: 开发、测试、产品经理

---

## 📊 学习路线总览

```
阶段 1: 入门基础 (Week 1)
├─ 安装配置
├─ 核心概念
└─ 第一个项目

阶段 2: 核心技能 (Week 2)
├─ 上下文管理
├─ 代码修改
└─ 自定义命令

阶段 3: 高级功能 (Week 3)
├─ MCP 服务器
├─ GitHub 集成
└─ Hooks 机制

阶段 4: Skill 开发 (Week 4)
├─ 5 种设计模式
├─ 9 种类型分类
└─ Gotchas + Memory + Hooks

阶段 5: 角色化应用 (Week 5)
├─ 开发者专场
├─ 测试工程师专场
└─ 产品经理专场

阶段 6: 团队落地 (Week 6)
├─ 最佳实践分享
├─ Skill 库建设
└─ 持续优化机制
```

---

## 阶段 1: 入门基础 (Week 1)

### 📚 学习资源

| 资源 | 链接 | 时长 |
|------|------|------|
| **官方中文文档 - 概述** | code.claude.com/docs/zh-CN/ | 30 min |
| **实战课程 01-04 章** | cholf5.com/claude-code-in-action | 2 h |
| **视频教程** | YouTube + longcut.ai | 1 h |

### 🎯 学习目标

1. **理解 Claude Code 是什么**
   - 编码助手 vs 对话式 AI
   - 核心能力：读代码、写代码、改代码、跑命令
   - 与 GitHub Copilot / Cursor 的区别

2. **完成安装配置**
   - macOS / Windows / Linux 安装
   - API Key 配置
   - 权限设置

3. **运行第一个项目**
   - 创建简单项目（如待办事项应用）
   - 理解 "信任目录" 概念
   - 体验基本工作流

### 📝 实战练习

**练习 1.1: 安装验证**
```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version

# 首次启动
claude
```

**练习 1.2: 第一个项目**
```
任务: 用 Claude Code 创建一个简单的 Python 计算器

要求:
1. 支持 +、-、*、/ 四则运算
2. 有简单的错误处理
3. 包含单元测试
4. 生成 README.md

时间: 30 分钟
```

### ✅ 阶段检查

- [ ] 能解释 Claude Code 的核心能力
- [ ] 成功安装并启动 Claude Code
- [ ] 完成第一个小项目
- [ ] 理解"信任目录"概念

---

## 阶段 2: 核心技能 (Week 2)

### 📚 学习资源

| 资源 | 链接 | 时长 |
|------|------|------|
| **实战课程 05-07 章** | cholf5.com | 3 h |
| **实战课程 09-10 章** | cholf5.com | 2 h |
| **官方文档 - Skills** | code.claude.com/docs/zh-CN/skills | 1 h |

### 🎯 学习目标

1. **上下文管理**
   - 理解 Claude 的"记忆"机制
   - CLAUDE.md 文件的作用
   - 如何添加/移除上下文
   - 控制上下文大小

2. **代码修改**
   - 理解 Claude 的修改策略
   - 大改动 vs 小改动
   - 如何审查 Claude 的修改
   - 撤销和回滚

3. **自定义命令**
   - 创建常用命令别名
   - 工作流自动化
   - 团队命令共享

### 📝 实战练习

**练习 2.1: 上下文管理**
```
场景: 你有一个中型 Python 项目（~5000 行代码）

任务:
1. 让 Claude 理解项目结构（创建 CLAUDE.md）
2. 添加关键文件的上下文
3. 控制上下文大小在合理范围
4. 测试 Claude 是否理解项目

时间: 45 分钟
```

**练习 2.2: 代码修改**
```
场景: 重构一个遗留模块

任务:
1. 让 Claude 分析代码问题
2. 生成重构计划
3. 逐步执行修改
4. 运行测试验证

时间: 1 小时
```

**练习 2.3: 自定义命令**
```bash
# 创建常用命令
claude config set alias.review "review the last commit"
claude config set alias.test "run all tests and show coverage"
claude config set alias.deploy "build and deploy to staging"
```

### ✅ 阶段检查

- [ ] 能创建和管理 CLAUDE.md
- [ ] 理解上下文大小控制
- [ ] 能审查 Claude 的修改
- [ ] 创建至少 3 个自定义命令

---

## 阶段 3: 高级功能 (Week 3)

### 📚 学习资源

| 资源 | 链接 | 时长 |
|------|------|------|
| **实战课程 11-12 章** | cholf5.com (MCP + GitHub) | 2 h |
| **实战课程 13-18 章** | cholf5.com (Hooks) | 3 h |
| **官方文档 - MCP** | code.claude.com/docs/zh-CN/mcp | 1 h |

### 🎯 学习目标

1. **MCP 服务器**
   - 理解 MCP 架构
   - 连接外部工具（数据库、API）
   - 创建自定义 MCP 服务器

2. **GitHub 集成**
   - PR 创建和管理
   - Issue 自动化
   - CI/CD 集成

3. **Hooks 机制**
   - 理解 Hooks 类型
   - PreToolUse / PostToolUse
   - 常见坑点（Gotchas）
   - 实用 Hooks 配置

### 📝 实战练习

**练习 3.1: GitHub 集成**
```
任务: 用 Claude Code 完成 PR 工作流

1. 创建新分支
2. 开发一个功能
3. 创建 PR（包含描述、标签）
4. 回复 PR review comments
5. Merge PR

时间: 45 分钟
```

**练习 3.2: 实现一个 Hook**
```yaml
# 任务: 创建一个阻止危险命令的 Hook

# .claude/hooks/pre-tool-use.yaml
hooks:
  - match: "rm -rf /"
    action: block
    message: "❌ 禁止删除根目录"
  
  - match: "DROP TABLE"
    action: confirm
    message: "⚠️ 确认删除表？"
```

**练习 3.3: 实用 Hooks**
```yaml
# 任务: 配置常用 Hooks

# 自动添加 TODO 注释
hooks:
  - match: "TODO|FIXME"
    action: notify
    message: "发现待办事项"

# 自动运行测试
hooks:
  - match: "\\.test\\.ts$"
    action: run
    command: "npm test -- {{file}}"
```

### ✅ 阶段检查

- [ ] 能连接至少 1 个 MCP 服务器
- [ ] 完成 PR 创建和管理流程
- [ ] 配置至少 3 个实用 Hooks
- [ ] 理解 Hooks 常见坑点

---

## 阶段 4: Skill 开发 (Week 4)

### 📚 学习资源

| 资源 | 链接 | 时长 |
|------|------|------|
| **5 种设计模式** | 我们的培训材料 | 2 h |
| **9 种 Skill 类型** | memory/2026-03-21-claude-skills-best-practices.md | 2 h |
| **官方 Skills 示例** | github.com/anthropics/skills | 1 h |

### 🎯 学习目标

1. **理解 5 种设计模式**
   - 工具封装（Tool Wrapper）
   - 生成器（Generator）
   - 审查器（Reviewer）
   - 反转（Inversion）
   - 流水线（Pipeline）

2. **掌握 9 种 Skill 类型**
   - Library & API Reference
   - Product Verification
   - Data Fetching & Analysis
   - Business Process Automation
   - Code Scaffolding
   - Code Quality & Review
   - CI/CD & Deployment
   - Runbooks
   - Infrastructure Operations

3. **Skill 高级功能**
   - Gotchas（踩坑清单）
   - Memory（记忆机制）
   - On Demand Hooks

### 📝 实战练习

**练习 4.1: 创建工具封装 Skill**
```
任务: 为团队内部 API 创建 Skill

要求:
1. SKILL.md（<100 行）
2. references/api-spec.md（API 规范）
3. references/gotchas.md（踩坑清单）
4. 完整的 description 触发器

模式: Tool Wrapper
类型: Library & API Reference
```

**练习 4.2: 创建流水线 Skill**
```
任务: 创建文档生成流水线

流程:
1. 解析代码
2. 提取 API
3. 生成文档字符串（用户确认）
4. 组装文档
5. 质量检查

模式: Pipeline
类型: Code Scaffolding
```

**练习 4.3: 实现记忆机制**
```python
# 任务: 为 Skill 添加记忆功能

# scripts/session-history.json
{
  "sessions": [
    {
      "id": "abc123",
      "task": "Build feature X",
      "gotchas_encountered": ["需要 PTY", "需要 git repo"],
      "lessons_learned": ["使用 --full-auto"]
    }
  ]
}

# 在 SKILL.md 添加：
每次启动时读取 session-history.json
每次完成后更新 session-history.json
```

### ✅ 阶段检查

- [ ] 能区分 5 种设计模式
- [ ] 创建至少 2 个不同类型的 Skill
- [ ] 为 Skill 添加 Gotchas 和 Memory
- [ ] 优化 description 字段为触发器

---

## 阶段 5: 角色化应用 (Week 5)

### 👨‍💻 开发者专场 (Day 1-2)

**学习资源**: 培训材料模块二（开发者部分）

**实战场景**:
1. **代码理解**: 快速理解陌生代码库
2. **功能开发**: 搭建新功能脚手架
3. **重构优化**: 重构遗留代码
4. **调试排错**: 定位和修复 Bug

**练习**:
```
场景: 接手一个 5000 行的 Python 项目

任务:
1. 用 Claude 生成"30 分钟快速上手指南"
2. 添加一个新 API 端点（含测试）
3. 重构一个复杂函数（降低圈复杂度）
4. 修复一个隐蔽的 Bug

时间: 4 小时
输出: 3 个 Skills（项目专家、API 生成器、重构审查器）
```

---

### 🧪 测试工程师专场 (Day 3-4)

**学习资源**: 培训材料模块二（测试部分）

**实战场景**:
1. **用例生成**: 从需求文档生成测试用例
2. **边界测试**: 自动生成边界值
3. **回归测试**: E2E 测试自动化
4. **测试报告**: 生成结构化报告

**练习**:
```
场景: 为用户注册 API 创建测试套件

任务:
1. 生成单元测试（正常 + 边界 + 异常）
2. 生成 E2E 测试（Playwright）
3. 配置失败时录制视频
4. 生成测试覆盖率报告

时间: 3 小时
输出: 2 个 Skills（测试生成器、E2E 自动化）
```

---

### 📊 产品经理专场 (Day 5)

**学习资源**: 培训材料模块二（产品部分）

**实战场景**:
1. **需求收集**: 用反转模式收集需求
2. **原型生成**: PRD 转原型
3. **逻辑验证**: 业务逻辑决策树
4. **文档生成**: 批量生成多格式文档

**练习**:
```
场景: "用户偏好设置"功能

任务:
1. 用反转模式收集需求（6 个问题）
2. 生成信息架构图
3. 生成可交互 HTML 原型
4. 生成全套文档（功能说明 + 用户手册 + FAQ）

时间: 3 小时
输出: 3 个 Skills（需求收集器、原型生成器、文档生成器）
```

---

### ✅ 阶段检查

- [ ] 每个角色完成至少 2 个专属 Skills
- [ ] Skills 通过团队评审
- [ ] Skills 已添加到团队库

---

## 阶段 6: 团队落地 (Week 6)

### 📚 学习资源

| 资源 | 内容 |
|------|------|
| **最佳实践分析** | memory/2026-03-21-claude-skills-best-practices.md |
| **官方 Tips** | 10 大 Skill 设计铁律 |
| **团队分享** | 每人分享 1-2 个最佳实践 |

### 🎯 目标

1. **Skill 库建设**
   - 整理团队已创建的 Skills
   - 按类型分类
   - 建立 Marketplace 机制

2. **最佳实践固化**
   - 总结踩坑经验
   - 更新 Gotchas
   - 建立 Memory 机制

3. **持续优化机制**
   - 每周 Skill 评审
   - 使用情况统计（Measuring）
   - 迭代优化流程

### 📝 实战练习

**练习 6.1: 建立 Skill Marketplace**
```
目录结构:
skills/
├── marketplace/        # 经过验证的 Skills
│   ├── api-expert/
│   ├── test-generator/
│   └── doc-generator/
├── sandbox/           # 实验性 Skills
└── archive/           # 已废弃的 Skills

流程:
1. 在 sandbox/ 创建新 Skill
2. 团队试用 1 周
3. 通过评审后移至 marketplace/
4. 不再使用移至 archive/
```

**练习 6.2: 实施 Measuring**
```python
# 任务: 统计 Skill 使用情况

# scripts/log_skill_usage.py
import json
from datetime import datetime

def log_usage(skill_name, tool_name):
    record = {
        "skill": skill_name,
        "tool": tool_name,
        "timestamp": datetime.now().isoformat()
    }
    # 写入数据库或 JSON 文件

# 每周生成报告
# 发现从不使用的 Skills → 删除或改进
# 发现高频 Skills → 重点优化
```

**练习 6.3: 持续优化流程**
```markdown
# 团队 Skill 优化流程

## 每周
- [ ] 查看 Measuring 报告
- [ ] 识别需要优化的 Skills
- [ ] 收集新的踩坑经验

## 每月
- [ ] 评审所有 Skills 的 Gotchas
- [ ] 更新 Memory 数据
- [ ] 清理不再使用的 Skills

## 每季度
- [ ] 对标最新最佳实践
- [ ] 识别缺失的 Skill 类型
- [ ] 团队培训升级
```

### ✅ 最终检查

- [ ] 团队 Skill 库建立完成
- [ ] 至少 10 个高质量 Skills
- [ ] Measuring 机制上线
- [ ] 持续优化流程文档化
- [ ] 所有成员掌握 Skill 开发方法

---

## 📊 学习资源汇总

### 官方资源

| 资源 | 链接 | 说明 |
|------|------|------|
| **官方中文文档** | code.claude.com/docs/zh-CN/ | 最权威，反复精读 |
| **实战课程（中文）** | cholf5.com/claude-code-in-action | 21 章完整课程 |
| **Skilljar 原课程** | anthropic.skilljar.com | 官方视频 + 交互 |
| **YouTube 频道** | Anthropic YouTube | 英文视频教程 |
| **示例 Skills** | github.com/anthropics/skills | 官方 Skill 仓库 |

### 我们的资源

| 资源 | 位置 | 说明 |
|------|------|------|
| **培训手册** | memory/2026-03-21-claude-code-training.md | 5 种设计模式 + 角色化应用 |
| **最佳实践** | memory/2026-03-21-claude-skills-best-practices.md | 9 种类型 + 10 大 Tips |
| **提示词分析** | memory/2026-03-05-claude-code-prompt-analysis.md | 官方提示词设计模式 |
| **学习路线** | 本文档 | 完整学习路径 |

### 辅助工具

| 工具 | 用途 |
|------|------|
| **longcut.ai** | 翻译英文视频 |
| **NotebookLM** | 生成播客/测验/幻灯片 |
| **ClawHub** | 发现新 Skills |

---

## 🎯 培训后行动清单

### 立即行动（本周）
- [ ] 完成 Week 1 入门课程
- [ ] 安装 Claude Code
- [ ] 完成第一个小项目
- [ ] 加入团队学习群

### 本月内
- [ ] 完成阶段 1-3
- [ ] 创建第一个 Skill
- [ ] 在团队中分享经验

### 持续优化
- [ ] 每周学习 1 个新场景
- [ ] 每月创建 1 个新 Skill
- [ ] 每季度对标最佳实践

---

## 📈 预期效果

### 个人能力提升

| 能力 | 提升前 | 提升后 | 提升 |
|------|--------|--------|------|
| **代码理解速度** | 2h/模块 | 30min/模块 | 4x |
| **测试用例生成** | 4h/功能 | 30min/功能 | 8x |
| **文档生成** | 2h/功能 | 5min/功能 | 24x |
| **Bug 修复** | 4h/bug | 1h/bug | 4x |

### 团队效率提升

| 指标 | 提升前 | 提升后 |
|------|--------|--------|
| **测试自动化率** | 60% | 90% |
| **代码审查一致性** | 50% | 95% |
| **新人上手速度** | 2 周 | 3 天 |
| **知识复用率** | 20% | 80% |

---

## 💬 结语

**学习 Claude Code 不是终点，而是起点。**

> Skill = 把你平时怎么干活，固化成 Claude 可复用的能力模块

**你有多少稳定流程，就能做出多少 Skill。**  
**你踩过多少坑，就能让 Claude 少踩多少坑。**

本质上，你是在把自己训练成一个可以复制的 AI 工作流系统。

---

**开始你的学习之旅吧！** 🚀

---

## 📝 更新日志

| 日期 | 变更 |
|------|------|
| 2026-03-21 | 初始版本，设计 6 阶段学习路线 |
