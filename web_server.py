#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户友好版 Web 服务器

特点:
- 直接显示讲义内容
- 在线播放语音
- 一键下载所有文件
- 无需懂技术
"""

from flask import Flask, render_template_string, request, jsonify, send_file, send_from_directory
from pathlib import Path
import sys
import os
import json
import zipfile
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from src.main import LectureGenerator

app = Flask(__name__)
generator = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 讲课生成器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 16px; }
        .history-bar {
            background: #f8f9fa;
            padding: 15px 40px;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .history-count { color: #667eea; font-weight: 600; font-size: 15px; }
        .btn-history {
            background: white;
            border: 2px solid #667eea;
            color: #667eea;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-history:hover { background: #667eea; color: white; }
        .content { padding: 40px; }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 8px; color: #555; font-weight: 600; font-size: 15px; }
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
        textarea { min-height: 100px; resize: vertical; }
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
        .btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
        .loading { text-align: center; padding: 40px; display: none; }
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
        .result { display: none; margin-top: 30px; }
        .result.show { display: block; }
        .result-header {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
        }
        .result-header h2 { color: #28a745; font-size: 24px; margin-bottom: 10px; }
        .result-actions { display: flex; gap: 10px; margin-bottom: 20px; }
        .result-actions button {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-download { background: #28a745; color: white; }
        .btn-download:hover { background: #218838; }
        .section { margin-bottom: 25px; }
        .section-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        .content-box {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        .content-box h3 { color: #333; margin-bottom: 15px; }
        .content-box p { color: #666; line-height: 1.8; white-space: pre-wrap; }
        .audio-player {
            width: 100%;
            margin-top: 15px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #e0e0e0;
        }
        .stat-value { font-size: 24px; font-weight: 600; color: #667eea; }
        .stat-label { font-size: 13px; color: #888; margin-top: 5px; }
        .error { color: #dc3545; background: #fff5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 AI 讲课生成器</h1>
            <p>输入主题，一键生成完整讲课内容（讲义 + PPT + 语音）</p>
        </div>
        
        <div class="content">
            <form id="form" onsubmit="generate(event)">
                <div class="form-group">
                    <label>📝 课程主题 <span style="color: #dc3545">*</span></label>
                    <input type="text" id="topic" placeholder="例如：人工智能基础、Python 入门、时间管理..." required>
                </div>
                
                <div class="form-group">
                    <label>📄 参考资料 (可选)</label>
                    <textarea id="content" placeholder="粘贴相关文章、资料... 留空则 AI 自动发挥"></textarea>
                </div>
                
                <div class="form-group">
                    <label>⏱️ 讲课时长</label>
                    <select id="duration">
                        <option value="5">5 分钟 - 简短介绍</option>
                        <option value="10" selected>10 分钟 - 标准课程</option>
                        <option value="15">15 分钟 - 详细讲解</option>
                        <option value="20">20 分钟 - 深入探讨</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>🎨 讲课风格</label>
                    <select id="style">
                        <option value="通俗易懂">通俗易懂 - 适合大学生</option>
                        <option value="故事化">故事化 - 罗辑思维风格</option>
                        <option value="儿童版">儿童版 - 芝麻街风格</option>
                        <option value="专业版">专业版 - TED 演讲风格</option>
                    </select>
                </div>
                
                <button type="submit" class="btn" id="btn">🚀 开始生成</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在生成中，请稍候...（约 3-4 分钟）</p>
                <p style="color: #888; font-size: 14px; margin-top: 10px;">AI 正在：提取知识点 → 生成讲义 → 制作 PPT → 录制语音</p>
            </div>
            
            <div class="result" id="result"></div>
        </div>
    </div>
    
    <script>
        // 加载历史记录数量
        fetch('/api/history')
            .then(r => r.json())
            .then(data => {
                document.getElementById('history-count').textContent = '📚 已生成 ' + data.length + ' 个课程';
            })
            .catch(() => {
                document.getElementById('history-count').textContent = '📚 历史记录';
            });
        
        function showHistory() {
            fetch('/api/history')
                .then(r => r.json())
                .then(data => {
                    if (data.length === 0) {
                        alert('还没有历史记录');
                        return;
                    }
                    
                    let html = '<div style="max-height: 400px; overflow-y: auto; text-align: left;">';
                    data.forEach((item, i) => {
                        html += '<div style="padding: 15px; border-bottom: 1px solid #e0e0e0;">';
                        html += '<strong>' + (i+1) + '. ' + item.topic + '</strong><br>';
                        html += '<small style="color: #888;">📅 ' + new Date(item.timestamp).toLocaleString() + ' | ⏱️ ' + item.elapsed_seconds.toFixed(0) + '秒</small><br>';
                        html += '<a href="/workspace/output/' + item.lecture_path.split('/').pop() + '" target="_blank" style="color: #667eea;">📄 查看讲义</a>';
                        if (item.audio_path) {
                            html += ' | <a href="' + item.audio_path + '" target="_blank">🔊 播放语音</a>';
                        }
                        html += '</div>';
                    });
                    html += '</div>';
                    
                    alert(html);
                });
        }
        
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
                    result.innerHTML = '<div class="error"><strong>❌ 生成失败</strong><br>' + data.error + '</div>';
                } else {
                    showResult(data);
                }
                result.classList.add('show');
            } catch (err) {
                result.innerHTML = '<div class="error"><strong>❌ 错误</strong><br>' + err.message + '</div>';
                result.classList.add('show');
            } finally {
                btn.disabled = false;
                loading.classList.remove('show');
            }
        }
        
        function showResult(data) {
            const stats = `
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value">${data.elapsed_seconds?.toFixed(0) || 'N/A'}秒</div>
                        <div class="stat-label">生成耗时</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${data.duration || 10}分钟</div>
                        <div class="stat-label">课程时长</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${data.word_count || 'N/A'}字</div>
                        <div class="stat-label">讲义字数</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${data.slide_count || 'N/A'}页</div>
                        <div class="stat-label">PPT 页数</div>
                    </div>
                </div>
            `;
            
            const actions = `
                <div class="result-actions">
                    <button class="btn-download" onclick="downloadAll()">📦 下载全部文件</button>
                    ${data.audio_path ? '<button class="btn-download" style="background:#17a2b8" onclick="playAudio()">▶️ 播放语音</button>' : ''}
                </div>
            `;
            
            const lecture = data.lecture_content ? `
                <div class="section">
                    <div class="section-title">📄 讲义预览</div>
                    <div class="content-box">
                        <h3>${data.topic}</h3>
                        <p>${data.lecture_content}</p>
                    </div>
                </div>
            ` : '';
            
            const audio = data.audio_path ? `
                <div class="section">
                    <div class="section-title">🔊 语音讲解</div>
                    <div class="content-box">
                        <audio controls class="audio-player" id="audio-player">
                            <source src="${data.audio_path}" type="audio/mpeg">
                            您的浏览器不支持音频播放
                        </audio>
                    </div>
                </div>
            ` : '';
            
            const ppt = data.ppt_content ? `
                <div class="section">
                    <div class="section-title">📊 PPT 大纲预览</div>
                    <div class="content-box">
                        <p>${data.ppt_content}</p>
                    </div>
                </div>
            ` : '';
            
            document.getElementById('result').innerHTML = `
                <div class="result-header">
                    <h2>✅ 生成完成!</h2>
                    <p>课程主题：${data.topic}</p>
                </div>
                ${stats}
                ${actions}
                ${lecture}
                ${ppt}
                ${audio}
            `;
        }
        
        function downloadAll() {
            window.location.href = '/api/download/' + currentSessionId;
        }
        
        function playAudio() {
            const audio = document.getElementById('audio-player');
            if (audio) audio.play();
        }
        
        function showHistory() {
            fetch('/api/history')
                .then(r => r.json())
                .then(data => {
                    if (data.length === 0) {
                        alert('还没有历史记录');
                        return;
                    }
                    
                    let html = '<div style="max-height: 400px; overflow-y: auto; text-align: left;">';
                    data.forEach((item, i) => {
                        html += `<div style="padding: 15px; border-bottom: 1px solid #e0e0e0;">
                            <strong>${i+1}. ${item.topic}</strong><br>
                            <small style="color: #888;">📅 ${new Date(item.timestamp).toLocaleString()} | ⏱️ ${item.elapsed_seconds.toFixed(0)}秒</small><br>
                            <a href="/workspace/output/${item.lecture_path.split('/').pop()}" target="_blank" style="color: #667eea;">📄 查看讲义</a>
                            ${item.audio_path ? ` | <a href="${item.audio_path}" target="_blank">🔊 播放语音</a>` : ''}
                        </div>`;
                    });
                    html += '</div>';
                    
                    alert(html);
                });
        }
        
        let currentSessionId = '';
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
            return jsonify({'error': '请填写课程主题'}), 400
        
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
        
        if 'error' in result:
            return jsonify(result)
        
        # 读取讲义内容
        lecture_content = ''
        if result.get('lecture_path'):
            try:
                with open(result['lecture_path'], 'r', encoding='utf-8') as f:
                    lecture_content = f.read()
            except:
                pass
        
        # 读取 PPT 内容
        ppt_content = ''
        if result.get('ppt_path'):
            try:
                with open(result['ppt_path'], 'r', encoding='utf-8') as f:
                    ppt_data = json.load(f)
                    ppt_content = f"共{len(ppt_data.get('slides', []))}页幻灯片\\n\\n"
                    for slide in ppt_data.get('slides', [])[:5]:
                        ppt_content += f"第{slide.get('page', 0)}页：{slide.get('title', '')}\\n"
                        for point in slide.get('points', [])[:3]:
                            ppt_content += f"  • {point}\\n"
                        ppt_content += "\\n"
            except:
                pass
        
        # 统计信息
        result['topic'] = topic
        result['lecture_content'] = lecture_content
        result['ppt_content'] = ppt_content
        result['word_count'] = len(lecture_content) if lecture_content else 0
        result['slide_count'] = len(ppt_data.get('slides', [])) if 'ppt_data' in dir() else 0
        
        # 生成 session ID 用于下载
        session_id = datetime.now().strftime('%Y%m%d%H%M%S')
        result['session_id'] = session_id
        
        # 保存结果元数据
        output_dir = Path(generator.config['workspace']['output'])
        meta_file = output_dir / f"meta_{session_id}.json"
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<session_id>')
def download_all(session_id):
    """下载所有文件"""
    try:
        output_dir = Path('./workspace/output')
        
        # 创建临时 ZIP
        zip_path = output_dir / f"lecture_{session_id}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 查找并添加所有相关文件
            for file in output_dir.glob(f"*{session_id}*"):
                if file.suffix != '.zip':
                    zipf.write(file, file.name)
            
            # 添加最新的讲义
            lecture_files = sorted(output_dir.glob("*讲义.md"), key=lambda x: x.stat().st_mtime, reverse=True)
            if lecture_files:
                zipf.write(lecture_files[0], lecture_files[0].name)
        
        return send_file(zip_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/workspace/output/<path:filename>')
def serve_output(filename):
    """提供输出文件"""
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
