# AI 讲课生成系统

> 🎯 本地离线版「今天学点啥」- 一键生成讲义 + PPT + 测试题

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行示例
python3 examples/example_basic.py

# 3. 命令行使用
python3 src/main.py -s "人工智能是..." -t "AI 基础" -d 10
```

## ✨ 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 📥 内容获取 | ✅ | URL/PDF/文本 |
| 🧠 知识点提取 | ✅ | AI 智能分析 |
| 📚 讲义生成 | ✅ | 多种风格 |
| 📊 PPT 大纲 | ✅ | JSON 格式 |
| ❓ 测试题 | ✅ | 自动出题 |
| 🔊 语音合成 | ⏳ | 待集成 |

## 📁 项目结构

```
ai-lecture-generator/
├── src/                      # 源代码
│   ├── main.py              # 主入口
│   ├── ollama_client/       # Ollama 客户端
│   ├── fetcher/             # 内容获取
│   ├── processor/           # 内容处理
│   └── tts/                 # 语音合成
├── examples/                 # 使用示例
├── workspace/                # 工作目录
│   ├── input/               # 输入文件
│   └── output/              # 输出文件
├── config.yaml               # 配置文件
└── requirements.txt          # 依赖
```

## 🎯 使用示例

### 从文本生成

```python
from src.main import LectureGenerator

generator = LectureGenerator()

result = generator.generate(
    source="人工智能是计算机科学的一个分支...",
    topic="AI 基础入门",
    duration=10
)

print(f"讲义：{result['lecture_path']}")
print(f"PPT: {result['ppt_path']}")
print(f"测试题：{result['questions_path']}")
```

### 命令行

```bash
# 从文本
python3 src/main.py -s "人工智能是..." -t "AI 基础" -d 10

# 从 URL
python3 src/main.py -s "https://zh.wikipedia.org/wiki/人工智能" -t "AI 入门"

# 从 PDF
python3 src/main.py -s "./paper.pdf" -t "论文讲解" -d 15
```

## 🎨 支持的讲义风格

- ✅ 通俗易懂（大学生）
- ✅ 故事化（罗辑思维风格）
- ✅ 辩论式（启发式教学）
- ✅ 儿童版（芝麻街风格）
- ✅ 专业版（TED 演讲风格）

## 📊 输出示例

### 讲义（Markdown）

```markdown
【开场白】（1 分 30 秒）
各位同学好！今天我们要聊一个超酷的话题——人工智能！...

【知识点讲解】（3 分 30 秒）
1. 人工智能的定义（1 分钟）
2. 人工智能的三个阶段（2 分 30 秒）

【互动环节】（2 分钟）
问题 1：以下哪个例子属于符号主义阶段？...

【总结回顾】（1 分 30 秒）
今天我们用 5 分钟，穿越了 AI 的三个发展阶段...
```

### PPT 大纲（JSON）

```json
{
  "title": "人工智能基础",
  "slides": [
    {"page": 1, "title": "封面", "points": [...]},
    {"page": 2, "title": "目录", "points": [...]},
    ...
  ]
}
```

### 测试题（JSON）

```json
[
  {
    "type": "single_choice",
    "question": "以下哪个例子属于符号主义阶段？",
    "options": ["A. ...", "B. ..."],
    "answer": "C"
  },
  ...
]
```

## ⚙️ 配置

编辑 `config.yaml`:

```yaml
ollama:
  host: "http://192.168.0.214:11434"
  timeout: 120
  models:
    chat: "qwen3:latest"
    summary: "deepseek-r1:1.5b"

workspace:
  root: "./workspace"
  output: "./workspace/output"
```

## 🧪 测试

```bash
# 运行示例
python3 examples/example_basic.py

# 测试 Ollama 连接
python3 src/ollama_client/client.py

# 测试提示词模板
python3 src/ollama_client/prompts.py
```

## 📈 性能指标

| 任务 | 耗时 |
|------|------|
| 内容解析 | <1 秒 |
| 知识点提取 | ~60 秒 |
| 讲义生成 | ~40 秒 |
| PPT 大纲 | ~40 秒 |
| 测试题 | ~30 秒 |
| **总计** | **~3 分钟** |

## 🛠️ 技术栈

- **大模型**: Ollama (qwen3:8b, deepseek-r1:1.5b)
- **内容抓取**: requests + BeautifulSoup
- **PDF 处理**: PyMuPDF
- **流程调度**: Python 原生
- **开发语言**: Python 3.10+

## 📝 开发计划

- [x] 基础框架搭建
- [x] Ollama 客户端封装
- [x] 内容抓取模块
- [x] 讲义生成提示词优化
- [x] PPT 大纲生成
- [x] 测试题生成
- [ ] 语音合成 (Fish Speech / Edge TTS)
- [ ] Web UI 界面
- [ ] 批量处理支持

## 📄 许可证

MIT License

---

🦞 龙虾 41 号 2026-03-14
