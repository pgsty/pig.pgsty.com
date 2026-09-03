---
title: "Build and Packaging: An Overlooked but Scarce Skill"
linkTitle: "Build and Packaging"
date: 2025-08-18
lastmod: 2026-08-30
description: "On the rare craft of production-grade Linux packaging in the PostgreSQL ecosystem."
tags: [build, repo]
authors: [Vonng]
---

I was recently chatting with my friend Yurii, the founder of Omnigres. He wants to hire a PostgreSQL packaging expert and has even coined a title for the role: EEE, or Extension Ecosystem Engineer. It is an interesting idea. The [job description is public](https://github.com/omnigres/rfc/pull/2/files), so I have included it at the end.

## A Scarce Skill: Linux Packaging

I think this job description asks for a little too much: DevRel + SRE + DBA + build engineer + PostgreSQL specialist, all in one person. It almost reads as though it were written for me. But I have genuinely never met anyone else with that exact combination, so I advised Yurii that hiring a build engineer who knows Debian and Enterprise Linux packaging inside out would be more realistic. Even that will be difficult, though. Scarce hardly begins to describe people who understand build and packaging work. DevRel talent may be scarcer still.

The context here is specifically building and packaging PostgreSQL kernels and extensions for Linux. Most of the code is C or C++, with some Rust, Java, Go, and other languages mixed in. The main deliverables are RPM and DEB packages distributed through YUM and APT repositories. I believe this is a remarkably valuable skill that gets very little attention.

## When Did I Realize This?

I first recognized the importance of packaging in 2017, during an interview with Pivotal. One of the interviewers asked, almost in passing, "Do you know how to package software? We don't have anyone who does." I wondered what kind of package he meant. RPMs? As it turned out, yes. Later, Yao of YMatrix, who had also come out of Pivotal, asked me much the same thing: "You know build and packaging work pretty well, don't you? We badly need that skill right now." That made the gap stick in my mind.

Since then, I have examined software released by many database companies in China and abroad. Their packaging is often painful to behold. How, for example, did Greenplum used to ship to customers? As a single CentOS 7.9 RPM. That was it. Wanted to run it on EL 8, EL 9, Ubuntu, Debian, or another Linux distribution? Tough luck.

Alibaba Cloud's PolarDB for PostgreSQL and HighGo's IvorySQL also started with only one or two EL RPMs. After a great deal of pushing from me, they eventually covered the mainstream Linux distributions. For the MySQL-compatible OpenHalo kernel and OrioleDB, I simply stepped in and packaged them myself.

![Pigsty database kernel catalog](/article/packaging-skill/01.webp)

## Why Build and Packaging Matter

Packaging expertise is scarce, but where does its value come from? Most end users **do not care whether your software is open source**. What they care about is whether a stable, reliable—and **preferably free**—binary package is available to download. Greenplum is now closed source, yet friends still ask me from time to time for Greenplum RPMs. Yao's YMatrix, a closed-source branch of GP7, is commercial software. But it offers a free trial download, so people can still use it. Whether its source is open hardly matters to them.

A more recent example is the [KubeSphere community's binary cutoff](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247490196&idx=1&sn=6c9a10f35182119ac8ad3171d732a596&scene=21#wechat_redirect). The source code was still there, but the project deleted its binary artifacts—the container images—and that directly affected end users. Whether the code was open source made no practical difference to them. The real supply-chain chokepoint has never been source code, but the finished software artifacts users actually run.

## Packaging Makes Open Source Self-Reliant

Open-source expert Tison explored this issue in depth in his articles ["How Can You Use Open Source Software with Confidence?"](https://mp.weixin.qq.com/s?__biz=MzIzMDEwODM5OQ==&mid=2647852959&idx=1&sn=54447d633589061f469174818654e958&scene=21#wechat_redirect) and ["Can Open Source Software Be Cut Off?"](https://mp.weixin.qq.com/s?__biz=MzIzMDEwODM5OQ==&mid=2647852894&idx=1&sn=a18cb659f93dbef7bfab20ed312311e3&scene=21#wechat_redirect). His conclusion is that open-source software itself cannot be cut off, but its artifacts can. If you want to use open source with confidence, the most important safeguard is to keep a local copy of the software or operate your own package repository. Build and packaging work is the foundation for that independence.

Consider the recent [PGDG repository supply disruption](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247490317&idx=1&sn=ccc027f478d1f6b930e145325894588b&scene=21#wechat_redirect). Almost every mirror worldwide lost synchronization with the PGDG upstream and remained stuck on versions five months out of date. At the time, only xTom in Germany, Yandex in Russia, and Pigsty in China were providing manually updated mirrors of the latest PGDG packages.

Of course, a mirror merely copies binary artifacts built by someone else. Imagine the more extreme case: instead of merely stopping incremental synchronization, PGDG locked everything down completely. To build an independent repository from scratch, with separate packages for RISC-V, MIPS, ARM, and the rest of the architectural menagerie, you would still have to cross the build-and-packaging barrier.

## Not All Packaging Is Equal

Someone will inevitably say, "But it is open source. You can compile it yourself." That is true. Software written in modern languages often comes with a much smoother packaging workflow. Go programs, for example, are exceptionally easy to build and package. Tools such as GoReleaser can build an entire cross-platform matrix in one shot, generate RPM and DEB packages, build and push Docker images, and create a GitHub Release automatically. With vibe coding, you could probably implement such a workflow in under half an hour.

But that is not what we are talking about. We are talking about ecosystem-scale projects such as Debian and PostgreSQL, especially the C and C++ software at their core. Packaging the PostgreSQL database is not a matter of producing a handful of RPMs, either. Across the 10 Linux distributions and five PostgreSQL major versions I support, plus extensions and tools, I now provide roughly 40,000 RPM and DEB packages.

Build and packaging work is not easy. You must untangle dependencies involving glibc, ICU, OpenSSL, and PostGIS's enormous dependency tree; deal with the obscure system libraries required by assorted extensions; resolve version conflicts across distributions and even across major releases of the same distribution; and master a whole toolbox that includes CMake, Make, Ninja, Cargo, and more.

## Why Not Docker?

Docker looks like a shortcut around packaging: build once, run anywhere. If only. Docker does remove Linux distribution releases—EL 9, Debian 12, Ubuntu 24.04, and so on—from the build matrix. But you still need separate builds for PostgreSQL major versions, system architectures, and hundreds of extensions in multiple versions. And if you inspect PostgreSQL Docker images, you will find that their Dockerfiles often still use `apt install` to install PGDG's DEB packages. Linux packages are upstream of Docker images, not the other way around.

Second, extensions are one of PostgreSQL's defining advantages over other databases, yet container images still have no elegant answer to the problem of persistent PostgreSQL extensions. You do not know which of hundreds of extensions a user will need, but installing every one of them makes an image bloated and foolish. Álvaro is doing some pioneering work in this area, but in my view the approach remains some distance from mature operational practice.

[Is Putting a Database in Docker a Good Idea?](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247486572&idx=1&sn=274a51976bf8ae5974beb1d3173380c1&scene=21#wechat_redirect)

[Should Databases Be Deployed in Kubernetes?](https://vonng.com/en/db/db-in-k8s/)

## How I Got Into Packaging

I started doing this work only about two years before writing this article. I wanted Pigsty to support self-hosted Supabase, but Supabase depended on more than a dozen PostgreSQL extensions, most of which were absent from the official PGDG binary repositories. I asked Devrim, the maintainer of the PGDG YUM repository, about them. He told me that extensions written in Rust would never make it into PGDG because they took too long to compile. So I rolled up my sleeves and built the RPMs myself.

Once the RPMs existed, I thought I might as well produce DEBs too. And once I supported more than a dozen PostgreSQL extensions, why not package the other 200-plus extensions missing from the official PGDG repositories?

Step by step, that effort grew into the PostgreSQL extension repository I maintain. At the time of writing, it contained nine flavors of the PostgreSQL kernel and more than 200 PostgreSQL extensions—423 available extensions when combined with PGDG. It offered the world's broadest selection of usable PostgreSQL extension artifacts. Without false modesty, when it comes to PostgreSQL build and packaging work, Devrim on the YUM repository, Christoph on the APT repository, Álvaro on the OCI repository, David Wheeler on PGXN, and I are among the strongest practitioners in the field.

The clearest example is Supabase. As the darling of the AI wave and perhaps the database sector's biggest winner, it should have drawn an army of vendors into the market. Yet at the time of writing, the only open-source PostgreSQL distributions capable of delivering self-hosted Supabase were Pigsty, my Linux-native distribution based on RPM and DEB packages, and Álvaro's StackGres, based on OCI images and Kubernetes.

![Supabase self-hosting documentation listing Pigsty and StackGres](/article/packaging-skill/02.webp)

That is because we solved the build, packaging, and distribution problems for Supabase's specialized extensions. This is the actual bottleneck. Even if Supabase publishes the source code for those extensions—and later switches to the OrioleDB kernel—how many people understand that code? How many users can turn it into something they can actually run?

Engineers who know EL or Debian packaging do exist. Engineers who also understand the PostgreSQL ecosystem well enough to build hundreds of PostgreSQL packages across more than ten Linux distributions are genuinely rare.

## A Vanishingly Rare Craft

In practice, I have found this skill astonishingly scarce. Yurii asked me who else understands it. In China, nobody comes to mind. Even globally, perhaps the author of ZomboDB, who also created pgrx and was hired by ParadeDB, could do it well. Beyond that, I struggle to name anyone.

The PostgreSQL ecosystem has a huge number of extensions, but ParadeDB is the only extension vendor I know that ships mainstream Linux RPM and DEB packages at release time for `pg_search`. They do it because they release so frequently. I grew tired of packaging every release for them, so I taught them the process step by step. PGroonga, TimescaleDB, and Citus also produce their own packages, but those packages do not consistently follow PGDG conventions and their build matrices often have holes. Citus has long lacked ARM packages; TimescaleDB misses several specific distributions; and PGroonga packages against the PostgreSQL version bundled by Debian. The list goes on.

The same pattern appears among Chinese database vendors. Alibaba Cloud's PolarDB for PostgreSQL and IvorySQL once offered only a few EL RPMs. After I pushed them hard, they eventually produced packages for all 10 mainstream Linux distributions supported by Pigsty. I also helped them fix several elementary packaging mistakes. For the MySQL-compatible OpenHalo, I simply built the DEB and RPM packages myself. Supabase's OrioleDB appeared to lack this capability as well, so I packaged it too and made it work out of the box in Pigsty.

![Pigsty documentation for supported database kernels](/article/packaging-skill/03.webp)

## Conclusion

Value often comes from non-consensus skills. Build and packaging work is a perfect example. To a casual observer, it looks like little more than compiling some code and wrapping it in a package. In reality, it is an exceptionally scarce craft—one whose absence creates painful supply-chain chokepoints.

## References

![Extension Ecosystem Engineer RFC](/article/packaging-skill/04.webp)

![Extension Ecosystem Engineer role definition](/article/packaging-skill/05.webp)

---

> **Archive note (August 30, 2026):** This article first appeared as a [Chinese original on vonng.com](https://vonng.com/misc/packaging-skill/). Package counts, screenshots, and context reflect the original publication date; for current behavior, see the [PIG documentation](/docs/) and live [extension catalog](https://pigsty.io/ext/).
