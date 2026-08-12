---
title: PIG 博客
url: /zh/blog/
linkTitle: 博客
description: 发布注记与项目动态
weight: 40
type: blog
sidebar_root_for: self
sidebar_root_link_self: true
# 根下拉里已经有「博客」这一项，文档树里不必再出现一次。
toc_root: true

outputs:
  - HTML
  - RSS
  - print
  - markdown
cascade:
  type: blog
  outputs:
    - HTML
    - print
    - markdown
  params:
    # 发布列表刻意采用 OINK 的纯文本卡片，不重复铺同一张默认图片。
    default_featured: false
    ui:
      sidebar_menu_foldable: false
      sidebar_menu_compact: false
      ul_show: 3
icon: fa-solid fa-blog
---

PIG 的发布注记与项目动态 —— Pigsty 出品的 PostgreSQL 扩展包管理器。
