#!/usr/bin/env python3
"""
使用 Alby Access Token 测试 NWC 功能
"""

import requests

ALBY_TOKEN = "N2ZJN2JIZJATOTA5YY0ZMTCYLTKXNJGTNWJLZJEXYZAYYZQ1"

# 测试 Alby API
headers = {"Authorization": f"Bearer {ALBY_TOKEN}"}

# 1. 检查账户信息
print("1️⃣ 检查账户信息...")
resp = requests.get("https://api.getalby.com/me", headers=headers)
print(f"账户信息: {resp.json()}")

# 2. 检查 NWC 连接
print("\n2️⃣ 检查 NWC 连接...")
resp = requests.get("https://api.getalby.com/nwc", headers=headers)
print(f"NWC 连接: {resp.json()}")

# 3. 创建 NWC 连接
print("\n3️⃣ 尝试创建 NWC 连接...")
resp = requests.post(
    "https://api.getalby.com/nwc",
    headers=headers,
    json={"name": "Dia AI Agent"}
)
print(f"创建结果: {resp.json()}")
