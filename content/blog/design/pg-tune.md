---
title: "The 70% Tuner: Defining the Boundary of pig pg tune"
linkTitle: "The 70% Tuner"
date: 2026-03-21
lastmod: 2026-10-13
description: "How pig pg tune calculates initial PostgreSQL parameters from hardware and workload inputs."
tags: [postgres]
weight: 20
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-03-21<br>
> **Status:** Released in [pig v1.3.2](/release/pig-1.3.2/), following implementation on 2026-03-23.<br>
> **Current reference:** [`pig pg tune`](/pg/#pg-tune)<br>
> **Scope:** Generate a starting configuration from hardware, PostgreSQL version, and workload profile.

## Decision {#decision}

`pig pg tune` calculates core PostgreSQL parameters and prints them for review. It detects CPU,
memory, and disk capacity, accepts explicit overrides, and applies a selected workload profile.
Text output displays the generated parameters; JSON and YAML output include the inputs and parameters.
Review the values and select the settings to apply through your configuration system.

The original “70% tuner” name describes a practical starting point. It is not a measured accuracy score.

## Context {#context}

A fresh installation needs an initial configuration before workload measurements are available.
One static configuration cannot fit both a small development machine and a large database server.
Hardware-based formulas provide a repeatable baseline that the operator can inspect and adjust.

## Alternatives considered {#alternatives}

- **Ship one fixed configuration.** Memory and parallelism settings need to scale with the host.
- **Build an adaptive tuner.** This would require workload data, experiments, and a feedback loop.
- **Apply settings automatically.** The operator needs to review the generated values and choose
  how to deploy them through the existing configuration workflow.
- **Calculate every PostgreSQL parameter.** Replication, security, and availability settings also
  depend on requirements that hardware detection cannot determine.

## Contract {#contract}

- Use the detected hardware or the operator's explicit CPU, memory, and disk values.
- Select formulas through `oltp`, `olap`, `tiny`, or `crit`.
- Produce the same parameters for the same resolved inputs and PostgreSQL version.
- Include the resolved profile, hardware, and PostgreSQL version in structured results.
- Print text parameters in a stable order and identify the SSD assumption in the header.
- Validate input ranges and omit parameters unavailable in the selected PostgreSQL version.
- Leave configuration files and the running server unchanged.

## Consequences {#impact}

Operators can use the output for a new installation or initial sizing. Review the values, apply
them through the configuration system in use, then measure the workload. Query concurrency,
checkpoint behavior, storage latency, and replication requirements guide later adjustments.

## Verification and evolution {#verification}

The initial implementation is
[`60eecfe`](https://github.com/pgsty/pig/commit/60eecfe045449e72d80986a0357fbe24b9e71f00).
The [v1.3.2 release](/release/pig-1.3.2/) introduced parameter generation.
The [current implementation](https://github.com/pgsty/pig/blob/v1.9.0/cli/postgres/tune_result.go)
returns a result for rendering. Tests in
[`tune_test.go`](https://github.com/pgsty/pig/blob/v1.9.0/cli/postgres/tune_test.go)
cover workload formulas, resource limits, overrides, and version-dependent parameters.

## Current status {#status}

Parameter generation is released.
See the [`pig pg` reference](/pg/#pg-tune) for inputs and output examples.
