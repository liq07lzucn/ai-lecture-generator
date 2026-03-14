#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容解析器
"""

from typing import Dict, List
from loguru import logger


class ContentParser:
    """内容解析器"""
    
    def __init__(self):
        """初始化"""
        pass
    
    def parse(self, content: str) -> Dict:
        """
        解析内容，提取结构化信息
        
        Args:
            content: 原始内容
        
        Returns:
            结构化信息 {title, sections, word_count}
        """
        logger.info(f"解析内容，{len(content)}字符")
        
        # 提取标题 (第一行或包含标题标签的行)
        lines = content.split('\n')
        title = ""
        sections = []
        current_section = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 如果没有标题，第一行作为标题
            if not title:
                title = line
                continue
            
            # 检测章节标题 (包含# 或数字 + 点)
            if line.startswith('#') or (len(line) < 100 and line[0].isdigit() and '.' in line[:5]):
                if current_section:
                    sections.append('\n'.join(current_section))
                current_section = [line]
            else:
                current_section.append(line)
        
        # 添加最后一个章节
        if current_section:
            sections.append('\n'.join(current_section))
        
        result = {
            'title': title,
            'sections': sections,
            'word_count': len(content),
            'paragraph_count': len([l for l in lines if l.strip()]),
        }
        
        logger.info(f"解析完成：{len(sections)}个章节")
        return result
    
    def clean(self, content: str) -> str:
        """
        清理内容 (移除多余空白、特殊字符等)
        
        Args:
            content: 原始内容
        
        Returns:
            清理后的内容
        """
        # 移除多余空白
        lines = []
        for line in content.split('\n'):
            cleaned = ' '.join(line.split())
            if cleaned:
                lines.append(cleaned)
        
        return '\n'.join(lines)
    
    def split_chunks(self, content: str, chunk_size: int = 2000) -> List[str]:
        """
        将内容分块 (用于处理长文本)
        
        Args:
            content: 原始内容
            chunk_size: 每块大小 (字符)
        
        Returns:
            文本块列表
        """
        chunks = []
        current_chunk = ""
        
        for line in content.split('\n'):
            if len(current_chunk) + len(line) < chunk_size:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        logger.info(f"分块完成：{len(chunks)}块")
        return chunks


if __name__ == '__main__':
    # 测试
    parser = ContentParser()
    
    test_content = """# 人工智能简介

人工智能是计算机科学的一个分支。

## 发展历程

1956 年，达特茅斯会议提出了人工智能的概念。

## 应用领域

1. 机器学习
2. 自然语言处理
3. 计算机视觉
"""
    
    result = parser.parse(test_content)
    print(f"标题：{result['title']}")
    print(f"章节数：{len(result['sections'])}")
    print(f"字数：{result['word_count']}")
