# 闸孔净宽计算器（C# / WPF）

桌面端窗口化工具，按附录 A 公式 A.0.1（平底闸门）、A.0.2（高底闸门）、A.0.3（潜没闸门）计算闸孔总净宽，并显示中间参数。

## 运行
1. 需要 .NET 8 SDK。 
2. 在当前目录执行：
   - 构建：`dotnet build GateCalculator`  
   - 运行：`dotnet run --project GateCalculator`

## 功能要点
- 三个标签页对应 A.0.1 / A.0.2 / A.0.3。
- 输入量为图示公式中的参数，系数 g、m、phi 提供默认值，可手动改。
- 实时展示中间结果：sigma、epsilon、mu0、mu、epsilon'、lambda、sigma' 等。
- 表 A.0.3 的 d'（sigma'）内置插值，按 (he - hc)/(H - hc) 线性插值，超界取端点值。

## 主要计算公式
- A.0.1：`B0 = Q / (sigma * epsilon * m * sqrt(2*g) * H^(3/2))`，sigma 由 `2.31*(h1/H0*(1-h1/H0))^0.4` 计算，epsilon 按单孔或多孔公式求。
- A.0.2：`B0 = Q / (sigma * mu0 * sqrt(2*g*(H0-h0)))`，`mu0 = 0.877 + (hs/H0 - 0.65)^2`。
- A.0.3：`B0 = Q / (sigma' * mu * he * sqrt(2*g*H0))`，`mu = phi * exp(epsilon') / sqrt(1 - epsilon' * he/H)`，`epsilon' = 1 / (1 + sqrt(lambda * (1 - (he/H)^2)))`，`lambda = 0.4 / e^(ln(6*epsilon_c)^2)`。

## 示例与计算简图
- A.0.1 示例：Q=120 m³/s, H0=8 m, H=10 m, h1=5 m, b0=3 m, b1=3.5 m, N=1, m=0.885, g=9.81 ⇒ sigma≈1.2929, epsilon≈0.9774, B0≈0.7660 m。
- A.0.2 示例：Q=150 m³/s, H0=8 m, h0=2 m, hs=5 m, sigma=0.82, g=9.81 ⇒ mu0≈0.8776, B0≈19.2107 m。
- A.0.3 示例：Q=180 m³/s, H0=9 m, H=10 m, he=4 m, hc=1.5 m, epsilon_c=0.2, phi=0.96, g=9.81 ⇒ ratio≈0.2941, sigma'≈0.1565, lambda≈0.3869, epsilon'≈0.6369, mu≈2.1025, B0≈10.2940 m。
- 计算简图（A.0.3）：
```
   水面
   |<--H0-->|
   |--------| he
   |--hc--|
   |<----H---->|
   基床
```
## 注意
- 请确保输入单位与公式一致（米、立方米每秒）。
- 对表述或符号有不同习惯时，可直接修改 UI 文本或计算公式对应代码。
