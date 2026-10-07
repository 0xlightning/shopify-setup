"""Copy templates/ into a new Shopify theme project and fill the placeholders.

  python bootstrap.py <target-dir> --brand "Acme" --prefix acme --store acme-shop \
      --base-theme Dwell --base-version 4.2.0 --repo owner/acme-theme

Existing files are never overwritten (use --force). Prints any placeholders left to fill by hand.
"""
import argparse, datetime, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "templates")
RENAME = {  # template name -> name in the new project
    "CLAUDE.template.md": "CLAUDE.md",
    "gitignore.template": ".gitignore",
    "verify_architecture.py": os.path.join("scripts", "verify_architecture.py"),
}

sys.stdout.reconfigure(encoding="utf8")
ap = argparse.ArgumentParser()
ap.add_argument("target")
for k in ("brand", "prefix", "store", "base-theme", "base-version", "repo"):
    ap.add_argument("--" + k, required=True)
ap.add_argument("--force", action="store_true", help="overwrite existing files")
a = ap.parse_args()

vals = {"BRAND": a.brand, "PREFIX": a.prefix, "STORE": a.store, "BASE_THEME": a.base_theme,
        "BASE_VERSION": a.base_version, "REPO": a.repo, "date": datetime.date.today().isoformat()}
fill = lambda s: re.sub(r"\{\{(BRAND|PREFIX|STORE|BASE_THEME|BASE_VERSION|REPO|date)\}\}", lambda m: vals[m.group(1)], s)

os.makedirs(a.target, exist_ok=True)
written, skipped, left = 0, [], {}
for root, _, files in os.walk(SRC):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), SRC)
        rel = RENAME.get(rel, rel)
        dst = os.path.join(a.target, rel)
        if os.path.exists(dst) and not a.force:
            skipped.append(rel)
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        text = open(os.path.join(root, f), encoding="utf8", newline="").read()
        text = fill(text)
        open(dst, "w", encoding="utf8", newline="").write(text)
        written += 1
        found = set(re.findall(r"\{\{[A-Za-z_][\w-]*(?:[^{}\n]*)\}\}", text))  # Liquid like {{ x }} has a space after braces: not matched
        if found:
            left[rel] = sorted(found)

print(f"wrote {written} files to {a.target}")
if skipped:
    print("skipped (exist):", ", ".join(skipped))
for rel, ph in left.items():
    print(f"fill by hand in {rel}: {', '.join(ph)}")
