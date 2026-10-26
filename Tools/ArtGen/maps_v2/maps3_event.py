"""v3 event maps (3/4 view): HALLOWEEN - a cosy harvest-night pumpkin valley (cute, not scary)."""
import math
from style import OL, shade, mix, rng, lin, rad, contact_shadow, cloud
from world import World, S, W, H, HY, hills
from city2 import townhouse, fluffy_tree, lamp
from props3 import g, sw, barn, fence, haystack, crop_rows, scarecrow, bush, rock
from props3c import glow, string_lights

AUTUMN = ['#E9A23B', '#D9772E', '#C9A63E', '#B8B04A', '#E3B341']


def sky_harvest(moon=(560, 250)):
    d = (lin('skyh', [(0, '#3F4C78', 1), (0.5, '#B0687A', 1), (0.8, '#F2A27A', 1), (1, '#FFD49A', 1)]) +
         rad('moonh', [(0, '#FFF6C8', 0.9), (0.35, '#FFE9A0', 0.35), (1, '#FFE9A0', 0)]))
    r = rng(31)
    out = [f'<defs>{d}</defs><rect width="{W}" height="{HY + 140}" fill="url(#skyh)"/>']
    for _ in range(70):
        x, y = r.uniform(0, W), r.uniform(0, HY * 0.55)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.2, 3.2):.1f}" fill="#FFF6D8" opacity="{r.uniform(0.35, 0.95):.2f}"/>')
    out += [f'<circle cx="{moon[0]}" cy="{moon[1]}" r="300" fill="url(#moonh)"/>',
            f'<circle cx="{moon[0]}" cy="{moon[1]}" r="118" fill="#FFF0B8" stroke="#E8CF7A" stroke-width="6"/>',
            f'<circle cx="{moon[0] - 38}" cy="{moon[1] - 26}" r="22" fill="#F2DE96"/><circle cx="{moon[0] + 30}" cy="{moon[1] + 34}" r="16" fill="#F2DE96"/>'
            f'<circle cx="{moon[0] + 44}" cy="{moon[1] - 44}" r="10" fill="#F2DE96"/>']
    for x, y, s in [(150, 170, 0.9), (930, 120, 0.8), (300, 330, 0.6)]:
        out.append(cloud(x, y, s, 0.5, '#F7C9B0'))
    for x, y, s in [(470, 200, 1.1), (520, 160, 0.8), (640, 210, 0.9), (700, 300, 0.7), (380, 300, 0.6)]:
        out.append(bat(x, y, s))
    return ''.join(out)


def bat(x, y, s, c='#3A2238'):
    return (f'<path d="M{x:.1f} {y:.1f} Q{x - 10 * s:.1f} {y - 14 * s:.1f} {x - 30 * s:.1f} {y - 10 * s:.1f} Q{x - 24 * s:.1f} {y - 2 * s:.1f} {x - 26 * s:.1f} {y + 6 * s:.1f} '
            f'Q{x - 14 * s:.1f} {y - 2 * s:.1f} {x - 8 * s:.1f} {y + 4 * s:.1f} Q{x - 4 * s:.1f} {y - 2 * s:.1f} {x:.1f} {y + 6 * s:.1f} '
            f'Q{x + 4 * s:.1f} {y - 2 * s:.1f} {x + 8 * s:.1f} {y + 4 * s:.1f} Q{x + 14 * s:.1f} {y - 2 * s:.1f} {x + 26 * s:.1f} {y + 6 * s:.1f} '
            f'Q{x + 24 * s:.1f} {y - 2 * s:.1f} {x + 30 * s:.1f} {y - 10 * s:.1f} Q{x + 10 * s:.1f} {y - 14 * s:.1f} {x:.1f} {y:.1f} Z" fill="{c}"/>'
            f'<circle cx="{x:.1f}" cy="{y - 4 * s:.1f}" r="{6 * s:.1f}" fill="{c}"/>')


def castle_silhouette(cx=820, base=HY + 20):
    c, lit = '#5A4A6A', '#FFD86B'
    out = [f'<path d="M{cx - 150} {base} L{cx - 150} {base - 90} L{cx - 110} {base - 90} L{cx - 110} {base - 150} L{cx - 60} {base - 150} '
           f'L{cx - 60} {base - 110} L{cx + 20} {base - 110} L{cx + 20} {base - 190} L{cx + 70} {base - 190} L{cx + 70} {base - 120} '
           f'L{cx + 130} {base - 120} L{cx + 130} {base} Z" fill="{c}"/>',
           f'<path d="M{cx - 118} {base - 150} L{cx - 85} {base - 210} L{cx - 52} {base - 150} Z" fill="{c}"/>',
           f'<path d="M{cx + 12} {base - 190} L{cx + 45} {base - 262} L{cx + 78} {base - 190} Z" fill="{c}"/>']
    for x, y in [(-88, -120), (40, -160), (40, -128), (-20, -80), (90, -84), (-130, -60)]:
        out.append(f'<rect x="{cx + x}" y="{base + y}" width="10" height="16" rx="4" fill="{lit}" opacity="0.9"/>')
    return ''.join(out)


def bare_tree(x, y, s, seed=0, leaves=True):
    r = rng(seed)
    trunk = '#6B4A3A'
    k = sw(s)
    out = [contact_shadow(x, y + 3 * s, 46 * s, 10 * s, 0.25),
           f'<path d="M{x - 12 * s:.1f} {y:.1f} Q{x - 6 * s:.1f} {y - 70 * s:.1f} {x - 2 * s:.1f} {y - 120 * s:.1f} L{x + 8 * s:.1f} {y - 120 * s:.1f} '
           f'Q{x + 8 * s:.1f} {y - 60 * s:.1f} {x + 14 * s:.1f} {y:.1f} Z" fill="{trunk}" {g(s)}/>']
    for a, L, h in [(-0.9, 60, 100), (0.8, 64, 96), (-0.4, 52, 128), (0.35, 56, 126), (-1.3, 40, 70), (1.25, 44, 74)]:
        x0, y0 = x + 3 * s, y - h * s
        x1, y1 = x0 + math.sin(a) * L * s, y0 - math.cos(a) * L * s * 0.9
        out.append(f'<path d="M{x0:.1f} {y0:.1f} Q{(x0 + x1) / 2 + 8 * s * math.copysign(1, a):.1f} {(y0 + y1) / 2:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{OL}" stroke-width="{11 * s:.1f}" stroke-linecap="round"/>'
                   f'<path d="M{x0:.1f} {y0:.1f} Q{(x0 + x1) / 2 + 8 * s * math.copysign(1, a):.1f} {(y0 + y1) / 2:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{trunk}" stroke-width="{6 * s:.1f}" stroke-linecap="round"/>')
        if leaves and r.random() < 0.8:
            c = r.choice(AUTUMN)
            out.append(f'<ellipse cx="{x1:.1f}" cy="{y1:.1f}" rx="{r.uniform(14, 22) * s:.1f}" ry="{r.uniform(10, 15) * s:.1f}" fill="{c}" {g(s, 0.7)}/>')
    return ''.join(out)


def autumn_tree(x, y, s, seed=0):
    r = rng(seed)
    return fluffy_tree(x, y, s, r.choice(AUTUMN), seed=seed)


def grave(x, y, s, tilt=0):
    c = '#B9B3C2'
    k = sw(s)
    return (contact_shadow(x, y + 2 * s, 26 * s, 6 * s, 0.25) +
            f'<g transform="rotate({tilt} {x:.1f} {y:.1f})">'
            f'<path d="M{x - 20 * s:.1f} {y:.1f} L{x - 20 * s:.1f} {y - 36 * s:.1f} Q{x - 20 * s:.1f} {y - 58 * s:.1f} {x:.1f} {y - 58 * s:.1f} '
            f'Q{x + 20 * s:.1f} {y - 58 * s:.1f} {x + 20 * s:.1f} {y - 36 * s:.1f} L{x + 20 * s:.1f} {y:.1f} Z" fill="{c}" {g(s)}/>'
            f'<path d="M{x + 8 * s:.1f} {y - 52 * s:.1f} Q{x + 16 * s:.1f} {y - 44 * s:.1f} {x + 15 * s:.1f} {y - 30 * s:.1f} L{x + 15 * s:.1f} {y - 2 * s:.1f}" fill="none" stroke="{shade(c, -0.18)}" stroke-width="{5 * s:.1f}"/>'
            f'<path d="M{x:.1f} {y - 44 * s:.1f} L{x:.1f} {y - 20 * s:.1f} M{x - 8 * s:.1f} {y - 36 * s:.1f} L{x + 8 * s:.1f} {y - 36 * s:.1f}" stroke="{shade(c, -0.3)}" stroke-width="{4 * s:.1f}" stroke-linecap="round"/>'
            f'<path d="M{x - 26 * s:.1f} {y:.1f} q6 {-8 * s:.1f} 12 0 q6 {-10 * s:.1f} 12 0" fill="#7DA44A" stroke="none"/></g>')


def ghost(x, y, s):
    return (f'<ellipse cx="{x:.1f}" cy="{y + 30 * s:.1f}" rx="{22 * s:.1f}" ry="{6 * s:.1f}" fill="#2A1205" opacity="0.15"/>'
            f'<path d="M{x - 24 * s:.1f} {y:.1f} L{x - 24 * s:.1f} {y - 34 * s:.1f} Q{x - 24 * s:.1f} {y - 64 * s:.1f} {x:.1f} {y - 64 * s:.1f} '
            f'Q{x + 24 * s:.1f} {y - 64 * s:.1f} {x + 24 * s:.1f} {y - 34 * s:.1f} L{x + 24 * s:.1f} {y:.1f} '
            f'Q{x + 16 * s:.1f} {y - 10 * s:.1f} {x + 8 * s:.1f} {y:.1f} Q{x:.1f} {y - 10 * s:.1f} {x - 8 * s:.1f} {y:.1f} Q{x - 16 * s:.1f} {y - 10 * s:.1f} {x - 24 * s:.1f} {y:.1f} Z" fill="#FFFDF5" {g(s)}/>'
            f'<ellipse cx="{x - 8 * s:.1f}" cy="{y - 38 * s:.1f}" rx="{4 * s:.1f}" ry="{6 * s:.1f}" fill="{OL}"/>'
            f'<ellipse cx="{x + 8 * s:.1f}" cy="{y - 38 * s:.1f}" rx="{4 * s:.1f}" ry="{6 * s:.1f}" fill="{OL}"/>'
            f'<ellipse cx="{x:.1f}" cy="{y - 24 * s:.1f}" rx="{5 * s:.1f}" ry="{4 * s:.1f}" fill="#FF8FA3"/>'
            f'<circle cx="{x - 14 * s:.1f}" cy="{y - 28 * s:.1f}" r="{4 * s:.1f}" fill="#FFB5C2" opacity="0.8"/><circle cx="{x + 14 * s:.1f}" cy="{y - 28 * s:.1f}" r="{4 * s:.1f}" fill="#FFB5C2" opacity="0.8"/>')


def jack(x, y, s, lit=True, big=1.0):
    s = s * big
    out = [contact_shadow(x, y + 2 * s, 30 * s, 7 * s, 0.25)]
    if lit:
        out.append(glow(x, y - 18 * s, 46 * s, '#FFC23A', 0.35))
    for dx, rx in [(-14, 18), (14, 18), (0, 16)]:
        out.append(f'<ellipse cx="{x + dx * s:.1f}" cy="{y - 18 * s:.1f}" rx="{rx * s:.1f}" ry="{19 * s:.1f}" fill="#F59A1E" {g(s)}/>')
    out.append(f'<ellipse cx="{x:.1f}" cy="{y - 18 * s:.1f}" rx="{14 * s:.1f}" ry="{18 * s:.1f}" fill="#FFB43A" stroke="none"/>')
    out.append(f'<rect x="{x - 3 * s:.1f}" y="{y - 44 * s:.1f}" width="{6 * s:.1f}" height="{9 * s:.1f}" rx="2" fill="#6C9E3A" {g(s, 0.6)}/>')
    face = '#FFE36A' if lit else '#5A2A0E'
    out.append(f'<path d="M{x - 13 * s:.1f} {y - 22 * s:.1f} l{6 * s:.1f} {-8 * s:.1f} l{5 * s:.1f} {8 * s:.1f} Z M{x + 13 * s:.1f} {y - 22 * s:.1f} l{-6 * s:.1f} {-8 * s:.1f} l{-5 * s:.1f} {8 * s:.1f} Z '
               f'M{x - 12 * s:.1f} {y - 13 * s:.1f} Q{x:.1f} {y - 2 * s:.1f} {x + 12 * s:.1f} {y - 13 * s:.1f} Z" fill="{face}"/>')
    return ''.join(out)


def cauldron(x, y, s):
    return (contact_shadow(x, y + 2 * s, 38 * s, 8 * s, 0.3) +
            glow(x, y - 50 * s, 40 * s, '#9BE36A', 0.3) +
            f'<path d="M{x - 26 * s:.1f} {y:.1f} l{-8 * s:.1f} {8 * s:.1f} M{x + 26 * s:.1f} {y:.1f} l{8 * s:.1f} {8 * s:.1f}" stroke="{OL}" stroke-width="{6 * s:.1f}" stroke-linecap="round"/>'
            f'<path d="M{x - 38 * s:.1f} {y - 40 * s:.1f} Q{x - 42 * s:.1f} {y + 4 * s:.1f} {x:.1f} {y + 4 * s:.1f} Q{x + 42 * s:.1f} {y + 4 * s:.1f} {x + 38 * s:.1f} {y - 40 * s:.1f} Z" fill="#3E3A44" {g(s)}/>'
            f'<ellipse cx="{x:.1f}" cy="{y - 40 * s:.1f}" rx="{40 * s:.1f}" ry="{10 * s:.1f}" fill="#7DD35A" {g(s)}/>'
            + ''.join(f'<circle cx="{x + dx * s:.1f}" cy="{y + dy * s:.1f}" r="{r_ * s:.1f}" fill="#A6EA7E" {g(s, 0.5)}/>' for dx, dy, r_ in [(-12, -54, 7), (8, -62, 9), (18, -50, 5), (0, -78, 5)]))


def lollipop(x, y, s, c='#FF6F91'):
    return (contact_shadow(x, y + 2 * s, 12 * s, 4 * s, 0.25) +
            f'<rect x="{x - 3 * s:.1f}" y="{y - 70 * s:.1f}" width="{6 * s:.1f}" height="{70 * s:.1f}" fill="#FFF8EA" {g(s, 0.6)}/>'
            f'<circle cx="{x:.1f}" cy="{y - 84 * s:.1f}" r="{22 * s:.1f}" fill="{c}" {g(s)}/>'
            f'<path d="M{x:.1f} {y - 84 * s:.1f} m{-12 * s:.1f} 0 a{12 * s:.1f} {12 * s:.1f} 0 1 1 {12 * s:.1f} {12 * s:.1f} a{7 * s:.1f} {7 * s:.1f} 0 1 1 {-7 * s:.1f} {-7 * s:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{4 * s:.1f}" opacity="0.85"/>')


def haunted_house(x, by, s):
    w = 230 * s
    out = [townhouse(x, by, w, 250 * s, s, '#8E8798', '#4E4458', side='l', floors=3, cols=3, seed=66, flowers=False)]
    # crooked tower + lit windows glow
    tx = x + w * 0.62
    out.append(f'<path d="M{tx - 26 * s:.1f} {by - 250 * s:.1f} L{tx - 22 * s:.1f} {by - 330 * s:.1f} L{tx + 26 * s:.1f} {by - 326 * s:.1f} L{tx + 28 * s:.1f} {by - 250 * s:.1f} Z" fill="#8E8798" {g(s)}/>'
               f'<path d="M{tx - 38 * s:.1f} {by - 326 * s:.1f} L{tx + 6 * s:.1f} {by - 410 * s:.1f} L{tx + 40 * s:.1f} {by - 322 * s:.1f} Z" fill="#4E4458" {g(s)}/>'
               f'<rect x="{tx - 8 * s:.1f}" y="{by - 306 * s:.1f}" width="{16 * s:.1f}" height="{24 * s:.1f}" rx="{6 * s:.1f}" fill="#FFD86B" {g(s, 0.6)}/>')
    out.append(glow(x + w * 0.5, by - 140 * s, 160 * s, '#FFD86B', 0.18))
    out.append(bat(tx + 60 * s, by - 420 * s, 0.9 * s))
    return ''.join(out)


def halloween():
    w = World(41)
    w.sky = sky_harvest()
    w.back = castle_silhouette() + hills(('#7F8B5E', '#6F7F52'), seed=12)
    d = lin('grh', [(0, '#B9B56A', 1), (1, '#7E9A48', 1)])
    w.ground = (f'<defs>{d}</defs><rect x="0" y="{HY + 20}" width="{W}" height="{H - HY}" fill="url(#grh)"/>' +
                ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{8 * S(y):.1f}" ry="{4 * S(y):.1f}" fill="{c}" opacity="0.8" transform="rotate({a} {x} {y})"/>'
                        for x, y, c, a in [(rng(i).uniform(0, W), rng(i + 99).uniform(HY + 60, H), AUTUMN[i % 5], i * 37 % 180) for i in range(260)]))
    w.path([(540, 470), (600, 640), (470, 860), (380, 1100), (520, 1380), (700, 1640), (590, 1940), (500, 2420)],
           w0=26, w1=150, fill='#E8C98E', edge='#BC9560')
    # pumpkin patches
    crop_rows(w, 40, 560, 380, 660, S(610), 'pumpkin', '#8A5A34', 3)
    crop_rows(w, 690, 980, 1060, 1100, S(1040), 'pumpkin', '#8A5A34', 4)
    crop_rows(w, 20, 1520, 300, 1660, S(1590), 'pumpkin', '#8A5A34', 4)
    # landmarks
    w.add(900, haunted_house(30, 900, S(900)))
    w.occ(20, 600, 330, 910)
    w.add(1260, barn(790, 1260, S(1260), w=170, h=120, col='#C2563A', side='l'))
    w.occ(770, 1110, 1080, 1270)
    for x, y, t in [(130, 1240, -6), (210, 1280, 4), (90, 1330, 8), (250, 1350, -4), (170, 1400, 2)]:
        w.add(y, grave(x, y, S(y), t))
    w.occ(40, 1200, 290, 1410)
    w.add(1820, cauldron(820, 1820, S(1820)))
    w.occ(760, 1760, 880, 1830)
    for x, y in [(840, 760), (300, 1960)]:
        w.add(y, scarecrow(x, y, S(y)))
    for x, y in [(930, 1480), (250, 1760), (840, 2150)]:
        w.add(y, haystack(x, y, S(y)))
        w.occ(x - 50, y - 30, x + 50, y + 10)
    w.add(2050, fence(20, 2050, 330, 2030, S(2050)))
    w.add(1700, fence(760, 1700, 1060, 1690, S(1700)))
    # ghosts floating, lit pumpkins along the path, candy
    for x, y in [(330, 820), (900, 1360), (160, 1880), (930, 2000)]:
        w.add(y + 40, ghost(x, y, S(y) * 1.4))
    for i, (x, y) in enumerate([(420, 620), (690, 700), (330, 980), (620, 1150), (420, 1300), (660, 1500), (800, 1640), (460, 1700), (720, 1900), (380, 2100), (660, 2250)]):
        w.add(y, jack(x, y, S(y), lit=True, big=1.1))
    for x, y, c in [(980, 1180, '#FF6F91'), (60, 2150, '#6FD3FF'), (1000, 2280, '#FFD23F')]:
        w.add(y, lollipop(x, y, S(y), c))
    w.add(1100, string_lights(560, 1060, 820, 1100, S(1100), sag=40, cols=('#FFC23A', '#FF8A3D', '#FFE36A')))
    w.scatter([(4, lambda x, y, s, r, i: autumn_tree(x, y, s, seed=i)), (2.4, lambda x, y, s, r, i: bare_tree(x, y, s, seed=i)),
               (1.2, lambda x, y, s, r, i: bush(x, y, s, r.choice(['#B8B04A', '#9AA84A']), r.choice([None, '#FF8A3D']))),
               (0.8, lambda x, y, s, r, i: jack(x, y, s, lit=False))], density=0.34)
    w.fg = ''.join(autumn_tree(x, y, s, seed=600 + k) for k, (x, y, s) in enumerate([(70, 2440, 2.1), (1030, 2450, 2.0), (330, 2510, 1.6), (780, 2520, 1.6)]))
    w.fg += f'<rect width="{W}" height="{H}" fill="#3A2848" opacity="0.08"/>'
    return w.render()


BUILDERS = {'halloween': halloween}
