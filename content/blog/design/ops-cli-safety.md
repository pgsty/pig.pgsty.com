---
title: "One Grammar for Dangerous Work: PIG's Operations CLI Safety Contract"
linkTitle: "Operations CLI Safety"
date: 2026-07-02
lastmod: 2026-09-03
description: "How PIG separates primitives from orchestrators, makes destructive intent explicit, and prevents aliases or structured output from changing operational meaning."
tags: [cli, postgres, pgbackrest, pitr]
weight: 40
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-07-02<br>
> **Status:** Released for `pg`, `pb`, `pt`, and `pitr` by v1.5.0; the 2026-08-29 `do` and `build proxy` refinements were released in [v1.8.1](/release/pig-1.8.1/).<br>
> **Current reference:** [`pig pg`](/pg/), [`pig pb`](/pb/), [`pig pitr`](/pitr/), [`pig do`](/do/), and [`pig build`](/build/)<br>
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
- command-specific names mirror the downstream Pigsty contract, or use the narrowest documented
  safe boundary when the downstream playbook has no explicit grammar;
- structured output and text mode share one result and one success definition;
- credential-bearing values stay out of diagnostics, and readiness or connectivity failure remains
  a command failure rather than a logged warning followed by success;
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

The same contract was applied to `pig do` name and cluster validation in
[`3e1603b`](https://github.com/pgsty/pig/commit/3e1603b2bfbb949fb77b7ecd5fd458ec2ee45d25),
with Ansible built-in targets closed in
[`a880485`](https://github.com/pgsty/pig/commit/a88048596dffdfd6c1bb51cdbe7da6782a11cc22).
Package-backed, credential-safe, truthful `build proxy` setup entered in
[`220ef9c`](https://github.com/pgsty/pig/commit/220ef9c722b54951d3dc502ea3e3baafd642b592),
followed by structured-argument redaction and corrected machine annotations in
[`74cb128`](https://github.com/pgsty/pig/commit/74cb1281860fae659f2aa4fec2898af34a0c2519),
and optional operands were reflected in the machine grammar in
[`de7ffd0`](https://github.com/pgsty/pig/commit/de7ffd0e81e500ea2f4268ca326917aa385150ca).
The changes were exercised on Ubuntu 24.04 and Rocky Linux 9 ARM64 Farrow guests, then released
from source commit [`e3d1eb4`](https://github.com/pgsty/pig/commit/e3d1eb4a86cedddcf49fff398fc69751e861372e)
after the [v1.8.1 CI run](https://github.com/pgsty/pig/actions/runs/33718574084) passed.

## Current status {#status}

Use `pig pb restore` when you intentionally want the pgBackRest primitive and [`pig pitr`](/pitr/)
when you want the managed recovery workflow. Current syntax, warnings, and platform requirements are
maintained in the command reference pages rather than frozen in this historical record.
