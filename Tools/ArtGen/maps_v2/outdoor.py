"""Outdoor maps (v2): NATURE, ANIMALS, FRUIT & VEG, WEATHER, TRAVEL."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from props import (T, acacia, apple_tree, balloon, barn, bench, cabbage, carrot_patch, chick, cow, crate, fence,  # noqa: E402
                   flagpole, haystack, hi, house, lamp, log, mushroom, palm, pine, plane, puddle, pumpkin, reed, rock,
                   scarecrow, sheep, shadow, signpost, snowman, stall, suitcase, umbrella, weathervane, windmill)
from scene import (H, OL, VX, W, Scene, combine, hills, lin, mountains, rad, shade, sparkle, tex_dashes,  # noqa: E402
                   tex_edge_dots, tex_planks, tex_stones)
from style import bird, bush, cloud, flower, grass_tuft, round_tree  # noqa: E402

FLOWERS = ['#FF7FA8', '#FFFFFF', '#FFD23F', '#C58BF2', '#FF9A3C']

DAY_SKY = [(0, '#6FBDEB'), (0.55, '#BFE4F8'), (0.88, '#F3F7DE'), (1, '#E6F3CF')]
WARM_SKY = [(0, '#7CC4F0'), (0.5, '#CFEBFA'), (0.85, '#FFE7B8'), (1, '#FFD9A0')]
CLOUDS = [(200, 170, 1.1, 1), (790, 110, 0.85, 0.95), (560, 330, 0.6, 0.9), (980, 360, 0.8, 0.95), (110, 520, 0.6, 0.85)]
GRASS = [(0, '#CFE7AE'), (0.18, '#A6D77A'), (1, '#74C14E')]


def meadow_fill(sc, n_tuft=110, n_flower=70, off=(30, 520)):
    sc.scatter(lambda x, y, s: grass_tuft(x, y, 0.5 + 1.0 * s, '#4E9F36'), n_tuft, 0.05, 1.02, *off)
    sc.scatter(lambda x, y, s: flower(x, y, 0.4 + 0.9 * s, sc.r.choice(FLOWERS)), n_flower, 0.1, 1.02, *off)


def pond(x, y, s, rx=150, ry=60):
    b = (f'<ellipse cx="0" cy="10" rx="{rx + 10}" ry="{ry + 8}" fill="#B99A6A" stroke-width="7"/>'
         f'<ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="url(#waterG)" stroke-width="6"/>'
         f'<path d="M{-rx * 0.6} {-ry * 0.35} q{rx * 0.3} -{ry * 0.2} {rx * 0.6} 0" stroke="#FFFFFF" stroke-width="6" fill="none" opacity="0.7"/>')
    for dx, dy in [(-0.45, 0.2), (0.4, -0.15), (0.55, 0.35)]:
        b += f'<path d="M{rx * dx - 18:.0f} {ry * dy:.0f} a18 11 0 1 0 36 0 l-18 -2 Z" fill="#6CC24A" stroke-width="3"/>'
    return T(x, y, s, b)


WATER_DEF = lin('waterG', [(0, '#7FD0F5', 1), (1, '#3FA2DE', 1)])


# ---------------- NATURE ----------------

def nature():
    sc = Scene(seed=11, curve=110, curve_freq=1.5)
    sc.defs.append(WATER_DEF)
    sc.sky(DAY_SKY, sun=(250, 360, 70, '#FFE39A'), clouds=CLOUDS, birds=[(640, 260, 1.1), (680, 236, 0.8), (712, 270, 0.9)])
    hz = sc.horizon
    sc.backdrop(mountains(hz - 60, [(140, 430, 260), (420, 560, 300), (760, 470, 280), (1010, 380, 230)], '#9DBFE0', shade_c='#86AAD2'))
    # waterfall down the big mountain
    sc.backdrop(f'<path d="M405 {hz - 330} Q400 {hz - 200} 410 {hz - 70} L446 {hz - 70} Q436 {hz - 200} 440 {hz - 330} Z" fill="#E8F7FF" opacity="0.9"/>'
                f'<path d="M418 {hz - 300} L418 {hz - 100} M430 {hz - 280} L430 {hz - 120}" stroke="#BFE6FA" stroke-width="5"/>')
    sc.backdrop(hills(hz, [('#B5DBA6', 70), ('#9CD08A', 30)], seed=4))
    sc.ground(GRASS)
    # tree line on the horizon
    for k in range(34):
        x = k * 34 + sc.r.uniform(-10, 10)
        if abs(x - sc.path_cx(0)) < 50:
            continue
        sc.add(hz + 4, pine(x, hz + 12, sc.r.uniform(0.18, 0.26), sc.r.choice(['#5FA86A', '#6DB377'])))
    sc.path('#E6C995', texture=combine(tex_stones('#CDA86E'), tex_edge_dots('#D9D2C4', 0.05)), border=('#D9C08C', 10))
    sc.at(lambda x, y, s: pond(x, y, s), 230, 0.62, 1.0)
    for x, t in [(110, 0.6), (350, 0.64), (130, 0.67)]:
        sc.at(reed, x, t, 0.9)
    pines = [(3, lambda x, y, s, c=c: pine(x, y, s, c)) for c in ('#3E9A4A', '#4FA65A', '#2F8A4A')]
    rounds = [(2, lambda x, y, s, c=c: round_tree(x, y, s, c)) for c in ('#6CC24A', '#5DB03E', '#7CCB4E')]
    small = [(2, rock), (1, mushroom), (3, bush), (1, log), (2, lambda x, y, s: flower(x, y, s, sc.r.choice(FLOWERS)))]
    pond_xy = (230, sc.ty(0.62), 200, 110)
    sc.populate(pines + rounds, gap=130, start=(150, 230), avoid=[pond_xy])
    sc.populate(small, gap=220, start=(40, 90), step=0.07, avoid=[pond_xy], skip=0.3)
    for x, t, s in [(-20, 0.86, 1.6), (1080, 0.80, 1.7), (40, 1.02, 1.4), (1030, 1.04, 1.5)]:
        sc.at(pine, x, t, s, '#2F8A4A')
    meadow_fill(sc)
    sc.haze('#F4FAE6')
    sc.bottom_fade()
    return sc.render()


# ---------------- ANIMALS (farm) ----------------

def animals():
    sc = Scene(seed=22, curve=90, curve_freq=1.2)
    sc.sky(WARM_SKY, sun=(800, 420, 80, '#FFE39A'), clouds=CLOUDS[:4], birds=[(360, 240, 1), (396, 220, 0.8)])
    hz = sc.horizon
    sc.backdrop(hills(hz, [('#B9DDA0', 150), ('#A3D48A', 90), ('#8FCB72', 40)], seed=9, amp=(60, 100)))
    sc.backdrop(windmill(860, hz - 120, 0.55) + house(200, hz - 95, 0.35, roof='#3A7BD5') + round_tree(120, hz - 70, 0.35))
    sc.ground(GRASS)
    sc.path('#E6C995', texture=tex_stones('#CDA86E', 140), border=('#D9C08C', 10))
    # fences along the path
    t = 0.06
    while t < 1.0:
        for side in (-1, 1):
            sc.place(lambda x, y, s: fence(x, y, s, 3), t, side, 70)
        t += 0.05 + 0.05 * t
    sc.place(barn, 0.24, -1, 200)
    sc.place(lambda x, y, s: barn(x, y, s, flip=True), 0.1, 1, 200)
    sc.place(windmill, 0.36, 1, 300)
    sc.place(haystack, 0.5, -1, 330)
    sc.place(haystack, 0.16, -1, 120)
    sc.place(haystack, 0.62, 1, 420)
    trees = [(3, lambda x, y, s: round_tree(x, y, s, sc.r.choice(['#6CC24A', '#5DB03E', '#7CCB4E']))), (2, bush), (1, apple_tree)]
    sc.populate(trees, gap=150, start=(380, 460), step=0.06)
    sc.populate([(4, lambda x, y, s: sheep(x, y, s, sc.r.random() < 0.5)), (1, haystack), (1, bush)],
                t0=0.26, t1=0.98, gap=140, start=(110, 160), sides=(1,), max_off=380, step=0.07)
    sc.populate([(3, lambda x, y, s: cow(x, y, s, sc.r.random() < 0.5)), (1, bush)],
                t0=0.3, t1=0.98, gap=170, start=(110, 160), sides=(-1,), max_off=380, step=0.09, skip=0.15)
    for t, side, off in [(0.74, 1, 60), (0.76, 1, 95), (0.9, -1, 70), (0.93, 1, 80), (0.97, -1, 100), (0.6, -1, 50)]:
        sc.place(lambda x, y, s, f=sc.r.random() < 0.5: chick(x, y, s, f), t, side, off)
    for x, t, s in [(-10, 0.86, 1.3), (1090, 0.9, 1.3)]:
        sc.at(round_tree, x, t, s, '#6CC24A')
    meadow_fill(sc, 90, 50)
    sc.haze()
    sc.bottom_fade()
    return sc.render()


# ---------------- FRUIT & VEG (garden) ----------------

def fruit_veg():
    sc = Scene(seed=33, curve=50, curve_freq=1.0, path_w=(60, 360))
    sc.sky(WARM_SKY, sun=(260, 420, 75, '#FFE39A'), clouds=CLOUDS, birds=[(700, 300, 1)])
    hz = sc.horizon
    sc.backdrop(hills(hz, [('#BCDDA2', 120), ('#A6D58C', 60)], seed=3))
    sc.backdrop(house(840, hz - 50, 0.4, roof='#E5533D') + windmill(150, hz - 60, 0.45))
    sc.ground([(0, '#CFE7AE'), (0.2, '#A9D87E'), (1, '#7DC352')])
    sc.path('#E6C995', texture=combine(tex_stones('#CDA86E', 120), tex_edge_dots('#C9874A', 0.04)))
    # crop rows: soil strips parallel to the path with plants on them
    def soil_strip(side, off0, off1):
        pts_a, pts_b = [], []
        for i in range(41):
            t = 0.05 + 0.98 * (i / 40) ** 1.1
            pts_a.append((sc.side_x(t, side, off0), sc.ty(t)))
            pts_b.append((sc.side_x(t, side, off1), sc.ty(t)))
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts_a) + ' L' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in reversed(pts_b)) + ' Z'
        sc.backdrop(f'<path d="{d}" fill="#9A6234" stroke="{OL}" stroke-width="4" stroke-linejoin="round"/>')
    rows = {-1: [(60, 110, cabbage), (170, 220, carrot_patch)], 1: [(60, 110, pumpkin), (170, 220, cabbage)]}
    for side, lst in rows.items():
        for o0, o1, fn in lst:
            soil_strip(side, o0, o1)
            t = 0.06
            while t < 1.0:
                sc.place(fn, t, side, (o0 + o1) / 2)
                t += 0.02 + 0.035 * t
    # orchard behind the crops
    sc.populate([(4, lambda x, y, s: apple_tree(x, y, s, fruit=sc.r.choice(['#E5533D', '#FFB21E', '#F0703A']))), (1, bush)],
                gap=140, start=(270, 300), step=0.05)
    sc.place(lambda x, y, s: stall(x, y, s, '#6CC24A', ('#E5533D', '#FFC93C', '#F08A24')), 0.47, -1, 300)
    sc.place(lambda x, y, s: stall(x, y, s, '#E5533D', ('#6CC24A', '#C58BF2', '#FFC93C')), 0.26, 1, 300)
    sc.place(scarecrow, 0.4, 1, 300)
    sc.place(scarecrow, 0.18, -1, 320)
    for t, side, fr in [(0.62, -1, '#E5533D'), (0.66, 1, '#FFC93C'), (0.85, 1, '#6CC24A'), (0.92, -1, '#F08A24')]:
        sc.place(crate, t, side, 40, fruit=fr)
        sc.haze()
    sc.bottom_fade()
    return sc.render()


# ---------------- WEATHER (sunny left, snowy right, rainbow above) ----------------

def rain_cloud(x, y, s):
    return (cloud(x, y, s, 1, '#B8C4D6') +
            ''.join(f'<path d="M{x + (dx - 60) * s:.0f} {y + 30 * s:.0f} l{-8 * s:.1f} {26 * s:.1f}" stroke="#7FB4E6" stroke-width="{5 * s:.1f}" stroke-linecap="round"/>'
                    for dx in range(0, 130, 24)) +
            f'<path d="M{x + 10 * s:.0f} {y + 26 * s:.0f} l{-16 * s:.0f} {34 * s:.0f} l{14 * s:.0f} 0 l{-12 * s:.0f} {34 * s:.0f} l{30 * s:.0f} {-44 * s:.0f} l{-14 * s:.0f} 0 l{12 * s:.0f} {-24 * s:.0f} Z" '
            f'fill="#FFD84A" stroke="{OL}" stroke-width="{3 * s:.1f}" stroke-linejoin="round"/>')


def snowy_pine(x, y, s):
    return pine(x, y, s, '#3E8E62') + T(x, y, s, '<path d="M-30 -96 Q0 -112 30 -96 L18 -90 Q0 -100 -18 -90 Z M-24 -140 Q0 -156 24 -140 L14 -134 Q0 -144 -14 -134 Z M-14 -178 Q0 -194 14 -178 Z" fill="#FFFFFF" stroke="none"/>')


def weather():
    sc = Scene(seed=44, curve=70, curve_freq=1.2)
    sc.sky([(0, '#6FB6E8'), (0.6, '#BFE0F6'), (1, '#EAF4F8')], sun=(180, 330, 70, '#FFE39A'))
    hz = sc.horizon
    # rainbow
    cols = ['#E5533D', '#F59B23', '#FFD84A', '#6CC24A', '#4FA3E3', '#8E6BE0']
    rb = ''
    for k, c in enumerate(cols):
        r_ = 470 - k * 26
        rb += f'<path d="M{540 - r_} {hz} A{r_} {r_ * 0.95} 0 0 1 {540 + r_} {hz}" fill="none" stroke="{c}" stroke-width="27" opacity="0.85"/>'
    sc.backdrop(rb)
    for c in [(200, 140, 1.1, 1), (470, 260, 0.7, 0.95)]:
        sc.backdrop(cloud(*c))
    sc.backdrop(rain_cloud(820, 170, 1.1) + rain_cloud(960, 420, 0.75))
    sc.backdrop(hills(hz, [('#B5DBA6', 60)], seed=6))
    sc.backdrop(mountains(hz - 20, [(900, 220, 200), (1060, 170, 160)], '#C9D9EC', shade_c='#B3C7E0'))
    sc.ground(GRASS)
    # snow covers the right side of the path
    pts = [(sc.path_cx(t) + sc.path_half(t) + 12 * sc.scale(t), sc.ty(t)) for t in [i / 30 * 1.02 for i in range(31)]]
    d = f'M{W} {hz - 10} L' + ' L'.join(f'{x:.1f} {y + 4 * math.sin(i):.1f}' for i, (x, y) in enumerate(pts)) + f' L{W} {H} Z'
    sc.backdrop(f'<path d="{d}" fill="url(#snowG)" stroke="{OL}" stroke-width="5" stroke-linejoin="round"/>')
    sc.defs.append(lin('snowG', [(0, '#F4F8FC', 1), (1, '#DDE8F4', 1)]))
    sc.path('#E6C995', texture=tex_stones('#CDA86E', 140))
    for t in (0.3, 0.55, 0.82):
        sc.at(puddle, sc.path_cx(t) - sc.path_half(t) * 0.4, t, 1.0)
    sc.populate([(3, lambda x, y, s: round_tree(x, y, s, sc.r.choice(['#6CC24A', '#7CCB4E']))), (2, bush), (1, apple_tree)],
                gap=150, start=(160, 240), sides=(-1,), step=0.05)
    sc.populate([(4, snowy_pine), (1, rock)], gap=130, start=(160, 240), sides=(1,), step=0.05)
    sc.place(windmill, 0.3, -1, 110)
    sc.place(weathervane, 0.58, -1, 60)
    sc.place(umbrella, 0.75, -1, 80, '#4FA3E3')
    sc.place(umbrella, 0.45, -1, 90, '#E5533D')
    sc.place(snowman, 0.4, 1, 90)
    sc.place(snowman, 0.84, 1, 80)
    sc.scatter(lambda x, y, s: grass_tuft(x, y, 0.5 + s, '#4E9F36'), 70, 0.05, 1.02, 30, 520, sides=(-1,))
    sc.scatter(lambda x, y, s: flower(x, y, 0.4 + 0.9 * s, sc.r.choice(FLOWERS)), 50, 0.1, 1.02, 30, 520, sides=(-1,))
    sc.scatter(lambda x, y, s: sparkle(x, y - 10 * s, 0.4 + 0.6 * s, '#FFFFFF', 0.9), 40, 0.05, 1.0, 40, 500, sides=(1,))
    for x, t, s in [(-20, 0.9, 1.6)]:
        sc.at(round_tree, x, t, s, '#6CC24A')
    sc.at(snowy_pine, 1080, 0.92, 1.6)
    sc.haze('#F6FAFC')
    sc.bottom_fade()
    return sc.render()


# ---------------- TRAVEL (road trip to the coast) ----------------

def lighthouse(x, y, s):
    b = (shadow(40) + '<path d="M-30 0 L-20 -170 L20 -170 L30 0 Z" fill="#FFFFFF"/>'
         '<path d="M-27 -40 L27 -40 L25 -70 L-25 -70 Z M-23 -110 L23 -110 L21 -140 L-21 -140 Z" fill="#E5533D" stroke="none"/>'
         '<rect x="-26" y="-200" width="52" height="30" fill="#FFE9A6"/><path d="M-32 -200 L0 -230 L32 -200 Z" fill="#E5533D"/>')
    return T(x, y, s, b)


def sailboat(x, y, s, c='#E5533D'):
    b = ('<path d="M-50 -16 L50 -16 L36 4 L-36 4 Z" fill="#A8642E"/><rect x="-3" y="-110" width="6" height="96" fill="#7A4520"/>'
         f'<path d="M4 -106 L48 -24 L4 -24 Z" fill="#FFFFFF"/><path d="M-4 -96 L-40 -24 L-4 -24 Z" fill="{c}"/>')
    return T(x, y, s, b)


def travel():
    sc = Scene(seed=55, curve=150, curve_freq=1.6, path_w=(50, 380))
    sc.sky(WARM_SKY, sun=(860, 520, 70, '#FFE39A'), clouds=CLOUDS[:4])
    hz = sc.horizon
    # sea at the horizon with a coast
    sc.backdrop(f'<rect y="{hz - 120}" width="{W}" height="160" fill="url(#seaG)"/>')
    sc.defs.append(lin('seaG', [(0, '#5CB8EC', 1), (1, '#8ED3F5', 1)]))
    sc.backdrop(''.join(f'<path d="M{x} {hz - 80 + k * 30} q20 -8 40 0" stroke="#FFFFFF" stroke-width="4" fill="none" opacity="0.7"/>'
                        for k in range(4) for x in range(40 + k * 50, W, 230)))
    sc.backdrop(lighthouse(120, hz - 100, 0.6) + sailboat(640, hz - 90, 0.45) + sailboat(880, hz - 60, 0.35, '#4FA3E3'))
    sc.backdrop(f'<path d="M0 {hz - 70} Q140 {hz - 120} 260 {hz - 80} L260 {hz} L0 {hz} Z" fill="#B48A5A"/>')
    sc.backdrop(hills(hz, [('#B9DDA0', 40)], seed=2))
    # sky travellers
    sc.backdrop(balloon(220, 480, 0.8) + balloon(380, 640, 0.5, '#4FA3E3', '#FFFFFF') + balloon(960, 260, 0.55, '#6CC24A', '#FFC93C'))
    sc.backdrop(plane(640, 170, 0.75) + f'<path d="M560 168 L120 140" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.7"/>')
    sc.ground(GRASS)
    sc.path('url(#roadG)', texture=tex_dashes(), border=('#BFA889', 12))
    sc.defs.append(lin('roadG', [(0, '#C2BBB3', 1), (1, '#A39A90', 1)]))
    sc.populate([(2, palm), (2, bush)], t1=0.3, gap=180, start=(110, 170), step=0.07, far_thin=0.8)
    sc.populate([(3, lambda x, y, s: round_tree(x, y, s, sc.r.choice(['#6CC24A', '#7CCB4E', '#5DB03E']))), (2, bush), (1, pine)],
                t0=0.3, gap=150, start=(200, 260), step=0.05)
    sc.place(house, 0.15, -1, 120, '#FBE6C4', '#3A7BD5')
    sc.place(lambda x, y, s: house(x, y, s, '#FCE1CF', '#E5533D', True), 0.22, 1, 120)
    sc.place(lambda x, y, s: signpost(x, y, s), 0.5, 1, 50)
    sc.place(lambda x, y, s: signpost(x, y, s, colors=('#6CC24A', '#E5533D')), 0.8, -1, 60)
    for t, side, off, c in [(0.62, -1, 90, '#E5533D'), (0.63, -1, 150, '#4FA3E3'), (0.9, 1, 120, '#FFC93C'), (0.92, 1, 60, '#C58BF2')]:
        sc.place(suitcase, t, side, off, c)
    sc.place(bench, 0.7, 1, 90)
    meadow_fill(sc, 80, 40, (60, 520))
    sc.haze()
    sc.bottom_fade()
    return sc.render()


BUILDERS = {'nature': nature, 'animals': animals, 'fruit_veg': fruit_veg, 'weather': weather, 'travel': travel}
