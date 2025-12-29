"""
消力池计算器 - Web版本
基于附录B.1规范
使用 Streamlit 框架
"""

import streamlit as st
import math
from datetime import datetime
from energy_basin import cbrt, solve_cubic

# 页面配置
st.set_page_config(
    page_title="消力池计算器",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown('''
    <style>
    .main {
        padding: 2rem;
    }
    h1 {
        color: #0891b2;
        text-align: center;
        padding: 1rem 0;
    }
    h2 {
        color: #0e7490;
        border-bottom: 2px solid #06b6d4;
        padding-bottom: 0.5rem;
    }
    </style>
    ''', unsafe_allow_html=True)

# 标题
st.title(" 消力池计算器")
st.markdown("**计算依据：** 附录B.1 - 消力池设计规范")
st.markdown("---")

# 侧边栏说明
with st.sidebar:
    st.header(" 使用说明")
    st.markdown('''
    **计算内容：**
    - 收缩水深 hc
    - 跃后水深 h''c
    - 消能 ΔE
    - 水跃长度 Lⱼ
    - 护坦长度 Lⱼ

    **主要参数：**
    - σ: 跃前淹没系数 (1.05~1.10)
    - α: 动能校正系数 (1.0~1.05)
    - β: 水跃长度校正 (0.7~0.8)

    **使用步骤：**
    1. 输入基本参数
    2. 输入水力参数
    3. 点击计算按钮
    4. 查看详细结果
    ''')
    
    st.markdown("---")
    st.markdown(f"**当前时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 主界面
st.header(" 参数输入与计算")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(" 输入参数")
    
    st.markdown("##### 基本参数")
    sigma0 = st.number_input("σ - 跃前淹没系数", min_value=1.0, value=1.05, step=0.01, format="%.2f",
                            help="1.05~1.10")
    alpha = st.number_input("α - 动能校正系数", min_value=1.0, value=1.00, step=0.01, format="%.2f",
                           help="1.0~1.05")
    q = st.number_input("q - 单宽流量 (m/s/m)", min_value=0.1, value=5.0, step=0.1)
    b1 = st.number_input("b - 首槛宽度 (m)", min_value=0.1, value=10.0, step=0.1)
    b2 = st.number_input("b - 末槛宽度 (m)", min_value=0.1, value=12.0, step=0.1)
    
    st.markdown("##### 水力参数")
    T0 = st.number_input("T - 总势能 (m)", min_value=0.1, value=8.0, step=0.1)
    p = st.number_input("p - 校正长度参数 (m)", min_value=0.0, value=1.0, step=0.1)
    hs = st.number_input("h' - 出池河床水深 (m)", min_value=0.1, value=3.0, step=0.1)
    Ls = st.number_input("L - 斜坡水平投影 (m)", min_value=0.0, value=5.0, step=0.1)
    
    beta = st.number_input("β - 水跃长度校正", min_value=0.0, value=0.75, step=0.01, format="%.2f",
                          help="0.7~0.8")
    g = st.number_input("g - 重力加速度 (m/s)", min_value=9.0, value=9.81, step=0.01, format="%.2f")
    
    # 工程名称
    st.markdown("---")
    project_name = st.text_input(" 工程名称", value="消力池计算", help="用于报告标题")

with col2:
    st.subheader(" 计算结果")
    
    if st.button(" 开始计算", type="primary", use_container_width=True):
        try:
            # 求解收缩水深 hc: T0 = hc + alpha * q^2 / (2*g*hc^2)
            # 整理为三次方程: hc^3 - T0*hc^2 + (alpha*q^2)/(2*g) = 0
            # 标准形式: x^3 + a*x^2 + b*x + d = 0
            a_coef = -T0
            b_coef = 0.0
            c_coef = 0.0
            d_coef = (alpha * q**2) / (2.0 * g)
            
            roots = solve_cubic(a_coef, b_coef, c_coef, d_coef)
            valid_hc = [r for r in roots if r > 0 and r < T0]
            
            if not valid_hc:
                st.error(" 无法求解收缩水深 hc，请检查输入参数")
            else:
                hc = min(valid_hc)
                
                # 计算后续值
                vc = q / hc  # 收缩流速
                Frc = vc / math.sqrt(g * hc)  # 弗劳德数
                
                # 跃后水深（未校正）: h'c = hc/2 * (-1 + sqrt(1 + 8*Frc^2))
                hc_prime = 0.5 * hc * (-1.0 + math.sqrt(1.0 + 8.0 * Frc**2))
                
                # 跃后水深（校正）: h''c = σ * h'c
                hc_prime_adj = sigma0 * hc_prime
                
                # 消能: ΔE = (h''c - hc)^3 / (4*hc*h''c)
                delta_E = ((hc_prime_adj - hc)**3) / (4.0 * hc * hc_prime_adj)
                
                # 水跃长度: Lⱼ = β * (4.5*h''c + p)
                Lj = beta * (4.5 * hc_prime_adj + p)
                
                # 护坦长度: Lⱼ = Lⱼ + L
                Lsj = Lj + Ls
                
                # 保存到session_state
                st.session_state.result = {
                    'hc': hc,
                    'vc': vc,
                    'Frc': Frc,
                    'hc_prime': hc_prime,
                    'hc_prime_adj': hc_prime_adj,
                    'delta_E': delta_E,
                    'Lj': Lj,
                    'Lsj': Lsj
                }
                st.session_state.input_params = {
                    'sigma0': sigma0, 'alpha': alpha, 'q': q, 'b1': b1, 'b2': b2,
                    'T0': T0, 'p': p, 'hs': hs, 'Ls': Ls, 'beta': beta, 'g': g
                }
                st.session_state.project_name = project_name
                
                st.success(" 计算完成！")
                
        except Exception as e:
            st.error(f" 计算错误：{str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    if "result" in st.session_state:
        result = st.session_state.result
        
        st.markdown("###  主要结果")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("hc - 收缩水深", f"{result['hc']:.4f} m")
            st.metric("h''c - 跃后水深", f"{result['hc_prime_adj']:.4f} m")
            st.metric("ΔE - 消能", f"{result['delta_E']:.4f} m")
        with col_b:
            st.metric("Lⱼ - 水跃长度", f"{result['Lj']:.4f} m")
            st.metric("Lⱼ - 护坦长度", f"{result['Lsj']:.4f} m")
            st.metric("Frc - 弗劳德数", f"{result['Frc']:.4f}")
        
        with st.expander(" 查看详细参数", expanded=False):
            col_c, col_d = st.columns(2)
            with col_c:
                st.metric("vc - 收缩流速", f"{result['vc']:.4f} m/s")
            with col_d:
                st.metric("h'c - 跃后水深(未校正)", f"{result['hc_prime']:.4f} m")
        
        with st.expander(" 查看计算公式", expanded=False):
            st.markdown("**能量方程求解收缩水深：**")
            st.latex(r"T_0 = h_c + \frac{\alpha q^2}{2g h_c^2}")
            
            st.markdown("**跃后水深计算：**")
            st.latex(r"h'_c = \frac{h_c}{2}\left(-1 + \sqrt{1 + 8Fr_c^2}\right)")
            st.latex(r"h''_c = \sigma_0 \cdot h'_c")
            
            st.markdown("**消能计算：**")
            st.latex(r"\Delta E = \frac{(h''_c - h_c)^3}{4 h_c h''_c}")
            
            st.markdown("**水跃长度：**")
            st.latex(r"L_j = \beta(4.5h''_c + p)")
            
            st.markdown("**护坦长度：**")
            st.latex(r"L_{sj} = L_j + L_s")
            
            st.markdown("**弗劳德数：**")
            st.latex(r"Fr_c = \frac{v_c}{\sqrt{g h_c}}")

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "消力池计算器 v1.1 | 基于附录B.1规范 |  2025"
    "</div>",
    unsafe_allow_html=True
)
