---
title: "The 70% Tuner: Defining the Boundary of pig pg tune"
linkTitle: "The 70% Tuner"
date: 2026-03-21
lastmod: 2026-08-28
description: "Why pig pg tune produces deterministic hardware-based core settings while refusing to present itself as complete production PostgreSQL tuning."
tags: [postgres]
weight: 20
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-03-21<br>
> **Status:** Implemented on 2026-03-23 and released in [pig v1.3.2](/release/pig-1.3.2/).<br>
> **Current reference:** [`pig pg tune`](/pg/#pg-tune)<br>
> **Scope:** A deterministic first-pass configuration for one local PostgreSQL instance, not a complete production design service.

## Decision {#decision}

`pig pg tune` should answer one bounded question: given a CPU count, memory size, disk size, and a
workload profile, what are sensible core PostgreSQL parameters for this machine?

The command targets a “70% correct” starting point. It detects hardware when possible, accepts
explicit overrides, calculates a small set of high-impact parameters, and can write them to
`postgresql.auto.conf`. It does not claim to design replication, durability, security, logging,
extensions, connection pooling, or workload-specific SQL behavior.

## Context {#context}

Operators repeatedly need a usable baseline before they have workload telemetry. Copying a static
configuration ignores machine size; a full tuning service would need workload traces, storage
characteristics, availability requirements, and continuous feedback.

PIG already knows how to locate a PostgreSQL installation and run as the database operating-system
user. A small deterministic tuner fits that boundary and remains inspectable.

## Alternatives considered {#alternatives}

- **Ship one universal configuration.** Rejected because memory and parallelism settings must scale
  with the host.
- **Build an adaptive autotuner.** Rejected because it would require telemetry, experiments,
  workload classification, and rollback machinery far beyond a local CLI command.
- **Rewrite the main configuration file.** Rejected because it mixes generated values with
  distribution- or operator-owned configuration and makes rollback difficult.
- **Tune every PostgreSQL parameter.** Rejected because many parameters encode business,
  durability, security, and topology decisions that hardware cannot determine.

## Contract {#contract}

The tuner follows these rules:

- hardware detection is observable and every detected value can be overridden;
- profiles change formulas, not hidden external state;
- calculations are deterministic for the same inputs;
- preview and structured output are available before any write;
- generated settings are confined to the auto-configuration surface;
- existing unrelated settings and comments are preserved by the editor;
- values remain bounded by PostgreSQL and machine constraints;
- the output states the assumed SSD storage model and the limits of the recommendation.

## Consequences {#impact}

The command is useful for development machines, fresh installations, and initial sizing, but it
must not be treated as proof that a production database is tuned. Replication lag, checkpoint
behavior, query concurrency, cache hit rates, storage latency, extensions, and failure objectives
still require measurement and operator judgment.

Keeping the scope small also makes the formulas testable and lets users reproduce a result without
a remote service.

## Verification and evolution {#verification}

The implementation landed in
[`60eecfe`](https://github.com/pgsty/pig/commit/60eecfe045449e72d80986a0357fbe24b9e71f00)
and was tagged as v1.3.2. Unit tests cover profile calculations, hardware overrides, result
rendering, and safe `postgresql.auto.conf` editing. Static-analysis cleanup followed without
changing the product boundary.

## Current status {#status}

`pig pg tune` remains a first-pass tool. Review its output before applying it and use Pigsty or a
workload-specific tuning process when topology, high availability, observability, or security must
be designed together. Current flags and examples are maintained in the [`pig pg` reference](/pg/).
