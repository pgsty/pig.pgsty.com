---
title: "PIG：PostgreSQL 包管理器"
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

PIG 是 PostgreSQL 与其扩展的命令行包管理器。它根据操作系统、CPU 架构和 PostgreSQL 大版本选择对应的软件包，再用 `apt` 或 `dnf` 安装。

可以先看 [快速上手](/zh/start/)，了解 [为什么需要 pig](/zh/intro/)，或者直接 [安装](/zh/install/)。
