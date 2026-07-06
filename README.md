# WEB-Startr.Team

The Startr.Team site: the **agent framework specification** and its runnable
examples, served at <https://startr.team>.

The reference library lives in its own repo:
[`startr-team-py`](https://github.com/Startr/startr-team-py) (`pip install startr-team`).

## Layout

- `src/` — Eleventy input. `src/spec/*.md` are the spec's contract pages;
  `src/index.html` is the landing page.
- `examples/` — runnable agents (`hello_agent`, `herald`, `review_loop`).
  The spec's Examples page renders these files at build time — they are the
  source of truth, never copy-pasted snippets.
- `_site/` — build output (generated; not committed).

## Develop

```bash
npm install
npm run start        # live-reload dev server
npm run build        # build to _site/
make it_run          # same, via Startr.sh
make verify          # Makefile self-check
```

Styling is [startr.style](https://startr.style) from CDN, authored
**mobile-first**: base inline props are the phone layout; `-md`/`-lg`
suffixes only where the layout changes going up.

## Deploy

Docker (nginx serving `_site/`) via CapRover — `make deploy` — or Netlify
(`netlify.toml`). Releases follow git-flow via the Makefile
(`make minor_release`, `make release_finish`).

## License

Apache-2.0 — the spec text, the site, and the examples.
