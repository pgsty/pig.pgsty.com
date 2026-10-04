---
title: "Install the Pigsty Repository Key Automatically"
linkTitle: "Automatic Pigsty Key"
date: 2026-10-04
lastmod: 2026-10-04
description: "Prepare the Pigsty key best-effort, reuse existing files, and fall back with a warning unless repository metadata explicitly names a key."
tags: [repo, sty]
weight: 95
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-10-04<br>
> **Status:** Implemented and locally tested; unreleased.<br>
> **Current reference:** [`pig repo`](/repo/)<br>
> **Scope:** Installing the existing embedded Pigsty public key during repository configuration.

## Decision {#decision}

When a selected module contains an available `pigsty-infra` or `pigsty-pgsql` repository,
prepare the embedded Pigsty public key before changing repository definitions. Apply this in
the shared configuration workflow so `repo add`, `repo set`, and callers that reuse it agree.
Reuse an existing key file. Automatic installation is best-effort; an explicit signing-key
reference in selected repository metadata makes installation failure fatal.

## Context {#context}

The [source baseline](https://github.com/pgsty/pig/blob/1c6f52401accc8ad6d7e8ab51248895632d7629b/cli/repo/add.go)
installed the key only when a caller requested `GPGCheck`, as native `sty boot` does.
Ordinary `repo add/set` therefore omitted a public key already shipped inside PIG.

The key is needed by both Pigsty repositories. Their membership spans `pigsty`, `infra`,
`pgsql`, and the default `all` selection, so checking only the literal argument `pigsty`
would miss normal usage.

APT does not discover files under `/etc/apt/keyrings` automatically. A repository must reference
the prepared file with `signed-by`; otherwise a successful write still leaves `NO_PUBKEY`
warnings during cache refresh.

## Alternatives considered {#alternatives}

- **Download the key at runtime.** The embedded release input already supplies it and works
  offline, without adding a network or external-tool dependency.
- **Install the key on every repository operation.** Unrelated repositories should not cause a
  Pigsty key write. Resolve membership and platform availability first.
- **Fail every repository operation when automatic key installation fails.** Rejected because
  optional key preparation should not prevent the existing compatibility mode from working.
  Explicit signing-key metadata remains a strict boundary.
- **Enable all signature checks at the same time.** Publisher identity, RPM package signatures,
  and APT metadata authentication are separate contracts. Automatic key installation does not
  establish signing coverage for every package or mirror.

## Contract {#contract}

- Validate requested modules before installing the key. A rejected replacement does not
  install it or move repository files.
- Match the two Pigsty repository identifiers in resolved modules, including custom modules;
  the URL's hostname alone does not select a signing identity.
- Write the existing embedded key to `/etc/pki/rpm-gpg/RPM-GPG-KEY-pigsty` on EL or
  `/etc/apt/keyrings/pigsty.asc` on Debian/Ubuntu when installation is needed, with mode `0644`.
- Check for an existing regular key file first, including a symlink resolving to one; reuse it
  without changing its contents or permissions. If the existence check fails, attempt installation.
- Create missing parent directories through the existing sudo fallback and use the atomic
  file writer. An occupied directory or dangling symlink is an installation error.
- Without explicit key metadata, installation failure warns and continues. Only selected Pigsty
  definitions fall back to APT `trusted=yes` or RPM `gpgcheck=0` and `repo_gpgcheck=0`.
- A non-empty `gpgkey` or `signed-by` value in any selected Pigsty definition makes installation
  failure fatal before backup, repository writes, or cache refresh. Do not replace explicit
  references or silently downgrade those definitions. Custom key acquisition remains outside
  this embedded-key installer.
- After successful preparation, fill missing key references in selected Pigsty definitions:
  `gpgkey` on EL and `signed-by` on Debian/Ubuntu. Preserve explicit references.
- Successful ordinary operations preserve signature-checking settings. `sty boot` requests signing on
  successful key preparation and follows the same implicit-key fallback on failure.
- Put fallback warnings on stderr and in `repo add/set`'s `data.warnings`; `sty boot` retains
  them in its own warnings. Do not import keys into RPM's database or APT's global trust store.
- Repository rollback restores definitions; an already installed public-key file remains.

## Consequences {#impact}

Adding a Pigsty repository also attempts to prepare its public-key file, including on offline
hosts. Ordinary key failures no longer prevent repository setup. Falling back disables signature
verification for those Pigsty definitions and is reported explicitly. A successful existence
check preserves the administrator's existing file; it does not validate that file's contents.
Third-party repository trust remains unchanged.
The maintained [repository reference](/repo/) describes the resulting defaults and paths.

## Verification and evolution {#verification}

The [automatic-key implementation](https://github.com/pgsty/pig/blob/ec86bb83824309370e258c8ac1dca87336865588/cli/repo/key.go)
and [repository regression tests](https://github.com/pgsty/pig/blob/ec86bb83824309370e258c8ac1dca87336865588/cli/repo/add_key_test.go)
are recorded in source commit `ec86bb8`. Local regression tests exercise EL, Debian, and Ubuntu on both supported architectures,
default and composite selections, existing-key reuse, denied existence checks, custom modules,
unavailable repositories, implicit-key fallback, and explicit-key failure before repository
mutation. Existing replacement tests continue to cover rollback.

Actual CLI tests on local EL9, EL10, Debian 12, and Ubuntu 24 ARM64 guests use isolated mount namespaces. They
verify installation as an ordinary user through sudo with missing key directories, exact embedded
bytes and permissions, repeated execution, composite selections, parseable structured output,
implicit-key failure continuing with a warning, and explicit-key failure stopping before
repository replacement. Real DNF/APT refreshes use fresh isolated caches, and the resulting indexes
are queried for available packages. APT tests also verify that the installed key is referenced
without `NO_PUBKEY` warnings and that explicit `signed-by` with `trusted=no` authenticates the
metadata. These checks do not install packages or verify RPM package signatures. The guests'
original repository definitions, keys, and caches remain unchanged.

## Current status {#status}

The automatic installation path is implemented and locally tested. It has no verified release
tag yet. Source integration, release artifacts, and public documentation deployment remain
separate gates; consult [release history](/release/) for shipped versions.
