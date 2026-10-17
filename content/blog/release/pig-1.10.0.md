---
title: "pig v1.10.0"
linkTitle: "v1.10.0"
date: 2026-10-17
description: "603 catalog entries, verified PostgreSQL targets, safer recovery and fork operations, faithful Inventory handling, and consistent automation results."
tags: [postgres, inventory, catalog, cli]
weight: 0
authors: [Vonng]
draft: false
release_url: https://github.com/pgsty/pig/releases/tag/v1.10.0
---

Pig `v1.10.0` strengthens the correctness and safety of existing commands. It verifies PostgreSQL
targets before operations, preserves Inventory sources and YAML types, and makes repository,
extension, and automation results match the work actually performed. The bundled catalog grows
from **600 to 603 records**. Embedded Pigsty remains `4.5.0`; the default `cargo-pgrx` remains `0.19.3`.

## PostgreSQL targets and maintenance

- An explicit `-D` binds `psql`, `ps`, `kill`, `vacuum`, `analyze`, `freeze`, and `repack` to the
  selected instance, including `--all` database enumeration. PIG validates the PID, data directory,
  port, socket, and process identity before starting the SQL client. Invalid, stale, copied, or
  uncertain runtime metadata causes failure instead of a fallback to another instance.
- Without `-D`, those SQL commands retain native client connection defaults. `pg clone` and
  `pg fork` retain their own port options. Promotion timeline checks use the selected instance
  or its control data; an unresolved timeline is left unknown.
- Plans and confirmation retry commands preserve the selected data directory, PostgreSQL version,
  operating-system user, and maintenance options. `VACUUM FULL` plans correctly require confirmation.
- Maintenance operands are literal database names. Values containing `=` or beginning with
  `postgres://` or `postgresql://` are rejected before planning or execution, without echoing
  the value. Spaces and non-ASCII names remain supported. Generated commands put names after
  `--`, so a database named `--all` cannot become a command option.
- `vacuum`, `analyze`, and `freeze --all` validate the complete database list before maintenance
  begins. Use native clients when a connection string or a database name rejected by this boundary is required.

See [`pig pg`](/pg/#global-options) for target selection and
[maintenance commands](/pg/#database-maintenance-commands) for database-name rules.

## Runtime state, recovery, and fork safety

- Permission failures, malformed PID metadata, and unavailable process identity are reported as
  errors or unknown state. They cannot authorize forced initialization, restore, or fork replacement.
  `pg status` returns `130201` (exit `3`) for permission failures and `130808` (exit `1`) for
  other runtime-probe failures. Plans report an unresolved precondition as `unknown`.
- Declining PITR confirmation or reaching EOF returns `161001` (exit `7`) before any service stop,
  restore, or startup. An unknown state cannot supply a PID for forced termination or count as
  successful startup. Post-restore SQL checks require a verified target.
- Replacing a nonempty unmanaged fork requires valid ownership metadata with a matching explicit
  target path. Missing, damaged, or mismatched metadata cannot authorize deletion. Existing
  protections for running targets and source/destination relationships remain in force.
- Clone and fork path checks run as the selected database operating-system user when needed,
  supporting private `0700` data directories. An inaccessible or unresolved path cannot bypass
  validation. Managed orphan cleanup remains available through the managed fork name.
- Files written as the database user use private sibling staging and exact-target replacement.
  The new file has `0600` permissions; directory or symlink targets are refused, and replacement
  does not overwrite the contents of another hard link to the old file.

The [PITR reference](/pitr/) explains the managed recovery workflow;
[`pig pb restore`](/pb/#pb-restore) remains a separate restore primitive.

## Inventory and Pigsty

- `sty deploy` and `do` pass the resolved Inventory path explicitly to Ansible. Flag and environment
  paths resolve from the caller's working directory; quoted `~/` paths expand before resolution.
  A selected missing or invalid source does not silently fall back to another inventory.
- `pg_users[].roles` preserves both role-name strings and structured grants, including grant state
  and optional `admin`, `set`, and `inherit` attributes.
- Editing, serialization, and CMDB export retain strings that YAML consumers might otherwise
  interpret as numbers, dates, or timestamps. Existing timestamp scalars retain their original
  source representation. Independent PyYAML checks verify the emitted string types.
- `sty conf --proxy` accepts uppercase and lowercase HTTP, HTTPS, ALL, and NO proxy variables.
  Missing HTTP and HTTPS values both fall back to ALL_PROXY. Version completion observes dotted
  version boundaries, so a request for `1.1` cannot select `1.10`.

See [Inventory source selection](/inventory/#source-selection) and [`pig sty`](/sty/).

## Repositories and extensions

- Repository commands validate the complete operand list before changing files. Empty values,
  empty comma-separated elements, and unsafe repository names fail before mutation.
  Only truly argument-free `repo rm` backs up all repository files; `repo rm all` expands the
  `node`, `pgsql`, and `infra` modules. Removal results preserve the original request and distinguish
  missing targets from removed files. `--update` also refreshes the cache after a full backup.
- Repository creation retains documentation RPMs. Debug package suppression continues to use
  `--nodbg`; a `-docs` or `-doc` name alone does not make a package a debug package.
- Default extension lists, availability summaries, and refresh results count all catalog records,
  including SQL utilities and retained lifecycle entries. The total describes catalog coverage,
  not how many extensions can be installed on one host or enabled with `CREATE EXTENSION`.
- Text, JSON, and YAML share availability rules. On covered Linux platforms, package matrices take
  precedence and a missing matrix cell means unavailable. Architecture aliases are normalized.
  On macOS, the status describes declared PostgreSQL support without promising an RPM/DEB package.
  `ext list -v` selects the version used to evaluate status; unavailable records remain listed.
- `ext import` reports failure if any requested package cannot be resolved or downloaded, while
  retaining successful downloads and reporting the completed and failed portions. APT virtual
  dependency markers are excluded from package download requests. Installed-library scanning also
  recognizes catalog entries without a control file.
- The three new catalog records are `pg_icu_parser`, `pg_vectorsearch`, and `textsearch_intl`.
  Existing versions and platform metadata are refreshed as well. Use `pig ext avail NAME` to inspect
  a target before installing.

Details: [`pig repo`](/repo/), [`pig ext`](/ext/).

## Builds and automation

- Multi-version build dependency installation expands package names for every selected PostgreSQL
  major version and removes duplicates. Default build targets retain their metadata and local
  installation rules independently of package-matrix gaps.
- Debian/Ubuntu builds preserve the inherited `PATH` order and append the current user's
  `~/.cargo/bin` when present, preserving an explicitly selected toolchain.
- Xray setup recognizes complete legacy service definitions, including marker-free macOS plists
  generated by the previous renderer. A comment alone cannot prove ownership; changed or foreign
  definitions still require explicit replacement. Matching reruns preserve a running service.
- JSON/YAML output and `PIG_NON_INTERACTIVE=1` consistently disable prompt input and use
  non-interactive sudo in PIG-owned adapters. Explicit data-input channels remain available;
  native Patronictl forwarding retains its interaction and exit contract.
- CMDB connection strings, legacy VMess credentials, and license keys are excluded from routine
  parameters and failure details. Explicit credential export and raw Inventory display retain
  their documented sensitive-output behavior.
- Exporter HTTP 4xx/5xx responses now fail with the numeric status and standard description,
  without including response bodies or custom status text. Unsupported `pig update` platforms
  fail explicitly. Command help and bilingual references are aligned with these behaviors.
- Go dependencies and validation tools are refreshed. CI includes Linux permission and instance
  boundary acceptance plus independent YAML consumer checks.

See [`pig build`](/build/), [`pig pe`](/pe/), and [global command behavior](/cmd/).

## Upgrade notes

Existing command names and flags remain available. Automation should handle the corrected failure
statuses for partial imports, HTTP errors, cancelled recovery, and indeterminate PostgreSQL state.
Scripts must supply valid repository operands, explicit confirmation where required, and literal
maintenance database names. When a name begins with `-`, place all options before `--` and the name.

Upgrade with the [installation instructions](/install/).

{{< release-card >}}
