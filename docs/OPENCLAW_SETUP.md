# OpenClaw 安装和启动指南

## 📦 安装 OpenClaw

### 方法 1: 从 GitHub 安装 (推荐)

```bash
# 克隆 OpenClaw 仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 安装
pip install -e .
```

### 方法 2: 使用 pip (如果已发布)

```bash
pip install openclaw
```

## ⚙️ 配置

### 1. 环境变量

确保 `.env` 文件已配置:

```bash
# Slack
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token

# AI
ANTHROPIC_API_KEY=sk-ant-your-key
AI_MODEL=claude-3-5-sonnet-20241022

# Database
DATABASE_TYPE=sqlite
DATABASE_PATH=./data/learning.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Scheduler
ENABLE_SCHEDULER=true
TIMEZONE=Asia/Shanghai
```

### 2. 初始化数据库

```bash
python scripts/init_db.py
```

## 🚀 启动系统

### 使用 OpenClaw CLI

```bash
# 启动 OpenClaw
openclaw start --config openclaw_config.yaml

# 或者使用简写
openclaw start
```

### 使用 Python

```bash
python main.py
```

## 📋 验证安装

### 1. 检查 OpenClaw 版本

```bash
openclaw --version
```

### 2. 测试 Slack 连接

在 Slack 的 `#语文-学习` 频道发送:

```
你好
```

如果 Agent 回复,说明配置成功!

## 🐛 故障排查

### OpenClaw 未安装

**错误**: `command not found: openclaw`

**解决**:
```bash
pip install openclaw
# 或从源码安装
```

### Slack 连接失败

**错误**: `Permission denied` 或 `Invalid token`

**解决**:
1. 检查 `.env` 中的 Token 是否正确
2. 确认 Slack App 已安装到 Workspace
3. 确认 Bot 已加入频道

### Agent 不响应

**检查**:
1. 查看日志: `tail -f logs/app.log`
2. 确认 Agent 配置文件路径正确
3. 确认 Skills 路径正确

### 数据库错误

**解决**:
```bash
# 重新初始化数据库
rm data/learning.db
python scripts/init_db.py
```

## 📚 更多资源

- [OpenClaw 官方文档](https://github.com/openclaw/openclaw)
- [Slack API 文档](https://api.slack.com/)
- [项目 README](README.md)
- [Slack 配置指南](docs/SLACK_SETUP.md)

## 💡 开发模式

开发时可以启用调试模式:

```bash
# 设置日志级别为 DEBUG
export LOG_LEVEL=DEBUG

# 启动
openclaw start --config openclaw_config.yaml --debug
```

## 🔄 重启系统

```bash
# 停止 (Ctrl+C)
# 然后重新启动
openclaw start
```

## 📊 监控

查看实时日志:

```bash
tail -f logs/app.log
```

查看数据库:

```bash
sqlite3 data/learning.db
.tables
.schema tasks
```
