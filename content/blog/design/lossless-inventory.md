---
title: "Edit the Declaration, Preserve the Document: Lossless Pigsty Inventory"
linkTitle: "Lossless Inventory"
date: 2026-07-18
lastmod: 2026-10-17
description: "Why pig inventory separates YAML semantics from source bytes so scoped edits can preserve comments, ordering, anchors, and formatting."
tags: [inventory, sty]
weight: 50
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-07-18<br>
> **Status:** Implemented and released in [pig v1.6.0](/release/pig-1.6.0/). The 2026-10-16 acceptance refinements below are Accepted for the next release, with no new release claim.<br>
> **Current reference:** [`pig inventory`](/inventory/)<br>
> **Scope:** Static Pigsty Inventory inspection, scoped editing, validation, comparison, and safe writes.

## Decision {#decision}

PIG treats `pigsty.yml` as both a semantic declaration and a human-maintained source document.
Semantic parsers determine what the Inventory means; the original bytes remain authoritative for
how it is written. Scoped edits replace bounded source ranges and then reparse the complete
candidate before an atomic write.

This avoids a common YAML-tool failure: a logically correct edit that silently rewrites comments,
key order, quoting, anchors, block scalars, or line endings across the entire file.

## Context {#context}

Pigsty Inventories are long-lived operational assets. They contain topology, tuning, credentials,
comments, examples, anchors, and locally meaningful ordering. A conventional parse-mutate-serialize
cycle can produce a valid but unreviewable diff and may change constructs the operator never
selected.

At the same time, raw text editing without semantic validation can put invalid or contradictory
configuration on disk. The design needed source fidelity and whole-document correctness together.

## Alternatives considered {#alternatives}

- **Round-trip through one YAML serializer.** Rejected because no selected serializer preserved the
  full source contract byte-for-byte across the real Pigsty corpus.
- **Use regular expressions for YAML.** Rejected because quoting, comments, aliases, block scalars,
  and nested collections make text-only semantic decisions unsafe.
- **Edit only a normalized generated copy.** Rejected because the active Inventory is operator-owned
  and would still diverge from the generated representation.
- **Allow every node type to be replaced.** Rejected because anchors, aliases, tags, and block
  scalars need stricter handling than ordinary mappings and scalars.

## Contract {#contract}

- duplicate keys and multi-document YAML are rejected;
- selectors address one unambiguous declaration fragment;
- semantic decoding and source-range discovery are separate concerns;
- an edit starts from the exact source revision and fails if the file changes concurrently;
- the edited fragment is normalized only as required for its insertion context;
- the complete candidate is reparsed and validated before commit;
- writes use a same-directory temporary file, sync, rename, and directory sync;
- symlink and unsafe path changes are rejected;
- a successful edit removes group and other permissions, preserving the owner's existing read and write permissions;
- diagnostics, diffs, plans, and structured results omit declaration values unless a command is
  explicitly a raw text surface.

The 2026-10-16 acceptance refinement preserves role-name strings and structured role grants in
`pg_users[].roles`. Editing, serialization, and CMDB export must preserve YAML 1.1 string semantics,
including `"1:30"`; `"010"` is a regression control, not a claim of an earlier defect.
The 2026-10-17 refinement also requires dates and timestamps supplied as strings to remain strings
when loaded by PyYAML. Existing timestamp values retain their source bytes as opaque scalars;
this does not add date arithmetic or normalize the document. Acceptance compares emitted types
with an independent YAML loader, rather than relying only on PIG's own round trip.

[`sty deploy`](/sty/#sty-deploy) and [`do`](/do/) consume the configuration layer's already resolved
Inventory path. Flag and environment relative paths use the caller's cwd, quoted `~/` uses the
user's home, and defaults remain explicit at execution. Missing sources do not fall back.
Static inspection still never executes dynamic sources; Ansible retains its execution boundary.

## Consequences {#impact}

The editor is more complex than ordinary YAML marshaling, and some syntactically valid fragments
are deliberately refused when source fidelity cannot be proven. The benefit is a reviewable diff:
unselected parts of the Inventory remain byte-for-byte stable, invalid YAML cannot be committed,
and a concurrent edit cannot be overwritten silently.

Inventory can contain custom credential fields, so field names alone cannot reliably identify secrets.
For this reason, `show` prints the selected declaration as raw text. Metadata and validation commands omit declaration values.

## Verification and evolution {#verification}

The root Inventory contract and existing-CMDB boundary were established in
[`ba6e678`](https://github.com/pgsty/pig/commit/ba6e678), with the implementation landing in
[`ea43858`](https://github.com/pgsty/pig/commit/ea43858). Tests exercise real Pigsty configuration
corpora, byte-identical round trips, scoped replacement, protected YAML forms, concurrent-change
rejection, atomic-write failures, selectors, validation, and secret-free diagnostics.

Later refactors removed legacy options and separated validation stages without changing the
source-fidelity model.

## Current status {#status}

The static Inventory remains the primary declaration surface. Use the current
[`pig inventory` reference](/inventory/) for selectors, validation profiles, structured output, and
the explicitly experimental CMDB bridge.
