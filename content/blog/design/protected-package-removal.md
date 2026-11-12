---
title: "Require Explicit Kernel Aliases for Protected Package Removal"
linkTitle: "Protected Package Removal"
date: 2026-11-11
lastmod: 2026-11-12
description: "A removal boundary based on the resolved package and the user's original operand, while retaining independent language-package removal."
tags: [ext, catalog, cli]
weight: 96
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-11-11<br>
> **Status:** Released in [pig v1.11.0](https://github.com/pgsty/pig/releases/tag/v1.11.0), from implementation commit [`a95f37f`](https://github.com/pgsty/pig/commit/a95f37f); the owner approved the package boundary, explicit aliases, and whole-request rejection on 2026-11-11.<br>
> **Current reference:** [`pig ext rm`](/ext/#ext-rm)<br>
> **Scope:** Package selection for `ext rm`; package-manager dependency simulation remains outside this scope.

## Decision {#decision}

Protect PostgreSQL server packages, shared contrib bundles, and supported replacement kernels.
A protected package may be removed only through an explicitly registered kernel or package-group
alias. An extension operand that resolves to the same package must be rejected before any
package-manager invocation. Independent language packages remain removable through extension names.

The decision depends on both the final package and the original operand. Neither an extension's
`contrib` flag nor a `postgresql` package-name prefix is sufficient.

## Context {#context}

The [baseline resolver](https://github.com/pgsty/pig/blob/2c2d365eae7e9b33cce8b17d852be82ae7f88764/cli/ext/pkgresolve.go)
maps extension names and aliases to packages and deduplicates them before
[removal](https://github.com/pgsty/pig/blob/2c2d365eae7e9b33cce8b17d852be82ae7f88764/cli/ext/rm.go).
On Debian, `pg_trgm` can resolve to `postgresql-18`; on EL it resolves to
`postgresql18-contrib`. `plpgsql` resolves to the server itself. These are larger removal
boundaries than the named extension. A fork extension such as `spock` can similarly resolve
to its `pgedge-18` kernel package.

PL/Python, PL/Tcl, and PL/Perl also have contrib metadata, but their OS packages are separate
from the server and contrib bundle. PL/Tcl and PL/TclU share one language package, as do
PL/Perl and PL/PerlU. Requiring literally one extension per package would reject valid language
removal and ordinary multi-extension packages such as PostGIS.

## Alternatives considered {#alternatives}

- **Reject every contrib extension.** This would also reject independent language packages.
- **Reject every shared package.** Ordinary extension suites intentionally share packages.
- **Trust every alias.** Category aliases can expand to catalog entries backed by kernels;
  being an alias alone does not establish deliberate kernel removal.
- **Allow a protected package whenever another operand authorizes it.** This makes a mixed
  request hide an unsafe extension operand. Validate each operand before deduplication instead.
- **Offer a generic force flag.** An explicit kernel alias expresses which package boundary
  the caller intends to remove; `--yes` should remain confirmation only.

## Contract {#contract}

Maintain a small code-owned registry of protected package templates and the explicit aliases
authorized for them. Expand templates using the target version encoded in the alias when present.
Match complete package names, including supported vendor kernel families; do not infer protection
from a broad prefix or editable catalog flags alone. The registry covers the supported kernel
families. Adding another family requires updating this code-owned boundary; catalog metadata
alone neither adds protection nor authorizes a new removal alias.

The accepted behavior for a PostgreSQL 18 target:

| Operand | Resolved boundary | Decision |
|:---|:---|:---|
| `pg_trgm`, `earthdistance`, `tablefunc` | Debian server or EL contrib bundle | Reject |
| `plpgsql` | Server | Reject |
| `plpython3u`, `pltcl`, `pltclu`, `plperl`, `plperlu` | Independent language package | Allow |
| `vector`, `postgis` | Ordinary extension package | Allow |
| `pg18-server`, `pgsql-server -v 18` | Explicit server group | Allow; show every package in that group |
| `pg18`, `pg18-core`, `pg18-mini`, `pg18-full`, `pg18-main` | Explicit PostgreSQL group | Allow the group's registered protected packages |
| `pg18-contrib` | Separate contrib bundle on EL | Allow through this dedicated alias |
| `pg18-contrib` on Debian | No separate bundle in the current mapping | Reject; do not silently substitute the server |
| `spock`, `snowflake`, `lolor` | pgEdge kernel | Reject |
| `pgedge -v 18` | Explicit pgEdge kernel | Allow |
| `ivorysql_ora`, `babelfishpg_tsql`, `aux_mysql` | Replacement kernel | Reject; name the corresponding kernel alias |
| `pg18-etl`, another category or unrelated group | Any protected package | Reject |
{.full-width}

Equivalent `pgsql-*` aliases use `-v`; existing `postgresql` and vendor kernel aliases are
registered explicitly with their exact package scope. Existing version restrictions remain.
An alias authorizes only its own package family and target major, never another operand.

`orioledb` currently names both an extension and a kernel alias. Preserve its extension meaning
for the protection check and use an unambiguous `orioledb-server` alias for deliberate kernel
removal. This avoids changing the meaning of an extension operand depending on lookup order.

Preserve, for each operand, its original spelling, resolution kind (extension, normalized
extension package, explicit group, or category), matched alias, and complete package list.
Check every operand before building the deduplicated command. If any operand requests a
protected package through an unauthorized route, reject the entire removal, including otherwise
safe operands; perform no sudo or package-manager call. Reordering operands must not change this.

Runtime and `--plan` share the same check. A blocked plan contains failed preconditions and no
executable removal actions; runtime returns a specific protected-package parameter error.
Runtime uses error code `100102`; both return usage exit status `2`. Diagnostics name the operand, resolved package, and
required explicit alias without running or automatically confirming that alternative.
`--yes` does not bypass protection. Existing package-manager confirmation remains in force.

An allowed plan describes package removal, including other extensions sharing an independent
language or ordinary extension package. It does not claim that only one database extension will
disappear. It also does not predict every dependency that APT or DNF may remove.

The same unintended-kernel-selection issue can affect `ext update`. Reusing the provenance check
there is a separate proposed extension of scope; this removal design does not silently ban updates.

## Consequences {#impact}

Scripts removing bundled extensions must select the documented package boundary explicitly or
manage database objects separately. Removing an independent PL package remains supported, even
when the catalog marks it contrib or the package supplies trusted and untrusted variants.

This change requires updates to the bilingual extension reference, alias help, removal result
errors, and plans. Install and category-list behavior should remain compatible.

## Verification {#verification}

Regression tests in [`a95f37f`](https://github.com/pgsty/pig/commit/a95f37f7af430c447953537dd70bdd5b77030a20) exercise both real catalog mappings and controlled resolver fixtures on Debian
and EL across supported majors. They cover server and contrib rejection, language-package allowance,
vendor kernels, the OrioleDB name collision, explicit aliases with a different `-v`, category
expansion, mixed requests in both orders, duplicate packages, and `--yes`.

Rejected runtime requests assert zero calls to the package-manager adapter. Plans
assert failed preconditions, no removal action, and the same rejection reason. Allowed aliases
produce only the listed packages. Cobra tests verify text/JSON behavior and exit
status using isolated fake executables rather than uninstalling host packages.

## Current status {#status}

Implemented in source commit [`a95f37f`](https://github.com/pgsty/pig/commit/a95f37f7af430c447953537dd70bdd5b77030a20), following owner approval on 2026-11-11. The [current reference](/ext/#ext-rm) documents the approved contract, and the pinned source links above establish the original defect; the implementation is included in the [v1.11.0 release artifacts](https://github.com/pgsty/pig/releases/tag/v1.11.0).
