---
title: "pig pe"
description: "Use the legacy pig pe shortcuts for a default pg_exporter HTTP endpoint"
weight: 175
icon: fas fa-chart-line
categories: [Reference]
tags: [postgres, cli]
---

`pig pe` (aliases: `pgexp`, `pgexporter`) is a legacy convenience wrapper for a running
[pg_exporter](https://github.com/Vonng/pg_exporter). It reads the default metrics and statistics
endpoints and can request a configuration reload. It is not a general or versioned pg_exporter
client.

```bash
pig pe get                     # print pg_ metrics
pig pe list                    # list metric families from HELP lines
pig pe stat                    # print exporter statistics
pig pe reload                  # request configuration reload
```

## Endpoint selection

The default endpoint is `http://127.0.0.1:9630`. Select another exporter with persistent options:

| Option | Default | Purpose |
|:---|:---|:---|
| `--host` | `127.0.0.1` | pg_exporter host name or IPv4 address |
| `-p, --port` | `9630` | pg_exporter HTTP port |
{.full-width}

```bash
pig pe --host pg-meta -p 9630 stat
pig pe --host 10.10.10.10 get
```

The command concatenates the host and port into a plain HTTP URL and assumes the standard
`/metrics`, `/stat`, and `/reload` paths. It does not support a custom telemetry path, HTTPS,
authentication, client certificates, or a base URL. Use `curl`, Prometheus tooling, or a secured
reverse proxy for those cases.

## pe get

Fetch `/metrics` and print PostgreSQL metric families. The command retains metric samples whose
names start with `pg_` and their matching Prometheus `HELP` and `TYPE` lines.

```bash
pig pe get
pig pe --host pg-meta get
```

Use a general Prometheus client or `curl` when you need the complete endpoint, including non-`pg_`
process and runtime metrics.

## pe list

Fetch `/metrics` and print one `HELP` declaration for each observed `pg_` metric family.

```bash
pig pe list
pig pe --host pg-meta list
```

This is discovery output from the current exporter configuration; it is not a static list embedded
in PIG.

## pe stat

Fetch and print pg_exporter's `/stat` response.

```bash
pig pe stat
```

The exact response is owned by the installed pg_exporter version.

## pe reload

Request `/reload` and print the response.

```bash
pig pe reload
```

Reload changes the running exporter's configuration state. Ensure the exporter configuration has
already been validated and that the selected endpoint is the intended instance.

## Legacy limitations and output

PIG uses its shared bounded-connect HTTP transport, but this legacy wrapper does not interpret
HTTP status codes or impose a response-body limit. Network and body-read failures return non-zero;
an endpoint's non-2xx body is otherwise handled like any other response. Call the exporter endpoint
directly when strict HTTP semantics matter.

The command family uses PIG's legacy structured adapter for `-o json|yaml`. The payload captures
the operation and text produced by the endpoint; the Prometheus exposition format itself remains
text owned by pg_exporter.

This command family does not consume `~/.pig/config.yml` and remains available if that file is
malformed; endpoint selection comes only from its command flags and defaults.

## Operational boundary

`pig pe` does not start pg_exporter, edit its files, scrape continuously, or act as a Prometheus
server. PIG installs the `pg-exporter` package through its package catalog, while pg_exporter owns
its daemon configuration and HTTP protocol. This command remains a compatibility shortcut for the
default local deployment rather than a new PIG client subsystem.
