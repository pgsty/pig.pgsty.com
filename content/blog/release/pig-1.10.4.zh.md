---
title: "pig v1.10.4"
linkTitle: "v1.10.4"
date: 2026-11-06T00:00:00+08:00
description: "新增七个目录条目，刷新包元数据，修复目标版本别名解析，目录增至 626 个条目。"
tags: [ext, catalog, install]
weight: -4
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.10.4
---

PIG `v1.10.4` 将内嵌 PostgreSQL 扩展目录从 **620 个条目更新到 626 个**，并修复分类别名未按指定 PostgreSQL 大版本选择软件包的问题。2026 年 11 月 6 日的目录快照新增七个条目，移除已退役的 `pgcontext_pgvector` 记录，净增六个。

## 新增目录条目

| 扩展 | 版本 | PostgreSQL 支持 | 说明 |
|:-----|:-----|:----------------|:-----|
| `pg_warren` | `0.8.0` | 15–18 | 基于 PostgreSQL 表的版本化图遍历与图计算 |
| `pg_statecharts` | `0.1.0` | 16–18 | 层次状态机与事务性事件处理 |
| `pg_statecharts_dev` | `0.1.0` | 16–18 | pg_statecharts 的 SCXML 导入与迁移开发工具 |
| `pg_lion` | `0.3.0` | 16–18 | 用于过滤、计数与聚合的 Roaring 位图倒排索引 |
| `pg_lion_citext` | `0.3.0` | 16–18 | 为 lion 索引提供大小写不敏感的 citext 运算符类 |
| `pg_lion_vector` | `0.3.0` | 16–18 | 为 pgvector 的 vector 与 halfvec 提供带过滤的近邻索引 |
| `opencc` | `0.1.0` | 14–18 | 基于 OpenCC 的简繁中文、地区用语与日文新字体转换 |

实际可安装性取决于目标 PostgreSQL 大版本、操作系统、架构与已配置的软件源。

## 版本与包元数据更新

部分目录版本变化如下：

| 扩展 | 版本变化 |
|:-----|:---------|
| `postgis` | `3.6.4` → `3.7.0` |
| `timescaledb_toolkit` | `1.26.0` → `1.27.0` |
| `vchord` | `1.1.1` → `1.2.0` |
| `vchord_bm25` | `0.3.0` → `1.0.0` |
| `pg_tokenizer` | `0.1.1` → `1.0.0` |
| `pg_search` | `0.26.3` → `0.26.5` |
| `pg_duckdb` | `1.1.1` → `1.2.0` |
| `pg_lake` | `3.5` → `3.6` |
| `anon` | `3.2.3` → `3.3.2` |
| `pg_integrity_checksums` | `2.0.0` → `2.1.0` |

本次还刷新了软件包可用性、依赖、描述与源信息。PostGIS 3.7 使用 `postgis37_N` RPM 包系列，地址标准化器与 Tiger Geocoder 使用独立软件包。EL 上 PostgreSQL 14、15 的 pgaudit 包名分别为 `pgaudit_14`、`pgaudit_15`。

## 分类别名遵循目标版本

对于稳定版 PostgreSQL，`pgsql-<category> -v N` 现在与 `pgN-<category>` 使用相同的平台及 PostgreSQL 大版本矩阵。例如，`pig ext add pgsql-gis -v 14 --plan` 不再混入仅适用于较新 PostgreSQL 大版本的软件包。软件包名称统一从目录取得，解析器中旧的 pgaudit 特殊改名规则已移除。Beta 目标仍沿用借用最新稳定版矩阵、仅保留 PGDG 来源的回退策略。

## 目录口径与构建版本

内嵌目录包含 **626 条记录**，其中 **624 条可用**、**2 条为保留的已移除记录**。包含 PostgreSQL contrib 模块时，共对应 **518 个不同包名**；非 contrib 包系列共 **457 个**。详见 [目录条目计数口径](/zh/ext/#catalog-count)。

Go 保持 `1.27.3`，内嵌 Pigsty 保持 `4.5.0`，默认 `cargo-pgrx` 保持 `0.19.3`。升级 PIG 请参阅 [安装文档](/zh/install/)。

## 校验和

```checksums
4981a060779423ab4d6c5baaa8fe6c26adb972fc34b9515119b9e5d4723513ce  pig-1.10.4-1.aarch64.rpm
d1624bbcec5d3f4715d223acca8311182ef1ee36542c16bcf82602674ee82b07  pig-1.10.4-1.x86_64.rpm
9384759851af53f5cddc381007f78de9a226b43b914848291df86ec41096119e  pig-v1.10.4.darwin-amd64.tar.gz
d0f876a518b82f021c83914c5909f1ac914cbe8c0aa0957cef37c83d69b79b0d  pig-v1.10.4.darwin-arm64.tar.gz
1caa6f4af13e1f40f5faa9752628efe1dd85190b344bf1597cb3c8d23e99fe0b  pig-v1.10.4.linux-amd64.tar.gz
756b7c94936a4c8cca1b0a15f3bcac8eee9669480b8d6af205e920b673a680ba  pig-v1.10.4.linux-arm64.tar.gz
98bbfce9dc263e94d4025debdd9bf0e137d9ec12afff4d57e4e08530b1255bf3  pig_1.10.4-1_amd64.deb
18447ccff10fd31c90ae16b34f2885a0415bc6efca5d0ff78f435e68ba6438e1  pig_1.10.4-1_arm64.deb
```

{{< release-card >}}
