# Work package

## Source and scope

- Objective and owner: 接入官方 OpenSpec，并补齐 Research Agent 对讨论文档/TODO 的执行追溯；owner 为 skill_evolve_workflow，沿用 Nature/local 任务边界。
- Authority: 用户 2026-09-08 明确同意修改并要求本地安装 OpenSpec、按科研任务微调；仓库 AGENTS.md 与 docs/architecture.md；现有 references/research-code-spec.md。
- Scope: 官方 CLI 安装、项目技能、schema、Research Agent 的局部引用/验收约定、使用文档和离线集成测试。生产研究代码、私有论文输入、全局 provider/hooks、自动多代理和模型评估不在本工作包内。
- Evidence: 已观察到旧项目入口与当前讨论文档冲突、下游 UNKNOWN 到 0 的条件性风险；原有条款与边界测试已覆盖部分要求。归类为项目状态修复和执行衔接缺口，不主张重写专业 owner 或新增科研裁决能力。
- Recovery: 原有 router/reference 在 Git 初始版本及忽略的 local_state 安装备份中；安装文件与项目配置独立于运行中的科研代码。

## 1. Tasks

- [x] 1.1 安装官方 OpenSpec 1.12.0 并配置项目级 Codex skills；验收 CLI 版本及安装路径。
- [x] 1.2 用 research-task schema 复用科学原文，只保留单份工作包；验收真实 CLI 解析、指令、待办及归档行为。
- [x] 1.3 补充 Research Agent 的双向追溯和条件性 OpenSpec 引用，核对原 owner/授权/科学边界；验收受影响文件、安装同步和技能结构检查。
- [x] 1.4 运行工具与集成测试，记录结果及行为评估限制；验证不读取私有研究输入、不调用模型。

## Acceptance evidence

| Requirement/source | Implementation/artifact | Check and expected observation | Actual result/evidence locator | Status |
|---|---|---|---|---|
| 用户安装要求 | 官方 npm 包及项目 .agents/skills | 版本 1.12.0，6 个上游技能 | openspec --version=1.12.0；生成技能经本机 quick_validate 校验通过 | 已验证 |
| 复用既有科学文档 | openspec/schemas/research-task | 单 tasks artifact；归档不改外部科学源 | tests/test_openspec.py 4/4：真实 CLI、临时目录，无模型调用 | 已验证 |
| TODO 执行一致性 | skills/research-agent/references | 明确科学源与实际验收，保留 owner 和已有授权 | 三个安装文件与维护源码逐字节一致；局部规则审阅；quick_validate 通过 | 文件接入通过，行为效果未评估 |
| 证据诚实 | tests 与 docs/openspec_usage.md | CLI ready 与实际完成分开；不宣称科学质量提高 | 总计 14/14 工具/集成测试；harness validate PASS，behavioral_evaluations_executed=0 | 已验证工具边界 |

## Review and handoff

- 无新增研究阶段、调度器、运行时、语义 hook 或模型调用。
- 官方工作流正文保持上游；兼容性字段移入 metadata、移除 Bash-only 工具元数据，以通过本机校验并使用会话工具权限。项目配置和 Research Agent reference 承担科研约定。
- 本次是用户指定安装与文件/CLI 接入验证。静态检查与同一 agent 的路由复核不等于独立行为评估；科学质量改善须另用真实任务和作者评价。
- 执行命令：`python -B -m unittest discover -s tests -v`、`python -B scripts/harness.py validate`、`openspec schema validate research-task`、`python -X utf8 -B <skill-creator>/scripts/quick_validate.py <affected-skill>`。
- 已修正测试中的 Windows 短路径/长路径比较假设。校验器的 GBK 默认读取通过 `-X utf8` 修正；上游 compatibility 顶层字段与本机校验 schema 不一致，通过元数据适配解决。
- 路由审阅：普通论文润色保留 nature-polishing；只读 TODO 审计不实施；已授权代码工作包沿用原 owner；外来建议修改科学定义须作者决策。此为同一 agent 的约定审阅，不计作行为试验或质量提升。
