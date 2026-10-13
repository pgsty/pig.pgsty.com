---
title: "The PostgreSQL 'Supply Cut' and Trust Issues in Software Supply Chain"
date: 2025-08-15
lastmod: 2026-10-13
authors: [Vonng]
description: "Why Pigsty built its own PGDG mirror after public mirrors stopped receiving updates."
tags: [repo, install, build]
---

This month, [KubeSphere removed its container images](https://vonng.com/en/cloud/kubesphere-rugpull), prompting a debate about open-source supply chains. A quieter disruption had already affected PostgreSQL: [PGDG had closed its mirror synchronization channels](/article/pg-mirror-break/). For me, that disruption tested how database vendors and cloud providers respond when their upstream supply chain fails.

I was disappointed by the response. I stopped relying on Chinese cloud and university mirrors and built a domestic mirror of the PGDG YUM and APT repositories myself.

## PGDG's "Supply Cut"

PostgreSQL is one of the most widely used open-source databases. Many Linux users install it through the PGDG APT and YUM repositories.
In mid-May, PGDG (PostgreSQL Global Development Group) closed the FTP and rsync channels used to synchronize its repositories. Most mirrors stopped receiving updates and continued serving packages that were months old.

I covered this in detail in ["Chokepoint: PGDG Cuts Mirror Sync Channels"](/article/pg-mirror-break/) on July 7th.
At that time, Germany's xTom appeared to update its mirror manually each month. Most other mirrors still held packages from March, April, or May. When I checked again yesterday, Russia's Yandex had also updated its APT mirror manually; the others were still stale.

| Provider        | Region  | Sync Timestamp     | URL                                                                   |
|-----------------|---------|-------------------|-----------------------------------------------------------------------|
| Alibaba-Cloud   | China   | 2025-03-31        | [sync timestamp](https://mirrors.aliyun.com/postgresql/sync_timestamp)                  |
| Tencent Cloud   | China   | 2025-03-31        | [sync timestamp](https://mirrors.cloud.tencent.com/postgresql/sync_timestamp)           |
| Volcano Cloud   | China   | 2025-03-10        | [sync timestamp](https://mirrors.volces.com/postgresql/sync_timestamp)                  |
| Huawei Cloud    | China   | 2024-01-02        | [sync timestamp](https://repo.huaweicloud.com/postgresql/sync_timestamp)                |
| Tsinghua TUNA   | China   | 2025-03-31        | [historical screenshot](/article/pg-mirror-break/tsinghua.webp)                          |
| Zhejiang Univ   | China   | 2025-03-31        | [sync timestamp](http://mirrors.zju.edu.cn/postgresql/sync_timestamp)                   |
| USTC            | China   | Removed           | [removal notice](https://servers.ustclug.org/2025/05/wine-postgresql-removal/)          |
| TrueNetwork     | Russia  | 2025-01-31        | [sync timestamp](http://mirror.truenetwork.ru/postgresql/sync_timestamp)                |
| JAIST           | Japan   | 2025-03-31        | [sync timestamp](https://ftp.jaist.ac.jp/pub/postgresql/sync_timestamp)                 |
| DOTSRC          | Denmark | 2025-03-31        | [sync timestamp](https://mirrors.dotsrc.org/postgresql/sync_timestamp)                  |
| MirrorService   | UK      | 2025-03-31        | [sync timestamp](https://www.mirrorservice.org/sites/ftp.postgresql.org/sync_timestamp) |
| Princeton Univ  | USA     | 2025-03-31        | [sync timestamp](https://mirror.math.princeton.edu/pub/postgresql/sync_timestamp)       |
| YANDEX          | Russia  | **2025-08-13**    | [mirror](https://mirror.yandex.ru/mirrors/postgresql/)                                  |
| XTOM            | Germany | **2025-07-24**    | [mirror](https://mirrors.xtom.de/postgresql/)                                           |
| PIGSTY          | China   | **2025-08-14**    | [repository docs](https://pigsty.io/docs/repo/)                                        |

## Mirrors "Stop Updating"

For instance, the 17.5 May update fixed [CVE-2025-4207](https://www.postgresql.org/support/security/CVE-2025-4207/) GB18030-related vulnerability,
and the just-released [17.6 series](https://www.postgresql.org/about/news/postgresql-176-1610-1514-1419-1322-and-18-beta-3-released-3118/) fixed 3 CVEs and 55 bugs. If you're a mirror user, you can't update and patch in time. Not to mention PostgreSQL 18 releasing next month. We're still in the early stages — just two PG minor versions behind, but soon it'll be a major version behind. All those accumulated vulnerability patches and security fixes become unavailable to domestic users, creating increasingly larger exposure risks.

From a mirror user's perspective, the flow of updates had stopped. PGDG did provide an alternative: direct downloads through a CDN.

## Why PGDG "Cut Supply"

In the PostgreSQL mailing list, on May 20th, a Korean mirror maintainer asked why rsync sync with PGDG official repository suddenly broke.

Dave Page explained that FTP and rsync had never been officially supported services. The repositories ran on two physical machines and handled about 10 TB of traffic each day, including substantial unwanted traffic. PGDG moved downloads behind Fastly's CDN.

The reasoning is understandable: a CDN can serve users directly across many locations. PGDG kept HTTP access available and closed FTP and rsync. Users who could reach the CDN could switch to the official repository.

## What This Meant for Users in China

The disruption had less impact where users could reach PGDG's CDN. In mainland China, access to those CDN endpoints was unreliable or blocked. Stale domestic mirrors therefore left many users without a practical source of current packages.

A proxy could restore access, but not every user could configure one, and downloads could still be slow. Domestic mirrors remained important. Docker did not remove that dependency: Docker Hub also had access problems, and many PostgreSQL images installed packages from the same APT repositories.

From this angle, **Chinese users faced a real supply-chain bottleneck**. PGDG had supplied an alternative, but local network restrictions made it hard to use. Whatever the cause, someone needed to restore access to current packages.

Common choices included Alibaba Cloud, Tsinghua University's TUNA, Zhejiang University, and USTC. The mirrors I checked had stopped updating. That was frustrating, although these were free services rather than contracted suppliers.

## Supply Chain Risk

In ["How to Safely Use Open-Source Software?"](https://mp.weixin.qq.com/s/-2CeJq1XZdwifZkJY2oXNA) and ["Does Open-Source Software Have Supply Cut Risk?"](https://mp.weixin.qq.com/s/vSxWUcFgbS3D_0tZnBIfdg), Tison distinguishes access to source code from access to a supplier's services. His argument is that a supplier cannot withdraw the rights already granted over an open-source copy. Expectations of continued service often get confused with those rights.

Users depend on a concrete supply chain, however. RPMs, DEBs, container images, and the repositories that distribute them can disappear or stop receiving updates. Keeping that delivery path available takes work and money.

Distribution has costs. Developers may enjoy writing software, but packaging, repository maintenance, and reliable delivery require sustained work. At ¥0.80 per GB, 10 TB of daily traffic would cost thousands of yuan a day. Universities and large internet companies often operate mirrors because they already have the infrastructure and need the packages themselves.

Most users do not pay PGDG or mirror operators. An open-source license does not require its authors to operate a package repository indefinitely. Users who depend on a free service still need to decide how to maintain their own supply chain.

## How to Solve Supply Chain Risk?

Could commercial database vendors solve this? Many Chinese database products derive from PostgreSQL, so I expected at least some vendors to maintain a local mirror. Yet many depended on Alibaba Cloud or TUNA themselves. Others shipped a few RPM files rather than maintaining a repository at all.

I maintain a repository with nine PostgreSQL kernel variants and more than 200 additional extensions—over 400 available extensions when combined with PGDG. Building it has given me substantial packaging experience, alongside the work of Devrim on YUM, Christoph on APT, Álvaro on OCI delivery, and David Wheeler on PGXN.

I still use PGDG for the standard PostgreSQL packages. Devrim and Christoph already do that work well; Pigsty's repository supplements it with extensions. PGDG is therefore an upstream supplier for Pigsty, and Alibaba Cloud had been our indirect supplier in China. When that mirror and the alternatives stopped updating, I needed a replacement.

I reported the problem to Alibaba Cloud and TUNA and discussed it with Dege. Weeks passed without a resolution. I was disappointed, but waiting longer would not solve the problem for Pigsty users.

## I'll Do It Myself

So I built the mirror. FTP and rsync were closed, but HTTP remained available. Yesterday, with help from Claude Code, I spent about two hours writing a synchronization process with apt-mirror and reposync, then downloaded and tested the packages. The solution was much simpler than I had expected. It was frustrating to see such a small amount of work remain undone for so long.

The complete repository occupied hundreds of gigabytes. I selected x86_64 and aarch64 packages for PostgreSQL 13–17 on Debian 11/12/13, Ubuntu 22.04/24.04, and EL 7/8/9/10. Keeping only the latest package versions reduced the mirror to a few dozen gigabytes.
After about two hours of downloading, I published the mirror behind a domestic CDN. PIG v0.6.1 uses this mirror in mainland China, and Pigsty v3.6.1 will follow. Pigsty can now maintain its own path from PGDG to local users.

The mirror is free to use, with or without Pigsty. Public downloads add bandwidth costs, but maintaining the mirror is also part of my commitment to customers, and everyone benefits from that work. Contributions of servers, CDN capacity, or funding are welcome.

```bash
curl https://repo.pigsty.io/pig | bash
pig repo add pgdg  # Add PGDG repository
```

This reminded me of the extension repository. Two years ago, I hoped projects such as Tembo and pgxman would provide the delivery tools I needed. After waiting for months, I built PIG, the extension catalog, and the package repository myself. Projects such as Omnigres and Autobase now use that repository to deliver packages to their users. My own supply chain has become part of theirs.

Publishing source code alone does not provide a reliable supply of packages. **Trust comes from sustained work**: maintaining releases, keeping delivery commitments, and responding when things break. An open-source repository is one part of that commitment.

---

> Originally published on [vonng.com](https://vonng.com/en/pg/pg-mirror-pigsty/).
