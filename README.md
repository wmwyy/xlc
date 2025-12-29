# 闸孔净宽与消力池计算器

 基于规范附录A和附录B的水工计算在线工具

## 功能特性

-  **A.0.1 平底闸闻**：计算平底闸闻净宽
-  **A.0.2 高底闸闻**：计算高底闸闻净宽
-  **A.0.3 潜没闸闻**：计算潜没闸闻净宽
-  **消力池计算**：基于附录B.1规范
-  **实时计算**：输入参数后即时获取结果
-  **美观界面**：现代化的 Web 界面
-  **多版本**：Streamlit Web版、tkinter桌面版、C# WPF版

## 在线访问

-  **Streamlit版**：部署后可用

## 本地部署

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. **克隆仓库**
\\\ash
git clone https://github.com/wmwyy/xlc.git
cd xlc
\\\

2. **安装依赖**
\\\ash
pip install -r requirements.txt
\\\

3. **运行 Streamlit Web 版**
\\\ash
streamlit run app.py
\\\

应用将在浏览器中自动打开，默认地址：http://localhost:8501

4. **运行消力池桌面版**（可选）
\\\ash
python energy_basin.py
\\\

## 使用说明

### Streamlit Web 版

1. 访问应用网址或本地运行
2. 选择计算类型标签页：
   - **A.0.1 平底闸闻**
   - **A.0.2 高底闸闻**
   - **A.0.3 潜没闸闻**
   - **消力池计算**
3. 输入相关参数
4. 点击"计算"按钮
5. 查看详细结果和中间参数

## 计算公式

### A.0.1 平底闸闻

\\\
B = Q / (σ  ε  m  (2g)  H^(3/2))
σ = 2.31  (h/H  (1 - h/H))^0.4
ε = b / (b + 20.1h)  [单孔]
ε = (Nb) / (Nb + 20.1h + (N-1)b)  [多孔]
\\\

### A.0.2 高底闸闻

\\\
B = Q / (σ  μ  (2g(H-h)))
μ = 0.877 + (h/H - 0.65)
\\\

### A.0.3 潜没闸闻

\\\
B = Q / (σ'  μ  hₑ  (2gH))
μ = φ  exp(ε') / (1 - ε'hₑ/H)
ε' = 1 / (1 + (λ(1 - (hₑ/H))))
λ = 0.4 / exp((ln(6εc)))
\\\

### 消力池计算（附录B.1）

\\\
T = hc + αq/(2ghc)
h'c = hc/2(-1 + (1 + 8Frc))
h''c = σ  h'c
ΔE = (h''c - hc) / (4hch''c)
Lⱼ = β(4.5h''c + p)
\\\

## 示例数据

### A.0.1 示例
- Q=120 m/s, H=8 m, H=10 m, h=5 m
- b=3 m, b=3.5 m, N=1, m=0.885
-  σ2.2929, ε0.9774, B3.7660 m

### A.0.2 示例
- Q=150 m/s, H=8 m, h=2 m, h=5 m, σ=0.82
-  μ0.8776, B9.2107 m

### A.0.3 示例
- Q=180 m/s, H=9 m, H=10 m, hₑ=4 m, hc=1.5 m
- εc=0.2, φ=0.96
-  σ'0.1565, λ0.3869, ε'0.6369, μ1.1025, B10.2940 m

## 技术栈

- **Python**: 3.8+
- **Web 框架**: Streamlit
- **文档导出**: python-docx
- **桌面 GUI**: tkinter (消力池)
- **C# 版本**: .NET 8 + WPF (GateCalculator目录)

## Streamlit Cloud 部署

1. Fork 本仓库到你的 GitHub 账号
2. 访问 [Streamlit Cloud](https://share.streamlit.io/)
3. 使用 GitHub 账号登录
4. 点击 "New app"
5. 选择仓库、分支（main）和主文件（app.py）
6. 点击 "Deploy"

## 更新日志

### v1.0.0 (2025-12-30)
-  新增 Streamlit Web 版本
-  整合闸孔净宽和消力池计算
-  紫色主题UI设计
-  完整的LaTeX公式显示
-  保留tkinter和C#版本

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License

## 联系方式

- GitHub: [wmwyy/xlc](https://github.com/wmwyy/xlc)

---

 如果这个项目对你有帮助，请给个 Star！
