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

PIG provides commands to find, install, and build PostgreSQL extension packages. It also manages PostgreSQL, Patroni, pgBackRest, and Pigsty workflows. Package installation uses the system's `apt`, `dnf`, or `yum`.

## Start here

| Your task | Page |
|:---|:---|
| Install PostgreSQL and enable your first extension | [Getting started](/start/) |
| Learn what PIG does and which platforms it supports | [Introduction](/intro/) |
| Download, install, update, or remove PIG | [Installation](/install/) |
| Look up commands, options, and automation features | [Command reference](/cmd/) |

## Install PostgreSQL and extensions

On a Linux host with root or `sudo` access, run:

```bash
curl -fsSL https://repo.pigsty.io/pig | bash
sudo pig repo add pgsql --update
sudo pig install -v 18 pg18 vector
```

In mainland China, use `https://repo.pigsty.cc/pig` for the installer. These commands install PostgreSQL 18 and pgvector packages. Continue with [Getting started](/start/) to start a test instance and enable the extension with `CREATE EXTENSION vector`.

## Command reference

| Task | Command |
|:---|:---|
| Configure APT/DNF repositories | [`pig repo`](/repo/) |
| Query the catalog, install, or update extension packages | [`pig ext`](/ext/), [`pig install`](/cmd/#pig-install) |
| Build extension packages from source | [`pig build`](/build/) |
| Manage local PostgreSQL instances and databases | [`pig pg`](/pg/) |
| Manage Patroni clusters through patronictl | [`pig pt`](/pt/) |
| Inspect or reload pg_exporter | [`pig pe`](/pe/) |
| Back up and restore with pgBackRest | [`pig pb`](/pb/) |
| Run point-in-time recovery | [`pig pitr`](/pitr/) |
| Install and configure Pigsty, manage Grafana | [`pig sty`](/sty/) |
| Read, edit, and validate Pigsty inventory | [`pig inventory`](/inventory/) |
| Run Pigsty administration playbooks | [`pig do`](/do/) |
| Collect host, database, and backup status | [`pig context`](/cmd/#pig-context) |

Run `pig help <command>` for command help. For automation, use `pig -o json --help` to inspect command capabilities, then select the relevant output and plan options.

## Find more information

Press {{< kbd "Ctrl" "K" >}} ({{< kbd "⌘" "K" >}} on macOS) to search the site. Press {{< kbd "/" >}} for page actions. An AI assistant action sends the public page URL and a reading prompt to the selected service.

- [Design Records](/design/): implementation decisions, trade-offs, and proposals.
- [Release notes](/release/): changes and download files for each version.
- [Extension catalog](https://pigsty.io/ext/list/): extension descriptions and package information.
- [GitHub Issues](https://github.com/pgsty/pig/issues): report a problem or request a feature.

PIG is developed by [Vonng](https://vonng.com/en/) and released under [Apache 2.0](https://github.com/pgsty/pig/blob/main/LICENSE). [Pigsty](https://pigsty.io/) provides PostgreSQL deployment, monitoring, backups, and high availability.
