Dear Editors,

I submit the manuscript "No binary [[14,3,d≥5]] quantum stabilizer code exists: A signed-shadow proof and exhaustive additive-code classification" for consideration in Designs, Codes and Cryptography.

The paper proves that no binary stabilizer code with parameters [[14,3,5]] exists, so d_max(14,3) = 4. This closes the open entry for n = 14, k = 3 in Grassl's table of quantum code bounds (codetables.de), which currently lists a lower bound of 4 and an upper bound of 5. The method is related to the nonexistence proof for [[13,5,4]] by Bierbrauer, Fears, Marcugini and Pambianco (IEEE Trans. Inf. Theory, 2011). It combines signed affine-shadow inequalities, exact integer Farkas certificates on split weight enumerators, a reduction to length-ten additive codes with symplectic hull dimension four, a reconstruction of the 37 equivalence classes counted by Grassl, Krotov, Sok and Solé, and a coset-capacity argument.

Since the proof is computer-assisted, I have tried to make it easy to check. Every computation uses exact integer arithmetic. Appendix A defines each Section 5 linear system row by row. The certificates are published as data files with a short standalone checker, so a referee can check Section 5 without reading the main code. All code and data are public and archived on Zenodo (doi:10.5281/zenodo.22885774), and the full verification runs in seconds on a laptop.

As stated in the acknowledgments, generative-AI tools assisted with exploring proof strategies, writing verification code and editing the text. I directed the work, checked the arguments and computations, and take full responsibility for the content.

The manuscript has not been published or submitted elsewhere. An earlier version is posted as a preprint on Zenodo.

Sincerely,
Brandon Li
Independent researcher
brandon.li.gn@gmail.com
