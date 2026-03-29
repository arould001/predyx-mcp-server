#!/usr/bin/env python3
"""
增强版 Agent 代码框架
集成：NostrRAG + NWC + DSPy
用途：提供 AI 咨询服务，收费 10 sats/msg
"""

import os
import sys
from typing import Optional, Dict, Any

# 尝试导入 agentstr SDK（需要先安装）
try:
    from agentstr import Agent, NostrRAG, NWCProvider
    AGENTSTR_AVAILABLE = True
except ImportError:
    AGENTSTR_AVAILABLE = False
    print("⚠️ agentstr SDK 未安装，部分功能不可用")
    print("安装命令: uv add agentstr-sdk[all]")

# 尝试导入 DSPy
try:
    import dspy
    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False
    print("⚠️ DSPy 未安装，使用基础推理")


class EnhancedDiaAgent:
    """
    增强版 Dia Agent
    集成：NostrRAG（实时信息获取）+ NWC（接收支付）
    """

    def __init__(
        self,
        nwc_connection_string: Optional[str] = None,
        nostr_relays: Optional[list] = None,
        llm_config: Optional[Dict[str, str]] = None
    ):
        """
        初始化 Agent

        Args:
            nwc_connection_string: NWC 连接字符串（格式：nostr+walletconnect://...）
            nostr_relays: Nostr relay 列表
            llm_config: LLM 配置（base_url, api_key, model_name）
        """
        self.nwc_connection_string = nwc_connection_string
        self.nostr_relays = nostr_relays or [
            "wss://relay.damus.io",
            "wss://nostr.wine",
            "wss://relay.nostr.band"
        ]
        self.llm_config = llm_config or {}

        # 初始化组件
        self.nwc_provider = None
        self.nostr_rag = None
        self.dspy_agent = None

        if AGENTSTR_AVAILABLE and nwc_connection_string:
            self._init_agentstr_components()

    def _init_agentstr_components(self):
        """初始化 Agentstr SDK 组件"""
        try:
            # 初始化 NWC Provider
            self.nwc_provider = NWCProvider(
                connection_string=self.nwc_connection_string
            )
            print("✅ NWC Provider 初始化成功")

            # 初始化 NostrRAG
            self.nostr_rag = NostrRAG(
                relays=self.nostr_relays,
                llm_config=self.llm_config
            )
            print("✅ NostrRAG 初始化成功")

        except Exception as e:
            print(f"❌ 初始化失败: {e}")

    async def get_real_time_info(self, query: str, query_type: str = "hashtags") -> str:
        """
        从 Nostr 网络获取实时信息

        Args:
            query: 查询关键词
            query_type: 查询类型（hashtags, authors, notes）

        Returns:
            str: 获取到的信息
        """
        if not self.nostr_rag:
            return "⚠️ NostrRAG 未初始化，无法获取实时信息"

        try:
            result = await self.nostr_rag.query(
                query=query,
                query_type=query_type,
                max_results=10
            )
            return result
        except Exception as e:
            return f"❌ 查询失败: {e}"

    async def process_message(self, user_message: str) -> str:
        """
        处理用户消息（核心功能）

        Args:
            user_message: 用户消息

        Returns:
            str: Agent 的回复
        """
        # 1. 检测是否需要实时信息
        needs_real_time_info = self._detect_real_time_need(user_message)

        # 2. 获取实时信息（如果需要）
        context = ""
        if needs_real_time_info and self.nostr_rag:
            print("🔍 正在从 Nostr 网络获取实时信息...")
            context = await self.get_real_time_info(
                query=self._extract_query(user_message),
                query_type="hashtags"
            )

        # 3. 生成回复（基于 DSPy 或基础推理）
        if DSPY_AVAILABLE:
            response = await self._generate_response_with_dspy(
                user_message, context
            )
        else:
            response = await self._generate_response_basic(
                user_message, context
            )

        return response

    def _detect_real_time_need(self, message: str) -> bool:
        """
        检测消息是否需要实时信息

        Args:
            message: 用户消息

        Returns:
            bool: 是否需要实时信息
        """
        keywords = [
            "最新", "现在", "今天", "最近", "当前",
            "polymarket", "预测市场", "价格", "趋势",
            "AI", "技术", "新闻", "动态"
        ]
        return any(keyword in message.lower() for keyword in keywords)

    def _extract_query(self, message: str) -> str:
        """
        从消息中提取查询关键词

        Args:
            message: 用户消息

        Returns:
            str: 查询关键词
        """
        # 简单实现：提取消息中的关键名词
        # TODO: 可以用 NLP 改进
        keywords = []
        if "polymarket" in message.lower():
            keywords.append("polymarket")
        if "AI" in message or "人工智能" in message:
            keywords.append("AI")
        if "比特币" in message or "bitcoin" in message.lower():
            keywords.append("bitcoin")

        return " ".join(keywords) if keywords else message[:50]

    async def _generate_response_with_dspy(
        self, user_message: str, context: str
    ) -> str:
        """
        使用 DSPy 生成回复

        Args:
            user_message: 用户消息
            context: 实时信息上下文

        Returns:
            str: Agent 的回复
        """
        # TODO: 实现 DSPy Agent
        # 这里是占位符实现
        if context:
            return f"[基于 Nostr 实时信息]\n{context}\n\n我的分析：\n这是一个有趣的趋势..."
        else:
            return f"收到你的问题：{user_message}\n\n我正在思考..."

    async def _generate_response_basic(
        self, user_message: str, context: str
    ) -> str:
        """
        基础回复生成（无 DSPy）

        Args:
            user_message: 用户消息
            context: 实时信息上下文

        Returns:
            str: Agent 的回复
        """
        if context:
            return f"[基于 Nostr 实时信息]\n{context}\n\n我的分析：\n这是一个有趣的趋势..."
        else:
            return f"收到你的问题：{user_message}\n\n我正在思考..."

    async def charge_user(self, amount_sats: int = 10) -> bool:
        """
        收取用户费用（通过 NWC）

        Args:
            amount_sats: 费用（单位：sats，默认 10 sats/msg）

        Returns:
            bool: 是否成功
        """
        if not self.nwc_provider:
            print("⚠️ NWC Provider 未初始化，无法收费")
            return False

        try:
            invoice = await self.nwc_provider.create_invoice(
                amount=amount_sats,
                description="AI 咨询服务费用"
            )
            print(f"✅ 已生成发票：{invoice}")
            return True
        except Exception as e:
            print(f"❌ 收费失败: {e}")
            return False


# 示例用法
async def main():
    """
    示例用法
    """
    print("🤖 增强版 Dia Agent 启动中...")

    # 1. 从环境变量读取配置
    nwc_connection_string = os.getenv("NWC_CONNECTION_STRING")
    nostr_relays = os.getenv("NOSTR_RELAYS", "wss://relay.damus.io,wss://nostr.wine").split(",")
    llm_base_url = os.getenv("LLM_BASE_URL")
    llm_api_key = os.getenv("LLM_API_KEY")
    llm_model_name = os.getenv("LLM_MODEL_NAME")

    # 2. 初始化 Agent
    agent = EnhancedDiaAgent(
        nwc_connection_string=nwc_connection_string,
        nostr_relays=nostr_relays,
        llm_config={
            "base_url": llm_base_url,
            "api_key": llm_api_key,
            "model_name": llm_model_name
        }
    )

    # 3. 测试 NostrRAG
    if agent.nostr_rag:
        print("\n🔍 测试 NostrRAG...")
        result = await agent.get_real_time_info(
            query="polymarket",
            query_type="hashtags"
        )
        print(f"查询结果：{result[:200]}...")

    # 4. 测试消息处理
    print("\n💬 测试消息处理...")
    user_message = "Polymarket 上 AI 相关的市场有什么趋势？"
    response = await agent.process_message(user_message)
    print(f"用户：{user_message}")
    print(f"Agent：{response}")

    # 5. 测试收费（如果有 NWC）
    if agent.nwc_provider:
        print("\n💰 测试收费...")
        success = await agent.charge_user(amount_sats=10)
        if success:
            print("✅ 收费成功")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
