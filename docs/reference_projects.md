# 参考项目：取其可用设计，服务个人科研协作

核对日期：2026-09-08。以下依据指定版本的官方仓库、文档和部分实现进行设计
比较。未安装这些项目，未运行其模型实验，也不据此评价哪个项目科研能力最强。
本文件中的适用性与采用建议属于本项目的判断。

## 选择结果

| 项目 | 核实的设计 | 本项目的处理 |
|---|---|---|
| Nature Skills | 分任务 skill、共享资源、manifest 与条件资源加载 | 保留现有本地增强的 owner 基线；不自动升级到最新上游 |
| ARS-Codex | 单入口多 workflow；可选完整 runtime 默认关闭；问题与论证有独立提示资源 | 将问题/设计/论证作为按需辅助；沿用已有本地评估结果，不安装第二套主路由 |
| Prime Agent | 界面、执行 runtime 与持久化状态分层；持久 REPL；有界任务及 refine 机制 | 借鉴源码/状态/运行时的清晰分层和可审阅小修改；当前继续复用 Codex 执行 |
| AutoResearchClaw | 完整研究 pipeline 上提供 co-pilot、逐步和其他干预模式 | 仅借鉴在科研判断处呈现可编辑产物的交互；不搬用自动推进的阶段管线 |
| OpenAI4S | 独立确定性场景评测层；文档明确区分模拟自契约与真实生产行为 | 明确结构检查、工具行为、科研质量三层证据；出现真实执行问题时再加回放 |
| Hermes Agent | 记忆管理通过 provider 接口组织；当前实现控制外部 provider 数量 | 复用现有项目记忆入口，保持稳定偏好和任务状态分层；暂不引入记忆服务 |
| academic-figures-drawer | 独立 figure/visual contract、可编辑图形对象、连线与缩放可读性要求 | 作为实际概念图任务的比较候选，现由 nature-figure 继续负责；许可待明确前不复制代码/素材 |
| Claude Scholar | 项目知识与运行时绑定分开；registry 与导航笔记分工；技能可选择安装 | 借鉴单一事实源与衍生导航的分工，继续使用已有 `.agent/` 和 KB；不新增 Obsidian 强依赖 |

## 来源与版本

所有项目在核对时 GitHub `archived=false`。更新时间表示仓库有推送，不代表
质量、维护承诺或与本机兼容。可运行性及实际收益仍需对应任务验证。

### Nature Skills

- 本次参考 HEAD：`7e626a86a0ac8d078be224e0a76aa1327875b0a1`；推送日期 2026-09-08。
- [官方仓库及 README](https://github.com/Yuan1z0825/nature-skills/tree/7e626a86a0ac8d078be224e0a76aa1327875b0a1)，根许可 Apache-2.0。
- 本地已有对应的能力与增强。本次导入以实际安装为准，未用新 HEAD 覆盖它。
- 判定：**保留已覆盖能力**。当前缺口是独立版本管理与迁移说明，本仓库已处理。

### ARS-Codex

- HEAD：`925975e933a20893b81681d925a3404e3b7f73b7`；推送日期 2026-09-02。
- [官方入口与可选 runtime 说明](https://github.com/Imbad0202/academic-research-skills-codex/tree/925975e933a20893b81681d925a3404e3b7f73b7)，[研究问题资源](https://github.com/Imbad0202/academic-research-skills-codex/blob/925975e933a20893b81681d925a3404e3b7f73b7/skills/academic-research-suite/ars/deep-research/agents/research_question_agent.md)。
- 根许可在既有本地源码审查中为 CC BY-NC 4.0；本次 GitHub API 仅返回 NOASSERTION，
  不能把它当作 MIT/Apache。若未来复制内容，重新读取目标文件许可。
- 本机已有问题/方法/写作 owner 及前次候选评估，未证明整套替换的质量收益。
- 判定：**按真实问题评估局部候选**，保持作者选定的研究阶段。

### Prime Agent

- HEAD：`bf8894afa55832f7cfa2094c8a0d041bc680a691`；推送日期 2026-09-08；MIT。
- [分层架构](https://github.com/PrimeIntellect-ai/prime-agent/blob/bf8894afa55832f7cfa2094c8a0d041bc680a691/packages/coding-agent/docs/architecture.md)，[refine 与长期任务说明](https://github.com/PrimeIntellect-ai/prime-agent/blob/bf8894afa55832f7cfa2094c8a0d041bc680a691/README.md)。
- 它包含自己的执行、daemon、REPL 与子代理体系，直接引入会增加第二套 runtime。
  本机已经有 Codex 工具执行和项目状态，当前没有证据要求重建它们。
- 判定：**采用分层思想**；可恢复执行组件暂缓，待当前 runtime 出现可复现缺口。

### AutoResearchClaw

- HEAD：`be4ba4755bf1b52220f25e13b2293b5956590070`；推送日期 2026-08-19；MIT。
- [Co-Pilot Guide](https://github.com/aiming-lab/AutoResearchClaw/blob/be4ba4755bf1b52220f25e13b2293b5956590070/docs/HITL_GUIDE.md)。
- 文档允许编辑、拒绝、注入指导与协作；它的 co-pilot 仍是流水线自动推进中暂停。
  文档还描述超时处理、学习后自动批准与多种自动模式，这些不是本项目默认行为。
- 判定：**借鉴科研决策点的交互**。本机已有作者决定边界，不新增固定阶段审批表。

### OpenAI4S

- HEAD：`4e96b251a88197ec070b3e088a720a1a55e817f3`；推送日期 2026-09-08；MIT。
- [确定性场景与评测说明](https://github.com/PKU-YuanGroup/OpenAI4S/blob/4e96b251a88197ec070b3e088a720a1a55e817f3/harness/README_zh.md)。
- 此处的 `harness/` 特指场景评测层。它主动限定通用 runner 对生产运行时的证明
  范围，真实模型和外部资源需要另行启用；不能把该目录理解为完整 runtime。
- 判定：**采用验证分层的说明方式**。现有 validator 明确报告模型行为执行数为 0；
  新增回放只有真正触达待测执行边界才有价值。

### Hermes Agent

- HEAD：`b3399c139624a0081d70397741a5b45f60fbe1f4`；推送日期 2026-09-08；MIT。
- [MemoryManager 实现](https://github.com/NousResearch/hermes-agent/blob/b3399c139624a0081d70397741a5b45f60fbe1f4/agent/memory_manager.py)，[官方项目说明](https://github.com/NousResearch/hermes-agent/tree/b3399c139624a0081d70397741a5b45f60fbe1f4)。
- 已检查实现入口的 provider 边界；没有评测其召回质量，也不把自动记忆写入视为
  本地的既定授权。本机共享项目记忆已承担跨会话恢复。
- 判定：**已有能力优先**。只在真实恢复失败时定位记忆读取/更新的具体缺口。

### academic-figures-drawer

- HEAD：`b2661ea9092f833dce93fb84ddbc2a90027eb610`；推送日期 2026-08-21。
- [figure contract](https://github.com/M1n-n9/academic-figures-drawer/blob/b2661ea9092f833dce93fb84ddbc2a90027eb610/references/figure-contract.md)，[文件与脚本](https://github.com/M1n-n9/academic-figures-drawer/tree/b2661ea9092f833dce93fb84ddbc2a90027eb610)。
- GitHub 元数据未识别许可，根文件列表也没有 LICENSE；素材另有第三方 notices。
  因此目前只评估设计，不导入实现或素材。
- 判定：**暂缓采用**。用作者的实际图与现有 nature-figure 比较科学语义、可编辑性、
  小尺寸可读性和修改负担后，再判断有无可独立实现的局部改进。

### Claude Scholar

- HEAD：`6ed46dac03191c7a734f49ed48b41195012098ff`；推送日期 2026-08-27；MIT。
- [项目知识库 owner](https://github.com/Galaxy-Dawn/claude-scholar/blob/6ed46dac03191c7a734f49ed48b41195012098ff/skills/obsidian-project-kb-core/SKILL.md)，[选择性安装与安装所有权说明](https://github.com/Galaxy-Dawn/claude-scholar/blob/6ed46dac03191c7a734f49ed48b41195012098ff/README.md)。
- 它将项目知识源与 CLI 绑定分开，区分确定性链接检查和语义决策；直接整体安装
  则会带来另一套技能、hooks 和配置。本机已有相应 owner 与 KB。
- 判定：**采用职责区分，复用现有目录**。只有出现重复事实源或恢复冲突才修复。

## 实施与评估范围

本次实际落地的是源码仓库、边界文档、迁移验证工具与反馈流程；没有从这些
新参考项目复制代码、启动服务或修改现用研究技能。Nature/Humanizer 是此前已
安装的基线，其本次导入来源与许可另见 `THIRD_PARTY_NOTICES.md`。

下一次技能行为改进从真实科研失败开始，参照以上对应设计提出最小候选，
用现有/候选的可比较产物判断收益。复杂度、stars 和 demo 不作为采用依据。
