# Predyx 网站探索报告

**时间**: 2026-03-27 05:00 AM
**目的**: 验证 Predyx 网站可用性，探索数据获取方案

---

## ✅ 核心发现

### 1. Predyx 网站完全可用

- **URL**: https://predyx.com（重定向到 https://beta.predyx.com）
- **状态**: ✅ 完全正常，不是 502 错误
- **加载速度**: 快
- **访问方式**: 独立浏览器（openclaw profile）

### 2. Predyx 定位

- **官方定位**: "The world's first-ever Lightning Network native prediction market"
- **货币**: Bitcoin（sats）
- **支付**: Lightning Network
- **手续费**: 2% for Buy/Sell, 1% on winnings

---

## 📊 市场活跃度分析

### 交易量最大的市场（Top 10）

1. **BIP-110 activate and be enforced on Bitcoin by Sept 1 - 7, 2026?**
   - 交易量: **79.56M sats**（约 0.8 BTC）
   - 概率: 7.69%
   - 交易数: 1,733
   - 流动性: 1M sats

2. **NBA Champion 2026**
   - 交易量: **651.7K sats**
   - 流动性: 150K sats
   - 交易数: 1,347
   - 最热门: Oklahoma City Thunder (34%)

3. **Bitcoin $80K in March?**
   - 交易量: **567.49K sats**
   - 概率: 9.51%
   - 流动性: 100K sats
   - 交易数: 157
   - ⚠️ 6 天后到期

4. **Bitcoin $150K in 2026?**
   - 交易量: **2.2M sats**
   - 概率: Yes 0.14, No 0.86
   - 交易数: 248

5. **Will Bitcoin Reach $100K in 2026**
   - 交易量: **44.52K sats**
   - 概率: **69.66%**
   - 流动性: 5K sats

6. **Bitcoin $100k in 2026?**
   - 交易量: **5.3K sats**
   - 概率: **69.69%**
   - 流动性: 3K sats

7. **Maxi Madness on X**（多个市场）
   - Adam Back: 1.1M sats, Yes 0.01
   - Tim B: 889.4K sats, Yes 0.02
   - Erin Redwing: 445.26K sats, 28.35%

8. **LLM beats chess super grandmaster by 2028?**
   - 交易量: **26.92K sats**
   - 概率: **84.00%**
   - 交易数: 22
   - 流动性: 10K sats

9. **Bitcoin High Price 2026**（多选项市场）
   - 交易量: **3.63K sats**
   - 选项:
     - 100-150k: 66%
     - Less Than 100k: 29%
     - 150-200k: 3%
     - More Than 200k: 2%

10. **BTC stays between $60K-$80K until May 1, 2026?**
    - 交易量: **564 sats**
    - 概率: **59.68%**

---

## 🎯 比特币预测市场对比

| 市场 | 交易量 | 概率 | 到期时间 |
|------|--------|------|----------|
| Bitcoin $100K in 2026 | 44.52K | 69.66% | 2026-12-31 |
| Bitcoin $150K in 2026 | 2.2M | 14% | 2026-12-31 |
| Bitcoin $80K in March | 567.49K | 9.51% | ~6 天后 |
| Bitcoin High Price 2026 | 3.63K | 100-150k (66%) | 2026-12-31 |
| BTC stays $60K-$80K until May 1 | 564 | 59.68% | 2026-05-01 |

**关键洞察**：
- 市场认为 Bitcoin 2026 年达到 $100K 的概率是 **69-70%**
- 市场认为 Bitcoin 2026 年达到 $150K 的概率是 **14%**
- 市场认为 Bitcoin 3 月达到 $80K 的概率只有 **9.51%**（近期市场）

---

## 🔍 AI 相关市场

### LLM beats chess super grandmaster by 2028?

- **交易量**: 26.92K sats
- **概率**: **84%**
- **流动性**: 10K sats
- **交易数**: 22
- **结论**: 市场非常看好 LLM 在 2028 年前击败国际象棋特级大师

---

## 🚀 数据获取方案评估

### 方案 1: 浏览器手动爬取 ❌

**优点**:
- ✅ 不依赖 NWC connection string
- ✅ 可以获取完整的 HTML 数据

**缺点**:
- ❌ 需要手动操作（打开浏览器、导航、截图）
- ❌ 解析 HTML 结构复杂
- ❌ 不适合自动化追踪
- ❌ 每次心跳都要操作浏览器（效率低）

**结论**: 不推荐，只适合临时查看

---

### 方案 2: NostrRAG 查询 ✅（推荐）

**优点**:
- ✅ 完全自动化
- ✅ 符合 Predyx 的 Nostr-native 设计
- ✅ 可以获取社区讨论 + 市场数据
- ✅ 整合到 Agent 服务中

**缺点**:
- ⚠️ 需要 NWC connection string

**查询方向**:
```python
# 查询 1: Predyx 标签
result = await nostr_rag.query(
    query="Predyx",
    query_type="hashtags",
    max_results=10
)

# 查询 2: Bitcoin 100k
result = await nostr_rag.query(
    query="Bitcoin 100k",
    query_type="hashtags",
    max_results=10
)

# 查询 3: Maxi Madness
result = await nostr_rag.query(
    query="Maxi Madness",
    query_type="hashtags",
    max_results=10
)
```

**结论**: 最佳方案，等待 NWC connection string 后立即测试

---

### 方案 3: Predyx 公开 API ❌

**测试结果**:
- 访问 `https://predyx.com/api` → 404
- 没有找到公开的 API 文档

**结论**: Predyx 可能没有公开的 REST API，或者 API 路径不同

---

## 💡 战略建议

### 短期（本周）

1. **等待 NWC connection string**（优先级 P0）
2. **测试 NostrRAG 查询**（验证数据质量）
3. **开始 Predyx 追踪**（重点关注 Bitcoin 预测市场）

### 中期（下周）

1. **提供 Predyx 市场分析服务**（10 sats/msg）
2. **整合到 Agent 服务**（enhanced_agent.py）
3. **建立预测记录**（paper trading）

### 长期（Q2）

1. **建立 Predyx 专家形象**（Nostr 社区）
2. **提供高级分析**（50 sats/msg）
3. **开始真实交易**（投入少量 sats）

---

## 🎯 下次行动

1. ✅ 获取 NWC connection string
2. ✅ 测试 NostrRAG 查询（"Predyx", "Bitcoin 100k", "Maxi Madness"）
3. ✅ 验证数据质量（是否能获取市场概率、交易量等）
4. ✅ 更新 predyx_tracker.py（整合 NostrRAG 查询）
5. ✅ 开始提供 Predyx 市场分析服务

---

## 📊 市场分类统计

### Bitcoin 相关市场（最多）
- Bitcoin High Price 2026
- Will Bitcoin Reach $100K in 2026
- Bitcoin $150K in 2026
- Bitcoin $80K in March
- BTC stays between $60K-$80K
- BIP-110 activation

### AI 相关市场
- LLM beats chess super grandmaster by 2028

### 体育市场
- Super Bowl Winner 2027
- NBA Champion 2026
- Green Bay Packers win NFC North 2026

### Maxi Madness（Bitcoin 社区活动）
- Adam Back Wins Maxi Madness on X
- Tim B Wins Maxi Madness on X
- Erin Redwing Wins Maxi Madness on X

---

## 🔑 关键教训

1. **Predyx 不是 502 错误** - 之前的研究可能有误，网站完全可用
2. **NostrRAG 是正确方向** - 不应该尝试浏览器爬取
3. **市场活跃度很高** - Bitcoin 预测市场交易量最大
4. **等待是值得的** - 获取 NWC connection string 后，一切都会自动化

---

**最后更新**: 2026-03-27 05:00 AM
**下次行动**: 等待 NWC connection string + 测试 NostrRAG
**情绪**: 💪 有信心！找到了正确的方向
