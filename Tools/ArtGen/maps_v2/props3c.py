"""v3 props for the special maps: entertainment, tech, space, underwater, shopping, food, wellness."""
import math
from style import OL, PALETTE, mix, shade, contact_shadow, rng
from city2 import sw, poly, pts, townhouse, fluffy_tree
from props3 import g, box


def glow(x, y, r, col, op=0.35):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" opacity="{op}"/>'


def string_lights(x0, y0, x1, y1, s, sag=30, cols=('#FFD23F', '#FF5E7E', '#6FD3FF', '#8CE06A')):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + sag * s
    out = [f'<path d="M{x0:.1f} {y0:.1f} Q{mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{OL}" stroke-width="{2.5 * s:.1f}"/>']
    n = 10
    for i in range(1, n):
        t = i / n
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
        c = cols[i % len(cols)]
        out.append(glow(x, y + 5 * s, 10 * s, c, 0.3) + f'<circle cx="{x:.1f}" cy="{y + 5 * s:.1f}" r="{4.5 * s:.1f}" fill="{c}" {g(s, 0.4)}/>')
    return ''.join(out)


def bunting(x0, y0, x1, y1, s, sag=24, cols=('#FF5E7E', '#FFD23F', '#4FA3E3', '#6CC24A', '#FF8A3D')):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + sag * s
    out = [f'<path d="M{x0:.1f} {y0:.1f} Q{mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{OL}" stroke-width="{2 * s:.1f}"/>']
    n = 9
    for i in range(n):
        t, t2 = i / n + 0.02, (i + 0.8) / n
        def at(t):
            return ((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1)
        a, b = at(t), at(t2)
        out.append(f'<path d="M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f} L{(a[0] + b[0]) / 2:.1f} {(a[1] + b[1]) / 2 + 22 * s:.1f} Z" fill="{cols[i % len(cols)]}" {g(s, 0.4)}/>')
    return ''.join(out)


# ------------------------------------------------------------------ cinema / music
def cinema(x, by, s, w=360, h=230):
    w, h = w * s, h * s
    out = [townhouse(x, by, w, h, s, '#F7E2B4', '#7A3B2A', side='r', floors=2, cols=5, seed=2, flowers=False, roof_kind='flat')]
    top = by - h
    # pediment + columns
    out.append(f'<path d="M{x - 10 * s:.1f} {top:.1f} L{x + w / 2:.1f} {top - 80 * s:.1f} L{x + w + 10 * s:.1f} {top:.1f} Z" fill="#E5533D" {g(s)}/>')
    out.append(f'<circle cx="{x + w / 2:.1f}" cy="{top - 34 * s:.1f}" r="{18 * s:.1f}" fill="#FFD23F" {g(s, 0.7)}/>')
    # marquee
    my = by - h * 0.55
    out.append(f'<rect x="{x + w * 0.12:.1f}" y="{my:.1f}" width="{w * 0.76:.1f}" height="{h * 0.2:.1f}" rx="{8 * s:.1f}" fill="#3B2A55" {g(s)}/>')
    for q in range(16):
        out.append(f'<circle cx="{x + w * 0.14 + q * w * 0.72 / 15:.1f}" cy="{my + 6 * s:.1f}" r="{3.5 * s:.1f}" fill="#FFE27A"/>'
                   f'<circle cx="{x + w * 0.14 + q * w * 0.72 / 15:.1f}" cy="{my + h * 0.2 - 6 * s:.1f}" r="{3.5 * s:.1f}" fill="#FFE27A"/>')
    for q in range(3):
        out.append(f'<rect x="{x + w * (0.25 + q * 0.18):.1f}" y="{my + h * 0.07:.1f}" width="{w * 0.12:.1f}" height="{h * 0.07:.1f}" rx="{3 * s:.1f}" fill="#FFD23F"/>')
    out.append(f'<rect x="{x + w * 0.38:.1f}" y="{by - h * 0.3:.1f}" width="{w * 0.24:.1f}" height="{h * 0.3:.1f}" fill="#8A2A3A" {g(s)}/>')
    return ''.join(out)


def searchlight(x, y, s, ang=-1.2, col='#FFF6C2'):
    ex, ey = x + math.cos(ang) * 1400, y + math.sin(ang) * 1400
    px, py = -math.sin(ang) * 90, math.cos(ang) * 90
    return (f'<path d="M{x:.1f} {y:.1f} L{ex + px:.1f} {ey + py:.1f} L{ex - px:.1f} {ey - py:.1f} Z" fill="{col}" opacity="0.18"/>'
            f'<rect x="{x - 18 * s:.1f}" y="{y - 20 * s:.1f}" width="{36 * s:.1f}" height="{24 * s:.1f}" rx="{6 * s:.1f}" fill="#3C4A5C" {g(s)}/>'
            f'<circle cx="{x:.1f}" cy="{y - 20 * s:.1f}" r="{14 * s:.1f}" fill="#FFF6C2" {g(s)}/>')


def studio(x, by, s, w=230, h=150, side='r', col='#E8E2D6', num='1'):
    w_, h_ = w * s, h * s
    b, dx, dy = box(x, by, w_, h_, s, col, side, dep=w_ * 0.8)
    out = [b]
    top = by - h_
    out.append(f'<path d="M{x:.1f} {top:.1f} Q{x + w_ / 2:.1f} {top - 50 * s:.1f} {x + w_:.1f} {top:.1f} L{x + w_ + dx:.1f} {top + dy:.1f} Q{x + w_ / 2 + dx:.1f} {top - 50 * s + dy:.1f} {x + dx:.1f} {top + dy:.1f} Z" fill="{shade(col, -0.1)}" {g(s)}/>')
    out.append(f'<path d="M{x:.1f} {top:.1f} Q{x + w_ / 2:.1f} {top - 50 * s:.1f} {x + w_:.1f} {top:.1f} Z" fill="{shade(col, 0.1)}" {g(s)}/>')
    out.append(f'<rect x="{x + w_ * 0.3:.1f}" y="{by - h_ * 0.6:.1f}" width="{w_ * 0.4:.1f}" height="{h_ * 0.6:.1f}" fill="#9AA5B1" {g(s)}/>')
    for k in range(1, 6):
        out.append(f'<line x1="{x + w_ * 0.3:.1f}" y1="{by - h_ * 0.6 * k / 6:.1f}" x2="{x + w_ * 0.7:.1f}" y2="{by - h_ * 0.6 * k / 6:.1f}" stroke="#7E8894" stroke-width="{2 * s:.1f}"/>')
    out.append(f'<circle cx="{x + w_ * 0.15:.1f}" cy="{by - h_ * 0.75:.1f}" r="{16 * s:.1f}" fill="#FFD23F" {g(s)}/>'
               f'<text x="{x + w_ * 0.15:.1f}" y="{by - h_ * 0.75 + 7 * s:.1f}" font-family="Baloo" font-weight="800" font-size="{20 * s:.1f}" text-anchor="middle" fill="{OL}">{num}</text>')
    return ''.join(out)


def movie_camera(x, y, s):
    return (contact_shadow(x, y + 2 * s, 30 * s, 6 * s, 0.25) +
            ''.join(f'<line x1="{x:.1f}" y1="{y - 50 * s:.1f}" x2="{x + q * 24 * s:.1f}" y2="{y:.1f}" stroke="{OL}" stroke-width="{4 * s:.1f}"/>' for q in (-1, 0, 1)) +
            f'<rect x="{x - 30 * s:.1f}" y="{y - 84 * s:.1f}" width="{50 * s:.1f}" height="{34 * s:.1f}" rx="{5 * s:.1f}" fill="#3C4A5C" {g(s)}/>'
            f'<path d="M{x + 20 * s:.1f} {y - 74 * s:.1f} L{x + 40 * s:.1f} {y - 84 * s:.1f} L{x + 40 * s:.1f} {y - 50 * s:.1f} L{x + 20 * s:.1f} {y - 60 * s:.1f} Z" fill="#5C6B80" {g(s)}/>'
            f'<circle cx="{x - 16 * s:.1f}" cy="{y - 98 * s:.1f}" r="{14 * s:.1f}" fill="#3C4A5C" {g(s)}/><circle cx="{x + 10 * s:.1f}" cy="{y - 98 * s:.1f}" r="{14 * s:.1f}" fill="#3C4A5C" {g(s)}/>')


def clapper(x, y, s):
    return (f'<rect x="{x - 26 * s:.1f}" y="{y - 36 * s:.1f}" width="{52 * s:.1f}" height="{36 * s:.1f}" fill="#33333D" {g(s)}/>'
            f'<path d="M{x - 28 * s:.1f} {y - 38 * s:.1f} L{x + 24 * s:.1f} {y - 56 * s:.1f} L{x + 28 * s:.1f} {y - 46 * s:.1f} L{x - 24 * s:.1f} {y - 28 * s:.1f} Z" fill="#FFFFFF" {g(s)}/>'
            + ''.join(f'<path d="M{x - 18 * s + q * 14 * s:.1f} {y - 40 * s - q * 5 * s:.1f} l{8 * s:.1f} {-3 * s:.1f} l{3 * s:.1f} {9 * s:.1f} l{-8 * s:.1f} {3 * s:.1f} Z" fill="#33333D"/>' for q in range(3)))


def stage(x, by, s, w=420, h=220, col='#8E3BB8'):
    w, h = w * s, h * s
    out = [contact_shadow(x + w / 2, by + 6 * s, w * 0.6, 20 * s, 0.3),
           f'<rect x="{x:.1f}" y="{by - 40 * s:.1f}" width="{w:.1f}" height="{40 * s:.1f}" fill="#3C3346" {g(s)}/>',
           f'<rect x="{x + 20 * s:.1f}" y="{by - h:.1f}" width="{w - 40 * s:.1f}" height="{h - 40 * s:.1f}" fill="#241C30" {g(s)}/>']
    # truss + roof arc
    out.append(f'<path d="M{x - 10 * s:.1f} {by - h:.1f} Q{x + w / 2:.1f} {by - h - 90 * s:.1f} {x + w + 10 * s:.1f} {by - h:.1f} L{x + w + 10 * s:.1f} {by - h + 26 * s:.1f} Q{x + w / 2:.1f} {by - h - 60 * s:.1f} {x - 10 * s:.1f} {by - h + 26 * s:.1f} Z" fill="{col}" {g(s)}/>')
    for px in (x + 4 * s, x + w - 14 * s):
        out.append(f'<rect x="{px:.1f}" y="{by - h:.1f}" width="{10 * s:.1f}" height="{h - 40 * s:.1f}" fill="#9AA5B1" {g(s, 0.7)}/>')
    # curtains + lights
    out.append(f'<path d="M{x + 20 * s:.1f} {by - h:.1f} L{x + 80 * s:.1f} {by - h:.1f} Q{x + 50 * s:.1f} {by - 120 * s:.1f} {x + 30 * s:.1f} {by - 40 * s:.1f} L{x + 20 * s:.1f} {by - 40 * s:.1f} Z" fill="#D8364A" {g(s, 0.7)}/>')
    out.append(f'<path d="M{x + w - 20 * s:.1f} {by - h:.1f} L{x + w - 80 * s:.1f} {by - h:.1f} Q{x + w - 50 * s:.1f} {by - 120 * s:.1f} {x + w - 30 * s:.1f} {by - 40 * s:.1f} L{x + w - 20 * s:.1f} {by - 40 * s:.1f} Z" fill="#D8364A" {g(s, 0.7)}/>')
    for q, c in enumerate(['#FF5E7E', '#FFD23F', '#6FD3FF', '#8CE06A', '#FF8A3D']):
        lx = x + w * (0.2 + q * 0.15)
        out.append(f'<path d="M{lx:.1f} {by - h + 10 * s:.1f} L{lx - 40 * s:.1f} {by - 40 * s:.1f} L{lx + 40 * s:.1f} {by - 40 * s:.1f} Z" fill="{c}" opacity="0.22"/>'
                   f'<circle cx="{lx:.1f}" cy="{by - h + 10 * s:.1f}" r="{7 * s:.1f}" fill="{c}" {g(s, 0.5)}/>')
    # instruments silhouettes
    out.append(f'<rect x="{x + w * 0.42:.1f}" y="{by - 90 * s:.1f}" width="{w * 0.16:.1f}" height="{30 * s:.1f}" rx="{6 * s:.1f}" fill="#FFD23F" {g(s, 0.7)}/>')
    out.append(f'<circle cx="{x + w * 0.5:.1f}" cy="{by - 106 * s:.1f}" r="{16 * s:.1f}" fill="#E8E2D6" {g(s, 0.7)}/>')
    return ''.join(out)


def speaker(x, y, s, h=1.0):
    hh = 90 * h
    return (contact_shadow(x, y + 2 * s, 30 * s, 6 * s, 0.3) +
            f'<rect x="{x - 26 * s:.1f}" y="{y - hh * s:.1f}" width="{52 * s:.1f}" height="{hh * s:.1f}" rx="{5 * s:.1f}" fill="#33333D" {g(s)}/>'
            f'<circle cx="{x:.1f}" cy="{y - hh * 0.32 * s:.1f}" r="{16 * s:.1f}" fill="#555566" {g(s, 0.6)}/><circle cx="{x:.1f}" cy="{y - hh * 0.32 * s:.1f}" r="{6 * s:.1f}" fill="#222"/>'
            f'<circle cx="{x:.1f}" cy="{y - hh * 0.75 * s:.1f}" r="{9 * s:.1f}" fill="#555566" {g(s, 0.6)}/>')


def festival_tent(x, y, s, col='#E5533D'):
    out = [contact_shadow(x, y + 3 * s, 70 * s, 10 * s, 0.25),
           f'<rect x="{x - 60 * s:.1f}" y="{y - 50 * s:.1f}" width="{120 * s:.1f}" height="{50 * s:.1f}" fill="#FFFFFF" {g(s)}/>']
    for q in range(4):
        c = col if q % 2 == 0 else '#FFFFFF'
        x0 = x - 70 * s + q * 35 * s
        out.append(f'<path d="M{x:.1f} {y - 120 * s:.1f} L{x0:.1f} {y - 46 * s:.1f} L{x0 + 35 * s:.1f} {y - 46 * s:.1f} Z" fill="{c}"/>')
    out.append(f'<path d="M{x:.1f} {y - 120 * s:.1f} L{x - 70 * s:.1f} {y - 46 * s:.1f} L{x + 70 * s:.1f} {y - 46 * s:.1f} Z" fill="none" {g(s)}/>')
    out.append(f'<line x1="{x:.1f}" y1="{y - 120 * s:.1f}" x2="{x:.1f}" y2="{y - 140 * s:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}"/><path d="M{x:.1f} {y - 140 * s:.1f} l{18 * s:.1f} {6 * s:.1f} l{-18 * s:.1f} {6 * s:.1f} Z" fill="#FFD23F"/>')
    out.append(f'<path d="M{x - 18 * s:.1f} {y:.1f} L{x:.1f} {y - 40 * s:.1f} L{x + 18 * s:.1f} {y:.1f} Z" fill="#5A3A22"/>')
    return ''.join(out)


def light_tower(x, y, s, col='#FF5E7E'):
    return (f'<rect x="{x - 6 * s:.1f}" y="{y - 200 * s:.1f}" width="{12 * s:.1f}" height="{200 * s:.1f}" fill="#9AA5B1" {g(s, 0.7)}/>'
            f'<rect x="{x - 30 * s:.1f}" y="{y - 222 * s:.1f}" width="{60 * s:.1f}" height="{24 * s:.1f}" fill="#3C4A5C" {g(s)}/>'
            + ''.join(glow(x + q * 18 * s, y - 210 * s, 14 * s, c, 0.5) + f'<circle cx="{x + q * 18 * s:.1f}" cy="{y - 210 * s:.1f}" r="{6 * s:.1f}" fill="{c}"/>' for q, c in [(-1, col), (0, '#FFD23F'), (1, '#6FD3FF')]))


def food_truck(x, y, s, col='#FFB82E', awning='#E5533D'):
    out = [contact_shadow(x, y + 3 * s, 80 * s, 10 * s, 0.3),
           f'<rect x="{x - 80 * s:.1f}" y="{y - 96 * s:.1f}" width="{124 * s:.1f}" height="{86 * s:.1f}" rx="{10 * s:.1f}" fill="{col}" {g(s)}/>',
           f'<path d="M{x + 44 * s:.1f} {y - 10 * s:.1f} L{x + 44 * s:.1f} {y - 70 * s:.1f} L{x + 70 * s:.1f} {y - 70 * s:.1f} L{x + 82 * s:.1f} {y - 44 * s:.1f} L{x + 82 * s:.1f} {y - 10 * s:.1f} Z" fill="{shade(col, -0.1)}" {g(s)}/>',
           f'<path d="M{x + 50 * s:.1f} {y - 46 * s:.1f} L{x + 50 * s:.1f} {y - 64 * s:.1f} L{x + 68 * s:.1f} {y - 64 * s:.1f} L{x + 76 * s:.1f} {y - 46 * s:.1f} Z" fill="{PALETTE["window"]}"/>',
           f'<rect x="{x - 66 * s:.1f}" y="{y - 78 * s:.1f}" width="{96 * s:.1f}" height="{36 * s:.1f}" fill="#3B2A22" {g(s, 0.7)}/>',
           f'<rect x="{x - 70 * s:.1f}" y="{y - 44 * s:.1f}" width="{104 * s:.1f}" height="{8 * s:.1f}" fill="#E8E2D6" {g(s, 0.6)}/>']
    for q in range(6):
        c = awning if q % 2 == 0 else '#FFFFFF'
        out.append(f'<path d="M{x - 72 * s + q * 18 * s:.1f} {y - 92 * s:.1f} l{18 * s:.1f} 0 l{4 * s:.1f} {16 * s:.1f} a{9 * s:.1f} {5 * s:.1f} 0 0 1 {-18 * s:.1f} 0 Z" fill="{c}" {g(s, 0.4)}/>')
    out.append(f'<circle cx="{x - 50 * s:.1f}" cy="{y - 8 * s:.1f}" r="{12 * s:.1f}" fill="#33333D" {g(s, 0.6)}/><circle cx="{x + 56 * s:.1f}" cy="{y - 8 * s:.1f}" r="{12 * s:.1f}" fill="#33333D" {g(s, 0.6)}/>')
    out.append(f'<circle cx="{x - 18 * s:.1f}" cy="{y - 116 * s:.1f}" r="{20 * s:.1f}" fill="#FFFFFF" {g(s)}/><circle cx="{x - 18 * s:.1f}" cy="{y - 116 * s:.1f}" r="{9 * s:.1f}" fill="{awning}"/>')
    return ''.join(out)


def picnic_table(x, y, s, cloth='#E5533D'):
    return (contact_shadow(x, y + 2 * s, 44 * s, 7 * s, 0.22) +
            f'<rect x="{x - 50 * s:.1f}" y="{y - 14 * s:.1f}" width="{100 * s:.1f}" height="{8 * s:.1f}" fill="#B8733F" {g(s, 0.7)}/>'
            f'<path d="M{x - 40 * s:.1f} {y - 30 * s:.1f} L{x + 40 * s:.1f} {y - 30 * s:.1f} L{x + 34 * s:.1f} {y:.1f} M{x - 40 * s:.1f} {y - 30 * s:.1f} L{x - 34 * s:.1f} {y:.1f}" stroke="#8A5326" stroke-width="{5 * s:.1f}" fill="none"/>'
            f'<rect x="{x - 44 * s:.1f}" y="{y - 38 * s:.1f}" width="{88 * s:.1f}" height="{10 * s:.1f}" fill="{cloth}" {g(s, 0.7)}/>'
            + ''.join(f'<rect x="{x - 44 * s + q * 22 * s:.1f}" y="{y - 38 * s:.1f}" width="{11 * s:.1f}" height="{10 * s:.1f}" fill="#FFFFFF"/>' for q in range(4)) +
            f'<circle cx="{x - 14 * s:.1f}" cy="{y - 44 * s:.1f}" r="{7 * s:.1f}" fill="#FFD23F" {g(s, 0.5)}/><circle cx="{x + 12 * s:.1f}" cy="{y - 44 * s:.1f}" r="{7 * s:.1f}" fill="#FF8A3D" {g(s, 0.5)}/>')


# ------------------------------------------------------------------ tech / space
def glass_tower(x, by, s, w=120, h=320, col='#5FA9E0', side='r', lit=0.4, seed=0):
    r = rng(seed)
    w, h = w * s, h * s
    b, dx, dy = box(x, by, w, h, s, col, side, dep=w * 0.6, top=shade(col, 0.2))
    out = [b]
    rows, cols = int(h / (18 * s)), max(2, int(w / (18 * s)))
    for i in range(rows):
        for j in range(cols):
            wx, wy = x + 6 * s + j * (w - 12 * s) / cols, by - h + 8 * s + i * (h - 12 * s) / rows
            c = '#FFE27A' if r.random() < lit else shade(col, 0.25)
            out.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{(w - 12 * s) / cols - 4 * s:.1f}" height="{(h - 12 * s) / rows - 5 * s:.1f}" fill="{c}"/>')
    out.append(f'<line x1="{x + w * 0.5 + dx * 0.5:.1f}" y1="{by - h + dy * 0.5:.1f}" x2="{x + w * 0.5 + dx * 0.5:.1f}" y2="{by - h + dy * 0.5 - 40 * s:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}"/>'
               + glow(x + w * 0.5 + dx * 0.5, by - h + dy * 0.5 - 42 * s, 10 * s, '#FF5E5E', 0.6))
    return ''.join(out)


def dish(x, y, s):
    return (contact_shadow(x, y + 2 * s, 40 * s, 8 * s, 0.25) +
            f'<path d="M{x - 10 * s:.1f} {y:.1f} L{x:.1f} {y - 60 * s:.1f} L{x + 10 * s:.1f} {y:.1f} Z" fill="#9AA5B1" {g(s)}/>'
            f'<path d="M{x - 56 * s:.1f} {y - 90 * s:.1f} Q{x - 20 * s:.1f} {y - 30 * s:.1f} {x + 50 * s:.1f} {y - 50 * s:.1f} Q{x + 10 * s:.1f} {y - 110 * s:.1f} {x - 56 * s:.1f} {y - 90 * s:.1f} Z" fill="#E8E2D6" {g(s)}/>'
            f'<line x1="{x - 4 * s:.1f}" y1="{y - 70 * s:.1f}" x2="{x + 18 * s:.1f}" y2="{y - 110 * s:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}"/>'
            + glow(x + 18 * s, y - 112 * s, 9 * s, '#FF5E5E', 0.6))


def solar_panel(x, y, s):
    return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 24 * s:.1f}" stroke="{OL}" stroke-width="{4 * s:.1f}"/>'
            f'<path d="M{x - 44 * s:.1f} {y - 22 * s:.1f} L{x + 30 * s:.1f} {y - 22 * s:.1f} L{x + 44 * s:.1f} {y - 52 * s:.1f} L{x - 30 * s:.1f} {y - 52 * s:.1f} Z" fill="#2E5FA8" {g(s)}/>'
            + ''.join(f'<line x1="{x - 44 * s + q * 18.5 * s:.1f}" y1="{y - 22 * s:.1f}" x2="{x - 30 * s + q * 18.5 * s:.1f}" y2="{y - 52 * s:.1f}" stroke="#7FB0E6" stroke-width="{1.5 * s:.1f}"/>' for q in range(1, 4)) +
            f'<line x1="{x - 37 * s:.1f}" y1="{y - 37 * s:.1f}" x2="{x + 37 * s:.1f}" y2="{y - 37 * s:.1f}" stroke="#7FB0E6" stroke-width="{1.5 * s:.1f}"/>')


def robot(x, y, s, col='#9AD0F0'):
    return (contact_shadow(x, y + 2 * s, 22 * s, 5 * s, 0.25) +
            f'<rect x="{x - 18 * s:.1f}" y="{y - 46 * s:.1f}" width="{36 * s:.1f}" height="{34 * s:.1f}" rx="{6 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<rect x="{x - 14 * s:.1f}" y="{y - 74 * s:.1f}" width="{28 * s:.1f}" height="{24 * s:.1f}" rx="{6 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<circle cx="{x - 6 * s:.1f}" cy="{y - 62 * s:.1f}" r="{3.5 * s:.1f}" fill="#33333D"/><circle cx="{x + 6 * s:.1f}" cy="{y - 62 * s:.1f}" r="{3.5 * s:.1f}" fill="#33333D"/>'
            f'<line x1="{x:.1f}" y1="{y - 74 * s:.1f}" x2="{x:.1f}" y2="{y - 86 * s:.1f}" stroke="{OL}" stroke-width="{2.5 * s:.1f}"/>' + glow(x, y - 88 * s, 6 * s, '#FF5E5E', 0.8) +
            f'<rect x="{x - 14 * s:.1f}" y="{y - 12 * s:.1f}" width="{10 * s:.1f}" height="{12 * s:.1f}" fill="#5C6B80" {g(s, 0.6)}/><rect x="{x + 4 * s:.1f}" y="{y - 12 * s:.1f}" width="{10 * s:.1f}" height="{12 * s:.1f}" fill="#5C6B80" {g(s, 0.6)}/>')


def dome(x, y, s, r=90, col='#BFE8F5', base='#E8E2D6'):
    r = r * s
    out = [contact_shadow(x, y + 4 * s, r * 1.1, 14 * s, 0.3),
           f'<rect x="{x - r:.1f}" y="{y - 26 * s:.1f}" width="{2 * r:.1f}" height="{26 * s:.1f}" fill="{base}" {g(s)}/>',
           f'<path d="M{x - r:.1f} {y - 24 * s:.1f} A{r:.1f} {r * 0.85:.1f} 0 0 1 {x + r:.1f} {y - 24 * s:.1f} Z" fill="{col}" opacity="0.85" {g(s)}/>']
    for q in (-0.5, 0, 0.5):
        out.append(f'<path d="M{x + q * r:.1f} {y - 24 * s:.1f} Q{x + q * r * 0.6:.1f} {y - 24 * s - r * 0.7:.1f} {x:.1f} {y - 24 * s - r * 0.85:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{2.5 * s:.1f}" opacity="0.7"/>')
    out.append(f'<path d="M{x - r * 0.6:.1f} {y - 24 * s - r * 0.45:.1f} Q{x - r * 0.3:.1f} {y - 24 * s - r * 0.78:.1f} {x + r * 0.1:.1f} {y - 24 * s - r * 0.8:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{6 * s:.1f}" stroke-linecap="round" opacity="0.8"/>')
    out.append(fluffy_tree(x - r * 0.3, y - 26 * s, s * 0.45, '#6CC24A', seed=int(x)) + fluffy_tree(x + r * 0.35, y - 26 * s, s * 0.4, '#8CE06A', seed=int(y)))
    out.append(f'<rect x="{x - 16 * s:.1f}" y="{y - 40 * s:.1f}" width="{32 * s:.1f}" height="{40 * s:.1f}" rx="{8 * s:.1f}" fill="#5C6B80" {g(s)}/>')
    return ''.join(out)


def rocket(x, y, s):
    out = [contact_shadow(x, y + 4 * s, 70 * s, 10 * s, 0.3),
           f'<path d="M{x - 60 * s:.1f} {y:.1f} L{x - 50 * s:.1f} {y - 260 * s:.1f} M{x + 60 * s:.1f} {y:.1f} L{x + 50 * s:.1f} {y - 260 * s:.1f}" stroke="#E5533D" stroke-width="{8 * s:.1f}"/>',
           f'<path d="M{x - 30 * s:.1f} {y - 30 * s:.1f} L{x - 30 * s:.1f} {y - 230 * s:.1f} Q{x:.1f} {y - 330 * s:.1f} {x + 30 * s:.1f} {y - 230 * s:.1f} L{x + 30 * s:.1f} {y - 30 * s:.1f} Z" fill="#FFFFFF" {g(s)}/>',
           f'<path d="M{x - 30 * s:.1f} {y - 230 * s:.1f} Q{x:.1f} {y - 330 * s:.1f} {x + 30 * s:.1f} {y - 230 * s:.1f} Z" fill="#E5533D" {g(s)}/>',
           f'<circle cx="{x:.1f}" cy="{y - 170 * s:.1f}" r="{16 * s:.1f}" fill="#6FD3FF" {g(s)}/>',
           f'<path d="M{x - 30 * s:.1f} {y - 90 * s:.1f} L{x - 56 * s:.1f} {y - 30 * s:.1f} L{x - 30 * s:.1f} {y - 40 * s:.1f} Z" fill="#E5533D" {g(s)}/>',
           f'<path d="M{x + 30 * s:.1f} {y - 90 * s:.1f} L{x + 56 * s:.1f} {y - 30 * s:.1f} L{x + 30 * s:.1f} {y - 40 * s:.1f} Z" fill="#E5533D" {g(s)}/>',
           f'<rect x="{x - 70 * s:.1f}" y="{y - 30 * s:.1f}" width="{140 * s:.1f}" height="{30 * s:.1f}" fill="#9AA5B1" {g(s)}/>']
    return ''.join(out)


def crater(x, y, s, col='#8A6FC8'):
    return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{60 * s:.1f}" ry="{22 * s:.1f}" fill="{shade(col, 0.15)}" {g(s)}/>'
            f'<ellipse cx="{x + 4 * s:.1f}" cy="{y + 3 * s:.1f}" rx="{44 * s:.1f}" ry="{14 * s:.1f}" fill="{shade(col, -0.25)}"/>')


def crystal(x, y, s, col='#6FD3FF'):
    out = [glow(x, y - 40 * s, 50 * s, col, 0.18)]
    for dx_, h, wd in [(-18, 60, 14), (14, 76, 16), (0, 100, 18), (28, 46, 12)]:
        bx = x + dx_ * s
        out.append(f'<path d="M{bx - wd * s:.1f} {y:.1f} L{bx - wd * s:.1f} {y - h * 0.7 * s:.1f} L{bx:.1f} {y - h * s:.1f} L{bx + wd * s:.1f} {y - h * 0.7 * s:.1f} L{bx + wd * s:.1f} {y:.1f} Z" fill="{col}" {g(s)}/>'
                   f'<path d="M{bx:.1f} {y - h * s:.1f} L{bx + wd * s:.1f} {y - h * 0.7 * s:.1f} L{bx + wd * s:.1f} {y:.1f} L{bx:.1f} {y:.1f} Z" fill="{shade(col, -0.2)}"/>')
    return ''.join(out)


def alien_plant(x, y, s, col='#FF7FD0'):
    return (f'<path d="M{x:.1f} {y:.1f} Q{x - 10 * s:.1f} {y - 50 * s:.1f} {x + 6 * s:.1f} {y - 90 * s:.1f}" fill="none" stroke="#5EC48A" stroke-width="{7 * s:.1f}" stroke-linecap="round"/>'
            + glow(x + 6 * s, y - 96 * s, 28 * s, col, 0.25) +
            f'<circle cx="{x + 6 * s:.1f}" cy="{y - 96 * s:.1f}" r="{16 * s:.1f}" fill="{col}" {g(s)}/><circle cx="{x + 1 * s:.1f}" cy="{y - 101 * s:.1f}" r="{5 * s:.1f}" fill="#FFFFFF" opacity="0.7"/>'
            f'<path d="M{x - 2 * s:.1f} {y - 40 * s:.1f} Q{x - 30 * s:.1f} {y - 50 * s:.1f} {x - 30 * s:.1f} {y - 30 * s:.1f} Q{x - 16 * s:.1f} {y - 30 * s:.1f} {x - 2 * s:.1f} {y - 40 * s:.1f} Z" fill="#5EC48A" {g(s, 0.6)}/>')


def planet(x, y, r, col, ring=None):
    out = [f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="{OL}" stroke-width="4"/>',
           f'<path d="M{x - r * 0.8} {y - r * 0.2} Q{x} {y - r * 0.05} {x + r * 0.85} {y - r * 0.3}" stroke="{shade(col, -0.15)}" stroke-width="{r * 0.18}" fill="none"/>',
           f'<circle cx="{x - r * 0.35}" cy="{y - r * 0.4}" r="{r * 0.2}" fill="#FFFFFF" opacity="0.35"/>']
    if ring:
        out.append(f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.7}" ry="{r * 0.4}" fill="none" stroke="{ring}" stroke-width="7" transform="rotate(-15 {x} {y})"/>')
    return ''.join(out)


# ------------------------------------------------------------------ underwater
def coral(x, y, s, col='#FF7F8A'):
    out = []
    for a in (-0.5, -0.15, 0.2, 0.55):
        ex, ey = x + math.sin(a) * 60 * s, y - math.cos(a) * 70 * s
        out.append(f'<path d="M{x:.1f} {y:.1f} Q{x + math.sin(a) * 20 * s:.1f} {y - 30 * s:.1f} {ex:.1f} {ey:.1f}" fill="none" stroke="{OL}" stroke-width="{16 * s + 3:.1f}" stroke-linecap="round"/>'
                   f'<path d="M{x:.1f} {y:.1f} Q{x + math.sin(a) * 20 * s:.1f} {y - 30 * s:.1f} {ex:.1f} {ey:.1f}" fill="none" stroke="{col}" stroke-width="{16 * s:.1f}" stroke-linecap="round"/>')
    out.append(''.join(f'<circle cx="{x + bx * s:.1f}" cy="{y + by * s:.1f}" r="{4 * s:.1f}" fill="{shade(col, 0.4)}"/>' for bx, by in [(-20, -40), (10, -56), (30, -36)]))
    return ''.join(out)


def fan_coral(x, y, s, col='#B07FE0'):
    return (f'<path d="M{x:.1f} {y:.1f} L{x - 50 * s:.1f} {y - 70 * s:.1f} Q{x:.1f} {y - 110 * s:.1f} {x + 50 * s:.1f} {y - 70 * s:.1f} Z" fill="{col}" {g(s)}/>'
            + ''.join(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + q * 12 * s:.1f}" y2="{y - 90 * s + abs(q) * 5 * s:.1f}" stroke="{shade(col, -0.25)}" stroke-width="{2 * s:.1f}"/>' for q in range(-3, 4)))


def kelp(x, y, s, col='#3FAE6A', h=200):
    d = f'M{x:.1f} {y:.1f} '
    for q in range(1, 6):
        d += f'Q{x + (16 if q % 2 else -16) * s:.1f} {y - (q - 0.5) * h / 5 * s:.1f} {x:.1f} {y - q * h / 5 * s:.1f} '
    out = [f'<path d="{d}" fill="none" stroke="{OL}" stroke-width="{12 * s + 3:.1f}" stroke-linecap="round"/>', f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{12 * s:.1f}" stroke-linecap="round"/>']
    for q in range(1, 5):
        yy = y - q * h / 5 * s
        out.append(f'<ellipse cx="{x + (14 if q % 2 else -14) * s:.1f}" cy="{yy:.1f}" rx="{12 * s:.1f}" ry="{6 * s:.1f}" fill="{shade(col, 0.2)}" {g(s, 0.5)}/>')
    return ''.join(out)


def fish(x, y, s, col='#FFB82E', flip=False):
    f = -1 if flip else 1
    return (f'<path d="M{x - f * 26 * s:.1f} {y:.1f} Q{x:.1f} {y - 20 * s:.1f} {x + f * 24 * s:.1f} {y:.1f} Q{x:.1f} {y + 20 * s:.1f} {x - f * 26 * s:.1f} {y:.1f} Z" fill="{col}" {g(s)}/>'
            f'<path d="M{x - f * 24 * s:.1f} {y:.1f} L{x - f * 40 * s:.1f} {y - 12 * s:.1f} L{x - f * 40 * s:.1f} {y + 12 * s:.1f} Z" fill="{col}" {g(s)}/>'
            f'<line x1="{x - f * 4 * s:.1f}" y1="{y - 12 * s:.1f}" x2="{x - f * 4 * s:.1f}" y2="{y + 12 * s:.1f}" stroke="#FFFFFF" stroke-width="{4 * s:.1f}" opacity="0.8"/>'
            f'<circle cx="{x + f * 12 * s:.1f}" cy="{y - 3 * s:.1f}" r="{3 * s:.1f}" fill="{OL}"/>')


def shipwreck(x, y, s):
    return (contact_shadow(x, y + 4 * s, 130 * s, 16 * s, 0.3) +
            f'<path d="M{x - 130 * s:.1f} {y - 70 * s:.1f} L{x + 120 * s:.1f} {y - 40 * s:.1f} L{x + 90 * s:.1f} {y:.1f} L{x - 100 * s:.1f} {y:.1f} Z" fill="#8A5A3A" {g(s)}/>'
            + ''.join(f'<line x1="{x - 120 * s:.1f}" y1="{y - 60 * s + q * 16 * s:.1f}" x2="{x + 110 * s:.1f}" y2="{y - 32 * s + q * 9 * s:.1f}" stroke="#6E452C" stroke-width="{3 * s:.1f}"/>' for q in range(3)) +
            f'<line x1="{x:.1f}" y1="{y - 56 * s:.1f}" x2="{x + 30 * s:.1f}" y2="{y - 220 * s:.1f}" stroke="#6E452C" stroke-width="{9 * s:.1f}" stroke-linecap="round"/>'
            f'<path d="M{x + 20 * s:.1f} {y - 190 * s:.1f} L{x + 80 * s:.1f} {y - 150 * s:.1f} L{x + 14 * s:.1f} {y - 130 * s:.1f} Z" fill="#E8DCC4" opacity="0.8" {g(s, 0.7)}/>'
            + ''.join(f'<circle cx="{x + cx * s:.1f}" cy="{y + cy * s:.1f}" r="{9 * s:.1f}" fill="#33333D"/>' for cx, cy in [(-60, -40), (-20, -36), (20, -30)]))


def chest(x, y, s):
    return (contact_shadow(x, y + 2 * s, 34 * s, 6 * s, 0.3) + glow(x, y - 30 * s, 40 * s, '#FFE27A', 0.3) +
            f'<rect x="{x - 30 * s:.1f}" y="{y - 32 * s:.1f}" width="{60 * s:.1f}" height="{32 * s:.1f}" fill="#A8642E" {g(s)}/>'
            f'<path d="M{x - 30 * s:.1f} {y - 32 * s:.1f} L{x - 26 * s:.1f} {y - 56 * s:.1f} L{x + 34 * s:.1f} {y - 62 * s:.1f} L{x + 30 * s:.1f} {y - 32 * s:.1f} Z" fill="#C27A3A" {g(s)}/>'
            + ''.join(f'<circle cx="{x + q * 10 * s:.1f}" cy="{y - 36 * s:.1f}" r="{6 * s:.1f}" fill="#FFD23F" {g(s, 0.5)}/>' for q in (-2, -1, 0, 1, 2)) +
            f'<rect x="{x - 5 * s:.1f}" y="{y - 26 * s:.1f}" width="{10 * s:.1f}" height="{10 * s:.1f}" fill="#FFD23F" {g(s, 0.5)}/>')


def bubbles(x, y, s, n=5, r=None):
    r = r or rng(int(x + y))
    return ''.join(f'<circle cx="{x + r.uniform(-20, 20) * s:.1f}" cy="{y - q * 30 * s:.1f}" r="{(4 + q * 1.5) * s:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{2.5 * s:.1f}" opacity="0.7"/>' for q in range(n))


# ------------------------------------------------------------------ shopping / wellness
def shopping_bags(x, y, s):
    out = []
    for dx_, c, h in [(-16, '#FF5E7E', 40), (12, '#4FA3E3', 34), (34, '#FFD23F', 28)]:
        bx = x + dx_ * s
        out.append(f'<rect x="{bx - 12 * s:.1f}" y="{y - h * s:.1f}" width="{24 * s:.1f}" height="{h * s:.1f}" fill="{c}" {g(s)}/>'
                   f'<path d="M{bx - 6 * s:.1f} {y - h * s:.1f} q{6 * s:.1f} {-14 * s:.1f} {12 * s:.1f} 0" fill="none" {g(s, 0.6)}/>')
    return ''.join(out)


def clothes_rack(x, y, s):
    cols = ['#FF5E7E', '#4FA3E3', '#FFD23F', '#6CC24A', '#B07FE0']
    out = [f'<path d="M{x - 50 * s:.1f} {y:.1f} L{x - 50 * s:.1f} {y - 90 * s:.1f} L{x + 50 * s:.1f} {y - 90 * s:.1f} L{x + 50 * s:.1f} {y:.1f}" fill="none" stroke="#9AA5B1" stroke-width="{5 * s:.1f}"/>']
    for q in range(5):
        cx = x - 40 * s + q * 20 * s
        out.append(f'<path d="M{cx - 9 * s:.1f} {y - 80 * s:.1f} L{cx + 9 * s:.1f} {y - 80 * s:.1f} L{cx + 11 * s:.1f} {y - 30 * s:.1f} L{cx - 11 * s:.1f} {y - 30 * s:.1f} Z" fill="{cols[q]}" {g(s, 0.6)}/>')
    return ''.join(out)


def gym_bar(x, y, s):
    return (f'<path d="M{x - 40 * s:.1f} {y:.1f} L{x - 40 * s:.1f} {y - 80 * s:.1f} L{x + 40 * s:.1f} {y - 80 * s:.1f} L{x + 40 * s:.1f} {y:.1f}" fill="none" stroke="{OL}" stroke-width="{9 * s:.1f}" stroke-linejoin="round"/>'
            f'<path d="M{x - 40 * s:.1f} {y:.1f} L{x - 40 * s:.1f} {y - 80 * s:.1f} L{x + 40 * s:.1f} {y - 80 * s:.1f} L{x + 40 * s:.1f} {y:.1f}" fill="none" stroke="#4FA3E3" stroke-width="{5 * s:.1f}" stroke-linejoin="round"/>')


def yoga_mat(x, y, s, col='#B07FE0'):
    return (f'<path d="M{x - 40 * s:.1f} {y:.1f} L{x + 30 * s:.1f} {y:.1f} L{x + 44 * s:.1f} {y - 14 * s:.1f} L{x - 26 * s:.1f} {y - 14 * s:.1f} Z" fill="{col}" {g(s)}/>'
            f'<ellipse cx="{x + 40 * s:.1f}" cy="{y - 10 * s:.1f}" rx="{6 * s:.1f}" ry="{8 * s:.1f}" fill="{shade(col, -0.2)}" {g(s, 0.6)}/>')


def dumbbell(x, y, s, col='#E5533D'):
    return (f'<rect x="{x - 20 * s:.1f}" y="{y - 10 * s:.1f}" width="{40 * s:.1f}" height="{6 * s:.1f}" fill="#9AA5B1" {g(s, 0.6)}/>'
            f'<rect x="{x - 30 * s:.1f}" y="{y - 20 * s:.1f}" width="{12 * s:.1f}" height="{24 * s:.1f}" rx="{3 * s:.1f}" fill="{col}" {g(s, 0.8)}/><rect x="{x + 18 * s:.1f}" y="{y - 20 * s:.1f}" width="{12 * s:.1f}" height="{24 * s:.1f}" rx="{3 * s:.1f}" fill="{col}" {g(s, 0.8)}/>')


def heart_hedge(x, y, s, col='#5CBF3F'):
    return (contact_shadow(x, y + 2 * s, 40 * s, 7 * s, 0.22) +
            f'<path d="M{x:.1f} {y - 4 * s:.1f} C{x - 70 * s:.1f} {y - 50 * s:.1f} {x - 40 * s:.1f} {y - 110 * s:.1f} {x:.1f} {y - 76 * s:.1f} C{x + 40 * s:.1f} {y - 110 * s:.1f} {x + 70 * s:.1f} {y - 50 * s:.1f} {x:.1f} {y - 4 * s:.1f} Z" fill="{col}" {g(s)}/>'
            f'<path d="M{x + 14 * s:.1f} {y - 84 * s:.1f} Q{x + 40 * s:.1f} {y - 96 * s:.1f} {x + 44 * s:.1f} {y - 62 * s:.1f}" stroke="{shade(col, 0.35)}" stroke-width="{6 * s:.1f}" fill="none" stroke-linecap="round"/>'
            + ''.join(f'<circle cx="{x + bx * s:.1f}" cy="{y + by * s:.1f}" r="{4 * s:.1f}" fill="#FF5E7E"/>' for bx, by in [(-20, -60), (10, -40), (24, -70)]))
