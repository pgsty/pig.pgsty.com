---
title: "Compile, Validate, Then Commit: The Native sty conf Pipeline"
linkTitle: "Native sty conf"
date: 2026-02-18
lastmod: 2026-08-28
description: "Why pig sty conf treats Inventory generation as a bounded compiler pipeline with path safety, structural mutations, secret discipline, and atomic output."
tags: [sty, inventory]
weight: 15
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-02-18; the production contract was finalized on 2026-08-14.<br>
> **Status:** Implemented and released in [pig v1.8.0](/release/pig-1.8.0/).<br>
> **Current reference:** [`pig sty conf`](/sty/#sty-conf)<br>
> **Scope:** Generating one validated static Inventory from a trusted Pigsty template; not arbitrary YAML transformation.

## Decision {#decision}

`pig sty conf` should behave like a small compiler: resolve one safe template, parse it, apply a
bounded set of structural mutations, validate the complete candidate, and atomically commit the
output only after every required stage succeeds.

The command does not invoke the legacy `configure` script and does not fall back to raw shell
execution. Its structured result reports selected inputs, effective choices, applied change kinds,
and warnings without returning generated secret values.

## Context {#context}

Template configuration looks simple until paths, symlinks, multiple IP placeholders, version-pinned
templates, mirrors, proxy environments, generated credentials, and partially valid YAML interact.
A text replacement pipeline can cascade IP substitutions, rewrite unrelated domains, leak secrets,
or truncate the destination after a late validation failure.

The output Inventory may contain administrative credentials, so both file handling and result
rendering are part of the security boundary.

## Alternatives considered {#alternatives}

- **Call the existing shell configure script.** Rejected because parsing, validation, and result
  semantics would remain outside PIG's control.
- **Use global search and replace.** Rejected because IP and domain values need exact placeholder
  boundaries and simultaneous mapping.
- **Write first and validate afterward.** Rejected because a failed candidate could replace a usable
  Inventory.
- **Accept arbitrary absolute templates.** Rejected because the command should compile known Pigsty
  modes, not become a privileged file copier.
- **Return generated passwords for convenience.** Rejected because structured logs and agent traces
  are not secret-delivery channels.

## Contract {#contract}

- templates resolve below the Pigsty configuration tree through safe relative names;
- absolute paths, traversal, path escape, and direct, symlink, symlinked-parent, or hard-link
  source/output aliasing are rejected;
- parsing and IP-collision checks precede external preflight;
- placeholder IPs are mapped simultaneously and unrelated addresses remain unchanged;
- domain replacement matches the exact template token;
- profile, region, proxy, locale, and PostgreSQL-version changes are structural and bounded;
- generated credentials use one random value per known identifier and expose only identifiers in
  results;
- the complete candidate receives native validation and optional bounded Ansible parsing;
- any failure leaves the destination untouched;
- success writes atomically with mode `0600`.

## Consequences {#impact}

The command supports a defined family of templates and mutations rather than arbitrary editing.
That limit is deliberate: existing Inventories belong to the lossless `pig inventory` workflow,
while `sty conf` owns reproducible compilation from a known template.

Version-pinned templates keep their effective version and warn when a conflicting generic request
cannot apply. This is more honest than reporting the requested version while producing another.

## Verification and evolution {#verification}

The native configure direction was first recorded on 2026-02-18. The production refinement landed with
[`74e084e`](https://github.com/pgsty/pig/commit/74e084e), and the final contract synchronization
followed in [`adc4260`](https://github.com/pgsty/pig/commit/adc4260). Tests cover traversal and
aliasing, simultaneous IP mapping, domain boundaries, interactive and closed-input selection,
version handling, proxy and region changes, secret generation and redaction, preflight ordering,
validation failures, permissions, and atomic writes.

## Current status {#status}

Use `pig sty conf` to generate a new Inventory from a Pigsty template and
[`pig inventory`](/inventory/) to inspect or edit an existing declaration. Current flags, modes,
and preflight behavior live in the [`pig sty` reference](/sty/).
