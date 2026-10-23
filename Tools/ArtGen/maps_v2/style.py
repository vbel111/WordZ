"""Word Z map art style sheet (v2) and shared drawing primitives.

Rules every map follows so the set reads as one family and matches the UI:
  * Palette: warm cream / wood browns from the UI + one category accent; skies are soft gradients.
  * Outline: chunky warm brown (#4A2410), width scales with depth (4-9 px at 1080 wide).
    Far layers drop the outline and fade into the sky colour (atmospheric depth).
  * Light comes from the upper left: every solid gets a lighter top/left highlight and a darker
    right side or bottom shadow, plus a soft contact shadow on the ground.
  * Composition (1080 x 2400, parallax background): ground and big props at the bottom, the scene
    recedes upwards to a horizon with the sky on top. The central column (x 300-780) is kept calm so the
    level path and nodes read clearly; the detail lives on the left and right edges.
"""
import math
import random

W, H = 1080, 2400
OL = '#4A2410'

PALETTE = {
    'cream': '#FBF1DE', 'cream2': '#F3E1C0', 'wood': '#A8642E', 'woodDark': '#7A4520',
    'gold': '#FFC93C', 'goldDark': '#E99A12', 'red': '#E5533D', 'redDark': '#B93A28',
    'green': '#6CC24A', 'greenDark': '#3E8E2F', 'greenLight': '#A6DE6A',
    'blue': '#4FA3E3', 'blueDark': '#2F78B8', 'sky1': '#7CC4F0', 'sky2': '#CFEBFA', 'skyWarm': '#FFE2A8',
    'window': '#9FD3F2', 'windowLit': '#FFD86B', 'shadow': '#2A1205',
}


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(a[i] + (b[i] - a[i]) * t):02X}' for i in range(3))


def shade(c, t):    # t<0 darker, t>0 lighter
    return mix(c, '#000000', -t) if t < 0 else mix(c, '#FFFFFF', t)


def svg(body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs}</defs>{body}</svg>')


def lin(id_, stops, x2=0, y2=1):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rad(id_, stops):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{id_}">{s}</radialGradient>'


# ---------------- generic props ----------------

def contact_shadow(x, y, rx, ry, o=0.22):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{PALETTE["shadow"]}" opacity="{o}"/>'


def cloud(x, y, s, o=1.0, tint='#FFFFFF'):
    """Chunky cartoon cloud: flat bottom, three puffs, soft blue under-shade."""
    under = mix(tint, '#9CC6E8', 0.55)
    puffs = [(-60, -8, 38), (-18, -34, 50), (36, -22, 42), (70, -4, 30)]
    body = ''.join(f'<circle cx="{x + dx * s:.1f}" cy="{y + dy * s:.1f}" r="{r * s:.1f}"/>' for dx, dy, r in puffs)
    base = f'<rect x="{x - 92 * s:.1f}" y="{y - 10 * s:.1f}" width="{184 * s:.1f}" height="{30 * s:.1f}" rx="{15 * s:.1f}"/>'
    shade_ = f'<rect x="{x - 88 * s:.1f}" y="{y + 4 * s:.1f}" width="{176 * s:.1f}" height="{16 * s:.1f}" rx="{8 * s:.1f}" fill="{under}"/>'
    hi = f'<ellipse cx="{x - 26 * s:.1f}" cy="{y - 52 * s:.1f}" rx="{20 * s:.1f}" ry="{9 * s:.1f}" fill="#FFFFFF" opacity="0.8"/>'
    return f'<g opacity="{o}"><g fill="{tint}">{body}{base}</g>{shade_}{hi}</g>'


def bird(x, y, s, c='#4A2410', o=0.7):
    return (f'<path d="M{x - 14 * s:.1f} {y:.1f} Q{x - 7 * s:.1f} {y - 8 * s:.1f} {x:.1f} {y:.1f} Q{x + 7 * s:.1f} {y - 8 * s:.1f} {x + 14 * s:.1f} {y:.1f}" '
            f'fill="none" stroke="{c}" stroke-width="{3 * s:.1f}" stroke-linecap="round" opacity="{o}"/>')


def round_tree(x, y, s, c='#6CC24A', sw=None):
    """Two-tone round tree with trunk, highlight blob and contact shadow. (x, y) = trunk base."""
    sw = sw if sw is not None else max(2.5, 5 * s)
    dark, light = shade(c, -0.22), shade(c, 0.3)
    return (contact_shadow(x + 6 * s, y + 2 * s, 46 * s, 11 * s) +
            f'<g stroke="{OL}" stroke-width="{sw:.1f}" stroke-linejoin="round">'
            f'<path d="M{x - 9 * s:.1f} {y:.1f} L{x - 6 * s:.1f} {y - 46 * s:.1f} L{x + 6 * s:.1f} {y - 46 * s:.1f} L{x + 9 * s:.1f} {y:.1f} Z" fill="#8A5326"/>'
            f'<circle cx="{x:.1f}" cy="{y - 86 * s:.1f}" r="{52 * s:.1f}" fill="{dark}"/>'
            f'</g>'
            f'<circle cx="{x - 6 * s:.1f}" cy="{y - 92 * s:.1f}" r="{44 * s:.1f}" fill="{c}"/>'
            f'<circle cx="{x - 22 * s:.1f}" cy="{y - 108 * s:.1f}" r="{18 * s:.1f}" fill="{light}"/>'
            f'<circle cx="{x + 22 * s:.1f}" cy="{y - 70 * s:.1f}" r="{5 * s:.1f}" fill="{dark}" opacity="0.6"/>'
            f'<circle cx="{x - 4 * s:.1f}" cy="{y - 62 * s:.1f}" r="{4 * s:.1f}" fill="{dark}" opacity="0.6"/>')


def bush(x, y, s, c='#5DB03E'):
    dark, light = shade(c, -0.2), shade(c, 0.3)
    sw = max(2.5, 4.5 * s)
    return (contact_shadow(x, y + 2 * s, 44 * s, 8 * s, 0.18) +
            f'<g stroke="{OL}" stroke-width="{sw:.1f}"><path d="M{x - 44 * s:.1f} {y:.1f} '
            f'A{22 * s:.1f} {22 * s:.1f} 0 0 1 {x - 14 * s:.1f} {y - 26 * s:.1f} A{26 * s:.1f} {26 * s:.1f} 0 0 1 {x + 22 * s:.1f} {y - 22 * s:.1f} '
            f'A{22 * s:.1f} {22 * s:.1f} 0 0 1 {x + 44 * s:.1f} {y:.1f} Z" fill="{dark}"/></g>'
            f'<path d="M{x - 38 * s:.1f} {y - 6 * s:.1f} A{18 * s:.1f} {18 * s:.1f} 0 0 1 {x - 12 * s:.1f} {y - 24 * s:.1f} '
            f'A{22 * s:.1f} {22 * s:.1f} 0 0 1 {x + 18 * s:.1f} {y - 20 * s:.1f} L{x + 10 * s:.1f} {y - 8 * s:.1f} Z" fill="{c}"/>'
            f'<ellipse cx="{x - 14 * s:.1f}" cy="{y - 22 * s:.1f}" rx="{9 * s:.1f}" ry="{5 * s:.1f}" fill="{light}"/>')


def flower(x, y, s, c='#FF7FA8'):
    petals = ''.join(f'<circle cx="{x + math.cos(a) * 7 * s:.1f}" cy="{y + math.sin(a) * 7 * s:.1f}" r="{5.5 * s:.1f}" fill="{c}"/>'
                     for a in [i * math.pi * 2 / 5 - math.pi / 2 for i in range(5)])
    return (f'<g stroke="{OL}" stroke-width="{max(1.5, 2 * s):.1f}">{petals}'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4 * s:.1f}" fill="#FFD23F"/></g>')


def grass_tuft(x, y, s, c='#4E9F36'):
    return (f'<path d="M{x - 10 * s:.1f} {y:.1f} Q{x - 8 * s:.1f} {y - 14 * s:.1f} {x - 12 * s:.1f} {y - 22 * s:.1f} Q{x - 2 * s:.1f} {y - 12 * s:.1f} {x:.1f} {y - 26 * s:.1f} '
            f'Q{x + 4 * s:.1f} {y - 12 * s:.1f} {x + 13 * s:.1f} {y - 20 * s:.1f} Q{x + 8 * s:.1f} {y - 10 * s:.1f} {x + 10 * s:.1f} {y:.1f} Z" fill="{c}"/>')


def lamp(x, y, s):
    sw = max(2, 4 * s)
    return (contact_shadow(x, y, 14 * s, 4 * s, 0.25) +
            f'<g stroke="{OL}" stroke-width="{sw:.1f}" stroke-linejoin="round">'
            f'<rect x="{x - 4 * s:.1f}" y="{y - 120 * s:.1f}" width="{8 * s:.1f}" height="{120 * s:.1f}" fill="#3C4A5C"/>'
            f'<rect x="{x - 10 * s:.1f}" y="{y - 10 * s:.1f}" width="{20 * s:.1f}" height="{10 * s:.1f}" fill="#3C4A5C"/>'
            f'<path d="M{x - 14 * s:.1f} {y - 120 * s:.1f} L{x + 14 * s:.1f} {y - 120 * s:.1f} L{x + 10 * s:.1f} {y - 146 * s:.1f} L{x - 10 * s:.1f} {y - 146 * s:.1f} Z" fill="#FFE9A6"/>'
            f'<path d="M{x - 16 * s:.1f} {y - 146 * s:.1f} L{x + 16 * s:.1f} {y - 146 * s:.1f} L{x:.1f} {y - 160 * s:.1f} Z" fill="#3C4A5C"/></g>'
            f'<circle cx="{x:.1f}" cy="{y - 133 * s:.1f}" r="{30 * s:.1f}" fill="#FFE9A6" opacity="0.25"/>')


def bench(x, y, s):
    sw = max(2, 4 * s)
    return (contact_shadow(x, y + 2 * s, 46 * s, 7 * s, 0.2) +
            f'<g stroke="{OL}" stroke-width="{sw:.1f}" stroke-linejoin="round">'
            f'<rect x="{x - 38 * s:.1f}" y="{y - 22 * s:.1f}" width="{6 * s:.1f}" height="{22 * s:.1f}" fill="#3C4A5C"/>'
            f'<rect x="{x + 32 * s:.1f}" y="{y - 22 * s:.1f}" width="{6 * s:.1f}" height="{22 * s:.1f}" fill="#3C4A5C"/>'
            f'<rect x="{x - 44 * s:.1f}" y="{y - 30 * s:.1f}" width="{88 * s:.1f}" height="{10 * s:.1f}" rx="{3 * s:.1f}" fill="{PALETTE["wood"]}"/>'
            f'<rect x="{x - 44 * s:.1f}" y="{y - 52 * s:.1f}" width="{88 * s:.1f}" height="{10 * s:.1f}" rx="{3 * s:.1f}" fill="{PALETTE["wood"]}"/></g>')


def car(x, y, s, c='#E5533D'):
    sw = max(2, 4 * s)
    dark = shade(c, -0.25)
    return (contact_shadow(x, y + 3 * s, 46 * s, 8 * s, 0.3) +
            f'<g stroke="{OL}" stroke-width="{sw:.1f}" stroke-linejoin="round">'
            f'<path d="M{x - 44 * s:.1f} {y - 6 * s:.1f} L{x - 44 * s:.1f} {y - 26 * s:.1f} Q{x - 40 * s:.1f} {y - 34 * s:.1f} {x - 28 * s:.1f} {y - 34 * s:.1f} '
            f'L{x - 20 * s:.1f} {y - 52 * s:.1f} L{x + 22 * s:.1f} {y - 52 * s:.1f} L{x + 32 * s:.1f} {y - 34 * s:.1f} Q{x + 44 * s:.1f} {y - 34 * s:.1f} {x + 44 * s:.1f} {y - 24 * s:.1f} '
            f'L{x + 44 * s:.1f} {y - 6 * s:.1f} Z" fill="{c}"/>'
            f'<path d="M{x - 14 * s:.1f} {y - 36 * s:.1f} L{x - 9 * s:.1f} {y - 46 * s:.1f} L{x + 17 * s:.1f} {y - 46 * s:.1f} L{x + 23 * s:.1f} {y - 36 * s:.1f} Z" fill="{PALETTE["window"]}"/>'
            f'<circle cx="{x - 26 * s:.1f}" cy="{y - 4 * s:.1f}" r="{9 * s:.1f}" fill="#33333D"/>'
            f'<circle cx="{x + 26 * s:.1f}" cy="{y - 4 * s:.1f}" r="{9 * s:.1f}" fill="#33333D"/></g>'
            f'<rect x="{x - 40 * s:.1f}" y="{y - 18 * s:.1f}" width="{80 * s:.1f}" height="{5 * s:.1f}" fill="{dark}" opacity="0.6"/>'
            f'<rect x="{x - 36 * s:.1f}" y="{y - 31 * s:.1f}" width="{20 * s:.1f}" height="{4 * s:.1f}" rx="{2 * s:.1f}" fill="#FFFFFF" opacity="0.55"/>')


def rng(seed):
    return random.Random(seed)
