# TROUBLESHOOTING.md - 故障排除经验

这里记录了遇到的问题和解决方案，方便以后快速排查。

---

## 📓 NotebookLM 登录问题

### 问题描述
`notebooklm login` 需要交互式终端，不能远程按 ENTER。

### 解决方案

**在本地终端窗口执行：**

```bash
source /opt/homebrew/lib/node_modules/openclaw/skills/notebooklm/.venv/bin/activate
notebooklm login
```

**操作步骤：**
1. 命令执行后，浏览器会自动打开
2. 登录 Google 账号
3. 看到 NotebookLM 主页后
4. **在终端窗口里按 ENTER**（不是在浏览器）
5. 看到 "Login successful" 表示登录成功

**登录状态保存位置：**
- `~/.notebooklm/storage_state.json`

**如果登录失败：**
1. 检查是否有代理影响（关闭系统代理）
2. 删除 `~/.notebooklm/` 目录重新登录
3. 确保 Playwright Chromium 已安装

---

## 🔌 飞书连接丢失（代理问题）

### 问题描述
飞书无法接收/发送消息，日志显示：
```
protocol mismatch: socks5h vs http
```

### 原因分析
macOS 系统代理（如 Clash）的 SOCKS5 代理会导致 axios 请求飞书 API 时失败。飞书插件通过代理连接，但代理协议不兼容。

### 解决方案

**临时关闭系统代理：**

```bash
# 关闭 Wi-Fi 的所有代理
networksetup -setwebproxystate Wi-Fi off
networksetup -setsecurewebproxystate Wi-Fi off
networksetup -setsocksfirewallproxystate Wi-Fi off
```

**或者在 Clash 里关闭"系统代理"开关**

**然后重启 Gateway：**
```bash
openclaw gateway restart
```

### 长期解决方案

**方案 A：在 Clash 配置里添加飞书直连规则**
```yaml
rules:
  - DOMAIN-SUFFIX,feishu.cn,DIRECT
  - DOMAIN-SUFFIX,larksuite.com,DIRECT
```

**方案 B：在 OpenClaw 配置里禁用飞书代理**
```json
{
  "channels": {
    "feishu": {
      "proxy": false
    }
  }
}
```

### 验证连接正常
```bash
# 检查日志
tail -20 /tmp/openclaw/openclaw-2026-02-22.log | grep feishu

# 应该看到类似这样的日志：
# feishu[main]: received message from ou_xxx
# feishu[main]: dispatching to agent
```

---

## 🛠️ Skills 在 Control UI 不显示

### 问题描述
Skill 文件已创建在 `~/.openclaw/workspace/skills/xxx/`，但 Control UI 的 Skills 页面看不到。

### 检查清单

1. **文件结构是否正确：**
   ```
   ~/.openclaw/workspace/skills/xxx/
   ├── SKILL.md          # 必须有
   ├── _meta.json        # 必须有
   └── .clawhub/
       └── origin.json   # 可选但推荐
   ```

2. **SKILL.md 格式：**
   ```yaml
   ---
   name: skill-name
   description: "描述"
   metadata: { "openclaw": { "emoji": "📝" } }
   ---
   # Skill 内容
   ```

3. **_meta.json 格式：**
   ```json
   {
     "ownerId": "local",
     "slug": "skill-name",
     "version": "1.0.0",
     "publishedAt": 1771689600000
   }
   ```

4. **重启 Gateway：**
   ```bash
   openclaw gateway restart
   ```

5. **刷新 Control UI 页面**（硬刷新：Cmd+Shift+R）

---

## 📥 NotebookLM 批量导入 Rate Limiting

### 问题描述
批量导入 URL 时，很多失败：
```
Error: Failed to add source: https://...
Possible causes: Rate limiting or quota exceeded
```

### 解决方案

1. **分批导入：** 每批 20-30 个 URL
2. **增加间隔：** 每批之间等待 30-60 秒
3. **检查失败的 URL：** 有些可能是重复或无效的

**批量导入脚本示例：**
```bash
# 分批导入，每批 20 个，间隔 30 秒
batch=0
while IFS= read -r url; do
  notebooklm source add "$url"
  count=$((count + 1))
  
  if [ $((count % 20)) -eq 0 ]; then
    batch=$((batch + 1))
    echo "批次 $batch 完成，等待 30 秒..."
    sleep 30
  fi
done < urls.txt
```

---

## 🔧 通用调试技巧

### 检查 Gateway 日志
```bash
# 实时查看日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# 过滤特定内容
tail -100 /tmp/openclaw/openclaw-*.log | grep -i error
```

### 检查 Gateway 状态
```bash
openclaw gateway status
```

### 重启 Gateway
```bash
openclaw gateway restart
```

### 检查进程
```bash
ps aux | grep openclaw
```
