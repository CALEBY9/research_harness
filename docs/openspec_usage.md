# OpenSpec 科研接入

本机安装官方 `@fission-ai/openspec` 1.12.0，Node.js 要求 >=20.19.0。
CLI 保持上游实现；科研适配位于项目 `openspec/` 和 Research Agent 的
`references/openspec-research.md`。OpenSpec 不调用模型、不判断科学结论。

## 使用

已经初始化的项目中，可以直接提出：

```text
调用 Research agent，按这份作者确认的 TODO 完成第 X 项，使用 OpenSpec
记录要求、实现和实际验收；沿用已有授权，科学口径变化交我决定。
```

当前选用 propose、explore、apply、verify、archive；上游自动加入 sync
依赖，共生成 6 个项目级 skill，位于 `.agents/skills/`。直接调用
`$openspec-propose` 表示先规划；已有明确实施请求可由 Research Agent
衔接 CLI 与当前 owner，不需要为阶段转换重复批准。

`research-task` schema 只生成一份 `tasks.md`：引用原有科学文档和 TODO，
固定本轮范围、待办、预期观察及实际证据。源科学文档不是 OpenSpec 的
自动同步目标。工作包只能代表本轮任务完成，不能代表整篇论文完成。

```powershell
openspec new change <change-name>
openspec instructions tasks --change <change-name> --json
openspec instructions apply --change <change-name> --json
openspec status --change <change-name> --json
openspec schema validate research-task
```

项目级 schema 可随仓库版本管理；不要覆盖其他项目的既有 schema。
在一个新项目使用本配置时，先读其规则，运行 `openspec init --tools codex`，
再按需复制 `openspec/schemas/research-task/`、设置默认 schema 并填写真实
科学依据。不能把本仓库或其他研究项目的路径直接当成新项目依据。

## 验收边界

- 检查要求到实现的覆盖，也检查新增代码到要求的依据。
- 验收观察来自作者确认的规则；不能为得到预期趋势而修改条件。
- CLI 的 artifact complete/ready 只说明文件或待办状态；不等于科学通过。
- 原版 verify 对 delta specs 提供检查；本 schema 无 delta specs 时，必须
  按 `tasks.md` 引用的科学条款与场景核对正确性，不能跳过。
- 缺失、部分实现、矛盾、未经要求的实现保留在现有证据表；未跑不勾完成。
- 简单修复沿用 MINI 约定，OpenSpec 不成为所有科研任务的必经步骤。

## 安装与维护

```powershell
npm install -g @fission-ai/openspec@1.12.0 --no-fund --no-audit
openspec config set telemetry.enabled false
openspec config set delivery skills
openspec config set workflows '["explore","propose","apply","verify","archive"]'
openspec config set profile custom
openspec init --tools codex --profile custom --language Chinese --no-animation
```

安装使用该软件自己的配置，不修改 Codex provider、hooks 或凭据。官方工作流
正文保留；只把本机校验器不接受的顶层 compatibility 移入 metadata，并移除
绑定 Bash 的 allowed-tools 声明，工具权限继续由当前会话控制。
`openspec update` 会重新生成 skills，之后需重做这两处元数据适配并用
`python -X utf8` 运行本机技能校验器；项目 schema 和科学规则不随生成覆盖。
新增技能应在新会话中检查发现情况；本轮只验证磁盘安装及 CLI，不声称已经
验证了新会话自动选择或科研质量提升。

离线集成测试：`python -B -m unittest discover -s tests -p test_openspec.py -v`。
测试在临时项目运行真实 CLI，检查 schema 解析、指令注入、待办状态和无
delta-spec 的归档行为；不发模型请求、不读私人科研输入。

来源：[OpenSpec 1.12.0 customization](https://github.com/Fission-AI/OpenSpec/blob/v1.12.0/docs/customization.md)。
