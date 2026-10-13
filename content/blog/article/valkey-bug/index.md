---
title: "How a Packaging Patch Broke Valkey’s Memory Accounting"
date: 2026-08-09
lastmod: 2026-10-13
authors: [Vonng]
description: "A packaging patch uses the wrong deallocator in Valkey. It can crash the server or trigger persistent out-of-memory errors."
tags: [build, repo]
---

I was updating the Redis module in Pigsty recently, adding Valkey as an alternative engine, and found a bug in an inherited packaging patch.

In affected Valkey DEB packages, failed synchronous saves can corrupt `used_memory` until it reports a value near 2^64.
With `maxmemory` set, commands subject to its limit then return OOM errors. Restarting the server resets the counter.

```console
> SET foo bar
(error) OOM command not allowed when used memory > 'maxmemory'.
> GET foo
"bar"                          # a value stored before the failure
```

There can be plenty of free memory. The log records the save failure, but not a separate memory-accounting error. `used_memory_rss` stays normal and RSS graphs are flat. The only number moving is `used_memory`, and nobody alerts on memory usage slowly going *down*.

**A build that applies the same patch and links the bundled private jemalloc can crash on the first failed `SAVE`. Pristine upstream source does not contain the patch and is unaffected.**

The cause is a single line in a packaging patch. Its lineage goes back to 2017, it was fixed once in Redis, came back in Valkey, and eventually got copied into Valkey's own release pipeline — so **all five official DEB packaging lines examined in this investigation**—7.2, 8.0, 8.1, 9.0, and 9.1—carried it. The official RPM packaging did not.

The [packaging fix](https://github.com/valkey-io/valkey-release-automation/pull/63) merged on August 7, 2026. Here is how it surfaced.

---

## What's wrong

Valkey logs the working directory on two RDB error paths: failure to open the temporary file and failure to rename it to the final snapshot name. Upstream uses a stack buffer, so there's nothing to release.

Debian's packaging patch moves it to the heap:

```c
char *cwdp = get_current_dir_name();        /* glibc malloc() */
serverLog(LL_WARNING, "... in server root dir %s ...", cwdp, ...);
zfree(cwdp);                                /* <- here */
```

The motivation is fine: keep a 4 KB array off the stack.

The problem is the last line. `get_current_dir_name()` allocates through **glibc's `malloc()`**. `zfree()` is **Valkey's own deallocator**. They are not interchangeable.

The usual reaction is "it's a free, what could go wrong". But `zfree()` isn't a wrapper around `free()`. It does three things: ask the allocator how big the block is, **subtract that from `used_memory`**, and then release it.

Step two is wrong unconditionally. This allocation never went through Valkey's allocator, so it was never added to `used_memory` — and `used_memory` is unsigned, so subtracting past zero wraps it.

Whether steps one and three break depends on which jemalloc the binary was linked against. With system `libjemalloc.so`, as used by the affected DEB packages, global `malloc()` and Valkey use the same allocator. The pointer belongs to the right heap, so nothing crashes and you only get the corrupted counter. With the bundled private jemalloc — upstream's default — it can't find the pointer in its own bookkeeping and dereferences null:

```text
valkey-server(je_malloc_usable_size+0x68)
valkey-server(valkey_free+0x28)
valkey-server(rdbSave+0x18c)
valkey-server(saveCommand+0x4c)
```

Look familiar? Same top-of-stack as [redis/redis#7927](https://github.com/redis/redis/issues/7927) from 2020 — the same bug, in Redis.

The saving grace is that only synchronous saves in the main process accumulate. `BGSAVE` and scheduled saves fork, so the damage dies with the child. The real-world trigger is a full disk, wrong permissions, or a read-only filesystem, combined with something calling synchronous `SAVE` in a loop: a monitoring script, a backup cron, a client that retries.

It waits until you already have a problem, then quietly adds a second one.

## How I found it

Not through any clever analysis. Upstream's own test suite caught it.

While reworking the Valkey DEB packaging for [Pigsty](https://pigsty.io), I ran `runtest` as usual. Three cases in `unit/shutdown` failed and the server left a crash report.

Our packages use the bundled jemalloc, so we were on the crashing side — louder symptoms than the official packages, and much easier to catch. Following the crash trace up, then opening `debian/patches/0003-*.patch`, and there it was.

The relevant test, by the way, deliberately creates a **directory** named `dump.rdb` to force `rename(2)` to fail — which is exactly one of the two patched paths.

Once I understood the mechanism, the first thing I did was disbelieve myself: two Valkey versions, three builds each (pristine, patched, patched-and-fixed), against three allocators, on two architectures. The result held.

Then I spent longer than the technical work checking whether someone had already reported it. Worth noting one trap: two of Debian's search endpoints were broken at the time and **returned zero rows for bugs I knew existed**. Without a "this query should definitely return something" control, I'd have walked away with a confident false negative.

I found no dedicated Debian bug report for this Valkey defect.

## Where the line came from

The patch header goes back further than I expected:

```text
From: Chris Lamb <lamby@debian.org>
Date: Thu, 16 Nov 2017 03:40:26 +0900
Subject: Use get_current_dir_name over PATHMAX, etc.
```

- **2017** — Chris Lamb writes the patch for Debian's **Redis** packaging.
- **2020** — a `zfree(cwdp)` shows up in Redis's copy and blows up: [redis/redis#7927](https://github.com/redis/redis/issues/7927) and [Debian #972683](https://bugs.debian.org/972683), fixed by switching to libc `free()`.
- Debian's Valkey packaging is **derived** from the Redis packaging, patch included.
- In October 2024, a change to fix the leak adds `zfree(cwdp)` again. It first ships in Debian Valkey `8.0.2+dfsg1-1`; `8.0.1+dfsg1-1` is unaffected. **The same mistake, in the same patch lineage, four years apart.**
- **March 2025** — Valkey maintainer zuiderkwast, reviewing these Debian patches, [spots the mismatch immediately](https://github.com/valkey-io/valkey/issues/1882):

  > ...the latter uses `malloc()` (rather than `zmalloc()`) and we later free it using `zfree()`. This means it will mess up the memory usage tracking done in zmalloc and zfree. Therefore, we may not want to take this patch, at least not unmodified.

  Correct diagnosis. He assumed the damage stopped at broken accounting, and the issue lost priority when jemalloc upstream was archived.
- **April 2026** — Valkey builds an automated pipeline covering five version lines, four distributions, and two CPU architectures, and **copies Debian's patch set wholesale**. The official `.deb`s inherit the bug.

The Debian packaging rules leave `override_dh_auto_test` empty, with the upstream regression-test commands commented out. The pipeline checks installation and service behavior, but those checks do not exercise the failing RDB paths.

## Reporting it

Two channels, handled separately.

**Debian takes email.** No account needed — send a **plain text** message to `submit@bugs.debian.org` with pseudo-headers as the first lines of the body:

```text
Package: src:valkey
Version: 8.1.4+dfsg1-2
Severity: normal
Tags: patch
```

My first attempt bounced, saying the body didn't start with `Package:`, so "**your message has been ignored completely**". Which was baffling, because it did:

```text
00000000: 5061 636b 6167 653a      Package:
```

The answer was in the message-id: it was **Apple Mail**, which sends rich text by default. BTS only parses plain text, so it never saw the line.

So if you're filing a Debian bug from a Mac: switch to plain text first (`Format` → `Make Plain Text`), and turn off smart quotes, or the quote characters in your patch get mangled and the patch is worthless. Resent, it went through as [#1143239](https://bugs.debian.org/1143239).

**Upstream took a comment, then a PR.** zuiderkwast's year-old comment was the natural hook, so I picked up from there with what he didn't have: under the bundled allocator this is a segfault, not drift; the upstream test suite already catches it; and the official `.deb`s have it today.

He asked for a PR on August 3. The change is one line:

```diff
-        zfree(cwdp);
+        zlibc_free(cwdp);
```

`zlibc_free()` exists in Valkey **for exactly this case** — it's defined specifically so callers can reach the real libc `free()`.

Which also explains how `zfree` got picked in the first place. A plain `free(cwdp)` **does not compile**: Valkey deliberately marks `free()` deprecated and builds with `-Werror`. One possible explanation is that the compiler rejected `free()` and the author chose the closest-looking name.

A defensive measure that pushed someone into the hole it was guarding.

## Outcome

zuiderkwast approved the same day, with a question: **why keep this patch at all?** The path is only used in one error message; just go back to the stack buffer.

Fair, and I'd listed dropping it as the alternative in the PR description. Since he was leaning that way, I did it downstream first — removed the patch entirely from Pigsty's Valkey and Redis packaging, rebuilt, and reported back: the shutdown tests pass, and ordinary paths still appear in the error message. If a path exceeds the stack buffer, upstream reports `unknown`. **The problem goes away along with the patch.**

Then it went somewhere I didn't expect. zuiderkwast turned to the maintainers who built the pipeline:

> Why did we copy Debian's patches?
>
> If some things need to be patched, that's better fixed upstream in Valkey itself. **Bugs in this repo's patches are harder to spot than bugs in Valkey main repo IMHO.**

That last sentence is the best summary of the whole episode.

**The PR merged on 2026-08-07.** It corrects both deallocation sites in all five packaging lines. The maintainer who built the pipeline replied "Thanks for the notification. Will investigate this!" — a review of the whole patch stack is underway.

As of this article’s publication on August 9, the Debian report had received no maintainer reply. The investigation also found the same defect in **bookworm’s Redis `5:7.0.15-1~deb12u7` package**. I included that finding in the Valkey report but had not filed it separately.

## Takeaway

Nobody involved did anything stupid.

Lamb's 2017 patch was legitimate packaging hygiene. Whoever added `zfree(cwdp)` was fixing a real leak and picked the wrong deallocator — pushed there by `free()` being deliberately deprecated. zuiderkwast spotted the mismatch a year ago and diagnosed it correctly; he just underestimated the consequence. Copying Debian's patches into the release pipeline was the pragmatic move, and Debian's packaging quality is famously good.

Every step was reasonable. The result sat quietly across five product lines and four distributions.

**Packaging patches are where bugs hide.** They can be absent from upstream CI, upstream code review, and the source history users normally inspect. They get copy-pasted across projects (Redis → Valkey) and across organizations (Debian → Valkey's own pipeline), losing a little context each time.

And the reason this surfaced at all: that test case was sitting there the whole time, creating a directory named `dump.rdb` to force exactly this failure. The official DEB build had the regression-test commands commented out, so this test did not run there.

Packaging is dull work. Run the tests anyway.

## Postscript: a question at PGConf

At PGConf this year I gave a talk called *Extension for Everyone*. Afterwards Christoph Berg, who maintains the PGDG APT repository, asked me a good question:

**How do you actually test all these packages?**

Pigsty maintains packaging for a few hundred extensions and components. The packaging repos alone carry over a hundred patches, a good share of them fixing small, fiddly details. One person cannot hand-verify every path in every package. There isn't enough time.

My answer: beyond whatever tests the package ships with, I have Codex run a smoke pass — model how the software actually gets used in production and try to hit the things that break.

It turns up a lot. This bug is the biggest thing it has found so far.

Which is worth sitting with for a moment: **why did this survive so long?**

Valkey is not an obscure project anymore; it's the default Redis replacement in several distributions. Debian is about as mainstream as it gets, with famously good packaging. Valkey's maintainers are excellent engineers — zuiderkwast diagnosed the mechanism correctly a year ago just by *reading* the patch. And Redis's own packaging copies Debian's patch the same way.

So the missing ingredient was never capability. It was **patience**.

Spending a full day on a footnote-grade bug in a cold error path — comparing patch states, allocators, versions, and architectures, reproducing the crash thirty times, tracing a patch lineage back a decade, checking five different search endpoints to confirm nobody had reported it — does not pay off on a human time budget. It is too boring.

Which happens to be exactly the kind of work an agent is good at.

End to end on this one: it ran the tests, built the reproduction matrix, wrote the patch, drafted the Debian report, and worded the exchanges with the maintainers on GitHub. My job was assigning the work, pushing back, and making the final calls.

I should be clear that this is not "the AI does everything and I put my feet up". During this investigation I had a second agent do an adversarial review of my draft at maximum effort, and it pulled out four factual errors in one pass: I had misremembered how the old Debian bug was actually fixed, `FLUSHDB` doesn't reach this code path at all, "refuses every write" overstated the impact, and I had missed entirely that bookworm's Redis is still affected today. Sending any of that to maintainers as-is would have been my embarrassment, not the model's.

So the value isn't that the agent gets it right the first time. It's that **the cost of making it disprove itself over and over is low enough to be worth doing** — where a human would decide that six builds to chase a statistics counter isn't worth the afternoon.

The change in pace is startling. Two years ago every step in that loop was mine to do by hand. Now I sit here handing out tasks, asking follow-up questions, and signing off — and the rest of it just runs.

---

> Originally published on [vonng.com](https://vonng.com/en/db/valkey-bug/).
