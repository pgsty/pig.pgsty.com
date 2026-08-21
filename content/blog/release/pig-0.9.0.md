---
title: "pig v0.9.0"
linkTitle: "v0.9.0"
date: 2025-12-28
description: "Rename sty deploy and expand sty conf options"
tags: [sty, ext]
weight: 156
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v0.9.0
---

## Changes

- Rename `pig sty install` to `pig sty deploy` so the command name reflects that it runs the Pigsty deployment playbook.
- Add the `-g`, `-p`, and `-o` options to `pig sty conf`, aligning it with the configure script available in this release.
- Keep `llvmjit` in the `pgsql-full` package alias.

## Checksums

```checksums
ea0c098d0829720b6e364d2f2a91328876962c7f0ae94eee7bdcde0bd43313fa  pig-0.9.0-1.aarch64.rpm
707f4e1fde76d3faa05165ac11e97969c22a8740c97ef84da52727d0328990cc  pig-0.9.0-1.x86_64.rpm
56aeb61674ddfb64368e6f5535e06a38b76f62e3d6c9536a63be7df6babed93e  pig-v0.9.0.darwin-amd64.tar.gz
a213d16817d6124ffa83d93ad880a040598b6ed3fe23a74d43420c095ed43de4  pig-v0.9.0.darwin-arm64.tar.gz
6a1a1836217fa723ca42bc2276ecf1453cd2ee0acacddfc313164701b24a452f  pig-v0.9.0.linux-amd64.tar.gz
5e5728aa5922138c61c900a731f97cdc1b9653c14d7fe804b6753fb6f222b8b0  pig-v0.9.0.linux-arm64.tar.gz
e80d2cb3ceb5fd58fc0262ab4b39b44e8dcccb7712151c73a41ba50cb510353b  pig_0.9.0-1_amd64.deb
ecb504efffde8d696b765579332fc0b3304751fa8077c4c0394e7f3c44aa0fe2  pig_0.9.0-1_arm64.deb
```

{{< release-card >}}
