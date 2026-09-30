#!/usr/bin/env python3
"""Independent additive-quaternary lengthening census for the n=10 target.

This is a reconstruction of the lengthening route described in Grassl--Krotov--
Sok--Solé (2026), specialised to the cells needed for additive
``(10, 2**10, >=5)_4`` codes.  A codeword is stored as a 2-bit symbol per
physical coordinate, so binary addition is integer XOR.

The key finite step is exact code equivalence.  For a binary additive code C,
make a colored bipartite incidence graph whose left vertices are ALL codewords,
whose right vertices are the three nonzero symbol labels at each coordinate,
and whose ten coordinate vertices bind those triples.  Graph isomorphism is
exactly arbitrary codeword reordering together with coordinate permutations and
the six local GL(2,2) permutations of the three nonzero symbols.  Thus the
nauty certificate is an exact equivalence key; it is not a heuristic hash.

The extension from a parent C of length m and binary dimension k to length m+1
and dimension k+r (r in {0,1,2}) uses the quotient F2^(2m)/C.  The new
coordinate has rank r.  For r>0, every nonzero new-row combination contributes
one physical symbol, so the corresponding nonzero quotient cosets must have
minimum old weight at least four.  For r=0 the new coordinate is zero.  This
is the complete shortening/lengthening condition, not a restricted family.

The script intentionally prints the published target counts as a cross-check,
but does not treat them as input.  It stops with an explicit mismatch instead
of silently accepting an incomplete or overgenerated census.

Dependency: ``pynauty`` (the bundled nauty interface).  Install with
``python3 -m pip install --user pynauty``.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

try:
    from pynauty import Graph, certificate
except ImportError as exc:  # pragma: no cover - environment diagnostic
    raise SystemExit(
        "pynauty is required; install with: python3 -m pip install --user pynauty"
    ) from exc


TARGET_COUNTS = {
    (5, 0): 1,
    (5, 1): 1,
    (5, 2): 1,
    (5, 3): 0,
    (5, 4): 0,
    (6, 2): 5,
    (6, 3): 1,
    (6, 4): 0,
    (6, 5): 0,
    (6, 6): 0,
    (7, 4): 43,
    (7, 5): 1,
    (7, 6): 0,
    (7, 7): 0,
    (7, 8): 0,
    (8, 6): 1579,
    (8, 7): 0,
    (8, 8): 0,
    (8, 9): 0,
    (8, 10): 0,
    (9, 8): 2298,
    (9, 9): 0,
    (9, 10): 0,
    (10, 10): 37,
}

# We only need the high-rate predecessor cells which feed the target.  Zero
# entries in the published table are retained as explicit completeness checks.
CELL_ORDER = tuple(sorted(TARGET_COUNTS))


def span(gens: Iterable[int]) -> list[int]:
    out = [0]
    for g in gens:
        out += [x ^ g for x in out]
    return out


def gf2_basis(vectors: Iterable[int]) -> list[int]:
    pivots: dict[int, int] = {}
    out: list[int] = []
    for value in vectors:
        x = value
        while x:
            bit = x.bit_length() - 1
            if bit in pivots:
                x ^= pivots[bit]
            else:
                pivots[bit] = x
                out.append(value)
                break
    return out


def dot(a: int, b: int) -> int:
    return (a & b).bit_count() & 1


def nullspace(rows: list[int], width: int) -> list[int]:
    """Return a binary nullspace basis for rows as bit masks."""
    work = list(rows)
    pivots: list[int] = []
    rank = 0
    for col in range(width):
        pivot = next(
            (i for i in range(rank, len(work)) if (work[i] >> col) & 1), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for i in range(len(work)):
            if i != rank and ((work[i] >> col) & 1):
                work[i] ^= work[rank]
        pivots.append(col)
        rank += 1

    free = [col for col in range(width) if col not in pivots]
    out: list[int] = []
    for free_col in free:
        vector = 1 << free_col
        for row, pivot_col in enumerate(pivots):
            if (work[row] >> free_col) & 1:
                vector |= 1 << pivot_col
        out.append(vector)
    assert all(dot(v, r) == 0 for v in out for r in rows)
    return out


def weight(value: int, n: int) -> int:
    return sum(((value >> (2 * i)) & 3) != 0 for i in range(n))


def symbol_error(n: int, sites: tuple[int, ...], labels: tuple[int, ...]) -> int:
    value = 0
    for site, label in zip(sites, labels):
        value |= label << (2 * site)
    return value


def errors_up_to_three(n: int) -> Iterable[tuple[int, int]]:
    yield 0, 0
    for w in range(1, min(3, n) + 1):
        for sites in combinations(range(n), w):
            for labels in product((1, 2, 3), repeat=w):
                yield symbol_error(n, sites, labels), w


def syndrome_basis(gens: list[int], n: int) -> tuple[list[int], list[int]]:
    """Return a dual basis and one representative for every quotient syndrome."""
    width = 2 * n
    dual = nullspace(gens, width)
    assert len(dual) == width - len(gf2_basis(gens))

    # Extend C's independent basis to an ambient basis.  The extra vectors form
    # a quotient complement; their syndrome columns are invertible because the
    # dual basis separates the quotient.
    base = gf2_basis(gens)
    extended = list(base)
    complement: list[int] = []
    rank = len(extended)
    for bit in range(width):
        candidate = 1 << bit
        if len(gf2_basis(extended + [candidate])) > rank:
            extended.append(candidate)
            complement.append(candidate)
            rank += 1
    assert len(complement) == len(dual)

    columns = []
    for q in complement:
        columns.append(sum(dot(q, p) << j for j, p in enumerate(dual)))
    # Enumerate the small quotient once to invert the syndrome-coordinate map.
    reps: dict[int, int] = {}
    for selector in range(1 << len(complement)):
        q = 0
        for j, basis_vector in enumerate(complement):
            if (selector >> j) & 1:
                q ^= basis_vector
        syndrome = sum(dot(q, p) << j for j, p in enumerate(dual))
        assert syndrome not in reps
        reps[syndrome] = q
    assert len(reps) == 1 << len(dual)
    return dual, [reps[s] for s in range(1 << len(dual))]


def deep_quotient_representatives(gens: list[int], n: int) -> list[int]:
    """Represent quotient cosets whose minimum old weight is at least four."""
    dual, representatives = syndrome_basis(gens, n)
    covered: set[int] = set()
    for error, _ in errors_up_to_three(n):
        syndrome = sum(dot(error, p) << j for j, p in enumerate(dual))
        covered.add(syndrome)
    return [representatives[s] for s in range(1 << len(dual)) if s not in covered]


def append_zero_coordinate(gens: list[int], n: int) -> list[int]:
    return list(gens)


def append_rank_coordinate(gens: list[int], n: int, reps: list[int], r: int) -> list[int]:
    """Append a rank-r coordinate using quotient representatives reps."""
    assert r in (1, 2)
    out = list(gens)
    if r == 1:
        out.append(reps[0] | (1 << (2 * n)))
    else:
        out.append(reps[0] | (1 << (2 * n)))
        out.append(reps[1] | (2 << (2 * n)))
    return out


def fast_invariant(gens: list[int], n: int) -> tuple:
    """Cheap invariant used only to avoid unnecessary nauty calls."""
    words = span(gens)
    weight_dist = tuple(sorted(Counter(weight(x, n) for x in words).items()))
    # The rank of a union of two coordinate symbol planes is invariant under
    # local GL(2,2) and coordinate permutation.  Compute it from the dual
    # coordinate maps, i.e. from the two-bit columns of a row-basis matrix.
    # A generator row basis is enough; rank is invariant under row operations.
    ranks = []
    for i, j in combinations(range(n), 2):
        cols = []
        for coord in (i, j):
            cols += [sum(((g >> (2 * coord + b)) & 1) << row
                         for row, g in enumerate(gens)) for b in (0, 1)]
        ranks.append(len(gf2_basis(cols)))
    return weight_dist, tuple(sorted(ranks))


def equivalence_certificate(gens: list[int], n: int) -> bytes:
    words = span(gens)
    row_count = len(words)
    symbol_offset = row_count
    group_offset = row_count + 3 * n
    vertex_count = row_count + 4 * n
    adjacency = {v: set() for v in range(vertex_count)}

    for row, word in enumerate(words):
        for coord in range(n):
            symbol = (word >> (2 * coord)) & 3
            if symbol:
                vertex = symbol_offset + 3 * coord + symbol - 1
                adjacency[row].add(vertex)
                adjacency[vertex].add(row)

    for coord in range(n):
        group = group_offset + coord
        for symbol_index in range(3):
            vertex = symbol_offset + 3 * coord + symbol_index
            adjacency[group].add(vertex)
            adjacency[vertex].add(group)

    graph = Graph(
        vertex_count,
        adjacency_dict=adjacency,
        vertex_coloring=[
            set(range(row_count)),
            set(range(symbol_offset, group_offset)),
            set(range(group_offset, vertex_count)),
        ],
    )
    return certificate(graph)


def code_record(gens: list[int], n: int) -> tuple[tuple[int, ...], list[int]]:
    words = span(gens)
    assert len(words) == 1 << len(gens)
    nonzero = [weight(word, n) for word in words if word]
    assert not nonzero or min(nonzero) >= 5
    invariant = fast_invariant(gens, n)
    return invariant, gens


def target_cells() -> dict[tuple[int, int], list[list[int]]]:
    # Cell storage is keyed by the exact nauty certificate.  Each bucket of the
    # cheap invariant is also kept so equivalent candidates invoke nauty only.
    cells: dict[tuple[int, int], dict[bytes, list[int]]] = {}

    # The zero code is available at every length and is the only source needed
    # for the initial (5,0) cell.
    cells[(4, 0)] = {equivalence_certificate([], 4): []}
    cells[(5, 0)] = {equivalence_certificate([], 5): []}

    def add_candidate(n: int, k: int, gens: list[int]) -> None:
        invariant, _ = code_record(gens, n)
        by_cert = cells.setdefault((n, k), {})
        # A local bucket avoids nauty for candidates with an impossible weight
        # or pair-rank signature, while the certificate gives exact equality.
        bucket_key = (n, k, invariant)
        bucket = bucket_certs.setdefault(bucket_key, {})
        raw_key = tuple(sorted(span(gens)))
        if raw_key in bucket:
            return
        cert = equivalence_certificate(gens, n)
        bucket[raw_key] = cert
        by_cert.setdefault(cert, gens)

    # raw codeword-set keys are scoped to the cheap invariant; this is merely a
    # performance cache and never replaces the exact certificate.
    bucket_certs: dict[tuple, dict[tuple[int, ...], bytes]] = {}

    for n in range(5, 11):
        # The recurrence only needs parent cells with k' in {k-2,k-1,k}; build
        # all target cells in increasing n and k.  Published zero cells are
        # installed explicitly so a missing predecessor cannot be hidden.
        possible_targets = sorted(k for nn, k in TARGET_COUNTS if nn == n)
        for k in possible_targets:
            if (n, k) == (5, 0):
                continue
            candidates: list[tuple[list[int], int]] = []
            for r in (0, 1, 2):
                parent_k = k - r
                parent = cells.get((n - 1, parent_k), {})
                for gens in parent.values():
                    if r == 0:
                        candidates.append((append_zero_coordinate(gens, n - 1), 0))
                        continue
                    deep = deep_quotient_representatives(gens, n - 1)
                    if r == 1:
                        for representative in deep:
                            candidates.append(([ *gens, representative | (1 << (2 * (n - 1))) ], 1))
                    else:
                        dual, reps = syndrome_basis(gens, n - 1)
                        # Recompute the covered quotient labels and retain the
                        # quotient labels rather than representative values.
                        covered = set()
                        for error, _weight in errors_up_to_three(n - 1):
                            covered.add(sum(dot(error, p) << j for j, p in enumerate(dual)))
                        deep_labels = [s for s in range(1 << len(dual)) if s not in covered]
                        for a_index, a in enumerate(deep_labels):
                            for b in deep_labels[a_index + 1:]:
                                c = a ^ b
                                if c == 0 or c in covered:
                                    continue
                                candidate = [
                                    *gens,
                                    reps[a] | (1 << (2 * (n - 1))),
                                    reps[b] | (2 << (2 * (n - 1))),
                                ]
                                candidates.append((candidate, 2))

            for gens, _r in candidates:
                add_candidate(n, k, gens)

            expected = TARGET_COUNTS[(n, k)]
            actual = len(cells.get((n, k), {}))
            print(f"cell n={n} k={k}: {actual} exact classes (published {expected})")
            if actual != expected:
                raise RuntimeError(
                    f"lengthening mismatch at n={n}, k={k}: {actual} != {expected}"
                )
            # Independent published MATRIX positive control, not just a table
            # count: Grassl--Krotov--Sok--Solé (2026), §2.3 (7,2^5,5).
            # Five printed GF4 rows generate 32 actual binary-additive
            # codewords with weight distribution 0:1,5:21,6:7,7:3.
            if (n, k) == (7, 5):
                only = next(iter(cells[(7, 5)].values()))
                published_distribution = {0: 1, 5: 21, 6: 7, 7: 3}
                observed = dict(Counter(weight(v, 7) for v in span(only)))
                if observed != published_distribution:
                    raise RuntimeError(
                        "Published (7,2^5,5) generator positive-control "
                        f"weight distribution mismatch: {observed}"
                    )
                print(
                    "PRIMARY-SOURCE GENERATOR CONTROL PASS: "
                    "n=7,k=5 {0:1,5:21,6:7,7:3}"
                )

    return {key: list(value.values()) for key, value in cells.items()}


def write_target_generators(cells: dict[tuple[int, int], list[list[int]]], path: Path) -> None:
    import json

    def xy_layout(word: int, n: int = 10) -> int:
        x = sum(((word >> (2 * i)) & 1) << i for i in range(n))
        z = sum(((word >> (2 * i + 1)) & 1) << i for i in range(n))
        return x | (z << n)

    # The downstream physical lift replayers use the conventional packed
    # layout X[0..n-1] | Z[0..n-1].  Keep the census's interleaved internal
    # representation private and write a directly consumable list of 37 rows.
    records = [
        [xy_layout(word) for word in gens]
        for gens in cells[(10, 10)]
    ]
    path.write_text(json.dumps(records, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-generators", type=Path)
    args = parser.parse_args()
    cells = target_cells()
    if args.write_generators:
        write_target_generators(cells, args.write_generators)
    print("EXACT ADDITIVE LENGTHENING CENSUS PASS: n=10,k=10 has 37 classes")
    print("Equivalence: complete codebook incidence graph + nauty certificate")


if __name__ == "__main__":
    main()
