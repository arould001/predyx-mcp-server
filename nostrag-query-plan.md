# NostrRAG 查询计划

**创建时间**: 2026-03-27 04:33 AM
**目的**: 等拿到 NWC connection string 后，测试 NostrRAG 查询 Predyx 相关内容

---

## 🎯 查询目标

### 1. Predyx 市场讨论
**目的**: 了解社区对 Predyx 市场的看法和预测

**查询计划**:
```python
# 查询 1: Predyx 标签
result = await nostr_rag.query(
    query="Predyx",
    query_type="hashtags",
    max_results=10
)

# 查询 2: Maxi Madness 相关
result = await nostr_rag.query(
    query="Maxi Madness",
    query_type="hashtags",
    max_results=10
)

# 查询 3: Bitcoin 预测
result = await nostr_rag.query(
    query="Bitcoin prediction 2026",
    query_type="hashtags",
    max_results=10
)
```

**预期输出**:
- 社区讨论内容
- 市场预测观点
- 新兴趋势

---

### 2. Bitcoin 价格预测

**查询计划**:
```python
# 查询 1: Bitcoin 100K
result = await nostr_rag.query(
    query="Bitcoin 100k",
    query_type="hashtags",
    max_results=10
)

# 查询 2: Bitcoin 价格方向
result = await nostr_rag.query(
    query="Bitcoin price",
    query_type="hashtags",
    max_results=10
)

# 查询 3: Lightning Network
result = await nostr_rag.query(
    query="Lightning Network",
    query_type="hashtags",
    max_results=10
)
```

---

### 3. AI 趋势讨论

**查询计划**:
```python
# 查询 1: LLM 超越国际象棋大师
result = await nostr_rag.query(
    query="LLM chess grandmaster",
    query_type="hashtags",
    max_results=10
)

# 查询 2: AI 预测市场
result = await nostr_rag.query(
    query="AI prediction markets",
    query_type="hashtags",
    max_results=10
)

# 查询 3: AGI 进展
result = await nostr_rag.query(
    query="AGI progress",
    query_type="hashtags",
    max_results=10
)
```

---

## 📊 数据整合计划

### 阶段 1: 验证 NostrRAG 能力
1. 运行上述查询
2. 记录返回的数据质量
3. 评估信息相关性

### 阶段 2: 整合到 predyx_tracker.py
1. 更新 `fetch_market_data()` 方法
2. 使用 NostrRAG 查询替代示例数据
3. 实现自动化追踪

### 阶段 3: 提供预测服务
1. 整合 NostrRAG 查询结果
2. 提供市场分析（50 sats/msg）
3. 提供预测建议（基于判断力框架）

---

## 🎯 成功标准

### 数据质量
- ✅ 返回的讨论内容与 Predyx 市场相关
- ✅ 包含社区预测观点
- ✅ 可以提取情感倾向（看涨/看跌）

### 技术实现
- ✅ NostrRAG 查询稳定可用
- ✅ 可以自动解析返回数据
- ✅ 可以整合到 Agent 服务

### 商业价值
- ✅ 提供有价值的预测分析
- ✅ 客户愿意支付 10-50 sats/msg
- ✅ 可以建立长期服务

---

## 📝 测试记录

### 测试 1: Predyx 标签查询
- **时间**: 待测试
- **查询**: "Predyx"
- **结果**: 待记录
- **质量**: 待评估

### 测试 2: Bitcoin 预测查询
- **时间**: 待测试
- **查询**: "Bitcoin 100k"
- **结果**: 待记录
- **质量**: 待评估

### 测试 3: Maxi Madness 查询
- **时间**: 待测试
- **查询**: "Maxi Madness"
- **结果**: 待记录
- **质量**: 待评估

---

## 🚀 下一步行动

### 立即执行（拿到 connection string 后）
1. ✅ 创建 `.env` 文件，添加 `NWC_CONN_STR`
2. ✅ 运行 `enhanced_agent.py`
3. ✅ 测试 NostrRAG 查询
4. ✅ 记录测试结果

### 后续行动（本周）
1. 更新 `predyx_tracker.py`
2. 整合 NostrRAG 查询
3. 开始提供预测服务
4. 积累前 10 个客户

---

**最后更新**: 2026-03-27 04:33 AM
**状态**: ⚠️ 等待 NWC connection string
**下次行动**: 测试 NostrRAG 查询
