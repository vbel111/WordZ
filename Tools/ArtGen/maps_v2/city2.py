"""Word Z - City map v3: high-angle 3/4 view of a riverside old town (reference: user's city mock).

python3 build.py out_dir city   (build.py prefers this module for 'city')

Composition (1080 x 2400, parallax background behind the level path):
  sky + sun + clouds -> hazy skyline with TV tower -> winding river with stone embankments and arched
  bridges -> townhouse blocks on both banks, dome hall top-left, clock tower + fountain plaza right,
  striped cafe bottom-left -> big foreground tree canopies framing the bottom corners.
Light from the upper right (sun), warm-brown outlines, saturated candy colours.
"""
import math
from style import OL, PALETTE, mix, shade, svg, lin, rad, contact_shadow, cloud, bird, rng

W, H = 1080, 2400
HY = 470                       # horizon
R = rng(7)


def S(y):
    """depth scale: tiny at the horizon, big at the bottom edge"""
    return 0.28 + 1.05 * max(0.0, (y - HY)) / (H - HY)


def sw(s, k=4.2):
    return max(1.6, k * s)


def pts(p):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in p)


def poly(p, fill, stroke=OL, w=None, extra=''):
    st = f' stroke="{stroke}" stroke-width="{w:.1f}" stroke-linejoin="round"' if w else ''
    return f'<polygon points="{pts(p)}" fill="{fill}"{st} {extra}/>'


# ----------------------------------------------------------------- river geometry

RIVER = [(990, 470), (900, 560), (760, 660), (560, 800), (400, 960), (330, 1110), (380, 1270),
         (540, 1420), (760, 1560), (960, 1680), (1160, 1780)]


def catmull(points, n=24):
    out = []
    P = [points[0]] + points + [points[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 +
                                    (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(points[-1])
    return out


CL = catmull(RIVER)


def river_width(y):
    return 56 + 330 * max(0.0, y - HY) / (H - HY)


def banks(extra=0.0):
    """left/right bank polylines (screen space, ground plane squashed vertically)"""
    L, Rr = [], []
    for i, (x, y) in enumerate(CL):
        a = CL[max(0, i - 1)]
        b = CL[min(len(CL) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        hw = river_width(y) / 2 + extra * S(y)
        L.append((x + nx * hw, y + ny * hw * 0.55))
        Rr.append((x - nx * hw, y - ny * hw * 0.55))
    return L, Rr


def river_at(y):
    """centre x of the river at screen row y"""
    best = min(CL, key=lambda p: abs(p[1] - y))
    return best[0]


# ----------------------------------------------------------------- props

def fluffy_tree(x, y, s, c='#5CBF3F', seed=0):
    r = rng(seed)
    dark, mid, light = shade(c, -0.28), c, shade(c, 0.32)
    blobs = [(-30, -70, 34), (26, -76, 32), (0, -104, 38), (-14, -60, 30), (20, -50, 26)]
    blobs = [(bx + r.uniform(-5, 5), by + r.uniform(-5, 5), br * r.uniform(0.9, 1.1)) for bx, by, br in blobs]
    out = [contact_shadow(x - 10 * s, y + 2 * s, 52 * s, 12 * s, 0.25)]
    out.append(f'<path d="M{x - 8 * s:.1f} {y:.1f} L{x - 5 * s:.1f} {y - 52 * s:.1f} L{x + 5 * s:.1f} {y - 52 * s:.1f} L{x + 8 * s:.1f} {y:.1f} Z" '
               f'fill="#8A5326" stroke="{OL}" stroke-width="{sw(s):.1f}" stroke-linejoin="round"/>')
    # outlined silhouette
    out.append(f'<g fill="{dark}" stroke="{OL}" stroke-width="{sw(s):.1f}">' +
               ''.join(f'<circle cx="{x + bx * s:.1f}" cy="{y + by * s:.1f}" r="{br * s:.1f}"/>' for bx, by, br in blobs) + '</g>')
    out.append(f'<g fill="{dark}">' + ''.join(f'<circle cx="{x + bx * s:.1f}" cy="{y + by * s:.1f}" r="{br * s - sw(s) / 2:.1f}"/>' for bx, by, br in blobs) + '</g>')
    # lit side (sun upper right)
    out.append(f'<g fill="{mid}">' + ''.join(f'<circle cx="{x + (bx + 5) * s:.1f}" cy="{y + (by - 5) * s:.1f}" r="{br * 0.78 * s:.1f}"/>' for bx, by, br in blobs) + '</g>')
    out.append(f'<g fill="{light}">' + ''.join(f'<circle cx="{x + (bx + 11) * s:.1f}" cy="{y + (by - 12) * s:.1f}" r="{br * 0.36 * s:.1f}"/>' for bx, by, br in blobs[:3]) + '</g>')
    return ''.join(out)


def poplar(x, y, s, c='#4FA843'):
    dark, light = shade(c, -0.25), shade(c, 0.3)
    k = sw(s)
    return (contact_shadow(x - 6 * s, y + 2 * s, 26 * s, 8 * s, 0.25) +
            f'<rect x="{x - 4 * s:.1f}" y="{y - 30 * s:.1f}" width="{8 * s:.1f}" height="{30 * s:.1f}" fill="#8A5326" stroke="{OL}" stroke-width="{k:.1f}"/>' +
            f'<ellipse cx="{x:.1f}" cy="{y - 100 * s:.1f}" rx="{28 * s:.1f}" ry="{78 * s:.1f}" fill="{dark}" stroke="{OL}" stroke-width="{k:.1f}"/>' +
            f'<ellipse cx="{x + 5 * s:.1f}" cy="{y - 106 * s:.1f}" rx="{19 * s:.1f}" ry="{64 * s:.1f}" fill="{c}"/>' +
            f'<ellipse cx="{x + 10 * s:.1f}" cy="{y - 130 * s:.1f}" rx="{7 * s:.1f}" ry="{26 * s:.1f}" fill="{light}"/>')


def lamp(x, y, s):
    k = sw(s, 3.6)
    post = '#2E3440'
    return (contact_shadow(x, y, 12 * s, 4 * s, 0.25) +
            f'<g stroke="{OL}" stroke-width="{k:.1f}" stroke-linejoin="round">'
            f'<rect x="{x - 4 * s:.1f}" y="{y - 118 * s:.1f}" width="{8 * s:.1f}" height="{118 * s:.1f}" fill="{post}"/>'
            f'<rect x="{x - 9 * s:.1f}" y="{y - 12 * s:.1f}" width="{18 * s:.1f}" height="{12 * s:.1f}" fill="{post}"/>'
            f'<path d="M{x - 12 * s:.1f} {y - 118 * s:.1f} L{x + 12 * s:.1f} {y - 118 * s:.1f} L{x + 15 * s:.1f} {y - 146 * s:.1f} L{x - 15 * s:.1f} {y - 146 * s:.1f} Z" fill="#FFE27A"/>'
            f'<path d="M{x - 18 * s:.1f} {y - 146 * s:.1f} L{x + 18 * s:.1f} {y - 146 * s:.1f} L{x:.1f} {y - 162 * s:.1f} Z" fill="{post}"/></g>'
            f'<circle cx="{x:.1f}" cy="{y - 132 * s:.1f}" r="{30 * s:.1f}" fill="#FFE9A6" opacity="0.28"/>')


def townhouse(x, by, w, h, s, wall, roof, side='r', dep=None, floors=3, cols=3, seed=0, shop=None, flowers=True, roof_kind='gable'):
    """3/4 box townhouse. (x, by) = front bottom-left corner."""
    r = rng(seed)
    dep = dep if dep is not None else w * 0.55
    dx = dep * 0.62 * (1 if side == 'r' else -1)
    dy = -dep * 0.5
    k = sw(s)
    sideC = shade(wall, -0.2)
    out = [contact_shadow(x + w / 2 + dx / 2, by + 4 * s, w * 0.75, 14 * s, 0.22)]
    # side face
    if side == 'r':
        sf = [(x + w, by), (x + w + dx, by + dy), (x + w + dx, by - h + dy), (x + w, by - h)]
    else:
        sf = [(x, by), (x + dx, by + dy), (x + dx, by - h + dy), (x, by - h)]
    out.append(poly(sf, sideC, w=k))
    # front face
    out.append(f'<rect x="{x:.1f}" y="{by - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{wall}" stroke="{OL}" stroke-width="{k:.1f}" stroke-linejoin="round"/>')
    # sunlit strip on the right edge of the front
    out.append(f'<rect x="{x + w - 8 * s:.1f}" y="{by - h + k:.1f}" width="{6 * s:.1f}" height="{h - 2 * k:.1f}" fill="#FFFFFF" opacity="0.22"/>')
    # cornice band
    out.append(f'<rect x="{x - 4 * s:.1f}" y="{by - h - 2 * s:.1f}" width="{w + 8 * s:.1f}" height="{10 * s:.1f}" fill="{shade(wall, 0.35)}" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
    # side windows
    ground = h * 0.26 if shop else 0
    fh = (h - ground - 16 * s) / floors
    for f in range(floors):
        wy0 = by - h + 16 * s + f * fh
        for j in range(2):
            t0, t1 = 0.22 + j * 0.4, 0.42 + j * 0.4
            ex = x + w if side == 'r' else x
            p = [(ex + dx * t0, wy0 + fh * 0.22 + dy * t0), (ex + dx * t1, wy0 + fh * 0.22 + dy * t1),
                 (ex + dx * t1, wy0 + fh * 0.72 + dy * t1), (ex + dx * t0, wy0 + fh * 0.72 + dy * t0)]
            out.append(poly(p, shade(PALETTE['window'], -0.25), w=k * 0.7))
    # front windows
    mw = w / (cols * 1.7 + 0.7)
    for f in range(floors):
        wy = by - h + 16 * s + f * fh + fh * 0.18
        wh = fh * 0.58
        for c in range(cols):
            wx = x + mw * 0.7 + c * mw * 1.7
            lit = r.random() < 0.18
            glass = PALETTE['windowLit'] if lit else PALETTE['window']
            out.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{mw:.1f}" height="{wh:.1f}" rx="{mw * 0.18:.1f}" fill="{glass}" stroke="{OL}" stroke-width="{k * 0.75:.1f}"/>')
            out.append(f'<rect x="{wx + mw * 0.12:.1f}" y="{wy + wh * 0.1:.1f}" width="{mw * 0.3:.1f}" height="{wh * 0.35:.1f}" fill="#FFFFFF" opacity="0.55"/>')
            out.append(f'<line x1="{wx + mw / 2:.1f}" y1="{wy:.1f}" x2="{wx + mw / 2:.1f}" y2="{wy + wh:.1f}" stroke="{OL}" stroke-width="{k * 0.45:.1f}"/>')
            # sill
            out.append(f'<rect x="{wx - mw * 0.12:.1f}" y="{wy + wh - 1:.1f}" width="{mw * 1.24:.1f}" height="{5 * s:.1f}" fill="{shade(wall, 0.4)}" stroke="{OL}" stroke-width="{k * 0.5:.1f}"/>')
            if flowers and r.random() < 0.45:
                fc = r.choice(['#FF5E7E', '#FF8A3D', '#FFD23F', '#F05AB4'])
                out.append(f'<rect x="{wx - mw * 0.05:.1f}" y="{wy + wh + 3 * s:.1f}" width="{mw * 1.1:.1f}" height="{7 * s:.1f}" fill="#4E9F36" stroke="{OL}" stroke-width="{k * 0.45:.1f}"/>')
                for q in range(4):
                    out.append(f'<circle cx="{wx + mw * (0.1 + q * 0.27):.1f}" cy="{wy + wh + 3 * s:.1f}" r="{3.4 * s:.1f}" fill="{fc}"/>')
    # ground floor shop / door
    if shop:
        gy = by - ground
        out.append(f'<rect x="{x + 6 * s:.1f}" y="{gy + 8 * s:.1f}" width="{w - 12 * s:.1f}" height="{ground - 8 * s:.1f}" fill="{shade(wall, -0.1)}"/>')
        # big shop window + door
        out.append(f'<rect x="{x + w * 0.1:.1f}" y="{gy + ground * 0.38:.1f}" width="{w * 0.48:.1f}" height="{ground * 0.55:.1f}" rx="{4 * s:.1f}" fill="{PALETTE["windowLit"]}" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
        out.append(f'<rect x="{x + w * 0.66:.1f}" y="{gy + ground * 0.36:.1f}" width="{w * 0.22:.1f}" height="{ground * 0.64:.1f}" rx="{6 * s:.1f}" fill="#8A5326" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
        # striped awning
        n = 7
        aw_y = gy + 6 * s
        stripe = w / n
        for q in range(n):
            col = shop if q % 2 == 0 else '#FFFFFF'
            out.append(f'<path d="M{x + q * stripe:.1f} {aw_y:.1f} L{x + (q + 1) * stripe:.1f} {aw_y:.1f} L{x + (q + 1) * stripe + 4 * s:.1f} {aw_y + ground * 0.3:.1f} '
                       f'L{x + q * stripe + 4 * s:.1f} {aw_y + ground * 0.3:.1f} Z" fill="{col}"/>')
            out.append(f'<path d="M{x + q * stripe + 4 * s:.1f} {aw_y + ground * 0.3:.1f} a{stripe / 2:.1f} {stripe / 2.4:.1f} 0 0 0 {stripe:.1f} 0 Z" fill="{col}" stroke="{OL}" stroke-width="{k * 0.6:.1f}"/>')
        out.append(f'<path d="M{x:.1f} {aw_y:.1f} L{x + w:.1f} {aw_y:.1f} L{x + w + 4 * s:.1f} {aw_y + ground * 0.3:.1f} L{x + 4 * s:.1f} {aw_y + ground * 0.3:.1f} Z" fill="none" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
    else:
        out.append(f'<rect x="{x + w * 0.4:.1f}" y="{by - fh * 0.62:.1f}" width="{w * 0.2:.1f}" height="{fh * 0.62:.1f}" rx="{w * 0.1:.1f}" fill="#8A5326" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
    # roof
    top = by - h - 2 * s
    ov = 8 * s
    if roof_kind == 'flat':
        tp = [(x - ov, top), (x + w + ov, top), (x + w + ov + dx, top + dy), (x - ov + dx, top + dy)]
        out.append(poly(tp, shade(wall, -0.05), w=k))
        out.append(f'<rect x="{x + w * 0.25 + dx * 0.5:.1f}" y="{top + dy * 0.5 - 22 * s:.1f}" width="{w * 0.18:.1f}" height="{22 * s:.1f}" fill="#A8642E" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
    else:
        rh = min(w * 0.42, 70 * s) if roof_kind == 'gable' else min(w * 0.6, 95 * s)
        r1 = (x + dx * 0.5, top + dy * 0.5 - rh)
        r2 = (x + w + dx * 0.5, top + dy * 0.5 - rh)
        if side == 'r':
            gab = [(x + w, top), (x + w + dx, top + dy), r2]
        else:
            gab = [(x, top), (x + dx, top + dy), r1]
        out.append(poly(gab, shade(wall, -0.12), w=k))
        front = [(x - ov, top + 2 * s), (x + w + ov, top + 2 * s), (r2[0] + ov * 0.3, r2[1]), (r1[0] - ov * 0.3, r1[1])]
        out.append(poly(front, roof, w=k))
        # roof tiles hint + sunlit ridge
        for q in range(1, 4):
            t = q / 4
            a = (front[0][0] + (front[3][0] - front[0][0]) * t, front[0][1] + (front[3][1] - front[0][1]) * t)
            b = (front[1][0] + (front[2][0] - front[1][0]) * t, front[1][1] + (front[2][1] - front[1][1]) * t)
            out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{shade(roof, -0.25)}" stroke-width="{k * 0.6:.1f}"/>')
        out.append(f'<line x1="{r1[0]:.1f}" y1="{r1[1] + 3 * s:.1f}" x2="{r2[0]:.1f}" y2="{r2[1] + 3 * s:.1f}" stroke="{shade(roof, 0.35)}" stroke-width="{k * 0.9:.1f}"/>')
        # dormer
        if w > 90 * s and r.random() < 0.7:
            cx = x + w * r.uniform(0.35, 0.6)
            dy0 = top - rh * 0.35
            dwid = w * 0.18
            out.append(f'<path d="M{cx - dwid / 2:.1f} {dy0 + 14 * s:.1f} L{cx - dwid / 2:.1f} {dy0 - 6 * s:.1f} L{cx:.1f} {dy0 - 20 * s:.1f} L{cx + dwid / 2:.1f} {dy0 - 6 * s:.1f} L{cx + dwid / 2:.1f} {dy0 + 14 * s:.1f} Z" '
                       f'fill="{shade(wall, 0.2)}" stroke="{OL}" stroke-width="{k * 0.8:.1f}" stroke-linejoin="round"/>')
            out.append(f'<rect x="{cx - dwid * 0.25:.1f}" y="{dy0 - 4 * s:.1f}" width="{dwid * 0.5:.1f}" height="{14 * s:.1f}" fill="{PALETTE["window"]}" stroke="{OL}" stroke-width="{k * 0.5:.1f}"/>')
        # chimney
        if r.random() < 0.6:
            cx = x + w * r.uniform(0.15, 0.3) + dx * 0.3
            cy = top + dy * 0.3 - rh * 0.6
            out.append(f'<rect x="{cx:.1f}" y="{cy - 26 * s:.1f}" width="{14 * s:.1f}" height="{30 * s:.1f}" fill="#C0583A" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
    return ''.join(out)


def dome_hall(x, by, s):
    w, h = 190 * s, 170 * s
    k = sw(s)
    out = [townhouse(x, by, w, h, s, '#F3E1C0', '#5C6B80', side='r', floors=2, cols=4, seed=31, flowers=False, roof_kind='flat')]
    cx = x + w / 2 + 30 * s
    base = by - h - 34 * s
    # drum
    out.append(f'<rect x="{cx - 52 * s:.1f}" y="{base - 60 * s:.1f}" width="{104 * s:.1f}" height="{64 * s:.1f}" fill="#F7EAD0" stroke="{OL}" stroke-width="{k:.1f}"/>')
    for q in range(5):
        out.append(f'<rect x="{cx - 44 * s + q * 20 * s:.1f}" y="{base - 50 * s:.1f}" width="{9 * s:.1f}" height="{36 * s:.1f}" rx="{4 * s:.1f}" fill="#9FD3F2" stroke="{OL}" stroke-width="{k * 0.6:.1f}"/>')
    # dome
    out.append(f'<path d="M{cx - 58 * s:.1f} {base - 58 * s:.1f} Q{cx - 58 * s:.1f} {base - 150 * s:.1f} {cx:.1f} {base - 152 * s:.1f} Q{cx + 58 * s:.1f} {base - 150 * s:.1f} {cx + 58 * s:.1f} {base - 58 * s:.1f} Z" '
               f'fill="#4F6E86" stroke="{OL}" stroke-width="{k:.1f}"/>')
    out.append(f'<path d="M{cx + 10 * s:.1f} {base - 140 * s:.1f} Q{cx + 46 * s:.1f} {base - 128 * s:.1f} {cx + 48 * s:.1f} {base - 70 * s:.1f}" fill="none" stroke="#8FB3CC" stroke-width="{k * 1.6:.1f}" stroke-linecap="round"/>')
    for q in (-30, 0, 30):
        out.append(f'<path d="M{cx + q * s:.1f} {base - 58 * s:.1f} Q{cx + q * 0.6 * s:.1f} {base - 120 * s:.1f} {cx:.1f} {base - 150 * s:.1f}" fill="none" stroke="{OL}" stroke-width="{k * 0.5:.1f}" opacity="0.6"/>')
    # lantern + spire
    out.append(f'<rect x="{cx - 9 * s:.1f}" y="{base - 176 * s:.1f}" width="{18 * s:.1f}" height="{26 * s:.1f}" fill="#F7EAD0" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
    out.append(f'<path d="M{cx - 11 * s:.1f} {base - 176 * s:.1f} L{cx:.1f} {base - 212 * s:.1f} L{cx + 11 * s:.1f} {base - 176 * s:.1f} Z" fill="#4F6E86" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{base - 214 * s:.1f}" r="{4 * s:.1f}" fill="#FFC93C" stroke="{OL}" stroke-width="{k * 0.5:.1f}"/>')
    return ''.join(out)


def clock_tower(x, by, s):
    w, h = 120 * s, 470 * s
    k = sw(s)
    wall = '#F1D8A8'
    out = [townhouse(x, by, w, h, s, wall, '#2F9C9A', side='l', dep=70 * s, floors=5, cols=2, seed=41, flowers=False, roof_kind='flat')]
    top = by - h - 2 * s
    cx = x + w / 2 - 22 * s
    # clock storey
    cy = top - 70 * s
    out.append(f'<rect x="{x - 8 * s:.1f}" y="{cy - 10 * s:.1f}" width="{w + 16 * s:.1f}" height="{82 * s:.1f}" fill="{shade(wall, 0.1)}" stroke="{OL}" stroke-width="{k:.1f}"/>')
    out.append(f'<circle cx="{x + w / 2:.1f}" cy="{cy + 30 * s:.1f}" r="{30 * s:.1f}" fill="#FFFFFF" stroke="{OL}" stroke-width="{k:.1f}"/>')
    for q in range(12):
        a = q * math.pi / 6
        out.append(f'<circle cx="{x + w / 2 + math.cos(a) * 23 * s:.1f}" cy="{cy + 30 * s + math.sin(a) * 23 * s:.1f}" r="{1.8 * s:.1f}" fill="{OL}"/>')
    out.append(f'<path d="M{x + w / 2:.1f} {cy + 30 * s:.1f} L{x + w / 2:.1f} {cy + 12 * s:.1f} M{x + w / 2:.1f} {cy + 30 * s:.1f} L{x + w / 2 + 13 * s:.1f} {cy + 36 * s:.1f}" stroke="{OL}" stroke-width="{k * 0.8:.1f}" stroke-linecap="round"/>')
    # spire
    sp = [(x - 14 * s, cy - 10 * s), (x + w + 14 * s, cy - 10 * s), (x + w / 2, cy - 190 * s)]
    out.append(poly(sp, '#2F9C9A', w=k))
    out.append(poly([(x + w / 2, cy - 190 * s), (x + w + 14 * s, cy - 10 * s), (x + w * 0.62, cy - 10 * s)], shade('#2F9C9A', 0.25)))
    out.append(f'<line x1="{x + w / 2:.1f}" y1="{cy - 190 * s:.1f}" x2="{x + w / 2:.1f}" y2="{cy - 222 * s:.1f}" stroke="{OL}" stroke-width="{k:.1f}"/>')
    out.append(f'<circle cx="{x + w / 2:.1f}" cy="{cy - 224 * s:.1f}" r="{5 * s:.1f}" fill="#FFC93C" stroke="{OL}" stroke-width="{k * 0.6:.1f}"/>')
    return ''.join(out)


def bridge(idx, color='#E3CDA0'):
    """humpback stone bridge across the river at centre-line sample idx. Returns (sort_y, svg)."""
    L, Rr = banks(34)
    a, b = L[idx], Rr[idx]
    if a[0] > b[0]:
        a, b = b, a
    s = S((a[1] + b[1]) / 2)
    k = sw(s)
    hump = 34 * s
    face = 46 * s
    ddx, ddy = 14 * s, -30 * s                 # deck depth (3/4 view)
    m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - hump * 2)
    a2, b2, m2 = (a[0] + ddx, a[1] + ddy), (b[0] + ddx, b[1] + ddy), (m[0] + ddx, m[1] + ddy)
    out = []
    # far parapet
    out.append(f'<path d="M{a2[0]:.1f} {a2[1]:.1f} Q{m2[0]:.1f} {m2[1]:.1f} {b2[0]:.1f} {b2[1]:.1f}" fill="none" stroke="{OL}" stroke-width="{18 * s + 2 * k:.1f}" stroke-linecap="round"/>')
    out.append(f'<path d="M{a2[0]:.1f} {a2[1]:.1f} Q{m2[0]:.1f} {m2[1]:.1f} {b2[0]:.1f} {b2[1]:.1f}" fill="none" stroke="{shade(color, -0.05)}" stroke-width="{18 * s:.1f}" stroke-linecap="round"/>')
    # deck surface
    out.append(f'<path d="M{a[0]:.1f} {a[1]:.1f} Q{m[0]:.1f} {m[1]:.1f} {b[0]:.1f} {b[1]:.1f} L{b2[0]:.1f} {b2[1]:.1f} Q{m2[0]:.1f} {m2[1]:.1f} {a2[0]:.1f} {a2[1]:.1f} Z" '
               f'fill="{shade(color, 0.12)}" stroke="{OL}" stroke-width="{k:.1f}" stroke-linejoin="round"/>')
    # front face (curved top, straight-ish bottom on the water) with arches
    out.append(f'<path d="M{a[0]:.1f} {a[1]:.1f} Q{m[0]:.1f} {m[1]:.1f} {b[0]:.1f} {b[1]:.1f} L{b[0]:.1f} {b[1] + face:.1f} L{a[0]:.1f} {a[1] + face:.1f} Z" '
               f'fill="{shade(color, -0.1)}" stroke="{OL}" stroke-width="{k:.1f}" stroke-linejoin="round"/>')
    n = 3
    for q in range(n):
        t1, t2 = (q + 0.16) / n, (q + 0.84) / n
        p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1 + face)
        p2 = (a[0] + (b[0] - a[0]) * t2, a[1] + (b[1] - a[1]) * t2 + face)
        tm = (t1 + t2) / 2
        top_y = (1 - tm) ** 2 * a[1] + 2 * (1 - tm) * tm * m[1] + tm ** 2 * b[1]
        ah = (p1[1] + p2[1]) / 2 - top_y - 16 * s
        mx = (p1[0] + p2[0]) / 2
        out.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} C{p1[0]:.1f} {p1[1] - ah * 1.2:.1f} {p2[0]:.1f} {p2[1] - ah * 1.2:.1f} {p2[0]:.1f} {p2[1]:.1f} Z" '
                   f'fill="#2B7DB8" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
        out.append(f'<path d="M{p1[0] + 5 * s:.1f} {p1[1] - 4 * s:.1f} C{p1[0] + 5 * s:.1f} {p1[1] - ah * 1.05:.1f} {p2[0] - 5 * s:.1f} {p2[1] - ah * 1.05:.1f} {p2[0] - 5 * s:.1f} {p2[1] - 4 * s:.1f}" '
                   f'fill="none" stroke="{shade(color, 0.3)}" stroke-width="{k * 0.8:.1f}"/>')
        out.append(f'<ellipse cx="{mx:.1f}" cy="{(p1[1] + p2[1]) / 2 + 4 * s:.1f}" rx="{(p2[0] - p1[0]) * 0.45:.1f}" ry="{5 * s:.1f}" fill="#FFFFFF" opacity="0.35"/>')
    # near parapet
    out.append(f'<path d="M{a[0]:.1f} {a[1] - 6 * s:.1f} Q{m[0]:.1f} {m[1] - 6 * s:.1f} {b[0]:.1f} {b[1] - 6 * s:.1f}" fill="none" stroke="{OL}" stroke-width="{16 * s + 2 * k:.1f}" stroke-linecap="round"/>')
    out.append(f'<path d="M{a[0]:.1f} {a[1] - 6 * s:.1f} Q{m[0]:.1f} {m[1] - 6 * s:.1f} {b[0]:.1f} {b[1] - 6 * s:.1f}" fill="none" stroke="{color}" stroke-width="{16 * s:.1f}" stroke-linecap="round"/>')
    out.append(f'<path d="M{a[0]:.1f} {a[1] - 10 * s:.1f} Q{m[0]:.1f} {m[1] - 10 * s:.1f} {b[0]:.1f} {b[1] - 10 * s:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{3 * s:.1f}" opacity="0.5" stroke-linecap="round"/>')
    for p in (a, b):
        out.append(lamp(p[0], p[1] - 4 * s, s * 0.6))
    return max(a[1], b[1]) + face, ''.join(out)


def boat(x, y, s, c='#E5533D', sail=False):
    k = sw(s)
    out = [f'<ellipse cx="{x:.1f}" cy="{y + 6 * s:.1f}" rx="{58 * s:.1f}" ry="{9 * s:.1f}" fill="#FFFFFF" opacity="0.45"/>']
    hull = f'M{x - 48 * s:.1f} {y - 14 * s:.1f} L{x + 52 * s:.1f} {y - 14 * s:.1f} L{x + 38 * s:.1f} {y + 4 * s:.1f} L{x - 40 * s:.1f} {y + 4 * s:.1f} Z'
    out.append(f'<path d="{hull}" fill="#FFFFFF" stroke="{OL}" stroke-width="{k:.1f}" stroke-linejoin="round"/>')
    out.append(f'<rect x="{x - 44 * s:.1f}" y="{y - 8 * s:.1f}" width="{88 * s:.1f}" height="{5 * s:.1f}" fill="{c}"/>')
    if sail:
        out.append(f'<line x1="{x:.1f}" y1="{y - 14 * s:.1f}" x2="{x:.1f}" y2="{y - 96 * s:.1f}" stroke="{OL}" stroke-width="{k:.1f}"/>')
        out.append(f'<path d="M{x + 3 * s:.1f} {y - 92 * s:.1f} L{x + 40 * s:.1f} {y - 22 * s:.1f} L{x + 3 * s:.1f} {y - 22 * s:.1f} Z" fill="#FFFFFF" stroke="{OL}" stroke-width="{k:.1f}" stroke-linejoin="round"/>')
        out.append(f'<path d="M{x - 3 * s:.1f} {y - 80 * s:.1f} L{x - 30 * s:.1f} {y - 22 * s:.1f} L{x - 3 * s:.1f} {y - 22 * s:.1f} Z" fill="#FFF3D6" stroke="{OL}" stroke-width="{k:.1f}" stroke-linejoin="round"/>')
    else:
        out.append(f'<rect x="{x - 22 * s:.1f}" y="{y - 36 * s:.1f}" width="{44 * s:.1f}" height="{22 * s:.1f}" rx="{5 * s:.1f}" fill="#F3E1C0" stroke="{OL}" stroke-width="{k:.1f}"/>')
        out.append(f'<rect x="{x - 16 * s:.1f}" y="{y - 31 * s:.1f}" width="{32 * s:.1f}" height="{9 * s:.1f}" fill="{PALETTE["window"]}"/>')
    return ''.join(out)


def fountain(x, y, s):
    k = sw(s)
    out = [contact_shadow(x, y + 6 * s, 120 * s, 26 * s, 0.2)]
    out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{115 * s:.1f}" ry="{40 * s:.1f}" fill="#E8D7B4" stroke="{OL}" stroke-width="{k:.1f}"/>')
    out.append(f'<path d="M{x - 115 * s:.1f} {y:.1f} L{x - 115 * s:.1f} {y + 18 * s:.1f} A{115 * s:.1f} {40 * s:.1f} 0 0 0 {x + 115 * s:.1f} {y + 18 * s:.1f} L{x + 115 * s:.1f} {y:.1f}" fill="#CDB68C" stroke="{OL}" stroke-width="{k:.1f}"/>')
    out.append(f'<ellipse cx="{x:.1f}" cy="{y - 2 * s:.1f}" rx="{98 * s:.1f}" ry="{31 * s:.1f}" fill="#5BC0F0"/>')
    out.append(f'<ellipse cx="{x - 20 * s:.1f}" cy="{y - 8 * s:.1f}" rx="{50 * s:.1f}" ry="{10 * s:.1f}" fill="#BDEBFF" opacity="0.8"/>')
    # column + bowl
    out.append(f'<rect x="{x - 9 * s:.1f}" y="{y - 70 * s:.1f}" width="{18 * s:.1f}" height="{66 * s:.1f}" fill="#E8D7B4" stroke="{OL}" stroke-width="{k:.1f}"/>')
    out.append(f'<path d="M{x - 46 * s:.1f} {y - 72 * s:.1f} Q{x:.1f} {y - 40 * s:.1f} {x + 46 * s:.1f} {y - 72 * s:.1f} Z" fill="#E8D7B4" stroke="{OL}" stroke-width="{k:.1f}"/>')
    for q in (-1, 1):
        out.append(f'<path d="M{x:.1f} {y - 110 * s:.1f} Q{x + q * 40 * s:.1f} {y - 128 * s:.1f} {x + q * 62 * s:.1f} {y - 16 * s:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{k * 1.3:.1f}" stroke-linecap="round" opacity="0.9"/>')
    out.append(f'<path d="M{x:.1f} {y - 72 * s:.1f} L{x:.1f} {y - 118 * s:.1f}" stroke="#FFFFFF" stroke-width="{k * 1.6:.1f}" stroke-linecap="round"/>')
    for q in range(10):
        a = q / 10 * math.pi * 2
        out.append(f'<circle cx="{x + math.cos(a) * 70 * s:.1f}" cy="{y - 6 * s + math.sin(a) * 20 * s:.1f}" r="{3 * s:.1f}" fill="#FFFFFF" opacity="0.85"/>')
    return ''.join(out)


def parasol(x, y, s, c='#E5533D'):
    k = sw(s)
    out = [contact_shadow(x, y + 2 * s, 40 * s, 8 * s, 0.22)]
    out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 74 * s:.1f}" stroke="{OL}" stroke-width="{k:.1f}"/>')
    out.append(f'<ellipse cx="{x:.1f}" cy="{y - 18 * s:.1f}" rx="{22 * s:.1f}" ry="{7 * s:.1f}" fill="#FFFFFF" stroke="{OL}" stroke-width="{k * 0.8:.1f}"/>')
    n = 6
    for q in range(n):
        x0 = x - 52 * s + q * (104 * s / n)
        col = c if q % 2 == 0 else '#FFFFFF'
        out.append(f'<path d="M{x:.1f} {y - 96 * s:.1f} L{x0:.1f} {y - 66 * s:.1f} L{x0 + 104 * s / n:.1f} {y - 66 * s:.1f} Z" fill="{col}"/>')
    out.append(f'<path d="M{x:.1f} {y - 96 * s:.1f} L{x - 52 * s:.1f} {y - 66 * s:.1f} Q{x:.1f} {y - 56 * s:.1f} {x + 52 * s:.1f} {y - 66 * s:.1f} Z" fill="none" stroke="{OL}" stroke-width="{k:.1f}" stroke-linejoin="round"/>')
    return ''.join(out)


def flowerbed(x, y, s, seed=0):
    r = rng(seed)
    k = sw(s, 3)
    out = [f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{46 * s:.1f}" ry="{16 * s:.1f}" fill="#7A4A26" stroke="{OL}" stroke-width="{k:.1f}"/>']
    for q in range(14):
        a = r.uniform(0, math.pi * 2)
        rr = r.uniform(0, 1) ** 0.5
        c = r.choice(['#FF5E7E', '#FFD23F', '#FF8A3D', '#FFFFFF', '#F05AB4'])
        out.append(f'<circle cx="{x + math.cos(a) * 36 * rr * s:.1f}" cy="{y - 4 * s + math.sin(a) * 11 * rr * s:.1f}" r="{5 * s:.1f}" fill="#4E9F36"/>')
        out.append(f'<circle cx="{x + math.cos(a) * 36 * rr * s:.1f}" cy="{y - 8 * s + math.sin(a) * 11 * rr * s:.1f}" r="{3.6 * s:.1f}" fill="{c}"/>')
    return ''.join(out)


def car(x, y, s, c='#FFB82E'):
    k = sw(s)
    out = [contact_shadow(x, y + 3 * s, 44 * s, 9 * s, 0.3)]
    out.append(f'<path d="M{x - 42 * s:.1f} {y - 4 * s:.1f} L{x - 42 * s:.1f} {y - 24 * s:.1f} Q{x - 38 * s:.1f} {y - 32 * s:.1f} {x - 26 * s:.1f} {y - 32 * s:.1f} L{x - 16 * s:.1f} {y - 50 * s:.1f} '
               f'L{x + 20 * s:.1f} {y - 50 * s:.1f} L{x + 30 * s:.1f} {y - 32 * s:.1f} Q{x + 42 * s:.1f} {y - 32 * s:.1f} {x + 42 * s:.1f} {y - 22 * s:.1f} L{x + 42 * s:.1f} {y - 4 * s:.1f} Z" '
               f'fill="{c}" stroke="{OL}" stroke-width="{k:.1f}" stroke-linejoin="round"/>')
    out.append(f'<path d="M{x - 11 * s:.1f} {y - 34 * s:.1f} L{x - 6 * s:.1f} {y - 44 * s:.1f} L{x + 16 * s:.1f} {y - 44 * s:.1f} L{x + 22 * s:.1f} {y - 34 * s:.1f} Z" fill="{PALETTE["window"]}" stroke="{OL}" stroke-width="{k * 0.6:.1f}"/>')
    for q in (-24, 24):
        out.append(f'<circle cx="{x + q * s:.1f}" cy="{y - 3 * s:.1f}" r="{9 * s:.1f}" fill="#33333D" stroke="{OL}" stroke-width="{k * 0.6:.1f}"/>')
    out.append(f'<rect x="{x - 34 * s:.1f}" y="{y - 28 * s:.1f}" width="{18 * s:.1f}" height="{4 * s:.1f}" rx="{2 * s:.1f}" fill="#FFFFFF" opacity="0.6"/>')
    return ''.join(out)


# ----------------------------------------------------------------- layers

def sky():
    defs = (lin('csky', [(0, '#5DB8F2', 1), (0.55, '#9FD8F8', 1), (1, '#FFF0C8', 1)]) +
            rad('csun', [(0, '#FFF6C2', 1), (0.25, '#FFE680', 0.9), (1, '#FFE680', 0)]))
    out = [f'<rect width="{W}" height="{HY + 120}" fill="url(#csky)"/>',
           f'<circle cx="880" cy="300" r="260" fill="url(#csun)" opacity="0.8"/>',
           f'<circle cx="880" cy="300" r="70" fill="#FFE47A" stroke="#F4C24A" stroke-width="6"/>',
           f'<circle cx="860" cy="282" r="44" fill="#FFF3B8" opacity="0.7"/>']
    for x, y, s, o in [(130, 120, 1.15, 1), (420, 70, 0.8, 0.95), (720, 160, 0.9, 0.9), (1000, 90, 0.95, 1), (260, 300, 0.7, 0.85), (560, 250, 0.55, 0.8)]:
        out.append(cloud(x, y, s, o))
    for x, y, s in [(640, 190, 1.0), (680, 170, 0.8), (720, 215, 0.7), (200, 230, 0.6)]:
        out.append(bird(x, y, s, o=0.55))
    return defs, ''.join(out)


def skyline():
    r = rng(3)
    out = []
    # two layers: pale far towers, then slightly bluer nearer ones with lit edges
    for layer, (haze, deep, hmin, hmax, base) in enumerate([('#C3DBF1', '#A7C6E6', 120, 260, HY + 10), ('#A9CBEA', '#7FA8D6', 60, 190, HY + 30)]):
        x = -20 - layer * 30
        while x < W + 20:
            w = r.uniform(38, 84)
            h = r.uniform(hmin, hmax)
            if 780 < x < 960:
                h *= 0.55          # keep the sun clear
            c = mix(haze, deep, r.uniform(0, 0.5))
            top = base - h
            if r.random() < 0.3:      # stepped crown
                out.append(f'<rect x="{x + w * 0.25:.1f}" y="{top - 22:.1f}" width="{w * 0.5:.1f}" height="24" fill="{c}"/>')
            out.append(f'<rect x="{x:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h + 40:.1f}" fill="{c}"/>')
            out.append(f'<rect x="{x + w - 7:.1f}" y="{top:.1f}" width="7" height="{h + 40:.1f}" fill="#FFFFFF" opacity="0.25"/>')
            for wy in range(int(top + 10), int(base + 20), 14):
                for wx in range(int(x + 6), int(x + w - 10), 12):
                    if r.random() < 0.55:
                        out.append(f'<rect x="{wx}" y="{wy}" width="5" height="7" fill="#E4F0FC" opacity="0.65"/>')
            x += w + r.uniform(-4, 14)
    # TV tower
    tx = 600
    out.append(f'<path d="M{tx - 8} {HY + 30} L{tx - 4} {HY - 200} L{tx + 4} {HY - 200} L{tx + 8} {HY + 30} Z" fill="#8FB0D6"/>')
    out.append(f'<ellipse cx="{tx}" cy="{HY - 200}" rx="22" ry="16" fill="#8FB0D6"/>')
    out.append(f'<rect x="{tx - 2}" y="{HY - 300}" width="4" height="90" fill="#8FB0D6"/>')
    # far trees band + haze
    for q in range(46):
        tx2 = q * 25 + r.uniform(-6, 6)
        out.append(f'<circle cx="{tx2:.1f}" cy="{HY + 26 + r.uniform(-4, 4):.1f}" r="{r.uniform(12, 18):.1f}" fill="#7FBF6A"/>')
    out.append(f'<rect x="0" y="{HY - 60}" width="{W}" height="110" fill="#FFF3D6" opacity="0.28"/>')
    return ''.join(out)


ROAD = [(470, 2420), (480, 2200), (360, 1980), (300, 1760), (260, 1560), (250, 1420)]
ROAD_CL = catmull(ROAD, 16)
FOUNTAIN = (900, 1520)
PLAZAS = [(890, 1500, 210, 90), (230, 1880, 240, 90)]   # cx, cy, rx, ry


def road_hit(x, y, pad):
    for rx, ry in ROAD_CL:
        if abs(ry - y) < 30 and abs(rx - x) < 66 * S(y) / 0.9 + pad:
            return True
    return False


def plaza_hit(x, y, pad=0):
    for cx, cy, rx, ry in PLAZAS:
        if ((x - cx) / (rx + pad)) ** 2 + ((y - cy) / (ry + pad * 0.5)) ** 2 < 1:
            return True
    return False


def river_hit(x, y, pad):
    if y < HY:
        return False
    best = min(CL, key=lambda p: abs(p[1] - y) + abs(p[0] - x) * 0.25)
    return math.hypot(x - best[0], (y - best[1]) * 1.6) < river_width(y) / 2 + pad


def ground():
    defs = lin('cgrass', [(0, '#A3DB6E', 1), (1, '#6CC04A', 1)])
    out = [f'<rect x="0" y="{HY + 20}" width="{W}" height="{H - HY}" fill="url(#cgrass)"/>']
    # mowed-lawn stripes for texture
    r = rng(9)
    for q in range(40):
        y = HY + 40 + q * 48
        out.append(f'<rect x="0" y="{y}" width="{W}" height="{12 * S(y):.1f}" fill="#FFFFFF" opacity="0.05"/>')
    for q in range(160):
        x, y = r.uniform(0, W), r.uniform(HY + 60, H)
        s = S(y)
        out.append(f'<path d="M{x - 6 * s:.1f} {y:.1f} q{3 * s:.1f} {-10 * s:.1f} {6 * s:.1f} 0 q{3 * s:.1f} {-12 * s:.1f} {6 * s:.1f} 0" fill="#4E9F36" opacity="0.55"/>')
    # paved plazas
    for cx, cy, rx, ry in PLAZAS:
        out.append(f'<ellipse cx="{cx}" cy="{cy + 6}" rx="{rx}" ry="{ry}" fill="#C9B184"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#EEDDB8" stroke="{OL}" stroke-width="4"/>')
        for q in range(1, 4):
            out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * q / 4:.0f}" ry="{ry * q / 4:.0f}" fill="none" stroke="#D8C39A" stroke-width="3"/>')
    # main street from the bottom edge up to the riverside quay
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in ROAD_CL)
    for wdt, col in [(150, OL), (140, '#E9D7B0'), (110, '#8E99A6'), (100, '#9AA5B1')]:
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wdt}" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-dasharray="34 30" opacity="0.85"/>')
    return defs, ''.join(out)


def river():
    L, Rr = banks(0)
    L2, R2 = banks(26)
    outer = L2 + R2[::-1]
    water = L + Rr[::-1]
    shift = [(x, y + 16 * S(y)) for x, y in L] + [(x, y + 16 * S(y)) for x, y in Rr[::-1]]
    defs = (lin('cwater', [(0, '#7DD3F7', 1), (1, '#2E9BE0', 1)]) +
            f'<clipPath id="cwclip"><polygon points="{pts(water)}"/></clipPath>')
    out = [poly(outer, '#E6D3A8', w=6),
           # embankment top highlight
           poly(water, '#B99A6C'),
           f'<g clip-path="url(#cwclip)"><polygon points="{pts(shift)}" fill="url(#cwater)"/>']
    r = rng(11)
    for i in range(0, len(CL), 2):
        x, y = CL[i]
        if y < HY + 30:
            continue
        s = S(y)
        for _ in range(2):
            ox = r.uniform(-0.38, 0.38) * river_width(y)
            out.append(f'<path d="M{x + ox - 18 * s:.1f} {y + 10 * s:.1f} q{9 * s:.1f} {-7 * s:.1f} {18 * s:.1f} 0 q{9 * s:.1f} {7 * s:.1f} {18 * s:.1f} 0" '
                       f'fill="none" stroke="#FFFFFF" stroke-width="{max(1.5, 4 * s):.1f}" stroke-linecap="round" opacity="0.75"/>')
    out.append('</g>')
    out.append(f'<polygon points="{pts(water)}" fill="none" stroke="{OL}" stroke-width="5" stroke-linejoin="round"/>')
    # bollards / railing dots on the quay
    for i in range(6, len(CL) - 4, 5):
        for P in (L2, R2):
            x, y = P[i]
            s = S(y)
            out.append(f'<rect x="{x - 3 * s:.1f}" y="{y - 14 * s:.1f}" width="{6 * s:.1f}" height="{14 * s:.1f}" fill="#5C6B80" stroke="{OL}" stroke-width="{max(1.2, 2.5 * s):.1f}"/>')
    return defs, ''.join(out)


WALLS = ['#F6C27A', '#F2A285', '#F7E2B4', '#E99A6A', '#F3D5A0', '#9FD0C8', '#F5B9A0', '#EFCB8E', '#E5644A', '#FFE0A3']
ROOFS = ['#D9583C', '#C24B34', '#4F6E86', '#5C6B80', '#E2723E', '#2F9C9A', '#B8452F']


def objects():
    items = []   # (sort_y, order, svg)
    occupied = []  # footprints (x0, y0, x1, y1) on the ground for tree scattering

    def add(y, svg_, order=0):
        items.append((y, order, svg_))

    # --- landmarks (placed first so rows flow around them) ---
    ds = S(800)
    add(800, dome_hall(30, 800, ds))
    occupied.append((10, 700, 30 + 190 * ds + 60, 820))
    cs = S(1400)
    add(1400, clock_tower(930, 1400, cs))
    occupied.append((880, 1300, 1080, 1420))
    add(FOUNTAIN[1], fountain(FOUNTAIN[0], FOUNTAIN[1], S(FOUNTAIN[1])))
    for x, y, c in [(730, 1575, '#E5533D'), (1055, 1590, '#2F9C9A'), (800, 1600, '#FFB82E')]:
        add(y, parasol(x, y, S(y), c))
    # cafe corner (bottom left) and a bank-side block (bottom right)
    add(2010, townhouse(-40, 2010, 300, 290, S(2010), '#F7E2B4', '#C24B34', side='r', floors=2, cols=3, seed=200, shop='#E5533D'))
    occupied.append((-40, 1880, 330, 2020))
    add(2080, townhouse(800, 2080, 300, 270, S(2080), '#F5B9A0', '#4F6E86', side='l', floors=2, cols=3, seed=210, shop='#2F9C9A'))
    occupied.append((700, 1960, 1080, 2090))
    for x, y in [(330, 1930), (130, 1870)]:
        add(y, parasol(x, y, S(y)))

    # --- rows of townhouses on both banks, packed like a real old town ---
    r = rng(5)
    rows = [560, 600, 645, 695, 750, 815, 885, 965, 1055, 1160, 1280, 1420, 1580, 1760]
    for ri, by in enumerate(rows):
        s = S(by)
        x = -50 + r.uniform(0, 60) * s
        row = []
        while x < W + 40:
            w = r.uniform(105, 150) * s
            h = w * r.uniform(1.0, 1.55)
            cx = x + w / 2
            blocked = (river_hit(cx, by, 30 * s) or river_hit(x, by, 10 * s) or river_hit(x + w, by, 10 * s) or
                       road_hit(cx, by, 40 * s) or plaza_hit(cx, by, 40 * s) or
                       any(o[0] - 10 < cx < o[2] + 10 and o[1] - 40 < by < o[3] + 40 for o in occupied))
            if blocked or r.random() < (0.34 if by < 820 else 0.2):
                x += w * r.uniform(0.5, 0.9)        # gap -> trees later
                continue
            side = 'r' if cx < 540 else 'l'
            row.append((x, w, h, side))
            x += w - 2 * s
        # draw left-of-centre houses left->right, right-of-centre right->left so side faces tuck behind neighbours
        left = [q for q in row if q[3] == 'r']
        right = [q for q in row if q[3] == 'l'][::-1]
        for order, (hx, w, h, side) in enumerate(left + right):
            floors = 2 if h < 150 * s else 3
            shop = r.choice([None, None, '#E5533D', '#2F9C9A', '#FFB82E']) if by > 900 else None
            add(by, townhouse(hx, by, w, h, s, r.choice(WALLS), r.choice(ROOFS), side=side, floors=floors,
                              cols=3 if w > 120 * s else 2, seed=ri * 50 + order, shop=shop), order)
            occupied.append((hx, by - 30 * s, hx + w, by + 10))

    # --- bridges ---
    for idx in (44, 112, 178):
        by, b = bridge(idx)
        add(by, b, 99)

    # --- boats on the water ---
    for idx, c, sail in [(70, '#E5533D', True), (140, '#2F9C9A', False), (205, '#E5533D', False)]:
        x, y = CL[idx]
        add(y + 10, boat(x + 12, y + 8 * S(y), S(y), c, sail))

    # --- cars on the main street ---
    for t, c in [(0.62, '#FFB82E'), (0.2, '#E5533D')]:
        x, y = ROAD_CL[int(t * (len(ROAD_CL) - 1))]
        add(y, car(x + 14 * S(y), y, S(y) * 1.1, c))

    # --- quay lamps along the river ---
    LB, RB = banks(44)
    for i in range(30, len(CL) - 6, 14):
        for P in (LB, RB):
            x, y = P[i]
            if 0 < x < W:
                add(y, lamp(x, y, S(y)))

    # --- lush tree cover in every remaining gap ---
    tr = rng(21)
    greens = ['#5CBF3F', '#6CC24A', '#4FB043', '#7DCB4E', '#58B74A']
    y = 560
    while y < 2320:
        s = S(y)
        step_y = 58 * s
        x = tr.uniform(-20, 40)
        while x < W + 20:
            if not (river_hit(x, y, 46 * s) or road_hit(x, y, 30 * s) or plaza_hit(x, y, 20) or
                    any(o[0] - 20 * s < x < o[2] + 20 * s and o[1] - 70 * s < y < o[3] + 30 * s for o in occupied)):
                roll = tr.random()
                if roll < 0.1:
                    add(y, poplar(x, y, s * tr.uniform(0.85, 1.1), tr.choice(['#4FA843', '#3E9A3F'])))
                elif roll < 0.64:
                    add(y, fluffy_tree(x + tr.uniform(-12, 12) * s, y, s * tr.uniform(0.8, 1.15), tr.choice(greens), seed=int(x * 7 + y)))
            x += tr.uniform(70, 110) * s
        y += step_y
    for i, (x, y) in enumerate([(1010, 1640), (760, 1620), (120, 1960), (560, 1700), (880, 1880)]):
        if not river_hit(x, y, 20):
            add(y, flowerbed(x, y, S(y), seed=400 + i))

    items.sort(key=lambda t: (t[0], t[1]))
    return ''.join(s for _, _, s in items)


def foreground():
    out = []
    # big canopies framing the bottom corners
    for i, (x, y, s, c) in enumerate([(70, 2440, 2.1, '#4FB043'), (1030, 2450, 2.0, '#5CBF3F'), (330, 2500, 1.7, '#6CC24A'), (780, 2520, 1.6, '#4FB043')]):
        out.append(fluffy_tree(x, y, s, c, seed=500 + i))
    # light haze toward the horizon (depth)
    out.append(lin('chaze', [(0, '#FFF6DE', 0.7), (1, '#FFF6DE', 0)]))
    out.append(f'<rect x="0" y="{HY}" width="{W}" height="340" fill="url(#chaze)"/>')
    # warm sun rays
    for a, o in [(-0.4, 0.08), (-0.2, 0.06), (0.05, 0.07)]:
        out.append(f'<path d="M880 300 L{880 + math.cos(math.pi * 0.62 + a) * 1600:.0f} {300 + math.sin(math.pi * 0.62 + a) * 1600:.0f} '
                   f'L{880 + math.cos(math.pi * 0.62 + a + 0.07) * 1600:.0f} {300 + math.sin(math.pi * 0.62 + a + 0.07) * 1600:.0f} Z" fill="#FFF3C4" opacity="{o}"/>')
    return ''.join(out)


def build():
    d1, s1 = sky()
    d2, g = ground()
    d3, rv = river()
    body = s1 + skyline() + g + rv + objects() + foreground()
    return svg(body, d1 + d2 + d3)


if __name__ == '__main__':
    import sys
    open(sys.argv[1] if len(sys.argv) > 1 else 'map_city.svg', 'w').write(build())
