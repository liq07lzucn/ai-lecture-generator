#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超简单 Web 服务器 - 保证历史记录能显示！
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import sys, os, json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from src.main import LectureGenerator

app = Flask(__name__)
generator = None

@app.route('/')
def index():
    # 获取历史记录
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
    
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI 讲课生成器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .history-bar { background: #f8f9fa; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e0e0e0; }
        .history-count { color: #667eea; font-weight: 600; }
        .btn-history { background: white; border: 2px solid #667eea; color: #667eea; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; }
        .btn-history:hover { background: #667eea; color: white; }
        .content { padding: 40px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #555; }
        input, textarea, select { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 15px; }
        textarea { min-height: 100px; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 14px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; width: 100%; }
        .btn:hover { opacity: 0.9; }
        .loading { text-align: center; padding: 30px; display: none; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s; margin: 0 auto 15px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .result { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 12px; display: none; }
        .history-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }
        .history-content { background: white; margin: 50px auto; padding: 30px; border-radius: 12px; max-width: 600px; max-height: 400px; overflow-y: auto; }
        .history-item { padding: 15px; border-bottom: 1px solid #e0e0e0; }
        .close-btn { float: right; font-size: 24px; cursor: pointer; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 AI 讲课生成器</h1>
            <p>输入主题，一键生成讲义 + PPT + 语音</p>
        </div>
        
        <div class="history-bar">
            <span class="history-count">📚 已生成 ''' + str(len(history)) + ''' 个课程</span>
            <button class="btn-history" onclick="showHistory()">📜 查看历史记录</button>
        </div>
        
        <div class="content">
            <form onsubmit="generate(event)">
                <div class="form-group">
                    <label>📝 课程主题</label>
                    <input type="text" id="topic" placeholder="例如：人工智能基础" required>
                </div>
                <div class="form-group">
                    <label>⏱️ 时长</label>
                    <select id="duration">
                        <option value="5">5 分钟</option>
                        <option value="10" selected>10 分钟</option>
                        <option value="15">15 分钟</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>🎨 风格</label>
                    <select id="style">
                        <option value="通俗易懂">通俗易懂</option>
                        <option value="故事化">故事化</option>
                        <option value="儿童版">儿童版</option>
                    </select>
                </div>
                <button type="submit" class="btn">🚀 开始生成</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>生成中...（约 3-4 分钟）</p>
            </div>
            
            <div class="result" id="result"></div>
        </div>
    </div>
    
    <div class="history-modal" id="historyModal">
        <div class="history-content">
            <span class="close-btn" onclick="closeHistory()">&times;</span>
            <h2 style="margin-bottom:20px;">📜 历史记录</h2>
            ''' + ''.join([f'<div class="history-item"><strong>{i+1}. {h["topic"]}</strong><br><small>{h["time"]}</small><br><a href="{h["lecture"]}" target="_blank" style="color:#667eea;">📄 讲义</a>' + (f' | <a href="{h["audio"]}" target="_blank">🔊 语音</a>' if h["audio"] else '') + '</div>' for i, h in enumerate(history)]) + '''
        </div>
    </div>
    
    <script>
        function showHistory() { document.getElementById('historyModal').style.display = 'block'; }
        function closeHistory() { document.getElementById('historyModal').style.display = 'none'; }
        function generate(e) {
            e.preventDefault();
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            fetch('/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    topic: document.getElementById('topic').value,
                    duration: parseInt(document.getElementById('duration').value),
                    style: document.getElementById('style').value
                })
            }).then(r => r.json()).then(data => {
                document.getElementById('loading').style.display = 'none';
                if (data.error) {
                    document.getElementById('result').innerHTML = '<p style="color:red;">❌ ' + data.error + '</p>';
                } else {
                    document.getElementById('result').innerHTML = '<h3>✅ 完成!</h3><p>讲义：<a href="' + data.lecture_path + '">' + data.lecture_path + '</a></p>' + (data.audio_path ? '<p>语音：<a href="' + data.audio_path + '">播放</a></p>' : '');
                }
                document.getElementById('result').style.display = 'block';
            }).catch(err => {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('result').innerHTML = '<p style="color:red;">❌ ' + err.message + '</p>';
                document.getElementById('result').style.display = 'block';
            });
        }
    </script>
</body>
</html>'''
    return html

@app.route('/api/generate', methods=['POST'])
def api_generate():
    global generator
    try:
        data = request.json
        if not generator:
            generator = LectureGenerator()
        result = generator.generate(
            source=f"生成关于{data.get('topic', '')}的内容",
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

if __name__ == '__main__':
    print("\n🦞 AI 讲课生成器 - 启动中...")
    print("访问：http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
