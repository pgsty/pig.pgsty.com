---
title: "为什么 PIG 默认构建调试包"
linkTitle: "默认构建调试包"
date: 2026-09-03
lastmod: 2026-10-06
description: "将 RPM debuginfo/debugsource 与 DEB dbgsym 从显式启用改为显式退出的构建策略决策。"
tags: [build, cli]
weight: 35
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-09-03<br>
> **状态：** Released（已发布），随 [v1.8.1](/zh/release/pig-1.8.1/) 交付。<br>
> **当前参考：** [`pig build`](/zh/build/)<br>
> **范围：** `pig build ext` 与 `pig build pkg` 的调试包策略；单个包的产物仍以其配方为权威。

## 决策 {#decision}

`pig build ext` 与 `pig build pkg` 默认请求平台的正常调试包产物。普通构建时，PIG
不再传入禁用参数；只有需要更小或更快产物集合的用户，才显式使用 `--nodbg` 退出。

在 RPM 系统上，普通构建保留发行版的 `debuginfo` 与 `debugsource` 机制；`--nodbg`
把 `debug_package` 定义为空。在 Debian 与 Ubuntu 上，`--nodbg` 会在保留已有选项的同时，
向 `DEB_BUILD_OPTIONS` 追加 `noautodbgsym`。旧的 `-s|--symbol` 继续作为弃用的兼容空操作
被接受，因为调试产物已经不需要额外启用。

## 背景 {#context}

旧命令通过 `--symbol` 显式启用 RPM 调试产物，否则主动注入 `debug_package %{nil}`。
这与平台惯例相反，也让默认产物不利于事后故障分析。Debian 的 Debhelper 已经在满足条件时
默认创建自动 `dbgsym` 包，并提供 `noautodbgsym` 作为显式退出机制。

调试包会增加构建时间、存储和仓库容量，但这些成本可见且可管理。等到精确源码、编译器和二进制
已经变化后，再重建匹配符号通常困难得多。

## 考虑过的方案 {#alternatives}

- **继续用 `--symbol` 显式启用。** 不采用，因为发布质量的产物默认就应保留匹配的诊断材料。
- **强制所有构建都必须有调试包。** 不采用，因为快速本地构建和受限产物流仍需要明确的退出方式。
- **由 PIG 改写包配方。** 不采用，因为 spec 与 `debian/rules` 负责包内容；运行时改写既意外又难审计。
- **用 `nostrip` 退出 DEB 调试包。** 不采用，因为它会改变主二进制，而不只是省略独立的自动调试包。

## 契约 {#contract}

- 未指定 `--nodbg` 时，PIG 不添加任何禁用调试包的宏或环境选项；
- RPM 上，`--nodbg` 为 `rpmbuild` 添加 `--define "debug_package %{nil}"`；
- DEB 上，`--nodbg` 向 `DEB_BUILD_OPTIONS` 追加 `noautodbgsym`，且不丢弃已有的
  `parallel=N`、`nocheck` 等值；
- `--symbol` 为兼容继续可解析，但被隐藏、弃用且不再有必要；
- 结构化命令结果新增 `nodbg`，并保留 `symbol` 作为实际行为的反向值；
- 普通安装包仍是构建成功的判据；调试包是附加产物，不能替代主包；
- 纯 SQL、`noarch` 或其它不满足条件的构建无需生成空调试包；
- 包配方或操作者提供的构建环境中的显式决定仍然具有最终权威。命令默认值是一项策略请求，
  不是改写配方的许可。

## 影响 {#impact}

包含编译产物的扩展通常会生成更多文件，占用更多构建与仓库存储。作为回报，默认构建可以直接用于
栈回溯、core 分析和符号服务，不必再做一次重建。已有的 `--symbol` 脚本仍能运行；有意保留旧式
精简产物集合的脚本应改用 `--nodbg`。

配方仓库应删除那些不代表具体包约束的全局调试禁用语句。这必须作为独立改动审查，因为部分包是
架构无关包、无法完成调试信息提取，或使用自定义构建系统。

## 验证与演进 {#verification}

已被取代的显式启用行为可在此前固定版本的
[`build` 参数注册](https://github.com/pgsty/pig/blob/e3d1eb4a86cedddcf49fff398fc69751e861372e/cmd/build.go#L306-L314)
和
[`rpmbuild` 命令构造](https://github.com/pgsty/pig/blob/e3d1eb4a86cedddcf49fff398fc69751e861372e/cli/build/builder.go#L701-L714)
中复核。替代实现由
[`1c6f524`](https://github.com/pgsty/pig/commit/1c6f52401accc8ad6d7e8ab51248895632d7629b)
固定。命令测试保证 `--nodbg` 可见、兼容参数已弃用；构建器测试保证默认 RPM argv 不含禁用宏、
退出模式包含该宏，并保证 DEB 环境保留已有选项且只追加一次 `noautodbgsym`。

平台验证应在一个 EL builder 与一个 DEB builder 上各抽样一个含编译产物的扩展，同时检查默认
调试产物以及使用 `--nodbg` 后不再生成调试产物。配方级例外必须单独报告，不能据此声称 PIG
忽略了自己的参数。

## 当前状态 {#status}

该实现已进入经过验证的 [v1.8.1 标签](https://github.com/pgsty/pig/tree/v1.8.1)
与[正式发布制品](https://github.com/pgsty/pig/releases/tag/v1.8.1)。上述实现与本地验证的证据范围保持不变。
软件仓库发布、公开文档部署与既有系统升级仍是独立交付阶段。
