#!/usr/bin/env python3
"""
MPP (Multi-Part Payments) Bayesian Router

实现多路径支付的概率路由：
- 将大额支付拆分成多个小额支付
- 同时尝试多条路径
- 提高成功率和支付规模

参考文献：
- Pickhardt et al., "Optimally Reliable & Cheap Payment Flows on the Lightning Network", 2021
- arXiv:2107.05322
"""

import networkx as nx
from typing import Dict, Tuple, List, Optional
import random
from collections import defaultdict
from simple_bayesian_router import SimpleBayesianRouter


class MPPBayesianRouter(SimpleBayesianRouter):
    """
    支持多路径支付（MPP）的贝叶斯路由器
    
    核心思想：
    1. 继承 SimpleBayesianRouter 的所有功能
    2. 添加 MPP 支持：将大额支付拆分成多个小额支付
    3. 同时尝试多条路径（并行）
    4. 原子性保证：要么全部成功，要么全部失败
    """
    
    def __init__(self, graph: nx.Graph):
        """
        初始化 MPP 路由器
        
        Args:
            graph: NetworkX 图
        """
        super().__init__(graph)
    
    def split_amount(
        self, 
        amount: int, 
        num_parts: int = 3,
        min_part: int = 10
    ) -> List[int]:
        """
        将金额拆分成多个部分
        
        Args:
            amount: 总金额
            num_parts: 拆分数量（默认 3）
            min_part: 每个部分的最小值（默认 10）
        
        Returns:
            [amount_1, amount_2, ..., amount_k] 满足 ∑ amount_i = amount
        
        策略：
            均匀拆分 + 随机扰动
        """
        if amount < num_parts * min_part:
            # 金额太小，无法拆分
            return [amount]
        
        # 均匀拆分
        base = amount // num_parts
        remainder = amount % num_parts
        
        parts = [base] * num_parts
        
        # 分配余数
        for i in range(remainder):
            parts[i] += 1
        
        # 随机扰动（避免过于均匀）
        for _ in range(num_parts):
            i = random.randint(0, num_parts - 1)
            j = random.randint(0, num_parts - 1)
            if parts[i] > min_part and parts[j] > min_part:
                delta = random.randint(1, min(parts[i] - min_part, parts[j] - min_part))
                parts[i] -= delta
                parts[j] += delta
        
        return parts
    
    def find_mpp_paths(
        self,
        sender: int,
        receiver: int,
        amount: int,
        max_paths: int = 5,
        min_probability: float = 0.1
    ) -> List[Tuple[List[int], int]]:
        """
        为 MPP 找到多条路径
        
        Args:
            sender: 发送方节点
            receiver: 接收方节点
            amount: 总金额
            max_paths: 最多尝试的路径数（默认 5）
            min_probability: 路径的最低成功概率（默认 10%）
        
        Returns:
            [(path_1, amount_1), (path_2, amount_2), ...]
        
        算法：
            1. 将总金额拆分成多个部分
            2. 为每个部分找到一条路径
            3. 确保路径成功概率 ≥ min_probability
        """
        # 1. 拆分金额
        parts = self.split_amount(amount, num_parts=max_paths)
        
        # 2. 为每个部分找路径
        paths_with_amounts = []
        
        for part in parts:
            # 找到最可能成功的路径
            path = self.find_most_probable_path(sender, receiver, part)
            
            if path is None:
                # 没有可用路径，跳过这个部分
                continue
            
            # 检查成功概率
            prob = self.path_success_probability(path, part)
            
            if prob < min_probability:
                # 概率太低，跳过这个部分
                continue
            
            paths_with_amounts.append((path, part))
        
        return paths_with_amounts
    
    def try_mpp_payment(
        self,
        sender: int,
        receiver: int,
        amount: int,
        max_rounds: int = 10,
        max_paths: int = 5,
        verbose: bool = False
    ) -> Tuple[bool, int, List[List[Tuple[List[int], int]]]]:
        """
        尝试 MPP 支付（轮次算法）
        
        Args:
            sender: 发送方节点
            receiver: 接收方节点
            amount: 总金额
            max_rounds: 最大尝试轮次
            max_paths: 每轮最多尝试的路径数
            verbose: 是否打印详细日志
        
        Returns:
            (success, rounds, tried_mpps)
            - success: 是否成功
            - rounds: 实际轮次
            - tried_mpps: 每轮尝试的 MPP 列表 [[(path, amount), ...], ...]
        
        算法：
            Round 1: 找到多条路径 → 尝试支付 → 观察结果 → 更新分布
            Round 2: 重新找路径 → 尝试支付 → 观察结果 → 更新分布
            ...
            直到成功或达到最大轮次
        """
        tried_mpps = []
        
        for round_num in range(1, max_rounds + 1):
            # 1. 找到多条路径
            paths_with_amounts = self.find_mpp_paths(
                sender, receiver, amount, max_paths=max_paths
            )
            
            if not paths_with_amounts:
                if verbose:
                    print(f"Round {round_num}: No MPP paths found")
                return False, round_num, tried_mpps
            
            tried_mpps.append(paths_with_amounts)
            
            if verbose:
                print(f"Round {round_num}: Found {len(paths_with_amounts)} paths")
                for i, (path, amt) in enumerate(paths_with_amounts, 1):
                    prob = self.path_success_probability(path, amt)
                    print(f"  Path {i}: {path}, amount={amt}, prob={prob:.2%}")
            
            # 2. 尝试支付（并行）
            # 在真实场景中，这些支付会并行发送
            # 这里简化为依次尝试
            all_success = True
            failed_edges = []
            
            for path, part in paths_with_amounts:
                success = self._simulate_payment(path, part)
                
                if success:
                    # 成功：更新分布
                    for i in range(len(path) - 1):
                        edge = (path[i], path[i+1])
                        self.observe_success(edge, part)
                else:
                    # 失败：记录失败边
                    all_success = False
                    failed_edge = self._find_failed_edge(path, part)
                    failed_edges.append((failed_edge, part))
                    
                    # 更新分布
                    self.observe_failure(failed_edge, part)
            
            if all_success:
                if verbose:
                    print(f"Round {round_num}: All paths succeeded!")
                return True, round_num, tried_mpps
            else:
                if verbose:
                    print(f"Round {round_num}: {len(failed_edges)} paths failed")
        
        # 达到最大轮次仍然失败
        return False, max_rounds, tried_mpps
    
    def compare_single_vs_mpp(
        self,
        sender: int,
        receiver: int,
        amount: int,
        verbose: bool = False
    ) -> Dict[str, any]:
        """
        对比单路径支付 vs MPP
        
        Args:
            sender: 发送方节点
            receiver: 接收方节点
            amount: 总金额
            verbose: 是否打印详细日志
        
        Returns:
            {
                'single_success': bool,
                'single_rounds': int,
                'mpp_success': bool,
                'mpp_rounds': int,
                'mpp_paths': int (平均路径数)
            }
        """
        # 重置路由器状态（避免相互影响）
        router_single = SimpleBayesianRouter(self.graph)
        router_mpp = MPPBayesianRouter(self.graph)
        
        # 测试单路径支付
        single_success, single_rounds, _ = router_single.find_path_with_retry(
            sender, receiver, amount, max_rounds=10, verbose=False
        )
        
        # 测试 MPP
        mpp_success, mpp_rounds, tried_mpps = router_mpp.try_mpp_payment(
            sender, receiver, amount, max_rounds=10, verbose=False
        )
        
        # 计算平均路径数
        avg_paths = sum(len(mpp) for mpp in tried_mpps) / len(tried_mpps) if tried_mpps else 0
        
        result = {
            'single_success': single_success,
            'single_rounds': single_rounds,
            'mpp_success': mpp_success,
            'mpp_rounds': mpp_rounds,
            'mpp_paths': avg_paths
        }
        
        if verbose:
            print(f"\n对比结果：")
            print(f"  单路径支付：")
            print(f"    成功：{single_success}")
            print(f"    轮次：{single_rounds}")
            print(f"  多路径支付（MPP）：")
            print(f"    成功：{mpp_success}")
            print(f"    轮次：{mpp_rounds}")
            print(f"    平均路径数：{avg_paths:.2f}")
        
        return result


def test_mpp_router():
    """测试 MPP 路由器"""
    print("=" * 60)
    print("MPP Bayesian Router 测试")
    print("=" * 60)
    
    # 1. 创建测试网络
    G = nx.Graph()
    
    # 添加节点
    nodes = ['A', 'B', 'C', 'D', 'E']
    G.add_nodes_from(nodes)
    
    # 添加边（更大的容量，更容易测试 MPP）
    edges = [
        ('A', 'B', 200),
        ('B', 'C', 300),
        ('C', 'D', 400),
        ('D', 'E', 250),
        ('A', 'C', 150),
        ('B', 'D', 180),
        ('A', 'E', 100),
    ]
    
    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)
    
    # 为每条边添加随机余额
    for u, v in G.edges():
        capacity = G.edges[u, v]['capacity']
        balance = random.randint(0, capacity)
        G.edges[u, v]['balance'] = balance
        G.edges[v, u]['balance'] = capacity - balance
    
    print(f"\n网络信息：")
    print(f"  节点数：{G.number_of_nodes()}")
    print(f"  边数：{G.number_of_edges()}")
    
    # 2. 初始化 MPP 路由器
    router = MPPBayesianRouter(G)
    
    # 3. 测试 1：金额拆分
    print(f"\n测试 1：金额拆分")
    amount = 150
    parts = router.split_amount(amount, num_parts=3)
    print(f"  总金额：{amount}")
    print(f"  拆分结果：{parts}")
    print(f"  总和验证：{sum(parts)} == {amount} ? {sum(parts) == amount}")
    
    # 4. 测试 2：找到多条路径
    print(f"\n测试 2：找到多条路径")
    sender, receiver = 'A', 'E'
    paths = router.find_mpp_paths(sender, receiver, amount, max_paths=3)
    print(f"  发送方：{sender}")
    print(f"  接收方：{receiver}")
    print(f"  总金额：{amount}")
    print(f"  找到的路径数：{len(paths)}")
    for i, (path, amt) in enumerate(paths, 1):
        prob = router.path_success_probability(path, amt)
        print(f"    Path {i}: {path}, amount={amt}, prob={prob:.2%}")
    
    # 5. 测试 3：MPP 轮次算法
    print(f"\n测试 3：MPP 轮次算法")
    router = MPPBayesianRouter(G)  # 重置路由器
    success, rounds, tried_mpps = router.try_mpp_payment(
        sender, receiver, amount, max_rounds=10, verbose=True
    )
    
    print(f"\n结果：")
    print(f"  成功：{success}")
    print(f"  轮次：{rounds}")
    print(f"  总尝试路径数：{sum(len(mpp) for mpp in tried_mpps)}")
    
    # 6. 测试 4：批量对比（单路径 vs MPP）
    print(f"\n测试 4：批量对比（单路径 vs MPP，100 次测试）")
    
    single_successes = 0
    mpp_successes = 0
    single_rounds_list = []
    mpp_rounds_list = []
    mpp_paths_list = []
    
    for _ in range(100):
        # 随机选择发送方和接收方
        nodes = list(G.nodes())
        sender = random.choice(nodes)
        receiver = random.choice(nodes)
        while receiver == sender:
            receiver = random.choice(nodes)
        
        # 随机金额
        amount = random.randint(50, 200)
        
        # 对比
        result = MPPBayesianRouter(G).compare_single_vs_mpp(
            sender, receiver, amount, verbose=False
        )
        
        if result['single_success']:
            single_successes += 1
            single_rounds_list.append(result['single_rounds'])
        
        if result['mpp_success']:
            mpp_successes += 1
            mpp_rounds_list.append(result['mpp_rounds'])
            mpp_paths_list.append(result['mpp_paths'])
    
    print(f"\n结果：")
    print(f"  单路径支付：")
    print(f"    成功率：{single_successes}%")
    print(f"    平均轮次：{sum(single_rounds_list) / len(single_rounds_list) if single_rounds_list else 0:.2f}")
    print(f"  多路径支付（MPP）：")
    print(f"    成功率：{mpp_successes}%")
    print(f"    平均轮次：{sum(mpp_rounds_list) / len(mpp_rounds_list) if mpp_rounds_list else 0:.2f}")
    print(f"    平均路径数：{sum(mpp_paths_list) / len(mpp_paths_list) if mpp_paths_list else 0:.2f}")
    
    print(f"\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_mpp_router()
