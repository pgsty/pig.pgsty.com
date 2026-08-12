---
title: "安装"
linkTitle: "安装"
description: "如何下载与安装 pig 包管理器"
weight: 30
icon: fas fa-download
categories: [任务]
---

## 脚本安装

安装 `pig` 最简单的方式是运行以下安装脚本：

**默认安装**（Cloudflare CDN）：

```bash
curl -fsSL https://repo.pigsty.io/pig | bash
```

**中国镜像**：

```bash
curl -fsSL https://repo.pigsty.cc/pig | bash
```

该脚本会从 Pigsty [软件仓库](https://pigsty.cc/docs/repo/) 下载最新版 `pig` 的 RPM / DEB 包，并通过 `rpm` 或 `dpkg` 进行安装。
脚本安装面向 Linux x86_64 / aarch64 的 RPM / DEB 系发行版；macOS 可使用发布压缩包中的二进制。

## 指定版本

您可以指定已经发布到所选镜像的特定版本，将版本号作为参数传入即可：

**默认安装**（Cloudflare CDN）：

```bash
curl -fsSL https://repo.pigsty.io/pig | bash -s X.Y.Z
```

**中国镜像**：

```bash
curl -fsSL https://repo.pigsty.cc/pig | bash -s X.Y.Z
```

镜像发布可能晚于 GitHub Release；如需精确获取当前版本，请使用下方 GitHub 制品。

## 发布产物下载

当前 `v{{< param version >}}` 安装包（`RPM`/`DEB`/压缩包）可从 [GitHub Release](https://github.com/pgsty/pig/releases/tag/v{{< param version >}}) 获取，发布哈希见 [checksums.txt](https://github.com/pgsty/pig/releases/download/v{{< param version >}}/checksums.txt)。直接下载格式如下：

- `https://github.com/pgsty/pig/releases/download/v{{< param version >}}/<filename>`

以下文件名模板中的 `X.Y.Z` 对应当前 {{< param version >}} 版本：

{{< filetree label="当前版本发布产物" >}}
  {{< filetree/folder name="vX.Y.Z" open=true >}}
    {{< filetree/file name="pig_X.Y.Z-1_amd64.deb" >}}
    {{< filetree/file name="pig_X.Y.Z-1_arm64.deb" >}}
    {{< filetree/file name="pig-X.Y.Z-1.aarch64.rpm" >}}
    {{< filetree/file name="pig-X.Y.Z-1.x86_64.rpm" >}}
    {{< filetree/file name="pig-vX.Y.Z.linux-amd64.tar.gz" >}}
    {{< filetree/file name="pig-vX.Y.Z.linux-arm64.tar.gz" >}}
    {{< filetree/file name="pig-vX.Y.Z.darwin-amd64.tar.gz" >}}
    {{< filetree/file name="pig-vX.Y.Z.darwin-arm64.tar.gz" >}}
  {{< /filetree/folder >}}
{{< /filetree >}}

将其解压后，将二进制文件放入您的 PATH 系统路径中即可。
对应的 Pigsty 镜像目录会在软件仓库同步后可用；使用锁定版本的安装命令前，请先检查目标 URL。

## 仓库安装

`pig` 软件位于 [`pigsty-infra`](https://pigsty.cc/docs/repo/infra/) 仓库中。你可以将该仓库添加到操作系统后，使用操作系统的包管理器进行安装：

请按目标主机选择包管理器：

{{< code-group id="install-pig-repository" persist=true label="选择包管理器" copy="all" >}}
  {{< code-tab title="YUM / DNF（EL）" value="yum" lang="bash" >}}
sudo tee /etc/yum.repos.d/pigsty-infra.repo > /dev/null <<-'EOF'
[pigsty-infra]
name=Pigsty Infra for $basearch
baseurl=https://repo.pigsty.io/yum/infra/$basearch
enabled = 1
gpgcheck = 0
module_hotfixes=1
EOF

sudo yum makecache
sudo yum install -y pig
  {{< /code-tab >}}
  {{< code-tab title="APT（Debian / Ubuntu）" value="apt" lang="bash" selected=true >}}
sudo tee /etc/apt/sources.list.d/pigsty-infra.list > /dev/null <<EOF
deb [trusted=yes] https://repo.pigsty.io/apt/infra generic main
EOF

sudo apt update
sudo apt install -y pig
  {{< /code-tab >}}
{{< /code-group >}}

这些最简仓库示例有意使用 `gpgcheck=0` / `trusted=yes`，与 PIG 偏兼容性的默认设置一致。安全敏感环境应安装并固定相应签名密钥、启用签名校验，并在采用仓库前审查软件包来源。

## 更新

若要将现有 `pig` 版本升级至最新可用版本，可以使用以下命令：

```bash
pig update            # 将 pig 自身升级到最新版
pig update -m         # 使用 pigsty.cc 镜像升级
pig update -v X.Y.Z   # 升级到已发布在当前软件仓库中的指定版本
```

若要将现有 `pig` 的扩展数据升级至最新可用版本，可以使用以下命令：

```bash
pig ext reload        # 将 pig 扩展数据更新至最新版本
```

## 卸载

```bash
apt remove -y pig     # Debian / Ubuntu 等 Debian 系统
yum remove -y pig     # RHEL / CentOS / RockyLinux 等 EL 系发行版
rm -f /usr/bin/pig    # 若直接使用二进制安装，删除二进制文件即可
```

## 构建

你也可以自行构建 `pig`。`pig` 使用 Go 语言开发，构建非常容易，源码托管在 [github.com/pgsty/pig](https://github.com/pgsty/pig)

```bash
git clone https://github.com/pgsty/pig.git; cd pig
go mod download
make build
```

正式发布的 PIG CLI RPM/DEB 包由项目的 GitHub Actions/Goreleaser 工作流构建。这里说的是 PIG 可执行程序的软件包，并不代表目录中每一个 PostgreSQL 扩展包都由该流程构建。
