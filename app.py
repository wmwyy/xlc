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
                
                # 跃后水深 h''c: B.1.1-2公式
                # h''c = (hc/2) * (√(1 + 8αq²/(ghc³)) - 1) * (b₁/b₂)^0.25
                width_ratio = (b1 / b2) ** 0.25
                sqrt_term = math.sqrt(1.0 + 8.0 * alpha * q**2 / (g * hc**3))
                hc_double_prime = (hc / 2.0) * (sqrt_term - 1.0) * width_ratio
                
                # 保持向后兼容的变量名
                hc_prime = hc_double_prime / sigma0  # 未校正值
                hc_prime_adj = hc_double_prime
                
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
            
            st.markdown("**跃后水深计算（B.1.1-2）：**")
            st.latex(r"h''_c = \frac{h_c}{2}\left(\sqrt{1 + \frac{8\alpha q^2}{gh_c^3}} - 1\right)\left(\frac{b_1}{b_2}\right)^{0.25}")
            
            st.markdown("**消能计算：**")
            st.latex(r"\Delta E = \frac{(h''_c - h_c)^3}{4 h_c h''_c}")
            
            st.markdown("**水跃长度：**")
            st.latex(r"L_j = \beta(4.5h''_c + p)")
            
            st.markdown("**护坦长度：**")
            st.latex(r"L_{sj} = L_j + L_s")
            
            st.markdown("**弗劳德数：**")
            st.latex(r"Fr_c = \frac{v_c}{\sqrt{g h_c}}")

        # Word导出
        st.markdown("---")
        st.markdown("### 📄 导出报告")
        
        if st.button("📥 下载 Word 报告", type="secondary", use_container_width=True):
            try:
                import tempfile
                import os
                from word_export import export_energy_basin_to_word
                
                # 准备结果数据
                results_data = {
                    'hc': result['hc'],
                    'hc_double_prime': result['hc_prime_adj'],
                    'delta_Z': result['delta_E'],
                    'd': result['hc_prime_adj'] - result['hc'],
                    'Lj': result['Lj'],
                    'Lsj': result['Lsj'],
                    'v': result['vc'],
                    'Fr': result['Frc']
                }
                
                # 创建临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                    output_path = export_energy_basin_to_word(
                        results=results_data,
                        output_path=tmp.name,
                        project_name=st.session_state.project_name,
                        input_params=st.session_state.input_params
                    )
                    
                    # 读取文件内容
                    with open(output_path, "rb") as f:
                        docx_data = f.read()
                    
                    # 删除临时文件
                    try:
                        os.unlink(output_path)
                    except:
                        pass
                    
                    # 提供下载
                    st.download_button(
                        label="💾 点击下载 Word 文档",
                        data=docx_data,
                        file_name=f"{st.session_state.project_name}_消力池计算报告.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                    
            except ImportError:
                st.warning("⚠️ Word导出功能需要安装 python-docx 库")
            except Exception as e:
                st.error(f"❌ 导出失败：{str(e)}")

# 添加新的计算功能页面
st.markdown("---")
st.markdown("---")

with st.expander(" B.1.3 消力池底板厚度计算", expanded=False):
    st.markdown("### 消力池底板厚度计算")
    
    col_t1, col_t2 = st.columns([1, 1])
    
    with col_t1:
        st.markdown("#### 输入参数")
        q_t = st.number_input("q - 单宽流量 (m³/s/m)", min_value=0.01, value=10.0, step=0.5, key="q_t")
        delta_H_t = st.number_input("ΔH' - 上下游水位差 (m)", min_value=0.01, value=5.0, step=0.1, key="dH_t")
        U_t = st.number_input("U - 底面扬压力 (kPa)", min_value=0.0, value=50.0, step=1.0, key="U_t")
        gamma_t = st.number_input("γ - 水重力密度 (kN/m³)", min_value=1.0, value=10.0, step=0.1, key="gamma_t")
        hd_t = st.number_input("hd - 消力池内水深 (m)", min_value=0.01, value=3.0, step=0.1, key="hd_t")
        Pm_t = st.number_input("Pm - 脉动压力 (kPa)", min_value=0.0, value=10.0, step=1.0, key="Pm_t")
        gamma_b_t = st.number_input("γb - 底板饱和容重 (kN/m³)", min_value=1.0, value=24.0, step=0.1, key="gamma_b_t")
        
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            k1_t = st.number_input("k₁ - 计算系数", min_value=0.1, value=0.175, step=0.005, format="%.3f", key="k1_t", help="0.15~0.20")
        with col_k2:
            k2_t = st.number_input("k₂ - 安全系数", min_value=0.1, value=1.2, step=0.1, key="k2_t", help="1.1~1.3")
        
        use_plus_t = st.radio("脉动压力符号", ["前半部（+）", "后半部（-）"], key="use_plus_t", horizontal=True)
    
    with col_t2:
        st.markdown("#### 计算结果")
        if st.button(" 计算厚度", key="calc_thickness", use_container_width=True):
            try:
                # B.1.3-1: 抗冲厚度
                t_impact = k1_t * math.sqrt(q_t * math.sqrt(delta_H_t))
                
                # B.1.3-2: 抗浮厚度
                if use_plus_t == "前半部（+）":
                    t_float = k2_t * (U_t - gamma_t * hd_t + Pm_t) / gamma_b_t
                else:
                    t_float = k2_t * (U_t - gamma_t * hd_t - Pm_t) / gamma_b_t
                
                t_design = max(t_impact, t_float)
                t_final = max(t_design, 0.5)
                
                st.session_state.thickness_result = {
                    't_impact': t_impact,
                    't_float': t_float,
                    't_design': t_design,
                    't_final': t_final
                }
                st.success(" 计算完成！")
            except Exception as e:
                st.error(f" 计算错误：{str(e)}")
        
        if "thickness_result" in st.session_state:
            tr = st.session_state.thickness_result
            st.metric("最终设计厚度", f"{tr['t_final']:.3f} m", help="≥0.5m")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("抗冲厚度", f"{tr['t_impact']:.3f} m")
            with col_b:
                st.metric("抗浮厚度", f"{tr['t_float']:.3f} m")
            
            with st.expander("查看公式"):
                st.latex(r"t_{\text{抗冲}} = k_1\sqrt{q\sqrt{\Delta H'}}")
                sign = "+" if use_plus_t == "前半部（+）" else "-"
                st.latex(r"t_{\text{抗浮}} = k_2\frac{U - \gamma h_d " + sign + r" P_m}{\gamma_b}")

with st.expander(" B.2.1 海漫长度计算", expanded=False):
    st.markdown("### 海漫长度计算")
    
    col_m1, col_m2 = st.columns([1, 1])
    
    with col_m1:
        st.markdown("#### 输入参数")
        qs_m = st.number_input("qs - 消力池末端单宽流量 (m³/(s·m))", min_value=0.01, value=10.0, step=0.5, key="qs_m")
        delta_H_m = st.number_input("ΔH' - 上下游水位差 (m)", min_value=0.01, value=5.0, step=0.1, key="dH_m")
        
        check_val = math.sqrt(qs_m * math.sqrt(delta_H_m))
        if check_val < 1 or check_val > 9:
            st.warning(f"⚠️ √(qs·√ΔH') = {check_val:.2f}，超出适用范围 [1, 9]")
        else:
            st.info(f"✓ √(qs·√ΔH') = {check_val:.2f}，在适用范围内")
        
        riverbed_type_m = st.selectbox(
            "河床土质类型",
            ["粉砂、细砂", "中砂、粗砂、粉质黏土", "粉质黏土", "坚硬黏土"],
            key="riverbed_m"
        )
        
        Ks_ranges = {
            "粉砂、细砂": (14.0, 13.0),
            "中砂、粗砂、粉质黏土": (12.0, 11.0),
            "粉质黏土": (10.0, 9.0),
            "坚硬黏土": (8.0, 7.0)
        }
        ks_min, ks_max = Ks_ranges[riverbed_type_m]
        st.info(f"该土质 Ks 范围：{ks_max} ~ {ks_min}")
        
        Ks_m = st.number_input("Ks - 海漫长度计算系数", min_value=1.0, value=(ks_min + ks_max)/2, step=0.5, key="Ks_m")
    
    with col_m2:
        st.markdown("#### 计算结果")
        if st.button(" 计算海漫长度", key="calc_apron", use_container_width=True):
            try:
                # B.2.1: Lp = Ks·√(qs·√ΔH')
                Lp = Ks_m * math.sqrt(qs_m * math.sqrt(delta_H_m))
                
                st.session_state.apron_result = {
                    'Lp': Lp,
                    'Ks': Ks_m
                }
                st.success(" 计算完成！")
            except Exception as e:
                st.error(f" 计算错误：{str(e)}")
        
        if "apron_result" in st.session_state:
            ar = st.session_state.apron_result
            st.metric("海漫长度 Lp", f"{ar['Lp']:.2f} m")
            st.metric("使用的 Ks 值", f"{ar['Ks']:.2f}")
            
            with st.expander("查看公式"):
                st.latex(r"L_p = K_s\sqrt{q_s\sqrt{\Delta H'}}")
                st.markdown("**适用条件：** √(qs·√ΔH') = 1~9，且消能扩散良好")

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "消力池计算器 v1.1 | 基于附录B.1规范 |  2025"
    "</div>",
    unsafe_allow_html=True
)
