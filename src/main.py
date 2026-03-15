#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 讲课生成器 - 主入口

功能:
1. 从 URL/PDF/文本获取内容
2. 提取知识点
3. 生成讲义和 PPT 大纲
4. 生成语音 (待实现)
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from loguru import logger
import yaml

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ollama_client import OllamaClient
from src.fetcher import URLFetcher, PDFReader
from src.processor import ContentParser, KnowledgeExtractor, LectureProcessor
from src.tts import EdgeTTSEngine, AudioMerger


class LectureGenerator:
    """AI 讲课生成器"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """初始化"""
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 初始化组件
        self.ollama = OllamaClient(
            host=self.config['ollama']['host'],
            timeout=self.config['ollama']['timeout']
        )
        self.url_fetcher = URLFetcher()
        self.pdf_reader = PDFReader()
        self.parser = ContentParser()
        self.extractor = KnowledgeExtractor(self.ollama)
        self.lecture_gen = LectureProcessor(self.ollama)
        self.tts = EdgeTTSEngine()
        self.audio_merger = AudioMerger()
        
        # 设置工作目录
        self._setup_workspace()
        
        # 配置日志
        self._setup_logging()
        
        logger.info("🦞 AI 讲课生成器初始化完成")
    
    def _load_config(self, config_path: str) -> dict:
        """加载配置"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {
            'ollama': {'host': 'http://192.168.0.214:11434', 'timeout': 120},
            'workspace': {'root': './workspace', 'output': './workspace/output'}
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
    
    def _setup_logging(self):
        """配置日志"""
        log_file = Path(self.config['workspace']['root']) / "logs" / "generator.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.remove()  # 移除默认处理器
        logger.add(sys.stderr, level="INFO")
        logger.add(log_file, level="DEBUG", rotation="10 MB")
    
    def generate(self, source: str, topic: str = None, duration: int = 10,
                 style: str = "大学讲课") -> dict:
        """
        生成完整讲课内容
        
        Args:
            source: 输入源 (URL/PDF 路径/文本)
            topic: 主题 (可选，会自动提取)
            duration: 时长 (分钟)
            style: 讲课风格
        
        Returns:
            生成结果 {lecture_path, ppt_path, summary}
        """
        start_time = datetime.now()
        logger.info(f"🎯 开始生成讲课：{topic or source}")
        
        # 1. 检查 Ollama 连接
        if not self.ollama.check_connection():
            logger.error("❌ Ollama 服务不可用")
            return {"error": "Ollama 服务不可用"}
        
        # 2. 获取内容
        logger.info("📥 获取内容...")
        content = self._fetch_content(source)
        if not content:
            logger.error("❌ 无法获取内容")
            return {"error": "无法获取内容"}
        
        # 3. 解析内容
        logger.info("📝 解析内容...")
        parsed = self.parser.parse(content)
        if not topic:
            topic = parsed['title'][:50]
        
        # 4. 提取知识点
        logger.info("💡 提取知识点...")
        key_points = self.extractor.extract(content, max_points=5)
        if not key_points:
            # 使用简单提取
            simple_points = self.extractor.extract_simple(content)
            key_points = [{"title": p, "summary": "", "level": "入门"} for p in simple_points]
        logger.info(f"提取 {len(key_points)} 个知识点")
        
        # 5. 生成讲义
        logger.info("📚 生成讲义...")
        lecture = self.lecture_gen.generate(topic, key_points, duration, style)
        lecture_path = self._save_output(lecture, f"{topic}_讲义.md")
        
        # 6. 生成 PPT 大纲
        logger.info("📊 生成 PPT 大纲...")
        ppt_outline = self.lecture_gen.generate_ppt_outline(lecture)
        ppt_path = self._save_json(ppt_outline, f"{topic}_PPT 大纲.json")
        
        # 7. 生成测试问题
        logger.info("❓ 生成测试问题...")
        questions = self.lecture_gen.generate_questions(lecture, count=3)
        questions_path = self._save_json(questions, f"{topic}_测试题.json")
        
        # 8. 生成摘要
        logger.info("📋 生成摘要...")
        summary = self._generate_summary(lecture)
        
        # 9. 生成语音
        logger.info("🔊 生成语音...")
        audio_path = self._generate_audio(lecture, topic)
        
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ 生成完成！耗时：{elapsed:.1f}秒")
        
        return {
            "lecture_path": str(lecture_path),
            "ppt_path": str(ppt_path),
            "questions_path": str(questions_path),
            "audio_path": str(audio_path) if audio_path else None,
            "summary": summary,
            "elapsed_seconds": elapsed,
        }
    
    def _fetch_content(self, source: str) -> str:
        """获取内容"""
        if source.startswith('http'):
            return self.url_fetcher.fetch(source) or ""
        elif source.endswith('.pdf'):
            return self.pdf_reader.read(source) or ""
        else:
            # 直接作为文本
            return source
    
    def _save_output(self, content: str, filename: str, session_id: str = None) -> Path:
        """保存输出文件"""
        output_dir = Path(self.config['workspace']['output'])
        
        # 如果有 session_id，创建子文件夹
        if session_id:
            session_dir = output_dir / f"session_{session_id}"
            session_dir.mkdir(parents=True, exist_ok=True)
            path = session_dir / filename
        else:
            path = output_dir / filename
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"保存到：{path}")
        return path
    
    def _save_json(self, data: dict, filename: str) -> Path:
        """保存 JSON 文件"""
        output_dir = Path(self.config['workspace']['output'])
        path = output_dir / filename
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"保存到：{path}")
        return path
    
    def _generate_summary(self, lecture: str) -> str:
        """生成摘要"""
        if not self.ollama:
            return lecture[:500]
        
        prompt = f"请用 200 字总结以下内容:\n\n{lecture[:3000]}"
        return self.ollama.generate('deepseek-r1:1.5b', prompt) or lecture[:500]
    
    def _generate_audio(self, lecture: str, topic: str) -> str:
        """
        生成语音
        
        Args:
            lecture: 讲义文本
            topic: 主题
        
        Returns:
            音频文件路径
        """
        try:
            output_dir = Path(self.config['workspace']['output'])
            audio_path = output_dir / f"{topic}_语音.mp3"
            
            # 使用默认音色
            voice = self.tts.get_voice_for_style("通俗易懂")
            
            # 合成完整讲课稿
            success = self.tts.synthesize(lecture, str(audio_path), voice=voice)
            
            if success:
                logger.info(f"✅ 语音生成成功：{audio_path}")
                return str(audio_path)
            else:
                logger.warning("⚠️ 语音生成失败")
                return None
                
        except Exception as e:
            logger.error(f"语音生成失败：{e}")
            return None


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI 讲课生成器')
    parser.add_argument('--source', '-s', required=True, help='输入源 (URL/PDF/文本)')
    parser.add_argument('--topic', '-t', help='主题 (可选)')
    parser.add_argument('--duration', '-d', type=int, default=10, help='时长 (分钟)')
    parser.add_argument('--style', default='大学讲课', help='讲课风格')
    parser.add_argument('--config', '-c', default='config.yaml', help='配置文件')
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = LectureGenerator(args.config)
    
    # 生成
    result = generator.generate(
        source=args.source,
        topic=args.topic,
        duration=args.duration,
        style=args.style
    )
    
    # 输出结果
    print("\n" + "=" * 60)
    if "error" in result:
        print(f"❌ 失败：{result['error']}")
    else:
        print("✅ 生成完成!")
        print(f"  讲义：{result['lecture_path']}")
        print(f"  PPT: {result['ppt_path']}")
        print(f"  测试题：{result['questions_path']}")
        print(f"  耗时：{result['elapsed_seconds']:.1f}秒")
        print(f"\n📝 摘要:\n{result['summary'][:300]}...")
    print("=" * 60)


if __name__ == '__main__':
    main()
