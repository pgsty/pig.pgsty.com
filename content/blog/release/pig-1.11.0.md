---
title: "pig v1.11.0"
linkTitle: "v1.11.0"
date: 2026-11-12
description: "Pigsty 4.6.0 alignment, ordered sty conf template lookup, command and package safety hardening, and 625 catalog entries."
tags: [cli, ext, sty, postgres]
weight: -1
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.11.0
---

PIG `v1.11.0` aligns embedded Pigsty support with `v4.6.0`, adds ordered template shorthand lookup in `pig sty conf`, hardens package and operational command safety across `ext`, `repo`, `do`, `pg`, `pb`, `pitr`, `sty`, and `inventory`, and updates the embedded PostgreSQL extension catalog to **625 entries**.

## Command and package safety {#command-and-package-safety}

- **Protected package removal**: [`pig ext rm`](/ext/#ext-rm) now blocks accidental removal of PostgreSQL server packages, shared contrib bundles, and supported replacement kernels when invoked through an extension name or category alias (`100102`, exit `2`). Independent procedural-language packages remain removable by extension name, while intentional server or kernel removal requires an explicit package-group alias such as `pg18-server`, `pg18-contrib` (EL), or `orioledb-server`. See the [protected package removal design](/design/protected-package-removal/).
- **APT release-level trust reconciliation**: [`pig repo add`](/repo/#trust-and-configuration-ownership) and `repo set` reconcile `trusted` and `signed-by` options across matching APT URIs and suites before writing repository files, preserving `sty boot` signing policies across additive operations while rejecting conflicting explicit definitions.
- **Explicit playbook removal boundaries**: [`pig do pgsql-rm`](/do/#postgresql-operations) passes `pg_rm_pkg=false` by default unless `--uninstall` sets `pg_rm_pkg=true`, and `pig do pgmon-rm` removes `/infra/targets/pgrds/<cluster>.yml` on `infra` hosts to match `pgmon-add`. See the [operations CLI safety contract](/design/ops-cli-safety/).
- **PostgreSQL and recovery execution guards**: text `pig pg status` now shares structured exit status and avoids external `test` dependency when already running as the target DBSU; `pig pg psql -f` enables `ON_ERROR_STOP=1` and resolves caller-relative paths before user switching; internal database enumeration passes `psql -X`; `pig pg fork` pins isolated `data_directory`, `hba_file`, `ident_file`, `port`, and recovery/archive overrides across both `postgresql.conf` and `postgresql.auto.conf`, while propagating `--force` into confirmation retry hints; `pig pg vacuum` and `pig pg freeze` enforce `--table` when `--schema` is specified; `pig pg kill` and `pig pg tune` reject invalid PID, watch, and floating-point boundaries; and `pig pb restore` / `pig pitr` preserve incremental/differential backup labels, reject `--reset-*` / `--no-*` overrides and empty `-D` flags, and omit raw option values from validation errors.
- **Structured output and inventory fidelity**: early argument-error rendering honors attached `-ojson` spellings without crossing `--`; atomic file writes preserve existing permissions instead of falling back to `0644`; legacy wrapper downloads keep progress off stdout; bounded diagnostic capture retains both head and tail context while preserving full data capture for configuration and SQL queries; `pig inventory cmdb dump` preserves signed/unsigned 64-bit integer and floating-point scalar types and flags multi-host PostgreSQL URI and `sslpassword` credentials; `pig pt status` emits structured JSON errors when Patroni configuration resolution fails; and `pig sty grafana` rejects unsafe dashboard path segments while redacting malformed endpoint URLs.

## Pigsty 4.6.0 bootstrap and configuration {#pigsty-bootstrap-and-configuration}

- [`pig sty conf`](/sty/#sty-conf) resolves bare template names in Pigsty's fixed order (`conf/`, `conf/ha/`, `conf/fork/`, `conf/app/`, `conf/demo/`, `conf/build/`), so shorthand names such as `full`, `trio`, or `oss` apply the selected template's version-pinning and preflight rules.
- `pig sty conf` writes explicitly selected or detected `default` region values into templates that start with `china`, keeping the output file and structured result aligned.
- [`pig sty boot`](/sty/#sty-boot) and `pig repo boot` check `/var/tmp/pkg.tgz` first and fall back to `/tmp/pkg.tgz` only when the primary path does not exist, rejecting untrusted or unreadable automatic bundles before creating target directories.

## Catalog and package aliases {#catalog-and-package-aliases}

- Added `kes` and `openbao` to the `infra` package-group alias on both EL and Debian/Ubuntu.
- Refreshed nine extension versions in the bundled catalog:
  - `login_hook`: `1.8` -> `1.9`
  - `pg_curl`: `2.4.6` -> `2.5.0`
  - `pg_improv`: `0.12.2` -> `0.14.0`
  - `pg_integrity_checksums`: `2.1.0` -> `2.2.0`
  - `pg_mentat`: `1.19.1` -> `1.20.0`
  - `pg_search`: `0.26.5` -> `0.26.6`
  - `pg_tokenizer`: `1.0.0` -> `1.1.0`
  - `vchord`: `1.2.0` -> `1.3.0`
  - `vchord_bm25`: `1.0.0` -> `1.1.0`
- Removed the retired `documentdb_distributed` catalog entry, cleaned its residual `require_by` references on `citus`, `documentdb`, and `documentdb_core`, and restored `columnar` to `available` status.

## Catalog count and build versions {#catalog-count-and-build-versions}

The embedded catalog contains **625 records** (**625 available** entries and **0 retained removed** records). They map to **518 distinct package names**, including PostgreSQL contrib modules, or **457 non-contrib package families**. See the [catalog-entry counting rule](/ext/#catalog-count).

PIG `v1.11.0` is built with Go `1.27.4`, embeds Pigsty `4.6.0`, and defaults `cargo-pgrx` to `0.19.3`. Follow the [installation guide](/install/) to upgrade PIG.

## Checksums {#checksums}

```checksums
c3c24b64dce312a13fe1b3bcb15d38101095dfd2569ed88186838a33291abcac  pig-1.11.0-1.aarch64.rpm
2c0d05aba718957f4654cb135771610f042b6f71b7902a792b598744632736b9  pig-1.11.0-1.x86_64.rpm
d9c0b9b3bde4e5e53d64a0df177dcda48575eed0310178adaff11f6d33a76cd9  pig-v1.11.0.darwin-amd64.tar.gz
474788f79563e99e7443e619bb7e594f598284c9a81f22d53f33bacf03c5da27  pig-v1.11.0.darwin-arm64.tar.gz
8f21efdd33d5a063eb7e12d2908912682af4dd94e336d82124ab9eb57808974c  pig-v1.11.0.linux-amd64.tar.gz
4c2699618fb50d6bb5d2c0807e407442c69c9873a4d33dc3193bbab9c039bdcd  pig-v1.11.0.linux-arm64.tar.gz
4bf90bbd4bc179391b5d88f2d51cb2d08b165212305434f59d12dcab0dc7ea5a  pig_1.11.0-1_amd64.deb
ba4fb6cd9927712fe6ac7af237a7f96076febd972cb99c121ebf620a08664979  pig_1.11.0-1_arm64.deb
```

{{< release-card >}}
