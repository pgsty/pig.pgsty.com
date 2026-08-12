---
title: "PIG Documentation"
linkTitle: "Docs"
description: "Install, manage, and build PostgreSQL and its extensions with the pig CLI."
search_keywords: [pig, PostgreSQL, extension, package manager, CLI]
search_boost: 1.5
weight: 1
type: docs
icon: fa-solid fa-book
# 根下拉已经把「文档」列为当前文档集，树里不必再出现一次。
toc_root: true
---

— **Packager Index Gateway, a PostgreSQL extension package manager**

PIG is a self-contained Go command-line tool for installing, managing, and building PostgreSQL extension packages and for selected PostgreSQL/Pigsty operations. It delegates package transactions to the native operating-system tools.
PIG is not a reinvented wheel, but rather a **PiggyBack** - a high-level abstraction layer that leverages existing Linux distribution package managers (`apt`/`dnf`).
Its catalog maps operating systems, CPU architectures, and PostgreSQL majors to native package names, allowing you to install PG kernels and query {{< param pgext_count >}} packaged extension entries through a consistent CLI. Availability still varies by target combination.

Many PIG-native workflows are automation-friendly: when the specific command documents support, use structured output, `--plan`, confirmation controls, and defined result codes. Passthrough, interactive, and streaming commands retain their upstream or terminal-oriented behavior.

Please note: for extension installation, **pig is not a mandatory component**. You can still use apt/dnf package managers to directly access the [**Pigsty PGSQL**](https://pigsty.io/docs/repo/pgsql/) repository.

Open search and page actions with {{< kbd "Ctrl" "K" >}} ({{< kbd "⌘" "K" >}} on macOS), or press {{< kbd "/" >}} to jump straight to commands.

Assistant actions open ChatGPT or Claude only when you select them. They pass the current page's public URL and a reading prompt to that third-party service; PIG does not send the page body automatically.

- [**Introduction**](/intro/): Why do we need a dedicated PG package manager?
- [**Getting Started**](/start/): Quick start guide and examples
- [**Installation**](/install/): Download, install, and update pig

## Quick Start

{{% steps %}}

### Install pig

Use the default Cloudflare-backed installer:

```bash
curl -fsSL https://repo.pigsty.io/pig | bash
```

In mainland China, use the mirror endpoint:

```bash
curl -fsSL https://repo.pigsty.cc/pig | bash
```

See [Installation](/install/) for packages, release archives, upgrades, and removal.

### Configure package repositories

On Linux, register the Pigsty and PGDG repositories once. Review the generated configuration before accepting the overwrite:

```bash
pig repo set
```

### Install PostgreSQL and extensions

Install the PostgreSQL 18 kernel plus the [`pg_duckdb`](https://pigsty.io/ext/e/pg_duckdb) and `vector` extension packages:

```bash
pig install -y pg18 pg_duckdb vector
```

{{% /steps %}}

These commands install host packages. Use `pig ext info NAME` and each extension's documentation to complete preload, restart, `CREATE EXTENSION`, and SQL upgrade steps in every intended database. Continue with the full [Getting Started](/start/) tutorial for catalog, alias, and inspection workflows.

## Command Reference

Run `pig help <command>` to get detailed help for subcommands.

**Extension Management:**

- [**pig repo**](/repo/): Manage software repositories
- [**pig ext**](/ext/): Manage PG extensions
- [**pig build**](/build/): Build extensions from source
- [**pig install**](/cmd/#pig-install): Install PostgreSQL and extension packages through the native package manager

**Pigsty Management:**

- [**pig sty**](/sty/): Manage Pigsty installation and Grafana dashboards
- [**pig inventory**](/inventory/): Inspect, edit, validate, and exchange the Pigsty inventory
- [**pig context**](/cmd/#pig-context): Collect host, PostgreSQL, Patroni, pgBackRest, and extension context
- [**pig pg**](/pg/): Manage local PostgreSQL server
- [**pig pt**](/pt/): Run patronictl transparently to manage Patroni HA clusters
- [**pig pb**](/pb/): Manage pgBackRest backup & restore
- [**pig pitr**](/pitr/): Point-in-time recovery workflow

## About

The `pig` CLI tool is developed by [Vonng](https://vonng.com/en/) (rh@vonng.com) and is open-sourced under the [Apache 2.0](https://github.com/pgsty/pig/blob/main/LICENSE) license.

You can also check out the [**PIGSTY**](https://pgsty.com) project, which provides a complete PostgreSQL RDS DBaaS experience including extension delivery.

- [**PGEXT**](https://github.com/pgsty/pgext): Extension data and management tools
- [**PIG**](https://github.com/pgsty/pig): PostgreSQL package manager
- [**PIGSTY**](https://github.com/pgsty/pigsty): Batteries-included PostgreSQL distribution
