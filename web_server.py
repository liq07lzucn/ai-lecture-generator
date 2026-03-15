#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易 Web 服务器 - 一键启动

用法: python3 web_server.py
访问：http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify, send_file
from pathlib import Path
import sys
import os

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.main import LectureGenerator

app = Flask(__name__)
generator = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI 讲课生成器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 { color: #333; margin-bottom: 10px; font-size: 32px; text-align: center; }
        .subtitle { color: #888; text-align: center; margin-bottom: 30px; }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 8px; color: #555; font-weight: 600; }
        input, textarea, select {
            width: 100%;
            padding: 14px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 15px;
            transition: all 0.3s;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        textarea { min-height: 120px; resize: vertical; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 16px 32px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .loading { text-align: center; padding: 30px; display: none; }
        .loading.show { display: block; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .result { margin-top: 30px; padding: 25px; background: #f8f9fa; border-radius: 12px; display: none; }
        .result.show { display: block; }
        .result-item { margin-bottom: 15px; padding: 15px; background: white; border-radius: 8px; border-left: 4px solid #667eea; }
        .result-item h3 { color: #333; font-size: 16px; margin-bottom: 8px; }
        .result-item p { color: #666; font-size: 14px; word-break: break-all; }
        .success { color: #28a745; font-weight: 600; }
        .error { color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 AI 讲课生成器</h1>
        <p class="subtitle">输入关键词，一键生成讲义 + PPT + 语音</p>
        
        <form id="form" onsubmit="generate(event)">
            <div class="form-group">
                <label>📝 课程主题</label>
                <input type="text" id="topic" placeholder="例如：人工智能基础" required>
            </div>
            
            <div class="form-group">
                <label>📄 输入内容 (可选，不填则 AI 自动生成)</label>
                <textarea id="content" placeholder="输入相关资料、文章内容... 留空则 AI 自动发挥"></textarea>
            </div>
            
            <div class="form-group">
                <label>⏱️ 讲课时长</label>
                <select id="duration">
                    <option value="5">5 分钟 (简短)</option>
                    <option value="10" selected>10 分钟 (标准)</option>
                    <option value="15">15 分钟 (详细)</option>
                    <option value="20">20 分钟 (深入)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>🎨 讲课风格</label>
                <select id="style">
                    <option value="通俗易懂">通俗易懂 (大学生)</option>
                    <option value="故事化">故事化 (罗辑思维风格)</option>
                    <option value="儿童版">儿童版 (芝麻街风格)</option>
                    <option value="专业版">专业版 (TED 演讲风格)</option>
                </select>
            </div>
            
            <button type="submit" class="btn" id="btn">🚀 开始生成</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>正在生成中，请稍候...（约 3-4 分钟）</p>
        </div>
        
        <div class="result" id="result"></div>
    </div>
    
    <script>
        async function generate(e) {
            e.preventDefault();
            
            const btn = document.getElementById('btn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            
            btn.disabled = true;
            loading.classList.add('show');
            result.classList.remove('show');
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        topic: document.getElementById('topic').value,
                        content: document.getElementById('content').value,
                        duration: parseInt(document.getElementById('duration').value),
                        style: document.getElementById('style').value
                    })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    result.innerHTML = '<div class="result-item"><h3 class="error">❌ 失败</h3><p>' + data.error + '</p></div>';
                } else {
                    result.innerHTML = `
                        <div class="result-item"><h3 class="success">✅ 生成完成!</h3></div>
                        <div class="result-item"><h3>📄 讲义</h3><p>${data.lecture_path}</p></div>
                        <div class="result-item"><h3>📊 PPT 大纲</h3><p>${data.ppt_path}</p></div>
                        <div class="result-item"><h3>❓ 测试题</h3><p>${data.questions_path}</p></div>
                        <div class="result-item"><h3>🔊 语音</h3><p>${data.audio_path || '未生成'}</p></div>
                        <div class="result-item"><h3>⏱️ 耗时</h3><p>${data.elapsed_seconds?.toFixed(1) || 'N/A'}秒</p></div>
                    `;
                }
                result.classList.add('show');
            } catch (err) {
                result.innerHTML = '<div class="result-item"><h3 class="error">❌ 错误</h3><p>' + err.message + '</p></div>';
                result.classList.add('show');
            } finally {
                btn.disabled = false;
                loading.classList.remove('show');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """生成 API"""
    global generator
    
    try:
        data = request.json
        topic = data.get('topic', '')
        content = data.get('content', '')
        duration = data.get('duration', 10)
        style = data.get('style', '通俗易懂')
        
        if not topic:
            return jsonify({'error': '请填写课程主题'})
        
        # 初始化生成器
        if not generator:
            generator = LectureGenerator()
        
        # 生成内容
        source = content if content else f"请生成关于{topic}的讲课内容"
        
        result = generator.generate(
            source=source,
            topic=topic,
            duration=duration,
            style=style
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🦞 AI 讲课生成器 - Web 服务启动中...")
    print("=" * 60)
    print("\n访问地址：http://localhost:5000")
    print("按 Ctrl+C 停止服务\n")
    
    # 安装 Flask
    try:
        import flask
    except ImportError:
        print("⚠️  正在安装 Flask...")
        os.system("pip3 install flask --break-system-packages -q")
        import flask
    
    app.run(host='0.0.0.0', port=5000, debug=False)
