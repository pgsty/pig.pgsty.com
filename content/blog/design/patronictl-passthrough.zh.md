---
title: "让 Patronictl 自己说话"
linkTitle: "Patronictl 透明透传"
date: 2026-07-21
lastmod: 2026-08-28
description: "为什么 pig pt 不再镜像 Patronictl 命令树，而是只保留少量 PIG 本地辅助功能的透明启动器。"
tags: [patroni, cli]
weight: 80
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-07-21<br>
> **状态：** 已实现并随 [pig v1.6.0](/zh/release/pig-1.6.0/) 发布。<br>
> **当前参考：** [`pig pt`](/zh/pt/)<br>
> **范围：** Patronictl 集群命令，以及 PIG 拥有的配置选择、参数设置、服务、状态和日志辅助功能。

## 决策 {#decision}

`pig pt` 是已安装 `patronictl` 的透明启动器。PIG 选择配置并分派少量本地辅助命令；
其它命令 token 及其后的所有参数原样传递，保留原生提示、终端行为、输出格式与退出码。

PIG 不再维护一份持续变化的 Patronictl 命令树副本。

## 背景 {#context}

镜像 Patronictl 要求 PIG 复制命令、参数、位置语法、确认方式、格式和版本相关行为。
上游接口持续演进，PIG 的副本必然漂移。同一个操作通过 `patronictl` 与 PIG 调用时可能出现不同语义。

包装器在 Pigsty 环境中仍有价值：以数据库操作系统用户选择正确配置，提供本地服务和日志工作流，
并把一小段参数设置便利语法翻译为一次原生 edit-config 调用。

## 考虑过的方案 {#alternatives}

- **继续镜像全部上游命令。** 必然滞后，并重复 Patronictl 已经拥有的校验。
- **只允许经过测试的命令白名单。** 新上游命令仍要等待 PIG 发布后才能使用。
- **把原生输出捕获成 PIG JSON。** 会破坏交互编辑、流式输出、提示、终端保真和上游 schema。
- **完全删除 `pig pt`。** 确定性配置选择与本地 Pigsty 辅助能力仍然有价值。

## 契约 {#contract}

- 第一个非选项命令 token 决定本地分派还是透传；
- `set`、本地 service shortcut、`status` 与 `log` 由 PIG 拥有；
- 其它命令和剩余 token 原样转发；
- `pig pt -- COMMAND ...` 显式绕过本地名称冲突；
- 包装器参数必须出现在原生命令 token 之前；
- 原生 help 可以在没有本地 Patroni 配置时运行；
- Patronictl 拥有交互提示、原生 `--format` 和退出码；
- 会产生原生参数歧义的 PIG 全局结构化输出被明确拒绝；
- 配置按确定顺序解析，进程以数据库系统用户运行。

## 影响 {#impact}

自动化需要采用 Patronictl 的 cluster-first 位置语法与原生输出参数。
部分 PIG 专有别名和结果 schema 被移除。换来的好处是：新 Patronictl 功能无需等待 PIG 发布，
行为也不再依赖滞后的包装器实现。

本地 `set` 辅助功能有意保持很小：它只分类 Patroni 标量键与 PostgreSQL 参数，然后执行一次原生 edit-config。

## 验证与演进 {#verification}

重写提交为 [`6cbc23b`](https://github.com/pgsty/pig/commit/6cbc23b)。
测试覆盖 token 边界、argv 原样保留、配置优先级、数据库用户执行、原生退出码、无配置 help、
输出模式拒绝、`--` 逃逸与本地辅助命令冲突。最终 help 路径修正在 v1.6.0 前完成。

## 当前状态 {#status}

透传命令语法以 Patronictl 自身文档为准；PIG 的配置选择与本地辅助功能以 [`pig pt`](/zh/pt/) 为准。
不能用 PIG `-o json` 代替 Patronictl 原生 `--format json`。
