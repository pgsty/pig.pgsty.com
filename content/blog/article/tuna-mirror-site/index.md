---
title: On Trusting Open-Source Supply Chains
date: 2025-11-22
lastmod: 2026-10-13
authors: [Vonng]
description: >
  In serious production you can’t rely on an upstream that explicitly says “no guarantees.” When someone says “don’t count on me,” the right answer is “then I’ll run it myself.”
tags: [repo, build]
---

My earlier post “[PG ‘Export Controls’ and Supply-Chain Trust](/article/pg-mirror-pigsty/)” drew a comment from an administrator at Tsinghua University's TUNA mirror:

> “As a university mirror admin, calling us ‘lying flat’ or ‘irresponsible’ is unfair and demoralizing.”

![Comment from a university mirror administrator](/article/tuna-mirror-site/comment.webp)

I replied:

> Thanks for the feedback, and for the time and work that TUNA and other university mirrors have contributed over the years. I see that TUNA's PostgreSQL repository [has resumed synchronization](/article/tuna-mirror-site/tuna.webp), which is good news.
>
> When I first found the problem, I was using Alibaba Cloud's PostgreSQL mirror. I later noticed the same problem at TUNA and [reported it on the mailing list](https://groups.google.com/g/tuna-general/c/BU8P7X3y4sI). The reply said that the list belonged to TUNA, not Alibaba Cloud. After I clarified the report, I heard nothing further. That experience affected the tone of my article.
>
> Looking back, “lying flat” and “irresponsible” were too emotional, especially when applied to **your team**. They could read as moral judgments on volunteers, which was not my intention. I apologize for that wording. I have [replaced it](https://github.com/Vonng/blog/commit/916697a88f143679d658dc52338827ce603444fd) with descriptions such as “not updated for a long time” and “no longer maintained.”
>
> I agree that university mirrors are volunteer projects without contractual service commitments. But downstream users still face a real problem: after PGDG cut off rsync, major mirrors in China remained months out of date. Users following instructions to use a recommended mirror experienced a supply-chain interruption. That damages trust.
>
> My conclusion is that treating a volunteer mirror as critical production infrastructure, without a service commitment, is a mistake. I now host my own PGDG mirror and control that part of my supply chain. Thank you for explaining the maintainer's perspective. Helping users understand what they can expect from mirrors is valuable in itself.

## My reflections

After receiving the comment, I checked TUNA again. PostgreSQL 18 packages were available, although “Last Update” still showed May 16, 2025. That suggested a manual sync. Besides the [Pigsty repository](https://pgext.cloud), China had another node providing reasonably current PGDG packages. Credit to TUNA for restoring it.

![TUNA PostgreSQL 18 package directory at the time of the discussion](/article/tuna-mirror-site/tuna.webp)

When this outage began, Pigsty used Alibaba Cloud's PostgreSQL mirror. My criticism was aimed mainly at a large company with substantial resources — familiar territory for my [Cloud Mudslide](https://vonng.com/cloud) articles. Alibaba Cloud benefits heavily from open source, yet left its PostgreSQL mirror stale. It was the TUNA volunteers who responded, and I understand why they objected.

![Stale Alibaba Cloud PostgreSQL mirror directory](/article/tuna-mirror-site/aliyun.webp)

I do not think that providing a free mirror obliges either group to maintain it forever. But users will still judge the result. My frustration was real; applying it to university volunteers in those terms was unfair. I changed the wording to describe the maintenance problem itself.

When I found the [global mirror synchronization problem](/article/pg-mirror-break/), I [emailed Alibaba Cloud](/article/pg-mirror-pigsty/). I also checked other mirrors and reported the same problem to TUNA. My message contained TUNA URLs whose labels still said “ALIYUN,” which prompted the reply about the wrong mailing list. I corrected that mistake and explained the shared upstream problem. There was no further reply until this November discussion.

![PostgreSQL mirror discussion on the TUNA mailing list](/article/tuna-mirror-site/maillist.webp)

After waiting about another month, I set up a PGDG mirror for China on Tencent Cloud, alongside Pigsty's own repository. I removed Alibaba Cloud's PostgreSQL mirror from Pigsty's dependencies and took control of PostgreSQL package distribution. Without this interruption, I probably would not have done it so soon.

I am often blunt with cloud vendors. That does not mean I dismiss the difficulties volunteers face. University maintainers deserve more support and fewer moral accusations. That is why I changed my wording.

## Open source and trust

I recently experienced the same problem from the maintainer's side. I maintain several open-source projects, including [pg_exporter](https://github.com/pgsty/pg_exporter), a Prometheus exporter used by some PostgreSQL vendors.

On November 20, I noticed a [comment on an issue opened in September](https://github.com/pgsty/pg_exporter/issues/79#issuecomment-3403244826). In October, the user had explained that two issues had gone unanswered for a month. They had been excited about version 1.0 and considered contributing, but the lack of response had changed their mind:

> “I am not willing to bet on a project with a maintainer who is absent.”

They hoped my absence was temporary and wished both me and the project well.

![Discussion of maintainer responsiveness in a pg_exporter issue](/article/tuna-mirror-site/pg_exporter.webp)

I had spent September driving around Xinjiang and barely used a computer. I had opened the issues, then forgotten about them. My lack of attention cost the project a user's trust, and perhaps a future contributor. I regretted letting them down. I put other work aside, addressed the reported problems, and released [version 1.0.3](https://github.com/pgsty/pg_exporter/releases/tag/v1.0.3).

When an upstream mirror stops working and a report receives neither a response nor a fix, I feel the same way that user did. I do not want to depend on a project whose maintainer appears absent.

## The software supply chain

In “[PG ‘Export Controls’ and Supply-Chain Trust](/article/pg-mirror-pigsty/),” I argued that publishing source code is only one way to build trust. Continued effort, dependable delivery, and a willingness to address problems matter too.

I understand the mirror administrator's frustration. They receive no pay, spend their own time maintaining the service, and take on security and compliance responsibilities. Being called irresponsible is a poor reward for that work.

There is an uncomfortable gap between the two perspectives. A maintainer can reasonably say, “I am not paid, and I have made no commitment.” A user sees a public service and starts to treat it as dependable infrastructure. That expectation may be unreasonable, but it exists.

A mirror also occupies a specific place in the supply chain. It carries software from upstream to downstream, so stale packages can directly affect production systems. Providers differ in reliability, in whether they offer an SLA, and in whether they accept responsibility when something fails.

Consistent maintenance and clear expectations build trust. Stale or unreliable results erode it. The TUNA administrator's statement that university mirrors make no service guarantees is honest. It also tells a production operator where that service's limits are.

My point is that **a production supply chain should not depend on an upstream service that explicitly makes no commitment to its availability.**

## Quality and commitments

TUNA provides useful services. I use its PyPI and Homebrew mirrors on my own computer to speed up downloads. Early versions of Pigsty also used some of TUNA's PostgreSQL mirrors. After several unexpected HTTP 403 failures disrupted automated deployments, I switched to Alibaba Cloud.

Alibaba Cloud's mirror was generally reliable until PGDG stopped rsync access. Its PostgreSQL packages then remained months out of date. That reduced my trust, so I took over the PGDG mirror myself. At the time of writing, I still use Alibaba Cloud for operating-system packages. If those mirrors repeatedly fail, I may also host Rocky Linux, Ubuntu, and Debian mirrors.

The choices follow from the commitments each party makes:

- TUNA says university mirrors offer no service commitment. Downstream users can choose their use cases accordingly.
- Alibaba Cloud has not made that point explicit. I judge its service by its record. If it keeps failing, I will report the problems, criticize the service, or replace it.
- For my Pigsty and PGDG APT/DNF repositories, I make a commitment: if they break, I will fix them. Failure damages my reputation; for paying customers, it also means failing an SLA.

Mirrors, repositories, and distributions support the rest of our infrastructure. Accepting responsibility for their operation is part of becoming a supplier that others can rely on.

When an upstream says, “Don't count on me,” my response is, “Then I'll take responsibility for it myself.”

## A word from our sponsor

I rarely pass up a chance to mention my own work. These three public repositories may be useful to you. They have global endpoints behind Cloudflare and separate endpoints in China, and can be configured through PIG, APT, or DNF. See the [repository documentation](https://pigsty.io/docs/repo/) for current addresses and setup instructions.

![Pigsty architecture and repository overview](/article/tuna-mirror-site/pigsty.webp)

### PGDG mirror

The mirror copies the PostgreSQL Global Development Group's packages for EL 7–10, Debian 11–13, and Ubuntu 20.04–24.04. On November 22, 2025, it had just completed a sync and was being updated weekly.

### PIGSTY PGSQL

This repository supplements PGDG with [PostgreSQL variants](https://pigsty.io/docs/pgsql/kernel/), including PolarDB, IvorySQL, Babelfish, OrioleDB, OpenHaloDB, Percona TDE, and Supabase. At the time of writing, it provided [437 PostgreSQL extensions](https://pgext.cloud/list) and ecosystem tools across [14 Linux distribution major versions](https://pgext.cloud/os).

![PGEXT.CLOUD extension catalog and availability counts](/article/tuna-mirror-site/extensions.webp)

### PIGSTY INFRA

This repository provides database tools, Grafana, Prometheus, and exporters. The following package versions describe the November 22, 2025 snapshot.

#### Databases and ecosystem tools

| Package | Version |
|---|---|
| [IvorySQL](https://github.com/IvorySQL/IvorySQL) | 4.6 |
| [etcd](https://github.com/etcd-io/etcd) | 3.6.6 |
| [minio](https://github.com/minio/minio) | 20250907161309 |
| [mcli](https://github.com/minio/mc) | 20250813083541 |
| [kafka](https://kafka.apache.org/downloads) | 4.0.0 |
| [duckdb](https://github.com/duckdb/duckdb) | 1.4.2 |
| [ferretdb](https://github.com/FerretDB/FerretDB) | 2.7.0 |
| [tigerbeetle](https://github.com/tigerbeetle/tigerbeetle) | 0.16.60 |
| [juicefs](https://github.com/juicedata/juicefs) | 1.3.0 |
| [dblab](https://github.com/danvergara/dblab) | 0.34.2 |
| [v2ray](https://github.com/v2fly/v2ray-core) | 5.28.0 |
| [pig](https://github.com/pgsty/pig) | 0.7.2 |
| [vip-manager](https://github.com/cybertec-postgresql/vip-manager) | 4.0.0 |
| [pev2](https://github.com/dalibo/pev2) | 1.17.0 |
| [promscale](https://github.com/timescale/promscale) | 0.17.0 |
| [pgschema](https://github.com/pgschema/pgschema) | 1.4.2 |

#### Prometheus and exporters

| Package | Version |
|---|---|
| [prometheus](https://github.com/prometheus/prometheus) | 3.7.3 |
| [pushgateway](https://github.com/prometheus/pushgateway) | 1.11.2 |
| [alertmanager](https://github.com/prometheus/alertmanager) | 0.29.0 |
| [blackbox_exporter](https://github.com/prometheus/blackbox_exporter) | 0.27.0 |
| [VictoriaMetrics](https://github.com/VictoriaMetrics/VictoriaMetrics) | 1.129.1 |
| [VictoriaLogs](https://github.com/VictoriaMetrics/VictoriaMetrics/releases) | 1.37.2 |
| [pg_exporter](https://github.com/pgsty/pg_exporter) | 1.0.3 |
| [pgbackrest_exporter](https://github.com/woblerr/pgbackrest_exporter) | 0.21.0 |
| [node_exporter](https://github.com/prometheus/node_exporter) | 1.10.2 |
| [keepalived_exporter](https://github.com/mehdy/keepalived-exporter) | 1.7.0 |
| [nginx_exporter](https://github.com/nginxinc/nginx-prometheus-exporter) | 1.5.1 |
| [zfs_exporter](https://github.com/waitingsong/zfs_exporter/releases/) | 3.8.1 |
| [mysqld_exporter](https://github.com/prometheus/mysqld_exporter) | 0.18.0 |
| [redis_exporter](https://github.com/oliver006/redis_exporter) | 1.80.0 |
| [kafka_exporter](https://github.com/danielqsj/kafka_exporter) | 1.9.0 |
| [mongodb_exporter](https://github.com/percona/mongodb_exporter) | 0.47.1 |

#### Grafana and log tools

| Package | Version |
|---|---|
| [grafana](https://github.com/grafana/grafana/) | 12.3.0 |
| [loki](https://github.com/grafana/loki) | 3.1.1 |
| [promtail](https://github.com/grafana/loki/releases/tag/v3.0.0) | 3.0.0 |
| [vector](https://github.com/vectordotdev/vector/releases) | 0.51.1 |
| [grafana-infinity-ds](https://github.com/grafana/grafana-infinity-datasource/) | 3.6.0 |
| [grafana-vmlogs-ds](https://github.com/VictoriaMetrics/victorialogs-datasource/releases/) | 0.21.4 |
| [grafana-vmetrics-ds](https://github.com/VictoriaMetrics/victoriametrics-datasource/releases/) | 0.19.6 |
| [grafana-plugins](https://github.com/pgsty/infra-pkg/tree/main/grafana-plugins) | 12.0.0 |

#### Utilities

| Package | Version |
|---|---|
| [sealos](https://github.com/labring/sealos) | 5.1.1 |
| [rclone](https://github.com/rclone/rclone/releases/) | 1.71.2 |
| [restic](https://github.com/restic/restic) | 0.18.1 |
| [mtail](https://github.com/google/mtail) | 3.0.8 |
| [genai-toolbox](https://github.com/googleapis/genai-toolbox) | 0.18.0 |
| [sqlcmd](https://github.com/microsoft/go-sqlcmd) | 1.8.0 |

---

> Originally published on [vonng.com](https://vonng.com/en/db/tuna-mirror-site/).
