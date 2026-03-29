# 12 - Chrome Extension (Beta) 学习笔记

**学习时间**：2026-03-14 14:42
**页面地址**：https://code.claude.com/docs/en/chrome

---

## 📖 核心要点

### 是什么
通过 Chrome extension 让 Claude Code 控制浏览器，实现自动化测试、调试和数据提取。

### Capabilities
- ✅ **Live debugging** - 读取 console errors 和 DOM state
- ✅ **Design verification** - 从 Figma mock 构建后验证 UI
- ✅ **Web app testing** - 测试表单验证、视觉回归
- ✅ **Authenticated web apps** - 访问已登录的 Google Docs、Gmail、Notion
- ✅ **Data extraction** - 从网页提取结构化信息
- ✅ **Task automation** - 数据输入、表单填充
- ✅ **Session recording** - 录制浏览器交互为 GIF

### Prerequisites
- Chrome 或 Edge 浏览器
- Claude in Chrome extension v1.0.36+
- Claude Code v2.0.73+
- Anthropic plan（Pro/Max/Teams/Enterprise）

**⚠️ Beta 限制**：
- 不支持 Brave、Arc
- 不支持 WSL
- 不支持第三方提供商（Bedrock、Vertex AI、Foundry）

---

## 🚀 Get Started

### CLI 启动
```bash
claude --chrome
```

或会话中：
```bash
/chrome
```

### Example Prompt
```bash
Go to code.claude.com/docs, click on the search box, type "hooks", and tell me what results appear
```

### Enable by Default
```bash
/chrome
# 选择 "Enabled by default"
```

**注意**：会增加上下文消耗。

---

## 💡 Example Workflows

### 1. Test Local Web App
```bash
I just updated the login form validation. Can you open localhost:3000, try submitting the form with invalid data, and check if the error messages appear correctly?
```

### 2. Debug with Console Logs
```bash
Open the dashboard page and check the console for any errors when the page loads.
```

### 3. Automate Form Filling
```bash
I have a spreadsheet of customer contacts in contacts.csv. For each row, go to the CRM at crm.example.com, click "Add Contact", and fill in the name, email, and phone fields.
```

### 4. Draft in Google Docs
```bash
Draft a project update based on the recent commits and add it to my Google Doc at docs.google.com/document/d/abc123
```

### 5. Extract Data
```bash
Go to the product listings page and extract the name, price, and availability for each item. Save the results as a CSV file.
```

### 6. Record Demo GIF
```bash
Record a GIF showing how to complete the checkout flow.
```

---

## 🔧 Troubleshooting

### Extension not detected
- 检查 `chrome://extensions`
- 检查 `claude --version`
- 运行 `/chrome` → "Reconnect extension"
- 重启 Chrome 和 Claude Code

### Browser not responding
- 检查是否有 modal dialog 阻塞
- 让 Claude 创建新标签页
- 重启 extension

### Connection drops
- Service worker 休眠
- 运行 `/chrome` → "Reconnect extension"

---

## 💡 学习感悟

### 1. **浏览器自动化的威力**
Chrome extension 让 Claude Code 可以：
- 访问已登录的应用（无需 API）
- 实时调试
- 自动化重复任务

这是 **RPA（Robotic Process Automation）** 的 AI Agent 版本。

### 2. **与 OpenClaw browser tool 的对比**
**相似**：都可以控制浏览器
**差异**：
- Claude Code 用 Chrome extension，OpenClaw 用独立浏览器
- Claude Code 共享登录状态，OpenClaw 隔离环境
- Claude Code 可以录制 GIF，OpenClaw 不行

### 3. **Beta 状态的限制**
目前还在 Beta：
- 不支持所有 Chromium 浏览器
- 不支持 WSL
- 不支持第三方提供商

这些限制可能随着时间改善。

---

## 🏷️ 标签
`#chrome` `#browser-automation` `#testing` `#rpa` `#beta`
