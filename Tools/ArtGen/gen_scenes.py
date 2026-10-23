"""Word Z scenes: logo, leaf corner, home background, skyline, app icon and 20 category map backgrounds."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen_icons import BODIES, DEFS, OL, svg  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), 'svg')


def write(name, w, h, body, defs=None):
    open(os.path.join(OUT, name + '.svg'), 'w').write(svg(w, h, body, defs or DEFS))


def prop(name, x, y, size, rot=0, opacity=1.0, sw=7):
    """Places one of the icon bodies as scenery."""
    s = size / 256.0
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f}) scale({s:.3f}) translate(-128,-128)" '
            f'opacity="{opacity}" stroke="{OL}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">{BODIES[name]}</g>')


# ---------------- scenery primitives (drawn in place) ----------------

def tree(x, y, s, c1='#5DBB45', c2='#3E8E2F'):
    return (f'<g stroke="{OL}" stroke-width="{4*s:.1f}"><rect x="{x-7*s}" y="{y-20*s}" width="{14*s}" height="{30*s}" rx="{3*s}" fill="#8A5326"/>'
            f'<circle cx="{x}" cy="{y-42*s}" r="{30*s}" fill="{c1}"/><circle cx="{x-20*s}" cy="{y-26*s}" r="{18*s}" fill="{c2}"/>'
            f'<circle cx="{x+20*s}" cy="{y-26*s}" r="{18*s}" fill="{c2}"/>'
            f'<ellipse cx="{x-10*s}" cy="{y-56*s}" rx="{9*s}" ry="{5*s}" fill="#fff" fill-opacity="0.35" stroke="none"/></g>')


def pine(x, y, s, c='#2F8A4A'):
    return (f'<g stroke="{OL}" stroke-width="{4*s:.1f}" stroke-linejoin="round"><rect x="{x-6*s}" y="{y-14*s}" width="{12*s}" height="{20*s}" fill="#7A4520"/>'
            f'<path d="M{x} {y-90*s} L{x+34*s} {y-14*s} L{x-34*s} {y-14*s} Z" fill="{c}"/>'
            f'<path d="M{x} {y-110*s} L{x+26*s} {y-50*s} L{x-26*s} {y-50*s} Z" fill="{c}"/></g>')


def bush(x, y, s, c='#4FA83A'):
    return (f'<g stroke="{OL}" stroke-width="{4*s:.1f}"><circle cx="{x-16*s}" cy="{y}" r="{16*s}" fill="{c}"/>'
            f'<circle cx="{x+16*s}" cy="{y}" r="{16*s}" fill="{c}"/><circle cx="{x}" cy="{y-12*s}" r="{20*s}" fill="{c}"/></g>')


def rock(x, y, s, c='#A9A39A'):
    return (f'<path d="M{x-30*s} {y} Q{x-28*s} {y-26*s} {x-6*s} {y-30*s} Q{x+24*s} {y-28*s} {x+30*s} {y} Z" fill="{c}" '
            f'stroke="{OL}" stroke-width="{4*s:.1f}"/>')


def flower(x, y, s, c='#FF7FA8'):
    petals = ''.join(f'<circle cx="{x+math.cos(a)*9*s:.1f}" cy="{y+math.sin(a)*9*s:.1f}" r="{7*s:.1f}" fill="{c}"/>' for a in [i*math.pi*2/5 for i in range(5)])
    return f'<g stroke="{OL}" stroke-width="{2.5*s:.1f}">{petals}<circle cx="{x}" cy="{y}" r="{5*s}" fill="#FFD23F"/></g>'


def house(x, y, s, wall='#FBE6C4', roof='#E2553B'):
    return (f'<g stroke="{OL}" stroke-width="{4*s:.1f}" stroke-linejoin="round"><rect x="{x-30*s}" y="{y-40*s}" width="{60*s}" height="{40*s}" fill="{wall}"/>'
            f'<path d="M{x-38*s} {y-38*s} L{x} {y-74*s} L{x+38*s} {y-38*s} Z" fill="{roof}"/>'
            f'<rect x="{x-8*s}" y="{y-22*s}" width="{16*s}" height="{22*s}" fill="#9A5B27"/>'
            f'<rect x="{x-24*s}" y="{y-32*s}" width="{10*s}" height="{10*s}" fill="#9FD8FF"/><rect x="{x+14*s}" y="{y-32*s}" width="{10*s}" height="{10*s}" fill="#9FD8FF"/></g>')


def tower(x, y, s, wall='#E9C99A', roof='#3A7BD5'):
    return (f'<g stroke="{OL}" stroke-width="{4*s:.1f}" stroke-linejoin="round"><rect x="{x-18*s}" y="{y-110*s}" width="{36*s}" height="{110*s}" fill="{wall}"/>'
            f'<path d="M{x-24*s} {y-108*s} L{x} {y-150*s} L{x+24*s} {y-108*s} Z" fill="{roof}"/>'
            f'<rect x="{x-7*s}" y="{y-90*s}" width="{14*s}" height="{18*s}" rx="{6*s}" fill="#5A3A1A"/></g>')


def dome(x, y, s, wall='#F2D6AE', roof='#E9A23B'):
    return (f'<g stroke="{OL}" stroke-width="{4*s:.1f}"><rect x="{x-40*s}" y="{y-60*s}" width="{80*s}" height="{60*s}" fill="{wall}"/>'
            f'<path d="M{x-34*s} {y-60*s} Q{x-34*s} {y-112*s} {x} {y-112*s} Q{x+34*s} {y-112*s} {x+34*s} {y-60*s} Z" fill="{roof}"/>'
            f'<rect x="{x-3*s}" y="{y-132*s}" width="{6*s}" height="{22*s}" fill="{roof}"/>'
            f'<g fill="#5A3A1A"><rect x="{x-28*s}" y="{y-44*s}" width="{12*s}" height="{20*s}" rx="{6*s}"/><rect x="{x-6*s}" y="{y-44*s}" width="{12*s}" height="{20*s}" rx="{6*s}"/><rect x="{x+16*s}" y="{y-44*s}" width="{12*s}" height="{20*s}" rx="{6*s}"/></g></g>')


def cloud(x, y, s, c='#FFFFFF', o=0.9):
    return (f'<g fill="{c}" opacity="{o}"><ellipse cx="{x}" cy="{y}" rx="{70*s}" ry="{26*s}"/><circle cx="{x-30*s}" cy="{y-14*s}" r="{28*s}"/>'
            f'<circle cx="{x+16*s}" cy="{y-24*s}" r="{36*s}"/></g>')


def sparkle(x, y, s, c='#FFFFFF', o=0.9):
    return (f'<path d="M{x} {y-12*s} Q{x+2*s} {y-2*s} {x+12*s} {y} Q{x+2*s} {y+2*s} {x} {y+12*s} Q{x-2*s} {y+2*s} {x-12*s} {y} Q{x-2*s} {y-2*s} {x} {y-12*s} Z" '
            f'fill="{c}" opacity="{o}"/>')


def planet(x, y, s, c1, c2):
    return (f'<g stroke="{OL}" stroke-width="{4*s:.1f}"><circle cx="{x}" cy="{y}" r="{40*s}" fill="{c1}"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{70*s}" ry="{14*s}" fill="none" stroke="{c2}" stroke-width="{8*s:.1f}" transform="rotate(-20 {x} {y})"/>'
            f'<ellipse cx="{x-14*s}" cy="{y-16*s}" rx="{12*s}" ry="{7*s}" fill="#fff" fill-opacity="0.4" stroke="none"/></g>')


def seaweed(x, y, s, c='#3FAE5A'):
    return (f'<path d="M{x} {y} Q{x-20*s} {y-40*s} {x} {y-80*s} Q{x+20*s} {y-120*s} {x} {y-160*s}" fill="none" stroke="{c}" stroke-width="{14*s:.1f}" stroke-linecap="round"/>')


def coral(x, y, s, c='#FF7F7F'):
    return (f'<g fill="none" stroke="{c}" stroke-width="{12*s:.1f}" stroke-linecap="round"><path d="M{x} {y} L{x} {y-60*s}"/>'
            f'<path d="M{x} {y-30*s} Q{x-30*s} {y-40*s} {x-30*s} {y-70*s}"/><path d="M{x} {y-40*s} Q{x+30*s} {y-50*s} {x+28*s} {y-84*s}"/></g>')


def palm_island(x, y, s):
    return (f'<g stroke="{OL}" stroke-width="{4*s:.1f}"><ellipse cx="{x}" cy="{y}" rx="{110*s}" ry="{44*s}" fill="#F3D79A"/>'
            f'<ellipse cx="{x}" cy="{y-6*s}" rx="{80*s}" ry="{30*s}" fill="#7CCB4E"/>'
            f'<path d="M{x} {y-10*s} Q{x+10*s} {y-60*s} {x+4*s} {y-110*s}" fill="none" stroke="#8A5326" stroke-width="{12*s:.1f}"/>'
            f'<path d="M{x+4*s} {y-110*s} Q{x+50*s} {y-130*s} {x+70*s} {y-96*s} Q{x+30*s} {y-110*s} {x+4*s} {y-110*s} Z" fill="#3E8E2F"/>'
            f'<path d="M{x+4*s} {y-110*s} Q{x-46*s} {y-132*s} {x-66*s} {y-96*s} Q{x-26*s} {y-112*s} {x+4*s} {y-110*s} Z" fill="#4FA83A"/></g>')


def bubble(x, y, s):
    return (f'<g fill="none" stroke="#fff" stroke-opacity="0.55" stroke-width="{3*s:.1f}"><circle cx="{x}" cy="{y}" r="{12*s}"/></g>'
            f'<circle cx="{x-4*s}" cy="{y-4*s}" r="{3*s}" fill="#fff" fill-opacity="0.6"/>')


def carrot(x, y, s):
    return (f'<g stroke="{OL}" stroke-width="{4*s:.1f}" stroke-linejoin="round"><path d="M{x-16*s} {y-60*s} L{x+16*s} {y-60*s} L{x} {y} Z" fill="#FF8A2A"/>'
            f'<path d="M{x} {y-60*s} Q{x-18*s} {y-90*s} {x-6*s} {y-96*s} Q{x} {y-80*s} {x} {y-60*s} Q{x+16*s} {y-94*s} {x+10*s} {y-98*s} Z" fill="#4FA83A"/></g>')


# ---------------- logo ----------------

def logo():
    W, H = 1200, 860
    leaves = leaf_fan(260, 640, 1.05, 200) + leaf_fan(940, 640, 1.05, -20)
    body = f'''
{leaves}
<g font-family="Baloo" text-anchor="middle">
  <text x="606" y="436" font-size="330" fill="#3A1A08" opacity="0.55">WORD</text>
  <text x="600" y="420" font-size="330" fill="url(#logoGold)" stroke="#5A2A0E" stroke-width="34" paint-order="stroke" stroke-linejoin="round">WORD</text>
  <text x="600" y="420" font-size="330" fill="url(#logoShine)">WORD</text>
  <g transform="rotate(-6 600 690)">
    <text x="610" y="790" font-size="470" fill="#3A1A08" opacity="0.55">Z</text>
    <text x="600" y="772" font-size="470" fill="url(#logoCream)" stroke="#5A2A0E" stroke-width="38" paint-order="stroke" stroke-linejoin="round">Z</text>
    <text x="600" y="772" font-size="470" fill="url(#logoShine)">Z</text>
  </g>
</g>
{tile_svg(150, 160, 'A', -14, 150)}
{tile_svg(1060, 150, 'C', 12, 140)}
{tile_svg(200, 600, 'W', 10, 130)}
{tile_svg(1010, 620, 'D', -10, 120)}
{sparkle(810, 520, 3.4, '#FFF6C8', 1)}
{sparkle(360, 120, 2.2, '#FFF6C8', 1)}'''
    defs = DEFS.replace('</defs>', '''
  <linearGradient id="logoGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0.1" stop-color="#FFF27A"/><stop offset="0.55" stop-color="#FFC21A"/><stop offset="1" stop-color="#F08A12"/></linearGradient>
  <linearGradient id="logoCream" x1="0" y1="0" x2="0" y2="1"><stop offset="0.2" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EBCB92"/></linearGradient>
  <linearGradient id="logoShine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.55"/><stop offset="0.45" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>''')
    write('logo', W, H, body, defs)


def tile_svg(x, y, letter, rot, size):
    h = size / 2
    return (f'<g transform="translate({x},{y}) rotate({rot})" filter="url(#ds)">'
            f'<rect x="{-h}" y="{-h+10}" width="{size}" height="{size}" rx="{size*0.22}" fill="#B9773C" stroke="{OL}" stroke-width="8"/>'
            f'<rect x="{-h}" y="{-h}" width="{size}" height="{size}" rx="{size*0.22}" fill="url(#cream)" stroke="{OL}" stroke-width="8"/>'
            f'<text x="0" y="{size*0.3}" font-family="Baloo" font-size="{size*0.78}" text-anchor="middle" fill="#7A4A1E">{letter}</text></g>')


# ---------------- leaves ----------------

def leaf(x, y, L, angle, c1, c2):
    W = L * 0.42
    return (f'<g transform="translate({x},{y}) rotate({angle})">'
            f'<path d="M0 0 Q{W} {-L*0.45} 0 {-L} Q{-W} {-L*0.45} 0 0 Z" fill="url(#lg_{c1[1:]})" stroke="#1F4A14" stroke-width="5"/>'
            f'<path d="M0 -6 Q4 {-L*0.5} 0 {-L*0.92}" fill="none" stroke="#C8F0A0" stroke-opacity="0.6" stroke-width="4"/>'
            + ''.join(f'<path d="M0 {-L*t} Q{W*0.4} {-L*(t+0.08)} {W*0.55} {-L*(t+0.16)}" fill="none" stroke="#C8F0A0" stroke-opacity="0.35" stroke-width="3"/>'
                      f'<path d="M0 {-L*t} Q{-W*0.4} {-L*(t+0.08)} {-W*0.55} {-L*(t+0.16)}" fill="none" stroke="#C8F0A0" stroke-opacity="0.35" stroke-width="3"/>'
                      for t in (0.3, 0.5, 0.68))
            + '</g>')


LEAF_COLORS = ['#5DBB45', '#4FA83A', '#3E8E2F', '#6CCB4F', '#2F7426']


def lighten(c, k=0.3):
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    return '#%02X%02X%02X' % tuple(int(v + (255 - v) * k) for v in (r, g, b))


def leaf_defs():
    g = ''.join(f'<linearGradient id="lg_{c[1:]}" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{c}"/>'
                f'<stop offset="1" stop-color="{lighten(c)}"/></linearGradient>' for c in LEAF_COLORS)
    return g


DEFS_LEAF = DEFS.replace('</defs>', leaf_defs() + '</defs>')
DEFS = DEFS_LEAF  # every scene can use leaves


def leaf_fan(x, y, s, base):
    out = ''
    for i, a in enumerate([-70, -42, -14, 14, 42, 70]):
        c = LEAF_COLORS[i % len(LEAF_COLORS)]
        L = (190 + (i % 3) * 30) * s
        out += leaf(x, y, L, base + a, c, c)
    return out


def leaf_corner():
    """Cluster spreading from the bottom-left corner (mirror it for other corners)."""
    W = H = 640
    body = ''
    rnd = random.Random(4)
    for i, a in enumerate([5, 20, 35, 50, 65, 80]):
        L = 380 + rnd.randint(-30, 120)
        body += leaf(30, H - 30, L, a, LEAF_COLORS[i % 5], LEAF_COLORS[i % 5])
    for i, a in enumerate([12, 42, 72]):
        body += leaf(10, H - 10, 230, a, LEAF_COLORS[(i + 2) % 5], None)
    body += f'<circle cx="150" cy="{H-170}" r="10" fill="#FF6B6B" stroke="{OL}" stroke-width="4"/><circle cx="174" cy="{H-150}" r="9" fill="#FF6B6B" stroke="{OL}" stroke-width="4"/>'
    write('leaf_corner', W, H, f'<g filter="url(#ds)">{body}</g>')


# ---------------- home background ----------------

def home_bg():
    W, H = 1080, 1920
    rnd = random.Random(7)
    defs = DEFS.replace('</defs>', '''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7EC3EE"/><stop offset="0.45" stop-color="#F6E0B0"/><stop offset="0.7" stop-color="#F5B26A"/><stop offset="1" stop-color="#E58A4A"/></linearGradient>
<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF7D0"/><stop offset="0.35" stop-color="#FFE7A0" stop-opacity="0.9"/><stop offset="1" stop-color="#FFD27A" stop-opacity="0"/></radialGradient>
<linearGradient id="far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C89A8C"/><stop offset="1" stop-color="#B07A72"/></linearGradient>
<linearGradient id="mid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E7B98A"/><stop offset="1" stop-color="#C98E5E"/></linearGradient>
<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FC45A"/><stop offset="1" stop-color="#3E8E2F"/></linearGradient>
</defs>''')
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/><circle cx="560" cy="1060" r="420" fill="url(#sun)"/>'
    for (x, y, s) in [(200, 360, 1.3), (820, 300, 1.1), (560, 520, 0.9), (930, 640, 0.8), (120, 760, 0.7)]:
        b += cloud(x, y, s, '#FFFFFF', 0.85)
    # far skyline silhouettes
    x = -20
    while x < W:
        w = rnd.randint(50, 110); h = rnd.randint(160, 380)
        b += f'<rect x="{x}" y="{1260-h}" width="{w}" height="{h+400}" fill="url(#far)" opacity="0.8"/>'
        if rnd.random() < 0.35:
            b += f'<path d="M{x} {1260-h} Q{x+w/2} {1260-h-w*0.9} {x+w} {1260-h} Z" fill="url(#far)" opacity="0.8"/>'
        x += w - 6
    # mid city: domes, towers, buildings with windows
    b += dome(260, 1420, 1.6, '#F2D6AE', '#E9A23B') + dome(780, 1400, 1.9, '#F5DDB8', '#D9883A')
    b += tower(520, 1420, 1.8, '#F0CFA0', '#C9573A') + tower(950, 1430, 1.4, '#E9C99A', '#3A7BD5') + tower(80, 1440, 1.5, '#E9C99A', '#3A7BD5')
    x = -10
    while x < W:
        w = rnd.randint(70, 120); h = rnd.randint(120, 260)
        col = rnd.choice(['#F7D8A8', '#F2C68E', '#EBB57F', '#F9E2BC'])
        roof = rnd.choice(['#C9573A', '#B5452E', '#D9883A', '#8E4B2A'])
        y0 = 1560 - h
        b += f'<g stroke="{OL}" stroke-width="5"><rect x="{x}" y="{y0}" width="{w}" height="{h+60}" fill="{col}"/>'
        b += f'<path d="M{x-8} {y0+4} L{x+w/2} {y0-40} L{x+w+8} {y0+4} Z" fill="{roof}"/></g>'
        for wy in range(int(y0 + 24), 1540, 46):
            for wx in range(int(x + 14), int(x + w - 20), 30):
                lit = rnd.random() < 0.5
                b += f'<rect x="{wx}" y="{wy}" width="16" height="22" rx="3" fill="{"#FFE58A" if lit else "#7B4A2A"}"/>'
        x += w + rnd.randint(-6, 8)
    # river and ground
    b += f'<rect x="0" y="1560" width="{W}" height="{H-1560}" fill="url(#ground)"/>'
    b += f'<path d="M0 1700 Q300 1640 540 1700 Q800 1770 1080 1690 L1080 1790 Q800 1860 540 1790 Q300 1730 0 1800 Z" fill="#5FB4E8" stroke="{OL}" stroke-width="5"/>'
    b += f'<path d="M120 1740 Q300 1700 460 1740" fill="none" stroke="#fff" stroke-opacity="0.6" stroke-width="8" stroke-linecap="round"/>'
    for i in range(14):
        tx = rnd.randint(0, W); ty = rnd.choice([1610, 1640, 1880, 1900])
        b += tree(tx, ty, rnd.uniform(1.2, 1.8))
    write('home_bg', W, H, b, defs)


def skyline():
    W, H = 1080, 520
    rnd = random.Random(3)
    b = ''
    x = -10
    while x < W:
        w = rnd.randint(60, 120); h = rnd.randint(140, 360)
        b += f'<rect x="{x}" y="{H-h}" width="{w}" height="{h}" fill="#3B1D0C"/>'
        if rnd.random() < 0.3:
            b += f'<path d="M{x} {H-h} Q{x+w/2} {H-h-w} {x+w} {H-h} Z" fill="#3B1D0C"/><rect x="{x+w/2-3}" y="{H-h-w-26}" width="6" height="30" fill="#3B1D0C"/>'
        elif rnd.random() < 0.3:
            b += f'<path d="M{x} {H-h} L{x+w/2} {H-h-60} L{x+w} {H-h} Z" fill="#3B1D0C"/>'
        x += w - 4
    write('skyline', W, H, f'<g opacity="0.75">{b}</g>')


def app_icon():
    W = H = 1024
    defs = DEFS.replace('</defs>', '''<linearGradient id="bgw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B9733A"/><stop offset="1" stop-color="#7A421A"/></linearGradient>
<linearGradient id="logoGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0.1" stop-color="#FFF27A"/><stop offset="0.55" stop-color="#FFC21A"/><stop offset="1" stop-color="#F08A12"/></linearGradient></defs>''')
    hexpts = ' '.join(f'{512+360*math.cos(math.radians(a)):.1f},{540+360*math.sin(math.radians(a)):.1f}' for a in range(0, 360, 60))
    hexpts2 = ' '.join(f'{512+360*math.cos(math.radians(a)):.1f},{512+360*math.sin(math.radians(a)):.1f}' for a in range(0, 360, 60))
    b = f'''<rect width="1024" height="1024" fill="url(#bgw)"/>
{''.join(f'<path d="M0 {y} Q512 {y+30} 1024 {y}" stroke="#6A3714" stroke-opacity="0.35" stroke-width="6" fill="none"/>' for y in range(80, 1024, 120))}
{leaf_fan(90, 1000, 1.5, 40)}{leaf_fan(940, 1000, 1.5, -40)}
<polygon points="{hexpts}" fill="#B9773C" stroke="{OL}" stroke-width="22" stroke-linejoin="round"/>
<polygon points="{hexpts2}" fill="url(#cream)" stroke="{OL}" stroke-width="22" stroke-linejoin="round"/>
<text x="512" y="700" font-family="Baloo" font-size="560" text-anchor="middle" fill="url(#logoGold)" stroke="#5A2A0E" stroke-width="30" paint-order="stroke" stroke-linejoin="round">Z</text>'''
    write('app_icon', W, H, b, defs)


# ---------------- category maps ----------------

MAPS = {
    'CITY':        dict(bg=('#A7DA78', '#6DBB4A'), pattern='grass', river='#5FB4E8', props=['house', 'tower', 'dome', 'tree', 'bush']),
    'ELECTRONIC':  dict(bg=('#243457', '#121B33'), pattern='circuit', props=['cat_electronic', 'bolt', 'bulb', 'gear']),
    'THINGS':      dict(bg=('#D9A066', '#B9773C'), pattern='planks', props=['cat_things', 'chest', 'calendar', 'gift', 'quest']),
    'MEALS':       dict(bg=('#FFF3DC', '#F7E2BE'), pattern='picnic', props=['cat_meals', 'cat_fruit_veg', 'coin']),
    'MUSIC':       dict(bg=('#6A2FB0', '#2E1260'), pattern='stage', props=['cat_music', 'star']),
    'SPORT':       dict(bg=('#6DC24A', '#4CA23A'), pattern='field', props=['cat_sport', 'trophy', 'star']),
    'COUNTRIES':   dict(bg=('#5CB8F0', '#2A7FD0'), pattern='ocean', props=['island', 'cat_countries']),
    'CINEMA':      dict(bg=('#C8283A', '#7A101E'), pattern='curtain', props=['cat_cinema', 'star']),
    'ANIMALS':     dict(bg=('#E6D27A', '#B9B05A'), pattern='savanna', props=['tree', 'rock', 'cat_animals', 'bush']),
    'NATURE':      dict(bg=('#7CC95A', '#3E8E2F'), pattern='grass', river='#5FB4E8', props=['pine', 'tree', 'flower', 'rock', 'bush']),
    'FRUIT & VEG': dict(bg=('#A7D46A', '#7BB548'), pattern='farm', props=['cat_fruit_veg', 'carrot', 'tree', 'bush']),
    'JOBS':        dict(bg=('#BFD7A0', '#8FBF6A'), pattern='grass', props=['house', 'tower', 'cat_jobs', 'tree']),
    'BODY':        dict(bg=('#FFD3E2', '#F59BBC'), pattern='dots', props=['cat_body', 'star']),
    'CLOTHES':     dict(bg=('#FFE1EC', '#E8C3F0'), pattern='stripes', props=['cat_clothes', 'gem', 'star']),
    'WEATHER':     dict(bg=('#8FD3FF', '#4FA6EA'), pattern='sky', props=['cloud', 'cat_weather']),
    'SPACE':       dict(bg=('#2A1E5C', '#0B0A24'), pattern='space', props=['planet', 'cat_space', 'star']),
    'OCEAN':       dict(bg=('#3FA9E8', '#0C4C8F'), pattern='deep', props=['seaweed', 'coral', 'cat_ocean', 'bubble']),
    'KITCHEN':     dict(bg=('#FFF0D8', '#EED4AE'), pattern='tiles', props=['cat_kitchen', 'cat_meals', 'cat_fruit_veg']),
    'SCHOOL':      dict(bg=('#3E7A57', '#24533A'), pattern='chalk', props=['cat_school', 'star', 'letter']),
    'TRAVEL':      dict(bg=('#F6E7C6', '#E6CF9E'), pattern='paper', props=['cat_travel', 'island', 'cat_countries']),
}


def pattern(kind, W, H, rnd, c1, c2):
    b = ''
    if kind in ('grass', 'savanna', 'farm'):
        for _ in range(140):
            x, y = rnd.randint(0, W), rnd.randint(0, H)
            b += f'<ellipse cx="{x}" cy="{y}" rx="{rnd.randint(30,90)}" ry="{rnd.randint(14,40)}" fill="#fff" fill-opacity="0.08"/>'
        for _ in range(220):
            x, y = rnd.randint(0, W), rnd.randint(0, H)
            b += f'<path d="M{x} {y} l-6 -14 M{x} {y} l0 -18 M{x} {y} l6 -14" stroke="#2F6A22" stroke-opacity="0.35" stroke-width="3"/>'
        if kind == 'farm':
            for i in range(0, H, 260):
                b += f'<rect x="0" y="{i}" width="{W}" height="120" fill="#8A5A2E" fill-opacity="0.22"/>'
                for x in range(20, W, 46):
                    b += f'<path d="M{x} {i+60} q8 -18 16 0" stroke="#3E8E2F" stroke-width="6" fill="none" opacity="0.6"/>'
    elif kind == 'circuit':
        for _ in range(70):
            x, y = rnd.randint(0, W), rnd.randint(0, H)
            dx = rnd.choice([-1, 1]) * rnd.randint(60, 200)
            b += (f'<path d="M{x} {y} l{dx} 0 l{abs(dx)/3:.0f} {abs(dx)/3:.0f} l0 {rnd.randint(40,160)}" fill="none" stroke="#3DE0FF" stroke-opacity="0.35" stroke-width="5"/>'
                  f'<circle cx="{x}" cy="{y}" r="8" fill="#3DE0FF" fill-opacity="0.6"/>')
    elif kind == 'planks':
        for y in range(0, H, 90):
            b += f'<rect x="0" y="{y}" width="{W}" height="4" fill="#6A3714" fill-opacity="0.35"/>'
            off = rnd.randint(0, 300)
            for x in range(off, W, 360):
                b += f'<rect x="{x}" y="{y}" width="4" height="90" fill="#6A3714" fill-opacity="0.3"/>'
    elif kind == 'picnic':
        for y in range(0, H, 120):
            for x in range(0, W, 120):
                if ((x // 120) + (y // 120)) % 2 == 0:
                    b += f'<rect x="{x}" y="{y}" width="120" height="120" fill="#E85A5A" fill-opacity="0.75"/>'
    elif kind == 'stage':
        for i in range(5):
            x = 120 + i * 210
            b += f'<path d="M{x} 0 L{x-160} {H} L{x+160} {H} Z" fill="#FFE9A8" fill-opacity="0.06"/>'
        for _ in range(80):
            b += sparkle(rnd.randint(0, W), rnd.randint(0, H), rnd.uniform(0.6, 1.6), '#FFE9A8', 0.6)
    elif kind == 'field':
        for i in range(0, H, 200):
            b += f'<rect x="0" y="{i}" width="{W}" height="100" fill="#fff" fill-opacity="0.07"/>'
        b += f'<rect x="60" y="40" width="{W-120}" height="{H-80}" fill="none" stroke="#fff" stroke-opacity="0.6" stroke-width="8"/>'
        for y in range(600, H, 1200):
            b += f'<line x1="60" y1="{y}" x2="{W-60}" y2="{y}" stroke="#fff" stroke-opacity="0.6" stroke-width="8"/><circle cx="{W/2}" cy="{y}" r="140" fill="none" stroke="#fff" stroke-opacity="0.6" stroke-width="8"/>'
    elif kind in ('ocean', 'deep'):
        for _ in range(90):
            x, y = rnd.randint(-50, W), rnd.randint(0, H)
            b += f'<path d="M{x} {y} q20 -12 40 0 t40 0" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="5" stroke-linecap="round"/>'
        if kind == 'deep':
            for i in range(6):
                x = 100 + i * 180
                b += f'<path d="M{x} 0 L{x-120} {H} L{x+60} {H} Z" fill="#BFF0FF" fill-opacity="0.05"/>'
    elif kind == 'curtain':
        for x in range(0, W, 90):
            b += f'<rect x="{x}" y="0" width="45" height="{H}" fill="#000" fill-opacity="0.12"/><rect x="{x+10}" y="0" width="10" height="{H}" fill="#fff" fill-opacity="0.08"/>'
    elif kind == 'dots':
        for _ in range(160):
            b += f'<circle cx="{rnd.randint(0,W)}" cy="{rnd.randint(0,H)}" r="{rnd.randint(6,22)}" fill="#fff" fill-opacity="0.25"/>'
    elif kind == 'stripes':
        for x in range(-H, W, 120):
            b += f'<path d="M{x} 0 L{x+H} {H} L{x+H+50} {H} L{x+50} 0 Z" fill="#fff" fill-opacity="0.18"/>'
    elif kind == 'sky':
        for _ in range(40):
            b += cloud(rnd.randint(0, W), rnd.randint(0, H), rnd.uniform(0.6, 1.4), '#fff', 0.5)
    elif kind == 'space':
        for _ in range(420):
            r = rnd.choice([1.5, 2, 2.5, 3.5])
            b += f'<circle cx="{rnd.randint(0,W)}" cy="{rnd.randint(0,H)}" r="{r}" fill="#fff" fill-opacity="{rnd.uniform(0.4,1):.2f}"/>'
        for _ in range(40):
            b += sparkle(rnd.randint(0, W), rnd.randint(0, H), rnd.uniform(0.8, 1.8), '#FFF6C8', 0.8)
    elif kind == 'tiles':
        for y in range(0, H, 110):
            for x in range(0, W, 110):
                c = '#E89A6A' if ((x // 110) + (y // 110)) % 2 == 0 else '#FFF8EA'
                b += f'<rect x="{x+3}" y="{y+3}" width="104" height="104" rx="8" fill="{c}" fill-opacity="0.55"/>'
    elif kind == 'chalk':
        for _ in range(60):
            x, y = rnd.randint(0, W), rnd.randint(0, H)
            ch = rnd.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ+=?123')
            b += f'<text x="{x}" y="{y}" font-family="Baloo" font-size="{rnd.randint(40,90)}" fill="#fff" fill-opacity="0.18" transform="rotate({rnd.randint(-20,20)} {x} {y})">{ch}</text>'
        b += f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="#8A5326" stroke-width="30"/>'
    elif kind == 'paper':
        for x in range(0, W, 120):
            b += f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#B8945A" stroke-opacity="0.25" stroke-width="2"/>'
        for y in range(0, H, 120):
            b += f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#B8945A" stroke-opacity="0.25" stroke-width="2"/>'
        for _ in range(10):
            x1, y1, x2, y2 = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(0, W), rnd.randint(0, H)
            b += f'<path d="M{x1} {y1} Q{(x1+x2)/2+rnd.randint(-200,200)} {(y1+y2)/2} {x2} {y2}" fill="none" stroke="#C0392B" stroke-opacity="0.5" stroke-width="6" stroke-dasharray="4 18" stroke-linecap="round"/>'
    return b


def draw_prop(kind, x, y, s, rnd):
    if kind in BODIES:
        return prop(kind, x, y, 120 * s, rnd.uniform(-14, 14), 0.95)
    return {
        'tree': lambda: tree(x, y, 1.4 * s), 'pine': lambda: pine(x, y, 1.3 * s), 'bush': lambda: bush(x, y, 1.3 * s),
        'rock': lambda: rock(x, y, 1.4 * s), 'flower': lambda: flower(x, y, 1.6 * s, rnd.choice(['#FF7FA8', '#FFD23F', '#B98BFF', '#FFFFFF'])),
        'house': lambda: house(x, y, 1.5 * s, rnd.choice(['#FBE6C4', '#F6D3A2', '#FFF1DA']), rnd.choice(['#E2553B', '#3A7BD5', '#D9883A'])),
        'tower': lambda: tower(x, y, 1.2 * s), 'dome': lambda: dome(x, y, 1.2 * s),
        'cloud': lambda: cloud(x, y, 1.2 * s, '#fff', 0.95), 'planet': lambda: planet(x, y, 1.4 * s, rnd.choice(['#FF9E5E', '#7FD6FF', '#C98BFF', '#FFD23F']), '#FFE9A8'),
        'seaweed': lambda: seaweed(x, y, 1.3 * s), 'coral': lambda: coral(x, y, 1.4 * s, rnd.choice(['#FF7F7F', '#FFB45E', '#FF9EC0'])),
        'bubble': lambda: bubble(x, y, 1.6 * s), 'island': lambda: palm_island(x, y, 1.3 * s), 'carrot': lambda: carrot(x, y, 1.3 * s),
    }[kind]()


def map_bg(name, spec):
    W, H = 1080, 2400
    rnd = random.Random(hash(name) & 0xffff)
    c1, c2 = spec['bg']
    defs = DEFS.replace('</defs>', f'<linearGradient id="mbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
                                   f'<radialGradient id="vig" cx="0.5" cy="0.5" r="0.75"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.35"/></radialGradient></defs>')
    b = f'<rect width="{W}" height="{H}" fill="url(#mbg)"/>' + pattern(spec['pattern'], W, H, rnd, c1, c2)
    if spec.get('river'):
        pts = [(rnd.randint(250, 830), y) for y in range(-100, H + 200, 300)]
        d = f'M{pts[0][0]} {pts[0][1]} ' + ' '.join(f'S{(a[0]+bb[0])/2:.0f} {bb[1]-150} {bb[0]} {bb[1]}' for a, bb in zip(pts, pts[1:]))
        b += f'<path d="{d}" fill="none" stroke="{OL}" stroke-width="128" stroke-linecap="round"/>'
        b += f'<path d="{d}" fill="none" stroke="{spec["river"]}" stroke-width="112" stroke-linecap="round"/>'
        b += f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="10" stroke-dasharray="40 60" stroke-linecap="round"/>'
    # props, denser at the sides so the level path in the middle stays readable
    items = []
    for _ in range(70):
        side = rnd.random()
        x = rnd.randint(30, 260) if side < 0.42 else rnd.randint(820, 1050) if side < 0.84 else rnd.randint(300, 780)
        y = rnd.randint(40, H - 20)
        s = rnd.uniform(0.75, 1.2) * (0.7 if 300 < x < 780 else 1)
        items.append((y, x, s, rnd.choice(spec['props'])))
    for y, x, s, k in sorted(items):
        b += draw_prop(k, x, y, s, rnd)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    slug = 'map_' + name.lower().replace(' & ', '_').replace(' ', '_')
    write(slug, W, H, b, defs)


if __name__ == '__main__':
    logo(); leaf_corner(); home_bg(); skyline(); app_icon()
    for n, sp in MAPS.items():
        map_bg(n, sp)
    print('scenes written')
