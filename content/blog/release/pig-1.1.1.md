---
title: "pig v1.1.1"
linkTitle: "v1.1.1"
date: 2026-02-14
author: "Ruohang Feng"
description: "Path, symlink, and build migration fixes"
categories: [release]
tags: [Release, pig]
weight: 135
---

## Fixes

- Preserve symlink semantics during build-tree migration and support cross-device moves.
- Handle a PostgreSQL log directory configured as the filesystem root without resolving files outside the intended directory.
- Allow `pig repo rm` to remove repository modules whose names contain dots while retaining safe-path validation.
- Accept safe relative symlinks when `pig sty init` extracts a Pigsty release archive.

## Checksums

```bash
22fe5e951f09e7cfa46ab22781199b3209792992940eb5615ace4928e41a7429  pig-1.1.1-1.aarch64.rpm
7f5a10bbefdc39e5d66a7e688fa78c5ba566c8140458b9f4b1536ff0d7ed457a  pig-1.1.1-1.x86_64.rpm
b90aec9dc559df81c46d32575a8d231fa6d7eeb8b25f4d2e0b6076cc0a9c0e59  pig-v1.1.1.darwin-amd64.tar.gz
3063e3a72e68371a082b4e629d12aafda46d96eddc22976beb2049881854f4ea  pig-v1.1.1.darwin-arm64.tar.gz
081ff8c81bf61108a35ca4cdc51007d4ddf1de8a041d8be087e58e7068e7e177  pig-v1.1.1.linux-amd64.tar.gz
9a81e868699f92d73f8aeb7752206b6eaac8d42d1688089a1f543b12ee0d272d  pig-v1.1.1.linux-arm64.tar.gz
85ce861cfbff846be2ba912ba8dfc766121dad14a59937387d9c5e26b0b6f541  pig_1.1.1-1_amd64.deb
3a108f0544af4d1f98acee55c06c5b5af3b856e3be2b18767e6db0b8a1cc664f  pig_1.1.1-1_arm64.deb
```

Release: https://github.com/pgsty/pig/releases/tag/v1.1.1
