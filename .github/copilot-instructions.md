 # GateCalculator 项目 Copilot 指南

 ## 项目概览
 本项目为 C# / WPF 桌面应用，计算水工闸门净宽，支持三种典型工况（A.0.1、A.0.2、A.0.3），界面多标签页，输入参数与国标公式一致，实时显示中间参数。

 ## 主要结构
 - **UI 层**：`MainWindow.xaml`/`.cs`，负责参数输入、结果展示、事件绑定。
 - **计算服务**：`Services/Calculators.cs`，每种工况有独立静态方法（如 `ComputeA01`），输入/输出均为强类型对象。
 - **模型层**：如有，位于 `Models/`，用于参数与结果的数据结构。

 ## 关键开发工作流
 - **构建**：`dotnet build GateCalculator`
 - **运行**：`dotnet run --project GateCalculator`
 - **调试**：推荐用 VS/VS Code F5 启动，主窗口为 `MainWindow`。
 - **依赖**：需 .NET 6 SDK，WPF 桌面支持（`<UseWPF>true</UseWPF>`）。

 ## 约定与模式
 - 计算公式严格按 README.md 及国标附录实现，参数单位为米、秒、立方米每秒。
 - 计算服务方法参数/返回值均为结构体，便于扩展和单元测试。
 - UI 事件处理只做参数收集和结果展示，所有业务逻辑集中在 `Services/Calculators.cs`。
 - 结果展示时，NaN 用 `--` 替代，便于界面友好。
 - 允许用户直接修改 UI 文本或计算公式代码以适应不同表述习惯。

 ## 典型扩展点
 - 新增工况：在 `Services/Calculators.cs` 增加静态方法，UI 增加 Tab 页及输入控件。
 - 参数校验：如需更严格校验，可在服务层补充。

 ## 参考文件
 - `README.md`：包含全部公式、参数说明、用法。
 - `GateCalculator.csproj`：项目依赖与目标框架。
 - `MainWindow.xaml(.cs)`：UI 结构与事件绑定。
 - `Services/Calculators.cs`：全部计算逻辑。

 ## 其他
 - 本项目无自动化测试，建议扩展时为计算服务补充单元测试。

 ---
 （以下为 Copilot 自动化开发流程通用指引，保留以供参考）
 - Work through each checklist item systematically.
 - Keep communication concise and focused.
 - Follow development best practices.
