---
title: "PIG 2.0 产品方向"
linkTitle: "PIG 2.0 提案"
date: 2026-08-13
lastmod: 2026-10-13
description: "PIG 2.0 提案：统一 Pigsty 初始化入口，校验 Catalog，固定项目所用版本，并保留独立部署步骤。"
tags: [cli, sty, catalog]
weight: 85
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-08-13<br>
> **状态：** 提案，待审议，尚未实现。<br>
> **当前参考：** [PIG 文档](/zh/docs/)与当前 [v1.9.0 发布](/zh/release/pig-1.9.0/)<br>
> **范围：** 未来 PIG 2.0 / Pigsty 5.0 的候选产品边界与验证门槛。

## 决策 {#decision}

提案方向是让 PIG 成为从空白控制节点到经过校验、可以部署的 Pigsty Inventory 的统一初始化入口。
PIG 负责 Catalog 选择与解析、执行计划、流程编排、结构化结果与脱敏执行记录；
软件包事务、配置应用与基础设施状态继续委托给 DNF/APT、Ansible 和未来的基础设施工具。

提案有意保留 PIG 的独立价值：`repo`、`ext`、`install` 在没有 Pigsty 项目时也必须可用。
它也保留独立部署步骤：未来的 `pig sty setup` 可以下载、引导与生成配置，但不能在用户没有单独调用部署时
自动执行多节点 deploy。

## 背景 {#context}

到 v1.8.0，PIG 已经能够下载 release、原生引导控制节点、编译 Inventory、管理仓库与扩展，
并执行部分运维操作。产品仍有以下问题：

- 仓库、包别名、扩展、路由与 Pigsty 元数据可以独立变化；
- 项目没有明确 Catalog 身份，无法防止后续解析受全局更新影响；
- 路由选择与仓库安全还不是一套可见产品契约；
- 初始化路径上的执行结果还没有形成持久、脱敏的执行记录；
- PIG、Pigsty、Catalog schema、操作系统与 Ansible 的兼容性需要统一发布矩阵，而不是分散假设。

提案将 2.0 的重点放在元数据一致性与可重复的初始化流程上。

## 考虑过的方案 {#alternatives}

- **把 PIG 变成单体配置与状态引擎。** Inventory、Catalog 编写工具、包管理器、Ansible 与基础设施工具
  已经分别拥有不同事实，因此否决。
- **让 Pigsty 运行时依赖 PIG 或 pgext checkout。** Pigsty release 必须依靠版本化生成产物独立工作。
- **让 setup 自动部署。** 生成并校验配置与修改远程节点属于不同的同意边界。
- **重新实现 DNF/APT failover 或 Ansible 执行。** PIG 应选择输入并解释结果，而不是成为另一个包管理器或配置引擎。
- **让 Vagrant/Terraform 统一阻塞 2.0。** 实验环境工具的状态语义不同，也不决定核心初始化路径。
- **立即发明万能 `sty plan`。** 至少两个 PIG 自有工作流证明同一计划 schema 可复用后再讨论。

## 契约 {#contract}

如果获得批准，产品方向将遵循以下边界：

- 每类事实只有一个权威：Inventory 负责集群声明，Catalog 编写来源负责产品元数据，
  项目锁定文件负责选中的快照身份，执行记录负责观测结果，基础设施工具负责实时状态；
- PIG 拥有 Catalog schema、校验、客户端、解析器与选择逻辑，但不拥有所有元数据编写数据库；
- `sty setup` 组合既有 init、boot、配置流程，不复制实现；
- setup 在 Inventory 校验后停止，deploy 继续显式执行；
- 独立命令跟踪兼容 Catalog 发布通道，Pigsty 项目在成功 setup 或 conf 提交后锁定当时的快照；
- 普通命令不隐式改写已有项目锁定文件；
- 路由选择来自显式配置或有边界的首次判断，不构建持续 GeoIP、云 IMDS 或后台测速服务；
- 软件包下载重试与下载端点切换由 DNF/APT 负责；
- 执行产物按版本管理并脱敏，raw 上游模式保持原生输出流与退出语义；
- doctor 保持诊断角色，不获得默认修复权限；
- 未来 lab 支持只做薄适配，PIG 不拥有 Terraform state。

## 影响 {#impact}

提案会让首次使用路径更清晰，也让元数据选择可以审计。与此同时，它会新增快照身份、
项目锁定文件、迁移规则、信任策略、执行记录和兼容矩阵等持久契约。
这些契约会显著增加测试与发布负担，不能作为松散功能各自交付。

Ansible 事件桥接需要先通过脱敏与兼容实验。诊断与支持包、实验环境适配器推迟到首版发布之后；
EL7 支持级别仍待决定。

## 验证与演进 {#verification}

提案成为发布契约前需要以下证据：

- 覆盖声明支持的 Linux 平台，验证原生初始化流程；
- Catalog 签名、过期、回滚、混装与离线场景的对抗测试；
- 证明 Pig、Pigsty、pgext 生成消费者不会漂移的语义差异检查；
- `no_log` 与秘密零泄露的 Ansible 回调实验；
- 全球、中国、代理和受限网络环境的路由选择测试；
- 修改安全默认值前的仓库签名矩阵；
- 1.x 到 2.0 的布局、lock 与混合版本迁移演练；
- 与明确兼容矩阵绑定的 schema 和结构化输出测试样例。

这份提案采用的实现基线是
[`v1.8.0`](https://github.com/pgsty/pig/commit/67dac09caab843252ea4376bf16b08c5e238ff22)。
该版本已经包含原生 boot 与 configure，但没有实现提案中的 Catalog v2、项目版本锁定、setup 命令、
事件执行记录或 2.0 迁移契约。

## 当前状态 {#status}

提案仍待审议。Catalog 安全机制、覆盖规则、路径、EL7 支持与 Ansible 事件桥接需要继续决策。
已发布命令的用法见[当前文档](/zh/docs/)。
