---
title: "先编译和校验，再提交：原生 sty conf 流水线"
linkTitle: "原生 sty conf"
date: 2026-02-18
lastmod: 2026-08-28
description: "为什么 pig sty conf 把 Inventory 生成视为带路径安全、结构化变更、秘密纪律和原子输出的编译流水线。"
tags: [sty, inventory]
weight: 15
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-02-18；生产契约于 2026-08-14 定稿。<br>
> **状态：** 已实现并随 [pig v1.8.0](/zh/release/pig-1.8.0/) 发布。<br>
> **当前参考：** [`pig sty conf`](/zh/sty/#sty-conf)<br>
> **范围：** 从受信 Pigsty 模板生成一份经过校验的静态 Inventory，不是任意 YAML 转换器。

## 决策 {#decision}

`pig sty conf` 应当像一台小型编译器：解析一个安全模板，读取结构，应用一组有边界的结构化变更，
校验完整候选文件，并且只在所有必要阶段成功后原子提交输出。

命令不调用旧 `configure` 脚本，也不回退到原始 Shell 执行。
结构化结果报告选中的输入、实际选择、变更类型与告警，但不返回生成的秘密值。

## 背景 {#context}

模板配置看似简单，直到路径、符号链接、多 IP 占位符、固定版本模板、镜像、代理环境、生成凭据与部分有效 YAML
同时出现。文本替换流水线可能级联替换 IP，修改无关域名，泄露秘密，或在最终校验失败后截断目标文件。

输出 Inventory 可能包含管理员凭据，因此文件处理与结果渲染都属于安全边界。

## 考虑过的方案 {#alternatives}

- **调用现有 Shell configure 脚本。** 解析、校验和结果语义仍在 PIG 控制之外。
- **使用全局搜索替换。** IP 与域名需要精确占位符边界和同时映射。
- **先写文件再校验。** 失败候选可能替换仍然可用的 Inventory。
- **接受任意绝对模板路径。** 命令应编译已知 Pigsty mode，而不是成为特权文件复制器。
- **为了方便返回生成密码。** 结构化日志与 Agent 轨迹不是秘密交付通道。

## 契约 {#contract}

- 模板通过安全相对名称解析到 Pigsty 配置树下；
- 拒绝绝对路径、目录穿越、路径逃逸，以及直接路径、符号链接父目录或硬链接造成的源/输出别名；
- 解析与 IP 冲突检查先于外部预检；
- 占位 IP 同时映射，无关地址保持不变；
- 域名替换只匹配精确模板 token；
- profile、region、proxy、locale 与 PostgreSQL 版本变更都是有边界的结构化操作；
- 每个已知凭据标识符只生成一个随机值，结果只暴露标识符；
- 完整候选接受原生校验，并可选执行有超时边界的 Ansible 解析；
- 任一失败都不改变目标文件；
- 成功结果以 `0600` 权限原子写入。

## 影响 {#impact}

该命令只支持定义明确的一组模板和变更，不提供任意编辑能力。
这个限制是刻意的：已有 Inventory 属于无损 `pig inventory` 工作流，`sty conf` 则拥有从已知模板进行可复现编译的职责。

固定版本模板保留自己的实际版本；通用版本请求无法应用时产生告警，而不是报告请求版本却生成另一个版本。

## 验证与演进 {#verification}

原生 configure 方向最早记录于 2026-02-18，生产实现收敛于
[`74e084e`](https://github.com/pgsty/pig/commit/74e084e)，
最终契约同步提交为 [`adc4260`](https://github.com/pgsty/pig/commit/adc4260)。
测试覆盖目录穿越与别名、同时 IP 映射、域名边界、交互与关闭输入选择、版本处理、代理和区域变更、
秘密生成与脱敏、预检顺序、校验失败、权限与原子写入。

## 当前状态 {#status}

使用 `pig sty conf` 从 Pigsty 模板生成新 Inventory，使用 [`pig inventory`](/zh/inventory/) 查看或编辑已有声明。
当前参数、mode 与预检行为维护在 [`pig sty` 参考文档](/zh/sty/)中。
