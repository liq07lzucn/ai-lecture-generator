#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为已生成的课程创建历史记录
"""

import json
from pathlib import Path
from datetime import datetime
import os

output_dir = Path('./workspace/output')

print("\n" + "=" * 60)
print("🔧 为已生成的课程创建历史记录")
print("=" * 60 + "\n")

# 查找所有讲义文件
lecture_files = list(output_dir.glob("*讲义.md"))

if not lecture_files:
    print("⚠️  没有找到已生成的讲义文件")
else:
    print(f"找到 {len(lecture_files)} 个讲义文件:\n")
    
    created_count = 0
    for lecture_file in lecture_files:
        try:
            # 提取课程名
            course_name = lecture_file.stem.replace('_讲义', '')
            
            # 查找相关文件
            ppt_file = lecture_file.with_name(f"{course_name}_PPT 大纲.json")
            questions_file = lecture_file.with_name(f"{course_name}_测试题.json")
            audio_file = lecture_file.with_name(f"{course_name}_语音.mp3")
            
            # 获取文件时间
            mtime = datetime.fromtimestamp(lecture_file.stat().st_mtime)
            session_id = mtime.strftime('%Y%m%d%H%M%S')
            
            # 计算耗时（估算）
            estimated_time = 240.0  # 默认 4 分钟
            
            # 创建元数据
            meta = {
                'session_id': session_id,
                'topic': course_name,
                'timestamp': mtime.isoformat(),
                'elapsed_seconds': estimated_time,
                'duration': 10,  # 默认 10 分钟
                'lecture_path': str(lecture_file.absolute()),
                'ppt_path': str(ppt_file.absolute()) if ppt_file.exists() else None,
                'questions_path': str(questions_file.absolute()) if questions_file.exists() else None,
                'audio_path': str(audio_file.absolute()) if audio_file.exists() else None,
                'word_count': lecture_file.stat().st_size,
                'restored': True  # 标记为恢复的历史记录
            }
            
            # 保存元数据
            meta_file = output_dir / f"meta_{session_id}.json"
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {course_name}")
            print(f"   讲义：{lecture_file.name}")
            print(f"   PPT: {'✅' if ppt_file.exists() else '❌'}")
            print(f"   测试题：{'✅' if questions_file.exists() else '❌'}")
            print(f"   语音：{'✅' if audio_file.exists() else '❌'}")
            print(f"   时间：{mtime.strftime('%Y-%m-%d %H:%M')}")
            print()
            
            created_count += 1
            
        except Exception as e:
            print(f"❌ 处理失败 {lecture_file.name}: {e}\n")
    
    print("=" * 60)
    print(f"\n✅ 已为 {created_count} 个课程创建历史记录")
    print("\n💡 现在可以:")
    print("  1. 启动 Web 服务：./start.sh")
    print("  2. 点击'查看历史记录'查看")
    print("  3. 或运行：python3 view_history.py")
    print()
