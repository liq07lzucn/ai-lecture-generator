#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整流程测试 - 包含语音合成
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import LectureGenerator

def test_full_flow():
    """测试完整流程（含语音）"""
    print("\n" + "=" * 60)
    print("🎯 完整流程测试 - 含语音合成")
    print("=" * 60)
    
    generator = LectureGenerator()
    
    text = """
    人工智能是计算机科学的一个重要分支，它试图理解智能的实质，
    并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    
    人工智能的发展经历了三个阶段：
    1. 符号主义阶段 (1950s-1980s) - 基于逻辑推理
    2. 连接主义阶段 (1980s-2010s) - 基于神经网络
    3. 深度学习阶段 (2010s 至今) - 基于大数据和 GPU
    
    主要应用领域包括：
    - 机器学习：让计算机通过数据学习规律
    - 自然语言处理：让机器理解人类语言
    - 计算机视觉：让机器"看懂"图像
    - 机器人技术：智能控制和自主导航
    """
    
    print("\n📝 生成内容...")
    result = generator.generate(
        source=text,
        topic="AI 基础入门",
        duration=5,
        style="通俗易懂"
    )
    
    print("\n" + "=" * 60)
    if "error" in result:
        print(f"❌ 失败：{result['error']}")
    else:
        print("✅ 生成完成!")
        print(f"  📄 讲义：{result['lecture_path']}")
        print(f"  📊 PPT: {result['ppt_path']}")
        print(f"  ❓ 测试题：{result['questions_path']}")
        print(f"  🔊 语音：{result['audio_path']}")
        print(f"  ⏱️  耗时：{result['elapsed_seconds']:.1f}秒")
        print(f"\n📝 摘要:\n{result['summary'][:300]}...")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    test_full_flow()
