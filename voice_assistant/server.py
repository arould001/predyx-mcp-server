#!/usr/bin/env python3
"""语音助手后端服务"""

import os
import uuid
import json
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='static')
CORS(app)

# ====== 配置 ======
# 豆包 TTS
APP_ID = "4015061462"
ACCESS_TOKEN = "P19U38Hqnh6_1nUmV2A0aUpXmi6l4wvq"
VOICE_TYPE = "zh_female_xiaohe_uranus_bigtts"
TTS_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"

# GLM API
GLM_API_KEY = "db17748753a240789101425160adfbbf.Ug0nnq7qn32aJ4Y9"
GLM_API_URL = "https://open.bigmodel.cn/api/coding/paas/v4/chat/completions"

# 代理配置（如果需要）
PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

# 创建静态文件目录
os.makedirs('static', exist_ok=True)


def get_ai_reply(user_text: str) -> str:
    """获取 AI 回复（GLM-5）"""
    try:
        print(f"[GLM] 发送请求: {user_text}")
        response = requests.post(
            GLM_API_URL,
            headers={
                "Authorization": f"Bearer {GLM_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "glm-4.7-flash",  # 使用flash版本，更快更简洁
                "messages": [
                    {
                        "role": "system",
                        "content": "你是小何，一个友好、温柔的语音助手。请直接回答问题，不要展示思考过程。回答要简洁自然，适合语音交互，不要用markdown格式。"
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 800  # 增加以避免截断
            },
            proxies=PROXIES,
            timeout=40
        )
        
        print(f"[GLM] 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]
            
            # 优先使用content，如果为空则使用reasoning_content
            reply = message.get("content") or message.get("reasoning_content", "")
            
            # 清理markdown格式
            reply = reply.replace("**", "").replace("##", "").replace("###", "")
            reply = reply.replace("\n\n", "。").replace("\n", " ")
            
            print(f"[GLM] 回复长度: {len(reply)}")
            return reply
        else:
            print(f"[GLM] API 错误: {response.status_code} - {response.text}")
            return "抱歉，我暂时无法回答，请稍后再试。"
    
    except requests.exceptions.Timeout:
        print("[GLM] 请求超时")
        return "网络有点慢，等下再试试？"
    except Exception as e:
        print(f"[GLM] 调用异常: {type(e).__name__}: {e}")
        return "网络好像有点问题，等下再试试？"


def text_to_speech(text: str) -> str:
    """TTS 合成，返回音频文件 URL"""
    print(f"[TTS] 开始合成，文本长度: {len(text)}")
    print(f"[TTS] 文本内容: {text[:100]}...")
    
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
    
    try:
        response = requests.post(TTS_URL, headers=headers, json=payload, stream=True, timeout=30)
        print(f"[TTS] 响应状态: {response.status_code}")
        
        # 解析音频
        audio_data = bytearray()
        chunk_count = 0
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    chunk_count += 1
                    if chunk.get("code") == 0 and chunk.get("data"):
                        audio_data.extend(base64.b64decode(chunk["data"]))
                    else:
                        print(f"[TTS] Chunk错误: {chunk}")
                except Exception as e:
                    print(f"[TTS] 解析chunk失败: {e}")
                    continue
        
        print(f"[TTS] 收到 {chunk_count} 个chunks，音频大小: {len(audio_data)} bytes")
        
        if not audio_data:
            print("[TTS] 没有收到音频数据")
            return None
        
        # 保存音频文件
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join('static', filename)
        
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        
        return f"/static/{filename}"
    
    except Exception as e:
        print(f"TTS 错误: {e}")
        return None


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data.get('text', '')
    
    if not user_text:
        return jsonify({'error': '请输入文本'}), 400
    
    # 1. 获取 AI 回复
    reply = get_ai_reply(user_text)
    
    # 2. TTS 合成
    audio_url = text_to_speech(reply)
    
    if audio_url:
        return jsonify({
            'reply': reply,
            'audio_url': audio_url
        })
    else:
        return jsonify({'error': '语音合成失败'}), 500


@app.route('/static/<filename>')
def serve_audio(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    print("🎙️ 语音助手服务启动中...")
    print("   打开浏览器访问: http://localhost:5001")
    print("   局域网访问: http://192.168.1.189:5001")
    print()
    app.run(host='0.0.0.0', port=5001, debug=False)  # 关闭debug模式
