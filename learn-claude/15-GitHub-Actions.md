# 15 - GitHub Actions 学习笔记

**学习时间**：2026-03-14 14:55
**页面地址**：https://code.claude.com/docs/en/github-actions

---

## 📖 核心概念

### 是什么
Claude Code GitHub Actions 让你用 `@claude` mention 在 PR 或 Issue 中触发 AI 自动化：
- 分析代码
- 创建 PR
- 实现功能
- 修复 Bug
- 遵循项目标准

### Why Use It
- **Instant PR creation** - 描述需求，Claude 创建完整 PR
- **Automated code implementation** - 用一条命令把 issue 转化为代码
- **Follows your standards** - Claude 遵循 `CLAUDE.md` 指南
- **Simple setup** - 几分钟开始
- **Secure by default** - 代码留在 GitHub runners

---

## 🚀 Setup

### Quick Setup (推荐)
```bash
# 在 Claude Code 中运行
/install-github-app
```

**要求**：
- Repository admin 权限
- GitHub app 需要 Contents、Issues、Pull requests 的 read & write 权限
- 仅适用于 direct Claude API 用户

### Manual Setup

**步骤**：
1. **Install Claude GitHub app**
   - https://github.com/apps/claude

2. **Add ANTHROPIC_API_KEY secret**
   - Settings → Secrets → Actions

3. **Copy workflow file**
   - 从 `examples/claude.yml` 到 `.github/workflows/`

---

## 🔄 Upgrading from Beta

**v1.0 Breaking Changes**：

| Old Beta | New v1.0 |
|----------|----------|
| `mode: "tag"` / `"agent"` | (Removed - auto-detected) |
| `direct_prompt` | `prompt` |
| `custom_instructions` | `claude_args: --append-system-prompt` |
| `max_turns` | `claude_args: --max-turns` |
| `model` | `claude_args: --model` |
| `claude_env` | `settings` (JSON format) |

**Example**：

**Before (Beta)**:
```yaml
- uses: anthropics/claude-code-action@beta
  with:
    mode: "tag"
    direct_prompt: "Review this PR"
    custom_instructions: "Follow our standards"
    max_turns: "10"
```

**After (v1.0)**:
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    prompt: "Review this PR"
    claude_args: |
      --append-system-prompt "Follow our standards"
      --max-turns 10
```

---

## 💡 Example Use Cases

### Basic Workflow
```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Code Review
```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review this pull request for code quality, correctness, and security"
          claude_args: "--max-turns 5"
```

### Daily Report
```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate a summary of yesterday's commits"
          claude_args: "--model opus"
```

---

## 🎯 Best Practices

### CLAUDE.md Configuration
在 repository root 创建 `CLAUDE.md`：
- Code style guidelines
- Review criteria
- Project-specific rules
- Preferred patterns

### Security
**Never** commit API keys directly：
```yaml
# ✅ Correct
anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}

# ❌ Wrong
anthropic_api_key: sk-ant-xxx
```

### Optimizing Performance
- Use issue templates 提供上下文
- Keep `CLAUDE.md` 简洁专注
- Configure appropriate timeouts

### CI Costs
**GitHub Actions costs**:
- 消耗 GitHub Actions minutes
- 根据运行时间和 runner 类型计费

**API costs**:
- 每次 Claude 交互消耗 API tokens
- 基于 prompt 和 response 长度
- 任务复杂性和代码库大小影响 token 使用

**Cost optimization**:
- Use specific `@claude` commands
- Configure `--max-turns` in `claude_args`
- Set workflow-level timeouts
- Use GitHub's concurrency controls

---

## 🔧 Configuration Examples

### Action Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `prompt` | Instructions for Claude (text or skill name) | No* |
| `claude_args` | CLI arguments passed to Claude Code | No |
| `anthropic_api_key` | Claude API key | Yes** |
| `github_token` | GitHub token for API access | No |
| `trigger_phrase` | Custom trigger phrase (default: `@claude`) | No |
| `use_bedrock` | Use AWS Bedrock | No |
| `use_vertex` | Use Google Vertex AI | No |

**Common claude_args**:
```yaml
claude_args: "--max-turns 5 --model claude-sonnet-4-6 --mcp-config /path/to/config.json"
```

- `--max-turns`: Maximum conversation turns (default: 10)
- `--model`: Model to use (e.g., `claude-sonnet-4-6`, `claude-opus-4-6`)
- `--mcp-config`: Path to MCP configuration
- `--allowed-tools`: Comma-separated list of allowed tools
- `--debug`: Enable debug output

---

## ☁️ Using with AWS Bedrock & Google Vertex AI

### Prerequisites

**Google Cloud Vertex AI**:
- GCP Project with Vertex AI enabled
- Workload Identity Federation configured
- Service account with required permissions
- GitHub App (recommended)

**AWS Bedrock**:
- AWS account with Amazon Bedrock enabled
- GitHub OIDC Identity Provider configured
- IAM role with Bedrock permissions
- GitHub App (recommended)

### Custom GitHub App (Recommended for 3P Providers)

**步骤**：
1. Go to https://github.com/settings/apps/new
2. Configure app settings:
   - GitHub App name: "YourOrg Claude Assistant"
   - Webhooks: Uncheck "Active"
3. Set permissions:
   - Contents: Read & Write
   - Issues: Read & Write
   - Pull requests: Read & Write
4. Click "Create GitHub App"
5. Generate private key (`.pem` file)
6. Install app to repository
7. Add secrets:
   - `APP_PRIVATE_KEY`: Contents of `.pem` file
   - `APP_ID`: Your GitHub App's ID

---

## 🛠️ Troubleshooting

### Claude not responding to @claude commands
- Verify GitHub App installed correctly
- Check workflows enabled
- Ensure API key in secrets
- Confirm comment contains `@claude` (not `/claude`)

### CI not running on Claude's commits
- Use GitHub App or custom app (not Actions user)
- Check workflow triggers include necessary events
- Verify app permissions include CI triggers

### Authentication errors
- Confirm API key valid with sufficient permissions
- For Bedrock/Vertex, check credentials configuration
- Ensure secrets named correctly in workflows

---

## 💡 学习感悟

### 1. **GitHub Actions 的 AI 自动化**

这是 **CI/CD 的未来**：
- 传统 CI/CD：脚本化、静态
- Claude Code GitHub Actions：AI 驱动、动态

**从"自动化"到"智能化"**。

### 2. **@claude Mention 的简洁性**

**只需一个 mention**：
```bash
@claude implement this feature
@claude fix the bug
@claude review this PR
```

**无需复杂配置**，降低了使用门槛。

### 3. **CLAUDE.md 的标准化作用**

`CLAUDE.md` 让 Claude：
- 遵循团队编码规范
- 理解项目特定规则
- 保持代码风格一致性

**这是"隐式知识显式化"**。

### 4. **Breaking Changes 的专业性**

Beta → v1.0 的 Breaking Changes 文档：
- 清晰的映射表
- Before/After 示例
- 详细的迁移指南

**体现了产品的成熟度**。

### 5. **多云支持的灵活性**

支持三种方式：
- **Direct Claude API** - 最简单
- **AWS Bedrock** - 企业数据驻留
- **Google Vertex AI** - 企业数据驻留

**满足不同企业需求**。

### 6. **成本意识**

文档明确提到：
- GitHub Actions costs
- API costs
- Cost optimization tips

**这体现了"Production Ready"**。

---

## 🎯 实践建议

### 1. **从 Simple Workflow 开始**

```yaml
# .github/workflows/claude.yml
name: Claude Code
on:
  issue_comment:
    types: [created]

jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### 2. **创建 CLAUDE.md**

```markdown
# Project Guidelines

## Code Style
- Use 2-space indentation
- Follow ESLint rules
- Write tests for new features

## Review Criteria
- Check for security issues
- Verify test coverage
- Ensure documentation

## Preferred Patterns
- Use async/await over callbacks
- Prefer functional components
- Follow React hooks best practices
```

### 3. **在 Issue 中测试**

```bash
# 创建 Issue
"Implement user authentication"

# 在 comment 中
@claude implement this feature based on the issue description
```

### 4. **配置 Code Review Workflow**

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review this PR for security, performance, and code quality"
          claude_args: "--max-turns 3"
```

### 5. **监控成本**

- 定期检查 GitHub Actions usage
- 设置 `--max-turns` 限制
- Use specific `@claude` commands 而非 generic

### 6. **企业部署**

如果需要数据驻留：
- 设置 AWS Bedrock 或 Google Vertex AI
- 创建 custom GitHub App
- Configure OIDC/Workload Identity

---

## 📚 与 OpenClaw 的对比

### 相似之处
- 都可以集成到 CI/CD
- 都支持自动化工作流

### 差异之处
1. **集成方式** - Claude Code 用 GitHub Actions，OpenClaw 用 cron
2. **触发方式** - Claude Code 用 `@claude` mention，OpenClaw 用定时任务
3. **标准化** - Claude Code 有 `CLAUDE.md`，OpenClaw 有 `AGENTS.md`

### 可以借鉴
1. **GitHub Actions Integration** - 更深度的 CI/CD 集成
2. **@mention Trigger** - 简单的触发方式
3. **CLAUDE.md Standard** - 项目特定指南
4. **Multi-cloud Support** - 支持多种云提供商
5. **Cost Documentation** - 明确的成本说明

---

## 🏷️ 标签
`#github-actions` `#ci-cd` `#automation` `#claude-md` `#enterprise` `#multi-cloud`
