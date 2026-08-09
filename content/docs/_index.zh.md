---
title: "PIG 文档"
linkTitle: "文档"
description: "使用 pig 命令行工具安装、管理、构建 PostgreSQL 与其扩展。"
weight: 1
type: docs
icon: fa-solid fa-book
# 根下拉已经把「文档」列为当前文档集，树里不必再出现一次。
toc_root: true
---

—— **Packager Index Gateway，PostgreSQL 扩展包管理器**

PIG 是一个自包含的 Go 命令行工具，用于安装、管理、构建 PostgreSQL 扩展软件包，并提供部分 PostgreSQL/Pigsty 运维能力；实际的软件包事务仍由操作系统原生工具完成。
PIG 包管理器并非重新发明的土鳖轮子，而是 **依托** （PiggyBack）现有 Linux 发行版包管理器 （`apt`/`dnf`）的一个高级抽象层。
它通过目录把操作系统、CPU 架构与 PostgreSQL 大版本映射为原生软件包名，让您用统一 CLI 安装 PG 内核、查询 {{< param pgext_count >}} 个已打包扩展条目；具体目标组合是否有包，仍以可用矩阵为准。

许多 PIG 原生工作流适合自动化：只有在具体命令文档明确支持时，才使用结构化输出、`--plan`、确认控制与结果码。透传、交互式和流式命令仍保留上游工具或终端自身的行为。

请注意：对于扩展安装来说，**pig 并非必须组件**，您依然可以使用 apt / dnf 等包管理器直接访问 [**Pigsty PGSQL**](https://pigsty.cc/docs/repo/pgsql/) 仓库。

- [**简介**](/zh/intro/)：为什么需要专用的 PG 包管理器？
- [**上手**](/zh/start/)：快速上手与样例
- [**安装**](/zh/install/)：下载、安装、更新 pig

## 快速上手

使用以下命令即可在您的系统上 [**安装**](/zh/install/) PIG 包管理器：

**默认安装**（Cloudflare CDN）：

```bash
curl -fsSL https://repo.pigsty.io/pig | bash
```

**中国镜像**：

```bash
curl -fsSL https://repo.pigsty.cc/pig | bash
```

安装完成后，几行命令即可 [**快速开始**](/zh/start/)。例如，若需安装 PG 18 与相应的 [**`pg_duckdb`**](https://pigsty.cc/ext/e/pg_duckdb) 扩展：

```bash
$ pig repo set                        # 一次性设置好 Linux, Pigsty + PGDG 仓库（覆盖式！）
$ pig install pg18                    # 安装 PostgreSQL 18 内核（原生 PGDG 包）
$ pig install pg_duckdb -v 18         # 安装 pg_duckdb 扩展（针对当前 pg 18）
$ pig install -y postgis timescaledb  # 针对当前活跃PG版本，安装多个扩展
$ pig install -y vector               # 您可以使用扩展名称（vector）或者扩展包名称（pgvector）来安装扩展！
```

这些命令安装的是主机软件包。请用 `pig ext info NAME` 配合扩展自身文档，在每个目标数据库中完成预加载、重启、`CREATE EXTENSION` 与 SQL 升级步骤。

## 命令参考

你可以执行 `pig help <command>` 获取子命令的详细帮助。

**扩展管理**：

- [**pig repo**](/zh/repo/)：管理 APT/YUM 软件仓库
- [**pig ext**](/zh/ext/)：管理 PostgreSQL 扩展
- [**pig build**](/zh/build/)：从源码构建扩展
- [**pig install**](/zh/cmd/#pig-install)：通过原生包管理器安装 PostgreSQL 与扩展包

**Pigsty 管理**：

- [**pig sty**](/zh/sty/)：管理 Pigsty 安装与 Grafana 仪表盘
- [**pig inventory**](/zh/inventory/)：检视、编辑、校验与交换 Pigsty 配置清单
- [**pig context**](/zh/cmd/#pig-context)：采集主机、PostgreSQL、Patroni、pgBackRest 与扩展上下文
- [**pig pg**](/zh/pg/)：管理本地 PostgreSQL 服务
- [**pig pt**](/zh/pt/)：透明运行 patronictl 管理 Patroni HA 集群
- [**pig pb**](/zh/pb/)：管理 pgBackRest 备份
- [**pig pitr**](/zh/pitr/)：时间点恢复工作流

## 关于

`pig` 命令行工具由 [Vonng](https://vonng.com/en/)（冯若航 rh@vonng.com）开发，并以 [Apache 2.0](https://github.com/pgsty/pig/blob/main/LICENSE) 许可证开源。

您还可以参考 [**PIGSTY**](https://pgsty.com) 项目，提供了包括扩展交付在内的完整 PostgreSQL RDS DBaaS 使用体验。

- [**PGEXT**](https://github.com/pgsty/pgext)：扩展数据与管理工具
- [**PIG**](https://github.com/pgsty/pig)：PostgreSQL 包管理器
- [**PIGSTY**](https://github.com/pgsty/pigsty)：开箱即用的 PostgreSQL 发行版
