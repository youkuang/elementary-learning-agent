# Docker 部署指南

## 🐳 快速开始

### 前提条件

- Docker 已安装
- Docker Compose 已安装

### 1. 克隆项目

```bash
git clone https://github.com/youkuang/elementary-learning-agent.git
cd elementary-learning-agent
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

必须配置的变量:
```bash
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
ANTHROPIC_API_KEY=sk-ant-your-key
```

### 3. 构建和启动

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 4. 验证运行

```bash
# 检查容器状态
docker-compose ps

# 查看实时日志
docker-compose logs -f learning-agent
```

在 Slack 的 `#语文-学习` 频道发送消息测试。

---

## 📋 常用命令

### 启动和停止

```bash
# 启动
docker-compose up -d

# 停止
docker-compose stop

# 重启
docker-compose restart

# 停止并删除容器
docker-compose down
```

### 查看日志

```bash
# 查看所有日志
docker-compose logs

# 实时查看日志
docker-compose logs -f

# 查看最近100行
docker-compose logs --tail=100
```

### 进入容器

```bash
# 进入容器 shell
docker-compose exec learning-agent bash

# 运行 Python 命令
docker-compose exec learning-agent python scripts/init_db.py
```

### 更新代码

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

---

## 🗄️ 数据持久化

数据存储在宿主机的以下目录:

```
./data/     # 数据库文件
./logs/     # 日志文件
```

即使删除容器,这些数据也会保留。

---

## 🔧 高级配置

### 使用 PostgreSQL

如果需要使用 PostgreSQL 而不是 SQLite:

1. 编辑 `docker-compose.yml`,取消注释 PostgreSQL 部分
2. 修改 `.env`:
   ```bash
   DATABASE_TYPE=postgresql
   DATABASE_HOST=postgres
   DATABASE_PORT=5432
   DATABASE_NAME=learning_agent
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your-password
   ```
3. 重新启动:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### 自定义端口

如果需要暴露 Web 端口:

编辑 `docker-compose.yml`:
```yaml
services:
  learning-agent:
    ports:
      - "8000:8000"
```

### 资源限制

限制容器资源使用:

编辑 `docker-compose.yml`:
```yaml
services:
  learning-agent:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## 🐛 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker-compose logs learning-agent

# 检查配置
docker-compose config
```

### 数据库初始化失败

```bash
# 手动初始化
docker-compose exec learning-agent python scripts/init_db.py
```

### Slack 连接失败

1. 检查 `.env` 中的 Token 是否正确
2. 确认网络连接正常
3. 查看日志:
   ```bash
   docker-compose logs -f learning-agent | grep -i slack
   ```

### 重置所有数据

```bash
# 停止并删除容器和数据
docker-compose down -v

# 删除数据目录
rm -rf data/* logs/*

# 重新启动
docker-compose up -d
```

---

## 📊 监控

### 查看资源使用

```bash
# 查看容器资源使用
docker stats elementary-learning-agent
```

### 健康检查

```bash
# 查看健康状态
docker inspect --format='{{.State.Health.Status}}' elementary-learning-agent
```

---

## 🚀 生产部署建议

### 1. 使用环境变量文件

不要将 `.env` 提交到 Git,使用密钥管理服务。

### 2. 配置日志轮转

编辑 `docker-compose.yml`:
```yaml
services:
  learning-agent:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 3. 使用外部数据库

生产环境建议使用 PostgreSQL 或云数据库。

### 4. 配置自动重启

```yaml
services:
  learning-agent:
    restart: always
```

### 5. 备份数据

```bash
# 备份数据库
docker-compose exec learning-agent sqlite3 data/learning.db .dump > backup.sql

# 恢复
cat backup.sql | docker-compose exec -T learning-agent sqlite3 data/learning.db
```

---

## 🔄 更新和维护

### 更新到最新版本

```bash
# 拉取最新代码
git pull

# 重新构建
docker-compose build --no-cache

# 重启服务
docker-compose up -d
```

### 清理旧镜像

```bash
# 删除未使用的镜像
docker image prune -a
```

---

## 📚 更多资源

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [项目 README](../README.md)
