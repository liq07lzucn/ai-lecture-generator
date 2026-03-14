#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama API 客户端封装
"""

import requests
import json
from typing import List, Dict, Optional, Generator
from loguru import logger


class OllamaClient:
    """Ollama API 客户端"""
    
    def __init__(self, host: str = "http://192.168.0.214:11434", timeout: int = 120):
        """
        初始化客户端
        
        Args:
            host: Ollama 服务地址
            timeout: 请求超时时间 (秒)
        """
        self.host = host.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        logger.info(f"Ollama 客户端初始化：{host}")
    
    def check_connection(self) -> bool:
        """检查连接状态"""
        try:
            response = self.session.get(f"{self.host}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get('models', [])
            logger.info(f"✅ Ollama 连接成功，{len(models)}个模型可用")
            return True
        except Exception as e:
            logger.error(f"❌ Ollama 连接失败：{e}")
            return False
    
    def list_models(self) -> List[Dict]:
        """获取可用模型列表"""
        try:
            response = self.session.get(f"{self.host}/api/tags", timeout=10)
            response.raise_for_status()
            return response.json().get('models', [])
        except Exception as e:
            logger.error(f"获取模型列表失败：{e}")
            return []
    
    def chat(self, model: str, messages: List[Dict], stream: bool = False) -> str:
        """
        聊天/对话
        
        Args:
            model: 模型名称
            messages: 消息列表 [{"role": "user", "content": "..."}]
            stream: 是否流式输出
        
        Returns:
            响应文本
        """
        url = f"{self.host}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        try:
            logger.debug(f"调用模型：{model}, 消息数：{len(messages)}")
            
            if stream:
                return self._stream_chat(url, payload)
            else:
                response = self.session.post(url, json=payload, timeout=self.timeout)
                response.raise_for_status()
                result = response.json()
                content = result.get('message', {}).get('content', '')
                logger.debug(f"响应长度：{len(content)}")
                return content
                
        except Exception as e:
            logger.error(f"聊天请求失败：{e}")
            return ""
    
    def _stream_chat(self, url: str, payload: Dict) -> str:
        """流式聊天"""
        full_response = ""
        
        try:
            with self.session.post(url, json=payload, stream=True, timeout=self.timeout) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if 'message' in data:
                            content = data['message'].get('content', '')
                            full_response += content
                            # 可以实时输出
                            # print(content, end='', flush=True)
                
        except Exception as e:
            logger.error(f"流式聊天失败：{e}")
        
        return full_response
    
    def generate(self, model: str, prompt: str, system: str = None) -> str:
        """
        文本生成 (使用 chat API，兼容性更好)
        
        Args:
            model: 模型名称
            prompt: 提示词
            system: 系统提示
        
        Returns:
            生成文本
        """
        messages = [{"role": "user", "content": prompt}]
        if system:
            messages.insert(0, {"role": "system", "content": system})
        
        return self.chat(model, messages)
    
    def embed(self, model: str, text: str) -> List[float]:
        """
        文本嵌入 (embedding)
        
        Args:
            model: 嵌入模型名称
            text: 输入文本
        
        Returns:
            嵌入向量
        """
        url = f"{self.host}/api/embeddings"
        payload = {
            "model": model,
            "prompt": text
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            return result.get('embedding', [])
        except Exception as e:
            logger.error(f"嵌入请求失败：{e}")
            return []


# 便捷函数
def get_client(config: Dict = None) -> OllamaClient:
    """获取客户端实例"""
    if config:
        return OllamaClient(
            host=config.get('host', 'http://192.168.0.214:11434'),
            timeout=config.get('timeout', 120)
        )
    return OllamaClient()


if __name__ == '__main__':
    # 测试
    client = OllamaClient()
    
    if client.check_connection():
        models = client.list_models()
        print(f"\n可用模型:")
        for m in models:
            print(f"  - {m['name']} ({m.get('size', 0)/1e9:.1f}GB)")
        
        # 测试对话
        response = client.chat(
            model="qwen3:8b",
            messages=[{"role": "user", "content": "你好，介绍一下你自己"}]
        )
        print(f"\n测试回复：{response[:200]}...")
