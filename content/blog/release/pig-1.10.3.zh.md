---
title: "pig v1.10.3"
linkTitle: "v1.10.3"
date: 2026-10-29T00:00:00+08:00
description: "新增四个扩展，刷新目录元数据，扩展条目增至 620 个。"
tags: [ext, catalog]
weight: -3
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.10.3
---

PIG `v1.10.3` 更新内嵌 PostgreSQL 扩展目录，从 **616 个条目增至 620 个**，
新增四个扩展，并刷新软件包、版本、兼容性与可用性元数据。

### 新增扩展

| 扩展 | 版本 | PostgreSQL 支持 | 说明 |
|:-----|:-----|:----------------|:-----|
| `oai_fdw` | `1.16` | 14–18 | 通过 HTTP/HTTPS 采集 OAI-PMH 元数据的只读外部数据包装器 |
| `pg_agent_gate` | `0.3.0` | 18 | 面向 Agent 角色的 SQL 提议、校验、受控执行与人工审批门 |
| `pg_integrity_checksums` | `2.0.0` | 14–18 | 为 PostgreSQL 页面、行、表、索引和数据库提供物理与逻辑校验和 |
| `pg_stat_tcpinfo` | `1.1` | 14–18 | Linux TCP 连接统计、延迟与重传观测 |

这些记录描述的是目录与软件包可用性；实际可安装性仍取决于目标 PostgreSQL
大版本、操作系统、架构和软件仓库快照。

### 版本与元数据更新

本次更新现有扩展的软件包与版本信息，包括 `pg_nanotime` `0.2.0` → `0.3.0`、
`supautils` `3.4.4` → `4.0.0`、`pg_ducklake` `1.0.2` → `1.0.3`、
`pg_improv` `0.10.0` → `0.12.1`、`wrappers` `0.6.3` → `0.6.4`、
`edtf_postgres` `1.2.3` → `1.3.2`、`hypopg` `1.4.3` → `1.4.4`、
`rdf_fdw` `3.0` → `3.1`。同时刷新维护目录中的包矩阵、兼容范围、描述和源信息。

### 扩展目录口径

目录现在包含 **620 个条目**：617 条可用记录和 3 条保留的已移除记录。
[目录计数口径](/zh/ext/#catalog-count) 包含 SQL 工具与生命周期保留记录，
具体可用性仍取决于平台。

Go 保持 `1.27.3`，内嵌 Pigsty 保持 `4.5.0`，默认 `cargo-pgrx` 保持 `0.19.3`。
升级 PIG 请参阅 [安装文档](/zh/install/)。

## 校验和

```checksums
2068ca8150df3ee837d0ba6e533ba651703c7223c14c522703ee1be9c41666ea  pig-1.10.3-1.aarch64.rpm
97ff1c1799262650a92d669dafc905d498d5ab3cf58619198322bc2d274b4ceb  pig-1.10.3-1.x86_64.rpm
16203993bbba93dee16a38eac3eedbf67ed2cce3c7894cedbba613e95578004c  pig-v1.10.3.darwin-amd64.tar.gz
0eb3f0447107734ae7decf3bc16caf99087e86119e83ce34987ebb376285fb14  pig-v1.10.3.darwin-arm64.tar.gz
a3e61d0d71b9226ac89aa3b1e29baa8c92e5109ecaa2c7e26343f474e5832e04  pig-v1.10.3.linux-amd64.tar.gz
5f25ff6cf634f708d5f70bde39a07d83fe9c7d1ef7d944395eb294eb64554ecf  pig-v1.10.3.linux-arm64.tar.gz
dfabbcf4fcdf612d79a7cce76db08d36683e00bd2b0f27c7e78258f54fcb721a  pig_1.10.3-1_amd64.deb
4065ed14209a4857b26fa1c7e19adbeee2e5be68df41710db33b64b18159045f  pig_1.10.3-1_arm64.deb
```

{{< release-card >}}
