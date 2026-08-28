---
title: "Catalog v2 提案：不可变 typed snapshot，而不是更大的 CSV"
linkTitle: "Catalog v2 提案"
date: 2026-08-13
lastmod: 2026-08-28
description: "一套候选的可验证 Catalog 模型：typed target、内容寻址 snapshot、显式激活、项目 pin 与离线导入。"
tags: [catalog, repo, ext, cli]
weight: 86
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-08-13<br>
> **状态：** 实现前提案；安全机制、overlay 范围、打包方式与路径 ADR 仍未决定。<br>
> **当前参考：** [`pig ext`](/zh/ext/) 与 [`pig repo`](/zh/repo/)描述 v1 Catalog 行为。<br>
> **范围：** PIG 2.0 产品元数据的候选发布与消费模型，不包含 Inventory 或实时系统状态。

## 决策 {#decision}

Catalog v2 应当是一份由多个 typed target 组成的不可变、可验证 snapshot。
Manifest 将平台、仓库、路由、package alias、扩展、兼容性、Pigsty release 与公钥元数据绑定到精确字节。
所有候选 target 一起校验，通过同一个 pointer 激活，避免新仓库 Catalog 与旧扩展矩阵被静默混装。

Snapshot digest 是最终身份。Package、system、user、portable 与 project scope 保存或选择的是同一份
已验证内容，而不是把无关 base snapshot 合并成一份人工 Catalog。

## 背景 {#context}

v1 Catalog 很实用，但相关事实散布在 embedded CSV、repository YAML、Pigsty 变量、生成站点和 reload 路径中。
部分字段重复维护可推导信息，extension matrix 也把几个独立身份压缩到同一条记录。
独立更新后，很难证明 repository、package、extension 与 compatibility 数据来自同一次发布。

因此，Catalog v2 首先是发布与信任问题，而不仅是换一种序列化格式。

## 考虑过的方案 {#alternatives}

- **制作更大的 `extension.csv` 或一个巨型 YAML。** 不同 target 类型演进速度不同，也无法独立流式处理并整体激活。
- **立即使用 SQLite、protobuf 或定制二进制矩阵。** 当前数据量没有证明值得承担新的运行时与调试成本。
- **按字段合并 system、user、project base snapshot。** 结果没有单一 publisher、digest、兼容声明或签名。
- **只把 active 或 project pin 内容放在 cache。** 删除缓存不能破坏持久的用户或项目决定。
- **允许 user file 遮蔽官方 trust root。** 安全 policy 是约束，不是普通的后写覆盖偏好。
- **后台静默更新并激活。** 元数据变化可能改变包解析，必须是可观察操作。

## 契约 {#contract}

候选 snapshot 契约是：

- Manifest 与小型 target 使用确定性 UTF-8 JSON，大型稀疏 target 使用 JSONL；
- 直接校验原始 manifest bytes 与 target length/hash，避免 parse 后重新序列化产生歧义；
- Manifest 包含 schema、单调安全版本、创建时间、过期时间、channel 和 PIG/Pigsty 兼容范围；
- 始终提供 embedded rescue baseline；
- package-owned baseline、durable snapshot store、可变状态 pointer 与可清理下载 cache 使用不同路径；
- Linux 遵循 FHS/XDG，macOS 使用 Application Support 与 Caches，portable `PIG_HOME` 仍区分
  config、data、state、cache 与 run；
- project lock 记录 snapshot 身份和有序 overlay，已验证 snapshot 物化到持久 project support data；
- 选择 digest 与寻找该 digest 的 bytes 是两个独立算法；
- 低层 scope 只能收紧 system security policy，不能静默放宽；
- 更新下载到私有 staging，校验每一层，sync 后移动到内容寻址 store，再原子替换 active pointer；
- 失败时保留此前 active snapshot；
- user/system active channel 更新不会移动 project pin；
- 离线导出包含验证元数据和公开 trust material，绝不包含私钥；
- 旧 `ext reload` 与 `repo reload` 可以在一个兼容周期内映射到整体 snapshot update，
  但不能分别激活 target。

运行时 Catalog 明确不包含 Inventory、凭据、实时探测、已安装包状态、Ansible event、provider state、
危险操作确认和不属于产品决策的短期波动指标。

## 影响 {#impact}

Typed target 让所有权与校验更清晰，内容寻址让 rollback 与 airgap import 可审计。
Project materialization 避免部署依赖某个用户的全局 cache。独立 OS package 可以更新只读 baseline，
而不改变 active user selection。

代价是一套更大的发布协议：key rotation、expiry、rollback protection、GC、路径权限、迁移、
包管理器生命周期、overlay 冲突与跨仓 generator 都会成为兼容敏感工作。

Extension 模型也必须分离 SQL extension 身份、上游项目、distribution/build unit、版本化 release、
OS package offer、目标可用性和展示 policy。Aggregate platform support、`required_by` 等派生字段应由
generator 计算，而不是维护第二份事实。

## 验证与演进 {#verification}

实现前必须通过 ADR 在 go-tuf 与最小 signed manifest 之间作出选择。
两个候选必须通过同一组威胁测试：坏签名、过期元数据、回滚、target 替换、snapshot 混装、截断下载与离线验证。
如果都不能通过，Catalog v2 就不能作为 2.0 发布功能。

其它门槛覆盖 FHS/XDG/macOS/portable 路径、root 与非 root 权限、只读 home/project、符号链接替换、
磁盘写满与并发激活、package upgrade/remove 语义、删除全局 cache 后 project 仍能工作，
以及当前扩展和可用矩阵的无损迁移。

当前源码基线仍是
[`v1.8.0`](https://github.com/pgsty/pig/commit/67dac09caab843252ea4376bf16b08c5e238ff22)，
其 embedded 与可 reload 的 v1 Catalog 继续定义已发布行为。

## 当前状态 {#status}

今天没有任何 Catalog v2 命令、manifest、trust root、store 布局、project lock 或迁移格式属于已发布 PIG 契约。
如果 typed overlay 的冲突与信任规则无法得到证明，应从 2.0 中删去；完整自定义签名 channel
比松散、未验证的 patch 更安全。当前安装与 Catalog 行为仍以 [`pig ext`](/zh/ext/) 和
[`pig repo`](/zh/repo/)为准。
