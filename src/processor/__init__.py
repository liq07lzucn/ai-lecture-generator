#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容处理模块
"""

from .content_parser import ContentParser
from .knowledge_extractor import KnowledgeExtractor
from .lecture_generator import LectureGenerator as LectureProcessor

__all__ = ["ContentParser", "KnowledgeExtractor", "LectureProcessor"]
