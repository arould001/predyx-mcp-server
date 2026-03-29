# 贝叶斯更新机制推导（2026-03-29）

**创建时间**：1:30 PM（第一百六十七次心跳，自由探索时间后续）

**目的**：推导 Lightning Network 通道余额的贝叶斯在线学习算法

---

## 核心问题

**场景**：
- 通道容量 `c` 已知（公开信息）
- 通道余额 `b` 未知（隐私保护）
- 通过观察支付成功/失败来学习余额分布

**目标**：
- 从初始分布 `P(b)` 开始
- 观察支付结果（成功/失败）
- 更新分布 `P(b | observation)`
- 逐步逼近真实余额

---

## 方法 1：均匀分布 → 离散贝叶斯更新

### 初始假设

**均匀分布**（最大熵）：
```
P(b) = 1/c,  b ∈ [0, c]
```

### 观察模型

**支付金额 `x` 的成功概率**：
```
P(success | b, x) = 1_{b ≥ x}
```

**失败概率**：
```
P(failure | b, x) = 1_{b < x}
```

### 后验更新

**成功支付 `x` 后**：
```
P(b | success, x) = P(success | b, x) * P(b) / P(success | x)
                  = 1_{b ≥ x} * (1/c) / (∫_x^c (1/c) db)
                  = 1_{b ≥ x} * (1/c) / ((c-x)/c)
                  = 1_{b ≥ x} / (c - x)
                  = Uniform(x, c)
```

**洞察**：成功支付 `x` 后，余额分布变为 `[x, c]` 上的均匀分布！

**失败支付 `x` 后**：
```
P(b | failure, x) = P(failure | b, x) * P(b) / P(failure | x)
                  = 1_{b < x} * (1/c) / (∫_0^x (1/c) db)
                  = 1_{b < x} * (1/c) / (x/c)
                  = 1_{b < x} / x
                  = Uniform(0, x)
```

**洞察**：失败支付 `x` 后，余额分布变为 `[0, x)` 上的均匀分布！

### 递推公式

**多轮观察后**：
```
Round 1: P_1(b) = Uniform(0, c)
观察成功 x_1: P_2(b) = Uniform(x_1, c)
观察失败 x_2: P_3(b) = Uniform(x_1, x_2)
观察成功 x_3: P_4(b) = Uniform(max(x_1, x_3), x_2)
...
```

**通用公式**：
```
P_k(b) = Uniform(lower_bound_k, upper_bound_k)

其中：
  lower_bound_k = max(成功的支付金额)
  upper_bound_k = min(失败的支付金额 + ε)
```

**收敛性**：
- 下界单调递增（每次成功支付提升下界）
- 上界单调递减（每次失败支付降低上界）
- 区间长度：`upper_bound_k - lower_bound_k` 单调递减
- **收敛到真实余额**（假设观察足够多）

### 计算复杂度

**每轮更新**：
- 成功：`lower_bound = max(lower_bound, x)` → **O(1)**
- 失败：`upper_bound = min(upper_bound, x)` → **O(1)**

**路径概率计算**：
```
P(路径成功 | x) = ∏ P(b_i ≥ x | observations_i)
              = ∏ (upper_bound_i - x) / (upper_bound_i - lower_bound_i)
```

**复杂度**：**O(k)**，`k` 是路径边数

**优势**：
- ✅ 极其简单（只需要维护上下界）
- ✅ 计算快速（常数时间更新）
- ✅ 直观易理解

**劣势**：
- ⚠️ 只使用边界信息（浪费中间观察）
- ⚠️ 均匀分布假设可能不真实
- ⚠️ 不考虑时间衰减（余额会变化）

---

## 方法 2：Beta 分布 → 连续贝叶斯更新

### 为什么 Beta 分布？

**Beta 分布特性**：
- 定义域：`[0, 1]`（适合表示比例）
- 参数：`α, β > 0`（形状参数）
- PDF：`P(p) = p^{α-1} (1-p)^{β-1} / B(α, β)`
- **共轭先验**：对二项分布（成功/失败）

**应用到通道余额**：
```
p = b / c  （余额比例）
p ~ Beta(α, β)
```

### 初始分布

**无信息先验**（最大熵）：
```
p ~ Beta(α=1, β=1) = Uniform(0, 1)
```

**对应余额分布**：
```
b = p * c
P(b) = Uniform(0, c)
```

### 观察模型（Bernoulli 似然）

**支付 `x` 的成功概率**：
```
P(success | p, x/c) = 1_{p ≥ x/c}
```

**但 Bernoulli 似然需要概率输出，而不是确定性的！**

**改进：使用概率观察模型**：
```
假设真实余额是 p_true
观察到的"成功"是有噪声的：
  P(observed_success | p_true, x/c) = σ(p_true - x/c)

其中 σ 是 sigmoid 函数：
  σ(z) = 1 / (1 + exp(-z))
```

**为什么需要噪声？**
- ✅ 避免确定性更新（Beta 分布需要概率观察）
- ✅ 反映不确定性（网络可能有延迟、错误）
- ✅ 数学上更优雅（连续可微）

### 后验更新

**观察到成功支付 `x/c` 后**：
```
P(p | success, x/c) ∝ P(success | p, x/c) * P(p)
                    ∝ σ(p - x/c) * Beta(α, β)

近似更新（忽略 sigmoid）：
  α' = α + 1
  β' = β
```

**观察到失败支付 `x/c` 后**：
```
P(p | failure, x/c) ∝ P(failure | p, x/c) * P(p)
                    ∝ (1 - σ(p - x/c)) * Beta(α, β)

近似更新：
  α' = α
  β' = β + 1
```

**精确更新**（使用数值积分）：
```
α' = α + ∫ p * P(observation | p) * Beta(α, β) dp / Z
β' = β + ∫ (1-p) * P(observation | p) * Beta(α, β) dp / Z

其中 Z 是归一化常数
```

### 计算复杂度

**每轮更新**：
- 近似：**O(1)**（只更新计数）
- 精确：**O(n)**（数值积分，`n` 是积分点数）

**路径概率计算**：
```
P(路径成功 | x) = ∏ E[p_i ≥ x/c_i]
              = ∏ E[1_{p_i ≥ x/c_i}]
              = ∏ (1 - CDF_i(x/c_i))

其中 CDF_i 是 Beta 分布的累积分布函数
```

**Beta CDF**：
```
CDF(p; α, β) = I(p; α, β)
             = ∫_0^p t^{α-1} (1-t)^{β-1} dt / B(α, β)
```

**复杂度**：**O(k)**，但每边需要计算 Beta CDF

**优势**：
- ✅ 更精确（使用所有观察）
- ✅ 理论优雅（共轭先验）
- ✅ 不确定性量化（Beta 分布方差）

**劣势**：
- ⚠️ 计算更复杂（Beta CDF）
- ⚠️ 需要假设 sigmoid 噪声
- ⚠️ 可能过度参数化

---

## 方法 3：Dirichlet 分布 → 多通道联合学习

### 为什么需要联合学习？

**问题**：
- Lightning Network 通道余额不是独立的！
- 支付经过多个通道 → 联合约束
- 需要建模通道之间的依赖关系

**例子**：
```
通道 A-B 容量：1000 sats
通道 B-C 容量：500 sats

如果 A-B 余额 = 800 sats（从 A 角度）
那么 B-C 余额 ≤ 500 sats（从 B 角度）

约束：b_{AB} + b_{BA} = 1000
      b_{BC} + b_{CB} = 500
```

### Dirichlet 分布

**定义**：
```
(p_1, ..., p_K) ~ Dirichlet(α_1, ..., α_K)

约束：∑ p_i = 1
PDF：P(p) = ∏ p_i^{α_i - 1} / B(α)
```

**应用到多通道**：
```
假设 K 个通道共享总容量 C_total
(p_1, ..., p_K) 表示每个通道的余额比例
(p_1, ..., p_K) ~ Dirichlet(α_1, ..., α_K)
```

### 观察模型

**多通道支付成功**：
```
路径：e_1 → e_2 → ... → e_k
支付金额：x

成功条件：∀ i, b_i ≥ x

P(success | p, x) = ∏ 1_{p_i * c_i ≥ x/C_total}
```

### 后验更新

**成功支付后**：
```
α_i' = α_i + 1 / k  （均匀分配）
```

**失败支付后**：
```
假设在边 e_j 失败：
α_j' = α_j - λ  （惩罚失败边，λ > 0 是学习率）
```

### 计算复杂度

**每轮更新**：**O(k)**，`k` 是通道数

**路径概率计算**：
```
P(路径成功 | x) = E[∏ 1_{b_i ≥ x}]
                = ∫ ... ∫ (∏ 1_{p_i c_i ≥ x}) * Dirichlet(α) dp
```

**复杂度**：**O(exp(k))**（高维积分）

**问题**：指数复杂度，不可行！

**解决方案**：
1. **独立性近似**：假设通道独立 → Beta 分布
2. **蒙特卡洛采样**：采样估计期望
3. **变分推断**：近似后验

---

## 推荐方案：混合方法

### 阶段 1：快速原型（方法 1）

**实现**：
```python
class SimpleBayesianRouter:
    def __init__(self):
        self.lower_bounds = {}  # edge -> lower_bound
        self.upper_bounds = {}  # edge -> upper_bound
    
    def observe_success(self, edge, amount):
        old_lower = self.lower_bounds.get(edge, 0)
        self.lower_bounds[edge] = max(old_lower, amount)
    
    def observe_failure(self, edge, amount):
        old_upper = self.upper_bounds.get(edge, capacity[edge])
        self.upper_bounds[edge] = min(old_upper, amount - 1)
    
    def path_probability(self, path, amount):
        prob = 1.0
        for edge in path:
            lower = self.lower_bounds.get(edge, 0)
            upper = self.upper_bounds.get(edge, capacity[edge])
            prob *= (upper - amount) / (upper - lower)
        return prob
```

**复杂度**：
- 更新：**O(1)**
- 查询：**O(k)**

**优势**：
- ✅ 极其简单（< 50 行代码）
- ✅ 计算快速
- ✅ 易于调试

### 阶段 2：精确版本（方法 2）

**实现**：
```python
from scipy.stats import beta

class BetaBayesianRouter:
    def __init__(self):
        self.alpha = {}  # edge -> α
        self.beta = {}   # edge -> β
    
    def observe_success(self, edge, amount):
        # 近似更新：增加成功计数
        self.alpha[edge] = self.alpha.get(edge, 1) + 1
    
    def observe_failure(self, edge, amount):
        # 近似更新：增加失败计数
        self.beta[edge] = self.beta.get(edge, 1) + 1
    
    def path_probability(self, path, amount):
        prob = 1.0
        for edge in path:
            α = self.alpha.get(edge, 1)
            β = self.beta.get(edge, 1)
            # 计算 P(余额 ≥ amount)
            p_success = 1 - beta.cdf(amount / capacity[edge], α, β)
            prob *= p_success
        return prob
```

**复杂度**：
- 更新：**O(1)**
- 查询：**O(k)**（每边需要 Beta CDF）

**优势**：
- ✅ 更精确
- ✅ 量化不确定性（Beta 分布方差）
- ✅ 理论优雅

**劣势**：
- ⚠️ 需要 `scipy.stats` 依赖
- ⚠️ Beta CDF 计算稍慢

---

## 实验验证计划

### 合成数据测试

**步骤 1：生成模拟网络**：
```python
import networkx as nx

# 创建随机图
G = nx.random_graphs.barabasi_albert_graph(100, 3)

# 为每条边分配容量
for edge in G.edges():
    G.edges[edge]['capacity'] = random.randint(100, 1000)
    G.edges[edge]['balance'] = random.randint(0, G.edges[edge]['capacity'])
```

**步骤 2：测试不同方法**：
```python
# 方法 1：最短路径（baseline）
paths_dijkstra = nx.shortest_path(G, sender, receiver, weight='fee')

# 方法 2：静态概率路由（我的推导）
paths_static = probabilistic_routing(G, sender, receiver, amount)

# 方法 3：贝叶斯更新（论文方法）
router = SimpleBayesianRouter()
for round in range(10):
    path = router.find_best_path(G, sender, receiver, amount)
    success = try_payment(path, amount)
    router.update(path, success)
```

**步骤 3：评估指标**：
- 成功率（最终支付成功的比例）
- 平均轮次（成功需要的重试次数）
- 支付规模（能处理的最大支付）
- 计算时间（每轮的求解时间）

### 真实数据测试

**步骤 1：获取 Lightning Network 快照**：
```bash
# 下载网络拓扑（公开数据）
wget https://ln.github.io/network_snapshots/latest.json
```

**步骤 2：模拟支付流**：
```python
# 生成随机支付请求
payments = [
    (random_node(), random_node(), random_amount())
    for _ in range(1000)
]

# 测试不同方法
for sender, receiver, amount in payments:
    path = router.find_path(sender, receiver, amount)
    result = simulate_payment(path, amount)
    router.update(path, result)
```

**步骤 3：对比论文结果**：
- 论文报告：单数字轮次成功
- 我的实现：验证是否也能单数字轮次成功

---

## 关键洞察总结

### 理论洞察

1. **均匀分布 → 贝叶斯区间**：
   - 最简单的动态学习
   - 只维护上下界
   - 计算复杂度 O(1)

2. **Beta 分布 → 概率建模**：
   - 更精确的估计
   - 量化不确定性
   - 需要数值计算（Beta CDF）

3. **Dirichlet 分布 → 联合建模**：
   - 建模通道依赖
   - 指数复杂度（不可行）
   - 需要近似方法

### 工程洞察

1. **先实现简单版本**：
   - 均匀分布 + 区间更新
   - < 50 行代码
   - 快速验证想法

2. **再优化精确版本**：
   - Beta 分布 + 贝叶斯更新
   - 需要科学计算库
   - 更好的性能

3. **实验驱动迭代**：
   - 先跑合成数据
   - 再测试真实数据
   - 对比论文结果

### 对 Predyx 的启发

1. **实现优先级**：
   ```
   第一优先级：SimpleBayesianRouter（1 小时）
   第二优先级：BetaBayesianRouter（2 小时）
   第三优先级：真实数据测试（3 小时）
   ```

2. **性能预期**：
   - 成功率：接近 100%（论文验证）
   - 轮次：单数字（1-9 轮）
   - 计算时间：< 1 秒/轮

3. **竞争优势**：
   - 大多数实现没有贝叶斯更新
   - 动态学习 > 静态估计
   - 论文方法已经验证有效

---

## 下一步行动

**立即行动**（优先级 P0）：
1. ✅ **创建贝叶斯更新推导文档**（本文档，1 小时）← **已完成！**
2. 🔜 **实现 SimpleBayesianRouter**（1 小时，< 100 行代码）

**本周行动**（优先级 P1）：
1. 🔜 **实现 BetaBayesianRouter**（2 小时）
2. 🔜 **合成数据测试**（2 小时）
3. 🔜 **对比论文结果**（1 小时）

**下周行动**（优先级 P2）：
1. 🔜 **集成到 Predyx MCP Server**（2 小时）
2. 🔜 **真实数据测试**（3 小时）
3. 🔜 **撰写技术博客**（2 小时）

---

## 文件位置

- **本文档**：`memory/BAYESIAN_UPDATE_DERIVATION_2026-03-29.md`（12,567 bytes）
- **论文验证**：`memory/PICKHARDT_PAPER_VERIFICATION_2026-03-29.md`（8,895 bytes）
- **理论重构**：`memory/PICKHARDT_THEORY_RECONSTRUCTION.md`（6,533 bytes）
- **总计**：27,995 bytes

---

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-03-29 | 贝叶斯更新机制完整推导（均匀分布 + Beta 分布 + Dirichlet 分布） |
| 2026-03-29 | Pickhardt Payments 论文验证完成 |
| 2026-03-29 | Pickhardt Payments 理论重构完成 |
