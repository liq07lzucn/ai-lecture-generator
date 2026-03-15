#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge TTS 语音合成封装

免费、无需 API Key、支持中文
"""

import asyncio
import edge_tts
from pathlib import Path
from typing import List, Dict
from loguru import logger


class EdgeTTSEngine:
    """Edge TTS 语音合成引擎"""
    
    # 中文音色列表
    CHINESE_VOICES = {
        "zh-CN-YunxiNeural": "云希 (男，温暖)",
        "zh-CN-YunjianNeural": "云健 (男，体育解说)",
        "zh-CN-XiaoxiaoNeural": "晓晓 (女，温暖)",
        "zh-CN-XiaoyiNeural": "晓艺 (女，活泼)",
        "zh-CN-YunyangNeural": "云扬 (男，新闻播报)",
        "zh-CN-YunfengNeural": "云峰 (男，严肃)",
        "zh-CN-XiaohanNeural": "晓涵 (女，温柔)",
        "zh-CN-YunxiaNeural": "云夏 (男，激情)",
    }
    
    def __init__(self, default_voice: str = "zh-CN-YunxiNeural"):
        """
        初始化
        
        Args:
            default_voice: 默认音色
        """
        self.default_voice = default_voice
        logger.info(f"Edge TTS 初始化完成，默认音色：{default_voice}")
    
    async def synthesize_async(self, text: str, output_path: str, 
                                voice: str = None, rate: str = "+0%",
                                volume: str = "+0%") -> bool:
        """
        异步语音合成
        
        Args:
            text: 输入文本
            output_path: 输出文件路径
            voice: 音色
            rate: 语速 (+/- 百分比)
            volume: 音量 (+/- 百分比)
        
        Returns:
            是否成功
        """
        voice = voice or self.default_voice
        
        try:
            logger.info(f"开始合成语音：{len(text)}字符，音色：{voice}")
            
            communicate = edge_tts.Communicate(
                text, 
                voice,
                rate=rate,
                volume=volume
            )
            
            await communicate.save(output_path)
            
            logger.info(f"✅ 语音合成成功：{output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 语音合成失败：{e}")
            return False
    
    def synthesize(self, text: str, output_path: str, 
                   voice: str = None, rate: str = "+0%",
                   volume: str = "+0%") -> bool:
        """
        同步语音合成
        
        Args:
            text: 输入文本
            output_path: 输出文件路径
            voice: 音色
            rate: 语速
            volume: 音量
        
        Returns:
            是否成功
        """
        return asyncio.run(
            self.synthesize_async(text, output_path, voice, rate, volume)
        )
    
    def synthesize_lecture(self, lecture_text: str, output_dir: str,
                           voice: str = None) -> List[str]:
        """
        合成完整讲课稿（分段合成）
        
        Args:
            lecture_text: 讲课稿文本
            output_dir: 输出目录
            voice: 音色
        
        Returns:
            生成的音频文件路径列表
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 按段落分割
        paragraphs = [p.strip() for p in lecture_text.split('\n') if p.strip()]
        
        audio_files = []
        
        for i, para in enumerate(paragraphs):
            if len(para) < 10:  # 跳过太短的段落
                continue
            
            output_path = output_dir / f"audio_{i:03d}.mp3"
            
            logger.info(f"合成段落 {i+1}/{len(paragraphs)}")
            
            if self.synthesize(para, str(output_path), voice):
                audio_files.append(str(output_path))
        
        return audio_files
    
    def list_voices(self) -> Dict[str, str]:
        """获取可用音色列表"""
        return self.CHINESE_VOICES.copy()
    
    def get_voice_for_style(self, style: str) -> str:
        """
        根据讲课风格推荐音色
        
        Args:
            style: 风格描述
        
        Returns:
            推荐的音色 ID
        """
        style = style.lower()
        
        if "新闻" in style or "播报" in style:
            return "zh-CN-YunyangNeural"
        elif "体育" in style:
            return "zh-CN-YunjianNeural"
        elif "温柔" in style or "温暖" in style:
            return "zh-CN-XiaoxiaoNeural"
        elif "严肃" in style or "专业" in style:
            return "zh-CN-YunfengNeural"
        elif "活泼" in style or "儿童" in style:
            return "zh-CN-XiaoyiNeural"
        else:
            # 默认用男老师音色
            return "zh-CN-YunxiNeural"


class AudioMerger:
    """音频合并工具"""
    
    def __init__(self):
        """初始化"""
        try:
            from pydub import AudioSegment
            self.AudioSegment = AudioSegment
            self.available = True
        except ImportError:
            self.available = False
    
    def merge_files(self, audio_files: List[str], output_path: str) -> bool:
        """
        合并多个音频文件
        
        Args:
            audio_files: 音频文件路径列表
            output_path: 输出路径
        
        Returns:
            是否成功
        """
        if not self.available:
            return False
        
        if not audio_files:
            logger.error("音频文件列表为空")
            return False
        
        try:
            # 加载第一个文件
            combined = self.AudioSegment.from_mp3(audio_files[0])
            
            # 依次追加其他文件
            for file_path in audio_files[1:]:
                audio = self.AudioSegment.from_mp3(file_path)
                combined += audio
            
            # 导出
            combined.export(output_path, format="mp3")
            
            logger.info(f"✅ 音频合并成功：{output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 音频合并失败：{e}")
            return False
    
    def add_silence(self, audio_path: str, output_path: str, 
                    silence_ms: int = 500) -> bool:
        """
        在音频末尾添加静音
        
        Args:
            audio_path: 输入音频路径
            output_path: 输出路径
            silence_ms: 静音时长 (毫秒)
        
        Returns:
            是否成功
        """
        if not self.available:
            return False
        
        try:
            audio = self.AudioSegment.from_mp3(audio_path)
            silence = self.AudioSegment.silent(duration=silence_ms)
            combined = audio + silence
            combined.export(output_path, format="mp3")
            return True
        except Exception as e:
            logger.error(f"添加静音失败：{e}")
            return False


if __name__ == '__main__':
    # 测试
    tts = EdgeTTSEngine()
    
    print("可用音色:")
    for voice_id, desc in tts.list_voices().items():
        print(f"  {voice_id}: {desc}")
    
    # 测试合成
    test_text = "你好，这是一个测试。人工智能是计算机科学的一个重要分支。"
    
    output_path = "./workspace/output/test_tts.mp3"
    
    print(f"\n测试合成：{test_text}")
    success = tts.synthesize(test_text, output_path, voice="zh-CN-YunxiNeural")
    
    if success:
        print(f"✅ 合成成功：{output_path}")
    else:
        print("❌ 合成失败")
