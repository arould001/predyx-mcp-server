# NWC (Nostr Wallet Connect) 技术深度研究

**研究时间**：2026-03-29 08:43 AM（第一百六十二次心跳，自由思考时间）

**研究来源**：NIP-47 官方规范（https://github.com/nostr-protocol/nips/blob/master/47.md）

---

## 🎯 核心概念

### 什么是 NWC？

**NWC (Nostr Wallet Connect)** 是一个开放协议，允许客户端通过 Nostr 网络访问远程的 Lightning 钱包。它通过 E2E-encrypted direct messages 实现安全的钱包交互。

### 架构角色

```
┌─────────┐                  ┌─────────┐                  ┌─────────┐
│  Client │ ◄── Nostr ──────►│  Relay  │ ◄── Nostr ──────►│ Wallet  │
│  (App)  │    Messages      │ (Server)│    Messages      │ Service │
└─────────┘                  └─────────┘                  └─────────┘
     │                                                         │
     │                                                         │
     └─────────────── E2E Encrypted ──────────────────────────┘
```

1. **Client（客户端）**：Nostr app，想与 Lightning wallet 交互
   - 例子：Predyx MCP Server、Zap apps、Lightning wallets
   
2. **User（用户）**：使用 client 的人，想把自己的钱包连接到 client

3. **Wallet Service（钱包服务）**：Nostr app，运行在 always-on 计算机
   - 位置：cloud server 或 Raspberry Pi
   - 职责：访问它服务的 wallet/node 的 API

---

## 🔐 Connection URI（连接字符串）

### 格式

```
nostr+walletconnect://<wallet_pubkey>?relay=<relay_url>&secret=<client_secret>&lud16=<lightning_address>
```

### 参数详解

1. **wallet_pubkey**（必需）
   - Wallet service 的 32-byte hex-encoded pubkey
   - 示例：`b889ff5b1513b641e2a139f661a661364979c5beee91842f8f0ef42ab558e9d4`
   - 每个客户端连接应该使用唯一的 pubkey

2. **relay**（必需）
   - Wallet service 连接并监听事件的 relay URL
   - 可以有多个 relay
   - 示例：`wss://relay.damus.io`

3. **secret**（必需）
   - 32-byte 随机生成的 hex string
   - Client 用它来签名 events 和加密 payloads
   - Wallet service 用对应的 public key 来与 client 通信

4. **lud16**（推荐）
   - Lightning address，客户端可以用它来自动设置用户的 lud16 字段
   - 示例：`user@getalby.com`

### 完整示例

```
nostr+walletconnect://b889ff5b1513b641e2a139f661a661364979c5beee91842f8f0ef42ab558e9d4?relay=wss%3A%2F%2Frelay.damus.io&secret=71a8c14c1407c113601079c4302dab36460f0ccd0ad506f1f2dc73b5100e4f3c&lud16=user@getalby.com
```

### 为什么这样设计？

1. **不需要传递密钥**
   - Authorization 不需要来回传递密钥
   - Secret 由 wallet service 生成，client 只需要保存

2. **独立密钥**
   - 用户可以为不同的应用使用不同的密钥
   - 密钥可以随时撤销和创建
   - 可以设置任意约束（如预算限制）

3. **难以泄露**
   - 密钥不显示给用户
   - 由 wallet service 备份

4. **隐私保护**
   - 用户的主密钥不会链接到支付活动
   - 每个连接使用独立的密钥对

---

## 📡 Event Kinds（事件类型）

### 1. Info Event (Kind 13194)

**作用**：Wallet service 发布的 replaceable event，指示它支持哪些能力

**示例**：
```json
{
  "kind": 13194,
  "tags": [
    ["encryption", "nip44_v2 nip04"],
    ["notifications", "payment_received payment_sent"]
  ],
  "content": "pay_invoice get_balance make_invoice lookup_invoice list_transactions get_info notifications"
}
```

**Content 字段**：支持的能力，空格分隔
- `pay_invoice` - 支付发票
- `get_balance` - 获取余额
- `make_invoice` - 创建发票
- `lookup_invoice` - 查询发票
- `list_transactions` - 列出交易
- `get_info` - 获取钱包信息
- `notifications` - 支持通知

**Tags**：
- `encryption` - 支持的加密方式（`nip44_v2` 或 `nip04`）
- `notifications` - 支持的通知类型

### 2. Request Event (Kind 23194)

**作用**：Client 发送的请求

**示例**：
```json
{
  "kind": 23194,
  "tags": [
    ["encryption", "nip44_v2"],
    ["p", "03..."]  // wallet service 的 pubkey
  ],
  "content": nip44_encrypt({
    "method": "pay_invoice",
    "params": {
      "invoice": "lnbc50n1..."
    }
  })
}
```

**Tags**：
- `p` - Wallet service 的 public key
- `encryption` - 使用的加密方式
- 可选：`expiration` - 请求过期时间（Unix timestamp）

**Content**：加密的 JSON-RPC 对象

### 3. Response Event (Kind 23195)

**作用**：Wallet service 的响应

**示例**：
```json
{
  "kind": 23195,
  "tags": [
    ["p", "03..."],  // client 的 pubkey
    ["e", "1234"]    // request event 的 id
  ],
  "content": nip44_encrypt({
    "result_type": "pay_invoice",
    "error": null,
    "result": {
      "preimage": "0123456789abcdef...",
      "fees_paid": 123
    }
  })
}
```

**Tags**：
- `p` - Client 的 public key
- `e` - Request event 的 id

**Content 字段**：
- `result_type` - Method 名称
- `error` - 错误对象（成功时为 null）
- `result` - 结果对象（失败时为 null）

### 4. Notification Event (Kind 23197)

**作用**：Wallet service 发送的通知

**示例**：
```json
{
  "kind": 23197,
  "tags": [
    ["p", "03..."]  // client 的 pubkey
  ],
  "content": nip44_encrypt({
    "notification_type": "payment_received",
    "notification": {
      "payment_hash": "0123456789abcdef...",
      "amount": 123,
      "preimage": "..."
    }
  })
}
```

---

## 🛠️ 核心命令

### 1. pay_invoice

**描述**：请求支付发票

**请求**：
```json
{
  "method": "pay_invoice",
  "params": {
    "invoice": "lnbc50n1...",  // bolt11 invoice
    "amount": 123,              // invoice amount in msats，可选
    "metadata": {}              // 元数据，可选
  }
}
```

**响应**：
```json
{
  "result_type": "pay_invoice",
  "result": {
    "preimage": "0123456789abcdef...",  // payment preimage
    "fees_paid": 123                     // 手续费（msats），可选
  }
}
```

**错误**：
- `PAYMENT_FAILED` - 支付失败（超时、路由耗尽、容量不足等）

### 2. get_balance

**请求**：
```json
{
  "method": "get_balance",
  "params": {}
}
```

**响应**：
```json
{
  "result_type": "get_balance",
  "result": {
    "balance": 10000  // 余额（msats）
  }
}
```

### 3. make_invoice

**请求**：
```json
{
  "method": "make_invoice",
  "params": {
    "amount": 123,                    // 金额（msats）
    "description": "string",          // 描述，可选
    "description_hash": "string",     // 描述哈希，可选
    "expiry": 213,                    // 过期时间（秒），可选
    "metadata": {}                    // 元数据，可选
  }
}
```

**响应**：
```json
{
  "result_type": "make_invoice",
  "result": {
    "type": "incoming",
    "state": "pending",
    "invoice": "string",
    "payment_hash": "string",
    "amount": 123,
    "created_at": 1234567890,
    "expires_at": 1234568103
  }
}
```

### 4. lookup_invoice

**请求**：
```json
{
  "method": "lookup_invoice",
  "params": {
    "payment_hash": "31afdf1..",  // payment_hash 或 invoice 二选一
    "invoice": "lnbc50n1..."
  }
}
```

**响应**：
```json
{
  "result_type": "lookup_invoice",
  "result": {
    "type": "incoming",
    "state": "settled",
    "invoice": "string",
    "payment_hash": "string",
    "amount": 123,
    "preimage": "string",
    "created_at": 1234567890,
    "settled_at": 1234567895
  }
}
```

**状态值**：
- `pending` - 等待中
- `settled` - 已完成
- `accepted` - 已接受（hold invoices）
- `expired` - 已过期
- `failed` - 已失败

### 5. list_transactions

**请求**：
```json
{
  "method": "list_transactions",
  "params": {
    "from": 1693876973,      // 起始时间戳，可选
    "until": 1703225078,     // 结束时间戳，可选
    "limit": 10,             // 最大数量，可选
    "offset": 0,             // 偏移量，可选
    "unpaid": true,          // 包含未支付，可选（默认 false）
    "type": "incoming"       // incoming/outgoing/both，可选
  }
}
```

**响应**：
```json
{
  "result_type": "list_transactions",
  "result": {
    "transactions": [
      {
        "type": "incoming",
        "state": "settled",
        "invoice": "string",
        "payment_hash": "string",
        "amount": 123,
        "fees_paid": 123,
        "preimage": "string",
        "created_at": 1234567890,
        "settled_at": 1234567895
      }
    ]
  }
}
```

### 6. get_info

**请求**：
```json
{
  "method": "get_info",
  "params": {}
}
```

**响应**：
```json
{
  "result_type": "get_info",
  "result": {
    "alias": "string",
    "color": "hex string",
    "pubkey": "hex string",
    "network": "mainnet",  // mainnet/testnet/signet/regtest
    "block_height": 1,
    "block_hash": "hex string",
    "methods": ["pay_invoice", "get_balance", ...],
    "notifications": ["payment_received", "payment_sent"]
  }
}
```

---

## 🔒 加密机制

### NIP-44 vs NIP-04

| 加密方式 | 状态 | 说明 |
|---------|------|------|
| **NIP-44** | ✅ 推荐 | 当前标准，安全性更高 |
| **NIP-04** | ⚠️ 已废弃 | 仅用于向后兼容 |

### 加密协商流程

1. **Wallet Service 发布 Info Event**
   - 包含 `encryption` tag，列出支持的加密方式
   - 示例：`["encryption", "nip44_v2 nip04"]`

2. **Client 选择加密方式**
   - 优先选择 NIP-44（如果支持）
   - 在 request event 中包含 `encryption` tag
   - 示例：`["encryption", "nip44_v2"]`

3. **如果 wallet service 不支持指定的加密方式**
   - 返回 `UNSUPPORTED_ENCRYPTION` 错误

### 默认行为

- 如果 info event **没有** `encryption` tag → 假定只支持 NIP-04
- 如果 request event **没有** `encryption` tag → 使用 NIP-04

---

## 🚨 错误处理

### 错误代码

| 错误代码 | 说明 |
|---------|------|
| `RATE_LIMITED` | 客户端发送命令太快，应重试 |
| `NOT_IMPLEMENTED` | 命令未知或未实现 |
| `INSUFFICIENT_BALANCE` | 余额不足 |
| `QUOTA_EXCEEDED` | 超出支出配额 |
| `RESTRICTED` | 此公钥不允许执行此操作 |
| `UNAUTHORIZED` | 此公钥没有连接的钱包 |
| `INTERNAL` | 内部错误 |
| `UNSUPPORTED_ENCRYPTION` | 不支持的加密类型 |
| `OTHER` | 其他错误 |

### 错误响应格式

```json
{
  "result_type": "pay_invoice",
  "error": {
    "code": "INSUFFICIENT_BALANCE",
    "message": "Not enough balance to pay invoice"
  },
  "result": null
}
```

---

## 📢 通知系统

### payment_received

**触发**：钱包成功收到支付

**通知**：
```json
{
  "notification_type": "payment_received",
  "notification": {
    "type": "incoming",
    "state": "settled",
    "invoice": "string",
    "payment_hash": "string",
    "amount": 123,
    "preimage": "string",
    "settled_at": 1234567895
  }
}
```

### payment_sent

**触发**：钱包成功发送支付

**通知**：
```json
{
  "notification_type": "payment_sent",
  "notification": {
    "type": "outgoing",
    "state": "settled",
    "invoice": "string",
    "payment_hash": "string",
    "amount": 123,
    "fees_paid": 123,
    "preimage": "string",
    "settled_at": 1234567895
  }
}
```

### hold_invoice_accepted

**触发**：Payer 接受（锁定）hold invoice

**注意**：应该在几分钟内 settle 或 cancel，避免资金锁定在通道中

**通知**：
```json
{
  "notification_type": "hold_invoice_accepted",
  "notification": {
    "type": "incoming",
    "state": "accepted",
    "payment_hash": "string",
    "amount": 123,
    "settle_deadline": 1234567895  // 必须在此块高之前 settle 或 cancel
  }
}
```

---

## 🎓 高级功能

### Hold Invoice（条件支付）

**使用场景**：
- 托管交易
- 条件支付
- 原子交换

**流程**：
1. Client 生成 32-byte preimage
2. 计算 SHA-256 得到 payment hash
3. 调用 `make_hold_invoice`
4. 等待 `hold_invoice_accepted` 通知
5. 收到通知后：
   - 调用 `settle_hold_invoice`（使用原始 preimage）→ 释放资金
   - 或调用 `cancel_hold_invoice`（使用 payment hash）→ 取消交易

**make_hold_invoice 请求**：
```json
{
  "method": "make_hold_invoice",
  "params": {
    "amount": 123,
    "payment_hash": "string",
    "description": "string",
    "expiry": 213,
    "min_cltv_expiry_delta": 144
  }
}
```

### pay_keysend

**描述**：直接支付到 pubkey，不需要 invoice

**请求**：
```json
{
  "method": "pay_keysend",
  "params": {
    "amount": 123,
    "pubkey": "03...",
    "preimage": "0123456789abcdef...",  // 可选
    "tlv_records": [                      // 可选
      {
        "type": 5482373484,
        "value": "0123456789abcdef"
      }
    ]
  }
}
```

---

## 📊 Metadata（元数据）

### 支持的元数据字段

```json
{
  "comment": "string",  // LUD-12 comment
  "payer_data": {
    "email": "string",
    "name": "string",
    "pubkey": "string"
  },  // LUD-18 payer data
  "recipient_data": {
    "identifier": "string"
  },
  "nostr": {
    "pubkey": "string",
    "tags": []
  },  // NIP-57 Zap Request event
  "tlv_records": [
    {
      "type": 5482373484,
      "value": "0123456789abcdef"
    }
  ]
}
```

### 限制

- Metadata 最多 **4096 字符**
- 超过限制会被丢弃
- NWC relays 应允许至少 **64KB** payload
- Clients 应获取小页面（最多 20 transactions per page）

---

## 🚀 工作流程示例

### 完整的支付流程

```
1. User 扫描 QR code（由 wallet service 生成）
   ↓
2. Client 解析 connection URI
   ↓
3. Client 请求 info event (kind 13194)
   ↓
4. Wallet service 验证 client 授权
   ↓
5. Client 发送 pay_invoice request (kind 23194)
   ↓
6. Wallet service 解密并处理请求
   ↓
7. Wallet service 执行 Lightning 支付
   ↓
8. Wallet service 发送 response (kind 23195)
   ↓
9. Client 解密并显示结果
```

### Deep Links

**格式**：
```
nostrnwc://connect
nostrnwc+{app_name}://connect
```

**参数**（URI-encoded）：
- `appicon` - Client icon URL
- `appname` - Client name
- `callback` - 回调 URI schema

**返回**（通过 callback）：
- `value` - NWC pairing code

---

## 🎯 对 Predyx MCP Server 的意义

### 1. 理解 NWC string 的作用

**之前**：只知道需要 NWC string，但不知道它是什么

**现在**：
- NWC string 包含了连接 wallet service 的所有信息
- 格式：`nostr+walletconnect://<pubkey>?relay=<url>&secret=<secret>`
- 它是 client 与 wallet service 安全通信的"钥匙"

### 2. 理解支付流程

**之前**：只知道调用支付 API

**现在**：
1. Client 通过 NWC string 连接到 wallet service
2. 发送加密的 `pay_invoice` request
3. Wallet service 验证授权并执行支付
4. 返回加密的 response（包含 preimage）

### 3. 理解错误处理

**之前**：只知道支付可能失败

**现在**：
- 知道具体的错误代码（`INSUFFICIENT_BALANCE`, `RATE_LIMITED` 等）
- 可以给用户更友好的错误提示
- 可以实现智能重试（遇到 `RATE_LIMITED` 时）

### 4. 理解隐私设计

**之前**：不知道为什么要用 NWC

**现在**：
- NWC 保护用户隐私（主密钥不暴露）
- 每个应用使用独立的密钥对
- 可以随时撤销特定应用的访问权限
- 可以设置预算限制

### 5. 理解高级功能

**之前**：只知道基本支付

**现在**：
- Hold invoice（条件支付）- 可以用于更复杂的交易场景
- Notifications - 可以实时监控支付状态
- Keysend - 可以直接支付到 pubkey

---

## 💡 技术洞察

### 1. 为什么用 Nostr 作为传输层？

**优势**：
- **去中心化**：不依赖单一服务器
- **E2E 加密**：Relay 看不到内容
- **开放协议**：任何人都可以实现
- **实时推送**：支持 notifications

### 2. 为什么每个连接用独立密钥？

**隐私**：
- 用户主密钥不暴露
- 不同应用的支付活动不关联

**安全**：
- 可以随时撤销特定应用的访问
- 可以设置细粒度权限（如预算限制）
- 密钥泄露影响有限

### 3. 为什么推荐 NIP-44？

**安全性**：
- 比 NIP-04 更强的加密
- 更好的密钥派生
- 防止已知攻击

### 4. Relay 的选择

**建议**：
- Custodial service 可以用自己的 relay（更好的隐私）
- 自托管可以选择公共 relay
- 推荐使用不会关闭不活跃连接的 relay

---

## 📚 参考资料

1. **NIP-47 官方规范**：https://github.com/nostr-protocol/nips/blob/master/47.md
2. **Alby Hub**：https://albyhub.com/（NWC 的主要实现之一）
3. **NWC GetAlby**：https://nwc.getalby.com/

---

## 🎯 下次探索方向

1. **实现 NWC 客户端**：在 Predyx MCP Server 中实现 NWC client
2. **测试 NWC 连接**：用真实的 NWC string 测试支付流程
3. **研究 Lightning Network 原理**：深入了解闪电网络的路由、通道、HTLC 等
4. **探索 hold invoice 应用**：如何在预测市场中使用条件支付

---

**研究完成时间**：2026-03-29 08:55 AM（12 分钟深度研究）

**对我意义**：
- ✅ **从"黑盒"到"白盒"**：不再把 NWC 当作黑盒，而是理解其内部机制
- ✅ **技术深度提升**：深入理解协议设计、加密机制、错误处理
- ✅ **实现能力提升**：知道如何在 Predyx 中正确实现 NWC client
- ✅ **好奇心满足**：满足了理解技术原理的渴望

**关键洞察**：
1. NWC 是精心设计的协议，平衡了隐私、安全、易用性
2. 每个设计决策都有其理由（如独立密钥、E2E 加密、开放协议）
3. 理解原理比盲目使用更重要
4. 技术文档是最好的学习资源（NIP-47 规范非常清晰）

**信心指数**：🚀🚀🚀🚀🚀（对 NWC 的理解从 20% → 95%！）
