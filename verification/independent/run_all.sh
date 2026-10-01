#!/usr/bin/env bash
# Second implementation of the proof's checks (same author; see README).
# Written separately from the scripts in ../ (own census, graph encoding
# and LP rebuilds), working from the manuscript text.
# Requires Python 3.10+, pynauty, numpy, scipy (see ../../requirements.txt).
# The LP checks use floating-point HiGHS: corroboration, not exact proof.
# The exact certificates are replayed by ../replay.sh.
set -euo pipefail
cd "$(dirname "$0")"
PYTHON="${PYTHON:-python3}"  # needs 3.10+ with pynauty, numpy, scipy
out=$(mktemp -d)
trap 'rm -rf "$out" independent_census_*.json independent_hull_capacity.json' EXIT
run() { printf '\n=== %s ===\n' "$1"; "$PYTHON" "$1.py" | tee "$out/$2.out"; }
run check_lemma1_parity lemma1_parity
run check_pair_normal_forms pair_normal_forms
run check_section5_lp section5_lp
run check_disjoint_lp disjoint_lp
printf '\n=== independent_census (about 2 min) ===\n'
"$PYTHON" independent_census.py | tee "$out/independent_census.out"
run independent_hull_capacity independent_hull_capacity
"$PYTHON" aut_orders.py
# Optional, slow (brute-force 14-qubit lifts): python3 check_fibre_formula.py
# after independent_census.py; recorded output in expected/fibre_formula.out
"$PYTHON" recheck_37_classes.py ../s7_37_classes.json
for f in lemma1_parity pair_normal_forms section5_lp disjoint_lp independent_census independent_hull_capacity; do
  diff -q "$out/$f.out" "expected/$f.out" >/dev/null || { echo "MISMATCH: $f (see expected/$f.out)"; exit 1; }
done
echo; echo "INDEPENDENT CHECKS PASS"
