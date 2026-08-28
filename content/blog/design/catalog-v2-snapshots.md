---
title: "Catalog v2 Proposal: Immutable Typed Snapshots Instead of Bigger CSV"
linkTitle: "Catalog v2 Proposal"
date: 2026-08-13
lastmod: 2026-08-28
description: "A proposed verifiable Catalog model with typed targets, content-addressed snapshots, explicit activation, project pins, and offline import."
tags: [catalog, repo, ext, cli]
weight: 86
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-08-13<br>
> **Status:** Pre-implementation proposal; security mechanism, overlay scope, packaging, and path ADRs remain open.<br>
> **Current reference:** [`pig ext`](/ext/) and [`pig repo`](/repo/) describe the v1 Catalog behavior.<br>
> **Scope:** A candidate PIG 2.0 publication and consumption model for product metadata, not Inventory or live system state.

## Decision {#decision}

Catalog v2 should be one immutable, verifiable snapshot composed of multiple typed targets. A
manifest binds platform, repository, route, package-alias, extension, compatibility, Pigsty
release, and public-key metadata to exact bytes. Candidate targets are validated together and
activated through one pointer, preventing a new repository catalog from being mixed silently with
an old extension matrix.

The snapshot digest is its identity. Package, system, user, portable, and project scopes store or
select the same verified content; they do not merge unrelated base snapshots into a synthetic
Catalog.

## Context {#context}

The v1 Catalog is practical but spreads related facts across embedded CSV, repository YAML,
Pigsty variables, generated sites, and reload paths. Some fields repeat derived information, and
the extension matrix compresses several independent identities into one record. Independent
updates make it difficult to prove that repository, package, extension, and compatibility data
belong to the same publication event.

Catalog v2 is therefore a publication and trust problem, not merely a new serialization format.

## Alternatives considered {#alternatives}

- **Create a larger `extension.csv` or one giant YAML file.** Rejected because unrelated target
  types evolve differently and cannot be activated or streamed independently.
- **Use SQLite, protobuf, or a custom binary matrix immediately.** Rejected because the current
  dataset has not demonstrated a performance need that justifies a new runtime and debugging cost.
- **Merge system, user, and project base snapshots field by field.** Rejected because the result has
  no single publisher, digest, compatibility statement, or signature.
- **Store active or project-pinned content only in a cache.** Rejected because deleting a cache must
  not destroy a durable user or project decision.
- **Let a user file shadow the official trust root.** Rejected because security policy is a
  constraint, not an ordinary last-writer-wins preference.
- **Silently update and activate in the background.** Rejected because metadata changes can alter
  package resolution and must be an observable operation.

## Contract {#contract}

The proposed snapshot contract is:

- deterministic UTF-8 JSON for manifests and small targets, and JSONL for large sparse targets;
- raw manifest bytes and target length/hash are verified without parse-and-reserialize ambiguity;
- manifests carry schema, monotonic security version, creation, expiry, channel, and PIG/Pigsty
  compatibility;
- an embedded rescue baseline is always available;
- package-owned baselines, durable snapshot stores, mutable state pointers, and purgeable download
  caches are separate paths;
- Linux follows FHS/XDG, macOS uses Application Support and Caches, and portable `PIG_HOME` keeps
  config, data, state, cache, and run roles distinct;
- a project lock records snapshot identity and ordered overlays, while the verified snapshot is
  materialized into durable project support data;
- selecting a digest and finding its bytes are separate algorithms;
- system security policy can only be tightened by lower scopes, not weakened silently;
- updates download into private staging, verify every layer, sync, move into a content-addressed
  store, and atomically replace the active pointer;
- failures retain the previous active snapshot;
- project pins do not move when user or system active channels update;
- offline export includes verification metadata and public trust material, never private keys;
- old `ext reload` and `repo reload` may map to one whole-snapshot update for one compatibility
  period, but cannot activate targets independently.

The runtime Catalog excludes Inventory, credentials, live probes, installed-package state,
Ansible events, provider state, confirmations, and metrics that change without a product decision.

## Consequences {#impact}

Typed targets make ownership and validation clearer, and content addressing makes rollback and
airgap import auditable. Project materialization prevents a deployment from depending on one
user's global cache. Independent OS packages can refresh a read-only baseline without changing an
active user selection.

The cost is a larger release protocol: key rotation, expiry, rollback protection, garbage
collection, path permissions, migration, package-manager lifecycle, overlay conflicts, and
cross-repository generators all become compatibility-sensitive work.

The extension model must also separate SQL extension identity, upstream project, distribution or
build unit, versioned release, OS package offer, target availability, and display policy. Derived
fields such as aggregate platform support or `required_by` should be generated, not maintained as a
second truth.

## Verification and evolution {#verification}

Before implementation, the proposal requires an ADR to choose between go-tuf and a minimal signed
manifest. Both candidates must pass the same threat tests: bad signatures, expired metadata,
rollback, target substitution, mix-and-match snapshots, truncated downloads, and offline
verification. If neither passes, Catalog v2 cannot be a 2.0 release feature.

Additional gates cover FHS/XDG/macOS/portable paths, root and non-root permissions, read-only homes
and projects, symlink replacement, disk-full and concurrent activation, package upgrade/remove
semantics, project survival after global-cache deletion, and parity migration of the current
extension and availability corpus.

The current source baseline remains
[`v1.8.0`](https://github.com/pgsty/pig/commit/67dac09caab843252ea4376bf16b08c5e238ff22),
whose embedded and reloadable v1 Catalog continues to define released behavior.

## Current status {#status}

No Catalog v2 command, manifest, trust root, store layout, project lock, or migration format is a
released PIG contract today. Typed overlays should be omitted from 2.0 if their conflict and trust
rules cannot be proven; a complete custom signed channel is safer than loose unverified patches.
Current installation and catalog behavior remains documented under [`pig ext`](/ext/) and
[`pig repo`](/repo/).
