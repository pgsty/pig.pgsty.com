---
title: "PIG 2.0 产品方向：一份提案，而不是发布契约"
linkTitle: "PIG 2.0 提案"
date: 2026-08-13
lastmod: 2026-09-03
description: "PIG 2.0 的候选边界：稳定的 Pigsty 初始化前门、可验证 Catalog 客户端，以及保持显式部署的薄编排层。"
tags: [cli, sty, catalog]
weight: 85
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-08-13<br>
> **状态：** 等待 owner 审议的提案；尚未实现，也不是 PIG 2.0 发布承诺。<br>
> **当前参考：** [PIG 文档](/zh/docs/)与当前 [v1.8.1 发布](/zh/release/pig-1.8.1/)<br>
> **范围：** 未来 PIG 2.0 / Pigsty 5.0 的候选产品边界与验证门槛。

## 决策 {#decision}

提案方向是让 PIG 成为从空白控制节点到经过校验、可以部署的 Pigsty Inventory 的稳定初始化前门。
PIG 拥有 Catalog 选择、解析、计划、有边界的执行编排、结构化结果与脱敏 receipt；
软件包事务、配置应用与基础设施状态继续委托给 DNF/APT、Ansible 和未来的 provider 工具。

提案有意保留 PIG 的独立价值：`repo`、`ext`、`install` 在没有 Pigsty 项目时也必须可用。
它也保留显式部署同意：未来的 `pig sty setup` 可以下载、引导与生成配置，但不能在用户没有单独调用部署时
自动执行多节点 deploy。

## 背景 {#context}

到 v1.8.0，PIG 已经能够下载 release、原生引导控制节点、编译 Inventory、管理仓库与扩展，
并执行部分运维操作。产品仍存在几个接缝：

- repository、package alias、extension、route 与 Pigsty 元数据可以独立变化；
- 项目没有明确 Catalog 身份，无法防止后续解析受全局更新影响；
- 路由选择与仓库安全还不是一套可见产品契约；
- 初始化路径上的执行结果还没有形成持久、脱敏的 receipt；
- PIG、Pigsty、Catalog schema、操作系统与 Ansible 的兼容性需要统一发布矩阵，而不是分散假设。

提案把这些接缝定义为 2.0 问题，而不是把大版本当作随意改名或重造既有工具的许可。

## 考虑过的方案 {#alternatives}

- **把 PIG 变成单体配置与状态引擎。** Inventory、Catalog authoring、包管理器、Ansible 与 provider
  已经分别拥有不同事实，因此否决。
- **让 Pigsty 运行时依赖 PIG 或 pgext checkout。** Pigsty release 必须依靠版本化生成产物独立工作。
- **让 setup 自动部署。** 生成并校验配置与修改远程节点属于不同的同意边界。
- **重新实现 DNF/APT failover 或 Ansible 执行。** PIG 应选择输入并解释结果，而不是成为另一个包管理器或配置引擎。
- **让 Vagrant/Terraform 统一阻塞 2.0。** Lab provider 状态语义不同，也不决定核心初始化路径。
- **立即发明万能 `sty plan`。** 至少两个 PIG 自有工作流证明同一计划 schema 可复用后再讨论。

## 契约 {#contract}

如果获得批准，产品方向将遵循以下边界：

- 每类事实只有一个权威：Inventory 负责集群声明，Catalog authoring source 负责产品元数据，
  project lock 负责选中 snapshot 身份，receipt 负责观测结果，provider 负责实时状态；
- PIG 拥有 Catalog schema、校验、客户端、resolver 与选择逻辑，但不拥有所有 authoring 数据库；
- `sty setup` 组合既有 init、boot、configure use case，不复制实现；
- setup 在 Inventory 校验后停止，deploy 继续显式执行；
- 独立命令跟踪兼容 Catalog channel，Pigsty 项目在成功 setup 或 conf 提交后 pin 当时的 snapshot；
- 普通命令不隐式改写已有 project lock；
- 路由选择来自显式配置或有边界的首次判断，不构建持续 GeoIP、云 IMDS 或后台测速服务；
- 软件包下载重试与 endpoint failover 由 DNF/APT 负责；
- 执行 artifact 版本化并脱敏，raw 上游模式保持原生输出流与退出语义；
- doctor 保持诊断角色，不获得默认修复权限；
- 未来 lab 支持只做薄适配，PIG 不拥有 Terraform state。

## 影响 {#impact}

提案会让首次使用路径更清晰，也让元数据选择可以审计。与此同时，它会新增 snapshot identity、
project lock、迁移规则、trust policy、receipt 和兼容矩阵等持久契约。
这些契约会显著增加测试与发布负担，不能作为松散功能各自交付。

一些有吸引力的工作被明确设为可选或延期。Ansible event bridge 只有在脱敏与兼容实验通过后才是目标；
doctor/support bundle 与 lab adapter 属于 GA 之后；EL7 支持档位仍是 owner 决策，不是隐含兼容承诺。

## 验证与演进 {#verification}

提案成为发布契约前需要以下证据：

- 覆盖声明 Linux 目标的原生 onboarding VM 矩阵；
- Catalog 签名、过期、回滚、混装与离线场景的对抗测试；
- 证明 Pig、Pigsty、pgext 生成消费者不会漂移的语义 diff；
- `no_log` 与秘密零泄露的 Ansible callback 实验；
- 全球、中国、代理和受限网络环境的路由选择测试；
- 修改安全默认值前的仓库签名矩阵；
- 1.x 到 2.0 的布局、lock 与混合版本迁移演练；
- 与明确兼容矩阵绑定的 schema 和结构化输出 fixture。

当前实现基线是
[`v1.8.0`](https://github.com/pgsty/pig/commit/67dac09caab843252ea4376bf16b08c5e238ff22)。
该版本已经包含原生 boot 与 configure，但没有实现提案中的 Catalog v2、project pin、setup 命令、
event receipt 或 2.0 迁移契约。

## 当前状态 {#status}

这是一份公开提案记录，不是发布公告。当前用户应继续遵循 [v1.8.1 文档](/zh/docs/)。
Catalog v2 安全方案、typed overlay、路径布局细节、EL7 支持档位、event bridge 可行性与最终 2.0 范围，
都需要明确决策和实验结果，之后才能作出实现或发布声明。
