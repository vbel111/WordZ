"""Home screen background v3 (3/4 view, matches the v3 maps).
Layout on the phone: logo over the upper-middle (y ~190-760), PLAY/CATEGORIES buttons around y 1300-1600,
dock at the bottom -> the hero (Word Z town on its hill) sits between logo and buttons, the bottom third stays calm."""
from style import OL, shade, rng
from world import World, S, W, H, HY, GREENS, sky_day, mountains, grass, haze_and_rays
from city2 import townhouse, fluffy_tree, poplar, lamp, clock_tower, boat
from props3 import bush, flowers, windmill, pine
from home import hex_tile, letter_balloon


def build():
    w = World(40)
    w.sky = sky_day(sun=(860, 300))
    balloons = (letter_balloon(110, 560, 0.85, '#E5533D', 'W') + letter_balloon(300, 330, 0.65, '#4FA3E3', 'O') +
                letter_balloon(790, 520, 0.7, '#6CC24A', 'R') + letter_balloon(990, 330, 0.6, '#FFB82E', 'D'))
    w.back = mountains(far='#B5D3EE', near='#93BEE3')
    w.ground = grass('#A8DD72', '#6CC04A', tufts=200)
    w.river([(1120, 560), (900, 640), (700, 760), (620, 900), (760, 1040), (1000, 1140), (1140, 1180)], w0=40, w1=220)
    cl, wf, L, Rr = w.path([(470, 560), (430, 760), (520, 980), (440, 1200), (520, 1440), (460, 1700), (540, 2000), (520, 2420)], w0=26, w1=170,
                           fill='#EBD9B0', edge='#C9AE7E')
    # hero: Word Z clock tower on its hill (centre-right, between logo and buttons)
    w.flat.append(f'<path d="M560 1000 Q760 820 1100 900 L1100 1080 Q820 1060 560 1000 Z" fill="#8FD25E" stroke="{OL}" stroke-width="5"/>')
    w.add(1010, clock_tower(800, 1010, S(1010) * 1.25))
    w.occ(760, 820, 980, 1020)
    w.add(980, townhouse(640, 980, 130 * S(980), 120 * S(980), S(980), '#F7E2B4', '#D9583C', side='l', floors=2, cols=2, seed=4))
    w.add(990, townhouse(960, 990, 130 * S(990), 130 * S(990), S(990), '#F2A285', '#2F9C9A', side='l', floors=2, cols=2, seed=5))
    w.add(820, windmill(170, 820, S(820) * 1.1, blades=0.5))
    w.occ(110, 700, 240, 830)

    def village(x, by, wd, s, side, r, idx):
        h = wd * r.uniform(0.9, 1.3)
        return townhouse(x, by, wd, h, s, r.choice(['#F6C27A', '#F2A285', '#F7E2B4', '#9FD0C8', '#FFE0A3']), r.choice(['#D9583C', '#4F6E86', '#2F9C9A', '#E2723E']),
                         side=side, floors=2, cols=2, seed=idx), wd, h
    w.rows([570, 610, 660, 720], village, gap=0.35, gap_far=0.38)
    # giant hex letter tiles along the path (the game's own pieces)
    for x, y, s, l, t in [(250, 1180, 0.9, 'W', -8), (720, 1330, 0.95, 'O', 6), (150, 1560, 1.15, 'R', -5), (900, 1720, 1.2, 'D', 8),
                          (300, 2050, 1.4, 'Z', -6), (820, 2200, 1.5, 'A', 5)]:
        w.add(y, hex_tile(x, y, s, l, tilt=t))
        w.occ(x - 70 * s, y - 40, x + 70 * s, y + 10)
    for x, y in [(380, 1060), (600, 1140), (360, 1450), (640, 1600)]:
        w.add(y, lamp(x, y, S(y)))
    # flora: dense up top, sparse in the bottom third so the buttons and dock read cleanly
    w.scatter([(4, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)), (1, lambda x, y, s, r, i: poplar(x, y, s)),
               (1, lambda x, y, s, r, i: pine(x, y, s, '#3E9A4F')), (1.2, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS), '#FF5E7E'))],
              y0=560, y1=1500, density=0.45)
    w.scatter([(2, lambda x, y, s, r, i: flowers(x, y, s, r, 8)), (1, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS), '#FF5E7E'))],
              y0=1500, y1=2350, density=0.3, step=(110, 170))
    w.fg = ''.join(fluffy_tree(x, y, s, c, seed=600 + i) for i, (x, y, s, c) in enumerate([(30, 2460, 2.0, '#4FB043'), (1060, 2470, 1.9, '#5CBF3F')])) + haze_and_rays((860, 300)) + balloons
    return w.render()


BUILDERS = {'home': build}
