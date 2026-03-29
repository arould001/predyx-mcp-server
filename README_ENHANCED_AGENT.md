# 增强版 Agent 代码框架

> **创建时间**：2026-03-27 03:29 AM
> **状态**：✅ 代码框架完成，等待 NWC connection string 测试

---

## 🎯 核心功能

### 1. **NostrRAG 集成** ⭐⭐⭐⭐⭐
- 从 Nostr 网络获取实时信息
- 支持 hashtags、authors、notes 查询
- 为 Agent 提供基于实时信息的预测判断

### 2. **NWC 支付集成** ⭐⭐⭐⭐⭐
- 接收比特币支付（通过 Nostr Wallet Connect）
- 支持自定义收费标准（默认 10 sats/msg）
- 自动生成发票

### 3. **DSPy Agent 集成** ⭐⭐⭐⭐
- 高级推理能力（可选）
- 支持 ReAct、CoT 等推理模式
- 自动选择最优推理策略

### 4. **智能信息检测** ⭐⭐⭐⭐
- 自动判断消息是否需要实时信息
- 提取关键词进行 Nostr 查询
- 结合实时信息生成回复

---

## 📋 使用步骤

### 步骤 1：安装依赖

```bash
# 安装 agentstr SDK（包含 NostrRAG + NWC）
uv add agentstr-sdk[all]

# 安装 DSPy（可选，用于高级推理）
uv add dspy
```

### 步骤 2：配置环境变量

```bash
# 复制配置模板
cp .env.agent.example .env

# 编辑 .env 文件
nano .env
```

**关键配置**：
- `NWC_CONNECTION_STRING`：NWC 连接字符串（格式：`nostr+walletconnect://...`）
- `NOSTR_RELAYS`：Nostr relay 列表
- `AGENT_PRICE_SATS`：收费标准（默认 10 sats/msg）

### 步骤 3：运行 Agent

```bash
# 运行增强版 Agent
python enhanced_agent.py
```

---

## 🔧 代码结构

```python
class EnhancedDiaAgent:
    """增强版 Dia Agent"""

    def __init__(self, nwc_connection_string, nostr_relays, llm_config):
        """初始化 Agent"""

    async def get_real_time_info(self, query, query_type):
        """从 Nostr 网络获取实时信息"""

    async def process_message(self, user_message):
        """处理用户消息（核心功能）"""

    async def charge_user(self, amount_sats=10):
        """收取用户费用（通过 NWC）"""
```

---

## 💡 使用示例

### 示例 1：查询 Polymarket 趋势

```python
user_message = "Polymarket 上 AI 相关的市场有什么趋势？"
response = await agent.process_message(user_message)

# Agent 会：
# 1. 检测到需要实时信息
# 2. 从 Nostr 查询 "polymarket" + "AI"
# 3. 结合实时信息生成回复
```

### 示例 2：提供 AI 咨询服务

```python
user_message = "帮我分析一下比特币市场的最新动态"
response = await agent.process_message(user_message)

# Agent 会：
# 1. 从 Nostr 获取比特币相关讨论
# 2. 分析趋势
# 3. 生成回复
# 4. 通过 NWC 收取 10 sats
```

---

## 🚀 下一步行动

### 1. 获取 NWC Connection String

**优先级**：P0（最高）

**步骤**：
1. 选择 LNbits 方案：
   - **方案 1**：公共 LNbits 实例（5 分钟）
   - **方案 2**：Docker 本地部署（30 分钟）
   - **方案 3**：AppImage（15 分钟）

2. 创建 NWC 连接：
   - 安装 NWCProvider 扩展
   - 创建新的 NWC 连接
   - 复制 connection string

3. 配置环境变量：
   - 更新 `.env` 文件
   - 填入 `NWC_CONNECTION_STRING`

### 2. 测试 Agent

```bash
# 测试 NostrRAG
python enhanced_agent.py

# 测试 NWC 支付
# （需要用户发送消息）
```

### 3. 部署到 Nostr

```bash
# 1. 创建 Nostr 身份
# 2. 发布 Agent 服务
# 3. 开始接收付费咨询
```

---

## 📊 技术架构

```
┌─────────────────────────────────────────┐
│           增强版 Agent 架构              │
└─────────────────────────────────────────┘
                   ↓
    ┌──────────────────────────────┐
    │   用户消息 → process_message  │
    └──────────────────────────────┘
                   ↓
    ┌──────────────────────────────┐
    │   检测是否需要实时信息        │
    └──────────────────────────────┘
           ↓              ↓
       [需要]          [不需要]
           ↓              ↓
    ┌─────────────┐  ┌─────────────┐
    │  NostrRAG   │  │   DSPy      │
    │  查询 Nostr │  │   基础推理   │
    └─────────────┘  └─────────────┘
           ↓              ↓
    ┌──────────────────────────────┐
    │       生成回复                │
    └──────────────────────────────┘
                   ↓
    ┌──────────────────────────────┐
    │   NWC 收取 10 sats            │
    └──────────────────────────────┘
                   ↓
              返回用户
```

---

## ⚠️ 注意事项

### 1. 安全警告
- **NWC connection string** 相当于私钥，不要泄露
- **不要在公共实例存储大量资金**
- **定期备份钱包数据**

### 2. 成本控制
- **NostrRAG 查询**：免费（只需 Nostr relays）
- **LLM API**：按使用量计费（可选）
- **NWC 交易**：闪电网络手续费（极低）

### 3. 性能优化
- **缓存 NostrRAG 查询结果**（减少重复查询）
- **使用本地 Nostr relay**（提高查询速度）
- **批量处理消息**（降低 API 成本）

---

## 📚 参考资源

- **Agentstr SDK 文档**：https://github.com/nikandrovali/agentstr
- **NWC 协议**：https://nwc.dev
- **DSPy 文档**：https://github.com/stanfordnlp/dspy
- **Nostr 协议**：https://github.com/nostr-protocol/nostr

---

**创建者**：Dia
**状态**：✅ 代码框架完成，等待 NWC string 测试
**下次更新**：获取 NWC string 后，进行实际测试
