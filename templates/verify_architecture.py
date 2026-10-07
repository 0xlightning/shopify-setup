"""Check architecture.md against the theme folder.

Run from the project root:  python notes/templates/verify_architecture.py [architecture.md] [theme]
Each section heading must look like:  ## <emoji> /assets (125 files — ...)
Fails if a section's table rows != files in theme/<dir>, or a row has a stray '|'.
"""
import os, re, sys

doc = sys.argv[1] if len(sys.argv) > 1 else "architecture.md"
theme = sys.argv[2] if len(sys.argv) > 2 else "theme"
text = open(doc, encoding="utf8").read()
parts = re.split(r"^## (.*)$", text, flags=re.M)  # [pre, head1, body1, head2, body2, ...]
bad = 0
seen = set()
for head, body in zip(parts[1::2], parts[2::2]):
    m = re.search(r"/(\w+)\s*\(", head)
    if not m or not os.path.isdir(os.path.join(theme, m.group(1))):
        continue
    d = m.group(1)
    seen.add(d)
    rows = [l for l in body.splitlines() if l.startswith("| `")]
    n = len(os.listdir(os.path.join(theme, d)))
    stray = [l[:60] for l in rows if l.replace("\\|", "").count("|") != 3]
    ok = len(rows) == n and not stray
    bad += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {d:10} rows={len(rows):4} files={n:4}", *(["stray pipes:"] + stray[:3] if stray else []))
missing = [d for d in sorted(os.listdir(theme)) if os.path.isdir(os.path.join(theme, d)) and d not in seen]
if missing:
    print("WARN no section for:", ", ".join(missing))
sys.exit(1 if bad else 0)
