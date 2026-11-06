---
title: "分类别名按目标 PostgreSQL 大版本解析"
linkTitle: "分类别名目标版本"
date: 2026-11-06
lastmod: 2026-11-06
description: "动态分类别名选择扩展软件包时，使用请求的 PostgreSQL 大版本。"
tags: [catalog, ext, install]
weight: 97
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-11-06<br>
> **状态：** 已在源码提交 [`7c069dc`](https://github.com/pgsty/pig/commit/7c069dcdc47a9fb51acd56a06dd2a4132723e6dd) 中实现，尚未发布。<br>
> **当前参考：** [`pig ext` 分类别名](/zh/ext/#category-aliases)<br>
> **范围：** 解析扩展软件包组的动态 `pgN-*` 与 `pgsql-*` 分类别名。

## 决策 {#decision}

稳定版本的分类别名使用请求的 PostgreSQL 大版本判断软件包可见性。`pgN-<category>` 从别名中取得大版本，
`pgsql-<category> -v N` 使用同一个目标大版本。完成可见性判断后，软件包模板也按请求的大版本渲染。

目录仍是软件包名称与平台可用性的事实来源。这样，目录刷新后可以直接描述软件包拆分和按版本变化的支持情况，
无需在别名解析器中加入扩展专用分支。当前目录将 EL PG14/15 的 pgaudit 描述为 `pgaudit_14`/`pgaudit_15`，
将 PostGIS 3.7 描述为 `postgis37_N`，并将地址标准化器和 PG16 以上的 Tiger Geocoder 描述为独立条目。

当前 Beta PostgreSQL 占位版本继续使用兼容策略：借用最新稳定版矩阵，并只保留 PGDG 来源的条目，因为目录还没有
该目标自己的矩阵行。

## 背景 {#context}

在本次修改之前，`pgsql-*` 分类别名会使用最新稳定版目录行判断稳定目标。于是 `pgsql-gis -v 14` 可能带入只在
PG18 矩阵中存在的软件包，例如 Tiger Geocoder。编号形式 `pg14-gis` 已经使用请求的大版本，因此两种别名会得到
不同的软件包组。

同一个解析器还包含 EL 上 PG14 和 PG15 的 pgaudit 硬编码改名。这一规则对应历史软件包名称，而当前 pgaudit 配方和
目录已经使用 `pgaudit_$v`。当软件包元数据修正后，继续把这个规则留在代码中就会使别名结果过时。

## 考虑过的方案 {#alternatives}

- **所有 `pgsql-*` 别名都继续使用最新稳定版模板。** 否决，因为显式 `-v N` 必须遵守请求的 PostgreSQL 大版本支持矩阵。
- **继续添加扩展专用的软件包特例。** 否决，因为 pgaudit 和 PostGIS 的软件包名称与支持行都是目录数据，通用解析器可以直接渲染。
- **只使用 RPM/DEB 版本元数据。** 否决，因为软件包矩阵还记录操作系统、架构、来源仓库、隐藏状态和不可用单元格。
- **删除 Beta 借用机制。** 否决，因为当前 Beta 目标没有自己的目录行，仍需要稳定版模板以及原有的 PGDG-only 限制。

## 契约 {#contract}

- 稳定版本的 `pgN-<category>` 别名按 PostgreSQL 大版本 N 判断可见性。
- 稳定版本的 `pgsql-<category>` 别名按命令传入的目标版本判断；显式 `-v N` 时，它与 `pgN-<category>` 的结果相同。
- 如果没有目标版本传入解析器，继续沿用现有命令探测与操作默认值；分类别名解析器收到零值时使用最新稳定大版本。
- 软件包模板按请求的目标大版本渲染。可见的主导非 contrib 条目按渲染后的软件包名称去重。
- 已知操作系统缺少矩阵单元时，仍视为不可用。现有未知操作系统的软件包元数据回退行为不变。
- Beta 目标借用最新稳定版矩阵，并只保留 PGDG 来源条目。这是唯一借用稳定模板的例外。
- 已配置的操作系统软件源必须提供目录命名的软件包；解析器不会把已安装的软件包从历史名称迁移到新名称。

## 影响 {#impact}

`pig ext add pgsql-gis -v 14 --plan` 与 `pig ext add pg14-gis --plan` 现在选择相同的 PG14 矩阵。PG14/15 不再继承
PG18 独有的 Tiger Geocoder 条目。修正后的 pgaudit 目录行会让 EL 上的 PG14/15 解析为 `pgaudit_14` 和 `pgaudit_15`；
PostGIS 3.7 目录行会在矩阵允许时解析为 `postgis37_N`，并分别解析地址标准化器和 PG16 以上的 Tiger Geocoder 软件包。

这样更容易通过刷新目录更新行为，因为软件包专用名称已经回到目录中。用户仍需配置包含所选软件包的软件源，尤其是
EL 上 PG14/15 pgaudit 的 Pigsty 来源条目。

## 验证与演进 {#verification}

源码提交 [`7c069dc`](https://github.com/pgsty/pig/commit/7c069dcdc47a9fb51acd56a06dd2a4132723e6dd) 在
`cli/ext/category_alias_test.go` 中增加了目标版本、编号别名、默认版本、Beta 与未来大版本路径的回归测试。
`cli/ext/catalog_embedded_test.go` 覆盖 EL8/9/10 与两种架构上的 pgaudit，以及 EL 和 Ubuntu 上 PG14-18 的 PostGIS、
地址标准化器与 Tiger Geocoder 软件包解析。目录变更位于 `cli/ext/assets/extension.csv`。

已提交源码通过 `git diff --check`、`go test -shuffle=on -count=1 ./...`、`go vet ./...`、
`go test -race -shuffle=on -count=1 ./cli/ext ./cli/install`、`staticcheck ./...`、配置的复杂度检查和
`deadcode ./...`。本记录描述已实现的源码契约；未来发布标签仍需单独作为发布证据。

## 当前状态 {#status}

目标版本行为已在上述源码提交中实现，并写入 [`pig ext` 参考文档](/zh/ext/#category-aliases)。发布注记和部署状态
与本实现记录分开维护。
