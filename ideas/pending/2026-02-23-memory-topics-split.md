# Idea: 记忆系统 Topics 拆分

> 来源：B站视频 AI超元域
> 优先级：中
> 创建时间：2026-02-23

---

## 问题

当前 MEMORY.md 是单文件，所有知识混在一起：
- 不同主题的记忆可能混淆
- 检索时不够精准
- 文件体积会越来越大

---

## 方案

按主题拆分 MEMORY.md：

```
memory/
├── MEMORY.md（索引+核心规则）
└── topics/
    ├── openclaw-config.md
    ├── multi-agent.md
    ├── browser-automation.md
    ├── external-services.md
    ├── workflow-rules.md
    └── ...
```

**核心思路**：
- MEMORY.md 只存索引和关键规则
- 详细内容按主题拆分到独立文件
- 按需加载，精准命中
- 每个主题独立膨胀，互不干扰

---

## 参考

视频作者将 15KB 的 MEMORY.md 拆分后变成 2.3KB（索引）+ 多个主题文件。

---

## 待研究

- [ ] 具体拆分规则
- [ ] 如何实现按需加载
- [ ] 与现有三层架构如何融合
