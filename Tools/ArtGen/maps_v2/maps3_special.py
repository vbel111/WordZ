"""v3 special maps: cinema, music, electronic, space, ocean, clothes, meals, body."""
import math
from style import OL, shade, mix, rng, cloud, lin, rad
from world import World, S, W, H, HY, GREENS, sky_day, sky_dusk, sky_night, skyline, mountains, hills, grass, haze_and_rays
from city2 import townhouse, fluffy_tree, poplar, lamp, fountain, parasol, flowerbed, car
from props3 import *  # noqa
from props3b import palm, pitch, bleachers, labelled_house, flagpole
from props3c import *  # noqa


def ground_grad(top, bottom, gid, tuft=None, tufts=0, seed=3):
    r = rng(seed)
    out = [f'<defs>{lin(gid, [(0, top, 1), (1, bottom, 1)])}</defs><rect x="0" y="{HY + 20}" width="{W}" height="{H - HY}" fill="url(#{gid})"/>']
    for _ in range(tufts):
        x, y = r.uniform(0, W), r.uniform(HY + 60, H)
        s = S(y)
        out.append(f'<path d="M{x - 6 * s:.1f} {y:.1f} q{3 * s:.1f} {-10 * s:.1f} {6 * s:.1f} 0 q{3 * s:.1f} {-12 * s:.1f} {6 * s:.1f} 0" fill="{tuft}" opacity="0.5"/>')
    return ''.join(out)


def mood(col, op):
    return f'<rect x="0" y="0" width="{W}" height="{H}" fill="{col}" opacity="{op}"/>'


def houses(walls, roofs, shops=(None,), kinds=('gable',), hmul=(1.0, 1.5)):
    def f(x, by, wd, s, side, r, idx):
        h = wd * r.uniform(*hmul)
        return townhouse(x, by, wd, h, s, r.choice(walls), r.choice(roofs), side=side, floors=2 if h < 150 * s else 3,
                         cols=3 if wd > 120 * s else 2, seed=idx, shop=r.choice(shops), roof_kind=r.choice(kinds)), wd, h
    return f


def canopies(cols=('#4FB043', '#5CBF3F', '#6CC24A', '#4FB043')):
    return ''.join(fluffy_tree(x, y, s, cols[i % len(cols)], seed=500 + i) for i, (x, y, s) in enumerate([(70, 2440, 2.1), (1030, 2450, 2.0), (330, 2500, 1.7), (780, 2520, 1.6)]))


# =================================================================== CINEMA - film studio boulevard at dusk
def cinema_map():
    w = World(21)
    w.sky = sky_dusk(sun=(540, 440)) + searchlight(260, HY + 20, 0.5, -1.25) + searchlight(820, HY + 20, 0.5, -1.9)
    w.back = skyline(('#B48BC0', '#9C76B6'), ('#8E6AAE', '#6E5296'), gap=(420, 660), tower=None)
    w.ground = ground_grad('#C9A6C0', '#7FB25C', 'gcin', '#4E7F36', 120)
    cl, wf, L, Rr = w.path([(540, 480), (600, 700), (460, 960), (560, 1240), (420, 1520), (560, 1800), (480, 2100), (520, 2420)], w0=40, w1=150,
                           fill='#D8364A', edge='#F2C14E')
    w.add(880, cinema(330, 880, S(880)))
    w.occ(320, 640, 330 + 360 * S(880) + 70, 890)
    for i, (x, y, n) in enumerate([(40, 1160, '1'), (760, 1260, '2'), (60, 1700, '3'), (800, 1820, '4')]):
        w.add(y, studio(x, y, S(y), side='r' if x < 540 else 'l', num=n, col=['#E8E2D6', '#F2D9A6', '#DCE6F0', '#F5C9B8'][i]))
        w.occ(x - 20, y - 140 * S(y), x + 300 * S(y), y + 10)
    for x, y in [(380, 1380), (700, 1560), (300, 2000)]:
        w.add(y, movie_camera(x, y, S(y) * 1.2))
    for x, y in [(640, 1680), (360, 1100)]:
        w.add(y, clapper(x, y, S(y) * 1.4))
    for i in range(10, len(cl) - 10, 16):
        for P in (L, Rr):
            x, y = P[i]
            if 0 < x < W:
                w.add(y, lamp(x, y, S(y)) if i % 32 else searchlight(x, y, S(y) * 0.8, -1.4 if x < 540 else -1.7))
    w.rows([560, 610, 670], houses(['#F2B8C6', '#E8C3E8', '#F7E2B4', '#C9B3E8'], ['#7A3B6A', '#4F4F86', '#C24B34'], kinds=('flat', 'gable')), gap=0.3)
    w.scatter([(4, lambda x, y, s, r, i: palm(x, y, s, r.choice([1, -1]))), (1, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)),
               (1, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS), '#FF5E7E'))], density=0.36)
    w.fg = ''.join(palm(x, y, s, l) for x, y, s, l in [(40, 2480, 2.0, 1), (1050, 2480, 1.9, -1)]) + mood('#5A2A6A', 0.12)
    return w.render()


# =================================================================== MUSIC - festival grounds at night
def music_map():
    w = World(22)
    w.sky = sky_night(moon=(880, 170), top='#241A5A', low='#7A4AA8')
    w.back = hills(('#3E3A7A', '#4C4590')) + ''.join(searchlight(x, HY + 30, 0.4, a, c) for x, a, c in [(200, -1.3, '#FF9FD8'), (540, -1.57, '#9FE8FF'), (880, -1.85, '#FFF09F')])
    w.ground = ground_grad('#4C6E8E', '#3F8A4E', 'gmus', '#2F6E3A', 100)
    # piano-key boardwalk
    cl, wf, L, Rr = w.path([(540, 480), (480, 700), (580, 960), (460, 1240), (580, 1520), (460, 1800), (540, 2100), (500, 2420)], w0=40, w1=150,
                           fill='#FFFFFF', edge='#33333D', tiles=('#33333D', 2))
    w.add(980, stage(560, 980, S(980) * 1.2))
    w.occ(560, 700, 560 + 420 * S(980) * 1.2, 990)
    for x, y in [(530, 990), (1060, 990)]:
        w.add(y + 1, speaker(x, y, S(y) * 1.3, 1.4))
    for x, y, c in [(120, 1100, '#E5533D'), (300, 1320, '#4FA3E3'), (780, 1420, '#FFB82E'), (120, 1600, '#8E3BB8'), (860, 1900, '#2F9C9A')]:
        w.add(y, festival_tent(x, y, S(y) * 1.2, c))
        w.occ(x - 80 * S(y), y - 40, x + 80 * S(y), y + 10)
    for x, y, c in [(420, 1080, '#FF5E7E'), (980, 1260, '#6FD3FF'), (250, 1860, '#FFD23F'), (740, 2120, '#8CE06A')]:
        w.add(y, light_tower(x, y, S(y), c))
    w.add(1700, food_truck(760, 1700, S(1700) * 1.1, '#FF8A3D', '#2F9C9A'))
    w.occ(660, 1600, 880, 1710)
    for i in range(6, len(cl) - 12, 20):
        a, b = L[i], Rr[i + 6]
        w.add(max(a[1], b[1]) + 1, string_lights(a[0] - 40 * S(a[1]), a[1] - 120 * S(a[1]), b[0] + 40 * S(b[1]), b[1] - 120 * S(b[1]), S(a[1])))
    for x, y in [(340, 1600), (680, 1960), (200, 2100)]:
        w.add(y, speaker(x, y, S(y)))
    w.scatter([(3, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(['#3E8A4A', '#2F7A40', '#4A9A55']), seed=i)), (1, lambda x, y, s, r, i: bush(x, y, s, '#3E8A4A', '#FF5E7E'))], density=0.3)
    w.fg = canopies(('#2F7A40', '#3E8A4A', '#2F7A40', '#3E8A4A')) + mood('#20103A', 0.18)
    return w.render()


# =================================================================== ELECTRONIC - tech campus at night
def electronic_map():
    w = World(23)
    w.sky = sky_night(moon=(860, 160), top='#0E1A3E', low='#2A4F8A', stars=80)
    w.back = skyline(('#2E4A7A', '#36588E'), ('#26406E', '#1E355E'), gap=None, tower=600)
    w.ground = ground_grad('#245C66', '#1F6E52', 'gele', '#2B8A5E', 60)
    # glowing circuit road
    cl, wf, L, Rr = w.path([(540, 480), (600, 720), (460, 980), (560, 1260), (420, 1540), (560, 1820), (480, 2120), (520, 2420)], w0=40, w1=150,
                           fill='#24324A', edge='#48E0FF', dash='#7CF2FF')
    rr = rng(5)
    for _ in range(26):   # circuit traces on the ground
        x, y = rr.uniform(0, W), rr.uniform(700, 2300)
        s = S(y)
        L_ = rr.uniform(60, 160) * s
        w.flat.append(f'<path d="M{x:.0f} {y:.0f} h{L_:.0f} l{20 * s:.0f} {-14 * s:.0f} h{L_ * 0.6:.0f}" fill="none" stroke="#48E0FF" stroke-width="{3 * s:.1f}" opacity="0.5"/>'
                      f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{5 * s:.1f}" fill="#7CF2FF" opacity="0.8"/>')
    w.rows([560, 610, 680, 770, 880, 1010], lambda x, by, wd, s, side, r, idx: (glass_tower(x, by, s, w=wd / s, h=wd / s * r.uniform(1.6, 2.6), col=r.choice(['#3F7FC0', '#4A6FB8', '#2F8F9F', '#5A5FB0']), side=side, lit=r.uniform(0.25, 0.55), seed=idx), wd, 0), gap=0.3, wmin=90, wmax=130)
    for x, y in [(160, 1300), (900, 1460), (240, 1960)]:
        w.add(y, dish(x, y, S(y) * 1.3))
    for x, y in [(760, 1150), (840, 1180), (920, 1210), (80, 1600), (160, 1630), (720, 2080), (800, 2110)]:
        w.add(y, solar_panel(x, y, S(y) * 1.2))
    for x, y in [(240, 1400), (760, 1760), (200, 2200)]:
        w.add(y, robot(x, y, S(y) * 1.3))
    for i in range(10, len(cl) - 10, 18):
        for P in (L, Rr):
            x, y = P[i]
            if 0 < x < W:
                w.add(y, lamp(x, y, S(y)))
    w.scatter([(3, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(['#2F8A6A', '#2A7A60']), seed=i)), (1, lambda x, y, s, r, i: bush(x, y, s, '#2F8A6A'))], density=0.25)
    w.fg = canopies(('#2A7A60', '#2F8A6A', '#2A7A60', '#2F8A6A')) + mood('#0A1030', 0.18)
    return w.render()


# =================================================================== SPACE - alien moon base
def space_map():
    w = World(24)
    w.sky = sky_night(moon=None, top='#120A3A', low='#3A2A8A', stars=160) + planet(860, 200, 80, '#F2A25A', '#FFD9A8') + planet(180, 300, 40, '#6FD3FF') + planet(560, 120, 22, '#FF7FD0')
    w.back = ''.join(f'<path d="M{x - 160} {HY + 40} Q{x} {HY - h} {x + 160} {HY + 40} Z" fill="{c}"/>' for x, h, c in [(120, 120, '#5A3FA8'), (420, 70, '#6448B4'), (760, 140, '#5A3FA8'), (1020, 90, '#6448B4')])
    w.ground = ground_grad('#7C5CC8', '#4A3A9A', 'gspc')
    cl, wf, L, Rr = w.path([(540, 480), (460, 720), (580, 980), (440, 1260), (580, 1540), (440, 1820), (540, 2120), (500, 2420)], w0=40, w1=150,
                           fill='#2A2060', edge='#6FD3FF', dash='#FFD23F')
    w.add(1060, rocket(820, 1060, S(1060) * 1.2))
    w.occ(720, 780, 920, 1070)
    for x, y, r_ in [(180, 900, 100), (240, 1500, 120), (860, 1700, 110), (260, 2120, 120)]:
        w.add(y, dome(x, y, S(y), r_))
        w.occ(x - r_ * S(y), y - r_ * S(y), x + r_ * S(y), y + 10)
    for x, y in [(700, 760), (360, 1200), (920, 1320), (620, 1900), (900, 2150)]:
        w.flat.append(crater(x, y, S(y) * 1.4))
        w.zones.append((x, y, 80 * S(y), 30 * S(y)))
    for x, y in [(620, 1340), (380, 1700), (700, 2250)]:
        w.add(y, robot(x, y, S(y) * 1.3, '#E8E2D6'))
    w.scatter([(3, lambda x, y, s, r, i: crystal(x, y, s, r.choice(['#6FD3FF', '#FF7FD0', '#8CE06A', '#FFD23F']))),
               (3, lambda x, y, s, r, i: alien_plant(x, y, s, r.choice(['#FF7FD0', '#FFD23F', '#6FD3FF']))),
               (1, lambda x, y, s, r, i: rock(x, y, s, '#6A52B0'))], density=0.4)
    w.fg = ''.join(crystal(x, y, s, c) for x, y, s, c in [(80, 2440, 2.2, '#6FD3FF'), (1000, 2450, 2.0, '#FF7FD0')]) + mood('#1A0A40', 0.1)
    return w.render()


# =================================================================== OCEAN - coral reef
def ocean_map():
    w = World(25)
    d = lin('sea3', [(0, '#3FB2E8', 1), (0.6, '#1E7FC4', 1), (1, '#2B9BD0', 1)])
    w.defs.append(d)
    rays = ''.join(f'<path d="M{x} 0 L{x + 60} 0 L{x + 260} {HY + 300} L{x + 140} {HY + 300} Z" fill="#FFFFFF" opacity="0.08"/>' for x in (80, 380, 700))
    w.sky = (f'<rect width="{W}" height="{HY + 140}" fill="url(#sea3)"/>' + rays +
             ''.join(f'<path d="M{x} 30 q30 -14 60 0 q30 14 60 0" stroke="#FFFFFF" stroke-width="5" fill="none" opacity="0.4"/>' for x in range(-20, W, 160)) +
             ''.join(fish(x, y, s, c, f) for x, y, s, c, f in [(200, 260, 0.6, '#FFB82E', False), (780, 200, 0.5, '#FF7F8A', True), (560, 360, 0.45, '#FFD23F', False)]) +
             f'<path d="M640 150 q90 -40 180 0 q-90 40 -180 0 Z M820 150 l40 -26 l0 52 Z" fill="#1A5E96" opacity="0.5"/>')
    w.back = ''.join(f'<path d="M{x - 180} {HY + 40} Q{x} {HY - h} {x + 180} {HY + 40} Z" fill="{c}"/>' for x, h, c in [(100, 90, '#2A80B8'), (450, 60, '#3388C0'), (800, 110, '#2A80B8'), (1060, 70, '#3388C0')])
    w.ground = ground_grad('#7FC3D8', '#F0D9A0', 'gsea')
    cl, wf, L, Rr = w.path([(540, 480), (480, 720), (600, 980), (440, 1260), (600, 1540), (460, 1820), (560, 2120), (500, 2420)], w0=40, w1=160,
                           fill='#FBEBC0', edge='#E3C98E')
    w.add(1100, shipwreck(820, 1100, S(1100) * 1.2))
    w.occ(680, 960, 1000, 1110)
    w.add(1700, chest(820, 1700, S(1700) * 1.4))
    for x, y in [(180, 920), (900, 1460), (220, 2000)]:
        w.add(y, rock(x, y, S(y) * 1.6, '#8A9AA8'))
    w.scatter([(3, lambda x, y, s, r, i: coral(x, y, s * 1.2, r.choice(['#FF7F8A', '#FF9F43', '#FFD23F', '#FF7FD0']))),
               (2, lambda x, y, s, r, i: fan_coral(x, y, s, r.choice(['#B07FE0', '#FF7FD0', '#FF9F43']))),
               (2, lambda x, y, s, r, i: kelp(x, y, s, r.choice(['#3FAE6A', '#58C27A']), r.uniform(150, 260))),
               (1, lambda x, y, s, r, i: rock(x, y, s, '#8A9AA8')),
               (1.5, lambda x, y, s, r, i: fish(x, y - 90 * s, s * 1.2, r.choice(['#FFB82E', '#FF7F8A', '#6FD3FF', '#FFD23F']), r.random() < 0.5) + bubbles(x + 30 * s, y - 120 * s, s, 3, r))],
              density=0.45)
    w.fg = ''.join(kelp(x, 2420, 2.0, '#3FAE6A', 300) for x in (40, 1040)) + mood('#0A3A6A', 0.08)
    return w.render()


# =================================================================== CLOTHES - fashion high street
def clothes_map():
    w = World(26)
    w.sky = sky_day(sun=(880, 260), top='#7EC8F4', low='#FFE3EE')
    w.back = skyline(('#E2CDEB', '#D3BDE4'), ('#D9B6D8', '#C79CC8'), tower=None)
    w.ground = ground_grad('#F2E2D2', '#E7CFB8', 'gclo')
    cl, wf, L, Rr = w.path([(540, 480), (600, 720), (460, 980), (580, 1260), (440, 1540), (580, 1820), (480, 2120), (520, 2420)], w0=50, w1=170,
                           fill='#FFF3F6', edge='#F2A6C0', tiles=('#FAD2DF', 2))
    w.plaza(800, 1500, 200, 80, fill='#FBE3EA', ring='#F2C6D4')
    w.add(1500, fountain(800, 1500, S(1500)))
    w.rows([560, 600, 650, 710, 790, 880, 990, 1110, 1250, 1420, 1600, 1800],
           houses(['#FAD2DF', '#FFE0A3', '#C9E8F0', '#E8D6F5', '#FFFFFF', '#F7C6B0'], ['#E2728E', '#7A6BC0', '#2F9C9A', '#E8A65A'],
                  shops=('#FF5E7E', '#4FA3E3', '#FFB82E', '#B07FE0'), hmul=(1.1, 1.6)), gap=0.18)
    for i in range(4, len(cl) - 12, 18):
        a, b = L[i], Rr[i]
        w.add(max(a[1], b[1]) + 1, bunting(a[0] - 30 * S(a[1]), a[1] - 130 * S(a[1]), b[0] + 30 * S(b[1]), b[1] - 130 * S(b[1]), S(a[1])))
    for x, y in [(330, 1350), (700, 1700), (300, 2050)]:
        w.add(y, clothes_rack(x, y, S(y) * 1.3))
    for x, y in [(640, 1120), (380, 1650), (650, 2150)]:
        w.add(y, shopping_bags(x, y, S(y) * 1.4))
    w.scatter([(3, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(['#5CBF3F', '#7DCB4E']), seed=i)), (2, lambda x, y, s, r, i: bush(x, y, s, '#58B74A', '#FF5E7E')),
               (1, lambda x, y, s, r, i: flowers(x, y, s, r))], density=0.4)
    w.fg = canopies() + haze_and_rays((880, 260), haze='#FFF0F4')
    return w.render()


# =================================================================== MEALS - food festival street
def meals_map():
    w = World(27)
    w.sky = sky_dusk(sun=(820, 420))
    w.back = skyline(('#F0B8A8', '#E6A598'), ('#D89A9A', '#C48A92'), gap=(700, 940), tower=None)
    w.ground = ground_grad('#E8CDA8', '#9ACD6A', 'gmea', '#6CA84A', 80)
    cl, wf, L, Rr = w.path([(540, 480), (600, 720), (460, 980), (580, 1260), (440, 1540), (580, 1820), (480, 2120), (520, 2420)], w0=50, w1=160,
                           fill='#E9D3B0', edge='#B8956A', tiles=('#DEC59C', 2))
    for x, y, c, a in [(60, 1000, '#FFB82E', '#E5533D'), (760, 1120, '#4FA3E3', '#FFFFFF'), (40, 1500, '#FF7FA8', '#FFFFFF'), (760, 1660, '#6CC24A', '#E5533D'), (100, 2050, '#E5533D', '#FFD23F')]:
        w.add(y, food_truck(x + 90 * S(y), y, S(y) * 1.25, c, a))
        w.occ(x, y - 130 * S(y), x + 230 * S(y), y + 10)
    for x, y, c in [(330, 1240, '#E5533D'), (900, 1420, '#2F9C9A'), (300, 1780, '#4FA3E3'), (860, 2010, '#E5533D'), (680, 2250, '#FFB82E')]:
        w.add(y, picnic_table(x, y, S(y) * 1.3, c))
    for x, y in [(700, 900), (220, 1350), (880, 1900)]:
        w.add(y, parasol(x, y, S(y) * 1.2, '#E5533D'))
    w.rows([560, 610, 670, 750, 840], houses(['#F7E2B4', '#F2A285', '#FFE0A3', '#F5B9A0'], ['#C24B34', '#4F6E86', '#E2723E'], shops=('#E5533D', '#2F9C9A', '#FFB82E')), gap=0.25)
    for i in range(4, len(cl) - 12, 16):
        a, b = L[i], Rr[i]
        w.add(max(a[1], b[1]) + 1, string_lights(a[0] - 40 * S(a[1]), a[1] - 140 * S(a[1]), b[0] + 40 * S(b[1]), b[1] - 140 * S(b[1]), S(a[1])))
    w.scatter([(3, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)), (1, lambda x, y, s, r, i: bush(x, y, s, '#58B74A', '#FF5E7E')),
               (1, lambda x, y, s, r, i: crates(x, y, s, r.choice(['#FF4E4E', '#FFD23F', '#FF8A3D'])))], density=0.35)
    w.fg = canopies() + mood('#FF9F6B', 0.06)
    return w.render()


# =================================================================== BODY - wellness park
def body_map():
    w = World(28)
    w.sky = sky_day(sun=(880, 260), low='#FFE3EA')
    w.back = hills(('#C6E494', '#AEDB80'))
    w.ground = grass('#B2E07C', '#74C450', tufts=160)
    cl, wf, L, Rr = w.path([(540, 480), (480, 720), (600, 980), (440, 1260), (600, 1540), (460, 1820), (560, 2120), (500, 2420)], w0=40, w1=150,
                           fill='#4FA3E3', edge='#FFFFFF', dash='#FFFFFF')
    w.add(940, labelled_house(640, 940, S(940), 330, 210, '#FFFFFF', '#4FA3E3', '#FFFFFF', 'cross', side='l'))
    w.occ(630, 720, 1080, 950)
    w.plaza(240, 1300, 200, 80, fill='#EEDDB8')
    w.add(1300, fountain(240, 1300, S(1300)))
    pitch(w, 660, 1480, 1040, 1640, kind='football')
    for x, y in [(160, 1600), (240, 1640), (320, 1680)]:
        w.add(y, gym_bar(x, y, S(y) * 1.2))
    for x, y, c in [(700, 1860, '#B07FE0'), (820, 1880, '#FF7FA8'), (940, 1900, '#6FD3FF'), (660, 1960, '#FFD23F')]:
        w.add(y, yoga_mat(x, y, S(y) * 1.3, c))
    for x, y in [(380, 1960), (440, 1990)]:
        w.add(y, dumbbell(x, y, S(y) * 1.3))
    for x, y in [(200, 980), (860, 1260), (160, 2060), (940, 2150)]:
        w.add(y, heart_hedge(x, y, S(y) * 1.4))
    w.rows([560, 610, 670, 740], houses(['#FFFFFF', '#FAD2DF', '#C9E8F0', '#F7E2B4'], ['#4FA3E3', '#E2728E', '#2F9C9A']), gap=0.3)
    w.scatter([(4, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)), (1, lambda x, y, s, r, i: bush(x, y, s, '#58B74A', '#FF5E7E')),
               (1.3, lambda x, y, s, r, i: flowers(x, y, s, r))], density=0.36)
    w.fg = canopies() + haze_and_rays((880, 260), haze='#FFF0F4')
    return w.render()


BUILDERS = {'cinema': cinema_map, 'music': music_map, 'electronic': electronic_map, 'space': space_map, 'ocean': ocean_map,
            'clothes': clothes_map, 'meals': meals_map, 'body': body_map}
