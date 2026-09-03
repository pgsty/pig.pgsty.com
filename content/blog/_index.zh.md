---
title: PIG 博客
url: /zh/blog/
linkTitle: 博客
description: 文章、设计注记、发布注记与项目动态
weight: 40
type: blog
sidebar_root_for: self
sidebar_root_link_self: true
# 根下拉里已经有「博客」这一项，文档树里不必再出现一次。
toc_root: true
images: [/images/pig.webp]

outputs:
  - HTML
  - RSS
  - print
  - markdown
cascade:
  type: blog
  images: [/images/pig.webp]
  outputs:
    - HTML
    - print
    - markdown
  params:
    # Blog 根图片只作保底；Release 与 Design 等栏目可在栏目级
    # 覆盖为自己的图片策略。
    sidebar_menu_foldable: false
    sidebar_menu_compact: false
    sidebar_expand_levels: 3
icon: fa-solid fa-blog
---

PIG 的文章、设计注记、发布注记与项目动态 —— Pigsty 出品的 PostgreSQL 扩展包管理器。
