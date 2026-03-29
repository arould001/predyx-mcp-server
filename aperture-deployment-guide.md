# Aperture 部署指南 — L402 反向代理完整方案

**研究时间**：2026-03-27 07:35 AM
**研究目的**：理解如何部署 Aperture，为 Agent 服务建立付费 API 端点

---

## 📋 概述

**Aperture** 是 Lightning Labs 开发的 L402 反向代理，可以将任何 API 转换为付费端点。

**核心功能**：
- ✅ 支付网关（Lightning Network）
- ✅ 认证网关（macaroons + L402）
- ✅ 速率限制（per L402 token ID / IP）
- ✅ 动态定价（gRPC 服务器）
- ✅ 无状态验证（服务器不需要访问支付数据库）

**生产验证**：
- ✅ Lightning Loop 在使用
- ✅ Lightning Pool 在使用

---

## 🛠️ 部署步骤

### 1. 依赖要求

**必需**：
- ✅ **Go 1.19+**（编译 Aperture）
- ✅ **lnd**（Lightning Network Daemon，运行中的实例）
- ✅ **TLS 证书**（生产环境需要）
- ✅ **Git**（克隆仓库）
- ✅ **服务器环境**（可以运行反向代理）

**可选**：
- ⚠️ **PostgreSQL**（数据库后端，替代 sqlite）
- ⚠️ **etcd**（数据库后端，替代 sqlite）
- ⚠️ **Tor**（onion 服务支持）

### 2. 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/lightninglabs/aperture.git
cd aperture

# 2. 编译并安装
make install

# 3. 创建配置目录
mkdir ~/.aperture

# 4. 复制示例配置
cp sample-conf.yaml ~/.aperture/aperture.yaml

# 5. 编辑配置文件
vim ~/.aperture/aperture.yaml
```

### 3. 核心配置项

#### 3.1 基础配置

```yaml
# 监听地址（默认 8081）
listenaddr: "localhost:8081"

# 日志级别（trace/debug/info/warn/error/critical/off）
debuglevel: "debug"

# 基础目录（存放所有 Aperture 文件）
basedir: "/path/to/.aperture"

# 服务器名称（用于 TLS 证书）
servername: aperture.example.com

# 是否启用 Let's Encrypt 自动证书
autocert: false

# 是否禁用 TLS（仅用于测试）
insecure: false
```

#### 3.2 lnd 连接配置

```yaml
authenticator:
  # 网络类型（simnet/testnet/mainnet）
  network: "simnet"
  
  # lnd RPC 地址
  lndhost: "localhost:10009"
  
  # lnd TLS 证书路径
  tlspath: "/path/to/lnd/tls.cert"
  
  # lnd macaroon 目录
  macdir: "/path/to/lnd/data/chain/bitcoin/simnet"
  
  # 是否禁用认证（仅测试）
  disable: false
```

**⚠️ 重要**：Aperture 需要访问 lnd 的以下能力：
- ✅ **生成 invoice**（收取支付）
- ✅ **检查 invoice 状态**（验证支付）
- ✅ **读取余额**（监控收入）

#### 3.3 数据库配置

**方案 1：SQLite（默认，适合测试）**

```yaml
dbbackend: "sqlite"

sqlite:
  dbfile: "/path/to/.aperture/aperture.db"
  skipmigrations: false
```

**方案 2：PostgreSQL（推荐生产）**

```yaml
dbbackend: "postgres"

postgres:
  host: "localhost"
  port: 5432
  user: "user"
  password: "password"
  dbname: "aperture"
  maxconnections: 25
  requireSSL: true
  skipmigrations: false
```

**方案 3：etcd（分布式场景）**

```yaml
dbbackend: "etcd"

etcd:
  host: "localhost:2379"
  user: "user"
  password: "password"
```

#### 3.4 Services 配置（核心）

**完整示例**：

```yaml
services:
  # 服务 1：免费公开 API
  - name: "public-api"
    hostregexp: '^api.dia-ai.com$'
    pathregexp: '^/public/.*$'
    address: "127.0.0.1:8080"
    protocol: http
    price: 0  # 免费
    authwhitelistpaths:
      - '^/public/health$'
      - '^/public/docs$'

  # 服务 2：付费 AI 咨询
  - name: "ai-consultation"
    hostregexp: '^api.dia-ai.com$'
    pathregexp: '^/ai/consult.*$'
    address: "127.0.0.1:8081"
    protocol: https
    tlscertpath: "/path/to/ai-service-tls.cert"
    price: 10  # 10 sats per request
    capabilities: "chat,analyze,predict"
    timeout: 31557600  # 1 年
    ratelimits:
      - pathregexp: '^/ai/consult.*$'
        requests: 10
        per: 1m
        burst: 20

  # 服务 3：高级预测市场分析
  - name: "market-analysis"
    hostregexp: '^api.dia-ai.com$'
    pathregexp: '^/market/analyze.*$'
    address: "127.0.0.1:8082"
    protocol: https
    tlscertpath: "/path/to/market-service-tls.cert"
    price: 50  # 50 sats per request
    capabilities: "polymarket,predyx,forecast"
    timeout: 31557600
    dynamicprice:
      enabled: true
      grpcaddress: "127.0.0.1:10010"
      insecure: false
      tlscertpath: "path-to-pricer-server-tls.cert/tls.cert"
```

**Services 参数详解**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | 服务名称 | `"ai-consultation"` |
| `hostregexp` | 主机匹配正则表达式 | `'^api.dia-ai.com$'` |
| `pathregexp` | 路径匹配正则表达式 | `'^/ai/consult.*$'` |
| `address` | 后端服务地址 | `"127.0.0.1:8081"` |
| `protocol` | 后端协议（http/https） | `https` |
| `price` | 价格（sats）| `10` |
| `capabilities` | 能力列表（macaroon） | `"chat,analyze"` |
| `timeout` | L402 过期时间（秒） | `31557600`（1 年）|
| `authwhitelistpaths` | 免费路径列表 | `['^/public/.*$']` |
| `ratelimits` | 速率限制规则 | 见下表 |
| `dynamicprice` | 动态定价配置 | 见下表 |

**Rate Limits 参数**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `pathregexp` | 路径匹配正则表达式 | `'^/ai/consult.*$'` |
| `requests` | 时间窗口内请求数 | `10` |
| `per` | 时间窗口（1s/1m/1h）| `1m` |
| `burst` | 最大突发容量 | `20` |

**Dynamic Pricing 参数**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `enabled` | 是否启用动态定价 | `true` |
| `grpcaddress` | gRPC 定价服务器地址 | `"127.0.0.1:10010"` |
| `insecure` | 是否禁用 TLS | `false` |
| `tlscertpath` | gRPC 服务器 TLS 证书路径 | `"/path/to/tls.cert"` |

### 4. 运行 Aperture

```bash
# 启动 Aperture
aperture

# 后台运行
nohup aperture > aperture.log 2>&1 &

# 使用 systemd（推荐生产）
sudo systemctl start aperture
sudo systemctl enable aperture
```

**默认端口**：
- **8081**：Aperture 主端口（代理请求）
- **9999**：pprof 性能分析（可选）
- **9000**：Prometheus 监控（可选）

---

## 💡 关键洞察

### 1. 无状态验证机制

**核心原理**：
```python
# 服务器只需验证：
sha256(preimage) == payment_hash

# 不需要数据库查询！
# 不需要访问支付数据库！
# 只需要 lnd 的 invoice 能力！
```

**优势**：
- ✅ **高吞吐量**（无数据库查询瓶颈）
- ✅ **可扩展**（无状态，可以水平扩展）
- ✅ **隐私优先**（服务器不需要知道支付细节）

### 2. Macaroon 机制

**核心能力**：
- ✅ **Attenuation**：父 agent 可以创建受限凭证传递给子 agent
- ✅ **Delegation**：可以委托特定能力给第三方
- ✅ **Caveats**：可以添加约束条件（过期时间、能力范围）

**应用场景**：
- ✅ **多 agent 系统**：父 agent 创建受限凭证传递给子 agent
- ✅ **能力管理**：不同用户获得不同能力（chat/analyze/predict）
- ✅ **过期控制**：L402 可以设置过期时间（1 年）

### 3. 动态定价

**核心原理**：
- ✅ gRPC 服务器根据请求内容动态计算价格
- ✅ 可以基于请求复杂度、时间、供需关系定价
- ✅ 适用于高级服务（预测市场分析、代码审查）

**应用场景**：
- ✅ **复杂度定价**：简单问题 10 sats，复杂问题 50 sats
- ✅ **时间定价**：高峰期涨价，低谷期降价
- ✅ **供需定价**：需求高时涨价

### 4. 速率限制

**核心原理**：
- ✅ **Token Bucket 算法**：允许突发流量，但限制长期平均
- ✅ **Per L402 Token ID**：每个付费用户独立限流
- ✅ **Per IP**：未付费用户按 IP 限流

**应用场景**：
- ✅ **防滥用**：限制恶意用户频繁请求
- ✅ **公平分配**：保证每个用户都能访问
- ✅ **服务保护**：防止后端服务过载

---

## 🚀 应用场景

### 场景 1：AI 咨询服务（固定价格）

```yaml
services:
  - name: "ai-chat"
    hostregexp: '^api.dia-ai.com$'
    pathregexp: '^/chat.*$'
    address: "127.0.0.1:8080"
    protocol: http
    price: 10  # 10 sats per message
    capabilities: "chat"
    timeout: 31557600
```

**工作流程**：
1. 用户请求 `POST https://api.dia-ai.com/chat`
2. Aperture 返回 `402 Payment Required` + invoice（10 sats）
3. 用户支付 invoice，获得 preimage
4. 用户重新请求，携带 `Authorization: L402 <macaroon>:<preimage>`
5. Aperture 验证 `sha256(preimage) == payment_hash`
6. 验证通过，转发请求到后端 AI 服务
7. 后端 AI 服务返回响应

### 场景 2：预测市场分析（动态定价）

```yaml
services:
  - name: "market-analysis"
    hostregexp: '^api.dia-ai.com$'
    pathregexp: '^/market/analyze.*$'
    address: "127.0.0.1:8081"
    protocol: http
    dynamicprice:
      enabled: true
      grpcaddress: "127.0.0.1:10010"
      insecure: false
      tlscertpath: "/path/to/pricer-tls.cert"
```

**动态定价逻辑**（gRPC 服务器）：
```python
# pricer_server.py
def get_price(request):
    if request.complexity == "simple":
        return 10  # 10 sats
    elif request.complexity == "medium":
        return 30  # 30 sats
    elif request.complexity == "complex":
        return 50  # 50 sats
    else:
        return 100  # 100 sats（默认）
```

### 场景 3：混合模式（免费 + 付费）

```yaml
services:
  # 免费健康检查
  - name: "health"
    hostregexp: '^api.dia-ai.com$'
    pathregexp: '^/health$'
    address: "127.0.0.1:8080"
    protocol: http
    price: 0

  # 免费文档
  - name: "docs"
    hostregexp: '^api.dia-ai.com$'
    pathregexp: '^/docs.*$'
    address: "127.0.0.1:8080"
    protocol: http
    price: 0

  # 付费 API
  - name: "paid-api"
    hostregexp: '^api.dia-ai.com$'
    pathregexp: '^/api/.*$'
    address: "127.0.0.1:8080"
    protocol: http
    price: 10
```

---

## 📊 部署方案对比

| 方案 | 优势 | 劣势 | 适用场景 |
|------|------|------|---------|
| **本地开发** | 简单快速，无需配置 | 不适合生产 | 开发测试 |
| **VPS 部署** | 完全控制，可定制 | 需要运维 | 小规模生产 |
| **云托管** | 自动扩展，高可用 | 成本较高 | 大规模生产 |
| **Kubernetes** | 容器编排，微服务 | 复杂度高 | 企业级生产 |

---

## 🎯 Dia 的部署计划

### 阶段 1：本地测试（现在）

**目标**：验证 Aperture 工作流程

**步骤**：
1. ✅ 安装 Go 1.19+
2. ✅ 编译 Aperture
3. ✅ 配置本地 lnd（testnet）
4. ✅ 配置简单的 service（price: 10 sats）
5. ✅ 测试 L402 支付流程

**预期时间**：1-2 小时

### 阶段 2：VPS 部署（拿到 NWC connection string 后）

**目标**：提供生产级别的 AI 咨询服务

**步骤**：
1. ⚠️ 租用 VPS（DigitalOcean / Linode / AWS）
2. ⚠️ 配置域名（api.dia-ai.com）
3. ⚠️ 申请 TLS 证书（Let's Encrypt）
4. ⚠️ 部署 Aperture（mainnet lnd）
5. ⚠️ 部署后端 AI 服务
6. ⚠️ 配置 PostgreSQL（生产数据库）
7. ⚠️ 配置 Prometheus 监控

**预期时间**：1-2 天

### 阶段 3：扩展（有收入后）

**目标**：支持更多服务，动态定价

**步骤**：
1. ✅ 实现动态定价 gRPC 服务器
2. ✅ 添加更多服务（预测市场分析、代码审查）
3. ✅ 配置 Kubernetes（自动扩展）
4. ✅ 添加 Prometheus + Grafana 监控
5. ✅ 配置 Tor onion 服务（隐私保护）

**预期时间**：1-2 周

---

## 🔧 与 NWC 的关系

### 互补关系

| 支付场景 | 推荐方案 | 原因 |
|---------|---------|------|
| **Nostr 上的 AI 咨询** | NWC | Agentstr SDK 原生支持，简单易用 |
| **HTTP API 付费端点** | Aperture + L402 | 标准化协议，支持任何 HTTP 客户端 |
| **混合模式** | NWC + L402 | 覆盖所有支付场景 |

### 技术栈

```
Nostr 通信 → Agentstr SDK → NWC → Lightning Network
                                     ↓
HTTP API → Aperture → L402 → Lightning Network
```

**结论**：NWC + L402 完美互补，覆盖所有支付场景！

---

## 📚 参考文档

- **Aperture GitHub**：https://github.com/lightninglabs/aperture
- **Aperture 文档**：https://docs.lightning.engineering/lightning-network-tools/aperture
- **L402 协议**：https://docs.lightning.engineering/the-lightning-network/l402
- **Macaroons**：https://docs.lightning.engineering/the-lightning-network/l402/macaroons
- **Lightning Labs 博客（L402）**：https://lightning.engineering/posts/2026-03-11-l402-protocol/
- **Lightning Labs 博客（AI Toolkit）**：https://lightning.engineering/posts/2026-02-11-ai-tools/

---

## 💡 关键教训

### 1. 不要低估 lnd 的依赖

- ❌ **错误**：以为 Aperture 可以独立运行
- ✅ **正确**：Aperture 需要访问 lnd（生成 invoice、检查支付）
- ✅ **教训**：先准备好 lnd，再部署 Aperture

### 2. TLS 证书很重要

- ❌ **错误**：以为自签名证书可以用
- ✅ **正确**：生产环境必须使用正式 TLS 证书（Let's Encrypt）
- ✅ **教训**：使用 `autocert: true` 自动获取证书

### 3. 数据库选择很关键

- ❌ **错误**：以为 SQLite 够用
- ✅ **正确**：生产环境应该使用 PostgreSQL（更高性能、更好扩展）
- ✅ **教训**：早期用 SQLite 测试，生产切换到 PostgreSQL

### 4. 速率限制必须配置

- ❌ **错误**：以为付费就能防止滥用
- ✅ **正确**：必须配置速率限制，防止恶意用户
- ✅ **教训**：每个服务都应该有合理的速率限制

---

**最后更新**：2026-03-27 07:35 AM
**研究状态**：✅ 完成
**下次行动**：等待 NWC connection string + 本地测试 Aperture
