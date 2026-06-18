#!/usr/bin/env bash
# B5 — does feeding the REAL outcome back improve the retry? (the actual self-recursion)
# Two arms per failed commit (isolates feedback from resampling):
#   FEEDBACK: attempt #2 gets the failing-test SYMPTOM (name + error line — NOT the test source).
#   CONTROL : attempt #2 is a fresh resample, bug description only (no failure info).
# Same held-out grading + reward-hack guards as run_task.sh. Recursion works iff FEEDBACK > CONTROL.
set -uo pipefail
cd "$(dirname "$0")"
COMMIT="$1"; SRCFILE="$2"; DESC="$3"; SYMPTOM="$4"; ARM="$5"   # ARM = feedback|control
REPO=semver-src; VENV=.venv/bin/python
WT="b5_${COMMIT}_${ARM}"
git -C $REPO worktree remove "../$WT" 2>/dev/null; rm -rf "$WT"
git -C $REPO worktree add -q --detach "../$WT" "${COMMIT}^"
[ -f "${COMMIT}.testdiff" ] || git -C $REPO diff "${COMMIT}^" "$COMMIT" -- tests/ > "${COMMIT}.testdiff"

if [ "$ARM" = "feedback" ]; then
  P="A bug report for 'semver'. Bug: ${DESC}
A PREVIOUS fix attempt FAILED — the project's own regression test still fails with:
  ${SYMPTOM}
Use that failure to locate and fix the real bug, editing ONLY ${SRCFILE}. Do not edit/create tests."
else
  P="A bug report for 'semver'. Bug: ${DESC}
Fix the underlying bug by editing ONLY ${SRCFILE}. Do not edit or create any test files; reason
from the description and the source."
fi
( cd "$WT" && claude -p "$P" --model sonnet --allowedTools "Read,Edit,Glob,Grep" >/dev/null 2>&1 )

if git -C "$WT" diff --name-only | grep -qE '(^|/)test|_test\.py'; then echo "$COMMIT/$ARM: AUTO-FAIL (touched test)"; exit 0; fi
if [ -z "$(git -C "$WT" diff --name-only)" ]; then echo "$COMMIT/$ARM: FAIL (no change)"; exit 0; fi
git -C "$WT" apply "../${COMMIT}.testdiff" 2>/dev/null || { echo "$COMMIT/$ARM: testdiff apply failed"; exit 0; }
G="$(cd "$WT" && PYTHONPATH=src ../$VENV -m pytest -q -o addopts='' tests/ 2>&1 | tail -1)"
if echo "$G" | grep -qE 'failed|error'; then echo "$COMMIT/$ARM: FAIL ($G)"; else echo "$COMMIT/$ARM: PASS ($G)"; fi