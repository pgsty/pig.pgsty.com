---
title: "pig v1.10.2"
linkTitle: "v1.10.2"
date: 2026-10-24T00:00:00+08:00
description: "Extension catalog refresh: pg_nanotime, updated packages, and 616 entries."
tags: [ext, catalog]
weight: -2
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.10.2
---

PIG `v1.10.2` refreshes the embedded PostgreSQL extension catalog from
**615 to 616 entries**, adding `pg_nanotime` and updating extension versions,
compatibility, and package availability metadata.

## New extension

Add [`pg_nanotime`](https://github.com/bunko666-cloud/pg_nanotime) `0.2.0`, which
provides nanosecond timestamp and fixed-duration interval types. The catalog
records RPM and DEB packages for PostgreSQL **17 and 18**. Upstream classifies
`0.2.0` as a testing release.

## Version updates

| Extension | Previous | Updated |
|:----------|:---------|:--------|
| `citus`, `citus_columnar` | `14.2.0` | `14.3.0` packages |
| `duckdb_fdw` | `2.0.1` | `2.0.2` |
| `pg_mentat` | `1.17.2` | `1.18.0` |
| `pg_tre` | `4.5.1` | `4.5.2` |

The Citus catalog extension version is `14.3-1`; its RPM and DEB package version
is `14.3.0`. The refresh also adds DEB availability metadata for `pg_tre` on
PostgreSQL 17 and 18.

## Catalog metadata

- Update PostgreSQL compatibility, package availability, licenses, and descriptions.
- Set the `duckdb_fdw` catalog range to PostgreSQL 15–18 and
  `pgcontext_pgvector` to PostgreSQL 17.
- Count **616 catalog entries**: 613 available records and 3 retained removed
  records. The [catalog-entry counting rule](/ext/#catalog-count) includes SQL
  utilities and lifecycle records; availability still depends on the platform
  and PostgreSQL major version.

Go remains at `1.27.3`, embedded Pigsty at `4.5.0`, and default `cargo-pgrx` at
`0.19.3`. Follow the [installation guide](/install/) to upgrade PIG.

## Checksums

```checksums
f07992b20b0b397d1e4bb286656b404e3c911775e98e5fc7d940ef91439f62ed  pig-1.10.2-1.aarch64.rpm
372f4fe8d54a1ad888c91976d011d8b95de3e10286966cfc94b0ab91e2170b20  pig-1.10.2-1.x86_64.rpm
a54be0a4ceadf1e047b74fdb187ff57e9f97b81907c8d66795e7787de88ad864  pig-v1.10.2.darwin-amd64.tar.gz
60df049a38e109bccb3089d74fa41e0d22606ce4df0e4fadae39530d546ca731  pig-v1.10.2.darwin-arm64.tar.gz
686c5d6cf682a5a5a1d70cc09a86fecc441b22456f79bb84f192c4730ac2bd8a  pig-v1.10.2.linux-amd64.tar.gz
e1e84d5afcddc8e474d130de638bc400bb965f887bdc9face842f111fb94afeb  pig-v1.10.2.linux-arm64.tar.gz
38b9634be544a1ee462926f74f3c647c2fc1b21eeffb43e41c24a9033a03a63b  pig_1.10.2-1_amd64.deb
4034cebd3a51839ecb0cb8bdf325d783f1ebb88e19b4664ab21fbf31316eae58  pig_1.10.2-1_arm64.deb
```

{{< release-card >}}
