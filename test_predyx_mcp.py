#!/usr/bin/env python3
"""
简单的 MCP Server 测试脚本
测试 Predyx MCP Server 的核心功能
"""

import sys
import json
import asyncio

# 模拟 MCP 客户端调用
async def test_resources():
    """测试 Resources 功能"""
    print("=" * 60)
    print("测试 1: Resources - 列出市场")
    print("=" * 60)
    
    # 模拟调用 predyx://markets
    from predyx_mcp_server import list_markets
    result = await list_markets()
    print(f"✅ 市场列表: {result[:100]}...")  # 只显示前100个字符
    
    print("\n" + "=" * 60)
    print("测试 2: Resources - 获取市场详情")
    print("=" * 60)
    
    # 模拟调用 predyx://markets/btc-100k-2026
    from predyx_mcp_server import get_market_details
    result = await get_market_details("btc-100k-2026")
    print(f"✅ 市场详情: {result[:100]}...")
    
    print("\n" + "=" * 60)
    print("测试 3: Resources - 列出分类")
    print("=" * 60)
    
    from predyx_mcp_server import list_categories
    result = await list_categories()
    print(f"✅ 分类列表: {result}")

async def test_tools():
    """测试 Tools 功能"""
    print("\n" + "=" * 60)
    print("测试 4: Tools - 市场分析")
    print("=" * 60)
    
    from predyx_mcp_server import analyze_market
    result = await analyze_market("btc-100k-2026")
    print(f"✅ 市场分析:")
    print(f"   - 问题: {result.question}")
    print(f"   - 当前概率: {result.current_probability}")
    print(f"   - 趋势: {result.trend}")
    print(f"   - 建议: {result.recommendation}")
    print(f"   - 信心度: {result.confidence}")
    
    print("\n" + "=" * 60)
    print("测试 5: Tools - 用户持仓追踪")
    print("=" * 60)
    
    from predyx_mcp_server import track_user_positions
    result = await track_user_positions("test_pubkey")
    print(f"✅ 用户持仓:")
    for pos in result:
        print(f"   - 市场: {pos.question}")
        print(f"   - 持仓: {pos.position}")
        print(f"   - 盈亏: {pos.pnl} sats")
    
    print("\n" + "=" * 60)
    print("测试 6: Tools - 价格预测")
    print("=" * 60)
    
    from predyx_mcp_server import get_price_prediction
    result = await get_price_prediction("btc-100k-2026", horizon_days=7)
    print(f"✅ 价格预测:")
    print(f"   - 当前价格: {result['current_price']}")
    print(f"   - 预测价格: {result['predicted_price']}")
    print(f"   - 预测区间: {result['confidence_interval']}")

async def test_prompts():
    """测试 Prompts 功能"""
    print("\n" + "=" * 60)
    print("测试 7: Prompts - 市场分析模板")
    print("=" * 60)
    
    from predyx_mcp_server import analyze_market_prompt
    result = analyze_market_prompt("btc-100k-2026")
    print(f"✅ 市场分析模板:")
    print(f"   {result[:200]}...")  # 只显示前200个字符
    
    print("\n" + "=" * 60)
    print("测试 8: Prompts - 投资策略模板")
    print("=" * 60)
    
    from predyx_mcp_server import investment_strategy_prompt
    result = investment_strategy_prompt("moderate")
    print(f"✅ 投资策略模板:")
    print(f"   {result[:200]}...")

async def main():
    """运行所有测试"""
    print("\n" + "🧪" * 30)
    print("Predyx MCP Server - 功能测试")
    print("🧪" * 30 + "\n")
    
    try:
        # 测试 Resources
        await test_resources()
        
        # 测试 Tools
        await test_tools()
        
        # 测试 Prompts
        await test_prompts()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过!")
        print("=" * 60)
        print("\n总结:")
        print("- ✅ Resources: 3/3 测试通过")
        print("- ✅ Tools: 3/3 测试通过")
        print("- ✅ Prompts: 2/2 测试通过")
        print("\n下一步:")
        print("1. 修复 npm 权限问题")
        print("2. 使用 MCP Inspector UI 模式测试")
        print("3. 准备 MCP Registry 发布材料")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
