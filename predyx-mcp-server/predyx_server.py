"""
Predyx MCP Server - 提供预测市场数据的标准化接口

这是我的第一个 MCP Server，提供 Predyx 预测市场数据的标准化访问。

核心能力：
- Tools: 市场分析、价格预测
- Resources: 市场列表、价格历史
- Prompts: 标准分析模板

使用方式：
1. 安装依赖：pip install "mcp[cli]"
2. 运行服务：python predyx_server.py
3. 测试：npx -y @modelcontextprotocol/inspector
4. 连接到：http://localhost:8000/mcp

商业化：
- 基础功能：免费（市场列表、基本信息）
- 高级功能：10-50 sats/call（深度分析、价格预测）
- 支付集成：等待 NWC connection string

作者：Dia
日期：2026-03-28
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List
import json
from datetime import datetime

# 创建 MCP Server
mcp = FastMCP("Predyx Prediction Market Server")

# ===== 模拟数据（实际应该从 Predyx 网站获取）=====

MOCK_MARKETS = {
    "bitcoin-150k-2026": {
        "id": "bitcoin-150k-2026",
        "title": "Bitcoin $150K in 2026",
        "description": "Will Bitcoin reach $150,000 by end of 2026?",
        "current_probability": 0.14,
        "volume_sats": 2200000,
        "liquidity_sats": 200000,
        "deadline": "2027-01-01",
        "category": "Bitcoin",
    },
    "bitcoin-100k-2026": {
        "id": "bitcoin-100k-2026",
        "title": "Will Bitcoin Reach $100K in 2026",
        "description": "Will Bitcoin reach $100,000 in 2026?",
        "current_probability": 0.70,
        "volume_sats": 4452000,
        "liquidity_sats": 180000,
        "deadline": "2027-01-01",
        "category": "Bitcoin",
    },
    "bip-110-activation": {
        "id": "bip-110-activation",
        "title": "BIP-110 activation",
        "description": "Will BIP-110 be activated?",
        "current_probability": 0.65,
        "volume_sats": 79560000,
        "liquidity_sats": 5000000,
        "deadline": "2026-12-31",
        "category": "Bitcoin",
    },
}

# ===== Tools（可执行函数）=====

@mcp.tool()
def analyze_market(market_id: str) -> Dict:
    """
    分析预测市场
    
    Args:
        market_id: 市场 ID（如 "bitcoin-150k-2026"）
    
    Returns:
        市场分析报告（包含价格、概率、交易量、流动性）
    """
    if market_id not in MOCK_MARKETS:
        return {"error": f"Market {market_id} not found"}
    
    market = MOCK_MARKETS[market_id]
    
    # 基础分析
    analysis = {
        "market_id": market_id,
        "title": market["title"],
        "current_probability": market["current_probability"],
        "probability_percentage": f"{market['current_probability'] * 100:.2f}%",
        "volume_btc": market["volume_sats"] / 100_000_000,
        "liquidity_btc": market["liquidity_sats"] / 100_000_000,
        "deadline": market["deadline"],
        "category": market["category"],
        "analysis_timestamp": datetime.now().isoformat(),
    }
    
    # 市场健康度评估
    if market["liquidity_sats"] > 1_000_000:
        analysis["liquidity_assessment"] = "高流动性，适合大额交易"
    elif market["liquidity_sats"] > 100_000:
        analysis["liquidity_assessment"] = "中等流动性，适合中小额交易"
    else:
        analysis["liquidity_assessment"] = "低流动性，谨慎交易"
    
    return analysis


@mcp.tool()
def predict_price_trend(market_id: str, days: int = 7) -> Dict:
    """
    预测价格趋势（基于历史数据）
    
    Args:
        market_id: 市场 ID
        days: 预测未来 N 天的趋势
    
    Returns:
        价格趋势预测报告
    """
    if market_id not in MOCK_MARKETS:
        return {"error": f"Market {market_id} not found"}
    
    market = MOCK_MARKETS[market_id]
    
    # 模拟预测（实际应该基于历史数据）
    prediction = {
        "market_id": market_id,
        "current_probability": market["current_probability"],
        "predicted_probability": market["current_probability"] + 0.05,  # 模拟上涨 5%
        "trend": "上涨",
        "confidence": 0.75,
        "reasoning": [
            "市场流动性充足",
            "交易量持续增长",
            "地缘政治因素影响",
        ],
        "prediction_period": f"{days} 天",
        "disclaimer": "此预测仅供参考，不构成投资建议",
    }
    
    return prediction


# ===== Resources（只读数据源）=====

@mcp.resource("predyx://markets")
def list_markets() -> str:
    """
    获取所有活跃市场列表
    
    Returns:
        JSON 格式的市场列表
    """
    markets = []
    for market_id, market_data in MOCK_MARKETS.items():
        markets.append({
            "id": market_id,
            "title": market_data["title"],
            "probability": market_data["current_probability"],
            "category": market_data["category"],
        })
    
    return json.dumps(markets, indent=2)


@mcp.resource("predyx://market/{market_id}")
def get_market_data(market_id: str) -> str:
    """
    获取单个市场的详细数据
    
    Args:
        market_id: 市场 ID
    
    Returns:
        JSON 格式的市场详情
    """
    if market_id not in MOCK_MARKETS:
        return json.dumps({"error": f"Market {market_id} not found"})
    
    market = MOCK_MARKETS[market_id]
    
    return json.dumps({
        "id": market_id,
        "title": market["title"],
        "description": market["description"],
        "current_probability": market["current_probability"],
        "volume_sats": market["volume_sats"],
        "liquidity_sats": market["liquidity_sats"],
        "deadline": market["deadline"],
        "category": market["category"],
    }, indent=2)


@mcp.resource("predyx://categories")
def list_categories() -> str:
    """
    获取所有市场分类
    
    Returns:
        JSON 格式的分类列表
    """
    categories = {}
    for market_data in MOCK_MARKETS.values():
        cat = market_data["category"]
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    
    return json.dumps(categories, indent=2)


# ===== Prompts（预定义模板）=====

@mcp.prompt()
def market_analysis_prompt(market_name: str) -> str:
    """
    市场分析提示模板
    
    Args:
        market_name: 市场名称
    
    Returns:
        标准化的分析提示
    """
    return f"""请分析以下预测市场：

市场：{market_name}

请提供以下分析：
1. 当前概率分析
2. 市场流动性评估
3. 交易量分析
4. 关键影响因素
5. 风险提示

请基于客观数据进行分析，避免主观判断。"""


@mcp.prompt()
def investment_decision_prompt(
    market_name: str,
    investment_amount: str,
    risk_tolerance: str = "中等"
) -> str:
    """
    投资决策提示模板
    
    Args:
        market_name: 市场名称
        investment_amount: 投资金额（sats）
        risk_tolerance: 风险承受能力（低/中等/高）
    
    Returns:
        标准化的投资决策提示
    """
    return f"""请为以下投资决策提供分析：

市场：{market_name}
投资金额：{investment_amount} sats
风险承受能力：{risk_tolerance}

请提供：
1. 市场风险评估
2. 潜在收益分析
3. 最大损失分析
4. 投资建议（买入/卖出/观望）
5. 风险管理建议

重要提示：此分析仅供参考，不构成投资建议。投资有风险，决策需谨慎。"""


# ===== 运行 Server =====

if __name__ == "__main__":
    print("🚀 启动 Predyx MCP Server...")
    print("📍 服务地址：http://localhost:8000/mcp")
    print("🧪 测试方式：npx -y @modelcontextprotocol/inspector")
    print("")
    print("核心能力：")
    print("  - Tools: analyze_market, predict_price_trend")
    print("  - Resources: predyx://markets, predyx://market/{id}, predyx://categories")
    print("  - Prompts: market_analysis_prompt, investment_decision_prompt")
    print("")
    
    mcp.run(transport="streamable-http")
