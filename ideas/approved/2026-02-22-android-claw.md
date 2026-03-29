# 安卓手机运行 Claw

**优先级：** ⭐ 最高
**发现时间：** 2026-02-22
**来源：** Steven 提到网上有相关帖子
**提出者：** Steven

## 目标

在安卓手机里安装和运行 Claw，并让它能操作安卓的原生 App。

## 研究进度

### ✅ 搜索现有的安卓 Claw 实现
已完成！社区已经有很多成熟的实现方案：

**主要资源：**
- [AbuZar-Ansarii/Clawbot](https://github.com/AbuZar-Ansarii/Clawbot) - 90 stars, 31 forks
- Reddit r/termux 自动安装脚本
- YouTube 多个教程视频（18K+ views）
- Medium 详细文章

### ✅ 技术可行性
**结论：完全可行，已经成熟**

**技术栈：**
1. **Termux** - 从 F-Droid 安装（不是 Play Store）
2. **proot-distro + Ubuntu** - 在 Termux 中运行 Ubuntu 环境
3. **Node.js 22.x** - 通过 NodeSource 安装
4. **OpenClaw** - 正常 npm 安装

**关键修复：**
需要创建 `hijack.js` 解决 Android 网络接口问题：
```bash
cat <<EOF > /root/hijack.js
const os = require('os');
os.networkInterfaces = () => ({});
EOF
export NODE_OPTIONS="-r /root/hijack.js"
```

### ⏳ 操作安卓原生 App（待研究）
目前方案只能运行 OpenClaw Gateway，不能直接操作安卓原生 App。

**可能的方案：**
- 无障碍服务 (Accessibility Service)
- ADB over TCP
- Termux:API + 模拟点击

**这是下一步的研究方向**

### ✅ 性能和实用性评估
**优点：**
- 不需要 root
- 可以 24/7 运行（配合 wake-lock + 关闭电池优化）
- 有 Web Dashboard (127.0.0.1:18789)
- 可以连接各种消息平台（Telegram 等）
- 可以用 Ollama 跑本地模型（免费）

**限制：**
- 性能取决于手机配置
- 不能直接操作安卓原生 App（目前）
- 需要保持 Termux 前台运行（或使用后台方案）

## 下一步行动

1. **实际安装测试** - 需要一部安卓手机
2. **研究操作原生 App** - 这是关键突破点
3. **评估适合的手机型号** - 旧手机 vs 新手机

## 预估成本

中高 - 可能需要技术调研 + 实验

## 为什么想研究这个

移动端是重要场景。如果能在手机上运行 Claw，就可以随时随地使用，而且可以自动化手机上的很多操作。

## 备注

Steven 之前在网上看到过相关介绍帖子。
