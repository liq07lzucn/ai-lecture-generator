#!/bin/bash
# AI 讲课生成器 - 快速启动脚本

echo "🦞 AI 讲课生成器 - 启动中..."
echo ""

cd /data/projects/work/ai-lecture-generator

# 检查依赖
echo "检查依赖..."
python3 -c "import flask" 2>/dev/null || {
    echo "安装 Flask..."
    pip3 install flask --break-system-packages -q
}

python3 -c "import edge_tts" 2>/dev/null || {
    echo "安装 Edge TTS..."
    pip3 install edge-tts --break-system-packages -q
}

echo ""
echo "✅ 依赖检查完成"
echo ""
echo "启动 Web 服务..."
echo ""

python3 web_server.py
