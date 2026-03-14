#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页内容抓取
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
from loguru import logger


class URLFetcher:
    """网页内容抓取器"""
    
    def __init__(self, timeout: int = 30):
        """
        初始化
        
        Args:
            timeout: 请求超时时间 (秒)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        })
    
    def fetch(self, url: str) -> Optional[str]:
        """
        抓取网页内容
        
        Args:
            url: 网页 URL
        
        Returns:
            提取的文本内容
        """
        try:
            logger.info(f"抓取网页：{url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # 解析 HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 移除不需要的标签
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            # 提取正文内容
            # 优先提取 article 标签
            article = soup.find('article')
            if article:
                text = self._extract_text(article)
            else:
                # 提取所有段落
                paragraphs = soup.find_all('p')
                text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
            
            # 清理空白
            text = ' '.join(text.split())
            
            logger.info(f"抓取成功，{len(text)}字符")
            return text
            
        except Exception as e:
            logger.error(f"抓取失败：{e}")
            return None
    
    def _extract_text(self, element) -> str:
        """提取元素中的文本"""
        texts = []
        for child in element.children:
            if child.name:
                texts.append(self._extract_text(child))
            elif isinstance(child, str):
                texts.append(child.strip())
        return ' '.join(texts)
    
    def fetch_title(self, url: str) -> Optional[str]:
        """获取网页标题"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.title.string if soup.title else ''
            return title.strip() if title else None
        except Exception as e:
            logger.error(f"获取标题失败：{e}")
            return None


if __name__ == '__main__':
    # 测试
    fetcher = URLFetcher()
    
    # 测试 Wikipedia
    url = "https://zh.wikipedia.org/wiki/人工智能"
    content = fetcher.fetch(url)
    
    if content:
        print(f"标题：{fetcher.fetch_title(url)}")
        print(f"内容长度：{len(content)}")
        print(f"\n前 500 字:\n{content[:500]}...")
