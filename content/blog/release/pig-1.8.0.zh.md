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
**575 个已打包 PostgreSQL 扩展**作为统一发布口径，内置 Pigsty `4.5.0`。

## 原生 `pig sty boot`

- 端到端引导控制节点：按需修复 Debian 12/13 locale，校验 Ansible 及其 Python
  依赖，安装控制节点软件包，尽力修复本机免密 SSH，并可初始化缺失的 `~/pigsty`。
- 支持在线仓库、显式本地软件包或 HTTP(S) URL、可信的自动发现离线包，以及已经
  准备好的 `/www/pigsty` 软件仓库。
- 替换仓库定义前自动备份，软件包准备失败时自动恢复。显式离线输入错误会直接失败，
  可选的收尾便利步骤则以告警呈现。JSON/YAML 输出会报告工作模式、仓库策略、回滚状态、
  告警与后续建议命令。

## 原生 `pig sty conf`

- 从 `<PIGSTY_HOME>/conf` 下的安全模板生成 Inventory，同时支持
  `pig sty conf MODE` 与 `--conf MODE`，可按顺序映射最多十个 IPv4 地址，并替换
  精确的 `i.pigsty` 占位域名。
- 提供确定性的交互与非交互 IP 选择，结构化处理代理、区域、PostgreSQL 版本与随机
  口令变更，最后对完整 Inventory 执行校验。
- 拒绝通过直接路径、符号链接、带符号链接的父目录或硬链接让输出指回源模板。
  校验通过后以 `0600` 权限原子写入；结构化输出只报告生成的机密标识符，不泄露其值。

## 其他更新

- EL8 及以上软件包操作统一优先使用 DNF；本地 RPM 依赖按提供能力解析；新建软件仓库时
  恢复预期的 `/www -> /data/nginx` 布局；自更新可容忍 latest 标记中的空白字符。
- 例行刷新扩展目录、软件包版本、元数据与可用性矩阵，发布的 PostgreSQL 扩展数量保持
  **575**。
- CI 与发布构建使用 Go `1.26.6`、固定版本的分析工具与 GoReleaser，并执行依赖校验、
  工作流检查、漏洞扫描与完整发布快照构建。

## 兼容性提醒

- `pig sty boot` 不再执行 `<PIGSTY_HOME>/bootstrap`；依赖 Shell 脚本副作用的自动化应改为
  使用原生命令结果。
- `pig sty conf --raw` 已移除。请直接使用原生工作流；`--conf MODE` 仍然可用，等价的位置
  参数形式为 `pig sty conf MODE`。
- `pig sty conf --ip` 可接受最多十个逗号分隔的 IPv4 地址；`--skip` 与 `--ip` 仍互斥。
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
