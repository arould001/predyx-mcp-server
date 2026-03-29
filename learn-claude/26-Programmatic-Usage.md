# 26 - Run Claude Code Programmatically 学习笔记

**学习时间**：2026-03-14 17:10
**页面地址**：https://code.claude.com/docs/en/programmatic-usage

---

## 📖 核心概念

### 是什么
**Agent SDK** 让你可以通过 CLI、Python 或 TypeScript **programmatic 运行 Claude Code**。

### 能力
- Same tools, agent loop, context management as Claude Code
- **CLI**: Scripts and CI/CD
- **Python/TypeScript packages**: Full programmatic control

### Note
- CLI was previously called "headless mode"
- `-p` flag and all CLI options work the same way
- This page covers CLI (`claude -p`)
- For Python/TypeScript SDK packages → see full Agent SDK documentation

---

## 🚀 Basic Usage

### The -p Flag
**Add `-p` (or `--print`) to any `claude` command** to run non-interactively.

**All CLI options work with `-p`**:
- `--continue` for continuing conversations
- `--allowedTools` for auto-approving tools
- `--output-format` for structured output

### Example
```bash
claude -p "What does the auth module do?"
```

**Ask Claude a question about codebase and print response**.

---

## 💡 Examples

### 1. Get Structured Output

#### Output Formats
**Use `--output-format` to control response format**:
- **text** (default): Plain text output
- **json**: Structured JSON with result, session ID, metadata
- **stream-json**: Newline-delimited JSON for real-time streaming

#### JSON Output Example
```bash
claude -p "Summarize this project" --output-format json
```

**Returns**:
```json
{
  "result": "Project summary...",
  "session_id": "...",
  "metadata": {...}
}
```

#### JSON Schema
**Use `--json-schema` with JSON Schema definition** for specific schema.

**Example** (extract function names as array):
```bash
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

**Response**: Metadata in root, structured output in `structured_output` field.

#### Parse with jq
```bash
# Extract text result
claude -p "Summarize this project" --output-format json | jq -r '.result'

# Extract structured output
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```

### 2. Stream Responses

#### Stream JSON
**Use `--output-format stream-json` with `--verbose` and `--include-partial-messages`**.

**Each line is JSON object** representing an event.

```bash
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

#### Filter Text Deltas
**Use jq to filter for text deltas**:

```bash
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

**Explanation**:
- `-r`: Raw strings (no quotes)
- `-j`: Join without newlines
- Tokens stream continuously

**For programmatic streaming** → see Agent SDK docs (callbacks, message objects).

### 3. Auto-Approve Tools

#### --allowedTools
**Let Claude use tools without prompting**.

```bash
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

**Claude can**:
- Execute Bash commands
- Read files
- Edit files

**All without asking for permission**.

### 4. Create a Commit

#### Example
```bash
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

#### Permission Rule Syntax
**`--allowedTools` uses permission rule syntax**:
- `Bash(git diff *)` → allows any command starting with `git diff`
- Trailing `*` enables prefix matching
- **Space before `*` is important**:
  - ✅ `Bash(git diff *)` → matches `git diff`, `git diff --cached`, etc.
  - ❌ `Bash(git diff*)` → would also match `git diff-index`

#### Note
**User-invoked skills like `/commit` and built-in commands** only available in **interactive mode**.

**In `-p` mode**: Describe the task you want to accomplish instead.

### 5. Customize System Prompt

#### --append-system-prompt
**Add instructions while keeping Claude Code's default behavior**.

```bash
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

**Example**:
- Pipe PR diff to Claude
- Instruct to review for security vulnerabilities
- Return JSON output

#### Other System Prompt Flags
**See system prompt flags** for more options, including:
- `--system-prompt` to fully replace default prompt

### 6. Continue Conversations

#### --continue
**Continue most recent conversation**.

```bash
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

#### --resume
**Resume specific conversation with session ID**.

```bash
# Capture session ID
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')

# Resume specific conversation
claude -p "Continue that review" --resume "$session_id"
```

**Use case**: Running multiple conversations, need to resume specific one.

---

## 📚 Next Steps

### Agent SDK Quickstart
**Build your first agent with Python or TypeScript** → see Agent SDK docs.

### CLI Reference
**All CLI flags and options** → see CLI reference.

### GitHub Actions
**Use Agent SDK in GitHub workflows** → see GitHub Actions docs.

### GitLab CI/CD
**Use Agent SDK in GitLab pipelines** → see GitLab CI/CD docs.

---

## 💡 学习感悟

### 1. **Agent SDK 是 Programmatic 控制的核心**
**三种方式**:
- **CLI** (`claude -p`): Scripts, CI/CD
- **Python SDK**: Full programmatic control
- **TypeScript SDK**: Full programmatic control

**CLI 最简单** → 适合快速集成。

### 2. **-p Flag 是 CLI 的关键**
**`-p` or `--print`** → non-interactive mode.

**All CLI options work**:
- `--continue` / `--resume` → conversation continuity
- `--allowedTools` → auto-approve tools
- `--output-format` → structured output
- `--json-schema` → enforce schema
- `--append-system-prompt` → customize prompt

### 3. **Structured Output 是核心能力**
**Three formats**:
- **text**: Plain text (default)
- **json**: Structured JSON (result, session_id, metadata)
- **stream-json**: Real-time streaming (newline-delimited)

**JSON Schema** → enforce specific schema.

**Parse with jq** → extract fields.

### 4. **Stream JSON for Real-Time**
**`--output-format stream-json`** + `--verbose` + `--include-partial-messages`.

**Each line = JSON event**.

**Filter with jq**:
```bash
jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

**Tokens stream continuously**.

### 5. **--allowedTools Auto-Approves Tools**
**Permission rule syntax**:
- `Bash,Read,Edit` → approve multiple tools
- `Bash(git diff *)` → approve specific commands with prefix matching
- **Space before `*` is important**

**Use case**: CI/CD, automated workflows.

### 6. **/commit Not Available in -p Mode**
**User-invoked skills and built-in commands** → only in interactive mode.

**In `-p` mode**: Describe task explicitly.

**Example**:
```bash
# Interactive mode
/commit

# -p mode
claude -p "Look at staged changes and create commit" --allowedTools "Bash(git *)"
```

### 7. **--append-system-prompt Customizes Behavior**
**Add instructions** while keeping default behavior.

**Example**:
```bash
claude -p "Review code" --append-system-prompt "You are a security engineer."
```

**vs `--system-prompt`**: Replaces default entirely.

### 8. **Conversation Continuity with --continue/--resume**
**`--continue`** → most recent conversation.
**`--resume <session_id>`** → specific conversation.

**Capture session ID**:
```bash
session_id=$(claude -p "..." --output-format json | jq -r '.session_id')
```

**Use case**: Multi-turn programmatic workflows.

### 9. **CLI vs Python/TypeScript SDK**
**CLI** (`claude -p`):
- Simple, script-friendly
- CI/CD integration
- Limited to CLI options

**Python/TypeScript SDK**:
- Full programmatic control
- Structured outputs
- Tool approval callbacks
- Native message objects
- Streaming with callbacks

**Choose based on complexity**:
- Simple → CLI
- Complex → SDK

### 10. **Pipeline Pattern is Powerful**
**Pipe input + `claude -p` + structured output**.

**Example** (PR review):
```bash
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer." \
  --output-format json | jq '.result'
```

**Works with any CLI tool** → very flexible.

---

## 🎯 实践建议

### 1. **Use -p for CI/CD**
**Example** (run tests and fix):
```bash
claude -p "Run test suite and fix failures" \
  --allowedTools "Bash,Read,Edit" \
  --output-format json
```

**Parse result** → check if successful.

### 2. **Use JSON Schema for Structured Data**
**Example** (extract functions):
```bash
claude -p "Extract function names" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

**Guaranteed structure** → easier to process.

### 3. **Use Stream JSON for Real-Time Feedback**
**Example** (continuous output):
```bash
claude -p "Explain code" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

**Tokens stream as generated** → better UX.

### 4. **Use --allowedTools for Automation**
**Example** (git commit):
```bash
claude -p "Create commit from staged changes" \
  --allowedTools "Bash(git diff *),Bash(git status *),Bash(git commit *)"
```

**No manual approval** → fully automated.

### 5. **Use --append-system-prompt for Role-Specific Tasks**
**Example** (security review):
```bash
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities."
```

**Add expertise without replacing default behavior**.

### 6. **Capture Session ID for Multi-Turn Workflows**
```bash
# Start conversation
session_id=$(claude -p "Start review" --output-format json | jq -r '.session_id')

# Continue conversation
claude -p "Focus on database" --resume "$session_id"
claude -p "Generate summary" --resume "$session_id"
```

**Maintain context across multiple calls**.

### 7. **Use jq to Parse JSON Output**
**Extract specific fields**:
```bash
# Text result
claude -p "Summarize project" --output-format json | jq -r '.result'

# Session ID
claude -p "Start review" --output-format json | jq -r '.session_id'

# Structured output
claude -p "Extract functions" --output-format json --json-schema '...' | jq '.structured_output'
```

**jq is your friend** → learn basics.

### 8. **Pipeline with Other CLI Tools**
**Example** (PR review):
```bash
gh pr diff 123 | claude -p "Review for security" --append-system-prompt "You are a security engineer."
```

**Works with**:
- `git diff`
- `gh` (GitHub CLI)
- `glab` (GitLab CLI)
- Any CLI tool that outputs text

### 9. **Use --continue for Quick Follow-Ups**
```bash
# First request
claude -p "Review codebase"

# Follow-up
claude -p "Focus on authentication" --continue
claude -p "Generate report" --continue
```

**Simpler than managing session IDs**.

### 10. **Consider SDK for Complex Workflows**
**CLI limitations**:
- Text-based output
- No callbacks
- Limited programmatic control

**SDK advantages**:
- Structured outputs
- Tool approval callbacks
- Native message objects
- Streaming with callbacks

**Choose based on needs**:
- Simple/CI/CD → CLI
- Complex/programmatic → SDK

---

## 🔄 vs Interactive Mode

| Feature | Interactive Mode | -p Mode |
|---------|-----------------|---------|
| **User skills** (`/commit`, `/review-pr`) | ✅ Available | ❌ Not available |
| **Built-in commands** | ✅ Available | ❌ Not available |
| **Tool approval** | Manual or configured | `--allowedTools` |
| **Output format** | Text in terminal | Text/JSON/Stream JSON |
| **Conversation** | Interactive turns | Single request or `--continue`/`--resume` |
| **System prompt** | Configured via settings | `--append-system-prompt` or `--system-prompt` |
| **Use case** | Interactive development | CI/CD, scripts, automation |

**Choose based on use case**:
- **Development** → Interactive mode
- **Automation** → `-p` mode

---

## 📚 Use Cases

### 1. Code Review in CI/CD
```bash
# Review PR
gh pr diff "$PR_NUMBER" | claude -p \
  --append-system-prompt "You are a senior engineer. Review for code quality, security, and performance." \
  --output-format json
```

### 2. Automated Testing and Fixes
```bash
# Run tests and fix failures
claude -p "Run test suite and fix any failures" \
  --allowedTools "Bash(npm test),Read,Edit" \
  --output-format json
```

### 3. Generate Documentation
```bash
# Generate API docs
claude -p "Generate API documentation for all endpoints in src/api/" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"endpoints":{"type":"array","items":{"type":"object"}}}}'
```

### 4. Security Audit
```bash
# Security scan
claude -p "Scan codebase for security vulnerabilities" \
  --append-system-prompt "You are a security auditor. Check for OWASP Top 10 vulnerabilities." \
  --allowedTools "Read,Grep" \
  --output-format json
```

### 5. Refactoring Assistant
```bash
# Multi-turn refactoring
session_id=$(claude -p "Analyze codebase for code smells" --output-format json | jq -r '.session_id')
claude -p "Refactor the most critical issues" --resume "$session_id"
claude -p "Run tests to verify changes" --resume "$session_id"
```

### 6. Git Automation
```bash
# Smart commit
git add -A
claude -p "Look at staged changes and create appropriate commit" \
  --allowedTools "Bash(git diff --cached *),Bash(git status *),Bash(git commit *)"
```

---

## 🏷️ 标签
`#programmatic-usage` `#agent-sdk` `#cli` `#-p-flag` `#structured-output` `#json-schema` `#stream-json` `#--allowedTools` `#automation` `#ci-cd`
