---
title: "七成正确的调优器：界定 pig pg tune 的边界"
linkTitle: "七成正确的调优器"
date: 2026-03-21
lastmod: 2026-10-13
description: "pig pg tune 如何根据硬件与工作负载计算 PostgreSQL 初始参数。"
tags: [postgres]
weight: 20
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-03-21<br>
> **状态：** 2026-03-23 实现，随 [pig v1.3.2](/zh/release/pig-1.3.2/) 发布。<br>
> **当前参考：** [`pig pg tune`](/zh/pg/#pg-tune)<br>
> **范围：** 根据硬件、PostgreSQL 版本与工作负载类型生成初始配置。

## 决策 {#decision}

`pig pg tune` 计算 PostgreSQL 核心参数，输出结果供用户审阅。命令探测 CPU、内存与磁盘容量，
接受用户指定的覆盖值，并按选定的工作负载类型计算。文本输出展示生成的参数；JSON 和 YAML 输出
包含输入条件与参数。用户审阅结果后，选择需要的参数，通过现有配置系统应用。

原名“七成正确的调优器”表达的是实用的起点，并非测得的准确率。

## 背景 {#context}

新安装的数据库尚无工作负载数据，也需要一套初始配置。小型开发机与大型数据库服务器无法
共用一份固定配置。根据硬件计算参数，可以提供可复现、便于检查和调整的基线。

## 考虑过的方案 {#alternatives}

- **发布一份固定配置。** 内存与并行参数需要随主机规模变化。
- **构建自适应调优器。** 这需要工作负载数据、实验与反馈循环。
- **自动应用参数。** 用户需要先审阅结果，再通过现有配置流程决定如何部署。
- **计算全部 PostgreSQL 参数。** 复制、安全与可用性设置还取决于硬件探测无法确定的业务要求。

## 契约 {#contract}

- 使用探测到的硬件，或用户明确指定的 CPU、内存与磁盘值。
- 通过 `oltp`、`olap`、`tiny`、`crit` 选择计算公式。
- 相同的实际输入与 PostgreSQL 版本产生相同参数。
- 结构化结果包含实际采用的工作负载类型、硬件与 PostgreSQL 版本。
- 文本参数按固定顺序输出，标题注明 SSD 假设。
- 校验输入范围，并省略所选 PostgreSQL 版本不支持的参数。
- 保持配置文件与运行中的服务器不变。

## 影响 {#impact}

用户可以将输出用于新安装或初步容量规划。先审阅参数，通过现有配置系统应用，再测量真实
工作负载。后续调整应依据查询并发、检查点行为、存储延迟与复制要求。

## 验证与演进 {#verification}

初始实现为
[`60eecfe`](https://github.com/pgsty/pig/commit/60eecfe045449e72d80986a0357fbe24b9e71f00)。
[v1.3.2](/zh/release/pig-1.3.2/) 首次发布参数生成功能。
[当前实现](https://github.com/pgsty/pig/blob/v1.9.0/cli/postgres/tune_result.go) 返回结果供输出层渲染。
[`tune_test.go`](https://github.com/pgsty/pig/blob/v1.9.0/cli/postgres/tune_test.go)
覆盖工作负载公式、资源边界、覆盖值与版本相关参数。

## 当前状态 {#status}

参数生成功能已经发布。
输入与输出示例见 [`pig pg` 参考文档](/zh/pg/#pg-tune)。
