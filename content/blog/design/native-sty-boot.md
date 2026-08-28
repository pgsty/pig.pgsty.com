---
title: "Bootstrapping a Pigsty Controller as a Recoverable Transaction"
linkTitle: "Native sty boot"
date: 2026-08-14
lastmod: 2026-08-28
description: "Why pig sty boot resolves sources before elevation, separates hard failures from finishing warnings, and restores repositories after failed setup."
tags: [sty, repo, install]
weight: 90
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-08-14<br>
> **Status:** Implemented and released in [pig v1.8.0](/release/pig-1.8.0/).<br>
> **Current reference:** [`pig sty boot`](/sty/#sty-boot)<br>
> **Scope:** Preparing a Pigsty controller and its package sources; not deploying a database cluster.

## Decision {#decision}

`pig sty boot` should be one native, failure-aware controller bootstrap workflow. It resolves an
explicit source before privilege elevation, prepares online or offline repositories, installs only
the required controller packages, proves Ansible is usable, and performs bounded finishing checks.

Repository replacement is transactional: definitions are backed up and restored when package
setup fails. Optional conveniences may warn, but invalid explicit input, package failures, and an
unusable final Ansible environment are hard failures.

## Context {#context}

The previous command delegated to a shell bootstrap script. That made source selection, download,
sudo boundaries, repository rollback, error classification, and structured automation difficult to
observe. A present `ansible-playbook` binary could also be mistaken for a usable environment even
when its Python dependencies were missing.

Offline installations added another ambiguity: an already ready controller may still need a local
repository prepared for later nodes.

## Alternatives considered {#alternatives}

- **Continue invoking the legacy script.** Rejected because PIG could not own the transaction or
  explain partial failure reliably.
- **Require the entire command to start as root.** Rejected because explicit downloads and source
  validation do not need privilege and should happen before one bounded elevation.
- **Treat an Ansible binary as readiness.** Rejected because the executable may use a Python
  environment missing required modules.
- **Skip repository work when Ansible is ready.** Rejected because staging an explicit offline
  source is an independent requested effect.
- **Make every finishing check fatal.** Rejected because locale convenience, localhost SSH repair,
  or tree initialization can fail without invalidating an otherwise usable controller.

## Contract {#contract}

- explicit local paths and URLs are validated and never silently fall back to online mode;
- automatic offline sources must pass ownership and permission checks;
- a committed local repository can take precedence over a selected package;
- download and restricted archive extraction use native bounded implementations;
- offline bundles require a `pigsty/repo_complete` sentinel; additional roots are preflighted and
  renamed before `pigsty`, while conflicts and interrupted residue fail closed for manual cleanup;
- privilege elevation happens once after source resolution and can be disabled or made
  non-interactive;
- overwritten repository definitions are recoverable on setup failure;
- readiness executes Ansible and checks the Python modules it will use;
- the result distinguishes ready, offline, online, and existing modes;
- hard failures and finishing warnings are separate structured fields;
- bootstrap does not claim that Pigsty deployment has succeeded.

## Consequences {#impact}

The native workflow is larger than a script launcher, but its side effects and rollback state are
visible. It can stage offline content on an already usable controller and gives automation a
stable result without hiding optional problems.

The command still cannot prove a deployed Pigsty environment. Controller readiness, Inventory
generation, deployment, and live service validation remain separate gates.

## Verification and evolution {#verification}

The native implementation landed in
[`222616e`](https://github.com/pgsty/pig/commit/222616e) and was refined in
[`74e084e`](https://github.com/pgsty/pig/commit/74e084e). Tests cover source precedence,
permission checks, restricted extraction, sudo re-exec, repository rollback, locale recovery,
Ansible/Python readiness, localhost SSH, initialization, warning classification, and structured
results. The release page records delivery in v1.8.0.

An unreleased post-v1.8 refinement extends the offline bundle path to preserve multiple safe
top-level repositories. It keeps the existing sentinel contract and deliberately does not add a
manifest or recovery journal. This refinement is implemented and locally tested, but is not part
of the v1.8.0 release claim above.

## Current status {#status}

`pig sty boot` prepares the controller; it does not run `deploy.yml` or prove database services.
Use the current [`pig sty` documentation](/sty/) for source modes, environment controls, and next
steps.
