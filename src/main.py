#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 讲课生成器 - 主入口
"""

import sys
import os
from pathlib import Path
from loguru import logger
import yaml

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.ollama_client import OllamaClient, PromptTemplates


class LectureGenerator:
    """讲课生成器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """初始化"""
        self.config = self._load_config(config_path)
        self.client = OllamaClient(
            host=self.config['ollama']['host'],
            timeout=self.config['ollama']['timeout']
        )
        self.prompts = PromptTemplates()
        
        # 创建工作目录
        self._setup_workspace()
        
        logger.info("🦞 AI 讲课生成器初始化完成")
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {
            'ollama': {'host': 'http://192.168.0.214:11434', 'timeout': 120},
            'workspace': {'root': './workspace'}
        }
    
    def _setup_workspace(self):
        """设置工作目录"""
        ws = self.config.get('workspace', {})
        dirs = [
            ws.get('root', './workspace'),
            ws.get('input', './workspace/input'),
            ws.get('output', './workspace/output'),
            ws.get('cache', './workspace/cache'),
            ws.get('temp', './workspace/temp'),
        ]
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
    
    def generate(self, source: str, topic: str = None, duration: int = 10, 
                 voice: str = "teacher_male") -> Dict:
        """
        生成讲课内容
        
        Args:
            source: 输入源 (URL/PDF 路径/文本)
            topic: 主题
            duration: 时长 (分钟)
            voice: 音色
        
        Returns:
            生成结果 {lecture_path, audio_path, ppt_path}
        """
        logger.info(f"开始生成讲课：{topic or source}")
        
        # 1. 检查连接
        if not self.client.check_connection():
            logger.error("Ollama 服务不可用")
            return {}
        
        # 2. 获取内容
        content = self._fetch_content(source)
        if not content:
            logger.error("无法获取内容")
            return {}
        
        # 3. 提取知识点
        key_points = self._extract_knowledge(content)
        logger.info(f"提取 {len(key_points)} 个知识点")
        
        # 4. 生成讲义
        lecture = self._generate_lecture(key_points, duration)
        lecture_path = self._save_lecture(lecture, topic)
        
        # 5. 生成 PPT 大纲
        ppt_outline = self._generate_ppt_outline(lecture)
        ppt_path = self._save_ppt_outline(ppt_outline)
        
        # 6. 生成语音 (待实现)
        # audio_path = self._generate_audio(lecture, voice)
        
        logger.info("✅ 生成完成")
        
        return {
            "lecture_path": str(lecture_path),
            "ppt_path": str(ppt_path),
            "audio_path": None,  # 待实现
        }
    
    def _fetch_content(self, source: str) -> str:
        """获取内容"""
        if source.startswith('http'):
            # TODO: 实现网页抓取
            return "网页内容待实现..."
        elif source.endswith('.pdf'):
            # TODO: 实现 PDF 读取
            return "PDF 内容待实现..."
        else:
            # 直接作为文本
            return source
    
    def _extract_knowledge(self, content: str) -> List[Dict]:
        """提取知识点"""
        prompt = self.prompts.fill("content_extract", text=content[:10000])
        response = self.client.chat(
            model="qwen3:8b",
            messages=[{"role": "user", "content": prompt}]
        )
        # TODO: 解析 JSON
        return [{"title": "知识点", "summary": response[:200], "level": "入门"}]
    
    def _generate_lecture(self, key_points: List[Dict], duration: int) -> str:
        """生成讲义"""
        prompt = self.prompts.fill(
            "lecture_generate",
            key_points=str(key_points),
            duration=duration,
            style="大学讲课",
            audience="大学生"
        )
        return self.client.chat(
            model="qwen3:8b",
            messages=[{"role": "user", "content": prompt}]
        )
    
    def _generate_ppt_outline(self, lecture: str) -> Dict:
        """生成 PPT 大纲"""
        prompt = self.prompts.fill("ppt_outline", lecture_content=lecture[:5000])
        response = self.client.chat(
            model="qwen3:8b",
            messages=[{"role": "user", "content": prompt}]
        )
        # TODO: 解析 JSON
        return {"title": "PPT", "slides": []}
    
    def _save_lecture(self, content: str, topic: str) -> Path:
        """保存讲义"""
        topic = topic or "lecture"
        path = Path(self.config['workspace']['output']) / f"{topic}_lecture.md"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path
    
    def _save_ppt_outline(self, outline: Dict) -> Path:
        """保存 PPT 大纲"""
        path = Path(self.config['workspace']['output']) / "ppt_outline.json"
        with open(path, 'w', encoding='utf-8') as f:
            import json
            json.dump(outline, f, ensure_ascii=False, indent=2)
        return path


if __name__ == '__main__':
    # 测试
    generator = LectureGenerator()
    
    # 简单测试
    result = generator.generate(
        source="人工智能是计算机科学的一个分支，它试图理解智能的实质...",
        topic="AI 基础入门",
        duration=5
    )
    
    print(f"\n生成结果:")
    print(f"  讲义：{result.get('lecture_path')}")
    print(f"  PPT: {result.get('ppt_path')}")
