"""Prop library for the v2 maps. Every prop is drawn in local units with its base at (0, 0) and placed
with T(x, y, s): stroke widths scale with depth, so far props get thinner outlines automatically.
Light from the upper left: highlight on the left/top, darker tone on the right/bottom."""
import math

from style import OL, PALETTE as P, mix, shade

SH = '#2A1205'


def T(x, y, s, body, flip=False, sw=5):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({-s if flip else s:.3f},{s:.3f})" stroke="{OL}" stroke-width="{sw}" '
            f'stroke-linejoin="round" stroke-linecap="round">{body}</g>')


def shadow(rx, ry=None, o=0.22, dx=6):
    ry = ry if ry is not None else rx * 0.22
    return f'<ellipse cx="{dx}" cy="2" rx="{rx}" ry="{ry}" fill="{SH}" opacity="{o}" stroke="none"/>'


def hi(x, y, rx, ry, o=0.45, c='#FFFFFF'):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity="{o}" stroke="none"/>'


# ---------------- plants ----------------

def pine(x, y, s, c='#3E9A4A'):
    d, l = shade(c, -0.22), shade(c, 0.25)
    b = (shadow(40) + '<rect x="-8" y="-30" width="16" height="32" fill="#7A4520"/>' +
         ''.join(f'<path d="M0 {-60 - k * 44} L{52 - k * 9} {-24 - k * 44} L{-52 + k * 9} {-24 - k * 44} Z" fill="{c}"/>'
                 f'<path d="M0 {-60 - k * 44} L{52 - k * 9} {-24 - k * 44} L{14 - k * 3} {-24 - k * 44} Z" fill="{d}" stroke="none"/>' for k in range(3)) +
         f'<path d="M-6 -150 L-26 -118" stroke="{l}" stroke-width="6" opacity="0.8"/>')
    return T(x, y, s, b)


def palm(x, y, s, c='#4FB548'):
    d = shade(c, -0.22)
    leaves = ''
    for a in (-160, -125, -90, -55, -20):
        r = math.radians(a)
        ex, ey = math.cos(r) * 90, -150 + math.sin(r) * 60 + 30
        leaves += f'<path d="M0 -150 Q{ex * 0.5:.0f} {-190 + (ey + 150) * 0.2:.0f} {ex:.0f} {ey:.0f} Q{ex * 0.45:.0f} {-160:.0f} 0 -150 Z" fill="{c if a < -80 else d}"/>'
    b = (shadow(40) + '<path d="M-10 0 Q-4 -80 6 -150 L16 -148 Q8 -80 10 0 Z" fill="#B8783C"/>' +
         ''.join(f'<path d="M{-8 + k * 1.2:.0f} {-20 - k * 26} l18 -4" stroke-width="3"/>' for k in range(5)) + leaves +
         '<circle cx="2" cy="-146" r="9" fill="#7A4520"/><circle cx="14" cy="-142" r="8" fill="#7A4520"/>')
    return T(x, y, s, b)


def acacia(x, y, s, c='#7FB53A'):
    b = (shadow(70) + '<path d="M-8 0 L-4 -70 L-40 -110 M-4 -70 L30 -116 M-4 -70 L0 -120" stroke-width="12" fill="none"/>'
         '<path d="M-8 0 L-4 -70 L-40 -110 M-4 -70 L30 -116" stroke="#8A5326" stroke-width="6" fill="none"/>'
         f'<path d="M-110 -110 Q-90 -150 -20 -152 Q60 -160 110 -124 Q80 -104 0 -108 Q-70 -100 -110 -110 Z" fill="{c}"/>'
         f'<path d="M-90 -128 Q-40 -146 20 -144" stroke="{shade(c, 0.3)}" stroke-width="8" fill="none"/>')
    return T(x, y, s, b)


def apple_tree(x, y, s, c='#5DB03E', fruit='#E5533D'):
    d, l = shade(c, -0.22), shade(c, 0.3)
    dots = ''.join(f'<circle cx="{fx}" cy="{fy}" r="8" fill="{fruit}" stroke-width="3"/>' for fx, fy in
                   [(-30, -90), (20, -110), (34, -70), (-10, -130), (-40, -60), (6, -80)])
    b = (shadow(50) + '<path d="M-10 0 L-6 -50 L6 -50 L10 0 Z" fill="#8A5326"/>'
         f'<circle cx="0" cy="-90" r="58" fill="{d}"/>' f'<circle cx="-6" cy="-96" r="49" fill="{c}" stroke="none"/>'
         + hi(-24, -116, 18, 11, 0.5, l) + dots)
    return T(x, y, s, b)


def mushroom(x, y, s, c='#E5533D'):
    b = (shadow(26) + '<path d="M-10 0 Q-12 -20 -8 -30 L8 -30 Q12 -20 10 0 Z" fill="#FBF1DE"/>'
         f'<path d="M-34 -28 Q-34 -70 0 -70 Q34 -70 34 -28 Z" fill="{c}"/>'
         '<circle cx="-14" cy="-50" r="7" fill="#FFFFFF" stroke="none"/><circle cx="12" cy="-44" r="5" fill="#FFFFFF" stroke="none"/>'
         '<circle cx="4" cy="-60" r="4" fill="#FFFFFF" stroke="none"/>')
    return T(x, y, s, b)


def rock(x, y, s, c='#B4ADA3'):
    b = (shadow(44) + f'<path d="M-44 0 Q-46 -30 -18 -42 Q14 -54 38 -30 Q50 -14 44 0 Z" fill="{c}"/>'
         f'<path d="M10 -46 Q40 -36 44 0 L18 0 Q22 -24 10 -46 Z" fill="{shade(c, -0.18)}" stroke="none"/>' + hi(-18, -30, 12, 6, 0.4))
    return T(x, y, s, b)


def log(x, y, s):
    b = (shadow(54) + '<rect x="-54" y="-30" width="96" height="30" rx="14" fill="#9A5B27"/>'
         '<ellipse cx="44" cy="-15" rx="12" ry="15" fill="#E9C48A"/><ellipse cx="44" cy="-15" rx="5" ry="7" fill="none" stroke-width="3"/>')
    return T(x, y, s, b)


def reed(x, y, s, c='#4E9F36'):
    return T(x, y, s, ''.join(f'<path d="M{dx} 0 Q{dx - 4} -40 {dx + lean} -{h}" fill="none" stroke="{c}" stroke-width="6"/>'
                              for dx, lean, h in [(-8, -10, 70), (0, 4, 90), (8, 12, 64)]) +
             '<rect x="-3" y="-96" width="8" height="26" rx="4" fill="#8A5326"/>')


# ---------------- built things ----------------

def fence(x, y, s, n=3, c='#E9C48A'):
    b = shadow(26 * n, 6)
    for k in range(n):
        px = -26 * n + k * 52 + 26
        b += f'<path d="M{px - 8} 0 L{px - 8} -50 L{px} -60 L{px + 8} -50 L{px + 8} 0 Z" fill="{c}"/>'
    b += f'<rect x="{-26 * n}" y="-42" width="{52 * n}" height="10" fill="{shade(c, -0.1)}"/><rect x="{-26 * n}" y="-20" width="{52 * n}" height="10" fill="{shade(c, -0.1)}"/>'
    return T(x, y, s, b)


def signpost(x, y, s, texts=('', ''), colors=('#E99A12', '#4FA3E3')):
    b = shadow(20) + '<rect x="-6" y="-130" width="12" height="130" fill="#8A5326"/>'
    for k, c in enumerate(colors):
        yy = -124 + k * 40
        dirn = 1 if k % 2 == 0 else -1
        b += (f'<path d="M{-40 * dirn} {yy} L{50 * dirn} {yy} L{66 * dirn} {yy + 14} L{50 * dirn} {yy + 28} L{-40 * dirn} {yy + 28} Z" fill="{c}"/>'
              f'<rect x="{min(-30 * dirn, 36 * dirn)}" y="{yy + 11}" width="66" height="6" rx="3" fill="#FFFFFF" opacity="0.7" stroke="none"/>')
    return T(x, y, s, b)


def flagpole(x, y, s, c='#E5533D'):
    b = (shadow(16) + '<rect x="-4" y="-170" width="8" height="170" fill="#D8D8D8"/><circle cx="0" cy="-174" r="7" fill="#FFC93C"/>'
         f'<path d="M4 -166 Q30 -176 56 -164 Q80 -152 96 -160 L96 -114 Q80 -106 56 -118 Q30 -130 4 -120 Z" fill="{c}"/>'
         f'<path d="M4 -140 Q30 -150 56 -138 Q80 -126 96 -134" stroke="{shade(c, 0.35)}" stroke-width="5" fill="none" opacity="0.7"/>')
    return T(x, y, s, b)


def bunting(x0, y0, x1, y1, s, colors=('#E5533D', '#FFC93C', '#4FA3E3', '#6CC24A', '#C58BF2')):
    n = max(4, int(abs(x1 - x0) / (40 * s)))
    sag = 40 * s
    out = f'<path d="M{x0:.1f} {y0:.1f} Q{(x0 + x1) / 2:.1f} {(y0 + y1) / 2 + sag * 2:.1f} {x1:.1f} {y1:.1f}" stroke="{OL}" stroke-width="{3 * s:.1f}" fill="none"/>'
    for k in range(n):
        u = (k + 0.5) / n
        px = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * (x0 + x1) / 2 + u * u * x1
        py = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * ((y0 + y1) / 2 + sag * 2) + u * u * y1
        out += (f'<path d="M{px - 14 * s:.1f} {py:.1f} L{px + 14 * s:.1f} {py:.1f} L{px:.1f} {py + 30 * s:.1f} Z" fill="{colors[k % len(colors)]}" '
                f'stroke="{OL}" stroke-width="{2.5 * s:.1f}" stroke-linejoin="round"/>')
    return out


def stall(x, y, s, awning='#E5533D', goods=('#E5533D', '#FFC93C', '#6CC24A')):
    b = shadow(90)
    b += '<rect x="-80" y="-60" width="160" height="60" fill="#C9874A"/><rect x="-80" y="-60" width="160" height="12" fill="#E9C48A"/>'
    b += '<rect x="-76" y="-170" width="10" height="112" fill="#8A5326"/><rect x="66" y="-170" width="10" height="112" fill="#8A5326"/>'
    for k in range(6):
        xa = -92 + k * 184 / 6
        b += (f'<path d="M{xa:.0f} -190 h{184 / 6:.1f} v40 q{-92 / 6:.1f} 16 {-184 / 6:.1f} 0 Z" fill="{awning if k % 2 == 0 else "#FFFFFF"}"/>')
    b += f'<path d="M-96 -190 L0 -226 L96 -190 Z" fill="{shade(awning, -0.1)}"/>'
    for k in range(9):
        gx = -64 + k * 16
        b += f'<circle cx="{gx}" cy="{-68 - (k % 2) * 8}" r="10" fill="{goods[k % len(goods)]}" stroke-width="3"/>'
    return T(x, y, s, b)


def parasol_table(x, y, s, c='#E5533D'):
    b = (shadow(60) + '<rect x="-46" y="-50" width="92" height="10" rx="4" fill="#FBF1DE"/>'
         '<rect x="-36" y="-40" width="6" height="40" fill="#8A5326"/><rect x="30" y="-40" width="6" height="40" fill="#8A5326"/>'
         '<rect x="-3" y="-160" width="6" height="112" fill="#8A5326"/>')
    for k in range(6):
        a0, a1 = math.pi + k * math.pi / 6, math.pi + (k + 1) * math.pi / 6
        b += (f'<path d="M0 -168 L{math.cos(a0) * 84:.0f} {-130 + math.sin(a0) * -6:.0f} L{math.cos(a1) * 84:.0f} {-130 + math.sin(a1) * -6:.0f} Z" '
              f'fill="{c if k % 2 == 0 else "#FFFFFF"}"/>')
    b += f'<path d="M-84 -130 Q0 -116 84 -130" fill="none"/>'
    return T(x, y, s, b)


def house(x, y, s, wall='#FBE6C4', roof='#E5533D', flip=False):
    b = (shadow(80) + f'<path d="M50 -96 L86 -110 L86 -10 L50 0 Z" fill="{shade(wall, -0.2)}"/>'
         f'<rect x="-60" y="-96" width="110" height="96" fill="{wall}"/>'
         f'<path d="M-72 -92 L-4 -160 L64 -92 Z" fill="{roof}"/><path d="M-4 -160 L66 -174 L100 -108 L64 -92 Z" fill="{shade(roof, -0.2)}"/>'
         '<rect x="-18" y="-50" width="28" height="50" rx="4" fill="#9A5B27"/>'
         f'<rect x="-50" y="-76" width="24" height="24" rx="3" fill="{P["window"]}"/><rect x="20" y="-76" width="24" height="24" rx="3" fill="{P["windowLit"]}"/>'
         '<rect x="28" y="-180" width="16" height="34" fill="#C9874A"/>')
    return T(x, y, s, b, flip)


def barn(x, y, s, flip=False):
    b = (shadow(110) + '<path d="M80 -120 L120 -134 L120 -14 L80 0 Z" fill="#9C3324"/>'
         '<rect x="-90" y="-120" width="170" height="120" fill="#D2412D"/>'
         '<path d="M-104 -114 L-60 -190 L36 -190 L94 -114 Z" fill="#7A4520"/><path d="M36 -190 L84 -206 L130 -128 L94 -114 Z" fill="#5E3416"/>'
         '<rect x="-36" y="-80" width="64" height="80" fill="#FBF1DE"/><path d="M-36 -80 L28 0 M28 -80 L-36 0" stroke-width="6"/>'
         '<rect x="-20" y="-160" width="32" height="28" fill="#FBF1DE"/>'
         '<rect x="-90" y="-120" width="12" height="120" fill="#FFFFFF" opacity="0.18" stroke="none"/>')
    return T(x, y, s, b, flip)


def windmill(x, y, s, sail='#FBF1DE'):
    b = (shadow(40) + '<path d="M-34 0 L-20 -150 L20 -150 L34 0 Z" fill="#FBE6C4"/>'
         '<path d="M6 -150 L20 -150 L34 0 L14 0 Z" fill="#E7CDA2" stroke="none"/>'
         '<path d="M-30 -150 Q0 -190 30 -150 Z" fill="#E5533D"/><rect x="-10" y="-40" width="20" height="40" rx="8" fill="#9A5B27"/>')
    for a in (20, 110, 200, 290):
        r = math.radians(a)
        cx, cy = math.cos(r), math.sin(r)
        px, py = -cy, cx
        b += (f'<path d="M{cx * 16:.0f} {-150 + cy * 16:.0f} L{cx * 110:.0f} {-150 + cy * 110:.0f} L{cx * 110 + px * 26:.0f} {-150 + cy * 110 + py * 26:.0f} '
              f'L{cx * 30 + px * 26:.0f} {-150 + cy * 30 + py * 26:.0f} Z" fill="{sail}"/>')
    b += '<circle cx="0" cy="-150" r="10" fill="#7A4520"/>'
    return T(x, y, s, b)


def haystack(x, y, s):
    b = (shadow(54) + '<path d="M-54 0 Q-60 -80 0 -86 Q60 -80 54 0 Z" fill="#F2C14E"/>'
         '<path d="M10 -84 Q56 -76 54 0 L24 0 Q30 -50 10 -84 Z" fill="#D9A23A" stroke="none"/>'
         '<path d="M-30 -50 l10 -14 M-6 -64 l8 -12 M20 -40 l10 -12 M-20 -20 l8 -12" stroke-width="3"/>')
    return T(x, y, s, b)


def sheep(x, y, s, flip=False):
    wool = ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF"/>' for cx, cy, r in
                   [(-28, -40, 20), (-6, -50, 22), (18, -44, 20), (-18, -26, 18), (12, -26, 18)])
    b = (shadow(40) + '<rect x="-24" y="-24" width="8" height="24" fill="#3A3A44"/><rect x="12" y="-24" width="8" height="24" fill="#3A3A44"/>'
         + wool + '<ellipse cx="36" cy="-44" rx="16" ry="18" fill="#3A3A44"/><circle cx="40" cy="-48" r="3.5" fill="#FFFFFF" stroke="none"/>'
         '<ellipse cx="24" cy="-54" rx="9" ry="5" fill="#3A3A44"/>' + hi(-12, -60, 10, 5, 0.6, '#FFFFFF'))
    return T(x, y, s, b, flip)


def chick(x, y, s, flip=False):
    b = (shadow(20) + '<path d="M-6 0 l0 -10 M6 0 l0 -10" stroke="#E99A12" stroke-width="5"/>'
         '<ellipse cx="0" cy="-28" rx="22" ry="20" fill="#FFD84A"/><circle cx="12" cy="-48" r="13" fill="#FFD84A"/>'
         '<path d="M24 -50 l12 4 l-12 4 Z" fill="#F08A24"/><circle cx="16" cy="-51" r="2.5" fill="#4A2410" stroke="none"/>'
         '<path d="M-10 -32 q10 -10 18 0" fill="none" stroke-width="3"/>')
    return T(x, y, s, b, flip)


def cow(x, y, s, flip=False):
    b = (shadow(60) + ''.join(f'<rect x="{lx}" y="-34" width="12" height="34" fill="#FFFFFF"/>' for lx in (-44, -24, 22, 38)) +
         '<rect x="-54" y="-90" width="110" height="60" rx="26" fill="#FFFFFF"/>'
         '<path d="M-30 -88 q20 6 10 30 q-24 4 -30 -16 Z" fill="#3A3A44" stroke="none"/><circle cx="20" cy="-60" r="12" fill="#3A3A44" stroke="none"/>'
         '<rect x="44" y="-110" width="44" height="46" rx="18" fill="#FFFFFF"/><ellipse cx="72" cy="-70" rx="22" ry="14" fill="#FFB4C0"/>'
         '<path d="M50 -110 l-8 -14 M80 -110 l8 -14" stroke-width="6"/><circle cx="58" cy="-94" r="3.5" fill="#4A2410" stroke="none"/>')
    return T(x, y, s, b, flip)


def pumpkin(x, y, s):
    b = (shadow(34) + '<ellipse cx="-14" cy="-26" rx="20" ry="26" fill="#F08A24"/><ellipse cx="14" cy="-26" rx="20" ry="26" fill="#F08A24"/>'
         '<ellipse cx="0" cy="-26" rx="18" ry="27" fill="#FFA43A"/><path d="M0 -52 q4 -14 12 -16" stroke="#3E8E2F" stroke-width="6" fill="none"/>')
    return T(x, y, s, b)


def cabbage(x, y, s, c='#7FCB5A'):
    b = (shadow(26) + f'<circle cx="0" cy="-20" r="22" fill="{shade(c, -0.15)}"/><path d="M-18 -16 Q0 -44 18 -16 Q0 -6 -18 -16 Z" fill="{c}"/>'
         + hi(-6, -30, 6, 4, 0.5))
    return T(x, y, s, b)


def carrot_patch(x, y, s):
    b = shadow(40, 8)
    for dx in (-30, 0, 30):
        b += (f'<path d="M{dx - 8} -6 L{dx} 14 L{dx + 8} -6 Z" fill="#F08A24"/>'
              f'<path d="M{dx} -6 q-12 -24 -6 -34 M{dx} -6 q2 -26 8 -36 M{dx} -6 q12 -20 16 -28" stroke="#3E8E2F" stroke-width="6" fill="none"/>')
    b += '<ellipse cx="0" cy="0" rx="48" ry="9" fill="#8A5326" stroke="none" opacity="0.6"/>'
    return T(x, y, s, b)


def scarecrow(x, y, s):
    b = (shadow(30) + '<rect x="-4" y="-150" width="8" height="150" fill="#8A5326"/><rect x="-60" y="-118" width="120" height="8" fill="#8A5326"/>'
         '<path d="M-36 -120 L36 -120 L30 -60 L-30 -60 Z" fill="#4FA3E3"/><rect x="-22" y="-100" width="12" height="12" fill="#E5533D"/>'
         '<circle cx="0" cy="-138" r="18" fill="#F2C14E"/><path d="M-30 -150 L30 -150 L16 -162 L0 -184 L-16 -162 Z" fill="#9A5B27"/>'
         '<path d="M-60 -114 l-10 10 M60 -114 l10 10" stroke="#F2C14E" stroke-width="5"/>')
    return T(x, y, s, b)


def crate(x, y, s, fruit='#E5533D'):
    b = (shadow(40) + '<rect x="-40" y="-44" width="80" height="44" fill="#C9874A"/><path d="M-40 -22 h80" stroke-width="4"/>'
         + ''.join(f'<circle cx="{-28 + k * 14}" cy="-48" r="9" fill="{fruit}" stroke-width="3"/>' for k in range(5)) +
         '<rect x="-40" y="-44" width="8" height="44" fill="#FFFFFF" opacity="0.2" stroke="none"/>')
    return T(x, y, s, b)


def lamp(x, y, s, glow='#FFE9A6'):
    b = (shadow(14, 4, 0.25, 0) + '<rect x="-4" y="-120" width="8" height="120" fill="#3C4A5C"/><rect x="-10" y="-10" width="20" height="10" fill="#3C4A5C"/>'
         f'<path d="M-14 -120 L14 -120 L10 -146 L-10 -146 Z" fill="{glow}"/><path d="M-16 -146 L16 -146 L0 -160 Z" fill="#3C4A5C"/>'
         f'<circle cx="0" cy="-133" r="30" fill="{glow}" opacity="0.25" stroke="none"/>')
    return T(x, y, s, b)


def bench(x, y, s):
    b = (shadow(46, 7, 0.2, 0) + '<rect x="-38" y="-22" width="6" height="22" fill="#3C4A5C"/><rect x="32" y="-22" width="6" height="22" fill="#3C4A5C"/>'
         '<rect x="-44" y="-30" width="88" height="10" rx="3" fill="#A8642E"/><rect x="-44" y="-52" width="88" height="10" rx="3" fill="#A8642E"/>')
    return T(x, y, s, b)


def cone(x, y, s):
    b = (shadow(22) + '<rect x="-22" y="-8" width="44" height="8" rx="2" fill="#F08A24"/><path d="M-14 -8 L-4 -56 L4 -56 L14 -8 Z" fill="#F08A24"/>'
         '<path d="M-10 -26 L10 -26 L8 -36 L-8 -36 Z" fill="#FFFFFF" stroke="none"/>')
    return T(x, y, s, b)


def balloon(x, y, s, c1='#E5533D', c2='#FFC93C'):
    b = (f'<path d="M-50 -120 Q-56 -190 0 -192 Q56 -190 50 -120 Q40 -80 14 -60 L-14 -60 Q-40 -80 -50 -120 Z" fill="{c1}"/>'
         f'<path d="M-16 -190 Q-30 -130 -8 -62 L8 -62 Q30 -130 16 -190 Q0 -194 -16 -190 Z" fill="{c2}"/>'
         '<path d="M-14 -60 L-12 -30 M14 -60 L12 -30" stroke-width="3"/><rect x="-16" y="-32" width="32" height="26" rx="4" fill="#A8642E"/>'
         + hi(-28, -160, 10, 18, 0.35))
    return T(x, y, s, b)


def plane(x, y, s, c='#FFFFFF', flip=False):
    b = ('<path d="M-90 -8 Q-90 -24 -60 -24 L60 -24 Q92 -22 100 -10 Q92 2 60 4 L-60 4 Q-90 4 -90 -8 Z" fill="' + c + '"/>'
         '<path d="M-10 -10 L-40 34 L-14 34 L30 -8 Z" fill="#4FA3E3"/><path d="M-70 -22 L-92 -56 L-72 -56 L-50 -24 Z" fill="#E5533D"/>'
         + ''.join(f'<circle cx="{-40 + k * 18}" cy="-12" r="5" fill="#9FD3F2" stroke-width="2.5"/>' for k in range(6)))
    return T(x, y, s, b, flip)


def suitcase(x, y, s, c='#E5533D'):
    b = (shadow(40) + '<rect x="-16" y="-96" width="32" height="20" rx="6" fill="none" stroke-width="7"/>'
         f'<rect x="-40" y="-82" width="80" height="82" rx="10" fill="{c}"/><rect x="-40" y="-56" width="80" height="8" fill="{shade(c, -0.2)}" stroke="none"/>'
         '<circle cx="-18" cy="-24" r="10" fill="#FFC93C" stroke-width="3"/><rect x="6" y="-34" width="22" height="16" rx="3" fill="#FFFFFF" stroke-width="3"/>'
         + hi(-26, -70, 6, 4, 0.5))
    return T(x, y, s, b)


def umbrella(x, y, s, c='#E5533D'):
    b = '<path d="M0 -120 L0 -10 q0 12 -12 12" fill="none" stroke-width="6"/>'
    for k in range(4):
        a0 = -180 + k * 45
        x0, x1 = math.cos(math.radians(a0)) * 70, math.cos(math.radians(a0 + 45)) * 70
        y0, y1 = math.sin(math.radians(a0)) * 50, math.sin(math.radians(a0 + 45)) * 50
        b += f'<path d="M0 -120 L{x0:.0f} {-110 + y0 * -0.6:.0f} Q{(x0 + x1) / 2:.0f} {-104:.0f} {x1:.0f} {-110 + y1 * -0.6:.0f} Z" fill="{c if k % 2 == 0 else "#FFFFFF"}"/>'
    b = f'<g transform="translate(0,-40)">{b}</g>'
    return T(x, y, s, b)


def puddle(x, y, s):
    b = ('<ellipse cx="0" cy="0" rx="60" ry="16" fill="#8CCBEF" stroke-width="4"/>'
         '<path d="M-36 -2 q14 -6 28 0" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.8"/>')
    return T(x, y, s, b)


def snowman(x, y, s):
    b = (shadow(40) + '<circle cx="0" cy="-36" r="38" fill="#FFFFFF"/><circle cx="0" cy="-100" r="28" fill="#FFFFFF"/>'
         '<path d="M2 -98 l26 6 l-26 4 Z" fill="#F08A24" stroke-width="3"/><circle cx="-8" cy="-108" r="3.5" fill="#4A2410" stroke="none"/>'
         '<circle cx="10" cy="-110" r="3.5" fill="#4A2410" stroke="none"/><path d="M-26 -78 Q0 -66 26 -78 L26 -70 Q0 -58 -26 -70 Z" fill="#E5533D"/>'
         '<rect x="-24" y="-148" width="48" height="26" fill="#3A3A44"/><rect x="-32" y="-126" width="64" height="8" fill="#3A3A44"/>'
         + hi(-14, -50, 10, 14, 0.25, '#9CC6E8'))
    return T(x, y, s, b)


def weathervane(x, y, s):
    b = (shadow(16) + '<rect x="-4" y="-170" width="8" height="170" fill="#7A4520"/>'
         '<path d="M-60 -150 L50 -150 M-40 -150 l-20 -14 l0 28 Z" fill="#E99A12"/><path d="M50 -150 l-16 -12 l0 24 Z" fill="#E99A12"/>'
         '<path d="M-10 -180 q4 -18 18 -14 q10 4 6 14 Z" fill="#E99A12"/>'
         '<circle cx="0" cy="-150" r="6" fill="#FFC93C"/>')
    return T(x, y, s, b)


def sign_board(x, y, s, c='#FFC93C', text=''):
    b = (shadow(40) + '<rect x="-40" y="-90" width="10" height="90" fill="#8A5326"/><rect x="30" y="-90" width="10" height="90" fill="#8A5326"/>'
         f'<rect x="-64" y="-150" width="128" height="70" rx="12" fill="{c}"/><rect x="-54" y="-140" width="118" height="10" rx="5" fill="#FFFFFF" opacity="0.35" stroke="none"/>')
    if text:
        b += f'<text x="0" y="-104" font-family="Arial Black,Arial" font-weight="900" font-size="30" text-anchor="middle" fill="#FFFFFF" stroke="{OL}" stroke-width="2">{text}</text>'
    return T(x, y, s, b)
