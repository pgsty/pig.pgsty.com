---
title: "pig v1.10.1"
linkTitle: "v1.10.1"
date: 2026-10-24T00:00:00+08:00
description: "Go 1.27.3 security update, refreshed dependencies, and 615 extension catalog entries."
tags: [build, catalog, cli]
weight: -1
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.10.1
---

PIG `v1.10.1` is a security and catalog maintenance release. It upgrades Go to
`1.27.3`, refreshes tooling dependencies, and expands the embedded PostgreSQL
extension catalog from **603 to 615 entries**.

## Security update

- Upgrade the Go toolchain from `1.27.2` to `1.27.3`. CI and release builds read
  the version from `go.mod`.
- Include the `crypto/x509` fix for
  [CVE-2026-111943 / GO-2026-6809](https://pkg.go.dev/vuln/GO-2026-6809).
  Go's certificate verifier rejects chains containing specific intermediate
  certificates that are no longer trusted.

Go `1.27.3` adds **one security fix** over `1.27.2`, as documented in the
[Go release announcement](https://groups.google.com/g/golang-announce/c/66pojueaQek).
Earlier Go security fixes are already included in the `1.27.2` baseline used by PIG `v1.10.0`.

## Dependency updates

Update inherited tooling dependencies through version-specific module replacements:

| Module | Previous | Updated |
|:-------|:---------|:--------|
| `github.com/cpuguy83/go-md2man/v2` | `v2.0.6` | `v2.0.7` |
| `github.com/stretchr/objx` | `v0.1.0` | `v0.8.0` |
| `golang.org/x/mod` | `v0.41.0` | `v0.42.0` |
| `golang.org/x/tools` | `v0.51.0` | `v0.52.0` |

## Extension catalog

The embedded catalog now contains **615 entries**, with **12 additions** since `v1.10.0`:

- `codesystem`, `encsearch`, `hdr_histogram`, `pg_improv`
- `pg_kv`, `pg_lease`, `pg_synonym`, `pg_table_range`
- `pg_tre`, `pg_try_cast`, `stannum`, `tin`

The refresh also updates existing extension versions and package availability metadata.
The total follows the [catalog-entry counting rule](/ext/#catalog-count): it includes
packaged SQL utilities and retained records for removed extensions. It does not imply
that all 615 entries support `CREATE EXTENSION` or can be installed on every platform.

## Compatibility

Commands, flags, and configuration remain compatible with `v1.10.0`.
Embedded Pigsty remains at `4.5.0`, and default `cargo-pgrx` remains at `0.19.3`.

Building from source requires Go `1.27.3` or later. Prebuilt packages do not require a local Go installation.
Follow the [installation guide](/install/) to upgrade PIG. Replacing the PIG executable
brings in the updated Go standard library; upgrading the host's Go installation alone
does not update an existing PIG binary.

## Checksums

```checksums
fbd58de4cd1fa767c6d2b15d4fcb029fe38c90a0d12db2e387b7f698b5c8a69d  pig-1.10.1-1.aarch64.rpm
7955e93744fcc2d4cce9044102c2bd7ca470388a0556d3220a624f78e38c629b  pig-1.10.1-1.x86_64.rpm
31fea0e9513e551e2be8dc99a8fc0f77de4bdfe40e66dadc206e227254bb7942  pig-v1.10.1.darwin-amd64.tar.gz
1177f3b616279100ce97d23eb4fa6bc2e8daf02dbd23780a8dd5025240082c5a  pig-v1.10.1.darwin-arm64.tar.gz
0e837098d45b080ddf9205681709dbc38318d2b65cbdaed711246fd5834c3b50  pig-v1.10.1.linux-amd64.tar.gz
6658242816263ea4f5e3abeb3454665098c7100c75c76a3e45386a15faf6f397  pig-v1.10.1.linux-arm64.tar.gz
37f5dca9407010c56d8c5747c8ddcef101d7f07602296e0bb89620c633692eab  pig_1.10.1-1_amd64.deb
f385d1c6fac40a6cf648505d349a72e7e3eadf2948024f086efe81733c2a9be5  pig_1.10.1-1_arm64.deb
```

{{< release-card >}}
