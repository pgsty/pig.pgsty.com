---
title: "PIG 2.0 Product Direction: A Proposal, Not a Release Contract"
linkTitle: "PIG 2.0 Proposal"
date: 2026-08-13
lastmod: 2026-08-28
description: "The proposed PIG 2.0 boundary: a stable Pigsty onboarding front door, verifiable Catalog client, and thin orchestrator that keeps deployment explicit."
tags: [cli, sty, catalog]
weight: 85
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-08-13<br>
> **Status:** Proposal for owner review; it is not implemented and is not a PIG 2.0 release commitment.<br>
> **Current reference:** [PIG documentation](/docs/) and the current [v1.8.0 release](/release/pig-1.8.0/)<br>
> **Scope:** Candidate product boundaries and verification gates for a future PIG 2.0 / Pigsty 5.0 line.

## Decision {#decision}

The proposed direction makes PIG the stable onboarding front door from an empty controller to a
validated, deployable Pigsty Inventory. PIG would own Catalog selection, resolution, plans,
bounded execution orchestration, structured results, and redacted receipts. It would continue to
delegate package transactions, configuration application, and infrastructure state to DNF/APT,
Ansible, and future provider-specific tools.

The proposal deliberately preserves PIG's standalone value: `repo`, `ext`, and `install` must work
without a Pigsty project. It also preserves explicit deployment consent: a future `pig sty setup`
may download, bootstrap, and configure, but it must stop before multi-node deploy unless the user
invokes deployment separately.

## Context {#context}

By v1.8.0 PIG could download releases, bootstrap a controller natively, compile Inventory, manage
repositories and extensions, and run selected operations. Several product seams remained:

- repository, package-alias, extension, route, and Pigsty metadata could change independently;
- projects had no explicit Catalog identity to protect later resolution from global updates;
- route choice and repository safety were not one visible product contract;
- execution results did not yet form a durable, redacted receipt across the onboarding path;
- compatibility among PIG, Pigsty, Catalog schema, operating systems, and Ansible needed one release
  matrix rather than separate assumptions.

The proposal treats those seams as the 2.0 problem. It does not use the major version as permission
to rename commands or rebuild tools that already have an authority.

## Alternatives considered {#alternatives}

- **Turn PIG into a monolithic configuration and state engine.** Rejected because Inventory,
  Catalog authoring, package managers, Ansible, and providers already own different facts.
- **Make Pigsty depend on a live PIG or pgext checkout.** Rejected because a Pigsty release must
  remain independently usable from generated, versioned artifacts.
- **Make setup deploy automatically.** Rejected because creating and validating configuration is a
  different consent boundary from changing remote nodes.
- **Reimplement DNF/APT failover or Ansible execution.** Rejected because PIG should select inputs
  and explain results, not become another package manager or configuration engine.
- **Block 2.0 on Vagrant/Terraform unification.** Rejected because lab providers have different
  state semantics and do not determine the core onboarding path.
- **Invent a universal `sty plan` immediately.** Rejected until at least two owned workflows prove
  that one reusable plan schema exists.

## Contract {#contract}

If accepted, the product direction would enforce these boundaries:

- each fact type has one authority: Inventory for cluster declarations, Catalog authoring sources
  for product metadata, project lock for selected snapshot identity, receipts for observed results,
  and providers for live state;
- PIG owns Catalog schema, validation, client, resolver, and selection, but not every authoring
  database;
- `sty setup` composes existing init, boot, and configure use cases instead of duplicating them;
- setup stops after a validated Inventory; deploy remains explicit;
- standalone commands follow a compatible Catalog channel, while a Pigsty project pins its
  selected snapshot after a successful setup or configuration commit;
- ordinary commands never rewrite an existing project lock implicitly;
- route selection is explicit or a bounded first-run decision, not a continuous GeoIP, cloud-IMDS,
  or background-latency service;
- package download retry and endpoint failover remain owned by DNF/APT;
- execution artifacts are versioned and redacted; raw upstream modes preserve native streams and
  exit behavior;
- doctor remains diagnostic and does not gain default repair authority;
- future lab support is a thin adapter and never makes PIG the owner of Terraform state.

## Consequences {#impact}

The proposal creates a clearer first-run story and makes metadata selection auditable. It also adds
new durable contracts: snapshot identities, project locks, migration rules, trust policy,
receipts, and compatibility matrices. Those contracts increase the testing and release burden and
must not ship as loosely coupled features.

Some attractive work is intentionally optional or deferred. An Ansible event bridge is a target
only if redaction and compatibility experiments pass. Doctor/support bundles and lab adapters are
post-GA. EL7 support remains an owner decision rather than an implied compatibility promise.

## Verification and evolution {#verification}

This proposal requires evidence before it can become a release contract:

- a native onboarding VM matrix across the declared Linux targets;
- adversarial Catalog signature, expiry, rollback, mix-and-match, and offline tests;
- semantic-diff proof that generated Pig, Pigsty, and pgext consumers do not drift;
- an Ansible callback experiment with zero `no_log` or secret leakage;
- route-selection tests for global, China, proxy, and restricted-network environments;
- repository-signing tests before secure defaults are changed;
- rehearsed 1.x-to-2.0 layout, lock, and mixed-version migration;
- schema and structured-output fixtures tied to an explicit compatibility matrix.

The current implementation baseline is
[`v1.8.0`](https://github.com/pgsty/pig/commit/67dac09caab843252ea4376bf16b08c5e238ff22).
That release contains native boot and configure, but it does not implement the proposed Catalog v2,
project pin, setup command, event receipt, or 2.0 migration contract.

## Current status {#status}

This is a public proposal record, not an announcement. Current users should follow the
[v1.8.0 documentation](/docs/). Catalog v2 security selection, typed overlays, path layout details,
EL7 support tier, event-bridge viability, and the final 2.0 scope still require explicit decisions
and experimental evidence before implementation or release claims are appropriate.
