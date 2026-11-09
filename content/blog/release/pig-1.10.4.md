---
title: "pig v1.10.4"
linkTitle: "v1.10.4"
date: 2026-11-06
description: "Seven new catalog entries, refreshed package metadata, target-version alias fixes, and 626 entries."
tags: [ext, catalog, install]
weight: 1
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.10.4
---

PIG `v1.10.4` refreshes the embedded PostgreSQL extension catalog from **620 to 626 entries** and fixes category aliases to respect the requested PostgreSQL major version. The November 6, 2026 snapshot adds seven entries and drops the retired `pgcontext_pgvector` record, for a net increase of six.

## New catalog entries {#new-catalog-entries}

| Extension | Version | PostgreSQL support | Description |
|:----------|:--------|:-------------------|:------------|
| `pg_warren` | `0.8.0` | 15–18 | Versioned graph traversal and computation over PostgreSQL tables |
| `pg_statecharts` | `0.1.0` | 16–18 | Hierarchical state machines and transactional event handling |
| `pg_statecharts_dev` | `0.1.0` | 16–18 | SCXML import and migration tooling for pg_statecharts |
| `pg_lion` | `0.3.0` | 16–18 | Roaring bitmap inverted indexes for filtering, counts and aggregates |
| `pg_lion_citext` | `0.3.0` | 16–18 | Case-insensitive citext operator class for lion indexes |
| `pg_lion_vector` | `0.3.0` | 16–18 | Filtered nearest-neighbor indexes for pgvector vector and halfvec |
| `opencc` | `0.1.0` | 14–18 | OpenCC conversion between Simplified Chinese, Traditional Chinese, regional variants and Japanese Shinjitai |
{.wide .expand}

Installability depends on the target PostgreSQL major, operating system, architecture, and configured repository.

## Version and package metadata updates {#version-and-package-metadata-updates}

Selected catalog version changes:

| Extension | Version change |
|:----------|:---------------|
| `postgis` | `3.6.4` → `3.7.0` |
| `timescaledb_toolkit` | `1.26.0` → `1.27.0` |
| `vchord` | `1.1.1` → `1.2.0` |
| `vchord_bm25` | `0.3.0` → `1.0.0` |
| `pg_tokenizer` | `0.1.1` → `1.0.0` |
| `pg_search` | `0.26.3` → `0.26.5` |
| `pg_duckdb` | `1.1.1` → `1.2.0` |
| `pg_lake` | `3.5` → `3.6` |
| `anon` | `3.2.3` → `3.3.2` |
| `pg_integrity_checksums` | `2.0.0` → `2.1.0` |

The refresh also updates package availability, dependencies, descriptions, and source metadata. PostGIS 3.7 uses the `postgis37_N` RPM family, with separate address-standardizer and Tiger Geocoder packages. The EL pgaudit catalog uses `pgaudit_14` and `pgaudit_15` for PostgreSQL 14 and 15.

## Category aliases follow the target version {#category-aliases-follow-the-target-version}

For stable PostgreSQL versions, `pgsql-<category> -v N` now selects the same platform and PostgreSQL-major matrix as `pgN-<category>`. For example, `pig ext add pgsql-gis -v 14 --plan` no longer includes packages available only for a newer PostgreSQL major. Package names come from the catalog, replacing the obsolete pgaudit rename in the resolver. Beta targets retain the existing latest-stable, PGDG-only fallback.

## Catalog count and build versions {#catalog-count-and-build-versions}

The embedded catalog contains **626 records**: **624 available** entries and **2 retained removed** records. They map to **518 distinct package names**, including PostgreSQL contrib modules, or **457 non-contrib package families**. See the [catalog-entry counting rule](/ext/#catalog-count).

Go remains at `1.27.3`, embedded Pigsty at `4.5.0`, and default `cargo-pgrx` at `0.19.3`. Follow the [installation guide](/install/) to upgrade PIG.

## Checksums {#checksums}

```checksums
4981a060779423ab4d6c5baaa8fe6c26adb972fc34b9515119b9e5d4723513ce  pig-1.10.4-1.aarch64.rpm
d1624bbcec5d3f4715d223acca8311182ef1ee36542c16bcf82602674ee82b07  pig-1.10.4-1.x86_64.rpm
9384759851af53f5cddc381007f78de9a226b43b914848291df86ec41096119e  pig-v1.10.4.darwin-amd64.tar.gz
d0f876a518b82f021c83914c5909f1ac914cbe8c0aa0957cef37c83d69b79b0d  pig-v1.10.4.darwin-arm64.tar.gz
1caa6f4af13e1f40f5faa9752628efe1dd85190b344bf1597cb3c8d23e99fe0b  pig-v1.10.4.linux-amd64.tar.gz
756b7c94936a4c8cca1b0a15f3bcac8eee9669480b8d6af205e920b673a680ba  pig-v1.10.4.linux-arm64.tar.gz
98bbfce9dc263e94d4025debdd9bf0e137d9ec12afff4d57e4e08530b1255bf3  pig_1.10.4-1_amd64.deb
18447ccff10fd31c90ae16b34f2885a0415bc6efca5d0ff78f435e68ba6438e1  pig_1.10.4-1_arm64.deb
```

{{< release-card >}}
