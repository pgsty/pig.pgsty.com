---
title: "Target PostgreSQL Versions for Category Aliases"
linkTitle: "Category Alias Target Versions"
date: 2026-11-06
lastmod: 2026-11-06
description: "Use the requested PostgreSQL major when dynamic category aliases select extension packages."
tags: [catalog, ext, install]
weight: 97
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-11-06<br>
> **Status:** Implemented in source commit [`7c069dc`](https://github.com/pgsty/pig/commit/7c069dcdc47a9fb51acd56a06dd2a4132723e6dd); not released.<br>
> **Current reference:** [`pig ext` category aliases](/ext/#category-aliases)<br>
> **Scope:** Dynamic `pgN-*` and `pgsql-*` category aliases that resolve extension package groups.

## Decision {#decision}

Stable category aliases use the requested PostgreSQL major when evaluating package visibility.
`pgN-<category>` takes the major from the alias, and `pgsql-<category> -v N` uses the same target
major. Package templates are rendered for that requested major after visibility is evaluated.

The catalog remains the source of package names and platform availability. This lets refreshed
metadata describe package splits and version-specific support without adding extension-specific
branches to the alias resolver. The current catalog describes EL PG14/15 pgaudit as
`pgaudit_14`/`pgaudit_15`, PostGIS 3.7 as `postgis37_N`, and the address-standardizer and
PG16+ Tiger Geocoder packages as separate entries.

The current Beta PostgreSQL placeholder keeps its compatibility rule: it borrows the latest stable
matrix and retains PGDG-origin entries only, because the catalog does not yet have a matrix row for
that target.

## Context {#context}

Before this change, `pgsql-*` category aliases evaluated stable targets against the latest stable
catalog row. A command such as `pgsql-gis -v 14` could therefore include a package whose matrix
entry existed only for PG18, such as the Tiger Geocoder. The numbered form, `pg14-gis`, already
used the requested major and produced a different package group.

The same resolver also contained a hardcoded EL pgaudit rename for PG14 and PG15. That rename
reflected historical package names, while the current pgaudit recipes and catalog use
`pgaudit_$v`. Keeping the package rule in code made the alias result stale when the package
metadata was corrected.

## Alternatives considered {#alternatives}

- **Keep the latest stable template for every `pgsql-*` alias.** Rejected because an explicit
  `-v N` must respect the requested PostgreSQL-major support matrix.
- **Add more extension-specific package exceptions.** Rejected because pgaudit and PostGIS
  package names and support rows are catalog data that can be rendered by the common resolver.
- **Use only RPM/DEB version metadata.** Rejected because the package matrix also records OS,
  architecture, source repository, hidden state, and unavailable cells.
- **Remove Beta borrowing.** Rejected because the current Beta target has no catalog row of its
  own; it continues to need a stable template with the existing PGDG-only restriction.

## Contract {#contract}

- A stable `pgN-<category>` alias evaluates visibility against PostgreSQL major N.
- A stable `pgsql-<category>` alias evaluates visibility against the command's target version;
  an explicit `-v N` therefore has the same result as `pgN-<category>`.
- When no target reaches the resolver, the existing command probing and operation defaults remain
  in force; a zero target inside the alias parser resolves to the latest stable major.
- Package templates are rendered for the requested target major. Visible leading non-contrib
  entries are deduplicated by rendered package name.
- On a known operating system, a missing matrix cell remains unavailable. Existing unknown-OS
  metadata fallback behavior is unchanged.
- The Beta target borrows the latest stable matrix and keeps only PGDG-origin entries. This is the
  sole stable-template borrowing exception.
- The configured OS repository must provide the package named by the catalog; the resolver does
  not migrate an already installed package between historical names.

## Consequences {#impact}

`pig ext add pgsql-gis -v 14 --plan` and `pig ext add pg14-gis --plan` now select the same PG14
matrix. PG14/15 no longer inherit the PG18-only Tiger Geocoder entry. The corrected pgaudit catalog
rows produce `pgaudit_14` and `pgaudit_15` on EL, and the PostGIS 3.7 catalog rows produce
`postgis37_N` plus the independent address-standardizer and PG16+ Tiger Geocoder packages where
the matrix says they are available.

The behavior is easier to refresh because package-specific naming lives in the catalog. Users still
need a repository containing the selected package, especially for the Pigsty-origin EL pgaudit
PG14/15 rows.

## Verification and evolution {#verification}

Source commit [`7c069dc`](https://github.com/pgsty/pig/commit/7c069dcdc47a9fb51acd56a06dd2a4132723e6dd)
adds regression coverage for the target-version, numbered-alias, default-version, Beta, and
future-major paths in `cli/ext/category_alias_test.go`. Embedded catalog tests in
`cli/ext/catalog_embedded_test.go` cover pgaudit across EL8/9/10 and both architectures, and
PostGIS, address-standardizer, and Tiger Geocoder package resolution across EL and Ubuntu PG14-18.
The catalog changes are in `cli/ext/assets/extension.csv`.

The committed source was checked with `git diff --check`, `go test -shuffle=on -count=1 ./...`,
`go vet ./...`, `go test -race -shuffle=on -count=1 ./cli/ext ./cli/install`, `staticcheck ./...`,
the configured complexity lint, and `deadcode ./...`. This record describes an implemented source
contract; a future release tag is separate evidence.

## Current status {#status}

The target-version behavior is implemented in the source commit above and documented in the
[`pig ext` reference](/ext/#category-aliases). Release notes and deployment status remain separate
from this implementation record.
