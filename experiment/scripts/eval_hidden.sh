#!/usr/bin/env bash
# Usage: eval_hidden.sh <git-ref> <issue-number>
# Runs the hidden acceptance tests for one issue against a ref of the fork, in a temp worktree.
set -euo pipefail
REF=$1; N=$2
HERE=$(cd "$(dirname "$0")/.." && pwd)            # experiment/
FORK=$(cd "$HERE/../fork" && pwd)
OUT="$HERE/../results/hidden"; mkdir -p "$OUT"
WT=$(mktemp -d)
git -C "$FORK" fetch -q origin "$REF" 2>/dev/null || true
git -C "$FORK" worktree add -q --detach "$WT" "$REF" 2>/dev/null || git -C "$FORK" worktree add -q --detach "$WT" "origin/$REF"
cp "$HERE/hidden_tests/issue-$N/"test_*.py "$WT/tests/"
SAFE=$(echo "$REF" | tr '/' '_')
( cd "$WT" && PYTHONPATH="$WT/src" "$FORK/.venv/bin/python" -m pytest -q "tests/test_hidden_issue$N.py" -p no:cacheprovider ) > "$OUT/issue$N-$SAFE.txt" 2>&1 && rc=0 || rc=$?
tail -1 "$OUT/issue$N-$SAFE.txt"
git -C "$FORK" worktree remove --force "$WT"
exit $rc
