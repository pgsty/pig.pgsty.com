---
title: PIG Blog
url: /blog/
linkTitle: Blog
description: Release notes, design records, and project news
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
    # The blog-wide image is a fallback. Subsections such as Release and Design
    # override it with their own section-level image policy.
    sidebar_menu_foldable: false
    sidebar_menu_compact: false
    sidebar_expand_levels: 3
icon: fa-solid fa-blog
---

Release notes, design records, and project news for PIG — the PostgreSQL extension package manager by Pigsty.
