#!/usr/bin/env python3
"""
小红书内容生成工具
作者：Steven
助手：Claude AI
"""

import os
import json
from typing import List, Dict

# TODO: 配置你的 Anthropic API Key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

def generate_topics(theme: str, count: int = 10) -> List[str]:
    """生成选题"""
    # TODO: 调用 Claude API
    # 暂时返回示例
    examples = [
        f"{theme}主题的5个治愈时刻",
        f"一个人过{theme}的小确幸",
        f"不是孤独，是自由：{theme}教会我的事",
        f"独居{theme}的3个美学小技巧",
        f"{theme}：单身女孩的自我浪漫",
    ]
    return examples[:count]

def generate_draft(topic: str, style: str = "治愈") -> str:
    """生成内容草稿"""
    # TODO: 调用 Claude API
    draft = f"""# {topic}

{style}系的开始...

## 第1个
...

## 第2个
...

## 第3个
...

{style}不是什么大道理，就是些小确幸。"""
    return draft

def optimize_titles(title: str) -> List[str]:
    """优化标题（情绪化）"""
    # TODO: 调用 Claude API
    return [
        f"{title}｜终于学会了爱自己",
        f"不敢相信{title}能做到这样...",
        f"{title}天花板级分享✨",
    ]

def generate_image_scenes(topic: str) -> List[str]:
    """生成图片拍摄方案"""
    # TODO: 调用 Claude API
    return [
        "暖光下的一本书+一杯热茶",
        "阳台上绿植+瑜伽垫",
    ]

def main():
    print("🌸 小红书内容生成工具")
    print("=" * 40)
    
    # 交互式菜单
    while True:
        print("\n选择功能：")
        print("1. 生成选题")
        print("2. 生成内容草稿")
        print("3. 优化标题")
        print("4. 生成图片方案")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == "1":
            theme = input("输入主题（如：独居、悦己、治愈）：")
            topics = generate_topics(theme)
            print("\n✨ 生成的选题：")
            for i, t in enumerate(topics, 1):
                print(f"{i}. {t}")
        
        elif choice == "2":
            topic = input("输入选题：")
            style = input("风格（默认：治愈）：") or "治愈"
            draft = generate_draft(topic, style)
            print(f"\n📝 内容草稿：\n{draft}")
        
        elif choice == "3":
            title = input("输入原标题：")
            titles = optimize_titles(title)
            print("\n✨ 优化后的标题：")
            for i, t in enumerate(titles, 1):
                print(f"{i}. {t}")
        
        elif choice == "4":
            topic = input("输入选题：")
            scenes = generate_image_scenes(topic)
            print("\n📸 图片拍摄方案：")
            for i, s in enumerate(scenes, 1):
                print(f"{i}. {s}")
        
        elif choice == "5":
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选项，请重新选择")

if __name__ == "__main__":
    main()
