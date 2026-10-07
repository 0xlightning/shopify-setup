# 01 — New Shopify theme project checklist

Do in order. Commands are for Git Bash / PowerShell on Windows; project root = folder containing `theme/`.

## A. Prerequisites
- [ ] Node 20+ (`node -v`), Git 2.40+, Python 3.10+ (graphify only; `pip install graphifyy`).
- [ ] Shopify CLI comes from the project (`npm install`), **not** global — run it with `npm run …` or `npx shopify`.
- [ ] Know: store domain (`xxx.myshopify.com`), GitHub repo URL, base theme name + version (check `theme/config/settings_schema.json` → `theme_info`).

## B. Repo skeleton
```text
<project>/
├── .claude/            settings.json, settings.local.json (git-ignored), skills/<name>/SKILL.md
├── notes/              (optional, personal; move out before sharing)
├── references/         (optional) standards read on demand
├── theme/              the Shopify theme (assets blocks config layout locales sections snippets templates [+ AGENTS.md])
├── .editorconfig  .gitignore  .graphifyignore  .theme-check.yml
├── CLAUDE.md  README.md  architecture.md
└── package.json
```

## C. Steps
1. **Get the theme into `theme/`** — `npm run pull` after login, or unzip a theme download. Count files per folder (`ls theme/<dir> | wc -l`); you need these for docs.
2. **Read `theme/AGENTS.md`** if present (modern Shopify themes ship one). It is the authority on Liquid/schema/component contracts; `CLAUDE.md` must point to it, not contradict it.
3. **Bootstrap the kit** (steps 3–5 in one command) from this repo's root:
   ```bash
   python bootstrap.py <project-dir> --brand "Acme" --prefix acme --store acme-shop \
     --base-theme Dwell --base-version 4.2.0 --repo owner/acme-theme
   ```
   It copies `templates/` into the project and fills placeholders: `package.json` (scripts, store, repo), `.gitignore`, `.editorconfig`, `.theme-check.yml`, `.graphifyignore`, `CLAUDE.md`, `references/`, `.claude/settings*.json`, `.claude/skills/`, `scripts/verify_architecture.py`. Never overwrites existing files. Then `npm install`.
4. **Fill what it lists** — any `{{…}}` the script reports (e.g. the CLAUDE.md "current state" line). Commit `package-lock.json` (do **not** ignore it).
5. **Claude config** — review [02-claude-config.md](./02-claude-config.md); permissions are already narrowed, skills already in `.claude/skills/`.
6. **Lint baseline** — `npm run lint`. Stock themes should report 0 offenses; record the number.
7. **Graphify** — [03-graphify-setup.md](./03-graphify-setup.md). JS only.
8. **Docs** — [04-docs-templates.md](./04-docs-templates.md): per-file `architecture.md`, `CLAUDE.md` from template, short `README.md`. Run `python scripts/verify_architecture.py`.
9. **Security look** — scan `.claude/`, `references/`, `CLAUDE.md` for `curl|wget|base64|eval|https?://|ignore previous|do not tell` and invisible Unicode before trusting any imported skill/config (see 02).
10. **First commit** (below). Check `git ls-files` for `node_modules`, `settings.local.json`, secrets.

## D. First commit + push
```bash
git init
git add -A
git status --short | head           # sanity: no node_modules, no settings.local.json, no graphify-out/cache
git commit -m "chore: initial commit — {{BASE_THEME}} v{{BASE_VERSION}} theme baseline"
git remote add origin https://github.com/{{REPO}}.git
git branch -M main
git ls-remote origin                # must print nothing (empty remote). If refs appear: STOP, never force-push
git push -u origin main
git ls-remote origin refs/heads/main   # hash must equal: git rev-parse HEAD
```
- Commit author = `git config --global user.name/email`. Check it is the identity you want **before** the first commit.
- CRLF→LF "warning: in the working copy" lines on Windows are harmless.
- No `gh` CLI needed; push uses Git Credential Manager. Never paste tokens into commands.

## E. Definition of done
- [ ] `npm run lint` clean · `git status` clean · remote hash == local HEAD
- [ ] `architecture.md` rows == files per folder
- [ ] `.claude/` permissions narrowed, skills in `skills/`
- [ ] Graph builds, `query` returns real theme files
