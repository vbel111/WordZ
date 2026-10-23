"""Shared scene engine for the v2 maps: sky, far backdrop, a path receding to the horizon, and props
placed in perspective on both sides (painter's order). Category files describe *what* is in the scene;
this file handles *where* and *how big*, so every map shares one camera and one look."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from style import H, OL, W, cloud, contact_shadow, lin, mix, rad, rng, shade, svg  # noqa: E402,F401

HORIZON = 930
VX = W / 2


class Scene:
    def __init__(self, seed=1, horizon=HORIZON, path_w=(70, 420), curve=80.0, curve_freq=1.3):
        self.r = rng(seed)
        self.horizon = horizon
        self.path_w = path_w
        self.curve = curve
        self.curve_freq = curve_freq
        self.back = []        # drawn first, in order (sky, backdrop, ground, path)
        self.items = []       # (sort_y, svg) painter-sorted
        self.front = []       # overlays (haze, vignette)
        self.defs = []

    # ---- camera ----
    def ty(self, t):
        return self.horizon + t * (H - self.horizon)

    def tdepth(self, y):
        return (y - self.horizon) / (H - self.horizon)

    def scale(self, t):
        return 0.3 + 1.45 * t

    def path_cx(self, t):
        return VX + math.sin(t * math.pi * self.curve_freq) * self.curve * t

    def path_half(self, t):
        a, b = self.path_w
        return a / 2 + (b - a) / 2 * t

    def side_x(self, t, side, off):
        """x of a point `off` (scaled by depth) beyond the path edge on `side` (-1 left, +1 right)."""
        return self.path_cx(t) + side * (self.path_half(t) + off * self.scale(t))

    # ---- adding things ----
    def add(self, y, g):
        self.items.append((y, g))

    def place(self, fn, t, side, off, *args, **kw):
        y = self.ty(t)
        x = self.side_x(t, side, off)
        self.items.append((y, fn(x, y, self.scale(t), *args, **kw)))

    def at(self, fn, x, t, scale_mul=1.0, *args, **kw):
        y = self.ty(t)
        self.items.append((y, fn(x, y, self.scale(t) * scale_mul, *args, **kw)))

    def scatter(self, fn, n, t0, t1, off0, off1, *args, sides=(-1, 1), sort_bias=-60, **kw):
        for _ in range(n):
            t = self.r.uniform(t0, t1)
            side = self.r.choice(sides)
            y = self.ty(t)
            x = self.side_x(t, side, self.r.uniform(off0, off1))
            if -40 < x < W + 40:
                self.items.append((y + sort_bias, fn(x, y, self.scale(t), *args, **kw)))

    def populate(self, choices, t0=0.03, t1=1.0, step=0.06, gap=135, start=(60, 110), sides=(-1, 1), jitter=0.4, skip=0.0, max_off=9999, avoid=(), far_thin=0.6):
        """Fills the land on each side, from the path edge out past the screen edge, row after row.
        choices: list of (weight, fn) where fn(x, y, s) draws a prop."""
        total = sum(w for w, _ in choices)

        def pick():
            v = self.r.uniform(0, total)
            for w, fn in choices:
                v -= w
                if v <= 0:
                    return fn
            return choices[-1][1]
        t = t0
        while t < t1:
            for side in sides:
                off = self.r.uniform(*start)
                while True:
                    tt = min(1.04, t + self.r.uniform(-0.3, 0.3) * step * (0.4 + t))
                    x = self.side_x(tt, side, off)
                    if x < -90 or x > W + 90 or off > max_off:
                        break
                    y0 = self.ty(tt)
                    blocked = any(((x - ax) / arx) ** 2 + ((y0 - ay) / ary) ** 2 < 1 for ax, ay, arx, ary in avoid)
                    if not blocked and self.r.random() >= skip + far_thin * (1 - min(1, tt)) ** 2:
                        y = self.ty(tt)
                        self.items.append((y, pick()(x, y, self.scale(tt) * self.r.uniform(1 - jitter / 3, 1 + jitter / 3))))
                    off += gap * self.r.uniform(0.75, 1.3)
            t += step * (0.4 + t)

    # ---- big layers ----
    def sky(self, stops, sun=None, moon=None, stars=0, clouds=(), birds=()):
        self.defs.append(lin('skyG', [(o, c, 1) for o, c in stops]))
        self.back.append(f'<rect width="{W}" height="{self.horizon + 60}" fill="url(#skyG)"/>')
        if stars:
            for _ in range(stars):
                x, y = self.r.uniform(0, W), self.r.uniform(0, self.horizon - 80)
                rr = self.r.choice([1.5, 2, 2.5, 3.5])
                self.back.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr}" fill="#FFFFFF" opacity="{self.r.uniform(0.5, 1):.2f}"/>')
            for _ in range(stars // 12):
                x, y = self.r.uniform(30, W - 30), self.r.uniform(30, self.horizon - 200)
                s = self.r.uniform(0.8, 1.5)
                self.back.append(sparkle(x, y, s))
        if sun:
            x, y, rr, col = sun
            self.defs.append(rad('sunGlowG', [(0, col, 0.9), (0.4, col, 0.4), (1, col, 0)]))
            self.back.append(f'<circle cx="{x}" cy="{y}" r="{rr * 2.8}" fill="url(#sunGlowG)"/>')
            self.back.append(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="#FFF3C4" stroke="{shade(col, -0.05)}" stroke-width="10"/>')
        if moon:
            x, y, rr = moon
            self.defs.append(rad('moonGlowG', [(0, '#FFF6D8', 0.55), (1, '#FFF6D8', 0)]))
            self.back.append(f'<circle cx="{x}" cy="{y}" r="{rr * 2.6}" fill="url(#moonGlowG)"/>')
            self.back.append(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="#FFF3C4" stroke="#F2D58A" stroke-width="8"/>'
                             f'<circle cx="{x - rr * 0.3}" cy="{y + rr * 0.2}" r="{rr * 0.18}" fill="#F2DDA0"/>'
                             f'<circle cx="{x + rr * 0.35}" cy="{y - rr * 0.25}" r="{rr * 0.12}" fill="#F2DDA0"/>')
        for c in clouds:
            self.back.append(cloud(*c))
        for b in birds:
            from style import bird
            self.back.append(bird(*b))

    def backdrop(self, svg_str):
        self.back.append(svg_str)

    def ground(self, stops):
        self.defs.append(lin('groundG', [(o, c, 1) for o, c in stops]))
        self.back.append(f'<rect y="{self.horizon}" width="{W}" height="{H - self.horizon}" fill="url(#groundG)"/>')

    def path(self, fill, edge=OL, edge_w=7, t0=0.0, texture=None, border=None):
        """Draws the receding path. texture(scene) may add marks on top (planks, stones, lanes)."""
        left, right = [], []
        steps = 60
        for i in range(steps + 1):
            t = t0 + (1.02 - t0) * (i / steps) ** 1.15
            y = self.ty(t)
            left.append((self.path_cx(t) - self.path_half(t), y))
            right.append((self.path_cx(t) + self.path_half(t), y))
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in left) + ' L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(right)) + ' Z'
        if border:
            # a wider band under the path (kerb / sand edge)
            bl, br = [], []
            for i in range(steps + 1):
                t = t0 + (1.02 - t0) * (i / steps) ** 1.15
                y = self.ty(t)
                w = self.path_half(t) + border[1] * self.scale(t)
                bl.append((self.path_cx(t) - w, y)); br.append((self.path_cx(t) + w, y))
            bd = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in bl) + ' L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(br)) + ' Z'
            self.back.append(f'<path d="{bd}" fill="{border[0]}"/>')
        self.back.append(f'<path d="{d}" fill="{fill}" stroke="{edge}" stroke-width="{edge_w}" stroke-linejoin="round"/>')
        if texture:
            self.back.append(texture(self))

    def haze(self, color='#FFF1D6', height=380, opacity=0.55):
        self.defs.append(lin('hazeG', [(0, color, 0), (0.1, color, opacity), (1, color, 0)]))
        self.front.append(f'<rect y="{self.horizon - 40}" width="{W}" height="{height}" fill="url(#hazeG)"/>')

    def bottom_fade(self, opacity=0.18):
        self.defs.append(lin('fadeB', [(0, '#2A1205', 0), (1, '#2A1205', opacity)]))
        self.front.append(f'<rect y="{H - 260}" width="{W}" height="260" fill="url(#fadeB)"/>')

    def render(self):
        self.items.sort(key=lambda it: it[0])
        return svg(''.join(self.back) + ''.join(g for _, g in self.items) + ''.join(self.front), ''.join(self.defs))


# ---------------- textures for paths ----------------

def tex_stones(color='#D9BE8E', n=180, seed=3):
    def f(sc):
        r = rng(seed)
        out = []
        for _ in range(n):
            t = r.uniform(0.02, 1.0) ** 0.8
            y = sc.ty(t)
            half = sc.path_half(t) * 0.85
            x = sc.path_cx(t) + r.uniform(-half, half)
            s = sc.scale(t)
            out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{12 * s:.1f}" ry="{6.5 * s:.1f}" fill="{color}" opacity="0.7"/>')
        return ''.join(out)
    return f


def tex_planks(color='#8A5326', n=40):
    def f(sc):
        out = []
        for i in range(1, n):
            t = (i / n) ** 1.6
            y = sc.ty(t)
            x0, x1 = sc.path_cx(t) - sc.path_half(t), sc.path_cx(t) + sc.path_half(t)
            out.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="{1 + 4 * t:.1f}"/>')
        return ''.join(out)
    return f


def tex_lanes(color='#FFFFFF', lanes=4, opacity=0.8):
    def f(sc):
        out = []
        for k in range(1, lanes):
            pts = []
            for i in range(41):
                t = (i / 40) ** 1.15 * 1.02
                pts.append((sc.path_cx(t) - sc.path_half(t) + 2 * sc.path_half(t) * k / lanes, sc.ty(t)))
            d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
            out.append(f'<path d="{d}" stroke="{color}" stroke-width="5" fill="none" opacity="{opacity}"/>')
        return ''.join(out)
    return f


def tex_dashes(color='#FFF6E0', n=26):
    def f(sc):
        out = []
        for i in range(n):
            t0 = (i / n) ** 1.7
            t1 = ((i + 0.45) / n) ** 1.7
            w0, w1 = 1 + 5 * t0, 1 + 5 * t1
            x0, x1 = sc.path_cx(t0), sc.path_cx(t1)
            out.append(f'<path d="M{x0 - w0:.1f} {sc.ty(t0):.1f} L{x0 + w0:.1f} {sc.ty(t0):.1f} L{x1 + w1:.1f} {sc.ty(t1):.1f} L{x1 - w1:.1f} {sc.ty(t1):.1f} Z" fill="{color}" opacity="0.85"/>')
        return ''.join(out)
    return f


def tex_tiles(c1, c2, rows=22, cols=6):
    def f(sc):
        out = []
        for i in range(rows):
            ta, tb = (i / rows) ** 1.5 * 1.02, ((i + 1) / rows) ** 1.5 * 1.02
            for j in range(cols):
                if (i + j) % 2:
                    continue
                pts = []
                for t, k in ((ta, j), (ta, j + 1), (tb, j + 1), (tb, j)):
                    pts.append((sc.path_cx(t) - sc.path_half(t) + 2 * sc.path_half(t) * k / cols, sc.ty(t)))
                out.append(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)} Z" fill="{c2}"/>')
        return ''.join(out)
    return f


def tex_edge_dots(color='#EFE3CC', every=0.035):
    def f(sc):
        out = []
        t = 0.08
        while t < 1.03:
            s = sc.scale(t)
            for side in (-1, 1):
                x = sc.path_cx(t) + side * sc.path_half(t)
                out.append(f'<circle cx="{x:.1f}" cy="{sc.ty(t):.1f}" r="{7 * s:.1f}" fill="{color}" stroke="{OL}" stroke-width="{max(1.5, 3 * s):.1f}"/>')
            t += every * (0.4 + t)
        return ''.join(out)
    return f


def combine(*fs):
    return lambda sc: ''.join(f(sc) for f in fs)


# ---------------- backdrop helpers ----------------

def hills(horizon, layers, seed=1, amp=(40, 120), base_off=0):
    """layers: list of (color, height_above_horizon). Rolling hills, far to near."""
    r = rng(seed)
    out = []
    for col, hgt in layers:
        pts = []
        x = -60
        while x <= W + 60:
            pts.append((x, horizon + base_off - hgt + r.uniform(-amp[0], amp[0]) * 0.5))
            x += r.uniform(160, 300)
        d = f'M-60 {horizon + 80} L' + ' '.join(f'{x:.0f} {y:.0f}' for x, y in pts[:1])
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            mx = (x0 + x1) / 2
            d += f' Q{x0:.0f} {y0:.0f} {mx:.0f} {(y0 + y1) / 2:.0f}'
        d += f' L{W + 60} {pts[-1][1]:.0f} L{W + 60} {horizon + 80} Z'
        out.append(f'<path d="{d}" fill="{col}"/>')
        out.append(f'<path d="{d}" fill="#FFFFFF" opacity="0.0"/>')
    return ''.join(out)


def mountains(horizon, peaks, color, snow='#FFFFFF', shade_c=None, outline=False):
    """peaks: list of (x, height, half_width)."""
    shade_c = shade_c or shade(color, -0.15)
    out = []
    sw = f' stroke="{OL}" stroke-width="5" stroke-linejoin="round"' if outline else ''
    for x, h, hw in peaks:
        top = horizon - h
        out.append(f'<path d="M{x - hw} {horizon + 40} L{x} {top} L{x + hw} {horizon + 40} Z" fill="{color}"{sw}/>')
        out.append(f'<path d="M{x} {top} L{x + hw} {horizon + 40} L{x + hw * 0.25} {horizon + 40} Z" fill="{shade_c}"/>')
        if snow:
            sh = h * 0.28
            out.append(f'<path d="M{x - hw * sh / h} {top + sh} L{x} {top} L{x + hw * sh / h} {top + sh} '
                       f'L{x + hw * sh / h * 0.4} {top + sh * 0.8} L{x} {top + sh * 1.05} L{x - hw * sh / h * 0.45} {top + sh * 0.8} Z" fill="{snow}"/>')
    return ''.join(out)


def sparkle(x, y, s, c='#FFFFFF', o=0.95):
    return (f'<path d="M{x:.1f} {y - 14 * s:.1f} Q{x + 2 * s:.1f} {y - 2 * s:.1f} {x + 14 * s:.1f} {y:.1f} Q{x + 2 * s:.1f} {y + 2 * s:.1f} {x:.1f} {y + 14 * s:.1f} '
            f'Q{x - 2 * s:.1f} {y + 2 * s:.1f} {x - 14 * s:.1f} {y:.1f} Q{x - 2 * s:.1f} {y - 2 * s:.1f} {x:.1f} {y - 14 * s:.1f} Z" fill="{c}" opacity="{o}"/>')
