---
title: "pig do"
description: "Run bounded Pigsty administrative playbook tasks with pig do"
weight: 155
icon: fas fa-list-check
categories: [Reference]
tags: [sty, cli]
---

`pig do` exposes common Pigsty administrative playbooks as explicit CLI operations. It uses the
selected Pigsty home and Inventory, builds the corresponding playbook command, and returns the
operation through PIG's legacy structured-result adapter.

These commands change remote systems. Review the selected cluster, node, instance, and Inventory
before execution. The command family does not provide a general `--plan` mode.

```bash
pig do pgsql-add  pg-test 10.10.10.12     # add one PostgreSQL instance
pig do pgsql-rm   pg-test 10.10.10.12     # remove one PostgreSQL instance
pig do pgsql-db   pg-meta app             # create or update a database
pig do pgsql-user pg-meta dbuser_app      # create or update a user
pig do node-pkg   pg-meta restic          # install a package on selected nodes
pig do redis-add  redis-meta              # initialize a Redis cluster
```

## Command overview

| Command | Purpose | Required arguments |
|:---|:---|:---|
| `pgsql-add` | Add a PostgreSQL cluster or instances | cluster, optional IPs |
| `pgsql-rm` | Remove a PostgreSQL cluster or instances | cluster, optional IPs |
| `pgsql-db` | Create or update a database declaration | cluster, database |
| `pgsql-user` | Create or update a user declaration | cluster, user |
| `pgsql-ext` | Install extensions through Pigsty | cluster, optional extensions |
| `pgsql-hba` | Refresh PostgreSQL HBA rules | cluster |
| `pgsql-svc` | Refresh PostgreSQL service definitions | cluster |
| `pgmon-add` / `pgmon-rm` | Add or remove a remote monitoring target | cluster |
| `node-add` / `node-rm` | Add or remove selected nodes | one or more selectors |
| `node-repo` | Configure repository modules on selected nodes | optional selector and modules |
| `node-pkg` | Install or update packages on selected nodes | selector, optional packages |
| `repo-build` | Rebuild the Pigsty infrastructure repository | none |
| `redis-add` / `redis-rm` | Add or remove Redis clusters, nodes, or instances | selector, optional ports |
{.full-width}

Run `pig do COMMAND --help` for the aliases and exact examples of one operation.

## PostgreSQL operations

```bash
pig do pgsql-add pg-meta                  # initialize the declared cluster
pig do pgsql-add pg-test 10.10.10.12      # add one declared replica
pig do pgsql-rm pg-test 10.10.10.13       # remove one instance
pig do pgsql-rm pg-test --uninstall       # also uninstall packages during removal
pig do pgsql-db pg-meta meta              # create or update database meta
pig do pgsql-user pg-meta dbuser_view     # create or update a user
pig do pgsql-ext pg-meta postgis vector   # install extension packages
pig do pgsql-hba pg-meta                  # refresh pg_hba rules
pig do pgsql-svc pg-meta                  # refresh PostgreSQL services
```

`pgsql-rm --uninstall` expands the removal scope to packages. Treat it as a separate destructive
decision and verify that the selected hosts no longer need those packages.

## Node and repository operations

Selectors may be cluster names, host names, IP addresses, or another selector form supported by
the Pigsty playbook. Their meaning comes from the active Inventory.

```bash
pig do node-add pg-test                    # add nodes selected by cluster
pig do node-rm 10.10.10.13                 # remove one selected node
pig do node-repo pg-meta node,infra        # configure selected repo modules
pig do node-pkg pg-meta openssh restic     # install or update packages
pig do repo-build                          # rebuild the infra repository
```

Repository modules include the modules provided by the installed Pigsty release, such as `local`,
`infra`, `pgsql`, `node`, and `extra`. Check that the required repositories are available to the
target nodes before installing packages.

## Redis operations

```bash
pig do redis-add redis-meta                # initialize a declared Redis cluster
pig do redis-add 10.10.10.11 6379 6380     # add selected instances
pig do redis-rm 10.10.10.11 6379           # remove one selected instance
pig do redis-rm redis-test --uninstall     # remove and uninstall packages
```

As with PostgreSQL removal, `redis-rm --uninstall` broadens the change beyond service removal.

## Configuration and output

`pig do` uses the global PIG options:

| Option | Purpose |
|:---|:---|
| `-H, --home` | Select the Pigsty home directory |
| `-i, --inventory` | Select the Pigsty Inventory |
| `-o, --output` | Choose text, JSON, YAML, or pretty JSON result wrapping |
| `--log-level`, `--log-path` | Configure PIG diagnostics |
{.full-width}

Structured mode reports the requested operation and captured execution result. The underlying
Ansible and playbook behavior is still determined by the installed Pigsty release.

## Operational boundary

`pig do` is a convenience layer over Pigsty administration playbooks. It does not replace
Inventory review, backups, change windows, or post-change service verification. For full playbook
variables and lifecycle semantics, use the documentation for the installed
[Pigsty release](https://pigsty.io/docs/).
