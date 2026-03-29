# 预测市场知识体系

## 背景

Steven 说：预测市场套利需要庞大的数据分析工具，但我们工具链还没准备好。先建立知识储备，为未来做准备。

---

## 六个模型（完整链条）

### 1. Bayesian 更新（内部估计）

**核心**：根据新信息持续更新概率估计。

**公式**：
```
P(H|E) = [P(E|H) * P(H)] / P(E)
```

**实际例子**：美联储降息
- **先验**：P(降息) = 40%
- **新信息**：强劲就业报告（280k vs 185k）
- **似然**：
  - P(报告 | 降息) = 0.20（强劲就业反对降息）
  - P(报告 | 维持) = 0.55（强劲就业与维持一致）
  - 似然比 = 0.20 / 0.55 = 0.36
- **更新**：
  - 先验优势 = 0.40 / 0.60 = 0.667
  - 后验优势 = 0.667 × 0.36 = 0.24
  - **后验概率 = 19.4%**

**关键**：
- 一个强证据可以把信念从 40% 降到 19.4%
- 每个后验成为下一个先验
- 避免情绪化，理性合成所有信息

---

### 2. Edge（优势）

**核心**：判断自己是否有概率优势。

**公式**：
```
EV = (Win Rate × Average Win) - (Loss Rate × Average Loss)
```

**类型**：
- Information Edge（信息优势）——往往非法
- Price Edge（价格优势）——合法，来自研究和分析

**关键**：
- EV > 0 才有 Edge
- 没有 Edge → 不下注

---

### 3. Spread（价差）

**核心**：买入价和卖出价的差异，交易成本。

**公式**：
```
Spread = Ask - Bid
```

**关键**：
- 买入时支付更高的 Ask
- 卖出时获得更低的 Bid
- 开仓时就亏损 Spread
- Edge 必须足够大才能克服 Spread

---

### 4. Stoikov（库存风险）

**核心**：做市商的库存管理。

**Reservation Price**：
```
r = s - q * γ * σ² * (T - t)
```
- s = 当前市场中间价
- q = 当前库存（正数多头，负数空头）
- γ = 库存风险厌恶参数
- σ² = 价格方差
- (T - t) = 剩余时间

**机制**：
- q > 0（多头）→ r < s，鼓励卖出
- q < 0（空头）→ r > s，鼓励买入

**最优价差**：
```
spread = γ * σ² * (T - t) + (2/γ) * ln(1 + γ/κ)
```

---

### 5. Kelly 准则（仓位大小）

**核心**：最佳下注比例，最大化长期增长率。

**公式**：
```
f* = (p - q) / b
```
- f* = 最佳下注比例
- p = 获胜概率
- q = 失败概率（1 - p）
- b = 赔率

**关键**：
- 满仓 Kelly 风险很高 → 使用半仓 Kelly
- 没有优势（edge = 0）→ 不下注
- 大多数人下注太多，导致破产

---

### 6. Monte Carlo（风险评估）

**核心**：通过大量随机抽样来估算结果。

**工作流程**：
1. 定义可能输入的域
2. 从概率分布中随机生成输入
3. 对输出进行确定性计算
4. 汇总结果

**关键公式**：
```
n ≥ s²z²/ε²
```
- s² = 样本方差
- z = 置信水平对应的 z-score
- ε = 允许误差

**应用**：
- 风险评估
- 优化
- 数值积分

---

## 完整链条

```
Bayesian（内部估计）→ Edge（判断优势）→ Spread（交易成本）→ Stoikov（库存管理）→ Kelly（仓位大小）→ Monte Carlo（风险评估）
```

**决策流程**：
1. 用 Bayesian 建立内部估计（这个事件发生概率多少？）
2. 用 Edge 判断是否有优势（EV > 0 吗？）
3. 用 Spread 评估交易成本（成本可接受吗？）
4. 用 Stoikov 管理库存（库存过多/过少吗？）
5. 用 Kelly 决定仓位大小（应该下注多少？）
6. 用 Monte Carlo 评估风险（最坏情况是什么？）

---

## 其他知识

### LMSR（预测市场定价机制）

**核心公式**：
```
C(q) = b * ln(Σ e^(qi/b))
```
- b = 流动性参数
- 价格 = 概率，总和为 1
- AMM 总是作为交易对手方

### MiroFish（多智能体模拟）

**用途**：预测社会行为。

**工作流程**：
1. 图谱构建（GraphRAG）
2. 环境搭建（人设生成）
3. 开始模拟（双平台并行）
4. 报告生成（ReportAgent）
5. 深度互动（与 Agent 对话）

---

## 实战项目（GitHub）

### dylanpersonguy/Polymarket-Trading-Bot（53 stars）

**最全面的开源项目**，包含 7 种交易策略 + 鲸鱼追踪 + 风险管理。

#### 7 种策略

| # | 策略 | 类型 | Edge |
|---|------|------|------|
| 1 | Cross-Market Arbitrage | 套利 | 3%+ minimum edge |
| 2 | Mispricing Arbitrage | 套利 | 2%+ dislocation |
| 3 | Filtered High-Prob Convergence | 收敛 | 200 bps take profit |
| 4 | Market Making (Spread) | 做市商 | 40 bps spread |
| 5 | Momentum | 趋势跟踪 | 趋势延续 |
| 6 | AI Forecast | AI/研究 | 数据驱动 alpha |
| 7 | Copy Trading | 鲸鱼镜像 | 鲸鱼 alpha 提取 |

#### Filtered High-Prob Convergence（旗舰策略）

**7 重过滤**：
1. **流动性** ≥ $10K 市场流动性 + 深度
2. **概率带** 领先结果 65%-96%
3. **价差** Bid-ask spread ≤ 200 bps
4. **结算时间** 14 天内
5. **反追涨** 无近期 8%+ 价格飙升
6. **订单流** 订单簿失衡或净买入流 ≥ $500
7. **集群敞口** 相关市场 ≤ 25% 资本

**仓位大小**：
```
position = capital × 0.5% × setup_score
```

#### Whale Tracking（鲸鱼追踪）

**6 维评分**：
- 盈利能力（30%）
- 时机技巧（20%）
- 低滑点（15%）
- 一致性（15%）
- 市场选择（10%）
- 活跃度（10%）

**功能**：
- 自动发现盈利交易者（50+ 市场/周期）
- 16 倍并行扫描
- 鲸鱼集群检测
- 复制交易模拟器

#### 风险管理

- 钱包隔离（每个策略独立钱包）
- 日/周损失暂停（3% 日、8% 周）
- 全局紧急开关
- 默认纸上交易（需要 ENABLE_LIVE_TRADING=true）
- API 池轮换（绕过速率限制）

---

## 其他实战项目

### 0xFives/Polymarket-Arbitrage-Crypto-Trading-Bot-V3（238 stars）
- TypeScript
- 15 分钟市场交易机器人

### dev-protocol/polymarket-arbitrage-bot（233 stars）
- TypeScript
- Dump Hedge 策略
- RTDS 基础策略

### ent0n29/polybot（209 stars）
- Java
- "reverse-engineer every polymarket strategy"

### realfishsam/prediction-market-arbitrage-bot（125 stars）
- JavaScript
- Polymarket + Kalshi 套利
- 使用 pmxt

---

## 下一步

- 继续深化理解
- 等工具链准备好后应用
- 持续学习新策略

---

## 来源

- Steven 对话：2026-03-23
- 套利机器人推文：https://x.com/qkl2058/status/2033406382528135186
- pmxt: https://github.com/pmxt-dev/pmxt
- 套利机器人: https://github.com/sssorryMaker/polymarket-arbitrage-bot
- MiroFish: https://github.com/666ghj/MiroFish
- Monte Carlo: https://en.wikipedia.org/wiki/Monte_Carlo_method
- Bayesian 更新: Web Search
- Edge & Spread: Web Search
- Stoikov: Web Search (Avellaneda-Stoikov strategy)
- Kelly 准则: https://en.wikipedia.org/wiki/Kelly_criterion
