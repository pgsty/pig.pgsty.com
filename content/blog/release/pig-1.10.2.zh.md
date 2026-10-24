---
title: "pig v1.10.2"
linkTitle: "v1.10.2"
date: 2026-10-24T00:00:00+08:00
description: "新增 pg_nanotime，更新扩展版本与软件包信息，目录增至 616 个条目。"
tags: [ext, catalog]
weight: -2
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.10.2
---

PIG `v1.10.2` 更新内嵌 PostgreSQL 扩展目录，从 **615 个条目增至 616 个**，
新增 `pg_nanotime`，并刷新扩展版本、兼容性与软件包可用性信息。

## 新增扩展

收录 [`pg_nanotime`](https://github.com/bunko666-cloud/pg_nanotime) `0.2.0`，
提供纳秒时间戳与固定时长间隔类型。目录包含 PostgreSQL **17、18** 的 RPM 与 DEB
软件包信息；上游将 `0.2.0` 标记为测试版本。

## 版本更新

| 扩展 | 原版本 | 新版本 |
|:-----|:-------|:-------|
| `citus`、`citus_columnar` | `14.2.0` | `14.3.0` 软件包 |
| `duckdb_fdw` | `2.0.1` | `2.0.2` |
| `pg_mentat` | `1.17.2` | `1.18.0` |
| `pg_tre` | `4.5.1` | `4.5.2` |

Citus 的目录扩展版本为 `14.3-1`，对应 RPM / DEB 软件包版本为 `14.3.0`。
本次还补充了 `pg_tre` 在 PostgreSQL 17、18 上的 DEB 包可用性信息。

## 目录信息

- 刷新 PostgreSQL 兼容范围、包可用性、许可证与扩展描述。
- 将 `duckdb_fdw` 的目录兼容范围调整为 PostgreSQL 15–18，
  `pgcontext_pgvector` 调整为 PostgreSQL 17。
- 扩展数量统一按 **616 个目录条目** 计：613 条可用记录与 3 条保留的已移除记录。
  [目录计数口径](/zh/ext/#catalog-count) 包含 SQL 工具与生命周期保留记录，
  具体可用性仍取决于平台和 PostgreSQL 大版本。

Go 保持 `1.27.3`，内嵌 Pigsty 保持 `4.5.0`，默认 `cargo-pgrx` 保持 `0.19.3`。
升级 PIG 请参阅 [安装文档](/zh/install/)。

## 校验和

```checksums
f07992b20b0b397d1e4bb286656b404e3c911775e98e5fc7d940ef91439f62ed  pig-1.10.2-1.aarch64.rpm
372f4fe8d54a1ad888c91976d011d8b95de3e10286966cfc94b0ab91e2170b20  pig-1.10.2-1.x86_64.rpm
a54be0a4ceadf1e047b74fdb187ff57e9f97b81907c8d66795e7787de88ad864  pig-v1.10.2.darwin-amd64.tar.gz
60df049a38e109bccb3089d74fa41e0d22606ce4df0e4fadae39530d546ca731  pig-v1.10.2.darwin-arm64.tar.gz
686c5d6cf682a5a5a1d70cc09a86fecc441b22456f79bb84f192c4730ac2bd8a  pig-v1.10.2.linux-amd64.tar.gz
e1e84d5afcddc8e474d130de638bc400bb965f887bdc9face842f111fb94afeb  pig-v1.10.2.linux-arm64.tar.gz
38b9634be544a1ee462926f74f3c647c2fc1b21eeffb43e41c24a9033a03a63b  pig_1.10.2-1_amd64.deb
4034cebd3a51839ecb0cb8bdf325d783f1ebb88e19b4664ab21fbf31316eae58  pig_1.10.2-1_arm64.deb
```

{{< release-card >}}
