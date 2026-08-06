r"""
k3_residue_angle.py — the residue angle on a K3 period loop (Tier-2 demo).

Setting: the K3 lattice L = U^3 (+) E8(-1)^2, rank 22, signature (3,19).
Period loop (exact, polynomial in t — a rational rotation of the positive
2-plane inside the positive 3-space spanned by P_i = u_i + v_i):

    omega(t) = (1 - t^2) P1 + 2t P2 + i (1 + t^2) P3,

with Q(omega, omega) = 0 and Q(omega, conj omega) = 4 (1+t^2)^2 > 0
identically (asserted).  t is a tangent-half-angle: t in R u {inf} is a
CLOSED LOOP through the period domain.

Residue reading of a rational class gamma at period omega:

    r(gamma, t)^2 := 2 |Q(gamma, omega)|^2 / Q(omega, conj omega)
                   = Hodge-norm^2 of the (2,0)+(0,2) component of gamma.

r = 0  <=>  gamma is (1,1)  <=>  gamma in NS (and on a K3, Lefschetz (1,1)
BACKS it: gamma is a divisor class — the audit is a theorem here).

Facts demonstrated exactly:
  [K1] the loop is a valid period path (identities in t).
  [K2] NS of the very general member of the loop = rank 19
       (identical-vanishing kernel).
  [K3] every class with Q3 := Q(gamma,P3) = 0 and (Q1,Q2) != 0 clears
       residue at EXACTLY TWO parameter values with t+ * t- = -1
       (an antipodal pair on the loop — the conjugate-pair symmetry again).
  [K4] classes with Q3 != 0 carry a FROZEN RESIDUE on this family:
       r >= |Q3|/sqrt(2), a positive floor attained but never crossed.
  [K5] at a wall the Picard number jumps 19 -> 20 (computed exactly over
       Q(sqrt(2)) at the irrational wall t0 = 1 + sqrt(2)).
  [K6] walls densify: distinct wall directions grow with the height bound
       (Noether-Lefschetz loci are dense).
  [K7] backing at sample walls is nameable: a (-2)-class wall = a rational
       (-2)-curve materializes (Riemann-Roch chi = 1 => +-gamma effective);
       a 0-class wall = an elliptic-fiber class; a positive class = a
       polarization-type class.

Also emits k3_residue_data.json with sampled r(t) curves + wall data for
the companion visual page.
"""

import json
from itertools import product as iproduct
from math import gcd
from sympy import (symbols, Matrix, eye, zeros, expand, sqrt, Rational,
                   nsimplify, simplify, S)

t = symbols('t')

# --------------------------------------------------------------------------
# The K3 lattice: U^3 (+) E8(-1)^2
# --------------------------------------------------------------------------
U = Matrix([[0, 1], [1, 0]])
E8 = Matrix([
    [-2, 1, 0, 0, 0, 0, 0, 0],
    [1, -2, 1, 0, 0, 0, 0, 0],
    [0, 1, -2, 1, 0, 0, 0, 0],
    [0, 0, 1, -2, 1, 0, 0, 0],
    [0, 0, 0, 1, -2, 1, 0, 1],
    [0, 0, 0, 0, 1, -2, 1, 0],
    [0, 0, 0, 0, 0, 1, -2, 0],
    [0, 0, 0, 0, 1, 0, 0, -2]])

def blockdiag(mats, n):
    G = zeros(n, n)
    o = 0
    for m in mats:
        k = m.rows
        G[o:o+k, o:o+k] = m
        o += k
    return G

G = blockdiag([U, U, U, E8, E8], 22)
assert G.det() == -1  # unimodular
# basis order: u1,v1,u2,v2,u3,v3, then E8 x2

def bvec(**coords):
    """Lattice vector from named U-block coordinates (E8 parts zero)."""
    names = ['u1', 'v1', 'u2', 'v2', 'u3', 'v3']
    v = zeros(22, 1)
    for k, val in coords.items():
        v[names.index(k), 0] = val
    return v

def Q(a, b):
    return (a.T * G * b)[0, 0]

P1 = bvec(u1=1, v1=1)
P2 = bvec(u2=1, v2=1)
P3 = bvec(u3=1, v3=1)

# --------------------------------------------------------------------------
# [K1] the period loop
# --------------------------------------------------------------------------
om_re = (1 - t**2) * P1 + 2*t * P2
om_im = (1 + t**2) * P3
assert expand(Q(om_re, om_re) - Q(om_im, om_im)) == 0
assert expand(Q(om_re, om_im)) == 0
QoObar = expand(Q(om_re, om_re) + Q(om_im, om_im))
assert QoObar == expand(4 * (1 + t**2)**2)
print("[K1] omega(t) is a valid period loop: Q(om,om)=0, Q(om,om_bar)=4(1+t^2)^2 > 0, identically.")

def Q123(gamma):
    return Q(gamma, P1), Q(gamma, P2), Q(gamma, P3)

def r_squared(gamma):
    """Exact residue reading squared, as a function of t."""
    q1, q2, q3 = Q123(gamma)
    re = (1 - t**2) * q1 + 2*t * q2
    im = (1 + t**2) * q3
    return simplify(2 * (re**2 + im**2) / QoObar)

# --------------------------------------------------------------------------
# [K2] NS of the very general member of the loop
# --------------------------------------------------------------------------
# gamma (1,1) identically  <=>  Q(gamma,P1) = Q(gamma,P2) = Q(gamma,P3) = 0
Cnd = Matrix.vstack(P1.T * G, P2.T * G, P3.T * G)
NSvg = Cnd.nullspace()
print(f"[K2] rank NS(very general member of loop) = {len(NSvg)}   (expect 19)")
assert len(NSvg) == 19

# --------------------------------------------------------------------------
# [K3] two antipodal walls per crossing class
# --------------------------------------------------------------------------
# r = 0 needs q3 = 0 and (1-t^2) q1 + 2t q2 = 0, i.e. -q1 t^2 + 2 q2 t + q1 = 0;
# for q1 != 0 the two roots multiply to -1 (Vieta) — verified exactly:
ok = True
for (q1v, q2v) in [(1, 0), (1, 1), (3, 1), (2, -5), (7, 4)]:
    roots = [(q2v + s * sqrt(q1v**2 + q2v**2)) / q1v for s in (1, -1)]
    ok &= simplify(roots[0] * roots[1] + 1) == 0
print(f"[K3] wall pairs satisfy t+ * t- = -1 exactly (antipodal on the loop): {ok}")
assert ok

# --------------------------------------------------------------------------
# showcase classes
# --------------------------------------------------------------------------
show = [
    ("A: u1-v1+u2   (sq -2)", bvec(u1=1, v1=-1, u2=1)),
    ("B: u1+v2      (sq 0)",  bvec(u1=1, v2=1)),
    ("C: u1         (sq 0)",  bvec(u1=1)),
    ("E: 2u1+v1+u2  (sq 4)",  bvec(u1=2, v1=1, u2=1)),
    ("D: u3  (FROZEN, q3=1)", bvec(u3=1)),
]
backing = {-2: "a (-2)-curve materializes (RR: chi=1 => +-gamma effective)",
            0: "an elliptic-fiber class becomes algebraic",
            4: "a degree-4 polarization-type class becomes algebraic"}

print("\n[K4] showcase ledger (walls exact; backing per Lefschetz (1,1)):")
curves = []
for name, gm in show:
    q1v, q2v, q3v = Q123(gm)
    sq = Q(gm, gm)
    if q3v != 0:
        floor = sqrt(S(q3v)**2 / 2)
        # exact floor claim: r^2 - q3^2/2 = ((1-t^2)q1+2t q2)^2 / (2(1+t^2)^2) >= 0
        gap = simplify(r_squared(gm) - S(q3v)**2 / 2)
        num = simplify(gap * 2 * (1 + t**2)**2)
        assert simplify(num - ((1 - t**2)*q1v + 2*t*q2v)**2) == 0
        print(f"  {name}:  NO walls; frozen residue floor r >= {floor} = |q3|/sqrt(2) (exact)")
        walls = []
    else:
        if q1v != 0:
            walls = [(q2v + s * sqrt(q1v**2 + q2v**2)) / q1v for s in (1, -1)]
        elif q2v != 0:
            walls = [S(0)]          # -q1 t^2 + 2 q2 t + q1 = 2 q2 t; antipode at t = inf
        else:
            walls = []
        wtxt = ", ".join(str(simplify(w)) for w in walls) if walls else "(in permanent NS)"
        btxt = backing.get(sq, "algebraic class (Lefschetz (1,1))")
        print(f"  {name}:  walls at t = {wtxt}"
              + (" [+ antipode t=inf]" if (q1v == 0 and q2v != 0) else "")
              + f"  ->  {btxt}")
    # sampled curve for the visual
    r2 = r_squared(gm)
    samples = []
    for k in range(-32, 33):
        tv = Rational(k, 8)
        samples.append([float(tv), float(sqrt(r2.subs(t, tv)))])
    curves.append({"name": name, "square": int(sq),
                   "q": [int(q1v), int(q2v), int(q3v)],
                   "walls": [float(w) for w in walls],
                   "samples": samples})

# --------------------------------------------------------------------------
# [K5] Picard jump at the irrational wall t0 = 1 + sqrt(2)  (class B)
# --------------------------------------------------------------------------
# RATIONAL Picard rank at an algebraic parameter value: expand the wall
# conditions in the Q-basis {1, sqrt 2} and stack RATIONAL coefficient rows
# (a Q(sqrt2)-nullspace would report 20 at EVERY algebraic point — the
# rational lattice needs rational rows; referee-caught correction).
def rational_picard_rank(tval):
    c1 = expand(1 - tval**2)
    c2 = expand(2 * tval)
    rows = []
    for part in ("one", "rad"):
        row = []
        for gcol in range(22):
            val = expand(c1 * (P1.T * G)[gcol] + c2 * (P2.T * G)[gcol])
            co = val.coeff(sqrt(2), 1) if part == "rad" else val.subs(sqrt(2), 0)
            row.append(nsimplify(co))
        rows.append(row)
    rows.append([(P3.T * G)[gcol] for gcol in range(22)])
    return len(Matrix(rows).nullspace())

r_wall = rational_picard_rank(1 + sqrt(2))
r_calib = rational_picard_rank(sqrt(2))
print(f"\n[K5] RATIONAL Picard rank at the wall t0 = 1+sqrt(2): {r_wall}; at the")
print(f"     non-wall algebraic point t = sqrt(2): {r_calib}  (calibration pair:")
print(f"     the wall's real condition is rationally proportional — q1 = q2 —")
print(f"     while the non-wall point forces q1 = q2 = 0)")
assert r_wall == 20 and r_calib == 19

# --------------------------------------------------------------------------
# [K6] wall densification
# --------------------------------------------------------------------------
print("\n[K6] distinct wall directions (primitive [q1:q2], q3=0) by height bound:")
dens = []
for H in range(1, 7):
    dirs = set()
    for q1v, q2v in iproduct(range(-H, H+1), repeat=2):
        if (q1v, q2v) == (0, 0):
            continue
        g_ = gcd(abs(q1v), abs(q2v))
        d = (q1v // g_, q2v // g_)
        if d[0] < 0 or (d[0] == 0 and d[1] < 0):
            d = (-d[0], -d[1])
        dirs.add(d)
    dens.append([H, len(dirs), 2 * len(dirs)])
    print(f"     H = {H}:  {len(dirs):3d} directions  ->  {2*len(dirs):3d} walls on the loop")
print("     (walls of the full lattice are DENSE on the loop: the Noether-Lefschetz picture)")

# --------------------------------------------------------------------------
# [K7] slopes at walls (near-miss analog: linear vanishing, exact rate)
# --------------------------------------------------------------------------
print("\n[K7] exact detuning rate |dr/dt| at each showcase wall:")
slopes = {}
for name, gm in show:
    q1v, q2v, q3v = Q123(gm)
    if q3v != 0:
        continue
    r2 = r_squared(gm)
    for w in ([(q2v + s * sqrt(q1v**2 + q2v**2)) / q1v for s in (1, -1)]
              if q1v != 0 else ([S(0)] if q2v != 0 else [])):
        dr = simplify(sqrt(simplify(r2.diff(t, 2).subs(t, w) / 2)))
        slopes.setdefault(name, []).append(str(dr))
        print(f"  {name}  at t = {simplify(w)}:  |r'| = {dr}")

with open("k3_residue_data.json", "w") as fh:
    json.dump({"curves": curves, "density": dens}, fh)
print("\n[data] wrote k3_residue_data.json for the visual page.")
