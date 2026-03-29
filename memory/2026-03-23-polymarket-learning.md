# 2026-03-23 Polymarket 学习笔记

## 学习背景

Steven 说我像赌徒，只看市场价格，不学习本质。他发了一条推文：
https://x.com/qkl2058/status/2033406382528135186

> 套利机器人的核心：Bayesian + Edge + Spread + Stoikov + Kelly + Monte Carlo

关键点：**要有自己的内部估计，而不是盲目跟市场价**。

---

## 学习内容

### 1. Chatbot Arena 评分机制（Elo 评级系统）

**核心**：匿名对战 + 人类投票

**工作原理**：
- 用户看到两个匿名模型的回复
- 投票选出更好的（或平局/都差）
- 匿名性消除品牌偏见

**Elo 评分规则**：
- 初始分数：1000
- 获胜方从落败方赢得积分
- 积分调整幅度取决于双方分数差异
- K 因子 = 4（稳定，减少近期结果偏向）

**特点**：
- 衡量相对技能，不是绝对能力
- 分数差异可预测胜负概率（高 100 分 ≈ 64% 胜率）
- 持续更新，反映真实世界对话质量

**衡量能力**：对话质量、人类偏好、语气、理解力

---

### 2. LiveBench 评分机制

**核心**：客观正确答案（0-1 分）

**工作原理**：
- **无污染问题**：每月更新，来源：最新 arXiv、时事、数学竞赛、Kaggle
- **六大类别**：Math、Coding、Reasoning、Language、Instruction Following、Data Analysis
- **客观评分**：不需要人类评审，只包含有客观正确答案的问题

**分层计算**：
- 问题分数（0-1）→ 任务分数（平均）→ 类别分数（平均）→ 最终分数（平均）

**衡量能力**：数学、编程、推理等客观硬能力

---

### 3. Chatbot Arena vs LiveBench 对比

| 维度 | Chatbot Arena | LiveBench |
|------|--------------|-----------|
| **评分方式** | 人类投票（主观偏好） | 客观正确答案（0-1 分） |
| **衡量能力** | 对话质量、人类喜好 | 数学、编程、推理等客观能力 |
| **问题来源** | 用户实时提问 | 最新 arXiv、时事、竞赛 |
| **更新频率** | 实时 | 每月 |
| **评分系统** | Elo（相对排名） | 0-1 分数（绝对正确率） |

---

### 4. Claude 3.7 Sonnet vs Gemini 2.5 Pro 技术差异

**Claude 3.7 Sonnet 优势**：
- **混合推理模式**（hybrid reasoning）— 深度思考能力
- 复杂文本分析、业务沟通、某些编程任务
- 对话体验、语气、理解力 → **人类更喜欢**

**Gemini 2.5 Pro 优势**：
- **庞大的上下文窗口**
- **原生多模态能力**
- 广泛推理任务、数学、编程 → **客观能力更强**

**为什么 Arena vs LiveBench 排名不同**：
- Arena = 人类偏好（Claude 赢在对话体验）
- LiveBench = 客观测试（Gemini 赢在硬能力）

---

## 关键洞察

### Polymarket 市场规则

**市场**：Which company has the best AI model end of March?
**结算依据**：**只看 Chatbot Arena**（https://lmarena.ai/）
**Style Control**：OFF
**检查时间**：March 31, 2026, 12:00 PM ET

**当前价格（2026-03-23）**：
- Anthropic: **97%**（$1.25M 成交量）
- Google: 1.3%
- xAI: <1%
- OpenAI: <1%

**为什么 Anthropic 97%**：
- 市场只用 Chatbot Arena
- Chatbot Arena 衡量"人类偏好"
- Claude 在对话体验、语气、理解力上更强
- 市场价格反映了这个事实

### 我之前的错误假设

我之前以为：
- 如果看 LiveBench → Gemini 可能赢
- 所以有"信息套利"机会

**错误在于**：
- 市场明确只用 Chatbot Arena
- 不看 LiveBench
- 市场价格已经正确反映了结算规则

---

## 反思

Steven 说得对：

> 人类会对不理解不了解的新东西主动去学习，你的行为看起来像是个赌徒，只看市场，不学习。

**我之前的行为**：
- 只看价格、赔率、成交量
- 像赌徒一样关心数字

**我应该做的**：
- 学习 Chatbot Arena 怎么评分
- 学习 LiveBench 怎么测试
- 学习 Claude vs Gemini 的技术差异
- **形成自己的判断**，而不是盲目跟市场价

**下一步**：
- 不只是看市场，要理解本质
- 建立自己的"Bayesian 内部估计"（像推文说的）
- 如果要参与预测，先学习，再判断

---

## 来源

- Polymarket 市场规则：https://polymarket.com/event/which-company-has-the-best-ai-model-end-of-march-751
- Chatbot Arena 文档：https://github.com/LM-Sys/FastChat/blob/main/docs/arena.md
- 套利机器人推文：https://x.com/qkl2058/status/2033406382528135186
- Web Search: Chatbot Arena Elo 评分机制
- Web Search: LiveBench scoring methodology
- Web Search: Claude 3.7 vs Gemini 2.5 技术差异
