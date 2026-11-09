---
title: "pig v1.6.1"
linkTitle: "v1.6.1"
date: 2026-07-30
description: "pig v1.6.1 refreshes the bundled extension catalog and aligns the embedded Pigsty version with 4.5.0."
tags: [catalog, ext, install, repo]
weight: 11
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.6.1
---

`pig` v1.6.1 is a maintenance release on top of [v1.6.0](/release/pig-1.6.0/). It carries no new
commands and no flag changes — the point of the release is the catalog that ships inside the
binary.

## What changed {#what-changed}

- **Extension catalog refreshed.** The embedded `extension.csv` is regenerated from the
  Pigsty package repositories, so `pig ext list` and `pig install` resolve against current
  package versions without a `pig ext reload` round trip.
- **Pigsty version aligned to 4.5.0.** The embedded Pigsty version that `pig sty` and
  `pig status` report now points at Pigsty 4.5.0.
- **Version strings bumped** across the build metadata and `pig update`.

The catalog embedded in the v1.6.1 release covers 562 packaged extensions across PostgreSQL
14–18 on EL 8/9/10, Debian 12/13, and Ubuntu 22/24/26, for both `x86_64` and `aarch64`.
Running `pig ext reload` can replace that release snapshot with a newer online catalog.

## Upgrading {#upgrading}

```bash
pig update                 # upgrade in place through the native package manager
pig update -v 1.6.1        # or pin the exact version
```

A fresh install picks up v1.6.1 automatically:

```bash
curl -fsSL https://repo.pigsty.io/pig | bash   # global (Cloudflare CDN)
curl -fsSL https://repo.pigsty.cc/pig | bash   # mainland China mirror
```

You can also refresh only the catalog on an existing install, without upgrading the binary:

```bash
pig ext reload             # download the latest catalog to ~/.pig/extension.csv
```

See the [release notes](/release/) for the full version history.

## Checksums {#checksums}

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
