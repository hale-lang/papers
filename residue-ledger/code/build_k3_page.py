r"""
build_k3_page.py — emit the K3 residue-angle instrument page from
k3_residue_data.json (static SVG polylines + hover layer + table views).
"""

import json

import os
OUT = os.environ.get("K3_PAGE_OUT", "k3-residue-angle.html")

with open("k3_residue_data.json") as fh:
    data = json.load(fh)

curves = data["curves"]
density = data["density"]

# display metadata keyed by curve initial
META = {
    "A": ("A", "(−2)-curve wall at t = 0", "s1", False),
    "B": ("B", "elliptic fiber, walls 1 ± √2", "s2", False),
    "C": ("C", "elliptic fiber, walls ±1", "s3", False),
    "E": ("E", "quartic class, walls (1 ± √10)/3", "s4", False),
    "D": ("D", "frozen: floor 1/√2, no walls", "s5", True),
}

W, H = 880, 400
ML, MR, MT, MB = 52, 168, 18, 40
PW, PH = W - ML - MR, H - MT - MB
TMIN, TMAX, RMIN, RMAX = -4.0, 4.0, 0.0, 2.4

def X(tv): return ML + (tv - TMIN) / (TMAX - TMIN) * PW
def Y(rv): return MT + (1 - (rv - RMIN) / (RMAX - RMIN)) * PH

def poly(samples):
    return " ".join(f"{X(tv):.1f},{Y(rv):.1f}" for tv, rv in samples)

walls_all = []
for c in curves:
    key = c["name"][0]
    for w in c["walls"]:
        walls_all.append((w, key))

# --- SVG pieces -----------------------------------------------------------
grid = []
for rv in (0.5, 1.0, 1.5, 2.0):
    grid.append(f'<line x1="{ML}" y1="{Y(rv):.1f}" x2="{ML+PW}" y2="{Y(rv):.1f}" class="grid"/>')
ticks = []
for tv in range(-4, 5):
    ticks.append(f'<line x1="{X(tv):.1f}" y1="{MT+PH}" x2="{X(tv):.1f}" y2="{MT+PH+4}" class="axis"/>'
                 f'<text x="{X(tv):.1f}" y="{MT+PH+16}" class="tick" text-anchor="middle">{tv}</text>')
for rv, lab in ((0, "0"), (0.7071, "1/√2"), (1.0, "1"), (2.0, "2")):
    ticks.append(f'<text x="{ML-8}" y="{Y(rv)+3.5:.1f}" class="tick" text-anchor="end">{lab}</text>')

wall_marks = "".join(
    f'<line x1="{X(w):.1f}" y1="{MT}" x2="{X(w):.1f}" y2="{MT+PH}" class="wall"/>'
    for w, _ in walls_all)

floor_line = (f'<line x1="{ML}" y1="{Y(0.7071):.1f}" x2="{ML+PW}" y2="{Y(0.7071):.1f}" '
              f'class="floorline"/>')

series_svg, labels_svg = [], []
ends = []
for c in curves:
    key = c["name"][0]
    short, desc, slot, dashed = META[key]
    dash = ' stroke-dasharray="7 4"' if dashed else ""
    series_svg.append(f'<polyline points="{poly(c["samples"])}" class="ser {slot}"{dash}/>')
    tv, rv = c["samples"][-1]
    ends.append([Y(rv) + 3.5, short, desc, slot])
# de-collide direct labels: sort by y, enforce >= 13px separation
ends.sort()
for k in range(1, len(ends)):
    if ends[k][0] - ends[k-1][0] < 13:
        ends[k][0] = ends[k-1][0] + 13
for ypos, short, desc, slot in ends:
    labels_svg.append(f'<text x="{X(TMAX)+6:.1f}" y="{ypos:.1f}" class="dlabel {slot}t">'
                      f'{short} · {desc}</text>')

# rho strip: 19 with unit spikes at walls
SH, SMT = 84, 10
rho_base = Y2 = lambda v: SMT + (1 - (v - 18.7) / (20.3 - 18.7)) * (SH - SMT - 22)
strip = [f'<line x1="{ML}" y1="{rho_base(19):.1f}" x2="{ML+PW}" y2="{rho_base(19):.1f}" class="rho"/>']
for w, _ in walls_all:
    strip.append(f'<line x1="{X(w):.1f}" y1="{rho_base(19):.1f}" x2="{X(w):.1f}" y2="{rho_base(20):.1f}" class="rho"/>'
                 f'<circle cx="{X(w):.1f}" cy="{rho_base(20):.1f}" r="3.2" class="rhodot"/>')
strip.append(f'<text x="{ML-8}" y="{rho_base(19)+3.5:.1f}" class="tick" text-anchor="end">19</text>')
strip.append(f'<text x="{ML-8}" y="{rho_base(20)+3.5:.1f}" class="tick" text-anchor="end">20</text>')

legend_rows = "".join(
    f'<span class="lg"><span class="sw {META[c["name"][0]][2]}bg'
    + (" swdash" if META[c["name"][0]][3] else "") + '"></span>'
    + f'{META[c["name"][0]][0]} · {META[c["name"][0]][1]}</span>'
    for c in curves)

density_rows = "".join(f"<tr><td>{h}</td><td>{d}</td><td>{wl}</td></tr>" for h, d, wl in density)

# sample data table (relief + accessibility)
head = "".join(f"<th>{META[c['name'][0]][0]}</th>" for c in curves)
rows = []
n = len(curves[0]["samples"])
for i in range(0, n):
    tv = curves[0]["samples"][i][0]
    cells = "".join(f"<td>{c['samples'][i][1]:.3f}</td>" for c in curves)
    rows.append(f"<tr><td>{tv:+.3f}</td>{cells}</tr>")
sample_table = f"<table><thead><tr><th>t</th>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>"

json_blob = json.dumps({"curves": [{"n": META[c["name"][0]][0],
                                    "s": c["samples"]} for c in curves]})

html = f"""<title>The K3 Residue Angle</title>
<style>
  :root {{
    --paper:#FAFAF7; --ink:#1B1E1C; --muted:#5C635E; --accent:#2E6B4F;
    --rule:#D9DBD4; --grid:#E4E5DE; --quote:#F1F4EF;
    --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --s5:#e87ba4;
  }}
  @media (prefers-color-scheme: dark) {{ :root {{
    --paper:#161917; --ink:#E5E7E1; --muted:#9AA29B; --accent:#6FBF97;
    --rule:#2C312D; --grid:#242825; --quote:#1C201D;
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181;
  }} }}
  :root[data-theme="dark"] {{
    --paper:#161917; --ink:#E5E7E1; --muted:#9AA29B; --accent:#6FBF97;
    --rule:#2C312D; --grid:#242825; --quote:#1C201D;
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181;
  }}
  :root[data-theme="light"] {{
    --paper:#FAFAF7; --ink:#1B1E1C; --muted:#5C635E; --accent:#2E6B4F;
    --rule:#D9DBD4; --grid:#E4E5DE; --quote:#F1F4EF;
    --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --s5:#e87ba4;
  }}
  html {{ background: var(--paper); }}
  body {{ background: var(--paper); color: var(--ink); margin: 0; padding: 0 1.25rem;
    font-family: "Palatino Linotype", Palatino, "URW Palladio L", "Book Antiqua", Georgia, serif;
    line-height: 1.6; }}
  .sheet {{ max-width: 62rem; margin: 0 auto; padding: 3.5rem 0 4.5rem; }}
  .eyebrow {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .72rem;
    letter-spacing: .14em; text-transform: uppercase; color: var(--accent); margin: 0 0 1.2rem; }}
  h1 {{ font-size: clamp(1.7rem, 4.5vw, 2.4rem); font-weight: 400; line-height: 1.15;
    margin: 0 0 .8rem; text-wrap: balance; }}
  .sub {{ font-style: italic; color: var(--muted); margin: 0 0 2rem; max-width: 60ch; }}
  p {{ max-width: 66ch; }}
  .panel {{ border: 1px solid var(--rule); padding: 1.1rem 1rem .6rem; margin: 1.6rem 0; }}
  .paneltitle {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .72rem;
    letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin: 0 0 .6rem; }}
  .chartwrap {{ position: relative; overflow-x: auto; }}
  svg {{ display: block; max-width: 100%; height: auto; }}
  .grid {{ stroke: var(--grid); stroke-width: 1; }}
  .axis {{ stroke: var(--muted); stroke-width: 1; }}
  .tick {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 10.5px;
    fill: var(--muted); font-variant-numeric: tabular-nums; }}
  .wall {{ stroke: var(--muted); stroke-width: 1; stroke-dasharray: 2 4; opacity: .55; }}
  .floorline {{ stroke: var(--s5); stroke-width: 1; stroke-dasharray: 2 5; opacity: .5; }}
  .ser {{ fill: none; stroke-width: 2; stroke-linejoin: round; }}
  .s1 {{ stroke: var(--s1); }} .s2 {{ stroke: var(--s2); }} .s3 {{ stroke: var(--s3); }}
  .s4 {{ stroke: var(--s4); }} .s5 {{ stroke: var(--s5); }}
  .dlabel {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 10.5px; }}
  .s1t {{ fill: var(--s1); }} .s2t {{ fill: var(--s2); }} .s3t {{ fill: var(--s3); }}
  .s4t {{ fill: var(--s4); }} .s5t {{ fill: var(--s5); }}
  .rho {{ stroke: var(--muted); stroke-width: 1.6; }}
  .rhodot {{ fill: var(--accent); }}
  .lg {{ display: inline-flex; align-items: center; gap: .45rem;
    font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .72rem;
    color: var(--ink); margin: 0 1.1rem .5rem 0; }}
  .sw {{ width: 14px; height: 3px; display: inline-block; border-radius: 2px; }}
  .swdash {{ background-image: linear-gradient(90deg, currentColor 60%, transparent 40%);
    background-size: 6px 3px; }}
  .s1bg {{ background: var(--s1); color: var(--s1); }} .s2bg {{ background: var(--s2); color: var(--s2); }}
  .s3bg {{ background: var(--s3); color: var(--s3); }} .s4bg {{ background: var(--s4); color: var(--s4); }}
  .s5bg {{ background: var(--s5); color: var(--s5); }}
  .crosshair {{ stroke: var(--muted); stroke-width: 1; opacity: 0; }}
  .tip {{ position: absolute; pointer-events: none; background: var(--paper);
    border: 1px solid var(--rule); padding: .4rem .6rem; font-family: ui-monospace, Menlo,
    Consolas, monospace; font-size: .7rem; line-height: 1.5; opacity: 0; white-space: nowrap;
    font-variant-numeric: tabular-nums; }}
  table {{ border-collapse: collapse; font-size: .85rem; font-variant-numeric: tabular-nums; }}
  th {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .68rem;
    letter-spacing: .08em; text-transform: uppercase; font-weight: 400; color: var(--muted);
    text-align: left; padding: .35rem .9rem .35rem 0; border-bottom: 1px solid var(--ink); }}
  td {{ padding: .35rem .9rem .35rem 0; border-bottom: 1px solid var(--rule); }}
  .tablewrap {{ overflow-x: auto; }}
  details {{ margin: 1rem 0; }}
  summary {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .75rem;
    color: var(--accent); cursor: pointer; }}
  summary:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
  .note {{ font-size: .85rem; color: var(--muted); max-width: 66ch; }}
  code {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .9em; }}
</style>

<div class="sheet">
  <p class="eyebrow">The residue ledger · instrument two</p>
  <h1>The K3 Residue Angle</h1>
  <p class="sub">A rational loop of periods through the K3 moduli, and the exact residue
  reading r(γ, t) — the Hodge-length of each rational class's off-(1,1) component — for five
  lattice classes. Zeros are Noether–Lefschetz wall-crossings — and the loop is sharply
  dichotomous: away from walls the fibers are <em>nonprojective</em> with ρ = 19 (their
  Néron–Severi lattice is negative definite), while at every wall the clearing coset contains a
  positive-square class, so the wall surface is <em>projective</em> with ρ = 20, the maximum.
  Clearing and projectivity arrive together, and Lefschetz (1,1) applies in full exactly there.</p>

  <div class="panel">
    <p class="paneltitle">Residue reading r(γ, t) along the period loop ω(t) — exact curves, sampled at t = k/8</p>
    <div class="chartwrap" id="cw">
      <svg viewBox="0 0 {W} {H}" role="img"
           aria-label="Residue readings of five K3 lattice classes along a period loop. Four curves touch zero at their walls; the frozen class stays at the constant floor 1 over root 2.">
        {''.join(grid)}
        <line x1="{ML}" y1="{MT+PH}" x2="{ML+PW}" y2="{MT+PH}" class="axis"/>
        {wall_marks}
        {floor_line}
        {''.join(series_svg)}
        {''.join(labels_svg)}
        {''.join(ticks)}
        <text x="{ML+PW/2}" y="{H-6}" class="tick" text-anchor="middle">t  (loop parameter; t and −1/t are antipodal)</text>
        <line id="xh" class="crosshair" x1="0" y1="{MT}" x2="0" y2="{MT+PH}"/>
        <rect id="hit" x="{ML}" y="{MT}" width="{PW}" height="{PH}" fill="transparent"/>
      </svg>
      <div class="tip" id="tip"></div>
    </div>
    <div>{legend_rows}</div>
  </div>

  <div class="panel">
    <p class="paneltitle">Picard number ρ(t) along the loop — the imposed count (jumps at the showcased walls)</p>
    <svg viewBox="0 0 {W} {SH}" role="img" aria-label="Picard number 19 along the loop with isolated jumps to 20 at each wall.">
      {''.join(strip)}
    </svg>
    <p class="note">ρ = 19 at very general t, 20 at each wall — verified exactly, including over
    ℚ(√2) at the irrational wall t = 1 + √2. The walls of the <em>full</em> lattice are dense on
    the loop; only the five showcased classes' walls are marked. The count is the unstable,
    imposed integer; the residue reading above is the continuous data that compensates it.</p>
  </div>

  <div class="panel">
    <p class="paneltitle">The wall ledger — walls are projective (ρ = 20); Lefschetz (1,1) + RR apply in full</p>
    <div class="tablewrap">
    <table>
      <thead><tr><th>class</th><th>γ²</th><th>walls (exact)</th><th>|dr/dθ| at wall (chart-free)</th><th>backing at the wall</th></tr></thead>
      <tbody>
        <tr><td>A = u₁−v₁+u₂</td><td>−2</td><td>0 and ∞ (antipodes)</td><td>√2/2</td><td>a (−2) class becomes algebraic; ±γ effective (RR: χ = 1); irreducibility chamber-dependent</td></tr>
        <tr><td>B = u₁+v₂</td><td>0</td><td>1 ± √2</td><td>1</td><td>square-0 class becomes algebraic — elliptic fibration after reflection into the nef chamber</td></tr>
        <tr><td>C = u₁</td><td>0</td><td>±1</td><td>√2/2</td><td>square-0 class becomes algebraic — elliptic fibration after nef reflection</td></tr>
        <tr><td>E = 2u₁+v₁+u₂</td><td>4</td><td>(1 ± √10)/3</td><td>√5</td><td>square-4 polarization-type class becomes algebraic (ampleness chamber-dependent)</td></tr>
        <tr><td>D = u₃</td><td>0</td><td>none on the real loop — frozen</td><td>—</td><td>r ≥ 1/√2 exactly (conserved channel q₃ ≠ 0); clears only at t = ±i on the complexified conic — frozen is family-relative</td></tr>
      </tbody>
    </table>
    </div>
    <p class="note">Every crossing pair satisfies t₊·t₋ = −1 exactly, and antipodal walls have
    <em>identical</em> angular crossing strength |dr/dθ| = √((q₁²+q₂²)/2) — the differing slopes in
    the t-chart are stereographic artifacts (dθ/dt = 2/(1+t²)). In the angular coordinate the whole
    instrument is one formula: z_γ(θ) = (q₁cosθ + q₂sinθ + i·q₃)/√2, with r = |z| — a rotating
    channel plus a conserved channel. D's floor is the conserved channel: a class whose residue has a
    component along a direction conserved by the family cannot clear on that family (though it does
    clear at t = ±i on the complexified twistor line — frozen is family-relative). One more structure:
    the residue is invariant under the permanent rank-19 lattice N, so it factors through Λ/N ≅ ℤ³ —
    a wall clears an entire coset at once (isotropic, root, and positive-square lifts together); the
    class labels here are lift-specific readings of their wall, not intrinsic wall types.</p>
  </div>

  <div class="panel">
    <p class="paneltitle">Wall densification — distinct wall directions by height bound H</p>
    <div class="tablewrap">
    <table>
      <thead><tr><th>H</th><th>primitive directions [q₁ : q₂]</th><th>walls on the loop</th></tr></thead>
      <tbody>{density_rows}</tbody>
    </table>
    </div>
    <p class="note">Walls of the full lattice are dense — the Noether–Lefschetz picture. Each is cut by
    an explicit rational quadratic (here) and by an algebraic equation in general
    (Cattani–Deligne–Kaplan): residue-free-ness is polynomially certified even where cycles are
    hard to construct.</p>
  </div>

  <details>
    <summary>table view — sampled r(γ, t) values (t = k/8)</summary>
    <div class="tablewrap">{sample_table}</div>
  </details>

  <p class="note">Instrument: <code>k3_residue_angle.py</code> (exact sympy; all identities asserted
  identically in t). Setting: Λ = U³ ⊕ E₈(−1)², ω(t) = (1−t²)P₁ + 2tP₂ + i(1+t²)P₃ with
  P_i = u_i + v_i; r(γ,t)² = 2|Q(γ,ω)|²/Q(ω,ω̄). Companion: "The Ledger Reading" essay and the
  two-meters Weil-class suite. Interpretation layer only — the mathematics shown is classical.</p>
</div>

<script type="application/json" id="d">{json_blob}</script>
<script>
(function () {{
  var data = JSON.parse(document.getElementById('d').textContent).curves;
  var svg = document.querySelector('#cw svg'), hit = document.getElementById('hit'),
      xh = document.getElementById('xh'), tip = document.getElementById('tip'),
      cw = document.getElementById('cw');
  var ML = {ML}, PW = {PW}, TMIN = {TMIN}, TMAX = {TMAX};
  function px2t(px) {{ return TMIN + (px - ML) / PW * (TMAX - TMIN); }}
  function t2px(tv) {{ return ML + (tv - TMIN) / (TMAX - TMIN) * PW; }}
  hit.addEventListener('mousemove', function (ev) {{
    var pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
    var loc = pt.matrixTransform(svg.getScreenCTM().inverse());
    var tv = Math.max(TMIN, Math.min(TMAX, px2t(loc.x)));
    var i = Math.round((tv - TMIN) * 8);
    var ts = TMIN + i / 8;
    xh.setAttribute('x1', t2px(ts)); xh.setAttribute('x2', t2px(ts));
    xh.style.opacity = 1;
    var rows = 't = ' + ts.toFixed(3);
    data.forEach(function (c) {{ rows += '<br>' + c.n + ' · r = ' + c.s[i][1].toFixed(3); }});
    tip.innerHTML = rows;
    var wr = cw.getBoundingClientRect();
    tip.style.left = Math.min(ev.clientX - wr.left + 14, wr.width - 150) + 'px';
    tip.style.top = (ev.clientY - wr.top + 10) + 'px';
    tip.style.opacity = 1;
  }});
  hit.addEventListener('mouseleave', function () {{
    xh.style.opacity = 0; tip.style.opacity = 0;
  }});
}})();
</script>
"""

with open(OUT, "w") as fh:
    fh.write(html)
print("wrote", OUT, len(html), "bytes")
