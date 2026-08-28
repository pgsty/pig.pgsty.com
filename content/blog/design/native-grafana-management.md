---
title: "A Bounded Grafana Client Instead of Dashboard Shell Scripts"
linkTitle: "Native Grafana Management"
date: 2026-07-18
lastmod: 2026-08-28
description: "Why pig sty grafana owns a small HTTP contract for dashboard lifecycle, preferences, and safe cleanup without becoming a general Grafana administration client."
tags: [sty]
weight: 70
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-07-18<br>
> **Status:** Implemented in v1.6.0; Grafana dashboard schema v2 support followed in v1.6.2.<br>
> **Current reference:** [`pig sty grafana`](/sty/#sty-grafana)<br>
> **Scope:** Pigsty-owned dashboard folders, dashboards, and UI preferences; not general Grafana provisioning.

## Decision {#decision}

PIG should manage the Grafana assets that ship with Pigsty through a bounded native HTTP client.
It may inspect readiness, list managed assets, load or initialize dashboards, dump them, remove only
owned dashboards, and adjust the supported language and style preferences.

The command must not grow into a general Grafana administration API. Datasources, organizations,
users, arbitrary folders, plugins, and unrelated dashboards remain outside its ownership.

## Context {#context}

Legacy dashboard workflows were tied to scripts and local file layout. They offered little
structured evidence about which endpoint was contacted, what assets were owned, or why a partial
failure occurred. At the same time, calling the full Grafana API without a narrow ownership model
could delete user content or expose credentials in arguments and diagnostics.

A native client was justified only if its network, authentication, ownership, and result boundaries
were explicit.

## Alternatives considered {#alternatives}

- **Keep shell scripts as the public interface.** Rejected because timeout, redirect, response-size,
  redaction, and structured-result behavior would remain inconsistent.
- **Expose arbitrary Grafana API calls.** Rejected because it would make PIG a second Grafana CLI
  without a stable product boundary.
- **Delete by folder name alone.** Rejected because names are not sufficient proof of ownership.
- **Embed a demo password.** Rejected because default credentials become long-lived secrets and
  encourage unsafe automation.

## Contract {#contract}

- every request has bounded connection and response behavior;
- unsafe redirects and oversized responses are refused;
- public health is checked before authenticated operations;
- credentials come from explicit safe inputs, environment, or Inventory resolution, with no
  embedded default password;
- command-line passwords are documented as an emergency path because argv and shell history may
  expose them;
- errors and structured results never contain credentials or response bodies;
- load and init operate on Pigsty's known dashboard bundle;
- clean removes only assets proven to be PIG/Pigsty-owned;
- language and style accept a fixed vocabulary and map `auto` to Grafana's system preference;
- schema v1 and schema v2 dashboard representations are normalized at the client boundary.

## Consequences {#impact}

The native client produces better plans, error classification, and automation results, but it must
track the small Grafana API surface it owns. Supporting a new dashboard schema is acceptable;
supporting unrelated Grafana resources is not implied.

Operators can use another Grafana client for general administration without PIG claiming authority
over those resources.

## Verification and evolution {#verification}

The native dashboard workflow landed in
[`3060485`](https://github.com/pgsty/pig/commit/3060485). Tests cover health, authentication,
timeouts, redirects, size limits, ownership checks, preference requests, redaction, partial
failures, and load/dump behavior. Dashboard schema v2 support followed in
[`67f6e3b`](https://github.com/pgsty/pig/commit/67f6e3b) and shipped in v1.6.2.

## Current status {#status}

`pig sty grafana` is the supported PIG entry point for the bounded Pigsty dashboard lifecycle.
Use the current [`pig sty` reference](/sty/) for commands and credentials; use Grafana-native tools
for resources outside this ownership boundary.
