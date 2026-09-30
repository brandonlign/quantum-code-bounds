#!/usr/bin/env bash
# Exact replay for the nonexistence manuscript.
#
# Default mode uses the committed 37 representatives and does not rerun the
# lengthening census. Pass --census to regenerate representatives in a
# temporary directory before checking the same class-level exclusions.
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
if [[ $# -eq 0 ]]; then
  :
elif [[ $# -eq 1 && "$1" == "--census" ]]; then
  mode="census"
else
  echo "Usage: bash verification/replay.sh [--census]" >&2
  exit 2
fi

# Keep replay outputs out of the tracked certificate and representative data.
scratch_dir=$(mktemp -d)
trap 'rm -rf "$scratch_dir"' EXIT
audit_path="$scratch_dir/s7_class_audit.json"
generators_path="verification/s7_37_classes.json"

run() {
  printf '\n=== %s ===\n' "$*"
  "$@"
}

# Stage I: original-physical shadows, subgroup cosets, and exact duals.
run python3 verification/s4_low_weight_bound.py
run python3 verification/s4_shadow_parity.py
run node verification/s4_shadow_parity.mjs
run python3 verification/s5_3_weight_two.py
run node verification/s5_3_weight_two.mjs
run python3 verification/s5_4_weight_three.py
run node verification/s5_4_weight_three.mjs
run python3 verification/s5_4_bell.py
run node verification/s5_4_bell.mjs
run node verification/s5_4_five_site.mjs
run python3 verification/s5_4_six_site_same_letter.py
run node verification/s5_4_six_site_same_letter.mjs
run python3 verification/s5_4_six_site_crossed.py
run node verification/s5_4_six_site_crossed.mjs
run node verification/s5_5_support_geometries.mjs
run python3 verification/s5_6_rank_three.py
run node verification/s5_6_rank_three.mjs
run python3 verification/s5_7_disjoint.py
run node verification/s5_7_disjoint.mjs
run node verification/s5_7_disjoint_bigint.mjs

# Stage II: the onto graph reduction and the exact physical control path.
run python3 verification/s6_controls.py
run python3 verification/s6_weight_five_bound.py
run python3 verification/s6_lift_test.py
run node verification/s7_hull_capacity.mjs
run node verification/s7_class_audit.mjs

if [[ "$mode" == "census" ]]; then
  generators_path="$scratch_dir/s7_37_classes.json"
  run python3 verification/s7_census.py \
    --write-generators "$generators_path"
fi

# Stage III: exact class-level hull and coset-capacity audit.
run python3 verification/s7_class_audit.py \
  --generators "$generators_path" \
  --output "$audit_path"

python3 - "$audit_path" <<'PY'
import json
import sys

with open(sys.argv[1]) as handle:
    result = json.load(handle)

assert result["class_count"] == 37
assert result["hull_dimension_counts"] == {"0": 7, "2": 14, "4": 12, "6": 2, "8": 2}
assert result["physical_lift_status_counts"] == {
    "NO LIFT: COSET-CAPACITY BOUND FAILS": 12,
    "NOT APPLICABLE: symplectic hull dimension is not 4": 25,
}
print("37 target classes; hull dimensions {0:7, 2:14, 4:12, 6:2, 8:2}")
print("12 hull-four classes; all 12 fail the coset-capacity bound")
print("NONEXISTENCE CORE REPLAY PASS")
PY
