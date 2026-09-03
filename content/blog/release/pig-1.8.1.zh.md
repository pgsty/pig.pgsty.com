---
title: "pig v1.8.1"
linkTitle: "v1.8.1"
date: 2026-09-03
description: "CLI 安全与仓库流程加固、扩展目录刷新、Go 1.27.1，以及 cargo-pgrx 0.19.2。"
tags: [cli, repo, build, catalog]
weight: 1
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

- Go 升级到 `1.27.1`，Logrus 升级到 `1.10.2`，GoReleaser 升级到 `2.18.0`，
  golangci-lint 升级到 `2.13.2`。
- `pig build pgrx` 默认安装 `cargo-pgrx 0.19.2`；如果某个扩展的目录元数据要求旧版 pgrx，
  仍可通过 `-v` 显式选择。
- 内置目录从维护中的 pgext 视图刷新：新增 `acdat 0.1.0`，将已被取代的
  `pgcontext_pgvector` 标记为 removed，并更新软件包版本、仓库归属、PostgreSQL 覆盖与可用性矩阵。

## 验证

本版本从源码提交
[`e3d1eb4`](https://github.com/pgsty/pig/commit/e3d1eb4a86cedddcf49fff398fc69751e861372e)
构建。该精确提交通过完整 [CI 工作流](https://github.com/pgsty/pig/actions/runs/33718574084)，
覆盖随机顺序测试、命令 race 回归、vet、静态分析、死代码检查、漏洞扫描与 GoReleaser snapshot。
随后 tag 通过 [Release 工作流](https://github.com/pgsty/pig/actions/runs/33718945217)，生成并发布
RPM、DEB、macOS 与 Linux 制品。

## 兼容性提醒

- 本版本没有移除 CLI 命令或参数。
- 如果旧脚本依赖只读命令顺便创建本地配置，应改为显式准备所需状态。
- pgrx 默认值变为 `0.19.2`；构建特定扩展时，仍以该扩展的目录元数据为准。

## 校验和

制品：[GitHub Release](https://github.com/pgsty/pig/releases/tag/v1.8.1) · [checksums.txt](https://github.com/pgsty/pig/releases/download/v1.8.1/checksums.txt)

```checksums
839ce3818941318be7707bd6c845f371c609d6f176f04705916108f04cbee38c  pig-1.8.1-1.aarch64.rpm
54183895b09f82fb4d00d75f99e84f6bb4761e4bebd24042d646ee8b309a6d03  pig-1.8.1-1.x86_64.rpm
167891e181d460d478a5ed8637d41017bc73201ec479a5735ca43c09dcf3826f  pig-v1.8.1.darwin-amd64.tar.gz
1338500b4373c3ee3a08d6233202b3f391f5bf69ac0517501884ed2978e17d26  pig-v1.8.1.darwin-arm64.tar.gz
5050cc4444313edc5863acd1a6c20bcfd3ae4af6e849c978d9a5882bc58f60a3  pig-v1.8.1.linux-amd64.tar.gz
ecf5fcf11e35169b557380bbfc717562db5a440271b79b9eb3b8fd74c0c7f167  pig-v1.8.1.linux-arm64.tar.gz
cf0de4f938c7360908ac0e315a7241ab7f3810eb026e28d4b92137ad743dde34  pig_1.8.1-1_amd64.deb
108f50c5e6ccaf87b27cb62e36bbd8b45436039626e7715dbb3912bcbbb6963b  pig_1.8.1-1_arm64.deb
```

{{< release-card >}}
