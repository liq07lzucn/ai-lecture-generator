#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看历史记录 - 不浪费任何一次生成
"""

import json
from pathlib import Path
from datetime import datetime

output_dir = Path('./workspace/output')

print("\n" + "=" * 60)
print("📚 历史生成记录")
print("=" * 60 + "\n")

# 查找所有元数据文件
meta_files = sorted(output_dir.glob("meta_*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

if not meta_files:
    print("⚠️  还没有历史记录")
    print("请先生成课程：./start.sh\n")
else:
    print(f"找到 {len(meta_files)} 条历史记录:\n")
    
    for i, meta_file in enumerate(meta_files[:20], 1):  # 显示最近 20 条
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            mtime = datetime.fromtimestamp(meta_file.stat().st_mtime)
            date_str = mtime.strftime('%Y-%m-%d %H:%M')
            
            print(f"{i:2}. {data.get('topic', '未知主题')}")
            print(f"    📅 生成时间：{date_str}")
            print(f"    ⏱️  耗时：{data.get('elapsed_seconds', 0):.1f}秒")
            print(f"    📄 讲义：{meta_file.parent / (data.get('topic', '') + '_讲义.md')}")
            print(f"    🔊 语音：{data.get('audio_path', '未生成')}")
            print()
            
        except Exception as e:
            print(f"{i:2}. 读取失败：{e}\n")

print("=" * 60)
print("\n💡 提示:")
print("  - 文件都在：./workspace/output/")
print("  - 讲义是 .md 文件，可以用文本编辑器打开")
print("  - 语音是 .mp3 文件，可以用播放器播放")
print("  - PPT 大纲是 .json 文件，包含幻灯片结构")
print()
