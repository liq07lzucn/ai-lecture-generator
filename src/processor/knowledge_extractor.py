#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识点提取器
"""

from typing import List, Dict
from loguru import logger


class KnowledgeExtractor:
    """知识点提取器"""
    
    def __init__(self, ollama_client=None):
        """
        初始化
        
        Args:
            ollama_client: Ollama 客户端实例
        """
        self.client = ollama_client
    
    def extract(self, content: str, max_points: int = 5) -> List[Dict]:
        """
        提取知识点
        
        Args:
            content: 输入内容
            max_points: 最大知识点数量
        
        Returns:
            知识点列表 [{title, summary, level}]
        """
        logger.info(f"提取知识点，内容长度：{len(content)}")
        
        if not self.client:
            logger.error("Ollama 客户端未初始化")
            return []
        
        # 构建提示词
        prompt = f"""你是一位专业的教育内容分析师。请分析以下文本，提取{max_points}个关键知识点。

文本内容:
{content[:8000]}  # 限制长度

请按以下 JSON 格式输出:
{{
    "topic": "核心主题",
    "key_points": [
        {{"title": "知识点 1", "summary": "一句话概括", "level": "入门"}},
        {{"title": "知识点 2", "summary": "一句话概括", "level": "进阶"}}
    ]
}}

只输出 JSON，不要其他内容。"""
        
        try:
            response = self.client.generate('qwen3:latest', prompt)
            
            # 解析 JSON (简化处理，实际应该用 json.loads)
            points = self._parse_json_response(response)
            
            logger.info(f"提取成功：{len(points)}个知识点")
            return points
            
        except Exception as e:
            logger.error(f"提取失败：{e}")
            return []
    
    def _parse_json_response(self, response: str) -> List[Dict]:
        """解析 JSON 响应"""
        import json
        import re
        
        try:
            # 提取 JSON 部分
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                json_str = match.group()
                data = json.loads(json_str)
                return data.get('key_points', [])
        except:
            pass
        
        # 解析失败时返回空列表
        return []
    
    def extract_simple(self, content: str) -> List[str]:
        """
        简单提取 (不使用 AI，基于规则)
        
        Args:
            content: 输入内容
        
        Returns:
            知识点标题列表
        """
        points = []
        
        # 提取标题行
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('#') or (len(line) < 100 and line[0].isdigit() and '.' in line[:5]):
                points.append(line.lstrip('#').strip())
        
        return points if points else ["核心内容"]


if __name__ == '__main__':
    # 测试
    from src.ollama_client import OllamaClient
    
    client = OllamaClient()
    extractor = KnowledgeExtractor(client)
    
    test_content = """
    人工智能是计算机科学的一个分支，它试图理解智能的实质。
    机器学习是 AI 的核心，让计算机通过数据学习规律。
    深度学习模拟人脑的神经网络，处理复杂任务。
    自然语言处理让机器理解人类语言。
    """
    
    points = extractor.extract(test_content, max_points=3)
    print(f"提取 {len(points)} 个知识点:")
    for p in points:
        print(f"  - {p.get('title', 'N/A')}: {p.get('summary', 'N/A')[:50]}")
