---
title: "PIG: Packager Index Gateway"
description: "PIG is a PostgreSQL extension package manager: resolve and install PostgreSQL 14-18 and cataloged extension packages on EL, Debian, and Ubuntu with one self-contained CLI."
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

PIG is a command-line package manager for PostgreSQL and its extensions. It piggybacks on the
native `apt` and `dnf` package managers, hiding the differences between distributions, CPU
architectures, and PostgreSQL major versions behind a handful of commands.

Start with the [Getting Started](/start/) tutorial, read [why pig exists](/intro/), or jump
straight to [installation](/install/).
