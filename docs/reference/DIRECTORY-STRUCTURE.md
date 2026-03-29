# Workspace 目录规范

> 最后更新：2026-02-23

---

## 目录结构

```
~/.openclaw/workspace/
│
├── 📄 根目录（核心配置）
│   ├── CORE.md              # 核心记忆
│   ├── MEMORY.md            # 长期记忆
│   ├── RELATIONSHIPS.md     # 关系图谱
│   ├── HEARTBEAT.md         # 触发器配置
│   ├── SOUL.md              # 人格定义
│   ├── USER.md              # 用户信息
│   ├── IDENTITY.md          # 身份详情
│   ├── AGENTS.md            # 行为准则
│   ├── TOOLS.md             # 工具笔记
│   ├── TROUBLESHOOTING.md   # 故障排除
│   └── rules.md             # 防错规则
│
├── 📁 memory/（记忆系统）
│   ├── YYYY-MM-DD.md        # 话题日志
│   ├── heartbeat-state.json # 定时任务状态
│   └── pending-share.md     # 待分享内容
│
├── 📁 docs/（文档）
│   ├── guides/               # 教程指南
│   │   └── MEMORY-SYSTEM-GUIDE.md
│   ├── social/               # 社交媒体内容
│   │   └── openclaw-*.md
│   ├── topics/               # 主题文章
│   │   ├── memory-system/    # 记忆系统相关
│   │   ├── gateway/          # Gateway 相关
│   │   └── skills/           # 技能相关
│   ├── reference/            # 参考资料
│   │   └── DIRECTORY-STRUCTURE.md
│   └── drafts/               # 草稿/待发布
│       └── *.md
│
├── 📁 ideas/（想法系统）
│   ├── pending/              # 待确认
│   └── approved/             # 已批准
│
├── 📁 archive/（归档）
│   ├── experiments/          # 实验性项目
│   └── projects/             # 正式项目
│
└── 📁 skills/（技能）
    └── */                    # 自定义技能
```

---

## 放置规则

| 内容类型 | 放置位置 | 例子 |
|---------|---------|------|
| 核心配置文件 | 根目录 | CORE.md, MEMORY.md |
| 话题日志 | memory/ | 2026-02-23.md |
| **教程/指南** | docs/guides/ | MEMORY-SYSTEM-GUIDE.md |
| **社交媒体内容** | docs/social/ | 小红书、微博文章 |
| **主题文章** | docs/topics/{主题}/ | 深度技术文章 |
| **参考资料** | docs/reference/ | 目录规范、配置说明 |
| **草稿** | docs/drafts/ | 待发布内容 |
| 待研究想法 | ideas/pending/ | 新功能提案 |
| 已批准想法 | ideas/approved/ | 准备执行的想法 |
| 归档项目 | archive/ | 不再活跃的项目 |
| 自定义技能 | skills/ | 新开发的技能 |

---

## docs/ 子目录说明

| 子目录 | 用途 | 例子 |
|--------|------|------|
| guides/ | 教程、指南类 | 《OpenClaw 记忆系统搭建指南》 |
| social/ | 社交媒体内容 | 小红书笔记、微博文章 |
| topics/ | 主题深度文章 | 按技术主题分类 |
| reference/ | 参考资料 | 规范文档、配置说明 |
| drafts/ | 草稿 | 还没写完或待审核的内容 |

---

## 新建文件前检查

1. 这个文件属于哪个目录？
2. 是否需要新建文件夹？（先问用户）
3. 根目录保持干净，只放核心配置

---

## 禁止

- ❌ 在根目录随意创建新文件夹
- ❌ 创建未在规范中的目录
- ❌ 把临时文件放在根目录
