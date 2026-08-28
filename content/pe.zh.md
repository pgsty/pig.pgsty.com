---
title: "pig pe"
description: "使用 legacy pig pe 快捷命令访问默认 pg_exporter HTTP 端点"
weight: 175
icon: fas fa-chart-line
categories: [参考]
tags: [postgres, cli]
---

`pig pe`（别名：`pgexp`、`pgexporter`）是运行中
[pg_exporter](https://github.com/Vonng/pg_exporter) 的 legacy 便利包装。
它读取默认指标与统计端点，也可以请求配置重载，但不是一套通用或版本化的 pg_exporter 客户端。

```bash
pig pe get                     # 输出 pg_ 指标
pig pe list                    # 从 HELP 行列出指标族
pig pe stat                    # 输出 exporter 统计信息
pig pe reload                  # 请求配置重载
```

## 端点选择

默认端点是 `http://127.0.0.1:9630`。使用持久选项选择其它 exporter：

| 选项 | 默认值 | 用途 |
|:---|:---|:---|
| `--host` | `127.0.0.1` | pg_exporter 主机名或 IPv4 地址 |
| `-p, --port` | `9630` | pg_exporter HTTP 端口 |
{.full-width}

```bash
pig pe --host pg-meta -p 9630 stat
pig pe --host 10.10.10.10 get
```

命令直接把 host 与 port 拼成普通 HTTP URL，并假定使用标准 `/metrics`、`/stat` 与
`/reload` 路径。它不支持自定义 telemetry path、HTTPS、认证、客户端证书或 base URL；
这些场景应直接使用 `curl`、Prometheus 工具或安全反向代理。

## pe get

读取 `/metrics` 并输出 PostgreSQL 指标族。命令保留名称以 `pg_` 开头的指标样本，
以及对应的 Prometheus `HELP` 和 `TYPE` 行。

```bash
pig pe get
pig pe --host pg-meta get
```

如果需要包含非 `pg_` 进程与运行时指标在内的完整端点，请使用通用 Prometheus 客户端或 `curl`。

## pe list

读取 `/metrics`，并为每个观察到的 `pg_` 指标族输出一条 `HELP` 声明。

```bash
pig pe list
pig pe --host pg-meta list
```

这是当前 exporter 配置的发现结果，不是内置在 PIG 中的静态列表。

## pe stat

读取并输出 pg_exporter 的 `/stat` 响应。

```bash
pig pe stat
```

响应的具体格式由已安装的 pg_exporter 版本拥有。

## pe reload

请求 `/reload` 并输出响应。

```bash
pig pe reload
```

Reload 会改变运行中 exporter 的配置状态。执行前应确认 exporter 配置已经校验，且选中的端点就是目标实例。

## Legacy 限制与输出

PIG 使用带连接阶段超时的共享 HTTP transport，但这个 legacy 包装不会解释 HTTP 状态码，
也不限制响应正文大小。网络或正文读取失败会返回非零；除此之外，非 2xx 正文仍按普通响应处理。
需要严格 HTTP 语义时应直接访问 exporter 端点。

该命令族使用 PIG 的旧命令结构化适配器支持 `-o json|yaml`。
结果会捕获操作与端点产生的文本；Prometheus exposition format 本身仍是 pg_exporter 拥有的文本格式。

## 操作边界

`pig pe` 不会启动 pg_exporter、编辑其配置文件、持续抓取指标或充当 Prometheus 服务器。
PIG 通过软件包目录安装 `pg-exporter`，而 daemon 配置与 HTTP 协议由 pg_exporter 自己拥有。
该命令只是默认本地部署的兼容性快捷入口，不代表 PIG 新增了一套客户端子系统。
