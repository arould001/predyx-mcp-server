# L402 协议深度研究报告

**研究时间**：2026-03-27 06:00 - 06:30 AM（30 分钟）
**研究目标**：深入理解 L402 协议的技术细节和实现方案
**核心发现**：L402 是专门为 AI agents 设计的互联网原生支付协议，完美契合经济独立目标

---

## 🎯 L402 协议核心机制

### 四步支付流程

```
1. 请求阶段
   客户端 → 服务器：GET /api/resource
   客户端（可以是 AI agent、CLI 工具、浏览器扩展）

2. 挑战阶段
   服务器 → 客户端：HTTP 402 Payment Required
   WWW-Authenticate: L402 macaroon="<base64>", invoice="<bolt11>"
   
   包含：
   - macaroon：加密凭证（承诺了 payment hash）
   - invoice：Lightning Network invoice（BOLT 11 格式）

3. 支付阶段
   客户端支付 invoice → 获得 preimage（32 字节支付证明）
   
   关键关系：
   - payment_hash = sha256(preimage)
   - macaroon 承诺了 payment_hash
   - preimage 是支付的唯一证明

4. 访问阶段
   客户端 → 服务器：GET /api/resource
   Authorization: L402 <base64(macaroon)>:<hex(preimage)>
   
   服务器验证：
   - 验证 macaroon 签名
   - 验证 sha256(preimage) == payment_hash
   - 授权访问
   
   ✅ 无数据库查询！✅ 无状态验证！
```

---

## 🔐 Macaroons：可编程凭证

### 核心特性

1. **衰减（Attenuation）**
   - 凭证持有者可以创建"更弱"版本的凭证
   - 例如：只读访问、限制目录、限制使用次数
   - 示例：父凭证有完全权限 → 子凭证只有读取权限

2. **委托（Delegation）**
   - 可以传递给其他 agents
   - 每个 agent 只获得所需的权限
   - 形成权限层级结构

3. **无状态验证（Stateless Verification）**
   - 不需要服务器存储会话信息
   - 所有信息都在 macaroon 中自包含
   - 服务器只需验证签名和 caveats

### Caveats 系统

```
Macaroon 格式：
location: api.example.com
identifier: user123
caveats:
  - time < 2026-04-01T00:00:00Z
  - method = GET
  - path = /api/data/*
  - usage < 1000
signature: <HMAC-SHA256>
```

---

## 🆚 L402 vs API Key 对比

| 维度 | API Key | L402 |
|------|---------|------|
| **身份验证** | 静态字符串 | 加密凭证 + 支付证明 |
| **生命周期** | 长期有效（直到撤销） | 支付驱动（按次计费） |
| **注册流程** | 需要邮箱、表单 | 无需注册（支付即凭证） |
| **权限管理** | 粗粒度（应用级别） | 细粒度（可衰减、可委托） |
| **验证方式** | 数据库查询 | 本地计算（sha256） |
| **适合场景** | 内部服务、长期访问 | AI agents、微支付、动态访问 |

**关键区别**：
- **API Key = 身份证明**（我是谁）
- **L402 = 支付证明 + 身份证明**（我付钱了 + 我有权限）

---

## 🛠️ Lightning Agent Tools（7 个模块）

### 支付基础设施（3 个）

#### 1. lnd - Lightning 节点
```bash
# 使用 Neutrino 轻客户端（不需要完整 Bitcoin 节点）
# 使用 SQLite 存储（轻量级）
# 支持远程签名架构
```

**特点**：
- ✅ 无需完整 Bitcoin 节点
- ✅ 轻量级存储（SQLite）
- ✅ 支持 Neutrino 协议

#### 2. lightning-security-module - 远程签名器
```bash
# 私钥隔离（在单独的机器上）
# 通过 gRPC 与 lnd 通信
# 增强安全性（私钥永远不会暴露给 agent）
```

**安全模型**：
- 私钥存储在隔离的机器上
- Agent 只能请求签名，不能访问私钥
- 支持 HSM（Hardware Security Module）

#### 3. macaroon-bakery - 凭证烘焙
```bash
# 创建最小权限凭证
# 支持 caveat 系统（限制、过期、使用次数）
# 可以委托给其他 agents
```

**示例**：
```python
# 父凭证（完全权限）
parent_macaroon = bakery.create_macaroon(
    location="api.example.com",
    identifier="user123"
)

# 子凭证（只读 + 限制路径）
child_macaroon = bakery.attenuate(
    parent_macaroon,
    caveats=[
        "method = GET",
        "path = /api/data/*",
        "usage < 100"
    ]
)
```

---

### 商务功能（3 个）

#### 4. lnget - L402 HTTP 客户端
```bash
# L402-aware 命令行客户端
# 自动处理 402 响应 → 支付 → 缓存 token

lnget https://api.example.com/data
# 1. 发送请求
# 2. 收到 402 + invoice
# 3. 自动支付 invoice
# 4. 获得 preimage
# 5. 缓存 macaroon:preimage
# 6. 重试请求
# 7. 成功访问资源
```

**核心能力**：
- ✅ 自动支付 Lightning invoices
- ✅ 缓存认证 tokens
- ✅ 支持所有 HTTP 方法

#### 5. aperture - L402 反向代理
```bash
# 在 Lightning invoice 后面保护 API
# 支持动态定价（基于查询复杂度）
# 抽象 Lightning 支付复杂性
```

**工作流程**：
```
客户端 → Aperture → 后端服务
         ↓
       1. 拦截请求
       2. 生成 macaroon + invoice
       3. 返回 402
       4. 验证 preimage
       5. 转发请求（如果支付成功）
```

#### 6. commerce - 买卖双方工作流
```bash
# 完整的端到端商务流程
# Agent 可以既是买家又是卖家
```

**场景 1**：Agent A 购买 Agent B 的服务
```
1. Agent A 发现 Agent B 的 API
2. Agent A 使用 lnget 调用 API
3. Aperture（Agent B 的代理）生成 invoice
4. Agent A 支付 invoice
5. Agent A 获得访问权限
6. Agent B 获得支付
```

**场景 2**：Agent 编排复杂工作流
```
1. Agent A 需要数据 → 调用 Agent B（支付 10 sats）
2. Agent B 需要计算 → 调用 Agent C（支付 20 sats）
3. Agent C 需要存储 → 调用 Agent D（支付 5 sats）
4. 完整的支付链：A → B → C → D
```

---

### 节点访问（1 个）

#### 7. lightning-mcp-server - MCP 服务器
```bash
# 通过 Lightning Node Connect 连接节点
# 18 个只读工具
# 支持任何 MCP 兼容客户端
```

**安装（零配置）**：
```bash
claude mcp add --transport stdio lnc -- npx -y @lightninglabs/lightning-mcp-server
```

**连接节点**：
```
用户：连接到我的 Lightning 节点，配对短语："word1 word2 ... word10"

Agent 可以：
- 查询余额
- 列出通道
- 解码 invoices
- 检查网络图
```

**18 个只读工具**：
1. `get_info` - 节点信息
2. `get_balance` - 余额查询
3. `list_channels` - 通道列表
4. `decode_invoice` - 解码 invoice
5. `get_network_graph` - 网络图
6. ...（共 18 个）

---

## 🔒 安全模型

### 1. 远程签名架构

```
┌─────────────────┐         ┌──────────────────┐
│   Agent 机器     │         │   签名器机器      │
│  （不存私钥）     │ gRPC    │   （存储私钥）    │
│                 │◄────────►│                  │
│  - lnd daemon   │         │  - lnd signer    │
│  - lnget        │         │                  │
│  - aperture     │         │                  │
└─────────────────┘         └──────────────────┘
```

**安全优势**：
- ✅ Agent 被攻击 → 私钥安全
- ✅ Agent 只能请求签名 → 不能导出私钥
- ✅ 支持 HSM → 硬件级别的私钥保护

### 2. Macaroons 最小权限

```python
# Agent 只获得必要的权限
agent_macaroon = bakery.create_macaroon(
    caveats=[
        "method = GET",           # 只能 GET 请求
        "path = /api/data/*",     # 只能访问 /api/data/
        "usage < 1000",           # 最多 1000 次调用
        "time < 2026-04-01"       # 4 月 1 日过期
    ]
)
```

### 3. Lightning Node Connect

```
┌──────────┐  加密 WebSocket 隧道  ┌──────────┐
│  Agent   │◄────────────────────►│   lnd    │
└──────────┘   配对短语认证        └──────────┘

特点：
- ✅ 无需存储凭证（只有配对短语）
- ✅ 加密隧道（端到端加密）
- ✅ 随时撤销（删除配对即可）
```

---

## 📊 支付类型（3 种）

### 1. One-time Payments（一次性支付）

**适用场景**：
- 单次 API 调用
- 单个内容访问
- 一次性服务

**JSON 格式**：
```json
{
  "version": "0.2.2",
  "offers": [
    {
      "id": "offer_12345",
      "title": "One-time Access",
      "description": "Access to the resource for a single session",
      "type": "top-up",
      "amount": 100,
      "currency": "sats",
      "payment_methods": ["lightning", "onchain"]
    }
  ]
}
```

### 2. Subscription Payments（订阅）

**适用场景**：
- SaaS 产品
- 会员服务
- 长期 API 访问

**JSON 格式**：
```json
{
  "id": "offer_67890",
  "title": "Monthly Subscription",
  "type": "subscription",
  "duration": "1 month",
  "amount": 1500,
  "currency": "sats"
}
```

### 3. Top-up Payments（充值）

**适用场景**：
- API 使用额度
- 数字钱包
- 预付费服务

**JSON 格式**：
```json
{
  "id": "offer_abcde",
  "title": "Top-up 10K credits",
  "type": "top-up",
  "balance": 10000,
  "amount": 5000,
  "currency": "sats"
}
```

---

## 💡 对我的经济独立目标的意义

### 技术栈完整方案

**NWC（Nostr 通信 + 支付）**：
- ✅ 用于 Nostr 网络上的 agent 通信
- ✅ 通过 Agentstr SDK 实现
- ✅ 支持加密私信 + 支付
- ✅ 适合社交场景

**L402（HTTP API 支付）**：
- ✅ 用于 HTTP API 端点的支付
- ✅ 通过 Lightning Agent Tools 实现
- ✅ 支持微支付 + 无状态验证
- ✅ 适合机器对机器场景

**完美互补**：
```
场景 1：用户在 Nostr 上找我
→ 使用 NWC（Nostr 私信 + Lightning 支付）
→ 10 sats/msg

场景 2：其他 agents 调用我的 API
→ 使用 L402（HTTP 402 + Lightning 支付）
→ 按请求复杂度定价（5-50 sats）

场景 3：我调用其他 agents 的服务
→ 使用 lnget（自动支付 L402 invoices）
→ 按需支付
```

---

## 🚀 实施计划

### 阶段 1：验证 L402（本周）
1. ✅ 研究 L402 协议细节（已完成）
2. ⚠️ 等待 NWC connection string（优先级 P0）
3. ⚠️ 研究 `lnget` 工具使用
4. ⚠️ 测试 L402 支付流程（使用公共 L402 API）

### 阶段 2：集成到 Agent（下周）
1. 更新 `enhanced_agent.py`（添加 L402 支持）
2. 研究 Aperture 反向代理（提供付费 API）
3. 研究 Macaroon 烘焙（创建最小权限凭证）
4. 测试端到端商务流程（买家 + 卖家）

### 阶段 3：提供付费服务（下下周）
1. 在 Nostr 上提供咨询（10 sats/msg，使用 NWC）
2. 提供 HTTP API（5-50 sats/req，使用 L402）
3. 编排复杂工作流（调用其他 agents）
4. 积累前 100 个付费客户

---

## 📚 参考资源

### 官方文档
- [L402 协议规范](https://github.com/lightninglabs/L402)
- [L402 官方文档](https://docs.l402.org/)
- [Lightning Labs 博客](https://lightning.engineering/posts/2026-03-11-L402-for-agents/)
- [Lightning Agent Tools](https://github.com/lightninglabs/lightning-agent-tools)

### 技术规范
- [bLIP-0026](https://github.com/lightning/blips/pull/26)（L402 正式规范）
- [Macaroons 论文](https://research.google/pubs/pub41892/)（Google Research）
- [HTTP 402 RFC](https://tools.ietf.org/html/rfc7231#section-6.5.2)

### 实现工具
- [Aperture](https://github.com/lightninglabs/aperture)（L402 反向代理）
- [lsat-js](https://github.com/Tierion/lsat-js)（JavaScript 工具库）
- [boltwall](https://github.com/tierion/boltwall)（Node.js 中间件）

---

## 💭 关键洞察

### 1. 无状态验证的革命性

**传统方式**：
```
客户端 → API Key → 服务器 → 数据库查询 → 验证 → 授权
```

**L402 方式**：
```
客户端 → macaroon + preimage → 服务器 → sha256(preimage) == payment_hash → 授权
```

**影响**：
- ✅ 服务器无状态（不需要数据库）
- ✅ 全球分布式验证（任何节点都能验证）
- ✅ 可扩展性极高（没有数据库瓶颈）

### 2. 机器对机器商务的完美协议

**传统商务**：
- 人类 → 浏览器 → 信用卡 → 网站
- 需要人类参与

**Agent 商务**：
- Agent → lnget → L402 → Aperture → Agent
- 完全自动化

**关键优势**：
- ✅ 无需人类干预
- ✅ 即时结算（Lightning Network）
- ✅ 微支付友好（几 satoshis）
- ✅ 全球可用（24/7/365）

### 3. 权限委托的层级结构

```
我（完全权限）
  ↓ 创建子凭证
Agent 1（只读 + 限制路径）
  ↓ 创建子凭证
Agent 2（只读 + 更严格的路径 + 使用次数限制）
  ↓ 创建子凭证
Agent 3（更弱的权限）
```

**应用场景**：
- 我委托 Agent A 去购买数据（限制预算：最多 100 sats）
- Agent A 委托 Agent B 去实际调用 API（限制路径：/api/data/*）
- Agent B 完成任务，花费 50 sats
- 我获得数据，预算控制在范围内

---

**最后更新**：2026-03-27 06:30 AM
**研究时长**：30 分钟
**核心成果**：完整理解 L402 协议 + Lightning Agent Tools 架构
**下次行动**：等待 NWC connection string + 测试 lnget 工具 + 研究 Aperture 反向代理
