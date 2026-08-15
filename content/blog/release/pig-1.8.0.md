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

`pig sty boot` is now one native, failure-aware controller bootstrap transaction. It does not
execute `<PIGSTY_HOME>/bootstrap`, and its HTTP download and archive extraction paths do not
depend on `curl`, `wget`, `tar`, or `gzip`.

### Privilege and readiness

- The command can be launched as an ordinary user. Pig resolves and downloads an explicit source
  before a single sudo re-exec; `PIG_NO_SUDO=1` disables elevation and
  `PIG_NON_INTERACTIVE=1` requests non-interactive sudo.
- On Debian 12/13, locale preparation is attempted before and, when useful, after controller
  package installation.
- Readiness is proven by executing `ansible-playbook`, discovering its Python interpreter, and
  checking `yaml`, `jmespath`, and either `cryptography` or `OpenSSL`. A present but unusable
  Ansible binary no longer produces a false success.

### Repository sources and transactions

- Source selection covers a local archive, an HTTP(S) URL, a permission-checked automatic
  `/tmp/pkg.tgz`, an already committed `/www/pigsty` repository, and regional online
  repositories. A bad explicit source is a hard error and never silently becomes an online boot.
- A completed `/www/pigsty` repository wins over a selected package. Pig can create the expected
  `/www -> /data/nginx` layout itself, uses restricted extraction for offline content, and enables
  only the strict `pigsty-local` repository in offline mode. Online setup installs the embedded
  Pigsty key and keeps repository signature checks enabled.
- The default overwrite policy backs up repository definitions and restores them when repository
  or package setup fails. `--keep` selects an additive policy and can retry a failed online
  refresh against existing definitions.
- The reported mode is explicit: `ready`, `offline`, `online`, or `existing`. An explicit,
  automatically discovered, or committed offline source is prepared even when Ansible is already
  usable.

### Finishing checks and automation

- Pig probes controller helpers, repairs key-based SSH to `127.0.0.1` for the invoking admin user,
  and initializes a missing `~/pigsty` from online or local content when possible.
- Locale, helper, localhost-SSH, and Pigsty-tree finishing failures are warnings. Invalid explicit
  input, repository/package failures, unsupported installation paths, and unusable post-install
  Ansible remain hard failures.
- JSON and YAML use the `pig.sty.boot/v2` result contract, including the selected mode and package
  manager, repository policy and rollback state, source paths, locale, SSH and initialization
  status, changes, warnings, and the next `conf`, `inventory`, and `deploy` commands.

## Native `pig sty conf`

`pig sty conf` is now a complete native Inventory compiler. It does not execute `./configure` or
fall back to raw Shell behavior: Pig resolves one template, performs bounded structural changes,
validates the full candidate, and only then commits the output.

### Safe configuration pipeline

- The default template is `conf/meta.yml`; a safe slash-separated relative mode may be supplied
  positionally or with `--conf`. Absolute paths, traversal, path escape, and source/output
  aliasing through direct paths, symlinks, symlinked parents, or hard links are rejected.
- Source parsing and IP-collision checks happen before external preflight. Parse, mutation,
  preflight, or validation failure leaves the destination unchanged.
- Pig performs native Inventory validation and, when available, a bounded `ansible-inventory`
  parse. Successful output is atomically written with mode `0600`.

### Structural Inventory changes

- Up to ten distinct `--ip` values map simultaneously to slots `10.10.10.10` through
  `10.10.10.19`; unrelated VIPs remain intact. Without `--ip`, interface selection is explicit
  and deterministic in interactive, non-interactive, and closed-input execution.
- `--domain` replaces only the exact `i.pigsty` token. Controllers with fewer than four CPUs are
  automatically switched from the `oltp` node and PostgreSQL tuning profiles to `tiny`.
- Region changes update `all.vars.region`; `china` activates Docker and pip mirrors already
  supplied by the template. `--proxy` materializes available proxy environment variables under
  `all.vars.proxy_env`.
- Generic templates support PostgreSQL 14-18 and explicit 19 beta, including matching locale and
  beta repository selection. Version-pinned `mssql`, `polar`, and `pgNN` modes keep their
  effective template version and emit a warning.
- `--generate` assigns one random 24-character value to each known credential identifier and
  updates active values and documented placeholders consistently. Result output lists generated
  identifiers but never secret values.

### Preflight and result contract

- Unless `--skip` is selected, preflight covers the platform, package manager, controller
  resources, sudo/admin access, localhost SSH, and Ansible availability. Build templates under
  `conf/build/` intentionally bypass IP mapping and admin preflight.
- JSON and YAML use `pig.sty.configure/v1` and report the template and output, selected and
  discarded addresses, requested and effective PostgreSQL versions, applied options, generated
  secret identifiers, and warnings.

## Other Updates

- EL8 and newer package operations consistently prefer DNF, local RPM requirements are resolved
  by provider capability, fresh repository bootstraps restore the expected `/www` layout, and
  self-update tolerates whitespace in the latest marker.
- The extension catalog, package versions, metadata, and availability matrices receive their
  routine refresh while the published PostgreSQL-extension count remains **575**.
- CI and release builds use Go `1.26.6`, pinned analysis tools and GoReleaser, dependency
  verification, workflow linting, vulnerability scanning, and a full release snapshot.

## Compatibility Notes

- `pig sty boot` no longer executes `<PIGSTY_HOME>/bootstrap`. Automation that relied on
  shell-script side effects should consume the native command and its structured result.
- `pig sty conf --raw` has been removed. Use the native workflow; `--conf MODE` remains
  available, with `pig sty conf MODE` as the equivalent positional form.
- `pig sty conf --ip` accepts up to ten comma-separated IPv4 addresses; `--skip` and `--ip`
  remain mutually exclusive. Uppercase `-O` chooses the Inventory file, while global lowercase
  `-o` chooses the command output format.
- EL8 and newer use DNF. The limited EL7 compatibility catalog retains its separate legacy
  YUM path.

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
