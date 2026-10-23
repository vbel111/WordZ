"""City map (v2): park at the bottom, a boulevard lined with shops and apartments receding to a
skyline under a warm afternoon sky. 1080 x 2400, see style.py for the rules."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from style import (H, OL, PALETTE as P, W, bench, bird, bush, car, cloud, contact_shadow, flower,  # noqa: E402
                   grass_tuft, lamp, lin, mix, rad, rng, round_tree, shade, svg)

HORIZON = 930
VX = W / 2


def depth(y):          # 0 at horizon, 1 at the bottom edge
    return (y - HORIZON) / (H - HORIZON)


def road_half(t):
    return 46 + 300 * t


def walk_half(t):
    return road_half(t) + 18 + 78 * t


# ---------------- sky ----------------

def sky():
    out = [f'<rect width="{W}" height="{HORIZON + 40}" fill="url(#sky)"/>']
    out.append(f'<circle cx="790" cy="560" r="230" fill="url(#sunGlow)"/>')
    out.append(f'<circle cx="790" cy="560" r="82" fill="#FFF3C4" stroke="#FFD86B" stroke-width="10"/>')
    for x, y, s, o in [(200, 170, 1.15, 1), (760, 120, 0.8, 0.95), (520, 330, 0.65, 0.9), (110, 470, 0.7, 0.85),
                       (980, 330, 0.9, 0.95), (330, 620, 0.5, 0.8)]:
        out.append(cloud(x, y, s, o))
    for x, y, s in [(420, 230, 1.2), (462, 205, 0.9), (498, 250, 1.0), (640, 420, 0.8), (668, 402, 0.7)]:
        out.append(bird(x, y, s))
    return ''.join(out)


def skyline():
    """Two layers of distant towers, fading into the sky."""
    r = rng(7)
    out = []
    for layer, (col, base, hmin, hmax, wmin, wmax, op) in enumerate([
            ('#B9D3EE', HORIZON + 10, 160, 430, 60, 120, 1.0),
            ('#97B8DE', HORIZON + 20, 90, 300, 70, 140, 1.0)]):
        x = -40
        while x < W + 40:
            w = r.uniform(wmin, wmax)
            h = r.uniform(hmin, hmax)
            if layer == 0 and 380 < x < 640:
                h *= 1.25                    # a taller cluster right behind the boulevard
            top = base - h
            hi = shade(col, 0.18)
            kind = r.random()
            g = [f'<rect x="{x:.0f}" y="{top:.0f}" width="{w:.0f}" height="{h + 30:.0f}" fill="{col}"/>']
            g.append(f'<rect x="{x:.0f}" y="{top:.0f}" width="{w * 0.28:.0f}" height="{h + 30:.0f}" fill="{hi}"/>')
            if kind < 0.18:     # spire
                g.append(f'<path d="M{x + w * 0.3:.0f} {top:.0f} L{x + w / 2:.0f} {top - h * 0.35:.0f} L{x + w * 0.7:.0f} {top:.0f} Z" fill="{col}"/>')
            elif kind < 0.32:   # dome
                g.append(f'<path d="M{x + w * 0.1:.0f} {top:.0f} A{w * 0.4:.0f} {w * 0.4:.0f} 0 0 1 {x + w * 0.9:.0f} {top:.0f} Z" fill="{col}"/>')
            elif kind < 0.5:    # stepped top
                g.append(f'<rect x="{x + w * 0.2:.0f}" y="{top - h * 0.12:.0f}" width="{w * 0.6:.0f}" height="{h * 0.12 + 2:.0f}" fill="{col}"/>')
            elif kind < 0.6:    # antenna
                g.append(f'<rect x="{x + w / 2 - 2:.0f}" y="{top - 60:.0f}" width="4" height="60" fill="{col}"/>')
            # windows as faint rows
            wc = shade(col, 0.35 if layer == 0 else 0.28)
            for wy in range(int(top + 18), int(base - 10), 26):
                for wx in range(int(x + 10), int(x + w - 14), 18):
                    if r.random() < 0.55:
                        g.append(f'<rect x="{wx}" y="{wy}" width="8" height="12" rx="2" fill="{wc}"/>')
            out.append(f'<g opacity="{op}">{"".join(g)}</g>')
            x += w + r.uniform(-12, 10)
    return ''.join(out)


# ---------------- ground ----------------

T_END = 0.6          # the street ends in a plaza; below it is the park


def ty(t):
    return HORIZON + t * (H - HORIZON)


def path_x(y):
    """Centre line of the park footpath (gentle S-curve)."""
    u = (y - ty(0.66)) / (H - ty(0.66))
    return VX + math.sin(u * math.pi * 1.2) * 70


def ground():
    out = [f'<rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="url(#ground)"/>']

    def trap(hfun, fill, t1=T_END + 0.04):
        return (f'<path d="M{VX - hfun(0):.1f} {HORIZON} L{VX + hfun(0):.1f} {HORIZON} '
                f'L{VX + hfun(t1):.1f} {ty(t1):.1f} L{VX - hfun(t1):.1f} {ty(t1):.1f} Z" fill="{fill}"/>')
    out.append(trap(walk_half, '#E9D7B6'))
    for i in range(1, 22):
        t = (i / 22) ** 1.6 * (T_END + 0.04)
        y = ty(t)
        for sgn in (-1, 1):
            x0, x1 = VX + sgn * road_half(t), VX + sgn * walk_half(t)
            out.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke="#D6BF98" stroke-width="{1 + 3 * t:.1f}"/>')
    out.append(trap(lambda t: road_half(t) + 6 * t + 3, '#BFA889'))
    out.append(trap(road_half, 'url(#road)'))
    for i in range(0, 24):
        t0 = (i / 24) ** 1.7 * T_END
        t1 = ((i + 0.45) / 24) ** 1.7 * T_END
        w0, w1 = 1 + 5 * t0, 1 + 5 * t1
        out.append(f'<path d="M{VX - w0:.1f} {ty(t0):.1f} L{VX + w0:.1f} {ty(t0):.1f} L{VX + w1:.1f} {ty(t1):.1f} L{VX - w1:.1f} {ty(t1):.1f} Z" fill="#FFF6E0" opacity="0.85"/>')
    tc = 0.24
    hw = road_half(tc)
    for k in range(9):
        xa = VX - hw + (2 * hw) * (k + 0.15) / 9
        xb = VX - hw + (2 * hw) * (k + 0.75) / 9
        out.append(f'<rect x="{xa:.1f}" y="{ty(tc):.1f}" width="{xb - xa:.1f}" height="{14 + 40 * tc:.1f}" fill="#FFF6E0" opacity="0.8"/>')

    # footpath through the park (drawn before the plaza so the plaza caps it)
    left, right = [], []
    y = ty(0.64)
    while y <= H + 40:
        u = (y - ty(0.64)) / (H - ty(0.64))
        half = 150 + 90 * u
        cx = path_x(y)
        left.append((cx - half, y)); right.append((cx + half, y))
        y += 40
    d = 'M' + ' L'.join(f'{x:.1f} {yy:.1f}' for x, yy in left) + ' L' + ' L'.join(f'{x:.1f} {yy:.1f}' for x, yy in reversed(right)) + ' Z'
    out.append(f'<path d="{d}" fill="url(#cobble)" stroke="{OL}" stroke-width="7" stroke-linejoin="round"/>')
    r = rng(5)
    for _ in range(170):        # cobble stones
        yy = r.uniform(ty(0.66), H)
        u = (yy - ty(0.64)) / (H - ty(0.64))
        half = 150 + 90 * u - 16
        xx = path_x(yy) + r.uniform(-half, half)
        sz = 6 + 8 * u
        out.append(f'<ellipse cx="{xx:.1f}" cy="{yy:.1f}" rx="{sz * 1.4:.1f}" ry="{sz * 0.8:.1f}" fill="#D9BE8E" opacity="0.7"/>')
    # edging stones along the path
    for pts in (left, right):
        for x, yy in pts[1::1]:
            out.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="7" fill="#EFE3CC" stroke="{OL}" stroke-width="3"/>')

    # plaza where the street meets the park
    py = ty(T_END + 0.05)
    prx, pry = walk_half(T_END + 0.05) + 90, 120
    out.append(f'<ellipse cx="{VX}" cy="{py + 8}" rx="{prx}" ry="{pry}" fill="#C9A978"/>')
    out.append(f'<ellipse cx="{VX}" cy="{py}" rx="{prx}" ry="{pry}" fill="#F1DFBC" stroke="{OL}" stroke-width="7"/>')
    for k, c in enumerate(['#E6CC9E', '#F6E8CC', '#E6CC9E']):
        f = 0.8 - k * 0.22
        out.append(f'<ellipse cx="{VX}" cy="{py}" rx="{prx * f:.1f}" ry="{pry * f:.1f}" fill="{c}"/>')
    for k in range(16):
        ang = k * math.pi / 8
        out.append(f'<line x1="{VX + math.cos(ang) * prx * 0.2:.1f}" y1="{py + math.sin(ang) * pry * 0.2:.1f}" '
                   f'x2="{VX + math.cos(ang) * prx * 0.8:.1f}" y2="{py + math.sin(ang) * pry * 0.8:.1f}" stroke="#D9BE8E" stroke-width="3"/>')
    return ''.join(out)


# ---------------- buildings ----------------

FACADES = ['#F6D9A8', '#F2B694', '#E7C9E3', '#BFE0EF', '#F9E7C4', '#D8E9B8', '#F5C7A0', '#E2D2F0']
ROOFS = ['#E5533D', '#3A7BD5', '#5FAE48', '#E99A12', '#9B59B6']


def building(inner_x, base, s, side, r, idx):
    """Front face away from the road; inner_x is the edge closest to the road. side=-1 left, +1 right."""
    sw = max(2.5, 7 * s)
    w = r.uniform(230, 320) * s
    h = r.uniform(250, 460) * s
    face = FACADES[idx % len(FACADES)]
    roof = ROOFS[r.randrange(len(ROOFS))]
    side_w = 60 * s
    x0 = inner_x if side > 0 else inner_x - w           # front face left edge
    x1 = x0 + w
    top = base - h
    out = [contact_shadow((x0 + x1) / 2, base + 2, w * 0.6, 12 * s, 0.25)]
    out.append(f'<g stroke="{OL}" stroke-width="{sw:.1f}" stroke-linejoin="round">')
    # side face toward the road, slanting toward the vanishing point
    sx = inner_x
    lean = side * -1
    pts = [(sx, base), (sx, top), (sx + lean * side_w, top + 14 * s), (sx + lean * side_w, base)]
    out.append(f'<path d="M{" L".join(f"{a:.1f} {b:.1f}" for a, b in pts)} Z" fill="{shade(face, -0.22)}"/>')
    out.append(f'<rect x="{x0:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{face}"/>')
    # roof: cornice, sometimes a pitched roof or a water tank
    kind = r.random()
    out.append(f'<rect x="{x0 - 8 * s:.1f}" y="{top - 16 * s:.1f}" width="{w + 16 * s:.1f}" height="{18 * s:.1f}" fill="{shade(face, -0.12)}"/>')
    if kind < 0.35:
        out.append(f'<path d="M{x0 - 6 * s:.1f} {top - 16 * s:.1f} L{x0 + w / 2:.1f} {top - 90 * s:.1f} L{x1 + 6 * s:.1f} {top - 16 * s:.1f} Z" fill="{roof}"/>')
        out.append(f'<circle cx="{x0 + w / 2:.1f}" cy="{top - 46 * s:.1f}" r="{12 * s:.1f}" fill="{P["window"]}"/>')
    elif kind < 0.6:
        tx = x0 + w * r.uniform(0.25, 0.65)
        out.append(f'<rect x="{tx - 22 * s:.1f}" y="{top - 70 * s:.1f}" width="{44 * s:.1f}" height="{40 * s:.1f}" rx="{6 * s:.1f}" fill="{P["wood"]}"/>'
                   f'<path d="M{tx - 26 * s:.1f} {top - 70 * s:.1f} L{tx:.1f} {top - 92 * s:.1f} L{tx + 26 * s:.1f} {top - 70 * s:.1f} Z" fill="{P["woodDark"]}"/>'
                   f'<line x1="{tx - 16 * s:.1f}" y1="{top - 30 * s:.1f}" x2="{tx - 16 * s:.1f}" y2="{top - 16 * s:.1f}"/>'
                   f'<line x1="{tx + 16 * s:.1f}" y1="{top - 30 * s:.1f}" x2="{tx + 16 * s:.1f}" y2="{top - 16 * s:.1f}"/>')
    elif kind < 0.75:
        tx = x0 + w * 0.7
        out.append(f'<line x1="{tx:.1f}" y1="{top - 16 * s:.1f}" x2="{tx:.1f}" y2="{top - 80 * s:.1f}"/>'
                   f'<circle cx="{tx:.1f}" cy="{top - 84 * s:.1f}" r="{6 * s:.1f}" fill="{P["red"]}"/>')
    out.append('</g>')
    # light from the upper left: highlight strip and a soft shade at the bottom
    out.append(f'<rect x="{x0 + sw / 2:.1f}" y="{top + sw / 2:.1f}" width="{w * 0.12:.1f}" height="{h - sw:.1f}" fill="#FFFFFF" opacity="0.22"/>')
    # windows
    shop_h = 70 * s
    cols = max(2, int(w / (62 * s)))
    rows = max(2, int((h - shop_h - 30 * s) / (70 * s)))
    cw = w / cols
    rh = (h - shop_h - 24 * s) / rows
    wsw = max(1.5, 4 * s)
    for rr in range(rows):
        for cc in range(cols):
            wx = x0 + cc * cw + cw * 0.24
            wy = top + 20 * s + rr * rh + rh * 0.18
            ww, wh = cw * 0.52, rh * 0.6
            lit = r.random() < 0.18
            fill = P['windowLit'] if lit else P['window']
            out.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{ww:.1f}" height="{wh:.1f}" rx="{4 * s:.1f}" fill="{fill}" stroke="{OL}" stroke-width="{wsw:.1f}"/>')
            out.append(f'<path d="M{wx + ww * 0.15:.1f} {wy + wh * 0.75:.1f} L{wx + ww * 0.55:.1f} {wy + wh * 0.15:.1f}" stroke="#FFFFFF" stroke-width="{3 * s:.1f}" opacity="0.6" stroke-linecap="round"/>')
            if r.random() < 0.25:   # flower box
                out.append(f'<rect x="{wx - 3 * s:.1f}" y="{wy + wh:.1f}" width="{ww + 6 * s:.1f}" height="{8 * s:.1f}" fill="{P["wood"]}" stroke="{OL}" stroke-width="{wsw:.1f}"/>')
                for k in range(3):
                    out.append(f'<circle cx="{wx + ww * (0.2 + 0.3 * k):.1f}" cy="{wy + wh - 1:.1f}" r="{5 * s:.1f}" fill="{["#FF7FA8", "#FFD23F", "#FF9A3C"][k]}"/>')
    # shop front with striped awning
    sy = base - shop_h
    aw = ROOFS[(idx + 2) % len(ROOFS)]
    out.append(f'<rect x="{x0 + w * 0.12:.1f}" y="{sy + 18 * s:.1f}" width="{w * 0.76:.1f}" height="{shop_h - 18 * s:.1f}" fill="{P["window"]}" stroke="{OL}" stroke-width="{wsw:.1f}"/>')
    stripes = 6
    for k in range(stripes):
        xa = x0 + w * 0.06 + (w * 0.88) * k / stripes
        out.append(f'<path d="M{xa:.1f} {sy - 4 * s:.1f} h{w * 0.88 / stripes:.1f} v{26 * s:.1f} q{-w * 0.44 / stripes:.1f} {12 * s:.1f} {-w * 0.88 / stripes:.1f} 0 Z" '
                   f'fill="{aw if k % 2 == 0 else "#FFFFFF"}" stroke="{OL}" stroke-width="{wsw:.1f}" stroke-linejoin="round"/>')
    return ''.join(out), (x0 if side < 0 else x1)


def street_side(side):
    r = rng(100 + side)
    items = []
    t = 0.03
    idx = 0 if side < 0 else 3
    while t < 0.56:
        y = HORIZON + t * (H - HORIZON)
        s = 0.22 + 0.85 * t
        inner = VX + side * (walk_half(t) + 4)
        g, outer = building(inner, y, s, side, r, idx)
        items.append((y, g))
        # back rows fill the block out to the screen edge (slightly behind, so drawn first)
        k = 1
        while 0 < outer < W:
            g, outer = building(outer + side * 6 * s, y - 8 * s * k, s * 0.98, side, r, idx + 3 * k)
            items.append((y - 8 * s * k - 0.5, g))
            k += 1
        # a lamp and a tree on the sidewalk in front of every other building
        if idx % 2 == 0:
            ly = y + 26 * s
            lt = depth(ly)
            items.append((ly + 1, lamp(VX + side * (road_half(lt) + 20 * lt + 8), ly, 0.25 + 0.85 * lt)))
        else:
            ty = y + 30 * s
            tt = depth(ty)
            items.append((ty + 1, round_tree(VX + side * (walk_half(tt) - 30 * tt), ty, 0.3 + 0.7 * tt, P['green'])))
        idx += 1
        t += 0.05 + 0.09 * t
    return items


# ---------------- park at the bottom ----------------

def pond(x, y, rx, ry):
    out = [f'<ellipse cx="{x}" cy="{y + 10}" rx="{rx + 10}" ry="{ry + 8}" fill="#B99A6A" stroke="{OL}" stroke-width="7"/>',
           f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#water)" stroke="{OL}" stroke-width="6"/>',
           f'<path d="M{x - rx * 0.6} {y - ry * 0.35} q{rx * 0.3} -{ry * 0.2} {rx * 0.6} 0" stroke="#FFFFFF" stroke-width="6" fill="none" stroke-linecap="round" opacity="0.7"/>',
           f'<path d="M{x + rx * 0.1} {y + ry * 0.3} q{rx * 0.2} -{ry * 0.12} {rx * 0.4} 0" stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.5"/>']
    for dx, dy in [(-0.45, 0.2), (0.4, -0.15), (0.55, 0.35)]:
        out.append(f'<path d="M{x + rx * dx:.1f} {y + ry * dy:.1f} m-18 0 a18 11 0 1 0 36 0 l-18 -2 Z" fill="#6CC24A" stroke="{OL}" stroke-width="3"/>')
    # a duck
    dx, dy = x + rx * 0.05, y - ry * 0.05
    out.append(f'<g stroke="{OL}" stroke-width="4" stroke-linejoin="round"><path d="M{dx - 26} {dy} q4 -22 30 -16 q4 -18 18 -14 q14 6 4 18 q10 4 2 14 Z" fill="#FFFFFF"/>'
               f'<path d="M{dx + 30} {dy - 26} l14 4 l-12 4 Z" fill="#FFB21E"/></g><circle cx="{dx + 24}" cy="{dy - 26}" r="3" fill="{OL}"/>')
    return ''.join(out)


def park():
    r = rng(42)
    items = []
    top = ty(T_END + 0.1)
    items.append((ty(0.80) - 120, pond(170, ty(0.80) - 20, 150, 70)))
    # hedges along the footpath
    y = top + 60
    while y < H + 40:
        u = (y - ty(0.64)) / (H - ty(0.64))
        half = 150 + 90 * u
        for side in (-1, 1):
            if side < 0 and ty(0.76) < y < ty(0.86):
                continue
            items.append((y, bush(path_x(y) + side * (half + 46), y, 0.75 + 0.35 * u, '#5DB03E' if side < 0 else '#66B844')))
        y += 150
    # big edge trees, cropped by the screen edge: strong foreground depth
    for x, t, s, c in [(30, 0.70, 1.25, '#5FB845'), (1050, 0.68, 1.3, '#7CCB4E'), (-10, 0.92, 1.9, '#6CC24A'),
                       (1090, 0.88, 1.8, '#5FB845'), (980, 0.78, 1.1, '#6CC24A'), (90, 1.02, 1.6, '#7CCB4E'),
                       (960, 1.03, 1.5, '#6CC24A')]:
        items.append((ty(t), round_tree(x, ty(t), s, c)))
    for x, t, s in [(330, 0.78, 0.95), (760, 0.95, 1.1)]:
        items.append((ty(t), bench(x, ty(t), s)))
    for x, t in [(330, 0.86), (790, 0.80), (300, 1.0)]:
        items.append((ty(t), lamp(x, ty(t), 1.0 + 0.3 * (t - 0.7))))
    # flower beds
    for cx, t, n in [(820, 0.80, 14), (290, 1.0, 12), (850, 0.98, 10)]:
        yb = ty(t)
        items.append((yb - 30, f'<ellipse cx="{cx}" cy="{yb - 10}" rx="110" ry="34" fill="#8A5326" stroke="{OL}" stroke-width="6"/>'
                      f'<ellipse cx="{cx}" cy="{yb - 16}" rx="98" ry="26" fill="#6B3E1C"/>'))
        for k in range(n):
            fx = cx + r.uniform(-85, 85)
            fy = yb - 16 + r.uniform(-14, 10)
            items.append((yb - 29, flower(fx, fy, 1.2, r.choice(['#FF7FA8', '#FFFFFF', '#FFD23F', '#C58BF2', '#FF9A3C']))))
    for _ in range(70):
        t = r.uniform(T_END + 0.08, 1.02)
        y = ty(t)
        u = (y - ty(0.64)) / (H - ty(0.64))
        half = 150 + 90 * u
        side = r.choice((-1, 1))
        x = path_x(y) + side * r.uniform(half + 30, half + 420)
        if -20 < x < W + 20:
            items.append((y - 60, grass_tuft(x, y, 0.8 + 0.6 * u, '#4E9F36')))
    for _ in range(40):
        t = r.uniform(T_END + 0.08, 1.0)
        y = ty(t)
        u = (y - ty(0.64)) / (H - ty(0.64))
        half = 150 + 90 * u
        x = path_x(y) + r.choice((-1, 1)) * r.uniform(half + 40, half + 380)
        items.append((y - 59, flower(x, y, 0.9 + 0.5 * u, r.choice(['#FF7FA8', '#FFFFFF', '#FFD23F', '#C58BF2']))))
    return items


def traffic():
    items = []
    for t, lane, c in [(0.16, 0.45, '#3A7BD5'), (0.34, -0.5, '#FFC93C'), (0.47, 0.55, '#E5533D')]:
        y = HORIZON + t * (H - HORIZON)
        items.append((y, car(VX + lane * road_half(t), y, 0.3 + 0.8 * t, c)))
    return items


def defs():
    return (lin('sky', [(0, '#6FBDEB', 1), (0.55, '#BFE4F8', 1), (0.86, '#FFE7B8', 1), (1, '#FFD9A0', 1)]) +
            rad('sunGlow', [(0, '#FFF3C4', 0.9), (0.4, '#FFE39A', 0.45), (1, '#FFE39A', 0)]) +
            lin('ground', [(0, '#D3E9B2', 1), (0.2, '#A9D97C', 1), (1, '#78C452', 1)]) +
            lin('grass', [(0, '#93D466', 1), (1, '#6DBE45', 1)]) +
            lin('cobble', [(0, '#F3E2BF', 1), (1, '#EAD2A2', 1)]) +
            lin('water', [(0, '#7FD0F5', 1), (1, '#3FA2DE', 1)]) +
            lin('road', [(0, '#CFC4B4', 1), (1, '#B5A794', 1)]) +
            lin('haze', [(0, '#FFF1D6', 0.75), (1, '#FFF1D6', 0)]) +
            lin('fadeBottom', [(0, '#2A1205', 0), (1, '#2A1205', 0.18)]))


def build():
    body = [sky(), skyline(), ground()]
    items = street_side(-1) + street_side(1) + park() + traffic()
    items.sort(key=lambda it: it[0])            # painter's order: far (top) first
    body += [it[1] for it in items]
    # atmospheric haze over the far street and a gentle darkening at the very bottom
    body.append(f'<rect y="{HORIZON - 20}" width="{W}" height="520" fill="url(#haze)"/>')
    body.append(f'<rect y="{H - 260}" width="{W}" height="260" fill="url(#fadeBottom)"/>')
    return svg(''.join(body), defs())


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'map_city.svg'
    open(out, 'w').write(build())
    print('wrote', out)
