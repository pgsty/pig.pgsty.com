---
title: "用有边界的 Grafana 客户端替代仪表盘脚本"
linkTitle: "原生 Grafana 管理"
date: 2026-07-18
lastmod: 2026-10-13
description: "pig sty grafana 如何通过原生 HTTP 客户端管理仪表盘与偏好设置。"
tags: [sty]
weight: 70
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-07-18<br>
> **状态：** 随 [v1.6.0](/zh/release/pig-1.6.0/) 发布；[v1.6.2](/zh/release/pig-1.6.2/) 加入仪表盘 schema v2 支持。<br>
> **当前参考：** [`pig sty grafana`](/zh/sty/#sty-grafana)<br>
> **范围：** 仪表盘导入、导出、清理，以及部分组织与用户偏好设置。

## 决策 {#decision}

PIG 使用原生 HTTP 客户端管理 Grafana 仪表盘。本地 JSON 路径选择单个仪表盘、一个文件夹或
完整仪表盘目录。装载、导出与清理采用同一套选择规则，破坏性操作可以先预览。

默认目录是 Pigsty 仪表盘集合，用户也可以选择其他符合格式的目录。
清理默认按本地文件声明的仪表盘 UID 选择目标；显式指定 `clean --all` 时，
目标是当前 Grafana 组织中的全部仪表盘与文件夹。

## 背景 {#context}

旧 Shell 脚本依赖本地文件布局，对部分失败的说明有限。将这些操作纳入 PIG 后，
可以统一超时、认证、路径校验与结果输出。本地声明也为默认清理提供了明确范围。

## 考虑过的方案 {#alternatives}

- **继续把 Shell 脚本作为公开接口。** 网络限制、脱敏与结构化结果仍会分散在各脚本中。
- **开放任意 Grafana API 调用。** PIG 只需要仪表盘操作与少量偏好设置。
- **按文件夹名称选择清理目标。** 名称可能重复。本地 JSON 提供仪表盘 UID，文件夹仅在清空后删除。
- **内置默认密码。** 凭据应由用户配置。

## 契约 {#contract}

- 限制请求时间与响应大小，拒绝不安全的重定向。
- 认证前检查公开健康端点。没有密码时，`info` 可以仅返回健康状态。
- 凭据来自显式输入、环境或 Inventory；诊断与结构化结果不包含凭据和响应正文。
- `list` 列出当前组织的全部仪表盘。
- `load` 校验并导入所选本地文件，不删除远端仪表盘。
- `boot` 将已有的 `pigsty` 仪表盘设为首页并收藏，将组织命名为 Pigsty。
- `init` 装载完整仪表盘目录，全部成功后才执行 `boot`。
- `dump` 将所选远端内容导出为确定性的 JSON，并原子写入文件。
- `clean` 删除本地声明的 UID，再删除空文件夹。`--all` 显式选择整个当前组织。
  两种模式都显示计划，并要求确认。
- `lang` 与 `style` 修改组织和当前用户的对应偏好。样式 `auto` 映射为 Grafana 的 `system`。
- 读写时统一处理受支持的 schema v1 与 v2 仪表盘格式。

## 影响 {#impact}

装载与清理使用同一份本地声明，用户可以只操作一个仪表盘或文件夹。
UID 匹配用于定位目标，不代表该仪表盘最初由 PIG 创建。执行清理前应审阅计划，
尤其是使用 `--all` 时。

数据源配置、插件安装与用户管理继续使用 Grafana 自身工具。

## 验证与演进 {#verification}

原生工作流落地于 [`3060485`](https://github.com/pgsty/pig/commit/3060485)，
[`67f6e3b`](https://github.com/pgsty/pig/commit/67f6e3b) 加入仪表盘 schema v2 支持。
[已发布测试](https://github.com/pgsty/pig/blob/v1.9.0/cli/sty/grafana_test.go)
覆盖仅查健康状态、认证、装载范围、初始化顺序、导出稳定性、偏好更新、本地 UID 清理、
显式全量清理与计划变更拒绝。HTTP 客户端测试覆盖超时、重定向、响应限制与脱敏。

## 当前状态 {#status}

仪表盘工作流已经发布。路径选择、凭据与清理示例见
[`pig sty grafana`](/zh/sty/#sty-grafana)。
