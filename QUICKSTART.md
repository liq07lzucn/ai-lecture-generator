# 🚀 快速启动指南

> AI 讲课生成系统 - 本地离线版「今天学点啥」

## ✅ 当前状态

| 模块 | 状态 | 说明 |
|------|------|------|
| **核心功能** | ✅ 完成 | 文本→讲义→PPT→测试题 |
| **Ollama 集成** | ✅ 完成 | 已连接测试 |
| **内容获取** | ✅ 完成 | URL/PDF/文本 |
| **知识提取** | ✅ 完成 | AI+ 规则双模式 |
| **讲义生成** | ✅ 完成 | 支持多种风格 |
| **PPT 大纲** | ✅ 完成 | JSON 格式输出 |
| **测试题** | ✅ 完成 | 自动生成 |
| **语音合成** | ⏳ 待安装 | Fish Speech |

## 📦 安装

### 1. 基础依赖

```bash
cd /data/projects/work/ai-lecture-generator

# 创建虚拟环境 (可选)
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 检查 Ollama

```bash
# 测试连接
curl http://192.168.0.214:11434/api/tags

# 应返回模型列表
```

### 3. 安装 Fish Speech (可选)

```bash
# Docker 方式 (推荐)
docker run --gpus all -p 8080:8000 fishaudio/fish-speech:latest

# 或本地安装
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech
pip install -e .
```

## 🎯 快速使用

### 方式 1: 命令行

```bash
# 从文本生成
python3 src/main.py -s "人工智能是计算机科学的一个分支..." -t "AI 基础" -d 10

# 从 URL 生成
python3 src/main.py -s "https://zh.wikipedia.org/wiki/人工智能" -t "AI 入门"

# 从 PDF 生成
python3 src/main.py -s "./workspace/input/paper.pdf" -t "论文讲解" -d 15
```

### 方式 2: Python 代码

```python
from src.main import LectureGenerator

generator = LectureGenerator()

result = generator.generate(
    source="人工智能是计算机科学的一个分支...",
    topic="AI 基础入门",
    duration=10,
    style="通俗易懂"
)

print(f"讲义：{result['lecture_path']}")
print(f"PPT: {result['ppt_path']}")
```

### 方式 3: 运行示例

```bash
python3 examples/example_basic.py
```

## 📊 输出示例

### 讲义 (Markdown)

```markdown
【开场白】（1 分 30 秒）
各位同学好！今天我们要聊一个超酷的话题——人工智能！...

【知识点讲解】（3 分 30 秒）
1. 人工智能的定义（1 分钟）
人工智能，简单说就是让机器像人一样"思考"...

【互动环节】（2 分钟）
现在，我来考考大家！
问题 1：以下哪个例子属于符号主义阶段？...

【总结回顾】（1 分 30 秒）
今天我们用 5 分钟，穿越了 AI 的三个发展阶段...
```

### PPT 大纲 (JSON)

```json
{
  "title": "人工智能基础",
  "slides": [
    {
      "page": 1,
      "title": "封面",
      "points": ["人工智能基础", "主讲人：AI 讲师"],
      "notes": "开场白"
    },
    ...
  ]
}
```

### 测试题 (JSON)

```json
[
  {
    "type": "选择题",
    "question": "以下哪个例子属于符号主义阶段？",
    "answer": "C. 早期的下棋程序",
    "explanation": "符号主义依赖逻辑规则..."
  },
  ...
]
```

## ⚙️ 配置

编辑 `config.yaml`:

```yaml
ollama:
  host: "http://192.168.0.214:11434"
  models:
    chat: "qwen3:latest"      # 主力模型
    summary: "deepseek-r1:1.5b"  # 轻量模型

tts:
  provider: "fish_speech"
  voices:
    teacher_male:
      speaker_id: "中文男老师"
```

## 📁 目录结构

```
ai-lecture-generator/
├── src/
│   ├── main.py              # 主入口
│   ├── ollama_client/       # Ollama 客户端
│   ├── fetcher/             # 内容获取
│   ├── processor/           # 内容处理
│   └── tts/                 # 语音合成
├── workspace/
│   ├── input/               # 输入文件
│   └── output/              # 输出文件
├── examples/                # 使用示例
├── config.yaml              # 配置
└── requirements.txt         # 依赖
```

## 🧪 测试

```bash
# 运行示例
python3 examples/example_basic.py

# 测试 Ollama
python3 src/ollama_client/client.py

# 测试内容抓取
python3 src/fetcher/url_fetcher.py
```

## 📈 性能

| 任务 | 耗时 | 说明 |
|------|------|------|
| 内容解析 | <1 秒 | 300-5000 字 |
| 知识点提取 | ~60 秒 | 5 个知识点 |
| 讲义生成 | ~40 秒 | 1000-2000 字 |
| PPT 大纲 | ~40 秒 | 10-15 页 |
| 测试题 | ~30 秒 | 3 个问题 |
| **总计** | **~3 分钟** | 完整流程 |

## ⚠️ 注意事项

1. **Ollama 连接**: 确保 192.168.0.214:11434 可达
2. **模型名称**: 使用 `qwen3:latest` 而非 `qwen3:8b`
3. **存储空间**: 预留 1GB 用于输出文件
4. **PDF 支持**: 需要安装 PyMuPDF (`pip install PyMuPDF`)

## 🛠️ 下一步

- [ ] 安装 Fish Speech 语音合成
- [ ] 完善 URL 抓取 (反爬处理)
- [ ] 添加更多提示词模板
- [ ] Web UI 界面
- [ ] 批量处理支持

---

🦞 龙虾 41 号 2026-03-14
