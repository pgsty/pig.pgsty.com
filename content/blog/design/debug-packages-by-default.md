---
title: "Why PIG Builds Debug Packages by Default"
linkTitle: "Debug Packages by Default"
date: 2026-09-03
lastmod: 2026-09-03
description: "The build-policy decision that makes RPM debuginfo/debugsource and DEB dbgsym output opt-out rather than opt-in."
tags: [build, cli]
weight: 35
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-09-03<br>
> **Status:** Implemented in [`c90edd1`](https://github.com/pgsty/pig/commit/c90edd19a6dd5d863250f37d4c31d993bef9722e); not yet released.<br>
> **Current reference:** [`pig build`](/build/)<br>
> **Scope:** Debug-package policy for `pig build ext` and `pig build pkg`; individual package recipes remain authoritative for their payload.

## Decision {#decision}

`pig build ext` and `pig build pkg` request the platform's normal debug-package output by default.
PIG does not pass a suppression setting during an ordinary build. Users who need the smaller or
faster artifact set opt out explicitly with `--nodbg`.

On RPM systems, the ordinary build leaves the distribution's `debuginfo` and `debugsource`
machinery enabled; `--nodbg` defines `debug_package` as empty. On Debian and Ubuntu,
`--nodbg` adds `noautodbgsym` to `DEB_BUILD_OPTIONS` while preserving existing options. The old
`-s|--symbol` spelling remains accepted as a deprecated compatibility no-op because debug output
no longer needs to be enabled.

## Context {#context}

The earlier command made RPM debug output opt-in with `--symbol` and otherwise injected
`debug_package %{nil}`. That inverted the platform convention and made the default build less
useful for post-crash analysis. Debian's Debhelper already creates automatic `dbgsym` packages by
default when eligible, and provides `noautodbgsym` as the explicit opt-out.

Debug packages increase build time, storage, and repository volume, but those costs are visible and
manageable. Missing symbols are much harder to reconstruct after the exact source, compiler, and
binary have moved on.

## Alternatives considered {#alternatives}

- **Keep `--symbol` as an opt-in.** Rejected because release-quality artifacts should retain the
  matching diagnostic material by default.
- **Always require debug packages.** Rejected because quick local builds and constrained artifact
  pipelines need an explicit opt-out.
- **Rewrite package recipes from PIG.** Rejected because spec files and `debian/rules` own package
  payload details; mutating them at execution time would be surprising and difficult to audit.
- **Use `nostrip` for DEB opt-out.** Rejected because it changes the main binary instead of merely
  suppressing the separate automatic debug package.

## Contract {#contract}

- without `--nodbg`, PIG adds no debug-suppression macro or environment option;
- on RPM, `--nodbg` adds `--define "debug_package %{nil}"` to `rpmbuild`;
- on DEB, `--nodbg` appends `noautodbgsym` to `DEB_BUILD_OPTIONS` without discarding existing
  values such as `parallel=N` or `nocheck`;
- `--symbol` remains parseable for compatibility but is hidden, deprecated, and redundant;
- structured command results expose `nodbg` and retain `symbol` as the effective inverse value;
- the normal installation package remains the build-success authority; debug packages are
  additional artifacts, not substitutes for it;
- pure SQL, `noarch`, or otherwise ineligible builds need not emit an empty debug package;
- an explicit decision inside a package recipe or an operator-supplied build environment remains
  authoritative. The command default is a policy request, not permission to rewrite recipes.

## Consequences {#impact}

Compiled extensions normally produce more files and consume more build and repository space. In
return, a default build is suitable for stack traces, core analysis, and symbol servers without a
second reconstruction build. Existing scripts that pass `--symbol` keep working, while scripts
that intentionally want the old reduced artifact set must move to `--nodbg`.

Recipe repositories should remove blanket debug suppression where it does not represent a specific
package constraint. That is a separate reviewed change because some packages are architecture
independent, fail debug extraction, or use custom build systems.

## Verification and evolution {#verification}

The superseded opt-in behavior is pinned in the earlier
[`build` flag registration](https://github.com/pgsty/pig/blob/e3d1eb4a86cedddcf49fff398fc69751e861372e/cmd/build.go#L306-L314)
and
[`rpmbuild` command construction](https://github.com/pgsty/pig/blob/e3d1eb4a86cedddcf49fff398fc69751e861372e/cli/build/builder.go#L701-L714).
The replacement was implemented in
[`c90edd1`](https://github.com/pgsty/pig/commit/c90edd19a6dd5d863250f37d4c31d993bef9722e).
Command tests keep `--nodbg` visible and the compatibility flag deprecated. Builder tests verify
that the default RPM argv omits the suppression macro, the opt-out includes it, and the DEB
environment preserves existing options while adding `noautodbgsym` once.

Platform validation should sample a compiled extension on one EL builder and one DEB builder,
checking both default debug artifacts and their absence under `--nodbg`. Recipe-level exceptions
must be reported separately rather than treated as proof that the PIG command ignored its option.

## Current status {#status}

The policy is implemented in source with focused tests at
[`c90edd1`](https://github.com/pgsty/pig/commit/c90edd19a6dd5d863250f37d4c31d993bef9722e),
but it is not yet released. This record becomes Released only after the behavior is present in a
verified PIG release artifact. Recipe cleanup, package builds, repository publication, and
deployment remain separate gates.
