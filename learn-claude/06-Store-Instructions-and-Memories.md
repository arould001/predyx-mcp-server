# 06 - Store Instructions and Memories 学习笔记

**学习时间**：2026-03-14 13:55  
**页面地址**：https://code.claude.com/docs/en/memory

---

## 📖 原文要点

### 两大记忆系统

Claude Code 有两种互补的记忆机制：

| 方面 | CLAUDE.md | Auto Memory |
|------|-----------|-------------|
| **谁写** | You | Claude |
| **包含什么** | 指令和规则 | 学习和模式 |
| **作用域** | Project、user、org | Per working tree |
| **加载到** | 每个会话 | 每个会话（前 200 行） |
| **用于** | 编码标准、工作流、项目架构 | 构建命令、调试见解、Claude 发现的偏好 |

**关键区别**：
- **CLAUDE.md** - 你写的，指导 Claude 行为
- **Auto Memory** - Claude 写的，从纠正中学习

---

## 📝 CLAUDE.md 文件

### 1. 位置选择（按优先级）

| 作用域 | 位置 | 目的 | 共享给 |
|--------|------|------|--------|
| **Managed policy** | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br>• Linux/WSL: `/etc/claude-code/CLAUDE.md`<br>• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | 组织范围指令（IT/DevOps 管理） | 组织内所有用户 |
| **Project instructions** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 项目团队共享指令 | 团队成员（通过源码控制） |
| **User instructions** | `~/.claude/CLAUDE.md` | 所有项目的个人偏好 | 只给你（所有项目） |

**优先级**：更具体的位置优先于更广泛的位置。

### 2. 创建项目 CLAUDE.md

**两种方式**：
1. **手动创建** - `./CLAUDE.md` 或 `./.claude/CLAUDE.md`
2. **自动生成** - 运行 `/init`

**`/init` 命令**：
- 分析代码库
- 自动发现构建命令、测试指令、项目约定
- 如果已存在，建议改进而非覆盖
- 从那里改进 Claude 不会自己发现的指令

### 3. 写有效指令

**CLAUDE.md 是上下文，不是强制配置**。如何写指令影响 Claude 遵循的可靠性。

#### 最佳实践

**1. 大小控制**
- 目标：< 200 行
- 更长 = 更多 token 消耗 + 降低遵循度
- 如果增长：用 imports 或 `.claude/rules/` 拆分

**2. 结构**
- 用 markdown headers 和 bullets 组织
- Claude 扫描结构与读者一样：有组织的章节比密集段落更容易遵循

**3. 具体性**
写足够具体可验证的指令：

❌ **不好**：
```markdown
Format code properly
Test your changes
Keep files organized
```

✅ **好**：
```markdown
Use 2-space indentation
Run npm test before committing
API handlers live in src/api/handlers/
```

**4. 一致性**
- 两条规则矛盾时，Claude 可能任意选一个
- 定期审查 CLAUDE.md、嵌套 CLAUDE.md、`.claude/rules/` 移除过时或冲突指令
- Monorepos 用 `claudeMdExcludes` 跳过不相关的其他团队文件

### 4. 导入额外文件

**语法**：`@path/to/import`

**特点**：
- 相对和绝对路径都允许
- 相对路径相对于包含 import 的文件，不是工作目录
- 可以递归导入，最多 5 跳

**示例**：
```markdown
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md

# Individual Preferences
- @~/.claude/my-project-instructions.md
```

**安全**：
- 首次遇到外部 imports 时，显示批准对话框列出文件
- 拒绝则 imports 保持禁用，对话框不再出现

### 5. CLAUDE.md 文件加载机制

**从工作目录向上走目录树**：
- `foo/bar/` → 加载 `foo/bar/CLAUDE.md` + `foo/CLAUDE.md`

**子目录发现**：
- 子目录中的 CLAUDE.md 不在启动时加载
- 在读取子目录文件时才包含

**大型 monorepo**：
- 用 `claudeMdExcludes` 跳过其他团队的文件

**额外目录**：
```bash
# 默认不加载额外目录的 CLAUDE.md
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

---

## 📂 用 .claude/rules/ 组织规则

### 为什么用 Rules？

**大型项目的优势**：
- 模块化指令
- 团队更易维护
- 可限定到特定文件路径
- 只在匹配文件时加载，减少噪音，节省上下文

**vs Skills**：
- **Rules** - 每个会话或打开匹配文件时加载
- **Skills** - 按需加载，适合任务特定指令

### 设置规则

**目录结构**：
```
your-project/
├── .claude/
│   ├── CLAUDE.md           # 主项目指令
│   └── rules/
│       ├── code-style.md   # 代码风格指南
│       ├── testing.md      # 测试约定
│       └── security.md     # 安全要求
```

**特点**：
- 所有 `.md` 文件递归发现
- 可组织到子目录（如 `frontend/`、`backend/`）
- 无 `paths` frontmatter 的 rules 在启动时加载，优先级与 `.claude/CLAUDE.md` 相同

### Path-Specific Rules（路径特定规则）

**YAML frontmatter 限定到特定文件**：
```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

**触发时机**：
- 只在 Claude 处理匹配模式的文件时触发
- 不是每次工具使用

**Glob 模式示例**：

| 模式 | 匹配 |
|------|------|
| `**/*.ts` | 任何目录的所有 TypeScript 文件 |
| `src/**/*` | `src/` 目录下的所有文件 |
| `*.md` | 项目根目录的 Markdown 文件 |
| `src/components/*.tsx` | 特定目录的 React 组件 |

**多模式**：
```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

### 跨项目共享规则（Symlinks）

**支持的符号链接**：
```bash
# 链接共享目录
ln -s ~/shared-claude-rules .claude/rules/shared

# 链接单个文件
ln -s ~/company-standards/security.md .claude/rules/security.md
```

**特点**：
- 符号链接正常解析和加载
- 循环符号链接被检测并优雅处理

### User-Level Rules

**位置**：`~/.claude/rules/`

**用于**：非项目特定的偏好

**示例**：
```
~/.claude/rules/
├── preferences.md    # 你的个人编码偏好
└── workflows.md      # 你偏好的工作流
```

**优先级**：User-level rules 在 project rules 之前加载，给 project rules 更高优先级。

---

## 🏢 大型团队管理

### 部署组织范围 CLAUDE.md

**位置**：
- macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
- Linux/WSL: `/etc/claude-code/CLAUDE.md`
- Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`

**特点**：
- 不能被个人设置排除
- 用 MDM、Group Policy、Ansible 等分发
- 确保组织范围指令始终应用

### 排除特定 CLAUDE.md 文件

**场景**：大型 monorepo，祖先 CLAUDE.md 不相关

**配置**：`.claude/settings.local.json`
```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

**特点**：
- 用 glob 语法匹配绝对文件路径
- 可在任何 settings 层配置：user、project、local、managed policy
- 数组跨层合并
- **Managed policy CLAUDE.md 无法排除**

---

## 🧠 Auto Memory

### 是什么？

**Auto Memory 让 Claude 跨会话积累知识，无需你写任何东西**。

**Claude 自动保存**：
- 构建命令
- 调试见解
- 架构笔记
- 代码风格偏好
- 工作流习惯

**决策机制**：
- Claude 决定什么值得记住
- 基于信息在未来对话中是否有用

**要求**：Claude Code v2.1.59+

### 启用/禁用

**默认**：开启

**切换方式**：
1. **UI**：会话中运行 `/memory`，使用 auto memory 切换
2. **Settings**：
   ```json
   {
     "autoMemoryEnabled": false
   }
   ```
3. **环境变量**：`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`

### 存储位置

**默认**：`~/.claude/projects/<project>/memory/`

**项目路径来源**：
- Git 仓库（所有 worktrees 和子目录共享一个目录）
- 非 git repo 用项目根

**自定义位置**：
```json
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

**接受来源**：policy、local、user settings
**不接受**：project settings（防止共享项目重定向到敏感位置）

**目录结构**：
```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 简洁索引，加载到每个会话
├── debugging.md       # 调试模式详细笔记
├── api-conventions.md # API 设计决策
└── ...                # Claude 创建的任何其他主题文件
```

**MEMORY.md 作用**：索引记忆目录

### 工作机制

**加载规则**：
- **MEMORY.md 前 200 行**在每个会话开始时加载
- 超过 200 行的内容不在会话开始时加载
- Claude 通过将详细笔记移到单独主题文件保持 MEMORY.md 简洁

**200 行限制**：
- 只适用于 MEMORY.md
- CLAUDE.md 文件完整加载（虽然更短文件产生更好遵循度）

**主题文件**（如 `debugging.md`、`patterns.md`）：
- 不在启动时加载
- Claude 需要时用标准文件工具按需读取

**读写时机**：
- 会话中 Claude 读写记忆文件
- 看到界面中 "Writing memory" 或 "Recalled memory" 时，Claude 正在主动更新或读取

**本地性**：
- 机器本地
- 同一 git 仓库的所有 worktrees 和子目录共享一个 auto memory 目录
- 不在机器或云环境间共享

### 审计和编辑记忆

**Auto memory 文件是普通 markdown**：
- 可随时编辑或删除
- 运行 `/memory` 浏览和打开记忆文件

**查看和编辑**：
- `/memory` 命令列出所有加载的 CLAUDE.md 和 rules 文件
- 切换 auto memory 开关
- 提供打开 auto memory 文件夹的链接
- 选择任何文件在编辑器中打开

**添加指令**：
- 让 Claude 记住："always use pnpm, not npm" → 保存到 auto memory
- 添加到 CLAUDE.md："add this to CLAUDE.md" → 添加到 CLAUDE.md
- 或通过 `/memory` 自己编辑

---

## 🔧 故障排除

### 1. Claude 不遵循我的 CLAUDE.md

**原因**：CLAUDE.md 内容作为用户消息传递，不是系统提示的一部分。Claude 尝试遵循，但无严格合规保证，特别是模糊或冲突指令。

**调试步骤**：
1. 运行 `/memory` 验证 CLAUDE.md 文件被加载
2. 检查相关 CLAUDE.md 在会话加载的位置
3. 使指令更具体："Use 2-space indentation" > "format code nicely"
4. 检查跨 CLAUDE.md 文件的冲突指令

**系统提示级别**：用 `--append-system-prompt`（必须每次调用传递，适合脚本和自动化）

**调试工具**：
- `InstructionsLoaded` hook - 记录加载了哪些指令文件、何时、为什么
- 有用于调试 path-specific rules 或子目录延迟加载文件

### 2. 我不知道 auto memory 保存了什么

**解决**：
- 运行 `/memory`
- 选择 auto memory folder 浏览 Claude 保存的内容
- 都是普通 markdown，可读、编辑、删除

### 3. 我的 CLAUDE.md 太大

**解决**：
- 200+ 行文件消耗更多上下文，可能降低遵循度
- 移动详细内容到用 `@path` imports 引用的单独文件
- 或拆分指令到 `.claude/rules/` 文件

### 4. /compact 后指令似乎丢失

**原因**：
- CLAUDE.md 完全在压缩中存活
- 压缩后，Claude 从磁盘重新读取 CLAUDE.md 并重新注入会话
- 如果压缩后指令消失，它只在对话中给出，未写入 CLAUDE.md

**解决**：添加到 CLAUDE.md 使其跨会话持久

---

## 💡 学习感悟

### 1. **双层记忆系统的优雅**

Claude Code 的记忆系统设计非常优雅：
- **CLAUDE.md** - 显式记忆（你写的）
- **Auto Memory** - 隐式记忆（Claude 学的）

这类似于人类的**陈述性记忆**（Declarative Memory）和**程序性记忆**（Procedural Memory）。

### 2. **上下文管理的精细化**

记忆系统体现了精细化上下文管理：
- **200 行限制** - 控制 token 消耗
- **Path-specific rules** - 按需加载
- **懒加载** - 子目录发现

这符合 "Context is precious" 原则。

### 3. **模块化的威力**

`.claude/rules/` 的设计：
- 模块化指令
- 可限定作用域
- 跨项目共享（symlinks）

这符合软件工程的**模块化原则**。

### 4. **Auto Memory 的智能**

Auto Memory 的关键洞察：
- **Claude 决定**什么值得记住
- 基于未来对话的**有用性**
- **机器本地**（安全）
- **自动整理**（MEMORY.md + 主题文件）

这是真正的**自主学习**能力。

### 5. **组织管理的平衡**

Managed policy + claudeMdExcludes 的设计：
- **组织控制** - Managed policy 无法排除
- **个人灵活** - 可排除不相关文件
- **分层优先** - 明确的优先级规则

平衡了**安全性**和**灵活性**。

### 6. **与 OpenClaw 的对比**

**相似**：
- CLAUDE.md vs AGENTS.md（显式记忆）
- Auto Memory vs MEMORY.md（隐式记忆）

**差异**：
- Claude Code 的 Auto Memory 是自动的，OpenClaw 的 MEMORY.md 需要手动更新
- Claude Code 有 `.claude/rules/` 的模块化，OpenClaw 更单一
- Claude Code 有 200 行限制，OpenClaw 没有

**可以借鉴**：
- Auto Memory 的自动学习机制
- `.claude/rules/` 的模块化设计
- Path-specific rules 的按需加载

---

## 🎯 实践建议

### 1. **立即创建 CLAUDE.md**

```bash
# 在项目中
cd your-project
claude
/init
```

### 2. **保持 CLAUDE.md < 200 行**

```markdown
# 项目约定（CLAUDE.md）

## 核心规则
- Use pnpm, not npm
- Run npm test before committing
- API handlers in src/api/handlers/

## 构建命令
- Dev: `pnpm dev`
- Build: `pnpm build`
- Test: `pnpm test`

## 详细内容移到 Rules
- Code style → .claude/rules/code-style.md
- Security → .claude/rules/security.md
- Testing → .claude/rules/testing.md
```

### 3. **用 Path-Specific Rules**

```markdown
# .claude/rules/api.md
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- All endpoints must include input validation
- Use standard error response format
- Include OpenAPI documentation
```

### 4. **启用 Auto Memory**

```bash
# 默认已启用，检查
/memory

# 如果禁用，重新启用
# Settings:
{
  "autoMemoryEnabled": true
}
```

### 5. **定期审查**

```bash
# 查看加载了什么
/memory

# 检查 auto memory
# 打开 ~/.claude/projects/<project>/memory/
```

### 6. **用 Symlinks 共享**

```bash
# 跨项目共享规则
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

---

## 📚 与 OpenClaw 的对比

### 可以借鉴

1. **Auto Memory** - 自动学习机制
2. **Path-Specific Rules** - 按需加载
3. **200 行限制** - 控制上下文
4. **Symlinks 共享** - 跨项目复用

### 已有的优势

1. **MEMORY.md** - 类似 Auto Memory，但需手动更新
2. **AGENTS.md** - 类似 CLAUDE.md
3. **Skills** - 类似 Rules

### 建议改进

1. **自动记忆** - 让 OpenClaw 自动更新 MEMORY.md
2. **模块化记忆** - 支持 `memory/rules/*.md`
3. **Path-Specific** - 支持 paths frontmatter
4. **上下文限制** - 添加行数限制提示

---

## 🏷️ 标签
`#memory` `#claudemd` `#auto-memory` `#rules` `#context-management` `#organization`
