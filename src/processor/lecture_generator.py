#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
讲义生成处理器
"""

from typing import Dict, List
from loguru import logger


class LectureGenerator:
    """讲义生成器"""
    
    def __init__(self, ollama_client=None):
        """
        初始化
        
        Args:
            ollama_client: Ollama 客户端实例
        """
        self.client = ollama_client
    
    def generate(self, topic: str, key_points: List[Dict], 
                 duration: int = 10, style: str = "大学讲课") -> str:
        """
        生成讲义
        
        Args:
            topic: 主题
            key_points: 知识点列表
            duration: 时长 (分钟)
            style: 讲课风格
        
        Returns:
            讲义文本
        """
        logger.info(f"生成讲义：{topic}, {duration}分钟")
        
        if not self.client:
            logger.error("Ollama 客户端未初始化")
            return ""
        
        # 构建提示词
        points_text = '\n'.join([
            f"- {p.get('title', '知识点')}: {p.get('summary', '')}"
            for p in key_points
        ])
        
        prompt = f"""你是一位经验丰富的{style}讲师。请根据以下知识点生成一份讲课稿。

主题：{topic}
时长：{duration}分钟
目标受众：大学生

知识点:
{points_text}

要求:
1. 开场白 (吸引注意力，1-2 分钟)
2. 知识点讲解 (每个知识点 3-5 分钟，包含例子)
3. 互动环节 (提问或小测试，2 分钟)
4. 总结回顾 (1-2 分钟)

请生成完整的讲课稿，标注每个部分的时间分配。
使用通俗易懂的语言，避免过多专业术语。"""
        
        try:
            response = self.client.generate('qwen3:latest', prompt)
            logger.info(f"讲义生成成功，{len(response)}字符")
            return response
            
        except Exception as e:
            logger.error(f"生成失败：{e}")
            return ""
    
    def generate_ppt_outline(self, lecture: str) -> Dict:
        """
        生成 PPT 大纲
        
        Args:
            lecture: 讲义文本
        
        Returns:
            PPT 大纲 {title, slides: [{page, title, points, notes}]}
        """
        logger.info("生成 PPT 大纲")
        
        if not self.client:
            return {"title": "PPT", "slides": []}
        
        prompt = f"""根据以下讲课内容，生成 10-15 页 PPT 大纲。

讲课内容:
{lecture[:5000]}

请按以下 JSON 格式输出:
{{
    "title": "PPT 标题",
    "slides": [
        {{
            "page": 1,
            "title": "封面",
            "points": ["主标题", "副标题"],
            "notes": "开场白"
        }},
        ...
    ]
}}

只输出 JSON，不要其他内容。"""
        
        try:
            import json
            import re
            
            response = self.client.generate('qwen3:latest', prompt)
            
            # 解析 JSON
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                data = json.loads(match.group())
                return data
        except Exception as e:
            logger.error(f"生成 PPT 大纲失败：{e}")
        
        return {"title": topic, "slides": []}
    
    def generate_questions(self, content: str, count: int = 3) -> List[Dict]:
        """
        生成测试问题
        
        Args:
            content: 内容
            count: 问题数量
        
        Returns:
            问题列表 [{type, question, answer, explanation}]
        """
        logger.info(f"生成 {count} 个测试问题")
        
        if not self.client:
            return []
        
        prompt = f"""根据以下内容，生成{count}个测试问题 (含答案):

{content[:3000]}

格式:
1. 问题类型 (选择/填空/简答)
2. 问题内容
3. 正确答案
4. 解析

按 JSON 数组格式输出。"""
        
        try:
            import json
            import re
            
            response = self.client.generate('qwen3:latest', prompt)
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass
        
        return []


if __name__ == '__main__':
    # 测试
    from src.ollama_client import OllamaClient
    
    client = OllamaClient()
    generator = LectureGenerator(client)
    
    key_points = [
        {"title": "机器学习", "summary": "让计算机通过数据学习", "level": "入门"},
        {"title": "深度学习", "summary": "模拟人脑神经网络", "level": "进阶"},
    ]
    
    lecture = generator.generate("AI 基础", key_points, duration=5)
    print(f"讲义长度：{len(lecture)}")
    print(f"\n前 500 字:\n{lecture[:500]}...")
