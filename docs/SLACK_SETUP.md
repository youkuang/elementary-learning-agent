# Slack 配置指南

## 1. 创建 Slack Workspace

1. 访问 https://slack.com/create
2. 输入邮箱创建新的 Workspace
3. 命名为 "家庭学习助手" 或其他名称

## 2. 创建频道

在 Workspace 中创建以下频道:

- `#语文-学习` - 语文 Agent 工作频道
- `#数学-学习` - 数学 Agent 工作频道
- `#英语-学习` - 英语 Agent 工作频道
- `#学习-总览` - 协调器 Agent 发送每日计划
- `#学习-报告` - 协调器 Agent 发送每周报告

## 3. 创建 Slack App

1. 访问 https://api.slack.com/apps
2. 点击 "Create New App"
3. 选择 "From scratch"
4. 输入 App 名称: "学习助手"
5. 选择你的 Workspace

## 4. 配置 Bot Token Scopes

在 "OAuth & Permissions" 页面,添加以下 Bot Token Scopes:

- `channels:history` - 读取频道消息
- `channels:read` - 查看频道信息
- `chat:write` - 发送消息
- `im:history` - 读取私信
- `im:read` - 查看私信
- `im:write` - 发送私信
- `users:read` - 读取用户信息

## 5. 安装 App 到 Workspace

1. 在 "OAuth & Permissions" 页面
2. 点击 "Install to Workspace"
3. 授权

## 6. 获取 Token

安装后会显示:
- **Bot User OAuth Token**: 以 `xoxb-` 开头
- 复制这个 Token 到 `.env` 文件的 `SLACK_BOT_TOKEN`

## 7. 启用 Socket Mode (可选)

如果需要实时交互:

1. 进入 "Socket Mode" 页面
2. 启用 Socket Mode
3. 生成 App-Level Token
4. 复制 Token (以 `xapp-` 开头) 到 `.env` 文件的 `SLACK_APP_TOKEN`

## 8. 邀请 Bot 到频道

在每个频道中:
1. 输入 `/invite @学习助手`
2. Bot 会加入频道

## 9. 测试

在 `#语文-学习` 频道发送:
```
新任务:测试任务
```

如果 Bot 回复,说明配置成功!

## 故障排查

### Bot 不回复

1. 检查 Token 是否正确
2. 检查 Bot 是否在频道中
3. 检查 Scopes 是否配置完整
4. 查看日志文件 `logs/app.log`

### 权限错误

确保添加了所有必需的 Bot Token Scopes

### 连接问题

检查网络连接和防火墙设置
