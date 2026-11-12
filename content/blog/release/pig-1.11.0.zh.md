---
title: "pig v1.11.0"
linkTitle: "v1.11.0"
date: 2026-11-12
description: "对齐 Pigsty 4.6.0，支持 sty conf 有序模板简写查找，全面加固软件包与运维命令安全边界，目录更新为 625 个条目。"
tags: [cli, ext, sty, postgres]
weight: -1
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.11.0
---

PIG `v1.11.0` 对齐内嵌 Pigsty `v4.6.0`，新增 `pig sty conf` 有序模板简写查找，全面加固 `ext`、`repo`、`do`、`pg`、`pb`、`pitr`、`sty` 与 `inventory` 的软件包及运维安全边界，并将内嵌 PostgreSQL 扩展目录更新为 **625 个条目**。

## 命令与软件包安全边界 {#command-and-package-safety}

- **受保护软件包卸载边界**：[`pig ext rm`](/zh/ext/#ext-rm) 现在阻止通过扩展名或分类别名意外卸载 PostgreSQL server、共享 contrib 包及受支持的替代内核（错误码 `100102`，退出码 `2`）。独立过程语言包仍可按扩展名卸载；确需卸载 server 或内核包组时，须显式使用 `pg18-server`、`pg18-contrib`（仅 EL）或 `orioledb-server` 等包组别名。详见 [受保护软件包卸载设计](/zh/design/protected-package-removal/)。
- **APT Release 级信任协调**：[`pig repo add`](/zh/repo/#trust-and-configuration-ownership) 与 `repo set` 在写入仓库文件前按 APT URI 和 suite 协调 `trusted` 与 `signed-by` 选项，在追加模块时保留 `sty boot` 已启用的签名校验策略，并在显式配置冲突时提前拒绝。
- **Pigsty 剧本移除保护**：[`pig do pgsql-rm`](/zh/do/#postgresql-operations) 默认传递 `pg_rm_pkg=false`，仅在指定 `--uninstall` 时传递 `pg_rm_pkg=true`；`pig do pgmon-rm` 统一清理 `infra` 主机上的 `/infra/targets/pgrds/<cluster>.yml`，与 `pgmon-add` 保持一致。详见 [运维 CLI 安全契约](/zh/design/ops-cli-safety/)。
- **PostgreSQL 与恢复命令边界**：文本模式 `pig pg status` 与结构化输出保持一致的退出码，且当前用户已是目标 DBSU 时不再依赖外部 `test` 命令；`pig pg psql -f` 启用 `ON_ERROR_STOP=1` 并在切换用户前解析调用者相对路径；内部库名枚举传入 `psql -X`；`pig pg fork` 在 `postgresql.conf` 与 `postgresql.auto.conf` 中同步锁定独立的 `data_directory`、`hba_file`、`ident_file`、`port` 及归档/恢复覆盖项，并在确认重试提示中保留 `--force`；`pig pg vacuum` 与 `pig pg freeze` 在传入 `--schema` 时强制要求搭配 `--table`；`pig pg kill` 与 `pig pg tune` 拦截非法 PID、轮询间隔与浮点边界；`pig pb restore` 与 `pig pitr` 保留复合增量/差异备份标签，拒绝 `--reset-*` / `--no-*` 透传覆盖及显式空 `-D` 参数，并隐藏错误诊断中的原始选项值。
- **结构化输出与配置保真**：早期参数错误渲染支持连写的 `-ojson` 且不跨越 `--` 转发边界；原子文件写回严格保留原有权限模式而不再回退为 `0644`；旧式包装器下载期间抑制进度条污染 stdout；有上限诊断同时保留首尾上下文，而配置与 SQL 查询保持完整读取；`pig inventory cmdb dump` 保留有符号/无符号 64 位整型与浮点标量类型，并识别多主机 PostgreSQL URI 及 `sslpassword` 凭据；`pig pt status` 在解析 Patroni 配置失败时返回结构化 JSON 错误；`pig sty grafana` 拒绝不安全的仪表盘路径分量并对异常端点 URL 脱敏。
- **目录加载与安装路径**：`pig ext` 正确加载用户配置的目录来源，并在执行安装操作前校验 PostgreSQL 安装路径。

## Pigsty 4.6.0 引导与配置 {#pigsty-bootstrap-and-configuration}

- [`pig sty conf`](/zh/sty/#sty-conf) 按 Pigsty 固定顺序（`conf/`、`conf/ha/`、`conf/fork/`、`conf/app/`、`conf/demo/`、`conf/build/`）解析裸模板名，`full`、`trio`、`oss` 等简写均可继承对应模板的版本锁定与预检规则。
- `pig sty conf` 支持将显式指定或自动探测出的 `default` 区域写回原为 `china` 的模板，确保输出文件与结构化结果一致。
- [`pig sty boot`](/zh/sty/#sty-boot) 与 `pig repo boot` 自动发现离线包时优先检查 `/var/tmp/pkg.tgz`，仅在该路径不存在时回退至 `/tmp/pkg.tgz`，并在创建目标目录前拒绝不安全或不可读的自动候选归档。

## 扩展目录与软件包别名 {#catalog-and-package-aliases}

- EL 与 Debian/Ubuntu 的 `infra` 软件包组别名新增 `kes` 与 `openbao`。
- 刷新九个内嵌目录条目的版本号：
  - `login_hook`：`1.8` -> `1.9`
  - `pg_curl`：`2.4.6` -> `2.5.0`
  - `pg_improv`：`0.12.2` -> `0.14.0`
  - `pg_integrity_checksums`：`2.1.0` -> `2.2.0`
  - `pg_mentat`：`1.19.1` -> `1.20.0`
  - `pg_search`：`0.26.5` -> `0.26.6`
  - `pg_tokenizer`：`1.0.0` -> `1.1.0`
  - `vchord`：`1.2.0` -> `1.3.0`
  - `vchord_bm25`：`1.0.0` -> `1.1.0`
- 移除已退役的 `documentdb_distributed` 目录记录，清理 `citus`、`documentdb` 与 `documentdb_core` 中残留的 `require_by` 引用，并将 `columnar` 状态恢复为 `available`。

## 目录口径与构建版本 {#catalog-count-and-build-versions}

内嵌目录包含 **625 条记录**（全部 **625 条** 均为 `available` 状态，保留已移除记录为 **0 条**）。包含 PostgreSQL contrib 模块时，共对应 **518 个不同包名**；非 contrib 包系列共 **457 个**。详见 [目录条目计数口径](/zh/ext/#catalog-count)。

PIG `v1.11.0` 使用 Go `1.27.4` 构建，内嵌 Pigsty `4.6.0`，默认 `cargo-pgrx` 为 `0.19.3`。升级 PIG 请参阅 [安装文档](/zh/install/)。

## 升级 {#upgrade}

使用已安装的 PIG 升级到本版本：

```bash
pig update -v 1.11.0
pig version
```

首次安装及各平台说明见[安装文档](/zh/install/)。

## 校验和 {#checksums}

```checksums
c3c24b64dce312a13fe1b3bcb15d38101095dfd2569ed88186838a33291abcac  pig-1.11.0-1.aarch64.rpm
2c0d05aba718957f4654cb135771610f042b6f71b7902a792b598744632736b9  pig-1.11.0-1.x86_64.rpm
d9c0b9b3bde4e5e53d64a0df177dcda48575eed0310178adaff11f6d33a76cd9  pig-v1.11.0.darwin-amd64.tar.gz
474788f79563e99e7443e619bb7e594f598284c9a81f22d53f33bacf03c5da27  pig-v1.11.0.darwin-arm64.tar.gz
8f21efdd33d5a063eb7e12d2908912682af4dd94e336d82124ab9eb57808974c  pig-v1.11.0.linux-amd64.tar.gz
4c2699618fb50d6bb5d2c0807e407442c69c9873a4d33dc3193bbab9c039bdcd  pig-v1.11.0.linux-arm64.tar.gz
4bf90bbd4bc179391b5d88f2d51cb2d08b165212305434f59d12dcab0dc7ea5a  pig_1.11.0-1_amd64.deb
ba4fb6cd9927712fe6ac7af237a7f96076febd972cb99c121ebf620a08664979  pig_1.11.0-1_arm64.deb
```

{{< release-card >}}
