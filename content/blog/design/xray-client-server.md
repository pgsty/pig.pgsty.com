---
title: "One-command Xray Clients and Servers"
linkTitle: "Xray Client and Server"
date: 2026-10-05
lastmod: 2026-10-06
description: "One-command VLESS, REALITY, and Vision client/server setup, stable server credentials, and verified proxy connectivity."
tags: [build, cli, install]
weight: 90
authors: [Vonng]
draft: false
---

> **Decision date:** 2026-10-05<br>
> **Status:** Released in [v1.9.0](/release/pig-1.9.0/).<br>
> **Current reference:** [`pig build`](/build/), [operations safety](/design/ops-cli-safety/), and [release history](/release/)<br>
> **Scope:** One-command Xray client and server setup; Linux clients and servers, plus a macOS client. Shared Nginx ingress remains a separate deployment boundary.

## Decision {#decision}

Extend `pig build proxy` with explicit `client` and `server` subcommands. Use VLESS over RAW,
REALITY, and `xtls-rprx-vision` for the new workflow. First server setup generates matching credentials;
repeated setup preserves the existing client connection contract and offers the same standard URI.
The client takes a URI or explicit command-line parameters,
installs Xray, configures the local listener, starts its service, and verifies the connection.
File transfer is optional, not a prerequisite for setup.

Retain the existing command path and `x` alias. The zero-argument command installs or verifies
Xray. The historical `id@host:port [local]` form retains its VMess meaning and default port during
a compatibility period; it must never silently become a VLESS connection with missing parameters.

## Context {#context}

The [previous implementation](https://github.com/pgsty/pig/blob/74cb1281860fae659f2aa4fec2898af34a0c2519/cli/build/proxy.go)
installs `vray`, writes an HTTP-to-VMess configuration to `/etc/v2ray.json`, grants the `v2ray`
group access, writes shell aliases, restarts `v2ray`, and checks an HTTPS request. Existing tests
cover argument parsing, package-manager selection, and credential redaction.

The inspected reference pair uses Xray 26.3.27. The running macOS client exposes HTTP and SOCKS
on one loopback port, 8888, and uses VLESS/RAW/REALITY/Vision with a Chrome fingerprint, disabled
multiplexing, and ML-DSA-65 verification. Both HTTP and SOCKS requests succeeded during the review.
The client UUID, short ID, and SNI match the server's corresponding fields.

The reference Linux server listens on loopback port 9443. Nginx owns public port 443 and selects
the backend by SNI, forwarding a PROXY protocol header. Xray accepts that header, connects to a
REALITY target, sends allowed traffic through `freedom`, and blocks destinations matching
`geoip:private`. This is an ingress composition, not a standalone Xray listener on port 443.

Inspected Pigsty RPM and DEB artifacts for both architectures provide `/usr/bin/xray`,
`/etc/xray.json` with mode 0640 and ownership `root:xray`, an `xray:xray` service account,
`xray.service`, and geodata in `/usr/share/xray`. Their installation scripts reload systemd without
automatically starting or enabling the service. Public repository indexes list version
26.3.27-1PGSTY; artifact inspection and repository listing do not prove installation on every OS.

## Alternatives considered {#alternatives}

- **Rename V2Ray paths and keep only VMess.** Insufficient: it does not provide server setup or the
  working reference protocol. The old template passes Xray's configuration validator, but Xray
  emits a VMess deprecation warning.
- **Build a general proxy manager.** Deferred: subscriptions, protocol catalogs, TUN, transparent
  routing, traffic accounting, and arbitrary configuration import are outside the requested pair.
- **Create a new top-level command now.** Deferred: the existing `build proxy` entry can hold the
  two roles without changing the root grammar or creating a second implementation.
- **Copy the reference server verbatim.** Rejected: a loopback listener requiring PROXY protocol
  cannot serve direct public connections, and existing Nginx port ownership must be respected.
- **Require a connection file for client setup.** Rejected: pasting one URI or supplying parameters
  directly is the primary workflow; a protected file or stdin remains useful for automation.
- **Print generated credentials in ordinary success output.** Rejected: structured results and
  routine logs must remain safe to retain. An explicit export can return a URI to the terminal.

## Contract {#contract}

The implemented role grammar is:

```bash
# On a Linux server, explicitly print the connection URI for copying.
pig build proxy server --host proxy.example.com --target www.example.net:443 --export -

# On a Linux or macOS client, paste the URI returned by the server.
pig build proxy client 'vless://UUID@proxy.example.com:443?encryption=none&security=reality&type=tcp&flow=xtls-rprx-vision&sni=www.example.net&fp=chrome&pbk=PUBLIC_KEY&sid=SHORT_ID&pqv=VERIFY_KEY'

# Alternatively supply connection parameters directly.
pig build proxy client --server proxy.example.com:443 --id UUID --sni www.example.net --public-key PUBLIC_KEY --short-id SHORT_ID --pqv VERIFY_KEY

# Optional protected file input.
pig build proxy client --from ./client.uri

# Reuse a running Linux server's credentials without changing its deployment.
pig build proxy server --host proxy.example.com --export-only --export -

# Non-mutating preview using the default client listener, 127.0.0.1:12345.
pig build proxy client --from ./client.uri --plan

# Explicitly match the inspected client's listener.
pig build proxy client --from ./client.uri --listen 127.0.0.1:8888

# Xray backend behind an already-configured trusted ingress; default bind is 127.0.0.1:9443.
pig build proxy server --host proxy.example.com --target www.example.net:443 --proxy-protocol --export ./client.uri
```

**Server inputs and defaults.** Require the advertised `--host` and a REALITY `--target`.
Public `--port` defaults to 443; the direct listener defaults to that port on all IPv4 interfaces.
On first setup with `--proxy-protocol`, the listener instead defaults to `127.0.0.1:9443`.
An explicit `--listen` changes the bind endpoint without changing the advertised public port.
On repeated setup, omitting `--listen` preserves the existing supported listener rather than
replacing it with a first-setup default.
On first setup, derive SNI from the target hostname unless `--sni` is supplied. On repeated setup,
preserve the existing SNI instead of deriving a replacement. Validate the target's TLS
compatibility before applying configuration; do not silently choose an unrelated camouflage host.

Generate a UUID, X25519 key pair, random eight-byte short ID, and a distinct ML-DSA-65 seed and
verification key. Reuse existing PIG-managed material on repeated setup; ordinary reruns do not
rotate credentials. Rotation and multi-user management require a later explicit contract.
Use `warning` logging, disabled access logging, `decryption: none`, the Vision flow, and an
explicit private-destination blocking rule. Set the geodata environment to the packaged asset path.

**Server idempotence.** Repeating setup with the same inputs must leave existing clients usable
without changing their configuration. Preserve the UUID, X25519 private key and corresponding
client authentication material, short ID, ML-DSA seed and verification key, SNI, and protocol defaults.
With the same advertised host and public port, export the same canonical URI. Generate credentials
only when creating a server configuration for the first time, never because setup runs again.

If the managed configuration and service settings already match the requested state and the
service is running and enabled, perform checks without rewriting files or restarting the service.
If only the service has stopped or become disabled, restore the requested service state using the
existing credentials. Missing, malformed, or ambiguous existing authentication material is an error;
do not repair it by silently regenerating credentials. Reject setup inputs that conflict with the
existing authentication or SNI contract. Such changes need an explicit migration or rotation
contract rather than an ordinary rerun.

**Reuse an existing server.** `server --export-only --host HOST --export DESTINATION` reads the
existing packaged server configuration and exports a connection URI using its current UUID, SNI,
short ID, and derived client verification material. The advertised public port still defaults to
443; never infer it from a loopback backend port. Require one unambiguous supported VLESS/REALITY
inbound, client, SNI, and short ID. Reject ambiguity or malformed material instead of selecting an
arbitrary entry. This mode does not install, rewrite server or service configuration, restart,
enable, or rotate credentials. An explicitly requested file export is its only persistent write.
Derive verification material in process so existing private keys and seeds do not enter subprocess
arguments. This branch performs a read-only query with explicit credential export; the shared server command retains its conservative action annotation.

**Client inputs and defaults.** Accept a single quoted `vless://` positional URI as the primary
workflow. Also support direct parameter mode with `--server host:port`, `--id`, `--sni`,
`--public-key`, and `--short-id`; `--pqv` supplies ML-DSA verification when used by the server.
The direct mode supplies the connection fields while REALITY, RAW, Vision, and Chrome retain
the defaults below. All input forms feed the same validated connection model and renderer.
Keep `--from FILE` and `--from -` as optional file/stdin inputs. Reject mixed connection input
forms rather than silently overriding URI fields with flags. Local options such as `--listen`
remain available for every input form.

`client.uri` is an ordinary UTF-8 text file containing one standard `vless://` URI and an optional
trailing newline; the filename is arbitrary. It is not a new PIG configuration format.
Support the reference combination only: REALITY, Vision, and TCP/RAW. Map URI `type=tcp` to JSON
`network: raw`, `pbk` to `password`, `sid` to `shortId`, and `pqv` to `mldsa65Verify`.
Preserve the ML-DSA verification field; never silently drop it. Reject duplicate or unsupported
parameters that would change connection meaning. The mapping follows the
[upstream sharing specification](https://github.com/XTLS/Xray-core/discussions/716).

On first setup, bind a `socks` inbound to `127.0.0.1:12345`, retaining the existing PIG client
endpoint default. `--listen` can explicitly select `127.0.0.1:8888` to match the inspected client.
On repeated setup, omitting `--listen` preserves the existing managed client's listener.
Provide HTTP support on the same port, UDP enabled, and
multiplexing disabled. Use `encryption: none`, the Vision flow, a Chrome fingerprint, and
`spiderX: /`. The upstream [Socks reference](https://xtls.github.io/en/config/inbounds/socks.html)
documents HTTP support. Validate HTTP and SOCKS independently; a TCP listener alone is insufficient.

The CLI fields map to the existing reference configuration as follows. Client paths below are
relative to its VLESS outbound; server paths are relative to its VLESS inbound.

| CLI field | Client configuration | Server configuration or export |
|:---|:---|:---|
| Server `--host`, `--port`; client `--server` | `settings.vnext[0].address` and `.port` | Advertised URI endpoint; not necessarily the bind endpoint |
| Role-specific `--listen` | Local inbound `listen` and `port` | VLESS inbound `listen` and `port` |
| Client `--id` | `settings.vnext[0].users[0].id` | Matches `settings.clients[0].id` |
| `--sni` | `streamSettings.realitySettings.serverName` | Member of `streamSettings.realitySettings.serverNames` |
| Client `--public-key` | `streamSettings.realitySettings.password` | Derived from `streamSettings.realitySettings.privateKey` |
| Client `--short-id` | `streamSettings.realitySettings.shortId` | Member of `streamSettings.realitySettings.shortIds` |
| Client `--pqv` | `streamSettings.realitySettings.mldsa65Verify` | Derived from `streamSettings.realitySettings.mldsa65Seed` |
| Server `--target` | No direct client field; SNI must be compatible | `streamSettings.realitySettings.target` |
| Server `--proxy-protocol` | No client field | `streamSettings.rawSettings.acceptProxyProtocol: true` |

The reference server keeps `realitySettings.xver: 0`: accepting a PROXY header from Nginx and
forwarding a PROXY header to the REALITY target are different settings. Template defaults preserve
the reference flow, transport security, logging, disabled multiplexing, server private-destination
blocking, and client fingerprint. The public endpoint, bind endpoint, and target have separate roles.

**Platform and service ownership.** Linux uses the configured package repositories and the package
account, configuration path, and unit above. macOS clients use Homebrew Xray, a mode-0600 user
configuration at `~/.config/xray/pig-proxy.json`, and a dedicated user LaunchAgent named
`com.pigsty.xray-proxy`; do not take over another Xray daemon or Homebrew service.
Linux setup requires root and a running systemd instance; macOS client setup requires a regular user and existing Homebrew. macOS server setup is outside this change.

New role setup explicitly starts and enables the managed service; install-only does not start or enable it.
On Linux, PIG owns a bounded `pig-proxy.conf` systemd drop-in for asset location and capabilities.
Direct binding to a privileged port requires only `CAP_NET_BIND_SERVICE` in the bounding and
ambient sets. Reset both sets before assignment because systemd combines positive directives
with the package unit. A loopback backend on an unprivileged port does not need that capability.
Do not depend on permissive host sysctl settings or run Xray as root to make port 443 work.

**Application and recovery.** Parse arguments and preflight paths, port ownership, service conflicts,
and existing configuration before mutations. Recognize managed configuration by its complete
supported shape, not merely an inbound tag. Replacing a different or unsupported client configuration requires `--replace --yes`. Unsupported
server configurations and service units using another account, an explicit different group, or
extra configuration arguments are refused. Preview supports `--plan`, with no installation, credential creation, file writes, or restarts.

Render JSON through Go serialization. Stage protected candidates, validate them with Xray under
the actual service identity, then atomically apply configuration and service changes. Compare
content, ownership, and permissions before treating files as unchanged. On macOS, track persistent
disablement separately from loaded state, enable the managed LaunchAgent on start, and restore both
states on failure. Save original
content, ownership, mode, service enablement, and running state for bounded rollback. Check service
health and connectivity before publishing shell aliases or connection exports. Client setup requires
HTTP 204 from `https://www.google.com/generate_204` through both HTTP and SOCKS, so server outbound
access to this endpoint is part of the client acceptance condition. An application
failure returns nonzero and reports which recovery steps succeeded; an installed package may remain.

Never delete or automatically stop V2Ray. A port conflict stops preflight and produces a migration
instruction. Existing V2Ray configuration remains available for operator-controlled rollback.
Retain `po`, `px`, and `pck` for client convenience, including lowercase proxy variables needed by
build tools. Activating those variables in the calling shell still requires sourcing the generated
shell file and invoking `po`; a child process cannot modify its parent shell.

**Secrets and exports.** `--export FILE` writes the explicitly requested connection export with
mode 0600 and no server private key or ML-DSA seed. `--export -` explicitly delivers one complete
URI on stdout, with non-secret setup diagnostics on stderr. This credential-export mode requires
text output; reject JSON/YAML combinations before mutations instead of putting the URI inside a
structured result. Ordinary setup output remains redacted. Command-line input is supported even
though the caller's shell history or process inspection can retain those supplied credentials;
file and stdin input remain available when that matters.

Treat the whole URI as a credential, including its UUID and authentication fields. Default logs,
plans, JSON/YAML results, and failure details contain only redacted summaries and export paths.
Generate and derive key material in process. Capture validator output privately:
upstream configuration errors can include the invalid secret value. Never use a generic subprocess
capture as a safe credential boundary. Re-exporting to an existing protected file containing the
same canonical URI succeeds without rewriting it. A different existing export is a conflict;
never silently overwrite it or print its contents in a diagnostic.

**Ingress and verification boundaries.** Direct mode is the default one-command server setup.
The explicit `--proxy-protocol` backend mode requires loopback binding and a trusted pre-existing
frontend. PIG does not rewrite Nginx or firewall/cloud rules in this change. A busy public port
causes a clear failure instead of stopping its owner. Backend readiness does not prove public ingress;
server setup reports local checks and leaves external reachability pending until a client handshake
and HTTPS request succeed.

Generating equivalent Xray configurations includes all of the reference pair's protocol and
authentication fields. Reproducing the entire reference deployment also requires Nginx's SNI map,
its PROXY-enabled website backend, and OS-specific service registration. This implementation
manages Xray and its own service settings; it does not claim to recreate that Nginx composition
from a server URI. Configuration equivalence does not imply byte-for-byte preservation of tags,
field order, or installation-specific names.

## Consequences {#impact}

Users get two setup operations connected by one standard URI, or supply client parameters directly,
with matching generated parameters instead of manual JSON editing. No connection file is required.
Both new clients and the historical VMess form default to `127.0.0.1:12345` on first setup.
Direct servers default to the public port on all IPv4 interfaces; PROXY-protocol backends default
to `127.0.0.1:9443`. Repeated setup preserves existing listeners when `--listen` is omitted.
Configuration and service management remain explicit about role, OS, ownership,
and external ingress.

The implementation stays in `cmd/build.go` and focused files under `cli/build`, reusing the
existing plan, output, confirmation, privileged-write, and logging helpers. Current reference pages
change only when executable behavior exists. Release notes change only at the release gate.

## Verification and evolution {#verification}

The initial review on 2026-10-05 inspected the running reference pair, Xray 26.3.27, four RPM/DEB
package artifacts, and the previous VMess behavior. Those observations established the baseline;
they are distinct from the following implementation acceptance.

The [source implementation](https://github.com/pgsty/pig/commit/d090b7c9ab9301c06f9ccb2151c732d598f0e40c) has focused tests for
role grammar, URI/direct/file/stdin equivalence, strict parameter parsing, credential redaction,
listener defaults and preservation, read-only export, malformed and ambiguous server refusal,
server credential reuse, repeated export, protected files, capability selection, and non-mutating
plans. `go test ./...`, `go vet ./...`, static analysis, dead-code and complexity checks, and repeated
randomized race tests for the command/build packages passed locally.

A fresh Debian 13 ARM64 VM used one SSH pipeline to read the existing reference server's connection
and run `client --from -`. PIG installed Xray 26.3.27, configured and enabled the service as `xray`,
and passed its independent HTTP/SOCKS health checks. Additional HTTPS requests through both
protocols returned HTTP 200. Repeating setup preserved configuration bytes and the running PID.
A wrong-UUID replacement returned nonzero, restored the original configuration and service, and
was followed by a successful request. The existing reference server's configuration hash and PID
remained unchanged throughout these read-only exports and client tests.

A second fresh Debian VM exercised direct server creation, privileged-port binding as `xray`,
mode-0640 configuration, mode-0600 export, and repeated setup. Configuration, export content, and
PID were unchanged on the second setup. An export failure after applying a changed listener restored
the original configuration and running service. The generated URI also established a new
REALITY/Vision connection, including ML-DSA verification, with HTTP and SOCKS requests returning
HTTP 200 to a reachable TLS site. This test server's local network could not reach the Google health
endpoint; the full client setup therefore correctly failed and rolled back for that pair. The full
one-command client acceptance passed against the existing reference server.

The [final review fixes](https://github.com/pgsty/pig/commit/5d8660c8c12e6c00b77d409efd2287b8299377b1) cover file ownership,
systemd capability resets, service identity and exact startup arguments, and persistent macOS
enablement recovery. Debian tests first reproduced an unchanged-content configuration with the
wrong group being treated as unchanged, then verified ownership repair with identical bytes and
subsequent setup without a restart. The direct server retained only `CAP_NET_BIND_SERVICE` in both
the bounding and ambient sets; authentication and export content were unchanged. An isolated macOS
LaunchAgent client using the existing Homebrew Xray also passed HTTP/SOCKS requests through the
reference server, unchanged reruns, disabled-state recovery, and wrong-UUID rollback restoring
both configuration and the original disabled state. Requests succeeded after rollback. The
original macOS reference service was not taken over.

These checks do not establish RPM runtime acceptance, fresh Homebrew installation, UDP forwarding,
arbitrary Xray-version compatibility, or a newly deployed PROXY-protocol frontend.
The reference server's existing Nginx/PROXY ingress was exercised by the successful client test;
PIG did not modify that ingress. These additional platform and transport checks remain unverified.

Current bilingual reference and this record are delivered together and checked with `make docs-check`.
Source commits, documentation commits, push/CI, tagged artifacts, and public deployment remain
separate completion gates.

## Current status {#status}

The implementation is present in the verified [v1.9.0 tag](https://github.com/pgsty/pig/tree/v1.9.0)
and its [published release artifacts](https://github.com/pgsty/pig/releases/tag/v1.9.0).
The implementation and local checks described above remain the scope of the evidence.
Repository publication, public documentation deployment, and upgrades of existing systems
remain separate gates.

Nginx ingress automation and credential rotation remain separate future decisions.
