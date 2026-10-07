# 02 — Claude Code configuration for a Shopify theme repo

## Layout
| Path | Committed? | Purpose |
|:---|:---|:---|
| `CLAUDE.md` | yes | Project rules (template: `templates/CLAUDE.template.md`, rendered by `bootstrap.py`). `claude.md` and `CLAUDE.md` are the same file on Windows. |
| `.claude/settings.json` | yes | Shared permissions (template: `templates/.claude/settings.json`). |
| `.claude/settings.local.json` | **no** (`.gitignore`) | Personal allow-rules. |
| `.claude/skills/<dir>/SKILL.md` | yes | Project skills. **Folder is `skills` (plural)** — `skill/` is silently ignored. |
| `theme/AGENTS.md` | yes (ships with theme) | Theme authoring contracts. CLAUDE.md defers to it. |

## Permissions — narrow allow-list
Broad rules (`Bash(git *)`, `Bash(npm run *)`) let Claude run any git command and any npm script **without a prompt**, including `git push --force` and `npm run push` (deploys to the live store). Use specific patterns:

```json
"permissions": { "allow": [
  "Bash(git status*)", "Bash(git diff*)", "Bash(git log*)", "Bash(git branch*)",
  "Bash(git add*)", "Bash(git commit*)",
  "Bash(npm run lint)", "Bash(npm run dev)", "Bash(npm run list)",
  "Bash(python -m graphify *)"
] }
```
- Leave **push / pull / `npm run push` / `npm run pull`** un-allowed so each one prompts.
- `settings.local.json` too: `{"permissions":{"allow":["Bash(npm run lint)"]}}`.
- The `"commands": {…}` block that older templates carry is not a documented Claude Code setting (inert). Omit it in new projects.

## Hooks — decision: don't install graphify hooks
`python -m graphify claude install` adds `PreToolUse` hooks that inject "MANDATORY: run graphify before grep/read" text into every Bash/Grep/Read/Glob call and tell subagents to repeat it. For a Liquid theme that is noise (the graph covers only JS) and it is instruction injection into context. Also on Windows the installed command is bare `graphify`, which is **not on PATH** → fix to `python -m graphify …` or just remove.
- If it was run: delete the `hooks` block from `.claude/settings.json`, delete `settings.json.graphify-bak`, keep/trim the `## graphify` section it appends to `CLAUDE.md` (rewrite commands as `python -m graphify`).

## Skills
- Frontmatter needs `name` + `description` (description decides auto-trigger). Optional: `allowed-tools`, `argument-hint`, `license`.
- Directory name can differ from the skill `name:`; invoke by the `name`.
- **Name collisions:** a project skill called `code-review` collides with the built-in `code-review`. Rename the `name:` (the kit's copy is `theme-code-review`).
- **Scope third-party skills in CLAUDE.md.** Example: a generic frontend-design skill may assume React/Next/Tailwind and `npm install` of UI kits — wrong for Liquid. CLAUDE.md should say "principles only; never add npm UI packages". Generic code-review skill (Python/PHP greps) needs a pointer to Liquid/schema standards.
- Plugin skills installed globally are namespaced `plugin:skill`, so they don't clash with project skills of the same base name.
- Skills are read at **session start** — restart / new session to see changes.

## Standards files (`references/`)
Optional on-demand docs (liquid, styling/a11y, templates, checklist) referenced from CLAUDE.md, not auto-loaded. Check their token names against the real theme before trusting them — standards copied from one theme often use another theme's variable names (e.g. `--spacing-*` vs `--gap-*`, single- vs double-dash). State "theme source wins on conflict" in CLAUDE.md.

## Audit checklist before trusting any imported Claude config / skill
1. Read every file fully (settings, hooks, skills, references, CLAUDE.md, AGENTS.md).
2. Grep: `curl|wget|Invoke-WebRequest|base64|atob|eval\(|powershell|bash -c|https?://|\.ssh|id_rsa|token|api[_-]?key|webhook|rm -rf|ignore (all )?(previous|prior)|do not (tell|mention|reveal)|silently|without (telling|asking)`.
3. Invisible Unicode + HTML comments:
```python
import os,re,unicodedata
for d,_,fs in os.walk('.claude'):
    for f in fs:
        p=os.path.join(d,f); s=open(p,encoding='utf8',errors='replace').read()
        inv=[c for c in s if unicodedata.category(c) in ('Cf','Co','Cn') or 0xE0000<=ord(c)<=0xE007F]
        print(p,'invisible=',len(inv),'comments=',len(re.findall(r'<!--.*?-->',s,re.S)))
```
4. For any hook: read the command's source (`graphify hook-guard` lives in `…/site-packages/graphify/cli.py`) — confirm local-only, no network, fails open.
5. Permissions: anything that can deploy, delete, or run arbitrary scripts must prompt.
Record the audit result (and date) in the project notes.
