---
title: "PIG：Packager Index Gateway"
description: "PIG 是 PostgreSQL 扩展包管理器：通过一个自包含 CLI，在 EL、Debian 与 Ubuntu 上解析并安装 PostgreSQL 14-18 及目录中的扩展包。"
weight: 1
type: home
cascade:
  # 只把 type: docs 洒到普通页与栏目上。分类法（tags / categories / authors）
  # 的列表页与词条页也是 home 的后代，如果一起被染成 docs，就会落到
  # OINK 的 docs/list.html，丢掉 term 页自己的标题与博客行样式。
  - target:
      kind: '{page,section}'
    type: docs
body_class: landing-page
---

PIG 是 PostgreSQL 与其扩展的命令行包管理器。它依托（PiggyBack）系统原生的 `apt` / `dnf`
包管理器，把操作系统发行版、芯片架构、PG 大版本之间的差异，收敛到几条命令背后。

可以先看 [快速上手](/zh/start/)，了解 [为什么需要 pig](/zh/intro/)，或者直接 [安装](/zh/install/)。
