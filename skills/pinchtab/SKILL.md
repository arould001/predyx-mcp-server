# PinchTab Skill

> 轻量级浏览器自动化工具，用于简单网页信息获取

---

## 核心命令

### 服务管理
```bash
# 启动 daemon（后台运行）
pinchtab daemon

# 检查健康状态
pinchtab health

# 列出所有 tab
pinchtab tabs list

# 关闭指定 tab
pinchtab tabs close <tabId>
```

### 页面操作
```bash
# 导航到 URL
pinchtab nav <url>

# 获取页面结构（紧凑格式）
pinchtab snap -c --max-tokens <n>

# 提取页面文本
pinchtab text

# 点击元素
pinchtab click <ref>

# 截图
pinchtab screenshot

# 保存为 PDF
pinchtab pdf --tab <tabId> -o output.pdf
```

---

## 常用工作流

### 1. 获取网页文本内容
```bash
# 步骤 1: 导航
pinchtab nav "https://example.com"

# 步骤 2: 提取文本
pinchtab text 2>&1
```

### 2. 网页自动化（点击 + 提取）
```bash
# 步骤 1: 导航
pinchtab nav "https://example.com/docs"

# 步骤 2: 获取结构，找到要点击的元素
pinchtab snap -c --max-tokens 800

# 步骤 3: 点击链接
pinchtab click e6

# 步骤 4: 提取内容
pinchtab text 2>&1
```

### 3. 处理 Tab 满了的情况
```bash
# 检查 tab 数量
pinchtab tabs list

# 如果满了（20/20），重启 daemon
pkill -f pinchtab && pinchtab daemon
```

---

## 最佳实践

### 优先级
**简单网页信息获取 → 优先使用 PinchTab**

**原因**：
- ✅ 轻量级，启动快
- ✅ 命令简单，易于使用
- ✅ 支持基础自动化（点击、导航）
- ✅ 文本提取完整

### 适用场景
- ✅ 读取文档页面
- ✅ 获取网页文本内容
- ✅ 简单的点击操作
- ✅ 截图保存

### 不适用场景
- ❌ 复杂的 JS 交互
- ❌ 需要登录的页面
- ❌ 表单填写
- ❌ 多步骤操作

**这些场景使用独立浏览器**：`browser(action="...", profile="openclaw")`

---

## 注意事项

### Tab 管理
- **上限**：20 个 tab
- **定期清理**：`pinchtab tabs close <id>`
- **满了重启**：`pkill -f pinchtab && pinchtab daemon`

### 输出处理
```bash
# text 命令可能有 warning，用 2>&1 过滤
pinchtab text 2>&1
```

### 元素引用
- Snapshot 返回的元素引用格式：`e0`, `e1`, `e2`...
- 使用 `pinchtab snap -c` 获取紧凑格式
- `--max-tokens` 控制输出长度

---

## 常见问题

### Q: Tab 满了怎么办？
```bash
# 方案 1: 关闭不需要的 tab
pinchtab tabs close <tabId>

# 方案 2: 重启 daemon（清空所有 tab）
pkill -f pinchtab && pinchtab daemon
```

### Q: 如何找到要点击的元素？
```bash
# 获取页面结构
pinchtab snap -c --max-tokens 800

# 查找特定文本
pinchtab snap 2>&1 | grep -i "关键词"
```

### Q: 输出太多怎么办？
```bash
# 限制 token 数量
pinchtab snap -c --max-tokens 500

# 只看前 N 行
pinchtab text 2>&1 | head -100
```

---

## 已验证能力

| 功能 | 状态 | 备注 |
|------|------|------|
| **健康检查** | ✅ | `pinchtab health` |
| **Tab 列表** | ✅ | `pinchtab tabs list` |
| **导航** | ✅ | 已测试 Claude Code 文档 |
| **Snapshot** | ✅ | 紧凑格式 `-c` |
| **点击** | ✅ | 元素引用 `e0`, `e1`... |
| **文本提取** | ✅ | 完整提取 |
| **截图** | ✅ | `pinchtab screenshot` |

---

## 对比其他工具

| 工具 | 场景 | 复杂度 | 优先级 |
|------|------|--------|--------|
| **PinchTab** | 简单网页信息获取 | ⭐ | **最高** |
| **独立浏览器** | 复杂交互、JS 渲染 | ⭐⭐⭐ | 中等 |
| **web_fetch** | 已知 URL 抓取 | ⭐ | 最低（JS 渲染差） |

---

## 相关文件

- **TOOLS.md**: 网络搜索工具对比
- **MEMORY.md**: PinchTab 验证记录

---

## 更新日志

| 日期 | 变更 |
|------|------|
| 2026-03-14 | 初始版本，基于实战测试创建 |
