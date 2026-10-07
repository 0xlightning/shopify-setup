# 03 — graphify (code knowledge graph) for a Shopify theme

graphify (`pip install graphifyy`, tested 0.9.30) parses code locally into `graphify-out/graph.json` so you can query "who depends on X" instead of grepping. **Code-only mode needs no API key.**

## Hard facts for Shopify themes
- Indexes **JS/TS only**. `.liquid`, `.css`, `.json`, `.svg` are *unclassified* and skipped. Expect the graph to come almost entirely from `theme/assets/`.
- Files named like `password*.liquid/json` are skipped as "potentially sensitive". Settings JSON yields zero nodes (warning is harmless).
- The command is **not on PATH** on this Windows setup → always `python -m graphify …`, from the project root.
- Not a git repo → no "built from commit" stamp; it appears after `git init`+commit and a rebuild (that rebuild is a new uncommitted change — optional).

## Setup
```bash
pip install graphifyy                                   # once per machine
python -m graphify install --platform claude            # optional: installs /graphify skill to ~/.claude/skills/graphify
```
Create `.graphifyignore` (gitignore syntax) — see `templates/.graphifyignore` (installed by `bootstrap.py`):
```
node_modules/
*.zip
references/
.claude/skills/
package-lock.json
theme/locales/
theme/config/settings_data.json
```
Build:
```bash
python -m graphify extract . --code-only --out . && python -m graphify cluster-only . --no-label
```
`--no-label` skips the only step that would call an LLM (community names stay `Community N`).

Outputs in `graphify-out/`: `graph.json`, `GRAPH_REPORT.md`, `graph.html`, `manifest.json`, `cache/`, `.graphify_*`. Commit all **except `cache/`** (machine-local stamps) — add `graphify-out/cache/` to `.gitignore`.

## Everyday commands
```bash
python -m graphify query "<question about a feature>"       # BFS; --dfs deep path; --budget 1500 cap tokens
python -m graphify explain "<NodeName>"                       # node + neighbours
python -m graphify path "<NodeA>" "<NodeB>"                    # shortest link
python -m graphify affected "<file.js>"                      # blast radius BEFORE editing a hub
python -m graphify god-nodes --top 10                        # the most connected nodes (hubs)
python -m graphify check-update .                            # is a re-read pending?
python -m graphify update .                                  # after normal edits (changed files only)
python -m graphify extract . --code-only --out . && python -m graphify cluster-only . --no-label   # after refactors/renames/deletions
```
- `update` refusing because the graph shrank → `--force` once you know code really shrank.
- Habit: `query` → open only that snippet → edit → `update .`.

## Do NOT
- Run `python -m graphify claude install` unless you want hooks (see 02 — we removed them). If run, it also appends a `## graphify` section to CLAUDE.md and edits `.claude/settings.json`.
- Expect answers about Liquid/CSS from the graph — use `architecture.md` + grep.
