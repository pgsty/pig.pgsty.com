---
title: "pig do"
description: "使用 pig do 执行有边界的 Pigsty 管理 Playbook 任务"
weight: 155
icon: fas fa-list-check
categories: [参考]
tags: [sty, cli]
---

`pig do` 将常见 Pigsty 管理 Playbook 暴露为明确的 CLI 操作。它使用选定的 Pigsty 主目录与
Inventory，构造对应的 Playbook 命令，并通过 PIG 的旧命令结构化结果适配器返回操作结果。

这些命令会修改远程系统。执行前应检查选中的集群、节点、实例和 Inventory。
该命令族不提供通用 `--plan` 模式。

```bash
pig do pgsql-add  pg-test 10.10.10.12     # 添加一个 PostgreSQL 实例
pig do pgsql-rm   pg-test 10.10.10.12     # 移除一个 PostgreSQL 实例
pig do pgsql-db   pg-meta app             # 创建或更新数据库
pig do pgsql-user pg-meta dbuser_app      # 创建或更新用户
pig do node-pkg   pg-meta restic          # 在选中节点安装软件包
pig do redis-add  redis-meta              # 初始化 Redis 集群
```

## 命令总览

| 命令 | 用途 | 必需参数 |
|:---|:---|:---|
| `pgsql-add` | 添加 PostgreSQL 集群或实例 | 集群，可选 IP |
| `pgsql-rm` | 移除 PostgreSQL 集群或实例 | 集群，可选 IP |
| `pgsql-db` | 创建或更新数据库声明 | 集群、数据库 |
| `pgsql-user` | 创建或更新用户声明 | 集群、用户 |
| `pgsql-ext` | 通过 Pigsty 安装扩展 | 集群，可选扩展 |
| `pgsql-hba` | 刷新 PostgreSQL HBA 规则 | 集群 |
| `pgsql-svc` | 刷新 PostgreSQL 服务定义 | 集群 |
| `pgmon-add` / `pgmon-rm` | 添加或移除远程监控目标 | 集群 |
| `node-add` / `node-rm` | 添加或移除选中节点 | 一个或多个 selector |
| `node-repo` | 在选中节点配置仓库模块 | 可选 selector 与模块 |
| `node-pkg` | 在选中节点安装或更新软件包 | selector，可选软件包 |
| `repo-build` | 重建 Pigsty 基础设施仓库 | 无 |
| `redis-add` / `redis-rm` | 添加或移除 Redis 集群、节点或实例 | selector，可选端口 |
{.full-width}

使用 `pig do COMMAND --help` 查看单项操作的别名与精确示例。

## PostgreSQL 操作

```bash
pig do pgsql-add pg-meta                  # 初始化声明的集群
pig do pgsql-add pg-test 10.10.10.12      # 添加一个声明的副本
pig do pgsql-rm pg-test 10.10.10.13       # 移除一个实例
pig do pgsql-rm pg-test --uninstall       # 移除时同时卸载软件包
pig do pgsql-db pg-meta meta              # 创建或更新 meta 数据库
pig do pgsql-user pg-meta dbuser_view     # 创建或更新用户
pig do pgsql-ext pg-meta postgis vector   # 安装扩展软件包
pig do pgsql-hba pg-meta                  # 刷新 pg_hba 规则
pig do pgsql-svc pg-meta                  # 刷新 PostgreSQL 服务
```

`pgsql-rm --uninstall` 会把移除范围扩大到软件包。应将其视为独立的破坏性决策，
确认选中主机已经不再需要这些软件包。

参数明确为 PostgreSQL 集群名的命令会在运行 Ansible 前完成校验。PIG 接受
`^[A-Za-z0-9][A-Za-z0-9-]*$`：它沿用 Pigsty 的字母数字与连字符契约，并额外要求首字符为字母或数字，
防止形似选项的值进入 Ansible limit。`root` 与 Ansible 内置组 `all`、`ungrouped` 均为保留值。
`pgsql-user` 接受匹配 `^[a-z_][a-z0-9_@.-]{0,62}$` 的 Pigsty 用户名，并保留 `postgres`。
`pgsql-db` 接受以字母或下划线开头、后续仅包含字母、数字、`_`、`@`、`.`、`-` 的有界 ASCII 名称；
这样可避免 Inventory 查询与生成路径产生歧义，同时不强制数据库名使用小写。以 selector 为参数的命令仍保留更宽的 selector 语法。

## 节点与仓库操作

Selector 可以是集群名、主机名、IP 地址，或 Pigsty Playbook 支持的其它选择形式。
它的实际含义来自当前 Inventory。

```bash
pig do node-add pg-test                    # 按集群选择并添加节点
pig do node-rm 10.10.10.13                 # 移除一个选中节点
pig do node-repo pg-meta node,infra        # 配置选中的仓库模块
pig do node-pkg pg-meta openssh restic     # 安装或更新软件包
pig do repo-build                          # 重建 infra 仓库
```

仓库模块来自已安装的 Pigsty 版本，例如 `local`、`infra`、`pgsql`、`node` 与 `extra`。
安装软件包前，应确认目标节点能够访问所需仓库。

## Redis 操作

```bash
pig do redis-add redis-meta                # 初始化声明的 Redis 集群
pig do redis-add 10.10.10.11 6379 6380     # 添加选中实例
pig do redis-rm 10.10.10.11 6379           # 移除一个选中实例
pig do redis-rm redis-test --uninstall     # 移除并卸载软件包
```

与 PostgreSQL 移除相同，`redis-rm --uninstall` 会把变化范围扩大到服务移除之外。

## 配置与输出

`pig do` 使用 PIG 全局选项：

| 选项 | 用途 |
|:---|:---|
| `-H, --home` | 选择 Pigsty 主目录 |
| `-i, --inventory` | 选择 Pigsty Inventory |
| `-o, --output` | 选择文本、JSON、YAML 或格式化 JSON 包装 |
| `--log-level`、`--log-path` | 配置 PIG 诊断日志 |
{.full-width}

结构化模式报告请求的操作与捕获到的执行结果。底层 Ansible 与 Playbook 行为仍由已安装的 Pigsty 版本决定。

## 操作边界

`pig do` 是 Pigsty 管理 Playbook 的便利层，不会替代 Inventory 审阅、备份、变更窗口和变更后服务验证。
完整 Playbook 变量与生命周期语义以已安装 [Pigsty 版本文档](https://pigsty.cc/docs/)为准。
