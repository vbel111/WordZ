"""More v3 props: travel, weather, landmarks, sport, school, jobs, camping."""
import math
from style import OL, PALETTE, mix, shade, contact_shadow, rng, cloud
from city2 import sw, poly, pts, townhouse, fluffy_tree
from props3 import g, box


def field(w, x0, y0, x1, y1, col, stripe=None):
    sk = (x1 - x0) * 0.1
    p = [(x0 + sk, y0), (x1 + sk, y0), (x1, y1), (x0, y1)]
    ex = ''
    stripe = stripe or shade(col, -0.1)
    n = 5
    for i in range(1, n):
        t = i / n
        ex += f'<line x1="{x0 + sk * (1 - t) + 6:.1f}" y1="{y0 + (y1 - y0) * t:.1f}" x2="{x1 + sk * (1 - t) - 6:.1f}" y2="{y0 + (y1 - y0) * t:.1f}" stroke="{stripe}" stroke-width="5"/>'
    w.patch(p, col, extra=ex)


# ------------------------------------------------------------------ camping / nature
def cabin(x, by, s, w=150, h=100, side='r'):
    out = [townhouse(x, by, w * s, h * s, s, '#B8733F', '#7A4A26', side=side, floors=1, cols=2, seed=int(x), flowers=True)]
    for q in range(1, 6):
        yy = by - h * s * q / 6
        out.append(f'<line x1="{x:.1f}" y1="{yy:.1f}" x2="{x + w * s:.1f}" y2="{yy:.1f}" stroke="#8A5326" stroke-width="{2.5 * s:.1f}" opacity="0.7"/>')
    return ''.join(out)


def tent(x, y, s, col='#FF8A3D'):
    return (contact_shadow(x, y + 3 * s, 50 * s, 9 * s, 0.25) +
            f'<path d="M{x - 50 * s:.1f} {y:.1f} L{x - 6 * s:.1f} {y - 70 * s:.1f} L{x + 40 * s:.1f} {y - 64 * s:.1f} L{x + 70 * s:.1f} {y - 6 * s:.1f} L{x + 30 * s:.1f} {y:.1f} Z" fill="{shade(col, -0.2)}" {g(s)}/>'
            f'<path d="M{x - 50 * s:.1f} {y:.1f} L{x - 6 * s:.1f} {y - 70 * s:.1f} L{x + 30 * s:.1f} {y:.1f} Z" fill="{col}" {g(s)}/>'
            f'<path d="M{x - 6 * s:.1f} {y - 40 * s:.1f} L{x - 18 * s:.1f} {y:.1f} L{x + 6 * s:.1f} {y:.1f} Z" fill="#5A3A22"/>')


def campfire(x, y, s):
    return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{26 * s:.1f}" ry="{8 * s:.1f}" fill="#8A8077" {g(s, 0.6)}/>'
            f'<path d="M{x - 18 * s:.1f} {y - 4 * s:.1f} L{x + 18 * s:.1f} {y - 12 * s:.1f} M{x - 18 * s:.1f} {y - 12 * s:.1f} L{x + 18 * s:.1f} {y - 4 * s:.1f}" stroke="#8A5326" stroke-width="{6 * s:.1f}" stroke-linecap="round"/>'
            f'<path d="M{x - 12 * s:.1f} {y - 8 * s:.1f} Q{x - 14 * s:.1f} {y - 34 * s:.1f} {x:.1f} {y - 44 * s:.1f} Q{x + 14 * s:.1f} {y - 30 * s:.1f} {x + 12 * s:.1f} {y - 8 * s:.1f} Z" fill="#FF8A3D" {g(s, 0.6)}/>'
            f'<path d="M{x - 5 * s:.1f} {y - 9 * s:.1f} Q{x - 4 * s:.1f} {y - 24 * s:.1f} {x + 2 * s:.1f} {y - 28 * s:.1f} Q{x + 6 * s:.1f} {y - 18 * s:.1f} {x + 5 * s:.1f} {y - 9 * s:.1f} Z" fill="#FFE27A"/>')


def waterfall(x, top, bottom, wd):
    return (f'<rect x="{x - wd / 2:.1f}" y="{top:.1f}" width="{wd:.1f}" height="{bottom - top:.1f}" fill="#8FD5F5" stroke="{OL}" stroke-width="4"/>'
            + ''.join(f'<line x1="{x - wd / 2 + q * wd / 5:.1f}" y1="{top + 6:.1f}" x2="{x - wd / 2 + q * wd / 5:.1f}" y2="{bottom - 6:.1f}" stroke="#FFFFFF" stroke-width="4" opacity="0.7"/>' for q in range(1, 5))
            + ''.join(f'<circle cx="{x + dx:.1f}" cy="{bottom + 4:.1f}" r="{r:.1f}" fill="#FFFFFF" opacity="0.9"/>' for dx, r in [(-wd * 0.5, 14), (-wd * 0.15, 18), (wd * 0.2, 16), (wd * 0.5, 12)]))


# ------------------------------------------------------------------ travel / seaside
def palm(x, y, s, lean=1):
    k = sw(s)
    tx, ty = x + 26 * s * lean, y - 150 * s
    out = [contact_shadow(x, y + 2 * s, 34 * s, 7 * s, 0.25),
           f'<path d="M{x - 8 * s:.1f} {y:.1f} Q{x + 4 * s * lean:.1f} {y - 80 * s:.1f} {tx - 5 * s:.1f} {ty:.1f} L{tx + 5 * s:.1f} {ty:.1f} Q{x + 14 * s * lean:.1f} {y - 80 * s:.1f} {x + 8 * s:.1f} {y:.1f} Z" fill="#B8733F" {g(s)}/>']
    for q in range(1, 6):
        yy = y - q * 25 * s
        out.append(f'<line x1="{x + (q * 4) * s * lean - 7 * s:.1f}" y1="{yy:.1f}" x2="{x + (q * 4) * s * lean + 7 * s:.1f}" y2="{yy + 3 * s:.1f}" stroke="{OL}" stroke-width="{k * 0.5:.1f}"/>')
    for a in [-2.7, -2.2, -1.6, -1.0, -0.45, 0.1]:
        ex, ey = tx + math.cos(a) * 80 * s, ty + math.sin(a) * 40 * s + 34 * s
        mx, my = tx + math.cos(a) * 40 * s, ty + math.sin(a) * 40 * s - 14 * s
        out.append(f'<path d="M{tx:.1f} {ty:.1f} Q{mx:.1f} {my:.1f} {ex:.1f} {ey:.1f} Q{mx:.1f} {my + 18 * s:.1f} {tx:.1f} {ty + 6 * s:.1f} Z" fill="#4FB043" {g(s, 0.8)}/>')
    out.append(f'<circle cx="{tx - 6 * s:.1f}" cy="{ty + 8 * s:.1f}" r="{7 * s:.1f}" fill="#8A5326" {g(s, 0.5)}/><circle cx="{tx + 7 * s:.1f}" cy="{ty + 9 * s:.1f}" r="{7 * s:.1f}" fill="#8A5326" {g(s, 0.5)}/>')
    return ''.join(out)


def beach_umbrella(x, y, s, col='#FF5E7E'):
    from city2 import parasol
    return (f'<rect x="{x - 30 * s:.1f}" y="{y - 8 * s:.1f}" width="{60 * s:.1f}" height="{14 * s:.1f}" rx="{4 * s:.1f}" fill="#FFFFFF" {g(s, 0.6)}/>'
            + parasol(x, y, s, col))


def beach_hut(x, by, s, col='#4FA3E3', side='r'):
    out = [townhouse(x, by, 80 * s, 80 * s, s, '#FFFFFF', col, side=side, floors=1, cols=1, seed=int(x), flowers=False)]
    for q in range(4):
        out.append(f'<rect x="{x + q * 20 * s + 2 * s:.1f}" y="{by - 78 * s:.1f}" width="{8 * s:.1f}" height="{76 * s:.1f}" fill="{col}" opacity="0.8"/>')
    return ''.join(out)


def lighthouse(x, y, s):
    out = [contact_shadow(x, y + 4 * s, 50 * s, 10 * s, 0.25),
           f'<path d="M{x - 34 * s:.1f} {y:.1f} L{x - 22 * s:.1f} {y - 220 * s:.1f} L{x + 22 * s:.1f} {y - 220 * s:.1f} L{x + 34 * s:.1f} {y:.1f} Z" fill="#FFFFFF" {g(s)}/>']
    for q in (0, 2):
        y0, y1 = y - (q * 55 + 30) * s, y - (q * 55 + 85) * s
        out.append(f'<path d="M{x - 32 * s + q * 2.5 * s:.1f} {y0:.1f} L{x - 28 * s + q * 2.5 * s:.1f} {y1:.1f} L{x + 28 * s - q * 2.5 * s:.1f} {y1:.1f} L{x + 32 * s - q * 2.5 * s:.1f} {y0:.1f} Z" fill="#E5533D"/>')
    out.append(f'<path d="M{x - 34 * s:.1f} {y:.1f} L{x - 22 * s:.1f} {y - 220 * s:.1f} L{x + 22 * s:.1f} {y - 220 * s:.1f} L{x + 34 * s:.1f} {y:.1f} Z" fill="none" {g(s)}/>')
    out.append(f'<rect x="{x - 30 * s:.1f}" y="{y - 232 * s:.1f}" width="{60 * s:.1f}" height="{12 * s:.1f}" fill="#3C4A5C" {g(s, 0.8)}/>')
    out.append(f'<rect x="{x - 18 * s:.1f}" y="{y - 270 * s:.1f}" width="{36 * s:.1f}" height="{38 * s:.1f}" fill="#FFE27A" {g(s, 0.8)}/>')
    out.append(f'<path d="M{x - 24 * s:.1f} {y - 270 * s:.1f} L{x:.1f} {y - 300 * s:.1f} L{x + 24 * s:.1f} {y - 270 * s:.1f} Z" fill="#E5533D" {g(s, 0.8)}/>')
    out.append(f'<path d="M{x + 18 * s:.1f} {y - 252 * s:.1f} L{x + 140 * s:.1f} {y - 280 * s:.1f} L{x + 140 * s:.1f} {y - 224 * s:.1f} Z" fill="#FFF6C2" opacity="0.4"/>')
    return ''.join(out)


def plane(x, y, s, col='#FFFFFF', tail='#E5533D', ground=True):
    out = []
    if ground:
        out.append(contact_shadow(x, y + 4 * s, 120 * s, 14 * s, 0.25))
    by = y - (26 * s if ground else 0)
    out.append(f'<path d="M{x - 40 * s:.1f} {by - 6 * s:.1f} L{x - 90 * s:.1f} {by + 34 * s:.1f} L{x - 60 * s:.1f} {by + 36 * s:.1f} L{x + 10 * s:.1f} {by + 4 * s:.1f} Z" fill="{shade(col, -0.12)}" {g(s)}/>')
    out.append(f'<path d="M{x - 130 * s:.1f} {by - 4 * s:.1f} Q{x - 130 * s:.1f} {by - 20 * s:.1f} {x - 100 * s:.1f} {by - 20 * s:.1f} L{x + 110 * s:.1f} {by - 20 * s:.1f} Q{x + 140 * s:.1f} {by - 14 * s:.1f} {x + 140 * s:.1f} {by - 2 * s:.1f} Q{x + 136 * s:.1f} {by + 8 * s:.1f} {x + 110 * s:.1f} {by + 8 * s:.1f} L{x - 110 * s:.1f} {by + 8 * s:.1f} Q{x - 130 * s:.1f} {by + 8 * s:.1f} {x - 130 * s:.1f} {by - 4 * s:.1f} Z" fill="{col}" {g(s)}/>')
    out.append(f'<path d="M{x - 110 * s:.1f} {by - 18 * s:.1f} L{x - 130 * s:.1f} {by - 60 * s:.1f} L{x - 100 * s:.1f} {by - 60 * s:.1f} L{x - 70 * s:.1f} {by - 18 * s:.1f} Z" fill="{tail}" {g(s)}/>')
    out.append(f'<path d="M{x - 30 * s:.1f} {by - 4 * s:.1f} L{x - 70 * s:.1f} {by - 44 * s:.1f} L{x - 44 * s:.1f} {by - 44 * s:.1f} L{x + 10 * s:.1f} {by - 6 * s:.1f} Z" fill="{shade(col, -0.05)}" {g(s)}/>')
    for q in range(8):
        out.append(f'<circle cx="{x - 70 * s + q * 22 * s:.1f}" cy="{by - 8 * s:.1f}" r="{4 * s:.1f}" fill="{PALETTE["window"]}" {g(s, 0.4)}/>')
    out.append(f'<path d="M{x + 116 * s:.1f} {by - 14 * s:.1f} Q{x + 130 * s:.1f} {by - 12 * s:.1f} {x + 134 * s:.1f} {by - 4 * s:.1f} L{x + 116 * s:.1f} {by - 4 * s:.1f} Z" fill="#3C4A5C"/>')
    out.append(f'<rect x="{x - 110 * s:.1f}" y="{by - 2 * s:.1f}" width="{220 * s:.1f}" height="{4 * s:.1f}" fill="{tail}"/>')
    if ground:
        for q in (-60, 40):
            out.append(f'<line x1="{x + q * s:.1f}" y1="{by + 8 * s:.1f}" x2="{x + q * s:.1f}" y2="{y - 6 * s:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}"/><circle cx="{x + q * s:.1f}" cy="{y - 4 * s:.1f}" r="{6 * s:.1f}" fill="#33333D"/>')
    return ''.join(out)


def balloon(x, y, s, cols=('#E5533D', '#FFD23F')):
    out = [f'<path d="M{x - 50 * s:.1f} {y:.1f} Q{x - 54 * s:.1f} {y - 70 * s:.1f} {x:.1f} {y - 74 * s:.1f} Q{x + 54 * s:.1f} {y - 70 * s:.1f} {x + 50 * s:.1f} {y:.1f} Q{x + 30 * s:.1f} {y + 40 * s:.1f} {x + 12 * s:.1f} {y + 52 * s:.1f} L{x - 12 * s:.1f} {y + 52 * s:.1f} Q{x - 30 * s:.1f} {y + 40 * s:.1f} {x - 50 * s:.1f} {y:.1f} Z" fill="{cols[0]}" {g(s)}/>']
    for q in (-1, 1):
        out.append(f'<path d="M{x + q * 18 * s:.1f} {y - 72 * s:.1f} Q{x + q * 34 * s:.1f} {y:.1f} {x + q * 8 * s:.1f} {y + 52 * s:.1f} L{x + q * 2 * s:.1f} {y + 52 * s:.1f} Q{x + q * 16 * s:.1f} {y:.1f} {x + q * 4 * s:.1f} {y - 74 * s:.1f} Z" fill="{cols[1]}"/>')
    out.append(f'<ellipse cx="{x - 20 * s:.1f}" cy="{y - 40 * s:.1f}" rx="{10 * s:.1f}" ry="{20 * s:.1f}" fill="#FFFFFF" opacity="0.35"/>')
    out.append(f'<path d="M{x - 12 * s:.1f} {y + 52 * s:.1f} L{x - 10 * s:.1f} {y + 66 * s:.1f} M{x + 12 * s:.1f} {y + 52 * s:.1f} L{x + 10 * s:.1f} {y + 66 * s:.1f}" stroke="{OL}" stroke-width="{2.5 * s:.1f}"/>')
    out.append(f'<rect x="{x - 12 * s:.1f}" y="{y + 66 * s:.1f}" width="{24 * s:.1f}" height="{16 * s:.1f}" rx="{3 * s:.1f}" fill="#B8733F" {g(s, 0.8)}/>')
    return ''.join(out)


def suitcase(x, y, s, col='#4FA3E3'):
    return (contact_shadow(x, y + 2 * s, 24 * s, 5 * s, 0.25) +
            f'<rect x="{x - 22 * s:.1f}" y="{y - 46 * s:.1f}" width="{44 * s:.1f}" height="{46 * s:.1f}" rx="{6 * s:.1f}" fill="{col}" {g(s)}/>'
            f'<rect x="{x - 9 * s:.1f}" y="{y - 56 * s:.1f}" width="{18 * s:.1f}" height="{12 * s:.1f}" rx="{4 * s:.1f}" fill="none" {g(s)}/>'
            f'<line x1="{x - 22 * s:.1f}" y1="{y - 24 * s:.1f}" x2="{x + 22 * s:.1f}" y2="{y - 24 * s:.1f}" stroke="#FFFFFF" stroke-width="{4 * s:.1f}" opacity="0.7"/>')


def control_tower(x, y, s):
    return (contact_shadow(x, y + 3 * s, 30 * s, 7 * s, 0.25) +
            f'<path d="M{x - 18 * s:.1f} {y:.1f} L{x - 12 * s:.1f} {y - 170 * s:.1f} L{x + 12 * s:.1f} {y - 170 * s:.1f} L{x + 18 * s:.1f} {y:.1f} Z" fill="#E8E2D6" {g(s)}/>'
            f'<path d="M{x - 40 * s:.1f} {y - 170 * s:.1f} L{x + 40 * s:.1f} {y - 170 * s:.1f} L{x + 30 * s:.1f} {y - 210 * s:.1f} L{x - 30 * s:.1f} {y - 210 * s:.1f} Z" fill="#7FC6EE" {g(s)}/>'
            f'<rect x="{x - 34 * s:.1f}" y="{y - 222 * s:.1f}" width="{68 * s:.1f}" height="{12 * s:.1f}" fill="#3C4A5C" {g(s, 0.8)}/>'
            f'<line x1="{x:.1f}" y1="{y - 222 * s:.1f}" x2="{x:.1f}" y2="{y - 250 * s:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}"/><circle cx="{x:.1f}" cy="{y - 252 * s:.1f}" r="{4 * s:.1f}" fill="#E5533D"/>')


# ------------------------------------------------------------------ weather
def rainbow(cx, cy, r, width=26, op=0.85):
    cols = ['#FF5E5E', '#FF9F43', '#FFD23F', '#6CC24A', '#4FA3E3', '#8E7CF0']
    return ''.join(f'<path d="M{cx - r + i * width:.0f} {cy} A{r - i * width:.0f} {r - i * width:.0f} 0 0 1 {cx + r - i * width:.0f} {cy}" fill="none" stroke="{c}" stroke-width="{width + 1}" opacity="{op}"/>'
                   for i, c in enumerate(cols))


def rain_cloud(x, y, s, rain=True, dark='#A9B7C9'):
    out = [cloud(x, y, s, 1.0, dark)]
    if rain:
        for q in range(7):
            rx = x + (-70 + q * 24) * s
            out.append(f'<line x1="{rx:.1f}" y1="{y + 26 * s:.1f}" x2="{rx - 10 * s:.1f}" y2="{y + 60 * s:.1f}" stroke="#4FA3E3" stroke-width="{4 * s:.1f}" stroke-linecap="round" opacity="0.8"/>')
    return ''.join(out)


def snowman(x, y, s):
    return (contact_shadow(x, y + 2 * s, 30 * s, 7 * s, 0.22) +
            f'<circle cx="{x:.1f}" cy="{y - 26 * s:.1f}" r="{28 * s:.1f}" fill="#FFFFFF" {g(s)}/>'
            f'<circle cx="{x:.1f}" cy="{y - 72 * s:.1f}" r="{20 * s:.1f}" fill="#FFFFFF" {g(s)}/>'
            f'<path d="M{x:.1f} {y - 72 * s:.1f} l{18 * s:.1f} {4 * s:.1f} l{-18 * s:.1f} {3 * s:.1f} Z" fill="#FF8A3D"/>'
            f'<circle cx="{x - 7 * s:.1f}" cy="{y - 78 * s:.1f}" r="{2.5 * s:.1f}" fill="{OL}"/><circle cx="{x + 7 * s:.1f}" cy="{y - 78 * s:.1f}" r="{2.5 * s:.1f}" fill="{OL}"/>'
            f'<rect x="{x - 22 * s:.1f}" y="{y - 58 * s:.1f}" width="{44 * s:.1f}" height="{8 * s:.1f}" rx="{4 * s:.1f}" fill="#E5533D" {g(s, 0.6)}/>'
            f'<rect x="{x - 14 * s:.1f}" y="{y - 108 * s:.1f}" width="{28 * s:.1f}" height="{20 * s:.1f}" fill="#3C4A5C" {g(s, 0.7)}/><rect x="{x - 20 * s:.1f}" y="{y - 92 * s:.1f}" width="{40 * s:.1f}" height="{5 * s:.1f}" fill="#3C4A5C" {g(s, 0.7)}/>')


def wind_turbine(x, y, s, a=0.4):
    out = [contact_shadow(x, y + 2 * s, 20 * s, 5 * s, 0.22),
           f'<path d="M{x - 6 * s:.1f} {y:.1f} L{x - 3 * s:.1f} {y - 200 * s:.1f} L{x + 3 * s:.1f} {y - 200 * s:.1f} L{x + 6 * s:.1f} {y:.1f} Z" fill="#FFFFFF" {g(s, 0.8)}/>']
    hx, hy = x, y - 200 * s
    for q in range(3):
        ang = a + q * 2 * math.pi / 3
        ex, ey = hx + math.cos(ang) * 90 * s, hy + math.sin(ang) * 90 * s
        px, py = -math.sin(ang) * 8 * s, math.cos(ang) * 8 * s
        out.append(f'<path d="M{hx:.1f} {hy:.1f} L{hx + px:.1f} {hy + py:.1f} L{ex:.1f} {ey:.1f} Z" fill="#FFFFFF" {g(s, 0.7)}/>')
    out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{7 * s:.1f}" fill="#E8E2D6" {g(s, 0.7)}/>')
    return ''.join(out)


def weather_station(x, y, s):
    return (contact_shadow(x, y + 2 * s, 30 * s, 6 * s, 0.22) +
            f'<rect x="{x - 26 * s:.1f}" y="{y - 46 * s:.1f}" width="{52 * s:.1f}" height="{46 * s:.1f}" fill="#FFFFFF" {g(s)}/>'
            + ''.join(f'<line x1="{x - 22 * s:.1f}" y1="{y - 40 * s + q * 9 * s:.1f}" x2="{x + 22 * s:.1f}" y2="{y - 40 * s + q * 9 * s:.1f}" stroke="#C9C2B4" stroke-width="{3 * s:.1f}"/>' for q in range(5)) +
            f'<line x1="{x:.1f}" y1="{y - 46 * s:.1f}" x2="{x:.1f}" y2="{y - 120 * s:.1f}" stroke="{OL}" stroke-width="{4 * s:.1f}"/>'
            + ''.join(f'<line x1="{x:.1f}" y1="{y - 116 * s:.1f}" x2="{x + math.cos(a) * 26 * s:.1f}" y2="{y - 116 * s + math.sin(a) * 10 * s:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}"/>'
                      f'<circle cx="{x + math.cos(a) * 26 * s:.1f}" cy="{y - 116 * s + math.sin(a) * 10 * s:.1f}" r="{6 * s:.1f}" fill="#E5533D" {g(s, 0.5)}/>' for a in (0.3, 2.4, 4.4)))


def umbrella_stand(x, y, s, col='#4FA3E3'):
    return (f'<path d="M{x:.1f} {y:.1f} L{x:.1f} {y - 60 * s:.1f}" stroke="{OL}" stroke-width="{4 * s:.1f}"/>'
            f'<path d="M{x - 40 * s:.1f} {y - 58 * s:.1f} Q{x:.1f} {y - 106 * s:.1f} {x + 40 * s:.1f} {y - 58 * s:.1f} Q{x + 26 * s:.1f} {y - 66 * s:.1f} {x + 13 * s:.1f} {y - 58 * s:.1f} Q{x:.1f} {y - 66 * s:.1f} {x - 13 * s:.1f} {y - 58 * s:.1f} Q{x - 26 * s:.1f} {y - 66 * s:.1f} {x - 40 * s:.1f} {y - 58 * s:.1f} Z" fill="{col}" {g(s)}/>'
            f'<path d="M{x:.1f} {y:.1f} q{-8 * s:.1f} 0 {-8 * s:.1f} {-8 * s:.1f}" fill="none" stroke="{OL}" stroke-width="{4 * s:.1f}"/>')


# ------------------------------------------------------------------ landmarks (countries)
def pyramid(x, y, s, sz=1.0):
    k = sz * s
    return (contact_shadow(x + 20 * k, y + 4 * k, 120 * k, 16 * k, 0.25) +
            f'<path d="M{x - 110 * k:.1f} {y:.1f} L{x:.1f} {y - 120 * k:.1f} L{x + 40 * k:.1f} {y + 4 * k:.1f} Z" fill="#F2C97A" {g(s)}/>'
            f'<path d="M{x:.1f} {y - 120 * k:.1f} L{x + 40 * k:.1f} {y + 4 * k:.1f} L{x + 120 * k:.1f} {y - 20 * k:.1f} Z" fill="#D9A55A" {g(s)}/>'
            + ''.join(f'<line x1="{x - 110 * k + q * 22 * k:.1f}" y1="{y - q * 24 * k:.1f}" x2="{x + 40 * k - q * 8 * k:.1f}" y2="{y + 4 * k - q * 25 * k:.1f}" stroke="#D9A55A" stroke-width="{2.5 * s:.1f}"/>' for q in range(1, 5)))


def pagoda(x, y, s, col='#E5533D'):
    out = [contact_shadow(x, y + 4 * s, 70 * s, 12 * s, 0.25)]
    for i in range(4):
        wd, yy = 70 - i * 12, y - i * 58 * s
        out.append(f'<rect x="{x - wd * 0.6 * s:.1f}" y="{yy - 40 * s:.1f}" width="{wd * 1.2 * s:.1f}" height="{40 * s:.1f}" fill="#FFF3D6" {g(s)}/>')
        out.append(f'<rect x="{x - 10 * s:.1f}" y="{yy - 30 * s:.1f}" width="{20 * s:.1f}" height="{22 * s:.1f}" fill="{col}" {g(s, 0.6)}/>')
        out.append(f'<path d="M{x - wd * s - 14 * s:.1f} {yy - 34 * s:.1f} Q{x - wd * 0.6 * s:.1f} {yy - 44 * s:.1f} {x - wd * 0.5 * s:.1f} {yy - 58 * s:.1f} L{x + wd * 0.5 * s:.1f} {yy - 58 * s:.1f} Q{x + wd * 0.6 * s:.1f} {yy - 44 * s:.1f} {x + wd * s + 14 * s:.1f} {yy - 34 * s:.1f} Z" fill="{col}" {g(s)}/>')
    out.append(f'<line x1="{x:.1f}" y1="{y - 232 * s:.1f}" x2="{x:.1f}" y2="{y - 270 * s:.1f}" stroke="{OL}" stroke-width="{4 * s:.1f}"/><circle cx="{x:.1f}" cy="{y - 272 * s:.1f}" r="{5 * s:.1f}" fill="#FFC93C" {g(s, 0.5)}/>')
    return ''.join(out)


def lattice_tower(x, y, s):
    c = '#B8733F'
    out = [contact_shadow(x, y + 4 * s, 70 * s, 10 * s, 0.25),
           f'<path d="M{x - 60 * s:.1f} {y:.1f} Q{x - 20 * s:.1f} {y - 120 * s:.1f} {x - 8 * s:.1f} {y - 300 * s:.1f} L{x + 8 * s:.1f} {y - 300 * s:.1f} Q{x + 20 * s:.1f} {y - 120 * s:.1f} {x + 60 * s:.1f} {y:.1f} L{x + 36 * s:.1f} {y:.1f} Q{x:.1f} {y - 60 * s:.1f} {x - 36 * s:.1f} {y:.1f} Z" fill="{c}" {g(s)}/>']
    for yy, wd in [(110, 34), (200, 18)]:
        out.append(f'<rect x="{x - wd * s:.1f}" y="{y - yy * s:.1f}" width="{wd * 2 * s:.1f}" height="{8 * s:.1f}" fill="{shade(c, -0.15)}" {g(s, 0.6)}/>')
    for q in range(6):
        y0 = y - (20 + q * 40) * s
        out.append(f'<path d="M{x - (40 - q * 5) * s:.1f} {y0:.1f} L{x + (34 - q * 5) * s:.1f} {y0 - 36 * s:.1f} M{x + (40 - q * 5) * s:.1f} {y0:.1f} L{x - (34 - q * 5) * s:.1f} {y0 - 36 * s:.1f}" stroke="{shade(c, -0.25)}" stroke-width="{2 * s:.1f}"/>')
    out.append(f'<line x1="{x:.1f}" y1="{y - 300 * s:.1f}" x2="{x:.1f}" y2="{y - 340 * s:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}"/>')
    return ''.join(out)


def onion_dome(x, by, s, cols=('#E5533D', '#2F9C9A', '#FFC93C')):
    out = [townhouse(x - 70 * s, by, 140 * s, 120 * s, s, '#F7E2B4', '#C24B34', side='r', floors=2, cols=3, seed=int(x), roof_kind='flat', flowers=False)]
    for i, (dx, sz, c) in enumerate([(-38, 0.7, cols[1]), (38, 0.7, cols[2]), (0, 1.0, cols[0])]):
        cx, base = x + dx * s, by - 120 * s - 30 * s
        out.append(f'<rect x="{cx - 16 * sz * s:.1f}" y="{base - 40 * sz * s:.1f}" width="{32 * sz * s:.1f}" height="{44 * sz * s:.1f}" fill="#FFF3D6" {g(s)}/>')
        out.append(f'<path d="M{cx:.1f} {base - 110 * sz * s:.1f} Q{cx + 40 * sz * s:.1f} {base - 70 * sz * s:.1f} {cx + 22 * sz * s:.1f} {base - 40 * sz * s:.1f} L{cx - 22 * sz * s:.1f} {base - 40 * sz * s:.1f} Q{cx - 40 * sz * s:.1f} {base - 70 * sz * s:.1f} {cx:.1f} {base - 110 * sz * s:.1f} Z" fill="{c}" {g(s)}/>')
        out.append(f'<path d="M{cx - 8 * sz * s:.1f} {base - 90 * sz * s:.1f} Q{cx - 18 * sz * s:.1f} {base - 70 * sz * s:.1f} {cx - 12 * sz * s:.1f} {base - 50 * sz * s:.1f}" stroke="#FFFFFF" stroke-width="{3 * s:.1f}" fill="none" opacity="0.6"/>')
    return ''.join(out)


def flagpole(x, y, s, cols=('#E5533D', '#FFFFFF', '#4FA3E3'), vertical=False):
    out = [f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 110 * s:.1f}" stroke="{OL}" stroke-width="{4 * s:.1f}"/>']
    fw, fh = 50 * s, 32 * s
    for i, c in enumerate(cols):
        if vertical:
            out.append(f'<rect x="{x + i * fw / 3:.1f}" y="{y - 110 * s:.1f}" width="{fw / 3 + 0.5:.1f}" height="{fh:.1f}" fill="{c}"/>')
        else:
            out.append(f'<rect x="{x:.1f}" y="{y - 110 * s + i * fh / 3:.1f}" width="{fw:.1f}" height="{fh / 3 + 0.5:.1f}" fill="{c}"/>')
    out.append(f'<rect x="{x:.1f}" y="{y - 110 * s:.1f}" width="{fw:.1f}" height="{fh:.1f}" fill="none" {g(s, 0.6)}/>')
    return ''.join(out)


# ------------------------------------------------------------------ sport
def pitch(w, x0, y0, x1, y1, col='#5DB84A', line='#FFFFFF', kind='football'):
    sk = (x1 - x0) * 0.1
    p = [(x0 + sk, y0), (x1 + sk, y0), (x1, y1), (x0, y1)]
    ex = []
    for q in range(6):
        t0, t1 = q / 6, (q + 1) / 6
        if q % 2:
            ex.append(poly([(x0 + sk + (x1 - x0) * t0, y0), (x0 + sk + (x1 - x0) * t1, y0), (x0 + (x1 - x0) * t1, y1), (x0 + (x1 - x0) * t0, y1)], shade(col, 0.08)))
    m = 10
    q = [(x0 + sk * 0.92 + m, y0 + m * 0.6), (x1 + sk * 0.92 - m, y0 + m * 0.6), (x1 - m, y1 - m * 0.6), (x0 + m, y1 - m * 0.6)]
    ex.append(poly(q, 'none', stroke=line, w=4))
    mx0, mx1 = (q[0][0] + q[1][0]) / 2, (q[3][0] + q[2][0]) / 2
    ex.append(f'<line x1="{mx0:.1f}" y1="{q[0][1]:.1f}" x2="{mx1:.1f}" y2="{q[3][1]:.1f}" stroke="{line}" stroke-width="4"/>')
    cx, cy = (mx0 + mx1) / 2, (y0 + y1) / 2
    ex.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{(x1 - x0) * 0.09:.1f}" ry="{(y1 - y0) * 0.16:.1f}" fill="none" stroke="{line}" stroke-width="4"/>')
    if kind == 'tennis':
        ex.append(f'<line x1="{q[0][0]:.1f}" y1="{(y0 + y1) / 2:.1f}" x2="{q[1][0]:.1f}" y2="{(y0 + y1) / 2:.1f}" stroke="{line}" stroke-width="4"/>')
    w.patch(p, col, extra=''.join(ex))


def goal(x, y, s):
    return (f'<path d="M{x - 40 * s:.1f} {y:.1f} L{x - 40 * s:.1f} {y - 40 * s:.1f} L{x + 40 * s:.1f} {y - 40 * s:.1f} L{x + 40 * s:.1f} {y:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{6 * s:.1f}"/>'
            + ''.join(f'<line x1="{x - 40 * s + q * 10 * s:.1f}" y1="{y - 40 * s:.1f}" x2="{x - 36 * s + q * 10 * s:.1f}" y2="{y:.1f}" stroke="#FFFFFF" stroke-width="{1.5 * s:.1f}" opacity="0.7"/>' for q in range(9)))


def hoop(x, y, s):
    return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y - 110 * s:.1f}" stroke="#3C4A5C" stroke-width="{6 * s:.1f}"/>'
            f'<rect x="{x - 26 * s:.1f}" y="{y - 140 * s:.1f}" width="{52 * s:.1f}" height="{36 * s:.1f}" fill="#FFFFFF" {g(s)}/>'
            f'<rect x="{x - 10 * s:.1f}" y="{y - 130 * s:.1f}" width="{20 * s:.1f}" height="{14 * s:.1f}" fill="none" stroke="#E5533D" stroke-width="{3 * s:.1f}"/>'
            f'<ellipse cx="{x:.1f}" cy="{y - 104 * s:.1f}" rx="{14 * s:.1f}" ry="{4 * s:.1f}" fill="none" stroke="#FF8A3D" stroke-width="{4 * s:.1f}"/>')


def stadium(x, y, s, col='#E5533D'):
    rx, ry = 300 * s, 120 * s
    out = [contact_shadow(x, y + 10 * s, rx, 30 * s, 0.25),
           f'<ellipse cx="{x:.1f}" cy="{y - 40 * s:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{col}" {g(s)}/>',
           f'<path d="M{x - rx:.1f} {y - 40 * s:.1f} L{x - rx:.1f} {y - 10 * s:.1f} A{rx:.1f} {ry:.1f} 0 0 0 {x + rx:.1f} {y - 10 * s:.1f} L{x + rx:.1f} {y - 40 * s:.1f}" fill="{shade(col, -0.2)}" {g(s)}/>',
           f'<ellipse cx="{x:.1f}" cy="{y - 44 * s:.1f}" rx="{rx * 0.86:.1f}" ry="{ry * 0.76:.1f}" fill="#F7EAD0" {g(s)}/>']
    r = rng(int(x))
    for q in range(90):
        a = r.uniform(0, math.pi * 2)
        rr = r.uniform(0.62, 0.84)
        out.append(f'<circle cx="{x + math.cos(a) * rx * rr:.1f}" cy="{y - 44 * s + math.sin(a) * ry * rr * 0.9:.1f}" r="{4 * s:.1f}" fill="{r.choice(["#E5533D", "#4FA3E3", "#FFD23F", "#FFFFFF", "#6CC24A"])}"/>')
    out.append(f'<ellipse cx="{x:.1f}" cy="{y - 40 * s:.1f}" rx="{rx * 0.56:.1f}" ry="{ry * 0.44:.1f}" fill="#5DB84A" {g(s)}/>')
    out.append(f'<line x1="{x:.1f}" y1="{y - 40 * s - ry * 0.44:.1f}" x2="{x:.1f}" y2="{y - 40 * s + ry * 0.44:.1f}" stroke="#FFFFFF" stroke-width="{3 * s:.1f}"/>')
    for q in (-1, 1):
        lx = x + q * rx * 0.95
        out.append(f'<line x1="{lx:.1f}" y1="{y - 30 * s:.1f}" x2="{lx:.1f}" y2="{y - 230 * s:.1f}" stroke="#3C4A5C" stroke-width="{6 * s:.1f}"/>'
                   f'<rect x="{lx - 26 * s:.1f}" y="{y - 260 * s:.1f}" width="{52 * s:.1f}" height="{30 * s:.1f}" fill="#FFF3B8" {g(s)}/>')
    for q in range(5):
        fx = x - rx * 0.5 + q * rx * 0.25
        out.append(flagpole(fx, y - 40 * s - ry * 0.95, s * 0.7, (['#E5533D', '#4FA3E3', '#FFD23F', '#6CC24A', '#FF8A3D'][q],) * 3))
    return ''.join(out)


def bleachers(x, y, s, w=200, col='#4FA3E3'):
    w = w * s
    out = [contact_shadow(x + w / 2, y + 3 * s, w * 0.6, 8 * s, 0.25)]
    for q in range(4):
        yy = y - q * 14 * s
        out.append(f'<rect x="{x + q * 8 * s:.1f}" y="{yy - 14 * s:.1f}" width="{w - q * 16 * s:.1f}" height="{14 * s:.1f}" fill="{shade(col, -0.05 * q)}" {g(s, 0.8)}/>')
    return ''.join(out)


# ------------------------------------------------------------------ school / jobs
def school(x, by, s, w=330, h=230):
    w, h = w * s, h * s
    out = [townhouse(x, by, w, h, s, '#E86A4E', '#7A3B2A', side='r', floors=3, cols=6, seed=3, flowers=False, roof_kind='flat')]
    cx = x + w / 2
    top = by - h
    out.append(f'<rect x="{cx - 36 * s:.1f}" y="{top - 90 * s:.1f}" width="{72 * s:.1f}" height="{92 * s:.1f}" fill="#E86A4E" {g(s)}/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{top - 50 * s:.1f}" r="{22 * s:.1f}" fill="#FFFFFF" {g(s)}/>')
    out.append(f'<path d="M{cx:.1f} {top - 50 * s:.1f} L{cx:.1f} {top - 64 * s:.1f} M{cx:.1f} {top - 50 * s:.1f} L{cx + 10 * s:.1f} {top - 46 * s:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}" stroke-linecap="round"/>')
    out.append(f'<path d="M{cx - 46 * s:.1f} {top - 88 * s:.1f} L{cx:.1f} {top - 140 * s:.1f} L{cx + 46 * s:.1f} {top - 88 * s:.1f} Z" fill="#7A3B2A" {g(s)}/>')
    out.append(flagpole(cx + 2 * s, top - 140 * s, s * 0.8, ('#FFD23F', '#4FA3E3', '#FFD23F')))
    out.append(f'<rect x="{cx - 34 * s:.1f}" y="{by - 66 * s:.1f}" width="{68 * s:.1f}" height="{66 * s:.1f}" rx="{8 * s:.1f}" fill="#8A5326" {g(s)}/>')
    out.append(f'<rect x="{cx - 50 * s:.1f}" y="{by - 86 * s:.1f}" width="{100 * s:.1f}" height="{18 * s:.1f}" fill="#FFF3D6" {g(s, 0.8)}/>')
    return ''.join(out)


def bus(x, y, s, col='#FFC21A'):
    return (contact_shadow(x, y + 3 * s, 80 * s, 10 * s, 0.3) +
            f'<rect x="{x - 80 * s:.1f}" y="{y - 64 * s:.1f}" width="{160 * s:.1f}" height="{56 * s:.1f}" rx="{10 * s:.1f}" fill="{col}" {g(s)}/>'
            + ''.join(f'<rect x="{x - 70 * s + q * 26 * s:.1f}" y="{y - 56 * s:.1f}" width="{20 * s:.1f}" height="{18 * s:.1f}" rx="{3 * s:.1f}" fill="{PALETTE["window"]}" {g(s, 0.5)}/>' for q in range(6)) +
            f'<rect x="{x - 80 * s:.1f}" y="{y - 30 * s:.1f}" width="{160 * s:.1f}" height="{5 * s:.1f}" fill="#33333D" opacity="0.7"/>'
            f'<circle cx="{x - 50 * s:.1f}" cy="{y - 6 * s:.1f}" r="{11 * s:.1f}" fill="#33333D" {g(s, 0.6)}/><circle cx="{x + 50 * s:.1f}" cy="{y - 6 * s:.1f}" r="{11 * s:.1f}" fill="#33333D" {g(s, 0.6)}/>')


def slide(x, y, s):
    return (contact_shadow(x, y + 2 * s, 50 * s, 8 * s, 0.22) +
            f'<rect x="{x - 40 * s:.1f}" y="{y - 80 * s:.1f}" width="{8 * s:.1f}" height="{80 * s:.1f}" fill="#4FA3E3" {g(s, 0.7)}/>'
            f'<rect x="{x - 14 * s:.1f}" y="{y - 80 * s:.1f}" width="{8 * s:.1f}" height="{80 * s:.1f}" fill="#4FA3E3" {g(s, 0.7)}/>'
            + ''.join(f'<line x1="{x - 36 * s:.1f}" y1="{y - 20 * s - q * 16 * s:.1f}" x2="{x - 10 * s:.1f}" y2="{y - 20 * s - q * 16 * s:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}"/>' for q in range(4)) +
            f'<path d="M{x - 10 * s:.1f} {y - 80 * s:.1f} Q{x + 20 * s:.1f} {y - 70 * s:.1f} {x + 50 * s:.1f} {y - 4 * s:.1f} L{x + 62 * s:.1f} {y - 8 * s:.1f} Q{x + 30 * s:.1f} {y - 84 * s:.1f} {x - 8 * s:.1f} {y - 92 * s:.1f} Z" fill="#FF5E7E" {g(s)}/>')


def swing(x, y, s):
    return (f'<path d="M{x - 50 * s:.1f} {y:.1f} L{x - 36 * s:.1f} {y - 90 * s:.1f} L{x + 36 * s:.1f} {y - 90 * s:.1f} L{x + 50 * s:.1f} {y:.1f}" fill="none" stroke="#E5533D" stroke-width="{7 * s:.1f}" stroke-linejoin="round"/>'
            + ''.join(f'<line x1="{x + q * s - 8 * s:.1f}" y1="{y - 90 * s:.1f}" x2="{x + q * s - 8 * s:.1f}" y2="{y - 26 * s:.1f}" stroke="{OL}" stroke-width="{2.5 * s:.1f}"/><line x1="{x + q * s + 8 * s:.1f}" y1="{y - 90 * s:.1f}" x2="{x + q * s + 8 * s:.1f}" y2="{y - 26 * s:.1f}" stroke="{OL}" stroke-width="{2.5 * s:.1f}"/>'
                      f'<rect x="{x + q * s - 12 * s:.1f}" y="{y - 28 * s:.1f}" width="{24 * s:.1f}" height="{6 * s:.1f}" fill="#FFD23F" {g(s, 0.5)}/>' for q in (-18, 18)))


def crane(x, y, s):
    c = '#FFC21A'
    out = [contact_shadow(x, y + 3 * s, 40 * s, 8 * s, 0.25),
           f'<rect x="{x - 12 * s:.1f}" y="{y - 330 * s:.1f}" width="{24 * s:.1f}" height="{330 * s:.1f}" fill="{c}" {g(s)}/>']
    for q in range(11):
        yy = y - q * 30 * s
        out.append(f'<path d="M{x - 12 * s:.1f} {yy:.1f} L{x + 12 * s:.1f} {yy - 30 * s:.1f}" stroke="{OL}" stroke-width="{2 * s:.1f}"/>')
    out.append(f'<rect x="{x - 90 * s:.1f}" y="{y - 350 * s:.1f}" width="{260 * s:.1f}" height="{20 * s:.1f}" fill="{c}" {g(s)}/>')
    for q in range(13):
        xx = x - 90 * s + q * 20 * s
        out.append(f'<path d="M{xx:.1f} {y - 330 * s:.1f} L{xx + 20 * s:.1f} {y - 350 * s:.1f}" stroke="{OL}" stroke-width="{2 * s:.1f}"/>')
    out.append(f'<rect x="{x - 22 * s:.1f}" y="{y - 380 * s:.1f}" width="{40 * s:.1f}" height="{30 * s:.1f}" fill="#4FA3E3" {g(s)}/>')
    out.append(f'<rect x="{x - 96 * s:.1f}" y="{y - 344 * s:.1f}" width="{30 * s:.1f}" height="{30 * s:.1f}" fill="#8A8077" {g(s)}/>')
    out.append(f'<line x1="{x + 140 * s:.1f}" y1="{y - 330 * s:.1f}" x2="{x + 140 * s:.1f}" y2="{y - 200 * s:.1f}" stroke="{OL}" stroke-width="{2.5 * s:.1f}"/>')
    out.append(f'<rect x="{x + 116 * s:.1f}" y="{y - 200 * s:.1f}" width="{48 * s:.1f}" height="{18 * s:.1f}" fill="#E5533D" {g(s)}/>')
    return ''.join(out)


def site_building(x, by, s, w=200, h=180, side='r'):
    """unfinished building with scaffolding"""
    w, h = w * s, h * s
    b, dx, dy = box(x, by, w, h, s, '#C9C2B4', side, dep=w * 0.5)
    out = [b]
    for q in range(1, 4):
        yy = by - h * q / 4
        out.append(f'<line x1="{x - 10 * s:.1f}" y1="{yy:.1f}" x2="{x + w + 10 * s:.1f}" y2="{yy:.1f}" stroke="#FF9F2E" stroke-width="{5 * s:.1f}"/>')
    for q in range(5):
        xx = x + w * q / 4
        out.append(f'<line x1="{xx:.1f}" y1="{by:.1f}" x2="{xx:.1f}" y2="{by - h - 10 * s:.1f}" stroke="#FF9F2E" stroke-width="{5 * s:.1f}"/>')
    for q in range(3):
        out.append(f'<rect x="{x + w * (0.12 + q * 0.3):.1f}" y="{by - h * 0.7:.1f}" width="{w * 0.16:.1f}" height="{h * 0.2:.1f}" fill="#7E7769"/>')
    return ''.join(out)


def labelled_house(x, by, s, w, h, wall, roof, sign_col, sign_icon, side='r', garage=False):
    out = [townhouse(x, by, w * s, h * s, s, wall, roof, side=side, floors=2, cols=3, seed=int(x + by), flowers=False, roof_kind='flat' if garage else 'gable')]
    W_, H_ = w * s, h * s
    out.append(f'<rect x="{x + W_ * 0.2:.1f}" y="{by - H_ - 30 * s:.1f}" width="{W_ * 0.6:.1f}" height="{28 * s:.1f}" rx="{6 * s:.1f}" fill="{sign_col}" {g(s)}/>')
    cx, cy = x + W_ / 2, by - H_ - 16 * s
    if sign_icon == 'cross':
        out.append(f'<path d="M{cx - 4 * s:.1f} {cy - 10 * s:.1f} h{8 * s:.1f} v{6 * s:.1f} h{6 * s:.1f} v{8 * s:.1f} h{-6 * s:.1f} v{6 * s:.1f} h{-8 * s:.1f} v{-6 * s:.1f} h{-6 * s:.1f} v{-8 * s:.1f} h{6 * s:.1f} Z" fill="#E5533D"/>')
    elif sign_icon == 'bread':
        out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{16 * s:.1f}" ry="{8 * s:.1f}" fill="#E8A65A" {g(s, 0.5)}/>')
    elif sign_icon == 'flame':
        out.append(f'<path d="M{cx:.1f} {cy - 11 * s:.1f} Q{cx + 10 * s:.1f} {cy:.1f} {cx:.1f} {cy + 10 * s:.1f} Q{cx - 10 * s:.1f} {cy:.1f} {cx:.1f} {cy - 11 * s:.1f} Z" fill="#FFD23F"/>')
    elif sign_icon == 'mail':
        out.append(f'<rect x="{cx - 12 * s:.1f}" y="{cy - 8 * s:.1f}" width="{24 * s:.1f}" height="{16 * s:.1f}" fill="#FFFFFF" {g(s, 0.5)}/><path d="M{cx - 12 * s:.1f} {cy - 8 * s:.1f} L{cx:.1f} {cy + 2 * s:.1f} L{cx + 12 * s:.1f} {cy - 8 * s:.1f}" fill="none" {g(s, 0.5)}/>')
    if garage:
        for q in range(2):
            gx = x + W_ * (0.1 + q * 0.45)
            out.append(f'<rect x="{gx:.1f}" y="{by - H_ * 0.45:.1f}" width="{W_ * 0.38:.1f}" height="{H_ * 0.45:.1f}" fill="#F7EAD0" {g(s)}/>')
            for k in range(1, 5):
                out.append(f'<line x1="{gx:.1f}" y1="{by - H_ * 0.45 * k / 5:.1f}" x2="{gx + W_ * 0.38:.1f}" y2="{by - H_ * 0.45 * k / 5:.1f}" stroke="#C9B48E" stroke-width="{2 * s:.1f}"/>')
    return ''.join(out)


def truck(x, y, s, col='#E5533D', ladder=True):
    out = [contact_shadow(x, y + 3 * s, 70 * s, 9 * s, 0.3),
           f'<rect x="{x - 70 * s:.1f}" y="{y - 50 * s:.1f}" width="{100 * s:.1f}" height="{42 * s:.1f}" rx="{5 * s:.1f}" fill="{col}" {g(s)}/>',
           f'<path d="M{x + 30 * s:.1f} {y - 8 * s:.1f} L{x + 30 * s:.1f} {y - 56 * s:.1f} L{x + 56 * s:.1f} {y - 56 * s:.1f} L{x + 70 * s:.1f} {y - 34 * s:.1f} L{x + 70 * s:.1f} {y - 8 * s:.1f} Z" fill="{col}" {g(s)}/>',
           f'<path d="M{x + 36 * s:.1f} {y - 36 * s:.1f} L{x + 36 * s:.1f} {y - 50 * s:.1f} L{x + 54 * s:.1f} {y - 50 * s:.1f} L{x + 62 * s:.1f} {y - 36 * s:.1f} Z" fill="{PALETTE["window"]}"/>',
           f'<circle cx="{x - 44 * s:.1f}" cy="{y - 6 * s:.1f}" r="{11 * s:.1f}" fill="#33333D" {g(s, 0.6)}/><circle cx="{x + 46 * s:.1f}" cy="{y - 6 * s:.1f}" r="{11 * s:.1f}" fill="#33333D" {g(s, 0.6)}/>']
    if ladder:
        out.append(f'<rect x="{x - 66 * s:.1f}" y="{y - 64 * s:.1f}" width="{94 * s:.1f}" height="{10 * s:.1f}" fill="#E8E2D6" {g(s, 0.7)}/>')
        out.append(f'<rect x="{x + 34 * s:.1f}" y="{y - 64 * s:.1f}" width="{12 * s:.1f}" height="{8 * s:.1f}" fill="#4FA3E3" {g(s, 0.5)}/>')
    return ''.join(out)
