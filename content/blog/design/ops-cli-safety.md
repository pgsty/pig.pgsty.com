---
title: "One Grammar for Dangerous Work: PIG's Operations CLI Safety Contract"
linkTitle: "Operations CLI Safety"
date: 2026-07-02
lastmod: 2026-08-28
description: "How PIG separates primitives from orchestrators, makes destructive intent explicit, and prevents aliases or structured output from changing operational meaning."
tags: [cli, postgres, pgbackrest, pitr]
weight: 40
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-07-02<br>
> **Status:** Implemented across the `pg`, `pb`, `pt`, and `pitr` command families and released by v1.5.0.<br>
> **Current reference:** [`pig pg`](/pg/), [`pig pb`](/pb/), and [`pig pitr`](/pitr/)<br>
> **Scope:** PIG-owned operational commands; transparent upstream commands retain upstream confirmation and exit behavior.

## Decision {#decision}

Operational convenience must not blur operational meaning. PIG distinguishes low-level primitives
from multi-stage orchestrators, makes destructive intent explicit, reserves aliases carefully, and
requires plans and structured results to describe the same action that text mode will execute.

The most important example is recovery: `pig pb restore` is the pgBackRest primitive, while
`pig pitr` coordinates Patroni, PostgreSQL shutdown, restore, restart, and post-recovery guidance.
An alias must never make those two paths look interchangeable.

## Context {#context}

The first generation of convenience aliases accumulated inconsistent positional arguments,
confirmation flags, output handling, and service semantics. Similar words such as `restart`,
`restore`, `promote`, and `failover` can refer to very different layers. A short alias that crosses
those layers can turn a harmless-looking invocation into an unmanaged destructive primitive.

Automation also exposed false-success risks when wrapper output, subprocess output, and result
rendering used different definitions of success.

## Alternatives considered {#alternatives}

- **Maximize shorthand aliases.** Rejected because collisions and cross-layer synonyms are more
  dangerous than a few saved characters are valuable.
- **Put confirmation on every risky-looking word.** Rejected for passthrough commands because the
  upstream tool must own its prompt and semantics.
- **Make the orchestrator call a convenience alias of the primitive.** Rejected because recovery
  coordination has additional stop, verification, and restart invariants.
- **Return success after launching the inner command.** Rejected because the result must reflect the
  complete owned workflow.

## Contract {#contract}

- sibling command names and aliases are unique;
- an alias cannot shadow a different top-level command;
- destructive PIG-owned operations require explicit confirmation and support non-mutating plans
  where a meaningful plan exists;
- command-layer validation rejects malformed or extra positional arguments before side effects;
- structured output and text mode share one result and one success definition;
- low-level restore does not claim to manage Patroni or HA routing;
- the PITR orchestrator stops the manager when required, proves PostgreSQL is stopped, restores,
  optionally starts PostgreSQL, and deliberately leaves Patroni stopped for operator verification;
- native tools receive extra arguments only through an explicit, documented boundary.

## Consequences {#impact}

Some historical shorthand disappeared and some scripts had to adopt cluster-first or explicit
target syntax. In return, command names now preserve layer boundaries, plans correspond to real
actions, and recovery automation cannot silently substitute a primitive for the orchestrator.

The contract does not eliminate operational risk. It makes risk visible and keeps a convenience
layer from inventing ambiguity.

## Verification and evolution {#verification}

The normative command specifications entered the repository in
[`c62c0f5`](https://github.com/pgsty/pig/commit/c62c0f5). Subsequent commits aligned aliases,
early validation, restore targets, service semantics, and role detection. Guard tests traverse the
Cobra tree to reject sibling and cross-layer alias collisions. Recovery tests cover plan,
confirmation, stop escalation, side restores, restart behavior, and structured failure results.

Patroni later moved to transparent passthrough. That refinement keeps the same safety principle:
PIG owns safeguards only for workflows it owns.

## Current status {#status}

Use `pig pb restore` when you intentionally want the pgBackRest primitive and [`pig pitr`](/pitr/)
when you want the managed recovery workflow. Current syntax, warnings, and platform requirements are
maintained in the command reference pages rather than frozen in this historical record.
