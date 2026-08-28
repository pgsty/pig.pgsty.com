---
title: "Use the CMDB Pigsty Already Has"
linkTitle: "Existing CMDB Boundary"
date: 2026-07-18
lastmod: 2026-08-28
description: "Why PIG retired a new revision-store design and became a thin, guarded adapter to Pigsty's existing PostgreSQL CMDB."
tags: [inventory, sty]
weight: 60
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-07-18<br>
> **Status:** The greenfield revision store is superseded; the thin existing-CMDB adapter is implemented and remains experimental.<br>
> **Current reference:** [`pig inventory cmdb`](/inventory/)<br>
> **Scope:** Exchanging declarations with Pigsty's existing CMDB, not designing another configuration database.

## Decision {#decision}

PIG must reuse the CMDB already provided by Pigsty. Its responsibility is a bounded adapter:
validate a static Inventory, load declarations into the existing tables, dump the existing
projection, check consistency, and switch Ansible between the static and dynamic sources safely.

PIG does not own a second schema, migration history, snapshot ledger, compare-and-swap revision
store, three-way merge engine, or rollback database.

## Context {#context}

An early design treated CMDB support as a greenfield backend. It proposed a separate schema,
immutable snapshots, revision tokens, merge and rollback operations, backup bundles, and source
switch records. The design was internally coherent but started from the wrong premise: Pigsty
already had the `pigsty` and `pglog` schemas, load scripts, dynamic Inventory projection, and source
switching behavior.

Building a parallel control plane would duplicate facts, create synchronization problems, and make
PIG responsible for a data model owned by another project.

## Alternatives considered {#alternatives}

- **Keep the new revision store as an advanced mode.** Rejected because two authorities are still
  two authorities, even if one is optional.
- **Mirror between the new and existing schemas.** Rejected because conflict resolution and
  migration would become permanent product responsibilities.
- **Hide the existing scripts behind a shell wrapper.** Rejected because PIG needs bounded timeouts,
  safe connection handling, structured plans, and atomic source switching.
- **Remove CMDB support entirely.** Rejected because a small native adapter adds useful validation
  and automation without redefining the schema.

## Contract {#contract}

- Pigsty's existing schema and projections are the data-model authority;
- PIG connects through an explicit database target, environment configuration, or `service=meta`;
- credentials, DSNs, SQL bodies, and declaration values never enter plans or diagnostics;
- `check` is read-only;
- `init` applies the existing baseline and does not claim to back up an existing database;
- `load` replaces declaration rows transactionally and requires explicit confirmation;
- `dump` refuses an unexpected overwrite unless forced;
- `enable` and `disable` edit only recognized Ansible Inventory source forms and write atomically;
- unfamiliar executable Inventory sources are refused rather than rewritten;
- the entire command family remains labeled experimental.

## Consequences {#impact}

The correction deleted a large amount of already implemented revision-store code. That deletion
was intentional scope recovery, not lost functionality: the removed features described a product
PIG should not own.

The remaining adapter is smaller, easier to audit, and compatible with existing Pigsty operations.
It also inherits the limits of that system: `init` needs an operator-managed backup, and loading a
declaration set is a replacement operation rather than collaborative version control.

## Verification and evolution {#verification}

The corrected boundary was recorded in
[`ba6e678`](https://github.com/pgsty/pig/commit/ba6e678). The abandoned implementation was removed
in [`e0f73ed`](https://github.com/pgsty/pig/commit/e0f73ed), deleting the parallel schema, snapshot,
merge, revision, and rollback machinery. Tests for the retained path cover PostgreSQL compatibility,
connection redaction, transaction failures, digest-pinned confirmation, dump safety, and atomic
source switching.

## Current status {#status}

The existing-CMDB adapter shipped in [v1.6.0](/release/pig-1.6.0/) but remains experimental.
Operators should back up real CMDB state before initialization or replacement and use the current
[`pig inventory` documentation](/inventory/) rather than the historical abandoned design.
