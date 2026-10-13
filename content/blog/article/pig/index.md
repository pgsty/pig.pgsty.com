---
title: Pig, The Postgres Extension Wizard
linkTitle: "Pig - The Postgres Extension Wizard"
date: 2024-12-29
lastmod: 2026-10-13
authors: [Vonng]
description: Why would we need yet another package manager for PostgreSQL & extensions?
tags: [cli, ext, repo, postgres]
---

PIG is a Go command-line tool for installing PostgreSQL and extensions through the system package
manager. It selects packages for the operating system, CPU architecture, and PostgreSQL version,
then uses APT, YUM, or DNF to install them.

The extension repository supplies native RPM and DEB packages, including TimescaleDB, Citus,
pgvector, and Rust extensions. It follows PGDG packaging conventions so these packages can be used
with the standard PostgreSQL packages.

I built PIG to make that repository easier to use. You can search by extension name, inspect its
metadata, and install the matching package without assembling package names yourself.

[PIG v0.1 release](https://github.com/pgsty/pig/releases/tag/v0.1.0) ·
[Source code](https://github.com/pgsty/pig) ·
[The ideal way to deliver PostgreSQL extensions](/article/pg-ext-repo/)

-------

## Get Started

Install the `pig` package with the installer or the system package manager.

```bash
curl -fsSL https://repo.pigsty.io/pig | bash
```

Then it's ready to use; assume you want to install the [`pg_duckdb`](https://pigsty.io/ext/e/pg_duckdb/) extension:

```bash
$ pig repo add pigsty pgdg -u  # add pgdg & pigsty repo, update cache
$ pig repo set -u              # replace the existing repository configuration

$ pig ext install pg17         # install native PGDG PostgreSQL 17 kernels packages
$ pig ext install pg_duckdb    # install the pg_duckdb extension (for current pg17)
```

### Extension management

```bash
pig ext list    [query]      # list & search extension
pig ext info    [ext...]     # get information of a specific extension
pig ext status  [-v]         # show installed extension and pg status
pig ext add     [ext...]     # install extension for current pg version
pig ext rm      [ext...]     # remove extension for current pg version
pig ext update  [ext...]     # update extension to the latest version
pig ext import  [ext...]     # download extension to local repo
pig ext link    [ext...]     # link postgres installation to path
pig ext build   [ext...]     # setup building env for extension
```

### Repository management

```bash
pig repo list                    # available repo list             (info)
pig repo info   [repo|module...] # show repo info                  (info)
pig repo status                  # show current repo status        (info)
pig repo add    [repo|module...] # add repo and modules            (root)
pig repo rm     [repo|module...] # remove repo & modules           (root)
pig repo update                  # update repo pkg cache           (root)
pig repo create                  # create repo on current system   (root)
pig repo boot                    # boot repo from offline package  (root)
pig repo cache                   # cache repo as offline package   (root)
```

---

> Originally published on [vonng.com](https://vonng.com/en/pg/pig/).
