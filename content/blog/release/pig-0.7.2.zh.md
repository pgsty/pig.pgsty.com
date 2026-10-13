---
title: "pig v0.7.2"
linkTitle: "v0.7.2"
date: 2025-11-20
description: "437 个扩展，修复 pig build 的一些问题"
tags: [build, catalog]
weight: 201
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v0.7.2
---

- 批量更新扩展，数量达到 437 个
- 新增 PGDG EL10 Sysupdate 仓库
- 新增 LLVM APT 仓库
- 在 pig build 命令中使用可选的本地 extension.csv 扩展定义问题。

- 更新的扩展： vchord pg_later pgvectorscale pglite_fusion pgx_ulid pg_search citus timescaledb pg_profile pg_stat_monitor documentdb
- 新增的扩展：pglinter pg_typeid pg_enigma pg_retry pg_biscuit pg_weighted_statistics

## 校验和

```checksums
080dd93c33faf81e8f9d3b9d543b9949604b834ccd55331cce697df79049a9af  pig-0.7.2-1.aarch64.rpm
b91056230d3a790ab0190b3680fc5dbc3eb1306b7a1c2416fb6ef421bf48dcf7  pig-0.7.2-1.x86_64.rpm
9b294e58b8c3629066b905e25dda4f51eacc1eb4b6d5d87fab32d17fb13a9cb7  pig-v0.7.2.darwin-amd64.tar.gz
74f3276752d826c8130ca22a791da48548608378a453908e7cdd095c0564a1eb  pig-v0.7.2.darwin-arm64.tar.gz
0c9f6e6bf930e70206df2c6d58d1296f1a7a77ca7d89d27d47112bc44544cda4  pig-v0.7.2.linux-amd64.tar.gz
f62842217be958569ca09051e8cad0d674ee9446245e45655b91f9918927b340  pig-v0.7.2.linux-arm64.tar.gz
091d12d5d5c3c8e52b8b60ab180b88b7aeaff512aa344af0e039c7d4b73c75a0  pig_0.7.2-1_amd64.deb
53346bd96538a20b0bb3bb4161ba117bca7b5cf6633f5d3c357fe9e560b06ff5  pig_0.7.2-1_arm64.deb
```

{{< release-card >}}
