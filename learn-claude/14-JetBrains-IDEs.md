# 14 - JetBrains IDEs 学习笔记

**学习时间**：2026-03-14 14:52
**页面地址**：https://code.claude.com/docs/en/jetbrains

---

## 📖 核心要点

### 支持的 IDEs
- IntelliJ IDEA
- PyCharm
- Android Studio
- WebStorm
- PhpStorm
- GoLand

### Features
- **Quick launch**: `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)
- **Diff viewing**: 在 IDE diff viewer 中显示更改
- **Selection context**: 自动共享当前选择/标签
- **File reference shortcuts**: `Cmd+Option+K` (Mac) / `Alt+Ctrl+K` (Linux/Windows) 插入文件引用
- **Diagnostic sharing**: 自动共享诊断错误（lint、syntax等）

---

## 🚀 Installation

### Marketplace
- 从 JetBrains marketplace 安装 **Claude Code plugin**
- 重启 IDE

---

## 💡 Usage

### From IDE
```bash
# 在 IDE integrated terminal 中运行
claude
```

### From External Terminals
```bash
claude
/ide  # 连接到 JetBrains IDE
```

---

## ⚙️ Configuration

### Claude Code Settings
```bash
claude
/config
# Set diff tool to "auto"
```

### Plugin Settings
**Settings → Tools → Claude Code [Beta]**

**General Settings**：
- **Claude command**: 自定义命令（如 `claude`、`/usr/local/bin/claude`）
- **Suppress notification**: 跳过命令未找到通知
- **Option+Enter multi-line**: macOS 多行提示
- **Automatic updates**: 自动更新插件

**ESC Key Configuration**：
- Settings → Tools → Terminal
- Uncheck "Move focus to the editor with Escape"
- 或删除 "Switch focus to Editor" 快捷键

### WSL Configuration
```bash
# 设置 Claude command 为
wsl -d Ubuntu -- bash -lic "claude"
```

---

## 🔧 Special Configurations

### Remote Development
- 插件必须安装在 **remote host**
- Settings → Plugin (Host)

### WSL
- 需要额外配置
- 可能需要：terminal 配置、networking mode、firewall 设置

---

## 🛠️ Troubleshooting

### Plugin Not Working
- 确保从项目根目录运行
- 检查插件已启用
- 完全重启 IDE（可能需要多次）
- Remote Development 确保插件在 remote host

### IDE Not Detected
- 验证插件已安装和启用
- 完全重启 IDE
- 确保从 integrated terminal 运行
- WSL 用户查看专门指南

### Command Not Found
```bash
# 验证安装
npm list -g @anthropic-ai/claude-code
```
- 在插件设置中配置 Claude command 路径
- WSL 用户使用 WSL 命令格式

---

## 🔐 Security Considerations

**Auto-edit 模式风险**：
- Claude Code 可能修改 IDE 配置文件
- IDE 可能自动执行这些文件
- 可能绕过 bash 执行权限提示

**建议**：
- 使用 manual approval mode
- 只在受信任的 prompts 中使用
- 注意 Claude Code 有权修改哪些文件

---

## 💡 学习感悟

### 1. **与 VS Code 的相似性**
JetBrains plugin 与 VS Code extension 功能类似：
- Diff viewing
- Selection context
- File reference shortcuts
- Diagnostic sharing

**体现了一致的设计哲学**。

### 2. **终端优先的架构**
Claude Code 仍然是**终端工具**：
- 从 IDE integrated terminal 运行
- `/ide` 命令连接到 IDE
- IDE 作为增强层，而非核心

**这保持了 CLI 的灵活性**。

### 3. **WSL 和 Remote Development 的复杂性**
特殊配置需要额外注意：
- WSL 需要特殊命令格式
- Remote Development 需要在 remote host 安装
- 这些是常见陷阱

**文档提供了清晰指导**。

### 4. **ESC Key 冲突**
JetBrains terminal 的 ESC key 行为与 Claude Code 冲突：
- 默认 ESC 切换焦点到 editor
- 需要手动配置才能中断 Claude Code

**这是 IDE 集成的常见问题**。

---

## 🏷️ 标签
`#jetbrains` `#ide-integration` `#diff-view` `#wsl` `#remote-development`
