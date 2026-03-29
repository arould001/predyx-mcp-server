#!/bin/bash
# Gateway 救援工具包
# 用途：观察 Coco 的破坏 + 救援挂掉的 gateway

# ============================================
# Phase 1: 建立观察点（只读操作）
# ============================================

# 1. 连接到2号机（需要 Steven 提供 SSH 信息）
# ssh user@2号机IP -p 端口

# 2. 持续监控 gateway 状态
watch_gateway() {
  echo "=== Gateway 状态监控 ==="
  echo "时间: $(date)"
  echo ""
  
  # 检查主 gateway
  echo "【主 Gateway】"
  curl -s http://127.0.0.1:18789/health 2>&1 | head -20
  echo ""
  
  # 检查医生 gateway（如果存在）
  echo "【医生 Gateway】"
  curl -s http://127.0.0.1:19789/health 2>&1 | head -20
  echo ""
  
  # 检查进程
  echo "【进程状态】"
  ps aux | grep -E "openclaw|gateway" | grep -v grep
  echo ""
  
  # 检查端口占用
  echo "【端口占用】"
  lsof -i :18789 2>/dev/null || echo "18789 未占用"
  lsof -i :19789 2>/dev/null || echo "19789 未占用"
  echo ""
  
  # 检查最近的错误日志
  echo "【最近错误日志】"
  tail -50 ~/.openclaw/logs/*.log 2>/dev/null | grep -i "error\|fail\|crash" | tail -10
}

# 3. 观察配置改动
watch_config() {
  echo "=== 配置文件监控 ==="
  echo "时间: $(date)"
  echo ""
  
  # 检查配置文件修改时间
  ls -lh ~/.openclaw/openclaw.json
  echo ""
  
  # 检查配置差异（如果有备份）
  if [ -f ~/.openclaw/openclaw.json.bak ]; then
    echo "【与上次备份的差异】"
    diff ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
  fi
}

# ============================================
# Phase 2: 救援操作（Coco 搞挂后执行）
# ============================================

# 1. 自动诊断
rescue_diagnose() {
  echo "=== 开始诊断 ==="
  
  # 尝试自动修复
  echo "1. 尝试 openclaw doctor fix..."
  openclaw doctor fix
  
  # 检查配置文件语法
  echo -e "\n2. 检查配置文件..."
  if openclaw config validate; then
    echo "✅ 配置文件语法正确"
  else
    echo "❌ 配置文件有错误"
  fi
  
  # 检查 gateway 状态
  echo -e "\n3. 检查 gateway 状态..."
  openclaw gateway status
}

# 2. 重启 gateway
rescue_restart() {
  echo "=== 重启 Gateway ==="
  
  # 停止服务
  echo "1. 停止 gateway..."
  openclaw gateway stop
  sleep 3
  
  # 检查是否真的停了
  if pgrep -f "openclaw gateway" > /dev/null; then
    echo "⚠️  进程还在，强制杀死..."
    pkill -9 -f "openclaw gateway"
    sleep 2
  fi
  
  # 启动服务
  echo "2. 启动 gateway..."
  openclaw gateway start
  sleep 5
  
  # 验证
  echo "3. 验证启动..."
  openclaw gateway status
}

# 3. 回滚到备份配置
rescue_rollback() {
  echo "=== 回滚配置 ==="
  
  # 检查是否有备份
  if [ ! -f ~/.openclaw/openclaw.json.bak ]; then
    echo "❌ 没有备份文件"
    return 1
  fi
  
  # 备份当前配置
  echo "1. 备份当前（损坏的）配置..."
  cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.broken-$(date +%Y%m%d-%H%M%S)
  
  # 恢复备份
  echo "2. 恢复备份..."
  cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
  
  # 重启
  echo "3. 重启 gateway..."
  rescue_restart
}

# 4. 查看日志
rescue_logs() {
  echo "=== 最近的 Gateway 日志 ==="
  tail -100 ~/.openclaw/logs/gateway.log | grep -A 5 -B 5 "error\|fail\|crash"
}

# ============================================
# Phase 3: 交互式菜单
# ============================================

menu() {
  echo ""
  echo "🚑 Gateway 救援工具包"
  echo "====================="
  echo ""
  echo "【观察模式】"
  echo "  1) 监控 gateway 状态"
  echo "  2) 监控配置改动"
  echo ""
  echo "【救援模式】"
  echo "  3) 自动诊断"
  echo "  4) 重启 gateway"
  echo "  5) 回滚配置"
  echo "  6) 查看日志"
  echo ""
  echo "  q) 退出"
  echo ""
  read -p "选择操作: " choice
  
  case $choice in
    1) watch_gateway ;;
    2) watch_config ;;
    3) rescue_diagnose ;;
    4) rescue_restart ;;
    5) rescue_rollback ;;
    6) rescue_logs ;;
    q) exit 0 ;;
    *) echo "无效选择" ;;
  esac
  
  # 循环
  menu
}

# ============================================
# 执行
# ============================================

if [ "$1" = "watch" ]; then
  # 持续监控模式
  while true; do
    clear
    watch_gateway
    sleep 5
  done
elif [ "$1" = "rescue" ]; then
  # 救援模式
  rescue_diagnose
  read -p "是否重启 gateway? (y/n): " confirm
  if [ "$confirm" = "y" ]; then
    rescue_restart
  fi
else
  # 交互式菜单
  menu
fi
