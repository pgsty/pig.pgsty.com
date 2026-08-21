---
title: "pig v1.6.2"
linkTitle: "v1.6.2"
date: 2026-08-11
description: "572 packaged extensions, Grafana dashboard schema v2, and SOW-first local repository generation."
tags: [catalog, repo, ext, sty]
weight: 5
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.6.2
---

Pig `v1.6.2` is a feature and catalog release on top of [v1.6.1](/release/pig-1.6.1/). It grows the packaged extension catalog from 562 to 572, adds native Grafana dashboard schema v2 support, and improves local repository generation. The embedded Pigsty version remains locked at `4.5.0`.

## Highlights

- `pig sty grafana` now accepts both legacy dashboard JSON and native `dashboard.grafana.app/v2` Dashboard resources. Loading a v2 dashboard uses Grafana's resource API so tabs and section variables survive the round trip; dumping preserves an existing v2 destination while new dumps keep the legacy format by default.
- `pig repo create` now prefers `sow create --pigsty --timeout 10m -- <dir>` when SOW is available, requires the resulting `repo_complete` marker to exist as a regular file, and falls back to `createrepo_c` / `dpkg-scanpackages` on Linux.
- Local repository creation now works on macOS through SOW, defaults to the current directory there, and does not require `sudo`. The Linux default remains `/www/pigsty`.
- Release metadata is bumped to `1.6.2`; the embedded Pigsty version stays at `4.5.0`.

## Extension Catalog

- Packaged extensions: **562 -> 572**, with no removals.
- 10 new extensions: `pg_turbovec`, `pg_disorder`, `pg_mentat`, `plruby`, `jsonb_plruby`, `hstore_plruby`, `ltree_plruby`, `pg_describe`, `cat_tools`, and `pg_vault_tde`.
- 12 version refreshes: `timescaledb 2.29.1`, `q3c 2.0.5`, `pgmnemo 0.16.1`, `pg_search 0.25.1`, `citus 14.2.0`, `citus_columnar 14.2.0`, `provsql 1.12.0`, `plpgsql_check 2.10.4`, `pg_rational 0.0.3`, `pgbson 2.1.0`, `pg_readme 0.7.1`, and `pg_readme_test_extension 0.7.1`.
- Package metadata and availability matrices are refreshed. Run `pig ext reload` to replace the embedded release snapshot with the latest online catalog.

## Compatibility Notes

- No commands or global flags are removed in this release.
- When SOW is installed, `pig repo create` now prefers it over the legacy Linux generators and checks that the completion marker exists before reporting success.
- The catalog count is not a promise that every package is available on every PostgreSQL / OS / architecture combination; use `pig ext avail NAME` on the target host.
- Package-manager and install-script upgrades use the newest version published by the configured Pigsty repository, which may lag GitHub. Use the GitHub assets when you need this exact release.

## Checksums

```checksums
6697a96bbf476e697a5c3da8b6c861719e4b7208e1e4fe927cf4b475ea1f162f  pig-1.6.2-1.aarch64.rpm
ad0b311867bc6cd689dd73e9a96b84f1fe0f49f6c0f1184abf9eb3232a07a184  pig-1.6.2-1.x86_64.rpm
bb167e04fceb6cebee5c8a2423279cefb4474f46301a5055c464ac98294dc9db  pig-v1.6.2.darwin-amd64.tar.gz
3de74e33321884a0c36596c1e7df9370be594a315395538e9ba5b775bbc1a79d  pig-v1.6.2.darwin-arm64.tar.gz
7b69214e115e6815e772b7e179aa4070bd8553e585b164ba3a0f69a1d53a0294  pig-v1.6.2.linux-amd64.tar.gz
b511e727642987867be5921d72e8019e9c6186b82e63ddc34ad653773abed5a8  pig-v1.6.2.linux-arm64.tar.gz
3d1a80b833c6179b84ac5cc590ad06695b187b2bb4a09f544b1a14f9684dc4bc  pig_1.6.2-1_amd64.deb
00e4c84cd6b07a98401c73fb58dedaafe34bc794d7604edbcb76c5de39b0fb44  pig_1.6.2-1_arm64.deb
```

{{< release-card >}}
