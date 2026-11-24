---
title: "PostgreSQL 19 Lifecycle Window and Default Major Decoupling"
linkTitle: "PostgreSQL 19 Lifecycle"
date: 2026-11-21
lastmod: 2026-11-24
description: "Advance the active PostgreSQL support window to 15-19 on GA while keeping 18 as the default major and preserving explicit legacy operations."
tags: [ext, repo, build, sty]
weight: 98
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-11-21<br>
> **Status:** Implemented (verified in source and local tests above [`v1.11.0`](https://github.com/pgsty/pig/releases/tag/v1.11.0); not yet published in a release).<br>
> **Current reference:** [`pig ext`](/ext/), [`pig repo`](/repo/), [`pig build`](/build/), [`pig sty`](/sty/), [`pig pg tune`](/pg/#pg-tune)<br>
> **Scope:** Active PostgreSQL major window, default major selection, legacy explicit version operations, repository modules, build toolsets, Pigsty template mutations, and version-gated tuning parameters.

## Decision {#decision}

Promote PostgreSQL 19 from Beta to the active support window (`19, 18, 17, 16, 15`) and retire
end-of-life PostgreSQL 14 from active lifecycle defaults, availability matrices, repository
bundles, build toolsets, and Pigsty template configuration.

Decouple the recommended default major (`PostgresDefaultMajorVersion = 18`) from the newest active
major (`PostgresLatestMajorVersion() = 19`). Commands that previously fell back to the newest
active major when no local PostgreSQL installation or explicit `-v` flag was present now resolve to
PostgreSQL 18.

Retain retired majors (`10–14`) as explicitly addressable legacy versions for package installation,
extension management, dynamic category aliases, local installation discovery, and protected kernel
removal, without keeping EOL repositories in the bundled repository definitions.

## Context {#context}

In [`v1.11.0`](https://github.com/pgsty/pig/releases/tag/v1.11.0) (commit
[`365bf12`](https://github.com/pgsty/pig/commit/365bf1282fdb)), PIG modeled `18, 17, 16, 15, 14` as
active stable majors and `19` as a Beta target. Multiple subsystems coupled implicit default
selection directly to `PostgresLatestMajorVersion()`:

- `pig install`, `pig ext add/rm/update/import`, and unversioned `pgsql-<category>` aliases defaulted
  to the highest active version (`18`) only because `19` was still outside the active slice.
- `pig sty conf -v 19` injected the `beta` repository module and emitted Beta warnings.
- `cli/repo/assets/repo.yml` pointed PG 19 at `testing` repositories and included EOL `pgdg14` and
  `pgdg14-nonfree`, while upstream PGDG published GA `yum/19` repositories for RHEL 9 and 10 only
  (dropping RHEL 8 and Debian 11 for PostgreSQL 19).
- `pig pg tune` emitted `io_workers` for every `pgVersion >= 18`, even though PostgreSQL 19 removed
  static `io_workers` in favor of `io_min_workers` and `io_max_workers`.

Advancing the active list to include `19` without decoupling the default major or gating `el8` and
`io_workers` would silently switch unpinned installs to PostgreSQL 19, break `pig build tool` on
EL 8, and emit invalid PostgreSQL 19 configuration lines.

## Alternatives considered {#alternatives}

- **Advance the default major immediately to PostgreSQL 19.** Rejected because third-party extension
  coverage and Pigsty configuration templates still target PostgreSQL 18 by default during early
  PostgreSQL 19 adoption.
- **Keep PostgreSQL 14 in the active window and `pgdg` repository module.** Rejected because
  PostgreSQL 14 has reached upstream end of life; keeping it in `pgdg` and `build tool` adds
  unneeded repository metadata and build dependencies on every fresh host.
- **Drop `10–14` from alias generation and `-v` resolution completely.** Rejected because operators
  managing existing PostgreSQL 14 (or older) hosts still need `pig ext`, `pig pg`, `pg14*` aliases,
  and kernel removal safeguards to work when compatible repositories or local installations exist.
- **Remove the `beta` repository module and `--beta` flags outright, or leave `beta` empty until
  PG 20 Beta1.** Rejected because PGDG already publishes PostgreSQL 20 testing repositories for
  EL 9/10 (`yum/testing/20`) and exposes component `20` in `pgdg-testing` for Debian 12/13 and
  Ubuntu 22/24/26; advancing the opt-in Beta target directly to PostgreSQL 20 keeps `beta`,
  `--beta`, `pg20*` aliases, and `pig sty conf -v 20` immediately usable for PG 20 testing while
  leaving `beta` safely empty on unsupported `el8` and `d11`.

## Contract {#contract}

- **Version tiers & platform bounds (`cli/ext`):**
  - `PostgresActiveMajorVersions` is `[19, 18, 17, 16, 15]`.
  - `PostgresDefaultMajorVersion` is `18`; `PostgresBetaMajorVersion` advances to `20` (PG 20
    testing/devel).
  - `PostgresLegacyMajorVersions` is `[14, 13, 12, 11, 10]`.
  - `SupportsOSPG(osCode, ver)` centralizes the OS × PostgreSQL compatibility boundary (`el8` and
    `d11` stop at PG 18; `el7` stops at PG 15) across `cli/ext`, `cli/build`, and `cli/sty`.
- **Implicit defaults vs. explicit targets:**
  - When no active `pg_config` is detected and `-v` is omitted, `pig install`,
    `pig ext add/rm/update/import`, unversioned `pgsql-<category>` aliases, and `pig pg tune`
    fall back to `18`.
  - Local `DetectPostgres()` installation discovery prefers the highest installed major (for example,
    an installed PostgreSQL 19 instance takes precedence when multiple versions exist and none is on
    `PATH`) while still discovering `10–14` installations.
  - Numbered static aliases (`pg10*`–`pg20*`), dynamic category aliases (`pg10-<cate>`–`pg20-<cate>`),
    and protected removal checks cover all known majors (`10–20`), with Beta `pg20-<cate>` borrowing
    the PG 19 PGDG-origin matrix.
- **Catalog & availability matrices (`cli/ext`):**
  - Embedded `extension.csv` is refreshed to the `2026-11-24` 627-entry snapshot, adding PostgreSQL 19
    contrib entries `pg_plan_advice` (controlless shared library, `need_ddl=false`) and
    `pg_stash_advice` (`need_ddl=true`), along with live native PostgreSQL 15–19 availability matrices
    (`32,923` available, `160` missing, and `3,477` not-applicable cells).
  - `pig ext avail` text and structured outputs filter matrix summaries and entries to the active
    `15–19` window (`80` cells across 8 OS releases × 2 architectures × 5 active majors). Single-extension
    tables render `PkgNA` (`N`) cells as dimmed `n/a` (distinct from blank `M` missing cells), while
    global `pig ext avail` displays only OS-supported active majors (`15–18` on `el8`, `15–19` on
    EL 9/10 and Debian/Ubuntu).
  - Active majors (`15–19`) use exact native matrix cells (`el8` has no PG 19 packages and never
    borrows PG 18). Retired majors (`10–14`) remain explicitly operable for direct extension packages,
    static aliases (`pg14*`), and removal safeguards; dynamic category aliases fall back to non-fork
    `rpm_pg`/`deb_pg` declarations when present in a catalog (the refreshed PG 15–19 catalog no longer
    declares PG 14 entries).
- **Repositories (`cli/repo`):**
  - Add `pgdg19` for EL 9 and EL 10 (`x86_64`, `aarch64`) across `default`, `china`, and `europe`
    mirrors; filter module memberships per OS/arch so EL 9/10 `pgdg` contains `pgdg-common` plus
    `pgdg19`–`pgdg15`, EL 8 `pgdg` omits `pgdg19`, and EL 7 `pgdg` contains `pgdg-common` and `pgdg15`.
  - Remove `pgdg14`, `pgdg14-nonfree`, and `pgdg19-beta`; align `pgdg15-nonfree` through
    `pgdg18-nonfree` on `skip_if_unavailable=1`.
  - Advance the `beta` module to PostgreSQL 20 testing: `pgdg20-beta` (`yum/testing/20`, EL 9/10,
    `x86_64`/`aarch64`, `module_hotfixes=1`) and `pgdg-beta` (`${distro_codename}-pgdg-testing main 20`,
    Debian 12/13 and Ubuntu 22/24/26, `x86_64`/`aarch64`). On `el8`, `el7`, and `d11` where PG 20
    testing is unavailable, `beta` remains an empty compatibility module (`[]`) that writes no
    repository file, omits `file_path` in structured results, returns a clean empty result from
    `pig repo info beta`, does not interfere with replacement rollback, and fails closed before
    backing up active repositories when `pig repo set` selects only empty modules.
- **Build & Pigsty configuration (`cli/build`, `cli/sty`, `cmd`):**
  - `pig build tool` installs server/devel packages for `15–19` on EL 9/10 and `15–18` on EL 8
    (plus `openssl-devel` across EL 8/9/10), and gates future Beta packages through `SupportsOSPG`.
  - `pig build pgrx` defaults to `cargo-pgrx 0.20.1`, resolves Cargo across `CARGO_HOME`,
    `~/.cargo/bin/cargo`, and `PATH`, validates OS-compatible `--pg` targets, and fails fast when
    requested or auto-detected Linux `pg_config` paths are absent.
  - `pig build dep`, `pig build ext`, and `pig build pkg` validate `--pg` against OS-supported
    installable majors, pick OS-compatible `rpm_pg`/`deb_pg` defaults (for example, PG 18 on `el8`),
    fail fast when an extension resolves to zero compatible targets, propagate explicit `--pg`
    environment variables (`PG_VERSIONS`, `PG_SUPPORTED_VERSIONS`, and single-major `PG_MAJOR` /
    `PG_CONFIG`) to Debian `make` builds, and update `libpgfeutils` sources to PG 15–19 (`15.20`–`19.0`).
  - `pig build repo --beta`, `pig build tool --beta`, and `pig build pgrx --beta` target PostgreSQL 20
    testing/beta on supported platforms (EL 9/10, Debian 12/13, Ubuntu 22/24/26; safely skipped on
    `el8` and `d11`).
  - `pig sty conf` accepts `-v` in `15–19` plus explicit `20` beta (reporting `19|18|17|16|15 (beta: 20)`
    in help output), rewrites generic templates to PostgreSQL 19 without injecting `beta`, injects
    `beta` and emits a Beta warning for PostgreSQL 20, and emits a non-fatal warning when configuring
    PG 19 or 20 on a Linux `el8` host.
- **Parameter tuning (`cli/postgres`):**
  - `pig pg tune` emits `io_workers` only when `pgVersion == 18`, omitting it on PostgreSQL 19+.

## Consequences {#impact}

PostgreSQL 19 packages, extensions, build environments, and Pigsty configurations work out of the
box on EL 9/10, Debian 12/13, and Ubuntu 22.04/24.04/26.04 without Beta flags, while default
installations and templates remain anchored on PostgreSQL 18. EL 8 hosts continue to build and
install PostgreSQL 15–18 cleanly without requesting nonexistent `postgresql19-*` RPMs. Existing
PostgreSQL 14 environments retain explicit CLI operability when their repositories remain configured
on the host, while new hosts no longer pull EOL PostgreSQL 14 repository definitions.

Because user-cached `~/.pig/extension.csv` and `~/.pig/repo.yml` take precedence over embedded
assets when present, publishing updated remote catalog files alongside the binary release is
required for existing installations running `pig repo reload` or `pig ext reload`.

## Verification and evolution {#verification}

Implemented in PIG commits
[`b36d683`](https://github.com/pgsty/pig/commit/b36d683585c3),
[`461339c`](https://github.com/pgsty/pig/commit/461339ceb7a6),
[`a7061b1`](https://github.com/pgsty/pig/commit/a7061b14ef0e),
[`52847f4`](https://github.com/pgsty/pig/commit/52847f47155b),
[`ba77eac`](https://github.com/pgsty/pig/commit/ba77eacc1f3e),
[`9d16584`](https://github.com/pgsty/pig/commit/9d16584eda9f), and
[`9bf3093`](https://github.com/pgsty/pig/commit/9bf3093f8e10)
and verified locally with:

- `git diff --check`, `go vet ./...`, `go mod verify`, `make gr-check`, `actionlint`, and `govulncheck ./...`
- `go test -shuffle=on -count=1 ./...` (26/26 packages)
- `go test -race -shuffle=on -count=1 ./cli/ext ./cli/repo ./cli/build ./cli/sty ./cli/postgres`
  and CI `./cmd` race regressions (`-count=3` on both CI shuffle seeds)
- `staticcheck ./...`, `golangci-lint run --enable-only gocognit,gocyclo --tests=false`, and `deadcode ./...`
- `make docs-check` (Hugo build, `bin/check_markdown.py`, `bin/check_design.py`, and `bin/check_internal_links.py`)

When PostgreSQL 20 reaches GA, advance `PostgresActiveMajorVersions` to `[20, 19, 18, 17, 16]` and
retarget `PostgresBetaMajorVersion` and `beta` repositories to PostgreSQL 21 testing.

## Current status {#status}

Implemented in source commits [`b36d683`](https://github.com/pgsty/pig/commit/b36d683585c3)–[`9bf3093`](https://github.com/pgsty/pig/commit/9bf3093f8e10)
and companion documentation; not yet published in a tagged binary release or deployed to remote
catalog endpoints. See the [release notes](/release/) for published binary releases.
