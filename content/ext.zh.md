---
title: "pig ext"
description: "使用 pig ext 检索扩展目录并管理 PostgreSQL 扩展软件包"
weight: 120
icon: fas fa-puzzle-piece
categories: [参考]
tags: [ext, catalog]
---

`pig ext` 用于检索扩展目录并管理主机上的 PostgreSQL 扩展 **软件包**。它可以解析名称、查询软件包可用性，安装、移除、升级 RPM/DEB 包，也能处理 PostgreSQL 内核包；数据库内部的启用与迁移不属于这一命令组的职责。

```bash
pig ext - Manage PostgreSQL Extensions

  pig repo add -ru             # add all repo and update cache (brute but effective)
  pig ext add pg18             # install optional postgresql 18 package
  pig ext list duck            # search extension in catalog
  pig ext scan -v 18           # scan installed extension for pg 18
  pig ext add pg_duckdb        # install certain postgresql extension

Examples:
  pig ext list    [query]      # list & search extension
  pig ext info    [ext...]     # get information of a specific extension
  pig ext status  [-v]         # show installed extension and pg status
  pig ext add     [ext...]     # install extension for current pg version
  pig ext rm      [ext...]     # remove extension for current pg version
  pig ext update  [ext...]     # update extension to the latest version
  pig ext import  [ext...]     # download extension to local repo
  pig ext link    [ext...]     # link postgres installation to path
  pig ext reload               # reload the latest extension catalog data
```

| 命令           | 描述             | 备注                |
|:-------------|:---------------|:------------------|
| `ext list`   | 搜索扩展           |                   |
| `ext info`   | 显示扩展详细信息       |                   |
| `ext avail`  | 显示扩展可用性矩阵      |                   |
| `ext status` | 显示主机可见的扩展文件/软件包 | 不会逐库查询            |
| `ext scan`   | 扫描已安装的控制文件/共享库  | 不会逐库查询            |
| `ext add`    | 安装扩展           | 需要 sudo 或 root 权限 |
| `ext rm`     | 移除扩展           | 需要 sudo 或 root 权限 |
| `ext update` | 更新扩展           | 需要 sudo 或 root 权限 |
| `ext import` | 下载扩展以供离线使用     | 需要 sudo 或 root 权限 |
| `ext link`   | 链接 PG 版本到 PATH | 需要 sudo 或 root 权限 |
| `ext reload` | 刷新扩展目录         |                   |
{.full-width}

## 快速入门

在安装 PostgreSQL 扩展前，你需要先添加 [`pig repo add`](/zh/repo/)：

```bash
pig repo add pgdg pigsty -u    # 温和方式添加 pgdg 和 pigsty 仓库
pig repo set                   # 粗暴方式移除并添加所有所需仓库
```

然后你可以搜索并安装 PostgreSQL 扩展：

```bash
pig ext install pg_duckdb
pig ext install pg_partman
pig ext install pg_cron
pig ext install pg_repack
pig ext install pg_stat_statements
pig ext install pg_stat_kcache
```

可用扩展及其名称请查阅 [**扩展列表**](https://pigsty.cc/ext/list/)。

**使用说明：**

1. 未指定 PostgreSQL 版本时，工具会尝试从 `PATH` 中的 `pg_config` 自动检测当前活动的 PostgreSQL 安装。
2. PostgreSQL 可通过主版本号（`-v`）或 pg_config 路径（`-p`）指定。
   - 若指定 `-v`，pig 会使用该版本 PGDG 内核包的默认路径。
     - EL 发行版为 `/usr/pgsql-$v/bin/pg_config`，
     - DEB 发行版为 `/usr/lib/postgresql/$v/bin/pg_config` 等。
   - 若指定 `-p`，则直接用该路径定位 PostgreSQL。
3. 扩展管理器会根据操作系统自动适配不同的包格式：
   - RHEL/CentOS/Rocky Linux/AlmaLinux 使用 RPM 包
   - Debian/Ubuntu 使用 DEB 包
4. 某些扩展可能有依赖项，安装时会自动解决。
5. 谨慎使用 `-y` 参数，它会自动确认所有提示。

Pigsty 假定你已安装官方 PGDG 内核包，如未安装，可用如下命令：

```bash
pig ext install pg18          # 安装 PostgreSQL 18 内核（除 devel 包）
```

## 软件包层与数据库层

PIG 的主要作用范围是操作系统软件包层。明确这条边界，可以避免几种常见而危险的误解：

| 命令 | 实际改变的内容 | **不会** 做的事情 |
|:---|:---|:---|
| `ext add` | 安装所选 RPM/DEB 包及其软件包依赖 | 执行 `CREATE EXTENSION`、修改 PostgreSQL 参数或重启 PostgreSQL |
| `ext rm` | 移除所选 RPM/DEB 包 | 执行 `DROP EXTENSION`，或逐库检查是否仍依赖这些文件 |
| `ext update` | 升级显式指定的操作系统软件包 | 执行 `ALTER EXTENSION UPDATE`，或迁移扩展拥有的数据库对象 |
| `ext status` / `ext scan` | 检查所选 PostgreSQL 安装树与主机可见文件 | 证明扩展已在每个数据库中创建、运行正常，或 SQL 版本已经一致 |
| `ext reload` | 将新版目录下载到 `~/.pig/extension.csv` | 安装或升级任何软件包、数据库扩展 |

完成软件包事务后，应先用 `pig ext info NAME` 查看预加载与 DDL 提示，再对每个目标数据库应用配置与 SQL；扩展有要求时还需重载或重启 PostgreSQL。最后应核对 `pg_available_extensions`、`pg_extension` 及扩展自己的升级文档。移除软件包前必须先做数据库依赖审计；若数据库对象仍存在就删除共享文件，相关数据库可能无法正常使用。

## ext list

列出（或搜索）扩展目录中的可用扩展。

```bash
pig ext list                     # 列出所有扩展
pig ext list duck                # 搜索包含 "duck" 的扩展
pig ext list -v 18               # 按 PG 版本筛选
pig ext ls olap                  # 列出 olap 类别扩展
pig ext ls gis -v 16             # 列出 PG 16 的 GIS 类扩展
pig ext ls rag                   # 列出 RAG 类别扩展
```

分类筛选通过查询参数直接指定分类名实现，支持的分类包括：`time`, `gis`, `rag`, `fts`, `olap`, `feat`, `lang`, `type`, `func`, `util`, `admin`, `stat`, `sec`, `fdw`, `sim`, `etl`。

**选项：**

- `-v|--version`：按 PG 版本筛选
- `--pkg`：显示包名而非扩展名，仅列出主导扩展

**Status 列说明：**

- `installed`：扩展已安装（绿色）
- `available`：扩展可用但未安装（黄色）
- `not avail`：扩展在当前系统不可用（红色）

默认扩展目录定义在 [**`cli/ext/assets/extension.csv`**](https://github.com/pgsty/pig/blob/main/cli/ext/assets/extension.csv)。

可用 `pig ext reload` 命令更新到最新扩展目录，数据将下载到 `~/.pig/extension.csv`；在线最新版目录同步发布于 [**repo.pigsty.cc/ext/data/extension.csv**](https://repo.pigsty.cc/ext/data/extension.csv)。

## ext info

显示指定扩展的详细信息。

```bash
pig ext info postgis        # 显示 PostGIS 详细信息
pig ext info timescaledb    # 显示 TimescaleDB 信息
pig ext info vector postgis # 显示多个扩展信息
```

## ext avail

显示扩展的可用性矩阵，展示扩展在不同操作系统、架构和 PostgreSQL 版本上的可用情况。

```bash
pig ext avail                     # 显示当前系统上所有包的可用性
pig ext avail timescaledb         # 显示 timescaledb 的可用性矩阵
pig ext avail postgis pg_duckdb   # 显示多个扩展的可用性
pig ext av pgvector               # 显示 pgvector 的可用性
pig ext matrix citus              # avail 命令的别名
```

可用性矩阵会显示扩展在各个操作系统（EL8/9/10, Debian 12/13, Ubuntu 22/24/26）、架构（x86_64/aarch64）和 PostgreSQL 版本（14-18）上的可用情况。

## ext status

显示所选 PostgreSQL 安装在当前主机上可见的扩展文件/软件包状态。

```bash
pig ext status              # 显示已安装扩展
pig ext status -c           # 包含 contrib 扩展
pig ext status -v 16        # 显示 PG 16 已安装扩展
```

**选项：**

- `-c|--contrib`：结果中包含 contrib 扩展

## ext scan

扫描所选 PostgreSQL 安装的扩展目录。

```bash
pig ext scan [-v version]
```

该命令扫描 PostgreSQL 控制文件及相关安装路径，反映的是主机层可用性；它不会连接所有数据库，也不会检查各数据库的 `pg_extension` 目录。

## ext add

安装一个或多个 PostgreSQL 扩展。`pig ext add` 的同级别名包括 `pig ext install`、`pig ext ins` 与 `pig ext a`。顶层 [`pig install`](/zh/cmd/#pig-install) 是另一个原生包管理器包装命令，也支持 PostgreSQL 与扩展包 alias 翻译。

```bash
pig ext add pg_duckdb            # 安装 pg_duckdb
pig ext add pg_duckdb -v 18      # 为 PG 18 安装
pig ext add pg_duckdb -y         # 自动确认安装
pig ext add vector postgis       # 安装多个扩展
pig ext add postgis --plan       # 预览安装计划，不执行

# 使用别名
pig install pg_duckdb
pig install pg_duckdb -v 18 -y

# 安装 PostgreSQL 内核
pig ext install pgsql            # 安装最新版 postgresql 内核
pig ext a pg18                   # 安装 postgresql 18 内核包
pig ext ins pg16                 # 安装 postgresql 16 内核包
pig ext install pg15-core        # 安装 postgresql 15 核心包
pig ext install pg14-main -y     # 安装 pg 14 + 常用扩展（vector, repack, wal2json）
```

**选项：**

- `-v|--version`：指定 PG 大版本
- `-y|--yes`：自动确认安装
- `--plan`：预览安装计划，不执行包管理器命令

软件包安装成功，只代表主机上已有扩展文件。请按照 `ext info` 给出的提示完成预加载、重启与 `CREATE EXTENSION`。

## ext rm

移除一个或多个 PostgreSQL 扩展。

```bash
pig ext rm pg_duckdb             # 移除 pg_duckdb
pig ext rm pg_duckdb -v 18       # 移除 PG 18 版本
pig ext rm pgvector -y           # 自动确认移除
pig ext rm pgvector --plan       # 预览移除计划，不执行
```

**选项：**

- `-v|--version`：指定 PG 大版本
- `-y|--yes`：自动确认移除
- `--plan`：预览移除计划，不执行包管理器命令

该命令移除的是操作系统软件包，而不是数据库对象。删除共享文件前，应先在所有受影响数据库中移除或迁移依赖它的扩展。

## ext update

将指定的已安装扩展更新到最新版。出于安全考虑，无参数 `pig ext update` 不会更新所有扩展，而是 no-op；必须显式写出要更新的目标。

```bash
pig ext update                   # no-op：必须显式指定目标
pig ext update pg_duckdb         # 更新特定扩展
pig ext update postgis timescaledb  # 更新多个扩展
pig ext update pg_duckdb -y      # 自动确认更新
pig ext update pg_duckdb -m      # 选择内置中国区域软件源
```

**选项：**

- `-v|--version`：指定 PG 大版本
- `-y|--yes`：自动确认更新
- `-m|--mirror`：优先使用 `pigsty.cc` 镜像作为更新来源

该命令不会执行 SQL 迁移。软件包升级完成后，请按扩展发布说明，在每个适用数据库中执行 `ALTER EXTENSION ... UPDATE`。

## ext import

下载扩展包到本地仓库，便于离线安装。

```bash
pig ext import postgis                # 导入 PostGIS 包
pig ext import timescaledb pg_cron    # 导入多个扩展包
pig ext import pg16                   # 导入 PostgreSQL 16 包
pig ext import pgsql-common           # 导入常用工具包
pig ext import -d /www/pigsty postgis # 指定路径导入
```

**选项：**

- `-d|--repo`：指定仓库目录（默认：`/www/pigsty`）

## ext link

将指定 PG 版本链接到系统 PATH。

```bash
pig ext link 18                  # 链接 PG 18 到 PATH
pig ext link pg17                # pg 前缀会被剥离，链接 PG 17
pig ext link 16                  # 链接 PG 16 到 /usr/pgsql
pig ext link /usr/pgsql-16       # 从指定路径链接到 /usr/pgsql
pig ext link polar               # 链接 PolarDB / PolarPG 安装
pig ext link /usr/polar-17       # 从指定 PolarDB 路径链接
pig ext link null                # 取消当前 PostgreSQL 链接
pig ext link none                # null / none / nil / nop / no 均可取消链接
```

该命令会创建 `/usr/pgsql` 软链接，并写入 `/etc/profile.d/pgsql.sh`。

## ext reload

刷新扩展元数据。

```bash
pig ext reload                   # 刷新扩展目录
```

更新后的文件会放置于 `~/.pig/extension.csv` 中。
