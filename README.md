# PIG Documentation

This repository contains the bilingual website for **PIG** — *Packager Index
Gateway*, the PostgreSQL extension package manager by
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

## Theme boundary

OINK 0.2.0 owns the documentation and blog layouts, navigation shell, search, table
of contents, blocks and shortcodes, styles, scripts, fonts, and third-party
runtimes. The site imports a pinned OINK commit as a Hugo Module.

The local layout surface is intentionally small:

- `layouts/index.html` and its `pig/` partials preserve the custom PIG
  landing page.
- `layouts/index.md` and `layouts/index.llms.txt` index PIG's intentionally
  root-level documents; the generic OINK indexes assume documents live below
  `/docs/`.
- `layouts/_partials/shell/sidebar.html` keeps root-level documentation
  rooted at `Site.Home`; `/docs/` remains an overview rather than a content
  container.
- `layouts/_partials/shell/sidebar-tree.html` adds the PIG-specific
  `sidebar_divider` grouping row.
- the favicon, robots, and math render-hook files contain site policy rather
  than theme chrome.

Do not copy OINK layouts, blocks, or assets into this repository for ordinary
customization. Prefer OINK configuration and upstream generic theme changes;
keep local overrides limited to PIG-specific behavior.

## Local development

Install Hugo Extended 0.160.1 or newer, Go, and Git. OINK vendors its runtime
assets, so this site does not require Node.js, npm, or a CDN.

Debug against the latest sibling OINK checkout with an ignored Go workspace:

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
`make dev` retains the pinned-theme preview. Preview targets let Hugo choose an
available port unless `PORT` is set explicitly.

The production build also publishes Markdown copies for pages and sections,
printable section bundles under `/_print/`, and bilingual `llms.txt` indexes.
These outputs come from OINK; the landing-page JSON output remains the source
for PIG's custom command-palette search.

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
