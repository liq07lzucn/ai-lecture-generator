#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型配置
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelConfig:
    """模型配置"""
    
    # 聊天/讲义生成 (主力模型)
    chat_model: str = "qwen3:latest"
    
    # 轻量任务 (摘要、分类等)
    light_model: str = "deepseek-r1:1.5b"
    
    # 嵌入模型 (可选)
    embed_model: str = "nomic-embed-text"
    
    # 模型参数
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 4096
    
    @classmethod
    def from_dict(cls, config: Dict) -> "ModelConfig":
        """从字典创建配置"""
        return cls(
            chat_model=config.get('chat', 'qwen3:8b'),
            light_model=config.get('summary', 'deepseek-r1:1.5b'),
        )
    
    def get_model_for(self, task: str) -> str:
        """根据任务选择模型"""
        if task in ['summary', 'classify', 'extract_keywords']:
            return self.light_model
        return self.chat_model
