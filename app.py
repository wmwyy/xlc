"""
闸孔净宽与消力池计算器 - Web版本
基于附录A和附录B规范
使用 Streamlit 框架
"""

import streamlit as st
import math
import tempfile
import os
from datetime import datetime
from gate_calculator import calc_a01, calc_a02, calc_a03
from energy_basin import cbrt, solve_cubic

# 页面配置
st.set_page_config(
    page_title="闸孔净宽与消力池计算器",
    page_icon="🚪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown('''
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7c3aed;
        color: white;
    }
    h1 {
        color: #6d28d9;
        text-align: center;
        padding: 1rem 0;
    }
    h2 {
        color: #7c3aed;
        border-bottom: 2px solid #8b5cf6;
        padding-bottom: 0.5rem;
    }
    </style>
    ''', unsafe_allow_html=True)

# 标题
st.title("🚪 闸孔净宽与消力池计算器")
st.markdown("**计算依据：** 附录A（闸孔净宽）、附录B（消力池）")
st.markdown("---")

# 侧边栏说明
with st.sidebar:
    st.header("📖 使用说明")
    st.markdown('''
    **闸孔净宽计算：**
    - A.0.1: 平底闸闻
    - A.0.2: 高底闸闻
    - A.0.3: 潜没闸闻

    **消力池计算：**
    - 基于附录B.1规范
    - 计算跃后水深、护坦长度等

    **使用步骤：**
    1. 选择计算类型标签页
    2. 输入相关参数
    3. 点击计算按钮
    4. 查看详细结果
    ''')
    
    st.markdown("---")
    st.markdown(f"**当前时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 创建标签页
tab1, tab2, tab3, tab4 = st.tabs(["🔲 A.0.1 平底闸闻", "⬆️ A.0.2 高底闸闻", "💧 A.0.3 潜没闸闻", "🌊 消力池计算"])

# ============== A.0.1 平底闸闻 ==============
with tab1:
    st.header("A.0.1 平底闸闻净宽计算")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔧 输入参数")
        
        Q_a01 = st.number_input("Q - 流量 (m³/s)", min_value=0.1, value=120.0, step=1.0, key="Q_a01")
        H0_a01 = st.number_input("H₀ - 闸前水头 (m)", min_value=0.1, value=8.0, step=0.1, key="H0_a01")
        H_a01 = st.number_input("H - 上游水深 (m)", min_value=0.1, value=10.0, step=0.1, key="H_a01")
        h1_a01 = st.number_input("h₁ - 闸孔开度 (m)", min_value=0.1, value=5.0, step=0.1, key="h1_a01")
        
        st.markdown("#### 闸孔参数")
        b0_a01 = st.number_input("b₀ - 单孔净宽 (m)", min_value=0.1, value=3.0, step=0.1, key="b0_a01")
        b1_a01 = st.number_input("b₁ - 闸墩厚度 (m)", min_value=0.0, value=3.5, step=0.1, key="b1_a01")
        N_a01 = st.number_input("N - 闸孔数量", min_value=1, value=1, step=1, key="N_a01")
        
        m_a01 = st.number_input("m - 流量系数", min_value=0.1, value=0.885, step=0.001, format="%.3f", key="m_a01")
        g_a01 = st.number_input("g - 重力加速度 (m/s²)", min_value=9.0, value=9.81, step=0.01, format="%.2f", key="g_a01")
    
    with col2:
        st.subheader("📊 计算结果")
        
        if st.button("🚀 计算 A.0.1", type="primary", use_container_width=True, key="calc_a01"):
            try:
                result = calc_a01(
                    Q=Q_a01, H0=H0_a01, H=H_a01, h1=h1_a01,
                    b0=b0_a01, b1=b1_a01, N=N_a01, m=m_a01, g=g_a01
                )
                
                st.success("✅ 计算完成！")
                
                st.markdown("### 🎯 主要结果")
                st.metric("B₀ - 闸孔总净宽", f"{result.B0:.4f} m")
                
                st.markdown("#### 📋 中间参数")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("σ - 流量系数", f"{result.sigma:.4f}")
                    st.metric("ε - 侧收缩系数", f"{result.epsilon:.4f}")
                with col_b:
                    st.metric("h₁/H₀", f"{result.h1_H0:.4f}")
                    st.metric("h₁/H₀(1-h₁/H₀)", f"{result.ratio_term:.4f}")
                
                with st.expander("📐 查看计算公式", expanded=False):
                    st.latex(r"B_0 = \frac{Q}{\sigma \cdot \varepsilon \cdot m \cdot \sqrt{2g} \cdot H^{3/2}}")
                    st.latex(r"\sigma = 2.31 \cdot \left(\frac{h_1}{H_0} \cdot \left(1 - \frac{h_1}{H_0}\right)\right)^{0.4}")
                    if N_a01 == 1:
                        st.latex(r"\varepsilon = \frac{b_0}{b_0 + 2 \cdot 0.1 \cdot h_1}")
                    else:
                        st.latex(r"\varepsilon = \frac{N \cdot b_0}{N \cdot b_0 + 2 \cdot 0.1 \cdot h_1 + (N-1) \cdot b_1}")
                
            except Exception as e:
                st.error(f"❌ 计算错误：{str(e)}")

# ============== A.0.2 高底闸闻 ==============
with tab2:
    st.header("A.0.2 高底闸闻净宽计算")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔧 输入参数")
        
        Q_a02 = st.number_input("Q - 流量 (m³/s)", min_value=0.1, value=150.0, step=1.0, key="Q_a02")
        H0_a02 = st.number_input("H₀ - 闸前水头 (m)", min_value=0.1, value=8.0, step=0.1, key="H0_a02")
        h0_a02 = st.number_input("h₀ - 底坎高度 (m)", min_value=0.0, value=2.0, step=0.1, key="h0_a02")
        hs_a02 = st.number_input("hₛ - 下游水深 (m)", min_value=0.1, value=5.0, step=0.1, key="hs_a02")
        
        sigma_a02 = st.number_input("σ - 流量系数", min_value=0.1, value=0.82, step=0.01, format="%.2f", key="sigma_a02")
        g_a02 = st.number_input("g - 重力加速度 (m/s²)", min_value=9.0, value=9.81, step=0.01, format="%.2f", key="g_a02")
    
    with col2:
        st.subheader("📊 计算结果")
        
        if st.button("🚀 计算 A.0.2", type="primary", use_container_width=True, key="calc_a02"):
            try:
                result = calc_a02(
                    Q=Q_a02, H0=H0_a02, h0=h0_a02, hs=hs_a02,
                    sigma=sigma_a02, g=g_a02
                )
                
                st.success("✅ 计算完成！")
                
                st.markdown("### 🎯 主要结果")
                st.metric("B₀ - 闸孔总净宽", f"{result.B0:.4f} m")
                
                st.markdown("#### 📋 中间参数")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("μ₀ - 流量系数", f"{result.mu0:.4f}")
                with col_b:
                    st.metric("hₛ/H₀", f"{result.hs_H0:.4f}")
                
                with st.expander("📐 查看计算公式", expanded=False):
                    st.latex(r"B_0 = \frac{Q}{\sigma \cdot \mu_0 \cdot \sqrt{2g(H_0-h_0)}}")
                    st.latex(r"\mu_0 = 0.877 + \left(\frac{h_s}{H_0} - 0.65\right)^2")
                
            except Exception as e:
                st.error(f"❌ 计算错误：{str(e)}")

# ============== A.0.3 潜没闸闻 ==============
with tab3:
    st.header("A.0.3 潜没闸闻净宽计算")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔧 输入参数")
        
        Q_a03 = st.number_input("Q - 流量 (m³/s)", min_value=0.1, value=180.0, step=1.0, key="Q_a03")
        H0_a03 = st.number_input("H₀ - 闸前水头 (m)", min_value=0.1, value=9.0, step=0.1, key="H0_a03")
        H_a03 = st.number_input("H - 上游水深 (m)", min_value=0.1, value=10.0, step=0.1, key="H_a03")
        he_a03 = st.number_input("hₑ - 闸后水深 (m)", min_value=0.1, value=4.0, step=0.1, key="he_a03")
        hc_a03 = st.number_input("hc - 收缩断面水深 (m)", min_value=0.1, value=1.5, step=0.1, key="hc_a03")
        
        epsilon_c_a03 = st.number_input("εc - 收缩系数", min_value=0.01, value=0.2, step=0.01, format="%.2f", key="epsilon_c_a03")
        phi_a03 = st.number_input("φ - 流速系数", min_value=0.01, value=0.96, step=0.01, format="%.2f", key="phi_a03")
        g_a03 = st.number_input("g - 重力加速度 (m/s²)", min_value=9.0, value=9.81, step=0.01, format="%.2f", key="g_a03")
    
    with col2:
        st.subheader("📊 计算结果")
        
        if st.button("🚀 计算 A.0.3", type="primary", use_container_width=True, key="calc_a03"):
            try:
                result = calc_a03(
                    Q=Q_a03, H0=H0_a03, H=H_a03, he=he_a03, hc=hc_a03,
                    epsilon_c=epsilon_c_a03, phi=phi_a03, g=g_a03
                )
                
                st.success("✅ 计算完成！")
                
                st.markdown("### 🎯 主要结果")
                st.metric("B₀ - 闸孔总净宽", f"{result.B0:.4f} m")
                
                st.markdown("#### 📋 中间参数")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("σ' - 流量系数", f"{result.sigma_prime:.4f}")
                    st.metric("μ - 流量系数", f"{result.mu:.4f}")
                with col_b:
                    st.metric("ε' - 收缩系数", f"{result.epsilon_prime:.4f}")
                    st.metric("λ - 参数", f"{result.lambda_val:.4f}")
                with col_c:
                    st.metric("(hₑ-hc)/(H-hc)", f"{result.ratio:.4f}")
                    st.metric("hₑ/H", f"{result.he_H:.4f}")
                
                with st.expander("📐 查看计算公式", expanded=False):
                    st.latex(r"B_0 = \frac{Q}{\sigma' \cdot \mu \cdot h_e \cdot \sqrt{2g H_0}}")
                    st.latex(r"\mu = \varphi \cdot \frac{e^{\varepsilon'}}{\sqrt{1 - \varepsilon' \cdot \frac{h_e}{H}}}")
                    st.latex(r"\varepsilon' = \frac{1}{1 + \sqrt{\lambda \cdot \left(1 - \left(\frac{h_e}{H}\right)^2\right)}}")
                    st.latex(r"\lambda = \frac{0.4}{e^{(\ln(6\varepsilon_c))^2}}")
                
            except Exception as e:
                st.error(f"❌ 计算错误：{str(e)}")

# ============== 消力池计算 ==============
with tab4:
    st.header("消力池计算（附录B.1）")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔧 输入参数")
        
        st.markdown("##### 基本参数")
        sigma0_b = st.number_input("σ₀ - 跃前淹没系数", min_value=1.0, value=1.05, step=0.01, format="%.2f", key="sigma0_b",
                                  help="1.05~1.10")
        alpha_b = st.number_input("α - 动能校正系数", min_value=1.0, value=1.00, step=0.01, format="%.2f", key="alpha_b",
                                 help="1.0~1.05")
        q_b = st.number_input("q - 单宽流量 (m³/s/m)", min_value=0.1, value=5.0, step=0.1, key="q_b")
        b1_b = st.number_input("b₁ - 首槛宽度 (m)", min_value=0.1, value=10.0, step=0.1, key="b1_b")
        b2_b = st.number_input("b₂ - 末槛宽度 (m)", min_value=0.1, value=12.0, step=0.1, key="b2_b")
        
        st.markdown("##### 水力参数")
        T0_b = st.number_input("T₀ - 总势能 (m)", min_value=0.1, value=8.0, step=0.1, key="T0_b")
        p_b = st.number_input("p - 校正长度参数 (m)", min_value=0.0, value=1.0, step=0.1, key="p_b")
        hs_b = st.number_input("h'ₛ - 出池河床水深 (m)", min_value=0.1, value=3.0, step=0.1, key="hs_b")
        Ls_b = st.number_input("Lₛ - 斜坡水平投影 (m)", min_value=0.0, value=5.0, step=0.1, key="Ls_b")
        
        beta_b = st.number_input("β - 水跃长度校正", min_value=0.0, value=0.75, step=0.01, format="%.2f", key="beta_b",
                                help="0.7~0.8")
        g_b = st.number_input("g - 重力加速度 (m/s²)", min_value=9.0, value=9.81, step=0.01, format="%.2f", key="g_b")
    
    with col2:
        st.subheader("📊 计算结果")
        
        if st.button("🚀 计算消力池", type="primary", use_container_width=True, key="calc_basin"):
            try:
                # 消力池计算逻辑（从energy_basin.py）
                # 求解 hc: T0 = hc + alpha * q^2 / (2*g*hc^2)
                a_coef = -T0_b
                b_coef = 1.0
                c_coef = 0.0
                d_coef = (alpha_b * q_b**2) / (2.0 * g_b)
                
                roots = solve_cubic(a_coef, b_coef, c_coef, d_coef)
                valid_hc = [r for r in roots if r > 0]
                
                if not valid_hc:
                    st.error("❌ 无法求解收缩水深 hc")
                else:
                    hc = min(valid_hc)
                    
                    # 计算后续值
                    vc = q_b / hc
                    Frc = vc / math.sqrt(g_b * hc)
                    
                    # 跃后水深
                    hc_prime = 0.5 * hc * (-1.0 + math.sqrt(1.0 + 8.0 * Frc**2))
                    hc_prime_adj = sigma0_b * hc_prime
                    
                    # 消能
                    delta_E = ((hc_prime_adj - hc)**3) / (4.0 * hc * hc_prime_adj)
                    
                    # 水跃长度
                    Lj = beta_b * (4.5 * hc_prime_adj + p_b)
                    
                    # 护坦长度
                    Lsj = Lj + Ls_b
                    
                    st.success("✅ 计算完成！")
                    
                    st.markdown("### 🎯 主要结果")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("hc - 收缩水深", f"{hc:.4f} m")
                        st.metric("h''c - 跃后水深", f"{hc_prime_adj:.4f} m")
                        st.metric("ΔE - 消能", f"{delta_E:.4f} m")
                    with col_b:
                        st.metric("Lⱼ - 水跃长度", f"{Lj:.4f} m")
                        st.metric("Lₛⱼ - 护坦长度", f"{Lsj:.4f} m")
                        st.metric("Frc - 弗劳德数", f"{Frc:.4f}")
                    
                    with st.expander("🔍 查看详细参数", expanded=False):
                        st.metric("vc - 收缩流速", f"{vc:.4f} m/s")
                        st.metric("h'c - 跃后水深(未校正)", f"{hc_prime:.4f} m")
                    
                    with st.expander("📐 查看计算公式", expanded=False):
                        st.latex(r"T_0 = h_c + \frac{\alpha q^2}{2g h_c^2}")
                        st.latex(r"h'_c = \frac{h_c}{2}\left(-1 + \sqrt{1 + 8Fr_c^2}\right)")
                        st.latex(r"h''_c = \sigma_0 \cdot h'_c")
                        st.latex(r"\Delta E = \frac{(h''_c - h_c)^3}{4 h_c h''_c}")
                        st.latex(r"L_j = \beta(4.5h''_c + p)")
                
            except Exception as e:
                st.error(f"❌ 计算错误：{str(e)}")
                import traceback
                st.code(traceback.format_exc())

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "闸孔净宽与消力池计算器 v1.0 | 基于附录A、B规范 | © 2025"
    "</div>",
    unsafe_allow_html=True
)
