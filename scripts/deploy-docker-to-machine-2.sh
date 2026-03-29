#!/bin/bash

# Docker 方案部署到 2号机（IP: 192.168.1.96）

set -e

MACHINE_2_IP="192.168.1.96"
MACHINE_2_USER="caidengyong"
PROJECT_NAME="bzt-ic"
LOCAL_DIR="/Users/caidengyong/Desktop/steven/bzt-ic"
REMOTE_DIR="~/projects/${PROJECT_NAME}"

echo "========================================="
echo "🐳 Docker 方案部署到 2号机"
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

# 第四步：检查并安装 Docker Desktop
echo "🐳 检查 2号机 Docker..."
if ! ssh ${MACHINE_2_USER}@${MACHINE_2_IP} "command -v docker" &> /dev/null; then
    echo "⚠️  2号机未安装 Docker"
    echo ""
    echo "📦 准备安装 Docker Desktop..."
    echo ""
    read -p "是否继续安装 Docker Desktop？[Y/n]: " install_docker
    install_docker=${install_docker:-Y}
    
    if [[ $install_docker =~ ^[Yy]$ ]]; then
        echo "📦 安装 Docker Desktop（需要几分钟）..."
        ssh ${MACHINE_2_USER}@${MACHINE_2_IP} << 'EOF'
# 使用 Homebrew 安装
if command -v brew &> /dev/null; then
    echo "使用 Homebrew 安装..."
    brew install --cask docker
else
    echo "❌ 未安装 Homebrew，请先安装 Homebrew"
    echo "   访问：https://brew.sh"
    exit 1
fi
EOF
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "⚠️  Docker Desktop 安装完成！"
            echo ""
            echo "⚠️  请在 2号机上执行以下操作："
            echo "   1. 打开 Docker Desktop 应用"
            echo "   2. 等待 Docker 启动完成（右上角小鲸鱼图标变绿）"
            echo "   3. 完成后回到这里按回车继续..."
            echo ""
            read -p "按回车继续..."
        else
            echo "❌ Docker Desktop 安装失败"
            exit 1
        fi
    else
        echo "❌ 取消部署"
        exit 1
    fi
else
    echo "✅ 2号机 Docker 已安装"
    
    # 检查 Docker 是否运行
    if ! ssh ${MACHINE_2_USER}@${MACHINE_2_IP} "docker ps" &> /dev/null; then
        echo "⚠️  Docker 未运行"
        echo ""
        echo "请在 2号机上启动 Docker Desktop，然后按回车继续..."
        read -p "按回车继续..."
    fi
fi
echo ""

# 第五步：配置环境变量
echo "⚙️  配置环境变量..."
ssh ${MACHINE_2_USER}@${MACHINE_2_IP} << 'EOF'
cd ~/projects/bzt-ic

if [ ! -f .env ]; then
    echo "📝 创建 .env 文件..."
    cp .env.example .env
    
    # 生成随机密码
    DB_PASSWORD=$(openssl rand -base64 16 | tr -d '/+=' | cut -c1-20)
    JWT_SECRET=$(openssl rand -base64 32)
    
    # 更新 .env 文件
    sed -i '' "s/your_secure_password_here/${DB_PASSWORD}/g" .env
    sed -i '' "s/your_jwt_secret_here_at_least_32_characters_long/${JWT_SECRET}/g" .env
    
    echo "✅ .env 文件已创建"
    echo ""
    echo "数据库密码：${DB_PASSWORD}"
    echo "JWT Secret：已自动生成"
else
    echo "✅ .env 文件已存在"
fi
EOF
echo ""

# 第六步：在 2号机上部署
echo "🚀 在 2号机上执行部署..."
echo ""

ssh ${MACHINE_2_USER}@${MACHINE_2_IP} << 'EOF'
cd ~/projects/bzt-ic

echo "========================================="
echo "🔨 构建 Docker 镜像"
echo "========================================="
echo ""

# 赋予执行权限
chmod +x deploy.sh

# 构建镜像
echo "📦 构建 Docker 镜像（需要几分钟）..."
docker-compose build

echo ""
echo "========================================="
echo "🚀 启动服务"
echo "========================================="
echo ""

# 启动服务
docker-compose up -d

echo ""
echo "⏳ 等待数据库启动（10秒）..."
sleep 10

echo ""
echo "========================================="
echo "📊 运行数据库迁移"
echo "========================================="
echo ""

# 运行迁移
docker-compose exec -T backend npx prisma migrate deploy

echo ""
echo "========================================="
echo "✅ 部署完成！"
echo "========================================="
echo ""

# 显示容器状态
docker-compose ps

echo ""
echo "📍 本地访问地址："
echo "   前端：http://localhost"
echo "   后端：http://localhost:3000"
echo ""
echo "📋 常用命令："
echo "   查看状态：docker-compose ps"
echo "   查看日志：docker-compose logs -f"
echo "   重启服务：docker-compose restart"
echo "   停止服务：docker-compose down"
echo ""

EOF

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
