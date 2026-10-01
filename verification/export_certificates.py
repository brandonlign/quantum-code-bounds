#!/usr/bin/env python3
"""Export the Section 5 Farkas certificates as labelled JSON (Appendix A).

The original verifiers store multipliers by internal row index. This script
translates each index into a self-describing row label (type + split cell),
rescaling multipliers wherever an original row was multiplied by 2048, and
writes verification/certificates/*.json. Those files are then checked by
verification/check_certificates.py, which does not use the original scripts.

Run from the repository root:  python3 verification/export_certificates.py
"""
import contextlib
import importlib.util
import io
import json
import re
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "certificates"
S = 2048


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def low_cells(sizes):
    return [c for c in product(*[range(n + 1) for n in sizes]) if 1 <= sum(c) <= 4]


def all_cells(sizes):
    return list(product(*[range(n + 1) for n in sizes]))


def standard_rows(sizes, scale_unit_total=1, weight_rows=()):
    """E = [unit, total, low..., weight...], G = [incl..., cnonneg..., shadow...]."""
    E = [("unit", None, scale_unit_total), ("total", None, scale_unit_total)]
    E += [("low", c, 1) for c in low_cells(sizes)]
    E += [("weight", w, 1) for w in weight_rows]
    cells = all_cells(sizes)
    G = [("incl", c, 1) for c in cells] + [("cnonneg", c, 1) for c in cells] \
        + [("shadow", c, 1) for c in cells]
    return E, G


def label(entry, mult):
    t, c, scale = entry
    row = {"type": t}
    if t == "weight":
        row["w"], row["value"] = c, (3 if c == 4 else 0)
    elif t in ("coset_eq", "coset_le"):
        row["weights"], row["suffix_weight"] = c
    elif c is not None:
        row["cell"] = list(c)
    row["multiplier"] = mult * scale
    return row


def certificate(E, G, lam, nu):
    rows = [label(E[i], v) for i, v in sorted(nu.items()) if v]
    rows += [label(G[i], v) for i, v in sorted(lam.items())]
    return rows


def block(sites, gens, variables, pats=None):
    b = {"sites": sites, "generators": gens, "variables": variables}
    if pats is not None:
        b["patterns"] = [[list(p), c] for p, c in sorted(pats.items())]
    return b


def pattern_counts(prefix, mult):
    return dict(zip([tuple(p) for p in prefix], mult))


def write(name, section, desc, blocks, f, rows, columns, nu_rhs, positive):
    data = {"name": name, "section": section, "description": desc,
            "blocks": blocks, "suffix_sites": f, "certificate": rows,
            "expected": {"columns": columns, "nu_rhs": nu_rhs,
                         "positive_residuals": positive}}
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(data, indent=1) + "\n")
    print("wrote", name, len(rows), "rows")


def weight_two():
    m = load("s5_3_weight_two")
    sizes = (2, 12)
    E = [("unit", None, S), ("total", None, S)]
    E += [("low", (a, b), 1) for a in range(3) for b in range(13) if 0 < a + b <= 4]
    G = [("coset_le", ([1, 0, -1], b), S) for b in range(13)]
    for a in range(3):
        for b in range(13):
            G += [("incl", (a, b), 1), ("cnonneg", (a, b), 1), ("shadow", (a, b), 1)]
    write("s5_3_weight_two", "5.3", "R = <Z0 Z1>; variables are the split counts H_{a,b}",
          [block(2, ["ZZ"], "cells")], 12, certificate(E, G, m.LAM, m.NU),
          39, -m.BOUND, len(m.C))


def weight_three():
    m = load("s5_4_weight_three")
    E, G = standard_rows((3, 11))
    pats = {(0, 0, 1, 1): 12, (0, 1, 1, 0): 3, (1, 0, 0, 1): 1}
    write("s5_4_1_weight_three", "5.4.1", "R = <ZZZ>",
          [block(3, ["ZZZ"], "coset_patterns", pats)], 11,
          certificate(E, G, m.LAM, m.NU), 36, -m.BOUND, len(m.RESIDUAL))


def bell():
    m = load("s5_4_bell")
    E = [("unit", None, S), ("total", None, S), ("zero", (0, 1), S)]  # A_1 = 0
    for b in range(11):
        E += [("coset_eq", ([0, 1, 0, 0, 0], b), S),
              ("coset_eq", ([-3, 0, -1, 0, 1], b), S)]
    G = []
    for a in range(5):
        for b in range(11):
            if 0 < a + b <= 4:
                E.append(("low", (a, b), 1))
            G += [("incl", (a, b), 1), ("cnonneg", (a, b), 1), ("shadow", (a, b), 1)]
    write("s5_4_2_bell", "5.4.2", "R = <XXXX, ZZZZ>; variables are the split counts H_{a,b}",
          [block(4, ["XXXX", "ZZZZ"], "cells")], 10, certificate(E, G, m.LAM, m.NU),
          55, -m.BOUND, len(m.C))


def five_site():
    src = (HERE / "s5_4_five_site.mjs").read_text()
    def grab(name):
        body = re.search(r"const %s=\{(.*?)\};" % name, src, re.S).group(1)
        return {int(k): int(v) for k, v in re.findall(r"(\d+):(-?\d+)", body)}
    lam, nu = grab("L"), grab("NU")
    E, G = standard_rows((5, 9))
    prefix = [[0,0,1,0,3,0],[1,0,0,0,3,0],[0,0,0,2,0,2],[0,0,0,3,0,1],[0,0,0,1,0,3],
              [0,0,0,0,4,0],[0,0,2,0,2,0],[0,1,0,2,0,1],[0,0,0,4,0,0]]
    mult = [12, 1, 12, 12, 8, 12, 3, 3, 1]
    write("s5_4_3_five_site", "5.4.3", "R = <XXZZI, ZZZIZ>",
          [block(5, ["XXZZI", "ZZZIZ"], "coset_patterns", pattern_counts(prefix, mult))], 9,
          certificate(E, G, lam, nu), 90, -52501014528, 42)


def six_site(modname, name, gens, desc, positive):
    m = load(modname)
    E, G = standard_rows((6, 8))
    write(name, "5.4.4", desc,
          [block(6, gens, "coset_patterns", pattern_counts(m.PREFIX, m.MULT))], 8,
          certificate(E, G, m.LAM, m.NU), len(m.PREFIX) * 9, -m.BOUND, positive)


def rank_three():
    m = load("s5_6_rank_three")
    for key, sets in m.SETS.items():
        u, pats = m.normalizer_patterns(sets)
        gens = ["".join("Z" if k in s else "I" for k in range(u)) for s in sets]
        E, G = standard_rows((u, 14 - u), weight_rows=(4, 1, 2, 3))
        c = m.CERT[key]
        write(f"s5_6_rank_three_{key}", "5.6", f"R = <{', '.join(gens)}>, branch A_4 = 3",
              [block(u, gens, "coset_patterns", pats)], 14 - u,
              certificate(E, G, c["L"], c["NU"]), c["columns"], -c["bound"], c["positive"])


def disjoint():
    data = json.loads((HERE / "s5_7_disjoint_certificate.json").read_text())
    sizes = (4, 4, 4, 2)
    E = [("unit", None, S), ("total", None, S)]
    E += [("low", c, 1) for c in low_cells(sizes)]
    E += [("weight", w, S) for w in (1, 2, 3, 4)]
    G = [("incl", c, 1) for c in all_cells(sizes)] + \
        [("cnonneg", c, 1) for c in all_cells(sizes)] + \
        [("shadow", c, 1) for c in all_cells(sizes)]
    lam = {int(k): v for k, v in data["L"].items()}
    nu = {int(k): v for k, v in data["NU"].items()}
    pats = {(1,0,0,0,1): 1, (0,1,0,1,0): 4, (0,0,2,0,0): 3,
            (0,0,1,0,1): 24, (0,0,0,2,0): 24, (0,0,0,0,2): 8}
    blocks = [block(4, ["ZZZZ"], "coset_patterns", pats) for _ in range(3)]
    write("s5_7_disjoint", "5.7", "three blocks, each R_i = <ZZZZ>, branch A_4 = 3",
          blocks, 2, certificate(E, G, lam, nu), 648, data["constant"], data["positive"])


if __name__ == "__main__":
    weight_two()
    weight_three()
    bell()
    five_site()
    six_site("s5_4_six_site_same_letter", "s5_4_4_six_site_same_letter",
             ["ZZZZII", "ZZIIZZ"], "R = <ZZZZII, ZZIIZZ>", 75)
    six_site("s5_4_six_site_crossed", "s5_4_4_six_site_crossed",
             ["ZZZZII", "XXIIXX"], "R = <ZZZZII, XXIIXX>", 78)
    rank_three()
    disjoint()
