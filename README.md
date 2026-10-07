# Shopify Setup Kit

Reusable starter for **any** Shopify theme project: Claude Code config, skills, standards, docs templates and a graphify setup — with a notes playbook explaining every choice. Contains no project-specific names; `bootstrap.py` fills the placeholders for a new project.

## Quick start (new theme project)
```bash
git clone https://github.com/0xlightning/shopify-setup.git
cd shopify-setup
python bootstrap.py ../my-theme --brand "Acme" --prefix acme --store acme-shop \
  --base-theme Dwell --base-version 4.2.0 --repo owner/acme-theme
cd ../my-theme
npm install
npm run pull            # after: npx shopify auth login --store=acme-shop.myshopify.com  → fills theme/
python scripts/verify_architecture.py   # after you write architecture.md
```
Then follow [01-new-theme-setup-checklist.md](./01-new-theme-setup-checklist.md) from step 6 (lint → graphify → docs → first commit/push). `bootstrap.py` never overwrites existing files; add `--force` to replace them.

## What the kit installs (`templates/` → project root)
| In the kit | In the new project | Notes |
|:---|:---|:---|
| `.claude/settings.json`, `settings.local.json` | same | Narrow allow-list; push/pull still prompt; no hooks |
| `.claude/skills/{Taste,codereview,ponytail}/` | same | `codereview` is named `theme-code-review`. Taste is third-party (React-oriented) — principles only |
| `CLAUDE.template.md` | `CLAUDE.md` | Rules, boundaries, tokens section, skills table, graphify rules |
| `references/*.md` | `references/` | On-demand standards. Starter values — verify CSS variable names against the base theme |
| `package.json` | `package.json` | Scripts bound to `{{STORE}}`, repo URL, Shopify CLI deps |
| `gitignore.template` | `.gitignore` | Stored under another name so it doesn't act as an ignore file inside this repo |
| `.graphifyignore`, `.editorconfig`, `.theme-check.yml` | same | |
| `verify_architecture.py` | `scripts/verify_architecture.py` | Row counts of `architecture.md` vs `theme/<dir>` |

## Playbook
| Read | When |
|:---|:---|
| [01-new-theme-setup-checklist.md](./01-new-theme-setup-checklist.md) | Day 0 of any new theme, in order |
| [02-claude-config.md](./02-claude-config.md) | Permissions, skills, hooks decision, audit checklist |
| [03-graphify-setup.md](./03-graphify-setup.md) | Code knowledge graph (JS only) |
| [04-docs-templates.md](./04-docs-templates.md) | CLAUDE/README/architecture docs, per-file 2-line descriptions |
| [05-lessons-learned.md](./05-lessons-learned.md) | Gotchas — skim before starting |

## Placeholders
`{{BRAND}}` project/brand name · `{{PREFIX}}` lowercase CSS prefix for new code · `{{STORE}}` store handle (before `.myshopify.com`) · `{{BASE_THEME}}` + `{{BASE_VERSION}}` (see `theme/config/settings_schema.json` → `theme_info`) · `{{REPO}}` `owner/repo` · `{{date}}` auto.
Real Liquid like `{{ section.id }}` (with spaces) is left untouched.

## Requirements
Node 20+, Git 2.40+, Python 3.10+ (`pip install graphifyy` for the graph), Claude Code. Shopify CLI comes from the project (`npm install`).

## Trust note
The skills in `templates/.claude/skills/` were read in full and scanned (no network calls, no hidden text). Re-audit anything you add — checklist in [02](./02-claude-config.md#audit-checklist-before-trusting-any-imported-claude-config--skill).
