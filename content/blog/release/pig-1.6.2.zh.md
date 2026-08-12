---
title: "pig v1.6.2"
linkTitle: "v1.6.2"
date: 2026-08-11
author: "冯若航"
description: "572 个已打包扩展、Grafana 仪表盘 schema v2，以及 SOW 优先的本地软件仓库生成。"
categories: [release]
tags: [Release, pig]
weight: 5
---

Pig `v1.6.2` 是 [v1.6.1](/zh/release/pig-1.6.1/) 之上的功能与目录更新版本：已打包扩展从 562 个增加到 572 个，新增 Grafana 仪表盘 schema v2 原生支持，并改进本地软件仓库生成流程。内置 Pigsty 版本继续锁定为 `4.5.0`。

## 主要变化

- `pig sty grafana` 现在同时支持传统仪表盘 JSON 与原生 `dashboard.grafana.app/v2` Dashboard 资源。载入 v2 仪表盘时使用 Grafana resource API，确保标签页与 section 变量可以完整往返；导出到现有 v2 文件时保持 v2 格式，新文件默认仍使用传统格式。
- `pig repo create` 在 SOW 可用时优先执行 `sow create --pigsty --timeout 10m -- <dir>`，要求生成的 `repo_complete` 完成标记存在且为普通文件；Linux 上仍可回退到 `createrepo_c` / `dpkg-scanpackages`。
- macOS 现在可通过 SOW 创建本地软件仓库，默认使用当前目录且无需 `sudo`；Linux 默认目录仍为 `/www/pigsty`。
- 发布元数据升级到 `1.6.2`，内置 Pigsty 版本保持 `4.5.0`。

## 扩展目录

- 已打包扩展数量从 **562** 增加到 **572**，没有移除项。
- 新增 10 个扩展：`pg_turbovec`、`pg_disorder`、`pg_mentat`、`plruby`、`jsonb_plruby`、`hstore_plruby`、`ltree_plruby`、`pg_describe`、`cat_tools`、`pg_vault_tde`。
- 更新 12 个扩展版本：`timescaledb 2.29.1`、`q3c 2.0.5`、`pgmnemo 0.16.1`、`pg_search 0.25.1`、`citus 14.2.0`、`citus_columnar 14.2.0`、`provsql 1.12.0`、`plpgsql_check 2.10.4`、`pg_rational 0.0.3`、`pgbson 2.1.0`、`pg_readme 0.7.1`、`pg_readme_test_extension 0.7.1`。
- 刷新软件包元数据与可用性矩阵；运行 `pig ext reload` 可以用最新在线目录替换内置的发布快照。

## 兼容性提醒

- 本版本没有移除命令或全局参数。
- 安装 SOW 后，`pig repo create` 会优先使用 SOW 而非传统 Linux 生成器，并在报告成功前检查完成标记是否存在。
- 目录总数不代表每个包都适用于所有 PostgreSQL / 操作系统 / 架构组合；请在目标主机上使用 `pig ext avail NAME` 查看实际可用矩阵。
- 包管理器与安装脚本会使用配置的软件仓库中已经发布的最新版本，可能晚于 GitHub；需要精确获取本版本时请使用 GitHub 制品。

## 校验和

制品：[GitHub Release](https://github.com/pgsty/pig/releases/tag/v1.6.2) · [checksums.txt](https://github.com/pgsty/pig/releases/download/v1.6.2/checksums.txt)

```bash
6697a96bbf476e697a5c3da8b6c861719e4b7208e1e4fe927cf4b475ea1f162f  pig-1.6.2-1.aarch64.rpm
ad0b311867bc6cd689dd73e9a96b84f1fe0f49f6c0f1184abf9eb3232a07a184  pig-1.6.2-1.x86_64.rpm
bb167e04fceb6cebee5c8a2423279cefb4474f46301a5055c464ac98294dc9db  pig-v1.6.2.darwin-amd64.tar.gz
3de74e33321884a0c36596c1e7df9370be594a315395538e9ba5b775bbc1a79d  pig-v1.6.2.darwin-arm64.tar.gz
7b69214e115e6815e772b7e179aa4070bd8553e585b164ba3a0f69a1d53a0294  pig-v1.6.2.linux-amd64.tar.gz
b511e727642987867be5921d72e8019e9c6186b82e63ddc34ad653773abed5a8  pig-v1.6.2.linux-arm64.tar.gz
3d1a80b833c6179b84ac5cc590ad06695b187b2bb4a09f544b1a14f9684dc4bc  pig_1.6.2-1_amd64.deb
00e4c84cd6b07a98401c73fb58dedaafe34bc794d7604edbcb76c5de39b0fb44  pig_1.6.2-1_arm64.deb
```

发布：https://github.com/pgsty/pig/releases/tag/v1.6.2
