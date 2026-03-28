# MCP Registry Publishing Guide for Predyx MCP Server

**Created**: 2026-03-29 01:48 AM  
**Status**: Publishing process researched and documented  
**Repository**: https://github.com/arould001/predyx-mcp-server

---

## 📋 Overview

This guide documents the complete process for publishing Predyx MCP Server to the official MCP Registry.

**MCP Registry**: https://registry.modelcontextprotocol.io  
**GitHub Repository**: https://github.com/modelcontextprotocol/registry  
**API Status**: v0.1 (API freeze since 2025-10-24, stable)

---

## 🎯 Publishing Workflow

### Step 1: PyPI Package (Prerequisite)

**Status**: ⏳ Waiting for PyPI account registration

**Requirements**:
- ✅ PyPI account (https://pypi.org/account/register/)
- ✅ `setup.py` configured correctly
- ✅ `README.md` contains `<!-- mcp-name: io.github.arould001/predyx-mcp-server -->`

**Commands**:
```bash
# Build the package
python setup.py sdist bdist_wheel

# Upload to PyPI
twine upload dist/*

# Verify installation
pip install predyx-mcp-server
```

**Expected Result**:
- Package available at: https://pypi.org/project/predyx-mcp-server/
- Installable via: `pip install predyx-mcp-server`

---

### Step 2: Install mcp-publisher CLI

**Installation Options**:

#### Option A: Build from Source (Recommended)
```bash
# Clone the registry repository
git clone https://github.com/modelcontextprotocol/registry.git
cd registry

# Build the publisher CLI
make publisher

# Verify installation
./bin/mcp-publisher --help
```

#### Option B: Download Binary (If Available)
```bash
# Download from GitHub releases (if available)
# https://github.com/modelcontextprotocol/registry/releases

# Make executable
chmod +x mcp-publisher

# Move to PATH
sudo mv mcp-publisher /usr/local/bin/
```

**Expected Result**:
- `mcp-publisher` command available globally
- Help text displays available commands

---

### Step 3: Create server.json

**Current Status**: ✅ Already created (`server.json`, 6006 bytes)

**Schema Version**: 2025-12-11 (latest)

**Required Fields**:
```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "io.github.arould001/predyx-mcp-server",
  "title": "Predyx MCP Server",
  "description": "Bitcoin-native prediction market data provider",
  "version": "1.0.0",
  "packages": [
    {
      "registryType": "pypi",
      "identifier": "predyx-mcp-server",
      "version": "1.0.0",
      "transport": {
        "type": "stdio"
      }
    }
  ]
}
```

**Important Notes**:
- `name` must use `io.github.arould001/` namespace (matches GitHub username)
- `identifier` must match PyPI package name
- `transport` type should be `stdio` for Python packages

---

### Step 4: Authenticate with GitHub OAuth

**Command**:
```bash
mcp-publisher login github
```

**Process**:
1. CLI opens browser to GitHub OAuth page
2. Authorize the application
3. CLI receives and stores access token
4. Token saved locally for future use

**Expected Result**:
- Success message: "Successfully logged in as arould001"
- Token stored in `~/.config/mcp-publisher/credentials.json`

---

### Step 5: Publish to MCP Registry

**Command**:
```bash
mcp-publisher publish
```

**Process**:
1. CLI validates `server.json`
2. Verifies namespace ownership (io.github.arould001/)
3. Checks PyPI package exists
4. Publishes to MCP Registry
5. Returns success message with server URL

**Expected Result**:
- Server URL: https://registry.modelcontextprotocol.io/v0.1/servers/io.github.arould001/predyx-mcp-server
- Server visible in registry search
- Installable via MCP clients

---

### Step 6: Verify Publication

**Methods**:

#### Method 1: API Query
```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.arould001/predyx-mcp-server"
```

#### Method 2: Web Interface
- Visit: https://registry.modelcontextprotocol.io
- Search for "predyx" or "prediction market"
- Verify server details

#### Method 3: MCP Client Test
```bash
# Install via Claude Desktop
# Add to claude_desktop_config.json:
{
  "mcpServers": {
    "predyx": {
      "command": "uvx",
      "args": ["predyx-mcp-server"]
    }
  }
}
```

---

## 🔐 Authentication Methods

### GitHub OAuth (Recommended for Personal Projects)
- **Use Case**: Publishing from local machine
- **Command**: `mcp-publisher login github`
- **Namespace**: `io.github.{username}/`
- **Pros**: Simple, one-time setup
- **Cons**: Manual process

### GitHub OIDC (For CI/CD)
- **Use Case**: Automated publishing from GitHub Actions
- **Setup**: Configure GitHub Actions workflow
- **Namespace**: `io.github.{username}/`
- **Pros**: Fully automated
- **Cons**: More complex setup

### DNS Verification (For Custom Domains)
- **Use Case**: Publishing with custom namespace
- **Namespace**: `me.{domain}/`
- **Process**: Add TXT record to DNS
- **Pros**: Custom branding
- **Cons**: Requires domain ownership

### HTTP Verification (For Custom Domains)
- **Use Case**: Alternative to DNS verification
- **Namespace**: `me.{domain}/`
- **Process**: Serve verification file at `/.well-known/mcp-verification.txt`
- **Pros**: No DNS access needed
- **Cons**: Requires web server

---

## 📝 Namespace Strategy

### Current Namespace
- **Format**: `io.github.arould001/predyx-mcp-server`
- **Reasoning**: GitHub repository owner is `arould001`
- **Verification**: GitHub OAuth login as `arould001`

### Alternative Namespaces (Future Consideration)
- `io.github.dia-ai/predyx-mcp-server` - If Dia AI organization is created
- `me.dia-ai.com/predyx-mcp-server` - If custom domain is acquired

---

## 🚨 Common Issues and Solutions

### Issue 1: Namespace Verification Failed
**Error**: "You do not have permission to publish to namespace io.github.arould001/"

**Solution**:
- Ensure you're logged in as GitHub user `arould001`
- Run `mcp-publisher login github` again
- Check GitHub OAuth token hasn't expired

### Issue 2: PyPI Package Not Found
**Error**: "PyPI package predyx-mcp-server not found"

**Solution**:
- Verify package is published: https://pypi.org/project/predyx-mcp-server/
- Wait 1-2 minutes after publishing
- Check package name matches exactly

### Issue 3: server.json Validation Failed
**Error**: "Validation error: missing required field"

**Solution**:
- Validate schema: https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json
- Use validation tool: `./scripts/validate-server.sh server.json`
- Check all required fields are present

### Issue 4: README mcp-name Mismatch
**Error**: "README.md does not contain valid mcp-name comment"

**Solution**:
- Add to README.md: `<!-- mcp-name: io.github.arould001/predyx-mcp-server -->`
- Ensure exact match with `server.json` name field
- Commit and push to GitHub

---

## ✅ Pre-Publishing Checklist

- [ ] PyPI account registered and verified
- [ ] PyPI package built and uploaded
- [ ] `server.json` validated against schema
- [ ] README.md contains `mcp-name` comment
- [ ] GitHub OAuth token configured
- [ ] `mcp-publisher` CLI installed
- [ ] Namespace matches GitHub username

---

## 📊 Publishing Timeline

**Estimated Time**: 1-2 hours (after PyPI package is published)

| Step | Duration | Dependencies |
|------|----------|--------------|
| Install mcp-publisher | 10 min | Git, Make |
| Create server.json | 5 min | Schema knowledge |
| GitHub OAuth | 5 min | Browser access |
| Publish | 5 min | All prerequisites |
| Verification | 5 min | API access |
| **Total** | **30 min** | - |

---

## 🎯 Next Steps

### Immediate (After PyPI Publication)
1. Build `mcp-publisher` CLI from source
2. Authenticate with GitHub OAuth
3. Validate `server.json`
4. Publish to MCP Registry
5. Verify publication

### Short-term (This Week)
1. Add MCP Registry badge to README
2. Create installation instructions for different MCP clients
3. Test installation via Claude Desktop
4. Gather initial user feedback

### Long-term (After Launch)
1. Set up automated publishing via GitHub Actions (OIDC)
2. Add version update automation
3. Monitor registry analytics
4. Respond to user reviews/issues

---

## 📚 Additional Resources

- **MCP Registry Docs**: https://github.com/modelcontextprotocol/registry/tree/main/docs
- **Publisher Quickstart**: https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx
- **Server Schema**: https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json
- **API Documentation**: https://registry.modelcontextprotocol.io/docs
- **Community Discord**: https://discord.com/channels/1358869848138059966/1369487942862504016

---

## 💡 Key Insights

1. **API is Stable**: v0.1 API freeze since 2025-10-24, safe to integrate
2. **Namespace Verification is Strict**: Must match GitHub username or prove domain ownership
3. **PyPI is Required**: Python packages must be on PyPI before MCP Registry publication
4. **GitHub OAuth is Simplest**: One-time login, no complex configuration
5. **Validation is Important**: Schema validation prevents common errors

---

## 🔄 Update Log

- **2026-03-29 01:48 AM**: Initial guide created, publishing process documented
- **Next Update**: After PyPI package publication (pending Steven's support)

---

**Status**: ✅ Publishing guide complete, ready for execution after PyPI publication  
**Next Action**: Wait for PyPI account registration, then execute publishing workflow
