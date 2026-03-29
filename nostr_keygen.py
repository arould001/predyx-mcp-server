#!/usr/bin/env python3
"""
Nostr Key Generator - 简化版
用于生成 Nostr 密钥对（nsec/npub）

依赖：
  pip install secp256k1 bech32

运行：
  python3 nostr_keygen.py
"""

from secp256k1 import PrivateKey
from bech32 import bech32

def generate_nostr_keys():
    """生成 Nostr 密钥对"""
    # 生成私钥
    private_key = PrivateKey()
    private_bytes = private_key.private_key
    public_bytes = private_key.pubkey.serialize()[1:]  # 去掉第一个字节（前缀）
    
    # 转换为 bech32 格式
    public_bits = bech32.convertbits(public_bytes, 8, 5)
    private_bits = bech32.convertbits(private_bytes, 8, 5)
    
    npub = bech32.bech32_encode("npub", public_bits, bech32.Encoding.BECH32)
    nsec = bech32.bech32_encode("nsec", private_bits, bech32.Encoding.BECH32)
    
    return {
        "private_key_hex": private_bytes.hex(),
        "public_key_hex": public_bytes.hex(),
        "nsec": nsec,
        "npub": npub
    }

if __name__ == "__main__":
    keys = generate_nostr_keys()
    
    print("=" * 60)
    print("🔑 Nostr 密钥对")
    print("=" * 60)
    print(f"Private Key (hex): {keys['private_key_hex']}")
    print(f"Public Key (hex):  {keys['public_key_hex']}")
    print("-" * 60)
    print(f"nsec (私钥): {keys['nsec']}")
    print(f"npub (公钥): {keys['npub']}")
    print("=" * 60)
    print("\n⚠️  警告：nsec 是你的私钥，绝对不要泄露！")
    print("💡 提示：npub 是你的公钥，可以公开分享。")
