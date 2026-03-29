#!/usr/bin/env python3
"""豆包 TTS HTTP 测试脚本 - 小何 2.0 音色（HTTP Chunked 方式）"""

import requests
import json

# 配置
APP_ID = "4015061462"
ACCESS_TOKEN = "P19U38Hqnh6_1nUmV2A0aUpXmi6l4wvq"
VOICE_TYPE = "zh_female_xiaohe_uranus_bigtts"  # 小何 2.0

# HTTP API URL
API_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"


def test_tts(text: str, output_file: str = "output.mp3"):
    """测试 TTS（HTTP Chunked 方式）"""
    headers = {
        "X-Api-App-Key": APP_ID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": "seed-tts-2.0",
        "Content-Type": "application/json",
    }
    
    payload = {
        "req_params": {
            "text": text,
            "speaker": VOICE_TYPE,
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000,
            }
        }
    }
    
    print(f"🎙️ 豆包 TTS 测试（HTTP Chunked）")
    print(f"   音色: {VOICE_TYPE}")
    print(f"   文本: {text}")
    print(f"   URL: {API_URL}")
    print()
    
    try:
        print("📤 发送请求...")
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        
        print(f"📥 响应状态: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ 请求失败: {response.text}")
            return False
        
        # 解析 NDJSON 响应（多行 JSON）
        import base64
        audio_data = bytearray()
        
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    if chunk.get("code") == 0 and chunk.get("data"):
                        audio_chunk = base64.b64decode(chunk["data"])
                        audio_data.extend(audio_chunk)
                        print(f"🎵 收到音频: {len(audio_chunk)} bytes")
                except json.JSONDecodeError:
                    continue
        
        if not audio_data:
            print(f"❌ 没有收到音频数据")
            return False
        
        with open(output_file, 'wb') as f:
            f.write(audio_data)
        
        print(f"✅ 音频已保存: {output_file} ({len(audio_data)} bytes)")
        return True
    
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    
    text = sys.argv[1] if len(sys.argv) > 1 else "大家好，我是小何，很高兴认识你们"
    output = sys.argv[2] if len(sys.argv) > 2 else "output.mp3"
    
    test_tts(text, output)
