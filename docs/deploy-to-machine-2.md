# 🖥️ BZT-IC 部署到 2号机指南

## 2号机信息

- **IP**: 192.168.1.218
- **用户**: caidengyong
- **系统**: macOS 26.0.1 (arm64)
- **已安装**: Node.js v24.13.1, OpenClaw

---

## 🎯 部署方案选择

### 方案一：Docker 部署（推荐）⭐⭐⭐⭐⭐
**优点**：
- 环境隔离，不影响现有服务
- 一键启动/停止
- 易于维护和更新

**缺点**：
- 需要安装 Docker Desktop（约 2GB）
- 占用资源稍多

**适合场景**：长期运行，生产环境

---

### 方案二：直接运行（轻量）⭐⭐⭐⭐
**优点**：
- 不需要 Docker
- 资源占用少
- 启动快

**缺点**：
- 需要手动管理进程
- 环境可能冲突

**适合场景**：开发测试，资源紧张

---

## 🚀 方案一：Docker 部署（推荐）

### 第一步：安装 Docker Desktop（15分钟）

在 2号机上执行：

```bash
# 方法1：使用 Homebrew（推荐）
brew install --cask docker

# 方法2：手动下载
# 访问 https://www.docker.com/products/docker-desktop
# 下载 Apple Silicon 版本
```

安装后：
1. 打开 Docker Desktop
2. 等待启动完成（右上角小鲸鱼图标变绿）
3. 验证安装：
```bash
docker --version
docker-compose --version
```

### 第二步：传输代码到 2号机（5分钟）

**方法1：使用 rsync（推荐）**
```bash
# 在你的主电脑上执行
rsync -avz /Users/caidengyong/Desktop/steven/bzt-ic \
  caidengyong@192.168.1.218:~/projects/
```

**方法2：使用 Git**
```bash
# 在 2号机上执行
cd ~
mkdir projects && cd projects
git clone https://github.com/your-org/bzt-ic.git
```

**方法3：使用 scp**
```bash
# 在你的主电脑上执行
scp -r /Users/caidengyong/Desktop/steven/bzt-ic \
  caidengyong@192.168.1.218:~/projects/
```

### 第三步：配置环境变量（5分钟）

在 2号机上执行：

```bash
cd ~/projects/bzt-ic

# 复制环境变量模板
cp .env.example .env

# 编辑配置
nano .env
```

修改以下内容：
```env
# 数据库配置（使用强密码！）
DB_ROOT_PASSWORD=ChangeMe123!@#
DB_NAME=bzt_ic
DB_USER=bzt_user
DB_PASSWORD=SecurePassword456!@#

# JWT 配置（至少 32 位）
JWT_SECRET=your_super_secret_jwt_key_at_least_32_chars_long_change_me
JWT_EXPIRES_IN=7d

# 其他配置
NODE_ENV=production
```

### 第四步：一键部署（10分钟）

在 2号机上执行：

```bash
cd ~/projects/bzt-ic

# 赋予执行权限
chmod +x deploy.sh

# 一键部署
./deploy.sh
```

部署脚本会：
1. ✅ 检查 Docker 环境
2. ✅ 构建 Docker 镜像
3. ✅ 启动数据库
4. ✅ 启动后端
5. ✅ 启动前端
6. ✅ 运行数据库迁移

### 第五步：验证部署（2分钟）

```bash
# 查看容器状态
docker-compose ps

# 应该看到 3 个容器都是 Up 状态：
# - bzt-ic-web
# - bzt-ic-api
# - bzt-ic-db

# 查看日志
docker-compose logs -f

# 测试访问
curl http://localhost:80
curl http://localhost:3000/health
```

### 第六步：设置开机自启动（可选）

```bash
# 创建 LaunchAgent
cat > ~/Library/LaunchAgents/com.bzt-ic.docker.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.bzt-ic.docker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/docker-compose</string>
        <string>up</string>
        <string>-d</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/Users/caidengyong/projects/bzt-ic</string>
</dict>
</plist>
EOF

# 加载服务
launchctl load ~/Library/LaunchAgents/com.bzt-ic.docker.plist
```

---

## 🎈 方案二：直接运行（轻量）

### 第一步：安装依赖（20分钟）

在 2号机上执行：

```bash
# 安装 MariaDB
brew install mariadb

# 启动 MariaDB 服务
brew services start mariadb

# 设置 root 密码
mysql_secure_installation

# 创建数据库和用户
mysql -u root -p
```

在 MySQL 中执行：
```sql
CREATE DATABASE bzt_ic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bzt_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON bzt_ic.* TO 'bzt_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 第二步：传输和配置代码（5分钟）

```bash
# 传输代码（参考方案一的第二步）
cd ~/projects/bzt-ic

# 配置环境变量
cp apps/api/.env.example apps/api/.env
nano apps/api/.env
```

编辑 `apps/api/.env`：
```env
DATABASE_URL="mysql://bzt_user:your_password@localhost:3306/bzt_ic"
JWT_SECRET="your_jwt_secret"
JWT_EXPIRES_IN="7d"
PORT=3000
```

### 第三步：安装项目依赖（10分钟）

```bash
# 后端
cd ~/projects/bzt-ic/apps/api
npm install
npx prisma generate
npx prisma migrate deploy

# 前端
cd ~/projects/bzt-ic/apps/web
npm install
npm run build
```

### 第四步：使用 PM2 管理进程（10分钟）

```bash
# 安装 PM2
npm install -g pm2

# 创建 PM2 配置
cd ~/projects/bzt-ic
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'bzt-ic-api',
      cwd: './apps/api',
      script: 'dist/main.js',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 3000
      }
    }
  ]
}
EOF

# 启动后端
pm2 start ecosystem.config.js

# 保存 PM2 配置
pm2 save

# 设置开机自启动
pm2 startup
```

### 第五步：配置 Nginx（10分钟）

```bash
# 安装 Nginx
brew install nginx

# 配置 Nginx
nano /opt/homebrew/etc/nginx/servers/bzt-ic.conf
```

粘贴以下内容：
```nginx
server {
    listen 80;
    server_name localhost;

    # 前端静态文件
    location / {
        root /Users/caidengyong/projects/bzt-ic/apps/web/dist;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api/ {
        proxy_pass http://localhost:3000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# 启动 Nginx
brew services start nginx

# 验证
curl http://localhost
```

---

## 🔧 常用命令

### Docker 方案

```bash
# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 更新代码
git pull
docker-compose build
docker-compose up -d
docker-compose exec backend npx prisma migrate deploy

# 数据库备份
docker-compose exec mariadb mysqldump -u bzt_user -p bzt_ic > backup_$(date +%Y%m%d).sql

# 数据库恢复
docker-compose exec -T mariadb mysql -u bzt_user -p bzt_ic < backup.sql
```

### 直接运行方案

```bash
# 查看 PM2 状态
pm2 status

# 查看日志
pm2 logs bzt-ic-api

# 重启服务
pm2 restart bzt-ic-api

# 停止服务
pm2 stop bzt-ic-api

# 更新代码
git pull
cd apps/api && npm install && npm run build && npx prisma migrate deploy
pm2 restart bzt-ic-api

cd ../web && npm install && npm run build
```

---

## 📊 资源占用对比

| 方案 | CPU | 内存 | 磁盘 | 优点 |
|------|-----|------|------|------|
| **Docker** | 5-10% | 1.5GB | 3GB | 隔离、易管理 |
| **直接运行** | 3-5% | 800MB | 1GB | 轻量、快速 |

---

## 🌐 局域网访问

部署完成后，局域网内其他设备可以通过以下地址访问：

```
前端：http://192.168.1.218
后端：http://192.168.1.218/api
```

如果需要外网访问，可以使用：
1. **内网穿透**：ngrok、frp
2. **端口映射**：路由器配置
3. **VPN**：Tailscale、ZeroTier

---

## 🚨 故障排查

### 问题1：Docker 启动失败

```bash
# 检查 Docker Desktop 是否运行
docker ps

# 重启 Docker Desktop
osascript -e 'quit app "Docker"'
open -a Docker
```

### 问题2：数据库连接失败

```bash
# 检查数据库状态
docker-compose ps mariadb

# 查看数据库日志
docker-compose logs mariadb

# 手动连接测试
docker-compose exec mariadb mysql -u bzt_user -p
```

### 问题3：前端访问 404

```bash
# 检查前端容器
docker-compose logs frontend

# 重新构建前端
docker-compose build frontend
docker-compose up -d frontend
```

---

## 💾 备份策略

### 自动备份脚本

```bash
cat > ~/projects/bzt-ic/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/backups/bzt-ic
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec -T mariadb mysqldump -u bzt_user -p${DB_PASSWORD} bzt_ic > $BACKUP_DIR/db_$DATE.sql

# 备份代码
tar -czf $BACKUP_DIR/code_$DATE.tar.gz --exclude='node_modules' --exclude='dist' ~/projects/bzt-ic

# 保留最近 7 天的备份
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

chmod +x ~/projects/bzt-ic/backup.sh
```

### 设置定时备份

```bash
# 每天凌晨 2 点自动备份
crontab -e

# 添加以下行
0 2 * * * /Users/caidengyong/projects/bzt-ic/backup.sh >> /Users/caidengyong/projects/bzt-ic/backup.log 2>&1
```

---

## 🎯 我的推荐

### 如果机器配置好（16GB+ 内存）
**选择 Docker 方案**：
- 环境隔离好
- 维护简单
- 一键启动

### 如果机器配置一般（8GB 内存）
**选择直接运行方案**：
- 资源占用少
- 性能更好

---

## ✅ 部署检查清单

### 部署前
- [ ] 2号机已开机且可以 SSH 连接
- [ ] Docker Desktop 已安装（方案一）
- [ ] MariaDB 已安装（方案二）
- [ ] 代码已传输到 2号机

### 部署中
- [ ] 环境变量已配置
- [ ] 依赖已安装
- [ ] 数据库已创建
- [ ] 迁移已运行

### 部署后
- [ ] 容器/进程正常运行
- [ ] 可以访问前端页面
- [ ] API 接口正常
- [ ] 数据库连接正常
- [ ] 局域网可以访问
- [ ] 开机自启动已配置
- [ ] 备份策略已设置

---

## 📞 需要帮助？

如果遇到问题，可以：
1. 查看日志：`docker-compose logs -f` 或 `pm2 logs`
2. 查看本文档的"故障排查"章节
3. 联系我协助解决

---

**准备好开始了吗？** 🚀

等 2号机开机后，告诉我你选择哪个方案，我可以一步步指导你完成部署！
