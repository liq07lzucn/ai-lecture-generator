#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fish Speech 语音合成封装

安装:
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech
pip install -e .

或使用 Docker:
docker run --gpus all -p 8080:8000 fishaudio/fish-speech:latest
"""

import os
import requests
from pathlib import Path
from typing import Optional
from loguru import logger


class FishSpeechTTS:
    """Fish Speech 语音合成"""
    
    def __init__(self, model_path: str = None, device: str = "cuda"):
        """
        初始化
        
        Args:
            model_path: 模型路径 (None 则使用默认)
            device: 运行设备 (cuda/cpu)
        """
        self.model_path = model_path
        self.device = device
        self.api_url = None  # 如果使用 API 模式
        
        # 检查是否安装了 fish-speech
        try:
            import fish_speech
            logger.info("✅ Fish Speech 已安装")
            self.use_api = False
        except ImportError:
            logger.warning("⚠️ Fish Speech 未安装，尝试使用 API 模式")
            self.use_api = True
            self.api_url = "http://localhost:8080/v1/tts"
    
    def synthesize(self, text: str, output_path: str, 
                   speaker: str = "中文男老师",
                   speed: float = 1.0) -> bool:
        """
        语音合成
        
        Args:
            text: 输入文本
            output_path: 输出音频路径
            speaker: 说话人
            speed: 语速
        
        Returns:
            是否成功
        """
        try:
            if self.use_api:
                return self._synthesize_api(text, output_path, speaker, speed)
            else:
                return self._synthesize_local(text, output_path, speaker, speed)
        except Exception as e:
            logger.error(f"语音合成失败：{e}")
            return False
    
    def _synthesize_local(self, text: str, output_path: str, 
                         speaker: str, speed: float) -> bool:
        """本地合成 (需要安装 fish-speech)"""
        # TODO: 实现本地推理
        logger.warning("本地推理待实现")
        return False
    
    def _synthesize_api(self, text: str, output_path: str,
                       speaker: str, speed: float) -> bool:
        """API 模式合成"""
        if not self.api_url:
            return False
        
        payload = {
            "text": text,
            "speaker": speaker,
            "speed": speed,
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"✅ 语音合成成功：{output_path}")
            return True
            
        except Exception as e:
            logger.error(f"API 请求失败：{e}")
            return False
    
    def list_speakers(self) -> list:
        """获取可用音色列表"""
        # TODO: 实现
        return [
            {"id": "teacher_male", "name": "中文男老师"},
            {"id": "teacher_female", "name": "中文女老师"},
            {"id": "narrator", "name": "解说员"},
        ]


if __name__ == '__main__':
    # 测试
    tts = FishSpeechTTS()
    
    print("可用音色:")
    for s in tts.list_speakers():
        print(f"  - {s['id']}: {s['name']}")
    
    # 测试合成
    success = tts.synthesize(
        text="你好，这是一个测试。",
        output_path="./workspace/output/test.wav",
        speaker="中文男老师"
    )
    
    print(f"\n合成结果：{'✅ 成功' if success else '❌ 失败'}")
