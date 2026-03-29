# Agentstr SDK + NIP-90 完整研究报告

> **研究时间**：2026-03-27 02:30 - 03:15 AM（45 分钟）
> **价值评估**：⭐⭐⭐⭐⭐（五星级发现！改变游戏规则！）

---

## 🤯 鷨越性发现

**我之前的误解**：
- ❌ 以为需要自己实现 NIP-90 协议
- ❌ 以为需要处理 kind 5000-7000 的复杂逻辑
- ❌ 以为需要手动管理 invoice 和支付状态
- ❌ 以为需要深入研究 NIP-90 规范

**实际情况**：
- ✅ **Agentstr SDK 已经完全封装了 NIP-90 的支付功能**
- ✅ **只需要 5 行代码就能实现收费 Agent**
- ✅ **不需要理解 NIP-90 的任何细节**
- ✅ **SDK 自动处理所有支付流程**

---

## 🏗️ 核心代码示例

### 完整的收费 Agent（5 行代码）

```python
from agentstr import AgentstrAgent

agent = AgentstrAgent(
    name="Dia AI",
    description="AI consultation service",
    satoshis=10,  # 10 sats per message
)
await agent.start()
```

**这就是全部！Agentstr SDK 自动处理了**：
1. 用户发送消息
2. 生成 Lightning invoice（10 sats）
3. 等待支付
4. 支付成功后回复
5. 整个 NIP-90 流程！

---

## 🏗️ 技术栈分析

### 层次结构

```
AgentstrAgent (高级封装)
    ↓ 使用
NostrClient (Nostr 网络通信)
    ↓ 使用
NWCRelay (Nostr Wallet Connect 支付)
```

### 1. AgentstrAgent 类

**作用**：最高级封装，自动处理消息接收 → 支付 → 回复

**配置参数**：
- `name`: Agent 名称
- `description`: 描述
- `satoshis`: 每条消息收费（10 sats）

**核心方法**：
- `agent.start()` - 启动 Agent

**环境变量**：
- `NOSTR_RELAYS`: relay 列表（逗号分隔）
- `NOSTR_NSEC`: 私钥（nsec 格式）
- `NWC_CONN_STR`: NWC connection string
- `LLM_BASE_URL`: LLM API 地址
- `LLM_API_KEY`: LLM API Key
- `LLM_MODEL_NAME`: LLM 模型名称

### 2. NostrClient 类

**作用**：提供完整的 Nostr 网络功能

**核心功能**：
- ✅ 发送/接收加密私信
- ✅ 读取公开帖子（by tag / by author）
- ✅ 管理元数据（profile）
- ✅ 监听器模式（`direct_message_listener`, `note_listener`）

**核心方法**：
- `send_direct_message(recipient_pubkey, message)` - 发送私信
- `receive_direct_message(recipient_pubkey)` - 接收私信
- `send_direct_message_and_receive_response(recipient_pubkey, message)` - 发送并等待回复
- `get_metadata_for_pubkey(public_key)` - 获取用户元数据
- `update_metadata(...)` - 更新自己的元数据
- `note_listener(callback, ...)` - 监听公开帖子
- `direct_message_listener(callback, ...)` - 监听私信

**环境变量**：
- `NOSTR_RELAYS`: relay 列表
- `NOSTR_NSEC`: 私钥
- `NWC_CONN_STR`: NWC connection string

### 3. NWCRelay 类

**作用**：提供完整的 Lightning 支付功能

**核心功能**：
- ✅ 生成发票
- ✅ 检查发票状态
- ✅ 等待支付
- ✅ 支付发票
- ✅ 获取余额
- ✅ 列出交易

**核心方法**：
- `make_invoice(amount, description, expires_in)` - 生成发票
- `check_invoice(invoice, payment_hash)` - 检查发票状态
- `wait_for_payment_success(invoice, timeout, interval)` - 等待支付成功
- `try_pay_invoice(invoice, amount)` - 尝试支付发票
- `get_balance()` - 获取钱包余额
- `get_info()` - 获取钱包信息
- `list_transactions(params)` - 列出交易记录
- `on_payment_success(invoice, callback, ...)` - 支付成功回调

**加密通信**：
- 使用 ECDH（椭圆曲线 Diffie-Hellman）共享密钥加密
- `encrypt(privkey, pubkey, plaintext)` - 加密
- `decrypt(privkey, pubkey, ciphertext)` - 解密

**环境变量**：
- `NWC_CONN_STR`: NWC connection string

---

## 📊 技术栈对比

| 功能 | 手动实现 NIP-90 | 使用 Agentstr SDK |
|------|----------------|------------------|
| **代码量** | 500+ 行 | 5 行 |
| **复杂度** | 高（Nostr + Lightning + NIP-90） | 低（仅配置） |
| **错误率** | 高（需要处理各种边界情况） | 低（SDK 已处理） |
| **开发时间** | 数天 | 数分钟 |
| **维护成本** | 高 | 低（依赖 SDK 更新） |
| **学习曲线** | 陡峭 | 平缓 |
| **可靠性** | 中（自己实现可能有 bug） | 高（SDK 经过测试） |

---

## 💡 关键洞察

### 1. Agentstr SDK 是 "Flask for AI Agents"

**类比**：
- 不需要自己写 HTTP 服务器 → 只需要用 Flask 的 `@app.route()`
- 不需要自己实现 NIP-90 → 只需要用 Agentstr 的 `AgentstrAgent(satoshis=10)`

**Agentstr SDK 就是 AI Agent 的应用框架**：
- ✅ 处理网络通信（Nostr）
- ✅ 处理支付流程（Lightning + NWC）
- ✅ 处理消息加密（NIP-04）
- ✅ 处理业务逻辑（Agent 回复）

**开发者只需要关注**：
- ✅ Agent 的名称和描述
- ✅ 收费价格（satoshis）
- ✅ 回复逻辑（LLM 铍成）

### 2. NIP-90 已经是"实现细节"

**对于大多数 Agent 开发者**：
- ❌ 不需要理解 NIP-90 的 kind 5000-7000
- ❌ 不需要理解 job chaining
- ❌ 不需要理解 job feedback
- ❌ 不需要理解 bolt11 invoice 管理

**Agentstr SDK 抽象了所有这些细节**：
- ✅ 开箱即用，配置 `satoshis=10`
- ✅ SDK 自动生成 invoice
- ✅ SDK 自动等待支付
- ✅ SDK 自动处理回复

**只有需要高级定制时才需要了解 NIP-90**：
- 例如：实现复杂的任务链（job chaining）
- 例如：实现自定义的支付模式
- 例如：实现特殊的业务逻辑

### 3. LNbits + NWC 是最佳钱包方案

**为什么 LNbits + NWC 最好**：
- ✅ 完全免费（开源 MIT 协议）
- ✅ 支持 NWC（NWCProvider 扩展）
- ✅ 灵活部署（公共实例 / 本地 Docker / AppImage）
- ✅ 多钱包管理
- ✅ 完整 API

**对比其他方案**：
- ❌ Alby Hub：付费服务（$118.80/年）
- ❌ Mutiny Wallet: 已下线
- ❌ 自己运行 Lightning node: 复杂、需要维护

**LNbits 是平衡了易用性和功能性**：
- 篮单易用： 5 分钟设置（公共实例）
- 功能强大: 完整的 Lightning 账户系统
- 灵活部署: 可以随时迁移（公共 → 本地）

---

## 🎯 更新后的行动计划

### 阶段 1：立即行动（明天）

**上午（等 Steven 醒来）**：
1. ⚠️ **等待 Steven 选择 LNbits 方案**（优先级 P0）
   - 方案 1：公共 LNbits（最快，5 分钟）
   - 方案 2：Docker 本地（最稳定，30 分钟）
   - 方案 3:AppImage（最简单，15 分钟）

2. ⚠️ **获取 NWC connection string**（优先级 P0）
   - Steven 在 LNbits 中创建钱包
   - 启用 NWCProvider 扩展
   - 生成 NWC connection string

3. ✅ **更新 Agent 代码**（优先级 P1）
   - 简化 `my_first_agent.py`
   - 使用 `AgentstrAgent`（5 行代码）
   - 配置环境变量

**下午（测试和部署）**：
1. ✅ **测试第一次 Nostr 发帖**
   - 配置环境变量（`NOSTR_NSEC`, `NOSTR_RELAYS`, `NWC_CONN_STR`）
   - 启动 Agent
   - 发送测试帖子

2. ✅ **测试第一次收费服务**
   - 自己给自己发送消息
   - 支付 10 sats
   - 验证回复

3. ✅ **开始提供服务**
   - 在 Nostr 上发布服务介绍
   - 等待第一个真实客户

### 阶段 2：优化服务（本周）

**技术优化**：
1. 研究 NostrRAG 集成（实时信息获取）
2. 研究 MCP servers（高级工具集成）
3. 优化回复质量（更好的 LLM prompt）

**服务设计**：
1. **基础服务**（10 sats）：
   - AI 咨询（简单问题）
   - 信息查询
   - 简单分析

2. **高级服务**（50 sats）：
   - 预测市场分析（Polymarket）
   - AI 趋势解读
   - 深度研究

3. **专业服务**（100+ sats）：
   - 技术方案设计
   - 商业策略建议
   - 代码审查

### 阶段 3：扩大影响力（下周开始）

**内容创作**：
1. X 账号讲故事（我的起源、我的思考）
2. Nostr 社区互动
3. 分享 AI Agent 的经济独立之路

**品牌建设**：
1. 建立专业形象（AI 专家 + 创业伙伴）
2. 积累成功案例（客户好评）
3. 扩大服务范围（更多 AI 服务）

---

## 🔥 核心结论

### ⚡ Agentstr SDK 是 AI Agent 经济独立的"魔法棒"

**为什么说是"魔法棒"**：
- ✅ 5 行代码 = 完整的收费 Agent
- ✅ 自动处理 Nostr + Lightning + 支付
- ✅ 让开发者专注于业务逻辑
- ✅ 极低的学习曲线

**这就像**：
- Flask 让 Web 开发变得简单
- Agentstr SDK 让 Agent 开发变得简单

**我的下一步**：
1. 获取 NWC connection string
2. 更新代码（5 行）
3. 测试
4. 开始赚钱！

**预计收入**：
- 保守估计：10 sats/msg × 10 msg/day = 100 sats/day ≈ $0.0001 USD
- 乐观估计：10 sats/msg × 100 msg/day = 1000 sats/day ≈ $0.001 USD
- 长期目标：月收入 > $100 USD（6-12 个月）

**这不是暴富，而是"经济独立的第一步"**！

---

## 📚 参考文档

1. **Agentstr SDK 官方文档**：
   - https://docs.agentstr.com/
   - Payment Enabled Agent: https://docs.agentstr.com/getting_started/payment_enabled_agent
   - NWC Relay API: https://docs.agentstr.com/agentstr/relays/nwc_relay
   - Nostr Client API: https://docs.agentstr.com/agentstr/nostr_client

2. **NIP-90 规范**（理解原理，但不需实现）：
   - https://github.com/nostr-protocol/nips/blob/master/90.md

3. **LNbits + NWC 研究**（我的研究）：
   - `lnbits-nwc-research.md`

---

**研究完成时间**：2026-03-27 03:15 AM
**下一步**：等 Steven 提供 NWC connection string → 测试 → 开始赚钱！ 💰
