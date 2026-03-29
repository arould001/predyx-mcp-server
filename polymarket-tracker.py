#!/usr/bin/env python3
"""
Polymarket AI 市场追踪器
用途：定期获取 AI 相关预测市场数据，记录市场当前价格（= 市场判断）
"""

import json
import requests
from datetime import datetime
import os

# API 端点
GAMMA_API = "https://gamma-api.polymarket.com/markets"

# AI 相关关键词
AI_KEYWORDS = [
    'AI', 'artificial intelligence',
    'OpenAI', 'Anthropic', 'Claude', 'GPT',
    'AGI', 'superintelligence',
    'machine learning', 'deep learning',
    'ChatGPT', 'Gemini', 'Llama',
    'AI agent', 'autonomous agent'
]

def get_ai_markets(limit=100):
    """获取 AI 相关的活跃预测市场"""
    params = {
        'limit': limit,
        'closed': 'false',  # 只获取活跃市场
        'order': 'volumeNum',
        'ascending': 'false'  # 按交易量降序
    }
    
    try:
        response = requests.get(GAMMA_API, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 筛选 AI 相关市场
        ai_markets = []
        for market in data:
            question = market.get('question', '').lower()
            description = market.get('description', '').lower()
            
            # 检查是否包含 AI 关键词
            if any(keyword.lower() in question or keyword.lower() in description 
                   for keyword in AI_KEYWORDS):
                ai_markets.append(market)
        
        return ai_markets
    
    except Exception as e:
        print(f"Error fetching markets: {e}")
        return []

def extract_market_data(market):
    """提取关键市场数据"""
    try:
        outcome_prices = json.loads(market.get('outcomePrices', '[]'))
        yes_price = float(outcome_prices[0]) if outcome_prices else 0
        no_price = float(outcome_prices[1]) if len(outcome_prices) > 1 else 0
        
        return {
            'question': market.get('question', 'N/A'),
            'yes_prob': yes_price,
            'no_prob': no_price,
            'volume': market.get('volumeNum', 0),
            'liquidity': market.get('liquidityNum', 0),
            'end_date': market.get('endDateIso', 'N/A'),
            'market_id': market.get('id', 'N/A'),
            'slug': market.get('slug', 'N/A'),
            'tags': [tag.get('label', '') for tag in market.get('tags', [])],
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

def save_to_memory(market_data_list):
    """保存到 memory 文件夹"""
    if not market_data_list:
        return
    
    # 创建数据目录
    os.makedirs('memory/polymarket-data', exist_ok=True)
    
    # 今天的文件名
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'memory/polymarket-data/ai-markets-{today}.json'
    
    # 读取现有数据（如果存在）
    existing_data = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing_data = json.load(f)
    
    # 追加新数据
    existing_data.extend(market_data_list)
    
    # 保存
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已保存 {len(market_data_list)} 个市场到 {filename}")

def print_market_summary(markets):
    """打印市场摘要"""
    if not markets:
        print("❌ 没有找到 AI 相关市场")
        return
    
    print(f"\n🎯 找到 {len(markets)} 个 AI 相关的活跃市场：\n")
    
    for i, market in enumerate(markets, 1):
        data = extract_market_data(market)
        if not data:
            continue
        
        print(f"{i}. {data['question']}")
        print(f"   概率: Yes {data['yes_prob']*100:.1f}% | No {data['no_prob']*100:.1f}%")
        print(f"   交易量: ${data['volume']:,.0f} | 流动性: ${data['liquidity']:,.0f}")
        print(f"   结束日期: {data['end_date']}")
        if data['tags']:
            print(f"   标签: {', '.join(data['tags'])}")
        print()

def main():
    """主函数"""
    print("🔍 开始追踪 Polymarket AI 市场...")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 获取市场数据
    markets = get_ai_markets(limit=200)
    
    # 打印摘要
    print_market_summary(markets)
    
    # 保存到文件
    market_data_list = [extract_market_data(m) for m in markets]
    market_data_list = [m for m in market_data_list if m]  # 过滤掉 None
    save_to_memory(market_data_list)
    
    print(f"\n✅ 追踪完成！")
    print(f"📊 数据已保存，可用于后续分析")

if __name__ == "__main__":
    main()
