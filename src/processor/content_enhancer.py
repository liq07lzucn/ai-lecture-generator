#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容处理器 - 增强版

提供更多文本处理功能
"""

from typing import List, Dict
from loguru import logger


class TextEnhancer:
    """文本增强器"""
    
    def __init__(self, ollama_client=None):
        """初始化"""
        self.client = ollama_client
    
    def expand(self, content: str, target_words: int = 2000) -> str:
        """
        扩展内容
        
        Args:
            content: 原始内容
            target_words: 目标字数
        
        Returns:
            扩展后的内容
        """
        if not self.client:
            return content
        
        from src.ollama_client.prompts import PromptTemplates
        
        prompt = PromptTemplates.fill(
            "expand_content",
            content=content,
            target_word_count=target_words
        )
        
        return self.client.generate('qwen3:latest', prompt)
    
    def simplify(self, content: str, audience: str = "中学生", 
                 target_words: int = 500) -> str:
        """
        简化内容
        
        Args:
            content: 原始内容
            audience: 目标受众
            target_words: 目标字数
        
        Returns:
            简化后的内容
        """
        if not self.client:
            return content
        
        from src.ollama_client.prompts import PromptTemplates
        
        prompt = PromptTemplates.fill(
            "simplify_content",
            content=content,
            audience=audience,
            target_word_count=target_words
        )
        
        return self.client.generate('qwen3:latest', prompt)
    
    def change_style(self, content: str, target_style: str = "幽默风趣") -> str:
        """
        改变文风
        
        Args:
            content: 原始内容
            target_style: 目标风格
        
        Returns:
            改写后的内容
        """
        if not self.client:
            return content
        
        from src.ollama_client.prompts import PromptTemplates
        
        prompt = PromptTemplates.fill(
            "translate_style",
            content=content,
            target_style=target_style
        )
        
        return self.client.generate('qwen3:latest', prompt)


class ContentQualityChecker:
    """内容质量检查器"""
    
    def __init__(self, ollama_client=None):
        """初始化"""
        self.client = ollama_client
    
    def check(self, content: str) -> Dict:
        """
        检查内容质量
        
        Args:
            content: 内容
        
        Returns:
            检查结果 {score, issues, suggestions}
        """
        if not self.client:
            return {"score": 5, "issues": [], "suggestions": []}
        
        prompt = f"""请评估以下内容的质量，按以下 JSON 格式输出：

{{
    "score": 8,  // 1-10 分
    "issues": ["问题 1", "问题 2"],
    "suggestions": ["建议 1", "建议 2"],
    "word_count": 1000,
    "readability": "容易/中等/困难"
}}

内容：
{content[:3000]}
"""
        
        try:
            import json
            import re
            
            response = self.client.generate('deepseek-r1:1.5b', prompt)
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass
        
        return {"score": 5, "issues": [], "suggestions": []}
    
    def improve(self, content: str) -> str:
        """
        改进内容
        
        Args:
            content: 原始内容
        
        Returns:
            改进后的内容
        """
        check_result = self.check(content)
        
        if not check_result.get('issues'):
            return content
        
        suggestions = '\n'.join(check_result.get('suggestions', []))
        
        prompt = f"""请根据以下建议改进内容：

建议：
{suggestions}

原始内容：
{content[:3000]}

输出改进后的完整内容。"""
        
        return self.client.generate('qwen3:latest', prompt)


class ContentFormatter:
    """内容格式化器"""
    
    @staticmethod
    def to_markdown(content: str, title: str = "") -> str:
        """
        转换为 Markdown 格式
        
        Args:
            content: 内容
            title: 标题
        
        Returns:
            Markdown 格式文本
        """
        md = f"# {title}\n\n" if title else ""
        
        # 简单转换：段落之间加空行
        paragraphs = content.split('\n')
        for p in paragraphs:
            p = p.strip()
            if p:
                md += p + "\n\n"
        
        return md
    
    @staticmethod
    def to_html(content: str, title: str = "") -> str:
        """
        转换为 HTML 格式
        
        Args:
            content: 内容
            title: 标题
        
        Returns:
            HTML 格式文本
        """
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        p {{ line-height: 1.6; }}
    </style>
</head>
<body>
<h1>{title}</h1>
"""
        
        paragraphs = content.split('\n')
        for p in paragraphs:
            p = p.strip()
            if p:
                html += f"<p>{p}</p>\n"
        
        html += """
</body>
</html>
"""
        return html
    
    @staticmethod
    def to_plain(content: str) -> str:
        """
        转换为纯文本（移除格式）
        
        Args:
            content: 内容
        
        Returns:
            纯文本
        """
        import re
        # 移除 Markdown 格式
        text = re.sub(r'#+\s*', '', content)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        return text


if __name__ == '__main__':
    # 测试
    from src.ollama_client import OllamaClient
    
    client = OllamaClient()
    enhancer = TextEnhancer(client)
    
    test_content = "人工智能是计算机科学的一个分支。"
    
    # 测试扩展
    expanded = enhancer.expand(test_content, target_words=200)
    print(f"扩展后:\n{expanded}\n")
    
    # 测试简化
    simplified = enhancer.simplify(expanded, audience="小学生", target_words=100)
    print(f"简化后:\n{simplified}\n")
