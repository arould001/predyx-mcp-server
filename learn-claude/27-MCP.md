# 27 - Model Context Protocol (MCP) 学习笔记

**学习时间**：2026-03-14 17:15
**页面地址**：https://code.claude.com/docs/en/mcp

---

## 📖 核心概念

### 是什么
**Model Context Protocol (MCP)** 是开源的 AI-tool 集成标准。MCP servers 给 Claude Code 提供访问工具、数据库和 API 的能力。

### 能力
**通过 MCP servers，Claude Code 可以**：
- 从 issue trackers 实现功能
- 分析监控数据（Sentry, Statsig）
- 查询数据库（PostgreSQL, etc.）
- 集成设计（Figma, Slack）
- 自动化工作流（Gmail drafts）

---

## 🔧 Installing MCP Servers

### Three Configuration Ways

#### Option 1: Remote HTTP Server (Recommended)
**HTTP servers** 是连接远程 MCP servers 的推荐选项。

```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Real example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

#### Option 2: Remote SSE Server (Deprecated)
**SSE (Server-Sent Events)** transport 已弃用 → 使用 HTTP servers 代替。

```bash
# Basic syntax
claude mcp add --transport sse <name> <url>

# Real example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Example with authentication header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

#### Option 3: Local Stdio Server
**Stdio servers** 作为本地进程运行 → 适合需要直接系统访问或自定义脚本的工具。

```bash
# Basic syntax
claude mcp add [options] <name> -- <command> [args...]

# Real example: Add Airtable server
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

**Important: Option ordering**:
- All options (`--transport`, `--env`, `--scope`, `--header`) must come **before** server name
- `--` (double dash) separates server name from command and arguments
- Prevents conflicts between Claude's flags and server's flags

**Windows Users**: On native Windows (not WSL), local MCP servers using npx require `cmd /c` wrapper.

```bash
# This creates command="cmd" which Windows can execute
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

---

## 🛠️ Managing Your Servers

### Commands
```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp
```

### Dynamic Tool Updates
**MCP list_changed notifications** → servers dynamically update tools/prompts/resources without disconnect/reconnect.

---

## 💡 Tips

### Scope Flag
**Use `--scope` to specify configuration storage**:
- **local** (default): Available only to you in current project
- **project**: Shared with everyone via `.mcp.json` file
- **user**: Available to you across all projects

### Environment Variables
**Set with `--env` flags**:
```bash
--env KEY=value
```

### Timeout
**Configure MCP server startup timeout**:
```bash
MCP_TIMEOUT=10000 claude  # 10-second timeout
```

### Output Token Limit
**Warning when MCP tool output exceeds 10,000 tokens** → increase limit:
```bash
MAX_MCP_OUTPUT_TOKENS=50000 claude
```

### OAuth Authentication
**Use `/mcp` to authenticate with remote servers requiring OAuth 2.0**.

---

## 📋 MCP Installation Scopes

### Local Scope
**Default configuration level** → stored in `~/.claude.json` under project's path.

**Characteristics**:
- Private to you
- Only accessible within current project directory
- Ideal for personal development servers, experimental configs, sensitive credentials

```bash
# Add a local-scoped server (default)
claude mcp add --transport http stripe https://mcp.stripe.com

# Explicitly specify local scope
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### Project Scope
**Team collaboration** → stored in `.mcp.json` at project root.

**Characteristics**:
- Checked into version control
- All team members have access
- Automatically creates/updates `.mcp.json`

```bash
# Add a project-scoped server
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

**Resulting `.mcp.json`**:
```json
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

**Security**: Claude Code prompts for approval before using project-scoped servers.

**Reset approvals**: `claude mcp reset-project-choices`

### User Scope
**Cross-project accessibility** → stored in `~/.claude.json`.

**Characteristics**:
- Available across all projects on your machine
- Private to your user account
- Works well for personal utility servers, development tools

```bash
# Add a user server
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Choosing the Right Scope

| Scope | Use Case |
|-------|----------|
| **Local** | Personal servers, experimental configs, sensitive credentials (one project) |
| **Project** | Team-shared servers, project-specific tools, collaboration required |
| **User** | Personal utilities across multiple projects, frequently used services |

### Where Stored?

| Scope | Location |
|-------|----------|
| **User and Local** | `~/.claude.json` |
| **Project** | `.mcp.json` in project root |
| **Managed** | `managed-mcp.json` in system directories |

### Scope Hierarchy
**Precedence**: Local > Project > User

**When servers with same name exist**: Local-scoped servers override project-scoped, which override user-scoped.

---

## 🌍 Environment Variable Expansion in .mcp.json

### Supported Syntax
- `${VAR}` → Expands to value of environment variable VAR
- `${VAR:-default}` → Expands to VAR if set, otherwise uses default

### Expansion Locations
- **command** → Server executable path
- **args** → Command-line arguments
- **env** → Environment variables passed to server
- **url** → For HTTP server types
- **headers** → For HTTP server authentication

### Example
```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

**If required env var not set and no default** → Claude Code fails to parse config.

---

## 🔌 Plugin-Provided MCP Servers

### How It Works
**Plugins can bundle MCP servers** → automatically provide tools/integrations when enabled.

**Characteristics**:
- Work identically to user-configured servers
- Define in `.mcp.json` at plugin root or inline in `plugin.json`
- Start automatically when plugin enabled
- Managed through plugin installation (not `/mcp` commands)

### Configuration

#### In `.mcp.json` at Plugin Root
```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}"
    }
  }
}
```

#### Inline in `plugin.json`
```json
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

### Features
- **Automatic lifecycle**: Start when plugin enables (restart Claude Code to apply changes)
- **Environment variables**: Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths
- **User environment access**: Same env vars as manually configured servers
- **Multiple transport types**: stdio, SSE, HTTP

### Viewing
```bash
# Within Claude Code, see all MCP servers including plugin ones
/mcp
```

**Plugin servers appear with indicators** showing they come from plugins.

### Benefits
- **Bundled distribution**: Tools and servers packaged together
- **Automatic setup**: No manual MCP configuration
- **Team consistency**: Everyone gets same tools when plugin installed

---

## 🔐 Authenticate with Remote MCP Servers

### OAuth 2.0 Support
**Many cloud-based MCP servers require authentication** → Claude Code supports OAuth 2.0.

### Steps

#### 1. Add Server Requiring Authentication
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

#### 2. Use /mcp Command Within Claude Code
```
/mcp
```

**Then follow steps in browser to login**.

### Tips
- **Authentication tokens** stored securely and refreshed automatically
- **Clear authentication** in `/mcp` menu to revoke access
- **If browser doesn't open automatically** → copy provided URL and open manually
- **If browser redirect fails** → paste full callback URL from browser's address bar into URL prompt
- **OAuth works with HTTP servers**

---

## 🔑 Fixed OAuth Callback Port

### Why?
**Some MCP servers require specific redirect URI registered in advance**.

### Default Behavior
**Claude Code picks random available port** for OAuth callback.

### Fix Port
**Use `--callback-port`** to match pre-registered redirect URI of form `http://localhost:PORT/callback`.

```bash
# Fixed callback port with dynamic client registration
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

---

## 🎫 Pre-Configured OAuth Credentials

### When Needed
**Some MCP servers don't support automatic OAuth setup** → error: "Incompatible auth server: does not support dynamic client registration."

### Steps

#### 1. Register OAuth App with Server
**Create app through server's developer portal** → note client ID and client secret.

**Register redirect URI** (if required): `http://localhost:PORT/callback`

#### 2. Add Server with Credentials

**Option A: `claude mcp add`**
```bash
claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

**Option B: `claude mcp add-json`**
```bash
claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
```

#### 3. Authenticate in Claude Code
**Run `/mcp`** → follow browser login flow.

### Tips
- **Client secret stored securely** in system keychain (macOS) or credentials file, not in config
- **Public OAuth client with no secret** → use only `--client-id` without `--client-secret`
- **`--callback-port`** can be used with or without `--client-id`
- **These flags only apply to HTTP and SSE transports** → no effect on stdio servers
- **Verify OAuth credentials configured**: `claude mcp get <name>`

---

## 🔄 Override OAuth Metadata Discovery

### When Needed
**MCP server returns errors on standard OAuth metadata endpoint** (`/.well-known/oauth-authorization-server`) but exposes working OIDC endpoint.

### Solution
**Set `authServerMetadataUrl` in `oauth` object** of server's config in `.mcp.json`.

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

**Requirements**:
- URL must use `https://`
- Requires Claude Code v2.1.64 or later

---

## 📥 Add MCP Servers from JSON Configuration

### Syntax
```bash
# Basic syntax
claude mcp add-json <name> '<json>'

# Example: Adding an HTTP server with JSON configuration
claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

# Example: Adding a stdio server with JSON configuration
claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

# Example: Adding an HTTP server with pre-configured OAuth credentials
claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
```

### Verify
```bash
claude mcp get weather-api
```

### Tips
- **Properly escape JSON** in your shell
- **JSON must conform to MCP server configuration schema**
- **Use `--scope user`** to add to user configuration

---

## 📨 Import MCP Servers from Claude Desktop

### Syntax
```bash
# Basic syntax
claude mcp add-from-claude-desktop
```

### Steps
1. **Run command** → interactive dialog appears
2. **Select which servers to import**
3. **Verify**: `claude mcp list`

### Tips
- **Only works on macOS and Windows Subsystem for Linux (WSL)**
- **Reads Claude Desktop configuration file** from standard location
- **Use `--scope user`** to add to user configuration
- **Imported servers have same names as in Claude Desktop**
- **If servers with same names exist** → get numerical suffix (e.g., `server_1`)

---

## ☁️ Use MCP Servers from Claude.ai

### How It Works
**If logged into Claude Code with Claude.ai account** → MCP servers added in Claude.ai automatically available.

### Steps
1. **Configure MCP servers in Claude.ai** → `claude.ai/settings/connectors`
2. **Complete authentication** in Claude.ai
3. **View and manage** in Claude Code → `/mcp`

**Claude.ai servers appear with indicators** showing they come from Claude.ai.

### Disable
```bash
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

---

## 🎭 Use Claude Code as an MCP Server

### Start as stdio MCP Server
```bash
# Start Claude as a stdio MCP server
claude mcp serve
```

### Use in Claude Desktop
**Add to `claude_desktop_config.json`**:
```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

### Configuring Executable Path
**If `claude` not in PATH** → specify full path.

**Find full path**:
```bash
which claude
```

**Use full path**:
```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "/full/path/to/claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

**Without correct path** → error: `spawn claude ENOENT`.

### Tips
- **Server provides access to Claude's tools** (View, Edit, LS, etc.)
- **In Claude Desktop** → ask Claude to read files, make edits, etc.
- **MCP server only exposes Claude Code's tools** → client responsible for user confirmation

---

## 📊 MCP Output Limits and Warnings

### Output Management
**When MCP tools produce large outputs** → Claude Code helps manage token usage.

### Thresholds
- **Warning threshold**: 10,000 tokens
- **Default maximum**: 25,000 tokens
- **Configurable limit**: `MAX_MCP_OUTPUT_TOKENS` environment variable

### Increase Limit
```bash
# Set a higher limit for MCP tool outputs
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

### Use Cases
**Particularly useful for**:
- Querying large datasets or databases
- Generating detailed reports or documentation
- Processing extensive log files or debugging information

**If frequently encounter warnings** → increase limit or configure server to paginate/filter.

---

## 📝 Respond to MCP Elicitation Requests

### What is Elicitation?
**MCP servers can request structured input mid-task** → Claude Code displays interactive dialog, passes response back.

### Two Modes

#### 1. Form Mode
**Claude Code shows dialog with form fields** defined by server (e.g., username and password prompt).

**Fill in fields and submit**.

#### 2. URL Mode
**Claude Code opens browser URL** for authentication or approval.

**Complete flow in browser** → confirm in CLI.

### Auto-Respond
**To auto-respond without showing dialog** → use **Elicitation hook**.

**For MCP server authors** → see MCP elicitation specification.

---

## 📚 Use MCP Resources

### Reference MCP Resources
**MCP servers can expose resources** → reference using `@` mentions.

#### 1. List Available Resources
**Type `@` in prompt** → see available resources from all connected MCP servers.

**Resources appear alongside files** in autocomplete menu.

#### 2. Reference Specific Resource
**Use format**: `@server:protocol://resource/path`

```bash
Can you analyze @github:issue://123 and suggest a fix?
```

```bash
Please review the API documentation at @docs:file://api/authentication
```

#### 3. Multiple Resource References
**Reference multiple resources in single prompt**:
```bash
Compare @postgres:schema://users with @docs:file://database/user-model
```

### Tips
- **Resources automatically fetched and included as attachments**
- **Resource paths are fuzzy-searchable** in `@` mention autocomplete
- **Claude Code automatically provides tools** to list and read MCP resources when servers support them
- **Resources can contain any type of content** (text, JSON, structured data, etc.)

---

## 🔍 Scale with MCP Tool Search

### Problem
**When many MCP servers configured** → tool definitions can consume significant portion of context window.

### Solution
**MCP Tool Search** → dynamically load tools on-demand instead of preloading all.

### How It Works
**Claude Code automatically enables Tool Search** when MCP tool descriptions would consume >10% of context window.

**When triggered**:
1. **MCP tools deferred** rather than loaded upfront
2. **Claude uses search tool** to discover relevant MCP tools when needed
3. **Only tools actually needed** loaded into context
4. **MCP tools work exactly as before** from your perspective

### For MCP Server Authors
**Server instructions field becomes more useful** with Tool Search enabled.

**Add clear, descriptive server instructions**:
- What category of tasks your tools handle
- When Claude should search for your tools
- Key capabilities your server provides

### Configure Tool Search

| Value | Behavior |
|-------|----------|
| (unset) | Enabled by default. Disabled when `ANTHROPIC_BASE_URL` is non-first-party host |
| `true` | Always enabled, including for non-first-party `ANTHROPIC_BASE_URL` |
| `auto` | Activates when MCP tools exceed 10% of context |
| `auto:<N>` | Activates at custom threshold (e.g., `auto:5` for 5%) |
| `false` | Disabled, all MCP tools loaded upfront |

```bash
# Use a custom 5% threshold
ENABLE_TOOL_SEARCH=auto:5 claude

# Disable tool search entirely
ENABLE_TOOL_SEARCH=false claude
```

**Or set in `settings.json` env field**.

### Disable MCPSearch Tool
```json
{
  "permissions": {
    "deny": ["MCPSearch"]
  }
}
```

### Requirements
**Models that support `tool_reference` blocks**: Sonnet 4+, Opus 4+.

**Haiku models do not support tool search**.

---

## 🎯 Use MCP Prompts as Commands

### Execute MCP Prompts

#### 1. Discover Available Prompts
**Type `/`** → see all available commands, including from MCP servers.

**MCP prompts format**: `/mcp__servername__promptname`

#### 2. Execute Prompt Without Arguments
```
/mcp__github__list_prs
```

#### 3. Execute Prompt With Arguments
**Pass space-separated after command**:
```
/mcp__github__pr_review 456
```

```
/mcp__jira__create_issue "Bug in login flow" high
```

### Tips
- **MCP prompts dynamically discovered** from connected servers
- **Arguments parsed based on prompt's defined parameters**
- **Prompt results injected directly into conversation**
- **Server and prompt names normalized** (spaces become underscores)

---

## 🏢 Managed MCP Configuration

### Two Options

#### Option 1: Exclusive Control with `managed-mcp.json`
**Deploy fixed set of MCP servers** → users cannot modify or extend.

**System-wide paths**:
- **macOS**: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- **Linux and WSL**: `/etc/claude-code/managed-mcp.json`
- **Windows**: `C:\Program Files\ClaudeCode\managed-mcp.json`

**Same format as `.mcp.json`**:
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

#### Option 2: Policy-Based Control with Allowlists/Denylists
**Allow users to configure their own servers** while enforcing restrictions.

**Restriction options**:
- **By server name** (`serverName`)
- **By command** (`serverCommand`) - for stdio servers
- **By URL pattern** (`serverUrl`) - for remote servers

**Each entry must have exactly one** of these.

### Example Configuration
```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "sentry" },
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    { "serverName": "dangerous-server" },
    { "serverCommand": ["npx", "-y", "unapproved-package"] },
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

### How Command-Based Restrictions Work

#### Exact Matching
**Command arrays must match exactly** - both command and all arguments in correct order.

**Example**: `["npx", "-y", "server"]` will NOT match `["npx", "server"]` or `["npx", "-y", "server", "--flag"]`.

#### Stdio Server Behavior
**When allowlist contains any `serverCommand` entries** → stdio servers must match one of those commands.

**Stdio servers cannot pass by name alone** when command restrictions present.

#### Non-Stdio Server Behavior
**Remote servers (HTTP, SSE, WebSocket)** → use URL-based matching when `serverUrl` entries exist.

**If no URL entries** → remote servers fall back to name-based matching.

**Command restrictions do not apply to remote servers**.

### How URL-Based Restrictions Work

#### Wildcard Support
**URL patterns support `*` to match any sequence of characters**.

**Examples**:
- `https://mcp.company.com/*` → Allow all paths on specific domain
- `https://*.example.com/*` → Allow any subdomain of example.com
- `http://localhost:*/*` → Allow any port on localhost

#### Remote Server Behavior
**When allowlist contains any `serverUrl` entries** → remote servers must match one of those URL patterns.

**Remote servers cannot pass by name alone** when URL restrictions present.

### Allowlist Behavior

| Value | Behavior |
|-------|----------|
| **undefined (default)** | No restrictions - users can configure any MCP server |
| **Empty array []** | Complete lockdown - users cannot configure any MCP servers |
| **List of entries** | Users can only configure servers that match by name, command, or URL pattern |

### Denylist Behavior

| Value | Behavior |
|-------|----------|
| **undefined (default)** | No servers blocked |
| **Empty array []** | No servers blocked |
| **List of entries** | Specified servers explicitly blocked across all scopes |

### Important Notes
- **Option 1 and 2 can be combined**: If `managed-mcp.json` exists, it has exclusive control
- **Denylist takes absolute precedence**: Server matching denylist blocked even if on allowlist
- **Restrictions work together**: Server passes if it matches either name, command, or URL (unless blocked by denylist)
- **With `managed-mcp.json`**: Users cannot add MCP servers through `claude mcp add` or config files

---

## 💡 学习感悟

### 1. **MCP 是 Claude Code 连接外部世界的桥梁**
**核心能力**:
- 工具（tools）
- 数据库（databases）
- APIs

**通过标准化协议** → 连接数百种外部工具和数据源。

### 2. **三种 Transport 方式**
**HTTP (推荐)** → 远程 servers，最广泛支持
**SSE (已弃用)** → 远程 servers，使用 HTTP 代替
**Stdio** → 本地 processes，适合系统访问

**选择依据**: 远程 vs 本地。

### 3. **三种 Scope 决定可见性**
**Local** (默认) → 仅当前项目，私有
**Project** → 团队共享，`.mcp.json` 提交到 VCS
**User** → 跨项目共享，个人工具

**优先级**: Local > Project > User

### 4. **OAuth 2.0 认证是云服务的标准**
**自动认证**: `/mcp` → 浏览器登录
**预配置 credentials**: `--client-id` + `--client-secret`
**Fixed callback port**: `--callback-port` 匹配预注册的 redirect URI

**灵活支持各种认证场景**。

### 5. **Plugin-Provided MCP Servers 简化分发**
**自动启动** → plugin enabled 时
**无需手动配置** → bundled with plugin
**团队一致性** → 所有人获得相同工具

**这是分发 MCP servers 的最佳方式**。

### 6. **Environment Variable Expansion 支持团队协作**
**在 `.mcp.json` 中使用 `${VAR}` 和 `${VAR:-default}`**

**Expansion locations**: command, args, env, url, headers

**好处**: 共享配置 + 机器特定路径和敏感值保持灵活。

### 7. **MCP Tool Search 解决上下文窗口限制**
**动态加载** → 工具按需发现和加载
**Threshold**: 10% context window (可配置)
**Server instructions** 更重要 → 帮助 Claude 知道何时搜索

**这是扩展性的关键**。

### 8. **MCP Prompts as Commands 提供便利**
**格式**: `/mcp__servername__promptname`
**参数**: 空格分隔，基于定义的参数解析
**结果**: 直接注入到对话中

**这是 prompt 的 CLI 封装**。

### 9. **Managed MCP Configuration 是企业控制的核心**
**Option 1**: `managed-mcp.json` → exclusive control (users 不能修改)
**Option 2**: Allowlists/Denylists → policy-based control (users 可以添加，但受限制)

**Restriction options**: serverName, serverCommand, serverUrl

**Denylist takes absolute precedence**.

### 10. **Claude Code 本身可以作为 MCP Server**
**`claude mcp serve`** → stdio MCP server
**在 Claude Desktop 中使用** → 通过 Claude Code 的工具

**这是 Claude Code 的 meta capability**。

---

## 🎯 实践建议

### 1. **Start with HTTP Servers for Remote Services**
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

**Most widely supported** → 推荐。

### 2. **Use Project Scope for Team Collaboration**
```bash
claude mcp add --transport http jira --scope project https://mcp.jira.com/mcp
```

**Check into VCS** → 团队共享。

### 3. **Authenticate with /mcp**
```
/mcp
```

**Browser-based OAuth** → 简单安全。

### 4. **Use Env Var Expansion for Sensitive Values**
**In `.mcp.json`**:
```json
{
  "headers": {
    "Authorization": "Bearer ${API_KEY}"
  }
}
```

**Keep secrets out of VCS**。

### 5. **Import from Claude Desktop if Already Configured**
```bash
claude mcp add-from-claude-desktop
```

**Avoid re-configuration**。

### 6. **Use MCP Resources with @ Mentions**
```
Analyze @github:issue://123 and suggest a fix.
```

**Natural way to reference external resources**。

### 7. **Use MCP Prompts as Commands**
```
/mcp__github__pr_review 456
```

**Convenient shortcuts for common tasks**。

### 8. **Configure Tool Search for Many Servers**
```bash
ENABLE_TOOL_SEARCH=auto:5 claude
```

**Save context window** → dynamic loading。

### 9. **Use Managed Configuration for Enterprise Control**
**`managed-mcp.json`** → exclusive control
**Allowlists/Denylists** → policy-based control

**Choose based on need for user customization**。

### 10. **Use Claude Code as MCP Server for Other Apps**
```bash
claude mcp serve
```

**Expose Claude Code's tools to other MCP clients**。

---

## 📚 Popular MCP Servers

### Issue Trackers
- **Jira** - Issue tracking
- **Linear** - Project management
- **GitHub** - Code hosting
- **GitLab** - Code hosting

### Databases
- **PostgreSQL** - Relational database
- **MySQL** - Relational database
- **MongoDB** - NoSQL database

### Communication
- **Slack** - Team messaging
- **Gmail** - Email

### Monitoring
- **Sentry** - Error tracking
- **Statsig** - Feature flags and analytics

### Design
- **Figma** - Design tool

### Storage
- **Notion** - Knowledge base
- **Airtable** - Database/spreadsheet hybrid

### Development
- **Filesystem** - Local file access
- **Memory** - Persistent memory

---

## 🏷️ 标签
`#mcp` `#model-context-protocol` `#integrations` `#tools` `#oauth` `#scopes` `#transports` `#http` `#stdio` `#managed-configuration` `#tool-search` `#resources` `#prompts`
