# AGENTS.md

pig.pgsty.com —— PIG 官网（Hugo + Docsy，与 pigsty.cc / silo.pgsty.com 同一套 chrome）。
给 AI agent 的项目约定，改动前先读这里。

## OINK build baseline

As of 2026-10-18, this site uses OINK v1.3.2 and Hugo Extended 0.168.0.
Keep CI and local builds on this baseline. Do not enable `--panicOnWarning`
or `HUGO_PANICONWARNING`; keep warnings visible and review them. The upstream
LibSass deprecation warning is accepted. No external Sass compiler is required.

## 硬性约定（不要「顺手修正」）

### 文档 URL 不带 `/docs/` 前缀

文档正文页直接挂在站点根下：`/install/`、`/repo/`、`/pg/`。`/docs/` 只是文档总览页。
这是刻意的布局（对齐 silo.pgsty.com），看到有人给文档页加 `content/docs/` 目录或
front matter `url: /docs/xxx/`，那是回归。

对应地：

- 侧栏树的根是 `Site.Home`，条目顺序由 front matter `weight` 决定，没有
  silo / sow 那套 `data/docs_nav.json` 冻结目录，也不需要跑生成脚本。
- `content/docs/_index.md` 与 `content/blog/_index.md` 都带 `toc_root: true`，
  这样它们只出现在侧栏顶部的根下拉里，不会在树里重复一行。
- `content/_div_cmd.md` 是分组标题（`sidebar_divider: true` + `build.render: link`），
  不是阅读页。OINK 原生侧栏树渲染该语义，项目样式只调整其 PIG 视觉。

### 博客 URL 不带 `blog` 前缀

内容按栏目放在 `content/blog/` 下，但 URL 里没有 `blog` 这一段 ——
`hugo.yaml` 的 `permalinks.page/section` 用 `:sections[1:]` 砍掉了第一段：

    content/blog/release/pig-1.6.0.md → /release/pig-1.6.0/
    content/blog/release/_index.md    → /release/

新开一个博客栏目（比如 `content/blog/news/`）自动就是 `/news/`，不用改配置。
只有 `content/blog/_index.md` 自己算出来是 `/`，所以它 front matter 里写死了
`url: /blog/` —— 别删。

### Design 栏目记录「为什么」，不复制当前命令手册

设计归档放在 `content/blog/design/`，公开 URL 是 `/design/` 与 `/zh/design/`。
每篇中英成对，`date` 使用有提交、发布或原始设计日期佐证的决策形成日，`lastmod`
表示最近一次事实与状态复核。当前命令行为仍以根级文档页为准，何时交付以 `/release/`
为准，设计文章必须链接这两类当前权威。

设计文章固定使用同一组显式 heading anchor：`decision`、`context`、`alternatives`、
`contract`、`impact`、`verification`、`status`。不得公开原始 Agent prompt、临时评审稿、
本机绝对路径、秘密或未经验证的完成声明。新增或修改后要通过 `bin/check_design.py`。

### 发布注记一个版本一篇，放在 `content/blog/release/`

发新版时加一对 `pig-X.Y.Z.md` / `.zh.md`，`weight` 从最新的往下递增（最新的最小）。
文中的 `**要点**` 这类整行加粗标签统一写成 `## 要点`，这样每篇都有目录。
front matter 与正文的具体形态见下面「发布注记写成 OINK 0.6 的原生形态」。

文档侧栏里的「版本 / Release」是 `content/_link_release.md` 这个占位页：
`manual_link` 指向 `/release/`，`build.render: link` 表示不产出页面本身。
它和 `content/_div_cmd.md`（分组标题）是同一类东西，别当成漏写正文的页面删掉。

### 版本号只从站点参数取

正文里不要硬写版本号，用站点参数：

- `{{< param version >}}` —— pig 自身版本（对应 `internal/config.PigVersion`）
- `{{< param pigsty_version >}}` —— pig 内嵌的 Pigsty 版本（`internal/config.PigstyVersion`）
- `{{< param pgext_count >}}` —— 已打包扩展数量

注意 `pigsty_version` 与 `version` 不是一回事：pigsty.cc 上的 `version` 指的是 Pigsty
版本，那边的文案照搬过来时容易串。

### 文档 chrome 与 blocks 由 OINK 提供，不在本站复制维护

本站通过 Hugo Module 固定引入 `github.com/pgsty/oink`。docs / blog 的布局、侧栏、
搜索、TOC、blocks/shortcodes、CSS、JS 与字体使用 OINK 的 `td-shell-*` 实现；不要再把
silo / sow / pigsty.cc 的整套模板或 `pig-*` chrome 拷回本仓库。

本站只保留站点专属覆盖：

- `layouts/index.html`、`layouts/download/landing.html` 是首页与下载页的版面本体
  （只出 `main`，chrome 由 OINK 提供）；
- `assets/scss/_styles_project.scss` 保留 PIG 品牌与 `sidebar_divider` 的站点视觉；
- 根级文档树由 `params.ui.docs_sidebar_root: home` 声明，`sidebar_divider`
  由 OINK 原生侧栏组件渲染，不要再复制整个主题 sidebar partial。

通用能力或 bug 修复应优先提交到 OINK；站点覆盖只承载 PIG 特有的信息架构或品牌外观。

### 首页与下载页跑在 OINK 的 landing shell 里

`layouts/index.html` 与 `layouts/download/landing.html` 都只是一个
`{{ define "main" }}` 块：`<head>`、navbar、胖页脚、搜索框与命令面板、脚本包
全部由 OINK 提供，本站不再自己写一套 chrome。站点侧只剩：

- `layouts/_partials/pig/hero-diagram.html` —— 首页 Hero 右半的内联 SVG 架构图；
- `layouts/_partials/hooks/head-end.html` / `body-end.html` —— 只在首页与下载页
  额外加载 `fonts.css` + `landing-v3.css` / `pig-v3.css` / `download.css` 与
  `landing-v3.js`（下载页再加 `download.js`）；
- `data/footer/<lang>.yaml` —— 胖页脚的品牌块与四列链接；
- 页脚版权行走各语言的 `params.copyright.authors`（按 Markdown 渲染）；
  要放 ICP 备案号就写进 `params.footer_center_info`。

`content/download.md` 写 `layout: landing`，一是让 `baseof.landing.html` 生效，
二是 `params.ui.landing_search` 认这个 layout —— 否则 navbar 上不会有搜索框。
两页的 front matter 都带 `body_class`，给站点样式圈定作用域。

**改样式前先看这段 shell 接缝。** OINK 会给 `main` 里的每个 `section` 压上 5rem
区块内边距（`.td-default main section`，权重 (0,1,2)），它高过版面自己的
`.hero` / `.landing-section`（(0,1,0)）。解决办法不是一刀清零 —— 那样连版面
自己的节奏一起没了 —— 而是给「设置 section 内边距的那几条规则」加 `.landing-page`
前缀：(0,2,0) 的类计数高于 (0,1,2)。首屏那一段还要再压过
`.td-default main > section:first-of-type`（(0,2,2)），所以顶部内边距经
`--pig-section-pad-top` 自定义属性交给 landing-v3.css 里的接缝规则，值仍然只写一处。
下载页里的嵌套 `section`（安装方式面板、子标签面板）同理。

`static/img/pig-word.svg` 是**纯文字**字标。OINK 0.6 的品牌是「图标 + 文字」的
组合标：图标一直在，字标是旁边可折叠的那一半。字标里再画一次猪头会重复。

改 Hero 文案时注意：`.pig-hero-title` 的窄屏字号 clamp 在 `pig-v3.css` 里，
双栏版的覆盖必须写在 `@media (min-width: 981px)` 内，否则窄屏会被高权重规则压住。

下载页的版本号与制品名全部由 `params.version` 推出来（`pig-X.Y.Z-1.x86_64.rpm`
这类命名跟着 goreleaser 走），发布日期从 `/blog/release/pig-<version>/` 那篇取。
发新版时改 `hugo.yaml` 的 `version` 就够了，下载页不用动。

### 分类法：categories 本地化，tags 用一套子系统词表

`hugo.yaml` 声明了三个分类法：`categories`、`tags`、`authors`。

- `categories` 是页面种类，中英各写各的，**只有文档页用**：Diátaxis 四类
  （`Tutorial`/`Task`/`Concept`/`Reference` ↔ `教程`/`任务`/`概念`/`参考`）。
  发布注记不带 categories —— 栏目本身已经说明它是什么，每篇再挂一个
  `Release` 分不出任何东西。
- `tags` 是页面讲的 pig 子系统，中英两版写同一套英文词，词表是封闭的：
  `repo`、`ext`、`postgres`、`patroni`、`pgbackrest`、`pitr`、`sty`、`build`、
  `inventory`、`catalog`、`cli`、`install`。文档与发布注记共用这套词表正是重点 ——
  `/tags/repo/` 会把 `pig repo` 参考页和每一个动过仓库处理的版本排在一起。
  单页最多四个。
- `authors` 是分类法不是字符串：文章写 `authors: [Vonng]`，档案页是词条页
  `content/authors/vonng/_index.md`（title=显示名，description=一句话简介，
  正文=长简介，页面包里的 `featured-avatar.png` 是头像）。
  不要再用 0.4 那种 `author: "..."` 字符串。

`content/_index.md` 的 cascade 带 `target: {kind: '{page,section}'}`，
这是刻意的：分类法列表页与词条页也是 home 的后代，一起染成 `type: docs`
会落到 OINK 的 `docs/list.html`，丢掉作者档案与博客行的样式。

博客索引用 OINK 默认的列表形态；站点开了 `blog_index_toggle`，工具栏里那个按钮
可以让读者在列表 / 卡片 / 表格之间切换。

### 发布注记写成 OINK 0.6 的原生形态

新增一个版本时，一篇发布注记长这样（中英各一份）：

    ---
    title: "pig vX.Y.Z"
    linkTitle: "vX.Y.Z"
    date: YYYY-MM-DD
    description: "一句话说清这版干了什么"
    tags: [repo, catalog]          # 子系统词表，最多四个；不要写 categories
    weight: 1                      # 最新的最小，往下递增
    authors: [Vonng]
    release_url: https://github.com/pgsty/pig/releases/tag/vX.Y.Z
    ---

    <正文>

    ## Checksums

    ```checksums
    <sha256sum / md5sum 的原始输出，一行一个文件>
    ```

    {{< release-card >}}

要点：

- `release_url` 是唯一需要写的发布事实。owner、项目、tag、源码归档地址都从它
  解析出来，日期用页面自己的 `date`。
- ```` ```checksums ```` 围栏直接吃 `sha256sum` / `md5sum` 的输出（`<hash>` +
  **两个空格** + 文件名）。主题渲染成资产表：每行一个下载链接、系统与架构徽章、
  按十六进制长度识别出的算法、截断的哈希 + 单行复制按钮，外加一个整表复制。
  下载基地址由 `release_url` 推出，所以围栏里只要文件名。打印 / Markdown / RSS
  输出会退回朴素清单。混用两种算法会告警，分块写。
- `{{< release-card >}}` 放在**结尾**。博客列表行的摘要取自 `.Plain`，卡片放开头
  会把摘要变成卡片里的链接文字。
- 不要再手写 `Release: <url>` 结尾行，也不要手写 "Artifacts: …" 链接行 ——
  发布卡片已经给出这些。

### 评论与统计

Google Analytics 4（`services.googleAnalytics.id: G-1D95QFXC80`）只在生产构建注入。
giscus 评论在 `params.comments`，讨论区开在**站点仓库** `pgsty/pig.pgsty.com` 下，
不占产品仓库 `pgsty/pig` 的 Discussions。首页与下载页是整页模板、没有 page-end，
所以两者都不渲染评论与分享栏。

页尾分享栏是 `params.ui.share`，每一项都是普通 `<a href>` 意图链接或本地复制按钮，
不引第三方脚本，也没有计数。

### 上游文档在 pigsty.cc / pigsty.io

英文正文来自 `pigsty.io/content/docs/pig/`，中文来自 `pigsty.cc/content/docs/pig/`。
从上游同步时记得改写链接：`/docs/pig/xxx/` → `/xxx/`（中文加 `/zh/` 前缀），其余
`/docs/...`、`/ext/...` 改成 `https://pigsty.io` / `https://pigsty.cc` 绝对链接。

## 其它

- 文案改动同时维护中英两版（`$zh` 分支 / `.md` 与 `.zh.md` 成对）。
- 本站构建只需要 Hugo Extended、Go 与 Git；OINK 已内置运行资源，不需要 Node/npm。
- 改完模板或 CSS 跑 `make check` 验证：它会做 production 构建并跑
  `bin/check_internal_links.py`。`static/css/*` 靠 md5 query string 破缓存，
  不需要手动改版本号。
- 首页计数在 `data/home/metrics.yaml`，每个数字都要能在它链向的文档页里查证。
- 品牌图形：`static/img/pig.svg` 是源，`pig-*.png` / `favicon.*` /
  `pig-social-card.png` 是从它派生的位图。

## Git 内容与大文件规则

用户于 2026-10-10 明确的通用仓库规则：

- 仓库默认保存源代码、配置和必要的轻量文档、元数据。构建产物、可执行文件、软件包、容器/虚拟机镜像、下载压缩包、数据库导出和大体积原始数据默认不进入 Git；文本格式的数据大文件同样需要检查。
- 在工作树内下载或生成上述文件之前，先选择仓库外的制品/数据位置，或补上合理的 `.gitignore` 规则并验证实际路径已被忽略，防止暂存和代理恢复/差异快照将它们写入 Git 对象库。
- 暂存、提交前检查新增文件的大小、类型和 staged 文件列表，只加入本次需要的源文件；不得用强制添加绕过忽略规则。优先保留来源清单、校验值及可复现的下载/构建方法。
- 对二进制素材、数据集或生成文件是否应纳入版本控制拿不准时，先问用户，再暂存或提交；确需例外时也先取得用户明确指示。
- 本规则不授权删除已有文件、stash、恢复快照或改写 Git 历史。忽略规则不会清除已存在的 Git 对象，历史清理需要单独明确范围。
