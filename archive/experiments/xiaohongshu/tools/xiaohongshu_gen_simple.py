#!/usr/bin/env python3
"""
小红书内容生成工具（简化版 - 使用 requests）
作者：Steven & Claude
"""

import os
import json
import sys
from typing import List, Optional

try:
    import requests
except ImportError:
    print("❌ 请安装 requests: pip3 install --break-system-packages --user requests")
    sys.exit(1)


class XiaohongshuGenerator:
    """小红书内容生成器"""

    def __init__(self, api_key: Optional[str] = None):
        """初始化"""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 请设置 ANTHROPIC_API_KEY 环境变量")
        
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-7-sonnet"
        self.headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }

    def call_claude(self, prompt: str, max_tokens: int = 1000) -> str:
        """调用 Claude API"""
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["content"][0]["text"]
        except requests.exceptions.RequestException as e:
            return f"❌ API 调用失败: {e}"
        except Exception as e:
            return f"❌ 未知错误: {e}"

    def generate_topics(self, theme: str, count: int = 10) -> List[str]:
        """生成选题"""
        prompt = f"""生成 {count} 个小红书爆款选题。

主题：{theme}

要求：
1. 要有情绪价值（共鸣、治愈、自我认同）
2. 标题要吸引人（但不要太标题党）
3. 内容要有实际价值
4. 适合单身女性/精致独居人群

格式：每行一个选题
"""
        result = self.call_claude(prompt, max_tokens=1500)
        topics = [line.strip() for line in result.strip().split('\n') if line.strip()]
        return topics[:count]

    def generate_draft(self, topic: str, style: str = "治愈") -> str:
        """生成内容草稿"""
        prompt = f"""写一篇小红书内容。

主题：{topic}
风格：{style}

要求：
1. 开头要有场景或故事，让人代入
2. 中间要有实际内容（干货、分享）
3. 结尾要有情绪升华
4. 文字要有节奏，不要太密
5. 可以适当用 emoji，但不要太多
6. 1000-1500 字
"""
        return self.call_claude(prompt, max_tokens=2000)

    def optimize_titles(self, title: str, count: int = 5) -> List[str]:
        """优化标题（情绪化）"""
        prompt = f"""原标题：{title}

优化成 {count} 个小红书爆款标题。

要求：
1. 有情绪价值（共鸣、治愈、独立）
2. 吸引人但不标题党
3. 符合小红书风格
4. 可以适当用 emoji

格式：每行一个标题
"""
        result = self.call_claude(prompt, max_tokens=500)
        titles = [line.strip() for line in result.strip().split('\n') if line.strip()]
        return titles[:count]

    def generate_image_scenes(self, topic: str, count: int = 5) -> List[str]:
        """生成图片拍摄方案"""
        prompt = f"""主题：{topic}

生成 {count} 个小红书图片拍摄方案。

要求：
1. 描述场景（光线、背景、道具）
2. 要有审美和氛围感
3. 符合精致独居/单身生活风格
4. 实际可拍摄

格式：每行一个方案
"""
        result = self.call_claude(prompt, max_tokens=800)
        scenes = [line.strip() for line in result.strip().split('\n') if line.strip()]
        return scenes[:count]


def main():
    """主函数"""
    print("🌸 小红书内容生成工具")
    print("=" * 50)

    try:
        generator = XiaohongshuGenerator()
        print("✅ Claude API 连接成功")
    except ValueError as e:
        print(e)
        print("\n💡 如何设置 API Key：")
        print("export ANTHROPIC_API_KEY='your-key-here'")
        return
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return

    # 交互式菜单
    while True:
        print("\n" + "=" * 50)
        print("选择功能：")
        print("1. 生成选题")
        print("2. 生成内容草稿")
        print("3. 优化标题")
        print("4. 生成图片方案")
        print("5. 一键生成（选题+草稿+图片）")
        print("6. 退出")
        
        choice = input("\n请输入选项 (1-6): ").strip()

        if choice == "1":
            theme = input("📝 输入主题（如：独居、悦己、治愈、单身美学）：")
            topics = generator.generate_topics(theme)
            print("\n✨ 生成的选题：")
            for i, t in enumerate(topics, 1):
                print(f"{i}. {t}")

        elif choice == "2":
            topic = input("📝 输入选题：")
            style = input("🎨 风格（默认：治愈）：") or "治愈"
            draft = generator.generate_draft(topic, style)
            print(f"\n📄 内容草稿：\n{draft}")

        elif choice == "3":
            title = input("📝 输入原标题：")
            titles = generator.optimize_titles(title)
            print("\n✨ 优化后的标题：")
            for i, t in enumerate(titles, 1):
                print(f"{i}. {t}")

        elif choice == "4":
            topic = input("📝 输入选题：")
            scenes = generator.generate_image_scenes(topic)
            print("\n📸 图片拍摄方案：")
            for i, s in enumerate(scenes, 1):
                print(f"{i}. {s}")

        elif choice == "5":
            theme = input("📝 输入主题：")
            print(f"\n🔄 正在为 '{theme}' 生成全套内容...\n")
            
            # 选题
            topics = generator.generate_topics(theme, count=3)
            print("✨ 生成的选题：")
            for i, t in enumerate(topics, 1):
                print(f"{i}. {t}")
            
            # 选第一个
            selected_topic = topics[0]
            print(f"\n🎯 选中：{selected_topic}")
            
            # 草稿
            draft = generator.generate_draft(selected_topic)
            print(f"\n📄 内容草稿：\n{draft}")
            
            # 标题优化
            titles = generator.optimize_titles(selected_topic, count=3)
            print("\n✨ 优化后的标题：")
            for i, t in enumerate(titles, 1):
                print(f"{i}. {t}")
            
            # 图片方案
            scenes = generator.generate_image_scenes(selected_topic, count=3)
            print("\n📸 图片拍摄方案：")
            for i, s in enumerate(scenes, 1):
                print(f"{i}. {s}")

        elif choice == "6":
            print("👋 再见，期待下次创作！")
            break

        else:
            print("❌ 无效选项，请重新选择")


if __name__ == "__main__":
    main()
