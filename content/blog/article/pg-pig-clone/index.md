---
title: "Instantly Clone PostgreSQL Databases—No Black Magic Required"
linkTitle: "Instantly Clone PG Databases—No Black Magic Required"
date: 2026-07-06
lastmod: 2026-10-13
authors: [Vonng]
description: "pig v1.5 adds pig pg clone and pig pg fork, bringing PostgreSQL 18 database cloning and instance forks to the command line."
tags: [postgres, cli, sty]
---

Six months ago, on January 8, 2026, I wrote [**Git for Data: Instant PostgreSQL Database and Instance Cloning**](https://vonng.com/en/pg/pg-clone/), introducing a new feature in PostgreSQL 18 and Pigsty v4.0: instant database cloning. With filesystem copy-on-write (CoW) and PostgreSQL 18's new `file_copy_method = clone` setting, **you can clone a huge database in seconds while initially sharing its data blocks**.

This is a particularly good fit for AI agents. As I wrote in [What Kind of Database Do AI Agents Need?](https://vonng.com/en/db/agent-native-db/), ultra-low-cost database cloning is critical for counterfactual experiments. So when Pigsty 4.0 shipped, I added this capability to its PostgreSQL database provisioning workflow.

Today I saw [an article from Aliyun](https://mp.weixin.qq.com/s?__biz=Mzk2NDgzOTk3NA==&mid=2247523890&idx=1&sn=fdfe899fc6f7601f586b4ba32eaf147b&scene=21#wechat_redirect) announcing support for this feature in Alibaba Cloud RDS for PostgreSQL. I couldn't help laughing: that took them long enough. The feature itself is not complicated. It requires no kernel patch—just enable one setting in PostgreSQL 18 and add a `STRATEGY` option when creating the database. But simple as it sounds, a robust implementation still has a few edge cases to handle.

## A Few Improvements

Previously, cloning a database through Pigsty's IaC-style workflow was still somewhat cumbersome: first define the clone with another database as its template, then run the database creation workflow.

So for the Pig v1.5 release, I turned database cloning into one simple command: `pig pg clone`. If you have a database named `meta`, just run `pig pg clone meta`, and it automatically creates a clone.

![Running pig pg clone](/article/pg-pig-clone/clone-run.webp)

You can, of course, customize its behavior with options—for example, by specifying the branch name. If you do not provide one, Pig generates names sequentially by appending an underscore and a number.

![List of cloned databases](/article/pg-pig-clone/clone-list.webp)

The command automatically detects whether instant cloning is both enabled and supported. At the moment, Pigsty on XFS satisfies those prerequisites. If so, Pig performs an instant clone. If not, it warns you, waits for confirmation, and performs a conventional clone instead. Use `-y` to skip the confirmation.

As long as the underlying filesystem supports CoW, such as XFS, cloning a database takes essentially constant time—usually a few hundred milliseconds—and initially needs only metadata space. Subsequent writes allocate new space for the modified blocks.

## Agent-Native CLI

This command-line tool is built specifically for DBAs and DBA agents. You could already clone a database with an Ansible playbook or Pigsty's `/pg/bin/pg-clone` shell script, but neither is as convenient as using the `pig` CLI directly.

For example, before executing an operation, you can use `--plan` to print the plan. It tells you what Pig will do and what risks are involved. You can also use `-o json` or `-o yaml` to return results in JSON or YAML.

![Plan output from pig pg clone](/article/pg-pig-clone/clone-plan.webp)

Incidentally, both normal command output and help output are available as text, JSON, or YAML. That is especially useful to agents: they can explore the CLI and retrieve exactly the structured help they need. The `pg clone` and `pg fork` commands provide structured results.

![Structured help from pig pg clone](/article/pg-pig-clone/clone-help.webp)

I call this design an Agent-Native CLI, and I have written about it before.

## Instance-Level Forks

Database cloning is not the only related new feature worth mentioning. In [Git for Data: Instant PostgreSQL Database and Instance Cloning](https://vonng.com/en/pg/pg-clone/), I also covered instant instance-level cloning, which I call a “fork.”

![Running pig pg fork](/article/pg-pig-clone/fork-run.webp)

Run `pig pg fork dev`, and Pig creates an instance named `dev` from the current instance, assigning it a new random port. This is extremely useful when recovering from an accidental deletion: first create a temporary fork, then quickly run an incremental PITR on the fork to roll back and validate the result. Once you know the recovery is correct, perform it on the main instance.

PITR with `pig` is now very convenient as well. The example below performs an end-to-end point-in-time recovery to a specific timestamp, coordinating shutdown, restore, and the subsequent startup steps. You can still use `pig pgbackrest` when you want precise control over every operation.

![Running pig pitr](/article/pg-pig-clone/pitr-run.webp)

This release of the `pig` CLI adds many management features, including operations for PostgreSQL, Patroni, and pgBackRest. They are now all exposed as Agent-Native CLI commands like `pg clone` and `pg fork`, making them equally convenient for human DBAs and AI agents. I will write a dedicated article about them in a few days.

![PIG instant PostgreSQL cloning workflow](/article/pg-pig-clone/featured.webp)

## Further Reading

- [Git for Data: Instant PostgreSQL Database Cloning](https://vonng.com/en/pg/pg-clone/)
- [Put Your AI Agent's State in a Database](https://vonng.com/en/db/agent-state-db/)
- [What Kind of Database Do AI Agents Need?](https://vonng.com/en/db/agent-native-db/)

---

> Originally published on [vonng.com](https://vonng.com/en/pg/pg-pig-clone/).
