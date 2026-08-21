---
title: "pig v1.7.0"
linkTitle: "v1.7.0"
date: 2026-08-12
description: "更安全的 EL 模块处理、更新的中国镜像、精简的 EL7 兼容目录，以及 575 个已打包扩展。"
tags: [repo, catalog, ext]
weight: 2
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.7.0
---

Pig `v1.7.0` 是 [v1.6.2](/zh/release/pig-1.6.2/) 之上的仓库兼容性与目录更新版本：明确中国镜像选择语义，默认保留 DNF 原生模块过滤，恢复精简的 EL7 仓库目录，并将内置扩展快照从 572 个增加到 575 个。内置 Pigsty 版本仍为 `4.5.0`。

## 主要变化

- `-m|--mirror` 现在直接选择内置的 `china` 仓库定义。PGDG、Rocky Linux、Debian、Ubuntu、Docker 等区域路由使用维护中的镜像列表，不再进行旧版运行时 PGDG 代理改写。
- EL 仓库不再全局注入 `module_hotfixes=1`。确实需要覆盖模块流的 Pigsty 与 PGDG 仓库会显式启用；BaseOS、AppStream、EPEL 等普通仓库继续使用 DNF 原生模块过滤。
- EL7 保留有意精简的兼容目录：面向 `x86_64` 的 CentOS 7 Base/Updates/Extras/SCLo 与 EPEL 归档源，以及共享的 Pigsty 和仍受支持的 PGDG 条目。渲染 EL7 YUM 配置时会移除仅适用于 DNF 的 `module_hotfixes`。
- 当目录中没有匹配当前平台的仓库定义时，仓库设置会明确报告平台不受支持，而不是继续处理空仓库集合。
- 发布元数据升级到 `1.7.0`，内置 Pigsty 版本保持 `4.5.0`。

## 扩展目录

- 已打包扩展数量从 **572** 增加到 **575**，没有移除项。
- 新增 3 个扩展：`pg_local_cache 1.2.0`、`pg_statviz 0.1.0`、`pg_policy 0.1.0`。
- 版本更新包括 `biscuit 3.0.0`、`pg_clickhouse 0.10.0`、`pg_search 0.25.2`、`pg_turbovec` 软件包 `1.29.0`、`pg_uuid_v8 1.1.0`，以及 Debian `q3c 2.0.5` 软件包。
- 刷新软件包元数据与可用性矩阵；需要比本版本内置快照更新的目录时，请运行 `pig ext reload`。

## 兼容性提醒

- 本版本没有移除命令或全局参数。
- `-m|--mirror` 现在明确选择中国区域，不再进行 PGDG 代理改写。需要固定路由时请使用 `--region=default|china|europe`。
- 自定义 EL 仓库如果确实需要覆盖模块流，现在必须显式设置 `meta.module_hotfixes: 1`；普通操作系统仓库会有意省略该设置，EL7 上则会移除它。
- EL7 已停止维护，仅提供有限兼容性；当前 PostgreSQL 与扩展软件包应优先使用 EL8 或更高版本。

## 校验和

制品：[GitHub Release](https://github.com/pgsty/pig/releases/tag/v1.7.0) · [checksums.txt](https://github.com/pgsty/pig/releases/download/v1.7.0/checksums.txt)

```checksums
e3a339fefdd2203825d15438b52f18e729547eb88dae014212a46006a9bd47d1  pig-1.7.0-1.aarch64.rpm
34ce29d75ef9f669f3bf832cc812ae082abda7320ee2b2336ea61e701b9b67f8  pig-1.7.0-1.x86_64.rpm
d26803c685ba29c01cb8e6dfe50c6c1b0f004173be82015618fa8cdf6a329ba7  pig-v1.7.0.darwin-amd64.tar.gz
ea8120d48b93da936919f590ebbefeb72e73277e6bc133c1ef0bb1abc055d3ce  pig-v1.7.0.darwin-arm64.tar.gz
40295b64a2423094fa6f4e6d31da8d8ad5b26698c397d8916c0289591522d0bf  pig-v1.7.0.linux-amd64.tar.gz
7929091732957d85751ef3381285a1e5b0c3c7f82c0e00fc24ed085c496012d5  pig-v1.7.0.linux-arm64.tar.gz
41523c15f36a6c1acaf4af5c851d2626472fc15c21d25f91fc1e991fe8411072  pig_1.7.0-1_amd64.deb
adf7b2d9ce8fe42bad935428d16a9c998337df986b1065e0761dc167ce837ef5  pig_1.7.0-1_arm64.deb
```

{{< release-card >}}
