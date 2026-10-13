---
title: "PostgreSQL神功大成！最全扩展仓库来了！"
linkTitle: "PostgreSQL神功大成！"
date: 2024-11-02
lastmod: 2026-10-13
authors: [Vonng]
description: "PostgreSQL 扩展为什么难装？一个原生 RPM/DEB 软件仓库如何交付 340 个扩展。"
tags: [ext, repo, catalog, build]
---

最近没怎么更新，因为在憋大招。最近功成出关，遂发此文为贺 —— 我做了一个收录 PG 生态中 340 个扩展的[仓库](https://pgext.cloud/zh)，让 PostgreSQL 在成为数据库全能王的道路上又往前迈出了坚实的一步！

自从我在 《[**PostgreSQL正在吞噬数据库世界**](https://vonng.com/pg/pg-eat-db-world)》 一文中指出 **可扩展性** 对于 PostgreSQL 的重要性以来，PG 社区对此进行了[**热烈的讨论**](https://vonng.com/pg/pgcondev-2024)，并且达成了共识。
最终体现在《[**PostgreSQL 17 发布注记！**](https://vonng.com/pg/pg-17)》中。

但真正重要的事情不是认识世界，而是改变世界。既然大家都已经认清了扩展很重要，**那么我们应该做什么，怎么做**，就成了真正关键的问题。

那么什么是 PostgreSQL 扩展最关键的问题？在我看来，扩展用得上用不上，是 PG 扩展生态的首要问题。

--------

## PG 扩展分发现状

大家知道 PG 生态有很多扩展插件，但这些扩展插件如何安装使用？这第一道门槛就成了许多用户的拦路虎。怎么解决这个问题？
PGXN 说，用我的办法，我可以现场下载编译扩展；
Tembo 说，我提前帮你打好 docker 镜像；
StackGres 和 Omnigres 说，我们可以在线下载编译好的 So 文件；
八仙过海，各显神通。

大家都有很多好想法，唯独没仔细考虑绝大多数用户到底是如何安装扩展的。
作为前 DBA，我只能说什么现场编译，OCI镜像，下载so文件，在实战中都有些离谱了 —— **使用最广泛且最可靠的扩展安装方式，依然是用操作系统的包管理器安装签名二进制包**。
而 yum / dnf / apt 在解决这个问题上已经做的足够好了！所以真的问题其实是，谁来把这几百个扩展插件打成开箱即用的软件包？

PostgreSQL 的 PGDG 官方仓库中，提供了大约 **100** 个左右的扩展，但存在各种问题：有的扩展在 Debian/Ubuntu 的 APT 仓库里有，在 EL 系统的 YUM 仓库里没有；
有的扩展在 EL8 上有，EL9 没有；有的扩展在 Ubuntu 22 上有，在 24 上没有；有的扩展针对 PostgreSQL 12 - 15 提供，PG 16，17 不提供；有的扩展只有 x86_64 架构，没有 arm 架构；有时候碰上这种问题确实蛮让人头疼。

--------

## 怎么办？我行我上！

作为一个 PostgreSQL 发行版维护者，我曾经寄希望于 PG 生态的其他人来解决这个问题。
每当我看见 PGDG 仓库有出现错漏缺失，我都会第一时间反馈给仓库维护者 Devrim 和 Cris 。

有的时候这种模式挺管用，比如去年当我发现 pgvector 这个强力向量数据库扩展还没有二进制软件包制成品时，我第一时间[提给 Devrim](https://github.com/pgvector/pgvector/issues/76) ，
[将其放入 PGDG 仓库](https://vonng.com/pg/vector-json-pg/#译者评论)，然后 pgvector 遂成为 PG 生态中的向量数据库事实标准，进入到各家云厂商 RDS 中。

但有的时候，事情并不总能如意。例如，**Devrim** 表示，他绝对不会接受任何 Rust 扩展插件进入 PGDG YUM 仓库。
但我确实有二十多个用 Rust 编写的 PostgreSQL 扩展需要分发（例如自建 Supabase 就需要 pg_graphql, pg_jsonschema, wrappers 三个 Rust 扩展），怎么办呢？

再比如说，最近 PG 生态非常火热的 [DuckDB 缝合大赛](https://vonng.com/pg/pg-duckdb)，大家都在密集地更新跟进 DuckDB 系扩展 ，这些扩展插件我第一时间 [打好了 RPM/DEB 包](https://pgext.cloud/e/olap)，但是如何分发呢？

思来想去，我决定还是我行我上，自己维护一个 PostgreSQL 扩展插件的 APT / YUM 仓库，分发 PG 扩展。

[![PGEXT.CLOUD 扩展目录首页](/article/pg-ext-repo/ext-website.webp)](https://pgext.cloud)

--------

## PG 扩展大全

在过去的半年中，我的工作重心放在 PG 扩展生态的整合上。而最近，这项工作终于达到了一个让我自己感到满意的里程碑。我建设了一个 PG Yum/APT 仓库，收录了 340 个可用 PG 扩展的元数据，以及二进制制成品。

| Entry / Filter | All | PGDG | PIGSTY | CONTRIB | MISC | MISS | PG17 | PG16 | PG15 | PG14 | PG13 | PG12 |
|:--------------:|:---:|:----:|:------:|:-------:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| RPM Extension  | 334 | 119  |  139   |   70    |  4   |  6   | 301  | 330  | 333  | 319  | 307  | 294  |
| DEB Extension  | 326 | 104  |  143   |   70    |  5   |  14  | 302  | 322  | 325  | 316  | 303  | 293  |
|  RPM Package   | 251 | 107  |  138   |    1    |  4   |  1   | 220  | 247  | 250  | 239  | 229  | 216  |
|  DEB Package   | 241 |  90  |  142   |    1    |  5   |  1   | 218  | 237  | 240  | 234  | 223  | 213  |

以上是这个仓库的一些统计数字：总共有 340 个可用 Extension，去除 PG 自带的 70 个，总共 270 个第三方扩展插件。其中一部分由 PGDG 官方仓库提供，其余扩展由我维护、修复、编译、打包、测试与分发。上表列出了各仓库和平台的覆盖情况。

每一个扩展，我都针对最新的 PostgreSQL 12 - 17 这六个生命周期大版本分别打包构建，针对 EL8，EL9，Ubuntu 22.04，Ubuntu 24.04，以及 Debian 12 这五个绝对主流 Linux 发行版构建。此外也对 EL7，Debian 11， Ubuntu 20.04 这些过保系统提供部分有限支持。

[![PGEXT.CLOUD 扩展仓库使用说明](/article/pg-ext-repo/usage.webp)](https://pgext.cloud)

这个仓库还解决了扩展对齐的问题，例如，原本在 APT 和 YUM 仓库中的扩展，APT 有一小半几十个扩展 YUM 仓库没有，YUM 仓库有一小半 APT 仓库没有。我把两者独有的扩展都尽可能移植到另一个操作系统生态中，现在只有 7 个 APT 扩展在 YUM 仓库中缺失，16 个扩展在 APT 仓库缺失，只占总数的 6%。很多 PGDG 扩展版本缺失的问题，也在这里得到了一并修复。

我提供了一个完整的目录，列出了支持的扩展，并且对每一个扩展，都给出了详情，依赖安装说明与注意事项。

[![PostGIS 扩展详情页面](/article/pg-ext-repo/postgis.webp)](https://pgext.cloud/e/postgis)

我想，用户吭哧吭哧抱怨扩展编译失败的问题，应该能在这里得到最终的解决。

当然题外话是广告时间，安装这些扩展，使用这个仓库的最简单的方式是什么？当然是开箱即用的 PostgreSQL 数据库发行版 —— **Pigsty** —— **但这并非必选项**。
你也可以在支持的 EL、Debian 或 Ubuntu 系统上直接配置此仓库。具体步骤见[仓库参考](/zh/repo/)。

<details><summary>使用Pigsty一次性配置好并拉起用于自建Supabase的PostgreSQL集群，只要简单地声明要安装哪些扩展插件即可！</summary><br>

一键自建 Supabase 所需的 PostgreSQL 集群，请参考样例配置文件：[`conf/supabase.yml`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml)。

```yaml
# pg-meta, the underlying postgres database for supabase
pg-meta:
  hosts: { 10.10.10.10: { pg_seq: 1, pg_role: primary } }
  vars:
    pg_cluster: pg-meta
    pg_users:
      # supabase roles: anon, authenticated, dashboard_user
      - { name: anon           ,login: false }
      - { name: authenticated  ,login: false }
      - { name: dashboard_user ,login: false ,replication: true ,createdb: true ,createrole: true }
      - { name: service_role   ,login: false ,bypassrls: true }
      # supabase users: please use the same password
      - { name: supabase_admin             ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: true   ,roles: [ dbrole_admin ] ,superuser: true ,replication: true ,createdb: true ,createrole: true ,bypassrls: true }
      - { name: authenticator              ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] }
      - { name: supabase_auth_admin        ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
      - { name: supabase_storage_admin     ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] ,createrole: true }
      - { name: supabase_functions_admin   ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
      - { name: supabase_replication_admin ,password: 'DBUser.Supa' ,replication: true ,roles: [ dbrole_admin ]}
      - { name: supabase_read_only_user    ,password: 'DBUser.Supa' ,bypassrls: true ,roles: [ dbrole_readonly, pg_read_all_data ] }
    pg_databases:
      - name: postgres
        baseline: supabase.sql
        owner: supabase_admin
        comment: supabase postgres database
        schemas: [ extensions ,auth ,realtime ,storage ,graphql_public ,supabase_functions ,_analytics ,_realtime ]
        extensions:
          - { name: pgcrypto  ,schema: extensions  } # 1.3   : cryptographic functions
          - { name: pg_net    ,schema: extensions  } # 0.9.2 : async HTTP
          - { name: pgjwt     ,schema: extensions  } # 0.2.0 : json web token API for postgres
          - { name: uuid-ossp ,schema: extensions  } # 1.1   : generate universally unique identifiers (UUIDs)
          - { name: pgsodium        }                # 3.1.9 : pgsodium is a modern cryptography library for Postgres.
          - { name: supabase_vault  }                # 0.2.8 : Supabase Vault Extension
          - { name: pg_graphql      }                # 1.5.9 : pg_graphql: GraphQL support
          - { name: pg_jsonschema   }                # 0.3.3 : pg_jsonschema: Validate json schema
          - { name: wrappers        }                # 0.4.3 : wrappers: FDW collections
          - { name: http            }                # 1.6   : http: allows web page retrieval inside the database.
          - { name: pg_cron         }                # 1.6   : pg_cron: Job scheduler for PostgreSQL
          - { name: timescaledb     }                # 2.17  : timescaledb: Enables scalable inserts and complex queries for time-series data
          - { name: pg_tle          }                # 1.2   : pg_tle: Trusted Language Extensions for PostgreSQL
    # supabase required extensions
    pg_libs: 'pg_stat_statements, pgaudit, plpgsql, plpgsql_check, pg_cron, pg_net, timescaledb, auto_explain, pg_tle, plan_filter'
    pg_extensions: # extensions to be installed on this cluster
      - supa-stack
      - timescaledb pg_cron pg_timetable
      - postgis pg_geohash
      - pgvector pgvectorscale pg_similarity smlar pg_summarize pg_tiktoken
      - pg_search pg_bigm zhparser hunspell
      - pg_analytics pg_parquet pg_duckdb
      - pg_hint_plan hll rum pg_graphql pg_jsonschema index_advisor pg_plan_filter hypopg pg_ivm pgmq pg_cardano
      - pg_tle plv8 plpgsql_check #pljava
      - pgunit md5hash asn1oid roaringbitmap pgfaceting pgsphere pg_country pg_currency pgmp numeral pg_rational pguint pg_uint128 ip4r pg_uri pgemailaddr acl timestamp9
      - pg_gzip pg_zstd pg_http pg_net pg_html5_email_address pgsql_tweaks pg_extra_time pg_timeit count_distinct extra_window_functions first_last_agg tdigest aggs_for_arrays aggs_for_vecs pg_arraymath quantile lower_quantile
      - pg_idkit pg_uuidv7 permuteseq pg_hashids sequential_uuids pg_math pg_random pg_base36 pg_base62 pg_base58 floatvec pg_financial pgjwt pg_hashlib shacrypt cryptint pg_ecdsa pgpcre icu_ext pgqr envvar pg_protobuf url_encode
      - pg_repack pg_squeeze pg_dirtyread ddlx pg_readonly safeupdate pg_permissions pg_savior pg_fio
      - pg_profile pg_show_plans pg_stat_kcache pg_stat_monitor pg_qualstats pg_track_settings system_stats pg_meta pgnodemx pg_sqlog bgw_replstatus toastinfo pg_explain_ui pg_relusage
      - passwordcheck supautils pgsodium pg_vault anonymizer pgsmcrypto pgaudit pgauditlogtofile pg_auth_mon credcheck logerrors login_hook set_user pgextwlist pg_auditor sslutils noset
      - wrappers mysql_fdw redis_fdw pg_redis_pubsub aws_s3 log_fdw
      - pglogical wal2json decoder_raw pg_fact_loader
    pg_parameters:
      cron.database_name: postgres
      pgsodium.enable_event_trigger: off
    pg_hba_rules: # supabase hba rules, require access from docker network
      - { user: all ,db: postgres  ,addr: intra         ,auth: pwd ,title: 'allow supabase access from intranet'    }
      - { user: all ,db: postgres  ,addr: 172.17.0.0/16 ,auth: pwd ,title: 'allow access from local docker network' }
    pg_vip_enabled: true
    pg_vip_address: 10.10.10.2/24
    pg_vip_interface: eth1
```

</details>

--------------

## 这个仓库里有什么？

在 Pigsty 的扩展仓库中，所有的扩展都已经被预先分为了十五类之一：TIME，GIS，RAG，FTS，OLAP，FEAT，LANG，TYPE，FUNC，ADMIN，STAT，SEC，FDW，SIM，ETL，如下所示。

请移步 [pgext.cloud](https://pgext.cloud/zh) 查看完整详情。

--------

## 一些感想与体会

PG 每个大版本都会引入一些变动，因此维护一百多个扩展插件并不是一件轻松的事情。特别是一些扩展的作者都好几年没动静了，那还真就只能自己上。我自己修复了十几个扩展插件，提供了最新的 PG 大版本支持。能联系上作者的，我也提交了一堆 PR 或者 Issue，推动解决。

[![GitHub 贡献活动](/article/pg-ext-repo/github-contrib.webp)](https://github.com/Vonng)

在这个过程中，我和许多扩展作者都建立了联系。例如，我手把手帮助 ParadeDB 的老板与作者 [解决了](https://github.com/paradedb/paradedb/issues/1116) RPM / DEB 包打包与分发的问题。我说动了 duckdb_fdw 的作者使用一个单独的 libduckdb，并发布了 v1.0.0 ，我给一些PG扩展的作者发邮件/Issue，国产机器学习框架 PG4ML 的作者也找到了我希望能够通过这个渠道进行分发。

再比如说，最近 PG 生态 OLAP 缝合 DuckDB 的竞赛如火如荼，但不管是ParadeDB 的 pg_analytics，国内个人开发者李红艳编写的 duckdb_fdw，CrunchyData 的 pg_parquet，MooncakeLab 的 pg_mooncake， Hydra 和 DuckDB 原厂 MotherDuck 亲自下场搞的 pg_duckdb ，都被我在第一时间编译打包收录整合其中，做到了 —— 你卷你的，反正我全都要。

言归正传，**我希望这个仓库能设立起 PostgreSQL 扩展安装分发的标准，解决让人头大的分发难题**。目前最让我感到高兴的进展是，流行的开源 PostgreSQL高可用集群搭建项目 [`postgresql_cluster`](https://postgresql-cluster.org/) 的作者 Vitaliy Kukharik 已经将这个仓库作为默认启用的仓库来安装 PostgreSQL 扩展。

[![postgresql_cluster 采用 Pigsty 扩展仓库](/article/pg-ext-repo/pg-clusters.webp)](https://x.com/VKukharik/status/1853012121623155117)

目前这个仓库 (repo.pigsty.io) 托管在 Cloudflare 上，所以没有什么流量成本。国内有一个镜像站点 repo.pigsty.cc，方便墙内用户使用，每月有小几百块流量费，不是什么大问题。两个仓库加起来，过去一个月的下载流量大概 200GB ，考虑到扩展平均几十KB到几MB的大小，总下载量小几十万是有了。

因为[赛博菩萨 Cloudflare](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247487240&idx=1&sn=ba535fd0c1026bc2482ea6ad1e1fb8bf&chksm=fe4b3ad3c93cb3c50bfeaed64963cce25c49bee80364d3a8ca78b87d7c9f19fd4d79d3c62ddc&scene=21#wechat_redirect)不收流量费，所以总的来说，我觉得做一个永久免费的声明与承诺并不困难，所以 So be it。我承诺这个仓库将持续维护并永久免费。如果有国内开源软件站点的朋友愿意赞助或提供镜像服务，欢迎联系我。

我相信我的工作可以帮助到全球PG用户，并对 PostgreSQL 生态的繁荣贡献一份力量。我也希望我的工作可以帮到您，**Enjoy PostgreSQL**！

---

> 原文：[vonng.com](https://vonng.com/pg/pg-ext-repo/)。
