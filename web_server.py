#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 讲课生成器 - Web 服务（修复版）

功能：
- 直接显示讲义内容
- 在线播放语音
- 历史记录弹窗
- 一键下载
"""

from flask import Flask, render_template_string, request, jsonify, send_from_directory
from pathlib import Path
import sys, os, json, zipfile
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from src.main import LectureGenerator

app = Flask(__name__)
generator = None

# 获取历史记录
def get_history():
    output_dir = Path('./workspace/output')
    history = []
    for meta_file in sorted(output_dir.glob("meta_*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                history.append({
                    'topic': data.get('topic', ''),
                    'time': datetime.fromtimestamp(meta_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M'),
                    'lecture': data.get('lecture_path', ''),
                    'audio': data.get('audio_path', '')
                })
        except:
            pass
    return history

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 讲课生成器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .history-bar { background: #f8f9fa; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e0e0e0; }
        .history-count { color: #667eea; font-weight: 600; }
        .btn-history { background: white; border: 2px solid #667eea; color: #667eea; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
        .btn-history:hover { background: #667eea; color: white; }
        .content { padding: 40px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #555; }
        input, textarea, select { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 15px; transition: all 0.3s; }
        input:focus, textarea:focus, select:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        textarea { min-height: 100px; resize: vertical; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 14px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; width: 100%; transition: all 0.3s; }
        .btn:hover { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
        .loading { text-align: center; padding: 30px; display: none; }
        .loading.show { display: block; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .result { display: none; margin-top: 30px; padding: 25px; background: #f8f9fa; border-radius: 12px; }
        .result.show { display: block; }
        .result-header { background: #e8f5e9; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center; }
        .result-header h2 { color: #28a745; }
        .history-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }
        .history-content { background: white; margin: 50px auto; padding: 30px; border-radius: 12px; max-width: 600px; max-height: 500px; overflow-y: auto; position: relative; }
        .history-item { padding: 15px; border-bottom: 1px solid #e0e0e0; }
        .history-item:last-child { border-bottom: none; }
        .close-btn { position: absolute; top: 15px; right: 20px; font-size: 28px; cursor: pointer; color: #888; }
        .close-btn:hover { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 AI 讲课生成器</h1>
            <p>输入主题，一键生成讲义 + PPT + 语音</p>
        </div>
        
        <div class="history-bar">
            <span class="history-count">📚 已生成 {{ history|length }} 个课程</span>
            <button class="btn-history" onclick="showHistory()">📜 查看历史记录</button>
        </div>
        
        <div class="content">
            <form onsubmit="generate(event)">
                <div class="form-group">
                    <label>📝 课程主题</label>
                    <input type="text" id="topic" placeholder="例如：人工智能基础" required>
                </div>
                <div class="form-group">
                    <label>📄 参考资料 (可选)</label>
                    <textarea id="content" placeholder="粘贴相关文章... 留空则 AI 自动发挥"></textarea>
                </div>
                <div class="form-group">
                    <label>⏱️ 讲课时长</label>
                    <select id="duration">
                        <option value="5">5 分钟 - 简短</option>
                        <option value="10" selected>10 分钟 - 标准</option>
                        <option value="15">15 分钟 - 详细</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>🎨 讲课风格</label>
                    <select id="style">
                        <option value="通俗易懂">通俗易懂</option>
                        <option value="故事化">故事化</option>
                        <option value="儿童版">儿童版</option>
                        <option value="专业版">专业版</option>
                    </select>
                </div>
                <button type="submit" class="btn">🚀 开始生成</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在生成中，请稍候...（约 3-4 分钟）</p>
            </div>
            
            <div class="result" id="result"></div>
        </div>
    </div>
    
    <div class="history-modal" id="historyModal">
        <div class="history-content">
            <span class="close-btn" onclick="closeHistory()">&times;</span>
            <h2 style="margin-bottom:20px;">📜 历史记录</h2>
            {% for h in history %}
            <div class="history-item">
                <strong>{{ loop.index }}. {{ h.topic }}</strong><br>
                <small style="color:#888;">📅 {{ h.time }}</small><br>
                <a href="{{ h.lecture }}" target="_blank" style="color:#667eea;">📄 查看讲义</a>
                {% if h.audio %} | <a href="{{ h.audio }}" target="_blank">🔊 播放语音</a>{% endif %}
            </div>
            {% endfor %}
        </div>
    </div>
    
    <script>
        function showHistory() { document.getElementById('historyModal').style.display = 'block'; }
        function closeHistory() { document.getElementById('historyModal').style.display = 'none'; }
        function generate(e) {
            e.preventDefault();
            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
            fetch('/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    topic: document.getElementById('topic').value,
                    content: document.getElementById('content').value,
                    duration: parseInt(document.getElementById('duration').value),
                    style: document.getElementById('style').value
                })
            }).then(r => r.json()).then(data => {
                document.getElementById('loading').classList.remove('show');
                if (data.error) {
                    document.getElementById('result').innerHTML = '<div class="result-header" style="background:#ffebee;"><h2 style="color:#f44336;">❌ 生成失败</h2><p>' + data.error + '</p></div>';
                } else {
                    document.getElementById('result').innerHTML = '<div class="result-header"><h2>✅ 生成完成!</h2><p>课程：' + (data.topic||'') + '</p></div>' + 
                        '<p style="margin-top:15px;"><strong>📄 讲义：</strong><a href="' + (data.lecture_path||'') + '" target="_blank">' + (data.lecture_path||'') + '</a></p>' +
                        (data.audio_path ? '<p><strong>🔊 语音：</strong><a href="' + data.audio_path + '" target="_blank">播放</a> <audio controls src="' + data.audio_path + '" style="margin-top:10px;"></audio></p>' : '') +
                        '<p style="margin-top:15px;"><strong>⏱️ 耗时：</strong>' + (data.elapsed_seconds||0).toFixed(1) + '秒</p>';
                }
                document.getElementById('result').classList.add('show');
            }).catch(err => {
                document.getElementById('loading').classList.remove('show');
                document.getElementById('result').innerHTML = '<div class="result-header" style="background:#ffebee;"><h2 style="color:#f44336;">❌ 错误</h2><p>' + err.message + '</p></div>';
                document.getElementById('result').classList.add('show');
            });
        }
    </script>
</body>
</html>'''

@app.route('/')
def index():
    history = get_history()
    return render_template_string(HTML_TEMPLATE, history=history)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    global generator
    try:
        data = request.json
        if not generator:
            generator = LectureGenerator()
        result = generator.generate(
            source=data.get('content', '') or f"生成关于{data.get('topic', '')}的内容",
            topic=data.get('topic', ''),
            duration=data.get('duration', 10),
            style=data.get('style', '通俗易懂')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/workspace/output/<path:filename>')
def serve_output(filename):
    return send_from_directory('./workspace/output', filename)

@app.route('/file/<filename>')
def serve_file(filename):
    """提供输出文件访问"""
    return send_from_directory('./workspace/output', filename)

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🦞 AI 讲课生成器 - Web 服务")
    print("=" * 60)
    print("\n访问地址：http://localhost:5000")
    print("按 Ctrl+C 停止服务\n")
    
    try:
        import flask
    except ImportError:
        print("⚠️  正在安装 Flask...")
        os.system("pip3 install flask --break-system-packages -q")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
"pip3 install flask --break-system-packages -q")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
