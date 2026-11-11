---
title: "危险操作只有一套语法：PIG 运维 CLI 安全契约"
linkTitle: "运维 CLI 安全"
date: 2026-07-02
lastmod: 2026-11-11
description: "PIG 如何分离底层原语与编排器、显式表达破坏性意图，并防止别名或结构化输出改变操作含义。"
tags: [cli, postgres, pgbackrest, pitr]
weight: 40
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-07-02<br>
> **状态：** `pg`、`pb`、`pt`、`pitr` 已于 v1.5.0 交付；2026-08-29 的 `do` 与 `build proxy` 修订随 [v1.8.1](/zh/release/pig-1.8.1/) 发布，2026-10-16 至 2026-10-17 的验收修订随 [v1.10.0](/zh/release/pig-1.10.0/) 发布。2026-11-10 的移除修订与 2026-11-11 的执行修订已在 [`a95f37f`](https://github.com/pgsty/pig/commit/a95f37f) 实现，不声明已发布。<br>
> **当前参考：** [`pig pg`](/zh/pg/)、[`pig pb`](/zh/pb/)、[`pig pitr`](/zh/pitr/)、[`pig do`](/zh/do/) 与 [`pig build`](/zh/build/)<br>
> **范围：** PIG 实现的运维命令；透明上游命令继续采用上游的确认与退出行为。

## 决策 {#decision}

操作便利性不能模糊操作含义。PIG 明确区分底层原语与多阶段编排器，显式表达破坏性意图，
谨慎分配别名，并要求计划与结构化结果描述的动作必须和文本模式真正执行的动作一致。

最重要的例子是恢复：`pig pb restore` 是 pgBackRest 原语，`pig pitr` 则协调 Patroni、
PostgreSQL 停止、恢复、重新启动与恢复后指引。任何别名都不能让这两条路径看起来可以互换。

## 背景 {#context}

第一代便利别名积累了不一致的位置参数、确认参数、输出处理与服务语义。
`restart`、`restore`、`promote`、`failover` 等相似词在不同层次代表完全不同的操作。
跨越层次的短别名可能把看似无害的调用变成缺少编排保护的破坏性原语。

自动化还暴露出假成功问题：包装器输出、子进程输出和结果渲染可能使用不同的成功定义。

## 考虑过的方案 {#alternatives}

- **尽可能增加短别名。** 冲突和跨层同义词带来的风险高于节省几个字符的价值。
- **给所有看起来危险的单词都加确认。** 对透传命令不成立，因为提示与语义必须由上游工具拥有。
- **让编排器成为原语的便利别名。** 恢复编排拥有额外的停止、验证与重启不变量，不能合并。
- **启动内层命令后立即返回成功。** 结果必须反映 PIG 拥有的完整工作流。
- **将维护命令的库名限制为 ASCII 标识符。** 这会拒绝原本支持的空格和非 ASCII 名称。
  只拒绝 libpq 连接串语法，并在生成命令时保留位置参数边界。

## 契约 {#contract}

- 同级命令名称与别名唯一；
- 子命令别名不能遮蔽另一个顶层命令；
- PIG 实现的破坏性操作要求显式确认，并在有意义时提供无副作用计划；
- 命令层在产生副作用前拒绝错误或多余的位置参数；
- 命令专用名称遵循下游 Pigsty 契约；下游 Playbook 没有显式语法时，只采用有文档说明的最窄安全边界；
- 结构化输出与文本模式共享同一个结果和成功定义；
- 含凭据的值不进入诊断输出；就绪或连通性失败必须保持命令失败，不能只记警告后返回成功；
- 底层 restore 不声称管理 Patroni 或 HA 路由；
- PITR 编排器按需停止管理器，检查 PostgreSQL 已停止，执行恢复，可选启动 PostgreSQL，
  并有意保持 Patroni 停止，等待运维人员验证；
- 额外原生参数只通过明确记录的边界传递。

2026-10-16 至 2026-10-17 的修订将相同边界用于 v1.10.0：

- 跨用户 DBSU 写入以排他方式创建私有临时文件，使用 `0600` 和执行 DBSU 的属主，拒绝符号链接与
  非普通文件目标，精确替换目标路径，失败时清理暂存。Linux 使用精确目标重命名；macOS 使用系统
  Perl 的 `rename` 系统调用，避免 BSD `mv` 将源文件移入目录的语义。
- [`repo rm`](/zh/repo/#repo-rm) 在变更前校验完整参数列表。只有零参数代表全量备份；
  `all` 仍只表示 `node`、`pgsql`、`infra`。
  `requested_modules` 保留原始请求，`removed_repos` 描述展开后的执行动作。
  `repo add`、`repo set`、`repo info` 同样整次拒绝显式空名称和逗号空项；只有省略参数
  才保留 add/set 默认选择 `all` 的行为。
  add/set 还会在初始化仓库管理器前校验模块名格式。不安全名称使整次请求失败；格式正确但
  不存在的名称仍保留添加模式的部分成功行为，替换模式则在变更前整次拒绝。
- 显式指定 `pg -D` 时，SQL 操作和数据库枚举绑定到该目录记录的端口与 socket，元数据不明确时先失败。
  省略 `-D` 时保留原生客户端的默认连接方式；实例操作的默认目录仍为 `/pg/data`。
  显式空字符串或纯空白的 `-D` 在配置初始化和操作前失败。
  计划、确认重试和验证命令保留相同的目标与操作选项，包括显式的 `-D /pg/data`。
  `VACUUM FULL` 计划与执行一样要求确认。
  2026-10-17 的维护命令修订要求在计划、确认和执行前拒绝连接串形式的数据库参数，且不回显原值。
  否则 libpq 连接串仍能覆盖所选主机和端口，并将凭据带入输出。
  `vacuum`、`analyze`、`freeze` 在维护任何数据库前，先校验枚举出的完整库名列表。
  生成的 `vacuum` 和 `repack` 命令将全部选项放在 `--` 之前、库名放在其后，
  保证 `--all` 这样的库名仍表示单个数据库。
- 覆盖非空非托管 fork 目标必须有明确记录目标的匹配元数据，普通非 PGDATA 目录也不例外。
  空目标仍可使用，托管 fork 必须按名称替换。私有路径以 DBSU 解析；无法解析的别名仍直接失败。
  2026-10-17 的复核撤销额外的 `/pg/data` 禁令，按目标归属、源目标关系和运行状态决定是否允许操作。
  约定路径既不能识别所有主库，也可能是合法的 fork 目标。
  保留受管孤儿目录的强制清理契约。
  非托管 fork 删除的本地路径检查遇到权限不足时，以所选 DBSU 重试；确认目标为目录且不是
  符号链接后，才允许继续删除。
- 不能仅凭 `EPERM` 放行 `pg init --force` 或 PITR 恢复。独立的可执行程序身份可证明 PID 已被复用；
  身份无法确认时仍为未知。向存活 PID 发信号或使用其连接元数据执行 SQL 前，必须确认它属于 PostgreSQL。
  未知状态不提供可用于强制停止升级的 PID，fork start 也不能写入成功状态；列表显示 `unknown`
  并在结构化结果中设置 `runtime_unknown: true`。
  角色检测在运行状态不明时同样失败；文件中的角色证据不能推翻已确认的停止状态。
  强制初始化分别报告探测失败与正在运行的冲突。
  计划前置检查将无法确认的运行状态报告为 `unknown`，不能以 PID 零标记为检查通过。
  状态查询区分权限失败（`130201`，退出码 `3`）与其他探测失败（`130808`，退出码 `1`）；
  两类失败中的部分数据均不能证明实例已停止。
- 时间线查询将 SQL 绑定到所选目录有效 PID 元数据中的端口与 socket。无法解析时，使用该目录的
  `pg_controldata` 或报告未知时间线；promote 执行过程及必须确认主库角色的成功判据保持不变。
- PITR 取消确认或遇到 EOF 时，在停服务、恢复与启动之前返回确认缺失（`161001`，退出码 `7`）。
  验收必须执行真实确认路径，并检查生命周期操作的副作用为零。
- `PIG_NON_INTERACTIVE` 和结构化执行关闭提示 stdin，并加上 sudo `-n`，旧式结构化包装也遵循
  此规则。原生透传与显式数据 stdin 保留各自契约。
- 敏感捕获输出和错误详情保持私有，签发密钥加载失败不回显输入。文档规定的原始导出通道仍然可用。

2026-11-10 接受的修订要求 [`pig do`](/zh/do/#postgresql-operations) 显式表达移除意图：

- `pgsql-rm` 必须传递 `pg_rm_pkg=false`；只有启用 `--uninstall` 时才传递 `pg_rm_pkg=true`。
  集群与实例移除均覆盖 Inventory 和剧本的默认值。Pigsty 默认值为 `true` 时，省略变量不能表达按需卸载。
- `pgmon-rm` 必须删除 `pgmon-add` 创建的同一远程监控目标，即 `infra` 主机上的
  `/infra/targets/pgrds/<cluster>.yml`。对过时目录执行 `file state=absent` 成功，不能证明实际目标已移除。

2026-11-11 接受的修订补齐执行和诊断边界：

- 文本 `pg status` 与结构化结果采用相同的成功或失败退出状态，打印摘要不能把已停止实例或探测失败变成成功。
- `pg psql -f` 启用 `ON_ERROR_STOP=1`，包括从 stdin 输入的脚本；SQL 错误停止执行并返回失败。
  这不是隐式事务，不会撤销已提交的操作。相对脚本路径在切换用户前解析，交互式 psql 保留终端输入输出。
  PIG 的数据目录、日志目录与启动日志参数也采用相同的调用者相对路径规则。
- 内部数据库枚举使用 `psql -X`，用户启动文件的输出不能成为数据库操作数。
- `pg init --force` 确认重试与 `pg kill` 计划保留所选数据目录、PostgreSQL 安装、DBSU 和操作参数，
  生成的 shell 参数正确引用。
- 恢复与克隆的预检错误在文本模式可读，不额外打印用法；结构化模式继续采用既有结果契约。
- DBSU 流式操作只保留有上限的诊断尾部；用于读取完整数据的 API 保留全部内容，
  不对配置文件或 SQL 结果等机器消费数据实施诊断截断。

## 影响 {#impact}

部分历史缩写被移除，一些脚本需要采用 cluster-first 或显式目标语法。
作为回报，命令名称保留了层次边界，计划对应真实动作，恢复自动化也不会悄悄用原语替换编排器。

计划列出受影响的资源与动作，供用户在执行恢复前审阅。

## 验证与演进 {#verification}

v1.10.0 已提交修订的固定源码与回归测试证据包括：
[运行身份与 SQL 目标](https://github.com/pgsty/pig/commit/526410e2cbbfa9658533d179bff91a8cdc190ffd)、
[fork 归属与私有路径](https://github.com/pgsty/pig/commit/9db279947ef5d2492956a482a984685e8f807c5f)、
[PITR 取消与未知状态](https://github.com/pgsty/pig/commit/54d4bae5480a2424ec4842e64ca8e9f810e8d354)、
[计划目标保留](https://github.com/pgsty/pig/commit/da0706fa3c676b8d912b4c7a556ee58dbe8045f3)、
[状态错误分类](https://github.com/pgsty/pig/commit/e6cd11f59590d158749eface28a470a78e17bba4)。上述修订已随 [v1.10.0](https://github.com/pgsty/pig/releases/tag/v1.10.0) 发布。
后续的[维护数据库名与 `--` 操作数边界修订](https://github.com/pgsty/pig/commit/5cf691b7fc559a5f3dd0c9d346927188f8b63375)
包含 Cobra 参数重解析测试与真实 libpq 目标边界回归测试。
[仓库参数预检](https://github.com/pgsty/pig/commit/981726b27786be78832b2c1b457e55ebf7505fe9) 在准备密钥或写入仓库前拒绝
不安全模块名，并保留格式正确但模块不存在时的添加部分成功行为。

规范命令契约在 [`c62c0f5`](https://github.com/pgsty/pig/commit/c62c0f5) 中进入仓库。
后续提交继续统一别名、早期校验、恢复目标、服务语义与角色检测。
Guard 测试遍历 Cobra 树，拒绝同级与跨层别名冲突；恢复测试覆盖计划、确认、停止升级、旁路恢复、
重启行为与结构化失败结果。
维护命令的回归检查应使用 Cobra 重新解析生成的命令，并让真实 libpq 客户端访问受控本地端点；
仅检查参数列表中包含 `-h` 和 `-p` 不足以证明目标绑定正确。

Patroni 后来改成透明透传，这仍遵循同一原则：PIG 只为自己拥有的工作流提供安全保证。

同一契约在 [`3e1603b`](https://github.com/pgsty/pig/commit/3e1603b2bfbb949fb77b7ecd5fd458ec2ee45d25)
中扩展到 `pig do` 的名称与集群校验，并在
[`a880485`](https://github.com/pgsty/pig/commit/a88048596dffdfd6c1bb51cdbe7da6782a11cc22)
中封闭 Ansible 内置目标。软件包驱动、凭据安全且如实报告失败的 `build proxy` 设置进入
[`220ef9c`](https://github.com/pgsty/pig/commit/220ef9c722b54951d3dc502ea3e3baafd642b592)，
随后由 [`74cb128`](https://github.com/pgsty/pig/commit/74cb1281860fae659f2aa4fec2898af34a0c2519)
补齐结构化参数遮盖与机器注解，并在
[`de7ffd0`](https://github.com/pgsty/pig/commit/de7ffd0e81e500ea2f4268ca326917aa385150ca)
中把可选参数同步到机器语法。这些修改均在 Ubuntu 24.04 与 Rocky Linux 9 ARM64 Farrow
客体中完成实机测试，并在 [v1.8.1 CI](https://github.com/pgsty/pig/actions/runs/33747971725)
通过后，从源码提交 [`1c6f524`](https://github.com/pgsty/pig/commit/1c6f52401accc8ad6d7e8ab51248895632d7629b)
正式发布。

移除修订依据 Pigsty 固定源码中的
[`pg_rm_pkg` 默认值](https://github.com/pgsty/pigsty/blob/bc5c20b22081e6fffe43fd068a6682c34fc333e4/roles/pg_remove/defaults/main.yml)
与[远程目标注册路径](https://github.com/pgsty/pigsty/blob/bc5c20b22081e6fffe43fd068a6682c34fc333e4/roles/pg_exporters/tasks/main.yml)。
回归检查须覆盖集群和实例默认保留软件包、显式卸载软件包，以及删除远程目标时实际传给 Ansible 的参数。
这些检查验证包装器契约，不代表部署验收或 PIG 发布制品。

执行修订要求验证终端文件描述符、SQL 文件错误传播、调用者相对路径、不受启动文件影响的库名枚举、
状态退出码一致性，以及用 Cobra 重新解析生成的目标命令。大输出测试应区分诊断流式输出与完整数据捕获。
这些验收要求不构成发布证明。

## 当前状态 {#status}

明确需要 pgBackRest 原语时使用 `pig pb restore`；需要受控恢复流程时使用 [`pig pitr`](/zh/pitr/)。
当前语法与平台要求见对应命令参考页。
