<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

	<!-- Ask for project type, language, and frameworks if not specified. Skip if already provided. -->

	<!--
	Ensure that the previous step has been marked as completed.
	Call project setup tool with projectType parameter.
	Run scaffolding command to create project files and folders.
	Use '.' as the working directory.
	If no appropriate projectType is available, search documentation using available tools.
	Otherwise, create the project structure manually using available file creation tools.
	-->

	<!--
	Verify that all previous steps have been completed successfully and you have marked the step as completed.
	Develop a plan to modify codebase according to user requirements.
	Apply modifications using appropriate tools and user-provided references.
	Skip this step for "Hello World" projects.
	-->

	<!-- ONLY install extensions provided mentioned in the get_project_setup_info. Skip this step otherwise and mark as completed. -->

	<!--
	Verify that all previous steps have been completed.
	Install any missing dependencies.
	Run diagnostics and resolve any issues.
	Check for markdown files in project folder for relevant instructions on how to do this.
	-->

	<!--
	Verify that all previous steps have been completed.
	Check https://code.visualstudio.com/docs/debugtest/tasks to determine if the project needs a task. If so, use the create_and_run_task to create and launch a task based on package.json, README.md, and project structure.
	Skip this step otherwise.
	 -->

	<!--
	Verify that all previous steps have been completed.
	Prompt user for debug mode, launch only if confirmed.
	 -->

	<!--
	Verify that all previous steps have been completed.
	Verify that README.md and the copilot-instructions.md file in the .github directory exists and contains current project information.
	Clean up the copilot-instructions.md file in the .github directory by removing all HTML comments.
	 -->

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
<!--
## Execution Guidelines
PROGRESS TRACKING:
- If any tools are available to manage the above todo list, use it to track progress through this checklist.
- After completing each step, mark it complete and add a summary.
- Read current todo list status before starting each new step.

COMMUNICATION RULES:
- Avoid verbose explanations or printing full command outputs.
- If a step is skipped, state that briefly (e.g. "No extensions needed").
- Do not explain project structure unless asked.
- Keep explanations concise and focused.

DEVELOPMENT RULES:
- Use '.' as the working directory unless user specifies otherwise.
- Avoid adding media or external links unless explicitly requested.
- Use placeholders only with a note that they should be replaced.
- If a feature is assumed but not confirmed, prompt the user for clarification before including it.
- If you are working on a VS Code extension, use the VS Code API tool with a query to find relevant VS Code API references and samples related to that query.

FOLDER CREATION RULES:
- Always use the current directory as the project root.
- If you are running any terminal commands, use the '.' argument to ensure that the current working directory is used ALWAYS.
- Do not create a new folder unless the user explicitly requests it besides a .vscode folder for a tasks.json file.
- If any of the scaffolding commands mention that the folder name is not correct, let the user know to create a new folder with the correct name and then reopen it again in vscode.

EXTENSION INSTALLATION RULES:
- Only install extension specified by the get_project_setup_info tool. DO NOT INSTALL any other extensions.

PROJECT CONTENT RULES:
- If the user has not specified project details, assume they want a "Hello World" project as a starting point.
- Avoid adding links of any type (URLs, files, folders, etc.) or integrations that are not explicitly required.
- Avoid generating images, videos, or any other media files unless explicitly requested.
- If you need to use any media assets as placeholders, let the user know that these are placeholders and should be replaced with the actual assets later.
- Ensure all generated components serve a clear purpose within the user's requested workflow.
- If a feature is assumed but not confirmed, prompt the user for clarification before including it.
- If you are working on a VS Code extension, use the VS Code API tool with a query to find relevant VS Code API references and samples related to that query.

TASK COMPLETION RULES:
- Your task is complete when:
  - Project is successfully scaffolded and compiled without errors
  - copilot-instructions.md file in the .github directory exists in the project
  - README.md file exists and is up to date
  - User is provided with clear instructions to debug/launch the project

Before starting a new task in the above plan, update progress in the plan.
-->
- Work through each checklist item systematically.
- Keep communication concise and focused.
- Follow development best practices.
