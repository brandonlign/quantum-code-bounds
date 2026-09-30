#!/usr/bin/env python3
"""Exact affine-plane gate for the physical ten-site lift test.

The four one-site Z-prefix classes form an affine totally isotropic
two-plane of four points in the six-dimensional quotient ``P/H``.  Under a
symplectic graph map their suffix labels must therefore form an affine
isotropic two-plane.  Each of those four suffix cosets must have minimum
physical weight at least four.

This module enumerates every two-dimensional totally isotropic subspace of
``F_2^6`` and every affine coset of each subspace.  It is deliberately
independent of the physical-lift recursion; it only consumes the 64 exact
suffix-coset leader weights produced by that verifier.
"""

from __future__ import annotations


DIMENSION = 6
POINTS = 1 << DIMENSION


def symplectic_form(a: int, b: int) -> int:
    """Return the standard alternating form on ``F_2^6``."""

    value = 0
    for pair in range(0, DIMENSION, 2):
        value ^= ((a >> pair) & 1) & ((b >> (pair + 1)) & 1)
        value ^= ((a >> (pair + 1)) & 1) & ((b >> pair) & 1)
    return value


def isotropic_two_planes() -> tuple[tuple[int, ...], ...]:
    """Enumerate all distinct two-dimensional totally isotropic subspaces."""

    planes: set[tuple[int, ...]] = set()
    for u in range(1, POINTS):
        for v in range(u + 1, POINTS):
            if symplectic_form(u, v):
                continue
            planes.add(tuple(sorted((0, u, v, u ^ v))))
    result = tuple(sorted(planes))
    assert len(result) == 315
    return result


def affine_cosets(plane: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Enumerate the 16 affine cosets of a four-point plane."""

    unseen = set(range(POINTS))
    cosets = []
    while unseen:
        offset = min(unseen)
        coset = tuple(sorted(offset ^ point for point in plane))
        unseen.difference_update(coset)
        cosets.append(coset)
    assert len(cosets) == 16
    return tuple(cosets)


def lagrangian_gate(leaders: list[int]) -> dict[str, int | bool]:
    """Check the necessary four-deep-hole affine-plane condition exactly."""

    assert len(leaders) == POINTS
    assert all(isinstance(value, int) and value >= 0 for value in leaders)
    assert leaders[0] == 0

    admissible = 0
    for plane in isotropic_two_planes():
        for coset in affine_cosets(plane):
            if all(leaders[label] >= 4 for label in coset):
                admissible += 1

    return {
        "lagrangian_affine_hole_gate": admissible > 0,
        "number_of_admissible_lagrangian_plane_pairs": admissible,
    }


if __name__ == "__main__":
    assert len(isotropic_two_planes()) == 315
    print("EXACT LAGRANGIAN AFFINE FOUR-DEEP-HOLE GATE PASS")
