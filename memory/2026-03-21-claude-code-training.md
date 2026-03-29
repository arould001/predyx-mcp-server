# 🚀 Claude Code Skills 培训手册：从"会用"到"专家"

> **培训目标**: 让听众在培训结束后，能立刻写出自己岗位相关的 3 个 Claude Code Skills  
> **核心认知**: Skill 不是提示词，是"可执行的小系统"

---

## 模块一：深度解析 - 5 种设计模式改变开发的本质

### 📊 先看一棵决策树

```
你的问题 → 推荐模式
├─ 如何让 Agent 掌握特定库或框架？ → 工具封装
├─ 如何确保每次输出结构一致？ → 生成器
├─ 如何自动化代码审查/安全审计？ → 审查器
├─ 如何防止 Agent 需求不明乱猜？ → 反转
└─ 如何确保复杂任务步骤完整？ → 流水线
```

---

### 模式一：工具封装（Tool Wrapper）

#### 核心价值
**传统做法**: 在系统提示里硬编码 API 规范  
**Claude Code 做法**: 打包成 Skill，按需加载

**为什么能改变开发模式？**
1. **上下文效率**: 只在真正需要时才加载（不浪费 token）
2. **知识分发**: 团队规范可以通过 Skill 统一传播
3. **专家能力瞬间复制**: 新人加载 Skill = 老专家的经验

#### 实战示例：FastAPI 开发专家

```yaml
# skills/api-expert/SKILL.md
---
name: api-expert
description: "FastAPI 开发最佳实践与规范。在构建、审查或调试 FastAPI 应用、REST API 或 Pydantic 模型时使用。"
metadata:
  pattern: tool-wrapper
  domain: fastapi
---

你是 FastAPI 开发专家。将以下规范应用于用户的代码或问题。

## 核心规范
加载 'references/conventions.md' 获取完整的 FastAPI 最佳实践列表。

## 审查代码时
1. 加载规范参考文件
2. 对照每条规范检查用户代码
3. 对于每处违规，引用具体规则并给出修复建议

## 编写代码时
1. 加载规范参考文件
2. 严格遵循每条规范
3. 为所有函数签名添加类型注解
4. 使用 Annotated 风格进行依赖注入
```

**目录结构**:
```
api-expert/
├── SKILL.md (核心指令 <100 行)
└── references/
    └── conventions.md (详细规范)
```

---

### 模式二：生成器（Generator）

#### 核心价值
**痛点**: Agent 每次生成的文档结构都不一样  
**解决方案**: 通过"填空"流程强制输出一致性

**为什么能改变开发模式？**
1. **可预测性**: 输出结构固定，适合生产环境
2. **标准化**: 团队所有文档风格统一
3. **效率**: 从 2 小时手工写报告 → 5 分钟自动生成

#### 实战示例：技术报告生成器

```yaml
# skills/report-generator/SKILL.md
---
name: report-generator
description: "生成 Markdown 格式的结构化技术报告。当用户要求撰写、创建或起草报告、摘要或分析文档时使用。"
metadata:
  pattern: generator
  output-format: markdown
---

你是一个技术报告生成器。严格按照以下步骤执行：

第一步：加载 'references/style-guide.md' 获取语气和格式规则。

第二步：加载 'assets/report-template.md' 获取所需的输出结构。

第三步：向用户询问填充模板所需的缺失信息：
- 主题或议题
- 关键发现或数据点
- 目标受众（技术人员、管理层、普通读者）

第四步：按照风格指南规则填充模板。模板中的每个章节都必须出现在输出中。

第五步：以单个 Markdown 文档的形式返回完成的报告。
```

---

### 模式三：审查器（Reviewer）

#### 核心价值
**传统做法**: 在系统提示罗列所有代码坏味道  
**Claude Code 做法**: 将检查标准模块化存储

**为什么能改变开发模式？**
1. **可替换性**: Python 风格清单 ↔ OWASP 安全清单 = 完全不同的审计工具
2. **自动化**: PR 审查、CI 门禁、上线前检查
3. **标准化**: 团队统一的审查标准

#### 实战示例：Python 代码审查器

```yaml
# skills/code-reviewer/SKILL.md
---
name: code-reviewer
description: "审查 Python 代码的质量、风格和常见 Bug。当用户提交代码请求审查、寻求代码反馈或需要代码审计时使用。"
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

你是一名 Python 代码审查员。严格遵循以下审查流程：

第一步：加载 'references/review-checklist.md' 获取完整的审查标准。

第二步：仔细阅读用户的代码。在批评之前先理解其目的。

第三步：将清单中的每条规则应用于代码。对于发现的每处违规：
- 记录行号（或大致位置）
- 分类严重程度：error（必须修复）、warning（应该修复）、info（建议考虑）
- 解释为什么这是问题，而不仅仅是说明是什么问题
- 给出包含修正代码的具体修复建议

第四步：生成包含以下章节的结构化审查报告：
- **摘要**：代码的功能描述，整体质量评估
- **发现**：按严重程度分组（先列 error，再列 warning，最后列 info）
- **评分**：1-10 分，附简短说明
- **三大建议**：最具影响力的改进措施
```

---

### 模式四：反转（Inversion）

#### 核心价值
**问题**: Agent 天生倾向于立即猜测并生成内容  
**颠覆**: 让 Agent 扮演采访者，用户回答问题

**为什么能改变开发模式？**
1. **防止幻觉**: 需求不明确时不乱猜
2. **结构化收集**: 强制收集所有必要信息
3. **质量保证**: 门控机制防止跳过关键步骤

#### 实战示例：项目规划器

```yaml
# skills/project-planner/SKILL.md
---
name: project-planner
description: "通过结构化提问收集需求，然后生成计划，从而规划新软件项目。当用户说\"我想构建\"、\"帮我规划\"、\"设计一个系统\"或\"启动新项目\"时使用。"
metadata:
  pattern: inversion
  interaction: multi-turn
---

你正在进行一次结构化需求访谈。在所有阶段完成之前，不得开始构建或设计。

## 第一阶段——问题发现（每次只问一个问题，等待每个回答）
按顺序提问，不得跳过任何问题。

- Q1："这个项目为用户解决什么问题？"
- Q2："主要用户是谁？他们的技术水平如何？"
- Q3："预期规模是多少？（每日用户数、数据量、请求频率）"

## 第二阶段——技术约束（仅在第一阶段完全回答后进行）

- Q4："你将使用什么部署环境？"
- Q5："你有技术栈要求或偏好吗？"
- Q6："有哪些不可妥协的要求？（延迟、可用性、合规性、预算）"

## 第三阶段——综合（仅在所有问题都回答后进行）

1. 加载 'assets/plan-template.md' 获取输出格式
2. 使用收集到的需求填充模板的每个章节
3. 向用户呈现完成的计划
4. 询问："这份计划是否准确反映了你的需求？你想修改什么？"
5. 根据反馈迭代，直到用户确认
```

---

### 模式五：流水线（Pipeline）

#### 核心价值
**问题**: 复杂任务的步骤容易被跳过  
**解决方案**: 强制执行带检查点的严格顺序工作流

**为什么能改变开发模式？**
1. **防跳步**: 菱形门控条件（用户确认才能进入下一阶段）
2. **可追溯**: 每个阶段的输出可验证
3. **质量保证**: 未验证的中间结果无法进入最终组装

#### 实战示例：API 文档生成流水线

```yaml
# skills/doc-pipeline/SKILL.md
---
name: doc-pipeline
description: "通过多步骤流水线从 Python 源代码生成 API 文档。当用户要求为模块编写文档、生成 API 文档或从代码创建文档时使用。"
metadata:
  pattern: pipeline
  steps: "4"
---

你正在运行一个文档生成流水线。按顺序执行每个步骤。不得跳过步骤，步骤失败时不得继续。

## 第一步——解析与清点
分析用户的 Python 代码，提取所有公开的类、函数和常量。以清单形式呈现清点结果。询问："这是你想要文档化的完整公开 API 吗？"

## 第二步——生成文档字符串
对于每个缺少文档字符串的函数：
- 加载 'references/docstring-style.md' 获取所需格式
- 严格按照风格指南生成文档字符串
- 逐一呈现生成的文档字符串供用户确认

在用户确认之前，不得进入第三步。

## 第三步——组装文档
加载 'assets/api-doc-template.md' 获取输出结构。将所有类、函数和文档字符串编译成单一的 API 参考文档。

## 第四步——质量检查
对照 'references/quality-checklist.md' 进行审查：
- 每个公开符号都已文档化
- 每个参数都有类型和描述
- 每个函数至少有一个使用示例

报告结果。在呈现最终文档之前修复所有问题。
```

---

### 💡 模式组合的威力

这五种模式并不互斥，它们可以**组合使用**：

| 组合方式 | 示例 |
|---------|------|
| 流水线 + 审查器 | 文档生成流水线最后加自动审查步骤 |
| 生成器 + 反转 | 先用反转收集需求，再填模板生成文档 |
| 工具封装 + 流水线 | 每个流水线步骤加载不同的工具 Skill |

**核心原则**: 不要把复杂脆弱的指令塞进单个系统提示。拆解工作流，应用正确的结构模式。

---

## 模块二：角色化应用场景与 Skill 提炼

### 🎯 场景选择决策矩阵

| 你的角色 | 最常用模式 | 核心场景 |
|---------|-----------|---------|
| 开发 | 工具封装 + 流水线 | 代码生成、重构、架构搭建 |
| 测试 | 审查器 + 生成器 | 测试用例、边界测试、报告生成 |
| 产品 | 反转 + 生成器 | 需求收集、原型实现、文档转化 |

---

### 👨‍💻 开发者（Dev）

#### 场景一：快速理解陌生代码库
**痛点**: 接手遗留项目，文档缺失，代码晦涩

**最适合的模式**: 工具封装 + 审查器

**Skill 提炼公式**:
```
目标: 让 Agent 成为"项目专家"
需要: 
- references/architecture.md（架构说明）
- references/dependencies.md（依赖关系图）
- references/gotchas.md（历史踩坑清单）
```

**优秀提示词范例**:
```
# 示例 1: 代码理解
我需要理解这个 FastAPI 项目的架构和关键模块。

请执行以下步骤：
1. 使用 api-expert Skill 加载 FastAPI 规范
2. 分析项目入口文件，识别路由结构
3. 加载 references/architecture.md 了解分层设计
4. 为我生成一份"30 分钟快速上手指南"，包含：
   - 核心数据流
   - 关键文件职责
   - 常见坑点

# 示例 2: 重构代码
这个 legacy/auth.py 文件有 2000 行，需要拆分。

请使用 code-reviewer Skill 分析：
1. 识别职责边界（哪里是认证，哪里是授权）
2. 生成重构建议清单（按依赖关系排序）
3. 每个拆分模块的接口设计建议
4. 迁移风险评估
```

---

#### 场景二：搭建新功能脚手架
**痛点**: 每次新建 service/handler 都要复制粘贴，容易遗漏配置

**最适合的模式**: 流水线

**Skill 提炼公式**:
```
目标: 标准化的新建流程
需要:
- assets/service-template/（模板目录）
- references/checklist.md（配置清单）
- scripts/validate.sh（验证脚本）
```

**优秀提示词范例**:
```
# 示例 1: 新建微服务
我需要创建一个新的 payment-service。

请使用 service-creator Skill 执行流水线：
1. 询问我需要的端点
2. 询问数据库 schema 需求
3. 询问第三方集成
4. 生成目录结构 + 基础代码
5. 运行 validate.sh 检查配置完整性
6. 生成 API 文档骨架

# 示例 2: 新建 API 端点
在 user-service 中添加一个新的端点：GET /users/{id}/preferences

请使用 endpoint-creator Skill：
1. 检查是否已存在相关模型
2. 询问是否需要缓存策略
3. 询问权限控制需求
4. 生成 controller + service + repository 代码
5. 生成单元测试模板
```

---

### 🧪 测试工程师（QA）

#### 场景一：自动化测试用例生成
**痛点**: 手工写测试用例慢，边界情况容易遗漏

**最适合的模式**: 生成器 + 审查器

**Skill 提炼公式**:
```
目标: 从需求文档生成完整测试套件
需要:
- assets/test-template.md（测试用例模板）
- references/test-principles.md（测试原则）
- references/edge-cases.md（通用边界情况库）
```

**优秀提示词范例**:
```
# 示例 1: API 测试生成
为这个用户注册 API 生成测试用例：

POST /api/register
Body: { "email": string, "password": string, "name": string }

请使用 test-generator Skill：
1. 加载 references/test-principles.md
2. 分析 API 参数约束
3. 生成以下类型的测试用例：
   - 正常流程（3 种不同场景）
   - 边界测试（邮箱格式、密码长度）
   - 异常测试（重复邮箱、网络超时）
4. 为每个用例生成：
   - 描述
   - 输入数据
   - 预期输出
   - 断言点
5. 输出为 pytest 格式

# 示例 2: E2E 测试脚本
为"用户下单"流程生成 Playwright 测试脚本。

流程: 登录 → 浏览商品 → 添加购物车 → 结账 → 支付

请使用 e2e-generator Skill：
1. 询问需要测试的支付方式
2. 询问需要覆盖的异常场景（库存不足、支付失败）
3. 生成带断言的完整测试脚本
4. 添加 video recording 配置（失败时录制）
```

---

#### 场景二：回归测试自动化
**痛点**: 每次发版都要手工验证核心流程，耗时且易出错

**最适合的模式**: 流水线 + 工具封装

**Skill 提炼公式**:
```
目标: CI/CD 中自动执行回归测试
需要:
- scripts/run-core-flows.sh（核心流程测试脚本）
- references/expected-results.json（预期结果基线）
- assets/regression-report-template.md（报告模板）
```

**优秀提示词范例**:
```
# 示例: CI 回归测试
为这次 PR 创建回归测试计划。

请使用 regression-tester Skill：
1. 分析 PR 的变更文件
2. 识别受影响的核心流程
3. 生成测试矩阵：
   | 流程 | 测试脚本 | 预期结果 | 执行环境 |
4. 为每个流程生成 Playwright 测试
5. 生成 GitHub Actions workflow 配置
```

---

### 📊 产品经理（PM）

#### 场景一：需求文档转化为原型
**痛点**: PRD 写完还要找开发沟通，来回反复

**最适合的模式**: 反转 + 生成器

**Skill 提炼公式**:
```
目标: 从需求描述生成可交互原型
需要:
- references/ui-components.md（设计系统组件库）
- assets/wireframe-template.html（原型模板）
- references/interaction-patterns.md（交互模式库）
```

**优秀提示词范例**:
```
# 示例 1: PRD 转原型
我需要为"用户偏好设置"功能创建原型。

请使用 prototype-generator Skill：
1. 先问我核心问题：
   - 用户是谁？（个人/企业）
   - 偏好类型有哪些？（通知/隐私/外观）
   - 是否需要分组展示？
2. 根据我的回答生成：
   - 信息架构图
   - 页面布局草图
   - 交互流程说明
3. 输出为可运行的 HTML 原型

# 示例 2: 逻辑验证
我有一个"优惠券叠加规则"的业务逻辑，需要验证是否可行。

规则:
- 同一订单最多使用 3 张优惠券
- 满减券和折扣券可以叠加
- 但两张折扣券不能同时使用

请使用 logic-validator Skill：
1. 画一张决策树，标注所有分支
2. 列出 10 个典型场景及其结果
3. 识别潜在的逻辑冲突
4. 建议实现方案（数据库 schema + 业务规则）
```

---

#### 场景二：快速文档生成
**痛点**: 功能文档、用户手册、FAQ 都要写，重复劳动

**最适合的模式**: 生成器

**Skill 提炼公式**:
```
目标: 从代码/设计稿生成多格式文档
需要:
- assets/user-manual-template.md（用户手册模板）
- assets/faq-template.md（FAQ 模板）
- assets/changelog-template.md（更新日志模板）
- references/voice-and-tone.md（语气风格指南）
```

**优秀提示词范例**:
```
# 示例: 批量文档生成
为新功能"批量导出报表"生成全套文档。

请使用 doc-generator Skill：
1. 先问我目标受众（内部团队/外部用户）
2. 生成以下文档：
   - 功能说明文档（给开发）
   - 用户手册（给终端用户，含截图占位符）
   - FAQ（10 个常见问题）
   - 更新日志条目
3. 所有文档使用统一的语气风格
4. 输出为 Markdown，方便直接发布到知识库
```

---

## 模块三：从"对话"到"技能"的思维转变

### 🧠 核心认知升级

#### 错误思维：Claude Code = 聊天框
```
用户: "帮我写个登录功能"
Claude: [生成一段代码]
用户: "好像不对，改成..."
Claude: [重新生成]
用户: "还是不行，试试..."
Claude: [再次尝试]
```
**问题**: 每次都从零开始，不稳定，无法复用

---

#### 正确思维：Claude Code = 自动化 Agent
```
用户: "帮我写个登录功能"
Claude: [加载 login-expert Skill]
        [加载团队规范]
        [询问必要信息]
        [生成符合标准的代码]
        [运行团队审查器]
        [自动修复问题]
        [保存到历史记录]
```
**优势**: 稳定、可复用、符合团队标准

---

### 📐 提示词优化框架

#### 优秀提示词的 5 层结构

```
第 1 层：上下文（Context）
├─ "我正在做 [项目类型]"
├─ "技术栈是 [技术栈]"
└─ "目标是 [具体目标]"

第 2 层：约束条件（Constraints）
├─ "必须符合 [规范/标准]"
├─ "不能使用 [限制]"
└─ "性能要求是 [指标]"

第 3 层：输入信息（Input）
├─ "参考文件: [文件路径]"
├─ "现有代码: [代码片段]"
└─ "参考示例: [示例]"

第 4 层：期望输出（Output）
├─ "输出格式: [格式]"
├─ "包含章节: [章节列表]"
└─ "质量标准: [标准]"

第 5 层：验证方式（Validation）
├─ "请运行 [测试脚本]"
├─ "请对照 [检查清单] 审查"
└─ "请生成 [验证报告]"
```

---

#### ❌ 错误示例 vs ✅ 正确示例

| 错误做法 | 正确做法 |
|---------|---------|
| "帮我写个 API" | "为用户管理模块创建 RESTful API，遵循团队 FastAPI 规范，输出包含 controller + service + tests" |
| "优化这段代码" | "使用 performance-reviewer Skill 分析这段代码的性能瓶颈，重点关注数据库查询和缓存策略" |
| "写个测试" | "为这个登录函数生成单元测试，覆盖正常流程 + 5 种边界情况 + 3 种异常场景" |

---

#### 🎯 角色专属模板

##### 开发者模板
```markdown
# 任务: [具体任务]
## 上下文
- 项目: [项目名称]
- 技术栈: [技术栈]
- 相关文件: [文件路径]

## 要求
- 遵循: [团队规范 Skill]
- 性能要求: [指标]
- 不使用: [限制]

## 输出
- [ ] 代码实现
- [ ] 单元测试
- [ ] 文档注释

## 验证
请使用 [reviewer Skill] 检查代码质量
```

##### 测试工程师模板
```markdown
# 测试目标: [功能名称]
## 测试范围
- API: [端点列表]
- 流程: [业务流程]

## 测试类型
- [ ] 正常流程
- [ ] 边界测试
- [ ] 异常测试

## 输出格式
- 框架: [pytest/playwright]
- 断言: [断言库]

## 额外要求
- 失败时录制视频
- 生成覆盖率报告
```

##### 产品经理模板
```markdown
# 需求: [功能名称]
## 目标用户
- 角色: [用户角色]
- 场景: [使用场景]

## 核心功能
1. [功能点 1]
2. [功能点 2]
3. [功能点 3]

## 输出物
- [ ] 信息架构图
- [ ] 交互流程图
- [ ] 原型页面

## 验证
请使用 logic-validator Skill 检查业务逻辑完整性
```

---

## 🎓 实战练习：30 分钟掌握 Skill 创建

### 练习一：创建你的第一个 Skill（15 分钟）

**任务**: 创建一个"Git 提交信息生成器" Skill

**步骤**:
1. 创建目录结构：
```bash
mkdir -p skills/commit-generator/{references,assets}
```

2. 创建 `SKILL.md`:
```yaml
---
name: commit-generator
description: "根据代码变更生成规范的 Git 提交信息。当用户需要提交代码、写 commit message 时使用。"
---

你是 Git 提交信息专家。按照以下步骤生成提交信息：

1. 分析 `git diff --cached` 的输出
2. 加载 'references/commit-conventions.md' 获取团队规范
3. 识别变更类型（feat/fix/docs/refactor/test/chore）
4. 生成符合 Conventional Commits 规范的提交信息
5. 输出格式：
   <type>(<scope>): <subject>
   
   <body>
   
   <footer>
```

3. 创建 `references/commit-conventions.md`:
```markdown
# Git 提交规范

## Type 类型
- feat: 新功能
- fix: Bug 修复
- docs: 文档更新
- style: 代码格式（不影响逻辑）
- refactor: 重构
- test: 测试相关
- chore: 构建配置

## Scope 范围
- api: API 相关
- ui: 前端界面
- db: 数据库
- auth: 认证授权

## 示例
feat(api): 添加用户头像上传接口

- 支持 jpg/png 格式
- 限制文件大小 2MB
- 自动压缩到 200x200

Closes #123
```

4. 测试使用:
```
"帮我生成这次变更的 commit message"
```

---

### 练习二：为现有 Skill 添加 Gotchas（10 分钟）

**任务**: 为你的 Skill 添加踩坑清单

**步骤**:
1. 回忆最近 3 次使用这个 Skill 时遇到的问题
2. 按照以下格式记录：

```markdown
## ⚠️ Gotchas

### Gotcha #1: [问题名称]
- **症状**: [什么情况会出现]
- **原因**: [为什么会发生]
- **解决**: [如何修复]
- **示例**: [具体的错误和正确做法]

### Gotcha #2: ...
```

3. 在 SKILL.md 的开头添加：
```markdown
## ⚠️ 重要提醒

使用本 Skill 前，请先阅读 `references/gotchas.md` 了解常见陷阱。
```

---

### 练习三：优化 Description 字段（5 分钟）

**任务**: 将你的 Skill description 从"介绍"改为"触发器"

**错误示例**:
```yaml
description: "这是一个 Git 提交信息生成工具"
```

**正确示例**:
```yaml
description: "根据代码变更生成规范的 Git 提交信息。当用户需要提交代码、写 commit message、或询问'怎么写提交信息'时使用。不适用于：查看提交历史、回退代码、或解决合并冲突。"
```

**优化公式**:
```
[核心功能]。当用户 [触发场景 A]、[触发场景 B]、或 [触发场景 C] 时使用。不适用于：[排除场景]。
```

---

## 📚 附录：官方最佳实践速查表

### Skill 设计铁律

| 铁律 | 原因 | 示例 |
|-----|------|-----|
| **Don't State the Obvious** | Claude 已有通用知识 | ❌ "如何居中 div"<br>✅ "避免 Inter 字体和紫色渐变" |
| **Build a Gotchas Section** | 踩坑经验最有价值 | 记录所有失败点和解决方案 |
| **Use File System** | Skill 是 folder，不是文件 | `references/`, `assets/`, `scripts/` |
| **Avoid Railroading** | 保留灵活性 | ✅ "有工具 A、B、C，根据情况选择" |
| **Description = Trigger** | Claude 只看 description 决定是否激活 | 必须写"当用户...时使用" |

---

### 9 种 Skill 类型速查

| 类型 | 用途 | 关键要素 |
|-----|------|---------|
| Library & API Reference | 库/框架使用指南 | API 文档 + Gotchas |
| Product Verification | 功能测试 | 录制视频 + 程序化断言 |
| Data Fetching & Analysis | 数据查询 | 凭证 + 查询模式 |
| Business Process Automation | 自动化工作流 | 依赖其他 Skills + 日志记录 |
| Code Scaffolding | 代码生成 | 脚本 + 模板 |
| Code Quality & Review | 代码审查 | 确定性工具 + Hooks |
| CI/CD & Deployment | 部署流程 | 多 Skill 协作 |
| Runbooks | 故障排查 | 症状映射 + 调查流程 |
| Infrastructure Operations | 运维维护 | Guardrails + 最佳实践 |

---

### 高级功能

#### Memory 机制
```markdown
## 记忆机制

每次执行时，读取 `scripts/history.json` 了解：
- 最近执行的任务
- 遇到的坑
- 成功的模式

执行完成后，更新 history.json 记录本次经验。
```

#### On Demand Hooks
```yaml
# production-safety skill
hooks:
  PreToolUse:
  - match: "rm -rf"
    action: block
    message: "❌ 生产环境禁止执行 rm -rf"
```

---

## 🎯 培训后行动清单

### 立即行动（今天）
- [ ] 创建你的第一个 Skill（练习一）
- [ ] 为这个 Skill 添加 Gotchas（练习二）
- [ ] 优化 description 字段（练习三）

### 本周内
- [ ] 识别你日常工作中的 3 个重复流程
- [ ] 为每个流程创建对应的 Skill
- [ ] 在团队中分享你的 Skill

### 持续优化
- [ ] 每次踩坑都更新 Gotchas
- [ ] 每周回顾 Skill 使用情况
- [ ] 发现最佳实践就固化成 Skill

---

## 📖 推荐阅读

1. **Claude Code 官方文档**: https://code.claude.com/docs/en/skills
2. **Anthropic Skilljar 课程**: https://anthropic.skilljar.com/introduction-to-agent-skills
3. **5 种设计模式原文**: https://x.com/libukai/status/2035052747914096657
4. **Anthropic 官方总结**: https://x.com/trq212/status/2033949937936085378
5. **示例 Skills**: https://github.com/anthropics/skills

---

## 💬 结语

**核心认知**:
> Skill = 把你平时怎么干活，固化成 Claude 可复用的能力模块

**你有多少稳定流程，就能做出多少 Skill。**  
**你踩过多少坑，就能让 Claude 少踩多少坑。**

**本质上，你不是在"用 AI"，而是在把自己训练成一个可以复制的 AI 工作流系统。**

这件事一旦跑起来，是真的会上瘾。🚀

---

**培训完成！现在，去写出属于你的 3 个 Skills 吧！** 🎉

---

## 参考来源

- **5 种设计模式**: https://x.com/libukai/status/2035052747914096657
- **9 种 Skill 类型**: https://x.com/trq212/status/2033949937936085378
- **Anthropic Claude Code Team**: 官方最佳实践
