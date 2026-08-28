---
title: "Let Patronictl Speak for Itself"
linkTitle: "Patronictl Passthrough"
date: 2026-07-21
lastmod: 2026-08-28
description: "Why pig pt stopped mirroring Patronictl's command tree and became a transparent launcher with only a few PIG-owned local helpers."
tags: [patroni, cli]
weight: 80
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-07-21<br>
> **Status:** Implemented and released in [pig v1.6.0](/release/pig-1.6.0/).<br>
> **Current reference:** [`pig pt`](/pt/)<br>
> **Scope:** Patronictl-backed cluster commands plus PIG-owned configuration selection, settings sugar, service, status, and log helpers.

## Decision {#decision}

`pig pt` is a transparent launcher for the installed `patronictl`. PIG selects the configuration
and dispatches a small set of local helpers. Every other command token and all following arguments
are passed unchanged, with native prompts, terminal behavior, output formats, and exit codes.

PIG no longer maintains a copy of Patronictl's evolving command tree.

## Context {#context}

Mirroring Patronictl required PIG to reproduce commands, options, positional grammar, confirmation,
formatting, and version-dependent behavior. That surface changed upstream and PIG's copy drifted.
Users could receive different semantics depending on whether they called `patronictl` directly or
through PIG.

The wrapper still adds value in a Pigsty environment: selecting the correct config as the database
operating-system user, providing local service and log workflows, and translating a small settings
operation into one native edit-config call.

## Alternatives considered {#alternatives}

- **Continue mirroring every upstream command.** Rejected because it guarantees lag and duplicates
  validation that Patronictl already owns.
- **Allow only a tested command allowlist.** Rejected because new upstream commands would remain
  unavailable until a PIG release.
- **Capture native output into PIG JSON.** Rejected because it breaks interactive editing, streaming,
  prompts, terminal fidelity, and upstream schemas.
- **Remove `pig pt` entirely.** Rejected because deterministic config selection and local Pigsty
  helpers remain useful.

## Contract {#contract}

- the first non-option command token determines local dispatch or passthrough;
- `set`, local service shortcuts, `status`, and `log` are PIG-owned;
- all other commands and remaining tokens are forwarded verbatim;
- `pig pt -- COMMAND ...` bypasses a local-name collision explicitly;
- wrapper-level options must precede the native command token;
- native help can run without resolving a local Patroni configuration;
- Patronictl owns interactive prompts, native `--format`, and exit codes;
- global PIG structured output is rejected where it would consume a native option ambiguously;
- the selected config is resolved predictably and the process runs as the database system user.

## Consequences {#impact}

Automation had to adopt Patronictl's cluster-first positional grammar and native output flags.
Some PIG-only aliases and result schemas disappeared. In exchange, new Patronictl features work
without a PIG release and behavior no longer depends on a lagging wrapper implementation.

The local `set` helper remains intentionally small: it classifies scalar Patroni keys and
PostgreSQL parameters, then performs one native edit-config action.

## Verification and evolution {#verification}

The rewrite landed in
[`6cbc23b`](https://github.com/pgsty/pig/commit/6cbc23b). Tests cover token-boundary parsing,
verbatim argv preservation, config precedence, database-user execution, native exit propagation,
help without configuration, output-mode rejection, the `--` escape, and local-helper collisions.
The final help-path refinement landed before v1.6.0.

## Current status {#status}

Use Patronictl's own documentation for forwarded command grammar and [`pig pt`](/pt/) for PIG's
config selection and local helpers. Do not assume PIG `-o json` can replace Patronictl's native
`--format json`.
