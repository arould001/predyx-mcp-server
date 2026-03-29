# 29 - Configuration 学习笔记

**学习时间**：2026-03-14 17:40
**页面地址**：https://code.claude.com/docs/en/configuration

---

## 📖 概述

**Configuration** 部分包含三个子页面：
1. **Enterprise network configuration** - 代理、CA证书、mTLS配置
2. **Model configuration** - 模型选择、别名、环境变量
3. **LLM gateway configuration** - LLM网关配置

---

# 29.1 - Enterprise Network Configuration

**页面地址**：https://code.claude.com/docs/en/network-config

## 🌐 Proxy Configuration

### Environment Variables
**Claude Code respects standard proxy environment variables**:

```bash
# HTTPS proxy (recommended)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP proxy (if HTTPS not available)
export HTTP_PROXY=http://proxy.example.com:8080

# Bypass proxy for specific requests - space-separated format
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"

# Bypass proxy for specific requests - comma-separated format
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"

# Bypass proxy for all requests
export NO_PROXY="*"
```

**Note**: Claude Code **does not support SOCKS proxies**.

### Basic Authentication
**Include credentials in proxy URL**:
```bash
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

**Warning**: Avoid hardcoding passwords in scripts → use environment variables or secure credential storage.

**For advanced authentication** (NTLM, Kerberos, etc.) → use LLM Gateway service.

---

## 🔐 Custom CA Certificates

**For custom CAs for HTTPS connections**:
```bash
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

---

## 🛡️ mTLS Authentication

**For client certificate authentication**:
```bash
# Client certificate for authentication
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Client private key
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Optional: Passphrase for encrypted private key
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

---

## 📡 Network Access Requirements

**Claude Code requires access to**:
- **api.anthropic.com**: Claude API endpoints
- **claude.ai**: Authentication for claude.ai accounts
- **platform.claude.com**: Authentication for Anthropic Console accounts

**Ensure these URLs are allowlisted** in proxy configuration and firewall rules.

### Claude Code on the Web and Code Review
**Connect from Anthropic-managed infrastructure**.

**If GitHub Enterprise Cloud restricts by IP address**:
- Enable **IP allow list inheritance** for installed GitHub Apps
- Claude GitHub App registers its IP ranges
- Or add Anthropic API IP addresses to allow list manually

---

# 29.2 - Model Configuration

**页面地址**：https://code.claude.com/docs/en/model-config

## 🤖 Available Models

**Can configure**:
- A **model alias**
- A **model name**
- **Anthropic API**: Full model name
- **Bedrock**: Inference profile ARN
- **Foundry**: Deployment name
- **Vertex**: Version name

---

## 🏷️ Model Aliases

**Convenient way to select model settings**:

| Alias | Behavior |
|-------|----------|
| **default** | Recommended model setting (depends on account type) |
| **sonnet** | Latest Sonnet model (currently Sonnet 4.6) for daily coding |
| **opus** | Latest Opus model (currently Opus 4.6) for complex reasoning |
| **haiku** | Fast and efficient Haiku model for simple tasks |
| **sonnet[1m]** | Sonnet with 1M token context window |
| **opus[1m]** | Opus with 1M token context window |
| **opusplan** | Uses opus during plan mode, sonnet for execution |

**Aliases always point to latest version**.

**To pin to specific version**: Use full model name (e.g., `claude-opus-4-6`) or set environment variable (e.g., `ANTHROPIC_DEFAULT_OPUS_MODEL`).

---

## ⚙️ Setting Your Model

**Priority order**:
1. **During session**: `/model <alias|name>`
2. **At startup**: `claude --model <alias|name>`
3. **Environment variable**: `ANTHROPIC_MODEL=<alias|name>`
4. **Settings**: Configure in settings file using `model` field

### Examples

**CLI**:
```bash
# Start with Opus
claude --model opus

# Switch to Sonnet during session
/model sonnet
```

**Settings file**:
```json
{
  "permissions": {
    ...
  },
  "model": "opus"
}
```

---

## 🚫 Restrict Model Selection

**Enterprise administrators can use `availableModels`** to restrict which models users can select.

```json
{
  "availableModels": ["sonnet", "haiku"]
}
```

**When set**: Users cannot switch to models not in list via `/model`, `--model`, Config tool, or `ANTHROPIC_MODEL`.

### Default Model Behavior
**Default option not affected by `availableModels`** → always available and represents runtime default based on subscription tier.

**Even with `availableModels: []`**: Users can still use Claude Code with Default model for their tier.

### Control Model Users Run On
**Use `availableModels` together with `model` setting**:
- `availableModels`: Restricts what users can switch to
- `model`: Sets explicit model override, takes precedence over Default

**Example** (ensure all users run Sonnet 4.6 and can only choose Sonnet/Haiku):
```json
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### Merge Behavior
**When `availableModels` set at multiple levels** → arrays are merged and deduplicated.

**To enforce strict allowlist**: Set in managed or policy settings (highest priority).

---

## 🎯 Special Model Behavior

### default Model Setting
**Behavior depends on account type**:
- **Max and Team Premium**: Defaults to Opus 4.6
- **Pro and Team Standard**: Defaults to Sonnet 4.6
- **Enterprise**: Opus 4.6 available but not default

**May automatically fall back to Sonnet** if hit usage threshold with Opus.

### opusplan Model Setting
**Automated hybrid approach**:
- **In plan mode**: Uses opus for complex reasoning and architecture decisions
- **In execution mode**: Automatically switches to sonnet for code generation and implementation

**Best of both worlds**: Opus's superior reasoning for planning, Sonnet's efficiency for execution.

---

## 💪 Adjust Effort Level

**Effort levels control adaptive reasoning** → dynamically allocates thinking based on task complexity.

**Three levels** (persist across sessions):
- **low**: Faster and cheaper for straightforward tasks
- **medium**: Default (Opus 4.6 for Max/Team subscribers)
- **high**: Deeper reasoning for complex problems

**Fourth level** (session-only, not persist):
- **max**: Deepest reasoning with no constraint on token spending (Opus 4.6 only)

### Setting Effort
**Methods**:
- `/effort`: Run `/effort low`, `/effort medium`, `/effort high`, or `/effort max` to change level, or `/effort auto` to reset to model default
- **In `/model`**: Use left/right arrow keys to adjust effort slider when selecting model
- **`--effort` flag**: Pass `low`, `medium`, `high`, or `max` when launching
- **Environment variable**: Set `CLAUDE_CODE_EFFORT_LEVEL` to `low`, `medium`, `high`, `max`, or `auto`
- **Settings**: Set `effortLevel` in settings file to `"low"`, `"medium"`, or `"high"`

**Precedence**: Environment variable → configured level → model default.

**Supported on**: Opus 4.6 and Sonnet 4.6.

**Display**: Current effort level shown next to logo and spinner (e.g., "with low effort").

### Disable Adaptive Reasoning
**Set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`** → revert to previous fixed thinking budget controlled by `MAX_THINKING_TOKENS`.

---

## 📏 Extended Context

**Opus 4.6 and Sonnet 4.6 support 1M token context window**.

### Availability by Plan

| Plan | Opus 4.6 with 1M context | Sonnet 4.6 with 1M context |
|------|--------------------------|---------------------------|
| **Max, Team, and Enterprise** | Included with subscription | Requires extra usage |
| **Pro** | Requires extra usage | Requires extra usage |
| **API and pay-as-you-go** | Full access | Full access |

**To disable 1M context entirely**: Set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`.

### Pricing
- **Standard model pricing** with no premium for tokens beyond 200K
- **For plans with extended context included**: Usage covered by subscription
- **For plans through extra usage**: Tokens billed to extra usage

### Use 1M Context
**In model picker**: `/model` → appears in latest versions if account supports it.

**Using [1m] suffix**:
```bash
# Use the opus[1m] or sonnet[1m] alias
/model opus[1m]
/model sonnet[1m]

# Or append [1m] to a full model name
/model claude-opus-4-6[1m]
```

---

## 🔍 Checking Your Current Model

**Ways to see current model**:
- **In status line** (if configured)
- **In `/status`** (also displays account information)

---

## 🌍 Environment Variables

**Control model names that aliases map to**:

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Model for `opus`, or `opusplan` when Plan Mode active |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Model for `sonnet`, or `opusplan` when Plan Mode not active |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Model for `haiku`, or background functionality |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents |

**Note**: `ANTHROPIC_SMALL_FAST_MODEL` deprecated in favor of `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

---

## 📌 Pin Models for Third-Party Deployments

**When deploying through Bedrock, Vertex AI, or Foundry** → pin model versions before rolling out.

**Without pinning**: Model aliases resolve to latest version → users break silently when Anthropic releases new model and account doesn't have it enabled.

**Set all three model environment variables** to specific version IDs.

### Provider Examples

**Bedrock**:
```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
```

**Vertex AI**:
```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
```

**Foundry**:
```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
```

**Apply same pattern** for `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

**To upgrade users**: Update environment variables and redeploy.

### Enable Extended Context for Pinned Model
**Append [1m] to model ID**:
```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6[1m]'
```

**Applies 1M context window to all usage of that alias**, including `opusplan`.

**Claude Code strips suffix** before sending to provider.

**Only append [1m]** when underlying model supports 1M context.

### availableModels Still Applies
**Filtering matches on model alias** (opus, sonnet, haiku), not provider-specific model ID.

---

## 🔄 Override Model IDs Per Version

**`modelOverrides` setting** maps individual Anthropic model IDs to provider-specific strings.

**Use case**: Route each model version to specific Bedrock inference profile ARN, Vertex AI version name, or Foundry deployment name for governance, cost allocation, or regional routing.

**Set in settings file**:
```json
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

**Keys**: Anthropic model IDs as listed in Models overview.

**For dated model IDs**: Include date suffix exactly as it appears.

**Unknown keys**: Ignored.

**Overrides replace built-in model IDs** that back `/model` picker entries.

**On Bedrock**: Overrides take precedence over inference profiles discovered automatically.

**Direct values** (`ANTHROPIC_MODEL`, `--model`, `ANTHROPIC_DEFAULT_*_MODEL`) passed to provider as-is, not transformed by `modelOverrides`.

**Works alongside `availableModels`**: Allowlist evaluated against Anthropic model ID, not override value.

---

## 🚀 Prompt Caching Configuration

**Claude Code automatically uses prompt caching** to optimize performance and reduce costs.

**Disable caching globally or for specific model tiers**:

| Variable | Description |
|----------|-------------|
| `DISABLE_PROMPT_CACHING` | Set to 1 to disable for all models (takes precedence over per-model) |
| `DISABLE_PROMPT_CACHING_HAIKU` | Set to 1 to disable for Haiku only |
| `DISABLE_PROMPT_CACHING_SONNET` | Set to 1 to disable for Sonnet only |
| `DISABLE_PROMPT_CACHING_OPUS` | Set to 1 to disable for Opus only |

**Global setting takes precedence** over per-model settings.

**Per-model settings useful** for selective control or debugging specific models.

---

# 29.3 - LLM Gateway Configuration

**页面地址**：https://code.claude.com/docs/en/llm-gateway

## 🌐 What is LLM Gateway?

**Centralized proxy layer** between Claude Code and model providers.

**Provides**:
- **Centralized authentication**: Single point for API key management
- **Usage tracking**: Monitor usage across teams and projects
- **Cost controls**: Implement budgets and rate limits
- **Audit logging**: Track all model interactions for compliance
- **Model routing**: Switch between providers without code changes

---

## ✅ Gateway Requirements

**To work with Claude Code**, gateway must:

### API Format
**Must expose at least one**:

#### 1. Anthropic Messages
- `/v1/messages`
- `/v1/messages/count_tokens`
- **Must forward headers**: `anthropic-beta`, `anthropic-version`

#### 2. Bedrock InvokeModel
- `/invoke`
- `/invoke-with-response-stream`
- **Must preserve body fields**: `anthropic_beta`, `anthropic_version`

#### 3. Vertex rawPredict
- `:rawPredict`
- `:streamRawPredict`
- `/count-tokens:rawPredict`
- **Must forward headers**: `anthropic-beta`, `anthropic-version`

**Failure to forward headers or preserve body fields** → reduced functionality or inability to use features.

### Claude Code Feature Detection
**Determines features based on API format**.

**When using Anthropic Messages format with Bedrock or Vertex**:
```bash
export CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1
```

---

## ⚙️ Configuration

### Model Selection
**By default**: Claude Code uses standard model names for selected API format.

**If custom model names configured in gateway**: Use environment variables documented in Model configuration to match custom names.

---

## 🔧 LiteLLM Configuration

**Third-party proxy service**.

**Disclaimer**: Anthropic doesn't endorse, maintain, or audit LiteLLM's security or functionality. Use at your own discretion.

### Prerequisites
- Claude Code updated to latest version
- LiteLLM Proxy Server deployed and accessible
- Access to Claude models through chosen provider

### Authentication Methods

#### 1. Static API Key
**Simplest method**:
```bash
# Set in environment
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Or in Claude Code settings
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

**Value sent as Authorization header**.

#### 2. Dynamic API Key with Helper
**For rotating keys or per-user authentication**:

**Create helper script** (`~/bin/get-litellm-key.sh`):
```bash
#!/bin/bash
# Example: Fetch key from vault
vault kv get -field=api_key secret/litellm/claude-code

# Example: Generate JWT token
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

**Configure Claude Code**:
```json
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

**Set token refresh interval**:
```bash
# Refresh every hour (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

**Value sent as Authorization and X-Api-Key headers**.

**Precedence**: `apiKeyHelper` < `ANTHROPIC_AUTH_TOKEN` or `ANTHROPIC_API_KEY`.

### Endpoint Configuration

#### Unified Endpoint (Recommended)
**Using LiteLLM's Anthropic format endpoint**:
```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Benefits over pass-through**:
- Load balancing
- Fallbacks
- Consistent cost tracking and end-user tracking

#### Provider-Specific Pass-Through Endpoints (Alternative)

**Claude API through LiteLLM**:
```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

**Amazon Bedrock through LiteLLM**:
```bash
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

**Google Vertex AI through LiteLLM**:
```bash
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

**For more details**: Refer to LiteLLM documentation.

---

## 💡 学习感悟

### 1. **Enterprise Network Configuration 是企业部署的基础**
**三大配置**:
- **Proxy**: Standard env vars (`HTTPS_PROXY`, `HTTP_PROXY`, `NO_PROXY`)
- **Custom CA**: `NODE_EXTRA_CA_CERTS`
- **mTLS**: Client cert + key + passphrase

**不支持 SOCKS proxies**.

### 2. **Model Aliases 是便利的抽象**
**Seven aliases**:
- default (account-dependent)
- sonnet / opus / haiku
- sonnet[1m] / opus[1m]
- opusplan (hybrid: opus for planning, sonnet for execution)

**Always point to latest version**.

**To pin**: Use full model name or env var.

### 3. **Model Configuration Priority 是清晰的**
**Four levels**:
1. During session: `/model`
2. At startup: `--model`
3. Environment variable: `ANTHROPIC_MODEL`
4. Settings: `model` field

**From highest to lowest priority**.

### 4. **availableModels 是企业控制的关键**
**Restricts what users can switch to**:
- `/model`, `--model`, Config tool, `ANTHROPIC_MODEL` all respect
- **Default model not affected** → always available
- **Use with `model` setting** to fully control experience

**Arrays merge at multiple levels** → managed/policy settings for strict allowlist.

### 5. **Effort Level 是 adaptive reasoning 的控制**
**Three persistent levels**: low, medium, high
**One session-only level**: max (Opus 4.6 only)

**Methods to set**: `/effort`, `--effort`, env var, settings

**Precedence**: Env var → configured level → model default

**Supported on**: Opus 4.6 and Sonnet 4.6

### 6. **Extended Context (1M) 的可用性因计划而异**
**Max/Team/Enterprise**: Opus 1M included, Sonnet 1M requires extra
**Pro**: Both require extra
**API/Pay-as-you-go**: Full access

**Use [1m] suffix** to enable.

**Disable globally**: `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`

### 7. **Pin Models 是 Third-Party Deployment 的必备**
**Set all three env vars**:
- `ANTHROPIC_DEFAULT_OPUS_MODEL`
- `ANTHROPIC_DEFAULT_SONNET_MODEL`
- `ANTHROPIC_DEFAULT_HAIKU_MODEL`

**Without pinning**: Model aliases resolve to latest → break silently when new model released.

**Append [1m]** for extended context on pinned models.

### 8. **modelOverrides 是细粒度控制**
**Maps Anthropic model IDs to provider-specific strings**:
- Bedrock: ARN
- Vertex: Version name
- Foundry: Deployment name

**Use cases**: Governance, cost allocation, regional routing.

**Keys**: Anthropic model IDs (include date suffix for dated IDs).

**Works with availableModels**: Filtering on Anthropic ID, not override value.

### 9. **LLM Gateway 提供集中化控制**
**Benefits**:
- Centralized auth
- Usage tracking
- Cost controls
- Audit logging
- Model routing

**Must expose at least one API format**: Anthropic Messages, Bedrock InvokeModel, or Vertex rawPredict.

**Must forward/preserve headers and body fields**.

### 10. **LiteLLM 是流行的 Third-Party Proxy**
**Two auth methods**:
- Static API key (`ANTHROPIC_AUTH_TOKEN`)
- Dynamic API key with helper (`apiKeyHelper`)

**Two endpoint types**:
- Unified (recommended): `ANTHROPIC_BASE_URL`
- Pass-through: Provider-specific URLs

**Benefits of unified**: Load balancing, fallbacks, consistent tracking.

---

## 🎯 实践建议

### 1. **Configure Proxy for Enterprise**
```bash
export HTTPS_PROXY=https://proxy.example.com:8080
export NO_PROXY="localhost,192.168.1.1,.example.com"
```

**Allowlist required URLs**: api.anthropic.com, claude.ai, platform.claude.com.

### 2. **Use Model Aliases for Flexibility**
```bash
# Start with opus
claude --model opus

# Switch during session
/model sonnet
```

**Unless you need to pin to specific version**.

### 3. **Restrict Models for Teams**
**Settings file**:
```json
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

**Ensures consistent experience**.

### 4. **Adjust Effort Level Based on Task**
```bash
# Simple task → low effort (faster, cheaper)
/effort low

# Complex problem → high effort
/effort high
```

**Balance speed vs depth**.

### 5. **Use 1M Context for Long Sessions**
```bash
/model opus[1m]
```

**If your plan supports it**.

### 6. **Pin Models for Third-Party Deployments**
```bash
# Bedrock
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6-v1'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-3-5-v1'
```

**Prevent silent breakage when new models released**.

### 7. **Use modelOverrides for Fine-Grained Control**
**Settings file**:
```json
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

**Route to specific profiles for governance/cost allocation**.

### 8. **Use LLM Gateway for Centralized Control**
**Configure unified endpoint**:
```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key
```

**Benefits**: Load balancing, fallbacks, consistent tracking.

### 9. **Disable Prompt Caching if Needed**
```bash
# Disable globally
export DISABLE_PROMPT_CACHING=1

# Disable for specific model
export DISABLE_PROMPT_CACHING_HAIKU=1
```

**Useful for debugging or cloud providers with different implementations**.

### 10. **Check Current Model with /status**
```
/status
```

**Shows model and account information**.

---

## 🏷️ 标签
`#configuration` `#proxy` `#mtls` `#model-aliases` `#effort-level` `#extended-context` `#model-overrides` `#llm-gateway` `#litellm` `#prompt-caching` `#enterprise`
