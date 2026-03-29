#!/usr/bin/env python3
"""豆包 TTS 测试脚本 - 小何 2.0 音色"""

import asyncio
import websockets
import json
import struct
import uuid

# 配置
APP_ID = "4015061462"
ACCESS_TOKEN = "P19U38Hqnh6_1nUmV2A0aUpXmi6l4wvq"
VOICE_TYPE = "zh_female_xiaohe_uranus_bigtts"  # 小何 2.0

# WebSocket URL
WS_URL = "wss://openspeech.bytedance.com/api/v3/tts/bidirection"


def build_request_header(msg_type: int, msg_type_specific_flags: int, serial_method: int = 1,
                         compression: int = 0, reserved: int = 0) -> bytes:
    """构建 WebSocket 二进制协议 header"""
    # Byte 0: protocol version (4 bits) + header size (4 bits)
    byte0 = (1 << 4) | 1  # version=1, header_size=4
    # Byte 1: message type (4 bits) + message type specific flags (4 bits)
    byte1 = (msg_type << 4) | msg_type_specific_flags
    # Byte 2: serialization method (4 bits) + compression method (4 bits)
    byte2 = (serial_method << 4) | compression
    # Byte 3: reserved
    byte3 = reserved
    return bytes([byte0, byte1, byte2, byte3])


def build_start_session_request(text: str) -> bytes:
    """构建 StartSession 请求"""
    payload = {
        "event": 3,  # StartSession
        "namespace": "BidirectionalTTS",
        "req_params": {
            "text": text,
            "speaker": VOICE_TYPE,
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000,
            }
        }
    }
    payload_bytes = json.dumps(payload).encode('utf-8')
    
    # Full-client request (msg_type=1, flags=4)
    header = build_request_header(msg_type=1, msg_type_specific_flags=4)
    # Event number for StartSession = 3
    event_bytes = struct.pack('>I', 3)
    
    # Total message: header + event + payload_size + payload
    payload_size = struct.pack('>I', len(payload_bytes))
    return header + event_bytes + payload_size + payload_bytes


def build_finish_session_request() -> bytes:
    """构建 FinishSession 请求"""
    # FinishSession event = 4
    header = build_request_header(msg_type=1, msg_type_specific_flags=4)
    event_bytes = struct.pack('>I', 4)
    return header + event_bytes


async def test_tts(text: str, output_file: str = "output.mp3"):
    """测试 TTS"""
    connect_id = str(uuid.uuid4())
    headers = {
        "X-Api-App-Key": APP_ID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": "seed-tts-2.0",
        "X-Api-Connect-Id": connect_id,
    }
    
    print(f"🔗 连接 WebSocket...")
    print(f"   URL: {WS_URL}")
    print(f"   Headers: {headers}")
    
    audio_data = bytearray()
    
    try:
        print("⏳ 正在建立连接...")
        ws = await websockets.connect(
            WS_URL,
            additional_headers=headers,
            ping_interval=None
        )
        print("✅ 连接成功")
            
            # 发送 StartSession
            print(f"📝 发送文本: {text}")
            await ws.send(build_start_session_request(text))
            
            # 接收音频数据
            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=30)
                    
                    if isinstance(message, bytes):
                        # 解析 header
                        if len(message) < 4:
                            continue
                        
                        byte1 = message[1]
                        msg_type = (byte1 >> 4) & 0xF
                        msg_flags = byte1 & 0xF
                        
                        # Audio-only response (msg_type=11)
                        if msg_type == 11:
                            # 跳过 header (4 bytes) + event (4 bytes) + payload_size (4 bytes)
                            if len(message) > 12:
                                audio_chunk = message[12:]
                                audio_data.extend(audio_chunk)
                                print(f"🎵 收到音频: {len(audio_chunk)} bytes")
                        
                        # Full-server response (msg_type=9)
                        elif msg_type == 9:
                            print(f"📨 收到服务端响应")
                        
                        # Error (msg_type=15)
                        elif msg_type == 15:
                            print(f"❌ 收到错误: {message}")
                            break
                
                except asyncio.TimeoutError:
                    print("⏱️ 超时，停止接收")
                    break
            
            # 发送 FinishSession
            print("📤 发送 FinishSession")
            await ws.send(build_finish_session_request())
    
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 保存音频
    if audio_data:
        with open(output_file, 'wb') as f:
            f.write(audio_data)
        print(f"✅ 音频已保存: {output_file} ({len(audio_data)} bytes)")
        return True
    else:
        print("❌ 没有收到音频数据")
        return False


if __name__ == "__main__":
    import sys
    
    text = sys.argv[1] if len(sys.argv) > 1 else "大家好，我是小何，很高兴认识你们"
    output = sys.argv[2] if len(sys.argv) > 2 else "output.mp3"
    
    print(f"🎙️ 豆包 TTS 测试")
    print(f"   音色: {VOICE_TYPE}")
    print(f"   文本: {text}")
    print()
    
    asyncio.run(test_tts(text, output))
