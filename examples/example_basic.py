#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例

演示如何使用 AI 讲课生成器
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import LectureGenerator


def example_1_text_input():
    """示例 1: 从文本生成"""
    print("\n" + "=" * 60)
    print("示例 1: 从文本生成讲课")
    print("=" * 60)
    
    generator = LectureGenerator()
    
    # 输入文本
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
    
    result = generator.generate(
        source=text,
        topic="人工智能基础",
        duration=5,
        style="通俗易懂"
    )
    
    if "error" not in result:
        print(f"✅ 生成成功!")
        print(f"  讲义：{result['lecture_path']}")
        print(f"  耗时：{result['elapsed_seconds']:.1f}秒")
        print(f"\n📝 摘要:\n{result['summary'][:300]}...")


def example_2_url_input():
    """示例 2: 从 URL 生成"""
    print("\n" + "=" * 60)
    print("示例 2: 从 URL 生成讲课")
    print("=" * 60)
    
    generator = LectureGenerator()
    
    # 使用 Wikipedia 文章
    url = "https://zh.wikipedia.org/wiki/人工智能"
    
    result = generator.generate(
        source=url,
        topic="AI 入门",
        duration=10
    )
    
    if "error" not in result:
        print(f"✅ 生成成功!")
        print(f"  讲义：{result['lecture_path']}")
    else:
        print(f"⚠️ URL 抓取可能失败：{result.get('error')}")


def example_3_pdf_input():
    """示例 3: 从 PDF 生成"""
    print("\n" + "=" * 60)
    print("示例 3: 从 PDF 生成讲课")
    print("=" * 60)
    
    generator = LectureGenerator()
    
    # PDF 路径
    pdf_path = "./workspace/input/sample.pdf"
    
    result = generator.generate(
        source=pdf_path,
        topic="论文讲解",
        duration=15
    )
    
    if "error" not in result:
        print(f"✅ 生成成功!")
    else:
        print(f"⚠️ PDF 读取可能失败：{result.get('error')}")


if __name__ == '__main__':
    print("\n🦞 AI 讲课生成器 - 使用示例\n")
    
    # 运行示例 1 (文本输入)
    example_1_text_input()
    
    # 运行示例 2 (URL 输入，可能需要网络)
    # example_2_url_input()
    
    # 运行示例 3 (PDF 输入，需要 PDF 文件)
    # example_3_pdf_input()
    
    print("\n✨ 所有示例完成!\n")
