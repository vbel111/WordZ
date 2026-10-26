"""v3 indoor maps (3/4 view rooms): kitchen, things (toy room)."""
import math
from style import OL, PALETTE, shade, mix, rng, lin, contact_shadow
from world import World, S, W, H, HY
from city2 import sw, poly, fluffy_tree
from props3 import g, box


def wall(col='#FBE6C8', trim='#E9B97A', paper=None, window=True, shelf_items=()):
    out = [f'<rect width="{W}" height="{HY + 40}" fill="{col}"/>']
    if paper:
        for x in range(0, W, 60):
            out.append(f'<rect x="{x}" y="0" width="30" height="{HY + 40}" fill="{paper}" opacity="0.35"/>')
    if window:
        wx, wy, ww, wh = 380, 70, 320, 250
        out.append(f'<rect x="{wx - 14}" y="{wy - 14}" width="{ww + 28}" height="{wh + 28}" rx="10" fill="#FFFFFF" stroke="{OL}" stroke-width="6"/>'
                   f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="#8FD5F5" stroke="{OL}" stroke-width="5"/>'
                   f'<path d="M{wx} {wy + wh} Q{wx + 80} {wy + wh - 60} {wx + 160} {wy + wh - 20} T{wx + ww} {wy + wh - 40} L{wx + ww} {wy + wh} Z" fill="#7DCB4E"/>'
                   f'<circle cx="{wx + 250}" cy="{wy + 60}" r="30" fill="#FFE47A"/>'
                   f'<line x1="{wx + ww / 2}" y1="{wy}" x2="{wx + ww / 2}" y2="{wy + wh}" stroke="#FFFFFF" stroke-width="10"/>'
                   f'<line x1="{wx}" y1="{wy + wh / 2}" x2="{wx + ww}" y2="{wy + wh / 2}" stroke="#FFFFFF" stroke-width="10"/>'
                   f'<path d="M{wx - 30} {wy - 30} L{wx + 70} {wy - 30} Q{wx + 40} {wy + 140} {wx + 10} {wy + wh + 20} L{wx - 30} {wy + wh + 20} Z" fill="#FF8FA3" stroke="{OL}" stroke-width="5"/>'
                   f'<path d="M{wx + ww + 30} {wy - 30} L{wx + ww - 70} {wy - 30} Q{wx + ww - 40} {wy + 140} {wx + ww - 10} {wy + wh + 20} L{wx + ww + 30} {wy + wh + 20} Z" fill="#FF8FA3" stroke="{OL}" stroke-width="5"/>'
                   f'<rect x="{wx - 50}" y="{wy - 44}" width="{ww + 100}" height="16" rx="8" fill="#B8733F" stroke="{OL}" stroke-width="4"/>')
    # shelves left/right
    for sx in (40, 790):
        for k, sy in enumerate((140, 270)):
            out.append(f'<rect x="{sx}" y="{sy}" width="250" height="16" rx="4" fill="#B8733F" stroke="{OL}" stroke-width="4"/>')
            for j, item in enumerate(shelf_items[(k * 2 + (sx > 500)) % max(1, len(shelf_items))] if shelf_items else []):
                out.append(item(sx + 30 + j * 70, sy))
    out.append(f'<rect x="0" y="{HY + 10}" width="{W}" height="30" fill="{trim}" stroke="{OL}" stroke-width="5"/>')
    return ''.join(out)


def floor_tiles(c1='#F7EAD6', c2='#E9CFA8'):
    out = [f'<rect x="0" y="{HY + 38}" width="{W}" height="{H - HY}" fill="{c1}"/>']
    # perspective checker: rows get taller toward the bottom, columns fan out from a vanishing point
    vx = 540
    ys = []
    y = HY + 38
    while y < H:
        ys.append(y)
        y += 30 + (y - HY) * 0.16
    ys.append(H + 60)
    n = 14
    for i in range(len(ys) - 1):
        for j in range(-n, n):
            if (i + j) % 2:
                continue
            def X(col, yy):
                return vx + (col * 90) * (0.25 + (yy - HY) / (H - HY) * 1.6)
            p = [(X(j, ys[i]), ys[i]), (X(j + 1, ys[i]), ys[i]), (X(j + 1, ys[i + 1]), ys[i + 1]), (X(j, ys[i + 1]), ys[i + 1])]
            out.append(poly(p, c2))
    return ''.join(out)


def floor_boards(c='#D9A066'):
    out = [f'<rect x="0" y="{HY + 38}" width="{W}" height="{H - HY}" fill="{c}"/>']
    vx = 540
    for j in range(-16, 17):
        x0 = vx + j * 90 * 0.25
        x1 = vx + j * 90 * 1.85
        out.append(f'<line x1="{x0:.0f}" y1="{HY + 38}" x2="{x1:.0f}" y2="{H}" stroke="{shade(c, -0.15)}" stroke-width="4"/>')
    r = rng(4)
    for _ in range(60):
        y = r.uniform(HY + 60, H)
        x = r.uniform(0, W)
        out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x:.0f}" y2="{y + 30 * S(y):.0f}" stroke="{shade(c, -0.15)}" stroke-width="3" opacity="0.6"/>')
    return ''.join(out)


# ------------------------------------------------------------------ kitchen props
def counter(x, by, s, w=200, h=110, col='#FFFFFF', top='#E8C08A', side='r'):
    w_, h_ = w * s, h * s
    b, dx, dy = box(x, by, w_, h_, s, col, side, dep=w_ * 0.5, top=top)
    out = [b]
    n = max(1, int(w / 70))
    for q in range(n):
        cx = x + w_ * (q + 0.5) / n
        out.append(f'<rect x="{cx - w_ / n * 0.4:.1f}" y="{by - h_ * 0.8:.1f}" width="{w_ / n * 0.8:.1f}" height="{h_ * 0.7:.1f}" rx="{4 * s:.1f}" fill="{shade(col, -0.05)}" {g(s, 0.7)}/>'
                   f'<rect x="{cx - 8 * s:.1f}" y="{by - h_ * 0.72:.1f}" width="{16 * s:.1f}" height="{4 * s:.1f}" rx="{2 * s:.1f}" fill="#9AA5B1"/>')
    return ''.join(out), dx, dy


def stove(x, by, s, side='r'):
    c, dx, dy = counter(x, by, s, 170, 110, '#E8E2D6', '#3C4A5C', side)
    out = [c]
    top = by - 110 * s
    for i, (u, v) in enumerate([(0.25, 0.3), (0.65, 0.3), (0.3, 0.75), (0.7, 0.75)]):
        cx, cy = x + 170 * s * u + dx * v, top + dy * v
        out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{18 * s:.1f}" ry="{8 * s:.1f}" fill="#555566" {g(s, 0.6)}/>')
    out.append(f'<rect x="{x + 20 * s:.1f}" y="{by - 90 * s:.1f}" width="{130 * s:.1f}" height="{56 * s:.1f}" rx="{6 * s:.1f}" fill="#33333D" {g(s, 0.8)}/>'
               f'<rect x="{x + 30 * s:.1f}" y="{by - 80 * s:.1f}" width="{110 * s:.1f}" height="{36 * s:.1f}" rx="{4 * s:.1f}" fill="#FF8A3D" opacity="0.7"/>')
    out.append(pot(x + 170 * s * 0.25 + dx * 0.3, top + dy * 0.3, s, '#E5533D'))
    return ''.join(out)


def fridge(x, by, s, side='r'):
    w_, h_ = 120 * s, 260 * s
    b, dx, dy = box(x, by, w_, h_, s, '#DCEEF6', side, dep=w_ * 0.7)
    out = [b, f'<line x1="{x:.1f}" y1="{by - h_ * 0.62:.1f}" x2="{x + w_:.1f}" y2="{by - h_ * 0.62:.1f}" {g(s)}/>',
           f'<rect x="{x + w_ * 0.8:.1f}" y="{by - h_ * 0.9:.1f}" width="{6 * s:.1f}" height="{h_ * 0.2:.1f}" rx="{3 * s:.1f}" fill="#9AA5B1"/>',
           f'<rect x="{x + w_ * 0.8:.1f}" y="{by - h_ * 0.55:.1f}" width="{6 * s:.1f}" height="{h_ * 0.25:.1f}" rx="{3 * s:.1f}" fill="#9AA5B1"/>']
    for i, (u, v, c) in enumerate([(0.2, 0.25, '#FFD23F'), (0.45, 0.3, '#FF5E7E'), (0.3, 0.75, '#6CC24A')]):
        out.append(f'<circle cx="{x + w_ * u:.1f}" cy="{by - h_ + h_ * v:.1f}" r="{7 * s:.1f}" fill="{c}" {g(s, 0.5)}/>')
    return ''.join(out)


def pot(x, y, s, col='#E5533D'):
    return (f'<path d="M{x - 30 * s:.1f} {y - 40 * s:.1f} L{x - 26 * s:.1f} {y:.1f} L{x + 26 * s:.1f} {y:.1f} L{x + 30 * s:.1f} {y - 40 * s:.1f} Z" fill="{col}" {g(s)}/>'
            f'<ellipse cx="{x:.1f}" cy="{y - 42 * s:.1f}" rx="{32 * s:.1f}" ry="{8 * s:.1f}" fill="{shade(col, 0.2)}" {g(s)}/>'
            f'<rect x="{x - 42 * s:.1f}" y="{y - 34 * s:.1f}" width="{12 * s:.1f}" height="{6 * s:.1f}" rx="{3 * s:.1f}" fill="{OL}"/><rect x="{x + 30 * s:.1f}" y="{y - 34 * s:.1f}" width="{12 * s:.1f}" height="{6 * s:.1f}" rx="{3 * s:.1f}" fill="{OL}"/>'
            f'<path d="M{x - 10 * s:.1f} {y - 56 * s:.1f} q{-6 * s:.1f} {-10 * s:.1f} 0 {-20 * s:.1f} M{x + 8 * s:.1f} {y - 56 * s:.1f} q{-6 * s:.1f} {-10 * s:.1f} 0 {-20 * s:.1f}" stroke="#FFFFFF" stroke-width="{4 * s:.1f}" fill="none" opacity="0.7" stroke-linecap="round"/>')


def table(x, y, s, cloth='#E5533D', items=True):
    w_, d_ = 220 * s, 80 * s
    out = [contact_shadow(x, y + 4 * s, w_ * 0.6, 16 * s, 0.25)]
    for lx, ly in [(-0.42, 0), (0.42, 0), (-0.32, -0.6), (0.48, -0.6)]:
        out.append(f'<rect x="{x + lx * w_ - 5 * s:.1f}" y="{y + ly * d_ - 70 * s:.1f}" width="{10 * s:.1f}" height="{70 * s:.1f}" fill="#8A5326" {g(s, 0.7)}/>')
    top = [(x - w_ / 2, y - 70 * s), (x + w_ / 2, y - 70 * s), (x + w_ / 2 + 30 * s, y - 70 * s - d_ * 0.6), (x - w_ / 2 + 30 * s, y - 70 * s - d_ * 0.6)]
    out.append(poly(top, '#FFFFFF', w=sw(s)))
    for q in range(6):
        if q % 2 == 0:
            t0, t1 = q / 6, (q + 1) / 6
            out.append(poly([(top[0][0] + (top[1][0] - top[0][0]) * t0, top[0][1]), (top[0][0] + (top[1][0] - top[0][0]) * t1, top[0][1]),
                             (top[3][0] + (top[2][0] - top[3][0]) * t1, top[3][1]), (top[3][0] + (top[2][0] - top[3][0]) * t0, top[3][1])], cloth))
    out.append(f'<path d="M{top[0][0]:.1f} {top[0][1]:.1f} L{top[1][0]:.1f} {top[1][1]:.1f} L{top[1][0]:.1f} {top[1][1] + 26 * s:.1f} Q{x:.1f} {top[1][1] + 34 * s:.1f} {top[0][0]:.1f} {top[0][1] + 26 * s:.1f} Z" fill="{cloth}" {g(s)}/>')
    if items:
        cx, cy = x + 15 * s, y - 70 * s - d_ * 0.3
        out.append(fruit_bowl(cx - 40 * s, cy, s * 0.8) + teapot(cx + 50 * s, cy, s * 0.7))
    return ''.join(out)


def chair(x, y, s, col='#E8A65A'):
    return (contact_shadow(x, y + 2 * s, 30 * s, 6 * s, 0.22) +
            ''.join(f'<rect x="{x + lx * s:.1f}" y="{y - 50 * s:.1f}" width="{7 * s:.1f}" height="{50 * s:.1f}" fill="#8A5326" {g(s, 0.6)}/>' for lx in (-26, 18)) +
            f'<rect x="{x - 30 * s:.1f}" y="{y - 56 * s:.1f}" width="{60 * s:.1f}" height="{10 * s:.1f}" rx="{3 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<rect x="{x - 26 * s:.1f}" y="{y - 120 * s:.1f}" width="{52 * s:.1f}" height="{56 * s:.1f}" rx="{10 * s:.1f}" fill="{col}" {g(s)}/>')


def fruit_bowl(x, y, s):
    out = [f'<path d="M{x - 40 * s:.1f} {y - 20 * s:.1f} Q{x:.1f} {y + 18 * s:.1f} {x + 40 * s:.1f} {y - 20 * s:.1f} Z" fill="#4FA3E3" {g(s)}/>']
    for bx, by, c in [(-22, -30, '#FF4E4E'), (0, -38, '#FFD23F'), (20, -30, '#6CC24A'), (-8, -24, '#FF8A3D'), (12, -22, '#FF4E4E')]:
        out.append(f'<circle cx="{x + bx * s:.1f}" cy="{y + by * s:.1f}" r="{11 * s:.1f}" fill="{c}" {g(s, 0.6)}/>')
    out.append(f'<path d="M{x - 40 * s:.1f} {y - 20 * s:.1f} Q{x:.1f} {y + 18 * s:.1f} {x + 40 * s:.1f} {y - 20 * s:.1f}" fill="#4FA3E3" {g(s)}/>')
    return ''.join(out)


def teapot(x, y, s, col='#FF8FA3'):
    return (f'<ellipse cx="{x:.1f}" cy="{y - 24 * s:.1f}" rx="{28 * s:.1f}" ry="{24 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<path d="M{x + 26 * s:.1f} {y - 30 * s:.1f} q{20 * s:.1f} {-4 * s:.1f} {24 * s:.1f} {-20 * s:.1f}" stroke="{OL}" stroke-width="{8 * s + 3:.1f}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x + 26 * s:.1f} {y - 30 * s:.1f} q{20 * s:.1f} {-4 * s:.1f} {24 * s:.1f} {-20 * s:.1f}" stroke="{col}" stroke-width="{8 * s:.1f}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x - 26 * s:.1f} {y - 36 * s:.1f} q{-18 * s:.1f} 0 {-14 * s:.1f} {18 * s:.1f}" stroke="{OL}" stroke-width="{4 * s:.1f}" fill="none"/>'
            f'<ellipse cx="{x:.1f}" cy="{y - 46 * s:.1f}" rx="{14 * s:.1f}" ry="{5 * s:.1f}" fill="{shade(col, 0.2)}" {g(s, 0.7)}/><circle cx="{x:.1f}" cy="{y - 54 * s:.1f}" r="{5 * s:.1f}" fill="{col}" {g(s, 0.6)}/>')


def utensil_jar(x, y, s):
    return (f'<rect x="{x - 18 * s:.1f}" y="{y - 40 * s:.1f}" width="{36 * s:.1f}" height="{40 * s:.1f}" rx="{6 * s:.1f}" fill="#FFD23F" {g(s)}/>'
            f'<line x1="{x - 8 * s:.1f}" y1="{y - 40 * s:.1f}" x2="{x - 16 * s:.1f}" y2="{y - 90 * s:.1f}" stroke="#B8733F" stroke-width="{6 * s:.1f}" stroke-linecap="round"/>'
            f'<ellipse cx="{x - 17 * s:.1f}" cy="{y - 94 * s:.1f}" rx="{9 * s:.1f}" ry="{12 * s:.1f}" fill="#B8733F" {g(s, 0.6)}/>'
            f'<line x1="{x + 6 * s:.1f}" y1="{y - 40 * s:.1f}" x2="{x + 12 * s:.1f}" y2="{y - 96 * s:.1f}" stroke="#9AA5B1" stroke-width="{4 * s:.1f}"/>'
            + ''.join(f'<line x1="{x + 12 * s + q * 4 * s:.1f}" y1="{y - 96 * s:.1f}" x2="{x + 14 * s + q * 4 * s:.1f}" y2="{y - 112 * s:.1f}" stroke="#9AA5B1" stroke-width="{2.5 * s:.1f}"/>' for q in (-1, 0, 1)))


def plant_pot(x, y, s, col='#E8A65A'):
    return (contact_shadow(x, y + 2 * s, 24 * s, 5 * s, 0.22) +
            ''.join(f'<path d="M{x:.1f} {y - 36 * s:.1f} Q{x + a * 30 * s:.1f} {y - 80 * s:.1f} {x + a * 40 * s:.1f} {y - 100 * s:.1f} Q{x + a * 12 * s:.1f} {y - 70 * s:.1f} {x:.1f} {y - 36 * s:.1f} Z" fill="#4FB043" {g(s, 0.7)}/>' for a in (-1, -0.4, 0.3, 1)) +
            f'<path d="M{x - 22 * s:.1f} {y - 40 * s:.1f} L{x + 22 * s:.1f} {y - 40 * s:.1f} L{x + 16 * s:.1f} {y:.1f} L{x - 16 * s:.1f} {y:.1f} Z" fill="{col}" {g(s)}/>')


def jar_shelf(x, y):
    return f'<rect x="{x - 14}" y="{y - 40}" width="28" height="40" rx="6" fill="#FFD9A8" stroke="{OL}" stroke-width="3"/><rect x="{x - 16}" y="{y - 46}" width="32" height="8" rx="3" fill="#E5533D" stroke="{OL}" stroke-width="3"/>'


def plate_shelf(x, y):
    return f'<ellipse cx="{x}" cy="{y - 22}" rx="22" ry="22" fill="#FFFFFF" stroke="{OL}" stroke-width="3"/><circle cx="{x}" cy="{y - 22}" r="12" fill="#BFE8F5"/>'


def book_shelf(x, y):
    cols = ['#E5533D', '#4FA3E3', '#FFD23F', '#6CC24A']
    return ''.join(f'<rect x="{x - 24 + q * 13}" y="{y - 44 + (q % 2) * 6}" width="12" height="{44 - (q % 2) * 6}" fill="{cols[q]}" stroke="{OL}" stroke-width="3"/>' for q in range(4))


# ------------------------------------------------------------------ toy room props
def toy_blocks(x, y, s):
    out = []
    for i, (bx, by, c, l) in enumerate([(-30, 0, '#E5533D', 'A'), (30, 0, '#4FA3E3', 'B'), (0, -46, '#FFD23F', 'C')]):
        b, dx, dy = box(x + bx * s - 23 * s, y + by * s, 46 * s, 46 * s, s, c, 'r', dep=30 * s)
        out.append(b + f'<text x="{x + bx * s:.1f}" y="{y + by * s - 12 * s:.1f}" font-family="Baloo" font-weight="800" font-size="{30 * s:.1f}" text-anchor="middle" fill="#FFFFFF" stroke="{OL}" stroke-width="{2 * s:.1f}" paint-order="stroke">{l}</text>')
    return ''.join(out)


def teddy(x, y, s, col='#C98A4E'):
    l = shade(col, 0.3)
    return (contact_shadow(x, y + 2 * s, 40 * s, 8 * s, 0.25) +
            f'<ellipse cx="{x:.1f}" cy="{y - 36 * s:.1f}" rx="{34 * s:.1f}" ry="{36 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<ellipse cx="{x:.1f}" cy="{y - 30 * s:.1f}" rx="{18 * s:.1f}" ry="{20 * s:.1f}" fill="{l}"/>'
            f'<circle cx="{x - 30 * s:.1f}" cy="{y - 6 * s:.1f}" r="{14 * s:.1f}" fill="{col}" {g(s)}/><circle cx="{x + 30 * s:.1f}" cy="{y - 6 * s:.1f}" r="{14 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<circle cx="{x:.1f}" cy="{y - 92 * s:.1f}" r="{30 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<circle cx="{x - 24 * s:.1f}" cy="{y - 116 * s:.1f}" r="{11 * s:.1f}" fill="{col}" {g(s)}/><circle cx="{x + 24 * s:.1f}" cy="{y - 116 * s:.1f}" r="{11 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<ellipse cx="{x:.1f}" cy="{y - 82 * s:.1f}" rx="{13 * s:.1f}" ry="{10 * s:.1f}" fill="{l}"/><circle cx="{x:.1f}" cy="{y - 86 * s:.1f}" r="{4 * s:.1f}" fill="{OL}"/>'
            f'<circle cx="{x - 11 * s:.1f}" cy="{y - 98 * s:.1f}" r="{3.5 * s:.1f}" fill="{OL}"/><circle cx="{x + 11 * s:.1f}" cy="{y - 98 * s:.1f}" r="{3.5 * s:.1f}" fill="{OL}"/>'
            f'<path d="M{x - 14 * s:.1f} {y - 64 * s:.1f} L{x + 14 * s:.1f} {y - 64 * s:.1f} L{x:.1f} {y - 56 * s:.1f} Z" fill="#E5533D" {g(s, 0.6)}/>')


def ball(x, y, s):
    r = 30 * s
    return (contact_shadow(x, y + 2 * s, r, 6 * s, 0.25) +
            f'<circle cx="{x:.1f}" cy="{y - r:.1f}" r="{r:.1f}" fill="#FFFFFF" {g(s)}/>'
            f'<path d="M{x - r:.1f} {y - r:.1f} A{r:.1f} {r:.1f} 0 0 1 {x:.1f} {y - 2 * r:.1f} L{x:.1f} {y - r:.1f} Z" fill="#E5533D"/>'
            f'<path d="M{x:.1f} {y:.1f} A{r:.1f} {r:.1f} 0 0 1 {x - r:.1f} {y - r:.1f} L{x:.1f} {y - r:.1f} Z" fill="#4FA3E3"/>'
            f'<path d="M{x + r:.1f} {y - r:.1f} A{r:.1f} {r:.1f} 0 0 1 {x:.1f} {y:.1f} L{x:.1f} {y - r:.1f} Z" fill="#FFD23F"/>'
            f'<circle cx="{x:.1f}" cy="{y - r:.1f}" r="{r:.1f}" fill="none" {g(s)}/><circle cx="{x - r * 0.35:.1f}" cy="{y - r * 1.4:.1f}" r="{r * 0.2:.1f}" fill="#FFFFFF" opacity="0.6"/>')


def toy_train(x, y, s):
    out = [contact_shadow(x, y + 3 * s, 90 * s, 9 * s, 0.25)]
    for i, (dx_, c) in enumerate([(50, '#E5533D'), (-10, '#4FA3E3'), (-70, '#FFD23F')]):
        bx = x + dx_ * s
        out.append(f'<rect x="{bx - 26 * s:.1f}" y="{y - 46 * s:.1f}" width="{52 * s:.1f}" height="{34 * s:.1f}" rx="{5 * s:.1f}" fill="{c}" {g(s)}/>'
                   f'<circle cx="{bx - 14 * s:.1f}" cy="{y - 10 * s:.1f}" r="{9 * s:.1f}" fill="#33333D" {g(s, 0.6)}/><circle cx="{bx + 14 * s:.1f}" cy="{y - 10 * s:.1f}" r="{9 * s:.1f}" fill="#33333D" {g(s, 0.6)}/>')
    bx = x + 50 * s
    out.append(f'<rect x="{bx - 4 * s:.1f}" y="{y - 80 * s:.1f}" width="{30 * s:.1f}" height="{36 * s:.1f}" rx="{4 * s:.1f}" fill="#E5533D" {g(s)}/>'
               f'<rect x="{bx + 2 * s:.1f}" y="{y - 74 * s:.1f}" width="{18 * s:.1f}" height="{14 * s:.1f}" fill="{PALETTE["window"]}"/>'
               f'<rect x="{bx - 22 * s:.1f}" y="{y - 70 * s:.1f}" width="{12 * s:.1f}" height="{24 * s:.1f}" fill="#3C4A5C" {g(s, 0.7)}/>'
               f'<circle cx="{bx - 16 * s:.1f}" cy="{y - 82 * s:.1f}" r="{8 * s:.1f}" fill="#FFFFFF" opacity="0.8"/><circle cx="{bx - 8 * s:.1f}" cy="{y - 96 * s:.1f}" r="{10 * s:.1f}" fill="#FFFFFF" opacity="0.6"/>')
    return ''.join(out)


def book_stack(x, y, s):
    out = []
    for i, c in enumerate(['#4FA3E3', '#E5533D', '#6CC24A', '#FFD23F']):
        yy = y - i * 16 * s
        off = (i % 2) * 8 * s - 4 * s
        out.append(f'<rect x="{x - 44 * s + off:.1f}" y="{yy - 16 * s:.1f}" width="{88 * s:.1f}" height="{16 * s:.1f}" rx="{3 * s:.1f}" fill="{c}" {g(s)}/>'
                   f'<rect x="{x + 30 * s + off:.1f}" y="{yy - 13 * s:.1f}" width="{10 * s:.1f}" height="{10 * s:.1f}" fill="#FFFFFF" opacity="0.8"/>')
    return ''.join(out)


def armchair(x, y, s, col='#4FA3E3'):
    return (contact_shadow(x, y + 3 * s, 70 * s, 10 * s, 0.25) +
            f'<rect x="{x - 60 * s:.1f}" y="{y - 120 * s:.1f}" width="{120 * s:.1f}" height="{70 * s:.1f}" rx="{20 * s:.1f}" fill="{shade(col, -0.1)}" {g(s)}/>'
            f'<rect x="{x - 56 * s:.1f}" y="{y - 64 * s:.1f}" width="{112 * s:.1f}" height="{54 * s:.1f}" rx="{12 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<rect x="{x - 76 * s:.1f}" y="{y - 84 * s:.1f}" width="{30 * s:.1f}" height="{74 * s:.1f}" rx="{12 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<rect x="{x + 46 * s:.1f}" y="{y - 84 * s:.1f}" width="{30 * s:.1f}" height="{74 * s:.1f}" rx="{12 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<rect x="{x - 66 * s:.1f}" y="{y - 12 * s:.1f}" width="{10 * s:.1f}" height="{12 * s:.1f}" fill="#8A5326"/><rect x="{x + 56 * s:.1f}" y="{y - 12 * s:.1f}" width="{10 * s:.1f}" height="{12 * s:.1f}" fill="#8A5326"/>')


def floor_lamp(x, y, s):
    return (contact_shadow(x, y + 2 * s, 24 * s, 5 * s, 0.25) +
            f'<ellipse cx="{x:.1f}" cy="{y - 4 * s:.1f}" rx="{20 * s:.1f}" ry="{6 * s:.1f}" fill="#3C4A5C" {g(s, 0.7)}/>'
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 170 * s:.1f}" stroke="#3C4A5C" stroke-width="{6 * s:.1f}"/>'
            f'<circle cx="{x:.1f}" cy="{y - 180 * s:.1f}" r="{60 * s:.1f}" fill="#FFE9A6" opacity="0.25"/>'
            f'<path d="M{x - 36 * s:.1f} {y - 160 * s:.1f} L{x - 22 * s:.1f} {y - 210 * s:.1f} L{x + 22 * s:.1f} {y - 210 * s:.1f} L{x + 36 * s:.1f} {y - 160 * s:.1f} Z" fill="#FFD9A8" {g(s)}/>')


def toy_box(x, by, s, col='#6CC24A', side='r'):
    b, dx, dy = box(x, by, 150 * s, 80 * s, s, col, side, dep=90 * s, top=shade(col, -0.25))
    out = [b]
    out.append(teddy(x + 60 * s + dx * 0.5, by - 80 * s + dy * 0.5 + 30 * s, s * 0.45, '#E8A65A'))
    out.append(f'<circle cx="{x + 110 * s + dx * 0.4:.1f}" cy="{by - 92 * s + dy * 0.4:.1f}" r="{16 * s:.1f}" fill="#FF5E7E" {g(s, 0.7)}/>')
    out.append(f'<path d="M{x + 30 * s:.1f} {by - 50 * s:.1f} l{12 * s:.1f} {-12 * s:.1f} l{12 * s:.1f} {12 * s:.1f} l{-12 * s:.1f} {12 * s:.1f} Z" fill="#FFD23F" {g(s, 0.5)}/>')
    return ''.join(out)


def rug(w, cx, cy, rx, ry, c1='#FF8FA3', c2='#FFD6E0'):
    w.flat.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c1}" stroke="{OL}" stroke-width="5"/>'
                  f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * 0.72:.0f}" ry="{ry * 0.72:.0f}" fill="{c2}"/>'
                  f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * 0.42:.0f}" ry="{ry * 0.42:.0f}" fill="{c1}"/>')


# =================================================================== KITCHEN
def kitchen():
    w = World(31)
    w.sky = wall('#FBE6C8', '#E9B97A', paper='#FFFFFF', shelf_items=[[jar_shelf, jar_shelf, plate_shelf], [plate_shelf, plate_shelf, jar_shelf]])
    w.ground = floor_tiles('#F7EAD6', '#E2C49A')
    cl, wf, L, Rr = w.path([(540, 520), (480, 760), (600, 1020), (450, 1300), (600, 1580), (460, 1860), (560, 2140), (500, 2420)], w0=50, w1=170,
                           fill='#E5533D', edge='#FFD23F', tiles=('#F06A55', 3))
    # back counters along the wall
    x = -40
    for i, (kind, wd) in enumerate([('c', 150), ('stove', 170), ('gap', 0), ('fridge', 120), ('c', 170)]):
        s = S(600) * 2.1
        if kind == 'gap':
            x = 640
            continue
        if kind == 'c':
            c, _, _ = counter(x, 600, s, wd, 110, '#FFFFFF', '#E8C08A', 'r' if x < 540 else 'l')
            w.add(600, c + utensil_jar(x + wd * s * 0.5, 600 - 110 * s, s), i)
        elif kind == 'stove':
            w.add(600, stove(x, 600, s), i)
        else:
            w.add(600, fridge(x, 600, s, 'l'), i)
        w.occ(x, 500, x + wd * s, 610)
        x += wd * s
    # island counter + tables
    k = 1.9
    c, _, _ = counter(0, 1150, S(1150) * k, 210, 110, '#4FA3E3', '#E8C08A', 'r')
    sc = S(1150) * k
    w.add(1150, c + fruit_bowl(105 * sc, 1150 - 110 * sc - 6, sc) + pot(175 * sc, 1150 - 110 * sc, sc * 0.8, '#FFB82E'))
    w.occ(0, 960, 210 * sc + 80, 1160)
    w.add(1420, table(860, 1420, S(1420) * 1.6, '#E5533D'))
    w.occ(660, 1240, 1080, 1430)
    for x_, y_ in [(680, 1480), (1040, 1470)]:
        w.add(y_, chair(x_, y_, S(y_) * 1.6, '#FFB82E'))
    w.add(1960, table(250, 1960, S(1960) * 1.5, '#4FA3E3'))
    w.occ(20, 1780, 480, 1970)
    for x_, y_ in [(40, 2030), (450, 2030)]:
        w.add(y_, chair(x_, y_, S(y_) * 1.5, '#6CC24A'))
    for x_, y_ in [(960, 920), (100, 1600), (940, 1980), (780, 2280)]:
        w.add(y_, plant_pot(x_, y_, S(y_) * 2.4))
    for x_, y_ in [(300, 830), (860, 1720), (680, 2330)]:
        w.add(y_, pot(x_, y_, S(y_) * 2.2, '#9AA5B1'))
    w.add(1640, fruit_bowl(320, 1640, S(1640) * 2.2))
    w.add(2250, teapot(240, 2280, S(2280) * 2.2))
    w.add(870, utensil_jar(700, 880, S(880) * 2.2))
    return w.render()


# =================================================================== THINGS - toy room
def things():
    w = World(32)
    w.sky = wall('#DCEEF6', '#9FD0C8', paper='#FFFFFF', shelf_items=[[book_shelf, book_shelf], [plate_shelf, book_shelf]])
    w.ground = floor_boards('#D9A066')
    rug(w, 540, 1500, 470, 200)
    cl, wf, L, Rr = w.path([(540, 520), (600, 760), (460, 1020), (580, 1300), (440, 1580), (580, 1860), (480, 2140), (520, 2420)], w0=50, w1=160,
                           fill='#4FA3E3', edge='#FFFFFF', tiles=('#6FB6EC', 2))
    # furniture along the back wall
    s = S(600) * 2.1
    c, _, _ = counter(-20, 600, s, 200, 150, '#FFFFFF', '#E8C08A', 'r')
    w.add(600, c + book_stack(60 * s, 600 - 150 * s, s) + plant_pot(150 * s, 600 - 150 * s, s * 0.8))
    w.add(600, armchair(820, 600, s, '#FF8FA3'), 1)
    w.add(610, floor_lamp(1000, 610, s))
    w.occ(-20, 480, 1080, 620)
    w.add(1080, toy_box(30, 1080, S(1080) * 1.8, '#6CC24A'))
    w.occ(20, 900, 420, 1090)
    w.add(1200, armchair(880, 1200, S(1200) * 1.8, '#4FA3E3'))
    w.occ(700, 1000, 1080, 1210)
    for x, y, fn in [(270, 1350, teddy), (830, 1550, ball), (210, 1750, toy_train), (840, 1950, toy_blocks), (230, 2150, book_stack),
                     (760, 880, toy_blocks), (330, 860, ball), (920, 2280, teddy)]:
        w.add(y, fn(x, y, S(y) * 2.2))
        w.occ(x - 110 * S(y), y - 50, x + 110 * S(y), y + 10)
    w.add(1700, toy_box(760, 1700, S(1700) * 1.6, '#FFB82E', 'l'))
    for x, y in [(80, 2000), (980, 1350)]:
        w.add(y, plant_pot(x, y, S(y) * 2.4))
    return w.render()


BUILDERS = {'kitchen': kitchen, 'things': things}
