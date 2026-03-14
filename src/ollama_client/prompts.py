#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词模板优化版

包含更多场景和风格的提示词
"""

from typing import Dict


class PromptTemplates:
    """讲课生成提示词模板库"""
    
    # ========== 内容分析类 ==========
    
    CONTENT_SUMMARY = """
请用{word_count}字总结以下内容，要求：
1. 提取核心主题
2. 概括主要观点
3. 保持逻辑连贯

内容：
{content}
"""

    CONTENT_EXTRACT_JSON = """
你是一位专业的教育内容分析师。请分析以下文本，提取{max_points}个关键知识点。

文本内容：
{content}

请严格按以下 JSON 格式输出（不要其他内容）：
{
    "topic": "核心主题",
    "difficulty": "入门/进阶/专业",
    "key_points": [
        {"title": "知识点 1", "summary": "一句话概括", "level": "入门", "examples": ["例子 1"]},
        {"title": "知识点 2", "summary": "一句话概括", "level": "进阶", "examples": ["例子 2"]}
    ],
    "prerequisites": ["前置知识 1", "前置知识 2"],
    "learning_objectives": ["学习目标 1", "学习目标 2"]
}
"""

    # ========== 讲义生成类 ==========
    
    LECTURE_STANDARD = """
你是一位经验丰富的{style}讲师。请根据以下知识点生成一份讲课稿。

## 基本信息
- 主题：{topic}
- 时长：{duration}分钟
- 目标受众：{audience}
- 讲课风格：{style}

## 知识点
{key_points}

## 要求
1. **开场白**（10% 时间）：吸引注意力，介绍主题重要性
2. **知识点讲解**（70% 时间）：每个知识点包含：
   - 概念解释（是什么）
   - 实际例子（怎么用）
   - 常见误区（注意什么）
3. **互动环节**（10% 时间）：提问或小测试
4. **总结回顾**（10% 时间）：重点回顾 + 延伸思考

## 输出格式
使用 Markdown 格式，标注每个部分的时间分配。
语言风格：{language_style}
"""

    LECTURE_STORY = """
你是一位擅长讲故事的讲师。请用讲故事的方式讲解以下知识点。

主题：{topic}
知识点：{key_points}

要求：
1. 用一个真实或虚构的故事串联所有知识点
2. 故事要有起承转合
3. 每个知识点在故事的关键节点自然呈现
4. 让听众在听故事的过程中不知不觉学会知识
5. 时长：{duration}分钟

风格参考：罗辑思维、得到 App
"""

    LECTURE_DEBATE = """
你是一位擅长启发式教学的讲师。请用辩论/讨论的方式组织讲课。

主题：{topic}
知识点：{key_points}

设计思路：
1. 抛出一个有争议的问题开场
2. 呈现不同观点（正反方）
3. 在讨论中引入知识点作为论据
4. 引导听众自己得出结论
5. 最后总结共识

时长：{duration}分钟
"""

    # ========== PPT 生成类 ==========
    
    PPT_DETAILED = """
根据以下讲课内容，生成详细的 PPT 大纲（12-18 页）。

讲课内容：
{lecture_content}

请按以下 JSON 格式输出：
{
    "title": "PPT 主标题",
    "subtitle": "副标题",
    "total_slides": 15,
    "slides": [
        {
            "page": 1,
            "type": "cover",
            "title": "封面页",
            "content": {
                "main_title": "主标题文字",
                "subtitle": "副标题文字",
                "footer": "讲师姓名 | 日期"
            },
            "speaker_notes": "开场白：欢迎大家..."
        },
        {
            "page": 2,
            "type": "catalog",
            "title": "目录",
            "content": {
                "items": ["第一部分：XXX", "第二部分：XXX", "第三部分：XXX"]
            },
            "speaker_notes": "今天我们将学习三个部分..."
        },
        {
            "page": 3,
            "type": "content",
            "title": "知识点 1",
            "content": {
                "bullet_points": ["要点 1", "要点 2", "要点 3"],
                "image_suggestion": "建议配图：XXX"
            },
            "speaker_notes": "详细讲解内容..."
        }
    ]
}

注意：
- 封面、目录、过渡页、内容页、总结页要合理分布
- 每页内容要点不超过 5 个
- 标注建议配图类型
"""

    PPT_SIMPLE = """
根据讲课内容生成简洁的 PPT 大纲（8-10 页）。

内容：{lecture_content}

输出格式：每页包含 [页码，标题，3-5 个要点]
"""

    # ========== 测试题生成类 ==========
    
    QUESTIONS_MIXED = """
根据以下内容，生成一套测试题。

内容：
{content}

要求：
- 单选题：3 道（4 个选项）
- 判断题：2 道
- 简答题：1 道
- 难度分布：易 1 道，中 3 道，难 2 道

请按以下 JSON 格式输出：
{
    "questions": [
        {
            "id": 1,
            "type": "single_choice",
            "difficulty": "easy",
            "question": "问题内容",
            "options": ["A. 选项 1", "B. 选项 2", "C. 选项 3", "D. 选项 4"],
            "answer": "A",
            "explanation": "答案解析"
        },
        {
            "id": 2,
            "type": "true_false",
            "difficulty": "medium",
            "question": "问题内容",
            "answer": "正确",
            "explanation": "答案解析"
        },
        {
            "id": 3,
            "type": "short_answer",
            "difficulty": "hard",
            "question": "问题内容",
            "answer_points": ["要点 1", "要点 2", "要点 3"],
            "explanation": "答案解析"
        }
    ]
}
"""

    QUESTIONS_INTERACTIVE = """
根据讲课内容，设计一个互动问答环节。

内容：{content}
时长：5 分钟

要求：
1. 设计 3-5 个互动问题
2. 每个问题包含：
   - 问题内容
   - 预期答案
   - 追问（如果答对/答错）
   - 互动形式（举手/抢答/小组讨论）

格式：JSON 数组
"""

    # ========== 特殊场景类 ==========
    
    LECTURE_KIDS = """
你是一位擅长给儿童讲课的老师。请用儿童能理解的方式讲解。

主题：{topic}
知识点：{key_points}
目标年龄：{age_range}岁

要求：
1. 使用简单词汇（避免专业术语）
2. 多用比喻和类比
3. 加入趣味元素（故事、游戏、动画角色）
4. 每 3 分钟一个互动环节
5. 时长：{duration}分钟

风格参考：芝麻街、宝宝巴士
"""

    LECTURE_PROFESSIONAL = """
你是一位行业专家。请用专业严谨的方式讲解。

主题：{topic}
知识点：{key_points}
受众：行业从业者

要求：
1. 使用专业术语（必要时标注英文）
2. 引用行业数据/案例
3. 分析前沿趋势
4. 提供实践建议
5. 时长：{duration}分钟

风格参考： TED 演讲、行业峰会
"""

    # ========== 辅助工具类 ==========
    
    EXPAND_CONTENT = """
请扩展以下内容，使其更加丰富详细。

原始内容：
{content}

扩展要求：
1. 增加实际案例（至少 2 个）
2. 增加数据支撑
3. 增加历史背景
4. 增加未来展望
5. 扩展后字数：{target_word_count}字
"""

    SIMPLIFY_CONTENT = """
请用通俗易懂的语言重写以下内容，让{audience}能理解。

原始内容：
{content}

要求：
1. 避免专业术语（或用比喻解释）
2. 句子简短（每句不超过 20 字）
3. 增加生活化的例子
4. 字数控制在{target_word_count}字以内
"""

    TRANSLATE_STYLE = """
请将以下内容改写成{target_style}风格。

原始内容：
{content}

目标风格：{target_style}
（如：幽默风趣、严肃专业、温暖治愈、激情澎湃等）
"""

    @classmethod
    def get(cls, name: str) -> str:
        """获取模板"""
        templates = {
            # 内容分析
            "content_summary": cls.CONTENT_SUMMARY,
            "content_extract": cls.CONTENT_EXTRACT_JSON,
            # 讲义生成
            "lecture_standard": cls.LECTURE_STANDARD,
            "lecture_story": cls.LECTURE_STORY,
            "lecture_debate": cls.LECTURE_DEBATE,
            # PPT 生成
            "ppt_detailed": cls.PPT_DETAILED,
            "ppt_simple": cls.PPT_SIMPLE,
            # 测试题
            "questions_mixed": cls.QUESTIONS_MIXED,
            "questions_interactive": cls.QUESTIONS_INTERACTIVE,
            # 特殊场景
            "lecture_kids": cls.LECTURE_KIDS,
            "lecture_professional": cls.LECTURE_PROFESSIONAL,
            # 辅助工具
            "expand_content": cls.EXPAND_CONTENT,
            "simplify_content": cls.SIMPLIFY_CONTENT,
            "translate_style": cls.TRANSLATE_STYLE,
        }
        return templates.get(name, "")
    
    @classmethod
    def fill(cls, name: str, **kwargs) -> str:
        """填充模板"""
        template = cls.get(name)
        if not template:
            return ""
        return template.format(**kwargs)
    
    @classmethod
    def list_templates(cls) -> list:
        """列出所有模板"""
        return [
            ("content_summary", "内容摘要"),
            ("content_extract", "知识点提取"),
            ("lecture_standard", "标准讲义"),
            ("lecture_story", "故事化讲义"),
            ("lecture_debate", "辩论式讲义"),
            ("lecture_kids", "儿童版讲义"),
            ("lecture_professional", "专业版讲义"),
            ("ppt_detailed", "详细 PPT"),
            ("ppt_simple", "简洁 PPT"),
            ("questions_mixed", "混合题型"),
            ("questions_interactive", "互动问答"),
            ("expand_content", "内容扩展"),
            ("simplify_content", "内容简化"),
            ("translate_style", "风格转换"),
        ]


if __name__ == '__main__':
    # 测试模板
    print("可用提示词模板:\n")
    for name, desc in PromptTemplates.list_templates():
        print(f"  {name:25} - {desc}")
    
    # 测试填充
    print("\n" + "=" * 60)
    print("测试：讲义生成模板\n")
    
    prompt = PromptTemplates.fill(
        "lecture_standard",
        topic="人工智能基础",
        duration=10,
        audience="大学生",
        style="通俗易懂",
        language_style="生动有趣",
        key_points="- 机器学习：让计算机通过数据学习\n- 深度学习：模拟人脑神经网络"
    )
    
    print(prompt[:500] + "...")
