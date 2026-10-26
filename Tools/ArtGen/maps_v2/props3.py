"""Shared 3/4-view props for the v3 maps. Every function takes (x, y=ground contact, s=depth scale) and returns SVG.
Light from the upper right, warm-brown outlines (style.OL)."""
import math
from style import OL, PALETTE, mix, shade, contact_shadow, rng
from city2 import sw, poly, pts, townhouse, fluffy_tree, poplar, lamp, boat, fountain, parasol, flowerbed, car


def g(s, k=1.0):
    return f'stroke="{OL}" stroke-width="{sw(s) * k:.1f}" stroke-linejoin="round" stroke-linecap="round"'


def box(x, by, w, h, s, front, side='r', dep=None, top=None, side_col=None):
    """plain 3/4 box; returns (svg, dx, dy)"""
    dep = dep if dep is not None else w * 0.5
    dx, dy = dep * 0.62 * (1 if side == 'r' else -1), -dep * 0.5
    sc = side_col or shade(front, -0.2)
    tc = top or shade(front, 0.18)
    ex = x + w if side == 'r' else x
    out = [contact_shadow(x + w / 2 + dx / 2, by + 4 * s, w * 0.7, 12 * s, 0.22),
           poly([(ex, by), (ex + dx, by + dy), (ex + dx, by - h + dy), (ex, by - h)], sc, w=sw(s)),
           f'<rect x="{x:.1f}" y="{by - h:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{front}" {g(s)}/>',
           poly([(x, by - h), (x + w, by - h), (x + w + dx, by - h + dy), (x + dx, by - h + dy)], tc, w=sw(s))]
    return ''.join(out), dx, dy


# ------------------------------------------------------------------ nature
def pine(x, y, s, c='#3E9A4F', snow=False):
    dark, light = shade(c, -0.25), shade(c, 0.25)
    out = [contact_shadow(x - 6 * s, y + 2 * s, 30 * s, 8 * s, 0.25),
           f'<rect x="{x - 5 * s:.1f}" y="{y - 22 * s:.1f}" width="{10 * s:.1f}" height="{22 * s:.1f}" fill="#8A5326" {g(s)}/>']
    for i, (wd, ty, by_) in enumerate([(48, -70, -18), (38, -105, -55), (26, -138, -92)]):
        out.append(f'<path d="M{x - wd * s:.1f} {y + by_ * s:.1f} L{x:.1f} {y + ty * s - 20 * s:.1f} L{x + wd * s:.1f} {y + by_ * s:.1f} Z" fill="{dark}" {g(s)}/>')
        out.append(f'<path d="M{x:.1f} {y + ty * s - 16 * s:.1f} L{x + wd * 0.85 * s:.1f} {y + (by_ - 4) * s:.1f} L{x + 4 * s:.1f} {y + (by_ - 4) * s:.1f} Z" fill="{c}"/>')
        if snow:
            out.append(f'<path d="M{x - wd * 0.45 * s:.1f} {y + (ty * 0.55 + by_ * 0.45) * s:.1f} L{x:.1f} {y + ty * s - 18 * s:.1f} L{x + wd * 0.45 * s:.1f} {y + (ty * 0.55 + by_ * 0.45) * s:.1f} '
                       f'Q{x:.1f} {y + (ty * 0.5 + by_ * 0.5) * s:.1f} {x - wd * 0.45 * s:.1f} {y + (ty * 0.55 + by_ * 0.45) * s:.1f} Z" fill="#FFFFFF"/>')
    return ''.join(out)


def rock(x, y, s, c='#A9A39A'):
    return (contact_shadow(x, y + 2 * s, 34 * s, 7 * s, 0.22) +
            f'<path d="M{x - 34 * s:.1f} {y:.1f} Q{x - 30 * s:.1f} {y - 30 * s:.1f} {x - 6 * s:.1f} {y - 34 * s:.1f} Q{x + 26 * s:.1f} {y - 36 * s:.1f} {x + 34 * s:.1f} {y:.1f} Z" fill="{c}" {g(s)}/>'
            f'<path d="M{x - 4 * s:.1f} {y - 30 * s:.1f} Q{x + 20 * s:.1f} {y - 30 * s:.1f} {x + 26 * s:.1f} {y - 10 * s:.1f}" fill="none" stroke="{shade(c, 0.35)}" stroke-width="{sw(s) * 1.4:.1f}" stroke-linecap="round"/>')


def bush(x, y, s, c='#58B74A', berries=None):
    dark, light = shade(c, -0.25), shade(c, 0.3)
    out = [contact_shadow(x, y + 2 * s, 40 * s, 8 * s, 0.2),
           f'<g fill="{dark}" {g(s)}><circle cx="{x - 18 * s:.1f}" cy="{y - 16 * s:.1f}" r="{20 * s:.1f}"/><circle cx="{x + 16 * s:.1f}" cy="{y - 18 * s:.1f}" r="{22 * s:.1f}"/><circle cx="{x:.1f}" cy="{y - 30 * s:.1f}" r="{22 * s:.1f}"/></g>',
           f'<circle cx="{x + 6 * s:.1f}" cy="{y - 32 * s:.1f}" r="{14 * s:.1f}" fill="{c}"/><circle cx="{x + 20 * s:.1f}" cy="{y - 22 * s:.1f}" r="{12 * s:.1f}" fill="{c}"/>',
           f'<circle cx="{x + 10 * s:.1f}" cy="{y - 38 * s:.1f}" r="{6 * s:.1f}" fill="{light}"/>']
    if berries:
        for bx, by in [(-14, -22), (4, -14), (16, -30), (-4, -36)]:
            out.append(f'<circle cx="{x + bx * s:.1f}" cy="{y + by * s:.1f}" r="{4 * s:.1f}" fill="{berries}" {g(s, 0.4)}/>')
    return ''.join(out)


def flowers(x, y, s, r=None, n=6):
    r = r or rng(int(x + y))
    out = []
    for _ in range(n):
        fx, fy = x + r.uniform(-30, 30) * s, y + r.uniform(-8, 8) * s
        c = r.choice(['#FF5E7E', '#FFD23F', '#FF8A3D', '#FFFFFF', '#F05AB4'])
        out.append(f'<line x1="{fx:.1f}" y1="{fy:.1f}" x2="{fx:.1f}" y2="{fy - 14 * s:.1f}" stroke="#3E8E2F" stroke-width="{2.5 * s:.1f}"/>'
                   f'<circle cx="{fx:.1f}" cy="{fy - 16 * s:.1f}" r="{5 * s:.1f}" fill="{c}" {g(s, 0.4)}/><circle cx="{fx:.1f}" cy="{fy - 16 * s:.1f}" r="{1.8 * s:.1f}" fill="#FFD23F"/>')
    return ''.join(out)


def pond(x, y, rx, ry, s, ducks=True, lily=True):
    out = [f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx + 12 * s:.1f}" ry="{ry + 6 * s:.1f}" fill="#C9B184" {g(s)}/>',
           f'<ellipse cx="{x:.1f}" cy="{y + 3 * s:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#4FB6EC"/>',
           f'<ellipse cx="{x - rx * 0.3:.1f}" cy="{y - ry * 0.25:.1f}" rx="{rx * 0.45:.1f}" ry="{ry * 0.22:.1f}" fill="#BDEBFF" opacity="0.7"/>']
    if lily:
        for lx, ly in [(0.45, 0.2), (-0.5, 0.35), (0.1, 0.5)]:
            out.append(f'<ellipse cx="{x + rx * lx:.1f}" cy="{y + ry * ly:.1f}" rx="{12 * s:.1f}" ry="{5 * s:.1f}" fill="#4E9F36" {g(s, 0.4)}/>')
    if ducks:
        for dx_ in (-0.15, 0.25):
            dxp, dyp = x + rx * dx_, y + ry * 0.05
            out.append(f'<ellipse cx="{dxp:.1f}" cy="{dyp:.1f}" rx="{13 * s:.1f}" ry="{7 * s:.1f}" fill="#FFFFFF" {g(s, 0.6)}/>'
                       f'<circle cx="{dxp + 9 * s:.1f}" cy="{dyp - 9 * s:.1f}" r="{6 * s:.1f}" fill="#FFFFFF" {g(s, 0.6)}/>'
                       f'<path d="M{dxp + 14 * s:.1f} {dyp - 9 * s:.1f} l{6 * s:.1f} {2 * s:.1f} l{-6 * s:.1f} {2 * s:.1f} Z" fill="#FF9F2E"/>')
    for q in range(5):
        a = -0.9 + q * 0.12
        out.append(f'<path d="M{x + math.cos(a) * rx * 1.02:.1f} {y + math.sin(a) * ry + 4 * s:.1f} l{-2 * s:.1f} {-28 * s:.1f}" stroke="#3E8E2F" stroke-width="{3 * s:.1f}"/>')
    return ''.join(out)


# ------------------------------------------------------------------ farm
def barn(x, by, s, w=170, h=120, col='#D8452F', side='r'):
    w, h = w * s, h * s
    b, dx, dy = box(x, by, w, h, s, col, side, dep=w * 0.7, top=shade(col, -0.1))
    out = [b]
    top = by - h
    rk = poly([(x - 8 * s, top + 4 * s), (x + w * 0.2, top - h * 0.3), (x + w * 0.5, top - h * 0.48), (x + w * 0.8, top - h * 0.3), (x + w + 8 * s, top + 4 * s)], col, w=sw(s))
    roof = poly([(x + w * 0.5, top - h * 0.48), (x + w * 0.8, top - h * 0.3), (x + w + 8 * s, top + 4 * s), (x + w + 8 * s + dx, top + 4 * s + dy), (x + w * 0.8 + dx, top - h * 0.3 + dy), (x + w * 0.5 + dx, top - h * 0.48 + dy)] if side == 'r'
                else [(x + w * 0.5, top - h * 0.48), (x + w * 0.2, top - h * 0.3), (x - 8 * s, top + 4 * s), (x - 8 * s + dx, top + 4 * s + dy), (x + w * 0.2 + dx, top - h * 0.3 + dy), (x + w * 0.5 + dx, top - h * 0.48 + dy)],
                '#7A3B2A', w=sw(s))
    out += [roof, rk]
    # white trim + doors
    out.append(f'<rect x="{x + w * 0.3:.1f}" y="{by - h * 0.62:.1f}" width="{w * 0.4:.1f}" height="{h * 0.62:.1f}" fill="#B8382A" stroke="#FFFFFF" stroke-width="{4 * s:.1f}"/>')
    out.append(f'<path d="M{x + w * 0.3:.1f} {by - h * 0.62:.1f} L{x + w * 0.7:.1f} {by:.1f} M{x + w * 0.7:.1f} {by - h * 0.62:.1f} L{x + w * 0.3:.1f} {by:.1f}" stroke="#FFFFFF" stroke-width="{4 * s:.1f}"/>')
    out.append(f'<circle cx="{x + w * 0.5:.1f}" cy="{top - h * 0.12:.1f}" r="{12 * s:.1f}" fill="#FFF3D6" {g(s, 0.7)}/>')
    return ''.join(out)


def fence(x0, y0, x1, y1, s, col='#F7EAD0'):
    out = []
    n = max(2, int(math.hypot(x1 - x0, y1 - y0) / (28 * s)))
    for i in range(n + 1):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        out.append(f'<rect x="{x - 3 * s:.1f}" y="{y - 30 * s:.1f}" width="{6 * s:.1f}" height="{30 * s:.1f}" fill="{col}" {g(s, 0.6)}/>')
    for hh in (22, 10):
        out.append(f'<line x1="{x0:.1f}" y1="{y0 - hh * s:.1f}" x2="{x1:.1f}" y2="{y1 - hh * s:.1f}" stroke="{OL}" stroke-width="{6 * s:.1f}" stroke-linecap="round"/>'
                   f'<line x1="{x0:.1f}" y1="{y0 - hh * s:.1f}" x2="{x1:.1f}" y2="{y1 - hh * s:.1f}" stroke="{col}" stroke-width="{3.5 * s:.1f}" stroke-linecap="round"/>')
    return ''.join(out)


def cow(x, y, s, flip=False):
    f = -1 if flip else 1
    out = [contact_shadow(x, y + 2 * s, 34 * s, 6 * s, 0.25)]
    for lx in (-18, -8, 12, 22):
        out.append(f'<rect x="{x + f * lx * s - 3 * s:.1f}" y="{y - 16 * s:.1f}" width="{6 * s:.1f}" height="{16 * s:.1f}" fill="#FFFFFF" {g(s, 0.6)}/>')
    out.append(f'<rect x="{x - 28 * s:.1f}" y="{y - 40 * s:.1f}" width="{56 * s:.1f}" height="{28 * s:.1f}" rx="{12 * s:.1f}" fill="#FFFFFF" {g(s, 0.8)}/>')
    out.append(f'<ellipse cx="{x - f * 6 * s:.1f}" cy="{y - 30 * s:.1f}" rx="{10 * s:.1f}" ry="{7 * s:.1f}" fill="#3B2A22"/><ellipse cx="{x + f * 14 * s:.1f}" cy="{y - 24 * s:.1f}" rx="{6 * s:.1f}" ry="{5 * s:.1f}" fill="#3B2A22"/>')
    hx = x + f * 30 * s
    out.append(f'<rect x="{hx - 11 * s:.1f}" y="{y - 52 * s:.1f}" width="{22 * s:.1f}" height="{24 * s:.1f}" rx="{8 * s:.1f}" fill="#FFFFFF" {g(s, 0.8)}/>')
    out.append(f'<rect x="{hx - 10 * s:.1f}" y="{y - 38 * s:.1f}" width="{20 * s:.1f}" height="{10 * s:.1f}" rx="{5 * s:.1f}" fill="#FFB3BE" {g(s, 0.5)}/>')
    out.append(f'<circle cx="{hx - 4 * s:.1f}" cy="{y - 45 * s:.1f}" r="{1.8 * s:.1f}" fill="{OL}"/><circle cx="{hx + 4 * s:.1f}" cy="{y - 45 * s:.1f}" r="{1.8 * s:.1f}" fill="{OL}"/>')
    return ''.join(out)


def sheep(x, y, s):
    out = [contact_shadow(x, y + 2 * s, 26 * s, 5 * s, 0.25)]
    for lx in (-12, 10):
        out.append(f'<rect x="{x + lx * s - 3 * s:.1f}" y="{y - 12 * s:.1f}" width="{6 * s:.1f}" height="{12 * s:.1f}" fill="#3B2A22"/>')
    out.append(f'<g fill="#FFFFFF" {g(s, 0.7)}>' + ''.join(f'<circle cx="{x + bx * s:.1f}" cy="{y + by * s:.1f}" r="{11 * s:.1f}"/>' for bx, by in [(-14, -22), (0, -28), (14, -22), (-6, -16), (8, -16)]) + '</g>')
    out.append(f'<g fill="#FFFFFF">' + ''.join(f'<circle cx="{x + bx * s:.1f}" cy="{y + by * s:.1f}" r="{9 * s:.1f}"/>' for bx, by in [(-14, -22), (0, -28), (14, -22), (-6, -16), (8, -16)]) + '</g>')
    out.append(f'<ellipse cx="{x + 24 * s:.1f}" cy="{y - 24 * s:.1f}" rx="{8 * s:.1f}" ry="{10 * s:.1f}" fill="#3B2A22" {g(s, 0.6)}/>')
    return ''.join(out)


def pig(x, y, s):
    c = '#FFB3BE'
    return (contact_shadow(x, y + 2 * s, 24 * s, 5 * s, 0.25) +
            ''.join(f'<rect x="{x + lx * s - 3 * s:.1f}" y="{y - 10 * s:.1f}" width="{6 * s:.1f}" height="{10 * s:.1f}" fill="{c}" {g(s, 0.5)}/>' for lx in (-12, 10)) +
            f'<ellipse cx="{x:.1f}" cy="{y - 20 * s:.1f}" rx="{24 * s:.1f}" ry="{14 * s:.1f}" fill="{c}" {g(s, 0.8)}/>'
            f'<circle cx="{x + 22 * s:.1f}" cy="{y - 24 * s:.1f}" r="{11 * s:.1f}" fill="{c}" {g(s, 0.8)}/>'
            f'<ellipse cx="{x + 30 * s:.1f}" cy="{y - 22 * s:.1f}" rx="{5 * s:.1f}" ry="{4 * s:.1f}" fill="#FF8FA3" {g(s, 0.5)}/>')


def haystack(x, y, s):
    c = '#F2C14E'
    return (contact_shadow(x, y + 2 * s, 40 * s, 8 * s, 0.25) +
            f'<path d="M{x - 40 * s:.1f} {y:.1f} Q{x - 40 * s:.1f} {y - 60 * s:.1f} {x:.1f} {y - 64 * s:.1f} Q{x + 40 * s:.1f} {y - 60 * s:.1f} {x + 40 * s:.1f} {y:.1f} Z" fill="{c}" {g(s)}/>'
            + ''.join(f'<path d="M{x + q * 12 * s:.1f} {y - 6 * s:.1f} l{3 * s:.1f} {-20 * s:.1f}" stroke="{shade(c, -0.25)}" stroke-width="{3 * s:.1f}"/>' for q in (-2, -1, 0, 1, 2)) +
            f'<path d="M{x + 6 * s:.1f} {y - 56 * s:.1f} Q{x + 30 * s:.1f} {y - 50 * s:.1f} {x + 34 * s:.1f} {y - 20 * s:.1f}" stroke="#FFE59A" stroke-width="{5 * s:.1f}" fill="none" stroke-linecap="round"/>')


def windmill(x, y, s, col='#F7EAD0', blades=0.3):
    out = [contact_shadow(x, y + 4 * s, 60 * s, 12 * s, 0.25),
           f'<path d="M{x - 40 * s:.1f} {y:.1f} L{x - 26 * s:.1f} {y - 170 * s:.1f} L{x + 26 * s:.1f} {y - 170 * s:.1f} L{x + 40 * s:.1f} {y:.1f} Z" fill="{col}" {g(s)}/>',
           f'<path d="M{x + 10 * s:.1f} {y:.1f} L{x + 18 * s:.1f} {y - 170 * s:.1f} L{x + 26 * s:.1f} {y - 170 * s:.1f} L{x + 40 * s:.1f} {y:.1f} Z" fill="{shade(col, -0.15)}"/>',
           f'<path d="M{x - 34 * s:.1f} {y - 170 * s:.1f} Q{x:.1f} {y - 230 * s:.1f} {x + 34 * s:.1f} {y - 170 * s:.1f} Z" fill="#C24B34" {g(s)}/>',
           f'<rect x="{x - 10 * s:.1f}" y="{y - 40 * s:.1f}" width="{20 * s:.1f}" height="{40 * s:.1f}" rx="{10 * s:.1f}" fill="#8A5326" {g(s, 0.7)}/>',
           f'<rect x="{x - 8 * s:.1f}" y="{y - 120 * s:.1f}" width="{16 * s:.1f}" height="{18 * s:.1f}" fill="{PALETTE["window"]}" {g(s, 0.6)}/>']
    hx, hy = x, y - 178 * s
    for q in range(4):
        a = blades + q * math.pi / 2
        ex, ey = hx + math.cos(a) * 110 * s, hy + math.sin(a) * 110 * s
        px, py = -math.sin(a) * 16 * s, math.cos(a) * 16 * s
        out.append(f'<path d="M{hx + math.cos(a) * 18 * s:.1f} {hy + math.sin(a) * 18 * s:.1f} L{ex:.1f} {ey:.1f} L{ex + px:.1f} {ey + py:.1f} L{hx + math.cos(a) * 18 * s + px:.1f} {hy + math.sin(a) * 18 * s + py:.1f} Z" fill="#FFF8EC" {g(s, 0.7)}/>')
    out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{10 * s:.1f}" fill="#8A5326" {g(s, 0.7)}/>')
    return ''.join(out)


def tractor(x, y, s, col='#5CBF3F'):
    return (contact_shadow(x, y + 3 * s, 46 * s, 8 * s, 0.3) +
            f'<rect x="{x - 40 * s:.1f}" y="{y - 40 * s:.1f}" width="{56 * s:.1f}" height="{24 * s:.1f}" rx="{5 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<rect x="{x + 4 * s:.1f}" y="{y - 70 * s:.1f}" width="{30 * s:.1f}" height="{54 * s:.1f}" rx="{4 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<rect x="{x + 9 * s:.1f}" y="{y - 64 * s:.1f}" width="{20 * s:.1f}" height="{18 * s:.1f}" fill="{PALETTE["window"]}" {g(s, 0.6)}/>'
            f'<rect x="{x - 30 * s:.1f}" y="{y - 56 * s:.1f}" width="{6 * s:.1f}" height="{18 * s:.1f}" fill="#555" {g(s, 0.6)}/>'
            f'<circle cx="{x + 22 * s:.1f}" cy="{y - 18 * s:.1f}" r="{18 * s:.1f}" fill="#33333D" {g(s)}/><circle cx="{x + 22 * s:.1f}" cy="{y - 18 * s:.1f}" r="{8 * s:.1f}" fill="#FFC93C"/>'
            f'<circle cx="{x - 28 * s:.1f}" cy="{y - 10 * s:.1f}" r="{10 * s:.1f}" fill="#33333D" {g(s)}/><circle cx="{x - 28 * s:.1f}" cy="{y - 10 * s:.1f}" r="{4 * s:.1f}" fill="#FFC93C"/>')


# ------------------------------------------------------------------ fields & market
def crop_rows(w, x0, y0, x1, y1, s, plant='lettuce', soil='#A0683A', n=6):
    """field patch with rows of plants; corners: near-left (x0,y1) .. far-right (x1,y0) parallelogram"""
    sk = (x1 - x0) * 0.12
    pts_ = [(x0 + sk, y0), (x1 + sk, y0), (x1, y1), (x0, y1)]
    out = []
    for i in range(n):
        t = (i + 0.5) / n
        yy = y0 + (y1 - y0) * t
        ss = s * (0.8 + 0.3 * t)
        xa, xb = x0 + sk * (1 - t), x1 + sk * (1 - t)
        out.append(f'<line x1="{xa + 10:.1f}" y1="{yy:.1f}" x2="{xb - 10:.1f}" y2="{yy:.1f}" stroke="{shade(soil, -0.2)}" stroke-width="{8 * ss:.1f}" stroke-linecap="round"/>')
        k = int((xb - xa) / (34 * ss))
        for j in range(k):
            px = xa + 20 + j * (xb - xa - 40) / max(1, k - 1)
            out.append(crop(px, yy, ss, plant))
    w.patch(pts_, soil, extra=''.join(out))


def crop(x, y, s, kind):
    if kind == 'pumpkin':
        return (f'<ellipse cx="{x:.1f}" cy="{y - 9 * s:.1f}" rx="{14 * s:.1f}" ry="{10 * s:.1f}" fill="#FF8A3D" {g(s, 0.6)}/>'
                f'<rect x="{x - 2 * s:.1f}" y="{y - 23 * s:.1f}" width="{4 * s:.1f}" height="{6 * s:.1f}" fill="#3E8E2F"/>')
    if kind == 'carrot':
        return ''.join(f'<path d="M{x:.1f} {y - 4 * s:.1f} l{q * 6 * s:.1f} {-18 * s:.1f}" stroke="#4E9F36" stroke-width="{4 * s:.1f}" stroke-linecap="round"/>' for q in (-1, 0, 1)) + \
            f'<ellipse cx="{x:.1f}" cy="{y - 2 * s:.1f}" rx="{6 * s:.1f}" ry="{3 * s:.1f}" fill="#FF8A3D"/>'
    if kind == 'sunflower':
        return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 40 * s:.1f}" stroke="#3E8E2F" stroke-width="{3.5 * s:.1f}"/>'
                f'<circle cx="{x:.1f}" cy="{y - 42 * s:.1f}" r="{11 * s:.1f}" fill="#FFD23F" {g(s, 0.5)}/><circle cx="{x:.1f}" cy="{y - 42 * s:.1f}" r="{5 * s:.1f}" fill="#8A5326"/>')
    if kind == 'wheat':
        return ''.join(f'<path d="M{x + q * 5 * s:.1f} {y:.1f} l{q * 2 * s:.1f} {-26 * s:.1f}" stroke="#E8B94A" stroke-width="{4 * s:.1f}" stroke-linecap="round"/>' for q in (-1, 0, 1))
    # lettuce / cabbage
    return (f'<circle cx="{x:.1f}" cy="{y - 8 * s:.1f}" r="{11 * s:.1f}" fill="#6CC24A" {g(s, 0.6)}/>'
            f'<circle cx="{x + 3 * s:.1f}" cy="{y - 11 * s:.1f}" r="{5 * s:.1f}" fill="#A6DE6A"/>')


def stall(x, y, s, col='#E5533D', goods=('#FF5E7E', '#FFD23F', '#6CC24A', '#FF8A3D')):
    w = 120 * s
    out = [contact_shadow(x + w / 2, y + 3 * s, w * 0.6, 9 * s, 0.25)]
    out.append(f'<rect x="{x:.1f}" y="{y - 46 * s:.1f}" width="{w:.1f}" height="{46 * s:.1f}" fill="#C98A4E" {g(s)}/>')
    out.append(f'<rect x="{x - 6 * s:.1f}" y="{y - 56 * s:.1f}" width="{w + 12 * s:.1f}" height="{14 * s:.1f}" fill="#E0A869" {g(s)}/>')
    for i in range(6):
        cx = x + 12 * s + i * (w - 24 * s) / 5
        out.append(f'<circle cx="{cx:.1f}" cy="{y - 62 * s:.1f}" r="{8 * s:.1f}" fill="{goods[i % len(goods)]}" {g(s, 0.5)}/>')
    for px in (x + 4 * s, x + w - 4 * s):
        out.append(f'<rect x="{px - 3 * s:.1f}" y="{y - 120 * s:.1f}" width="{6 * s:.1f}" height="{70 * s:.1f}" fill="#8A5326" {g(s, 0.6)}/>')
    n = 6
    for q in range(n):
        c = col if q % 2 == 0 else '#FFFFFF'
        x0 = x - 10 * s + q * (w + 20 * s) / n
        out.append(f'<path d="M{x0 + 6 * s:.1f} {y - 136 * s:.1f} L{x0 + (w + 20 * s) / n + 6 * s:.1f} {y - 136 * s:.1f} L{x0 + (w + 20 * s) / n:.1f} {y - 110 * s:.1f} '
                   f'a{(w + 20 * s) / n / 2:.1f} {9 * s:.1f} 0 0 1 {-(w + 20 * s) / n:.1f} 0 Z" fill="{c}"/>')
    out.append(f'<path d="M{x - 4 * s:.1f} {y - 136 * s:.1f} L{x + w + 16 * s:.1f} {y - 136 * s:.1f} L{x + w + 10 * s:.1f} {y - 110 * s:.1f} L{x - 10 * s:.1f} {y - 110 * s:.1f} Z" fill="none" {g(s)}/>')
    return ''.join(out)


def greenhouse(x, by, s, w=160, h=80):
    w, h = w * s, h * s
    glass = '#BFE8F5'
    b, dx, dy = box(x, by, w, h, s, glass, 'r', dep=w * 0.8, top=glass)
    out = [b]
    top = by - h
    out.append(poly([(x, top), (x + w, top), (x + w + dx * 0.5, top + dy * 0.5 - 40 * s), (x + dx * 0.5, top + dy * 0.5 - 40 * s)], '#D8F2FB', w=sw(s)))
    out.append(poly([(x + w, top), (x + w + dx, top + dy), (x + w + dx * 0.5, top + dy * 0.5 - 40 * s)], '#A8DCEB', w=sw(s)))
    for q in range(1, 5):
        xx = x + w * q / 5
        out.append(f'<line x1="{xx:.1f}" y1="{by:.1f}" x2="{xx:.1f}" y2="{top:.1f}" stroke="#FFFFFF" stroke-width="{4 * s:.1f}"/>')
    for q in range(5):
        out.append(f'<circle cx="{x + w * (0.1 + q * 0.2):.1f}" cy="{by - 18 * s:.1f}" r="{12 * s:.1f}" fill="#6CC24A" opacity="0.8"/>')
    out.append(f'<path d="M{x + 14 * s:.1f} {top + 8 * s:.1f} L{x + w * 0.4:.1f} {top + 8 * s:.1f}" stroke="#FFFFFF" stroke-width="{5 * s:.1f}" opacity="0.8" stroke-linecap="round"/>')
    return ''.join(out)


def fruit_tree(x, y, s, fruit='#FF4E4E', seed=0):
    r = rng(seed)
    out = [fluffy_tree(x, y, s, '#5CBF3F', seed)]
    for _ in range(7):
        out.append(f'<circle cx="{x + r.uniform(-40, 40) * s:.1f}" cy="{y + r.uniform(-120, -50) * s:.1f}" r="{6 * s:.1f}" fill="{fruit}" {g(s, 0.45)}/>')
    return ''.join(out)


def crates(x, y, s, fruit='#FF4E4E'):
    out = []
    for i, (cx, cy) in enumerate([(-22, 0), (22, 0), (0, -24)]):
        bx, byy = x + cx * s, y + cy * s
        out.append(f'<rect x="{bx - 20 * s:.1f}" y="{byy - 24 * s:.1f}" width="{40 * s:.1f}" height="{24 * s:.1f}" fill="#D9A066" {g(s, 0.8)}/>')
        for q in range(3):
            out.append(f'<circle cx="{bx - 12 * s + q * 12 * s:.1f}" cy="{byy - 26 * s:.1f}" r="{6 * s:.1f}" fill="{fruit}" {g(s, 0.4)}/>')
    return ''.join(out)


def scarecrow(x, y, s):
    return (contact_shadow(x, y + 2 * s, 20 * s, 5 * s, 0.25) +
            f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 90 * s:.1f}" stroke="#8A5326" stroke-width="{6 * s:.1f}"/>'
            f'<line x1="{x - 34 * s:.1f}" y1="{y - 66 * s:.1f}" x2="{x + 34 * s:.1f}" y2="{y - 66 * s:.1f}" stroke="#8A5326" stroke-width="{6 * s:.1f}"/>'
            f'<path d="M{x - 22 * s:.1f} {y - 74 * s:.1f} L{x + 22 * s:.1f} {y - 74 * s:.1f} L{x + 16 * s:.1f} {y - 34 * s:.1f} L{x - 16 * s:.1f} {y - 34 * s:.1f} Z" fill="#4F86C6" {g(s)}/>'
            f'<circle cx="{x:.1f}" cy="{y - 88 * s:.1f}" r="{13 * s:.1f}" fill="#F7E2B4" {g(s)}/>'
            f'<path d="M{x - 22 * s:.1f} {y - 96 * s:.1f} L{x + 22 * s:.1f} {y - 96 * s:.1f} L{x + 10 * s:.1f} {y - 112 * s:.1f} L{x - 10 * s:.1f} {y - 112 * s:.1f} Z" fill="#E8B94A" {g(s)}/>')
