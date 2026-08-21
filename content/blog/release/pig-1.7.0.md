---
title: "pig v1.7.0"
linkTitle: "v1.7.0"
date: 2026-08-12
description: "Safer EL module handling, refreshed China mirrors, streamlined EL7 compatibility, and 575 packaged extensions."
tags: [repo, catalog, ext]
weight: 2
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.7.0
---

Pig `v1.7.0` is a repository compatibility and catalog release on top of [v1.6.2](/release/pig-1.6.2/). It makes China-mirror selection explicit, preserves native DNF module filtering by default, restores a streamlined EL7 repository catalog, and grows the bundled extension snapshot from 572 to 575. The embedded Pigsty version remains `4.5.0`.

## Highlights

- `-m|--mirror` now selects the bundled `china` repository definitions directly. PGDG, Rocky Linux, Debian, Ubuntu, Docker, and other regional routes use the maintained mirror list instead of the former runtime PGDG proxy rewrite.
- EL repository definitions no longer receive `module_hotfixes=1` globally. Pigsty and PGDG repositories that intentionally override module streams opt in explicitly; BaseOS, AppStream, EPEL, and other repositories retain native DNF module filtering.
- EL7 keeps a deliberately limited compatibility catalog: archived CentOS 7 Base/Updates/Extras/SCLo and EPEL definitions for `x86_64`, plus shared Pigsty and supported PGDG entries. The DNF-only `module_hotfixes` key is stripped when rendering EL7 YUM configuration.
- Repository setup now reports unsupported platforms when the catalog has no matching definitions, instead of continuing with an empty repository set.
- Release metadata is bumped to `1.7.0`; the embedded Pigsty version remains `4.5.0`.

## Extension Catalog

- Packaged extensions: **572 -> 575**, with no removals.
- 3 new extensions: `pg_local_cache 1.2.0`, `pg_statviz 0.1.0`, and `pg_policy 0.1.0`.
- Version refreshes include `biscuit 3.0.0`, `pg_clickhouse 0.10.0`, `pg_search 0.25.2`, `pg_turbovec` packages `1.29.0`, `pg_uuid_v8 1.1.0`, and the Debian `q3c 2.0.5` package.
- Package metadata and availability matrices are refreshed. Run `pig ext reload` when you need a catalog newer than this release snapshot.

## Compatibility Notes

- No commands or global flags are removed in this release.
- `-m|--mirror` is now an explicit China-region selection rather than a PGDG proxy rewrite. Use `--region=default|china|europe` when you need a specific route.
- Custom EL repository definitions that require module-stream overrides must now set `meta.module_hotfixes: 1` explicitly. This setting is intentionally omitted for ordinary OS repositories and removed on EL7.
- EL7 is end-of-life and only has limited compatibility coverage; prefer EL8 or newer for current PostgreSQL and extension packages.

## Checksums

```checksums
e3a339fefdd2203825d15438b52f18e729547eb88dae014212a46006a9bd47d1  pig-1.7.0-1.aarch64.rpm
34ce29d75ef9f669f3bf832cc812ae082abda7320ee2b2336ea61e701b9b67f8  pig-1.7.0-1.x86_64.rpm
d26803c685ba29c01cb8e6dfe50c6c1b0f004173be82015618fa8cdf6a329ba7  pig-v1.7.0.darwin-amd64.tar.gz
ea8120d48b93da936919f590ebbefeb72e73277e6bc133c1ef0bb1abc055d3ce  pig-v1.7.0.darwin-arm64.tar.gz
40295b64a2423094fa6f4e6d31da8d8ad5b26698c397d8916c0289591522d0bf  pig-v1.7.0.linux-amd64.tar.gz
7929091732957d85751ef3381285a1e5b0c3c7f82c0e00fc24ed085c496012d5  pig-v1.7.0.linux-arm64.tar.gz
41523c15f36a6c1acaf4af5c851d2626472fc15c21d25f91fc1e991fe8411072  pig_1.7.0-1_amd64.deb
adf7b2d9ce8fe42bad935428d16a9c998337df986b1065e0761dc167ce837ef5  pig_1.7.0-1_arm64.deb
```

{{< release-card >}}
