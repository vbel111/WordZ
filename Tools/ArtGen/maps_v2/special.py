"""Special-world maps (v2): SPACE, OCEAN (underwater), ELECTRONIC (circuit city)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from props import T, hi, shadow  # noqa: E402
from scene import (H, OL, VX, W, Scene, combine, hills, lin, rad, shade, sparkle, tex_dashes, tex_edge_dots,  # noqa: E402
                   tex_stones)

# =====================================================================================
# SPACE
# =====================================================================================


def crater(x, y, s, c='#7C66BE'):
    b = (f'<ellipse cx="0" cy="0" rx="70" ry="24" fill="{shade(c, 0.18)}"/>'
         f'<ellipse cx="0" cy="2" rx="52" ry="15" fill="{shade(c, -0.25)}" stroke="none"/>'
         f'<path d="M-52 2 Q0 -14 52 2" fill="none" stroke="{shade(c, 0.35)}" stroke-width="4"/>')
    return T(x, y, s, b)


def crystal(x, y, s, c='#6FF2FF'):
    d = shade(c, -0.25)
    b = shadow(40)
    for dx, h, w, rot in [(-20, 90, 18, -14), (8, 130, 22, 4), (32, 70, 16, 18)]:
        b += (f'<g transform="rotate({rot} {dx} 0)"><path d="M{dx - w} 0 L{dx - w} {-h * 0.7:.0f} L{dx} {-h} L{dx + w} {-h * 0.7:.0f} L{dx + w} 0 Z" fill="{c}"/>'
              f'<path d="M{dx} {-h} L{dx + w} {-h * 0.7:.0f} L{dx + w} 0 L{dx} 0 Z" fill="{d}" stroke="none"/></g>')
    b += f'<circle cx="0" cy="-60" r="70" fill="{c}" opacity="0.15" stroke="none"/>'
    return T(x, y, s, b)


def space_rock(x, y, s, c='#6A55B0'):
    b = (shadow(44) + f'<path d="M-44 0 Q-50 -34 -20 -44 Q10 -58 40 -34 Q52 -16 44 0 Z" fill="{c}"/>'
         f'<path d="M10 -50 Q44 -40 44 0 L18 0 Q22 -26 10 -50 Z" fill="{shade(c, -0.2)}" stroke="none"/>'
         f'<circle cx="-16" cy="-26" r="7" fill="{shade(c, -0.2)}" stroke="none"/>' + hi(-24, -34, 10, 5, 0.3))
    return T(x, y, s, b)


def alien_plant(x, y, s, c='#7CF0A6'):
    b = shadow(26)
    for dx, h, bc in [(-18, 70, '#FF9EC4'), (0, 100, '#FFE36A'), (20, 60, '#6FF2FF')]:
        b += (f'<path d="M{dx} 0 Q{dx - 10} {-h / 2} {dx} {-h}" fill="none" stroke="{c}" stroke-width="7"/>'
              f'<circle cx="{dx}" cy="{-h}" r="12" fill="{bc}" stroke-width="3"/><circle cx="{dx}" cy="{-h}" r="22" fill="{bc}" opacity="0.25" stroke="none"/>')
    return T(x, y, s, b)


def dome(x, y, s):
    b = (shadow(100) + '<rect x="-96" y="-30" width="192" height="30" fill="#BFC9D6"/>'
         '<path d="M-86 -30 A86 76 0 0 1 86 -30 Z" fill="#9FE3F5" fill-opacity="0.85"/>'
         '<path d="M-86 -30 A86 76 0 0 1 86 -30 M-50 -30 Q-46 -90 0 -106 M50 -30 Q46 -90 0 -106 M-82 -60 L82 -60" fill="none" stroke-width="3"/>'
         '<rect x="-20" y="-28" width="40" height="28" rx="6" fill="#4F5D7E"/>' + hi(-46, -80, 16, 8, 0.6)
         + '<circle cx="-30" cy="-50" r="16" fill="#7CF0A6"/><circle cx="24" cy="-46" r="12" fill="#7CF0A6"/>')
    return T(x, y, s, b)


def dish(x, y, s):
    b = (shadow(40) + '<path d="M-10 0 L0 -60 L10 0 Z" fill="#9AA6B8"/>'
         '<path d="M-60 -110 Q-30 -40 30 -50 Q-10 -80 -60 -110 Z" fill="#E9EEF5"/><path d="M-12 -74 L40 -110" stroke-width="5"/>'
         '<circle cx="42" cy="-112" r="8" fill="#FF6B8B"/><circle cx="42" cy="-112" r="22" fill="#FF6B8B" opacity="0.25" stroke="none"/>')
    return T(x, y, s, b)


def rocket(x, y, s):
    b = (shadow(90) + '<rect x="-100" y="-20" width="200" height="20" fill="#4F5D7E"/>'
         '<path d="M-80 -20 L-60 -200 M80 -20 L60 -200" stroke="#9AA6B8" stroke-width="10"/><path d="M-80 -20 L-60 -200 M80 -20 L60 -200" stroke-width="3"/>'
         '<path d="M-34 -40 L-34 -230 Q-34 -320 0 -350 Q34 -320 34 -230 L34 -40 Z" fill="#FBF1DE"/>'
         '<path d="M-34 -100 L-70 -40 L-34 -40 Z M34 -100 L70 -40 L34 -40 Z" fill="#E5533D"/>'
         '<path d="M-10 -40 L10 -40 L4 -20 L-4 -20 Z" fill="#9AA6B8"/>'
         '<path d="M-26 -300 Q0 -340 26 -300 Z" fill="#E5533D" stroke="none"/><circle cx="0" cy="-220" r="18" fill="#9FD3F2"/>'
         '<rect x="-34" y="-160" width="68" height="12" fill="#4FA3E3" stroke="none"/>' + hi(-18, -270, 6, 30, 0.45))
    return T(x, y, s, b)


def space_lamp(x, y, s):
    b = (shadow(14, 4) + '<rect x="-4" y="-110" width="8" height="110" fill="#4F5D7E"/>'
         '<circle cx="0" cy="-120" r="14" fill="#6FF2FF"/><circle cx="0" cy="-120" r="34" fill="#6FF2FF" opacity="0.25" stroke="none"/>')
    return T(x, y, s, b)


def ringed_planet(x, y, r, c, ring='#FFE9A6'):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.9}" ry="{r * 0.45}" fill="none" stroke="{ring}" stroke-width="{r * 0.16}" transform="rotate(-18 {x} {y})" opacity="0.9"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{OL}" stroke-width="6"/>'
            f'<path d="M{x - r * 0.9} {y - r * 0.2} Q{x} {y - r * 0.45} {x + r * 0.9} {y - r * 0.1}" stroke="{shade(c, -0.15)}" stroke-width="{r * 0.14}" fill="none"/>'
            f'<path d="M{x - r * 0.8} {y + r * 0.35} Q{x} {y + r * 0.15} {x + r * 0.85} {y + r * 0.4}" stroke="{shade(c, 0.2)}" stroke-width="{r * 0.12}" fill="none"/>'
            f'<path d="M{x - r * 1.9} {y + r * 0.62} A{r * 1.9} {r * 0.45} -18 0 0 {x + r * 1.75} {y - r * 0.55}" fill="none" stroke="{ring}" stroke-width="{r * 0.16}" transform="rotate(0)" opacity="0"/>'
            f'<circle cx="{x - r * 0.4}" cy="{y - r * 0.45}" r="{r * 0.18}" fill="#FFFFFF" opacity="0.35"/>')


def planet(x, y, r, c):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{OL}" stroke-width="5"/>'
            f'<circle cx="{x + r * 0.3}" cy="{y + r * 0.2}" r="{r * 0.22}" fill="{shade(c, -0.15)}"/>'
            f'<circle cx="{x - r * 0.35}" cy="{y + r * 0.35}" r="{r * 0.12}" fill="{shade(c, -0.15)}"/>'
            f'<circle cx="{x - r * 0.35}" cy="{y - r * 0.35}" r="{r * 0.2}" fill="#FFFFFF" opacity="0.35"/>')


def space():
    sc = Scene(seed=151, curve=90, curve_freq=1.3, path_w=(80, 420))
    sc.sky([(0, '#14123A'), (0.6, '#2B2470'), (1, '#5A3F9E')], stars=170)
    sc.backdrop(ringed_planet(250, 300, 110, '#F5A65B') + planet(870, 180, 60, '#6FC6F2') + planet(760, 560, 34, '#FF9EC4'))
    sc.backdrop('<path d="M940 420 L700 560" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.5"/><circle cx="940" cy="420" r="12" fill="#FFF3C4" stroke="#4A2410" stroke-width="3"/>')
    hz = sc.horizon
    sc.backdrop(hills(hz, [('#7E64C0', 170), ('#9278CF', 90)], seed=13, amp=(90, 140)))
    sc.backdrop(dome(860, hz - 30, 0.4) + dish(160, hz - 40, 0.45))
    sc.ground([(0, '#A48ED8'), (0.2, '#8C74C8'), (1, '#6E58B4')])
    sc.path('#3B3270', texture=combine(tex_dashes('#6FF2FF'), tex_edge_dots('#6FF2FF', 0.035)), border=('#5C4C9C', 14))
    sc.place(rocket, 0.3, 1, 300)
    sc.place(dome, 0.5, -1, 300)
    sc.place(dish, 0.7, 1, 200)
    sc.place(dome, 0.12, -1, 200)
    for t in (0.18, 0.4, 0.62, 0.86):
        sc.place(space_lamp, t, -1, 40)
        sc.place(space_lamp, t + 0.03, 1, 40)
    sc.populate([(3, lambda x, y, s: crater(x, y, s * 1.3)), (2, lambda x, y, s: space_rock(x, y, s * 1.3)),
                 (2, lambda x, y, s: crystal(x, y, s * 1.35, sc.r.choice(['#6FF2FF', '#FF9EC4', '#B6F07A']))),
                 (2, lambda x, y, s: alien_plant(x, y, s * 1.4))], gap=170, start=(110, 170), step=0.06, avoid=[(sc.side_x(0.3, 1, 300), sc.ty(0.3), 160, 60),
                                                                                   (sc.side_x(0.5, -1, 300), sc.ty(0.5), 170, 60)])
    sc.scatter(lambda x, y, s: sparkle(x, y - 30 * s, 0.4 + 0.5 * s, '#6FF2FF', 0.7), 30, 0.05, 1.0, 60, 520)
    sc.haze('#B9A6F0', 340, 0.4)
    sc.bottom_fade(0.3)
    return sc.render()


# =====================================================================================
# OCEAN (underwater reef)
# =====================================================================================

def fish(x, y, s, c='#FFB21E', flip=False):
    b = (f'<path d="M-40 0 Q-10 -30 30 -10 L52 -26 L48 0 L52 26 L30 10 Q-10 30 -40 0 Z" fill="{c}"/>'
         f'<path d="M-6 -20 Q4 0 -6 20" fill="none" stroke="#FFFFFF" stroke-width="6"/><path d="M-6 -20 Q4 0 -6 20" fill="none" stroke-width="2"/>'
         '<circle cx="-24" cy="-4" r="5" fill="#FFFFFF" stroke-width="2"/><circle cx="-25" cy="-4" r="2.5" fill="#4A2410" stroke="none"/>')
    return T(x, y, s, b, flip)


def jelly(x, y, s, c='#FF9EC4'):
    b = (f'<path d="M-30 0 Q-30 -40 0 -40 Q30 -40 30 0 Q20 -6 10 0 Q0 -6 -10 0 Q-20 -6 -30 0 Z" fill="{c}" fill-opacity="0.9"/>'
         + ''.join(f'<path d="M{dx} 0 q6 16 0 30 q-6 14 0 26" fill="none" stroke="{c}" stroke-width="4"/>' for dx in (-18, -6, 6, 18)) +
         hi(-12, -26, 8, 5, 0.6))
    return T(x, y, s, b)


def coral_branch(x, y, s, c='#FF7F7F'):
    d = shade(c, -0.2)
    b = shadow(50)
    for path, w in [('M0 0 Q-4 -50 -30 -80 Q-46 -100 -40 -130', 20), ('M-2 -40 Q20 -70 40 -90 Q52 -104 50 -124', 18),
                    ('M-26 -74 Q-60 -80 -70 -104', 14), ('M30 -80 Q50 -70 66 -84', 12), ('M0 0 Q6 -40 4 -110', 16)]:
        b += f'<path d="{path}" fill="none" stroke="{OL}" stroke-width="{w + 8}"/><path d="{path}" fill="none" stroke="{c}" stroke-width="{w}"/>'
    b += f'<path d="M-36 -116 Q-38 -96 -30 -80" fill="none" stroke="{shade(c, 0.35)}" stroke-width="5"/>'
    return T(x, y, s, b)


def fan_coral(x, y, s, c='#B98CF2'):
    b = shadow(50) + f'<path d="M0 0 Q-80 -60 -60 -130 Q0 -170 60 -130 Q80 -60 0 0 Z" fill="{c}"/>'
    for a in range(-60, 61, 20):
        r = math.radians(a - 90)
        b += f'<path d="M0 -6 L{math.cos(r) * 110:.0f} {-6 + math.sin(r) * 110:.0f}" stroke="{shade(c, -0.25)}" stroke-width="4"/>'
    b += f'<path d="M-40 -70 Q0 -100 40 -70 M-50 -110 Q0 -140 50 -110" fill="none" stroke="{shade(c, -0.25)}" stroke-width="4"/>'
    return T(x, y, s, b)


def brain_coral(x, y, s, c='#F7B267'):
    b = (shadow(54) + f'<path d="M-56 0 Q-60 -64 0 -66 Q60 -64 56 0 Z" fill="{c}"/>'
         f'<path d="M-40 -14 q10 -20 20 0 q10 20 20 0 q10 -20 20 0 M-30 -38 q10 -16 20 0 q10 16 20 0 q10 -16 20 0" fill="none" stroke="{shade(c, -0.25)}" stroke-width="5"/>'
         + hi(-26, -50, 12, 6, 0.4))
    return T(x, y, s, b)


def seaweed(x, y, s, c='#3EBA7A'):
    b = shadow(26)
    for dx, h, ph in [(-14, 170, 0), (4, 220, 1), (20, 150, 2)]:
        pts = ' '.join(f'{dx + math.sin(k * 0.7 + ph) * 14:.0f},{-k * h / 10:.0f}' for k in range(11))
        b += f'<polyline points="{pts}" fill="none" stroke="{OL}" stroke-width="18"/><polyline points="{pts}" fill="none" stroke="{c}" stroke-width="11"/>'
    return T(x, y, s, b)


def shell(x, y, s, c='#FFC3D4'):
    b = (shadow(20) + f'<path d="M-24 0 Q-30 -30 0 -36 Q30 -30 24 0 Z" fill="{c}"/>'
         + ''.join(f'<path d="M0 -2 L{dx} -32" stroke="{shade(c, -0.2)}" stroke-width="3"/>' for dx in (-16, -6, 6, 16)) +
         f'<rect x="-8" y="-6" width="16" height="8" rx="3" fill="{shade(c, -0.1)}"/>')
    return T(x, y, s, b)


def starfish(x, y, s, c='#FF8A3D'):
    pts = []
    for k in range(10):
        r = 30 if k % 2 == 0 else 13
        a = -math.pi / 2 + k * math.pi / 5
        pts.append(f'{math.cos(a) * r:.1f} {math.sin(a) * r * 0.55 - 6:.1f}')
    b = shadow(26, 6) + f'<path d="M{" L".join(pts)} Z" fill="{c}"/>' + ''.join(f'<circle cx="{math.cos(-math.pi / 2 + k * 2 * math.pi / 5) * 14:.0f}" cy="{math.sin(-math.pi / 2 + k * 2 * math.pi / 5) * 7 - 6:.0f}" r="2.5" fill="#FFE0B0" stroke="none"/>' for k in range(5))
    return T(x, y, s, b)


def chest(x, y, s):
    b = (shadow(60) + '<rect x="-56" y="-60" width="112" height="60" rx="6" fill="#A8642E"/>'
         '<path d="M-60 -56 L-56 -108 L56 -108 L60 -56 Z" fill="#C9874A" transform="rotate(-14 -56 -60)"/>'
         '<path d="M-40 -66 L40 -66 L30 -90 L-30 -90 Z" fill="#FFC93C" stroke="none" opacity="0.9"/>'
         '<circle cx="-14" cy="-76" r="10" fill="#FFD84A"/><circle cx="12" cy="-80" r="10" fill="#FFD84A"/><circle cx="0" cy="-70" r="9" fill="#FFE97A"/>'
         '<rect x="-56" y="-44" width="112" height="10" fill="#7A4520"/><rect x="-10" y="-50" width="20" height="22" rx="4" fill="#FFC93C"/>')
    return T(x, y, s, b)


def anchor(x, y, s):
    b = (shadow(40) + '<g transform="rotate(-20)"><path d="M0 -10 L0 -150" stroke-width="16"/><path d="M0 -10 L0 -150" stroke="#7A8798" stroke-width="9"/>'
         '<path d="M-50 -50 Q-50 -6 0 -6 Q50 -6 50 -50" fill="none" stroke-width="16"/><path d="M-50 -50 Q-50 -6 0 -6 Q50 -6 50 -50" fill="none" stroke="#7A8798" stroke-width="9"/>'
         '<circle cx="0" cy="-164" r="16" fill="none" stroke-width="14"/><circle cx="0" cy="-164" r="16" fill="none" stroke="#7A8798" stroke-width="7"/>'
         '<rect x="-30" y="-130" width="60" height="12" rx="5" fill="#7A8798"/></g>')
    return T(x, y, s, b)


def shipwreck(cx, base):
    c = '#5D8FB5'
    return (f'<g opacity="0.75"><path d="M{cx - 200} {base - 120} L{cx + 160} {base - 60} L{cx + 130} {base} L{cx - 170} {base} Z" fill="{c}"/>'
            f'<rect x="{cx - 60}" y="{base - 330}" width="16" height="230" fill="{c}" transform="rotate(12 {cx - 52} {base - 100})"/>'
            f'<path d="M{cx - 30} {base - 300} L{cx + 70} {base - 250} L{cx - 20} {base - 170} Z" fill="{c}" opacity="0.8" transform="rotate(12 {cx - 52} {base - 100})"/>'
            f'<circle cx="{cx - 100}" cy="{base - 70}" r="14" fill="#3E7099"/><circle cx="{cx - 40}" cy="{base - 56}" r="14" fill="#3E7099"/></g>')


def ocean():
    sc = Scene(seed=161, curve=100, curve_freq=1.4, path_w=(80, 420))
    sc.sky([(0, '#9BE4F7'), (0.12, '#5EC4EE'), (0.6, '#2E94D2'), (1, '#2A7FBF')])
    # surface ripples and light rays
    sc.backdrop(''.join(f'<path d="M{x} 40 q30 -16 60 0 q30 16 60 0" stroke="#FFFFFF" stroke-width="5" fill="none" opacity="0.6"/>' for x in range(-40, W, 150)))
    for k, (x0, w) in enumerate([(120, 90), (360, 60), (600, 110), (860, 70)]):
        sc.backdrop(f'<path d="M{x0} 0 L{x0 + w} 0 L{x0 + w + 220} {sc.horizon} L{x0 + 120} {sc.horizon} Z" fill="#FFFFFF" opacity="0.10"/>')
    hz = sc.horizon
    # whale far away, fish, jellies, bubbles
    sc.backdrop('<g opacity="0.45"><path d="M700 340 Q760 280 880 300 Q960 314 990 360 Q1010 330 1040 320 Q1030 360 1040 400 Q1000 380 980 380 Q900 420 780 400 Q720 390 700 340 Z" fill="#1F6FA8"/></g>')
    for x, y, s, c, f in [(200, 260, 0.9, '#FFB21E', False), (260, 300, 0.6, '#FFB21E', False), (150, 320, 0.6, '#FFB21E', False),
                          (820, 560, 0.8, '#FF7F7F', True), (520, 460, 0.6, '#FFE36A', True), (330, 640, 0.7, '#7CF0A6', False),
                          (900, 700, 0.5, '#B98CF2', True)]:
        sc.backdrop(fish(x, y, s, c, f))
    sc.backdrop(jelly(620, 230, 0.9) + jelly(110, 560, 0.6, '#C9A6F5'))
    sc.backdrop(''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.7"/>' for x, y, r in
                        [(460, 600, 10), (470, 560, 7), (455, 520, 5), (980, 500, 9), (990, 460, 6), (60, 200, 8), (70, 170, 5)]))
    sc.backdrop(hills(hz, [('#4A9CC9', 120), ('#5FB0CF', 60)], seed=17, amp=(60, 100)))
    sc.backdrop(shipwreck(830, hz - 20))
    sc.ground([(0, '#9FCFC8'), (0.15, '#E2D7A8'), (1, '#F0D29A')])
    sc.path('#F7E6BE', texture=combine(tex_stones('#E6CD98', 140), tex_edge_dots('#FFFFFF', 0.045)))
    sc.place(chest, 0.66, -1, 160)
    sc.place(anchor, 0.42, 1, 200)
    sc.populate([(3, lambda x, y, s: coral_branch(x, y, s, sc.r.choice(['#FF7F7F', '#FF9EC4', '#FFB26B']))), (2, fan_coral), (2, brain_coral),
                 (3, lambda x, y, s: seaweed(x, y, s, sc.r.choice(['#3EBA7A', '#5FCB6A'])))], gap=150, start=(120, 190), step=0.055,
                avoid=[(sc.side_x(0.66, -1, 160), sc.ty(0.66), 120, 50), (sc.side_x(0.42, 1, 200), sc.ty(0.42), 100, 40)])
    sc.scatter(lambda x, y, s: shell(x, y, s, sc.r.choice(['#FFC3D4', '#FFE0B0', '#FFFFFF'])), 26, 0.1, 1.0, 20, 140)
    sc.scatter(lambda x, y, s: starfish(x, y, s, sc.r.choice(['#FF8A3D', '#FF6B8B', '#FFC93C'])), 14, 0.2, 1.0, 20, 160)
    sc.haze('#7CC6EA', 420, 0.6)
    sc.bottom_fade(0.15)
    return sc.render()


# =====================================================================================
# ELECTRONIC (circuit-board city at night)
# =====================================================================================

def chip(x, y, s):
    b = shadow(70, 14)
    for k in range(5):
        b += f'<rect x="{-54 + k * 26}" y="-30" width="8" height="30" fill="#D8D8D8"/>'
    b += '<path d="M-70 -30 L70 -30 L56 -70 L-56 -70 Z" fill="#2C3346"/><path d="M-70 -30 L70 -30 L70 -20 L-70 -20 Z" fill="#1E2433"/>'
    b += '<rect x="-24" y="-60" width="48" height="20" rx="3" fill="#3E4762" stroke="#6FF2FF" stroke-width="2"/><circle cx="-44" cy="-36" r="4" fill="#9AA6B8" stroke="none"/>'
    return T(x, y, s, b)


def capacitor(x, y, s, c='#4F7FC8'):
    b = (shadow(30) + '<path d="M-8 0 L-8 16 M8 0 L8 16" stroke="#D8D8D8" stroke-width="4"/>'
         f'<rect x="-26" y="-90" width="52" height="90" rx="8" fill="{c}"/><ellipse cx="0" cy="-90" rx="26" ry="9" fill="#BFC9D6"/>'
         '<path d="M-4 -98 l8 8 M4 -98 l-8 8" stroke-width="2.5"/><rect x="10" y="-80" width="8" height="70" fill="#FFFFFF" opacity="0.5" stroke="none"/>')
    return T(x, y, s, b)


def resistor(x, y, s):
    b = (shadow(50) + '<path d="M-70 -14 L70 -14" stroke="#D8D8D8" stroke-width="5"/>'
         '<rect x="-44" y="-30" width="88" height="32" rx="14" fill="#E9D3A8"/>'
         + ''.join(f'<rect x="{-26 + k * 16}" y="-29" width="8" height="30" fill="{c}" stroke="none"/>' for k, c in enumerate(['#E5533D', '#6C5CE7', '#FFC93C', '#8A5326'])))
    return T(x, y, s, b)


def led(x, y, s, c='#FF6B8B'):
    b = (f'<circle cx="0" cy="-60" r="46" fill="{c}" opacity="0.22" stroke="none"/>'
         '<path d="M-8 0 L-8 -30 M8 0 L8 -40" stroke="#D8D8D8" stroke-width="4"/>'
         f'<path d="M-20 -36 L-20 -70 Q-20 -92 0 -92 Q20 -92 20 -70 L20 -36 Z" fill="{c}"/><rect x="-24" y="-40" width="48" height="8" rx="3" fill="{c}"/>'
         + hi(-8, -74, 5, 9, 0.6))
    return T(x, y, s, b)


def battery(x, y, s):
    b = (shadow(30) + '<rect x="-26" y="-120" width="52" height="120" rx="8" fill="#3A3A44"/><rect x="-26" y="-120" width="52" height="40" rx="8" fill="#FFC93C"/>'
         '<rect x="-10" y="-132" width="20" height="12" rx="3" fill="#BFC9D6"/><path d="M-6 -56 h12 M0 -62 v12" stroke="#FFFFFF" stroke-width="4"/>')
    return T(x, y, s, b)


def robot(x, y, s, c='#9FD3F2'):
    b = (shadow(50) + '<rect x="-30" y="-30" width="18" height="30" rx="6" fill="#7A8798"/><rect x="12" y="-30" width="18" height="30" rx="6" fill="#7A8798"/>'
         f'<rect x="-44" y="-100" width="88" height="74" rx="16" fill="{c}"/><rect x="-24" y="-80" width="48" height="30" rx="6" fill="#2C3346"/>'
         '<circle cx="-10" cy="-66" r="6" fill="#6FF2FF" stroke="none"/><circle cx="12" cy="-66" r="6" fill="#6FF2FF" stroke="none"/>'
         f'<rect x="-36" y="-160" width="72" height="56" rx="16" fill="{c}"/><circle cx="-14" cy="-134" r="9" fill="#FFFFFF"/><circle cx="14" cy="-134" r="9" fill="#FFFFFF"/>'
         '<circle cx="-14" cy="-134" r="4" fill="#2C3346" stroke="none"/><circle cx="14" cy="-134" r="4" fill="#2C3346" stroke="none"/>'
         '<path d="M0 -160 L0 -184" stroke-width="4"/><circle cx="0" cy="-188" r="7" fill="#FF6B8B"/>'
         '<path d="M-44 -90 Q-66 -70 -60 -44 M44 -90 Q66 -70 60 -44" fill="none" stroke-width="10"/><path d="M-44 -90 Q-66 -70 -60 -44 M44 -90 Q66 -70 60 -44" fill="none" stroke="#7A8798" stroke-width="5"/>'
         + hi(-22, -150, 10, 5, 0.5))
    return T(x, y, s, b)


def device_skyline(hz):
    out = []
    # laptop
    out.append(f'<path d="M80 {hz} L120 {hz - 30} L440 {hz - 30} L480 {hz} Z" fill="#7A8AB8" stroke="{OL}" stroke-width="6"/>'
               f'<rect x="130" y="{hz - 250}" width="300" height="220" rx="14" fill="#55639A" stroke="{OL}" stroke-width="6"/>'
               f'<rect x="148" y="{hz - 232}" width="264" height="180" rx="6" fill="#3BD1E8" opacity="0.9"/>'
               + ''.join(f'<rect x="{166}" y="{hz - 214 + k * 30}" width="{180 - k * 26}" height="12" rx="6" fill="#E9FBFF" opacity="0.8"/>' for k in range(5)))
    # phone tower
    out.append(f'<rect x="520" y="{hz - 420}" width="150" height="420" rx="24" fill="#4C5A8E" stroke="{OL}" stroke-width="6"/>'
               f'<rect x="534" y="{hz - 392}" width="122" height="350" rx="8" fill="#FF9EC4"/>'
               + ''.join(f'<rect x="{548 + (k % 3) * 36}" y="{hz - 376 + (k // 3) * 40}" width="26" height="26" rx="7" fill="{["#FFFFFF", "#FFE36A", "#6FF2FF", "#B6F07A"][k % 4]}"/>' for k in range(18)) +
               f'<rect x="575" y="{hz - 410}" width="40" height="6" rx="3" fill="#2C3346"/>')
    # monitor + antenna tower
    out.append(f'<rect x="720" y="{hz - 300}" width="260" height="190" rx="10" fill="#55639A" stroke="{OL}" stroke-width="6"/>'
               f'<rect x="736" y="{hz - 284}" width="228" height="158" rx="4" fill="#7CF0A6" opacity="0.85"/>'
               f'<path d="M760 {hz - 160} L800 {hz - 220} L840 {hz - 190} L890 {hz - 260} L940 {hz - 230}" stroke="#1E7F4E" stroke-width="8" fill="none"/>'
               f'<rect x="830" y="{hz - 110}" width="40" height="110" fill="#4C5A8E" stroke="{OL}" stroke-width="5"/>'
               f'<path d="M1000 {hz} L1030 {hz - 380} L1060 {hz}" fill="none" stroke="#9AA6B8" stroke-width="10"/>'
               f'<circle cx="1030" cy="{hz - 390}" r="12" fill="#FF6B8B" stroke="{OL}" stroke-width="4"/><circle cx="1030" cy="{hz - 390}" r="34" fill="#FF6B8B" opacity="0.3"/>')
    out.append(f'<rect x="-10" y="{hz - 180}" width="70" height="180" fill="#4C5A8E" stroke="{OL}" stroke-width="5"/>'
               + ''.join(f'<rect x="6" y="{hz - 164 + k * 22}" width="38" height="8" rx="3" fill="#6FF2FF" opacity="0.8"/>' for k in range(7)))
    return ''.join(out)


def tex_circuit(sc):
    """Gold traces running alongside the path, with solder pads."""
    out = []
    r = sc.r
    for side in (-1, 1):
        for lane in range(4):
            off = 30 + lane * 70
            pts = [(sc.side_x(t, side, off), sc.ty(t)) for t in [0.02 + 1.0 * (i / 30) ** 1.15 for i in range(31)]]
            d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
            out.append(f'<path d="{d}" stroke="#E6B84A" stroke-width="5" fill="none" opacity="0.85"/>')
            for t in [0.1 + lane * 0.07, 0.35 + lane * 0.1, 0.7 + lane * 0.05]:
                if t < 1:
                    x, y, s = sc.side_x(t, side, off), sc.ty(t), sc.scale(t)
                    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{9 * s:.1f}" fill="#E6B84A" stroke="{OL}" stroke-width="{2 * s:.1f}"/>'
                               f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.5 * s:.1f}" fill="#1A5E4E"/>')
    return ''.join(out)


def electronic():
    sc = Scene(seed=171, curve=0, path_w=(80, 400))
    sc.sky([(0, '#0F1840'), (0.6, '#22306E'), (1, '#3B4A9E')], stars=90)
    hz = sc.horizon
    # neon grid glow behind skyline
    sc.backdrop(f'<rect y="{hz - 120}" width="{W}" height="140" fill="url(#glowE)"/>')
    sc.defs.append(lin('glowE', [(0, '#6FF2FF', 0), (1, '#6FF2FF', 0.35)]))
    sc.backdrop(device_skyline(hz + 6))
    sc.ground([(0, '#2A8A72'), (0.2, '#1F7A62'), (1, '#196B55')])
    sc.backdrop(tex_circuit(sc))
    sc.path('#26324F', texture=combine(tex_dashes('#6FF2FF'), tex_edge_dots('#E6B84A', 0.04)), border=('#E6B84A', 8))
    sc.place(lambda x, y, s: robot(x, y, s * 1.3), 0.55, 1, 330)
    sc.place(lambda x, y, s: robot(x, y, s * 1.3, '#FFC3D4'), 0.85, -1, 340)
    sc.place(lambda x, y, s: battery(x, y, s * 1.4), 0.3, -1, 340)
    sc.populate([(3, lambda x, y, s: chip(x, y, s * 1.5)), (3, lambda x, y, s: capacitor(x, y, s * 1.5, sc.r.choice(['#4F7FC8', '#6C5CE7', '#2E9E6A']))),
                 (2, lambda x, y, s: resistor(x, y, s * 1.5)),
                 (3, lambda x, y, s: led(x, y, s * 1.5, sc.r.choice(['#FF6B8B', '#6FF2FF', '#B6F07A', '#FFE36A'])))],
                gap=200, start=(330, 380), step=0.06,
                avoid=[(sc.side_x(0.55, 1, 330), sc.ty(0.55), 110, 50), (sc.side_x(0.85, -1, 340), sc.ty(0.85), 140, 60), (sc.side_x(0.3, -1, 340), sc.ty(0.3), 70, 40)])
    for t in (0.15, 0.4, 0.65, 0.92):
        sc.place(lambda x, y, s: led(x, y, s * 1.2, '#6FF2FF'), t, -1, 30)
        sc.place(lambda x, y, s: led(x, y, s * 1.2, '#FF9EC4'), t + 0.03, 1, 30)
    sc.scatter(lambda x, y, s: sparkle(x, y - 40 * s, 0.4 + 0.5 * s, '#6FF2FF', 0.7), 24, 0.05, 1.0, 60, 520)
    sc.haze('#4FB6D8', 320, 0.4)
    sc.bottom_fade(0.3)
    return sc.render()


BUILDERS = {'space': space, 'ocean': ocean, 'electronic': electronic}
