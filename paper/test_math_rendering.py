#!/usr/bin/env python3
"""Regression checks for mathematical inequalities in the PDF renderer."""

from build_nonexistence_pdf import math_markup, unicode_math

tests = [
    ("nu dot rhs < 0", "&lt;", "⟨"),
    ("x > 0", "&gt;", "⟩"),
    ("c >= 0", "≥", None),
    ("d <= 5", "≤", None),
    ("<p>", "⟨p⟩", None),
]
for source, expected, forbidden in tests:
    rendered = math_markup(source)
    assert expected in rendered, (source, rendered)
    if forbidden is not None:
        assert forbidden not in rendered, (source, rendered)

assert "⟨" not in unicode_math("nu dot rhs < 0")
assert "<" in unicode_math("nu dot rhs < 0")
assert ">" in unicode_math("x > 0")
assert "⊕" in unicode_math("V_14=V_4 orthogonal-sum W_10")
print("PASS: strict inequalities and Pauli angle brackets remain distinct")

# Regress the multiline shadow-transform failure: no single Paragraph may
# contain two source formula rows separated by a <br/> tag.
from reportlab.platypus import Paragraph
from build_nonexistence_pdf import make_styles, parse_markdown, register_fonts

example = """```text
2048 C_(a,b)
  = sum_(i,j) H_(i,j) K_a^(m)(i) K_b^(f)(j),
2048 Sh_(a,b)
  = sum_(i,j) (-1)^(i+j) H_(i,j) K_a^(m)(i) K_b^(f)(j).
```
"""
register_fonts()
styles = make_styles()
equations = [
    flowable
    for flowable in parse_markdown(example, styles, 480)
    if isinstance(flowable, Paragraph) and flowable.style.name == "QECEquation"
]
assert len(equations) == 4, len(equations)
assert styles["Equation"].leading >= 20
assert all("<br/>" not in paragraph.text for paragraph in equations)
print("PASS: multiline equations are separate flowables with clear line spacing")

# Protect ordinary prose from conversion to a mathematical intersection sign.
from build_nonexistence_pdf import inline_markup
from reportlab.platypus import KeepTogether
assert "intersecting pairs" in inline_markup("two intersecting pairs")
archive_link = inline_markup(
    "[immutable code archive](https://github.com/brandonlign/"
    "quantum-code-bounds/archive/c14d6dadf2c5f902d9c149ed992fbac54b63596e.zip)"
)
assert '<link href="https://github.com/brandonlign/' in archive_link
assert "immutable code archive" in archive_link

census = """| length `n` | checked binary dimensions `k: count` |
|---:|---|
| 9 | `8:2298`, `9:0`, `10:0` |
| 10 | `10:37` |
"""
flowables = parse_markdown(census, styles, 480)
assert any(isinstance(x, KeepTogether) for x in flowables)
print("PASS: prose, linked archive and unbroken census table")

# A blank source line must not break a section heading's keepWithNext.
heading_sample = """## References

* A. Author, A mathematical paper.
"""
parts = parse_markdown(heading_sample, styles, 480)
assert isinstance(parts[0], Paragraph) and parts[0].style.name == "QECH1"
assert isinstance(parts[1], Paragraph) and "mathematical paper" in parts[1].text

# Keep subsection labels, introductory prose and the first displayed
# subgroup formula as a unit, so the definition cannot start a new page.
subgroup_sample = """#### The two six-site overlap subgroups

For the same-letter two-site overlap, use

```text
R = < ZZZZII, ZZIIZZ >.
```
"""
parts = parse_markdown(subgroup_sample, styles, 480)
assert isinstance(parts[0], KeepTogether)
assert any(
    isinstance(f, Paragraph) and f.style.name == "QECEquation"
    for f in parts[0]._content
)
print("PASS: no orphaned headings or detached subgroup formulas")
