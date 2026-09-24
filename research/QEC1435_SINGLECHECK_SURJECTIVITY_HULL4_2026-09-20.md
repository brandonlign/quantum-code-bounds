# SURJECTIVITY REPAIR: the unique-four-body case forces EXACT ten-site symplectic hull dimension four

Date: 20 September 2026. This supersedes the overbroad rank list {0,2,4,6} in QEC1435_SINGLE_H4_TENQ_PROJECTION_AND_CONTROL_2026-09-20.md. **New elementary original-physical necessary theorem**, conditional on the separately certified candidate H1=H2=H3=0, H4=1 reduction. The target [[14,3,5]] existence question remains OPEN. All weights and supports below refer to ORIGINAL fourteen physical qubits, not effective pseudoqubits.

## The corrected theorem

Suppose S≤F2^28 is an isotropic rank-eleven stabilizer with d>=5 and EXACTLY ONE nonidentity word of physical weight≤4, namely a four-site p. Conjugate it by real physical local Cliffords and site permutations to p=Z0Z1Z2Z3. Write V=V4 orthogonal-sum W10; let E=(p^perp∩V4)/<p> be the NONDEGENERATE six-dimensional symplectic quotient.

As in the earlier derivation, S/<p> is the graph of an F2-linear map T:P→E with P≤W10 a binary ten-space and

    <x,y>_W = <T(x),T(y)>_E,   x,y∈P.

The graph projection is injective because S has no other stabilizer supported on the four p sites.

**NEW LOAD-BEARING STEP: T is ONTO.** A vector z∈E orthogonal to im(T) has a physical representative v∈p^perp∩V4 which commutes with p and EVERY element of S. Every representative is supported on at most four ORIGINAL physical sites. Distance≥5 thus forces v∈S. But S∩V4=<p>, so z=0. Hence (im T)^perp_E={0}, and nondegeneracy of E implies

    im T=E,    rank T=6,    dim ker T=10−6=4.

Since T is onto, the radical of the pairing on P is EXACTLY ker T: if x∈P pairs trivially with P, its image T(x) pairs trivially with all of E and therefore vanishes. The reverse implication follows immediately from the pullback pairing identity. Therefore

    rad(P)=P∩P^perp_W=ker T,    dim rad(P)=4,
    rank(<.,.>|P)=6.

Put C=P^perp_W, the genuine ten-site additive [10,5,d>=5] code established in the earlier note. Its restricted pairing has the SAME radical P∩C, because dim C=dim P=10. Therefore

    |C|=1024, d(C)>=5,
    dim(C∩C^perp_W)=4,   rank(<.,.>|C)=6.

Moreover S∩W10=ker T is an EXACTLY four-dimensional ORIGINAL-PHYSICAL suffix-only stabilizer. This is much sharper than the earlier bound "at least four to six" and means any future full-code search must not treat the map T as an arbitrary rank-two or rank-four embedding.

## Constructive equivalence before the distance filter

Conversely, take ANY genuine ten-site additive code C of binary dimension ten, minimum distance≥5 and trace-symplectic hull H=C∩C^perp of EXACT binary dimension four. Put P=C^perp. The quotient P/H is a nondegenerate SIX-dimensional symplectic space. Choose ANY symplectic isomorphism φ:P/H→E and set

    T=P → P/H → E via φ,
    S/<p> = { T(x)+x : x∈P }.

Lifting this graph together with p gives a rank-eleven isotropic ORIGINAL fourteen-qubit stabilizer. It automatically has no extra four-site prefix-only stabilizer and no forbidden suffix-only weight≤4 centralizer. It may STILL have original-physical mixed-support logical operators of weight≤4, or extra mixed-support stabilizer words of weight≤4. Those are precisely the remaining obstruction and MUST be tested; no code existence is asserted by the graph construction alone.

Thus the unresolved original target is a sharply specified finite lifting problem:

    additive ten-site [10,5,d>=5] with HULL DIMENSION EXACTLY FOUR
       +
    symplectic isomorphism P/H ≅ E
       +
    NO forbidden mixed original-physical weight≤4 logicals,
    NO additional mixed weight≤4 stabilizers.

All potentially compatible maps are SIX-dimensional symplectic isometries; the choice of basis in P/H and E exposes Sp(6,2) choices per fixed C, before quotienting physical equivalences and pruning forbidden original-support words.

## Independent falsification of the earlier shortcut

The explicit shortened/punctured dodecacode control has length ten, 1024 words, minimum weight five, and symplectic rank TWO / hull dimension EIGHT. It satisfies the WEAKER size/distance/hull-at-least-four conditions but FAILS this corrected EXACT hull-four requirement. In its naive rank-two lift, at least one nonzero physical four-site quotient operator commutes with S and creates an original-physical logical of weight≤4. A direct independently calculated example finds weight-one logical labels with no short stabilizers beyond p. This is the expected concrete manifestation of nonsurjectivity, not a contradiction in the code construction.

The earlier length-ten self-dual rank-zero shadow obstruction remains a valid independent lemma but is NO LONGER a load-bearing branch of the single-H4 reduction; surjectivity excludes rank-zero, rank-two and rank-four at once.

## Review obligations

The new proof uses only original-physical distance and the exact quotient graph, not a numerical LP, published code classification or an unjustified substitution of pseudoqubit weight. An independent reviewer should specifically check the implication "prefix-only centralizer ≤4 -> belongs to <p>" and the dimensional identity rad(P)=ker T. The global H4=1 premise and the remaining rank-six compatible-lift search are separately open to adversarial scrutiny.
