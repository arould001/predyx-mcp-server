# Claude Code 提示词分析（2026-03-05）

## 背景
Steven 要求分析 Claude Code 的项目文件，找到可能的提示词。

## 文件位置
- Agent 设计模式: `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/agent-development/`
- Superpowers 插件: `~/.claude/plugins/cache/superpowers-marketplace/superpowers/4.1.1/`

## 核心发现

### 1. System Prompt 标准结构
```markdown
You are [角色] specializing in [领域].

**Your Core Responsibilities:**
1. [主要职责]

**Process:**
1. [具体步骤]

**Quality Standards:**
- [标准]

**Output Format:**
- [格式]

**Edge Cases:**
- [边界情况]
```

### 2. Subagent-Driven Development
- **流程**: Implementer → Spec Reviewer → Code Quality Reviewer
- **双阶段审查**: 
  1. Spec Compliance（是否做了要求的）
  2. Code Quality（是否做得好）
- **关键**: 每个 task 用全新 subagent，避免上下文污染

### 3. TDD 铁律
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```
- 必须看到测试失败（Verify RED）
- 必须看到测试通过（Verify GREEN）
- 先写代码再写测试 = 什么都没证明

### 4. Agent 创建系统
- Extract Core Intent
- Design Expert Persona
- Architect Comprehensive Instructions
- Optimize for Performance
- Create Identifier
- Include Examples

### 5. Code Reviewer 职责
1. Plan Alignment Analysis
2. Code Quality Assessment
3. Architecture Review
4. Documentation Check
5. Issue Identification (Critical/Important/Minor)
6. Communication Protocol

## 对 OpenClaw 的启示

### 可直接应用
1. System Prompt 标准模板
2. 双阶段审查机制
3. TDD 强制流程
4. Agent 生成流程

### 建议实施
1. 主 Agent 使用标准结构
2. Subagent 架构（实现 + 审查）
3. 审查机制（规格 + 质量）
4. 触发条件 + 示例

## 关键文件清单
- `system-prompt-design.md` - System prompt 设计模式
- `agent-creation-system-prompt.md` - Agent 生成系统提示
- `subagent-driven-development/SKILL.md` - Subagent 驱动开发
- `test-driven-development/SKILL.md` - TDD 铁律
- `implementer-prompt.md` - 实现 subagent 提示
- `spec-reviewer-prompt.md` - 规格审查提示
- `code-quality-reviewer-prompt.md` - 代码质量审查提示
- `code-reviewer.md` - Code reviewer agent

## 下一步
- [ ] 为 OpenClaw 设计类似的 System Prompt 模板
- [ ] 实现双阶段审查机制
- [ ] 创建 Agent 生成工具
- [ ] 加强 TDD 支持

---
Steven 的评价：待收集

<!-- compounded: 2026-03-06 -->
