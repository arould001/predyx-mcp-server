# Idea: Codex Deep Research Skill

> 来源：B站视频 AI超元域
> 优先级：中
> 创建时间：2026-02-23

---

## 问题

OpenClaw 自带搜索能力有限：
- Web Search 需要 Brave API
- Web Fetch 只是抓取网页
- 复杂深度研究无法满足

---

## 方案

把 **Codex 的 Deep Research** 做成 skill：

### 决策树

```
用户搜索请求
    ↓
有 URL？ → Web Fetch 抓取
    ↓
简单事实查询？ → Brave API
    ↓
复杂深度研究？ → Codex CLI 多轮搜索
```

### 输出

- 搜索结果 + 链接
- 详细分析
- 完整检索报告

---

## 使用方式

```
/codex 深入研究一下 AI agent 的最新进展
```

---

## 待研究

- [ ] skill 具体实现
- [ ] Codex CLI 调用方式
- [ ] 结果格式化
