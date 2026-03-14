#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL 输入测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fetcher import URLFetcher

def test_url_fetch():
    """测试 URL 抓取"""
    print("\n" + "=" * 60)
    print("📥 URL 抓取测试")
    print("=" * 60)
    
    fetcher = URLFetcher()
    
    # 测试 Wikipedia
    urls = [
        "https://zh.wikipedia.org/wiki/人工智能",
        "https://baike.baidu.com/item/人工智能",
    ]
    
    for url in urls:
        print(f"\n测试：{url}")
        content = fetcher.fetch(url)
        
        if content:
            print(f"  ✅ 抓取成功")
            print(f"  字符数：{len(content)}")
            print(f"  前 200 字：{content[:200]}...")
        else:
            print(f"  ❌ 抓取失败")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == '__main__':
    test_url_fetch()
