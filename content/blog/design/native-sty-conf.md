---
title: "Compile, Validate, Then Commit: The Native sty conf Pipeline"
linkTitle: "Native sty conf"
date: 2026-02-18
lastmod: 2026-11-12
description: "Why pig sty conf treats Inventory generation as a bounded compiler pipeline with path safety, structural mutations, secret discipline, and atomic output."
tags: [sty, inventory]
weight: 15
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-02-18; the production contract was finalized on 2026-08-14.<br>
> **Status:** Native pipeline released in [pig v1.8.0](/release/pig-1.8.0/); ordered template lookup is implemented in [`ba771a5`](https://github.com/pgsty/pig/commit/ba771a587ec11a55dd43350cce4e9ce36586b308) and the 2026-11-11 region refinement is implemented in [`a95f37f`](https://github.com/pgsty/pig/commit/a95f37f7af430c447953537dd70bdd5b77030a20); both refinements shipped in [pig v1.11.0](https://github.com/pgsty/pig/releases/tag/v1.11.0).<br>
> **Current reference:** [`pig sty conf`](/sty/#sty-conf)<br>
> **Scope:** Generating one validated static Inventory from a trusted Pigsty template; not arbitrary YAML transformation.

## Decision {#decision}

`pig sty conf` should behave like a small compiler: resolve one safe template, parse it, apply a
bounded set of structural mutations, validate the complete candidate, and atomically commit the
output only after every required stage succeeds.

The command does not invoke the legacy `configure` script and does not fall back to raw shell
execution. Its structured result reports selected inputs, effective choices, applied change kinds,
and warnings without returning generated secret values.

The 2026-11-08 extension resolves bare template names in the same fixed order as Pigsty:
root, `ha`, `fork`, `app`, `demo`, then `build`. Resolve once before preflight and mutation;
the selected relative name is the mode used throughout the pipeline and in structured results.

## Context {#context}

Template configuration looks simple until paths, symlinks, multiple IP placeholders, version-pinned
templates, mirrors, proxy environments, generated credentials, and partially valid YAML interact.
A text replacement pipeline can cascade IP substitutions, rewrite unrelated domains, leak secrets,
or truncate the destination after a late validation failure.

The output Inventory may contain administrative credentials, so both file handling and result
rendering are part of the security boundary.

Pigsty groups templates into subdirectories while accepting short names such as `full`. Merely
finding `ha/full.yml` is insufficient: build templates skip IP mapping and admin checks, and
`fork/mssql` and `fork/polar` pin their PostgreSQL version. These rules must follow the selected
template, regardless of the input spelling.

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
- **Recursively search every directory or reject every duplicate basename.** Rejected in favor of
  Pigsty's fixed precedence. Explicit paths select a particular template; unrelated directories
  do not acquire short names automatically.
- **Add a hard-coded alias table or use only the basename for special behavior.** Rejected because
  the installed files determine availability, and `app/mssql` must not inherit `fork/mssql` rules.

## Contract {#contract}

- templates resolve below the Pigsty configuration tree through safe relative names;
- bare names select the first regular file under `conf/`, `conf/ha/`, `conf/fork/`, `conf/app/`,
  `conf/demo/`, then `conf/build/`; explicit relative paths bypass probing;
- leading `./`, the `conf/` prefix, and the `.yml` suffix are optional; traversal components are
  rejected before path cleaning, and invalid selected content does not trigger fallback;
- the resolved mode drives preflight, mutation, and the existing `mode`/`template_path` result
  fields; root `mssql`/`polar` remain version-pinned for older Pigsty installations;
- absolute paths, traversal, path escape, and direct, symlink, symlinked-parent, or hard-link
  source/output aliasing are rejected;
- parsing and IP-collision checks precede external preflight;
- placeholder IPs are mapped simultaneously and unrelated addresses remain unchanged;
- domain replacement matches the exact template token;
- profile, region, proxy, locale, and PostgreSQL-version changes are structural and bounded;
- the 2026-11-11 refinement writes the explicitly selected or detected region even when it is
  `default`, replacing a template's `china` value; the result reports the value actually written;
- generated credentials use one random value per known identifier and expose only identifiers in
  results;
- the complete candidate receives native validation and optional bounded Ansible parsing;
- any failure leaves the destination untouched;
- success writes atomically with mode `0600`.

## Consequences {#impact}

Use `sty conf` to generate a new Inventory from a known template. Use the lossless
`pig inventory` workflow to edit an existing Inventory.

Version-pinned templates keep their version and warn when a conflicting version request cannot apply.

Root precedence preserves existing installations. With the standard grouped layout, `full` and
`ha/full` select the same template, as do `oss` and `build/oss`. Short-name collisions use the
documented order; an explicit path is the stable choice when the template tree contains duplicates.
The resolver does not invent a compatibility alias from `fork/mysql` to `fork/halo`.

## Verification and evolution {#verification}

The native configure direction was first recorded on 2026-02-18. The production refinement landed with
[`74e084e`](https://github.com/pgsty/pig/commit/74e084e), and the final contract synchronization
followed in [`adc4260`](https://github.com/pgsty/pig/commit/adc4260). Tests cover traversal and
aliasing, simultaneous IP mapping, domain boundaries, interactive and closed-input selection,
version handling, proxy and region changes, secret generation and redaction, preflight ordering,
validation failures, permissions, and atomic writes.

Ordered lookup follows Pigsty's
[`d3f3aae`](https://github.com/pgsty/pigsty/commit/d3f3aaeeb34c10be967dd34880b67d68f34b26ff).
The PIG implementation is recorded in
[`ba771a5`](https://github.com/pgsty/pig/commit/ba771a587ec11a55dd43350cce4e9ce36586b308),
including the template resolver, pinned-version handling, and accompanying regression tests.
Validation commands are `go test ./...`, `go vet ./...`, and `make docs-check`.
Regression coverage includes precedence, explicit paths, input normalization, canonical result
fields, build preflight/IP behavior, and old and grouped version-pinned templates.

The 2026-11-08 CLI review used all 54 `.yml` entries, including the Supabase symlink,
from Pigsty commit `d3f3aae` above. The command was `pig sty conf MODE -H FIXTURE -r default -s -n -o json -O OUTPUT`.
For each template, its bare, qualified, and `./conf/ha/full.yml`-style spellings produced identical inventories
and canonical results: 162 invocations in total, with bare names also exercised through `-c`.
Missing and invalid modes, source/output aliasing, root precedence, and explicit-path selection
were checked separately. The 2026-11-11 bidirectional `default` region override is implemented in [`a95f37f`](https://github.com/pgsty/pig/commit/a95f37f7af430c447953537dd70bdd5b77030a20) with regression tests covering templates that start with `china` or omit `region`. These checks cover configuration generation, not deployment.

## Current status {#status}

Use `pig sty conf` to generate a new Inventory from a Pigsty template and
[`pig inventory`](/inventory/) to inspect or edit an existing declaration. Current flags, modes,
and preflight behavior live in the [`pig sty` reference](/sty/).
Ordered template lookup and the `default` region override are included in the
[pig v1.11.0 release](https://github.com/pgsty/pig/releases/tag/v1.11.0), with implementation
evidence in `ba771a5` and `a95f37f`.
