# 端侧AI Demo

这是一个简单易用的端侧AI对话Demo，支持通过配置文件自定义AI服务地址和密钥。

## 📁 项目结构

```
/workspace/
├── config.py      # 配置文件（配置 URL 和 Key）
├── ai_demo.py     # 主程序
└── README.md      # 说明文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置 API 信息

编辑 `config.py` 文件，填入您的 AI 服务配置：

```python
# AI 服务 API 地址
url = "https://api.example.com/v1/chat/completions"

# API 访问密钥
key = "your-api-key-here"

# 模型名称（可选）
model = "gpt-3.5-turbo"
```

### 3. 运行程序

```bash
python ai_demo.py
```

## ✨ 功能特点

- **可配置化**: 通过 `config.py` 轻松配置 API 地址、密钥、模型等参数
- **多轮对话**: 自动保存对话历史，支持上下文理解
- **重试机制**: 网络异常时自动重试，提高稳定性
- **友好提示**: 丰富的 emoji 表情和清晰的错误提示
- **命令支持**: 
  - 输入 `clear` 清空对话历史
  - 输入 `quit` 或 `exit` 退出程序

## 📝 使用说明

1. 启动程序后，直接在提示符后输入您的问题
2. AI 会返回回答并保存对话历史
3. 如需开始新话题，可输入 `clear` 清空历史
4. 输入 `quit` 或 `exit` 退出程序

## ⚙️ 配置参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| url | AI 服务 API 地址 | - |
| key | API 访问密钥 | - |
| model | 使用的模型名称 | gpt-3.5-turbo |
| timeout | 请求超时时间（秒） | 30 |
| max_retries | 最大重试次数 | 3 |

## 🔧 示例配置

### OpenAI 配置示例
```python
url = "https://api.openai.com/v1/chat/completions"
key = "sk-your-openai-api-key"
model = "gpt-3.5-turbo"
```

### 其他兼容 OpenAI 格式的 API
```python
url = "https://your-custom-api.com/v1/chat/completions"
key = "your-custom-api-key"
model = "custom-model-name"
```

## 📄 License

MIT License
