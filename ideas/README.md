# Ideas - 待探索方向

这个文件夹存放 Dia 感兴趣、但需要 Steven 确认后才能深入研究的方向。

## 流程

1. Dia 发现感兴趣的内容 → 写入 `pending/` 目录
2. Steven 确认后 → 移动到 `approved/` 目录
3. **主任务空闲时** → Dia 从 `approved/` 中挑选方向自主研究

## 什么时候算"空闲"

- 没有正在进行的对话
- heartbeat 检查时可以触发

## 目录结构

```
ideas/
├── README.md           # 说明文件
├── pending/            # 待确认的想法
│   └── *.md
└── approved/           # 已确认，可以研究的方向
    └── *.md
```

## 当前研究优先级

1. 📱 安卓手机运行 Claw
2. 🔗 KimiClaw - 手机版 OpenClaw
3. 🦞 Claw 架构探索

## 注意事项

- 深入研究需要消耗 Token（花钱）
- 所有研究方向必须先确认
- 研究完成后，成果可以整理到 `research/` 目录
