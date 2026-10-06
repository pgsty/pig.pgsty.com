---
title: "pig v1.8.1"
linkTitle: "v1.8.1"
date: 2026-09-03
description: "CLI safety and repository hardening, a refreshed extension catalog, Go 1.27.1, and cargo-pgrx 0.19.2."
tags: [cli, repo, build, catalog]
weight: 2
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

- `pig build ext` and `pig build pkg` keep platform debug packages enabled by default;
  use `--nodbg` to omit them. `-s|--symbol` remains a deprecated compatibility no-op.

- Go is updated to `1.27.1`; Logrus to `1.10.2`; GoReleaser to `2.18.0`; and
  golangci-lint to `2.13.2`.
- `pig build pgrx` now installs `cargo-pgrx 0.19.2` by default. Use `-v` when an extension requires
  an older pgrx line recorded in its catalog metadata.
- The embedded catalog is refreshed from the maintained pgext view. It adds `acdat 0.1.0`, marks
  the superseded `pgcontext_pgvector` entry removed, and updates package versions, repository
  ownership, PostgreSQL coverage, and availability matrices.

## Verification

The release is built from source commit
[`1c6f524`](https://github.com/pgsty/pig/commit/1c6f52401accc8ad6d7e8ab51248895632d7629b).
The exact commit passed the full [CI workflow](https://github.com/pgsty/pig/actions/runs/33747971725),
including randomized tests, command race regressions, vet, static analysis, dead-code detection,
vulnerability scanning, and a GoReleaser snapshot. The tag then passed the
[Release workflow](https://github.com/pgsty/pig/actions/runs/33748002429), which produced the
published RPM, DEB, macOS, and Linux artifacts.

## Compatibility notes

- No CLI command or flag is removed in this release.
- Scripts that previously depended on read-only commands creating local configuration should
  create that state explicitly instead.
- The pgrx default changes to `0.19.2`; extension-specific metadata remains authoritative when a
  build requires another pgrx version.

## Checksums

```checksums
4154b3e49cb499e57d7c7b1ab4ae5e45d03d5d0c2ffe26d6ade64e46db6923cf  pig-1.8.1-1.aarch64.rpm
35c398f409d9293b4f8c0cdf949b19c62d06016ec7e724472143d2327199869d  pig-1.8.1-1.x86_64.rpm
6c08b6a698191b8b6494a0f60880fb17cafa535bad12d5c544333e4625048455  pig-v1.8.1.darwin-amd64.tar.gz
0fb6c86cc18a29aeb74e9d12e717c104087c6ecf5a43250dfcc71cd7681fb868  pig-v1.8.1.darwin-arm64.tar.gz
9219e87433ebd239e0773ae7417fdd08e97bb511312e6747542bf46b6b1bbf2b  pig-v1.8.1.linux-amd64.tar.gz
b30924880f21126ece3afc77ca75794a0ceb77964cdfd8bc20da72d9d3273078  pig-v1.8.1.linux-arm64.tar.gz
6fc304501671921b18439223c630c7d4635b10ac75493d5c12a5987ff80c618e  pig_1.8.1-1_amd64.deb
1a70cd71f6c1f443812fe30535427891513c0ba03be219ac21f1a3d6fd450051  pig_1.8.1-1_arm64.deb
```

{{< release-card >}}
