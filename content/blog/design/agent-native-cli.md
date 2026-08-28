---
title: "From Human-Friendly to Agent-Native: PIG's CLI Contract"
linkTitle: "Agent-Native CLI"
date: 2026-02-12
lastmod: 2026-08-28
description: "Why PIG separates human text, structured results, execution plans, and environment context instead of treating JSON as a formatting afterthought."
tags: [cli]
weight: 10
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-02-12<br>
> **Status:** Implemented in [pig v1.1.0](/release/pig-1.1.0/) and refined by later command-layer work.<br>
> **Current reference:** [`pig` command overview](/cmd/)<br>
> **Scope:** PIG-owned commands and their machine-consumption contract; opaque passthrough commands keep their native interface.

## Decision {#decision}

PIG should be usable by a person at a terminal and by an automation agent without making either
consumer parse the other's presentation. Human-facing text remains concise and operational.
Commands that own a stable result expose explicit JSON or YAML results, status codes, and plans.
Commands that merely forward an external tool preserve that tool's native stream, prompts, and
exit status instead of wrapping them in a misleading envelope.

Agent-native therefore means a clear capability boundary, not “append JSON to every command.”

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
- passthrough and interactive commands retain the upstream contract.

## Consequences {#impact}

This split makes scripts more reliable and lets agents choose commands based on risk and output
capability. It also creates maintenance obligations: every structured field becomes compatibility
surface, stdout purity needs tests, and a wrapper must not promise more stability than the tool it
delegates to.

The design intentionally allows mixed styles across PIG. Consistency is valuable, but semantic
honesty is more valuable than a uniform-looking wrapper.

## Verification and evolution {#verification}

The initial framework shipped with [v1.1.0](https://github.com/pgsty/pig/releases/tag/v1.1.0).
The command-layer consolidation in
[`fb93602`](https://github.com/pgsty/pig/commit/fb93602) later removed duplicated wrappers and
centralized plan and output glue. Patroni subsequently became a transparent passthrough, an
example of reducing PIG-owned structure when the upstream interface is already authoritative.

Tests now cover structured stdout isolation, result rendering, plan behavior, confirmation gates,
and context collection in the packages that own those contracts.

## Current status {#status}

The principle remains active: use the structured mode documented by a specific command, and do
not infer that global `-o` can safely transform every external or interactive stream. The current
command surface and supported examples live in the [`pig` reference](/cmd/).
