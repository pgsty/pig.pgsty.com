---
title: "PostgreSQL 19 生命周期窗口与默认大版本解耦"
linkTitle: "PostgreSQL 19 生命周期"
date: 2026-11-21
lastmod: 2026-11-24
description: "在 PostgreSQL 19 正式发布后将活跃支持窗口推进至 15-19，同时保持 18 为默认主版本并保留历史大版本的显式操作能力。"
tags: [ext, repo, build, sty]
weight: 98
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-11-21<br>
> **状态：** 已实现（已在 [`v1.11.0`](https://github.com/pgsty/pig/releases/tag/v1.11.0) 之上的源码与本地测试中验证，尚未随正式版本发布）。<br>
> **当前参考：** [`pig ext`](/zh/ext/)、[`pig repo`](/zh/repo/)、[`pig build`](/zh/build/)、[`pig sty`](/zh/sty/)、[`pig pg tune`](/zh/pg/#pg-tune)<br>
> **范围：** PostgreSQL 活跃大版本窗口、默认主版本选择、历史退役版本的显式操作、软件源模块、构建工具集、Pigsty 配置模板改写，以及按版本裁剪的调优参数。

## 决策 {#decision}

将 PostgreSQL 19 从 Beta 转为活跃支持窗口（`19, 18, 17, 16, 15`），并将已停止维护（EOL）的
PostgreSQL 14 移出活跃生命周期默认值、可用性矩阵展示、内置软件源模块、默认构建依赖与 Pigsty
配置模板候选。

将“推荐默认主版本”（`PostgresDefaultMajorVersion = 18`）与“最新活跃主版本”
（`PostgresLatestMajorVersion() = 19`）解耦。在未探测到本地 PostgreSQL 安装且未显式传入 `-v`
时，原本回退到最新活跃版本的命令统一保持默认选择 PostgreSQL 18。

保留已退役大版本（`10–14`）的显式操作能力，包括软件包安装、扩展管理、动态分类别名、本地实例探测与
核心包误删保护，但不在内置软件源清单中继续保留 EOL 的 `pgdg14` 仓库定义。

## 背景 {#context}

在 [`v1.11.0`](https://github.com/pgsty/pig/releases/tag/v1.11.0)（提交
[`365bf12`](https://github.com/pgsty/pig/commit/365bf1282fdb)）中，PIG 将 `18, 17, 16, 15, 14`
定义为活跃稳定版本，将 `19` 定义为 Beta 目标，且多处子系统将隐式默认版本直接绑定在
`PostgresLatestMajorVersion()` 上：

- `pig install`、`pig ext add/rm/update/import` 与不带版本号的 `pgsql-<category>` 别名之所以默认落到
  `18`，仅仅因为当时 `19` 尚未进入活跃版本切片。
- `pig sty conf -v 19` 会自动向仓库模块列表注入 `beta` 并给出 Beta 提示。
- `cli/repo/assets/repo.yml` 仍将 PG 19 指向 `testing` 仓库，同时包含已 EOL 的 `pgdg14` 与
  `pgdg14-nonfree`；而上游 PGDG 仅在 RHEL 9 与 10 上发布了正式的 `yum/19` 仓库（PostgreSQL 19
  不再支持 RHEL 8 与 Debian 11）。
- `pig pg tune` 对所有 `pgVersion >= 18` 输出 `io_workers`，但 PostgreSQL 19 已移除静态的
  `io_workers`，改用动态的 `io_min_workers` 与 `io_max_workers`。

如果只把 `19` 放进活跃列表而不解耦默认版本、不裁剪 `el8` 构建包与 `io_workers`，就会让省略版本的安装
静默切换到 PostgreSQL 19，导致 EL 8 上的 `pig build tool` 请求不存在的 RPM 包，并为 PostgreSQL 19
输出已废弃的参数。

## 考虑过的方案 {#alternatives}

- **立即将默认主版本切换为 PostgreSQL 19。** 否决，因为在 PostgreSQL 19 发布初期，大量第三方扩展配方与
  Pigsty 生产配置模板仍以 PostgreSQL 18 作为默认基线。
- **在活跃窗口与 `pgdg` 模块中继续保留 PostgreSQL 14。** 否决，因为 PostgreSQL 14 在上游已正式 EOL；
  继续保留在新主机的默认仓库与构建依赖中会带来无谓的元数据同步和开发包安装开销。
- **彻底移除别名生成与 `-v` 解析中的 `10–14` 支持。** 否决，因为仍在运维存量 PostgreSQL 14（或更早版本）
  主机的用户在主机已配置兼容软件源或本地已有实例时，仍需要 `pig ext`、`pig pg`、`pg14*` 别名和核心包卸载保护。
- **直接删除 `beta` 仓库模块与 `--beta` 命令行标志。** 否决，因为在无活跃 Beta 的空窗期内，已有脚本调用
  `pig build repo --beta` 或 `pig repo set ... beta` 应当平滑退化为空操作，而不是报未知模块错误。

## 契约 {#contract}

- **版本分层与平台边界（`cli/ext`）：**
  - `PostgresActiveMajorVersions` 为 `[19, 18, 17, 16, 15]`。
  - `PostgresDefaultMajorVersion` 为 `18`；`PostgresBetaMajorVersion` 为 `0`（当前无活跃 Beta）。
  - `PostgresLegacyMajorVersions` 为 `[14, 13, 12, 11, 10]`。
  - 通过 `SupportsOSPG(osCode, ver)` 统一封装 OS × PostgreSQL 兼容边界（`el8` 与 `d11` 上限为 PG 18，
    `el7` 上限为 PG 15），在 `cli/ext`、`cli/build` 与 `cli/sty` 间共享。
- **隐式默认值与显式目标：**
  - 未探测到活跃 `pg_config` 且未传入 `-v` 时，`pig install`、`pig ext add/rm/update/import`、
    不带版本号的 `pgsql-<category>` 别名及 `pig pg tune` 统一回退到 `18`。
  - 本地 `DetectPostgres()` 实例发现仍按最高已安装版本兜底（例如多版本并存且均不在 `PATH` 中时优先识别已安装的
    PostgreSQL 19），同时继续扫描 `10–14` 安装路径。
  - 带版本号的静态别名（`pg10*`–`pg19*`）、动态分类别名（`pg10-<cate>`–`pg19-<cate>`）与受保护包卸载检查覆盖全部已知大版本（`10–19`）。
- **扩展目录与可用性矩阵（`cli/ext`）：**
  - 内嵌 `extension.csv` 刷新为 `2026-11-23` 的 627 条目录快照，纳入 PostgreSQL 19 新增 contrib 模块
    `pg_plan_advice`（无 control 文件的共享库模块，`need_ddl=false`）与 `pg_stash_advice`（`need_ddl=true`），
    并刷新 PostgreSQL 15–19 原生可用性矩阵（`31,979` 可用、`1,034` 缺失、`3,547` 不适用单元）。
  - `pig ext avail` 的文本与结构化输出严格限定在活跃的 `15–19` 窗口（8 个发行版版本 × 2 种架构 × 5 个活跃大版本 = `80` 个单元）。单扩展矩阵将 `PkgNA`（`N`）渲染为弱化的 `n/a`（区别于留空的 `M` 缺包单元），全局 `pig ext avail` 仅展示当前 OS 支持的活跃大版本列（`el8` 为 `15–18`，EL 9/10 与 Debian/Ubuntu 为 `15–19`）。
  - 活跃版本（`15–19`）严格按目标平台与架构的原生矩阵单元判定（`el8` 无 PG 19 软件包，绝不借用 PG 18 矩阵）；
    已退役版本（`10–14`）继续支持显式包名安装、静态别名（`pg14*`）与受保护包卸载检查，动态分类别名在目录保留 `rpm_pg`/`deb_pg` 声明时按非 fork 条目回退解析（刷新后的 PG 15–19 目录不再声明 PG 14）。
- **软件仓库（`cli/repo`）：**
  - 新增面向 EL 9 与 EL 10（`x86_64`、`aarch64`）的 `pgdg19`（含 `default`、`china`、`europe` 镜像）；
    模块成员按当前 OS/架构过滤，使 EL 9/10 的 `pgdg` 包含 `pgdg-common` 与 `pgdg19`–`pgdg15`，EL 8 的
    `pgdg` 省略 `pgdg19`，EL 7 的 `pgdg` 仅包含 `pgdg-common` 与 `pgdg15`。
  - 移除 `pgdg14`、`pgdg14-nonfree`、`pgdg19-beta` 与 `pgdg-beta`；统一为 `pgdg15-nonfree` 至
    `pgdg18-nonfree` 配置 `skip_if_unavailable=1`。
  - 保留 `beta` 为空兼容模块（`[]`），添加时不生成空的仓库配置文件、不记录虚假文件路径、`pig repo info beta`
    返回干净的空结果，且不影响替换失败后的回滚；若整套替换（`pig repo set`）仅指定了空模块，则在备份移除既有仓库前直接拒绝。
- **构建与 Pigsty 配置（`cli/build`、`cli/sty`、`cmd`）：**
  - `pig build tool` 在 EL 9/10 上安装 `15–19` 的 server/devel 包，在 EL 8 上安装 `15–18`（并为 EL 8/9/10
    统一提供 `openssl-devel`），未来 Beta 包同样受 `SupportsOSPG` 约束。
  - `pig build pgrx` 默认版本升级至 `cargo-pgrx 0.20.1`，按 `CARGO_HOME`、`~/.cargo/bin/cargo` 与 `PATH`
    查找 Cargo，校验 OS 兼容的 `--pg` 版本，并在 Linux 缺少对应 `pg_config` 或未探测到任何受支持 PG 时快速失败。
  - `pig build dep`、`pig build ext` 与 `pig build pkg` 按 OS 兼容边界校验 `--pg`，在 EL 上按 OS 自动选择兼容的
    `rpm_pg` 默认版本（例如在 `el8` 上选 PG 18），当扩展无任何受支持的目标版本时直接失败而非空跑通过，在 Debian/Ubuntu
    显式传入 `--pg` 时向 `make` 传递 `PG_VERSIONS` / `PG_SUPPORTED_VERSIONS`（单版本附加 `PG_MAJOR` / `PG_CONFIG`），
    并将 `libpgfeutils` 源码映射更新至 PG 15–19（`15.20`–`19.0`）。
  - `PostgresBetaMajorVersion == 0` 期间，`pig build repo --beta`、`pig build tool --beta` 与
    `pig build pgrx --beta` 均保持为安全的兼容空操作。
  - `pig sty conf` 的 `-v` 接受 `15–19`，帮助文本不再显示失活的 `(beta: ...)` 后缀，显式选择 `19` 时直接改写通用模板而不再注入 `beta` 模块，并在 Linux `el8` 主机上选择 PG 19 时给出非致命告警。
- **参数调优（`cli/postgres`）：**
  - `pig pg tune` 仅在 `pgVersion == 18` 时输出 `io_workers`，PostgreSQL 19+ 不再输出该参数。

## 影响 {#impact}

EL 9/10、Debian 12/13 与 Ubuntu 22.04/24.04/26.04 环境无需任何 Beta 标志即可直接使用 PostgreSQL 19
的软件源、扩展包、构建工具链与 Pigsty 配置生成，同时未显式指定版本的默认安装与配置模板继续稳妥地锚定在
PostgreSQL 18。EL 8 主机继续正常构建与安装 PostgreSQL 15–18，不会因请求不存在的 `postgresql19-*` RPM
而失败。存量 PostgreSQL 14 主机在保留自身软件源时仍可通过显式命令与别名运维，而新初始化主机不再拉取已 EOL
的 PostgreSQL 14 仓库定义。

由于用户本地缓存的 `~/.pig/extension.csv` 与 `~/.pig/repo.yml` 优先级高于二进制内嵌资产，正式发版时需同步更新远程目录文件，确保执行 `pig repo reload` 或 `pig ext reload` 的存量用户获取最新目录。

## 验证与演进 {#verification}

实现位于 PIG 提交
[`b36d683`](https://github.com/pgsty/pig/commit/b36d683585c3)、
[`461339c`](https://github.com/pgsty/pig/commit/461339ceb7a6)、
[`a7061b1`](https://github.com/pgsty/pig/commit/a7061b14ef0e)、
[`52847f4`](https://github.com/pgsty/pig/commit/52847f47155b) 与
[`ba77eac`](https://github.com/pgsty/pig/commit/ba77eacc1f3e)，已在本地完成以下验证：

- `git diff --check` 与 `go vet ./...`
- `go test -shuffle=on -count=1 ./...`（全部 26 个包通过）
- `go test -race -shuffle=on -count=1 ./cli/ext ./cli/repo ./cli/build ./cli/sty ./cli/postgres`
  以及 CI 同款 `./cmd` 竞态回归（两组 CI shuffle 种子各跑 3 轮）
- `staticcheck ./...`、`golangci-lint run --enable-only gocognit,gocyclo --tests=false` 与 `deadcode ./...`
- 配套设计记录与 Markdown 校验（`bin/check_design.py`、`bin/check_markdown.py`）

后续当 PostgreSQL 20 进入 Beta 周期时，只需将 `PostgresBetaMajorVersion` 设为 `20` 并在 `repo.yml`
中填入对应 Beta 仓库定义；`cli/build` 与 `cli/sty` 的 Beta 分支已通过模拟 Beta 大版本的单元测试持续覆盖。

## 当前状态 {#status}

已在源码提交 [`b36d683`](https://github.com/pgsty/pig/commit/b36d683585c3)–[`ba77eac`](https://github.com/pgsty/pig/commit/ba77eacc1f3e)
与配套双语文档中实现；尚未推送、打标签或部署至远程目录端点。正式二进制发布进度以
[发布注记](/zh/release/) 为准。
