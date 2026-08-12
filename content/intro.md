---
title: "Introduction"
linkTitle: "Introduction"
description: "What PIG manages, where it helps, and where its package-management boundary ends"
search_keywords: [overview, architecture, scope, package boundary]
search_boost: 1.25
weight: 20
icon: fas fa-lightbulb
categories: [Concept]
---

PostgreSQL has an unusually rich extension ecosystem, but distributing those extensions is harder than discovering them. A usable package must match the PostgreSQL major version, Linux distribution release, CPU architecture, dependency set, and sometimes a vendor-specific repository. If no matching package exists, the operator also owns the compiler toolchain and future upgrades.

**PIG** is a Go command-line tool that makes the packaged path easier. It maintains a catalog of [{{< param pgext_count >}} packaged extensions](https://pigsty.io/ext/list), maps extension names to native RPM/DEB package names, configures known APT/DNF repositories, and delegates installation to the operating system package manager. It also provides source-build helpers and operational wrappers for PostgreSQL, Patroni, pgBackRest, PITR, Pigsty, and Grafana.

That is useful, but the boundary matters: PIG is a **package and host-management tool**, not a PostgreSQL extension registry inside each database, an independent dependency solver, or a substitute for database change management.

> [ANNOUNCE pig: The Postgres Extension Wizard](https://www.postgresql.org/about/news/announce-pig-the-postgres-extension-wizard-2988/)

## What PIG Actually Manages

| Layer | What PIG does | What remains with the operator |
|:---|:---|:---|
| Catalog | Searches extension metadata and resolves extension names to OS packages | Confirm that the selected release, license, and feature set fit the workload |
| Repository | Writes or updates APT/DNF repository definitions and refreshes metadata | Approve repository trust, mirrors, signatures, network policy, and package provenance |
| Package | Installs, removes, or updates native RPM/DEB packages | Plan maintenance windows and verify dependency changes or service impact |
| Database | Shows hints such as `CREATE EXTENSION` and preload requirements | Run SQL, edit `shared_preload_libraries`, restart when required, migrate schemas, and validate every database |
| Build | Applies the project build specification to a local source build | Provide a compatible toolchain, dependencies, reproducible inputs, and test the resulting package |
| Operations | Wraps selected PostgreSQL/Pigsty workflows and can preview some plans | Own backups, HA policy, credentials, approvals, and production verification |

Installing `pgvector`, for example, puts control files and shared libraries on the host; it does **not** create `vector` in every database. Likewise, `pig ext update` upgrades named OS packages but does not run `ALTER EXTENSION UPDATE`. See the [extension command boundary](/ext/#package-layer-vs-database-layer) for the exact behavior.

## The Questions Behind the Convenience

### Catalog size is not universal availability

The catalog currently contains {{< param pgext_count >}} packaged extension entries. That number is a catalog count, not a promise that every extension has a package for every PostgreSQL/OS/architecture cell. Licenses, upstream build support, abandoned projects, dependency conflicts, and architecture-specific failures all create gaps. Use `pig ext avail NAME` on the target host as the practical source of truth, then verify the actual package candidate with APT or DNF before a production rollout.

### Packages come from more than one producer

PIG can use packages maintained by Pigsty, PGDG, Linux distributions, and upstream/vendor repositories. They do not all share one release cadence, support policy, patch policy, or license. PIG records metadata and makes installation consistent; it does not relicense third-party software or turn every upstream package into a Pigsty-maintained artifact.

### Repository convenience changes trust state

`pig repo add` is additive, while `pig repo set` intentionally backs up existing definitions and writes a selected repository set. Inspect the intended definitions with `pig repo info` before using replacement mode on a managed host. The built-in compatibility defaults for Pigsty repositories are permissive (`gpgcheck=0` on RPM systems and `trusted=yes` on DEB systems), so security-sensitive environments should establish and enforce their own signing-key and repository-trust policy rather than treating a successful download as supply-chain verification.

### Source builds are a fallback, not a universal guarantee

When no binary package exists, [`pig build`](/build/) can apply maintained build specifications on a suitable build host. Success still depends on the upstream source, compiler and language toolchains, system libraries, network inputs, target PostgreSQL version, and architecture. The resulting package must be tested on the target combination; a local successful build is not by itself a reproducibility or support guarantee.

### Automation guarantees are command-specific

PIG offers structured output, confirmation prompts, and `--plan` on supported workflows. Those guarantees are not identical across every command: some commands wrap older tools, `pig pt` deliberately passes arguments through to `patronictl`, and interactive or third-party commands retain their own output and failure semantics. Automation should pin the PIG version, check exit status, avoid parsing human-oriented output, and use documented structured modes where available.

## Linux Compatibility

The current packaged repository matrix covers **eight Linux distribution majors**, each on `x86_64` and `aarch64` (16 OS/architecture targets). The catalog targets the five supported PostgreSQL majors **14-18**. Availability still varies by extension and target cell.

| OS code | Distribution family | Release line | Architectures | Current context (August 2026) |
|:---|:---|:---|:---|:---|
| `el8` | RHEL-compatible | EL 8 | x86_64, aarch64 | Maintenance phase; Rocky Linux 8 support runs to 2029 |
| `el9` | RHEL-compatible | EL 9 | x86_64, aarch64 | Supported |
| `el10` | RHEL-compatible | EL 10 | x86_64, aarch64 | Supported |
| `d12` | Debian | Debian 12 | x86_64, aarch64 | Oldstable/LTS track |
| `d13` | Debian | Debian 13 | x86_64, aarch64 | Stable release |
| `u22` | Ubuntu | Ubuntu 22.04 LTS | x86_64, aarch64 | Standard security maintenance through May 2027 |
| `u24` | Ubuntu | Ubuntu 24.04 LTS | x86_64, aarch64 | Standard security maintenance through May 2029 |
| `u26` | Ubuntu | Ubuntu 26.04 LTS | x86_64, aarch64 | Standard security maintenance through May 2031 |
{.full-width}

Lifecycle context comes from the [Rocky Linux version guide](https://wiki.rockylinux.org/rocky/version/), [Debian release information](https://www.debian.org/releases/), and [Ubuntu release cycle](https://ubuntu.com/about/release-cycle). A vendor-supported operating system is not automatically a PIG package target, and old aliases or detection code in the binary do not imply current hosted repository coverage. In particular, EL 7 and Debian 11 are not part of the current 16-target extension matrix.

PostgreSQL's own [versioning policy](https://www.postgresql.org/support/versioning/) currently lists 14-18 as supported majors; PostgreSQL 14 reaches end of life in November 2026. Pre-release PostgreSQL branches such as 19 require explicit testing and should not be inferred from the stable package matrix.

## Practical Adoption Checklist

Before treating PIG as part of a production software-supply workflow:

1. Run `pig status` and `pig ext avail NAME` on the exact target OS, architecture, and PostgreSQL major.
2. Inspect package provenance, version, license, dependencies, and repository trust settings.
3. Decide whether `repo add` or the replacement semantics of `repo set` match local configuration ownership.
4. Separate host package installation from database activation, preload, restart, and SQL migration steps.
5. Test installation, upgrade, rollback, backup, and restore on the same target combination.
6. Pin versions and use plan/structured-output modes where the specific command supports them.

PIG removes a great deal of repetitive packaging work. It is most valuable when its catalog and repository coverage match the target fleet—and most predictable when operators keep the package, database, and production-validation layers explicit.
