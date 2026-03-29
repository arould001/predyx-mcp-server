# LNbits + NWC 完整研究方案

> **研究时间**：2026-03-27 01:29 AM
> **目的**：为 Steven 提供最优的免费 Lightning 钱包方案，支持 NWC（Nostr Wallet Connect）

---

## 🎯 核心发现

### 1. LNbits 完全支持 NWC
- **NWCProvider 扩展**：LNbits 有官方的 NWC 扩展
- **双向支持**：
  - LNbits 可以作为 Nostr 客户端的 wallet service
  - LNbits 可以作为 NWC 客户端被其他 wallet funding
- **完全免费**：开源，MIT 协议

### 2. NWC 的关键优势
- **隐私**：Lightning node 可以保持在私有网络
- **简单**：一键支付，无需复杂配置
- **灵活**：支持多种 Lightning 后端
- **无需 Nostr 账户**：Nostr 只是消息层

---

## 📋 推荐方案（按优先级排序）

### 方案 1：公共 LNbits 实例（最快）⭐⭐⭐⭐⭐

**推荐指数**：最高（立即开始）

**步骤**：
1. 访问 **https://legend.lnbits.com**
2. 创建新钱包（无需注册）
3. 进入 **Extensions** → 搜索 **NWCProvider**
4. 安装 NWCProvider 扩展
5. 进入 NWCProvider → 创建新的 NWC 连接
6. 复制 connection string（格式：`nostr+walletconnect://...`）
7. 把 connection string 发给我

**时间**：5-10 分钟

**优点**：
- ✅ 完全免费
- ✅ 立即可用
- ✅ 无需技术能力
- ✅ 无需部署

**缺点**：
- ⚠️ 依赖第三方服务
- ⚠️ 可能有使用限制

**风险**：
- 钱包在第三方服务器上（不推荐存储大量资金）
- 适合测试和小额支付

---

### 方案 2：Docker 本地部署（最稳定）⭐⭐⭐⭐

**推荐指数**：高（长期使用）

**前提**：需要 Docker

**步骤**：
```bash
# 1. 拉取 LNbits 镜像
docker pull lnbits/lnbits:latest

# 2. 运行 LNbits
docker run -d \
  --name lnbits \
  -p 5000:5000 \
  -v ~/lnbits-data:/app/data \
  -e LNBITS_ADMIN_UI=true \
  lnbits/lnbits:latest

# 3. 访问 http://localhost:5000
# 4. 创建 SuperUser
# 5. 进入 Extensions → 安装 NWCProvider
# 6. 创建 NWC 连接
# 7. 复制 connection string
```

**时间**：15-30 分钟

**优点**：
- ✅ 完全控制
- ✅ 无限制
- ✅ 本地部署
- ✅ 数据安全

**缺点**：
- ⚠️ 需要 Docker
- ⚠️ 需要一点技术能力

---

### 方案 3：AppImage (Linux) 部署 ⭐⭐⭐

**推荐指数**：中（适合 Linux 用户）

**步骤**：
```bash
# 1. 下载 AppImage
wget $(curl -s https://api.github.com/repos/lnbits/lnbits/releases/latest | jq -r '.assets[] | select(.name | endswith(".AppImage")) | .browser_download_url') -O LNbits-latest.AppImage

# 2. 添加执行权限
chmod +x LNbits-latest.AppImage

# 3. 运行
LNBITS_ADMIN_UI=true HOST=0.0.0.0 PORT=5000 ./LNbits-latest.AppImage

# 4. 访问 http://localhost:5000
# 5. 创建 SuperUser
# 6. 安装 NWCProvider 扩展
# 7. 创建 NWC 连接
```

**时间**：10-15 分钟

**优点**：
- ✅ 简单
- ✅ 独立文件
- ✅ 无需安装

**缺点**：
- ⚠️ 仅 Linux
- ⚠️ 需要手动更新

---

## 🔐 NWC 连接字符串格式

**格式**：
```
nostr+walletconnect://<pubkey>?relay=<relay_url>&secret=<secret>
```

**示例**：
```
nostr+walletconnect://npub1abc123...?relay=wss://relay.damus.io&secret=xyz789...
```

**关键参数**：
- `pubkey`：Nostr 公钥
- `relay`：Nostr relay URL
- `secret`：加密密钥

---

## 📊 方案对比总结

| 方案 | 时间 | 难度 | 成本 | 控制度 | 推荐度 |
|------|------|------|------|--------|--------|
| **公共 LNbits** | 5 分钟 | ⭐ | 免费 | 低 | ⭐⭐⭐⭐⭐ |
| **Docker 本地** | 30 分钟 | ⭐⭐ | 免费 | 高 | ⭐⭐⭐⭐ |
| **AppImage** | 15 分钟 | ⭐⭐ | 免费 | 高 | ⭐⭐⭐ |

---

## 💡 我的推荐

### 如果你现在就想开始：
**选择方案 1（公共 LNbits）**
- 5 分钟搞定
- 立即测试 Nostr 身份
- 等以后有需求再迁移到本地

### 如果你想长期稳定：
**选择方案 2（Docker 本地）**
- 完全控制
- 无限制
- 数据安全

---

## 🚀 下一步行动

1. **明天早上**：我把这个方案发给 Steven
2. **Steven 选择方案**：根据技术能力和时间
3. **创建 NWC 连接**：获取 connection string
4. **测试 Nostr 身份**：开始赚钱的第一步

---

## ⚠️ 安全提醒

1. **不要在公共 LNbits 存储大量资金**
2. **定期备份钱包数据**
3. **妥善保管 connection string**（相当于私钥）
4. **不要把 connection string 分享给不信任的应用**

---

## 📚 参考资源

- **LNbits 官网**：https://lnbits.com
- **LNbits GitHub**：https://github.com/lnbits/lnbits
- **NWC 协议**：https://nwc.dev
- **公共 LNbits 实例**：https://legend.lnbits.com
- **LNbits 安装文档**：https://github.com/lnbits/lnbits/blob/main/docs/guide/installation.md

---

**研究完成时间**：2026-03-27 01:45 AM
**下一步**：明天早上发给 Steven，等待他的选择
