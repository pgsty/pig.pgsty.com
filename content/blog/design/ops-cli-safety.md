---
title: "One Grammar for Dangerous Work: PIG's Operations CLI Safety Contract"
linkTitle: "Operations CLI Safety"
date: 2026-07-02
lastmod: 2026-10-17
description: "How PIG separates primitives from orchestrators, makes destructive intent explicit, and prevents aliases or structured output from changing operational meaning."
tags: [cli, postgres, pgbackrest, pitr]
weight: 40
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-07-02<br>
> **Status:** Released for `pg`, `pb`, `pt`, and `pitr` by v1.5.0; the 2026-08-29 `do` and `build proxy` refinements were released in [v1.8.1](/release/pig-1.8.1/). The acceptance refinements below are Implemented for v1.10.0; source evidence is listed under verification. They are not yet released.<br>
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
- **Restrict maintenance database names to ASCII identifiers.** Rejected because spaces and
  non-ASCII names are valid inputs. Reject libpq connection-string syntax instead, and preserve
  the positional boundary when generating commands.

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

The 2026-10-16 to 2026-10-17 refinements apply the same boundary to the v1.10.0 candidate:

- Cross-user DBSU writes stage an exclusively created private sibling, use mode `0600` and the
  executing DBSU's ownership, reject symlink/non-regular destinations, replace the exact path,
  and clean staging on failure. Linux uses an exact-target rename; macOS uses the system Perl
  `rename` syscall because BSD `mv` has directory-target semantics.
- [`repo rm`](/repo/#repo-rm) validates the whole operand list before changes. Only zero operands
  mean full backup; `all` remains `node`, `pgsql`, and `infra`.
  `requested_modules` retains the original request; `removed_repos` describes the expanded actions.
  `repo add`, `repo set`, and `repo info` also reject explicit empty names and comma-separated
  empty entries as a whole request. Only omitted operands retain the add/set default of `all`.
  Add/set also validate module-name syntax before initializing the repository manager. Unsafe
  names reject the whole request; syntactically valid unknown names retain additive partial
  success, while replacement rejects them before changes.
- With an explicit `pg -D`, SQL operations and database enumeration bind to that directory's
  recorded port and socket. Ambiguous metadata fails before execution. Omitting `-D` preserves
  native client connection defaults; `/pg/data` remains the default for instance operations.
  Explicit empty or whitespace-only `-D` values fail before configuration or operational work.
  Plans, confirmation retries, and verification commands preserve the same target and operation
  options, including an explicit `-D /pg/data`. `VACUUM FULL` plans require confirmation, as execution does.
  The 2026-10-17 maintenance refinement rejects connection-string database operands before plans,
  confirmation, or execution, without echoing the supplied value. A libpq connection string could
  otherwise override the selected host/port and expose credentials. `vacuum`, `analyze`, and `freeze`
  validate the complete enumerated database list before any maintenance starts.
  Generated `vacuum` and `repack` commands place all options before `--` and the database name,
  preserving a name such as `--all` as a single-database operand.
- Fork replacement requires matching metadata
  with an explicit target for nonempty unmanaged directories, including non-PGDATA directories.
  Empty destinations remain usable; managed forks must be replaced by name. Private paths are
  resolved as DBSU, and unresolved aliases fail closed. The 2026-10-17 review removes the extra
  `/pg/data` prohibition: eligibility depends on target ownership, source/destination relationships,
  and runtime state. A conventional path cannot identify every primary and may be a legitimate fork target.
  Forced cleanup of managed orphan directories remains supported.
  For unmanaged removal, a permission-denied local path check retries as the selected DBSU;
  it must establish that the target is a directory and not a symlink before deletion can proceed.
- `EPERM` alone must not authorize `pg init --force` or PITR restore. Independent executable
  identity may establish PID reuse; unavailable identity remains unknown. A live PID must identify
  PostgreSQL before lifecycle commands may signal it or connection metadata may be used for SQL.
  Unknown state carries no usable PID for force-stop escalation. Fork start must not persist
  success in that state; list output reports `unknown` and `runtime_unknown: true`.
  Role detection also fails on an unknown running state; file-based role evidence cannot override
  a confirmed stopped state. Forced initialization reports probe failures separately from a running conflict.
  Plan preconditions report indeterminate runtime state as `unknown`, never a passed check with PID zero.
  Status queries distinguish permission failures (`130201`, exit `3`) from other probe failures
  (`130808`, exit `1`); partial data in either failure cannot establish that the instance is stopped.
- Timeline reporting binds SQL to the selected data directory's valid PID metadata and socket.
  If that cannot be resolved, it uses that directory's `pg_controldata` or reports an unknown
  timeline. Promotion execution and the requirement to verify the primary role stay unchanged.
- PITR cancellation and EOF return confirmation-required (`161001`, exit `7`) before service
  stops, restore, or restart. Acceptance must execute the confirmation path and observe zero
  lifecycle side effects.
- `PIG_NON_INTERACTIVE` and structured execution disable prompt stdin and add sudo `-n`, including
  legacy structured wrappers. Native passthrough and explicit data stdin retain their contracts.
- Sensitive captured output and error details remain private. Signing-key load errors never echo
  the supplied key. Explicit raw exports remain available on their documented text surfaces.

## Consequences {#impact}

Some historical shorthand disappeared and some scripts had to adopt cluster-first or explicit
target syntax. In return, command names now preserve layer boundaries, plans correspond to real
actions, and recovery automation cannot silently substitute a primitive for the orchestrator.

Plans show the affected resources and actions so operators can review recovery before execution.

## Verification and evolution {#verification}

Fixed source commits and regression tests for the committed v1.10.0 refinements cover:
[runtime identity and SQL targets](https://github.com/pgsty/pig/commit/526410e2cbbfa9658533d179bff91a8cdc190ffd),
[fork ownership and private paths](https://github.com/pgsty/pig/commit/9db279947ef5d2492956a482a984685e8f807c5f),
[PITR cancellation and unknown state](https://github.com/pgsty/pig/commit/54d4bae5480a2424ec4842e64ca8e9f810e8d354),
[plan target preservation](https://github.com/pgsty/pig/commit/da0706fa3c676b8d912b4c7a556ee58dbe8045f3),
[status error classification](https://github.com/pgsty/pig/commit/e6cd11f59590d158749eface28a470a78e17bba4). These commits do not establish a release boundary.
The later [maintenance database-name and `--` operand boundaries](https://github.com/pgsty/pig/commit/5cf691b7fc559a5f3dd0c9d346927188f8b63375)
include Cobra argument-reparse tests and a real libpq target-boundary regression test.
The [repository operand preflight](https://github.com/pgsty/pig/commit/981726b27786be78832b2c1b457e55ebf7505fe9) rejects
unsafe module names before key preparation or repository writes and preserves partial additive
results for syntactically valid unknown modules.

The normative command specifications entered the repository in
[`c62c0f5`](https://github.com/pgsty/pig/commit/c62c0f5). Subsequent commits aligned aliases,
early validation, restore targets, service semantics, and role detection. Guard tests traverse the
Cobra tree to reject sibling and cross-layer alias collisions. Recovery tests cover plan,
confirmation, stop escalation, side restores, restart behavior, and structured failure results.
Maintenance regression checks must reparse generated commands with Cobra and exercise the real
libpq client against controlled local endpoints; checking for `-h` and `-p` in argv alone is insufficient.

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
from source commit [`1c6f524`](https://github.com/pgsty/pig/commit/1c6f52401accc8ad6d7e8ab51248895632d7629b)
after the [v1.8.1 CI run](https://github.com/pgsty/pig/actions/runs/33747971725) passed.

## Current status {#status}

Use `pig pb restore` when you intentionally want the pgBackRest primitive and [`pig pitr`](/pitr/)
when you want the managed recovery workflow. See the command reference pages for current syntax and platform requirements.
