#!/usr/bin/env python3
"""
Simple Bayesian Router for Lightning Network

实现 Pickhardt Payments 论文中的贝叶斯更新机制：
- 使用均匀分布假设
- 维护每个通道的上下界
- 动态学习余额分布

参考文献：
- Pickhardt et al., "Optimally Reliable & Cheap Payment Flows on the Lightning Network", 2021
- arXiv:2107.05322
"""

import networkx as nx
from typing import Dict, Tuple, List, Optional
import heapq


class SimpleBayesianRouter:
    """
    基于贝叶斯更新的概率路由器
    
    核心思想：
    1. 每个通道维护余额的上下界 [lower, upper]
    2. 成功支付 x → 更新下界 lower = max(lower, x)
    3. 失败支付 x → 更新上界 upper = min(upper, x-1)
    4. 路径概率 = ∏ (upper_i - amount) / (upper_i - lower_i)
    """
    
    def __init__(self, graph: nx.Graph):
        """
        初始化路由器
        
        Args:
            graph: NetworkX 图，每条边需要有 'capacity' 属性
        """
        self.graph = graph
        self.lower_bounds: Dict[Tuple[int, int], int] = {}  # edge -> lower_bound
        self.upper_bounds: Dict[Tuple[int, int], int] = {}  # edge -> upper_bound
        
        # 初始化上下界
        for u, v, data in graph.edges(data=True):
            capacity = data['capacity']
            self.lower_bounds[(u, v)] = 0
            self.upper_bounds[(u, v)] = capacity
            # 双向通道（Lightning Network 特性）
            self.lower_bounds[(v, u)] = 0
            self.upper_bounds[(v, u)] = capacity
    
    def observe_success(self, edge: Tuple[int, int], amount: int):
        """
        观察到成功支付
        
        Args:
            edge: (u, v) 通道
            amount: 支付金额
        
        更新逻辑：
            lower_bound = max(lower_bound, amount)
        
        原因：
            成功支付 amount 意味着余额至少是 amount
        """
        old_lower = self.lower_bounds[edge]
        self.lower_bounds[edge] = max(old_lower, amount)
        
        # 更新反向通道（Lightning Network 双向通道）
        reverse_edge = (edge[1], edge[0])
        old_upper_reverse = self.upper_bounds[reverse_edge]
        capacity = self.graph.edges[edge]['capacity']
        # 正向余额 ≥ amount → 反向余额 ≤ capacity - amount
        self.upper_bounds[reverse_edge] = min(old_upper_reverse, capacity - amount)
    
    def observe_failure(self, edge: Tuple[int, int], amount: int):
        """
        观察到支付失败
        
        Args:
            edge: (u, v) 通道
            amount: 尝试支付的金额
        
        更新逻辑：
            upper_bound = min(upper_bound, amount - 1)
        
        原因：
            失败支付 amount 意味着余额 < amount
        """
        old_upper = self.upper_bounds[edge]
        self.upper_bounds[edge] = min(old_upper, amount - 1)
        
        # 更新反向通道
        reverse_edge = (edge[1], edge[0])
        old_lower_reverse = self.lower_bounds[reverse_edge]
        capacity = self.graph.edges[edge]['capacity']
        # 正向余额 < amount → 反向余额 > capacity - amount
        self.lower_bounds[reverse_edge] = max(old_lower_reverse, capacity - amount + 1)
    
    def edge_success_probability(self, edge: Tuple[int, int], amount: int) -> float:
        """
        计算单条边支付成功的概率
        
        Args:
            edge: (u, v) 通道
            amount: 支付金额
        
        Returns:
            成功概率 ∈ [0, 1]
        
        公式：
            P(余额 ≥ amount) = (upper - amount) / (upper - lower)
        
        假设：
            余额在 [lower, upper] 上均匀分布
        """
        lower = self.lower_bounds[edge]
        upper = self.upper_bounds[edge]
        
        # 边界检查
        if amount > upper:
            return 0.0  # 一定失败
        if amount <= lower:
            return 1.0  # 一定成功
        
        # 均匀分布概率
        range_size = upper - lower
        if range_size == 0:
            return 0.0  # 区间为空
        
        prob = (upper - amount) / range_size
        return max(0.0, min(1.0, prob))  # clamp to [0, 1]
    
    def path_success_probability(self, path: List[int], amount: int) -> float:
        """
        计算整条路径支付成功的概率
        
        Args:
            path: [u1, u2, ..., uk] 路径节点列表
            amount: 支付金额
        
        Returns:
            成功概率 ∈ [0, 1]
        
        公式：
            P(路径成功) = ∏ P(边_i 成功)
        
        假设：
            各边余额独立（独立性假设）
        """
        prob = 1.0
        
        for i in range(len(path) - 1):
            edge = (path[i], path[i+1])
            edge_prob = self.edge_success_probability(edge, amount)
            prob *= edge_prob
            
            # 提前终止（概率为 0）
            if prob == 0.0:
                break
        
        return prob
    
    def find_most_probable_path(
        self, 
        sender: int, 
        receiver: int, 
        amount: int,
        k: int = 10
    ) -> Optional[List[int]]:
        """
        找到最可能成功的路径
        
        Args:
            sender: 发送方节点
            receiver: 接收方节点
            amount: 支付金额
            k: 考虑的前 k 条最短路径
        
        Returns:
            最优路径 [sender, ..., receiver]，如果不存在则返回 None
        
        算法：
            1. 使用 Yen's K-Shortest Paths 算法找到前 k 条路径
            2. 计算每条路径的成功概率
            3. 返回概率最高的路径
        """
        try:
            # 使用 Yen's K-Shortest Paths（基于 Dijkstra）
            paths = list(nx.shortest_simple_paths(
                self.graph, 
                sender, 
                receiver,
                weight=lambda u, v, d: 1.0,  # 单位权重（跳数）
            ))
        except nx.NetworkXNoPath:
            return None
        
        # 限制到前 k 条路径
        paths = paths[:k]
        
        if not paths:
            return None
        
        # 计算每条路径的成功概率
        best_path = None
        best_prob = -1.0
        
        for path in paths:
            prob = self.path_success_probability(path, amount)
            if prob > best_prob:
                best_prob = prob
                best_path = path
        
        return best_path
    
    def find_path_with_retry(
        self,
        sender: int,
        receiver: int,
        amount: int,
        max_rounds: int = 10,
        verbose: bool = False
    ) -> Tuple[bool, int, List[List[int]]]:
        """
        轮次算法：找路径 → 尝试支付 → 观察结果 → 更新分布
        
        Args:
            sender: 发送方节点
            receiver: 接收方节点
            amount: 支付金额
            max_rounds: 最大尝试轮次
            verbose: 是否打印详细日志
        
        Returns:
            (success, rounds, tried_paths)
            - success: 是否成功
            - rounds: 实际轮次
            - tried_paths: 尝试过的路径列表
        
        这对应论文中的 "round-based algorithm of min-cost flow computations"
        """
        tried_paths = []
        
        for round_num in range(1, max_rounds + 1):
            # 1. 找到最可能成功的路径
            path = self.find_most_probable_path(sender, receiver, amount)
            
            if path is None:
                if verbose:
                    print(f"Round {round_num}: No path found")
                return False, round_num, tried_paths
            
            tried_paths.append(path)
            
            if verbose:
                prob = self.path_success_probability(path, amount)
                print(f"Round {round_num}: Path {[f'{u}' for u in path]} (prob={prob:.2%})")
            
            # 2. 模拟支付（这里用随机数模拟真实支付）
            # 在真实场景中，这里会调用 Lightning Network 节点 API
            success = self._simulate_payment(path, amount)
            
            if success:
                if verbose:
                    print(f"Round {round_num}: Payment successful!")
                
                # 3a. 更新分布（成功）
                for i in range(len(path) - 1):
                    edge = (path[i], path[i+1])
                    self.observe_success(edge, amount)
                
                return True, round_num, tried_paths
            else:
                # 3b. 找到失败的边（这里假设随机失败）
                # 在真实场景中，Lightning Network 会返回失败边
                failed_edge = self._find_failed_edge(path, amount)
                
                if verbose:
                    print(f"Round {round_num}: Payment failed at edge {failed_edge}")
                
                # 更新分布（失败）
                self.observe_failure(failed_edge, amount)
        
        # 达到最大轮次仍然失败
        return False, max_rounds, tried_paths
    
    def _simulate_payment(self, path: List[int], amount: int) -> bool:
        """
        模拟支付（用于测试）
        
        在真实场景中，这里会调用 Lightning Network 节点 API
        这里用简单的随机数模拟
        
        Args:
            path: 路径
            amount: 支付金额
        
        Returns:
            是否成功
        """
        import random
        
        # 计算路径的理论成功概率
        prob = self.path_success_probability(path, amount)
        
        # 以该概率返回成功
        return random.random() < prob
    
    def _find_failed_edge(self, path: List[int], amount: int) -> Tuple[int, int]:
        """
        找到失败的边（用于测试）
        
        在真实场景中，Lightning Network 会返回失败边
        这里返回概率最低的边
        
        Args:
            path: 路径
            amount: 支付金额
        
        Returns:
            失败的边 (u, v)
        """
        min_prob = 1.0
        failed_edge = None
        
        for i in range(len(path) - 1):
            edge = (path[i], path[i+1])
            prob = self.edge_success_probability(edge, amount)
            if prob < min_prob:
                min_prob = prob
                failed_edge = edge
        
        # 如果所有边概率都是 100%，随机选择一条
        if failed_edge is None:
            failed_edge = (path[0], path[1])
        
        return failed_edge
    
    def get_edge_info(self, edge: Tuple[int, int]) -> Dict[str, int]:
        """
        获取边的当前估计信息
        
        Args:
            edge: (u, v) 通道
        
        Returns:
            {
                'lower': 下界,
                'upper': 上界,
                'range': 区间大小,
                'capacity': 容量
            }
        """
        lower = self.lower_bounds[edge]
        upper = self.upper_bounds[edge]
        capacity = self.graph.edges[edge]['capacity']
        
        return {
            'lower': lower,
            'upper': upper,
            'range': upper - lower,
            'capacity': capacity
        }


def create_test_network() -> nx.Graph:
    """
    创建测试网络（模拟 Lightning Network）
    
    Returns:
        NetworkX Graph
    """
    G = nx.Graph()
    
    # 添加节点
    nodes = ['A', 'B', 'C', 'D', 'E']
    G.add_nodes_from(nodes)
    
    # 添加边（通道）
    edges = [
        ('A', 'B', 100),  # A-B 容量 100
        ('B', 'C', 150),  # B-C 容量 150
        ('C', 'D', 200),  # C-D 容量 200
        ('D', 'E', 120),  # D-E 容量 120
        ('A', 'C', 80),   # A-C 容量 80（替代路径）
        ('B', 'D', 90),   # B-D 容量 90（替代路径）
        ('A', 'E', 50),   # A-E 容量 50（直接路径）
    ]
    
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)
    
    # 为每条边添加随机余额（模拟真实情况）
    import random
    for u, v in G.edges():
        capacity = G.edges[u, v]['capacity']
        # 余额在 [0, capacity] 上均匀分布
        balance = random.randint(0, capacity)
        G.edges[u, v]['balance'] = balance  # 隐藏的真实值
        G.edges[v, u]['balance'] = capacity - balance  # 反向余额
    
    return G


def test_simple_router():
    """测试简单贝叶斯路由器"""
    print("=" * 60)
    print("Simple Bayesian Router 测试")
    print("=" * 60)
    
    # 1. 创建测试网络
    G = create_test_network()
    print(f"\n网络信息：")
    print(f"  节点数：{G.number_of_nodes()}")
    print(f"  边数：{G.number_of_edges()}")
    
    # 2. 初始化路由器
    router = SimpleBayesianRouter(G)
    
    # 3. 测试 1：单次路径查找
    print(f"\n测试 1：单次路径查找")
    sender, receiver, amount = 'A', 'E', 50
    path = router.find_most_probable_path(sender, receiver, amount)
    prob = router.path_success_probability(path, amount)
    print(f"  发送方：{sender}")
    print(f"  接收方：{receiver}")
    print(f"  金额：{amount}")
    print(f"  最优路径：{path}")
    print(f"  成功概率：{prob:.2%}")
    
    # 4. 测试 2：观察成功支付
    print(f"\n测试 2：观察成功支付")
    print(f"  支付前：{router.get_edge_info(('A', 'B'))}")
    router.observe_success(('A', 'B'), 30)
    print(f"  支付后（成功 30）：{router.get_edge_info(('A', 'B'))}")
    
    # 5. 测试 3：观察失败支付
    print(f"\n测试 3：观察失败支付")
    print(f"  支付前：{router.get_edge_info(('B', 'C'))}")
    router.observe_failure(('B', 'C'), 80)
    print(f"  支付后（失败 80）：{router.get_edge_info(('B', 'C'))}")
    
    # 6. 测试 4：轮次算法
    print(f"\n测试 4：轮次算法（轮次支付尝试）")
    # 重新初始化路由器
    router = SimpleBayesianRouter(G)
    sender, receiver, amount = 'A', 'E', 60
    success, rounds, tried_paths = router.find_path_with_retry(
        sender, receiver, amount, max_rounds=10, verbose=True
    )
    
    print(f"\n结果：")
    print(f"  成功：{success}")
    print(f"  轮次：{rounds}")
    print(f"  尝试路径数：{len(tried_paths)}")
    
    # 7. 测试 5：批量测试
    print(f"\n测试 5：批量测试（100 次随机支付）")
    import random
    
    router = SimpleBayesianRouter(G)
    successes = 0
    total_rounds = 0
    
    nodes = list(G.nodes())
    for _ in range(100):
        sender = random.choice(nodes)
        receiver = random.choice(nodes)
        while receiver == sender:
            receiver = random.choice(nodes)
        
        amount = random.randint(10, 100)
        
        success, rounds, _ = router.find_path_with_retry(
            sender, receiver, amount, max_rounds=10, verbose=False
        )
        
        if success:
            successes += 1
            total_rounds += rounds
    
    success_rate = successes / 100
    avg_rounds = total_rounds / successes if successes > 0 else 0
    
    print(f"  成功率：{success_rate:.2%}")
    print(f"  平均轮次（成功支付）：{avg_rounds:.2f}")
    
    print(f"\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_simple_router()
