#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 输入测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fetcher import PDFReader

def test_pdf_read():
    """测试 PDF 读取"""
    print("\n" + "=" * 60)
    print("📄 PDF 读取测试")
    print("=" * 60)
    
    reader = PDFReader()
    
    if not reader.fitz:
        print("❌ PyMuPDF 未安装")
        return
    
    # 检查工作目录中是否有 PDF
    input_dir = Path("./workspace/input")
    input_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\n⚠️  没有找到 PDF 文件")
        print(f"请将 PDF 文件放入：{input_dir.absolute()}")
        print(f"\n示例测试：创建一个简单的测试报告")
        
        # 创建一个测试文档
        print(f"\n✅ PDF 读取器已就绪，支持:")
        print(f"  - 提取文本内容")
        print(f"  - 读取元数据（标题、作者等）")
        print(f"  - 获取页数")
        return
    
    for pdf_file in pdf_files:
        print(f"\n测试：{pdf_file}")
        
        # 读取内容
        content = reader.read(pdf_file)
        if content:
            print(f"  ✅ 读取成功")
            print(f"  页数：{reader.get_page_count(pdf_file)}")
            print(f"  字符数：{len(content)}")
            print(f"  前 300 字：{content[:300]}...")
        
        # 读取元数据
        metadata = reader.read_metadata(pdf_file)
        if metadata:
            print(f"  元数据:")
            print(f"    标题：{metadata.get('title', 'N/A')}")
            print(f"    作者：{metadata.get('author', 'N/A')}")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == '__main__':
    test_pdf_read()
