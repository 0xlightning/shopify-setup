# 04 — Docs: CLAUDE.md, README.md, architecture.md

## package.json scripts
```json
{
  "name": "{{PREFIX}}-theme",
  "version": "1.0.0",
  "description": "{{BRAND}} storefront — custom Shopify theme based on {{BASE_THEME}} v{{BASE_VERSION}}",
  "scripts": {
    "shopify": "shopify",
    "dev":  "shopify theme dev  --store={{STORE}}.myshopify.com --path theme",
    "pull": "shopify theme pull  --store={{STORE}}.myshopify.com --path theme",
    "push": "shopify theme push  --store={{STORE}}.myshopify.com --path theme",
    "list": "shopify theme list  --store={{STORE}}.myshopify.com",
    "lint": "shopify theme check --path theme"
  },
  "repository": { "type": "git", "url": "https://github.com/{{REPO}}.git" },
  "license": "ISC",
  "type": "commonjs",
  "devDependencies": { "@shopify/cli": "^3.93.2", "@shopify/theme": "^3.58.2" }
}
```
Change the store and repo URL **together** when cloning a project into a new one (we missed `repository.url` once).

## CLAUDE.md — what to keep / tailor
Start from `templates/CLAUDE.template.md`. Sections, in order:
1. **Current state banner** — base theme + version, "customised yet?", "`theme/AGENTS.md` is authoritative". New-code-only prefix rule (`{{PREFIX}}-*`), never rename base-theme classes.
2. Standards (Liquid guardrails, CSS naming, JS, schema limits: `range` ≤ 101 steps, `max` ≤ 9999), performance, a11y, SEO, responsive, security, commit convention.
3. **Context boundaries** (AI-owned / user-supervised / read-only) + file-change protocol.
4. **Design tokens — verified in the real theme** (grep the theme's styles-variables snippet, e.g. `theme/snippets/theme-styles-variables.liquid`). Never copy token names from another theme — naming differs between themes.
5. **Skills & references** table.
6. **Graphify** section — `python -m graphify` commands + "JS only" note.
7. Ambiguity protocol (stop and ask on brand questions) and version/date footer.

## README.md skeleton
Title + badges (version, base theme, repo) → knowledge-map table (architecture.md, CLAUDE.md, theme/AGENTS.md, GRAPH_REPORT.md, skills) → prerequisites → quick start (`npm install`, `shopify auth login --store=…`, `npm run pull`, `npm run dev`) → scripts table → workflow (dev → lint → push) → graphify section → **current state** table (don't list features that aren't in `theme/`).

## architecture.md — per-file 2-line descriptions
Goal: every file in `theme/` gets two lines: **(1) what it does, (2) where it is used / key dependency.** Verified, not guessed.

### Method that worked (≈5 min for ~500 files)
1. Count files: `for d in theme/*/; do echo "$d $(ls $d | wc -l)"; done`.
2. Spawn parallel agents, one per folder group (assets · snippets split in 2 · blocks · sections+templates+layout+config). Each must **read** the files (snippets/blocks have `{% doc %}`/schema headers) and **grep for usage** (`render 'name'`, `asset_url`, schema `blocks` lists), then write a markdown table to a scratch file:
   `| File | Description |` / `|:---|:---|` / `| \`name.ext\` | line 1 <br> line 2 |`, alphabetical, row count == `ls | wc -l`.
3. Locales (57 files): generate by script from a language-name map — one row per file, 2 lines each; don't hand-write.
4. Assemble with a script (tables + header + tree + constraints). Header: "Last verified <date> on branch <b>".
5. Run `python scripts/verify_architecture.py` (installed by `bootstrap.py`) — every section's rows must equal the folder's file count, no row may contain a stray `|`.

### Pitfalls
- A literal `|` inside a table cell (e.g. `` `| t` filter ``) breaks the row → reword ("the `t` filter") or escape `\|`.
- Sort order is ASCII (`-` sorts before `.`, so `x-group.json` comes before `x.liquid`) — fine, just consistent.
- Agents flag "dead"/unused blocks from static grep; blocks can still be added via `@theme` pickers → word it "unused by shipped templates (editor-only)", not "dead".
- Re-verify the "Critical Architecture Constraints" section against the new theme version by grep — layout rules (e.g. how the cart drawer sizes its scroll area), the add-to-cart component contract and the CSS variable naming convention can change between theme versions. Keep only constraints you confirmed in source.
- Don't describe features (price-2 block, marquee bar…) that live only in an old build.
