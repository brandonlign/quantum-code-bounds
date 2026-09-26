#!/usr/bin/env python3
"""Audit all 37 independently censused additive length-10 representatives.

The input is the JSON emitted by ``qec1435_n10_additive_lengthening_census.py``.
This script checks the codebook invariants again, computes the exact binary
trace-symplectic hull, applies the ambient four-deep-hole gate to every class,
and sends only hull-four classes through the exact physical-lift verifier.

The final result is a finite computational audit of the published
``(10, 2**10, >=5)_4`` class list.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from qec1435_n10_ambient_four_deep_hole_gate_exact import deep_holes
from qec1435_n10_full_physical_symplectic_lift_exact import (
    basis,
    check_code,
    nullspace,
    span,
    sym,
    wt,
)


N = 10
MASK = (1 << N) - 1


def weight_distribution(gens: list[int]) -> dict[str, int]:
    return {str(weight): count for weight, count in sorted(Counter(wt(v) for v in span(gens)).items())}


def hull_basis(gens: list[int]) -> list[int]:
    gram = [sum(sym(a, b) << j for j, b in enumerate(gens)) for a in gens]
    coefficients = nullspace(gram, N)
    hull = []
    for mask in coefficients:
        value = 0
        for j, generator in enumerate(gens):
            if mask >> j & 1:
                value ^= generator
        hull.append(value)
    return basis(hull)


def check_input(gens: list[int]) -> None:
    assert len(gens) == N
    assert all(isinstance(value, int) and 0 <= value < (1 << (2 * N)) for value in gens)
    assert len(basis(gens)) == N
    words = span(gens)
    assert len(words) == len(set(words)) == 1 << N
    assert min(wt(word) for word in words if word) >= 5


def audit(generators_path: Path) -> dict:
    records = json.loads(generators_path.read_text())
    assert isinstance(records, list) and len(records) == 37

    classes = []
    for index, gens in enumerate(records, start=1):
        check_input(gens)
        hull = hull_basis(gens)
        ambient = deep_holes(gens)
        result = {
            "class": index,
            "distance": min(wt(word) for word in span(gens) if word),
            "weight_distribution": weight_distribution(gens),
            "hull_dimension": len(hull),
            "ambient_four_deep_hole_gate": ambient,
        }
        if len(hull) == 4:
            result["physical_lift"] = check_code(gens)
        else:
            result["physical_lift"] = {
                "status": "NOT APPLICABLE: symplectic hull dimension is not 4"
            }
        classes.append(result)
        status = result["physical_lift"]["status"]
        print(
            f"class {index:02d}: hull={len(hull)} "
            f"ambient_deep_holes={ambient['distinct_C_cosets_min_distance_at_least_4']} "
            f"status={status}"
        )

    statuses = Counter(item["physical_lift"]["status"] for item in classes)
    hulls = Counter(item["hull_dimension"] for item in classes)
    ambient_gate = Counter(
        item["ambient_four_deep_hole_gate"]["four_deep_hole_necessary_gate"]
        for item in classes
    )
    return {
        "input": str(generators_path),
        "class_count": len(classes),
        "hull_dimension_counts": dict(sorted(hulls.items())),
        "ambient_four_deep_hole_gate_counts": {
            str(key).lower(): value for key, value in sorted(ambient_gate.items())
        },
        "physical_lift_status_counts": dict(sorted(statuses.items())),
        "classes": classes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generators",
        type=Path,
        default=Path("experiments/qec1435_n10_additive_37_generators_xy.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/qec1435_n10_additive_37_class_audit.json"),
    )
    args = parser.parse_args()
    result = audit(args.generators)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        f"EXACT 37-CLASS AUDIT PASS: {result['physical_lift_status_counts']}"
    )


if __name__ == "__main__":
    main()
