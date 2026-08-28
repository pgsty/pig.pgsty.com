---
title: "Why PIG Keeps the Cobra Command Layer Flat"
linkTitle: "Flat Cobra Layer"
date: 2026-06-30
lastmod: 2026-08-28
description: "The source-layout decision that keeps one top-level command in one cmd file and moves concrete behavior into cli and internal packages."
tags: [cli]
weight: 30
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-06-30<br>
> **Status:** Active repository architecture.<br>
> **Current reference:** [`pig` command overview](/cmd/) and the [source repository](https://github.com/pgsty/pig)<br>
> **Scope:** Go source ownership and command registration, not the public command taxonomy itself.

## Decision {#decision}

The `cmd` package stays flat. One top-level command belongs in one top-level Go file: `pg.go`,
`pb.go`, `pt.go`, `pe.go`, `sty.go`, `do.go`, `repo.go`, and their peers. Even large command trees
remain in that entry-point file unless there is an explicit decision to change the layout.

The file may be long, but it should contain Cobra concerns: names, aliases, annotations, flags,
argument validation, help, registration, and option mapping. Concrete work belongs in `cli/*`,
`internal/*`, or another implementation package.

## Context {#context}

Earlier command growth produced many small files named after subcommands and several parallel
implementations of confirmation, structured output, plan rendering, and legacy wrapping. It became
difficult to answer simple questions: where is a top-level command registered, which file owns an
alias, and whether two helpers implement the same policy.

PIG's command families are large, but their public grammar is one surface. Keeping that grammar in
one place makes review and collision detection easier, while implementation packages remain
decomposed by responsibility.

## Alternatives considered {#alternatives}

- **A directory per command under `cmd`.** Rejected for normal commands because it scatters one
  public grammar across many packages and encourages business logic near Cobra.
- **One file per subcommand.** Rejected because registration, aliases, and inherited flags become
  hard to audit as one contract.
- **Put everything in `cmd`.** Rejected because tests, reuse, and error handling suffer when
  operational logic depends on Cobra state.
- **Abstract every repeated line.** Rejected because speculative frameworks can hide the command
  grammar; only stable, cross-command glue should be shared.

## Contract {#contract}

- `cmd/root.go` owns root setup, global flags, and top-level registration;
- `cmd/utils.go` owns shared command-layer helpers;
- each normal top-level command has one matching top-level source file and may have one matching
  test file;
- Cobra code validates syntax and maps options, but does not perform the operation;
- reusable confirmation, annotation, structured-output, and plan helpers have one implementation;
- implementation packages accept ordinary options and return typed results or errors without
  depending on Cobra globals.

## Consequences {#impact}

Some command files are intentionally large. The trade-off is accepted because the public surface
can be reviewed as a unit, while the implementation remains split below it. The rule also reduces
file churn when aliases or flags move and gives agents a deterministic starting point.

The boundary is architectural, not cosmetic: a short `cmd` file that hides business logic in
closures is still a violation, while a long file containing only declarative command glue is not.

## Verification and evolution {#verification}

The convention was recorded in
[`9eb70db`](https://github.com/pgsty/pig/commit/9eb70db), followed by the large command-surface
consolidation in [`fb93602`](https://github.com/pgsty/pig/commit/fb93602). Guard tests check alias
collisions and command registration, while package tests exercise the implementation beneath the
Cobra layer.

## Current status {#status}

This remains the repository rule for new work. Public command documentation belongs on this site;
source-layout enforcement remains close to the code so contributors and coding agents encounter it
before editing.
