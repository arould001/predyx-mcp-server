---
name: notebooklm
description: "通过命令行操作 Google NotebookLM，实现批量导入文档、自动清洗去重、生成播客/视频/测验等内容。Use when: 需要批量导入文档到 NotebookLM、生成播客或视频、基于 sources 进行问答。Requires Google account login."
homepage: https://github.com/teng-lin/notebooklm-py
metadata: { "openclaw": { "emoji": "📓", "requires": { "bins": ["notebooklm"] } } }
---

# NotebookLM Skill

> **版本**: v0.3.3 | **GitHub**: teng-lin/notebooklm-py (3.3k ⭐)
> 
> 香蕉推荐的"神级 Skill"，完整覆盖 NotebookLM 所有功能。

## 安装状态

✅ 已安装（2026-02-22）
✅ 已登录 Google 账号

## 使用方式

所有命令需要在 venv 环境中运行：

```bash
source /opt/homebrew/lib/node_modules/openclaw/skills/notebooklm/.venv/bin/activate
notebooklm <command>
```

---

## 核心能力

### 1. Notebook 管理
```bash
notebooklm list                    # 列出所有 notebooks
notebooklm create "标题"            # 创建新 notebook
notebooklm use <id>                 # 选择当前 notebook
notebooklm delete <id>              # 删除 notebook
notebooklm rename "新标题"          # 重命名当前 notebook
notebooklm share                    # 开启分享
notebooklm share --revoke           # 关闭分享
notebooklm summary                  # 获取 AI 摘要
```

### 2. Source 管理
```bash
notebooklm source add "https://..."           # 添加 URL
notebooklm source add "./file.pdf"            # 添加本地文件
notebooklm source add-drive <id> "标题"       # 添加 Google Drive 文件
notebooklm source add-research "搜索词"       # Web 研究并自动导入
notebooklm source add-research "词" --mode deep --from drive  # Drive 深度研究
notebooklm source list                         # 列出所有 sources
notebooklm source fulltext <id> -o out.txt    # 导出源文本
notebooklm source guide <id>                   # 获取源指南
notebooklm source delete <id>                  # 删除 source
```

**支持的 Source 类型**：
- URL（网页）
- YouTube 视频
- 文件（PDF、Text、Markdown、Word、Audio、Video、Images）
- Google Drive 文档
- 粘贴的文本

### 3. Research Agents 🆕
```bash
notebooklm research status           # 查看研究状态
notebooklm research wait --import-all  # 等待完成并自动导入所有结果
```

**两种模式**：
- `fast` - 快速搜索
- `deep` - 深度研究

**来源**：
- `web` - 网页搜索
- `drive` - Google Drive 搜索

### 4. 对话
```bash
notebooklm ask "问题"                          # 提问
notebooklm ask "问题" -s src1 -s src2          # 指定 sources
notebooklm ask "问题" --json                   # 返回带引用的 JSON
notebooklm ask "问题" --save-as-note           # 保存为笔记
notebooklm configure --mode learning-guide     # 设置对话模式
notebooklm history                             # 查看历史
notebooklm history --save                      # 保存历史为笔记
```

### 5. 内容生成

#### Audio Overview（播客）
```bash
notebooklm generate audio "描述" \
  --format deep-dive \      # deep-dive|brief|critique|debate
  --length default \        # short|default|long
  --language zh_Hans \      # 50+ 语言
  --wait
```

#### Video Overview（视频）🆕
```bash
notebooklm generate video "描述" \
  --format explainer \      # explainer|brief
  --style whiteboard \      # auto|classic|whiteboard|kawaii|anime|watercolor|retro-print|heritage|paper-craft
  --wait
```

#### Slide Deck（幻灯片）
```bash
notebooklm generate slide-deck "描述" \
  --format detailed \       # detailed|presenter
  --length default \        # default|short
  --wait

# 修改单张幻灯片 🆕
notebooklm generate revise-slide "把标题往上移" \
  --artifact <id> --slide 0 --wait
```

#### Quiz / Flashcards
```bash
notebooklm generate quiz --difficulty hard --quantity more --wait
notebooklm generate flashcards --difficulty medium --wait
```

#### Infographic（信息图）
```bash
notebooklm generate infographic \
  --orientation portrait \  # landscape|portrait|square
  --detail detailed \       # concise|standard|detailed
  --wait
```

#### Mind Map（脑图）
```bash
notebooklm generate mind-map   # 同步生成，无需 --wait
```

#### Data Table（数据表）🆕
```bash
notebooklm generate data-table "比较关键概念" --wait
```

#### Report（报告）🆕
```bash
notebooklm generate report \
  --format study-guide \    # briefing-doc|study-guide|blog-post|custom
  --append "额外指令" \
  --wait
```

### 6. 下载

```bash
# 音频/视频
notebooklm download audio ./podcast.mp3 --latest
notebooklm download video ./video.mp4 --all

# 幻灯片（支持 PPTX！🆕）
notebooklm download slide-deck ./slides.pdf
notebooklm download slide-deck ./slides.pptx --format pptx

# 测验/闪卡（多格式）
notebooklm download quiz --format markdown quiz.md
notebooklm download flashcards --format json cards.json

# 其他
notebooklm download infographic ./info.png
notebooklm download mind-map ./map.json
notebooklm download data-table ./data.csv
notebooklm download report ./report.md
```

### 7. Artifact 管理 🆕
```bash
notebooklm artifact list --type audio     # 列出特定类型
notebooklm artifact get <id>              # 查看详情
notebooklm artifact rename <id> "新标题"
notebooklm artifact delete <id>
notebooklm artifact export <id> --type docs --title "标题"  # 导出到 Google Docs
notebooklm artifact suggestions           # 获取生成建议
```

### 8. Note 管理
```bash
notebooklm note list
notebooklm note create "笔记内容"
notebooklm note get <id>
notebooklm note rename <id> "标题"
notebooklm note delete <id>
```

### 9. 语言设置 🆕
```bash
notebooklm language list         # 列出所有支持的语言
notebooklm language get          # 查看当前语言
notebooklm language set zh_Hans  # 设置为简体中文
```

---

## Web UI 没有的功能 💎

| 功能 | 说明 |
|------|------|
| **批量下载** | `--all` 一次下载所有同类产物 |
| **测验导出** | JSON/Markdown/HTML，Web UI 只能交互查看 |
| **脑图 JSON** | 可导入其他可视化工具 |
| **PPTX 导出** | Web UI 只给 PDF |
| **单页修改** | `revise-slide` 用自然语言修改单张幻灯片 |
| **Research Agents** | Web/Drive 自动研究并导入 |
| **权限管理** | 编程方式控制分享 |
| **源文本导出** | `fulltext` 获取索引的文本内容 |
| **保存对话为笔记** | `history --save` / `ask --save-as-note` |

---

## 典型用法

### 批量导入文档站
```bash
# 1. 创建 notebook
notebooklm create "文档站研究"
notebooklm use <id>

# 2. 批量添加 sources
for url in $(cat urls.txt); do
  notebooklm source add "$url"
done

# 3. 生成播客
notebooklm generate audio "专注于技术细节" --wait
notebooklm download audio --latest podcast.mp3
```

### 自动化内容生产
```bash
# 从 PDF 生成学习材料
notebooklm source add "./paper.pdf"
notebooklm generate quiz --difficulty hard --wait
notebooklm generate flashcards --wait
notebooklm generate slide-deck --wait

# 下载所有
notebooklm download quiz quiz.md --format markdown
notebooklm download flashcards cards.json
notebooklm download slide-deck slides.pptx --format pptx
```

### Research Workflow 🆕
```bash
# 1. 创建研究 notebook
notebooklm create "AI Agent 趋势研究"
notebooklm use <id>

# 2. Web 研究并自动导入
notebooklm source add-research "AI Agent 2026 trends" --mode deep --from web
notebooklm research wait --import-all

# 3. 生成报告
notebooklm generate report --format study-guide --wait
notebooklm download report research.md
```

---

## 注意事项

- **非官方库**：使用 Google 未公开的 API，可能随时变化
- **速率限制**：批量操作需要间隔，使用 `--retry` 自动重试
- **语言全局**：`language set` 影响账号下所有 notebooks
- **异步生成**：大部分 generate 需要 `--wait` 等待完成（mind-map 除外）

---

## 更新日志

| 日期 | 变更 |
|------|------|
| 2026-03-07 | 大更新：添加 Research、Video、Data Table、Report、Language、Sharing、revise-slide、PPTX 导出等新功能 |
| 2026-02-22 | 初始版本 |
