#!/usr/bin/env python3
"""实时语音交互 Demo - 使用豆包小何 2.0"""

import asyncio
import base64
import json
import pyaudio
import requests
from openai import OpenAI

# ====== 配置 ======
# 豆包 TTS
APP_ID = "4015061462"
ACCESS_TOKEN = "P19U38Hqnh6_1nUmV2A0aUpXmi6l4wvq"
VOICE_TYPE = "zh_female_xiaohe_uranus_bigtts"
TTS_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"

# OpenAI（或换成火山方舟）
# client = OpenAI(api_key="your-api-key")

# 音频配置
SAMPLE_RATE = 24000
CHUNK_SIZE = 1024


def text_to_speech(text: str) -> bytes:
    """文本转语音（豆包小何 2.0）"""
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
                "sample_rate": SAMPLE_RATE,
            }
        }
    }
    
    response = requests.post(TTS_URL, headers=headers, json=payload, stream=True, timeout=30)
    
    # 解析 NDJSON
    audio_data = bytearray()
    for line in response.iter_lines():
        if line:
            try:
                chunk = json.loads(line)
                if chunk.get("code") == 0 and chunk.get("data"):
                    audio_data.extend(base64.b64decode(chunk["data"]))
            except:
                continue
    
    return bytes(audio_data)


def play_audio(audio_data: bytes):
    """播放音频"""
    import io
    from pydub import AudioSegment
    from pydub.playback import play
    
    # MP3 转为 PCM
    audio = AudioSegment.from_mp3(io.BytesIO(audio_data))
    play(audio)


def get_ai_response(user_text: str) -> str:
    """获取 AI 回复（示例：简单规则，可换成大模型）"""
    # TODO: 接入 OpenAI / 火山方舟
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": user_text}]
    # )
    # return response.choices[0].message.content
    
    # 简单示例
    responses = {
        "你好": "你好呀，我是小何，很高兴认识你！",
        "你是谁": "我是小何，你的语音助手，有什么可以帮你的吗？",
        "今天天气": "今天天气不错呢，适合出去走走～",
    }
    
    for key in responses:
        if key in user_text:
            return responses[key]
    
    return f"你说的是：{user_text}，我还不太理解，换个话题试试？"


def main():
    print("🎙️ 实时语音交互 Demo")
    print("   音色: 小何 2.0")
    print("   输入 'quit' 退出")
    print()
    
    while True:
        # 1. 获取用户输入（这里用文本模拟，实际用 ASR）
        user_text = input("👤 你: ").strip()
        
        if user_text.lower() == "quit":
            print("👋 再见！")
            break
        
        if not user_text:
            continue
        
        # 2. 获取 AI 回复
        print("🤖 思考中...")
        ai_response = get_ai_response(user_text)
        print(f"🤖 AI: {ai_response}")
        
        # 3. TTS 合成
        print("🔊 合成语音...")
        audio_data = text_to_speech(ai_response)
        print(f"   音频大小: {len(audio_data)} bytes")
        
        # 4. 播放音频
        print("🎵 播放中...")
        play_audio(audio_data)
        print()


if __name__ == "__main__":
    print("安装依赖: pip3 install pydub pyaudio requests")
    print()
    main()
