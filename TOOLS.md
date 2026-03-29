# TOOLS.md

## ⚠️ P0 规则

### 🌐 联网操作（统一用独立浏览器）

```
所有联网操作 → browser(action="...", profile="openclaw")
```

**禁止**：web_fetch（JS 差）、Chrome 扩展（认证问题）、curl + DuckDuckGo（不稳定）

### 🔍 工具选择

```
需要联网？
├─ 搜索？→ Tavily
├─ 访问网页？
│  ├─ 简单网页 → PinchTab
│  ├─ 复杂网站 → browser
│  └─ 已知 URL → web_fetch
└─ 不联网 → 本地工具
```

---

## 📊 网络工具（2026-03-29 验证）

| 工具 | 用途 | 命令 | 状态 | 推荐 |
|------|------|------|------|------|
| Tavily | 搜索 | `tavily "query" --topic news` | ✅ | ⭐⭐⭐⭐⭐ |
| PinchTab | 简单网页 | `pinchtab nav <url>` | ✅ | ⭐⭐⭐⭐⭐ |
| browser | 复杂网站 | `browser(action="open")` | ✅ | ⭐⭐⭐⭐⭐ |
| web_fetch | 已知URL | `web_fetch(url="...")` | ✅ | ⭐⭐⭐⭐ |
| web_search | 简单搜索 | 需配置 Gemini Key | ⚠️ | ⭐⭐⭐ |

**不推荐**：DuckDuckGo（CAPTCHA）、searchGPT（19个月未更新）、Apify（OAuth复杂）

### 🎯 Tavily 使用

```bash
# 基础搜索
/Users/caidengyong/.openclaw/workspace/skills/liang-tavily-search/tavily "AI trends 2026"

# 新闻搜索（最近一周）
/Users/caidengyong/.openclaw/workspace/skills/liang-tavily-search/tavily "Claude Code" --topic news --time-range week

# 选项
-n <count>              结果数量（1-20）
--topic <news|general>  搜索类型
--time-range <range>    时间范围（day/week/month/year）
--include-domains <list> 域名白名单
--exclude-domains <list> 域名黑名单
```

### 🎯 PinchTab 使用

```bash
pinchtab nav <url>      # 导航
pinchtab text 2>&1      # 提取文本
pinchtab snap -c        # 获取结构
pinchtab click <ref>    # 点击
```

**限制**：Tab 上限 20 个，不支持 JS 渲染、需要登录的页面

---

## 🖥️ 远程服务器

### 2号机（Coco）

```bash
ssh 192.168.1.96
export PATH="/usr/local/bin:/Users/caidengyong/.npm-global/bin:$PATH"
```

**环境**：macOS 26.0.1 (arm64) | Node v24.13.1 | OpenClaw 2026.2.21 | Gateway 18789

---

## 📢 Discord 频道

**任务中心**：`1475337325117444217`（项目帖子专用）

---

## 🚀 快速访问

**Dia HUD**：http://localhost:8888 | **TTS语音助手**：http://localhost:5001
