---
title: "受保护软件包只能通过显式内核别名卸载"
linkTitle: "受保护软件包卸载"
date: 2026-11-11
lastmod: 2026-11-11
description: "根据最终软件包和原始输入决定卸载边界，同时保留独立语言包的卸载能力。"
tags: [ext, catalog, cli]
weight: 96
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-11-11<br>
> **状态：** 已实现，源码提交为 [`a95f37f`](https://github.com/pgsty/pig/commit/a95f37f)；2026-11-11 已批准软件包边界、显式别名与整单拒绝规则，不表示已发布。<br>
> **当前参考：** [`pig ext rm`](/zh/ext/#ext-rm)<br>
> **范围：** `ext rm` 的软件包选择；不表示已有对应发布标签，或已模拟包管理器依赖事务。

## 决策 {#decision}

保护 PostgreSQL server、共享 contrib 包以及支持的替代内核。只有显式使用登记的内核或软件包组
别名，才允许卸载对应的受保护包。通过扩展名解析到同一个包时，必须在调用包管理器之前拒绝。
独立的语言扩展包仍可通过扩展名卸载。

判定同时依赖最终包名与原始输入。扩展的 `contrib` 标记或软件包的 `postgresql` 前缀都不足以单独决定。

## 背景 {#context}

[基线解析器](https://github.com/pgsty/pig/blob/2c2d365eae7e9b33cce8b17d852be82ae7f88764/cli/ext/pkgresolve.go)
将扩展名和别名转换为软件包，并在[卸载](https://github.com/pgsty/pig/blob/2c2d365eae7e9b33cce8b17d852be82ae7f88764/cli/ext/rm.go)
之前按包去重。Debian 上 `pg_trgm` 可以解析为 `postgresql-18`，EL 上则是
`postgresql18-contrib`；`plpgsql` 直接对应 server。这些卸载范围都大于用户输入的扩展。
`spock` 等分支扩展同样可能解析到 `pgedge-18` 内核包。

PL/Python、PL/Tcl、PL/Perl 也带 contrib 元数据，但其系统软件包独立于 server 与 contrib 集合。
PL/Tcl 与 PL/TclU 共用语言包，PL/Perl 与 PL/PerlU 也一样。因此不能机械要求“一扩展一包”，
否则会误伤语言包以及 PostGIS 这类正常的多扩展软件包。

## 考虑过的替代方案 {#alternatives}

- **拒绝所有 contrib 扩展。** 会误伤独立语言包。
- **拒绝所有共享包。** 普通扩展套件本来就可能共用软件包。
- **只要是 alias 就放行。** 分类别名也可能展开到由内核提供的扩展，alias 身份不足以表达卸载内核的意图。
- **同一请求里有一个 alias 授权，就放行同包的所有输入。** 这会掩盖混合请求中的危险扩展输入；应先逐项校验再去重。
- **新增通用强制标志。** 专门的内核别名能表达具体卸载范围，`--yes` 继续只负责确认。

## 契约 {#contract}

在代码里维护一份小型受保护包模板与授权别名的对应表。别名带目标大版本时，按别名中的版本展开。
精确匹配完整包名，覆盖支持的内核分支；不根据宽泛前缀或可更新的目录标记授予权限。
登记表覆盖受支持的内核包族。新增内核包族需要更新这份代码中的边界；
仅更新目录元数据既不能增加保护范围，也不能授予新的卸载权限。

以 PostgreSQL 18 为例，已接受的行为如下：

| 输入 | 实际范围 | 判定 |
|:---|:---|:---|
| `pg_trgm`、`earthdistance`、`tablefunc` | Debian server 或 EL contrib 集合 | 拒绝 |
| `plpgsql` | server | 拒绝 |
| `plpython3u`、`pltcl`、`pltclu`、`plperl`、`plperlu` | 独立语言包 | 允许 |
| `vector`、`postgis` | 普通扩展包 | 允许 |
| `pg18-server`、`pgsql-server -v 18` | 显式 server 包组 | 允许，展示组内所有包 |
| `pg18`、`pg18-core`、`pg18-mini`、`pg18-full`、`pg18-main` | 显式 PostgreSQL 包组 | 允许该组登记的受保护包 |
| `pg18-contrib` | EL 独立 contrib 包 | 通过这个专用别名允许卸载 |
| Debian 上的 `pg18-contrib` | 当前映射没有独立包 | 拒绝，不能悄悄改为删除 server |
| `spock`、`snowflake`、`lolor` | pgEdge 内核 | 拒绝 |
| `pgedge -v 18` | 显式 pgEdge 内核 | 允许 |
| `ivorysql_ora`、`babelfishpg_tsql`、`aux_mysql` | 替代内核 | 拒绝，提示对应内核别名 |
| `pg18-etl` 等分类或无关包组 | 任意受保护包 | 拒绝 |
{.full-width}

对应的 `pgsql-*` 别名使用 `-v`；既有 `postgresql` 和各分支内核别名逐个登记精确授权范围。
保留已有版本限制。一个 alias 只能授权自己的包族和目标大版本，不能替另一项输入授权。

`orioledb` 当前同时是扩展名与内核 alias。保护判定保留其扩展含义，为明确卸载内核提供
无歧义的 `orioledb-server` 别名，避免由查找顺序决定是否允许删除。

每项输入保留原始名称、解析类型（扩展、扩展包简称、显式包组或分类）、命中的 alias 与完整软件包列表。
完成逐项保护检查后，再合并去重生成执行命令。只要任一输入通过未授权路径命中受保护包，
整次卸载拒绝，其他安全扩展也不先删；不调用 sudo 或包管理器。交换参数顺序不得改变结果。

执行与 `--plan` 共用同一检查。被阻止的计划包含失败的前置条件，不包含可执行的卸载动作；
执行返回错误码为 `100102` 的“受保护软件包”参数错误。两者都返回用法错误退出状态 `2`。
诊断包含原始输入、最终包名和所需的显式 alias，不自动执行或确认替代命令。
`--yes` 不能绕过保护，已有包管理器确认流程继续保留。

允许执行的计划应说明实际删除软件包的范围，包括独立语言包或普通扩展包中其他受影响的扩展，
不能声称只删除一个数据库扩展。计划也不宣称已经预测 APT/DNF 的全部依赖卸载。

`ext update` 同样存在通过扩展名意外选中整个内核的可能。建议后续复用来源检查，
但升级保护作为单独的范围建议，本卸载设计不自动扩大为禁止更新。

## 影响 {#impact}

删除内核捆绑扩展的脚本需要显式选择软件包边界，或另行管理数据库对象。
独立 PL 包仍可卸载，即使目录标记 contrib，或一个包同时提供受信与非受信变体。

实现时应同步中英文扩展参考、别名帮助、卸载错误与执行计划；安装和分类列表的既有行为保持兼容。

## 验证 {#verification}

使用真实目录映射与受控解析 fixture，覆盖 Debian、EL 和支持的大版本：server/contrib 拒绝、
语言包放行、分支内核、OrioleDB 名称冲突、alias 与 `-v` 不同、分类展开、混合请求的两种顺序、
重复软件包以及 `--yes`。

被拒绝的执行应断言包管理器调用数为零。计划应具有失败的前置条件、不含卸载动作，且与执行报告相同原因。
允许的 alias 必须只产生列明的软件包。Cobra 测试验证文本、JSON 和退出状态；使用隔离的假命令，
不在宿主机实际卸载软件包。

## 当前状态 {#status}

本决策已接受，[当前参考](/zh/ext/#ext-rm) 描述批准的契约。
上文的固定源码链接证明原始缺陷；实现已在 [`a95f37f`](https://github.com/pgsty/pig/commit/a95f37f)
中验证，发布产物仍是独立阶段。
