"""
闸孔净宽计算模块
基于附录A公式
"""

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class GateResultA01:
    """A.0.1 平底闸闻计算结果"""
    B0: float  # 闸孔总净宽 (m)
    sigma: float  # 流量系数
    epsilon: float  # 侧收缩系数
    h1_H0: float  # h1/H0
    ratio_term: float  # h1/H0*(1-h1/H0)


@dataclass
class GateResultA02:
    """A.0.2 高底闸闻计算结果"""
    B0: float  # 闸孔总净宽 (m)
    mu0: float  # 流量系数
    hs_H0: float  # hs/H0


@dataclass
class GateResultA03:
    """A.0.3 潜没闸闻计算结果"""
    B0: float  # 闸孔总净宽 (m)
    sigma_prime: float  # 流量系数 σ'
    mu: float  # 流量系数 μ
    epsilon_prime: float  # ε'
    lambda_val: float  # λ
    ratio: float  # (he - hc) / (H - hc)
    he_H: float  # he/H


def calc_a01(
    *,
    Q: float,
    H0: float,
    H: float,
    h1: float,
    b0: float,
    b1: float,
    N: int = 1,
    m: float = 0.885,
    g: float = 9.81
) -> GateResultA01:
    """
    计算A.0.1 平底闸闻净宽
    
    Args:
        Q: 流量 (m³/s)
        H0: 闸前水头 (m)
        H: 上游水深 (m)
        h1: 闸孔开度 (m)
        b0: 单孔净宽 (m)
        b1: 闸墩厚度 (m)
        N: 闸孔数量
        m: 流量系数 (默认0.885)
        g: 重力加速度 (m/s², 默认9.81)
    
    Returns:
        GateResultA01: 计算结果
    """
    # 计算 h1/H0
    h1_H0 = h1 / H0
    
    # 计算 h1/H0 * (1 - h1/H0)
    ratio_term = h1_H0 * (1 - h1_H0)
    
    # 计算流量系数 sigma = 2.31 * (h1/H0 * (1 - h1/H0))^0.4
    sigma = 2.31 * (ratio_term ** 0.4)
    
    # 计算侧收缩系数 epsilon
    if N == 1:
        # 单孔：ε = b0 / (b0 + 2*0.1*h1)
        epsilon = b0 / (b0 + 2 * 0.1 * h1)
    else:
        # 多孔：ε = (N*b0) / (N*b0 + 2*0.1*h1 + (N-1)*b1)
        epsilon = (N * b0) / (N * b0 + 2 * 0.1 * h1 + (N - 1) * b1)
    
    # 计算闸孔总净宽 B0 = Q / (sigma * epsilon * m * sqrt(2*g) * H^(3/2))
    denominator = sigma * epsilon * m * math.sqrt(2 * g) * (H ** 1.5)
    B0 = Q / denominator
    
    return GateResultA01(
        B0=B0,
        sigma=sigma,
        epsilon=epsilon,
        h1_H0=h1_H0,
        ratio_term=ratio_term
    )


def calc_a02(
    *,
    Q: float,
    H0: float,
    h0: float,
    hs: float,
    sigma: float = 0.82,
    g: float = 9.81
) -> GateResultA02:
    """
    计算A.0.2 高底闸闻净宽
    
    Args:
        Q: 流量 (m³/s)
        H0: 闸前水头 (m)
        h0: 底坎高度 (m)
        hs: 下游水深 (m)
        sigma: 流量系数 (默认0.82)
        g: 重力加速度 (m/s², 默认9.81)
    
    Returns:
        GateResultA02: 计算结果
    """
    # 计算 hs/H0
    hs_H0 = hs / H0
    
    # 计算 mu0 = 0.877 + (hs/H0 - 0.65)^2
    mu0 = 0.877 + ((hs_H0 - 0.65) ** 2)
    
    # 计算闸孔总净宽 B0 = Q / (sigma * mu0 * sqrt(2*g*(H0-h0)))
    denominator = sigma * mu0 * math.sqrt(2 * g * (H0 - h0))
    B0 = Q / denominator
    
    return GateResultA02(
        B0=B0,
        mu0=mu0,
        hs_H0=hs_H0
    )


def calc_a03(
    *,
    Q: float,
    H0: float,
    H: float,
    he: float,
    hc: float,
    epsilon_c: float = 0.2,
    phi: float = 0.96,
    g: float = 9.81
) -> GateResultA03:
    """
    计算A.0.3 潜没闸闻净宽
    
    Args:
        Q: 流量 (m³/s)
        H0: 闸前水头 (m)
        H: 上游水深 (m)
        he: 闸后水深 (m)
        hc: 收缩断面水深 (m)
        epsilon_c: 收缩系数 (默认0.2)
        phi: 流速系数 (默认0.96)
        g: 重力加速度 (m/s², 默认9.81)
    
    Returns:
        GateResultA03: 计算结果
    """
    # 计算比值
    ratio = (he - hc) / (H - hc) if (H - hc) != 0 else 0.0
    he_H = he / H if H != 0 else 0.0
    
    # 查表插值获取 d' (sigma')
    # 根据 (he - hc) / (H - hc) 线性插值
    # 表格数据（简化版）
    table_data = [
        (0.0, 0.2),
        (0.1, 0.22),
        (0.2, 0.24),
        (0.3, 0.26),
        (0.4, 0.28),
        (0.5, 0.30),
        (0.6, 0.32),
        (0.7, 0.34),
        (0.8, 0.36),
        (0.9, 0.38),
        (1.0, 0.40)
    ]
    
    # 线性插值
    sigma_prime = 0.2  # 默认值
    for i in range(len(table_data) - 1):
        x1, y1 = table_data[i]
        x2, y2 = table_data[i + 1]
        if x1 <= ratio <= x2:
            # 线性插值
            sigma_prime = y1 + (y2 - y1) * (ratio - x1) / (x2 - x1)
            break
    
    # 如果超出范围，取边界值
    if ratio < table_data[0][0]:
        sigma_prime = table_data[0][1]
    elif ratio > table_data[-1][0]:
        sigma_prime = table_data[-1][1]
    
    # 计算 lambda = 0.4 / exp(ln(6*epsilon_c)^2)
    if epsilon_c > 0:
        ln_term = math.log(6 * epsilon_c)
        lambda_val = 0.4 / math.exp(ln_term ** 2)
    else:
        lambda_val = 0.0
    
    # 计算 epsilon' = 1 / (1 + sqrt(lambda * (1 - (he/H)^2)))
    if he_H < 1.0:
        sqrt_term = math.sqrt(lambda_val * (1 - he_H ** 2))
        epsilon_prime = 1.0 / (1.0 + sqrt_term)
    else:
        epsilon_prime = 1.0
    
    # 计算 mu = phi * exp(epsilon') / sqrt(1 - epsilon' * he/H)
    exp_eps = math.exp(epsilon_prime)
    denominator_mu = 1.0 - epsilon_prime * he_H
    if denominator_mu > 0:
        mu = phi * exp_eps / math.sqrt(denominator_mu)
    else:
        mu = 0.0
    
    # 计算闸孔总净宽 B0 = Q / (sigma' * mu * he * sqrt(2*g*H0))
    denominator = sigma_prime * mu * he * math.sqrt(2 * g * H0)
    B0 = Q / denominator if denominator > 0 else 0.0
    
    return GateResultA03(
        B0=B0,
        sigma_prime=sigma_prime,
        mu=mu,
        epsilon_prime=epsilon_prime,
        lambda_val=lambda_val,
        ratio=ratio,
        he_H=he_H
    )
