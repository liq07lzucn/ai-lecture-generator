#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词模板库
"""

from typing import Dict


class PromptTemplates:
    """讲课生成提示词模板"""
    
    # 内容拆解
    CONTENT_EXTRACT = """
你是一位专业的教育内容分析师。请分析以下文本，提取关键知识点。

要求:
1. 识别核心主题
2. 提取 3-5 个关键知识点
3. 每个知识点用一句话概括
4. 标注难度等级 (入门/进阶/专业)

文本内容:
{text}

请按以下 JSON 格式输出:
{{
    "topic": "核心主题",
    "key_points": [
        {{"title": "知识点 1", "summary": "概括", "level": "入门"}},
        ...
    ],
    "estimated_duration": 10
}}
"""

    # 讲义生成
    LECTURE_GENERATE = """
你是一位经验丰富的大学讲师。请根据以下知识点生成一份讲课稿。

要求:
1. 开场白 (吸引注意力，介绍主题)
2. 知识点讲解 (每个知识点 3-5 分钟，包含例子)
3. 互动环节 (提问或小测试)
4. 总结回顾

风格：{style}
时长：{duration} 分钟
目标受众：{audience}

知识点:
{key_points}

请生成完整的讲课稿，标注每个部分的时间分配。
"""

    # PPT 大纲生成
    PPT_OUTLINE = """
根据以下讲课内容，生成 PPT 大纲。

要求:
1. 10-15 页幻灯片
2. 每页包含：标题、要点 (3-5 个)、备注
3. 结构清晰，逻辑连贯

讲课内容:
{lecture_content}

请按以下格式输出:
{{
    "title": "PPT 标题",
    "slides": [
        {{
            "page": 1,
            "title": "封面",
            "points": ["主标题", "副标题", "讲师姓名"],
            "notes": "开场白"
        }},
        ...
    ]
}}
"""

    # 摘要生成
    SUMMARY_GENERATE = """
请用 200 字总结以下内容:

{content}
"""

    # 问题生成
    QUESTION_GENERATE = """
根据以下内容，生成 3 个测试问题 (含答案):

{content}

格式:
1. 问题类型 (选择/填空/简答)
2. 问题内容
3. 正确答案
4. 解析
"""

    @classmethod
    def get(cls, name: str) -> str:
        """获取模板"""
        templates = {
            "content_extract": cls.CONTENT_EXTRACT,
            "lecture_generate": cls.LECTURE_GENERATE,
            "ppt_outline": cls.PPT_OUTLINE,
            "summary_generate": cls.SUMMARY_GENERATE,
            "question_generate": cls.QUESTION_GENERATE,
        }
        return templates.get(name, "")
    
    @classmethod
    def fill(cls, name: str, **kwargs) -> str:
        """填充模板"""
        template = cls.get(name)
        return template.format(**kwargs)
