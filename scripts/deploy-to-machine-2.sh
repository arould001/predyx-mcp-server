#!/bin/bash

# BZT-IC 一键部署到 2号机（IP: 192.168.1.96）
# 使用方法：bash deploy-to-machine-2.sh

set -e

MACHINE_2_IP="192.168.1.96"
MACHINE_2_USER="caidengyong"
PROJECT_NAME="bzt-ic"
LOCAL_DIR="/Users/caidengyong/Desktop/steven/bzt-ic"

echo "========================================="
echo "🚀 BZT-IC 部署到 2号机"
echo "========================================="
echo ""
echo "目标机器：${MACHINE_2_USER}@${MACHINE_2_IP}"
echo "项目路径：${LOCAL_DIR}"
echo ""

# 检查 SSH 连接
echo "📡 检查 2号机连接..."
if ! ssh ${MACHINE_2_USER}@${MACHINE_2_IP} "echo 'Connection OK'" &> /dev/null; then
    echo "❌ 无法连接到 2号机 (${MACHINE_2_IP})"
    echo "   请确认："
    echo "   1. 2号机已开机"
    echo "   2. SSH 服务已启动（系统偏好设置 → 共享 → 远程登录）"
    echo "   3. 网络连接正常"
    exit 1
fi
echo "✅ 2号机连接成功"
echo ""

# 显示系统信息
echo "📊 2号机信息："
ssh ${MACHINE_2_USER}@${MACHINE_2_IP} "uname -a && df -h ~ | tail -1"
echo ""

# 选择部署方案
echo "请选择部署方案："
echo ""
echo "  1) Docker 部署（推荐）"
echo "     - 环境隔离，易于维护"
echo "     - 需要安装 Docker Desktop（约 2GB）"
echo "     - 内存占用：约 1.5GB"
echo ""
echo "  2) 直接运行（轻量）"
echo "     - 资源占用少，性能好"
echo "     - 需要安装 MariaDB + PM2 + Nginx"
echo "     - 内存占用：约 800MB"
echo ""
read -p "请输入选择 [1-2，默认 1]: " choice
choice=${choice:-1}

case $choice in
    1)
        echo ""
        echo "🐳 使用 Docker 部署..."
        bash /Users/caidengyong/.openclaw/workspace/scripts/deploy-docker-to-machine-2.sh
        ;;
    2)
        echo ""
        echo "⚡ 使用直接运行部署..."
        bash /Users/caidengyong/.openclaw/workspace/scripts/deploy-native-to-machine-2.sh
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac
