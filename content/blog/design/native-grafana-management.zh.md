---
title: "用有边界的 Grafana 客户端替代仪表盘脚本"
linkTitle: "原生 Grafana 管理"
date: 2026-07-18
lastmod: 2026-08-28
description: "为什么 pig sty grafana 只拥有仪表盘生命周期与偏好设置的一小段 HTTP 契约，而不成为通用 Grafana 管理客户端。"
tags: [sty]
weight: 70
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-07-18<br>
> **状态：** v1.6.0 实现；Grafana dashboard schema v2 支持随后在 v1.6.2 交付。<br>
> **当前参考：** [`pig sty grafana`](/zh/sty/#sty-grafana)<br>
> **范围：** Pigsty 拥有的仪表盘目录、仪表盘与界面偏好；不是通用 Grafana provisioning。

## 决策 {#decision}

PIG 应通过有边界的原生 HTTP 客户端管理 Pigsty 随附的 Grafana 资产。
它可以检查就绪状态、列出托管资产、装载或初始化仪表盘、导出仪表盘、只清理自己拥有的资产，
并调整受支持的语言与样式偏好。

该命令不能扩张成通用 Grafana 管理 API。Datasource、organization、user、任意目录、plugin
和无关仪表盘都不属于它的所有权。

## 背景 {#context}

旧仪表盘工作流依赖脚本和本地文件布局，几乎无法提供结构化证据来说明连接了哪个端点、
哪些资产属于自己，或为什么只完成了一部分。另一方面，如果没有严格所有权模型就开放完整 Grafana API，
可能删除用户内容，也可能在参数和诊断中泄露凭据。

只有在网络、认证、所有权与结果边界都明确时，原生客户端才值得存在。

## 考虑过的方案 {#alternatives}

- **继续把 Shell 脚本作为公开接口。** 超时、重定向、响应大小、脱敏和结构化结果仍会不一致。
- **开放任意 Grafana API 调用。** 这会让 PIG 变成第二个没有稳定边界的 Grafana CLI。
- **仅凭目录名称删除。** 名称不足以证明资产所有权。
- **内置 demo 密码。** 默认凭据会变成长寿命秘密，并鼓励不安全自动化。

## 契约 {#contract}

- 每个请求都有连接与响应大小边界；
- 拒绝不安全重定向与过大响应；
- 认证操作前先检查公开 health；
- 凭据来自显式安全输入、环境或 Inventory，不内置默认密码；
- 命令行密码仅作为应急路径，并明确提示 argv 与 Shell 历史风险；
- 错误与结构化结果不包含凭据或响应正文；
- load 与 init 只处理 Pigsty 已知的仪表盘 bundle；
- clean 只删除能够证明由 PIG/Pigsty 拥有的资产；
- language 与 style 接受固定词表，并把 `auto` 映射到 Grafana 的 system 偏好；
- schema v1 与 schema v2 仪表盘表示在客户端边界完成规范化。

## 影响 {#impact}

原生客户端提供了更好的计划、错误分类与自动化结果，但必须维护自己拥有的那一小段 Grafana API。
支持新仪表盘 schema 是合理演进，不代表会支持无关 Grafana 资源。

运维人员可以继续使用其它 Grafana 客户端完成通用管理，PIG 不会声称拥有这些资源。

## 验证与演进 {#verification}

原生仪表盘工作流落地于 [`3060485`](https://github.com/pgsty/pig/commit/3060485)。
测试覆盖 health、认证、超时、重定向、大小限制、所有权检查、偏好请求、脱敏、部分失败与 load/dump。
Dashboard schema v2 支持随后在 [`67f6e3b`](https://github.com/pgsty/pig/commit/67f6e3b) 中加入，
并随 v1.6.2 发布。

## 当前状态 {#status}

`pig sty grafana` 是 PIG 支持的 Pigsty 仪表盘生命周期入口。
命令和凭据规则以当前 [`pig sty` 参考文档](/zh/sty/)为准；边界之外的资源使用 Grafana 原生工具。
