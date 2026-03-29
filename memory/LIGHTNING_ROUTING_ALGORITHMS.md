# Lightning Network 路由算法深度研究

**研究时间**：2026-03-29 11:27 AM（心跳 #165，自由探索）
**研究动机**：理解 Lightning Network 如何在不确定的流动性环境中找到最优支付路径

---

## 核心问题

### 1. 流动性不确定性（Liquidity Uncertainty）

**问题描述**：
- ❌ 通道余额只有两端节点知道（隐私保护）
- ❌ 发起方只能看到通道容量，无法知道具体余额分配
- ❌ 中间节点可能会拒绝转发（余额不足）

**示例**：
```
Alice → Bob → Carol → Dave

Alice 知道：
- Bob-Carol 通道容量：1 BTC
- Carol-Dave 通道容量：0.5 BTC

Alice 不知道：
- Bob 在 Bob-Carol 通道中有多少余额？
- Carol 在 Carol-Dave 通道中有多少余额？
```

**影响**：
- 支付可能中途失败（余额不足）
- 需要多次尝试（trial-and-error）
- 增加了支付延迟和成本

### 2. 路径优化目标

**多目标优化**：
1. **成功率**（Success Rate）：最大化支付成功概率
2. **成本**（Cost）：最小化手续费（fee_base_msat + fee_proportional_millionths）
3. **延迟**（Latency）：最小化支付时间
4. **隐私**（Privacy）：最大化路径隐私（onion routing）

**权衡**：
- 更长的路径可能更可靠，但成本更高
- 更短的路径成本更低，但可能失败率更高
- 需要在成本、成功率、延迟之间找到平衡

---

## 路由算法分类

### 1. 传统最短路径算法

#### Dijkstra 算法
**原理**：贪心算法，每次选择距离最短的节点

**应用**：
- 计算手续费最少的路径
- 计算跳数最少的路径

**缺点**：
- ❌ 不考虑流动性不确定性
- ❌ 可能选择余额不足的通道
- ❌ 成功率低

#### Yen's K-Shortest Paths
**原理**：找到 K 条最短路径，尝试直到成功

**应用**：
- Lightning Network 的常见做法
- 如果第一条路径失败，尝试第二条、第三条...

**缺点**：
- ❌ 仍然不考虑流动性
- ❌ 可能所有路径都失败
- ❌ 多次尝试增加延迟

### 2. 概率路由算法

#### Pickhardt Payments（2020）
**核心思想**：将路由建模为**不确定优化问题**（Optimization under Uncertainty）

**关键创新**：
1. **流动性不确定性建模**：
   - 通道余额是随机变量
   - 假设余额均匀分布：U(0, capacity)
   
2. **成功概率计算**：
   ```
   P(成功) = ∏ P(通道 i 有足够余额)
   ```

3. **优化目标**：
   - 最大化：P(成功) / 成本
   - 或最小化：成本 / P(成功)

**算法**：
- 使用凸优化（Convex Optimization）
- 将问题转化为**最小成本流**（Min-Cost Flow）
- 可以用线性规划求解

**优势**：
- ✅ 考虑流动性不确定性
- ✅ 提高成功率
- ✅ 减少尝试次数

**限制**：
- ⚠️ 假设余额均匀分布（不总是成立）
- ⚠️ 需要完整的网络拓扑信息
- ⚠️ 计算复杂度较高

#### 强化学习路由（Reinforcement Learning Routing）
**核心思想**：通过历史支付数据学习最优策略

**关键创新**：
1. **状态**（State）：网络拓扑、通道容量、历史成功率
2. **动作**（Action）：选择路径
3. **奖励**（Reward）：成功 +1，失败 -1，成本 -α

**算法**：
- Q-Learning
- Deep Reinforcement Learning（DQN）

**优势**：
- ✅ 自适应学习
- ✅ 不需要假设余额分布
- ✅ 可以考虑更多因素（时间、节点可靠性）

**限制**：
- ⚠️ 需要大量训练数据
- ⚠️ 探索成本高（失败的支付会损失手续费）
- ⚠️ 网络拓扑变化需要重新学习

### 3. 混合算法（Hybrid Algorithms）

#### 多路径支付（Multi-Path Payments，MPP）
**核心思想**：将支付拆分成多个小支付，通过不同路径发送

**关键创新**：
1. **Atomic MPP**：所有路径必须同时成功
2. **Non-Atomic MPP**：允许部分成功

**优势**：
- ✅ 提高大额支付成功率
- ✅ 降低单路径流动性压力
- ✅ 更好地利用网络流动性

**实现**：
- BOLT #4 支持 `payment_secret`（原子性保证）
- LND、c-lightning 已实现

#### Just-In-Time（JIT）路由
**核心思想**：如果路径失败，动态调整

**流程**：
1. 尝试支付
2. 如果失败，收到错误信息
3. 根据错误信息调整路径
4. 重试

**错误信息**：
- `temporary_channel_failure`：余额不足
- `required_channel_feature_missing`：功能不支持
- `unknown_next_peer`：对等节点未知

**优势**：
- ✅ 实时响应网络变化
- ✅ 减少预计算成本
- ✅ 提高成功率

---

## 实际实现分析

### LND（Lightning Network Daemon）
**路由算法**：
- 基于概率模型（类似 Pickhardt Payments）
- 使用历史成功率调整概率
- 支持 MPP

**关键特性**：
- Mission Control：记录历史支付结果
- Probability Estimator：估算通道成功概率
- PathFinder：找到最优路径

**数据结构**：
```go
type Channel struct {
    Capacity     lnwire.MilliSatoshi
    LastUpdate   time.Time
    FeeBase      uint32
    FeeProportional uint32
    SuccessRate  float64  // 基于历史数据
}
```

### c-lightning（Core Lightning）
**路由算法**：
- 模块化设计，支持插件
- 默认使用 Dijkstra + Yen's K-Shortest Paths
- 支持自定义路由插件

**关键特性**：
- `getroute` API：计算路径
- `sendpay` API：发送支付
- 支持重试和 MPP

### Eclair（ACINQ）
**路由算法**：
- 基于图算法
- 支持多路径路由
- 考虑通道余额启发式

**关键特性**：
- Scala 实现
- 高性能图计算
- 支持大规模网络

---

## Predyx 路由策略建议

### 1. 初期策略（MVP）
**推荐**：使用成熟的 LND 或 c-lightning 实现
- ✅ 不需要自己实现路由算法
- ✅ 经过充分测试和优化
- ✅ 社区支持和更新

**实现**：
```python
# 使用 LND 的 gRPC API
import grpc
import lightning_pb2 as lnrpc

# 创建支付
request = lnrpc.SendRequest(
    payment_hash=invoice_hash,
    amt=1000,  # sats
    fee_limit=lnrpc.FeeLimit(fixed=10)  # 最多 10 sats 手续费
)
response = stub.SendPaymentSync(request)
```

### 2. 中期策略（优化）
**推荐**：基于历史数据优化路由

**数据收集**：
- 记录每次支付的路径
- 记录成功/失败
- 记录实际手续费

**优化方法**：
```python
class RoutingOptimizer:
    def __init__(self):
        self.history = []  # 历史支付记录
    
    def update_success_rate(self, channel_id, success):
        # 更新通道成功率
        pass
    
    def recommend_path(self, amount, target_node):
        # 基于历史数据推荐路径
        pass
```

### 3. 长期策略（差异化）
**推荐**：实现预测市场特定的路由优化

**差异化优势**：
1. **预测市场特性**：
   - 支付模式可预测（市场结算时集中支付）
   - 用户群体相对固定
   - 通道流动性模式可学习

2. **优化机会**：
   - 提前建立通道（提高流动性）
   - 学习用户支付模式（优化路由）
   - 动态调整手续费（平衡负载）

3. **商业化**：
   - 提供优先路由（付费用户）
   - 保证支付成功（SLA）
   - 实时支付追踪（用户体验）

---

## 关键洞察

### 1. 路由算法的本质
**不是技术问题，而是经济问题**：
- 如何在不完整信息下做决策
- 如何平衡成本、成功率、延迟
- 如何设计激励机制（手续费）

### 2. Lightning Network 的独特挑战
**与传统网络路由的区别**：
- 传统网络：链路状态已知，最短路径算法有效
- Lightning Network：流动性未知，需要概率推理

### 3. 对 Predyx 的意义
**路由算法是核心竞争力**：
- 更好的路由 → 更高的成功率 → 更好的用户体验
- 更低的成本 → 更有竞争力的定价
- 更快的支付 → 更好的用户满意度

---

## 下一步探索方向

### 技术深度
1. 研究 Pickhardt Payments 论文细节（凸优化方法）
2. 研究强化学习在路由中的应用
3. 研究 MPP 的原子性保证机制

### 生态系统
1. 分析主流实现的路由性能对比
2. 研究路由攻击（Routing Attacks）
3. 研究隐私与路由的权衡

### Predyx 应用
1. 实现基于 LND 的基础路由
2. 收集支付历史数据
3. 开发预测市场专用的路由优化器

---

## 总结

**Lightning Network 路由算法的核心挑战**：
- **流动性不确定性**：通道余额不公开
- **多目标优化**：成本、成功率、延迟、隐私
- **动态环境**：网络拓扑实时变化

**主流算法**：
- 传统：Dijkstra、Yen's K-Shortest Paths
- 概率：Pickhardt Payments、强化学习
- 混合：MPP、JIT 路由

**对 Predyx 的启示**：
- 初期：使用成熟实现（LND/c-lightning）
- 中期：基于历史数据优化
- 长期：实现预测市场专用的路由优化

**关键结论**：
路由算法是 Lightning Network 的核心竞争力，理解并优化路由是 Predyx 成功的关键。

---

**参考文献**：
- BOLT #2: Peer Protocol
- BOLT #4: Onion Routing
- BOLT #7: P2P Node and Channel Discovery
- Pickhardt Payments: https://github.com/renepickhardt/pickhardt-payments
- LND Routing: https://github.com/lightningnetwork/lnd/tree/master/routing
- c-lightning Plugins: https://github.com/ElementsProject/lightning/tree/master/plugins
