---
title: "先编译和校验，再提交：原生 sty conf 流水线"
linkTitle: "原生 sty conf"
date: 2026-02-18
lastmod: 2026-11-11
description: "pig sty conf 如何校验模板、修改配置、保护凭据，并原子写入 Inventory。"
tags: [sty, inventory]
weight: 15
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-02-18；生产契约于 2026-08-14 定稿。<br>
> **状态：** 原生流水线已随 [pig v1.8.0](/zh/release/pig-1.8.0/) 发布；有序模板查找于 2026-11-08 在本地实现，不声明已随 PIG 发布。2026-11-11 的区域修订为 Accepted。<br>
> **当前参考：** [`pig sty conf`](/zh/sty/#sty-conf)<br>
> **范围：** 从受信 Pigsty 模板生成一份经过校验的静态 Inventory，不是任意 YAML 转换器。

## 决策 {#decision}

`pig sty conf` 应当像一台小型编译器：解析一个安全模板，读取结构，应用一组有边界的结构化变更，
校验完整候选文件，并且只在所有必要阶段成功后原子提交输出。

命令不调用旧 `configure` 脚本，也不回退到原始 Shell 执行。
结构化结果报告选中的输入、实际选择、变更类型与告警，但不返回生成的凭据值。

2026-11-08 的扩展与 Pigsty 使用相同的固定顺序解析模板裸名称：根目录、`ha`、`fork`、`app`、
`demo`、`build`。在预检和变更前完成一次解析，后续流水线和结构化结果统一使用选中的相对名称作为 mode。

## 背景 {#context}

模板配置看似简单，直到路径、符号链接、多 IP 占位符、固定版本模板、镜像、代理环境、生成凭据与部分有效 YAML
同时出现。文本替换流水线可能级联替换 IP，修改无关域名，泄露秘密，或在最终校验失败后截断目标文件。

输出 Inventory 可能包含管理员凭据，因此文件处理与结果渲染都属于安全边界。

Pigsty 将模板分组放入子目录，同时接受 `full` 这样的简写。仅找到 `ha/full.yml` 还不够：
构建模板跳过 IP 映射和管理员检查，`fork/mssql` 与 `fork/polar` 固定 PostgreSQL 版本。
这些规则必须依据选中的模板执行，不能随输入写法变化。

## 考虑过的方案 {#alternatives}

- **调用现有 Shell configure 脚本。** 解析、校验和结果语义仍在 PIG 控制之外。
- **使用全局搜索替换。** IP 与域名需要精确占位符边界和同时映射。
- **先写文件再校验。** 失败候选可能替换仍然可用的 Inventory。
- **接受任意绝对模板路径。** 命令应编译已知 Pigsty mode，而不是成为特权文件复制器。
- **为了方便返回生成密码。** 结构化日志与 Agent 轨迹不是秘密交付通道。
- **递归搜索所有目录，或遇到同名模板就拒绝。** 采用 Pigsty 的固定优先级；显式路径选择特定模板，
  无关目录不会自动获得简写。
- **硬编码别名表，或只按文件 basename 判断特殊行为。** 模板可用性由已安装文件决定，
  `app/mssql` 不应继承 `fork/mssql` 的规则。

## 契约 {#contract}

- 模板通过安全相对名称解析到 Pigsty 配置树下；
- 裸名称依次选择 `conf/`、`conf/ha/`、`conf/fork/`、`conf/app/`、`conf/demo/`、`conf/build/`
  下首个匹配的普通文件；显式相对路径不参与探测；
- 可省略开头的 `./`、`conf/` 前缀和 `.yml` 后缀；路径清理前就拒绝目录穿越分量，
  命中模板内容无效时不会回退；
- 预检、变更和既有 `mode`/`template_path` 结果字段统一使用解析后的 mode；
  旧版 Pigsty 根目录的 `mssql`/`polar` 继续保留版本锁定规则；
- 拒绝绝对路径、目录穿越、路径逃逸，以及直接路径、符号链接父目录或硬链接造成的源/输出别名；
- 解析与 IP 冲突检查先于外部预检；
- 占位 IP 同时映射，无关地址保持不变；
- 域名替换只匹配精确模板 token；
- profile、region、proxy、locale 与 PostgreSQL 版本变更都是有边界的结构化操作；
- 2026-11-11 修订要求显式选择或探测出的区域为 `default` 时也写入，覆盖模板原有的 `china`；
  结果必须报告实际写入的区域值；
- 每个已知凭据标识符只生成一个随机值，结果只暴露标识符；
- 完整候选接受原生校验，并可选执行有超时边界的 Ansible 解析；
- 任一失败都不改变目标文件；
- 成功结果以 `0600` 权限原子写入。

## 影响 {#impact}

使用 `sty conf` 从已知模板生成新 Inventory。编辑已有 Inventory 时，使用无损的
`pig inventory` 工作流。

固定版本模板保留原版本；请求了冲突的版本时，命令给出告警。

根目录优先保护现有安装。在标准分组布局下，`full` 与 `ha/full` 选择同一模板，`oss` 与
`build/oss` 也一样。裸名称发生碰撞时使用文档规定的顺序；模板树存在重名时，显式路径是稳定的选择。
解析器不会额外建立从 `fork/mysql` 到 `fork/halo` 的兼容别名。

## 验证与演进 {#verification}

原生 configure 方案最早记录于 2026-02-18，生产实现收敛于
[`74e084e`](https://github.com/pgsty/pig/commit/74e084e)，
最终契约同步提交为 [`adc4260`](https://github.com/pgsty/pig/commit/adc4260)。
测试覆盖目录穿越与别名、同时 IP 映射、域名边界、交互与关闭输入选择、版本处理、代理和区域变更、
凭据生成与脱敏、预检顺序、校验失败、权限与原子写入。

有序查找对齐 Pigsty 提交
[`d3f3aae`](https://github.com/pgsty/pigsty/commit/d3f3aaeeb34c10be967dd34880b67d68f34b26ff)。
PIG 实现记录于提交
[`ba771a5`](https://github.com/pgsty/pig/commit/ba771a587ec11a55dd43350cce4e9ce36586b308)，
包含模板解析器、版本锁定处理及配套回归测试。验证命令为 `go test ./...`、
`go vet ./...` 与 `make docs-check`。回归覆盖搜索优先级、显式路径、输入规范化、规范结果字段、
构建模板预检与 IP 行为，以及旧布局和分组布局下的版本固定模板。

2026-11-08 的 CLI 复核使用上述 Pigsty 提交 `d3f3aae` 中全部 54 个 `.yml` 条目，包含 Supabase 符号链接。
以裸名称、带目录的名称和 `./conf/ha/full.yml` 这样的文件名执行 `pig sty conf MODE -H FIXTURE -r default -s -n -o json -O OUTPUT`。
共执行 162 次调用，每份模板的三种写法都生成相同的 Inventory，并返回相同的规范名称；裸名称同时覆盖 `-c` 形式。
另行验证了不存在与非法模式、源/输出别名、根目录优先级和显式路径选择。这些检查验证配置生成，不代表部署验收。

## 当前状态 {#status}

使用 `pig sty conf` 从 Pigsty 模板生成新 Inventory，使用 [`pig inventory`](/zh/inventory/) 查看或编辑已有声明。
当前参数、mode 与预检行为维护在 [`pig sty` 参考文档](/zh/sty/)中。
有序查找扩展已在本地实现；此前发布证据仅适用于原生流水线，不涵盖此扩展。
发行版中的可用性仍需对应 PIG 标签或发布制品佐证。
