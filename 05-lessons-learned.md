# 05 — Lessons learned

| # | Gotcha | Fix |
|:-:|:---|:---|
| 1 | `.claude/skill/` (singular) is not read by Claude Code | Use `.claude/skills/<dir>/SKILL.md`; restart session |
| 2 | Project skill named `code-review` collides with built-in | Rename `name:` (prefix with `{{PREFIX}}-`) |
| 3 | `graphify` not on PATH (Windows user-site Scripts) | Always `python -m graphify …`; fix any hook/CLAUDE text that says bare `graphify` |
| 4 | `graphify claude install` adds noisy mandatory-text hooks + edits settings | Remove hooks; keep graph and a CLAUDE.md section |
| 5 | graphify only parses JS/TS; Liquid/CSS/JSON invisible | Say so in CLAUDE.md; use `architecture.md` + grep for Liquid |
| 6 | Docs copied from an older build described features the new theme doesn't have | Rewrite "current state"; verify claims by grep |
| 7 | Token names copied from another theme were wrong for the current one | Verify in the theme's styles-variables snippet; state "theme source wins" |
| 8 | A pipe character inside a markdown table cell broke 34 rows (e.g. the Liquid filter written with a leading pipe) | Reword or escape as `\|`; run `verify_architecture.py` |
| 9 | `.gitignore` excluded `package-lock.json` | Commit the lockfile for reproducible `@shopify/cli` |
| 10 | `repository.url`/README badge still pointed at the old repo | Update with the remote at the same time |
| 11 | Broad allow rules (`Bash(git *)`, `Bash(npm run *)`) skip prompts for push/deploy | Specific patterns only (see 02) |
| 12 | Folders can be added/removed outside the session | Re-`ls` before editing docs that reference them |
| 13 | Global git identity differs from the Claude account email | Check `git config --global user.email` before the first commit |
| 14 | `json.dumps` turns the em dash into the 6-character text `\u2014` when rewriting JSON from Python | Use `ensure_ascii=False`, `newline='\n'` |
| 15 | Remote repo must be empty for a plain `push -u`; never force | `git ls-remote origin` first |
| 16 | `npm run lint` on an untouched stock theme gives a baseline | Record it; new code must not raise it |

## Working agreements that paid off
- Plan first (read-only), ask 2–3 sharp questions (store/repo, git init, permissions), then execute.
- Parallel agents for per-file docs; scripts for anything mechanical (locales, assembly, verification).
- Report anything not done as "not verified" (e.g. skills load after restart).
- Commit only when asked; leave untracked/uncommitted changes visible.
