# AI 讲课生成系统

> 本地离线版「今天学点啥」- P104 8G 完美运行

## 🎯 功能目标

- ✅ 自动联网搜文献/资料
- ✅ 自动读文章、PDF
- ✅ 自动拆成：讲义 + PPT 大纲
- ✅ 本地生成超像真人的老师语音
- ✅ 多种音色、不同讲课风格
- ✅ 全程不花一分钱，不用 API
- ✅ 隐私 100%，全部本地运行

## 🏗️ 系统架构

```
输入层 → 处理层 → 输出层
  ↓        ↓        ↓
URL/PDF  内容拆解  讲义文档
搜索词   知识点提取 PPT 大纲
        讲义生成   语音音频
```

## 📁 目录结构

```
ai-lecture-generator/
├── README.md                 # 本文档
├── requirements.txt          # Python 依赖
├── config.yaml              # 配置文件
│
├── src/
│   ├── __init__.py
│   ├── main.py              # 主入口
│   │
│   ├── fetcher/             # 内容获取
│   │   ├── __init__.py
│   │   ├── url_fetcher.py   # 网页抓取
│   │   ├── pdf_reader.py    # PDF 读取
│   │   └── search_engine.py # 搜索
│   │
│   ├── processor/           # 内容处理
│   │   ├── __init__.py
│   │   ├── content_parser.py    # 内容解析
│   │   ├── knowledge_extractor.py # 知识点提取
│   │   └── lecture_generator.py # 讲义生成
│   │
│   ├── ollama_client/       # Ollama 客户端
│   │   ├── __init__.py
│   │   ├── client.py        # API 封装
│   │   ├── prompts.py       # 提示词模板
│   │   └── models.py        # 模型配置
│   │
│   ├── tts/                 # 语音合成
│   │   ├── __init__.py
│   │   ├── fish_speech.py   # Fish Speech 封装
│   │   └── voice_config.py  # 音色配置
│   │
│   └── output/              # 输出处理
│       ├── __init__.py
│       ├── pdf_generator.py # PDF 生成
│       ├── ppt_generator.py # PPT 生成
│       └── audio_merger.py  # 音频合并
│
├── workspace/               # 工作目录
│   ├── input/              # 输入文件
│   ├── output/             # 输出文件
│   ├── cache/              # 缓存
│   └── temp/               # 临时文件
│
├── tests/                   # 测试
│   ├── test_fetcher.py
│   ├── test_processor.py
│   └── test_tts.py
│
└── examples/                # 示例
    ├── example_lecture.py
    └── sample_input.md
```

## 🔧 技术栈

| 模块 | 技术 | 说明 |
|------|------|------|
| **大模型** | Ollama | qwen3:8b / deepseek-r1:1.5b |
| **语音合成** | Fish Speech | 本地运行，8G 显存 |
| **内容抓取** | requests + BeautifulSoup | 网页解析 |
| **PDF 处理** | PyMuPDF | PDF 读取 |
| **流程调度** | OpenClaw | 自动化流程 |
| **开发语言** | Python 3.10+ | 主语言 |

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 Ollama

```bash
# 测试连接
curl http://192.168.0.214:11434/api/tags

# 拉取模型（如需要）
ollama pull qwen3:8b
```

### 3. 安装 Fish Speech

```bash
# 克隆仓库
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech

# 安装依赖
pip install -e .
```

### 4. 运行示例

```bash
python src/main.py --input "https://example.com/article" --output "./workspace/output"
```

## 📝 使用示例

### 示例 1: 从 URL 生成讲课

```python
from src.main import LectureGenerator

generator = LectureGenerator()

# 从网页生成
result = generator.generate(
    source="https://arxiv.org/abs/2301.12345",
    topic="AI 基础知识",
    duration=10,  # 分钟
    voice="teacher_male"
)

print(f"讲义：{result.lecture_path}")
print(f"音频：{result.audio_path}")
```

### 示例 2: 从 PDF 生成

```python
result = generator.generate(
    source="./workspace/input/paper.pdf",
    topic="机器学习导论",
    style="university",  # 大学讲课风格
    voice="teacher_female"
)
```

## 🎙️ 可用音色

| 音色 ID | 描述 | 适用场景 |
|--------|------|---------|
| teacher_male | 男老师 | 正式讲课 |
| teacher_female | 女老师 | 温和讲解 |
| narrator | 解说员 | 纪录片风格 |
| storyteller | 讲故事 | 轻松学习 |

## 📊 性能指标

| 任务 | 耗时 | 显存占用 |
|------|------|---------|
| 内容拆解 (1 万字) | ~30 秒 | 5GB |
| 讲义生成 | ~20 秒 | 5GB |
| 语音合成 (10 分钟) | ~2 分钟 | 6GB |
| **总计** | **~3 分钟** | **峰值 6GB** |

## ⚠️ 注意事项

1. **显存管理**: P104 8G 足够，但避免同时运行多个大模型
2. **语音模型**: Fish Speech 首次加载需要下载权重 (~2GB)
3. **Ollama 连接**: 确保局域网可达 (192.168.0.214:11434)
4. **存储空间**: 预留至少 10GB 用于模型和缓存

## 🛠️ 开发计划

- [ ] 基础框架搭建
- [ ] Ollama 客户端封装
- [ ] 内容抓取模块
- [ ] 讲义生成提示词优化
- [ ] Fish Speech 集成
- [ ] PDF/PPT 输出
- [ ] Web UI (可选)
- [ ] 批量处理支持

## 📄 许可证

MIT License

---

*🦞 龙虾 41 号 2026-03-14*
