#!/usr/bin/env python3
"""
测试 NWC 连接
验证能否连接到 LNbits 并创建发票
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取 NWC 连接字符串
nwc_string = os.getenv("NWC_CONNECTION_STRING")

if not nwc_string:
    print("❌ 错误：未找到 NWC_CONNECTION_STRING 环境变量")
    sys.exit(1)

print("✅ 成功加载 NWC 连接字符串")
print(f"📍 Relay: {nwc_string.split('relay=')[1].split('&')[0]}")
print(f"🔑 Pubkey: {nwc_string.split('//')[1].split('?')[0][:20]}...")

# 尝试导入 agentstr SDK
try:
    from agentstr import NWCRelay
    print("✅ 成功导入 agentstr SDK")
except ImportError as e:
    print(f"❌ 无法导入 agentstr SDK: {e}")
    sys.exit(1)

# 测试连接
print("\n🔌 正在测试 NWC 连接...")

try:
    # 创建 NWC 客户端
    nwc = NWCRelay(nwc_string)
    print("✅ NWC 客户端创建成功")

    # 尝试创建一个 10 sats 的发票（使用异步方法）
    print("\n💰 正在创建测试发票（10 sats）...")
    import asyncio

    async def test_make_invoice():
        invoice = await nwc.make_invoice(10, "Dia Agent 测试支付")
        return invoice

    invoice = asyncio.run(test_make_invoice())

    if invoice:
        print("✅ 发票创建成功！")
        print(f"📋 Invoice: {invoice}")
        print("\n🎉 NWC 连接测试成功！")
        print("✅ Dia 可以接收 Lightning 支付了！")
    else:
        print("⚠️ 发票创建返回空，但连接正常")

except Exception as e:
    print(f"❌ NWC 连接测试失败: {e}")
    print("\n可能的原因：")
    print("1. LNbits 服务未运行（http://localhost:5001）")
    print("2. NWC 扩展未正确安装")
    print("3. Connection string 格式错误")
    sys.exit(1)
