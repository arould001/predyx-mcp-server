#!/bin/bash
# LNbits 本地部署脚本

echo "🚀 开始部署 LNbits..."

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装"
    exit 1
fi

echo "✅ Docker 已安装: $(docker --version)"

# 停止并删除旧容器（如果存在）
echo "🧹 清理旧容器..."
docker stop lnbits 2>/dev/null || true
docker rm lnbits 2>/dev/null || true

# 创建数据目录
mkdir -p ~/.lnbits

# 启动 LNbits
echo "🚀 启动 LNbits 容器..."
docker run -d \
  --name lnbits \
  -p 5000:5000 \
  -v ~/.lnbits:/app/data \
  --restart unless-stopped \
  lnbits/lnbits:latest

# 等待启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查状态
if docker ps | grep -q lnbits; then
    echo "✅ LNbits 已启动！"
    echo ""
    echo "📱 访问地址：http://localhost:5000"
    echo ""
    echo "下一步："
    echo "1. 打开浏览器访问 http://localhost:5000"
    echo "2. 创建新钱包"
    echo "3. 在 Extensions 中找到 NWCProvider"
    echo "4. 创建 NWC connection"
else
    echo "❌ 启动失败，检查日志："
    docker logs lnbits
fi
