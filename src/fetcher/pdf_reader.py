#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 文件读取
"""

from pathlib import Path
from typing import Optional, Union
from loguru import logger


class PDFReader:
    """PDF 文件读取器"""
    
    def __init__(self):
        """初始化"""
        try:
            import fitz  # PyMuPDF
            self.fitz = fitz
            logger.info("✅ PyMuPDF 已加载")
        except ImportError:
            logger.error("❌ PyMuPDF 未安装，请运行：pip install PyMuPDF")
            self.fitz = None
    
    def read(self, pdf_path: Union[str, Path]) -> Optional[str]:
        """
        读取 PDF 文件
        
        Args:
            pdf_path: PDF 文件路径
        
        Returns:
            提取的文本内容
        """
        if not self.fitz:
            return None
        
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                logger.error(f"文件不存在：{pdf_path}")
                return None
            
            logger.info(f"读取 PDF: {pdf_path}")
            
            # 打开 PDF
            doc = self.fitz.open(pdf_path)
            
            # 提取所有页面的文本
            texts = []
            for page_num, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    texts.append(f"--- 第{page_num + 1}页 ---\n{text}")
            
            doc.close()
            
            full_text = '\n'.join(texts)
            logger.info(f"读取成功，{len(full_text)}字符，{len(doc)}页")
            
            return full_text
            
        except Exception as e:
            logger.error(f"读取 PDF 失败：{e}")
            return None
    
    def read_metadata(self, pdf_path: Union[str, Path]) -> Optional[dict]:
        """
        读取 PDF 元数据
        
        Args:
            pdf_path: PDF 文件路径
        
        Returns:
            元数据字典
        """
        if not self.fitz:
            return None
        
        try:
            doc = self.fitz.open(pdf_path)
            metadata = doc.metadata
            doc.close()
            
            return {
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'subject': metadata.get('subject', ''),
                'pages': len(doc) if hasattr(doc, '__len__') else 0,
            }
        except Exception as e:
            logger.error(f"读取元数据失败：{e}")
            return None
    
    def get_page_count(self, pdf_path: Union[str, Path]) -> int:
        """获取 PDF 页数"""
        if not self.fitz:
            return 0
        
        try:
            doc = self.fitz.open(pdf_path)
            count = len(doc)
            doc.close()
            return count
        except:
            return 0


if __name__ == '__main__':
    # 测试
    reader = PDFReader()
    
    if reader.fitz:
        # 检查测试文件
        test_pdf = Path("./workspace/input/test.pdf")
        if test_pdf.exists():
            content = reader.read(test_pdf)
            print(f"内容长度：{len(content)}")
            print(f"\n前 500 字:\n{content[:500]}...")
        else:
            print("测试文件不存在，请放入 PDF 文件到 workspace/input/test.pdf")
    else:
        print("PyMuPDF 未安装")
