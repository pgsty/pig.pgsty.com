---
title: "Installation"
linkTitle: "Installation"
description: "How to download and install the pig package manager"
weight: 30
icon: fas fa-download
categories: [Task]
---

## Script Installation

The simplest way to install `pig` is to run the following installation script:

**Default Installation** (Cloudflare CDN):

```bash
curl -fsSL https://repo.pigsty.io/pig | bash
```

**China Mirror**:

```bash
curl -fsSL https://repo.pigsty.cc/pig | bash
```

This script downloads the latest `pig` RPM/DEB package from the Pigsty [software repository](https://pigsty.io/docs/repo/) and installs it using `rpm` or `dpkg`.
Script installation targets Linux x86_64 / aarch64 RPM or DEB distributions. On macOS, use the binary from the release tarball.

## Specify Version

You can request a particular version that is already published on the selected mirror by passing the version number as an argument:

**Default Installation** (Cloudflare CDN):

```bash
curl -fsSL https://repo.pigsty.io/pig | bash -s X.Y.Z
```

**China Mirror**:

```bash
curl -fsSL https://repo.pigsty.cc/pig | bash -s X.Y.Z
```

Mirror publication can lag the GitHub release. For the exact current release, use the GitHub artifacts below.

## Download Release Artifacts

Current `v{{< param version >}}` installation packages (`RPM`/`DEB`/tarball) are available from the [GitHub Release](https://github.com/pgsty/pig/releases/tag/v{{< param version >}}), with published hashes in [checksums.txt](https://github.com/pgsty/pig/releases/download/v{{< param version >}}/checksums.txt). Use the following direct URL pattern:

- `https://github.com/pgsty/pig/releases/download/v{{< param version >}}/<filename>`

```text
v{{< param version >}}
├── pig_{{< param version >}}-1_amd64.deb
├── pig_{{< param version >}}-1_arm64.deb
├── pig-{{< param version >}}-1.aarch64.rpm
├── pig-{{< param version >}}-1.x86_64.rpm
├── pig-v{{< param version >}}.linux-amd64.tar.gz
├── pig-v{{< param version >}}.linux-arm64.tar.gz
├── pig-v{{< param version >}}.darwin-amd64.tar.gz
└── pig-v{{< param version >}}.darwin-arm64.tar.gz
```

After extracting, place the binary file in your system PATH.
The equivalent Pigsty mirror directory becomes available after repository synchronization; check the target URL before using a version-pinned installer command.

## Repository Installation

The `pig` software is located in the [`pigsty-infra`](https://pigsty.io/docs/repo/infra/) repository. You can add this repository to your operating system and then install using the OS package manager:

### YUM

For RHEL, RockyLinux, CentOS, Alma Linux, OracleLinux, and other EL distributions:

```bash
sudo tee /etc/yum.repos.d/pigsty-infra.repo > /dev/null <<-'EOF'
[pigsty-infra]
name=Pigsty Infra for $basearch
baseurl=https://repo.pigsty.io/yum/infra/$basearch
enabled = 1
gpgcheck = 0
module_hotfixes=1
EOF

sudo yum makecache;
sudo yum install -y pig
```

### APT

For Debian, Ubuntu, and other DEB distributions:

```bash
sudo tee /etc/apt/sources.list.d/pigsty-infra.list > /dev/null <<EOF
deb [trusted=yes] https://repo.pigsty.io/apt/infra generic main
EOF

sudo apt update;
sudo apt install -y pig
```

These minimal repository examples deliberately use `gpgcheck=0` / `trusted=yes`, matching PIG's compatibility-oriented defaults. In a security-sensitive environment, install and pin the appropriate signing key, enable signature verification, and review package provenance before adopting the repository.

## Update

To upgrade an existing `pig` version to the latest available version, use the following command:

```bash
pig update            # upgrade pig itself to the latest version
pig update -m         # upgrade using the pigsty.cc mirror
pig update -v X.Y.Z   # upgrade to a version published by the configured repository
```

To update the extension data of an existing `pig` to the latest available version, use the following command:

```bash
pig ext reload        # Update pig extension data to the latest version
```

## Uninstall

```bash
apt remove -y pig     # Debian / Ubuntu and other Debian-based systems
yum remove -y pig     # RHEL / CentOS / RockyLinux and other EL distributions
rm -f /usr/bin/pig    # If installed directly from binary, just delete the binary file
```

## Build from Source

You can also build `pig` yourself. `pig` is developed in Go and is very easy to build. The source code is hosted at [github.com/pgsty/pig](https://github.com/pgsty/pig)

```bash
git clone https://github.com/pgsty/pig.git; cd pig
go mod download
make build
```

The published PIG CLI RPM/DEB release packages are built by the project's GitHub Actions/Goreleaser workflow. This statement applies to the PIG executable packages, not to every PostgreSQL extension package in the catalog.
