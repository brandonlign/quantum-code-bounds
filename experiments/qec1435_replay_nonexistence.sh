#!/usr/bin/env bash
# Exact replay for the nonexistence manuscript.
#
# Default mode uses the committed 37 representatives and does not rerun the
# memory-heavy lengthening census.  Pass --census to regenerate the 37-class
# representative JSON first.  This is separate from the historical monomial
# automorphism replay in qec1435_replay_core.sh.
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/.." && pwd)
cd "$repo_root"

# This proof replay is valid on main or at a detached, archived commit.
checkout_branch="$(git branch --show-current)"
printf 'Proof replay checkout: %s (%s)\n' "$(git rev-parse --short=12 HEAD)" "${checkout_branch:-detached HEAD}"

if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
  echo "ERROR: Python 3.10+ is required; found $(python3 --version 2>&1)" >&2
  exit 2
fi
if ! command -v node >/dev/null; then
  echo "ERROR: Node.js is required" >&2
  exit 2
fi

mode="committed"
if [[ "${1:-}" == "--census" ]]; then
  mode="census"
elif [[ $# -ne 0 ]]; then
  echo "Usage: bash experiments/qec1435_replay_nonexistence.sh [--census]" >&2
  exit 2
fi

run() {
  printf '\n=== %s ===\n' "$*"
  "$@"
}

# Stage I: original-physical shadows, subgroup cosets, and exact duals.
run python3 experiments/qec1435_shadow_lowweight_unconditional_exact.py
run python3 experiments/qec1435_shadow_parity_certificate.py
run node experiments/qec1435_shadow_parity_independent.mjs
run python3 experiments/qec1435_order2_weight2_split_shadow_exact.py
run node experiments/qec1435_order2_weight2_split_shadow_bigint_independent.mjs
run python3 experiments/qec1435_weight3_split_shadow_exact.py
run node experiments/qec1435_weight3_split_shadow_bigint_audit.mjs
run python3 experiments/qec1435_order2_m4_bell_split_shadow_exact.py
run node experiments/qec1435_order2_m4_bell_split_shadow_bigint_independent.mjs
run node experiments/qec1435_weight4_fivesite_triangle_split_shadow_bigint_exact.mjs
run python3 experiments/qec1435_triangle_sixsite_split_shadow_exact.py
run node experiments/qec1435_triangle_sixsite_bigint_audit.mjs
run python3 experiments/qec1435_crossed_bell_sixsite_split_shadow_exact.py
run node experiments/qec1435_crossed_bell_sixsite_bigint_audit.mjs
run node experiments/qec1435_weight4_five_support_types_exact.mjs
run python3 experiments/qec1435_sparse_h4_rank3_four_exact.py
run node experiments/qec1435_sparse_h4_rank3_four_bigint_independent.mjs
run python3 experiments/qec1435_disjoint_fourblock_shadow_exact.py
run node experiments/qec1435_disjoint_fourblock_shadow_independent.mjs
run node experiments/qec1435_disjoint_fourblock_shadow_bigint_independent.mjs

# Stage II: the onto graph reduction and the exact physical control path.
run python3 experiments/qec1435_singlecheck_tenqubit_controls_exact.py
run python3 experiments/qec1435_singlecheck_n10_min72_weightfive_exact.py
run python3 experiments/qec1435_n10_full_physical_symplectic_lift_exact.py
run node experiments/qec1435_n10_additive_37_hull_hall_independent.mjs
run node experiments/qec1435_n10_additive_37_js_independent_audit.mjs

if [[ "$mode" == "census" ]]; then
  run python3 experiments/qec1435_n10_additive_lengthening_census.py \
    --write-generators experiments/qec1435_n10_additive_37_generators_xy.json
fi

# Stage III: exact class-level hull and physical Hall audit.
run python3 experiments/qec1435_n10_additive_37_class_audit.py \
  --generators experiments/qec1435_n10_additive_37_generators_xy.json \
  --output experiments/qec1435_n10_additive_37_class_audit.json

python3 - <<'PY'
import json

with open("experiments/qec1435_n10_additive_37_class_audit.json") as handle:
    result = json.load(handle)

assert result["class_count"] == 37
assert result["hull_dimension_counts"] == {"0": 7, "2": 14, "4": 12, "6": 2, "8": 2}
assert result["physical_lift_status_counts"] == {
    "NO LIFT: EXACT 64-CLASS HALL NECESSITY": 12,
    "NOT APPLICABLE: symplectic hull dimension is not 4": 25,
}
print("37 target classes; hull dimensions {0:7, 2:14, 4:12, 6:2, 8:2}")
print("12 hull-four classes; all 12 fail the exact 64-class Hall necessity")
print("NONEXISTENCE CORE REPLAY PASS")
PY
