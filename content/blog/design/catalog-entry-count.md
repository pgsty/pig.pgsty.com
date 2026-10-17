---
title: "One Catalog Entry Count for the Website and CLI"
linkTitle: "Catalog Entry Count"
date: 2026-10-16
lastmod: 2026-10-16
description: "Count every catalog record consistently across the website, extension lists, availability summaries, and catalog refresh results."
tags: [catalog, ext, cli]
weight: 96
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-10-16<br>
> **Status:** Accepted; this decision does not establish a release boundary.<br>
> **Current reference:** [`pig ext` catalog count](/ext/#catalog-count)<br>
> **Scope:** Catalog totals and default listing membership; package installation and SQL activation rules remain defined by each entry.

## Decision {#decision}

Use the number of catalog records as the shared extension count. Include packaged SQL utilities
and retained lifecycle records. Calculate CLI totals from the catalog actually loaded or downloaded.

## Context {#context}

The catalog serves package discovery as well as PostgreSQL extension discovery. A packaged SQL
utility can be useful without a control file or a `CREATE EXTENSION` entry point. Excluding it
from the default list and total makes those outputs disagree with the website and catalog file,
even though an explicit name search still finds it.

## Alternatives considered {#alternatives}

- **Count only records classified as PostgreSQL extensions.** Rejected because it gives the CLI
  and website different totals for the same catalog.
- **Add a separate public count for every entry type.** Unnecessary for the current listing contract.
- **Hard-code the announced total in the CLI.** Rejected because a downloaded catalog can differ
  from the bundled one.

## Contract {#contract}

- The unfiltered default list includes every catalog record, including SQL utilities and removed records.
- Text row counts and JSON/YAML `data.count` equal the number of returned records.
- Searches count their matches; `--pkg` continues to count leading package records.
- The global availability text summary uses the complete catalog count.
- Catalog refresh results use the downloaded record count in `data.extension_count` and their message.
- Website totals follow the bundled catalog. A newer downloaded catalog may have a different total.
- Counting a record does not change its DDL requirements, lifecycle state, or platform availability.

## Impact {#impact}

SQL utilities appear in the default list as well as explicit searches. Output field names and
types remain stable. Consumers should interpret the extension total as catalog coverage; it is
not a count of extensions enabled in a database or installable on a particular host.

## Verification {#verification}

The preceding classification rule is preserved in the
[v1.9.0 catalog source](https://github.com/pgsty/pig/blob/9eb5488847ea34827a74c9f8bb7b2dd3778f5190/cli/ext/catalog.go).
Acceptance checks compare parsed record counts with default lists, availability summaries, and
catalog refresh results. They cover packaged SQL utilities and removed records, while keeping
search and package counts specific to their returned rows.

## Status {#status}

Accepted on 2026-10-16. Implementation and release status require their own fixed source revision
and tag or artifact evidence. Use the [current reference](/ext/#catalog-count) for the counting
contract and [release notes](/release/) for version boundaries.
