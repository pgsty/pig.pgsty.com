---
title: "pig v1.9.0"
linkTitle: "v1.9.0"
date: 2026-10-06
description: "600 条扩展目录记录、一键 Xray 客户端与服务端、自动准备仓库公钥，以及 cargo-pgrx 0.19.3。"
tags: [repo, build, catalog, cli]
weight: 1
authors: [Vonng]
release_url: https://github.com/pgsty/pig/releases/tag/v1.9.0
---

Pig `v1.9.0` 新增一键配置 Xray 客户端与服务端、自动准备 Pigsty 仓库签名公钥，
并将内置扩展目录更新为 **600 条记录**。`cargo-pgrx` 默认版本升级到 `0.19.3`，
内置 Pigsty 版本保持 `4.5.0`。

## Xray 客户端与服务端

- `pig build proxy` 安装或检查 Xray；`pig build proxy client` 配置
  VLESS/REALITY/Vision HTTP/SOCKS 客户端；`pig build proxy server` 配置 Linux 服务端。
  Linux 使用 systemd，macOS 客户端使用独立的用户 LaunchAgent。
- 客户端支持标准 VLESS URI、`--from FILE/-` 或显式连接参数。首次客户端监听
  `127.0.0.1:12345`，首次直连服务端监听 `0.0.0.0:443`；重复执行保留已有监听端点与服务端凭据。
- 配置、属主、权限与服务状态一致时不改写文件、不重启服务。客户端连通性检查失败会恢复
  原有受管文件与服务状态。替换不同的客户端配置需要 `--replace --yes`；两种角色均支持 `--plan`。
- `server --export-only --export -` 只导出已有连接，不改变部署。导出文件权限为 `0600`；
  显式导出到 stdout 要求文本输出。普通结果与计划不包含凭据。历史 VMess 位置参数形式
  继续使用 V2Ray。

```bash
sudo pig build proxy server --host proxy.example.com --target www.sraoss.co.jp:443 --export ./client.uri
sudo pig build proxy client --from ./client.uri
```

前置条件、macOS 配置、凭据处理与公网入口边界见 [**`pig build`**](https://pig.pgsty.com/zh/build/#build-proxy)。

## 仓库签名公钥

- `repo add`、`repo set` 与 `sty boot` 在选中仓库需要时准备内置 Pigsty 公钥。
  已有普通公钥文件直接复用；缺失的默认公钥离线写入
  `/etc/pki/rpm-gpg/RPM-GPG-KEY-pigsty` 或 `/etc/apt/keyrings/pigsty.asc`。
- 隐式默认公钥准备失败时给出警告，仅对选中的 Pigsty 仓库回退签名检查。
  默认公钥引用保持稳定，包括 APT 的 `signed-by`。
- 显式指定的签名公钥引用必须有效；无效或不可用的公钥在仓库替换、缓存刷新之前报错。
  EL 通过 `rpm --import` 导入显式引用。仅选择其他仓库时，不准备 Pigsty 公钥。

签名检查默认值、公钥准备与元数据刷新的区别见 [**`pig repo`**](https://pig.pgsty.com/zh/repo/#仓库定义)。

## 扩展目录与构建默认值

- 内置目录共 **600 条记录**，相较 v1.8.1 快照新增 22 条。新增条目包括
  `edtf_postgres`、`plphp`、`pg_lexo`、`pg_money`、`istore`、`colnames`、
  `pg_statkit`、`pgtelemetry`、`pg_rusage`、`pgexporter_ext`、`pg_statvfs` 与 `libx509pq`，
  同时刷新软件包版本与平台可用性元数据。
- 目录总数包含保留的生命周期记录。能否安装取决于扩展状态与操作系统、架构、PostgreSQL
  版本矩阵；600 并非每个平台都能安装的扩展数量。
- `pig build pgrx` 默认使用 `cargo-pgrx 0.19.3`；显式 `-v` 与扩展目录中的专用版本要求继续有效。
- 延续 v1.8.1 的平台调试包默认策略。`--nodbg` 可禁用 RPM 的 `debuginfo`/`debugsource`
  与 DEB 的 `dbgsym`；`-s|--symbol` 保留为已弃用的兼容空操作。

## 兼容性

没有移除已有命令或参数。新增 Xray 角色命令使用 VLESS/REALITY/Vision，历史 VMess
位置参数命令保持 V2Ray 行为。服务端配置成功只证明本地监听与服务就绪；防火墙、Nginx、
云安全组与公网连通性仍由操作者单独配置和验证。

## 验证

经过验证的 [v1.9.0 标签](https://github.com/pgsty/pig/tree/v1.9.0) 指向源码提交
[`9eb5488`](https://github.com/pgsty/pig/commit/9eb5488847ea34827a74c9f8bb7b2dd3778f5190)。该精确提交通过
[完整 CI](https://github.com/pgsty/pig/actions/runs/37483835198)，覆盖随机顺序测试、命令 race 回归、
vet、静态分析、漏洞扫描与发布 snapshot。[Release 工作流](https://github.com/pgsty/pig/actions/runs/37484632240)
生成八个 Linux/macOS 压缩包与 RPM/DEB 安装包，下载后已逐一验证 SHA-256。

## 校验和

```checksums
d0d80bd23a654308598f265ce4b4d4f78d6156c113ce6aa00f82bfc9519a180f  pig-1.9.0-1.aarch64.rpm
e3b25640c9e528f2b883f7e5f4838640a8897857fa22dc1324aca69b72966a7c  pig-1.9.0-1.x86_64.rpm
d7eb266e1b8ab60d20ac582c6b0e3741b7e8516ce1a56df447c0285b3e5dcab9  pig-v1.9.0.darwin-amd64.tar.gz
096284577d0493ddba871b51e820654b358c7f4eb9c11175674a1d21b2718824  pig-v1.9.0.darwin-arm64.tar.gz
a4b5ffca540bc4f924f86398bcad6cb7221ac7520b54b1d3fd32c9877d9cafd2  pig-v1.9.0.linux-amd64.tar.gz
ddfa80fbb34f6738dd68e0d04cd92355711330f6896cd650df7d71b012788def  pig-v1.9.0.linux-arm64.tar.gz
3d955a24a8ff805ee2b6da6428e2b882f97104e2fb597785225269443071d93a  pig_1.9.0-1_amd64.deb
c175b37552147e64590309801800826a0075ae8285ed78178c2adcaec3741471  pig_1.9.0-1_arm64.deb
```

{{< release-card >}}
