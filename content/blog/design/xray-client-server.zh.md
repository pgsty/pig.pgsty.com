---
title: "一键配置 Xray 客户端与服务端"
linkTitle: "Xray 客户端与服务端"
date: 2026-10-05
lastmod: 2026-10-05
description: "以现有可工作的客户端与服务端为参考，为 build proxy 增加配套的 VLESS、REALITY 与 Vision 初始化能力。"
tags: [build, cli, install]
weight: 90
authors: [Vonng]
draft: false
---

> **决策日期：** 2026-10-05<br>
> **状态：** Implemented（已实现），源码与本地测试已验证；尚未打 tag 或发布。既有参考部署保持不变。<br>
> **当前参考：** [`pig build`](/zh/build/)、[运维安全契约](/zh/design/ops-cli-safety/)与[发布历史](/zh/release/)<br>
> **范围：** 一键配置 Xray 客户端与服务端；Linux 客户端和服务端，以及 macOS 客户端。共享 Nginx 入口仍是独立部署边界。

## 决策 {#decision}

为 `pig build proxy` 增加明确的 `client` 与 `server` 子命令。新工作流采用
VLESS + RAW + REALITY + `xtls-rprx-vision`。服务端首次设置生成配套凭据，重复设置保留
已有客户端连接契约，并提供相同的标准 URI；
客户端直接接收 URI 或命令行参数、安装 Xray、配置本地监听、启动服务，并验证连接。
文件传递是可选方式，不是初始化的前提。

保留现有命令路径与 `x` 别名。无参数调用改为安装或确认 Xray。兼容期内，历史形式
`id@host:port [local]` 保留 VMess 语义与默认端口，不能在参数不足时静默解释成 VLESS。

## 背景 {#context}

[此前实现](https://github.com/pgsty/pig/blob/74cb1281860fae659f2aa4fec2898af34a0c2519/cli/build/proxy.go)
安装 `vray`，将 HTTP 到 VMess 的配置写入 `/etc/v2ray.json`，赋予 `v2ray` 组读取权限，
写入 Shell 别名，重启 `v2ray`，再检查 HTTPS 请求。现有测试覆盖参数解析、包管理器选择与凭据脱敏。

已检查的参考配对使用 Xray 26.3.27。运行中的 macOS 客户端在回环地址的 8888 端口同时提供
HTTP 与 SOCKS，出站使用 VLESS/RAW/REALITY/Vision，采用 Chrome 指纹、关闭 multiplexing，
并启用 ML-DSA-65 验证。检查期间 HTTP 与 SOCKS 请求均成功；客户端 UUID、short ID 与 SNI
匹配服务端相应字段。

参考 Linux 服务端监听回环地址的 9443 端口。Nginx 占用公网 443，按 SNI 选择后端，
并转发 PROXY protocol 头。Xray 接收该头，连接 REALITY target，使用 `freedom` 出站，
阻断匹配 `geoip:private` 的目的地址。这是入口组合，不是 Xray 独立监听公网 443。

检查过的 Pigsty RPM 与 DEB 制品覆盖两种架构，均提供 `/usr/bin/xray`、权限为 0640 且归属
`root:xray` 的 `/etc/xray.json`、`xray:xray` 服务账户、`xray.service`，以及
`/usr/share/xray` 中的地理数据。安装脚本只重载 systemd，不自动启动或启用服务。
公开仓库索引列出了 26.3.27-1PGSTY；制品检查和仓库收录不等于已在所有操作系统上完成安装验证。

## 考虑过的替代方案 {#alternatives}

- **只替换 V2Ray 名称，继续只支持 VMess。** 无法满足服务端初始化与参考协议需求。
  旧模板可以通过 Xray 配置校验，但 Xray 会输出 VMess 弃用警告。
- **建设通用代理管理器。** 暂缓：订阅、协议目录、TUN、透明代理、流量统计与任意配置导入
  超出了本次配套初始化需求。
- **立即新增顶层命令。** 暂缓：现有 `build proxy` 可以容纳两个角色，无须变更根命令语法或维护第二套实现。
- **原样复制参考服务端。** 否决：要求 PROXY protocol 的回环监听不能直接接收公网连接，
  也必须尊重现有 Nginx 对端口的占用。
- **要求客户端必须通过文件初始化。** 否决：粘贴一条 URI 或直接指定参数是主要用法；
  受保护文件与标准输入仍适用于自动化。
- **在普通成功输出中打印生成的凭据。** 否决：结构化结果和日常日志应可以安全保留；
  显式请求的导出可以将 URI 交付到终端。

## 契约 {#contract}

已经实现的角色语法如下：

```bash
# 在 Linux 服务端执行，显式打印连接 URI 供复制。
pig build proxy server --host proxy.example.com --target www.example.net:443 --export -

# 在 Linux 或 macOS 客户端粘贴服务端返回的 URI。
pig build proxy client 'vless://UUID@proxy.example.com:443?encryption=none&security=reality&type=tcp&flow=xtls-rprx-vision&sni=www.example.net&fp=chrome&pbk=PUBLIC_KEY&sid=SHORT_ID&pqv=VERIFY_KEY'

# 也可以逐项指定连接参数。
pig build proxy client --server proxy.example.com:443 --id UUID --sni www.example.net --public-key PUBLIC_KEY --short-id SHORT_ID --pqv VERIFY_KEY

# 可选的受保护文件输入。
pig build proxy client --from ./client.uri

# 复用运行中 Linux 服务端的凭据，不改变它的部署。
pig build proxy server --host proxy.example.com --export-only --export -

# 使用默认客户端监听 127.0.0.1:12345 做无变更预览。
pig build proxy client --from ./client.uri --plan

# 显式使用已检查的本地客户端监听地址。
pig build proxy client --from ./client.uri --listen 127.0.0.1:8888

# 位于已配置可信入口后的 Xray 后端，默认监听 127.0.0.1:9443。
pig build proxy server --host proxy.example.com --target www.example.net:443 --proxy-protocol --export ./client.uri
```

**服务端输入与默认值。** 必须指定对外公布的 `--host` 与 REALITY `--target`。
公网 `--port` 默认 443，直连模式默认在所有 IPv4 接口监听该端口。
首次设置指定 `--proxy-protocol` 时，改为默认监听 `127.0.0.1:9443`。
显式 `--listen` 改变绑定地址，不改变公布的公网端口。重复设置未指定 `--listen` 时，保留已有
受支持配置的监听地址，不使用首次设置的默认值替换它。首次设置时，除非指定 `--sni`，否则从 target
主机名推导 SNI；重复设置保留已有 SNI，不重新推导替代值。应用配置前检查 target 的 TLS 兼容性，
不静默选择无关的伪装站点。

生成 UUID、X25519 密钥对、随机八字节 short ID，以及独立的 ML-DSA-65 seed 与验证密钥。
重复设置复用已有 PIG 管理的材料，普通重跑不轮换凭据。轮换与多用户管理需要后续明确契约。
使用 `warning` 日志、关闭访问日志、`decryption: none`、Vision flow，并明确阻断私网目的地址。
地理数据环境变量指向软件包提供的资源目录。

**服务端幂等。** 用相同输入重复设置，必须让已有客户端继续可用，无须修改客户端配置。
保留 UUID、X25519 私钥及对应客户端认证材料、short ID、ML-DSA seed 与验证密钥、SNI，以及
协议默认值。公布的 host 与公网端口相同时，导出同一条规范 URI。只在首次创建服务端配置时
生成凭据，不能因为再次执行设置而重新生成。

已有受管理配置和服务设置满足请求，且服务已运行并启用时，只执行检查，不重写文件或重启服务。
若仅服务停止或自动启动被关闭，则使用原有凭据恢复请求的服务状态。已有认证材料缺失、损坏或
存在歧义时必须报错，不能通过静默重新生成凭据来修复。新输入与已有认证或 SNI 契约冲突时，
普通设置拒绝执行；此类变更需要明确的迁移或轮换契约，不能作为普通重跑处理。

**复用已有服务端。** `server --export-only --host HOST --export DESTINATION` 读取现有软件包
服务端配置，使用当前 UUID、SNI、short ID，以及派生的客户端验证材料，导出连接 URI。
公布的公网端口仍默认 443，不能从回环后端端口推断。要求存在唯一、无歧义且受支持的
VLESS/REALITY 入站、客户端账户、SNI 与 short ID；遇到歧义或错误材料时拒绝，不任意选择条目。
此模式不安装、不重写服务端或服务配置、不重启、不启用服务、不轮换凭据；显式请求的文件导出
是唯一持久写入。在进程内派生验证材料，避免将已有私钥或 seed 放入子进程参数。
这个分支执行只读查询与显式凭据导出；共享的 server 命令保留保守的 action 注解。

**客户端输入与默认值。** 主要用法是直接传入一个带引号的 `vless://` 位置参数。
同时支持参数模式：`--server host:port`、`--id`、`--sni`、`--public-key`、`--short-id`；
服务端使用 ML-DSA 验证时，通过 `--pqv` 提供验证密钥。参数模式指定连接字段，REALITY、RAW、
Vision 与 Chrome 采用下述默认值。所有输入形式进入同一份经过验证的连接模型与配置生成器。
保留 `--from FILE` 与 `--from -`，作为可选的文件与标准输入方式。拒绝混用不同连接输入，
不静默用 flags 覆盖 URI 字段；`--listen` 等本地选项可用于所有输入方式。

`client.uri` 是普通 UTF-8 文本文件，内容只有一条标准 `vless://` URI，可带结尾换行；
文件名可以任意指定，它不是新的 PIG 配置格式。
只支持参考组合 REALITY + Vision + TCP/RAW。URI 中的 `type=tcp` 映射为 JSON
`network: raw`，`pbk` 映射为 `password`，`sid` 映射为 `shortId`，`pqv` 映射为
`mldsa65Verify`。保留 ML-DSA 验证字段，不静默丢弃。拒绝重复参数，以及会改变连接语义的
不支持参数。映射遵循[上游分享链接规范](https://github.com/XTLS/Xray-core/discussions/716)。

首次设置使用 `socks` 入站，默认绑定 `127.0.0.1:12345`，沿用现有 PIG 客户端默认地址。
可通过 `--listen 127.0.0.1:8888` 显式使用已检查的本地客户端地址。重复设置未指定 `--listen` 时，
保留已有受管理客户端的监听地址。同一端口提供 HTTP，启用 UDP，关闭 multiplexing。
出站使用 `encryption: none`、Vision flow、Chrome 指纹与 `spiderX: /`。
上游 [Socks 参考](https://xtls.github.io/en/config/inbounds/socks.html)明确说明支持 HTTP。
分别验证 HTTP 与 SOCKS，不能仅以 TCP 端口开启认定代理工作。

命令行字段与现有参考配置的对应关系如下。客户端路径相对于 VLESS 出站，服务端路径相对于
VLESS 入站。

| 命令行字段 | 客户端配置 | 服务端配置或导出 |
|:---|:---|:---|
| 服务端 `--host`、`--port`；客户端 `--server` | `settings.vnext[0].address` 与 `.port` | URI 对外连接地址，不一定是绑定地址 |
| 各角色的 `--listen` | 本地入站的 `listen` 与 `port` | VLESS 入站的 `listen` 与 `port` |
| 客户端 `--id` | `settings.vnext[0].users[0].id` | 匹配 `settings.clients[0].id` |
| `--sni` | `streamSettings.realitySettings.serverName` | 属于 `streamSettings.realitySettings.serverNames` |
| 客户端 `--public-key` | `streamSettings.realitySettings.password` | 从 `streamSettings.realitySettings.privateKey` 派生 |
| 客户端 `--short-id` | `streamSettings.realitySettings.shortId` | 属于 `streamSettings.realitySettings.shortIds` |
| 客户端 `--pqv` | `streamSettings.realitySettings.mldsa65Verify` | 从 `streamSettings.realitySettings.mldsa65Seed` 派生 |
| 服务端 `--target` | 没有直接对应字段，SNI 需兼容 | `streamSettings.realitySettings.target` |
| 服务端 `--proxy-protocol` | 无对应字段 | `streamSettings.rawSettings.acceptProxyProtocol: true` |

参考服务端保持 `realitySettings.xver: 0`：接收 Nginx 的 PROXY 头，与向 REALITY target
发送 PROXY 头是不同设置。模板默认值保留参考配对的 flow、传输安全、日志、关闭 multiplexing、
服务端私网目的地址阻断，以及客户端指纹。公网连接地址、绑定地址与 target 各自承担不同角色。

**平台与服务所有权。** Linux 使用已经配置的软件仓库，以及上述软件包账户、配置路径与 unit。
macOS 客户端使用 Homebrew Xray、权限为 0600 的用户配置 `~/.config/xray/pig-proxy.json`，
以及专用用户 LaunchAgent `com.pigsty.xray-proxy`；不接管其它 Xray daemon 或 Homebrew 服务。
Linux 设置需要 root 与运行中的 systemd；macOS 客户端使用普通用户，并需要已有 Homebrew。macOS 服务端不属于本次变更范围。

新角色设置明确启动服务并启用自动启动；仅安装时不启动或启用服务。Linux 下，PIG 管理有边界的
`pig-proxy.conf` systemd drop-in，用于资源目录和 capabilities。直接绑定特权端口时，
先清空 bounding 与 ambient 集合，再按需授予 `CAP_NET_BIND_SERVICE`，避免 systemd 将正向设置
与软件包 unit 的权限叠加；回环地址上的非特权端口后端
不需要该能力。不能依赖宽松的主机 sysctl，也不能为了监听 443 改为以 root 运行 Xray。

**应用与恢复。** 变更前完成参数解析，检查路径、端口所有权、服务冲突与已有配置。
通过完整的受支持配置形态识别 PIG 管理的配置，不能只凭一个入站 tag 判断。
替换不同或不支持的客户端配置需要 `--replace --yes`。不支持的服务端配置，以及使用其他账户、显式指定其他服务组或加载额外配置的服务 unit 会被拒绝。
`--plan` 支持预览，不安装、不生成凭据、不写文件、不重启服务。

通过 Go 序列化生成 JSON。暂存受保护的候选配置，以实际服务身份执行 Xray 校验，再原子应用
配置和服务变更。判断是否需要应用变更时，同时检查内容、所有权与权限。
macOS 将持久禁用状态与已加载状态分别检查，启动时启用自己的 LaunchAgent，失败时恢复两种状态。
保存原始内容、所有权、权限、服务启用状态与运行状态，用于有边界的回滚。
服务健康与连通性检查通过后，才交付 Shell 别名或连接导出。客户端要求 HTTP 与 SOCKS 访问
`https://www.google.com/generate_204` 均返回 HTTP 204，因此服务端外网访问该端点是验收条件。
应用失败返回非零，并说明哪些
恢复步骤成功；安装过的软件包可能保留。

不删除或自动停止 V2Ray。端口冲突在预检阶段停止，并给出迁移指引；保留原 V2Ray 配置供操作者
控制回滚。保留 `po`、`px`、`pck` 便利命令，同时覆盖构建工具需要的小写代理环境变量。
当前 Shell 激活仍需要 source 生成的 Shell 文件并执行 `po`；子进程不能修改父 Shell 的环境。

**秘密与导出。** `--export FILE` 将显式请求的连接导出写入权限为 0600 的文件，
不包含服务端私钥或 ML-DSA seed。`--export -` 明确将一条完整 URI 交付到标准输出，
非秘密的初始化诊断写入标准错误。凭据导出模式要求文本输出，与 JSON/YAML 同时指定时在变更前
拒绝，不把 URI 放进结构化结果。普通初始化输出仍脱敏。允许命令行输入，同时明确调用者的
Shell 历史或进程检查可能保留这些凭据；需要避免留存时仍可选择文件或标准输入。

将整个 URI 视为凭据，包括 UUID 与认证字段。默认日志、计划、JSON/YAML 结果与失败详情只包含
脱敏摘要及导出路径。密钥材料在进程内生成和派生。校验器输出必须私下捕获：上游配置错误
可能直接包含错误的秘密值，不能将通用子进程输出捕获视为安全凭据边界。重复导出到已有受保护文件时，若内容是
同一条规范 URI，则成功返回而不重写；内容不同时报告冲突，不能静默覆盖或在诊断中打印原内容。

**入口与验证边界。** 一键服务端设置默认使用直连模式。显式 `--proxy-protocol` 后端模式
要求绑定回环地址，并已有可信前端。本次不重写 Nginx 或防火墙、云安全组规则。
公网端口已被占用时明确失败，不停止端口拥有者。后端就绪不能证明公网入口正常；服务端设置
分别报告本机检查，并将外部可达性保持为待验证，直到客户端握手与 HTTPS 请求实际成功。

生成等价的 Xray 配置应覆盖参考配对的全部协议与认证字段。复现完整参考部署还需要 Nginx 的
SNI map、接收 PROXY 头的网站后端，以及操作系统特定的服务注册。当前实现管理 Xray 及其服务设置，
不宣称可从一个服务端 URI 还原这套 Nginx 组合。配置等价不要求逐字节保留 tag、字段顺序或安装专属名称。

## 影响 {#impact}

用户通过一条标准 URI 衔接两次初始化操作，或直接指定客户端参数，配套参数自动生成，
无须手改 JSON，也无须创建连接文件。
新客户端与历史 VMess 形式首次设置都默认使用 `127.0.0.1:12345`。直连服务端默认在所有 IPv4
接口监听公网端口，PROXY protocol 后端默认监听 `127.0.0.1:9443`。重复设置未指定 `--listen` 时
保留已有监听地址。配置与服务管理明确区分角色、操作系统、所有权和外部入口。

实现保留在 `cmd/build.go` 与 `cli/build` 下的聚焦文件中，复用现有计划、输出、确认、特权写入
与日志辅助函数。只有可执行行为实现后才更新当前参考，只有到达发布门槛后才修改发布注记。

## 验证与演进 {#verification}

2026-10-05 的初始检查核对了运行中的参考配对、Xray 26.3.27、四份 RPM/DEB 软件包制品，
以及此前 VMess 行为。这些观察建立参考基线，与下面的新实现验收分开记录。

[源码实现](https://github.com/pgsty/pig/commit/d090b7c9ab9301c06f9ccb2151c732d598f0e40c) 的聚焦测试覆盖角色语法、
URI/直接参数/文件/标准输入等价、严格参数解析、凭据脱敏、监听默认值与保留、只读导出、
拒绝损坏或有歧义的服务端、复用服务端凭据、重复导出、受保护文件、capabilities 选择与无变更计划。
`go test ./...`、`go vet ./...`、静态分析、死代码与复杂度检查，以及命令/build 包重复随机竞态测试均在本地通过。

一台全新 Debian 13 ARM64 虚拟机通过一条 SSH 管道读取既有参考服务端连接并执行
`client --from -`。PIG 安装 Xray 26.3.27、以 `xray` 账户配置和启用服务，并通过独立的
HTTP/SOCKS 健康检查。另行通过两个协议发起 HTTPS 请求，均返回 HTTP 200。
重复设置保留配置字节与运行 PID。使用错误 UUID 替换时返回非零，恢复原配置与服务，
随后请求成功。整个只读导出与客户端测试期间，参考服务端配置哈希与 PID 均未改变。

第二台全新 Debian 虚拟机验证直连服务端创建、以 `xray` 身份绑定特权端口、0640 配置、
0600 导出与重复设置。第二次设置后配置、导出内容与 PID 均不变。
应用监听变更后的导出失败能够恢复原配置与运行服务。
生成的 URI 也成功建立新的 REALITY/Vision 连接，包含 ML-DSA 验证；
HTTP 和 SOCKS 访问可达 TLS 网站均返回 HTTP 200。
该测试服务端所在本地网络无法访问 Google 健康检查端点，因此这组配对的完整客户端设置
正确失败并回滚。完整的一行命令客户端验收通过既有参考服务端完成。

[最终复核修正](https://github.com/pgsty/pig/commit/5d8660c8c12e6c00b77d409efd2287b8299377b1) 补上文件归属、systemd 权限集重置、
服务身份与启动参数检查，以及 macOS 持久启用状态恢复。Debian 实测先复现了配置属组错误
仍被判定为无变更的行为，再验证修复归属后配置字节保持不变，随后重复设置不重启。
直连服务端的 bounding 与 ambient 集合均只保留 `CAP_NET_BIND_SERVICE`，认证与导出内容不变。
另用已有 Homebrew Xray 创建独立的 macOS 临时 LaunchAgent 客户端，验证连接参考服务端的
HTTP/SOCKS 请求、无变更重复设置、禁用状态恢复，以及错误 UUID 后恢复原配置和原禁用状态；
回滚后的代理请求也成功。原有 macOS 参考服务未被接管。

这些检查不能证明 RPM 运行验收、全新 Homebrew 安装、UDP 转发、
任意 Xray 版本兼容性或新部署的 PROXY protocol 前端。
成功的客户端测试经过参考服务端既有 Nginx/PROXY 入口，但 PIG 没有修改该入口。
其余平台与传输检查属于后续发布验收，不能推断为已经通过。

中英文当前参考与本记录配套交付，并通过 `make docs-check` 检查。
源码提交、文档提交、推送/CI、tag 制品与公开部署分别作为完成门槛。

## 当前状态 {#status}

所有者接受角色工作流、直连与后端监听默认值、首次客户端端口 12345，
以及服务端重复设置保持已有客户端有效的要求。
源码实现与本地 Debian 运行检查满足这些要求，包含通过既有服务端完成的一行命令客户端实测。
macOS 参考守护进程与既有 Linux 服务端均未变更。
不宣称已打 tag 发布、部署公开文档或升级系统 PIG。
Nginx 入口自动化与凭据轮换仍属于后续独立决策。
