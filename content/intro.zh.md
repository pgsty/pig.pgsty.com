---
title: "简介"
linkTitle: "简介"
description: "PIG 管什么、解决什么，以及包管理能力止步于哪里"
search_keywords: [概览, 架构, 职责边界, 软件包]
search_boost: 1.25
weight: 20
icon: fas fa-lightbulb
categories: [概念]
tags: [catalog, ext]
---

PostgreSQL 拥有极其丰富的扩展生态，但“找得到扩展”并不等于“能把它稳妥地装进生产环境”。一个可用的软件包必须同时匹配 PostgreSQL 大版本、Linux 发行版、CPU 架构与依赖组合，有时还依赖厂商自己的软件仓库。若没有现成的软件包，编译工具链与后续升级维护也都要由使用者承担。

**PIG** 是一个用 Go 编写的命令行工具，用来简化这条“软件包交付”路径。它维护 [{{< param pgext_count >}} 个已打包扩展](https://pigsty.cc/ext/list/)的目录，将扩展名解析为原生 RPM/DEB 包名，配置已知的 APT/DNF 软件仓库，再把安装工作交给操作系统包管理器。除此之外，它还提供源码构建辅助，以及 PostgreSQL、Patroni、pgBackRest、PITR、Pigsty 与 Grafana 的运维入口。

这些能力确实省事，但边界同样重要：PIG 是一个 **软件包与主机管理工具**，不是逐库管理扩展的 PostgreSQL 内部注册表，不是独立的依赖求解器，也不能替代数据库变更管理。

> 《[ANNOUNCE pig: The Postgres Extension Wizard](https://www.postgresql.org/about/news/announce-pig-the-postgres-extension-wizard-2988/)》

## PIG 实际管理什么

| 层次 | PIG 负责的事情 | 仍需使用者负责的事情 |
|:---|:---|:---|
| 扩展目录 | 检索扩展元数据，将扩展名解析为操作系统软件包 | 确认版本、许可证与功能是否适合实际负载 |
| 软件仓库 | 写入或更新 APT/DNF 仓库定义并刷新元数据 | 审批仓库信任、镜像、签名、网络策略与软件包来源 |
| 软件包 | 安装、移除或升级原生 RPM/DEB 包 | 安排维护窗口，核查依赖变化与服务影响 |
| 数据库 | 给出 `CREATE EXTENSION`、预加载等操作提示 | 执行 SQL、修改 `shared_preload_libraries`、按需重启、迁移扩展对象并逐库验证 |
| 源码构建 | 按项目构建规格在本机执行构建 | 提供兼容工具链与依赖、固定输入，并测试构建产物 |
| 运维操作 | 封装部分 PostgreSQL/Pigsty 工作流，对部分操作提供计划预览 | 负责备份、高可用策略、凭据、审批与生产验证 |

例如，安装 `pgvector` 只会把控制文件和共享库放到主机上，**不会** 自动在每个数据库中创建 `vector`。同样，`pig ext update` 只升级明确指定的操作系统软件包，不会替你执行 `ALTER EXTENSION UPDATE`。精确行为请参阅[扩展命令的职责边界](/zh/ext/#软件包层与数据库层)。

## 便利背后的具体争议

### 目录数量不等于全矩阵可用

当前目录收录 {{< param pgext_count >}} 个已打包扩展条目。这个数字是 **目录条目数**，不代表每一个扩展都在每一种 PostgreSQL、操作系统与 CPU 架构组合上有包可装。许可证限制、上游构建支持、项目停更、依赖冲突与架构特有的构建失败都会形成空缺。实际使用时，应在目标主机上执行 `pig ext avail NAME`，再通过 APT 或 DNF 核对最终候选包，不能只凭总数判断生产可用性。

### 软件包并非全部来自同一个生产者

PIG 可以使用 Pigsty、PGDG、Linux 发行版以及扩展厂商或上游仓库提供的软件包。这些来源的发布节奏、支持承诺、补丁策略与许可证并不相同。PIG 负责整理元数据并统一安装入口，但不会改变第三方软件的许可证，也不会让每一个上游包自动变成由 Pigsty 负责维护的产物。

### 配仓库很方便，但会改变系统的信任状态

`pig repo add` 是增量添加；`pig repo set` 则会备份已有定义，并按所选模块重新写入一组仓库。应先用 `pig repo info` 检查预期定义，再把替换模式用于受配置管理约束的主机。为了兼容离线仓库和镜像，PIG 内置的 Pigsty 仓库模板默认采用宽松信任设置：RPM 系统为 `gpgcheck=0`，DEB 系统为 `trusted=yes`。安全敏感环境应自行建立并强制执行签名密钥与仓库信任策略，不能把“下载成功”等同于“供应链已经验证”。

### 源码构建是退路，不是万能保证

缺少二进制包时，[`pig build`](/zh/build/) 可以在合适的构建主机上套用维护好的构建规格。但能否成功仍然取决于上游源码、编译器与语言工具链、系统库、网络输入、目标 PostgreSQL 版本及架构。构建出的包还必须在目标组合上测试；“本机编译通过”本身不构成可复现性或支持承诺。

### 自动化保证因命令而异

PIG 在受支持的工作流中提供结构化输出、确认提示与 `--plan`。但并非所有命令都具有完全一致的保证：一部分命令封装了历史工具，`pig pt` 会刻意把参数原样透传给 `patronictl`，交互式命令和第三方工具也保留自己的输出与失败语义。自动化脚本应固定 PIG 版本、检查退出状态、避免解析面向人的文本，并只在文档明确支持时使用结构化模式。

## Linux 兼容性

当前已打包仓库矩阵覆盖 **8 个 Linux 发行版大版本**，每个大版本均包含 `x86_64` 与 `aarch64`，合计 16 个“操作系统 × 架构”目标。目录面向仍在 PostgreSQL 支持窗口内的 **14-18** 五个大版本；具体扩展在具体格子中是否有包，仍以实际查询结果为准。

| OS 代码 | 发行版家族 | 版本线 | 架构 | 截至 2026 年 8 月的状态 |
|:---|:---|:---|:---|:---|
| `el8` | RHEL 兼容 | EL 8 | x86_64、aarch64 | 维护阶段；Rocky Linux 8 支持至 2029 年 |
| `el9` | RHEL 兼容 | EL 9 | x86_64、aarch64 | 支持中 |
| `el10` | RHEL 兼容 | EL 10 | x86_64、aarch64 | 支持中 |
| `d12` | Debian | Debian 12 | x86_64、aarch64 | Oldstable / LTS 阶段 |
| `d13` | Debian | Debian 13 | x86_64、aarch64 | 当前 Stable |
| `u22` | Ubuntu | Ubuntu 22.04 LTS | x86_64、aarch64 | 标准安全维护至 2027 年 5 月 |
| `u24` | Ubuntu | Ubuntu 24.04 LTS | x86_64、aarch64 | 标准安全维护至 2029 年 5 月 |
| `u26` | Ubuntu | Ubuntu 26.04 LTS | x86_64、aarch64 | 标准安全维护至 2031 年 5 月 |
{.full-width}

生命周期信息来自 [Rocky Linux 版本指南](https://wiki.rockylinux.org/rocky/version/)、[Debian 发布信息](https://www.debian.org/releases/)与 [Ubuntu 发布周期](https://ubuntu.com/about/release-cycle)。操作系统仍在厂商支持期内，并不自动意味着它属于 PIG 当前的软件包目标；二进制中保留的旧别名或识别代码，也不代表对应仓库仍在持续发布软件包。尤其需要注意：EL 7 与 Debian 11 已不在当前 16 个扩展包目标之中。

PostgreSQL 官方[版本策略](https://www.postgresql.org/support/versioning/)当前列出的受支持大版本为 14-18，其中 PostgreSQL 14 将于 2026 年 11 月停止支持。PostgreSQL 19 等预发布分支需要显式测试，不能从稳定版软件包矩阵中自行推断支持。

## 生产采用核对清单

在把 PIG 纳入生产软件供应链之前，建议逐项确认：

1. 在目标操作系统、架构与 PostgreSQL 大版本上运行 `pig status` 和 `pig ext avail NAME`。
2. 核查软件包来源、版本、许可证、依赖与仓库信任设置。
3. 明确 `repo add` 的增量语义或 `repo set` 的替换语义，是否符合现有配置归属。
4. 把主机软件包安装与数据库内的创建、预加载、重启、SQL 升级分成明确步骤。
5. 在相同目标组合上验证安装、升级、回滚、备份与恢复。
6. 固定版本；只有在具体命令明确支持时，才依赖计划预览或结构化输出。

PIG 能消除大量重复的软件包交付工作。目标环境落在其目录与仓库覆盖范围内时，它的价值最大；把软件包层、数据库层和生产验证层分开管理时，它的行为也最可预测。
