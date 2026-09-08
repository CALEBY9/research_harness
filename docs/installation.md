# 源码维护、暂存与安装

## 现有机器

初次导入采用 34 个实际已安装技能作为来源。Nature 源仓库的 HEAD 为
`54144dcf6376b034716bd70edd40ad2cf407943e`，工作树存在本地增强，因此不能
用该 commit 或最新上游版本替代本次实际安装快照。

`docs/import_manifest.json` 记录逐文件初次导入校验值，供迁移证据使用。
它不是今后禁止修改技能的冻结门槛。`scripts/import_local_skills.py` 是
一次性导入工具；目标已经存在时拒绝覆盖。正常维护使用文件 diff。

原安装保持在本机既有技能目录。本仓库不复制全局 AGENTS、运行时配置、
插件缓存、论文库、会话、项目状态或归档候选。

## 隔离暂存

下面命令需要指定一个尚不存在的目录，可选择单个技能，也可省略 `--skill`
暂存全部技能。暂存仅方便审阅，不会替换任何当前安装。

```powershell
python scripts/harness.py stage --target .\local_state\trial_skills --skill research-agent
```

重跑时换一个新的目标目录。工具不提供覆盖现有目录的选项。

## 换机器或安装候选

1. 克隆指定分支/commit，运行 `validate` 和单元测试。
2. 运行 `doctor`。它列出含本机绝对路径的文件和行号，不会自动改写路径。
3. 按需要绑定 Nature shared、KB、文档工具等依赖。路径提示也可能来自示例，
   须检查调用语义；简单字符串替换不能证明可迁移。
4. 查看现有安装与候选 diff，保留现有有效本地修改，选择本次安装的技能集合。
5. 使用该运行时支持的安装方式，并验证实际技能发现与一条目标任务。

Codex 当前官方文档支持仓库/用户级 `.agents/skills`，并说明同名技能不会
自动合并。本快照源自混合的 `.agents/skills` 与历史 `.codex/skills` 安装。
不要把所有快照目录再放进已含同名技能的发现目录。
[官方来源](https://learn.chatgpt.com/docs/build-skills)

`humanizer:humanizer` 是本机现有 English Humanizer 的名称约定；部分旧 adapter
含下划线。首版保留名称以避免破坏现有调用，不据此声称所有 Agent 都兼容。

## 公开发布

当前按私有个人维护仓库处理。转公开前需逐项处理本机路径、项目名称、私有
fixture 指针和第三方素材的再分发范围；本次的密钥模式扫描不等于完整脱敏。
保留第三方 LICENSE 和 NOTICE，不能给整包第三方内容重新指定统一许可。
面向其他用户的一键安装/plugin 发布是后续独立工作。
