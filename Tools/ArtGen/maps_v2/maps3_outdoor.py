"""v3 outdoor maps (3/4 view) built on world.py."""
import math
from style import OL, shade, mix, rng, cloud
from world import World, S, W, H, HY, GREENS, sky_day, sky_dusk, sky_night, skyline, mountains, hills, sea_horizon, grass, haze_and_rays
from city2 import townhouse, fluffy_tree, poplar, lamp, boat, fountain, parasol, flowerbed, car
from props3 import *  # noqa
from props3b import *  # noqa


def trees_and_bushes(w, extra=(), density=0.62, y0=560, y1=2320, pad=40):
    ch = [(5, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=int(x * 7 + y))),
          (1, lambda x, y, s, r, i: poplar(x, y, s, r.choice(['#4FA843', '#3E9A3F']))),
          (1.4, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS), r.choice([None, '#FF5E7E', None])))]
    w.scatter(list(ch) + list(extra), y0, y1, density, pad=pad)


def corner_canopies(w, cols=('#4FB043', '#5CBF3F', '#6CC24A', '#4FB043'), seed=500):
    out = []
    for i, (x, y, s) in enumerate([(70, 2440, 2.1), (1030, 2450, 2.0), (330, 2500, 1.7), (780, 2520, 1.6)]):
        out.append(fluffy_tree(x, y, s, cols[i % len(cols)], seed=seed + i))
    return ''.join(out)


def house(wall_choices, roof_choices, shops=(None,), roof_kinds=('gable',)):
    def f(x, by, wd, s, side, r, idx):
        h = wd * r.uniform(0.9, 1.4)
        floors = 2 if h < 150 * s else 3
        return townhouse(x, by, wd, h, s, r.choice(wall_choices), r.choice(roof_choices), side=side, floors=floors,
                         cols=3 if wd > 120 * s else 2, seed=idx, shop=r.choice(shops), roof_kind=r.choice(roof_kinds)), wd, h
    return f


# =================================================================== ANIMALS - farm valley
def animals():
    w = World(11)
    w.sky = sky_day(sun=(860, 280))
    w.back = hills(('#B9E08A', '#A3D676')) + ''.join(windmill(x, HY + 40, 0.3, blades=a) for x, a in [(160, 0.4), (930, 1.0)])
    w.ground = grass('#A8DD72', '#74C450', tufts=220)
    cl, wf, L, Rr = w.path([(560, 480), (620, 640), (470, 860), (380, 1100), (520, 1380), (720, 1640), (600, 1940), (480, 2420)],
                           w0=26, w1=150, fill='#E8CF98', edge='#C9A86C')
    w.river([(-40, 1080), (120, 1150), (250, 1260), (330, 1400), (300, 1560), (140, 1700), (-60, 1780)], w0=40, w1=170, rails=False, bank='#CDE8A8', wall='#9CC77A')
    for (x0, y0, x1, y1, c) in [(-20, 500, 200, 545, '#E8CF6A'), (240, 505, 430, 540, '#B6D96E'), (690, 500, 900, 540, '#D9B65A'), (930, 510, 1100, 560, '#C2E07E'), (40, 580, 260, 640, '#C8E38A')]:
        field(w, x0, y0, x1, y1, c)
    # landmarks
    w.add(900, barn(650, 900, S(900), side='l'))
    w.occ(620, 780, 900, 910)
    w.add(1230, barn(780, 1230, S(1230), w=180, h=130, side='l'))
    w.occ(760, 1080, 1080, 1240)
    w.add(1330, windmill(200, 1330, S(1330), blades=0.7))
    w.occ(130, 1180, 280, 1340)
    w.add(1840, townhouse(-20, 1840, 250, 210, S(1840), '#F7E2B4', '#C24B34', side='r', floors=2, cols=3, seed=7))
    w.occ(-20, 1720, 260, 1850)
    pw = S(1500)
    w.flat.append(pond(880, 1520, 130 * pw, 52 * pw, pw))
    w.zones.append((880, 1520, 150 * pw, 70 * pw))
    # paddocks with animals
    for (x0, y0, x1, y1, kind) in [(60, 700, 330, 760, 'sheep'), (720, 1000, 1060, 1050, 'cow'), (420, 1560, 640, 1600, 'pig'), (780, 1790, 1060, 1850, 'cow')]:
        s0, s1 = S(y0), S(y1)
        w.add(y0, fence(x0, y0, x1, y0, s0))
        w.add(y1 + 2, fence(x0, y1 + 50 * s1, x1, y1 + 50 * s1, s1))
        r = rng(int(x0 + y0))
        for q in range(4):
            ax, ay = r.uniform(x0 + 30, x1 - 30), r.uniform(y0 + 14, y1 + 36 * s1)
            fn = {'sheep': sheep, 'cow': cow, 'pig': pig}[kind]
            w.add(ay, fn(ax, ay, S(ay) * 1.45) if kind != 'cow' else cow(ax, ay, S(ay) * 1.45, flip=r.random() < 0.5))
        w.occ(x0, y0 - 20, x1, y1 + 50 * s1)
    for x, y in [(520, 770), (900, 1380), (360, 1950), (680, 2100)]:
        w.add(y, haystack(x, y, S(y)))
        w.occ(x - 40, y - 20, x + 40, y + 10)
    w.add(2000, tractor(700, 2000, S(2000)))
    w.occ(640, 1950, 760, 2010)
    for x, y in [(130, 900), (900, 760), (450, 1250)]:
        w.add(y, townhouse(x, y, 120 * S(y), 110 * S(y), S(y), '#F3D5A0', '#C24B34', side='r' if x < 540 else 'l', floors=2, cols=2, seed=int(x)))
        w.occ(x, y - 30, x + 130 * S(y), y + 10)
    trees_and_bushes(w, extra=[(1.6, lambda x, y, s, r, i: flowers(x, y, s, r)), (0.6, lambda x, y, s, r, i: haystack(x, y, s))], density=0.4)
    w.fg = corner_canopies(w) + haze_and_rays((860, 280))
    return w.render()


# =================================================================== FRUIT & VEG - market farm
def fruit_veg():
    w = World(12)
    w.sky = sky_day(sun=(860, 280), low='#FFE9B8')
    w.back = hills(('#C6E494', '#A9D97A')) + ''.join(windmill(x, HY + 40, 0.28, blades=a) for x, a in [(820, 0.3)])
    w.ground = grass('#B0DF78', '#7CC650', tufts=200)
    w.path([(520, 480), (440, 700), (560, 960), (700, 1220), (540, 1500), (360, 1760), (460, 2060), (560, 2420)], w0=26, w1=150, fill='#E8CF98', edge='#C9A86C')
    # fields in perspective (far -> near)
    crop_rows(w, 40, 560, 380, 660, S(610), 'wheat', '#C9984E', 3)
    crop_rows(w, 650, 600, 1040, 700, S(650), 'sunflower', '#A0683A', 3)
    crop_rows(w, 30, 960, 400, 1100, S(1030), 'lettuce', '#A0683A', 4)
    crop_rows(w, 760, 1320, 1070, 1460, S(1390), 'pumpkin', '#A0683A', 4)
    crop_rows(w, 20, 1560, 300, 1700, S(1630), 'carrot', '#A0683A', 4)
    # greenhouses, barn, market
    w.add(880, greenhouse(700, 880, S(880)))
    w.occ(690, 790, 950, 890)
    w.add(1200, greenhouse(60, 1200, S(1200), w=170))
    w.occ(50, 1080, 320, 1210)
    w.add(1150, barn(830, 1150, S(1150), w=150, h=110, side='l'))
    w.occ(800, 1040, 1080, 1160)
    w.plaza(780, 1880, 260, 100, fill='#EEDDB8')
    for i, (x, y, c) in enumerate([(580, 1830, '#E5533D'), (760, 1810, '#2F9C9A'), (930, 1840, '#FFB82E'), (660, 1960, '#2F9C9A'), (850, 1970, '#E5533D')]):
        w.add(y, stall(x, y, S(y), c))
    for x, y, f in [(520, 1880, '#FF4E4E'), (1000, 1920, '#FF8A3D')]:
        w.add(y, crates(x, y, S(y), f))
    w.add(1480, scarecrow(940, 1480, S(1480)))
    w.add(2120, tractor(260, 2120, S(2120), '#E5533D'))
    w.occ(200, 2070, 330, 2130)
    # orchards
    def orchard(x, y, s, r, i):
        return fruit_tree(x, y, s, r.choice(['#FF4E4E', '#FF8A3D', '#FFD23F']), seed=i)
    w.scatter([(3, orchard), (1.5, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)), (1, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS), '#FF5E7E')), (1.4, lambda x, y, s, r, i: flowers(x, y, s, r))], density=0.42)
    w.fg = corner_canopies(w) + haze_and_rays((860, 280))
    return w.render()




# =================================================================== NATURE - mountain valley
def nature():
    w = World(13)
    w.sky = sky_day(sun=(860, 230))
    w.back = mountains(far='#A9CBE8', near='#86B4DA') + waterfall(480, HY - 90, HY + 40, 46)
    w.ground = grass('#9FD86A', '#5DB84A', tufts=240)
    w.river([(480, 500), (440, 640), (560, 820), (760, 1000), (720, 1220), (480, 1420), (300, 1640), (360, 1880), (560, 2100), (640, 2420)],
            w0=50, w1=260, rails=False, bank='#B7A58A', wall='#8E7E66')
    w.path([(-20, 760), (180, 820), (320, 980), (300, 1200), (120, 1360), (-40, 1420)], w0=20, w1=90, fill='#E3C995', edge='#C3A26A', reserve=True)
    pw = S(1700)
    w.flat.append(pond(860, 1700, 150 * pw, 60 * pw, pw, ducks=True))
    w.zones.append((860, 1700, 170 * pw, 80 * pw))
    w.add(1000, cabin(120, 1000, S(1000)))
    w.occ(110, 880, 300, 1010)
    w.add(1350, cabin(860, 1350, S(1350), w=170, side='l'))
    w.occ(800, 1220, 1080, 1360)
    for x, y, c in [(640, 1560, '#FF8A3D'), (780, 1500, '#4FA3E3'), (160, 1980, '#6CC24A')]:
        w.add(y, tent(x, y, S(y), c))
        w.occ(x - 50, y - 30, x + 70, y + 10)
    w.add(1600, campfire(720, 1610, S(1610)))
    for idx_y, x in [(1180, 540), (2000, 560)]:
        pass
    for x, y in [(400, 1060), (950, 1100), (200, 1500), (900, 2050), (260, 2180)]:
        w.add(y, rock(x, y, S(y) * 1.3))
    w.scatter([(5, lambda x, y, s, r, i: pine(x, y, s * 1.05, r.choice(['#3E9A4F', '#2F8A45', '#4BAA55']))),
               (2, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)),
               (1, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS), r.choice([None, '#FF5E7E']))),
               (1.2, lambda x, y, s, r, i: flowers(x, y, s, r)), (0.4, lambda x, y, s, r, i: rock(x, y, s))], density=0.45)
    w.fg = ''.join(pine(x, y, s, c) for x, y, s, c in [(40, 2460, 2.2, '#2F8A45'), (1040, 2470, 2.1, '#3E9A4F'), (300, 2520, 1.6, '#4BAA55')]) + haze_and_rays((860, 230))
    return w.render()


# =================================================================== TRAVEL - airport + seaside resort
def travel():
    w = World(14)
    w.sky = sky_day(sun=(880, 260)) + plane(300, 260, 0.5, ground=False) + balloon(720, 330, 0.55) + balloon(140, 380, 0.4, ('#4FA3E3', '#FFFFFF'))
    w.back = sea_horizon() + ''.join(boat(x, HY + 20, 0.3, c, True) for x, c in [(260, '#E5533D'), (820, '#2F9C9A')])
    w.ground = grass('#A8DD72', '#74C450', tufts=160)
    # sea + beach on the right, from horizon down to the middle
    beach = [(620, HY + 30), (W + 20, HY + 30), (W + 20, 1500), (900, 1380), (760, 1160), (700, 900)]
    sea = [(700, HY + 30), (W + 20, HY + 30), (W + 20, 1400), (960, 1300), (840, 1100), (780, 860)]
    w.flat.append(poly(beach, '#F4DFA6', w=4) + poly(sea, '#4FB6EC', w=4) +
                  ''.join(f'<path d="M{x} {y} q12 -6 24 0" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.7"/>' for x, y in [(880, 600), (980, 700), (900, 820), (1000, 950), (960, 1150), (1040, 1250)]))
    w.zones.append((900, 900, 260, 520))
    w.add(1180, lighthouse(820, 1180, S(1180)))
    for x, y, c in [(700, 780, '#FF5E7E'), (760, 980, '#4FA3E3'), (850, 1330, '#FFD23F'), (980, 1420, '#FF5E7E')]:
        w.add(y, beach_umbrella(x, y, S(y), c))
    # runway + airport on the left
    rw = [(-20, 1180), (420, 1080), (520, 1180), (40, 1300)]
    w.patch([(-20, 1110), (430, 1040), (560, 1150), (-20, 1300)], '#8E99A6', extra=''.join(
        f'<line x1="{20 + q * 70}" y1="{1190 - q * 22}" x2="{60 + q * 70}" y2="{1178 - q * 22}" stroke="#FFFFFF" stroke-width="6"/>' for q in range(7)))
    w.add(1220, plane(220, 1220, S(1220) * 0.95))
    w.add(980, townhouse(120, 980, 330 * S(980), 140 * S(980), S(980), '#E8F3FA', '#4FA3E3', side='r', floors=2, cols=6, seed=8, roof_kind='flat', flowers=False))
    w.occ(110, 860, 120 + 330 * S(980) + 40, 990)
    w.add(1000, control_tower(560, 1000, S(1000)))
    w.occ(520, 820, 600, 1010)
    road = w.path([(560, 1180), (500, 1400), (360, 1640), (420, 1900), (560, 2160), (520, 2420)], w0=60, w1=150, fill='#9AA5B1', edge=OL, dash='#FFFFFF')
    w.add(1700, car(440, 1700, S(1700) * 1.1, '#E5533D'))
    w.add(2050, car(520, 2050, S(2050) * 1.1, '#FFB82E'))
    # resort hotels
    def hotel(x, by, wd, s, side, r, idx):
        h = wd * r.uniform(1.3, 1.9)
        return townhouse(x, by, wd, h, s, r.choice(['#FFFFFF', '#FFE0A3', '#F5B9A0', '#9FD0C8']), r.choice(['#4FA3E3', '#2F9C9A', '#E2723E']),
                         side=side, floors=4, cols=3, seed=idx, roof_kind='flat', shop=r.choice([None, '#4FA3E3'])), wd, h
    w.rows([1480, 1640, 1820], hotel, gap=0.35, x_from=560, wmin=120, wmax=160)
    for x, y in [(120, 1520), (300, 1440), (80, 1820), (700, 1560), (980, 1600), (640, 2000), (180, 2140)]:
        w.add(y, palm(x, y, S(y), 1 if x < 540 else -1))
    for x, y, c in [(330, 1980, '#4FA3E3'), (370, 1990, '#E5533D'), (240, 1780, '#FFD23F')]:
        w.add(y, suitcase(x, y, S(y), c))
    w.scatter([(3, lambda x, y, s, r, i: palm(x, y, s, r.choice([1, -1]))), (3, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)),
               (1, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS), '#FF5E7E')), (1, lambda x, y, s, r, i: flowers(x, y, s, r))], density=0.34)
    w.fg = ''.join(palm(x, y, s, l) for x, y, s, l in [(40, 2480, 2.0, 1), (1050, 2480, 1.9, -1)]) + corner_canopies(w)[0:0] + haze_and_rays((880, 260))
    return w.render()


# =================================================================== WEATHER - four seasons valley
def weather():
    w = World(15)
    w.sky = sky_day(sun=(880, 240), clouds=False) + rainbow(540, HY + 40, 470) + \
        rain_cloud(170, 170, 1.0) + rain_cloud(420, 110, 0.7, rain=False, dark='#FFFFFF') + rain_cloud(700, 200, 0.8, rain=False, dark='#FFFFFF') + \
        ''.join(f'<path d="M{x} {y} l-14 30 l12 0 l-10 28 l26 -36 l-12 0 l10 -22 Z" fill="#FFD23F" stroke="{OL}" stroke-width="3"/>' for x, y in [(190, 220)])
    w.back = mountains(far='#C9DDF0', near='#A9CBE8', snow='#FFFFFF')
    # snowy top band blending to green
    w.ground = (grass('#E9F4FB', '#A8DD72', tufts=0) +
                f'<rect x="0" y="{HY + 20}" width="{W}" height="520" fill="#F4FAFF"/>'
                f'<path d="M0 1000 Q200 960 400 1010 T800 990 T1080 1010 L1080 1120 Q800 1080 540 1120 T0 1100 Z" fill="#DDEFF8"/>'
                f'<rect x="0" y="1100" width="{W}" height="1300" fill="url(#gr3)" opacity="0"/>')
    w.ground += grass('#A8DD72', '#6CC04A', tufts=180)[0:0]
    w.flat.append(f'<path d="M0 1080 Q300 1040 540 1090 T1080 1070 L1080 2400 L0 2400 Z" fill="#8FD25E"/>'
                  f'<path d="M0 1700 Q300 1660 540 1710 T1080 1690 L1080 2400 L0 2400 Z" fill="#F2C55A" opacity="0.45"/>')
    w.path([(540, 480), (600, 700), (460, 940), (520, 1200), (700, 1460), (560, 1740), (420, 2040), (520, 2420)], w0=26, w1=140, fill='#EAD9B8', edge='#C9AE7E')
    # winter
    for x, y in [(200, 820), (860, 900)]:
        w.add(y, snowman(x, y, S(y) * 1.2))
    w.add(760, cabin(700, 760, S(760), w=160))
    w.occ(690, 660, 900, 770)
    # spring/summer
    for x, y, a in [(160, 1300, 0.2), (900, 1240, 1.0), (980, 1480, 2.0)]:
        w.add(y, wind_turbine(x, y, S(y), a))
        w.occ(x - 20, y - 20, x + 20, y + 10)
    w.add(1400, weather_station(300, 1400, S(1400)))
    w.add(1250, windmill(760, 1250, S(1250) * 0.9, blades=0.6))
    w.occ(700, 1130, 830, 1260)
    pw = S(1600)
    w.flat.append(pond(200, 1600, 120 * pw, 46 * pw, pw, ducks=True))
    w.zones.append((200, 1600, 140 * pw, 60 * pw))
    for x, y, c in [(820, 1640, '#FF5E7E'), (340, 1880, '#4FA3E3'), (900, 2000, '#FFD23F')]:
        w.add(y, umbrella_stand(x, y, S(y), c))
    crop_rows(w, 640, 1780, 980, 1880, S(1830), 'sunflower', '#A0683A', 3)

    def by_season(x, y, s, r, i):
        if y < 1060:
            return pine(x, y, s, '#3E9A4F', snow=True)
        if y > 1720:
            return fluffy_tree(x, y, s, r.choice(['#F2A23A', '#E5733D', '#E8C14A']), seed=i)
        return fluffy_tree(x, y, s, r.choice(GREENS), seed=i) if r.random() < 0.7 else bush(x, y, s, r.choice(GREENS), '#FF5E7E')
    w.scatter([(5, by_season), (1, lambda x, y, s, r, i: flowers(x, y, s, r) if y > 1100 else snowman(x, y, s * 0.7) if r.random() < 0.15 else pine(x, y, s, '#3E9A4F', True))], density=0.5)
    w.fg = ''.join(fluffy_tree(x, y, s, c, seed=i) for i, (x, y, s, c) in enumerate([(70, 2440, 2.1, '#E5733D'), (1030, 2450, 2.0, '#F2A23A'), (330, 2500, 1.7, '#E8C14A')])) + haze_and_rays((880, 240), rays=False)
    return w.render()


# =================================================================== COUNTRIES - world park
def countries():
    w = World(16)
    w.sky = sky_day(sun=(880, 260)) + plane(240, 200, 0.4, ground=False)
    w.back = hills(('#B9E08A', '#A3D676')) + pyramid(150, HY + 30, 0.3) + pagoda(930, HY + 34, 0.25) + lattice_tower(700, HY + 36, 0.22)
    w.ground = grass('#A8DD72', '#74C450', tufts=180)
    cl, wf, L, Rr = w.path([(540, 480), (470, 700), (600, 960), (420, 1240), (600, 1520), (440, 1800), (540, 2100), (500, 2420)], w0=30, w1=150, fill='#EEDDB8', edge='#C9AE7E')
    w.river([(1120, 1500), (960, 1560), (820, 1680), (760, 1820), (900, 1960), (1120, 2020)], w0=50, w1=150, rails=False)
    # landmark islands, each on a plaza
    marks = [(220, 800, lambda x, y: pyramid(x, y, S(y) * 1.7, 1.3)), (840, 860, lambda x, y: pagoda(x, y, S(y) * 1.5)),
             (170, 1300, lambda x, y: lattice_tower(x, y, S(y) * 1.45)), (840, 1300, lambda x, y: windmill(x, y, S(y) * 1.45)),
             (230, 1760, lambda x, y: onion_dome(x, y, S(y) * 1.35)), (760, 2160, lambda x, y: pagoda(x, y, S(y) * 1.3, '#2F9C9A'))]
    for x, y, fn in marks:
        s = S(y) * 1.5
        w.plaza(x, y - 20 * s, 170 * s, 66 * s, reserve=False)
        w.add(y, fn(x, y))
        w.occ(x - 150 * s, y - 160 * s, x + 150 * s, y + 20 * s)
        w.add(y + 30 * s, flowerbed(x - 120 * s, y + 30 * s, s * 0.8, seed=int(x)) + flowerbed(x + 120 * s, y + 30 * s, s * 0.8, seed=int(y)))
    def intl_house(x, by, wd, s, side, r, idx):
        h = wd * r.uniform(0.8, 1.2)
        return townhouse(x, by, wd, h, s, r.choice(['#FFFFFF', '#F7E2B4', '#F2A285', '#9FD0C8', '#FFE0A3']), r.choice(['#D9583C', '#2F9C9A', '#4F6E86', '#E8A65A']),
                         side=side, floors=2, cols=2, seed=idx, roof_kind=r.choice(['gable', 'flat', 'gable'])), wd, h
    w.rows([540, 580, 630], intl_house, gap=0.35, gap_far=0.35)
    flags = [('#E5533D', '#FFFFFF', '#4FA3E3'), ('#000000', '#E5533D', '#FFD23F'), ('#4FA3E3', '#FFFFFF', '#E5533D'), ('#3E9A4F', '#FFFFFF', '#E5533D'), ('#FFD23F', '#3E9A4F', '#E5533D')]
    for i in range(0, len(cl) - 10, 22):
        for P in (L, Rr):
            x, y = P[i]
            if 0 < x < W:
                w.add(y, flagpole(x, y, S(y), flags[(i // 22) % len(flags)], vertical=(i // 22) % 2 == 0))
    w.scatter([(3, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)), (1.5, lambda x, y, s, r, i: palm(x, y, s, r.choice([1, -1]))),
               (1, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS), '#FF5E7E')), (1.3, lambda x, y, s, r, i: flowers(x, y, s, r))], density=0.34)
    w.fg = corner_canopies(w) + haze_and_rays((880, 260))
    return w.render()


# =================================================================== SPORT - sports park
def sport():
    w = World(17)
    w.sky = sky_day(sun=(880, 260))
    w.back = skyline(gap=(780, 960), tower=None)
    w.ground = grass('#A8DD72', '#6CC04A', tufts=140)
    w.path([(540, 480), (600, 720), (470, 980), (560, 1260), (420, 1540), (560, 1820), (480, 2120), (520, 2420)], w0=40, w1=150, fill='#D8664A', edge='#FFFFFF', dash='#FFFFFF')
    w.add(820, stadium(560, 820, S(820)))
    w.occ(560 - 300 * S(820), 640, 560 + 300 * S(820), 830)
    pitch(w, 60, 1000, 400, 1160, kind='football')
    w.add(1000, goal(90, 1080, S(1080)))
    pitch(w, 700, 1060, 1040, 1200, col='#4FA3E3', kind='tennis')
    pitch(w, 650, 1520, 1050, 1680, col='#E8A65A', kind='basket')
    w.add(1600, hoop(690, 1610, S(1610)))
    w.add(1600, hoop(1010, 1600, S(1600)))
    pitch(w, 40, 1660, 360, 1840, kind='football')
    for x, y, c in [(70, 980, '#FFD23F'), (720, 1040, '#E5533D'), (680, 1500, '#4FA3E3'), (60, 1640, '#FF8A3D')]:
        w.add(y, bleachers(x, y, S(y), 220, c))
    for x, y in [(330, 1330), (880, 1360), (300, 2050), (840, 2000)]:
        w.add(y, lamp(x, y, S(y) * 1.2))
    w.scatter([(4, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)), (1, lambda x, y, s, r, i: poplar(x, y, s)),
               (1, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS))), (1, lambda x, y, s, r, i: flowers(x, y, s, r))], density=0.34)
    w.fg = corner_canopies(w) + haze_and_rays((880, 260))
    return w.render()


# =================================================================== SCHOOL - campus
def school_map():
    w = World(18)
    w.sky = sky_day(sun=(880, 260))
    w.back = hills(('#B9E08A', '#A3D676'))
    w.ground = grass('#A8DD72', '#6CC04A', tufts=160)
    w.path([(540, 480), (480, 720), (560, 1000), (420, 1300), (520, 1600), (440, 1900), (520, 2420)], w0=36, w1=140, fill='#EEDDB8', edge='#C9AE7E')
    w.add(1000, school(600, 1000, S(1000)))
    w.occ(600, 760, 600 + 330 * S(1000) + 80, 1010)
    w.plaza(760, 1080, 230, 60, reserve=True)
    road = w.path([(-20, 1250), (300, 1200), (700, 1250), (1100, 1200)], w0=90, w1=40, fill='#9AA5B1', edge=OL, dash='#FFFFFF')
    w.add(1250, bus(560, 1252, S(1250) * 1.2))
    pitch(w, 620, 1500, 1050, 1680, kind='football')
    for x, y in [(160, 1460), (330, 1520)]:
        w.add(y, slide(x, y, S(y) * 1.3))
    w.add(1600, swing(220, 1640, S(1640) * 1.3))
    w.patch([(80, 1400), (420, 1390), (440, 1680), (60, 1690)], '#F2D9A6', extra='')
    def house_row(x, by, wd, s, side, r, idx):
        h = wd * r.uniform(0.9, 1.3)
        return townhouse(x, by, wd, h, s, r.choice(['#F6C27A', '#F2A285', '#F7E2B4', '#9FD0C8']), r.choice(['#D9583C', '#4F6E86', '#2F9C9A']), side=side,
                         floors=2, cols=2, seed=idx), wd, h
    w.rows([560, 610, 680, 760], house_row, gap=0.35)
    w.rows([1880, 2050], house_row, gap=0.4, wmin=140, wmax=180)
    w.scatter([(4, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)), (1, lambda x, y, s, r, i: poplar(x, y, s)),
               (1, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS), '#FF5E7E')), (1, lambda x, y, s, r, i: flowers(x, y, s, r))], density=0.34)
    w.fg = corner_canopies(w) + haze_and_rays((880, 260))
    return w.render()


# =================================================================== JOBS - busy town at work
def jobs():
    w = World(19)
    w.sky = sky_day(sun=(880, 260))
    w.back = skyline(tower=None) + crane(160, HY + 30, 0.35) + crane(940, HY + 30, 0.3)
    w.ground = grass('#A8DD72', '#6CC04A', tufts=120)
    w.path([(540, 480), (600, 720), (480, 1000), (560, 1300), (440, 1600), (560, 1900), (500, 2420)], w0=60, w1=150, fill='#9AA5B1', edge=OL, dash='#FFFFFF')
    # construction site upper right
    w.patch([(660, 780), (1080, 760), (1080, 1000), (640, 1020)], '#D9B07A')
    w.add(980, site_building(780, 980, S(980), 220, 200, side='l'))
    w.add(1000, crane(700, 1000, S(1000)))
    w.add(1010, tractor(980, 1010, S(1010), '#FFC21A'))
    # services
    w.add(1250, labelled_house(40, 1250, S(1250), 280, 190, '#E5533D', '#7A3B2A', '#FFFFFF', 'flame', side='r', garage=True))
    w.occ(30, 1100, 330, 1260)
    w.add(1290, truck(380, 1300, S(1300)))
    w.add(1450, labelled_house(700, 1450, S(1450), 300, 230, '#FFFFFF', '#4FA3E3', '#FFFFFF', 'cross', side='l'))
    w.occ(690, 1260, 1080, 1460)
    w.add(1760, labelled_house(20, 1760, S(1760), 250, 200, '#F7E2B4', '#C24B34', '#FFFFFF', 'bread', side='r'))
    w.occ(10, 1600, 300, 1770)
    w.add(1980, labelled_house(760, 1980, S(1980), 280, 210, '#9FD0C8', '#4F6E86', '#FFFFFF', 'mail', side='l'))
    w.occ(700, 1820, 1080, 1990)
    w.add(1700, car(560, 1700, S(1700) * 1.1, '#4FA3E3'))
    w.add(2150, truck(420, 2150, S(2150) * 0.9, '#FFC21A', ladder=False))

    def shop_row(x, by, wd, s, side, r, idx):
        h = wd * r.uniform(1.0, 1.5)
        return townhouse(x, by, wd, h, s, r.choice(['#F6C27A', '#F2A285', '#F7E2B4', '#E99A6A', '#9FD0C8']), r.choice(['#D9583C', '#4F6E86', '#2F9C9A', '#C24B34']),
                         side=side, floors=2 if h < 150 * s else 3, cols=3, seed=idx, shop=r.choice(['#E5533D', '#2F9C9A', '#FFB82E', None])), wd, h
    w.rows([560, 610, 670, 740, 820, 1140], shop_row, gap=0.25)
    for x, y in [(380, 1100), (660, 1250), (360, 1880), (640, 2050)]:
        w.add(y, lamp(x, y, S(y)))
    w.scatter([(4, lambda x, y, s, r, i: fluffy_tree(x, y, s, r.choice(GREENS), seed=i)), (1, lambda x, y, s, r, i: bush(x, y, s, r.choice(GREENS))),
               (1, lambda x, y, s, r, i: flowers(x, y, s, r))], density=0.4)
    w.fg = corner_canopies(w) + haze_and_rays((880, 260))
    return w.render()


BUILDERS = {'animals': animals, 'fruit_veg': fruit_veg, 'nature': nature, 'travel': travel, 'weather': weather,
            'countries': countries, 'sport': sport, 'school': school_map, 'jobs': jobs}
