# PIG Documentation

This repository contains the bilingual website for **PIG** — *PostgreSQL
Install Guide*, the PostgreSQL extension package manager by
[Pigsty](https://pigsty.io). It is built with
[Hugo](https://gohugo.io/) and the [OINK](https://github.com/pgsty/oink)
documentation theme, with English at `/` and Simplified Chinese at `/zh/`.

- Site: <https://pig.pgsty.com>
- Project: <https://github.com/pgsty/pig>
- Theme: <https://github.com/pgsty/oink>

## Layout

Documentation pages live at the **site root** — `/install/`, `/repo/`,
`/pg/` — with no `/docs/` path prefix. `/docs/` is only the
documentation overview page, and the sidebar tree is built from the top-level
pages by front-matter `weight`.

```text
content/
  _index.md            # landing page metadata (the page itself is layouts/index.html)
  download.md          # /download/ — the release matrix page (layouts/download/single.html)
  docs/_index.md       # /docs/ — documentation overview, listed in the sidebar root menu
  start.md             # /start/      weight 10
  intro.md             # /intro/      weight 20
  install.md           # /install/    weight 30
  _link_release.md     # sidebar entry pointing at /release/ (manualLink, not a page)
  _div_cmd.md          # sidebar group heading (sidebar_divider, not a page)
  cmd.md               # /cmd/        weight 100
  repo.md ext.md build.md sty.md inventory.md pg.md pt.md pb.md pitr.md
  blog/                # /blog/ — all posts, newest first
    release/           # /release/ and /release/pig-X.Y.Z/
  authors/vonng/       # /authors/vonng/ — an author profile (the `authors` taxonomy term)
data/home/metrics.yaml # landing page counters
```

Blog URLs drop the `blog` prefix: `permalinks.page` and
`permalinks.section` in `hugo.yaml` use `:sections[1:]`, so
`content/blog/release/pig-1.6.0.md` publishes at
`/release/pig-1.6.0/`. A new blog subsection is a new top-level prefix with
no config change. Only `content/blog/_index.md` pins its own
`url: /blog/`, because slicing its single section would resolve to `/`.

Release notes are one dated post per version under
`content/blog/release/`. Adding a release means adding a
`pig-X.Y.Z.md` / `.zh.md` pair with `weight` ascending from the newest.

Each page ships as an English `.md` plus a Chinese `.zh.md`. Two sections
stay out of the docs sidebar tree via `toc_root: true` — `docs/` and
`blog/` — because the sidebar root menu already lists them.

## Taxonomy

Three taxonomies are declared in `hugo.yaml`: `categories`, `tags`, and OINK
0.6's `authors`.

- **categories** name the kind of page, and they are localized. Only
  documentation carries them, using the Diátaxis four — `Tutorial` / `Task` /
  `Concept` / `Reference` (`教程` / `任务` / `概念` / `参考`). Release notes
  carry no category: the section already says what they are, so a `Release`
  term on every post would classify nothing.
- **tags** name the pig subsystem a page is about, from one closed vocabulary
  shared by documentation and release notes, in English on both language
  trees: `repo`, `ext`, `postgres`, `patroni`, `pgbackrest`, `pitr`, `sty`,
  `build`, `inventory`, `catalog`, `cli`, `install`. That shared vocabulary is
  the point — `/tags/repo/` lists the `pig repo` reference page next to every
  release that touched repository handling. Cap a page at four.
- **authors** is a taxonomy, not a string. A post declares `authors: [Vonng]`;
  the profile is the term page at `content/authors/vonng/_index.md`, whose
  title is the display name, description the one-line bio, body the long one,
  and bundled `featured-avatar.png` the portrait. The pre-0.6 `author:` string
  is not used here.

Blog indexes publish as OINK's default row list. `params.ui.blog_index_toggle`
puts a control in the index toolbar so a reader can cycle any of them through
list, cards, and table.

Each release note is written in OINK 0.6's native release forms rather than by
hand:

- `release_url` in front matter is the one release fact. Everything else — the
  owner, the project, the tag, the source archive URLs — is parsed out of it,
  and the date is the page's own.
- `{{< release-card >}}` closes the post with the tag, the date, and links to
  the release, both source archives, and the repository. It sits at the *end*
  because blog list rows summarise from `.Plain`, and a card at the top would
  become the summary.
- A ```` ```checksums ```` fence turns `sha256sum` / `md5sum` output into the
  asset table: one row per file with a download link, OS and architecture
  badges, the algorithm (detected from the hex length), a truncated hash with
  a copy button, and a copy-all control. The base URL comes from
  `release_url`, so the filenames in the fence are the only thing to paste.
  Print, Markdown, and RSS output fall back to the plain listing.

## Comments and analytics

Google Analytics 4 (`services.googleAnalytics.id`) and giscus comments
(`params.comments`) are both configured in `hugo.yaml`. Analytics is injected
in production builds only. Comments render at the end of ordinary documentation
and blog pages; the landing page and the download page are standalone
templates with no page-end block, so they carry neither. Discussions live in
the site repository (`pgsty/pig.pgsty.com`), not the product repository, so
that user questions filed against `pgsty/pig` stay separate from page comments.

## Theme boundary

OINK 0.6.0 owns the documentation and blog layouts, navigation shell, search, table
of contents, blocks and shortcodes, styles, scripts, fonts, and third-party
runtimes. The site imports the pinned OINK 0.6.0 release as a Hugo Module.

The landing page and the download page keep their bespoke visual design, but
they render *inside* the theme shell: OINK supplies `<head>`, the navbar, the
fat footer, the search box and command palette, and the script bundle. Neither
page hand-rolls chrome any more. Documentation uses the new search metadata, sidebar icon policy,
content primitives, and assistant page actions. Release rows stay text-only:
no `images` cascade is set on the blog tree, so nothing resolves a featured
image and `params.ui.featured_image` has nothing to render.

The local layout surface is intentionally small:

- `layouts/index.html` and `layouts/download/landing.html` are the two bespoke
  page bodies. Each is a `{{ define "main" }}` block inside OINK's landing
  shell, so the navbar, footer, search, and scripts are the theme's. The only
  site partial they carry is `pig/hero-diagram.html`, the home page's inline
  SVG. `content/download.md` sets `layout: landing` so the landing base
  template applies and the navbar keeps its search box.
- `layouts/_partials/hooks/head-end.html` and `body-end.html` load
  `landing-v3.css` / `pig-v3.css` / `download.css` / `fonts.css` and
  `landing-v3.js` (plus `download.js`) on the home and download pages only.
  Every other page gets the theme bundle and nothing else.
- The landing stylesheets carry a short "shell seam" block. OINK gives every
  `section` inside `main` a 5rem block padding (`.td-default main section`,
  specificity `0,1,2`), which outranks the landing's own `.hero` /
  `.landing-section` rules. The fix is not a blanket reset — that would erase
  the landing's rhythm too — but a `.landing-page` prefix on the handful of
  rules that set section padding, since two classes outrank one class plus two
  elements. The first section is special-cased through the
  `--pig-section-pad-top` custom property so its value is still declared once.
- `data/footer/<lang>.yaml` drives OINK's fat footer, and the copyright line
  comes from each language's `params.copyright.authors` (rendered as Markdown).
  ICP filings, if ever needed, belong in `params.footer_center_info`.
- The home page cascade targets `kind: '{page,section}'` on purpose. Taxonomy
  and term pages are descendants of home too, and colouring them `type: docs`
  would route them to OINK's `docs/list.html` instead of the term layout that
  renders the author profile and the blog rows.
- `layouts/index.md` and `layouts/index.llms.txt` index PIG's intentionally
  root-level documents; the generic OINK indexes assume documents live below
  `/docs/`.
- `params.ui.docs_sidebar_root: home` keeps root-level documentation rooted at
  `Site.Home`; `/docs/` remains an overview rather than a content container.
- OINK renders the `sidebar_divider` grouping row; the project stylesheet only
  applies PIG's visual treatment to that theme-owned semantic row.
- the favicon, robots, and math render-hook files contain site policy rather
  than theme chrome.

Do not copy OINK layouts, blocks, or assets into this repository for ordinary
customization. Prefer OINK configuration and upstream generic theme changes;
keep local overrides limited to PIG-specific behavior.

## Local development

Install Hugo Extended 0.160.1 or newer, Go, and Git. OINK vendors its runtime
assets, so this site does not require Node.js, npm, or a CDN.

Debug against the latest sibling OINK checkout with an inline Hugo Module
replacement (no Go workspace file is created):

```bash
make d
```

Serve or build with the theme version pinned in `go.mod` using:

```bash
make s
make b
```

Run module verification, the warning-strict production build, Markdown
hygiene checks, and internal-link validation with:

```bash
make c
```

The corresponding long targets are `debug`, `serve`, `build`, and `check`;
`make dev` uses the sibling OINK checkout while `make serve` retains the pinned-theme preview. Preview targets let Hugo choose an
available port unless `PORT` is set explicitly.

The production build also publishes Markdown copies for pages and sections,
printable section bundles under `/_print/`, bilingual `llms.txt` indexes, and
language-local search indexes consumed by the shared OINK command palette.

## Writing conventions

- Every page ships as an English `.md` / Chinese `.zh.md` pair with
  aligned content.
- Do not set `url:` in front matter — the file path already produces the
  intended URL. Chinese pages get the `/zh/` prefix automatically.
- In-site links are written as absolute paths: `/install/` in English pages,
  `/zh/install/` in Chinese pages.
- Links into the rest of the Pigsty manual are absolute and language-specific:
  `https://pigsty.io/...` for English and `https://pigsty.cc/...` for
  Chinese.
- Command transcripts are real executions against the current `pig` binary;
  do not invent output.
- Version numbers come from site params, not prose:
  `{{< param version >}}` is the `pig` version,
  `{{< param pigsty_version >}}` is the embedded Pigsty version, and
  `{{< param pgext_count >}}` is the packaged extension count. Keep them in
  sync with `internal/config/config.go` in the `pig` repository.

## License

The website content in this repository is licensed under the
[Creative Commons Attribution 4.0 International License](LICENSE) (CC BY 4.0).
