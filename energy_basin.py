"""消力池计算 - 核心数学函数

公式来源：附录 B.1，计算 h_c、h_c''、ΔZ、d、L_j、L_sj。
仅包含数学计算函数，无GUI依赖，适用于Streamlit应用。
"""

import math


def cbrt(x: float) -> float:
    """立方根函数，保留符号
    
    Args:
        x: 输入值
        
    Returns:
        x的立方根，保留正负号
    """
    return math.copysign(abs(x) ** (1.0 / 3.0), x)


def solve_cubic(a: float, b: float, c: float, d: float):
    """求解三次方程 x^3 + a*x^2 + b*x + d = 0
    
    使用Cardano公式求解三次方程的实根
    
    Args:
        a, b, c, d: 三次方程系数
        
    Returns:
        包含实根的列表
    """
    p = b - (a * a) / 3.0
    q = (2 * a ** 3) / 27.0 - (a * b) / 3.0 + d
    disc = (q / 2.0) ** 2 + (p / 3.0) ** 3
    
    if disc >= 0:
        # 一个实根
        sqrt_disc = math.sqrt(disc)
        u = cbrt(-q / 2.0 + sqrt_disc)
        v = cbrt(-q / 2.0 - sqrt_disc)
        return [u + v - a / 3.0]
    
    # 三个实根
    r = math.sqrt(-p / 3.0)
    phi = math.acos(-q / (2.0 * r ** 3))
    roots = []
    for k in range(3):
        t = 2.0 * r * math.cos((phi + 2.0 * math.pi * k) / 3.0)
        roots.append(t - a / 3.0)
    return roots
