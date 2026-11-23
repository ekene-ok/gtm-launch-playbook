#!/usr/bin/env bash
# Create the program's milestones and issues from project/backlog.csv using the GitHub CLI.
# Then add the issues to a GitHub Projects board grouped by milestone.
# Usage: bash project/create_board.sh <owner/repo>
set -euo pipefail
REPO="$1"
python3 - "$REPO" <<'PY'
import csv, subprocess, sys
repo = sys.argv[1]
rows = list(csv.DictReader(open("project/backlog.csv")))
def gh(*a):
    return subprocess.run(["gh", *a], check=True, capture_output=True, text=True).stdout
for m in dict.fromkeys(r["milestone"] for r in rows):
    gh("api", f"repos/{repo}/milestones", "-f", f"title={m}")
labels = {l for r in rows for l in r["labels"].split(";")}
for l in labels:
    subprocess.run(["gh", "label", "create", l, "-R", repo, "--force"], capture_output=True)
for r in rows:
    body = f"{r['body']}\n\nWorkstream: {r['workstream']}\nOwner: {r['owner']}"
    args = ["issue", "create", "-R", repo, "-t", r["title"], "-b", body, "-m", r["milestone"]]
    for l in r["labels"].split(";"):
        args += ["-l", l]
    print(gh(*args).strip())
PY
