---
title: "复用 Pigsty 已经拥有的 CMDB"
linkTitle: "既有 CMDB 边界"
date: 2026-07-18
lastmod: 2026-08-28
description: "为什么 PIG 撤销全新的 revision store 设计，转而成为 Pigsty 既有 PostgreSQL CMDB 的轻量受控适配器。"
tags: [inventory, sty]
weight: 60
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-07-18<br>
> **状态：** 全新 revision store 已被取代；复用既有 CMDB 的薄适配器已经实现，但仍为实验功能。<br>
> **当前参考：** [`pig inventory cmdb`](/zh/inventory/)<br>
> **范围：** 与 Pigsty 既有 CMDB 交换声明，而不是再设计一个配置数据库。

## 决策 {#decision}

PIG 必须复用 Pigsty 已经提供的 CMDB。它的职责是有边界的适配：校验静态 Inventory，
将声明装载到既有表中，导出既有投影，检查一致性，并安全切换 Ansible 的静态与动态数据源。

PIG 不拥有第二套 schema、迁移历史、快照账本、CAS revision store、三方合并引擎或数据库回滚系统。

## 背景 {#context}

早期设计把 CMDB 支持当成一个全新后端，提出独立 schema、不可变快照、revision token、合并与回滚、
备份 bundle 和数据源切换记录。方案内部逻辑完整，但出发点错误：Pigsty 已经拥有 `pigsty` 与 `pglog`
schema、装载脚本、动态 Inventory 投影和数据源切换行为。

再建一套控制面会复制事实、制造同步问题，并让 PIG 对另一个项目拥有的数据模型负责。

## 考虑过的方案 {#alternatives}

- **把新 revision store 保留为高级模式。** 即使可选，两套权威仍然是两套权威。
- **在新旧 schema 之间双向镜像。** 冲突处理与迁移会成为永久产品责任。
- **只用 Shell 包装既有脚本。** PIG 仍需要有边界的超时、安全连接处理、结构化计划与原子数据源切换。
- **完全删除 CMDB 支持。** 一个小型原生适配器仍能提供有价值的校验与自动化，而不重新定义 schema。

## 契约 {#contract}

- Pigsty 既有 schema 与投影是数据模型权威；
- PIG 通过显式数据库目标、环境配置或 `service=meta` 连接；
- 凭据、DSN、SQL 正文与声明值不得进入计划或诊断；
- `check` 只读；
- `init` 应用既有基线，但不声称会备份现有数据库；
- `load` 在事务内替换声明行，并要求显式确认；
- `dump` 在没有 force 时拒绝意外覆盖；
- `enable` 与 `disable` 只修改能够识别的 Ansible Inventory source 形式，并原子写入；
- 无法识别的可执行 Inventory source 一律拒绝，不擅自重写；
- 整个命令族继续明确标记为实验功能。

## 影响 {#impact}

纠偏删除了大量已经写出的 revision-store 代码。这是有意恢复范围，不是功能损失：
被删除的功能描述的是一个 PIG 本就不应该拥有的产品。

保留下来的适配器更小、更容易审计，也与现有 Pigsty 运维方式兼容。
它同时继承既有系统的限制：`init` 需要运维人员自行备份，装载声明属于替换操作，而不是协同版本控制。

## 验证与演进 {#verification}

纠正后的边界记录在 [`ba6e678`](https://github.com/pgsty/pig/commit/ba6e678)。
废弃实现由 [`e0f73ed`](https://github.com/pgsty/pig/commit/e0f73ed) 删除，
其中包括平行 schema、snapshot、merge、revision 与 rollback 机制。
保留路径的测试覆盖 PostgreSQL 兼容性、连接信息脱敏、事务失败、摘要绑定确认、dump 安全和原子数据源切换。

## 当前状态 {#status}

既有 CMDB 适配器已随 [v1.6.0](/zh/release/pig-1.6.0/) 发布，但仍为实验功能。
在真实 CMDB 上执行初始化或替换前应自行备份，并使用当前 [`pig inventory` 文档](/zh/inventory/)，
不要再参考已经废弃的早期设计。
