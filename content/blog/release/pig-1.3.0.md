---
title: "pig v1.3.0"
linkTitle: "v1.3.0"
date: 2026-02-27
description: "Build pipeline hardening, 461 extensions, new pgedge/ivory support"
tags: [catalog, build, cli, ext]
weight: 121
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.3.0
---

This release is a focused engineering update from `v1.2.0` to `v1.3.0`: 15 commits, 74 files changed, `+1184 / -236` LOC.

It hardens the `pig build` pipeline and extends catalog/alias coverage, increasing total extensions from **451** to **461**.

## Highlights

- Build source download improvements (`pig build get`):
  - Parse multi-source `Source` fields (whitespace/newline/tab) and deduplicate entries.
  - Add source mappings for `agensgraph` / `agentsgraph`.
  - `pgedge` now downloads both `postgresql-17.9.tar.gz` and `spock-5.0.5.tar.gz`.
- Dependency resolution and install improvements (`pig build dep`):
  - RPM dependencies can infer PG major from `pgmajorversion` in spec files; missing spec/control files now return explicit errors.
  - DEB dependency parsing now covers `Build-Depends` / `Build-Depends-Arch` / `Build-Depends-Indep`, including multiline fields, alternatives, arch qualifiers, and build-profile cleanup.
  - `PGVERSION` placeholders can be expanded from `--pg`, installed PG majors, or extension metadata.
  - Dependency install failures are downgraded to warnings so batch runs continue.
- DEB build result semantics fixed (`pig build ext/pkg`):
  - Successful build command exit code is authoritative; artifact discovery is best-effort warning only.
  - Suppress empty package-list banners on successful no-artifact runs.
  - Partial artifacts are warnings, not failures.
  - Build logs now print real metadata source/version values instead of always composing `name-version`.
- Better machine-readable ext operation output (`pig ext rm/update`):
  - After alias resolution, `removed/updated` now returns resolved package names instead of extension aliases.
- Extension catalog and alias updates:
  - New aliases: `agensgraph` / `agens`, `pgedge`, `babelfishpg`.
  - `openhalodb` is aligned to PG14 package naming; `ivorysqldb` naming is aligned.
  - Fork metadata and availability matrix were refreshed in batch (including `timescaledb`, `pgmq`, `orioledb`, `documentdb`, `pg_tde`, and `babelfishpg_*` entries).
- Engineering and release:
  - Version bumped to `v1.3.0` (including a `v1.2.1` transition commit), copyright year moved to 2026, and README refreshed for 461 extensions and current alias docs.

## Compatibility Notes

- Structured `removed/updated` fields in `pig ext rm/update` now contain package names. Automation that matched extension aliases should update parsing logic.

## New Extensions (451 -> 461)

| Extension             | Version | Notes                                             |
|:----------------------|:--------|:--------------------------------------------------|
| `aux_mysql`           | 1.5     | openHalo MySQL compatibility helper (PG14)        |
| `gb18030_2022`        | 1.0     | IvorySQL charset conversion module                |
| `ivorysql_ora`        | 1.0     | IvorySQL Oracle compatibility extension           |
| `ora_btree_gin`       | 1.0     | Oracle datatype GIN indexing support              |
| `ora_btree_gist`      | 1.0     | Oracle datatype GiST indexing support             |
| `pg_get_functiondef`  | 1.0     | Function definition utility                        |
| `plisql`              | 1.0     | PL/iSQL procedural language                        |
| `snowflake`           | 2.4     | pgEdge Snowflake-style ID generator                |
| `spock`               | 5.0.5   | pgEdge multi-master logical replication extension  |
| `lolor`               | 1.2.2   | pgEdge logical-replication-friendly large objects  |

## Full Commit List (`v1.2.0..v1.3.0`)

- `b8ecf8d` bump version string to 1.2.1
- `55df9a4` build/get: support multi-source parsing and pgedge spock tarball
- `da8e347` add agensgraph and pgedge alias
- `86edbd7` ext: show resolved package names in rm/update results
- `ef3c905` build/dep: improve rpm/deb dependency resolution
- `7144e09` ext/catalog: refresh fork metadata and matrix entries
- `befffbf` build(deb): treat successful build command as authoritative result
- `33fd517` build(deb): avoid empty package list banner on successful no-artifact runs
- `3b450f2` avoid concat ext pkg name with version when download
- `33847ab` fix(ext): satisfy staticcheck S1011 in rm/update
- `b8b917d` build(dep): treat dependency install failures as warnings
- `8110c00` adjust ivorysqldb babelfishpg alias
- `fac9faf` bump version to 1.3.0
- `1f88f06` chore: update copyright year to 2026
- `c804757` v1.3.0

## Checksums

```checksums
196f32419886da095f303b1bcad2729b674abc03d412199e88a39390b2616534  pig-1.3.0-1.aarch64.rpm
a2dcc930dd47a08e85285c1fb7925e1355a1e67d458a265a7ef6d9666bc8e7ec  pig-1.3.0-1.x86_64.rpm
c7ebda6b9839408b12ffe1c8ea561f03e1793aae0732f9bbe2320a0d45160714  pig-v1.3.0.darwin-amd64.tar.gz
b717b485ed0a4a8c11dd8bf918400595b21df5ef43818836ec332f8518674c1a  pig-v1.3.0.darwin-arm64.tar.gz
40e6570c6ba0fe36c97950ff8de585eecb6bc1f862509a04f410a5f08ee90148  pig-v1.3.0.linux-amd64.tar.gz
d61430eeafc8005a22918a9aa60dea5c987916f9834331b5484f761b8235644f  pig-v1.3.0.linux-arm64.tar.gz
62c9a4fadc7dda393d6f28ab83b5f3d741e7d7f7de7abe40a5b89c393288519c  pig_1.3.0-1_amd64.deb
19261ae50e873a05a10a6ad500ab1b429b22e2612325c09f9cd5443dcd34308b  pig_1.3.0-1_arm64.deb
```

{{< release-card >}}
