---
title: "pig v1.4.1"
linkTitle: "v1.4.1"
date: 2026-05-01
description: "510 个扩展，支持 Ubuntu 26.04，仓库校准"
tags: [catalog, patroni]
weight: 61
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.4.1
---

- 扩展目录更新到 **510** 个扩展，新增 3 个扩展，更新 17 个扩展。
- 新增 Ubuntu 26.04 `resolute` 支持，移除 Ubuntu 20.04 `focal` 支持。
- 将 `el9.aarch64` 特例中的 `patroni` / `patroni-etcd` 提升到 `4.1.2`。
- 校准上游软件仓库定义。

## 校验和

```checksums
cbfbb04b9640dcf39fcd9ccfa49e500dd0e65b72c0326c0d166e6f43e52b6dc3  pig-1.4.1-1.aarch64.rpm
c3325c7c68559b3149567eddd5963c4bc3bb4b39622740ca469f9d5d274e462b  pig-1.4.1-1.x86_64.rpm
c82e8a5e010aed198748576a3740479ac73eaa4a05f50cd4afc82fbcc9075d4d  pig-v1.4.1.darwin-amd64.tar.gz
a62e223a9f3fb6755cfeabfed2b9241d1be8aad42251917ddb2a4757fa5df6bd  pig-v1.4.1.darwin-arm64.tar.gz
65938e1158deb8a795c32ae99ff09178b7dec6b09743f8bdfbd9fd09a522e89f  pig-v1.4.1.linux-amd64.tar.gz
0fe4172dd1f03ac1b6ac73a28cdfe78b70c6613996252a230710b291faf8db58  pig-v1.4.1.linux-arm64.tar.gz
bdcc318ed50bff505f193f3a265d8fd2c7b093a104d5e5728b8c070e3580827e  pig_1.4.1-1_amd64.deb
1a1acb69d41bcfb9df8fb86c8d3c076050df5a242b639c1215833cd6394e112d  pig_1.4.1-1_arm64.deb
```

{{< release-card >}}
