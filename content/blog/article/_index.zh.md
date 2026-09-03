---
title: 文章
linkTitle: 文章
description: 关于 PIG、PostgreSQL 扩展交付、Linux 打包与软件仓库供应链的长文。
weight: 10
icon: fa-solid fa-newspaper
sidebar_expanded: true
module: [BLOG]
blog_index: list
sidebar_enabled: true
breadcrumb: true
toc_taxonomies: true
toc_style: fixed
featured_image: none
cascade:
  featured_image: hero
  toc_style: flow
  toc_taxonomies: false
  sidebar_enabled: false
  breadcrumb: false
---

这里收录 PIG 所要解决的问题：怎样发现 PostgreSQL 扩展，怎样把它们构建成原生
RPM/DEB 软件包，怎样发布可信的软件仓库，以及怎样通过实用的命令行工具把这些能力交给用户。

文章保留原始发表日期、当时的软件包数量、截图与上下文。当前行为请以 [PIG 文档](/zh/docs/)、
实时[扩展目录](https://pigsty.cc/ext/)与[发布注记](/zh/release/)为准。

建议按以下线索阅读：

- **PIG 与猪猪家族：** [认识 PIG](/zh/article/pig/)、[瞬间克隆 PostgreSQL](/zh/article/pg-pig-clone/)，以及 [SOW 的仓库状态模型](/zh/article/sow/)。
- **扩展交付：** [最初的扩展仓库思考](/zh/article/pg-ext-repo/)、[PG 扩展云](/zh/article/pgext-cloud/)、[扩展百科全书](/zh/article/pgext-pedia/)，以及[人人可用的 PG 扩展](/zh/article/extensions-for-everyone/)。
- **打包与信任：** [为什么 Linux 打包如此稀缺](/zh/article/packaging-skill/)、[PGDG 镜像事件](/zh/article/pg-mirror-break/)、[Pigsty 的回应](/zh/article/pg-mirror-pigsty/)，以及 [Valkey 打包 Bug 的教训](/zh/article/valkey-bug/)。
- **发行版这一层：** [打造面向全球的 PostgreSQL 发行版](/zh/article/forge-a-pg-distro/)，以及[什么是 PostgreSQL 发行版](/zh/article/what-is-pg-distro/)。
