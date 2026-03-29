#!/bin/bash

# 直接运行方案部署到 2号机（IP: 192.168.1.96）- 完全自动化版本

set -e

MACHINE_2_IP="192.168.1.96"
MACHINE_2_USER="caidengyong"
PROJECT_NAME="bzt-ic"
LOCAL_DIR="/Users/caidengyong/Desktop/steven/bzt-ic"
REMOTE_DIR="~/projects/${PROJECT_NAME}"

echo "========================================="
echo "⚡ 直接运行方案部署到 2号机"
echo "========================================="
echo ""

# 第一步：检查本地项目
echo "📦 检查本地项目..."
if [ ! -d "${LOCAL_DIR}" ]; then
    echo "❌ 项目目录不存在：${LOCAL_DIR}"
    exit 1
fi
echo "✅ 本地项目存在"
echo ""

# 第二步：在 2号机上创建目录
echo "📁 在 2号机上创建项目目录..."
ssh ${MACHINE_2_USER}@${MACHINE_2_IP} "mkdir -p ~/projects"
echo "✅ 目录创建完成"
echo ""

# 第三步：传输代码到 2号机
echo "📤 传输代码到 2号机..."
echo "   （这可能需要几分钟，取决于代码大小）"

# 使用 rsync 传输（排除 node_modules）
rsync -avz --progress \
    --exclude 'node_modules' \
    --exclude 'dist' \
    --exclude '.git' \
    --exclude '.DS_Store' \
    --exclude 'coverage' \
    ${LOCAL_DIR}/ \
    ${MACHINE_2_USER}@${MACHINE_2_IP}:${REMOTE_DIR}/

echo "✅ 代码传输完成"
echo ""

# 第四步：在 2号机上安装依赖
echo "📦 在 2号机上安装系统依赖（MariaDB + PM2 + Nginx）..."
echo ""

ssh ${MACHINE_2_USER}@${MACHINE_2_IP} 'bash -s' << 'REMOTE_SCRIPT'
set -e

# ⚠️ 设置 PATH（重要！）
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

echo "========================================="
echo "📦 安装系统依赖"
echo "========================================="
echo ""

# 检查 brew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew 未找到"
    exit 1
fi

echo "✅ Homebrew 版本：$(brew --version)"

# 安装 MariaDB
if ! command -v mysql &> /dev/null; then
    echo "📦 安装 MariaDB..."
    brew install mariadb
    brew services start mariadb
    sleep 3
    echo "✅ MariaDB 安装完成"
else
    echo "✅ MariaDB 已安装"
    
    # 检查 MariaDB 是否运行
    if ! brew services list | grep mariadb | grep started &> /dev/null; then
        echo "⚠️  MariaDB 未运行，正在启动..."
        brew services start mariadb
        sleep 3
    fi
fi

# 安装 PM2
if ! command -v pm2 &> /dev/null; then
    echo "📦 安装 PM2..."
    npm install -g pm2
    echo "✅ PM2 安装完成"
else
    echo "✅ PM2 已安装"
fi

# 安装 Nginx
if ! command -v nginx &> /dev/null; then
    echo "📦 安装 Nginx..."
    brew install nginx
    echo "✅ Nginx 安装完成"
else
    echo "✅ Nginx 已安装"
fi

echo ""
echo "✅ 系统依赖安装完成"
echo ""

REMOTE_SCRIPT

echo ""

# 第五步：创建数据库和配置
echo "📊 创建数据库和配置..."
echo ""

ssh ${MACHINE_2_USER}@${MACHINE_2_IP} 'bash -s' << 'REMOTE_SCRIPT'
set -e

# ⚠️ 设置 PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

cd ~/projects/bzt-ic/apps/api

echo "========================================="
echo "📊 配置数据库"
echo "========================================="
echo ""

# 生成随机密码
DB_PASSWORD=$(openssl rand -base64 16 | tr -d '/+=' | cut -c1-20)
JWT_SECRET=$(openssl rand -base64 32)

# 创建数据库和用户（MariaDB 默认 root 无密码）
mysql -u root << SQL
CREATE DATABASE IF NOT EXISTS \`bzt_ic\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'bzt_user'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON \`bzt_ic\`.* TO 'bzt_user'@'localhost';
FLUSH PRIVILEGES;
SQL

if [ $? -eq 0 ]; then
    echo "✅ 数据库创建成功"
    echo ""
    echo "数据库用户名：bzt_user"
    echo "数据库密码：${DB_PASSWORD}"
    echo "数据库名：bzt_ic"
    echo ""
    
    # 创建 .env 文件
    cat > .env << ENVEOF
DATABASE_URL="mysql://bzt_user:${DB_PASSWORD}@localhost:3306/bzt_ic"
JWT_SECRET="${JWT_SECRET}"
JWT_EXPIRES_IN="7d"
PORT=3000
ENVEOF
    
    echo "✅ 配置文件已创建：.env"
else
    echo "❌ 数据库创建失败"
    exit 1
fi

REMOTE_SCRIPT

echo ""

# 第六步：安装项目依赖
echo "📦 安装项目依赖..."
echo ""

ssh ${MACHINE_2_USER}@${MACHINE_2_IP} 'bash -s' << 'REMOTE_SCRIPT'
set -e

# ⚠️ 设置 PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

cd ~/projects/bzt-ic

echo "========================================="
echo "📦 安装后端依赖"
echo "========================================="
echo ""

cd apps/api
npm install
npx prisma generate

echo ""
echo "========================================="
echo "📦 安装前端依赖"
echo "========================================="
echo ""

cd ../web
npm install

echo ""
echo "✅ 项目依赖安装完成"
echo ""

REMOTE_SCRIPT

echo ""

# 第七步：运行数据库迁移
echo "📊 运行数据库迁移..."
echo ""

ssh ${MACHINE_2_USER}@${MACHINE_2_IP} 'bash -s' << 'REMOTE_SCRIPT'
set -e

# ⚠️ 设置 PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

cd ~/projects/bzt-ic/apps/api
npx prisma migrate deploy
REMOTE_SCRIPT

echo "✅ 数据库迁移完成"
echo ""

# 第八步：构建项目
echo "🔨 构建项目..."
echo ""

ssh ${MACHINE_2_USER}@${MACHINE_2_IP} 'bash -s' << 'REMOTE_SCRIPT'
set -e

# ⚠️ 设置 PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

cd ~/projects/bzt-ic

echo "========================================="
echo "🔨 构建后端"
echo "========================================="
echo ""

cd apps/api
npm run build

echo ""
echo "========================================="
echo "🔨 构建前端"
echo "========================================="
echo ""

cd ../web
npm run build

echo ""
echo "✅ 构建完成"
echo ""

REMOTE_SCRIPT

echo ""

# 第九步：配置和启动服务
echo "🚀 配置和启动服务..."
echo ""

ssh ${MACHINE_2_USER}@${MACHINE_2_IP} 'bash -s' << 'REMOTE_SCRIPT'
set -e

# ⚠️ 设置 PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

cd ~/projects/bzt-ic

echo "========================================="
echo "🚀 配置 PM2"
echo "========================================="
echo ""

# 创建 PM2 配置
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
pm2 delete all 2>/dev/null || true
pm2 start ecosystem.config.js
pm2 save

echo ""
echo "✅ PM2 配置完成"
echo ""

echo "========================================="
echo "🚀 配置 Nginx"
echo "========================================="
echo ""

# 创建 Nginx 配置目录
mkdir -p /opt/homebrew/etc/nginx/servers

# 创建 Nginx 配置
cat > /opt/homebrew/etc/nginx/servers/bzt-ic.conf << 'NGINX'
server {
    listen 80;
    server_name localhost;

    # 前端静态文件
    location / {
        root /Users/caidengyong/projects/bzt-ic/apps/web/dist;
        try_files $uri $uri/ /index.html;
        
        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API 代理
    location /api/ {
        proxy_pass http://localhost:3000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
NGINX

# 重启 Nginx
brew services restart nginx 2>/dev/null || brew services start nginx

echo "✅ Nginx 配置完成"
echo ""

# 设置 PM2 开机自启动
echo "========================================="
echo "⚙️  设置开机自启动"
echo "========================================="
echo ""

pm2_startup_command=$(pm2 startup 2>&1 | grep -oE 'sudo.*' || true)
if [ -n "$pm2_startup_command" ]; then
    echo "⚠️  需要手动执行以下命令设置开机自启动："
    echo "$pm2_startup_command"
else
    echo "✅ PM2 开机自启动已配置"
fi

echo ""
echo "========================================="
echo "✅ 部署完成！"
echo "========================================="
echo ""

# 显示服务状态
pm2 status

echo ""
echo "📍 本地访问地址："
echo "   前端：http://localhost"
echo "   后端：http://localhost:3000"
echo ""
echo "📋 常用命令："
echo "   查看状态：pm2 status"
echo "   查看日志：pm2 logs bzt-ic-api"
echo "   重启服务：pm2 restart bzt-ic-api"
echo "   停止服务：pm2 stop bzt-ic-api"
echo ""

REMOTE_SCRIPT

echo ""
echo "========================================="
echo "🎉 部署成功！"
echo "========================================="
echo ""
echo "📍 局域网访问地址："
echo "   前端：http://${MACHINE_2_IP}"
echo "   后端：http://${MACHINE_2_IP}:3000"
echo ""
echo "📱 现在局域网内所有设备都可以访问了！"
echo ""
