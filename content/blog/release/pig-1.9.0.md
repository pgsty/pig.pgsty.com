---
title: "pig v1.9.0"
linkTitle: "v1.9.0"
date: 2026-10-06
description: "600 catalog entries, one-command Xray clients and servers, automatic repository keys, and cargo-pgrx 0.19.3."
tags: [repo, build, catalog, cli]
weight: 1
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.9.0
---

Pig `v1.9.0` adds one-command Xray client/server setup, automatic Pigsty repository-key
preparation, and a refreshed **600-entry extension catalog**. The default `cargo-pgrx`
version is now `0.19.3`; the embedded Pigsty version remains `4.5.0`.

## Xray clients and servers

- `pig build proxy` installs or verifies Xray. `pig build proxy client` configures a
  VLESS/REALITY/Vision HTTP/SOCKS client; `pig build proxy server` configures a Linux server.
  Linux uses systemd; the macOS client uses a dedicated user LaunchAgent.
- Client input accepts a standard VLESS URI, `--from FILE/-`, or explicit connection flags.
  The first client listener is `127.0.0.1:12345`; the first direct server listener is
  `0.0.0.0:443`. Repeated setup preserves existing listeners and server credentials.
- Matching configuration, ownership, permissions, and service state avoid rewrites and
  restarts. Failed client connectivity checks restore prior managed files and service state.
  Replacing a different client requires `--replace --yes`; `--plan` previews either role.
- `server --export-only --export -` exports an existing connection without changing the
  deployment. File exports use mode `0600`; explicit stdout export requires text output.
  Ordinary results and plans omit credentials. The historical VMess positional form remains
  available through V2Ray.

```bash
sudo pig build proxy server --host proxy.example.com --target www.sraoss.co.jp:443 --export ./client.uri
sudo pig build proxy client --from ./client.uri
```

See [`pig build`](https://pig.pgsty.com/build/#build-proxy) for prerequisites, macOS setup,
credential handling, and the separate public-ingress boundary.

## Repository keys

- `repo add`, `repo set`, and `sty boot` prepare the embedded Pigsty public key when selected
  repositories need it. Existing regular key files are reused; missing defaults are installed
  offline at `/etc/pki/rpm-gpg/RPM-GPG-KEY-pigsty` or `/etc/apt/keyrings/pigsty.asc`.
- Implicit default-key failure emits a warning and falls back only for selected Pigsty
  definitions. Default key references remain stable, including APT `signed-by`.
- Explicit signing-key references are mandatory: invalid or unavailable keys fail before
  repository replacement or cache refresh. EL imports explicit references with `rpm --import`.
  Selecting unrelated repositories does not prepare the Pigsty key.

See [`pig repo`](https://pig.pgsty.com/repo/#repository-definitions) for signature-enforcement
defaults and the distinction between key preparation and metadata refresh.

## Catalog and build defaults

- The embedded catalog contains **600 entries**, adding 22 entries to the v1.8.1 snapshot.
  New entries include `edtf_postgres`, `plphp`, `pg_lexo`, `pg_money`, `istore`, `colnames`,
  `pg_statkit`, `pgtelemetry`, `pg_rusage`, `pgexporter_ext`, `pg_statvfs`, and `libx509pq`.
  Package versions and platform-availability metadata are refreshed as well.
- The catalog total includes retained lifecycle records. Installability depends on each
  extension's state and OS/architecture/PostgreSQL matrix; 600 is not a per-platform count.
- `pig build pgrx` defaults to `cargo-pgrx 0.19.3`. An explicit `-v` and extension-specific
  catalog metadata continue to select another required version.
- Platform debug packages remain enabled by default, as in v1.8.1. Use `--nodbg` for RPM
  `debuginfo`/`debugsource` and DEB `dbgsym` suppression; `-s|--symbol` is a deprecated no-op.

## Compatibility

No existing command or flag is removed. New Xray role commands use VLESS/REALITY/Vision;
existing positional VMess commands retain their V2Ray behavior. A server setup result verifies
the local listener and service; firewall, Nginx, cloud security groups, and public reachability
remain separate operator responsibilities.

## Verification

The verified [v1.9.0 tag](https://github.com/pgsty/pig/tree/v1.9.0) points to
[`9eb5488`](https://github.com/pgsty/pig/commit/9eb5488847ea34827a74c9f8bb7b2dd3778f5190). The exact commit passed
[full CI](https://github.com/pgsty/pig/actions/runs/37483835198), including randomized tests,
command race regressions, vet, static analysis, vulnerability scanning, and a release snapshot.
The [Release workflow](https://github.com/pgsty/pig/actions/runs/37484632240) produced eight
Linux/macOS archives and RPM/DEB packages. Published downloads were verified against SHA-256.

## Checksums

```checksums
d0d80bd23a654308598f265ce4b4d4f78d6156c113ce6aa00f82bfc9519a180f  pig-1.9.0-1.aarch64.rpm
e3b25640c9e528f2b883f7e5f4838640a8897857fa22dc1324aca69b72966a7c  pig-1.9.0-1.x86_64.rpm
d7eb266e1b8ab60d20ac582c6b0e3741b7e8516ce1a56df447c0285b3e5dcab9  pig-v1.9.0.darwin-amd64.tar.gz
096284577d0493ddba871b51e820654b358c7f4eb9c11175674a1d21b2718824  pig-v1.9.0.darwin-arm64.tar.gz
a4b5ffca540bc4f924f86398bcad6cb7221ac7520b54b1d3fd32c9877d9cafd2  pig-v1.9.0.linux-amd64.tar.gz
ddfa80fbb34f6738dd68e0d04cd92355711330f6896cd650df7d71b012788def  pig-v1.9.0.linux-arm64.tar.gz
3d955a24a8ff805ee2b6da6428e2b882f97104e2fb597785225269443071d93a  pig_1.9.0-1_amd64.deb
c175b37552147e64590309801800826a0075ae8285ed78178c2adcaec3741471  pig_1.9.0-1_arm64.deb
```

{{< release-card >}}
