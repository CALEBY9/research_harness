# Research Harness

由研究者掌握方向、以真实证据为基础的个人科研 Agent 工作环境。

围绕已经在本机使用的 Research Agent，维护可版本化的技能、上下文约定、
工具和评估案例。你决定问题、方法与主张，Agent 完成明确授权的研究任务。
从已有手稿、分析结果或某个中间阶段开始都可以；任务完成后由你选择下一步。

## 当前版本

- 导入 34 个现用研究技能及其支持文件，保留 Nature Skills 的本地增强。
- 保留 Research Agent 的 31 条维护回归定义；其中 2 条需要私有论文片段。
- 提供 Python 标准库维护命令：源码验证、本机路径诊断、隔离暂存。
- 记录 8 个参考项目的来源、设计取舍与改进路线。
- 默认维护私有仓库。知识库、研究项目、论文片段、会话和凭据不在导入范围。

这是运行在现有 Codex 技能体系上的源码与维护层。模型调用、工具权限、
交互和会话执行仍由 Codex 提供。首版没有实现独立 Agent runtime、自动科研
流水线、定时自我修改或跨机器一键配置。

## 快速使用

需要 Python 3.10+。在仓库目录运行：

```powershell
python scripts/harness.py validate
python -m unittest discover -s tests -v
python scripts/harness.py doctor
```

现有安装可继续用原来的方式调用：

```text
调用 Research agent，基于这份已确认的大纲修改引言，保持研究问题和引用不变。
调用 Research agent，检查这个分析结果能支持什么结论，先只读。
调用 Research agent，帮我比较这两个方法，我来决定采用哪个。
```

仓库 `skills/` 是维护源码，不会因 `git pull` 自动替换本机技能。
在新机器上，先诊断环境依赖，再将需要的技能安装到该运行时支持的技能目录。
本机路径、KB、Office、文献服务与平台工具需要单独绑定，见
[迁移与环境说明](docs/installation.md)。

## 如何持续优化

1. 从真实任务记录一个具体问题，例如丢失已确认的大纲、把语言润色变成重写。
2. 在分支中修改对应 owner 的最小部分，并保留一条能重现问题的案例。
3. 先运行离线检查，再用相同资料比较现用版与候选版。
4. 由作者判断证据支撑、事实保留和修改负担；通过后合并并更新受影响的安装。

GitHub 保存技能和经过脱敏的反馈。真实论文评估留在本地，向仓库记录必要的
匿名结论；不把模型自评分当作科研质量提升的证明。

- [系统边界与个人习惯](docs/architecture.md)
- [参考项目比较与选择](docs/reference_projects.md)
- [迭代与评估](CONTRIBUTING.md)
- [优先级路线](docs/roadmap.md)
- [迁移验证记录](docs/validation.md)
- [第三方来源与许可](THIRD_PARTY_NOTICES.md)

技能的文件结构与渐进加载遵循 [OpenAI 官方技能说明](https://learn.chatgpt.com/docs/build-skills)。
当前导入包含历史平台约定；结构验证不会自动证明各平台都支持这些约定。
