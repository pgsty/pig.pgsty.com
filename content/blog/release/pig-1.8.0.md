---
title: "pig v1.8.0"
linkTitle: "v1.8.0"
date: 2026-08-14
author: "Ruohang Feng"
description: "Native pig sty boot and pig sty conf workflows, with 575 packaged PostgreSQL extensions."
categories: [release]
tags: [Release, pig]
weight: 1
---

Pig `v1.8.0` makes Pigsty controller setup native. The two core setup commands,
`pig sty boot` and `pig sty conf`, are now failure-aware Go workflows instead of
wrappers around the legacy `bootstrap` and `configure` shell scripts. The release
keeps the public catalog total at **575 packaged PostgreSQL extensions** and embeds
Pigsty `4.5.0`.

## Native `pig sty boot`

- Bootstraps the controller end to end: repairs the Debian 12/13 locale when needed,
  verifies Ansible and its Python dependencies, installs controller packages, repairs
  localhost SSH on a best-effort basis, and can initialize a missing `~/pigsty` tree.
- Supports online repositories, an explicit local package or HTTP(S) URL, a trusted
  automatically discovered offline package, and an already prepared `/www/pigsty`
  repository.
- Backs up replaced repository definitions and restores them when package setup fails.
  Explicit offline-input errors are hard failures, while optional final conveniences
  are reported as warnings. JSON and YAML output expose the selected mode, repository
  policy, rollback state, warnings, and recommended next commands.

## Native `pig sty conf`

- Generates Inventory from a safe template below `<PIGSTY_HOME>/conf`, supports both
  `pig sty conf MODE` and `--conf MODE`, and can map up to ten ordered IPv4 addresses
  plus the exact `i.pigsty` placeholder domain.
- Adds deterministic interactive and non-interactive IP selection, structural proxy,
  region, PostgreSQL-version, and secret-generation mutations, followed by complete
  Inventory validation.
- Refuses source/output aliasing through direct paths, symlinks, symlinked parents, or
  hard links. A validated result is written atomically with mode `0600`; structured
  output reports generated secret identifiers but never their values.

## Other Updates

- EL8 and newer package operations consistently prefer DNF, local RPM requirements are
  resolved by provider capability, fresh repository bootstraps restore the expected
  `/www -> /data/nginx` layout, and self-update tolerates whitespace in the latest marker.
- The extension catalog, package versions, metadata, and availability matrices receive
  their routine refresh while the published PostgreSQL-extension count remains **575**.
- CI and release builds use Go `1.26.6`, pinned analysis tools and GoReleaser, dependency
  verification, workflow linting, vulnerability scanning, and a full release snapshot.

## Compatibility Notes

- `pig sty boot` no longer executes `<PIGSTY_HOME>/bootstrap`. Automation that relied on
  shell-script side effects should consume the native command result instead.
- `pig sty conf --raw` has been removed. Use the native workflow; `--conf MODE` remains
  available, with `pig sty conf MODE` as the equivalent positional form.
- `pig sty conf --ip` accepts up to ten comma-separated IPv4 addresses; `--skip` and
  `--ip` remain mutually exclusive.
- EL8 and newer use DNF. The limited EL7 compatibility catalog retains its separate
  legacy YUM path.

## Checksums

Artifacts: [GitHub Release](https://github.com/pgsty/pig/releases/tag/v1.8.0) · [checksums.txt](https://github.com/pgsty/pig/releases/download/v1.8.0/checksums.txt)

```bash
02fd2628810c1b00de730ece32b09dba1318be4c99a4ff1a0551740e32bf223b  pig-1.8.0-1.aarch64.rpm
72ba72a00af52a84b08b1346f85b42668b52bc097e315774ff9f501ca23ece8b  pig-1.8.0-1.x86_64.rpm
f023a5c9049dc532a057e932c73a8197683eaf4d97cb7a8f219492da1ad2a65f  pig-v1.8.0.darwin-amd64.tar.gz
e0ccf61c4d135dbc45359c207751092aeb6df788e826bb73eccc1a1ed8800998  pig-v1.8.0.darwin-arm64.tar.gz
a24a08c1b8d54adcdef5a99ed7b91caeedef1552a1440b1258eb4eb07fb20353  pig-v1.8.0.linux-amd64.tar.gz
9d23875804f87e78039498245059fd6b765831f027aacfc511ad0ac42711fa7b  pig-v1.8.0.linux-arm64.tar.gz
96259ff7584cd52254c91a9fd7d77bd577f23c55cb09f4bc995a3ca0fcbc7321  pig_1.8.0-1_amd64.deb
2e7370211514df6355ef96fb812670febe6ee1b85a28378432c33ebdaecb4b63  pig_1.8.0-1_arm64.deb
```

Release: https://github.com/pgsty/pig/releases/tag/v1.8.0
