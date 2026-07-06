# WEB-Startr.Team

Eleventy static site hosting the **Startr.Team agent framework spec** and its
runnable examples. The reference library is a separate repo
(`~/Documents/Projects/GitHub/startr-team-py`) — spec pages here must stay
accurate to that library's actual interfaces; when the lib changes a contract,
update the matching `src/spec/*.md` page in the same change.

## Commands

- `npm run start` — dev server; `npm run build` — build to `_site/`
- `make verify` — Makefile self-check; `make deploy` — CapRover

## Conventions

- **Styling:** startr.style from CDN, inline props, **mobile-first** (base
  values = phone; `-md`/`-lg` overrides only where layout changes).
- **Spec pages** are markdown through `default.njk` (`layout: default` front
  matter). Each contract page states: interface verbatim, guarantees,
  extension seam. Markdown runs through Nunjucks — avoid literal `{%`/`{{`
  sequences in code samples.
- **Examples are source of truth:** `src/_data/examples.js` reads
  `examples/**` at build time; the Examples page renders those files. Never
  paste example code into pages.
- **Branches:** git-flow — `develop` working, `master` release. Releases via
  Makefile targets only.
- Code identifiers from the lib use `this`-style receivers — that is the
  documented house style (see `/spec/style/`), not a typo.
