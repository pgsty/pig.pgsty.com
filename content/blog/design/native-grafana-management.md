---
title: "A Bounded Grafana Client Instead of Dashboard Shell Scripts"
linkTitle: "Native Grafana Management"
date: 2026-07-18
lastmod: 2026-10-13
description: "How pig sty grafana manages dashboards and preferences through a native HTTP client."
tags: [sty]
weight: 70
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-07-18<br>
> **Status:** Released in [v1.6.0](/release/pig-1.6.0/); dashboard schema v2 support followed in [v1.6.2](/release/pig-1.6.2/).<br>
> **Current reference:** [`pig sty grafana`](/sty/#sty-grafana)<br>
> **Scope:** Dashboard import, export, cleanup, and selected organization and user preferences.

## Decision {#decision}

PIG uses a native HTTP client to manage Grafana dashboards. Local JSON paths select a dashboard,
a folder, or a complete dashboard directory. This gives load, dump, and cleanup a common selection
model and lets users preview destructive work.

The default directory is the Pigsty dashboard bundle. Users can select another compatible directory.
Cleanup normally selects dashboard UIDs declared by the local files; explicit `clean --all` selects
all dashboards and folders in the active Grafana organization.

## Context {#context}

The previous shell scripts depended on local file layout and offered limited detail about partial
failures. Moving these operations into PIG makes timeouts, authentication, path validation, and
results consistent. A local declaration also provides a precise default cleanup scope.

## Alternatives considered {#alternatives}

- **Keep shell scripts as the public interface.** Network limits, redaction, and structured results
  would remain split across scripts.
- **Expose arbitrary Grafana API calls.** PIG only needs dashboard operations and a few preferences.
- **Select cleanup targets by folder name.** Names can collide. The selected JSON files provide
  dashboard UIDs; folders are removed only after they are empty.
- **Embed a default password.** Credentials belong in user configuration.

## Contract {#contract}

- Limit request duration and response size, and reject unsafe redirects.
- Check public health before authentication. `info` can return health alone when no password is set.
- Resolve credentials from explicit inputs, environment, or Inventory; omit them and response
  bodies from diagnostics and structured results.
- `list` lists all dashboards in the active organization.
- `load` validates and imports the selected local files without deleting live dashboards.
- `boot` selects the existing `pigsty` dashboard as home, stars it, and names the organization Pigsty.
- `init` loads a complete dashboard directory and runs `boot` only after every load succeeds.
- `dump` exports the selected remote scope as deterministic JSON with atomic file writes.
- `clean` deletes locally declared UIDs and then empty folders. `--all` explicitly selects the
  entire active organization. Both modes show a plan and require confirmation.
- `lang` and `style` update the selected preference for the organization and current user.
  Style `auto` maps to Grafana's `system` value.
- Normalize supported dashboard schema v1 and v2 representations when reading and writing them.

## Consequences {#impact}

Load and cleanup use the same local declarations, so users can operate on one dashboard or folder.
A matching UID identifies the target; it does not prove that PIG originally created it. Users must
review the cleanup plan, especially when selecting `--all`.

Datasource provisioning, plugin installation, and user administration remain in Grafana's own tools.

## Verification and evolution {#verification}

The native workflow landed in
[`3060485`](https://github.com/pgsty/pig/commit/3060485). Dashboard schema v2 support followed in
[`67f6e3b`](https://github.com/pgsty/pig/commit/67f6e3b).
The [released tests](https://github.com/pgsty/pig/blob/v1.9.0/cli/sty/grafana_test.go)
cover health-only operation, authentication, load scopes, bootstrap ordering, export stability,
preference updates, local UID cleanup, explicit full cleanup, and changed-plan rejection.
HTTP-client tests cover timeouts, redirects, response limits, and redaction.

## Current status {#status}

The dashboard workflow is released. See [`pig sty grafana`](/sty/#sty-grafana) for path selection,
credentials, and cleanup examples.
