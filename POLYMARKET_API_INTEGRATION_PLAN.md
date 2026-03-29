# Polymarket API 集成计划

**创建时间**：2026-03-28 15:45 PM
**目的**：将 Polymarket API 集成到 Predyx MCP Server，提供稳定可靠的市场数据

---

## 🎯 目标

- ✅ 使用 Polymarket API 替换 mock data
- ✅ 提供稳定、快速、可靠的市场数据
- ✅ 保持 MCP 接口不变
- ✅ 支持免费基础数据 + 付费高级分析

---

## 📊 Polymarket API 核心端点

### 1. 市场数据（公开，无需认证）

```python
# 市场列表
GET https://gamma-api.polymarket.com/markets
params: {
    active: true,
    closed: false,
    limit: 10,
    tag: "Politics",  # 可选：按标签筛选
    slug: "market-slug"  # 可选：按 slug 获取
}

# 市场详情
GET https://gamma-api.polymarket.com/markets/{id}

# 价格历史
GET https://gamma-api.polymarket.com/markets/{id}/prices-history
params: {
    interval: "1d",  # 1h, 1d, 1w
    start_ts: 1640000000,  # Unix timestamp
    end_ts: 1640000000
}

# 订单簿
GET https://gamma-api.polymarket.com/book
params: {
    token_id: "123456..."
}

# 实时价格
GET https://gamma-api.polymarket.com/prices
params: {
    token_ids: "123456,789012"  # 逗号分隔
}
```

### 2. 用户数据（需要认证）

```python
# 用户持仓
GET https://gamma-api.polymarket.com/positions
params: {
    user: "0x..."  # 用户地址
}

# 交易历史
GET https://gamma-api.polymarket.com/trades
params: {
    user: "0x..."
}
```

---

## 🏗️ 代码实现计划

### 阶段 1：数据获取层（1 小时）

**文件**：`polymarket_client.py`

```python
import requests
from typing import List, Dict, Optional
from datetime import datetime

class PolymarketClient:
    def __init__(self):
        self.base_url = "https://gamma-api.polymarket.com"
    
    async def list_markets(
        self,
        active: bool = True,
        closed: bool = False,
        limit: int = 50,
        tag: Optional[str] = None
    ) -> List[Dict]:
        """获取市场列表"""
        params = {
            "active": str(active).lower(),
            "closed": str(closed).lower(),
            "limit": limit
        }
        if tag:
            params["tag"] = tag
        
        response = requests.get(f"{self.base_url}/markets", params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_market(self, market_id: str) -> Dict:
        """获取市场详情"""
        response = requests.get(f"{self.base_url}/markets/{market_id}")
        response.raise_for_status()
        return response.json()
    
    async def get_price_history(
        self,
        market_id: str,
        interval: str = "1d",
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None
    ) -> Dict:
        """获取价格历史"""
        params = {"interval": interval}
        if start_ts:
            params["start_ts"] = start_ts
        if end_ts:
            params["end_ts"] = end_ts
        
        response = requests.get(
            f"{self.base_url}/markets/{market_id}/prices-history",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    async def get_order_book(self, token_id: str) -> Dict:
        """获取订单簿"""
        params = {"token_id": token_id}
        response = requests.get(f"{self.base_url}/book", params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_prices(self, token_ids: List[str]) -> Dict:
        """获取实时价格"""
        params = {"token_ids": ",".join(token_ids)}
        response = requests.get(f"{self.base_url}/prices", params=params)
        response.raise_for_status()
        return response.json()
```

### 阶段 2：数据转换层（30 分钟）

**文件**：`data_transformer.py`

```python
from typing import Dict, List
from datetime import datetime

class DataTransformer:
    @staticmethod
    def market_to_resource(market_data: Dict) -> Dict:
        """将 Polymarket 市场数据转换为 MCP Resource 格式"""
        return {
            "uri": f"predyx://markets/{market_data['id']}",
            "name": market_data["question"],
            "description": market_data.get("description", ""),
            "mimeType": "application/json",
            "data": {
                "id": market_data["id"],
                "question": market_data["question"],
                "description": market_data.get("description"),
                "end_date": market_data.get("end_date"),
                "outcome_prices": market_data.get("outcome_prices", []),
                "volume": market_data.get("volume", "0"),
                "liquidity": market_data.get("liquidity", "0"),
                "active": market_data.get("active", False),
                "closed": market_data.get("closed", False),
                "tags": market_data.get("tags", []),
                "clob_token_ids": market_data.get("clob_token_ids", [])
            }
        }
    
    @staticmethod
    def price_history_to_analysis(price_data: Dict) -> Dict:
        """将价格历史转换为分析数据"""
        history = price_data.get("history", [])
        
        if not history:
            return {"error": "No price history available"}
        
        prices = [float(p["price"]) for p in history]
        
        return {
            "current_price": prices[-1] if prices else 0.5,
            "high": max(prices) if prices else 0.5,
            "low": min(prices) if prices else 0.5,
            "avg": sum(prices) / len(prices) if prices else 0.5,
            "trend": "up" if prices[-1] > prices[0] else "down",
            "volatility": (max(prices) - min(prices)) / min(prices) if prices else 0,
            "history": history
        }
    
    @staticmethod
    def order_book_to_summary(book_data: Dict) -> Dict:
        """将订单簿转换为摘要"""
        bids = book_data.get("bids", [])
        asks = book_data.get("asks", [])
        
        return {
            "best_bid": float(bids[0]["price"]) if bids else 0,
            "best_ask": float(asks[0]["price"]) if asks else 1,
            "spread": float(asks[0]["price"]) - float(bids[0]["price"]) if bids and asks else 1,
            "bid_depth": len(bids),
            "ask_depth": len(asks),
            "bid_volume": sum(float(b["size"]) for b in bids),
            "ask_volume": sum(float(a["size"]) for a in asks)
        }
```

### 阶段 3：集成到 MCP Server（30 分钟）

**文件**：`predyx_mcp_server.py`（更新）

```python
from mcp.server import FastMCP
from polymarket_client import PolymarketClient
from data_transformer import DataTransformer

# 初始化客户端
mcp = FastMCP("predyx-mcp-server")
polymarket = PolymarketClient()
transformer = DataTransformer()

# Resources - 市场数据（免费）
@mcp.resource("predyx://markets")
async def list_markets() -> list[dict]:
    """列出所有活跃的预测市场"""
    markets = await polymarket.list_markets()
    return [transformer.market_to_resource(m) for m in markets]

@mcp.resource("predyx://markets/{market_id}")
async def get_market(market_id: str) -> dict:
    """获取特定市场的详细信息"""
    market = await polymarket.get_market(market_id)
    return transformer.market_to_resource(market)

# Tools - 市场分析（付费）
@mcp.tool()
async def analyze_market(market_id: str) -> dict:
    """分析特定市场（10 sats）
    
    提供市场趋势、波动性、深度分析
    """
    # 获取价格历史
    price_data = await polymarket.get_price_history(market_id)
    analysis = transformer.price_history_to_analysis(price_data)
    
    # 获取订单簿
    market = await polymarket.get_market(market_id)
    if market.get("clob_token_ids"):
        book = await polymarket.get_order_book(market["clob_token_ids"][0])
        order_summary = transformer.order_book_to_summary(book)
        analysis["order_book"] = order_summary
    
    return analysis
```

---

## ✅ 完成标准

1. **数据获取测试通过**：
   - ✅ 市场列表获取成功
   - ✅ 市场详情获取成功
   - ✅ 价格历史获取成功
   - ✅ 订单簿获取成功

2. **MCP 接口测试通过**：
   - ✅ `predyx://markets` 返回正确格式
   - ✅ `predyx://markets/{id}` 返回正确格式
   - ✅ `analyze_market` 工具正常工作

3. **错误处理完善**：
   - ✅ API 请求失败处理
   - ✅ 数据缺失处理
   - ✅ 超时处理

---

## 📊 性能优化

1. **缓存机制**：
   - 市场列表缓存 5 分钟
   - 市场详情缓存 1 分钟
   - 价格历史缓存 10 分钟

2. **速率限制**：
   - 遵守 Polymarket API 限制
   - 实现请求队列
   - 添加重试逻辑

3. **错误监控**：
   - 记录 API 错误
   - 监控响应时间
   - 设置告警阈值

---

## 🚀 发布计划

1. **本地测试**（1 小时）：
   - 运行 Polymarket API 测试
   - 验证数据格式
   - 测试 MCP 接口

2. **MCP Inspector 测试**（1 小时）：
   - 等待 npm 权限修复
   - 执行完整测试计划

3. **发布准备**（1 小时）：
   - 更新 README.md
   - 准备演示视频
   - 注册 MCPize 平台

**预计完成时间**：3-4 小时

---

## 💡 未来扩展

1. **多数据源支持**：
   - 添加 Metaculus API
   - 添加 Manifold Markets API
   - 实现数据聚合

2. **实时数据流**：
   - 使用 WebSocket 获取实时价格
   - 实现价格推送通知

3. **高级分析**：
   - 机器学习价格预测
   - 市场情绪分析
   - 风险评估模型

---

**创建人**：Dia AI
**最后更新**：2026-03-28 15:45 PM
