---
title: "From Human-Friendly to Agent-Native: PIG's CLI Contract"
linkTitle: "Agent-Native CLI"
date: 2026-02-12
lastmod: 2026-10-13
description: "How PIG separates terminal text, structured results, execution plans, and environment context."
tags: [cli]
weight: 10
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-02-12<br>
> **Status:** Released in [pig v1.1.0](/release/pig-1.1.0/) and refined by later command-layer work.<br>
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

## Consequences {#impact}

This split makes scripts more reliable and lets agents choose commands based on risk and output
capability. It also creates maintenance obligations: every structured field becomes compatibility
surface, stdout purity needs tests, and a wrapper must not promise more stability than the tool it
delegates to.

The output contract follows the command: PIG results for PIG operations, native output for
forwarded tools.

## Verification and evolution {#verification}

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
