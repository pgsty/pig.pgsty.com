---
title: "pig v1.10.1"
linkTitle: "v1.10.1"
date: 2026-10-24T00:00:00+08:00
description: "升级 Go 1.27.3 修复安全问题，更新工具依赖，扩展目录增至 615 个条目。"
tags: [build, catalog, cli]
weight: -1
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.10.1
---

PIG `v1.10.1` 是一次安全与扩展目录维护版本：升级 Go 至 `1.27.3`，
更新工具依赖，并将内嵌 PostgreSQL 扩展目录从 **603 个条目增至 615 个**。

## 安全更新

- Go 工具链从 `1.27.2` 升级到 `1.27.3`。CI 与发布构建使用 `go.mod` 指定的版本。
- 纳入 `crypto/x509` 的
  [CVE-2026-111943 / GO-2026-6809](https://pkg.go.dev/vuln/GO-2026-6809) 修复。
  Go 证书验证器会拒绝包含特定不再受信任的中间证书的证书链。

根据 [Go 官方发布公告](https://groups.google.com/g/golang-announce/c/66pojueaQek)，
Go `1.27.3` 相比 `1.27.2` 新增 **1 项安全修复**。
更早的 Go 安全修复已包含在 PIG `v1.10.0` 使用的 `1.27.2` 基线中。

## 依赖更新

通过限定原版本的模块替换，更新间接工具依赖：

| 模块 | 原版本 | 新版本 |
|:-----|:-------|:-------|
| `github.com/cpuguy83/go-md2man/v2` | `v2.0.6` | `v2.0.7` |
| `github.com/stretchr/objx` | `v0.1.0` | `v0.8.0` |
| `golang.org/x/mod` | `v0.41.0` | `v0.42.0` |
| `golang.org/x/tools` | `v0.51.0` | `v0.52.0` |

## 扩展目录

内嵌目录现包含 **615 个条目**，相比 `v1.10.0` **新增 12 个**：

- `codesystem`、`encsearch`、`hdr_histogram`、`pg_improv`
- `pg_kv`、`pg_lease`、`pg_synonym`、`pg_table_range`
- `pg_tre`、`pg_try_cast`、`stannum`、`tin`

本次刷新还更新了已有扩展的版本与软件包可用性元数据。
总数沿用 [目录条目计数口径](/zh/ext/#catalog-count)，包含已打包的 SQL 工具和已移除扩展的保留记录。
615 不表示所有条目都支持 `CREATE EXTENSION`，也不表示它们在每个平台上都可安装。

## 兼容性

命令、参数与配置保持和 `v1.10.0` 兼容。
内置 Pigsty 保持 `4.5.0`，默认 `cargo-pgrx` 保持 `0.19.3`。

从源码构建需要 Go `1.27.3` 或更高版本。使用预编译软件包无需在本机安装 Go。
请按 [安装文档](/zh/install/) 升级 PIG 可执行文件，以使用更新后的 Go 标准库；
仅升级主机上的 Go 不会更新已经安装的 PIG 二进制。

## 校验和

```checksums
fbd58de4cd1fa767c6d2b15d4fcb029fe38c90a0d12db2e387b7f698b5c8a69d  pig-1.10.1-1.aarch64.rpm
7955e93744fcc2d4cce9044102c2bd7ca470388a0556d3220a624f78e38c629b  pig-1.10.1-1.x86_64.rpm
31fea0e9513e551e2be8dc99a8fc0f77de4bdfe40e66dadc206e227254bb7942  pig-v1.10.1.darwin-amd64.tar.gz
1177f3b616279100ce97d23eb4fa6bc2e8daf02dbd23780a8dd5025240082c5a  pig-v1.10.1.darwin-arm64.tar.gz
0e837098d45b080ddf9205681709dbc38318d2b65cbdaed711246fd5834c3b50  pig-v1.10.1.linux-amd64.tar.gz
6658242816263ea4f5e3abeb3454665098c7100c75c76a3e45386a15faf6f397  pig-v1.10.1.linux-arm64.tar.gz
37f5dca9407010c56d8c5747c8ddcef101d7f07602296e0bb89620c633692eab  pig_1.10.1-1_amd64.deb
f385d1c6fac40a6cf648505d349a72e7e3eadf2948024f086efe81733c2a9be5  pig_1.10.1-1_arm64.deb
```

{{< release-card >}}
