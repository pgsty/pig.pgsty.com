---
title: "From Human-Friendly to Agent-Native: PIG's CLI Contract"
linkTitle: "Agent-Native CLI"
date: 2026-02-12
lastmod: 2026-10-17
description: "How PIG separates terminal text, structured results, execution plans, and environment context."
tags: [cli]
weight: 10
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-02-12<br>
> **Status:** Released in [pig v1.1.0](/release/pig-1.1.0/) and refined by later command-layer work. The 2026-10-16 refinements below are Implemented in the v1.10.0 candidate, not yet released.<br>
> **Current reference:** [`pig` command overview](/cmd/)<br>
> **Scope:** PIG-owned commands and their machine-consumption contract; opaque passthrough commands keep their native interface.

## Decision {#decision}

PIG provides terminal text for people and structured results for automation. Commands that produce
stable data expose JSON or YAML and status codes. Supported workflows also expose execution plans.
Transparent passthroughs such as `pig pt` preserve the external tool's output, prompts, and exit status.

## Context {#context}

PIG began as a convenient package-management CLI. As it grew into PostgreSQL, Patroni,
pgBackRest, Pigsty, and repository operations, a human-only interface created several problems:

- automation had to scrape colored prose;
- a zero process exit could hide a failed inner operation;
- destructive workflows could not be inspected before execution;
- an agent had to issue many discovery commands before understanding the host;
- wrappers could accidentally mix subprocess chatter with structured output.

The v1.1.0 design introduced global output selection, stable result objects, execution plans, and
the `pig context` snapshot. Later refactors narrowed these promises to commands that can actually
own them reliably.

## Alternatives considered {#alternatives}

Three tempting approaches were rejected:

1. **Parse human text.** It is fragile across wording, localization, colors, and upstream tools.
2. **Capture every subprocess into JSON.** This breaks interactive programs, streaming output,
   terminal control, and native exit semantics.
3. **Invent one universal result schema.** Package transactions, recovery plans, metrics, and
   context snapshots have different stable data; flattening them loses meaning.

## Contract {#contract}

The durable contract is:

- text is the default interface for people;
- a command advertises structured output only when PIG owns a stable result;
- structured stdout contains one parseable result, while diagnostics and wrapped-tool output use
  stderr;
- a plan describes intended actions, scope, risk, and expected effects without performing them;
- destructive PIG-owned operations fail closed when confirmation is missing;
- status codes distinguish usage, confirmation, environment, dependency, and execution failures;
- `pig context` provides a bounded environment snapshot rather than forcing consumers to infer it;
- transparent passthroughs retain the upstream contract.

The 2026-10-16 refinements apply the same contract to [`pig ext`](/ext/):

- Availability checks and every summary format share matrix precedence, architecture aliases,
  and the metadata fallback. macOS reports declared PostgreSQL support without promising packages.
  This describes the catalog's package snapshot. Default [build targets](/build/#build-ext) retain
  their metadata and local-installation rules independently of the matrix.
- Partial imports return failure while preserving resolved, downloaded, and unresolved items.
  Completed downloads remain on disk; the operation does not promise an atomic transaction.
- [`pig pe`](/pe/) treats HTTP 4xx/5xx as failure. Error details expose the numeric status and
  standard description, never the response body or server-supplied reason phrase.
- [`pig license issue`](/cmd/#license) explicitly delivers a newly issued credential. Its successful
  structured result preserves the token in `data.captured_output`. Signing-key input is omitted
  from parameters, and raw key-loading errors are replaced with fixed messages at the command
  boundary. Parameter errors and safe signing-key diagnostics remain readable in every output
  format. Other sensitive command wrappers retain full output and error-detail redaction.

## Consequences {#impact}

This split makes scripts more reliable and lets agents choose commands based on risk and output
capability. It also creates maintenance obligations: every structured field becomes compatibility
surface, stdout purity needs tests, and a wrapper must not promise more stability than the tool it
delegates to.

The output contract follows the command: PIG results for PIG operations, native output for
forwarded tools.

## Verification and evolution {#verification}

Fixed source commits and regression tests for the committed v1.10.0 refinements cover:
[availability and counts](https://github.com/pgsty/pig/commit/863a271a924a1634630247643d9d96200a98572d),
[partial imports](https://github.com/pgsty/pig/commit/a0e9cc477f3834607c03620cb7c77187773218b5),
[exporter HTTP failures](https://github.com/pgsty/pig/commit/2214f598101c82ffb2b3bf2a6a7dd15d6f025483). These commits do not establish a release boundary.

The initial framework shipped with [v1.1.0](https://github.com/pgsty/pig/releases/tag/v1.1.0).
The command-layer consolidation in
[`fb93602`](https://github.com/pgsty/pig/commit/fb93602) later removed duplicated wrappers and
centralized plan and output glue. Patroni subsequently became a transparent passthrough, an
example of reducing PIG-owned structure when the upstream interface is already authoritative.

Tests now cover structured stdout isolation, result rendering, plan behavior, confirmation gates,
and context collection in the packages that own those contracts.

## Current status {#status}

Use the output mode supported by each command. See the [`pig` reference](/cmd/) for structured
results and passthrough behavior.
