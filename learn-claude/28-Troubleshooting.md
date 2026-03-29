# 28 - Troubleshooting 学习笔记

**学习时间**：2026-03-14 17:28
**页面地址**：https://code.claude.com/docs/en/troubleshooting

---

## 📖 核心概念

### 是什么
**Troubleshooting** 页面提供 Claude Code 安装和使用中常见问题的解决方案。

### 免终端选项
**Claude Code Desktop app** → 通过图形界面安装和使用，无需命令行。

---

## 🚨 Installation Issues Quick Reference

| Symptom | Solution |
|---------|----------|
| `command not found: claude` | Fix your PATH |
| `syntax error near unexpected token '<'` | Install script returns HTML |
| `curl: (56) Failure writing output to destination` | Download script first, then run |
| `Killed during install on Linux` | Add swap space for low-memory servers |
| `TLS connect error` or `SSL/TLS secure channel` | Update CA certificates |
| `Failed to fetch version` | Check network and proxy settings |
| `irm is not recognized` or `&& is not valid` | Use the right command for your shell |
| `Claude Code on Windows requires git-bash` | Install or configure Git Bash |
| `Error loading shared library` | Wrong binary variant for your system |
| `Illegal instruction on Linux` | Architecture mismatch |
| `dyld: cannot load` or `Abort trap on macOS` | Binary incompatibility |
| `Invoke-Expression: Missing argument in parameter list` | Install script returns HTML |
| `App unavailable in region` | Claude Code not available in your country |
| `unable to get local issuer certificate` | Configure corporate CA certificates |
| OAuth error or 403 Forbidden | Fix authentication |

---

## 🔍 Debug Installation Problems

### 1. Check Network Connectivity
**Verify you can reach Google Cloud Storage**:
```bash
curl -sI https://storage.googleapis.com
```

**If fails** → network may be blocking connection.

**Common causes**:
- Corporate firewalls/proxies blocking Google Cloud Storage
- Regional network restrictions → try VPN
- TLS/SSL issues → update CA certificates or check `HTTPS_PROXY`

**Corporate proxy setup**:
```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### 2. Verify Your PATH
**Check if install directory is in PATH**:
```bash
# macOS/Linux
echo $PATH | tr ':' '\n' | grep local/bin

# Windows PowerShell
$env:PATH -split ';' | Select-String local\\bin

# Windows CMD
echo %PATH% | findstr local
```

**If no output** → add to shell configuration:
```bash
# Zsh (macOS default)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Bash (Linux default)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Verify fix**:
```bash
claude --version
```

### 3. Check for Conflicting Installations
**List all claude binaries in PATH**:
```bash
# macOS/Linux
which -a claude

# Check for native installer and npm versions
ls -la ~/.local/bin/claude
ls -la ~/.claude/local/
npm -g ls @anthropic-ai/claude-code 2>/dev/null
```

**If multiple installations** → keep only one.

**Remove extra installations**:
```bash
# Uninstall npm global install
npm uninstall -g @anthropic-ai/claude-code

# Remove Homebrew install on macOS
brew uninstall --cask claude-code
```

### 4. Check Directory Permissions
**Check if directories are writable**:
```bash
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

**If not writable** → create and set ownership:
```bash
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### 5. Verify the Binary Works
**Confirm binary exists and is executable**:
```bash
ls -la $(which claude)
```

**Check for missing shared libraries (Linux)**:
```bash
ldd $(which claude) | grep "not found"
```

**Run sanity check**:
```bash
claude --version
```

---

## 🛠️ Common Installation Issues

### 1. Install Script Returns HTML
**Symptoms**:
```bash
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

**PowerShell**:
```powershell
Invoke-Expression: Missing argument in parameter list.
```

**Cause**: Install URL returned HTML page instead of script.

**If HTML says "App unavailable in region"** → Claude Code not available in your country.

**Solutions**:
- Use alternative install method:
  ```bash
  # macOS/Linux
  brew install --cask claude-code

  # Windows
  winget install Anthropic.ClaudeCode
  ```
- Retry after a few minutes (often temporary)

### 2. command not found: claude After Installation
**Symptoms**:
- **macOS**: `zsh: command not found: claude`
- **Linux**: `bash: claude: command not found`
- **Windows CMD**: `'claude' is not recognized as an internal or external command`
- **PowerShell**: `claude : The term 'claude' is not recognized`

**Cause**: Install directory not in shell's search path.

**Solution**: See "Verify Your PATH" above.

### 3. curl: (56) Failure writing output to destination
**Cause**: Connection broke before script finished downloading.

**Solutions**:
- Check network stability:
  ```bash
  curl -fsSL https://storage.googleapis.com -o /dev/null
  ```
- Try alternative install method (Homebrew/WinGet)

### 4. TLS or SSL Connection Errors
**Symptoms**:
- `curl: (35) TLS connect error`
- `schannel: next InitializeSecurityContext failed`
- `Could not establish trust relationship for the SSL/TLS secure channel`

**Solutions**:
- Update CA certificates:
  ```bash
  # Ubuntu/Debian
  sudo apt-get update && sudo apt-get install ca-certificates

  # macOS via Homebrew
  brew install ca-certificates
  ```
- Enable TLS 1.2 in PowerShell:
  ```powershell
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  irm https://claude.ai/install.ps1 | iex
  ```
- Set corporate CA certificate:
  ```bash
  export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
  ```

### 5. Failed to Fetch Version from storage.googleapis.com
**Cause**: `storage.googleapis.com` blocked on network.

**Solutions**:
- Test connectivity:
  ```bash
  curl -sI https://storage.googleapis.com
  ```
- Set proxy:
  ```bash
  export HTTPS_PROXY=http://proxy.example.com:8080
  curl -fsSL https://claude.ai/install.sh | bash
  ```
- Try different network/VPN or alternative install method

### 6. Windows: irm or && Not Recognized
**Symptom**: `'irm' is not recognized` or `The token '&&' is not valid`

**Cause**: Running wrong command for shell.

**Solutions**:
- **irm not recognized** (in CMD):
  - Open PowerShell and run:
    ```powershell
    irm https://claude.ai/install.ps1 | iex
    ```
  - Or use CMD installer:
    ```cmd
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
- **&& not valid** (in PowerShell but ran CMD command):
  ```powershell
  irm https://claude.ai/install.ps1 | iex
  ```

### 7. Install Killed on Low-Memory Linux Servers
**Symptom**:
```bash
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

**Cause**: Linux OOM killer terminated process (out of memory).

**Solutions**:
- Add swap space (2 GB):
  ```bash
  sudo fallocate -l 2G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  ```
- Close other processes to free memory
- Use larger instance (Claude Code requires at least 4 GB RAM)

### 8. Install Hangs in Docker
**Cause**: Installing as root into `/` causes excessive memory usage.

**Solutions**:
- Set working directory before installer:
  ```dockerfile
  WORKDIR /tmp
  RUN curl -fsSL https://claude.ai/install.sh | bash
  ```
- Increase Docker memory limits:
  ```bash
  docker build --memory=4g .
  ```

### 9. Windows: Claude Desktop Overrides claude CLI
**Symptom**: Running `claude` opens Desktop app instead of CLI.

**Cause**: Older Claude Desktop registers `Claude.exe` in WindowsApps with PATH priority.

**Solution**: Update Claude Desktop to latest version.

### 10. Windows: "Claude Code on Windows requires git-bash"
**Solutions**:
- Install Git for Windows from git-scm.com/downloads/win
- During setup, select "Add to PATH"
- Restart terminal after installing
- If Git installed but not found, set path in `settings.json`:
  ```json
  {
    "env": {
      "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
    }
  }
  ```

### 11. Linux: Wrong Binary Variant (musl/glibc mismatch)
**Symptom**:
```bash
Error loading shared library libstdc++.so.6: No such file or directory
```

**Cause**: Installer downloaded wrong binary variant (musl vs glibc).

**Solutions**:
- Check which libc:
  ```bash
  ldd /bin/ls | head -1
  ```
  - `linux-vdso.so` or `/lib/x86_64-linux-gnu/` → glibc
  - `musl` → musl
- If glibc but got musl binary → remove and reinstall
- If musl (Alpine Linux):
  ```bash
  apk add libgcc libstdc++ ripgrep
  ```

### 12. Illegal Instruction on Linux
**Symptom**:
```bash
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**Cause**: Binary doesn't match CPU architecture.

**Solutions**:
- Verify architecture:
  ```bash
  uname -m
  ```
  - `x86_64` → 64-bit Intel/AMD
  - `aarch64` → ARM64
- Try alternative install method:
  ```bash
  brew install --cask claude-code
  ```

### 13. dyld: cannot load on macOS
**Symptom**:
```bash
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**Cause**: Binary incompatible with macOS version or hardware.

**Solutions**:
- Check macOS version (requires 13.0+)
- Update macOS if on older version
- Try Homebrew:
  ```bash
  brew install --cask claude-code
  ```

### 14. WSL Installation Issues

#### OS/Platform Detection Issues
**Solutions**:
- Run `npm config set os linux` before installation
- Install with:
  ```bash
  npm install -g @anthropic-ai/claude-code --force --no-os-check
  ```
  (Do not use sudo)

#### Node Not Found Errors
**Cause**: WSL using Windows Node.js installation.

**Check**:
```bash
which npm
which node
```
Should point to Linux paths (`/usr/`) not Windows (`/mnt/c/`).

**Solution**: Install Node via Linux package manager or nvm.

#### nvm Version Conflicts
**Cause**: nvm installed in both WSL and Windows → version conflicts.

**Check**:
```bash
which npm
which node
```
If point to Windows paths → Windows versions being used.

**Solutions**:
- **Primary**: Ensure nvm properly loaded in shell:
  ```bash
  # Add to ~/.bashrc or ~/.zshrc
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
  ```
- **Alternative**: Adjust PATH order:
  ```bash
  export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
  ```

#### WSL2 Sandbox Setup
**Symptom**: "Sandbox requires socat and bubblewrap"

**Solution** (Ubuntu/Debian):
```bash
sudo apt-get install bubblewrap socat
```

**Note**: WSL1 does not support sandboxing.

### 15. Permission Errors During Installation
**Native installer fails with permission errors** → see "Check Directory Permissions".

**npm-specific permission errors** → switch to native installer:
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

---

## 🔐 Permissions and Authentication

### Repeated Permission Prompts
**Solution**: Allow specific tools to run without approval using `/permissions`.

### Authentication Issues
**Steps**:
1. Run `/logout` to sign out completely
2. Close Claude Code
3. Restart with `claude` and complete authentication again

**If browser doesn't open**:
- Press `c` to copy OAuth URL to clipboard
- Paste into browser manually

### OAuth Error: Invalid Code
**Cause**: Login code expired or truncated during copy-paste.

**Solutions**:
- Press Enter to retry and complete login quickly
- Type `c` to copy full URL if browser doesn't open automatically
- In remote/SSH session → copy URL from terminal and open in local browser

### 403 Forbidden After Login
**Symptom**: `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}`

**Solutions**:
- **Claude Pro/Max users**: Verify subscription active at `claude.ai/settings`
- **Console users**: Confirm account has "Claude Code" or "Developer" role assigned by admin
- **Behind proxy**: Corporate proxies can interfere → see network configuration

### OAuth Login Fails in WSL2
**Cause**: WSL can't open Windows browser.

**Solution**: Set `BROWSER` environment variable:
```bash
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

**Or**: Copy URL manually (press `c` when prompt appears).

### "Not Logged In" or Token Expired
**Cause**: OAuth token expired.

**Solution**: Run `/login` to re-authenticate.

**If happens frequently**: Check system clock accuracy (token validation depends on timestamps).

---

## ⚙️ Configuration File Locations

| File | Purpose |
|------|---------|
| `~/.claude/settings.json` | User settings (permissions, hooks, model overrides) |
| `.claude/settings.json` | Project settings (checked into source control) |
| `.claude/settings.local.json` | Local project settings (not committed) |
| `~/.claude.json` | Global state (theme, OAuth, MCP servers) |
| `.mcp.json` | Project MCP servers (checked into source control) |
| `managed-mcp.json` | Managed MCP servers |
| **Managed settings** | Server-managed, MDM/OS-level policies, or file-based |

**Note**: On Windows, `~` refers to user home directory (e.g., `C:\Users\YourName`).

### Resetting Configuration
**Remove configuration files**:
```bash
# Reset all user settings and state
rm ~/.claude.json
rm -rf ~/.claude/

# Reset project-specific settings
rm -rf .claude/
rm .mcp.json
```

**Warning**: Removes all settings, MCP servers, and session history.

---

## 🚀 Performance and Stability

### High CPU or Memory Usage
**Solutions**:
- Use `/compact` regularly to reduce context size
- Close and restart Claude Code between major tasks
- Add large build directories to `.gitignore`

### Command Hangs or Freezes
**Solutions**:
- Press `Ctrl+C` to attempt cancel
- If unresponsive → close terminal and restart

### Search and Discovery Issues
**Symptom**: Search tool, @file mentions, custom agents, custom skills not working.

**Solution**: Install system ripgrep:
```bash
# macOS (Homebrew)
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

Then set `USE_BUILTIN_RIPGREP=0` in environment.

### Slow or Incomplete Search Results on WSL
**Cause**: Disk read performance penalties across file systems on WSL.

**Solutions**:
- Submit more specific searches (reduce files searched)
- Move project to Linux filesystem (`/home/`) instead of Windows (`/mnt/c/`)
- Use native Windows instead of WSL

---

## 💻 IDE Integration Issues

### JetBrains IDE Not Detected on WSL2
**Cause**: WSL2's NAT networking or Windows Firewall blocking connection.

#### Option 1: Configure Windows Firewall (Recommended)
1. Find WSL2 IP address:
   ```bash
   wsl hostname -I
   # Example: 172.21.123.45
   ```

2. Open PowerShell as Administrator and create firewall rule:
   ```powershell
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```

3. Restart IDE and Claude Code

#### Option 2: Switch to Mirrored Networking
**Add to `.wslconfig` in Windows user directory**:
```ini
[wsl2]
networkingMode=mirrored
```

**Then restart WSL**: `wsl --shutdown` from PowerShell.

**Note**: These issues only affect WSL2. WSL1 uses host's network directly.

### Report Windows IDE Integration Issues
**Include in issue**:
- Environment type: native Windows (Git Bash) or WSL1/WSL2
- WSL networking mode (if applicable): NAT or mirrored
- IDE name and version
- Claude Code extension/plugin version
- Shell type: Bash, Zsh, PowerShell, etc.

### Escape Key Not Working in JetBrains IDE Terminals
**Cause**: Keybinding clash with JetBrains' default shortcuts.

**Solution**:
1. Go to **Settings → Tools → Terminal**
2. Either:
   - Uncheck "Move focus to the editor with Escape", or
   - Click "Configure terminal keybindings" and delete "Switch focus to Editor" shortcut
3. Apply changes

---

## 📝 Markdown Formatting Issues

### Missing Language Tags in Code Blocks
**Symptom**:
````markdown
```
function example() {
  return "hello";
}
```
````

**Instead of**:
````markdown
```javascript
function example() {
  return "hello";
}
```
````

**Solutions**:
- Ask Claude to add language tags
- Use post-processing hooks to detect and add missing tags
- Manually review generated markdown files

### Inconsistent Spacing and Formatting
**Solutions**:
- Request formatting corrections
- Use formatting tools (prettier, custom scripts)
- Specify formatting preferences in prompts or CLAUDE.md

### Reduce Markdown Formatting Issues
**Best practices**:
- Be explicit in requests (e.g., "properly formatted markdown with language-tagged code blocks")
- Use project conventions (document preferred markdown style in CLAUDE.md)
- Set up validation hooks (automatically verify and fix common issues)

---

## 🆘 Get More Help

### /bug Command
**Use `/bug` within Claude Code** to report problems directly to Anthropic.

### GitHub Repository
**Check GitHub for known issues**.

### /doctor Command
**Run `/doctor` to diagnose issues**.

**Checks**:
- Installation type, version, and search functionality
- Auto-update status and available versions
- Invalid settings files (malformed JSON, incorrect types)
- MCP server configuration errors
- Keybinding configuration problems
- Context usage warnings (large CLAUDE.md files, high MCP token usage, unreachable permission rules)
- Plugin and agent loading errors

### Ask Claude Directly
**Claude has built-in access to its documentation** → ask about capabilities and features.

---

## 💡 学习感悟

### 1. **Troubleshooting 是系统性的诊断过程**
**Debug 流程**:
1. Check network connectivity
2. Verify PATH
3. Check for conflicting installations
4. Check directory permissions
5. Verify binary works

**逐层排查** → 从网络到文件系统到二进制。

### 2. **安装问题占了大半篇幅**
**Most common issues**:
- PATH not configured
- Network/proxy issues
- Permission errors
- Architecture mismatches
- Binary incompatibilities

**这是用户遇到的最直接障碍**。

### 3. **WSL 有独特的问题集**
**WSL-specific issues**:
- OS/platform detection
- Node not found (Windows Node.js)
- nvm version conflicts
- Sandbox setup (bubblewrap, socat)
- IDE detection (firewall, networking modes)
- Search performance (disk I/O across filesystems)

**WSL 用户需要特别注意这些**。

### 4. **OAuth 认证有多点失败可能**
**Failure points**:
- Browser doesn't open
- Code expired or truncated
- 403 Forbidden (subscription/role issues)
- Token expired

**每种情况有对应的解决方案**。

### 5. **Configuration Files 有清晰的组织**
**Key locations**:
- User settings: `~/.claude/settings.json`
- Project settings: `.claude/settings.json`
- Global state: `~/.claude.json`
- MCP servers: `.mcp.json`

**理解这个结构有助于快速定位配置问题**。

### 6. **Performance 问题通常与上下文大小相关**
**Solutions**:
- Use `/compact` regularly
- Restart between major tasks
- Add large directories to `.gitignore`

**管理上下文窗口是关键**。

### 7. **IDE Integration 在 WSL2 需要特殊配置**
**Two options**:
- Configure Windows Firewall (recommended)
- Switch to mirrored networking

**理解 WSL2 的 NAT networking 是根本原因**。

### 8. **Markdown Formatting 是 Claude Code 的已知弱点**
**Issues**:
- Missing language tags in code blocks
- Inconsistent spacing

**Solutions**:
- Explicit requests
- Post-processing hooks
- Manual verification

**这是需要主动管理的问题**。

### 9. **/doctor 是强大的诊断工具**
**Checks**:
- Installation and version
- Settings validity
- MCP configuration
- Keybindings
- Context usage
- Plugin/agent errors

**一站式诊断** → very useful.

### 10. **Alternative Install Methods 是备胎**
**When standard install fails**:
- **macOS/Linux**: Homebrew (`brew install --cask claude-code`)
- **Windows**: WinGet (`winget install Anthropic.ClaudeCode`)

**记住这两个备选方案**。

---

## 🎯 实践建议

### 1. **Start with /doctor**
**Run `/doctor` first when troubleshooting**.

**Catches many common issues automatically**.

### 2. **Check PATH First for "command not found"**
**Most common installation issue** → add to shell configuration:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 3. **Use Alternative Install Methods as Backup**
**If standard install fails**:
```bash
# macOS/Linux
brew install --cask claude-code

# Windows
winget install Anthropic.ClaudeCode
```

### 4. **Configure Proxy Properly in Corporate Environments**
```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

**Set before installation**.

### 5. **Install ripgrep for Search**
```bash
# macOS
brew install ripgrep

# Set environment variable
export USE_BUILTIN_RIPGREP=0
```

**Fixes search/discovery issues**.

### 6. **Use /compact Regularly**
**Prevent high memory usage** → compact context window.

### 7. **For WSL2 IDE Integration, Configure Firewall**
```powershell
# Find WSL2 IP
wsl hostname -I

# Create firewall rule
New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
```

### 8. **Request Explicit Markdown Formatting**
**When generating markdown**:
- Ask for "properly formatted markdown with language-tagged code blocks"
- Document preferences in CLAUDE.md
- Set up validation hooks

### 9. **Check Configuration File Locations**
**Know where settings live**:
- User: `~/.claude/settings.json`
- Project: `.claude/settings.json`
- Global: `~/.claude.json`

### 10. **Use /bug to Report Issues**
**Direct channel to Anthropic** → helps improve Claude Code.

---

## 📚 Common Issues Summary

### Installation
- PATH not configured → add to shell config
- Network issues → check proxy/VPN
- Permission errors → check directory ownership
- Architecture mismatch → verify with `uname -m`
- Binary incompatibility → check OS version

### Authentication
- Browser doesn't open → copy URL manually (press `c`)
- Invalid code → retry quickly
- 403 Forbidden → check subscription/role
- Token expired → run `/login`

### Performance
- High memory → use `/compact`
- Search issues → install ripgrep
- Slow on WSL → move to Linux filesystem

### IDE Integration
- JetBrains not detected → configure firewall
- Escape key not working → adjust keybindings

### Markdown
- Missing language tags → request explicitly
- Inconsistent formatting → use hooks

---

## 🏷️ 标签
`#troubleshooting` `#installation` `#authentication` `#performance` `#ide-integration` `#markdown` `#diagnostics` `#wsl` `#proxy` `#path` `#firewall` `#/doctor` `#/bug`
