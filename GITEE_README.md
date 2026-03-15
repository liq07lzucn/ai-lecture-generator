# 🎯 AI 讲课生成系统

> 一键生成完整讲课内容：讲义 + PPT + 测试题 + 语音

## ✨ 功能特点

- 📥 **多种输入**: 支持文本、URL、PDF
- 🧠 **AI 分析**: 自动提取知识点
- 📚 **讲义生成**: 5 种风格（通俗/故事/儿童/专业）
- 📊 **PPT 大纲**: 自动生成 12-18 页幻灯片
- ❓ **测试题**: 混合题型（选择/判断/简答）
- 🔊 **语音合成**: Edge TTS，8 种中文音色
- 📜 **历史记录**: 查看所有生成的课程
- 💾 **一键下载**: 打包下载所有文件

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 Web 服务

```bash
./start.sh
```

### 3. 访问界面

打开浏览器访问：`http://localhost:5000`

## 📝 使用示例

### 命令行使用

```bash
python3 src/main.py -s "人工智能是..." -t "AI 基础" -d 10
```

### Python 代码

```python
from src.main import LectureGenerator

generator = LectureGenerator()
result = generator.generate(
    source="你的内容",
    topic="AI 基础",
    duration=10
)
```

## 🛠️ 技术栈

- **后端**: Python 3.10+, Flask
- **大模型**: Ollama (qwen3:8b, deepseek-r1:1.5b)
- **语音**: Edge TTS (免费)
- **PDF**: PyMuPDF
- **网页抓取**: BeautifulSoup

## 📁 项目结构

```
ai-lecture-generator/
├── src/                    # 源代码
│   ├── main.py            # 主入口
│   ├── ollama_client/     # Ollama 客户端
│   ├── fetcher/           # 内容获取
│   ├── processor/         # 内容处理
│   └── tts/               # 语音合成
├── examples/               # 使用示例
├── workspace/              # 工作目录
├── config.yaml             # 配置
├── requirements.txt        # 依赖
├── start.sh                # 启动脚本
└── web_simple.py           # Web 服务
```

## 📊 性能指标

| 任务 | 耗时 |
|------|------|
| 知识点提取 | ~60 秒 |
| 讲义生成 | ~40 秒 |
| PPT 大纲 | ~40 秒 |
| 语音合成 | ~60 秒 |
| **总计** | **~3-4 分钟** |

## 🎨 支持的讲义风格

1. **通俗易懂** - 适合大学生
2. **故事化** - 罗辑思维风格
3. **儿童版** - 芝麻街风格
4. **专业版** - TED 演讲风格

## 📄 许可证

MIT License

---

🦞 龙虾 41 号 | 2026-03-15
