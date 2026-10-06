---
title: "pig v1.8.1"
linkTitle: "v1.8.1"
date: 2026-09-03
description: "CLI 安全与仓库流程加固、扩展目录刷新、Go 1.27.1，以及 cargo-pgrx 0.19.2。"
tags: [cli, repo, build, catalog]
weight: 2
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.8.1
---

Pig `v1.8.1` 是 [v1.8.0](/zh/release/pig-1.8.0/) 之上的安全、正确性与维护版本。
本版本加固命令初始化、提权日志访问、仓库与构建流程、发布完整性，以及结构化输出脱敏；
同时刷新内置扩展目录，并将构建工具链升级到 Go `1.27.1` 与 `cargo-pgrx 0.19.2`。
内置 Pigsty 版本仍为 `4.5.0`。

## CLI 安全与正确性

- 只读且不依赖配置的命令不再要求 `HOME` 可写，也不会把创建 `~/.pig` 当作查询副作用；
  叶子命令会保留自己声明的初始化策略。
- `pig pg log`、`pig pt log` 与 `pig pb log` 通过 sudo 切换数据库 OS 用户时完整保留参数，
  并拒绝不安全的日志文件链接。
- `pig do` 在执行前校验 Pigsty 名称，并拒绝 Ansible 保留的集群目标。
- PostgreSQL 原生角色检测绑定到用户选中的实例，而不是无关的本机默认实例。
- 结构化结果会遮盖凭据、许可证材料与构建代理标识符，同时保持真实的失败状态。

## 仓库与构建加固

- 仓库添加与删除在任一请求失败时整体返回失败，对模块选择去重，并保持替换边界。
- 离线缓存包拒绝不安全路径、链接、特殊文件与不完整输入；归档解压继续采用有根、失败关闭的实现。
  生产路径迁移到结构化结果后，删除了仅由测试引用的旧导出缓存包装。
- 构建源码与制品校验会拒绝不完整或不安全输入；`pig build proxy` 使用软件包提供的服务契约，
  参数保持可选，结构化输出不再泄露秘密标识符。
- 自更新会验证发布校验和；发布工具拒绝脏工作区、错误 tag，以及覆盖不可变制品。

## 工具链与扩展目录

- `pig build ext` 与 `pig build pkg` 默认保留平台调试包；使用 `--nodbg` 显式省略。
  `-s|--symbol` 保留为已弃用的兼容空操作。

- Go 升级到 `1.27.1`，Logrus 升级到 `1.10.2`，GoReleaser 升级到 `2.18.0`，
  golangci-lint 升级到 `2.13.2`。
- `pig build pgrx` 默认安装 `cargo-pgrx 0.19.2`；如果某个扩展的目录元数据要求旧版 pgrx，
  仍可通过 `-v` 显式选择。
- 内置目录从维护中的 pgext 视图刷新：新增 `acdat 0.1.0`，将已被取代的
  `pgcontext_pgvector` 标记为 removed，并更新软件包版本、仓库归属、PostgreSQL 覆盖与可用性矩阵。

## 验证

本版本从源码提交
[`1c6f524`](https://github.com/pgsty/pig/commit/1c6f52401accc8ad6d7e8ab51248895632d7629b)
构建。该精确提交通过完整 [CI 工作流](https://github.com/pgsty/pig/actions/runs/33747971725)，
覆盖随机顺序测试、命令 race 回归、vet、静态分析、死代码检查、漏洞扫描与 GoReleaser snapshot。
随后 tag 通过 [Release 工作流](https://github.com/pgsty/pig/actions/runs/33748002429)，生成并发布
RPM、DEB、macOS 与 Linux 制品。

## 兼容性提醒

- 本版本没有移除 CLI 命令或参数。
- 如果旧脚本依赖只读命令顺便创建本地配置，应改为显式准备所需状态。
- pgrx 默认值变为 `0.19.2`；构建特定扩展时，仍以该扩展的目录元数据为准。

## 校验和

```checksums
4154b3e49cb499e57d7c7b1ab4ae5e45d03d5d0c2ffe26d6ade64e46db6923cf  pig-1.8.1-1.aarch64.rpm
35c398f409d9293b4f8c0cdf949b19c62d06016ec7e724472143d2327199869d  pig-1.8.1-1.x86_64.rpm
6c08b6a698191b8b6494a0f60880fb17cafa535bad12d5c544333e4625048455  pig-v1.8.1.darwin-amd64.tar.gz
0fb6c86cc18a29aeb74e9d12e717c104087c6ecf5a43250dfcc71cd7681fb868  pig-v1.8.1.darwin-arm64.tar.gz
9219e87433ebd239e0773ae7417fdd08e97bb511312e6747542bf46b6b1bbf2b  pig-v1.8.1.linux-amd64.tar.gz
b30924880f21126ece3afc77ca75794a0ceb77964cdfd8bc20da72d9d3273078  pig-v1.8.1.linux-arm64.tar.gz
6fc304501671921b18439223c630c7d4635b10ac75493d5c12a5987ff80c618e  pig_1.8.1-1_amd64.deb
1a70cd71f6c1f443812fe30535427891513c0ba03be219ac21f1a3d6fd450051  pig_1.8.1-1_arm64.deb
```

{{< release-card >}}
