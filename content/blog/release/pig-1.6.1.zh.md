---
title: "pig v1.6.1"
linkTitle: "v1.6.1"
date: 2026-07-30
description: "pig v1.6.1 刷新了内置的扩展目录，并将内嵌的 Pigsty 版本对齐到 4.5.0。"
tags: [catalog, ext, install, repo]
weight: 11
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.6.1
---

`pig` v1.6.1 是 [v1.6.0](/zh/release/pig-1.6.0/) 之上的维护版本：没有新增命令，也没有参数变更，
这次发布的重点是二进制里自带的那份扩展目录。

## 变更内容 {#what-changed}

- **扩展目录刷新**：内置的 `extension.csv` 依据 Pigsty 软件仓库重新生成，`pig ext list`
  与 `pig install` 无需先跑一次 `pig ext reload`，即可对齐当前的软件包版本。
- **Pigsty 版本对齐到 4.5.0**：`pig sty` 与 `pig status` 报告的内嵌 Pigsty 版本随之更新。
- **版本号同步**：构建元数据与 `pig update` 的版本字符串一并更新。

v1.6.1 发布包内置的目录覆盖 PostgreSQL 14–18 上的 562 个已打包扩展，
适用于 EL 8/9/10、Debian 12/13、Ubuntu 22/24/26，`x86_64` 与 `aarch64` 双架构。
运行 `pig ext reload` 后，这份发布快照可能会被更新的在线目录替换。

## 升级方式 {#upgrading}

```bash
pig update                 # 通过系统包管理器就地升级
pig update -v 1.6.1        # 或者指定精确版本
```

全新安装会直接拿到 v1.6.1：

```bash
curl -fsSL https://repo.pigsty.cc/pig | bash   # 中国大陆镜像
curl -fsSL https://repo.pigsty.io/pig | bash   # 全球站点（Cloudflare CDN）
```

如果只想刷新目录、不升级二进制，也可以：

```bash
pig ext reload             # 把最新目录下载到 ~/.pig/extension.csv
```

完整版本历史见 [发布注记](/zh/release/)。

## 校验和 {#checksums}

```checksums
088e62bf7c64dbbe1d66cb54e6a6971e4d245e76ac0b9ab9de2280053b692e77  pig-1.6.1-1.aarch64.rpm
11b81f43754bcd7691752025ff0a95aa39745883d1cc17183e81fd357f50f5d3  pig-1.6.1-1.x86_64.rpm
f0512d26fd934a9ac7b0bf5aba22aba151991a4edcc8e995441f79f66fc6080a  pig-v1.6.1.darwin-amd64.tar.gz
595f122c210b1e5a5211de5b397bfcf2a803179f52a97aa38e68e8c567381533  pig-v1.6.1.darwin-arm64.tar.gz
d6c0ad7784c8df33539d60cb22259bb1b6f92a6fc26543f4384448dd630a83fd  pig-v1.6.1.linux-amd64.tar.gz
017fbae1c32858b5438514685e45959ceaeb6bf29ae11ecf0496b52d00908627  pig-v1.6.1.linux-arm64.tar.gz
571bc16bc8490190935ecb6d8dde9c5827e63eced0b7bbd05cfad1e4363e385b  pig_1.6.1-1_amd64.deb
54010b414aaf3971c435db714d5e1c0e039f30a11adf95a902040e177f911fa6  pig_1.6.1-1_arm64.deb
```

{{< release-card >}}
