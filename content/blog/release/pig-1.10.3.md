---
title: "pig v1.10.3"
linkTitle: "v1.10.3"
date: 2026-10-29T00:00:00+08:00
description: "Four new extensions, metadata refresh, and 620 catalog entries."
tags: [ext, catalog]
weight: -3
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.10.3
---

PIG `v1.10.3` refreshes the embedded PostgreSQL extension catalog from
**616 to 620 entries**, adding four extensions and updating package, version,
compatibility, and availability metadata.

### New extensions

| Extension | Version | PostgreSQL support | Description |
|:----------|:--------|:-------------------|:------------|
| `oai_fdw` | `1.16` | 14–18 | Read-only OAI-PMH foreign data wrapper for metadata harvesting over HTTP/HTTPS |
| `pg_agent_gate` | `0.3.0` | 18 | SQL proposal, verification, and execution gate with human approval for agent roles |
| `pg_integrity_checksums` | `2.0.0` | 14–18 | Physical and logical checksums for PostgreSQL pages, rows, tables, indexes, and databases |
| `pg_stat_tcpinfo` | `1.1` | 14–18 | Linux TCP connection statistics, latency, and retransmission metrics |

These records describe catalog and package availability; actual installability
still depends on the target PostgreSQL major, operating system, architecture,
and repository snapshot.

### Version and metadata refresh

The catalog updates existing package and extension metadata, including
`pg_nanotime` `0.2.0` → `0.3.0`, `supautils` `3.4.4` → `4.0.0`,
`pg_ducklake` `1.0.2` → `1.0.3`, `pg_improv` `0.10.0` → `0.12.1`,
`wrappers` `0.6.3` → `0.6.4`, `edtf_postgres` `1.2.3` → `1.3.2`,
`hypopg` `1.4.3` → `1.4.4`, and `rdf_fdw` `3.0` → `3.1`.
It also refreshes package matrices, compatibility ranges, descriptions, and
source metadata for the maintained catalog.

### Catalog count

The catalog now contains **620 entries**: 617 available records and 3 retained
removed records. The [catalog-entry counting rule](/ext/#catalog-count) includes
SQL utilities and lifecycle records; availability remains platform-specific.

Go remains at `1.27.3`, embedded Pigsty at `4.5.0`, and default `cargo-pgrx` at
`0.19.3`. Follow the [installation guide](/install/) to upgrade PIG.

## Checksums

```checksums
2068ca8150df3ee837d0ba6e533ba651703c7223c14c522703ee1be9c41666ea  pig-1.10.3-1.aarch64.rpm
97ff1c1799262650a92d669dafc905d498d5ab3cf58619198322bc2d274b4ceb  pig-1.10.3-1.x86_64.rpm
16203993bbba93dee16a38eac3eedbf67ed2cce3c7894cedbba613e95578004c  pig-v1.10.3.darwin-amd64.tar.gz
0eb3f0447107734ae7decf3bc16caf99087e86119e83ce34987ebb376285fb14  pig-v1.10.3.darwin-arm64.tar.gz
a3e61d0d71b9226ac89aa3b1e29baa8c92e5109ecaa2c7e26343f474e5832e04  pig-v1.10.3.linux-amd64.tar.gz
5f25ff6cf634f708d5f70bde39a07d83fe9c7d1ef7d944395eb294eb64554ecf  pig-v1.10.3.linux-arm64.tar.gz
dfabbcf4fcdf612d79a7cce76db08d36683e00bd2b0f27c7e78258f54fcb721a  pig_1.10.3-1_amd64.deb
4065ed14209a4857b26fa1c7e19adbeee2e5be68df41710db33b64b18159045f  pig_1.10.3-1_arm64.deb
```

{{< release-card >}}
