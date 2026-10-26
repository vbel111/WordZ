"""Word Z map engine v3 - high-angle 3/4 worlds (see city2.py for the first hand-built one).

A World collects layers and standing objects, keeps track of what ground is taken (rivers, paths, plazas,
buildings) and draws everything back-to-front by base y (painter's algorithm).

    w = World(seed)
    w.sky = sky_day(); w.back = skyline(...); w.ground = grass()
    w.river([...]) / w.path([...]) / w.plaza(...)
    w.add(y, svg) for landmarks, w.rows(...) to pack buildings, w.scatter(...) to fill gaps with flora
    return w.render()
"""
import math
from style import OL, PALETTE, mix, shade, svg, lin, rad, contact_shadow, cloud, bird, rng
from city2 import S, sw, pts, poly, catmull, HY, W, H

GREENS = ['#5CBF3F', '#6CC24A', '#4FB043', '#7DCB4E', '#58B74A']


class World:
    def __init__(self, seed=1):
        self.r = rng(seed)
        self.seed = seed
        self.defs = []
        self.sky = ''
        self.back = ''
        self.ground = ''
        self.flat = []          # ground decals (paths, plazas, rivers) in draw order
        self.items = []         # (y, order, svg)
        self.fg = ''
        self.occupied = []      # (x0, y0, x1, y1)
        self.flows = []         # (centreline, width_fn, pad)
        self.zones = []         # (cx, cy, rx, ry)

    # ---------------------------------------------------------- bookkeeping
    def add(self, y, s, order=0):
        self.items.append((y, order, s))

    def occ(self, x0, y0, x1, y1):
        self.occupied.append((x0, y0, x1, y1))

    def hit(self, x, y, pad=0.0, occ_pad=(20, 70, 30)):
        s = S(y)
        for cl, wf, extra in self.flows:
            if y < cl[0][1] - 40 and y < cl[-1][1] - 40:
                continue
            best = min(cl, key=lambda p: abs(p[1] - y) + abs(p[0] - x) * 0.25)
            if math.hypot(x - best[0], (y - best[1]) * 1.6) < wf(best[1]) / 2 + extra * S(best[1]) + pad * s:
                return True
        for cx, cy, rx, ry in self.zones:
            if ((x - cx) / (rx + pad * s)) ** 2 + ((y - cy) / (ry + pad * s * 0.5)) ** 2 < 1:
                return True
        px, py0, py1 = occ_pad
        for o in self.occupied:
            if o[0] - px * s < x < o[2] + px * s and o[1] - py0 * s < y < o[3] + py1 * s:
                return True
        return False

    # ---------------------------------------------------------- ground features
    @staticmethod
    def edges(cl, wf, extra=0.0, squash=0.55):
        L, Rr = [], []
        for i, (x, y) in enumerate(cl):
            a, b = cl[max(0, i - 1)], cl[min(len(cl) - 1, i + 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(dx, dy) or 1
            nx, ny = -dy / ln, dx / ln
            hw = wf(y) / 2 + extra * S(y)
            L.append((x + nx * hw, y + ny * hw * squash))
            Rr.append((x - nx * hw, y - ny * hw * squash))
        return L, Rr

    def river(self, points, w0=56, w1=330, water=('#7DD3F7', '#2E9BE0'), bank='#E6D3A8', wall='#B99A6C', ripples=True, rails=True):
        cl = catmull(points)
        wf = lambda y: w0 + w1 * max(0.0, y - HY) / (H - HY)
        self.flows.append((cl, wf, 26))
        L, Rr = self.edges(cl, wf)
        L2, R2 = self.edges(cl, wf, 26)
        gid = f'wat{len(self.flows)}'
        self.defs.append(lin(gid, [(0, water[0], 1), (1, water[1], 1)]))
        self.defs.append(f'<clipPath id="{gid}c"><polygon points="{pts(L + Rr[::-1])}"/></clipPath>')
        shift = [(x, y + 16 * S(y)) for x, y in L] + [(x, y + 16 * S(y)) for x, y in Rr[::-1]]
        out = [poly(L2 + R2[::-1], bank, w=6), poly(L + Rr[::-1], wall),
               f'<g clip-path="url(#{gid}c)"><polygon points="{pts(shift)}" fill="url(#{gid})"/>']
        if ripples:
            for i in range(0, len(cl), 2):
                x, y = cl[i]
                if y < HY + 20:
                    continue
                s = S(y)
                for _ in range(2):
                    ox = self.r.uniform(-0.38, 0.38) * wf(y)
                    out.append(f'<path d="M{x + ox - 18 * s:.1f} {y + 10 * s:.1f} q{9 * s:.1f} {-7 * s:.1f} {18 * s:.1f} 0 q{9 * s:.1f} {7 * s:.1f} {18 * s:.1f} 0" '
                               f'fill="none" stroke="#FFFFFF" stroke-width="{max(1.5, 4 * s):.1f}" stroke-linecap="round" opacity="0.7"/>')
        out.append('</g>')
        out.append(f'<polygon points="{pts(L + Rr[::-1])}" fill="none" stroke="{OL}" stroke-width="5" stroke-linejoin="round"/>')
        if rails:
            for i in range(6, len(cl) - 4, 5):
                for P in (L2, R2):
                    x, y = P[i]
                    s = S(y)
                    out.append(f'<rect x="{x - 3 * s:.1f}" y="{y - 14 * s:.1f}" width="{6 * s:.1f}" height="{14 * s:.1f}" fill="#5C6B80" stroke="{OL}" stroke-width="{max(1.2, 2.5 * s):.1f}"/>')
        self.flat.append(''.join(out))
        return cl, wf

    def path(self, points, w0=40, w1=150, fill='#EBD9B0', edge='#C9AE7E', dash=None, tiles=None, n=16, reserve=True, outline=True):
        """ground ribbon (dirt path, road, carpet, track). Returns its centreline."""
        cl = catmull(points, n)
        wf = lambda y: w0 + w1 * max(0.0, y - HY) / (H - HY)
        if reserve:
            self.flows.append((cl, wf, 12))
        L, Rr = self.edges(cl, wf, 0, squash=0.75)
        L2, R2 = self.edges(cl, wf, 9, squash=0.75)
        out = []
        if outline:
            out.append(poly(L2 + R2[::-1], edge, w=5))
        out.append(poly(L + Rr[::-1], fill))
        if tiles:   # alternating cross bands (checker / piano / track lines)
            c1, step = tiles
            for i in range(0, len(cl) - step, step * 2):
                quad = [L[i], L[i + step], Rr[i + step], Rr[i]]
                out.append(poly(quad, c1))
        if dash:
            d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in cl)
            out.append(f'<path d="{d}" fill="none" stroke="{dash}" stroke-width="6" stroke-dasharray="30 28" opacity="0.85"/>')
        self.flat.append(''.join(out))
        return cl, wf, L, Rr

    def plaza(self, cx, cy, rx, ry, fill='#EEDDB8', ring='#D8C39A', reserve=True):
        if reserve:
            self.zones.append((cx, cy, rx, ry))
        out = [f'<ellipse cx="{cx}" cy="{cy + 6}" rx="{rx}" ry="{ry}" fill="{shade(fill, -0.18)}"/>',
               f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{OL}" stroke-width="4"/>']
        for q in range(1, 4):
            out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * q / 4:.0f}" ry="{ry * q / 4:.0f}" fill="none" stroke="{ring}" stroke-width="3"/>')
        self.flat.append(''.join(out))

    def patch(self, pts_, fill, stroke=OL, reserve_box=True, extra=''):
        """flat ground patch polygon (field, pitch, pond bed). Optionally reserves its bounding box."""
        if reserve_box:
            xs, ys = [p[0] for p in pts_], [p[1] for p in pts_]
            self.occ(min(xs), min(ys), max(xs), max(ys))
        self.flat.append(poly(pts_, fill, stroke=stroke, w=4) + extra)

    # ---------------------------------------------------------- filling
    def rows(self, row_ys, factory, gap=0.2, gap_far=0.34, x_from=-50, x_to=W + 40, wmin=105, wmax=150, pad=30):
        """pack objects along rows. factory(x, by, w, s, side, r, idx) -> (svg, used_width, height)"""
        r = self.r
        for ri, by in enumerate(row_ys):
            s = S(by)
            x = x_from + r.uniform(0, 60) * s
            row = []
            while x < x_to:
                w = r.uniform(wmin, wmax) * s
                cx = x + w / 2
                if (self.hit(cx, by, pad, (10, 40, 40)) or self.hit(x + 4, by, 6, (0, 0, 0)) or self.hit(x + w - 4, by, 6, (0, 0, 0))
                        or r.random() < (gap_far if by < 820 else gap)):
                    x += w * r.uniform(0.5, 0.9)
                    continue
                row.append((x, w, 'r' if cx < 540 else 'l'))
                x += w - 2 * s
            left = [q for q in row if q[2] == 'r']
            right = [q for q in row if q[2] == 'l'][::-1]
            new = []
            for order, (hx, w, side) in enumerate(left + right):
                svg_, used, h = factory(hx, by, w, s, side, r, ri * 50 + order)
                self.add(by, svg_, order)
                new.append((hx, by - 30 * s, hx + w, by + 10))
            self.occupied.extend(new)

    def scatter(self, choices, y0=560, y1=2320, density=0.62, step=(70, 110), pad=40):
        """fill free ground. choices: list of (weight, fn(x, y, s, r, i))"""
        r = self.r
        total = sum(c[0] for c in choices)
        y = y0
        i = 0
        while y < y1:
            s = S(y)
            x = r.uniform(-20, 40)
            while x < W + 20:
                if not self.hit(x, y, pad) and r.random() < density:
                    pick = r.uniform(0, total)
                    for wgt, fn in choices:
                        pick -= wgt
                        if pick <= 0:
                            self.add(y, fn(x + r.uniform(-12, 12) * s, y, s * r.uniform(0.85, 1.12), r, i))
                            break
                    i += 1
                x += r.uniform(*step) * s
            y += 58 * s

    # ---------------------------------------------------------- output
    def render(self):
        self.items.sort(key=lambda t: (t[0], t[1]))
        body = self.sky + self.back + self.ground + ''.join(self.flat) + ''.join(s for _, _, s in self.items) + self.fg
        return svg(body, ''.join(self.defs))


# =============================================================== skies & backdrops

def sky_day(sun=(880, 300), top='#5DB8F2', mid='#9FD8F8', low='#FFF0C8', clouds=True, seed=4):
    r = rng(seed)
    d = (lin('sky3', [(0, top, 1), (0.55, mid, 1), (1, low, 1)]) +
         rad('sun3', [(0, '#FFF6C2', 1), (0.25, '#FFE680', 0.9), (1, '#FFE680', 0)]))
    out = [f'<defs>{d}</defs><rect width="{W}" height="{HY + 140}" fill="url(#sky3)"/>']
    if sun:
        out += [f'<circle cx="{sun[0]}" cy="{sun[1]}" r="260" fill="url(#sun3)" opacity="0.8"/>',
                f'<circle cx="{sun[0]}" cy="{sun[1]}" r="70" fill="#FFE47A" stroke="#F4C24A" stroke-width="6"/>',
                f'<circle cx="{sun[0] - 20}" cy="{sun[1] - 18}" r="44" fill="#FFF3B8" opacity="0.7"/>']
    if clouds:
        for x, y, s, o in [(130, 120, 1.15, 1), (420, 70, 0.8, 0.95), (720, 160, 0.9, 0.9), (1000, 90, 0.95, 1), (260, 300, 0.7, 0.85), (560, 250, 0.55, 0.8)]:
            out.append(cloud(x + r.uniform(-30, 30), y + r.uniform(-15, 15), s, o))
        for x, y, s in [(640, 190, 1.0), (680, 170, 0.8), (720, 215, 0.7)]:
            out.append(bird(x, y, s, o=0.55))
    return ''.join(out)


def sky_dusk(sun=(540, 430)):
    d = (lin('sky3d', [(0, '#3E3A8C', 1), (0.45, '#C9619E', 1), (0.8, '#FF9F6B', 1), (1, '#FFD39A', 1)]) +
         rad('sun3d', [(0, '#FFF0B0', 1), (0.3, '#FFC46B', 0.8), (1, '#FF9F6B', 0)]))
    out = [f'<defs>{d}</defs><rect width="{W}" height="{HY + 140}" fill="url(#sky3d)"/>',
           f'<circle cx="{sun[0]}" cy="{sun[1]}" r="300" fill="url(#sun3d)"/>',
           f'<circle cx="{sun[0]}" cy="{sun[1]}" r="80" fill="#FFD36B"/>']
    r = rng(2)
    for _ in range(40):
        out.append(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, 220):.0f}" r="{r.uniform(1.5, 3.5):.1f}" fill="#FFFFFF" opacity="{r.uniform(0.4, 0.9):.2f}"/>')
    for x, y, s in [(200, 200, 0.8), (880, 150, 0.7)]:
        out.append(cloud(x, y, s, 0.55, '#FFD6E0'))
    return ''.join(out)


def sky_night(moon=(860, 180), top='#141A4A', low='#3B4FA0', stars=110, seed=3):
    r = rng(seed)
    d = lin('sky3n', [(0, top, 1), (1, low, 1)])
    out = [f'<defs>{d}</defs><rect width="{W}" height="{HY + 140}" fill="url(#sky3n)"/>']
    for _ in range(stars):
        x, y = r.uniform(0, W), r.uniform(0, HY)
        rr = r.uniform(1.2, 3.6)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="#FFFFFF" opacity="{r.uniform(0.35, 1):.2f}"/>')
    for _ in range(8):
        x, y, s = r.uniform(40, W - 40), r.uniform(30, HY - 60), r.uniform(0.6, 1.2)
        out.append(f'<path d="M{x} {y - 14 * s} Q{x + 2 * s} {y - 2 * s} {x + 14 * s} {y} Q{x + 2 * s} {y + 2 * s} {x} {y + 14 * s} Q{x - 2 * s} {y + 2 * s} {x - 14 * s} {y} Q{x - 2 * s} {y - 2 * s} {x} {y - 14 * s} Z" fill="#FFF6C8"/>')
    if moon:
        out.append(f'<circle cx="{moon[0]}" cy="{moon[1]}" r="120" fill="#FFF6C8" opacity="0.12"/>')
        out.append(f'<circle cx="{moon[0]}" cy="{moon[1]}" r="58" fill="#FFF3C4" stroke="#E8D48A" stroke-width="5"/>')
        out.append(f'<circle cx="{moon[0] + 18}" cy="{moon[1] - 10}" r="12" fill="#EADBA0"/><circle cx="{moon[0] - 16}" cy="{moon[1] + 18}" r="8" fill="#EADBA0"/>')
    return ''.join(out)


def skyline(base_tint=('#C3DBF1', '#A7C6E6'), near=('#A9CBEA', '#7FA8D6'), seed=3, gap=(780, 960), tower=600):
    r = rng(seed)
    out = []
    for layer, (haze, deep, hmin, hmax, base) in enumerate([(base_tint[0], base_tint[1], 120, 260, HY + 10), (near[0], near[1], 60, 190, HY + 30)]):
        x = -20 - layer * 30
        while x < W + 20:
            w = r.uniform(38, 84)
            h = r.uniform(hmin, hmax)
            if gap and gap[0] < x < gap[1]:
                h *= 0.55
            c = mix(haze, deep, r.uniform(0, 0.5))
            top = base - h
            out.append(f'<rect x="{x:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h + 40:.1f}" fill="{c}"/>')
            out.append(f'<rect x="{x + w - 7:.1f}" y="{top:.1f}" width="7" height="{h + 40:.1f}" fill="#FFFFFF" opacity="0.25"/>')
            for wy in range(int(top + 10), int(base + 20), 14):
                for wx in range(int(x + 6), int(x + w - 10), 12):
                    if r.random() < 0.5:
                        out.append(f'<rect x="{wx}" y="{wy}" width="5" height="7" fill="#E4F0FC" opacity="0.6"/>')
            x += w + r.uniform(-4, 14)
    if tower:
        tx = tower
        c = near[1]
        out.append(f'<path d="M{tx - 8} {HY + 30} L{tx - 4} {HY - 200} L{tx + 4} {HY - 200} L{tx + 8} {HY + 30} Z" fill="{c}"/>'
                   f'<ellipse cx="{tx}" cy="{HY - 200}" rx="22" ry="16" fill="{c}"/><rect x="{tx - 2}" y="{HY - 300}" width="4" height="90" fill="{c}"/>')
    return ''.join(out)


def mountains(peaks=None, far='#9EC3E6', near='#7FB0D8', snow='#FFFFFF', seed=6, base=HY + 40):
    r = rng(seed)
    peaks = peaks or [(-60, 300), (180, 230), (420, 330), (700, 250), (960, 320), (1160, 280)]
    out = []
    for layer, (col, scale, yoff) in enumerate([(far, 1.0, 0), (near, 0.7, 30)]):
        for i, (px, ph) in enumerate(peaks):
            px2 = px + (130 if layer else 0)
            ph2 = ph * scale + r.uniform(-20, 20)
            wdt = r.uniform(260, 340)
            top = base + yoff - ph2
            out.append(f'<path d="M{px2 - wdt:.0f} {base + yoff + 10} L{px2 - 30:.0f} {top + 20:.0f} Q{px2:.0f} {top - 6:.0f} {px2 + 30:.0f} {top + 20:.0f} L{px2 + wdt:.0f} {base + yoff + 10} Z" fill="{col}"/>')
            out.append(f'<path d="M{px2:.0f} {top + 4:.0f} L{px2 + 30:.0f} {top + 20:.0f} L{px2 + wdt:.0f} {base + yoff + 10} L{px2 + wdt * 0.4:.0f} {base + yoff + 10} Z" fill="{shade(col, -0.12)}" opacity="0.6"/>')
            if snow and ph2 > 200:
                sh = ph2 * 0.28
                out.append(f'<path d="M{px2 - sh * 0.8:.0f} {top + sh:.0f} L{px2 - 30:.0f} {top + 20:.0f} Q{px2:.0f} {top - 6:.0f} {px2 + 30:.0f} {top + 20:.0f} L{px2 + sh * 0.8:.0f} {top + sh:.0f} '
                           f'L{px2 + sh * 0.3:.0f} {top + sh * 0.75:.0f} L{px2:.0f} {top + sh:.0f} L{px2 - sh * 0.3:.0f} {top + sh * 0.75:.0f} Z" fill="{snow}"/>')
    return ''.join(out)


def hills(cols=('#B5DE86', '#9ED46E'), seed=8):
    r = rng(seed)
    out = []
    for layer, col in enumerate(cols):
        y = HY + 10 + layer * 18
        d = f'M0 {y + 40} '
        x = 0
        while x < W:
            nx = x + r.uniform(160, 280)
            d += f'Q{(x + nx) / 2:.0f} {y - r.uniform(20, 60):.0f} {nx:.0f} {y + r.uniform(-5, 15):.0f} '
            x = nx
        d += f'L{W} {y + 80} L0 {y + 80} Z'
        out.append(f'<path d="{d}" fill="{col}"/>')
    return ''.join(out)


def sea_horizon(col=('#5FB8EA', '#3C97D6')):
    return (f'<rect x="0" y="{HY - 10}" width="{W}" height="60" fill="{col[0]}"/>'
            f'<rect x="0" y="{HY + 20}" width="{W}" height="30" fill="{col[1]}"/>'
            + ''.join(f'<path d="M{x} {HY + 8} q10 -5 20 0" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.6"/>' for x in range(30, W, 90)))


def grass(top='#A3DB6E', bottom='#6CC04A', tufts=160, tuft='#4E9F36', seed=9, stripes=True):
    r = rng(seed)
    d = lin('gr3', [(0, top, 1), (1, bottom, 1)])
    out = [f'<defs>{d}</defs><rect x="0" y="{HY + 20}" width="{W}" height="{H - HY}" fill="url(#gr3)"/>']
    if stripes:
        for q in range(40):
            y = HY + 40 + q * 48
            out.append(f'<rect x="0" y="{y}" width="{W}" height="{12 * S(y):.1f}" fill="#FFFFFF" opacity="0.05"/>')
    for q in range(tufts):
        x, y = r.uniform(0, W), r.uniform(HY + 60, H)
        s = S(y)
        out.append(f'<path d="M{x - 6 * s:.1f} {y:.1f} q{3 * s:.1f} {-10 * s:.1f} {6 * s:.1f} 0 q{3 * s:.1f} {-12 * s:.1f} {6 * s:.1f} 0" fill="{tuft}" opacity="0.55"/>')
    return ''.join(out)


def haze_and_rays(sun=(880, 300), haze='#FFF6DE', rays=True, h=340, op=0.7):
    out = [lin('hz3', [(0, haze, op), (1, haze, 0)]), f'<rect x="0" y="{HY}" width="{W}" height="{h}" fill="url(#hz3)"/>']
    if rays and sun:
        for a, o in [(-0.4, 0.08), (-0.2, 0.06), (0.05, 0.07)]:
            out.append(f'<path d="M{sun[0]} {sun[1]} L{sun[0] + math.cos(math.pi * 0.62 + a) * 1600:.0f} {sun[1] + math.sin(math.pi * 0.62 + a) * 1600:.0f} '
                       f'L{sun[0] + math.cos(math.pi * 0.62 + a + 0.07) * 1600:.0f} {sun[1] + math.sin(math.pi * 0.62 + a + 0.07) * 1600:.0f} Z" fill="#FFF3C4" opacity="{o}"/>')
    return ''.join(out)
