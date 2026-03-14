# 🚀 快速启动指南

## 1. 项目结构已完成 ✅

```
ai-lecture-generator/
├── README.md              # 项目说明
├── config.yaml           # 配置文件
├── requirements.txt      # 依赖包
├── src/
│   ├── main.py          # 主入口
│   ├── ollama_client/   # Ollama 客户端 ✅
│   ├── tts/             # 语音合成 (待安装 Fish Speech)
│   ├── fetcher/         # 内容抓取 (待实现)
│   └── processor/       # 内容处理 (待实现)
└── workspace/           # 工作目录
```

## 2. 当前状态

| 模块 | 状态 | 说明 |
|------|------|------|
| Ollama 连接 | ✅ 完成 | 已连接 192.168.0.214:11434 |
| 可用模型 | ✅ 4 个 | qwen3:8b, deepseek-r1:1.5b 等 |
| 基础框架 | ✅ 完成 | 主入口、配置、日志 |
| 提示词模板 | ✅ 完成 | 讲义生成、PPT 大纲等 |
| Fish Speech | ⏳ 待安装 | 需要单独安装 |
| 内容抓取 | ⏳ 待实现 | URL/PDF 解析 |
| 语音合成 | ⏳ 待实现 | 集成 Fish Speech |

## 3. 下一步操作

### 方案 A: 先测试 Ollama (推荐)

```bash
cd /data/projects/work/ai-lecture-generator

# 测试 Ollama 对话
python3 -c "
from src.ollama_client import OllamaClient
client = OllamaClient()
response = client.generate('qwen3:8b', '用 100 字介绍人工智能')
print(response)
"
```

### 方案 B: 安装 Fish Speech

```bash
# 方法 1: 本地安装 (需要 CUDA)
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech
pip install -e .

# 方法 2: Docker (推荐)
docker run --gpus all -p 8080:8000 fishaudio/fish-speech:latest
```

### 方案 C: 完善内容抓取

实现 `src/fetcher/` 模块:
- URL 抓取 (BeautifulSoup)
- PDF 读取 (PyMuPDF)

## 4. 测试命令

```bash
# 测试基础功能
python3 src/main.py

# 检查配置
python3 -c "import yaml; print(yaml.safe_load(open('config.yaml')))"

# 查看日志
tail -f logs/lecture_generator.log
```

## 5. 预期效果

输入:
```python
generator.generate(
    source="https://example.com/ai-article",
    topic="AI 基础入门",
    duration=10
)
```

输出:
- `workspace/output/AI 基础入门_lecture.md` - 讲课稿
- `workspace/output/ppt_outline.json` - PPT 大纲
- `workspace/output/audio.mp3` - 语音 (待实现)

---

🦞 龙虾 41号 2026-03-14
