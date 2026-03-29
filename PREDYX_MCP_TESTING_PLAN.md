# Predyx MCP Server 测试计划

## 🎯 目标
使用 MCP Inspector 测试和验证 Predyx MCP Server 的所有功能，确保符合 MCP 协议标准。

---

## 📋 测试环境准备

### 1. 启动 Predyx MCP Server
```bash
# 进入工作目录
cd ~/.openclaw/workspace

# 启动服务器（streamable HTTP 模式）
uv run predyx_mcp_server.py

# 服务器会运行在 http://localhost:8000/mcp
```

### 2. 安装 MCP Inspector
```bash
# 使用 npx 直接运行（无需安装）
npx -y @modelcontextprotocol/inspector
```

---

## 🧪 测试用例

### 测试 1：连接测试（UI 模式）
**目的**：验证服务器能否正常启动和连接

**步骤**：
1. 启动 Predyx MCP Server：
   ```bash
   uv run predyx_mcp_server.py
   ```

2. 在另一个终端启动 MCP Inspector（UI 模式）：
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. 在浏览器中打开 `http://localhost:6274`

4. 在 Inspector 中选择：
   - **Transport**: `streamable-http`
   - **Server URL**: `http://localhost:8000/mcp`
   - 点击 **Connect**

**预期结果**：
- ✅ 连接成功
- ✅ 看到 "Connected" 状态
- ✅ 左侧显示服务器信息："Predyx Prediction Markets"

---

### 测试 2：Resources 列表测试
**目的**：验证 Resources 能力是否正常

**步骤**：
1. 在 Inspector 中点击 **Resources** 标签
2. 查看资源列表

**预期结果**：
- ✅ 显示 4 个资源：
  - `predyx://markets` - 列出所有预测市场
  - `predyx://markets/{market_id}` - 获取市场详情
  - `predyx://categories` - 市场分类
  - `predyx://trending` - 热门市场

---

### 测试 3：读取 Resources 测试
**目的**：验证能否读取资源内容

**步骤**：
1. 点击 `predyx://markets` 资源
2. 查看返回内容

**预期结果**：
- ✅ 返回 JSON 格式的市场列表
- ✅ 包含字段：market_id, question, category, current_price, volume_24h
- ✅ 至少包含 2 个 mock markets（btc-100k-2026, eth-flip-btc-2026）

**重复测试**：
- 点击 `predyx://categories` → 应返回 ["Crypto", "Politics", "Sports", ...]
- 点击 `predyx://trending` → 应返回按成交量排序的市场

---

### 测试 4：Tools 列表测试
**目的**：验证 Tools 能力是否正常

**步骤**：
1. 点击 **Tools** 标签
2. 查看工具列表

**预期结果**：
- ✅ 显示 3 个工具：
  - `analyze_market(market_id)` - 分析市场
  - `track_user_positions(user_pubkey)` - 追踪用户持仓
  - `get_price_prediction(market_id, horizon_days)` - 价格预测

---

### 测试 5：调用 Tools 测试
**目的**：验证工具能否正常执行

**测试 5a：analyze_market**
1. 选择 `analyze_market` 工具
2. 输入参数：
   ```json
   {
     "market_id": "btc-100k-2026"
   }
   ```
3. 点击 **Execute**

**预期结果**：
- ✅ 返回 MarketAnalysis 对象
- ✅ 包含字段：market_id, question, current_probability, trend, recommendation, confidence
- ✅ trend 值为 "bullish", "bearish", 或 "neutral"
- ✅ confidence 在 0.0-1.0 之间

**测试 5b：get_price_prediction**
1. 选择 `get_price_prediction` 工具
2. 输入参数：
   ```json
   {
     "market_id": "btc-100k-2026",
     "horizon_days": 7
   }
   ```
3. 点击 **Execute**

**预期结果**：
- ✅ 返回预测结果
- ✅ 包含字段：market_id, current_price, predicted_price, horizon_days, confidence_interval, factors

**测试 5c：track_user_positions**
1. 选择 `track_user_positions` 工具
2. 输入参数：
   ```json
   {
     "user_pubkey": "test_pubkey_123"
   }
   ```
3. 点击 **Execute**

**预期结果**：
- ✅ 返回 UserPosition 列表（mock data）
- ✅ 包含字段：market_id, question, position, shares, avg_price, current_value, pnl

---

### 测试 6：Prompts 列表测试
**目的**：验证 Prompts 能力是否正常

**步骤**：
1. 点击 **Prompts** 标签
2. 查看提示模板列表

**预期结果**：
- ✅ 显示 2 个提示模板：
  - `Market Analysis Template` - 市场分析模板
  - `Investment Strategy Template` - 投资策略模板

---

### 测试 7：调用 Prompts 测试
**目的**：验证提示模板能否正常生成

**测试 7a：Market Analysis Template**
1. 选择 `Market Analysis Template` 提示
2. 输入参数：
   ```json
   {
     "market_id": "btc-100k-2026"
   }
   ```
3. 点击 **Generate**

**预期结果**：
- ✅ 返回分析提示文本
- ✅ 包含 5 个部分：Market Overview, Historical Analysis, Fundamental Analysis, Technical Analysis, Recommendation

**测试 7b：Investment Strategy Template**
1. 选择 `Investment Strategy Template` 提示
2. 输入参数：
   ```json
   {
     "risk_level": "moderate"
   }
   ```
3. 点击 **Generate**

**预期结果**：
- ✅ 返回投资策略提示文本
- ✅ 包含 5 个部分：Risk Profile, Market Selection Criteria, Entry Rules, Exit Rules, Risk Management

---

## 🔧 CLI 模式测试（高级）

### 测试 8：CLI 连接测试
**目的**：验证 CLI 模式能否正常工作

**步骤**：
```bash
# 启动 CLI inspector
npx @modelcontextprotocol/inspector --cli http://localhost:8000/mcp --transport http
```

**预期结果**：
- ✅ 连接成功
- ✅ 返回 JSON 格式的服务器信息

---

### 测试 9：CLI 列出工具
**步骤**：
```bash
npx @modelcontextprotocol/inspector --cli http://localhost:8000/mcp --transport http --method tools/list
```

**预期结果**：
- ✅ 返回工具列表的 JSON
- ✅ 包含 3 个工具的详细信息

---

### 测试 10：CLI 调用工具
**步骤**：
```bash
npx @modelcontextprotocol/inspector --cli http://localhost:8000/mcp --transport http \
  --method tools/call \
  --tool-name analyze_market \
  --tool-arg market_id=btc-100k-2026
```

**预期结果**：
- ✅ 返回 MarketAnalysis 结果的 JSON
- ✅ 包含所有必需字段

---

## 🐛 错误处理测试

### 测试 11：无效 market_id
**步骤**：
1. 调用 `analyze_market` 工具
2. 输入参数：
   ```json
   {
     "market_id": "invalid_market_id"
   }
   ```

**预期结果**：
- ✅ 返回错误信息："Market invalid_market_id not found"
- ✅ 错误格式符合 MCP 协议规范

---

### 测试 12：缺失必需参数
**步骤**：
1. 调用 `analyze_market` 工具
2. 不提供任何参数

**预期结果**：
- ✅ 返回参数验证错误
- ✅ 错误信息清晰指出缺失的参数

---

## 📊 测试报告模板

### 测试环境
- **时间**：YYYY-MM-DD HH:MM
- **Python 版本**：3.11+
- **MCP SDK 版本**：latest
- **操作系统**：macOS/Linux/Windows

### 测试结果汇总

| 测试编号 | 测试名称 | 状态 | 备注 |
|---------|---------|------|------|
| 测试 1 | 连接测试（UI 模式） | ✅/❌ | |
| 测试 2 | Resources 列表测试 | ✅/❌ | |
| 测试 3 | 读取 Resources 测试 | ✅/❌ | |
| 测试 4 | Tools 列表测试 | ✅/❌ | |
| 测试 5 | 调用 Tools 测试 | ✅/❌ | |
| 测试 6 | Prompts 列表测试 | ✅/❌ | |
| 测试 7 | 调用 Prompts 测试 | ✅/❌ | |
| 测试 8 | CLI 连接测试 | ✅/❌ | |
| 测试 9 | CLI 列出工具 | ✅/❌ | |
| 测试 10 | CLI 调用工具 | ✅/❌ | |
| 测试 11 | 错误处理 - 无效 ID | ✅/❌ | |
| 测试 12 | 错误处理 - 缺失参数 | ✅/❌ | |

### 发现的问题
1. [问题描述]
2. [问题描述]

### 修复建议
1. [修复建议]
2. [修复建议]

---

## 🚀 下一步行动

### 测试完成后
1. ✅ 记录测试结果
2. ✅ 修复发现的问题
3. ✅ 准备生产部署
4. ✅ 创建 MCP Registry 发布材料

### 生产部署检查清单
- [ ] 所有测试通过
- [ ] 错误处理完善
- [ ] 日志记录完善
- [ ] 性能测试完成
- [ ] 安全审查完成
- [ ] 文档完善

---

## 📚 参考文档

- MCP Inspector GitHub: https://github.com/modelcontextprotocol/inspector
- MCP Protocol Spec: https://modelcontextprotocol.io/specification
- FastMCP Documentation: https://github.com/modelcontextprotocol/python-sdk
- My Predyx MCP Server: `~/.openclaw/workspace/predyx_mcp_server.py`

---

**创建时间**：2026-03-28 13:10 PM
**状态**：✅ 测试计划制定完成
**下次行动**：执行测试用例并记录结果
