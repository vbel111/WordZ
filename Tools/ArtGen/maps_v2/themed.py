"""Themed outdoor maps (v2): SPORT, MUSIC, CINEMA, COUNTRIES, SCHOOL, JOBS, BODY, CLOTHES, MEALS."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from props import (T, apple_tree, balloon, bench, bunting, cone, crate, fence, flagpole, hi, house, lamp,  # noqa: E402
                   palm, parasol_table, pine, rock, shadow, stall, suitcase)
from scene import (H, OL, VX, W, Scene, combine, hills, lin, rad, shade, sparkle, tex_dashes, tex_edge_dots,  # noqa: E402
                   tex_lanes, tex_planks, tex_stones, tex_tiles)
from style import PALETTE as PAL, bird, bush, cloud, flower, grass_tuft, mix, round_tree  # noqa: E402

FLOWERS = ['#FF7FA8', '#FFFFFF', '#FFD23F', '#C58BF2', '#FF9A3C']
DAY_SKY = [(0, '#6FBDEB'), (0.55, '#BFE4F8'), (0.88, '#F3F7DE'), (1, '#E6F3CF')]
WARM_SKY = [(0, '#7CC4F0'), (0.5, '#CFEBFA'), (0.85, '#FFE7B8'), (1, '#FFD9A0')]
DUSK_SKY = [(0, '#3B3E8F'), (0.45, '#7C5BB5'), (0.75, '#E78AA8'), (1, '#FFC98A')]
NIGHT_SKY = [(0, '#1D2160'), (0.6, '#3B3F99'), (1, '#7A63B8')]
CLOUDS = [(200, 170, 1.1, 1), (790, 110, 0.85, 0.95), (560, 330, 0.6, 0.9), (980, 360, 0.8, 0.95), (110, 520, 0.6, 0.85)]
GRASS = [(0, '#CFE7AE'), (0.18, '#A6D77A'), (1, '#74C14E')]
TREES = ['#6CC24A', '#5DB03E', '#7CCB4E']


def trees_and_bushes(sc, **kw):
    return [(3, lambda x, y, s: round_tree(x, y, s, sc.r.choice(TREES))), (2, bush)]


def meadow_fill(sc, n_tuft=90, n_flower=50, off=(30, 520)):
    sc.scatter(lambda x, y, s: grass_tuft(x, y, 0.5 + 1.0 * s, '#4E9F36'), n_tuft, 0.05, 1.02, *off)
    sc.scatter(lambda x, y, s: flower(x, y, 0.4 + 0.9 * s, sc.r.choice(FLOWERS)), n_flower, 0.1, 1.02, *off)


def strip(sc, side, off0, off1, t0, t1, fill, stroke=OL, sw=5):
    """A ground patch beside the path in perspective (pitch, court, flower bed, carpet edge...)."""
    pa, pb = [], []
    for i in range(31):
        t = t0 + (t1 - t0) * i / 30
        pa.append((sc.side_x(t, side, off0), sc.ty(t)))
        pb.append((sc.side_x(t, side, off1), sc.ty(t)))
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pa) + ' L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(pb)) + ' Z'
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'


def line_at(sc, side, off0, off1, t, color='#FFFFFF', w=4):
    return (f'<line x1="{sc.side_x(t, side, off0):.1f}" y1="{sc.ty(t):.1f}" x2="{sc.side_x(t, side, off1):.1f}" y2="{sc.ty(t):.1f}" '
            f'stroke="{color}" stroke-width="{w * sc.scale(t):.1f}"/>')


def line_along(sc, side, off, t0, t1, color='#FFFFFF', w=4):
    pts = [(sc.side_x(t0 + (t1 - t0) * i / 20, side, off), sc.ty(t0 + (t1 - t0) * i / 20)) for i in range(21)]
    return f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}" stroke="{color}" stroke-width="{w}" fill="none"/>'


# =====================================================================================
# SPORT
# =====================================================================================

def goal(x, y, s, flip=False):
    net = ''.join(f'<line x1="{-60 + k * 15}" y1="-70" x2="{-50 + k * 13}" y2="-6" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/>' for k in range(9))
    net += ''.join(f'<line x1="-60" y1="{-60 + k * 14}" x2="60" y2="{-60 + k * 14}" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/>' for k in range(4))
    b = shadow(70) + net + '<path d="M-64 0 L-64 -76 L64 -76 L64 0" fill="none" stroke="#FFFFFF" stroke-width="10"/>' \
        '<path d="M-64 0 L-64 -76 L64 -76 L64 0" fill="none" stroke-width="3"/>'
    return T(x, y, s, b, flip)


def ball(x, y, s, kind='soccer'):
    if kind == 'soccer':
        b = (shadow(16) + '<circle cx="0" cy="-16" r="16" fill="#FFFFFF"/><path d="M0 -24 l7 5 l-3 8 l-8 0 l-3 -8 Z" fill="#3A3A44" stroke="none"/>'
             '<path d="M-14 -22 l4 -2 M14 -22 l-4 -2 M-8 -2 l3 -4 M8 -2 l-3 -4" stroke-width="3"/>')
    elif kind == 'basket':
        b = (shadow(16) + '<circle cx="0" cy="-16" r="16" fill="#F08A24"/><path d="M-16 -16 h32 M0 -32 v32 M-11 -28 q8 12 0 24 M11 -28 q-8 12 0 24" fill="none" stroke-width="2.5"/>')
    else:
        b = shadow(10) + '<circle cx="0" cy="-10" r="10" fill="#D7F04A"/><path d="M-8 -16 q8 6 0 14 M8 -4 q-8 -6 0 -14" fill="none" stroke="#FFFFFF" stroke-width="2"/>'
    return T(x, y, s, b)


def stadium(cx, base, w, h):
    """Big stadium bowl on the horizon with floodlights and flags."""
    out = [f'<path d="M{cx - w / 2} {base} L{cx - w / 2 + 30} {base - h} Q{cx} {base - h - 60} {cx + w / 2 - 30} {base - h} L{cx + w / 2} {base} Z" '
           f'fill="#E9EEF5" stroke="{OL}" stroke-width="7" stroke-linejoin="round"/>']
    for k in range(5):
        yy = base - h + 30 + k * (h - 40) / 5
        out.append(f'<path d="M{cx - w / 2 + 34 - k * 6} {yy} Q{cx} {yy - 50 + k * 4} {cx + w / 2 - 34 + k * 6} {yy}" stroke="{["#E5533D", "#4FA3E3", "#FFC93C", "#6CC24A", "#E5533D"][k]}" '
                   f'stroke-width="14" fill="none"/>')
    for k in range(9):
        ax = cx - w / 2 + 60 + k * (w - 120) / 8
        out.append(f'<path d="M{ax} {base} L{ax} {base - 50}" stroke="{OL}" stroke-width="5"/><path d="M{ax - 16} {base - 50} L{ax + 16} {base - 50} L{ax + 10} {base - 26} L{ax - 10} {base - 26} Z" fill="#3A4C68" stroke="{OL}" stroke-width="4"/>')
    for fx in (cx - w / 2 + 40, cx + w / 2 - 40):
        out.append(f'<rect x="{fx - 4}" y="{base - h - 170}" width="8" height="170" fill="#9AA6B8" stroke="{OL}" stroke-width="4"/>'
                   f'<rect x="{fx - 34}" y="{base - h - 200}" width="68" height="36" rx="6" fill="#FFF3C4" stroke="{OL}" stroke-width="5"/>'
                   f'<circle cx="{fx}" cy="{base - h - 182}" r="90" fill="#FFF3C4" opacity="0.25"/>')
    for k, c in enumerate(['#E5533D', '#4FA3E3', '#FFC93C', '#6CC24A', '#C58BF2']):
        fx = cx - 160 + k * 80
        out.append(f'<line x1="{fx}" y1="{base - h - 40}" x2="{fx}" y2="{base - h - 100}" stroke="{OL}" stroke-width="4"/>'
                   f'<path d="M{fx} {base - h - 100} l34 10 l-34 10 Z" fill="{c}" stroke="{OL}" stroke-width="3"/>')
    return ''.join(out)


def bleachers(x, y, s, c='#4FA3E3'):
    b = shadow(110)
    for k in range(4):
        b += f'<rect x="{-110 + k * 8}" y="{-24 - k * 24}" width="{220 - k * 16}" height="24" fill="{c if k % 2 == 0 else shade(c, 0.25)}"/>'
    b += '<path d="M-110 0 L-110 -24 M110 0 L110 -24" stroke-width="5"/>'
    return T(x, y, s, b)


def sport():
    sc = Scene(seed=61, curve=40, curve_freq=1.0, path_w=(80, 520))
    sc.sky(DAY_SKY, sun=(880, 300, 64, '#FFE39A'), clouds=CLOUDS[:4], birds=[(300, 260, 1)])
    hz = sc.horizon
    sc.backdrop(hills(hz, [('#B5DBA6', 40)], seed=3))
    sc.backdrop(stadium(VX, hz + 10, 760, 230))
    sc.ground(GRASS)
    # football pitch (left) and tennis court (right)
    sc.backdrop(strip(sc, -1, 60, 560, 0.18, 0.62, 'url(#pitchG)'))
    sc.defs.append(lin('pitchG', [(0, '#7BC95A', 1), (1, '#5DB845', 1)]))
    for k in range(10):
        t0 = 0.18 + 0.044 * k
        if k % 2 == 0:
            sc.backdrop(strip(sc, -1, 60, 560, t0, t0 + 0.044, '#6CC24A', stroke='none', sw=0))
    sc.backdrop(strip(sc, -1, 60, 560, 0.18, 0.62, 'none', stroke='#FFFFFF', sw=5))
    sc.backdrop(line_at(sc, -1, 60, 560, 0.40))
    sc.backdrop(strip(sc, 1, 70, 420, 0.42, 0.86, '#4F8FD8'))
    sc.backdrop(strip(sc, 1, 100, 390, 0.46, 0.82, 'none', stroke='#FFFFFF', sw=5))
    sc.backdrop(line_along(sc, 1, 245, 0.46, 0.82, '#FFFFFF', 4))
    # tennis net across the court
    na, nb = sc.side_x(0.64, 1, 70), sc.side_x(0.64, 1, 420)
    s64 = sc.scale(0.64)
    sc.add(sc.ty(0.64), f'<rect x="{na:.0f}" y="{sc.ty(0.64) - 44 * s64:.0f}" width="{nb - na:.0f}" height="{44 * s64:.0f}" fill="#FFFFFF" fill-opacity="0.35" stroke="{OL}" stroke-width="4"/>'
           + ''.join(f'<line x1="{na + (nb - na) * k / 16:.0f}" y1="{sc.ty(0.64) - 44 * s64:.0f}" x2="{na + (nb - na) * k / 16:.0f}" y2="{sc.ty(0.64):.0f}" stroke="#FFFFFF" stroke-width="2"/>' for k in range(1, 16))
           + f'<rect x="{na:.0f}" y="{sc.ty(0.64) - 48 * s64:.0f}" width="{nb - na:.0f}" height="{8 * s64:.0f}" fill="#FFFFFF" stroke="{OL}" stroke-width="3"/>')
    sc.place(goal, 0.2, -1, 270)
    sc.place(goal, 0.6, -1, 270)
    sc.path('url(#trackG)', texture=tex_lanes('#FFFFFF', 5, 0.85), border=('#FFFFFF', 6))
    sc.defs.append(lin('trackG', [(0, '#E48A62', 1), (1, '#D9603F', 1)]))
    for t, side, off, k in [(0.3, -1, 300, 'soccer'), (0.52, -1, 200, 'soccer'), (0.7, 1, 180, 'tennis'), (0.75, 1, 300, 'tennis'),
                            (0.9, -1, 140, 'basket'), (0.95, 1, 120, 'soccer')]:
        sc.place(ball, t, side, off, k)
    for t in (0.66, 0.72, 0.78, 0.84):
        sc.place(cone, t, -1, 40 + (t - 0.66) * 300)
    sc.place(bleachers, 0.1, 1, 150)
    sc.place(bleachers, 0.28, 1, 180, '#E5533D')
    sc.place(lambda x, y, s: flagpole(x, y, s, '#E5533D'), 0.08, -1, 40)
    sc.place(lambda x, y, s: flagpole(x, y, s, '#4FA3E3'), 0.08, 1, 40)
    sc.populate(trees_and_bushes(sc), t0=0.62, gap=150, start=(200, 260), sides=(-1,), step=0.06)
    sc.populate(trees_and_bushes(sc), t0=0.86, gap=150, start=(160, 220), sides=(1,), step=0.06)
    sc.populate(trees_and_bushes(sc), t1=0.42, gap=150, start=(440, 470), sides=(1,), step=0.06)
    for x, t, s in [(-10, 0.92, 1.25), (1090, 0.96, 1.25)]:
        sc.at(round_tree, x, t, s, '#6CC24A')
    sc.scatter(lambda x, y, s: grass_tuft(x, y, 0.5 + s, '#4E9F36'), 40, 0.62, 1.02, 40, 500)
    sc.haze()
    sc.bottom_fade()
    return sc.render()


# =====================================================================================
# MUSIC (evening open-air concert, piano-key path)
# =====================================================================================

def speaker(x, y, s):
    b = shadow(40) + '<rect x="-36" y="-130" width="72" height="130" rx="8" fill="#3A3A50"/>'
    for cy, r in ((-96, 22), (-40, 28)):
        b += f'<circle cx="0" cy="{cy}" r="{r}" fill="#5A5A78"/><circle cx="0" cy="{cy}" r="{r * 0.4:.0f}" fill="#22222F"/>'
    b += hi(-24, -118, 6, 4, 0.4)
    return T(x, y, s, b)


def note_sign(x, y, s, c='#C58BF2'):
    b = (shadow(16) + '<rect x="-4" y="-80" width="8" height="80" fill="#8A5326"/>'
         f'<path d="M12 -160 L12 -96" stroke-width="12"/><path d="M12 -160 L12 -96" stroke="{c}" stroke-width="5"/>'
         f'<ellipse cx="-4" cy="-94" rx="20" ry="15" fill="{c}" transform="rotate(-20 -4 -94)"/>'
         f'<path d="M12 -160 q30 10 26 40 q-6 -18 -26 -20 Z" fill="{c}"/>')
    return T(x, y, s, b)


def drum(x, y, s, c='#E5533D'):
    b = (shadow(50) + f'<rect x="-50" y="-80" width="100" height="70" fill="{c}"/><ellipse cx="0" cy="-10" rx="50" ry="14" fill="{shade(c, -0.2)}"/>'
         '<ellipse cx="0" cy="-80" rx="50" ry="14" fill="#FBF1DE"/>'
         + ''.join(f'<path d="M{-46 + k * 23} -72 L{-34 + k * 23} -16" stroke="#FFC93C" stroke-width="4"/>' for k in range(4)) +
         '<path d="M-30 -96 l40 -50 M20 -100 l30 -46" stroke="#E9C48A" stroke-width="8"/>')
    return T(x, y, s, b)


def guitar(x, y, s, c='#F08A24'):
    b = (shadow(40) + f'<path d="M-30 -10 Q-56 -40 -36 -70 Q-48 -100 -20 -112 Q0 -120 16 -104 Q40 -96 32 -68 Q54 -36 26 -10 Q0 4 -30 -10 Z" fill="{c}"/>'
         '<circle cx="0" cy="-64" r="12" fill="#5A3A1A"/><rect x="-6" y="-230" width="14" height="140" fill="#8A5326" transform="rotate(8 0 -100)"/>'
         '<rect x="-2" y="-260" width="26" height="36" rx="6" fill="#5A3A1A" transform="rotate(8 0 -100)"/>'
         '<rect x="-18" y="-40" width="36" height="8" fill="#5A3A1A"/>')
    return T(x, y, s, b)


def stage(cx, base, w, h):
    out = []
    # light beams
    for k, c in enumerate(['#FFE9A6', '#C58BF2', '#7FD0F5', '#FF9EC4', '#FFE9A6']):
        bx = cx - w / 2 + 40 + k * (w - 80) / 4
        tx = bx + (k - 2) * 160
        out.append(f'<path d="M{bx - 10} {base - h} L{tx - 90} 80 L{tx + 90} 80 L{bx + 10} {base - h} Z" fill="{c}" opacity="0.22"/>')
    out.append(f'<rect x="{cx - w / 2}" y="{base - 60}" width="{w}" height="70" fill="#3A3A50" stroke="{OL}" stroke-width="7"/>'
               f'<path d="M{cx - w / 2 - 20} {base - h} L{cx + w / 2 + 20} {base - h} L{cx + w / 2} {base - 60} L{cx - w / 2} {base - 60} Z" fill="#2A2A3C" stroke="{OL}" stroke-width="7"/>'
               f'<path d="M{cx - w / 2 - 30} {base - h - 40} Q{cx} {base - h - 120} {cx + w / 2 + 30} {base - h - 40} L{cx + w / 2 + 30} {base - h} L{cx - w / 2 - 30} {base - h} Z" '
               f'fill="#7C3AB5" stroke="{OL}" stroke-width="7"/>')
    for k in range(10):
        lx = cx - w / 2 + 10 + k * w / 9
        out.append(f'<circle cx="{lx:.0f}" cy="{base - h - 20}" r="10" fill="{["#FFE9A6", "#FF9EC4", "#7FD0F5"][k % 3]}" stroke="{OL}" stroke-width="3"/>')
    # curtains
    out.append(f'<path d="M{cx - w / 2} {base - h} L{cx - w / 2 + 70} {base - h} Q{cx - w / 2 + 40} {base - 120} {cx - w / 2 + 10} {base - 60} L{cx - w / 2} {base - 60} Z" fill="#C0392B" stroke="{OL}" stroke-width="5"/>'
               f'<path d="M{cx + w / 2} {base - h} L{cx + w / 2 - 70} {base - h} Q{cx + w / 2 - 40} {base - 120} {cx + w / 2 - 10} {base - 60} L{cx + w / 2} {base - 60} Z" fill="#C0392B" stroke="{OL}" stroke-width="5"/>')
    return ''.join(out)


def string_lights(sc, t, side_span=True):
    y = sc.ty(t)
    s = sc.scale(t)
    x0, x1 = sc.side_x(t, -1, 60), sc.side_x(t, 1, 60)
    yy = y - 150 * s
    out = f'<path d="M{x0:.0f} {yy:.0f} Q{(x0 + x1) / 2:.0f} {yy + 60 * s:.0f} {x1:.0f} {yy:.0f}" stroke="{OL}" stroke-width="{2.5 * s:.1f}" fill="none"/>'
    n = 12
    for k in range(1, n):
        u = k / n
        px = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * (x0 + x1) / 2 + u * u * x1
        py = (1 - u) ** 2 * yy + 2 * (1 - u) * u * (yy + 60 * s) + u * u * yy
        c = ['#FFE9A6', '#FF9EC4', '#7FD0F5', '#B6F07A'][k % 4]
        out += f'<circle cx="{px:.0f}" cy="{py + 6 * s:.0f}" r="{14 * s:.1f}" fill="{c}" opacity="0.35"/><circle cx="{px:.0f}" cy="{py + 6 * s:.0f}" r="{6 * s:.1f}" fill="{c}" stroke="{OL}" stroke-width="{2 * s:.1f}"/>'
    return out


def tex_piano(sc):
    out = []
    n = 26
    for i in range(n):
        ta, tb = (i / n) ** 1.5 * 1.02, ((i + 0.55) / n) ** 1.5 * 1.02
        for side in (-1, 1):
            xa = sc.path_cx(ta) + side * sc.path_half(ta) * 0.05
            xb = sc.path_cx(ta) + side * sc.path_half(ta) * 0.62
            xc = sc.path_cx(tb) + side * sc.path_half(tb) * 0.62
            xd = sc.path_cx(tb) + side * sc.path_half(tb) * 0.05
            if i % 7 in (2, 6):
                continue
            out.append(f'<path d="M{xa:.1f} {sc.ty(ta):.1f} L{xb:.1f} {sc.ty(ta):.1f} L{xc:.1f} {sc.ty(tb):.1f} L{xd:.1f} {sc.ty(tb):.1f} Z" fill="#2A2A3C"/>')
        tl = ((i + 1) / n) ** 1.5 * 1.02
        out.append(f'<line x1="{sc.path_cx(tl) - sc.path_half(tl):.1f}" y1="{sc.ty(tl):.1f}" x2="{sc.path_cx(tl) + sc.path_half(tl):.1f}" y2="{sc.ty(tl):.1f}" stroke="#B9B2C8" stroke-width="{1 + 3 * tl:.1f}"/>')
    return ''.join(out)


def music():
    sc = Scene(seed=71, curve=60, curve_freq=1.2, path_w=(70, 440))
    sc.sky(DUSK_SKY, stars=60, moon=(170, 260, 50))
    hz = sc.horizon
    sc.backdrop(hills(hz, [('#6E5AA8', 140), ('#5F7FB0', 60)], seed=8))
    sc.backdrop(stage(VX, hz + 6, 560, 300))
    sc.ground([(0, '#8DB98A'), (0.2, '#7DB66A'), (1, '#5FA94A')])
    sc.path('#FBF6EE', texture=tex_piano, border=('#2A2A3C', 10))
    for t in (0.12, 0.3, 0.55, 0.85):
        sc.add(sc.ty(t) - 1, string_lights(sc, t))
    for t in (0.1, 0.32):
        sc.place(speaker, t, -1, 60)
        sc.place(speaker, t, 1, 60)
    sc.place(drum, 0.45, -1, 160)
    sc.place(guitar, 0.62, 1, 170)
    sc.place(drum, 0.8, 1, 260, '#4FA3E3')
    sc.place(guitar, 0.9, -1, 180, '#E5533D')
    for t, side, c in [(0.22, -1, '#C58BF2'), (0.4, 1, '#FF9EC4'), (0.7, -1, '#7FD0F5'), (0.97, 1, '#FFC93C')]:
        sc.place(note_sign, t, side, 70, c)
    for t in (0.2, 0.5, 0.78):
        sc.place(lamp, t, 1, 40, '#FFE9A6')
        sc.place(lamp, t + 0.04, -1, 40, '#FFE9A6')
    sc.populate([(3, lambda x, y, s: round_tree(x, y, s, sc.r.choice(['#4FA65A', '#5DB03E']))), (2, lambda x, y, s: bush(x, y, s, '#4E9F36'))],
                gap=150, start=(320, 400), step=0.06)
    sc.scatter(lambda x, y, s: grass_tuft(x, y, 0.5 + s, '#3E8E2F'), 60, 0.05, 1.02, 40, 520)
    sc.scatter(lambda x, y, s: sparkle(x, y - 60 * s, 0.4 + 0.5 * s, '#FFE9A6', 0.8), 30, 0.05, 1.0, 60, 520)
    sc.haze('#C6A4E0', 300, 0.45)
    sc.bottom_fade(0.25)
    return sc.render()


# =====================================================================================
# CINEMA (red carpet to the premiere)
# =====================================================================================

def rope_post(x, y, s):
    b = (shadow(14) + '<rect x="-12" y="-6" width="24" height="8" rx="3" fill="#E99A12"/><rect x="-5" y="-70" width="10" height="66" fill="#FFC93C"/>'
         '<circle cx="0" cy="-74" r="9" fill="#FFC93C"/>' + hi(-2, -76, 3, 3, 0.7))
    return T(x, y, s, b)


def ropes(sc, side, off, t0, t1, n):
    out = []
    ts = [t0 + (t1 - t0) * (k / n) ** 1.3 for k in range(n + 1)]
    for a, b in zip(ts, ts[1:]):
        xa, ya, sa = sc.side_x(a, side, off), sc.ty(a), sc.scale(a)
        xb, yb, sb = sc.side_x(b, side, off), sc.ty(b), sc.scale(b)
        out.append((yb - 1, f'<path d="M{xa:.1f} {ya - 64 * sa:.1f} Q{(xa + xb) / 2:.1f} {(ya + yb) / 2 - 30 * (sa + sb) / 2:.1f} {xb:.1f} {yb - 64 * sb:.1f}" '
                            f'stroke="{OL}" stroke-width="{9 * sb:.1f}" fill="none"/><path d="M{xa:.1f} {ya - 64 * sa:.1f} Q{(xa + xb) / 2:.1f} {(ya + yb) / 2 - 30 * (sa + sb) / 2:.1f} {xb:.1f} {yb - 64 * sb:.1f}" '
                            f'stroke="#C0392B" stroke-width="{5 * sb:.1f}" fill="none"/>'))
    for t in ts:
        out.append((sc.ty(t), rope_post(sc.side_x(t, side, off), sc.ty(t), sc.scale(t))))
    return out


def popcorn(x, y, s):
    b = shadow(40) + '<path d="M-40 -110 L40 -110 L30 0 L-30 0 Z" fill="#FFFFFF"/>'
    for k in range(4):
        b += f'<path d="M{-36 + k * 20} -110 L{-26 + k * 15} 0 L{-18 + k * 15} 0 L{-26 + k * 20} -110 Z" fill="#E5533D" stroke="none"/>'
    b += '<path d="M-40 -110 L40 -110 L30 0 L-30 0 Z" fill="none"/>'
    for cx, cy in [(-30, -118), (-10, -126), (10, -122), (28, -116), (0, -140), (-20, -136), (20, -138)]:
        b += f'<circle cx="{cx}" cy="{cy}" r="13" fill="#FFF3C4" stroke-width="3"/>'
    return T(x, y, s, b)


def film_reel(x, y, s):
    b = shadow(40) + '<circle cx="0" cy="-56" r="54" fill="#3A3A50"/><circle cx="0" cy="-56" r="10" fill="#9AA6B8"/>'
    for k in range(6):
        a = k * math.pi / 3
        b += f'<circle cx="{math.cos(a) * 30:.0f}" cy="{-56 + math.sin(a) * 30:.0f}" r="12" fill="#9AA6B8"/>'
    b += '<path d="M40 -20 q40 10 70 18" stroke-width="16" fill="none"/><path d="M40 -20 q40 10 70 18" stroke="#3A3A50" stroke-width="10" fill="none"/>'
    return T(x, y, s, b)


def clapper(x, y, s):
    b = (shadow(50) + '<rect x="-50" y="-70" width="100" height="70" rx="6" fill="#3A3A50"/>'
         '<path d="M-52 -74 L46 -110 L54 -90 L-44 -54 Z" fill="#FFFFFF"/>'
         + ''.join(f'<path d="M{-40 + k * 22} {-64 - k * 8} l10 18 l12 -4 l-10 -18 Z" fill="#3A3A50" stroke="none"/>' for k in range(4)) +
         '<rect x="-38" y="-46" width="76" height="6" fill="#FFFFFF" stroke="none" opacity="0.8"/><rect x="-38" y="-28" width="50" height="6" fill="#FFFFFF" stroke="none" opacity="0.8"/>')
    return T(x, y, s, b)


def star_tile(x, y, s):
    pts = []
    for k in range(10):
        r = 26 if k % 2 == 0 else 11
        a = -math.pi / 2 + k * math.pi / 5
        pts.append(f'{math.cos(a) * r:.1f} {math.sin(a) * r * 0.45:.1f}')
    b = '<ellipse cx="0" cy="0" rx="40" ry="16" fill="#E8A0A0"/>' + f'<path d="M{" L".join(pts)} Z" fill="#FFC93C" stroke-width="3"/>'
    return T(x, y, s, b)


def cinema_building(cx, base, w, h):
    out = []
    for k, c in enumerate(['#FFF3C4', '#FFE9A6']):
        for sgn in (-1, 1):
            out.append(f'<path d="M{cx + sgn * (w / 2 - 40)} {base - h - 10} L{cx + sgn * (w / 2 + 260 + k * 120)} 0 L{cx + sgn * (w / 2 + 120 + k * 120)} 0 Z" fill="{c}" opacity="0.18"/>')
    out.append(f'<rect x="{cx - w / 2}" y="{base - h}" width="{w}" height="{h}" fill="#F2D7A6" stroke="{OL}" stroke-width="7"/>')
    out.append(f'<path d="M{cx - w / 2 - 20} {base - h} L{cx} {base - h - 120} L{cx + w / 2 + 20} {base - h} Z" fill="#C0392B" stroke="{OL}" stroke-width="7" stroke-linejoin="round"/>')
    out.append(f'<circle cx="{cx}" cy="{base - h - 50}" r="34" fill="#FFC93C" stroke="{OL}" stroke-width="5"/>')
    # marquee
    my = base - h + 40
    out.append(f'<rect x="{cx - w / 2 + 30}" y="{my}" width="{w - 60}" height="90" rx="10" fill="#3A3A50" stroke="{OL}" stroke-width="6"/>')
    for k in range(16):
        out.append(f'<circle cx="{cx - w / 2 + 42 + k * (w - 84) / 15:.0f}" cy="{my + 10}" r="6" fill="#FFE9A6"/>'
                   f'<circle cx="{cx - w / 2 + 42 + k * (w - 84) / 15:.0f}" cy="{my + 80}" r="6" fill="#FFE9A6"/>')
    for k in range(4):
        out.append(f'<rect x="{cx - 120 + k * 64}" y="{my + 32}" width="44" height="26" rx="4" fill="#FFF3C4" stroke="{OL}" stroke-width="3"/>')
    # columns and doors
    for k in range(5):
        px = cx - w / 2 + 40 + k * (w - 80) / 4
        out.append(f'<rect x="{px - 10}" y="{my + 100}" width="20" height="{base - my - 100}" fill="#FBF1DE" stroke="{OL}" stroke-width="5"/>')
    out.append(f'<path d="M{cx - 40} {base} L{cx - 40} {base - 70} Q{cx} {base - 100} {cx + 40} {base - 70} L{cx + 40} {base} Z" fill="#7A4520" stroke="{OL}" stroke-width="5"/>')
    return ''.join(out)


def cinema():
    sc = Scene(seed=81, curve=0, path_w=(90, 380))
    sc.sky(NIGHT_SKY, stars=120)
    hz = sc.horizon
    sc.backdrop(cinema_building(VX, hz + 6, 520, 300))
    for x in (120, 960):
        sc.backdrop(f'<g opacity="0.65">{palm(x, hz, 0.7)}</g>')
    sc.ground([(0, '#C9A8C8'), (0.2, '#C7929F'), (1, '#B77C8C')])
    # pavement with star tiles both sides, then red carpet with gold edge
    sc.backdrop(strip(sc, -1, 0, 520, 0.0, 1.03, '#E9C9B8', stroke='none', sw=0) + strip(sc, 1, 0, 520, 0.0, 1.03, '#E9C9B8', stroke='none', sw=0))
    sc.path('url(#carpetG)', border=('#FFC93C', 10))
    sc.defs.append(lin('carpetG', [(0, '#D2423A', 1), (1, '#B5282B', 1)]))
    t = 0.08
    while t < 1.0:
        for side in (-1, 1):
            sc.place(star_tile, t, side, 210)
        t += 0.06 + 0.07 * t
    for it in ropes(sc, -1, 30, 0.05, 1.02, 14) + ropes(sc, 1, 30, 0.05, 1.02, 14):
        sc.add(*it)
    sc.place(popcorn, 0.48, -1, 300)
    sc.place(film_reel, 0.7, 1, 320)
    sc.place(clapper, 0.32, 1, 260)
    sc.place(popcorn, 0.9, 1, 230)
    sc.place(clapper, 0.86, -1, 340)
    sc.place(film_reel, 0.22, -1, 260)
    for t in (0.14, 0.4, 0.62, 0.95):
        sc.place(lamp, t, -1, 120, '#FFE9A6')
        sc.place(lamp, t, 1, 120, '#FFE9A6')
    sc.populate([(2, palm), (1, lambda x, y, s: bush(x, y, s, '#4E9F36'))], gap=170, start=(420, 470), step=0.07)
    sc.scatter(lambda x, y, s: sparkle(x, y - 80 * s, 0.4 + 0.5 * s, '#FFE9A6', 0.9), 30, 0.05, 1.0, 40, 520)
    sc.haze('#9C7CC8', 300, 0.4)
    sc.bottom_fade(0.25)
    return sc.render()



# =====================================================================================
# shared: shop / workplace building (front face + side face toward the road)
# =====================================================================================

def _glyph(kind):
    """Small window / sign decoration per shop kind, centred at (0,0), ~60 units."""
    if kind == 'dress':
        return ('<path d="M-6 -30 L6 -30 L8 -16 L22 24 L-22 24 L-8 -16 Z" fill="#FF7FA8"/><path d="M-6 -30 q6 -10 12 0" fill="none" stroke-width="3"/>')
    if kind == 'shirt':
        return '<path d="M-24 -20 L-10 -28 Q0 -20 10 -28 L24 -20 L18 -6 L12 -10 L12 24 L-12 24 L-12 -10 L-18 -6 Z" fill="#4FA3E3"/>'
    if kind == 'shoe':
        return '<path d="M-26 14 L-24 -10 L-10 -10 Q-4 2 14 4 Q28 8 26 16 Z" fill="#E5533D"/><rect x="-26" y="12" width="52" height="6" fill="#FFFFFF"/>'
    if kind == 'hat':
        return '<ellipse cx="0" cy="12" rx="30" ry="8" fill="#C58BF2"/><path d="M-16 12 Q-16 -18 0 -18 Q16 -18 16 12 Z" fill="#C58BF2"/><rect x="-16" y="2" width="32" height="6" fill="#FF7FA8" stroke="none"/>'
    if kind == 'bread':
        return '<path d="M-28 10 Q-30 -14 0 -16 Q30 -14 28 10 Z" fill="#E9A23B"/><path d="M-14 -10 l6 10 M0 -12 l6 10 M14 -10 l6 10" stroke-width="3"/>'
    if kind == 'cross':
        return '<circle cx="0" cy="0" r="26" fill="#FFFFFF"/><path d="M-6 -18 h12 v12 h12 v12 h-12 v12 h-12 v-12 h-12 v-12 h12 Z" fill="#E5533D"/>'
    if kind == 'fire':
        return '<path d="M0 -24 Q18 -6 12 10 Q8 22 0 22 Q-14 22 -14 8 Q-14 -6 -4 -12 Q-4 0 2 2 Q6 -10 0 -24 Z" fill="#FFB21E"/>'
    if kind == 'wrench':
        return '<path d="M-20 18 L6 -8 Q2 -22 14 -26 L8 -18 L14 -12 L22 -18 Q18 -6 6 -6 L-14 24 Z" fill="#9AA6B8"/>'
    if kind == 'book':
        return '<path d="M-26 -16 Q-12 -22 0 -14 Q12 -22 26 -16 L26 18 Q12 12 0 20 Q-12 12 -26 18 Z" fill="#FFFFFF"/><path d="M0 -14 L0 20" stroke-width="3"/>'
    if kind == 'cup':
        return '<path d="M-18 -14 L14 -14 L10 18 L-14 18 Z" fill="#FFFFFF"/><path d="M14 -6 q12 0 10 10 q-2 8 -12 6" fill="none" stroke-width="4"/><path d="M-6 -22 q4 -6 0 -12 M4 -22 q4 -6 0 -12" fill="none" stroke-width="3"/>'
    return '<circle cx="0" cy="0" r="20" fill="#FFC93C"/>'


def shop(x, y, s, wall='#F6D9A8', roof='#E5533D', kind='dress', flip=False, tall=1.0, awning=None):
    w, h = 210, 230 * tall
    awning = awning or roof
    b = shadow(120, 18)
    b += f'<path d="M{w / 2} {-h} L{w / 2 + 50} {-h + 16} L{w / 2 + 50} -6 L{w / 2} 0 Z" fill="{shade(wall, -0.22)}"/>'
    b += f'<rect x="{-w / 2}" y="{-h}" width="{w}" height="{h}" fill="{wall}"/>'
    b += f'<rect x="{-w / 2 - 8}" y="{-h - 18}" width="{w + 16}" height="22" fill="{roof}"/>'
    b += f'<rect x="{-w / 2 + 6}" y="{-h + 6}" width="18" height="{h - 12}" fill="#FFFFFF" opacity="0.2" stroke="none"/>'
    # upper windows
    if tall > 1.15:
        for k in range(3):
            b += (f'<rect x="{-w / 2 + 24 + k * 62}" y="{-h + 30}" width="40" height="46" rx="6" fill="{PAL["windowLit"] if k == 1 else PAL["window"]}"/>'
                  f'<path d="M{-w / 2 + 30 + k * 62} {-h + 66} l18 -26" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/>')
    # sign
    b += f'<g transform="translate(0,{-h * 0.56 - (20 if tall > 1.15 else 0)})"><circle cx="0" cy="0" r="34" fill="{shade(awning, 0.75)}"/>' + _glyph(kind) + '</g>'
    # shop window + door
    b += f'<rect x="{-w / 2 + 16}" y="-96" width="110" height="80" rx="6" fill="{PAL["window"]}"/>'
    b += f'<g transform="translate({-w / 2 + 71},-56) scale(0.75)">{_glyph(kind)}</g>'
    b += f'<path d="M{-w / 2 + 26} -30 l30 -50" stroke="#FFFFFF" stroke-width="4" opacity="0.6"/>'
    b += f'<rect x="{w / 2 - 70}" y="-100" width="52" height="100" rx="6" fill="#9A5B27"/><circle cx="{w / 2 - 28}" cy="-50" r="4" fill="#FFC93C"/>'
    for k in range(6):
        xa = -w / 2 - 4 + k * (w + 8) / 6
        b += f'<path d="M{xa:.0f} -126 h{(w + 8) / 6:.1f} v26 q{-(w + 8) / 12:.1f} 12 {-(w + 8) / 6:.1f} 0 Z" fill="{awning if k % 2 == 0 else "#FFFFFF"}"/>'
    return T(x, y, s, b, flip)


def street(sc, side, specs, t0=0.04, t1=0.62, inner=60, gap=0.0):
    """Places shops along one side of the path, nearest row on the kerb and back rows out to the screen edge."""
    t = t0
    k = 0
    while t < t1:
        wall, roof, kind, tall = specs[k % len(specs)]
        sc.place(lambda x, y, s, a=(wall, roof, kind, tall): shop(x, y, s, a[0], a[1], a[2], flip=side > 0, tall=a[3]), t, side, inner + 140)
        # back rows
        off = inner + 140 + 290
        j = 1
        while True:
            x = sc.side_x(t - 0.012 * j, side, off)
            if x < -160 or x > W + 160 or t - 0.012 * j < 0.02:
                break
            w2, r2, k2, _ = specs[(k + j * 3) % len(specs)]
            sc.place(lambda x, y, s, a=(w2, r2, k2): shop(x, y, s, a[0], a[1], a[2], flip=side > 0, tall=1.35), t - 0.012 * j, side, off)
            off += 290
            j += 1
        t += 0.06 + 0.11 * t + gap
        k += 1


# =====================================================================================
# COUNTRIES (world plaza: landmarks on the horizon, flags along the path)
# =====================================================================================

FLAGS = [('v', ('#2F5FB5', '#FFFFFF', '#E5533D')), ('h', ('#3A3A44', '#E5533D', '#FFC93C')), ('v', ('#2E9E4A', '#FFFFFF', '#E5533D')),
         ('disc', ('#FFFFFF', '#E5533D')), ('h', ('#FFFFFF', '#2F5FB5', '#E5533D')), ('cross', ('#2F5FB5', '#FFC93C')),
         ('h', ('#E5533D', '#FFFFFF', '#E5533D')), ('v', ('#2E9E4A', '#FFFFFF', '#F08A24')), ('h', ('#2E9E4A', '#FFC93C', '#2F5FB5')),
         ('cross', ('#E5533D', '#FFFFFF')), ('star', ('#E5533D', '#FFC93C')), ('h', ('#FFC93C', '#2F5FB5', '#E5533D'))]


def flag(x, y, s, design):
    kind, cols = design
    fw, fh, fx, fy = 92, 60, 4, -168
    inner = ''
    if kind == 'v':
        for k, c in enumerate(cols):
            inner += f'<rect x="{fx + k * fw / 3:.1f}" y="{fy}" width="{fw / 3 + 0.5:.1f}" height="{fh}" fill="{c}" stroke="none"/>'
    elif kind == 'h':
        for k, c in enumerate(cols):
            inner += f'<rect x="{fx}" y="{fy + k * fh / 3:.1f}" width="{fw}" height="{fh / 3 + 0.5:.1f}" fill="{c}" stroke="none"/>'
    elif kind == 'disc':
        inner = f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{cols[0]}" stroke="none"/><circle cx="{fx + fw / 2}" cy="{fy + fh / 2}" r="16" fill="{cols[1]}" stroke="none"/>'
    elif kind == 'cross':
        inner = (f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{cols[0]}" stroke="none"/>'
                 f'<rect x="{fx + 26}" y="{fy}" width="12" height="{fh}" fill="{cols[1]}" stroke="none"/><rect x="{fx}" y="{fy + 24}" width="{fw}" height="12" fill="{cols[1]}" stroke="none"/>')
    else:
        pts = ' '.join(f'{fx + fw / 2 + math.cos(-math.pi / 2 + k * math.pi / 5) * (16 if k % 2 == 0 else 7):.1f},{fy + fh / 2 + math.sin(-math.pi / 2 + k * math.pi / 5) * (16 if k % 2 == 0 else 7):.1f}' for k in range(10))
        inner = f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{cols[0]}" stroke="none"/><polygon points="{pts}" fill="{cols[1]}" stroke="none"/>'
    b = (shadow(16) + '<rect x="-4" y="-180" width="8" height="180" fill="#D8D8D8"/><circle cx="0" cy="-184" r="7" fill="#FFC93C"/>'
         f'<g>{inner}</g><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none"/>'
         f'<path d="M{fx} {fy + 10} h{fw}" stroke="#FFFFFF" stroke-width="4" opacity="0.35"/>')
    return T(x, y, s, b)


def landmarks(hz):
    c1, c2 = '#AFC6E4', '#98B3D8'
    out = []
    # lattice tower
    x = 190
    out.append(f'<path d="M{x - 90} {hz} Q{x - 30} {hz - 160} {x - 12} {hz - 380} L{x} {hz - 470} L{x + 12} {hz - 380} Q{x + 30} {hz - 160} {x + 90} {hz} '
               f'L{x + 50} {hz} Q{x} {hz - 110} {x - 50} {hz} Z" fill="{c2}"/>'
               f'<rect x="{x - 50}" y="{hz - 170}" width="100" height="14" fill="{c2}"/><rect x="{x - 30}" y="{hz - 300}" width="60" height="10" fill="{c2}"/>')
    # pyramid
    out.append(f'<path d="M330 {hz} L440 {hz - 170} L550 {hz} Z" fill="#E6CFA0"/><path d="M440 {hz - 170} L550 {hz} L470 {hz} Z" fill="#D2B57E"/>')
    # onion dome tower
    x = 640
    out.append(f'<rect x="{x - 40}" y="{hz - 230}" width="80" height="230" fill="{c1}"/>'
               f'<path d="M{x - 50} {hz - 230} Q{x - 60} {hz - 300} {x} {hz - 340} Q{x + 60} {hz - 300} {x + 50} {hz - 230} Z" fill="#E59AA0"/>'
               f'<rect x="{x - 3}" y="{hz - 380}" width="6" height="40" fill="#E59AA0"/>')
    # pagoda
    x = 790
    for k in range(4):
        w = 120 - k * 22
        yy = hz - 40 - k * 70
        out.append(f'<rect x="{x - w / 2 + 14}" y="{yy - 50}" width="{w - 28}" height="50" fill="{c1}"/>'
                   f'<path d="M{x - w / 2 - 20} {yy - 44} Q{x} {yy - 80} {x + w / 2 + 20} {yy - 44} L{x + w / 2} {yy - 54} L{x - w / 2} {yy - 54} Z" fill="#D9786A"/>')
    # clock tower
    x = 960
    out.append(f'<rect x="{x - 36}" y="{hz - 360}" width="72" height="360" fill="{c2}"/><path d="M{x - 40} {hz - 360} L{x} {hz - 450} L{x + 40} {hz - 360} Z" fill="{c2}"/>'
               f'<circle cx="{x}" cy="{hz - 310}" r="24" fill="#FFF3C4"/><path d="M{x} {hz - 310} l0 -14 M{x} {hz - 310} l10 4" stroke="#5A6A88" stroke-width="4"/>')
    return ''.join(out)


def globe(x, y, s):
    b = (shadow(50) + '<rect x="-40" y="-20" width="80" height="20" rx="4" fill="#A8642E"/><rect x="-6" y="-60" width="12" height="44" fill="#E99A12"/>'
         '<path d="M-70 -130 A70 70 0 0 0 40 -60" fill="none" stroke="#E99A12" stroke-width="10"/>'
         '<circle cx="-10" cy="-130" r="62" fill="#4FA3E3"/>'
         '<path d="M-50 -160 q20 -10 30 6 q10 18 -8 24 q-16 4 -22 -12 Z M0 -110 q20 -6 26 10 q2 20 -16 22 q-14 -8 -10 -32 Z M10 -176 q16 -4 22 10 q-10 6 -22 -10 Z" fill="#6CC24A" stroke-width="3"/>'
         + hi(-34, -158, 14, 9, 0.45))
    return T(x, y, s, b)


def countries():
    sc = Scene(seed=91, curve=50, curve_freq=1.0, path_w=(100, 520))
    sc.sky(WARM_SKY, sun=(540, 380, 70, '#FFE39A'), clouds=CLOUDS[:3] + [(980, 520, 0.6, 0.9)], birds=[(300, 300, 1), (330, 280, 0.8)])
    hz = sc.horizon
    sc.backdrop(landmarks(hz + 10))
    sc.backdrop(hills(hz, [('#BCDDA2', 20)], seed=5))
    sc.ground(GRASS)
    sc.path('#EFDDB8', texture=combine(tex_tiles('#EFDDB8', '#E4CC9C', 24, 6), tex_edge_dots('#FBF1DE', 0.04)))
    t = 0.05
    k = 0
    while t < 1.0:
        for side in (-1, 1):
            sc.place(flag, t, side, 50, FLAGS[k % len(FLAGS)])
            k += 1
        t += 0.045 + 0.07 * t
    styles = [('#FBE6C4', '#E5533D'), ('#FCE1CF', '#3A7BD5'), ('#FFFFFF', '#2E9E4A'), ('#F6D9A8', '#9B59B6'), ('#E9F2FB', '#E99A12')]
    sc.populate([(2, lambda x, y, s: house(x, y, s, *sc.r.choice(styles), flip=x > VX)), (2, lambda x, y, s: round_tree(x, y, s, sc.r.choice(TREES))),
                 (1, palm), (1, pine), (1, bush)], gap=170, start=(190, 240), step=0.06)
    sc.place(globe, 0.72, -1, 160)
    for t in (0.3, 0.6, 0.9):
        sc.add(sc.ty(t) - 2, bunting(sc.side_x(t, -1, 50), sc.ty(t) - 175 * sc.scale(t), sc.side_x(t, 1, 50), sc.ty(t) - 175 * sc.scale(t), sc.scale(t)))
    meadow_fill(sc, 50, 30, (150, 520))
    sc.haze()
    sc.bottom_fade()
    return sc.render()


# =====================================================================================
# SCHOOL
# =====================================================================================

def school_building(cx, base):
    w, h = 520, 210
    out = [f'<rect x="{cx - w / 2}" y="{base - h}" width="{w}" height="{h}" fill="#D9604A" stroke="{OL}" stroke-width="7"/>']
    for k in range(9):
        out.append(f'<line x1="{cx - w / 2}" y1="{base - h + 20 + k * 22}" x2="{cx + w / 2}" y2="{base - h + 20 + k * 22}" stroke="#C4503C" stroke-width="3"/>')
    out.append(f'<rect x="{cx - w / 2 - 12}" y="{base - h - 20}" width="{w + 24}" height="24" fill="#FBF1DE" stroke="{OL}" stroke-width="6"/>')
    for row in range(2):
        for k in range(8):
            if 3 <= k <= 4 and row == 1:
                continue
            wx = cx - w / 2 + 24 + k * 62
            out.append(f'<rect x="{wx}" y="{base - h + 26 + row * 80}" width="40" height="50" rx="4" fill="{PAL["window"]}" stroke="{OL}" stroke-width="4"/>'
                       f'<line x1="{wx + 20}" y1="{base - h + 26 + row * 80}" x2="{wx + 20}" y2="{base - h + 76 + row * 80}" stroke="{OL}" stroke-width="3"/>')
    # tower
    out.append(f'<rect x="{cx - 60}" y="{base - h - 170}" width="120" height="170" fill="#E5735C" stroke="{OL}" stroke-width="7"/>'
               f'<path d="M{cx - 76} {base - h - 170} L{cx} {base - h - 260} L{cx + 76} {base - h - 170} Z" fill="#4F7FC8" stroke="{OL}" stroke-width="7" stroke-linejoin="round"/>'
               f'<circle cx="{cx}" cy="{base - h - 110}" r="36" fill="#FFF3C4" stroke="{OL}" stroke-width="6"/>'
               f'<path d="M{cx} {base - h - 110} l0 -24 M{cx} {base - h - 110} l16 8" stroke="{OL}" stroke-width="5"/>'
               f'<path d="M{cx - 40} {base} L{cx - 40} {base - 80} Q{cx} {base - 110} {cx + 40} {base - 80} L{cx + 40} {base} Z" fill="#7A4520" stroke="{OL}" stroke-width="6"/>'
               f'<rect x="{cx - 2}" y="{base - h - 330}" width="4" height="70" fill="{OL}"/><path d="M{cx + 2} {base - h - 330} l46 12 l-46 12 Z" fill="#FFC93C" stroke="{OL}" stroke-width="4"/>')
    return ''.join(out)


def pencil(x, y, s, c='#E5533D'):
    b = (shadow(14) + f'<rect x="-11" y="-110" width="22" height="104" fill="{c}"/><rect x="-11" y="-110" width="7" height="104" fill="#FFFFFF" opacity="0.3" stroke="none"/>'
         '<path d="M-11 -110 L0 -136 L11 -110 Z" fill="#F2D3A0"/><path d="M-4 -126 L0 -136 L4 -126 Z" fill="#3A3A44" stroke="none"/>'
         '<rect x="-11" y="-12" width="22" height="12" fill="#FF9EC4"/>')
    return T(x, y, s, b)


def swings(x, y, s):
    b = (shadow(80) + '<path d="M-90 0 L-70 -150 L-50 0 M50 0 L70 -150 L90 0" fill="none" stroke="#E5533D" stroke-width="12"/>'
         '<path d="M-90 0 L-70 -150 L-50 0 M50 0 L70 -150 L90 0" fill="none" stroke-width="3"/>'
         '<rect x="-74" y="-156" width="148" height="12" rx="4" fill="#FFC93C"/>'
         '<path d="M-36 -146 L-36 -46 M-6 -146 L-6 -46 M14 -146 L14 -56 M44 -146 L44 -56" stroke-width="3"/>'
         '<rect x="-42" y="-48" width="42" height="10" rx="3" fill="#4FA3E3"/><rect x="8" y="-58" width="42" height="10" rx="3" fill="#6CC24A"/>')
    return T(x, y, s, b)


def slide(x, y, s, flip=False):
    b = (shadow(80) + '<path d="M-60 0 L-60 -130 M-20 0 L-20 -130" stroke-width="10"/>'
         + ''.join(f'<path d="M-60 {-20 - k * 26} L-20 {-20 - k * 26}" stroke-width="6"/>' for k in range(5)) +
         '<rect x="-66" y="-140" width="52" height="14" rx="4" fill="#FFC93C"/>'
         '<path d="M-20 -134 Q30 -120 50 -40 Q60 -6 90 -4 L90 8 Q46 8 36 -34 Q20 -110 -20 -116 Z" fill="#4FA3E3"/>')
    return T(x, y, s, b, flip)


def bus(x, y, s, flip=False):
    b = (shadow(130, 16) + '<path d="M-130 -20 L-130 -120 Q-130 -136 -114 -136 L110 -136 Q130 -136 134 -110 L140 -60 L140 -20 Z" fill="#FFC93C"/>'
         + ''.join(f'<rect x="{-116 + k * 50}" y="-122" width="38" height="40" rx="5" fill="{PAL["window"]}"/>' for k in range(5)) +
         '<rect x="-130" y="-66" width="270" height="10" fill="#3A3A44" stroke="none"/>'
         '<circle cx="-80" cy="-16" r="22" fill="#3A3A44"/><circle cx="90" cy="-16" r="22" fill="#3A3A44"/>'
         '<circle cx="-80" cy="-16" r="8" fill="#9AA6B8"/><circle cx="90" cy="-16" r="8" fill="#9AA6B8"/>'
         '<rect x="128" y="-50" width="12" height="12" rx="3" fill="#FFF3C4"/>' + hi(-100, -128, 30, 4, 0.5))
    return T(x, y, s, b, flip)


def books(x, y, s):
    b = shadow(46)
    for k, (c, w) in enumerate([('#4FA3E3', 90), ('#E5533D', 80), ('#6CC24A', 86), ('#FFC93C', 70)]):
        b += f'<rect x="{-w / 2 + (k % 2) * 6}" y="{-24 - k * 24}" width="{w}" height="24" rx="4" fill="{c}"/><rect x="{-w / 2 + (k % 2) * 6 + 6}" y="{-18 - k * 24}" width="{w - 12}" height="4" fill="#FFFFFF" opacity="0.6" stroke="none"/>'
    b += '<path d="M-10 -96 Q0 -116 14 -104 Q20 -94 6 -94 Z" fill="#E5533D"/><path d="M2 -110 q2 -10 8 -12" stroke-width="3" fill="none"/>'
    return T(x, y, s, b)


def tex_hopscotch(sc):
    out = []
    t = 0.55
    k = 0
    while t < 0.98:
        t2 = t + 0.035
        xs = [sc.path_cx(t) - 70 * sc.scale(t), sc.path_cx(t) + 70 * sc.scale(t)]
        y1, y2 = sc.ty(t), sc.ty(t2)
        if k % 3 == 1:
            for sgn in (-1, 1):
                xa = sc.path_cx(t) + (0 if sgn < 0 else 0) * 0
                out.append(f'<rect x="{sc.path_cx(t) - 70 * sc.scale(t) if sgn < 0 else sc.path_cx(t):.1f}" y="{y1:.1f}" width="{70 * sc.scale(t):.1f}" height="{y2 - y1:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{4 * sc.scale(t):.1f}" opacity="0.9"/>')
        else:
            out.append(f'<rect x="{sc.path_cx(t) - 35 * sc.scale(t):.1f}" y="{y1:.1f}" width="{70 * sc.scale(t):.1f}" height="{y2 - y1:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{4 * sc.scale(t):.1f}" opacity="0.9"/>')
        t = t2
        k += 1
    return ''.join(out)


def school():
    sc = Scene(seed=101, curve=40, curve_freq=1.0, path_w=(110, 480))
    sc.sky(DAY_SKY, sun=(860, 300, 64, '#FFE39A'), clouds=CLOUDS, birds=[(240, 330, 1), (270, 310, 0.8)])
    hz = sc.horizon
    sc.backdrop(hills(hz, [('#B5DBA6', 60)], seed=7))
    sc.backdrop(school_building(VX, hz + 10))
    sc.ground(GRASS)
    sc.path('#E9DCC6', texture=combine(tex_tiles('#E9DCC6', '#E0CFB2', 24, 6), tex_hopscotch), border=('#C9B79A', 8))
    cols = ['#E5533D', '#FFC93C', '#4FA3E3', '#6CC24A', '#C58BF2', '#F08A24']
    k = 0
    t = 0.05
    while t < 1.0:
        for side in (-1, 1):
            sc.place(pencil, t, side, 40, cols[k % len(cols)])
            k += 1
        t += 0.03 + 0.05 * t
    sc.place(swings, 0.5, 1, 260)
    sc.place(slide, 0.72, 1, 230)
    sc.place(lambda x, y, s: bus(x, y, s), 0.3, -1, 220)
    sc.place(books, 0.62, -1, 160)
    sc.place(globe, 0.88, -1, 200)
    sc.place(books, 0.96, 1, 140)
    sc.place(bench, 0.8, -1, 120)
    sc.populate([(3, lambda x, y, s: apple_tree(x, y, s)), (2, lambda x, y, s: round_tree(x, y, s, sc.r.choice(TREES))), (1, bush)],
                gap=160, start=(420, 470), step=0.06)
    meadow_fill(sc, 60, 30, (100, 520))
    sc.haze()
    sc.bottom_fade()
    return sc.render()


# =====================================================================================
# JOBS (town of workplaces with a construction site on the horizon)
# =====================================================================================

def crane(x, base, h):
    out = [f'<rect x="{x - 14}" y="{base - h}" width="28" height="{h}" fill="#FFC93C" stroke="{OL}" stroke-width="5"/>']
    for k in range(int(h / 28)):
        y = base - h + k * 28
        out.append(f'<path d="M{x - 14} {y} L{x + 14} {y + 28} M{x + 14} {y} L{x - 14} {y + 28}" stroke="{OL}" stroke-width="2.5"/>')
    out.append(f'<rect x="{x - 220}" y="{base - h - 24}" width="380" height="24" fill="#FFC93C" stroke="{OL}" stroke-width="5"/>'
               f'<rect x="{x + 110}" y="{base - h - 10}" width="50" height="40" fill="#9AA6B8" stroke="{OL}" stroke-width="4"/>'
               f'<path d="M{x - 180} {base - h} L{x - 180} {base - h + 140}" stroke="{OL}" stroke-width="3"/>'
               f'<rect x="{x - 210}" y="{base - h + 140}" width="60" height="30" fill="#E5533D" stroke="{OL}" stroke-width="4"/>'
               f'<rect x="{x - 20}" y="{base - h - 40}" width="40" height="30" fill="#4FA3E3" stroke="{OL}" stroke-width="4"/>')
    return ''.join(out)


def frame_building(x, base, w, h):
    out = [f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" fill="none" stroke="#C9874A" stroke-width="8"/>']
    for k in range(1, int(h / 50)):
        out.append(f'<line x1="{x}" y1="{base - k * 50}" x2="{x + w}" y2="{base - k * 50}" stroke="#C9874A" stroke-width="6"/>')
    for k in range(1, int(w / 50)):
        out.append(f'<line x1="{x + k * 50}" y1="{base - h}" x2="{x + k * 50}" y2="{base}" stroke="#C9874A" stroke-width="5"/>')
    return f'<g opacity="0.9">{"".join(out)}</g>'


def toolbox(x, y, s):
    b = (shadow(44) + '<path d="M-22 -60 L-22 -74 L22 -74 L22 -60" fill="none" stroke-width="7"/><rect x="-46" y="-62" width="92" height="62" rx="6" fill="#E5533D"/>'
         '<rect x="-46" y="-42" width="92" height="6" fill="#B93A28" stroke="none"/><rect x="-8" y="-46" width="16" height="12" fill="#FFC93C"/>'
         '<path d="M20 -62 L40 -100" stroke="#9AA6B8" stroke-width="8"/><path d="M-30 -62 L-40 -96" stroke="#8A5326" stroke-width="8"/>'
         '<rect x="-50" y="-104" width="24" height="12" rx="3" fill="#9AA6B8"/>')
    return T(x, y, s, b)


def jobs():
    sc = Scene(seed=111, curve=0, path_w=(80, 440))
    sc.sky(WARM_SKY, sun=(200, 360, 66, '#FFE39A'), clouds=CLOUDS[:4])
    hz = sc.horizon
    sc.backdrop(frame_building(560, hz + 10, 220, 300) + frame_building(800, hz + 10, 160, 200) + crane(700, hz + 10, 420) + crane(300, hz + 10, 300))
    sc.backdrop(hills(hz, [('#C6DDB0', 20)], seed=3))
    sc.ground([(0, '#D6E4C2'), (0.2, '#B9D89A'), (1, '#94C873')])
    sc.backdrop(strip(sc, -1, 0, 130, 0.0, 1.03, '#E9D7B6', stroke='none', sw=0) + strip(sc, 1, 0, 130, 0.0, 1.03, '#E9D7B6', stroke='none', sw=0))
    sc.path('url(#roadG)', texture=tex_dashes(), border=('#BFA889', 10))
    sc.defs.append(lin('roadG', [(0, '#C2BBB3', 1), (1, '#A39A90', 1)]))
    left = [('#E8F0F8', '#E5533D', 'cross', 1.3), ('#F6D9A8', '#E99A12', 'bread', 1.0), ('#D2412D', '#7A4520', 'fire', 1.2), ('#F9E7C4', '#6CC24A', 'book', 1.1)]
    right = [('#BFE0EF', '#3A7BD5', 'wrench', 1.0), ('#F5C7A0', '#9B59B6', 'cup', 1.2), ('#E7C9E3', '#E5533D', 'dress', 1.0), ('#D8E9B8', '#2E9E4A', 'cross', 1.3)]
    street(sc, -1, left, t1=0.6)
    street(sc, 1, right, t1=0.6)
    for t in (0.66, 0.7, 0.74):
        sc.place(cone, t, 1, 20)
    sc.place(toolbox, 0.82, -1, 120)
    for t in (0.2, 0.42, 0.64, 0.9):
        sc.place(lamp, t, -1, 30)
        sc.place(lamp, t + 0.03, 1, 30)
    sc.populate([(3, lambda x, y, s: round_tree(x, y, s, sc.r.choice(TREES))), (2, bush)], t0=0.66, gap=170, start=(170, 220), step=0.07)
    sc.haze()
    sc.bottom_fade()
    return sc.render()


# =====================================================================================
# BODY (sunrise fitness park)
# =====================================================================================

def pullup(x, y, s):
    b = (shadow(70) + '<path d="M-60 0 L-60 -150 M60 0 L60 -150 M0 0 L0 -110" stroke="#4FA3E3" stroke-width="12"/>'
         '<path d="M-60 0 L-60 -150 M60 0 L60 -150 M0 0 L0 -110" stroke-width="3"/>'
         '<rect x="-66" y="-156" width="132" height="10" rx="5" fill="#9AA6B8"/><rect x="-6" y="-116" width="72" height="10" rx="5" fill="#9AA6B8"/>')
    return T(x, y, s, b)


def dumbbell(x, y, s, c='#E5533D'):
    b = (shadow(40) + '<rect x="-30" y="-20" width="60" height="10" fill="#9AA6B8"/>'
         f'<rect x="-46" y="-34" width="18" height="38" rx="5" fill="{c}"/><rect x="28" y="-34" width="18" height="38" rx="5" fill="{c}"/>')
    return T(x, y, s, b)


def yoga_mat(x, y, s, c='#C58BF2'):
    b = (f'<path d="M-70 0 L-50 -26 L60 -26 L80 0 Z" fill="{c}"/><ellipse cx="80" cy="-12" rx="12" ry="14" fill="{shade(c, -0.15)}"/>'
         '<circle cx="-30" cy="-46" r="20" fill="#FF7FA8"/>' + hi(-36, -52, 6, 4, 0.6))
    return T(x, y, s, b)


def fountain_drink(x, y, s):
    b = (shadow(30) + '<rect x="-20" y="-80" width="40" height="80" rx="6" fill="#9AA6B8"/><rect x="-34" y="-96" width="68" height="20" rx="8" fill="#BFC9D6"/>'
         '<path d="M6 -98 q14 -30 26 -4" stroke="#7FD0F5" stroke-width="6" fill="none"/>')
    return T(x, y, s, b)


def heart_bush(x, y, s, c='#5DB03E', flower_c='#FF7FA8'):
    b = (shadow(50) + '<rect x="-6" y="-30" width="12" height="30" fill="#8A5326"/>'
         f'<path d="M0 -40 Q-70 -80 -54 -130 Q-36 -166 0 -134 Q36 -166 54 -130 Q70 -80 0 -40 Z" fill="{c}"/>'
         + ''.join(f'<circle cx="{fx}" cy="{fy}" r="7" fill="{flower_c}" stroke-width="2.5"/>' for fx, fy in [(-30, -120), (20, -110), (0, -80), (34, -134), (-14, -96)])
         + hi(-30, -132, 14, 8, 0.4))
    return T(x, y, s, b)


def heart_balloon(x, y, s, c='#FF6B8B'):
    b = (f'<path d="M0 -10 Q-60 -50 -46 -96 Q-30 -126 0 -100 Q30 -126 46 -96 Q60 -50 0 -10 Z" fill="{c}"/>'
         '<path d="M0 -10 q-6 30 6 60" stroke-width="3" fill="none"/>' + hi(-24, -96, 10, 7, 0.5))
    return T(x, y, s, b)


def body():
    sc = Scene(seed=121, curve=110, curve_freq=1.4, path_w=(70, 400))
    sc.sky([(0, '#8EC5F0'), (0.5, '#F7C6D9'), (0.85, '#FFE0C2'), (1, '#FFD6A8')], sun=(540, 760, 90, '#FFD08A'), clouds=CLOUDS[:4])
    for x, y, s, c in [(180, 420, 0.8, '#FF6B8B'), (900, 300, 0.6, '#FF9EC4'), (760, 560, 0.45, '#E5533D')]:
        sc.backdrop(heart_balloon(x, y, s, c))
    hz = sc.horizon
    sc.backdrop(hills(hz, [('#C9DDB0', 90), ('#B2D696', 40)], seed=12))
    sc.ground(GRASS)
    sc.path('url(#trackB)', texture=tex_lanes('#FFFFFF', 2, 0.9), border=('#FFFFFF', 6))
    sc.defs.append(lin('trackB', [(0, '#7FB8E6', 1), (1, '#4F95D8', 1)]))
    sc.place(pullup, 0.3, -1, 150)
    sc.place(pullup, 0.66, 1, 170)
    for t, side, off, c in [(0.42, 1, 120, '#E5533D'), (0.45, 1, 200, '#4FA3E3'), (0.86, -1, 150, '#6CC24A')]:
        sc.place(dumbbell, t, side, off, c)
    for t, side, off, c in [(0.52, -1, 140, '#C58BF2'), (0.56, -1, 300, '#6CC24A'), (0.9, 1, 160, '#FF9EC4')]:
        sc.place(yoga_mat, t, side, off, c)
    sc.place(fountain_drink, 0.76, -1, 90)
    sc.place(bench, 0.2, 1, 100)
    t = 0.05
    while t < 1.0:
        for side in (-1, 1):
            sc.place(heart_bush, t, side, 60 if side < 0 else 70, flower_c=sc.r.choice(['#FF7FA8', '#FFFFFF', '#FFD23F']))
        t += 0.09 + 0.12 * t
    sc.populate([(3, lambda x, y, s: round_tree(x, y, s, sc.r.choice(TREES))), (1, bush), (1, apple_tree)], gap=160, start=(380, 450), step=0.06)
    meadow_fill(sc, 60, 60, (100, 520))
    sc.haze('#FFE6E0')
    sc.bottom_fade()
    return sc.render()


# =====================================================================================
# CLOTHES (pastel boutique street)
# =====================================================================================

def clothes_rack(x, y, s):
    b = shadow(70) + '<path d="M-70 0 L-70 -130 L70 -130 L70 0" fill="none" stroke="#9AA6B8" stroke-width="8"/><path d="M-70 0 L-70 -130 L70 -130 L70 0" fill="none" stroke-width="2.5"/>'
    for k, c in enumerate(['#FF7FA8', '#4FA3E3', '#FFC93C', '#C58BF2', '#6CC24A']):
        hx = -50 + k * 25
        b += (f'<path d="M{hx} -130 q-4 -10 4 -12" fill="none" stroke-width="3"/>'
              f'<path d="M{hx - 12} -120 L{hx + 12} -120 L{hx + 16} -60 L{hx - 16} -60 Z" fill="{c}"/>')
    return T(x, y, s, b)


def shopping_bags(x, y, s):
    b = shadow(46)
    for dx, c, h in [(-22, '#FF7FA8', 70), (18, '#C58BF2', 56)]:
        b += (f'<path d="M{dx - 10} {-h} q10 -24 20 0" fill="none" stroke-width="4"/>'
              f'<path d="M{dx - 24} {-h} L{dx + 24} {-h} L{dx + 28} 0 L{dx - 28} 0 Z" fill="{c}"/><rect x="{dx - 20}" y="{-h + 8}" width="8" height="{h - 16}" fill="#FFFFFF" opacity="0.3" stroke="none"/>')
    return T(x, y, s, b)


def clothes():
    sc = Scene(seed=131, curve=0, path_w=(90, 420))
    sc.sky([(0, '#9CCBF2'), (0.6, '#E8D9F2'), (1, '#FFE3EE')], sun=(820, 320, 60, '#FFE3A0'), clouds=CLOUDS[:4])
    hz = sc.horizon
    sc.backdrop(f'<g opacity="0.55">' + ''.join(shop(x, hz + 6, 0.5, w, r, k, flip=x > VX, tall=1.4) for x, w, r, k in
                                                 [(120, '#F7D3E3', '#C58BF2', 'hat'), (300, '#E3F3EA', '#E84393', 'dress'),
                                                  (780, '#E8DFF7', '#E84393', 'shoe'), (960, '#FFE9D6', '#9B59B6', 'shirt')]) + '</g>')
    sc.ground([(0, '#F3E3EA'), (1, '#E9CFDB')])
    sc.path('#F8E9EF', texture=combine(tex_tiles('#F8E9EF', '#F1D3DF', 26, 5), tex_edge_dots('#FFFFFF', 0.04)))
    specs_l = [('#F7D3E3', '#E84393', 'dress', 1.3), ('#E3F3EA', '#2E9E6A', 'shirt', 1.0), ('#E8DFF7', '#9B59B6', 'hat', 1.2), ('#FFE9D6', '#E5533D', 'shoe', 1.0)]
    specs_r = [('#E8DFF7', '#9B59B6', 'shoe', 1.1), ('#FFF2C9', '#E99A12', 'dress', 1.3), ('#F7D3E3', '#E84393', 'hat', 1.0), ('#D9ECFA', '#3A7BD5', 'shirt', 1.2)]
    street(sc, -1, specs_l, t1=0.7)
    street(sc, 1, specs_r, t1=0.7)
    for t, side, off in [(0.3, 1, 40), (0.55, -1, 40), (0.8, 1, 50)]:
        sc.place(clothes_rack, t, side, off)
    for t, side, off in [(0.42, -1, 30), (0.68, 1, 30), (0.92, -1, 70)]:
        sc.place(shopping_bags, t, side, off)
    for t in (0.2, 0.5, 0.8):
        sc.add(sc.ty(t) - 2, bunting(sc.side_x(t, -1, 40), sc.ty(t) - 190 * sc.scale(t), sc.side_x(t, 1, 40), sc.ty(t) - 190 * sc.scale(t), sc.scale(t),
                                     ('#FF7FA8', '#FFFFFF', '#C58BF2', '#FFC93C')))
    sc.populate([(2, lambda x, y, s: round_tree(x, y, s, '#7CCB4E')), (2, lambda x, y, s: heart_bush(x, y, s, '#6CC24A')), (1, bush)],
                t0=0.74, gap=180, start=(150, 220), step=0.07)
    sc.haze('#FFF0F5')
    sc.bottom_fade()
    return sc.render()


# =====================================================================================
# MEALS (food festival)
# =====================================================================================

def food_sign(x, y, s, kind='burger'):
    b = shadow(18) + '<rect x="-5" y="-150" width="10" height="150" fill="#8A5326"/>'
    if kind == 'burger':
        b += ('<g transform="translate(0,-190)"><path d="M-46 -6 Q-46 -46 0 -46 Q46 -46 46 -6 Z" fill="#E9A23B"/>'
              '<rect x="-50" y="-6" width="100" height="12" rx="5" fill="#6CC24A"/><rect x="-46" y="4" width="92" height="16" rx="6" fill="#8A4A24"/>'
              '<rect x="-50" y="18" width="100" height="8" rx="3" fill="#FFC93C"/><path d="M-46 26 L46 26 Q46 44 0 44 Q-46 44 -46 26 Z" fill="#E9A23B"/>'
              '<circle cx="-16" cy="-30" r="3" fill="#FFF3C4" stroke="none"/><circle cx="10" cy="-36" r="3" fill="#FFF3C4" stroke="none"/></g>')
    elif kind == 'pizza':
        b += ('<g transform="translate(0,-196)"><path d="M-44 -36 L44 -36 L0 50 Z" fill="#FFD84A"/><path d="M-48 -44 L48 -44 L44 -32 L-44 -32 Z" fill="#E9A23B"/>'
              '<circle cx="-14" cy="-14" r="9" fill="#E5533D"/><circle cx="14" cy="-6" r="8" fill="#E5533D"/><circle cx="0" cy="18" r="7" fill="#E5533D"/></g>')
    elif kind == 'icecream':
        b += ('<g transform="translate(0,-196)"><path d="M-30 -6 L30 -6 L0 56 Z" fill="#E9A23B"/><path d="M-20 4 l30 30 M0 -6 l18 18" stroke-width="3"/>'
              '<circle cx="-14" cy="-20" r="22" fill="#FF9EC4"/><circle cx="16" cy="-20" r="22" fill="#FFF3C4"/><circle cx="0" cy="-44" r="22" fill="#9B6B4A"/>'
              '<circle cx="2" cy="-68" r="7" fill="#E5533D"/></g>')
    else:
        b += ('<g transform="translate(0,-190)"><circle cx="0" cy="0" r="44" fill="#E9A23B"/><circle cx="0" cy="-4" r="40" fill="#FF9EC4" stroke="none"/>'
              '<circle cx="0" cy="0" r="14" fill="#8FD6F5"/>'
              + ''.join(f'<rect x="{math.cos(a) * 26 - 3:.0f}" y="{math.sin(a) * 26 - 7:.0f}" width="6" height="12" rx="3" fill="{c}" stroke="none" transform="rotate({a * 57 + 30:.0f} {math.cos(a) * 26:.0f} {math.sin(a) * 26:.0f})"/>'
                        for a, c in zip([k * 0.9 for k in range(7)], ['#FFFFFF', '#FFC93C', '#6CC24A', '#4FA3E3', '#FFFFFF', '#E5533D', '#FFC93C'])) + '</g>')
    return T(x, y, s, b)


def picnic(x, y, s, c='#E5533D'):
    b = f'<path d="M-90 0 L-60 -40 L80 -40 L100 0 Z" fill="#FFFFFF"/>'
    for k in range(4):
        b += f'<path d="M{-82 + k * 46} 0 L{-56 + k * 36} -40 L{-38 + k * 36} -40 L{-60 + k * 46} 0 Z" fill="{c}" stroke="none"/>'
    b += '<path d="M-90 0 L-60 -40 L80 -40 L100 0 Z" fill="none"/>'
    b += ('<path d="M-10 -36 L40 -36 L36 -8 L-6 -8 Z" fill="#C9874A"/><path d="M-6 -36 q24 -30 42 0" fill="none" stroke-width="5"/>'
          '<circle cx="-40" cy="-20" r="10" fill="#E5533D"/><circle cx="64" cy="-18" r="9" fill="#FFC93C"/>')
    return T(x, y, s, b)


def meals():
    sc = Scene(seed=141, curve=70, curve_freq=1.2, path_w=(90, 460))
    sc.sky([(0, '#7CB8EC'), (0.45, '#F2C6C2'), (0.8, '#FFD39A'), (1, '#FFC27A')], sun=(780, 700, 90, '#FFC77A'), clouds=CLOUDS[:3])
    hz = sc.horizon
    sc.backdrop(hills(hz, [('#C8D7A4', 100), ('#B4D08E', 40)], seed=4))
    sc.backdrop('<g opacity="0.8">' + stall(220, hz + 6, 0.45, '#4FA3E3') + stall(860, hz + 6, 0.45, '#E99A12') + '</g>')
    sc.ground(GRASS)
    sc.path('#F0DCB2', texture=combine(tex_stones('#DCC08A', 150), tex_edge_dots('#FBF1DE', 0.04)), border=('#D9C08C', 10))
    awn = ['#E5533D', '#4FA3E3', '#6CC24A', '#E99A12', '#C58BF2']
    goods = [('#E9A23B', '#8A4A24', '#6CC24A'), ('#FF9EC4', '#FFF3C4', '#9B6B4A'), ('#E5533D', '#FFD84A', '#6CC24A'), ('#E5533D', '#FFC93C', '#F08A24')]
    t = 0.06
    k = 0
    while t < 0.75:
        for side in (-1, 1):
            sc.place(stall, t, side, 130, awn[k % len(awn)], goods[k % len(goods)])
            k += 1
        t += 0.08 + 0.1 * t
    for t, side, kind in [(0.16, 1, 'pizza'), (0.3, -1, 'burger'), (0.46, 1, 'icecream'), (0.62, -1, 'donut'), (0.82, 1, 'burger'), (0.94, -1, 'icecream')]:
        sc.place(food_sign, t, side, 40, kind)
    for t, side, off, c in [(0.5, -1, 330, '#E5533D'), (0.7, 1, 330, '#4FA3E3'), (0.86, -1, 250, '#6CC24A')]:
        sc.place(parasol_table, t, side, off, c)
    for t, side, off, c in [(0.78, -1, 120, '#E5533D'), (0.92, 1, 200, '#4FA3E3'), (0.6, 1, 420, '#6CC24A')]:
        sc.place(picnic, t, side, off, c)
    for t in (0.25, 0.55, 0.85):
        sc.add(sc.ty(t) - 1, string_lights(sc, t))
    sc.populate([(3, lambda x, y, s: round_tree(x, y, s, sc.r.choice(TREES))), (2, bush)], gap=170, start=(420, 480), step=0.07)
    meadow_fill(sc, 50, 30, (150, 520))
    sc.haze('#FFE7C8')
    sc.bottom_fade()
    return sc.render()


BUILDERS = {'sport': sport, 'music': music, 'cinema': cinema, 'countries': countries, 'school': school, 'jobs': jobs,
            'body': body, 'clothes': clothes, 'meals': meals}
