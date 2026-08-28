---
title: "危险操作只有一套语法：PIG 运维 CLI 安全契约"
linkTitle: "运维 CLI 安全"
date: 2026-07-02
lastmod: 2026-08-29
description: "PIG 如何分离底层原语与编排器、显式表达破坏性意图，并防止别名或结构化输出改变操作含义。"
tags: [cli, postgres, pgbackrest, pitr]
weight: 40
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-07-02<br>
> **状态：** `pg`、`pb`、`pt`、`pitr` 已于 v1.5.0 交付；2026-08-29 的 `do` 与 `build proxy` 修订已在源码中实现并通过测试，但尚未发布。<br>
> **当前参考：** [`pig pg`](/zh/pg/)、[`pig pb`](/zh/pb/)、[`pig pitr`](/zh/pitr/)、[`pig do`](/zh/do/) 与 [`pig build`](/zh/build/)<br>
> **范围：** PIG 自己拥有的运维命令；透明上游命令继续采用上游的确认与退出行为。

## 决策 {#decision}

操作便利性不能模糊操作含义。PIG 明确区分底层原语与多阶段编排器，显式表达破坏性意图，
谨慎分配别名，并要求计划与结构化结果描述的动作必须和文本模式真正执行的动作一致。

最重要的例子是恢复：`pig pb restore` 是 pgBackRest 原语，`pig pitr` 则协调 Patroni、
PostgreSQL 停止、恢复、重新启动与恢复后指引。任何别名都不能让这两条路径看起来可以互换。

## 背景 {#context}

第一代便利别名积累了不一致的位置参数、确认参数、输出处理与服务语义。
`restart`、`restore`、`promote`、`failover` 等相似词在不同层次代表完全不同的操作。
跨越层次的短别名可能把看似无害的调用变成缺少编排保护的破坏性原语。

自动化还暴露出假成功问题：包装器输出、子进程输出和结果渲染可能使用不同的成功定义。

## 考虑过的方案 {#alternatives}

- **尽可能增加短别名。** 冲突和跨层同义词带来的风险高于节省几个字符的价值。
- **给所有看起来危险的单词都加确认。** 对透传命令不成立，因为提示与语义必须由上游工具拥有。
- **让编排器成为原语的便利别名。** 恢复编排拥有额外的停止、验证与重启不变量，不能合并。
- **启动内层命令后立即返回成功。** 结果必须反映 PIG 拥有的完整工作流。

## 契约 {#contract}

- 同级命令名称与别名唯一；
- 子命令别名不能遮蔽另一个顶层命令；
- PIG 自己拥有的破坏性操作要求显式确认，并在有意义时提供无副作用计划；
- 命令层在产生副作用前拒绝错误或多余的位置参数；
- 命令专用名称遵循下游 Pigsty 契约；下游 Playbook 没有显式语法时，只采用有文档说明的最窄安全边界；
- 结构化输出与文本模式共享同一个结果和成功定义；
- 含凭据的值不进入诊断输出；就绪或连通性失败必须保持命令失败，不能只记警告后返回成功；
- 底层 restore 不声称管理 Patroni 或 HA 路由；
- PITR 编排器按需停止管理器，证明 PostgreSQL 已停止，执行恢复，可选启动 PostgreSQL，
  并有意保持 Patroni 停止，等待运维人员验证；
- 额外原生参数只通过明确记录的边界传递。

## 影响 {#impact}

部分历史缩写被移除，一些脚本需要采用 cluster-first 或显式目标语法。
作为回报，命令名称保留了层次边界，计划对应真实动作，恢复自动化也不会悄悄用原语替换编排器。

这套契约不会消除操作风险。它的作用是让风险可见，并阻止便利层制造歧义。

## 验证与演进 {#verification}

规范命令契约在 [`c62c0f5`](https://github.com/pgsty/pig/commit/c62c0f5) 中进入仓库。
后续提交继续统一别名、早期校验、恢复目标、服务语义与角色检测。
Guard 测试遍历 Cobra 树，拒绝同级与跨层别名冲突；恢复测试覆盖计划、确认、停止升级、旁路恢复、
重启行为与结构化失败结果。

Patroni 后来改成透明透传，这仍遵循同一原则：PIG 只为自己拥有的工作流提供安全保证。

同一契约在 [`3e1603b`](https://github.com/pgsty/pig/commit/3e1603b) 中扩展到 `pig do` 的名称与集群校验，
并在 [`a880485`](https://github.com/pgsty/pig/commit/a880485) 中封闭 Ansible 内置目标。
软件包驱动、凭据安全且如实报告失败的 `build proxy` 设置进入
[`220ef9c`](https://github.com/pgsty/pig/commit/220ef9c)，随后由
[`74cb128`](https://github.com/pgsty/pig/commit/74cb128) 补齐结构化参数遮盖与机器注解，
并在 [`de7ffd0`](https://github.com/pgsty/pig/commit/de7ffd0) 中把可选参数同步到机器语法。
这些修改均在 Ubuntu 24.04 与 Rocky Linux 9 ARM64 Farrow 客体中完成实机测试；
这属于源码与本地测试环境证据，不是发布证据。

## 当前状态 {#status}

明确需要 pgBackRest 原语时使用 `pig pb restore`；需要受控恢复流程时使用 [`pig pitr`](/zh/pitr/)。
当前语法、警告与平台要求维护在命令参考页中，而不是冻结在这篇历史记录里。
