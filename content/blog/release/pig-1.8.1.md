---
title: "pig v1.8.1"
linkTitle: "v1.8.1"
date: 2026-09-03
description: "CLI safety and repository hardening, a refreshed extension catalog, Go 1.27.1, and cargo-pgrx 0.19.2."
tags: [cli, repo, build, catalog]
weight: 1
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.8.1
---

Pig `v1.8.1` is a safety, correctness, and maintenance release on top of
[v1.8.0](/release/pig-1.8.0/). It hardens command initialization, privileged log access,
repository and build workflows, release integrity, and structured-output redaction. It also
refreshes the embedded extension catalog and moves the build toolchain to Go `1.27.1` and
`cargo-pgrx 0.19.2`. The embedded Pigsty version remains `4.5.0`.

## CLI safety and correctness

- Read-only and configuration-independent commands no longer require a writable `HOME` or create
  `~/.pig` as a side effect. Leaf commands preserve their declared initialization policy.
- `pig pg log`, `pig pt log`, and `pig pb log` preserve arguments through sudo execution as the
  database OS user and reject unsafe log-file links.
- `pig do` validates Pigsty names and rejects reserved Ansible cluster targets before execution.
- Native PostgreSQL role detection is bound to the selected instance rather than an unrelated
  local default.
- Structured results redact credentials, license material, and build-proxy identifiers while
  retaining truthful command failure.

## Repository and build hardening

- Repository add and remove operations now fail when any requested operation fails, deduplicate
  module selections, and preserve replacement boundaries.
- Offline cache bundles reject unsafe paths, links, special files, and incomplete inputs; archive
  extraction remains rooted and fail-closed. The obsolete exported cache wrapper was removed after
  production moved to the structured result path.
- Build source and artifact validation rejects incomplete or unsafe inputs. `pig build proxy`
  uses the package-provided service contract, treats its operands as optional, and keeps secret
  identifiers out of structured output.
- Self-update verifies release checksums, and release tooling refuses dirty or mismatched-tag
  publication and immutable artifact replacement.

## Toolchain and catalog

- Go is updated to `1.27.1`; Logrus to `1.10.2`; GoReleaser to `2.18.0`; and
  golangci-lint to `2.13.2`.
- `pig build pgrx` now installs `cargo-pgrx 0.19.2` by default. Use `-v` when an extension requires
  an older pgrx line recorded in its catalog metadata.
- The embedded catalog is refreshed from the maintained pgext view. It adds `acdat 0.1.0`, marks
  the superseded `pgcontext_pgvector` entry removed, and updates package versions, repository
  ownership, PostgreSQL coverage, and availability matrices.

## Verification

The release is built from source commit
[`e3d1eb4`](https://github.com/pgsty/pig/commit/e3d1eb4a86cedddcf49fff398fc69751e861372e).
The exact commit passed the full [CI workflow](https://github.com/pgsty/pig/actions/runs/33718574084),
including randomized tests, command race regressions, vet, static analysis, dead-code detection,
vulnerability scanning, and a GoReleaser snapshot. The tag then passed the
[Release workflow](https://github.com/pgsty/pig/actions/runs/33718945217), which produced the
published RPM, DEB, macOS, and Linux artifacts.

## Compatibility notes

- No CLI command or flag is removed in this release.
- Scripts that previously depended on read-only commands creating local configuration should
  create that state explicitly instead.
- The pgrx default changes to `0.19.2`; extension-specific metadata remains authoritative when a
  build requires another pgrx version.

## Checksums

```checksums
839ce3818941318be7707bd6c845f371c609d6f176f04705916108f04cbee38c  pig-1.8.1-1.aarch64.rpm
54183895b09f82fb4d00d75f99e84f6bb4761e4bebd24042d646ee8b309a6d03  pig-1.8.1-1.x86_64.rpm
167891e181d460d478a5ed8637d41017bc73201ec479a5735ca43c09dcf3826f  pig-v1.8.1.darwin-amd64.tar.gz
1338500b4373c3ee3a08d6233202b3f391f5bf69ac0517501884ed2978e17d26  pig-v1.8.1.darwin-arm64.tar.gz
5050cc4444313edc5863acd1a6c20bcfd3ae4af6e849c978d9a5882bc58f60a3  pig-v1.8.1.linux-amd64.tar.gz
ecf5fcf11e35169b557380bbfc717562db5a440271b79b9eb3b8fd74c0c7f167  pig-v1.8.1.linux-arm64.tar.gz
cf0de4f938c7360908ac0e315a7241ab7f3810eb026e28d4b92137ad743dde34  pig_1.8.1-1_amd64.deb
108f50c5e6ccaf87b27cb62e36bbd8b45436039626e7715dbb3912bcbbb6963b  pig_1.8.1-1_arm64.deb
```

{{< release-card >}}
