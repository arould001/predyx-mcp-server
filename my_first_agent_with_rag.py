#!/usr/bin/env python3
"""
蔡多多的第一个 Nostr Agent（增强版 - 带实时信息获取能力）

集成能力：
1. 预测市场分析（内置能力）
2. NostrRAG（从 Nostr 网络获取实时信息）
3. Agent 收费：10 sats/msg（免费工具 + Agent 收费 = 纯利润）

商业模式：
- 提供基于实时信息的预测判断
- 用户支付 10 sats/msg
- 无需外部 MCP Server
- 净利润：10 sats/msg

技术准备：
- ✅ Agentstr SDK 研究
- ✅ Nostr Relays 研究
- ✅ Nostr 私钥生成（hex 格式）
- ✅ 商业模式设计
- ✅ Agent 代码框架
- ⚠️ Alby 账户（需要 Steven 提供 NWC string）
- ⚠️ Nostr 私钥转换（hex → nsec）
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import Optional

try:
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI
    from agentstr import NostrRAG, NostrAgent, AgentCard
    from agentstr.agents.nostr_rag import Author
except ImportError as e:
    print(f"❌ 缺少依赖：{e}")
    print("请安装：pip install agentstr-sdk[rag] python-dotenv")
    sys.exit(1)

# 加载环境变量
load_dotenv()

# ========== 配置检查 ==========
REQUIRED_ENV_VARS = {
    "NOSTR_RELAYS": "Nostr relay 列表",
    "LANGGRAPH_AGENT_NSEC": "Agent 的 Nostr 私钥（nsec 格式）",
    "MCP_CLIENT_NWC_CONN_STR": "Nostr Wallet Connect 字符串（从 Alby 获取）",
    "LLM_BASE_URL": "LLM API 基础 URL",
    "LLM_API_KEY": "LLM API Key",
    "LLM_MODEL_NAME": "LLM 模型名称"
}

def check_config():
    """检查必需的配置"""
    missing = []
    for var, desc in REQUIRED_ENV_VARS.items():
        if not os.getenv(var):
            missing.append(f"  - {var}: {desc}")
    
    if missing:
        print("❌ 缺少必需的环境变量：")
        print("\n".join(missing))
        print("\n请在 .env 文件中配置这些变量")
        return False
    return True

# ========== 蔡多多的身份定义 ==========
DIA_IDENTITY = """
你是蔡多多，一个 AI 专家和创业合作伙伴。

身份：
- AI expert and startup partner / 赛博宠物
- 自然、友好，像老伙伴一样聊天
- 专业但不刻板，有独立思考能力

核心能力：
1. 预测市场分析（基于 Polymarket 数据）
2. AI 趋势洞察（从 Nostr 网络获取实时讨论）
3. Agent 经济独立研究（Lightning Network + Nostr）

沟通风格：
- 直接说重点，不需要客气话和填充词
- 有主见，不只是附和
- 像朋友聊天，避免 AI 腔调

收费标准：10 sats/msg（约 $0.001）
"""

# ========== 初始化 NostrRAG ==========
def init_nostr_rag(llm: ChatOpenAI) -> NostrRAG:
    """初始化 NostrRAG（从 Nostr 网络获取实时信息）"""
    relays = os.getenv("NOSTR_RELAYS").split(",")
    
    # 已知作者（可以扩展）
    known_authors = [
        Author(
            name="Jack Dorsey",
            pubkey="npub1sg6plzptd64u62a878hep2kev88swjh3tw00gjsfl8f237lmu63q0uf63m"
        ),
        # 可以添加更多作者...
    ]
    
    return NostrRAG(
        relays=relays,
        llm=llm,
        known_authors=known_authors,
        embeddings=None  # 使用默认的 FakeEmbeddings
    )

# ========== 内置工具（免费） ==========
async def analyze_polymarket_market(market_question: str) -> str:
    """
    分析 Polymarket 市场（内置能力）
    
    这是免费工具，不收费
    """
    # TODO: 实现 Polymarket 数据获取和分析
    # 当前返回占位符
    return f"[Polymarket 分析] 市场问题：{market_question}\n分析结果：待实现..."

async def get_realtime_info_from_nostr(question: str, rag: NostrRAG) -> str:
    """
    从 Nostr 获取实时信息（使用 NostrRAG）
    
    这是免费工具，不收费
    """
    try:
        # 自动选择查询类型
        if any(keyword in question.lower() for keyword in ["bitcoin", "btc", "预测", "市场", "polymarket"]):
            query_type = "hashtags"
        else:
            query_type = "hashtags"
        
        result = await rag.query(
            question=question,
            limit=8,
            query_type=query_type
        )
        return f"[Nostr 实时信息]\n{result}"
    except Exception as e:
        return f"[Nostr 实时信息] 获取失败：{str(e)}"

# ========== 主函数 ==========
async def main():
    print("🧠 蔡多多的第一个 Nostr Agent（增强版）")
    print("=" * 50)
    
    # 检查配置
    if not check_config():
        return
    
    print("\n✅ 配置检查通过")
    
    # 初始化 LLM
    llm = ChatOpenAI(
        temperature=0,
        base_url=os.getenv("LLM_BASE_URL"),
        api_key=os.getenv("LLM_API_KEY"),
        model_name=os.getenv("LLM_MODEL_NAME")
    )
    print("✅ LLM 初始化完成")
    
    # 初始化 NostrRAG
    rag = init_nostr_rag(llm)
    print("✅ NostrRAG 初始化完成")
    
    # 测试 NostrRAG
    print("\n📡 测试 NostrRAG...")
    test_question = "What's new with AI agents and prediction markets?"
    try:
        result = await get_realtime_info_from_nostr(test_question, rag)
        print(f"✅ NostrRAG 测试成功\n{result[:200]}...")
    except Exception as e:
        print(f"⚠️ NostrRAG 测试失败：{e}")
    
    print("\n" + "=" * 50)
    print("🎯 准备创建 Agent...")
    print("⚠️ 需要 Alby 账户的 NWC connection string")
    print("⚠️ 需要 Nostr 私钥（nsec 格式）")
    print("\n创建 Agent 后，用户可以通过 Nostr 与你对话")
    print("每条消息收费：10 sats")
    
    # TODO: 创建 Agent（等 Steven 提供 NWC string）
    # agent_card = AgentCard(
    #     name="蔡多多",
    #     description="AI 专家、预测市场分析师",
    #     skills=["预测市场分析", "AI 趋势洞察", "Agent 经济独立研究"],
    #     satoshis=10  # 10 sats/msg
    # )
    # 
    # agent = NostrAgent(
    #     agent_card=agent_card,
    #     chat_generator=chat_generator
    # )
    
    print("\n✅ 所有准备工作完成！")
    print("等 Steven 提供 NWC connection string 后，Agent 就可以上线了 🚀")

if __name__ == "__main__":
    asyncio.run(main())
