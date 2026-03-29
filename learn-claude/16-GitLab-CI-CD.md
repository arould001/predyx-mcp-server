# 16 - GitLab CI/CD 学习笔记

**学习时间**：2026-03-14 15:00
**页面地址**：https://code.claude.com/docs/en/gitlab-ci-cd

---

## 📖 核心概念

### Beta Status
- 目前 Beta 阶段
- 由 GitLab 维护
- 支持：GitLab issue #573776

### Why Use It
- **Instant MR creation** - 描述需求，Claude 提议完整 MR
- **Automated implementation** - 一条命令把 issue 转化为代码
- **Project-aware** - Claude 遵循 `CLAUDE.md` 指南
- **Simple setup** - 一个 job + 一个 masked variable
- **Enterprise-ready** - 支持 Claude API、AWS Bedrock、Google Vertex AI
- **Secure by default** - 在 GitLab runners 运行，遵循 branch protection 和 approvals

---

## 🔄 How It Works

### Event-driven Orchestration
- GitLab 监听 triggers（如 `@claude` mention）
- Job 收集 thread 和 repository 上下文
- 构建 prompts
- 运行 Claude Code

### Provider Abstraction
- **Claude API** (SaaS)
- **AWS Bedrock** (IAM-based access, cross-region)
- **Google Vertex AI** (GCP-native, Workload Identity Federation)

### Sandboxed Execution
- 隔离 container
- 严格 network 和 filesystem 规则
- workspace-scoped permissions
- 所有更改通过 MR

---

## 🚀 Setup

### Quick Setup

**1. Add masked CI/CD variable**
- Settings → CI/CD → Variables
- Add `ANTHROPIC_API_KEY` (masked, protected)

**2. Add Claude job to `.gitlab-ci.yml`**

```yaml
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update && apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude -p "${AI_FLOW_INPUT:-'Review this MR and implement the requested changes'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
```

---

## 💡 Example Use Cases

### Turn Issues into MRs
```bash
# In an issue comment
@claude implement this feature based on the issue description
```

Claude 分析 issue 和代码库，在分支写更改，打开 MR。

### Get Implementation Help
```bash
# In an MR discussion
@claude suggest a concrete approach to cache the results of this API call
```

### Fix Bugs Quickly
```bash
# In an issue or MR comment
@claude fix the TypeError in the user dashboard component
```

---

## ☁️ Using with AWS Bedrock & Google Vertex AI

### AWS Bedrock (OIDC)

**Prerequisites**:
- AWS account with Amazon Bedrock access
- GitLab configured as OIDC identity provider
- IAM role with Bedrock permissions

**Required CI/CD variables**:
- `AWS_ROLE_TO_ASSUME` (role ARN)
- `AWS_REGION` (Bedrock region)

**Job Example**:
```yaml
claude-bedrock:
  stage: ai
  image: node:24-alpine3.21
  before_script:
    - apk add --no-cache bash curl jq git python3 py3-pip
    - pip install --no-cache-dir awscli
    - curl -fsSL https://claude.ai/install.sh | bash
    # Exchange GitLab OIDC token for AWS credentials
    - export AWS_WEB_IDENTITY_TOKEN_FILE="${CI_JOB_JWT_FILE:-/tmp/oidc_token}"
    - aws sts assume-role-with-web-identity ... > /tmp/aws_creds.json
    - export AWS_ACCESS_KEY_ID=$(jq -r .Credentials.AccessKeyId /tmp/aws_creds.json)
    - export AWS_SECRET_ACCESS_KEY=$(jq -r .Credentials.SecretAccessKey /tmp/aws_creds.json)
    - export AWS_SESSION_TOKEN=$(jq -r .Credentials.SessionToken /tmp/aws_creds.json)
  script:
    - claude -p "..." --permission-mode acceptEdits --allowedTools "Bash Read Edit Write mcp__gitlab"
  variables:
    AWS_REGION: "us-west-2"
```

### Google Vertex AI (WIF)

**Prerequisites**:
- Vertex AI API enabled
- Workload Identity Federation configured
- Service account with Vertex AI permissions

**Required CI/CD variables**:
- `GCP_WORKLOAD_IDENTITY_PROVIDER`
- `GCP_SERVICE_ACCOUNT`
- `CLOUD_ML_REGION`

**Job Example**:
```yaml
claude-vertex:
  stage: ai
  image: gcr.io/google.com/cloudsdktool/google-cloud-cli:slim
  before_script:
    - apt-get update && apt-get install -y git
    - curl -fsSL https://claude.ai/install.sh | bash
    # Authenticate to Google Cloud via WIF
    - gcloud auth login --cred-file=<(...)
  script:
    - CLOUD_ML_REGION="${CLOUD_ML_REGION:-us-east5}" claude -p "..."
  variables:
    CLOUD_ML_REGION: "us-east5"
```

---

## 🎯 Best Practices

### CLAUDE.md Configuration
在仓库根创建 `CLAUDE.md`：
```markdown
# Project Guidelines

## Code Style
- Use 2-space indentation
- Follow ESLint rules
- Write tests for new features

## Security Requirements
- No hardcoded secrets
- Validate all inputs
- Use parameterized queries

## Review Criteria
- Check for security issues
- Verify test coverage
- Ensure documentation
```

### Security Considerations
- **Never commit API keys** to repository
- Use GitLab CI/CD variables (masked, protected)
- Use OIDC/WIF where possible (no long-lived keys)
- Limit job permissions and network egress
- Review Claude's MRs like any contributor

### Optimizing Performance
- Keep `CLAUDE.md` focused and concise
- Provide clear issue/MR descriptions
- Configure sensible job timeouts
- Cache npm and package installs

### CI Costs
**GitLab Runner time**:
- 消耗 compute minutes
- 根据运行时间和 runner 类型计费

**API costs**:
- 每次 Claude 交互消耗 tokens
- 基于 prompt 和 response 大小
- 任务复杂性和代码库大小影响

**Cost optimization**:
- Use specific `@claude` commands
- Set appropriate `max_turns` and job timeout
- Limit concurrency

---

## 🔐 Security and Governance

- **Isolated container** - 隔离容器，受限网络访问
- **MR-based changes** - 所有更改通过 MR，reviewers 看到每个 diff
- **Branch protection** - Branch protection 和 approval rules 适用于 AI 生成的代码
- **Workspace-scoped permissions** - 限制写入范围
- **Bring your own credentials** - 使用自己的 provider credentials

---

## 🛠️ Troubleshooting

### Claude not responding to @claude commands
- 验证 pipeline 被触发
- 确保 CI/CD variables 存在且 unmasked
- 确认 comment 包含 `@claude`（不是 `/claude`）

### Job can't write comments or open MRs
- 确保 `CI_JOB_TOKEN` 有足够权限
- 或使用 Project Access Token with `api` scope
- 检查 `mcp__gitlab` tool 在 `--allowedTools` 中启用

### Authentication errors
**Claude API**: 确认 `ANTHROPIC_API_KEY` 有效且未过期

**Bedrock/Vertex**: 验证 OIDC/WIF 配置、role impersonation、secret names

---

## 🔧 Advanced Configuration

### Common Parameters
- `prompt` / `prompt_file` - Instructions inline 或 via file
- `max_turns` - Limit back-and-forth iterations
- `timeout_minutes` - Limit total execution time
- `ANTHROPIC_API_KEY` - Required for Claude API

### Customizing Behavior
**Two ways**:
1. **CLAUDE.md** - 定义编码标准、安全要求、项目约定
2. **Custom prompts** - 通过 `prompt` / `prompt_file` 传递任务特定指令

---

## 💡 学习感悟

### 1. **与 GitHub Actions 的相似性**
GitLab CI/CD 与 GitHub Actions 非常相似：
- Event-driven
- Provider abstraction
- Sandboxed execution
- CLAUDE.md support

**差异主要在配置格式和 provider 配置**。

### 2. **OIDC/WIF 的重要性**
AWS Bedrock 和 Google Vertex AI 都使用：
- **OIDC (OpenID Connect)** for AWS
- **WIF (Workload Identity Federation)** for GCP

**无长期密钥，更安全**。

### 3. **GitLab MCP Server**
Job 中可以启动 GitLab MCP server：
```bash
/bin/gitlab-mcp-server || true
```

**让 Claude 通过 MCP 与 GitLab 交互**。

### 4. **MR-based 的安全模型**
所有更改通过 MR：
- Reviewers 看到每个 diff
- Branch protection 应用
- Approval rules 生效

**这是"Trust but Verify"原则**。

### 5. **Bring Your Own Credentials**
使用自己的 provider credentials：
- 完全控制成本
- 数据驻留可控
- 符合企业采购需求

**这是企业部署的关键**。

---

## 🎯 实践建议

### 1. **从 Simple Job 开始**

```yaml
# .gitlab-ci.yml
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - claude -p "Review this MR"
```

### 2. **创建 CLAUDE.md**

```markdown
# Guidelines
- Follow coding standards
- Write tests
- Document changes
```

### 3. **测试 Basic Workflow**

```bash
# 创建 Issue
"Implement user authentication"

# Comment
@claude implement this feature
```

### 4. **配置 OIDC/WIF（如需要）**

**AWS Bedrock**:
- Configure GitLab as OIDC provider
- Create IAM role with Bedrock permissions
- Set `AWS_ROLE_TO_ASSUME` and `AWS_REGION`

**Google Vertex AI**:
- Configure Workload Identity Federation
- Create service account
- Set `GCP_WORKLOAD_IDENTITY_PROVIDER` and `GCP_SERVICE_ACCOUNT`

### 5. **监控 Costs**

- Check GitLab runner usage
- Monitor API token consumption
- Set `max_turns` and timeouts

---

## 📚 与 GitHub Actions 的对比

### 相似之处
1. **Event-driven** - 都基于事件触发
2. **Provider abstraction** - 都支持多种 provider
3. **CLAUDE.md** - 都支持项目特定指南
4. **MR/PR-based** - 都通过 merge request/pull request

### 差异之处
1. **Configuration format** - GitLab YAML vs GitHub YAML
2. **OIDC setup** - GitLab CI/CD JWT vs GitHub OIDC
3. **MCP server** - GitLab 有专门的 MCP server
4. **Maintainer** - GitLab CI/CD 由 GitLab 维护

### 可以借鉴
1. **OIDC/WIF Configuration** - 无密钥认证
2. **GitLab MCP Server** - 集成 MCP
3. **MR-based Safety** - 所有更改通过 MR
4. **Provider Examples** - 完整的 AWS/Google 配置示例

---

## 🏷️ 标签
`#gitlab-ci` `#ci-cd` `#automation` `#oidc` `#enterprise` `#bedrock` `#vertex-ai`
