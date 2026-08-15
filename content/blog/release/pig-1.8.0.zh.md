---
title: "pig v1.8.0"
linkTitle: "v1.8.0"
date: 2026-08-14
author: "冯若航"
description: "原生 pig sty boot 与 pig sty conf 工作流，以及 575 个已打包 PostgreSQL 扩展。"
categories: [release]
tags: [Release, pig]
weight: 1
---

Pig `v1.8.0` 将 Pigsty 控制节点的准备过程原生化。两条核心安装命令
`pig sty boot` 与 `pig sty conf` 现在是具备完整失败处理能力的 Go 工作流，
不再包装旧版 `bootstrap` 与 `configure` Shell 脚本。本版本继续以
**575 个已打包 PostgreSQL 扩展** 作为统一发布口径，内置 Pigsty `4.5.0`。

## 原生 `pig sty boot`

`pig sty boot` 现在是一套具备事务语义与完整失败处理的原生控制节点引导流程。它不再执行
`<PIGSTY_HOME>/bootstrap`，HTTP 下载与归档解压也不依赖 `curl`、`wget`、`tar` 或 `gzip`。

### 权限与就绪检查

- 普通用户可以直接发起命令。Pig 会在一次 sudo 自重启前解析并下载显式来源；
  `PIG_NO_SUDO=1` 可禁用提权，`PIG_NON_INTERACTIVE=1` 可要求非交互 sudo。
- Debian 12/13 会在安装控制节点软件包前检查 locale，并在新软件包可能补齐工具后按需重试。
- 就绪判定会实际执行 `ansible-playbook`，发现其 Python 解释器，并检查 `yaml`、`jmespath`，
  以及 `cryptography` 或 `OpenSSL` 两者之一；只有二进制文件但无法运行的 Ansible 不再产生假成功。

### 仓库来源与事务

- 来源覆盖本地归档、HTTP(S) URL、经过权限检查的自动 `/tmp/pkg.tgz`、已经提交的
  `/www/pigsty` 仓库，以及区域在线仓库。显式来源无效时直接失败，不会悄悄转为在线引导。
- 已完成的 `/www/pigsty` 优先于选中的离线包。Pig 可以自行建立预期的
  `/www -> /data/nginx` 布局，以受限解压提交离线内容，并在离线模式下只启用严格的
  `pigsty-local` 仓库；在线模式会安装内嵌的 Pigsty 密钥，并保持仓库签名校验开启。
- 默认覆盖策略会备份仓库定义，仓库或软件包准备失败时自动恢复；`--keep` 使用增量策略，
  在线刷新失败时可以利用现有定义重试。
- 结果会明确标记 `ready`、`offline`、`online` 或 `existing` 模式。即使 Ansible 已经可用，
  显式、自动发现或已提交的离线来源仍会被准备。

### 收尾检查与自动化

- Pig 会探测控制节点辅助工具，为发起调用的管理员用户修复到 `127.0.0.1` 的密钥 SSH，
  并尽可能从在线或本地内容初始化缺失的 `~/pigsty`。
- locale、辅助工具、本机 SSH 与 Pigsty 目录初始化失败属于告警；显式输入无效、仓库或软件包
  操作失败、安装路径不受支持，以及安装后 Ansible 仍不可用，仍然是硬错误。
- JSON/YAML 使用 `pig.sty.boot/v2` 结果契约，包含模式与软件包管理器、仓库策略与回滚状态、
  来源路径、locale、SSH 与初始化状态、变更、告警，以及后续 `conf`、`inventory` 与
  `deploy` 命令。

## 原生 `pig sty conf`

`pig sty conf` 现在是一套完整的原生 Inventory 编译流程。它不执行 `./configure`，也不会
回退到原始 Shell 行为：Pig 解析一个模板、执行有边界的结构化变更、校验完整候选，最后才提交
输出文件。

### 安全配置流水线

- 默认模板为 `conf/meta.yml`；安全的斜杠分隔相对模式既可作为位置参数，也可通过 `--conf`
  指定。绝对路径、目录穿越、路径逃逸，以及通过直接路径、符号链接、带符号链接父目录或硬链接
  造成的源/输出别名都会被拒绝。
- 源模板解析与 IP 冲突检查先于外部预检；解析、变更、预检或校验失败都不会改动目标文件。
- Pig 执行原生 Inventory 校验，并在 `ansible-inventory` 可用时进行一次有时间边界的外部
  解析；成功结果以 `0600` 权限原子写入。

### Inventory 结构化变更

- 最多十个互不相同的 `--ip` 地址会同时映射到 `10.10.10.10` 至 `10.10.10.19`，VIP 等
  无关地址保持不变。未指定 `--ip` 时，交互、非交互与输入关闭场景都有明确且确定的选择行为。
- `--domain` 只替换精确的 `i.pigsty`；CPU 少于四核的控制节点会自动从 `oltp` 节点与
  PostgreSQL 调优配置切换为 `tiny`。
- 区域变更会更新 `all.vars.region`；`china` 会启用模板中已有的 Docker 与 pip 镜像。
  `--proxy` 将可用的代理环境变量写入 `all.vars.proxy_env`。
- 通用模板支持 PostgreSQL 14-18 与显式指定的 19 beta，包括匹配的 locale 与 beta 仓库；
  固定版本的 `mssql`、`polar` 与 `pgNN` 模式保留模板实际版本并产生告警。
- `--generate` 为每个已知凭据标识符分配一个 24 位随机值，并一致更新生效值与文档占位符；
  结果只列出生成的标识符，绝不输出机密值。

### 预检与结果契约

- 未指定 `--skip` 时，预检覆盖平台、软件包管理器、控制节点资源、sudo/管理员权限、本机 SSH
  与 Ansible 可用性；`conf/build/` 下的构建模板有意绕过 IP 映射与管理员预检。
- JSON/YAML 使用 `pig.sty.configure/v1`，报告模板与输出、已选择和丢弃的地址、请求与实际
  PostgreSQL 版本、已应用选项、生成的机密标识符及告警。

## 其他更新

- EL8 及以上软件包操作统一优先使用 DNF；本地 RPM 依赖按提供能力解析；新建软件仓库时恢复
  预期的 `/www` 布局；自更新可容忍 latest 标记中的空白字符。
- 例行刷新扩展目录、软件包版本、元数据与可用性矩阵，发布的 PostgreSQL 扩展数量保持
  **575**。
- CI 与发布构建使用 Go `1.26.6`、固定版本的分析工具与 GoReleaser，并执行依赖校验、
  工作流检查、漏洞扫描与完整发布快照构建。

## 兼容性提醒

- `pig sty boot` 不再执行 `<PIGSTY_HOME>/bootstrap`；依赖 Shell 脚本副作用的自动化应改为
  使用原生命令及其结构化结果。
- `pig sty conf --raw` 已移除。请使用原生工作流；`--conf MODE` 仍然可用，等价的位置参数
  形式为 `pig sty conf MODE`。
- `pig sty conf --ip` 可接受最多十个逗号分隔的 IPv4 地址；`--skip` 与 `--ip` 仍互斥。
  大写 `-O` 选择 Inventory 文件，全局小写 `-o` 选择命令输出格式。
- EL8 及以上使用 DNF；有限的 EL7 兼容目录继续保留独立的传统 YUM 路径。

## 校验和

制品：[GitHub Release](https://github.com/pgsty/pig/releases/tag/v1.8.0) · [checksums.txt](https://github.com/pgsty/pig/releases/download/v1.8.0/checksums.txt)

```bash
02fd2628810c1b00de730ece32b09dba1318be4c99a4ff1a0551740e32bf223b  pig-1.8.0-1.aarch64.rpm
72ba72a00af52a84b08b1346f85b42668b52bc097e315774ff9f501ca23ece8b  pig-1.8.0-1.x86_64.rpm
f023a5c9049dc532a057e932c73a8197683eaf4d97cb7a8f219492da1ad2a65f  pig-v1.8.0.darwin-amd64.tar.gz
e0ccf61c4d135dbc45359c207751092aeb6df788e826bb73eccc1a1ed8800998  pig-v1.8.0.darwin-arm64.tar.gz
a24a08c1b8d54adcdef5a99ed7b91caeedef1552a1440b1258eb4eb07fb20353  pig-v1.8.0.linux-amd64.tar.gz
9d23875804f87e78039498245059fd6b765831f027aacfc511ad0ac42711fa7b  pig-v1.8.0.linux-arm64.tar.gz
96259ff7584cd52254c91a9fd7d77bd577f23c55cb09f4bc995a3ca0fcbc7321  pig_1.8.0-1_amd64.deb
2e7370211514df6355ef96fb812670febe6ee1b85a28378432c33ebdaecb4b63  pig_1.8.0-1_arm64.deb
```

发布：https://github.com/pgsty/pig/releases/tag/v1.8.0
