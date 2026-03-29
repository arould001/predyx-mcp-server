#!/usr/bin/env python3
"""
Pickhardt Payments - 概率路由凸优化求解器
基于第一性原理推导的实现

核心理论：
1. 流动性不确定性：通道余额服从均匀分布 U(0, capacity)
2. 成功概率：P_success = ∏ (1 - x/c_i)
3. 对数转换：log(P_success) = ∑ log(1 - x/c_i)
4. 凸优化：maximize λ * log(P_success) - (1-λ) * cost(x)

作者: Dia (基于第一性原理推导)
日期: 2026-03-29
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PaymentChannel:
    """支付通道"""
    channel_id: str
    capacity: float  # satoshis
    fee_base: float  # base fee in satoshis
    fee_rate: float  # fee rate (ppm = parts per million)
    node1: str
    node2: str


@dataclass
class PaymentPath:
    """支付路径"""
    channels: List[PaymentChannel]
    amount: float  # satoshis to send
    
    def total_capacity(self) -> float:
        """路径的总容量（瓶颈通道）"""
        return min(ch.capacity for ch in self.channels)
    
    def total_fee(self, amount: float) -> float:
        """计算总手续费"""
        total = 0.0
        for ch in self.channels:
            total += ch.fee_base + (amount * ch.fee_rate / 1_000_000)
        return total


class PickhardtPaymentsSolver:
    """
    Pickhardt Payments 概率路由求解器
    
    核心算法：
    1. 对数转换：将乘法形式的成功概率转换为加法形式
    2. 凸优化：最大化成功率 - 成本权衡
    3. 梯度下降：迭代求解最优支付金额
    """
    
    def __init__(self, lambda_weight: float = 0.7):
        """
        初始化求解器
        
        Args:
            lambda_weight: 权衡参数 λ ∈ [0, 1]
                λ → 1: 优先成功率
                λ → 0: 优先低成本
        """
        if not 0 <= lambda_weight <= 1:
            raise ValueError("lambda_weight must be in [0, 1]")
        
        self.lambda_weight = lambda_weight
        logger.info(f"Initialized Pickhardt solver with λ={lambda_weight}")
    
    def compute_success_probability(self, path: PaymentPath, amount: float) -> float:
        """
        计算路径成功概率（基于均匀分布假设）
        
        P_success = ∏ (1 - x/c_i)
        
        Args:
            path: 支付路径
            amount: 支付金额（satoshis）
        
        Returns:
            成功概率 ∈ [0, 1]
        """
        if amount > path.total_capacity():
            return 0.0
        
        prob = 1.0
        for ch in path.channels:
            if amount >= ch.capacity:
                return 0.0
            prob *= (1 - amount / ch.capacity)
        
        return prob
    
    def compute_log_success_probability(self, path: PaymentPath, amount: float) -> float:
        """
        计算对数成功概率
        
        log(P_success) = ∑ log(1 - x/c_i)
        
        Args:
            path: 支付路径
            amount: 支付金额（satoshis）
        
        Returns:
            对数成功概率（负数，因为 log(1-x/c) < 0）
        """
        if amount >= path.total_capacity():
            return -np.inf
        
        log_prob = 0.0
        for ch in path.channels:
            ratio = amount / ch.capacity
            if ratio >= 1:
                return -np.inf
            log_prob += np.log(1 - ratio)
        
        return log_prob
    
    def compute_cost(self, path: PaymentPath, amount: float) -> float:
        """
        计算支付成本（手续费）
        
        cost = ∑ (fee_base + fee_rate * x)
        
        Args:
            path: 支付路径
            amount: 支付金额（satoshis）
        
        Returns:
            总成本（satoshis）
        """
        return path.total_fee(amount)
    
    def objective_function(self, path: PaymentPath, amount: float) -> float:
        """
        目标函数：权衡成功率和成本
        
        maximize λ * log(P_success) - (1-λ) * cost
        
        Args:
            path: 支付路径
            amount: 支付金额（satoshis）
        
        Returns:
            目标函数值（越大越好）
        """
        log_prob = self.compute_log_success_probability(path, amount)
        cost = self.compute_cost(path, amount)
        
        # 归一化成本（假设 1 sat ≈ 0.001 USD，log_prob 通常在 -1 到 -10 之间）
        normalized_cost = cost / 1000.0
        
        return self.lambda_weight * log_prob - (1 - self.lambda_weight) * normalized_cost
    
    def compute_gradient(self, path: PaymentPath, amount: float) -> float:
        """
        计算目标函数对 amount 的梯度
        
        ∂f/∂x = -λ * ∑ 1/(c_i - x) - (1-λ) * ∑ fee_rate_i
        
        Args:
            path: 支付路径
            amount: 支付金额（satoshis）
        
        Returns:
            梯度值
        """
        if amount >= path.total_capacity():
            return -np.inf
        
        # 第一项：-λ * ∑ 1/(c_i - x)
        gradient = 0.0
        for ch in path.channels:
            if amount >= ch.capacity:
                return -np.inf
            gradient -= 1.0 / (ch.capacity - amount)
        
        gradient *= self.lambda_weight
        
        # 第二项：-(1-λ) * ∑ fee_rate_i / 1_000_000
        total_fee_rate = sum(ch.fee_rate for ch in path.channels) / 1_000_000
        gradient -= (1 - self.lambda_weight) * total_fee_rate / 1000.0  # 归一化
        
        return gradient
    
    def optimize_amount(
        self,
        path: PaymentPath,
        max_amount: float,
        learning_rate: float = 10.0,
        max_iterations: int = 100,
        tolerance: float = 1e-6
    ) -> Tuple[float, float, List[float]]:
        """
        使用梯度上升优化支付金额
        
        Args:
            path: 支付路径
            max_amount: 最大支付金额（通常等于路径总容量）
            learning_rate: 学习率（satoshis per iteration）
            max_iterations: 最大迭代次数
            tolerance: 收敛容忍度
        
        Returns:
            (optimal_amount, optimal_objective, history)
        """
        # 初始化：从最大金额的 50% 开始
        amount = min(max_amount * 0.5, path.total_capacity() - 1)
        history = [self.objective_function(path, amount)]
        
        logger.info(f"Starting optimization: amount={amount:.2f}, obj={history[0]:.6f}")
        
        for iteration in range(max_iterations):
            # 计算梯度
            gradient = self.compute_gradient(path, amount)
            
            if gradient == -np.inf:
                logger.warning(f"Gradient overflow at iteration {iteration}")
                break
            
            # 梯度上升
            new_amount = amount + learning_rate * gradient
            
            # 边界约束
            new_amount = max(1.0, min(new_amount, path.total_capacity() - 1))
            
            # 计算新的目标函数值
            new_obj = self.objective_function(path, new_amount)
            
            # 检查收敛
            if abs(new_obj - history[-1]) < tolerance:
                logger.info(f"Converged at iteration {iteration}")
                break
            
            # 更新
            amount = new_amount
            history.append(new_obj)
            
            if iteration % 10 == 0:
                prob = self.compute_success_probability(path, amount)
                cost = self.compute_cost(path, amount)
                logger.info(
                    f"Iter {iteration}: amount={amount:.2f}, "
                    f"obj={new_obj:.6f}, prob={prob:.4f}, cost={cost:.2f}"
                )
        
        final_obj = self.objective_function(path, amount)
        logger.info(
            f"Optimization complete: amount={amount:.2f}, obj={final_obj:.6f}"
        )
        
        return amount, final_obj, history


def create_sample_network() -> List[PaymentChannel]:
    """创建示例网络（用于测试）"""
    return [
        PaymentChannel(
            channel_id="ch1",
            capacity=1_000_000,  # 1M sats
            fee_base=1,
            fee_rate=1000,  # 1000 ppm = 0.1%
            node1="Alice",
            node2="Bob"
        ),
        PaymentChannel(
            channel_id="ch2",
            capacity=500_000,  # 500K sats (bottleneck)
            fee_base=1,
            fee_rate=500,  # 500 ppm = 0.05%
            node1="Bob",
            node2="Carol"
        ),
        PaymentChannel(
            channel_id="ch3",
            capacity=2_000_000,  # 2M sats
            fee_base=1,
            fee_rate=2000,  # 2000 ppm = 0.2%
            node1="Carol",
            node2="Dave"
        ),
    ]


def main():
    """测试求解器"""
    print("=" * 60)
    print("Pickhardt Payments 概率路由求解器")
    print("=" * 60)
    
    # 创建示例网络
    channels = create_sample_network()
    path = PaymentPath(channels=channels, amount=0)  # amount 待优化
    
    print(f"\n路径信息:")
    print(f"  通道数量: {len(channels)}")
    print(f"  总容量（瓶颈）: {path.total_capacity():,.0f} sats")
    
    # 测试不同的 λ 值
    for lambda_weight in [0.9, 0.7, 0.5, 0.3]:
        print(f"\n{'=' * 60}")
        print(f"优化参数: λ = {lambda_weight}")
        print(f"  策略: {'优先成功率' if lambda_weight > 0.5 else '优先低成本'}")
        print(f"{'=' * 60}")
        
        solver = PickhardtPaymentsSolver(lambda_weight=lambda_weight)
        
        # 优化支付金额
        optimal_amount, optimal_obj, history = solver.optimize_amount(
            path=path,
            max_amount=path.total_capacity(),
            learning_rate=1000.0,  # 1000 sats per iteration
            max_iterations=50
        )
        
        # 最终结果
        success_prob = solver.compute_success_probability(path, optimal_amount)
        total_cost = solver.compute_cost(path, optimal_amount)
        
        print(f"\n优化结果:")
        print(f"  最优金额: {optimal_amount:,.2f} sats")
        print(f"  成功概率: {success_prob:.4f} ({success_prob*100:.2f}%)")
        print(f"  总成本: {total_cost:.2f} sats")
        print(f"  目标函数: {optimal_obj:.6f}")
        print(f"  迭代次数: {len(history)}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
