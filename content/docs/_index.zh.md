---
title: "PIG 文档"
linkTitle: "文档"
description: "使用 pig 命令行工具安装、管理、构建 PostgreSQL 与其扩展。"
search_keywords: [pig, PostgreSQL, 扩展, 包管理器, 命令行]
search_boost: 1.5
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

按 {{< kbd "Ctrl" "K" >}}（macOS 为 {{< kbd "⌘" "K" >}}）打开搜索与页面操作，或按 {{< kbd "/" >}} 直接进入命令模式。

AI 助手操作只会在您主动选择后打开 ChatGPT 或 Claude；届时会把当前页面的公开 URL 与阅读提示交给对应的第三方服务，PIG 不会自动发送页面正文。

- [**简介**](/zh/intro/)：为什么需要专用的 PG 包管理器？
- [**上手**](/zh/start/)：快速上手与样例
- [**安装**](/zh/install/)：下载、安装、更新 pig

## 快速上手

{{% steps %}}

### 安装 pig

使用默认的 Cloudflare 加速安装入口：

```bash
curl -fsSL https://repo.pigsty.io/pig | bash
```

中国大陆可改用镜像入口：

```bash
curl -fsSL https://repo.pigsty.cc/pig | bash
```

软件包、发布压缩包、升级与卸载方式详见 [安装](/zh/install/)。

### 配置软件仓库

在 Linux 上一次性注册 Pigsty 与 PGDG 仓库；该命令会覆盖对应配置，请先检查生成结果：

```bash
pig repo set
```

### 安装 PostgreSQL 与扩展

安装 PostgreSQL 18 内核，以及 [`pg_duckdb`](https://pigsty.cc/ext/e/pg_duckdb) 与 `vector` 扩展软件包：

```bash
pig install -y pg18 pg_duckdb vector
```

{{% /steps %}}

这些命令安装的是主机软件包。请用 `pig ext info NAME` 配合各扩展文档，在每个目标数据库中完成预加载、重启、`CREATE EXTENSION` 与 SQL 升级步骤。目录查询、别名解析与安装后检查详见完整的 [上手教程](/zh/start/)。

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
