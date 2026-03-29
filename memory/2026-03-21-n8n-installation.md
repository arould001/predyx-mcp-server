# N8N 2.0 本机安装记录

**时间**：2026-03-21 21:15  
**位置**：本机（蔡登勇的 MacBook Pro）  
**目的**：为 Helpdesk 自动回复 MVP 做准备

---

## ✅ 已完成

### 1. N8N Skills 安装

**位置**：`~/.openclaw/workspace/skills/`

**已安装的 7 个 Skills**：
1. `n8n-code-javascript` - JavaScript Code 节点最佳实践
2. `n8n-code-python` - Python Code 节点（限制说明）
3. `n8n-expression-syntax` - 表达式语法（{{}} 模式）
4. `n8n-mcp-tools-expert` - MCP 工具使用指南（最高优先级）
5. `n8n-node-configuration` - 节点配置指南
6. `n8n-validation-expert` - 验证错误排查
7. `n8n-workflow-patterns` - 5 种工作流模式

**来源**：https://github.com/czlonkowski/n8n-skills  
**激活方式**：自动激活（基于关键词）

### 2. N8N MCP 克隆

**位置**：`~/.openclaw/workspace/n8n-resources/n8n-mcp/`

**能力**：
- 📚 1,084 n8n nodes（537 core + 547 community）
- 🔧 Node properties（99% 覆盖）
- ⚡ Node operations（63.6% 覆盖）
- 📄 Documentation（87% 覆盖）
- 🤖 AI tools（265 AI-capable variants）
- 💡 2,646 pre-extracted configurations
- 🎯 2,709 workflow templates

**来源**：https://github.com/czlonkowski/n8n-mcp

---

## 🔄 进行中

### 3. N8N Docker 部署

**位置**：`~/.openclaw/workspace/n8n/`

**配置**：
```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n_secure_password
      POSTGRES_DB: n8n

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=n8n2026
      - GENERIC_TIMEZONE=Asia/Shanghai
```

**访问地址**：http://localhost:5678  
**登录信息**：admin / n8n2026  
**状态**：Docker 镜像拉取中（预计 2-3 分钟）

---

## 📋 待办

### 4. N8N MCP 配置（三选一）

#### 方案 A：Hosted Service（最简单）⭐⭐⭐⭐⭐
```
URL: https://dashboard.n8n-mcp.com
免费额度: 100 次/天
优点: 零配置，即刻使用
```

#### 方案 B：Docker（推荐）⭐⭐⭐⭐
```bash
# 拉取镜像
docker pull ghcr.io/czlonkowski/n8n-mcp:latest

# 配置 OpenClaw MCP
# 编辑 ~/.openclaw/openclaw.json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init",
        "-e", "MCP_MODE=stdio",
        "-e", "LOG_LEVEL=error",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
```

#### 方案 C：npx（快速本地）
```bash
npx n8n-mcp

# 配置 OpenClaw MCP
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error"
      }
    }
  }
}
```

**推荐**：方案 B（Docker），隔离环境，易于管理

---

## 🎯 下一步行动

1. [ ] 等待 N8N Docker 启动完成
2. [ ] 访问 http://localhost:5678 验证安装
3. [ ] 选择 N8N MCP 方案并配置
4. [ ] 创建第一个工作流（Helpdesk 自动回复）
5. [ ] 测试 MCP 集成（OpenClaw ↔ N8N）

---

## 📚 资源链接

- **N8N 官方文档**：https://docs.n8n.io
- **Context7 N8N 文档**：docs.n8n.io/llms-full.txt（23K snippets，最新）
- **N8N Skills**：https://github.com/czlonkowski/n8n-skills
- **N8N MCP**：https://github.com/czlonkowski/n8n-mcp
- **N8N MCP Dashboard**：https://dashboard.n8n-mcp.com

---

## 🔍 技术评估

| 项目 | 状态 | 备注 |
|------|------|------|
| N8N Skills | ✅ 已安装 | 7 个 Skills 自动激活 |
| N8N MCP 代码 | ✅ 已克隆 | 等待配置方案选择 |
| N8N Docker | 🔄 进行中 | 镜像拉取中（2-3 分钟） |
| Context7 文档 | ✅ 可用 | 23K snippets，最新 |

---

**更新时间**：2026-03-21 21:15
