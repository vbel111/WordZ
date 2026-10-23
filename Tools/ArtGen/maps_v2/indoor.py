"""Indoor maps (v2): KITCHEN and THINGS (cosy toy room). Same camera as the outdoor maps: the far
end of the room sits on the horizon line, the floor comes towards the player, a rug runner is the path."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from props import T, crate, hi, shadow  # noqa: E402
from scene import H, OL, VX, W, Scene, combine, lin, rad, shade, sparkle  # noqa: E402
from style import PALETTE as PAL, cloud  # noqa: E402

BACK_L, BACK_R, BACK_TOP = 170, 910, 250
VPY = -335  # vanishing point y (x = 540)


def wall_x(y, side):
    """x of the floor/side-wall junction at height y."""
    edge = BACK_L if side < 0 else BACK_R
    return VX + (edge - VX) * (y - VPY) / (930 - VPY)


def room_shell(sc, wall, wall_side, floor_a, floor_b, ceiling, trim):
    hz = sc.horizon
    out = []
    # ceiling and side walls
    out.append(f'<path d="M0 0 L{W} 0 L{BACK_R} {BACK_TOP} L{BACK_L} {BACK_TOP} Z" fill="{ceiling}"/>')
    for side in (-1, 1):
        ex = 0 if side < 0 else W
        bx = BACK_L if side < 0 else BACK_R
        yb = VPY + (ex - VX) / (bx - VX) * (930 - VPY)
        out.append(f'<path d="M{ex} 0 L{bx} {BACK_TOP} L{bx} {hz} L{ex} {yb:.0f} Z" fill="{wall_side}"/>')
        # skirting board along the floor line
        out.append(f'<path d="M{bx} {hz} L{ex} {yb:.0f} L{ex} {yb - 40:.0f} L{bx} {hz - 16} Z" fill="{trim}" stroke="{OL}" stroke-width="4"/>')
        out.append(f'<line x1="{bx}" y1="{BACK_TOP}" x2="{bx}" y2="{hz}" stroke="{OL}" stroke-width="6"/>')
    out.append(f'<rect x="{BACK_L}" y="{BACK_TOP}" width="{BACK_R - BACK_L}" height="{hz - BACK_TOP}" fill="{wall}"/>')
    out.append(f'<rect x="{BACK_L}" y="{hz - 18}" width="{BACK_R - BACK_L}" height="18" fill="{trim}" stroke="{OL}" stroke-width="4"/>')
    sc.backdrop(''.join(out))
    # checker / plank floor between the side walls
    fl = []
    ybl = VPY + (0 - VX) / (BACK_L - VX) * (930 - VPY)
    fl.append(f'<path d="M{BACK_L} {hz} L{BACK_R} {hz} L{W} {ybl:.0f} L{W} {H} L0 {H} L0 {ybl:.0f} Z" fill="{floor_a}"/>')
    return fl, floor_b


def floor_checker(sc, fl, floor_b, cols=8, rows=26):
    hz = sc.horizon
    xs = [BACK_L + (BACK_R - BACK_L) * k / cols for k in range(-12, cols + 13)]
    ys = [hz + (H - hz) * (j / rows) ** 1.55 for j in range(rows + 1)]

    def X(x0, y):
        return VX + (x0 - VX) * (y - VPY) / (930 - VPY)
    for j in range(rows):
        for i in range(len(xs) - 1):
            if (i + j) % 2:
                continue
            y0, y1 = ys[j], ys[j + 1]
            pts = [(X(xs[i], y0), y0), (X(xs[i + 1], y0), y0), (X(xs[i + 1], y1), y1), (X(xs[i], y1), y1)]
            fl.append(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)} Z" fill="{floor_b}"/>')
    sc.backdrop(''.join(fl))


def floor_planks(sc, fl, line_c, cols=14):
    hz = sc.horizon
    for k in range(-14, cols + 15):
        x0 = BACK_L + (BACK_R - BACK_L) * k / cols
        x1 = VX + (x0 - VX) * (H - VPY) / (930 - VPY)
        fl.append(f'<line x1="{x0:.1f}" y1="{hz}" x2="{x1:.1f}" y2="{H}" stroke="{line_c}" stroke-width="3"/>')
    r = sc.r
    for j in range(40):
        y = hz + (H - hz) * (j / 40) ** 1.5
        for k in range(-14, cols + 15, 2):
            x0 = BACK_L + (BACK_R - BACK_L) * (k + (j % 2)) / cols
            xx = VX + (x0 - VX) * (y - VPY) / (930 - VPY)
            xw = (BACK_R - BACK_L) / cols * (y - VPY) / (930 - VPY)
            fl.append(f'<line x1="{xx:.1f}" y1="{y:.1f}" x2="{xx + xw:.1f}" y2="{y:.1f}" stroke="{line_c}" stroke-width="{1 + 2.5 * (y - hz) / (H - hz):.1f}"/>')
    sc.backdrop(''.join(fl))


def rug(sc, c1, c2, trim):
    """The path is a long runner rug with stripes."""
    def tex(sc_):
        out = []
        n = 18
        for i in range(n):
            ta, tb = (i / n) ** 1.4 * 1.02, ((i + 0.35) / n) ** 1.4 * 1.02
            pa = [(sc_.path_cx(ta) - sc_.path_half(ta) * 0.86, sc_.ty(ta)), (sc_.path_cx(ta) + sc_.path_half(ta) * 0.86, sc_.ty(ta)),
                  (sc_.path_cx(tb) + sc_.path_half(tb) * 0.86, sc_.ty(tb)), (sc_.path_cx(tb) - sc_.path_half(tb) * 0.86, sc_.ty(tb))]
            out.append(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pa)} Z" fill="{c2}"/>')
        for sgn in (-1, 1):
            pts = [(sc_.path_cx(t) + sgn * sc_.path_half(t) * 0.92, sc_.ty(t)) for t in [i / 30 * 1.02 for i in range(31)]]
            out.append(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}" stroke="{trim}" stroke-width="6" fill="none"/>')
        return ''.join(out)
    sc.path(c1, texture=tex)


def place_floor(sc, fn, t, side, off, *a, **kw):
    """Place a prop on the floor `off` units in from the side wall (off grows towards the centre)."""
    y = sc.ty(t)
    s = sc.scale(t) * 1.5
    x = wall_x(y, side) - side * off * s
    sc.add(y, fn(x, y, s, *a, **kw))


# =====================================================================================
# KITCHEN
# =====================================================================================

def window_view(x0, y0, w, h, frame='#FBF1DE'):
    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#winSky)" stroke="{OL}" stroke-width="7"/>',
           f'<circle cx="{x0 + w * 0.72}" cy="{y0 + h * 0.3}" r="{h * 0.12}" fill="#FFF3C4" stroke="#FFD86B" stroke-width="5"/>',
           cloud(x0 + w * 0.3, y0 + h * 0.32, 0.45),
           f'<path d="M{x0} {y0 + h * 0.8} Q{x0 + w * 0.3} {y0 + h * 0.62} {x0 + w * 0.6} {y0 + h * 0.76} Q{x0 + w * 0.8} {y0 + h * 0.66} {x0 + w} {y0 + h * 0.74} L{x0 + w} {y0 + h} L{x0} {y0 + h} Z" fill="#8CCB7A"/>',
           f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="{frame}" stroke-width="16"/>',
           f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="{OL}" stroke-width="5"/>',
           f'<line x1="{x0 + w / 2}" y1="{y0}" x2="{x0 + w / 2}" y2="{y0 + h}" stroke="{frame}" stroke-width="12"/>',
           f'<line x1="{x0}" y1="{y0 + h / 2}" x2="{x0 + w}" y2="{y0 + h / 2}" stroke="{frame}" stroke-width="12"/>']
    return ''.join(out)


def jar(x, y, c):
    return (f'<rect x="{x - 14}" y="{y - 40}" width="28" height="40" rx="6" fill="#E9F6FB" stroke="{OL}" stroke-width="4"/>'
            f'<rect x="{x - 12}" y="{y - 24}" width="24" height="22" rx="4" fill="{c}"/>'
            f'<rect x="{x - 16}" y="{y - 48}" width="32" height="10" rx="3" fill="#C9874A" stroke="{OL}" stroke-width="3"/>')


def kitchen_back(hz):
    out = []
    out.append(window_view(400, 330, 280, 250))
    # upper cabinets
    for x0 in (190, 700):
        out.append(f'<rect x="{x0}" y="300" width="190" height="170" rx="8" fill="#7FC6B8" stroke="{OL}" stroke-width="6"/>'
                   f'<line x1="{x0 + 95}" y1="300" x2="{x0 + 95}" y2="470" stroke="{OL}" stroke-width="4"/>'
                   f'<circle cx="{x0 + 82}" cy="440" r="6" fill="#FFC93C" stroke="{OL}" stroke-width="2"/><circle cx="{x0 + 108}" cy="440" r="6" fill="#FFC93C" stroke="{OL}" stroke-width="2"/>')
    # shelf with jars under left cabinet
    out.append(f'<rect x="200" y="560" width="170" height="12" fill="#C9874A" stroke="{OL}" stroke-width="4"/>')
    for k, c in enumerate(['#E5533D', '#FFC93C', '#6CC24A', '#F08A24']):
        out.append(jar(222 + k * 42, 560, c))
    # hanging pans on the right
    for k, (c, r) in enumerate([('#3A3A44', 34), ('#E5533D', 28), ('#9AA6B8', 24)]):
        cx = 740 + k * 62
        out.append(f'<line x1="{cx}" y1="500" x2="{cx}" y2="{530}" stroke="{OL}" stroke-width="3"/>'
                   f'<rect x="{cx - 4}" y="{530}" width="8" height="40" fill="#7A4520" stroke="{OL}" stroke-width="3"/>'
                   f'<circle cx="{cx}" cy="{570 + r}" r="{r}" fill="{c}" stroke="{OL}" stroke-width="5"/>')
    out.append(f'<rect x="720" y="495" width="170" height="8" rx="4" fill="#9AA6B8" stroke="{OL}" stroke-width="3"/>')
    # counter along the back wall with oven and sink
    out.append(f'<rect x="{BACK_L}" y="{hz - 170}" width="{BACK_R - BACK_L}" height="170" fill="#F3E1C0" stroke="{OL}" stroke-width="6"/>'
               f'<rect x="{BACK_L - 8}" y="{hz - 186}" width="{BACK_R - BACK_L + 16}" height="22" fill="#E7EEF5" stroke="{OL}" stroke-width="6"/>')
    for k in range(6):
        x0 = BACK_L + 12 + k * (BACK_R - BACK_L - 24) / 6
        out.append(f'<rect x="{x0 + 6:.0f}" y="{hz - 150}" width="{(BACK_R - BACK_L - 24) / 6 - 12:.0f}" height="120" rx="6" fill="#FBF1DE" stroke="{OL}" stroke-width="4"/>'
                   f'<rect x="{x0 + (BACK_R - BACK_L - 24) / 12 - 14:.0f}" y="{hz - 136}" width="28" height="6" rx="3" fill="#C9874A"/>')
    # oven
    out.append(f'<rect x="440" y="{hz - 160}" width="200" height="150" rx="8" fill="#9AA6B8" stroke="{OL}" stroke-width="6"/>'
               f'<rect x="460" y="{hz - 120}" width="160" height="90" rx="8" fill="#3A3A44" stroke="{OL}" stroke-width="4"/>'
               f'<rect x="470" y="{hz - 110}" width="60" height="30" rx="5" fill="#FFB26B" opacity="0.6"/>'
               + ''.join(f'<circle cx="{465 + k * 50}" cy="{hz - 142}" r="8" fill="#3A3A44"/>' for k in range(4)))
    # pot on the hob with steam
    out.append(f'<rect x="470" y="{hz - 236}" width="90" height="56" rx="8" fill="#E5533D" stroke="{OL}" stroke-width="5"/>'
               f'<rect x="462" y="{hz - 244}" width="106" height="12" rx="6" fill="#B93A28" stroke="{OL}" stroke-width="4"/>'
               f'<path d="M495 {hz - 256} q-12 -20 0 -40 q12 -20 0 -40 M530 {hz - 256} q-12 -20 0 -40" stroke="#FFFFFF" stroke-width="7" fill="none" opacity="0.7" stroke-linecap="round"/>')
    # sink + plant
    out.append(f'<rect x="250" y="{hz - 194}" width="120" height="14" rx="5" fill="#BFC9D6" stroke="{OL}" stroke-width="4"/>'
               f'<path d="M300 {hz - 194} L300 {hz - 240} Q300 {hz - 256} 320 {hz - 256} L336 {hz - 256}" stroke="#9AA6B8" stroke-width="9" fill="none"/>'
               f'<rect x="770" y="{hz - 236}" width="46" height="50" rx="6" fill="#E99A12" stroke="{OL}" stroke-width="4"/>'
               f'<path d="M793 {hz - 236} q-30 -30 -20 -60 M793 {hz - 236} q0 -40 10 -66 M793 {hz - 236} q30 -26 30 -54" stroke="#3E8E2F" stroke-width="10" fill="none" stroke-linecap="round"/>')
    return ''.join(out)


def fridge(x, y, s):
    b = (shadow(70, 14) + '<rect x="-60" y="-300" width="120" height="300" rx="16" fill="#E7EEF5"/>'
         '<line x1="-60" y1="-190" x2="60" y2="-190" stroke-width="5"/><rect x="36" y="-280" width="8" height="70" rx="4" fill="#9AA6B8"/>'
         '<rect x="36" y="-170" width="8" height="90" rx="4" fill="#9AA6B8"/>'
         '<circle cx="-30" cy="-240" r="10" fill="#E5533D"/><rect x="-20" y="-150" width="30" height="36" fill="#FFF3C4" transform="rotate(-6)"/>'
         + hi(-40, -260, 8, 40, 0.5))
    return T(x, y, s, b)


def table_chairs(x, y, s):
    b = shadow(130, 20)
    b += '<rect x="-120" y="-70" width="16" height="70" fill="#9A5B27"/><rect x="104" y="-70" width="16" height="70" fill="#9A5B27"/>'
    b += '<rect x="-140" y="-92" width="280" height="26" rx="8" fill="#C9874A"/><rect x="-136" y="-90" width="272" height="8" fill="#E9C48A" stroke="none"/>'
    b += ('<path d="M-90 -92 L-92 -102 L-30 -102 L-32 -92 Z" fill="#FFFFFF"/><circle cx="-60" cy="-110" r="18" fill="#FFFFFF"/><circle cx="-60" cy="-112" r="12" fill="#FFC93C" stroke="none"/>'
          '<path d="M30 -92 L34 -140 L70 -140 L74 -92 Z" fill="#E9F6FB"/><path d="M40 -140 q4 -24 14 -30 M60 -140 q2 -26 16 -32" stroke="#6CC24A" stroke-width="6" fill="none"/>'
          '<circle cx="54" cy="-172" r="10" fill="#FF7FA8"/><circle cx="76" cy="-178" r="9" fill="#FFD23F"/>')
    for cx in (-170, 170):
        b += (f'<rect x="{cx - 34}" y="-60" width="68" height="14" rx="5" fill="#E5533D"/><rect x="{cx - 30}" y="-46" width="10" height="46" fill="#9A5B27"/>'
              f'<rect x="{cx + 20}" y="-46" width="10" height="46" fill="#9A5B27"/><rect x="{cx - (34 if cx < 0 else -24)}" y="-150" width="10" height="94" fill="#9A5B27"/>')
    return T(x, y, s, b)


def big_pot(x, y, s, c='#4FA3E3'):
    b = (shadow(60) + f'<path d="M-56 -100 L56 -100 L48 -6 Q46 0 40 0 L-40 0 Q-46 0 -48 -6 Z" fill="{c}"/>'
         f'<rect x="-64" y="-112" width="128" height="18" rx="8" fill="{shade(c, -0.2)}"/>'
         '<path d="M-64 -84 q-22 0 -22 18 M64 -84 q22 0 22 18" fill="none" stroke-width="8"/>'
         '<circle cx="-20" cy="-116" r="12" fill="#E5533D"/><circle cx="10" cy="-120" r="11" fill="#FFC93C"/><path d="M26 -120 q10 -20 20 -24" stroke="#6CC24A" stroke-width="8" fill="none"/>'
         + hi(-34, -70, 8, 20, 0.35))
    return T(x, y, s, b)


def stool(x, y, s, c='#FFC93C'):
    b = (shadow(40) + '<path d="M-30 0 L-22 -80 M30 0 L22 -80 M0 0 L0 -80" stroke-width="10"/><path d="M-30 0 L-22 -80 M30 0 L22 -80" stroke="#9A5B27" stroke-width="5"/>'
         f'<ellipse cx="0" cy="-84" rx="40" ry="12" fill="{c}"/>')
    return T(x, y, s, b)


def potted_plant(x, y, s, c='#E99A12'):
    b = (shadow(40) + f'<path d="M-34 -60 L34 -60 L26 0 L-26 0 Z" fill="{c}"/><rect x="-38" y="-70" width="76" height="14" rx="5" fill="{shade(c, -0.15)}"/>')
    for a, l in [(-60, 90), (-30, 120), (0, 130), (30, 110), (60, 86)]:
        r = math.radians(a - 90)
        ex, ey = math.cos(r) * l, -70 + math.sin(r) * l
        b += f'<path d="M0 -70 Q{ex * 0.2:.0f} {(-70 + ey) / 2:.0f} {ex:.0f} {ey:.0f} Q{ex * 0.7:.0f} {(-70 + ey) / 2 + 10:.0f} 0 -70 Z" fill="#5DB03E"/>'
    return T(x, y, s, b)


def kitchen():
    sc = Scene(seed=181, curve=0, path_w=(110, 380))
    sc.defs.append(lin('winSky', [(0, '#7CC4F0', 1), (1, '#CFEBFA', 1)]))
    fl, fb = room_shell(sc, '#FFF3DC', '#F6E3C2', '#F4EBDD', '#E2CDB0', '#FBF1DE', '#C9874A')
    floor_checker(sc, fl, '#D8C0A0', cols=8, rows=26)
    sc.backdrop(kitchen_back(sc.horizon))
    # wall tiles on the side walls (a few horizontal lines in perspective)
    sw = []
    for side in (-1, 1):
        bx = BACK_L if side < 0 else BACK_R
        ex = 0 if side < 0 else W
        for k in range(1, 8):
            yb = BACK_TOP + (sc.horizon - BACK_TOP) * k / 8
            ye = (yb - VPY) * (ex - VX) / (bx - VX) + VPY
            sw.append(f'<line x1="{bx}" y1="{yb:.0f}" x2="{ex}" y2="{ye:.0f}" stroke="#E7D2AE" stroke-width="3"/>')
    sc.backdrop(''.join(sw))
    rug(sc, '#E5533D', '#F3A06E', '#FFFFFF')
    place_floor(sc, fridge, 0.05, -1, 70)
    place_floor(sc, lambda x, y, s: fridge(x, y, s), 0.07, 1, 70)
    place_floor(sc, table_chairs, 0.36, -1, 230)
    place_floor(sc, big_pot, 0.55, 1, 140)
    place_floor(sc, stool, 0.24, 1, 160, '#4FA3E3')
    place_floor(sc, stool, 0.68, -1, 120, '#FFC93C')
    place_floor(sc, potted_plant, 0.2, -1, 60)
    place_floor(sc, potted_plant, 0.82, 1, 80, '#4FA3E3')
    place_floor(sc, crate, 0.46, -1, 80, fruit='#E5533D')
    place_floor(sc, crate, 0.75, 1, 210, fruit='#6CC24A')
    place_floor(sc, big_pot, 0.95, -1, 150, '#E5533D')
    place_floor(sc, crate, 0.98, 1, 110, fruit='#FFC93C')
    sc.bottom_fade(0.2)
    return sc.render()


# =====================================================================================
# THINGS (cosy toy room)
# =====================================================================================

def round_window(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#nightSky)" stroke="{OL}" stroke-width="7"/>'
            f'<circle cx="{cx + r * 0.35}" cy="{cy - r * 0.3}" r="{r * 0.18}" fill="#FFF3C4"/>'
            + ''.join(f'<circle cx="{cx + dx * r}" cy="{cy + dy * r}" r="3" fill="#FFFFFF"/>' for dx, dy in [(-0.5, -0.2), (-0.2, 0.3), (0.3, 0.4), (-0.4, 0.5), (0.1, -0.5)]) +
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#C9874A" stroke-width="18"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{OL}" stroke-width="5"/>'
            f'<line x1="{cx - r}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="#C9874A" stroke-width="10"/><line x1="{cx}" y1="{cy - r}" x2="{cx}" y2="{cy + r}" stroke="#C9874A" stroke-width="10"/>')


def bookshelf(x0, y0, w, h):
    out = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#A8642E" stroke="{OL}" stroke-width="6"/>']
    rows = 3
    for r_ in range(rows):
        sy = y0 + 14 + r_ * (h - 20) / rows
        sh = (h - 20) / rows - 14
        out.append(f'<rect x="{x0 + 12}" y="{sy}" width="{w - 24}" height="{sh}" fill="#7A4520"/>')
        bx = x0 + 16
        k = 0
        while bx < x0 + w - 30:
            bw = 14 + (k * 7) % 12
            bh = sh * (0.7 + ((k * 13) % 5) / 20)
            c = ['#E5533D', '#4FA3E3', '#FFC93C', '#6CC24A', '#C58BF2', '#F08A24'][k % 6]
            out.append(f'<rect x="{bx}" y="{sy + sh - bh}" width="{bw}" height="{bh}" fill="{c}" stroke="{OL}" stroke-width="3"/>')
            bx += bw + 3
            k += 1
    return ''.join(out)


def wall_clock(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FBF1DE" stroke="{OL}" stroke-width="6"/><circle cx="{cx}" cy="{cy}" r="{r - 10}" fill="none" stroke="#E5533D" stroke-width="5"/>'
            f'<path d="M{cx} {cy} L{cx} {cy - r * 0.6} M{cx} {cy} L{cx + r * 0.4} {cy + r * 0.1}" stroke="{OL}" stroke-width="6" stroke-linecap="round"/>')


def picture(x0, y0, w, h):
    return (f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#BFE4F8" stroke="#C9874A" stroke-width="12"/>'
            f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="{OL}" stroke-width="4"/>'
            f'<path d="M{x0 + 6} {y0 + h - 6} L{x0 + w * 0.35} {y0 + h * 0.45} L{x0 + w * 0.55} {y0 + h * 0.7} L{x0 + w * 0.75} {y0 + h * 0.35} L{x0 + w - 6} {y0 + h - 6} Z" fill="#6CC24A"/>'
            f'<circle cx="{x0 + w * 0.75}" cy="{y0 + h * 0.25}" r="{h * 0.1}" fill="#FFD86B"/>')


def blocks(x, y, s):
    b = shadow(70)
    for (bx, by, c, ch) in [(-50, -50, '#E5533D', 'A'), (0, -50, '#4FA3E3', 'B'), (-25, -100, '#FFC93C', 'C'), (50, -50, '#6CC24A', '')]:
        b += (f'<rect x="{bx - 24}" y="{by}" width="48" height="48" rx="6" fill="{c}"/><rect x="{bx - 16}" y="{by + 8}" width="32" height="32" rx="4" fill="#FFFFFF" opacity="0.35" stroke="none"/>')
    return T(x, y, s, b)


def teddy(x, y, s, c='#C98A4E'):
    l = shade(c, 0.3)
    b = (shadow(50) + f'<ellipse cx="-24" cy="-14" rx="20" ry="14" fill="{c}"/><ellipse cx="24" cy="-14" rx="20" ry="14" fill="{c}"/>'
         f'<ellipse cx="0" cy="-60" rx="42" ry="46" fill="{c}"/><ellipse cx="0" cy="-54" rx="24" ry="28" fill="{l}" stroke="none"/>'
         f'<circle cx="-36" cy="-150" r="16" fill="{c}"/><circle cx="36" cy="-150" r="16" fill="{c}"/>'
         f'<circle cx="0" cy="-124" r="40" fill="{c}"/><ellipse cx="0" cy="-112" rx="16" ry="12" fill="{l}"/>'
         '<circle cx="0" cy="-118" r="5" fill="#4A2410" stroke="none"/><circle cx="-14" cy="-134" r="4.5" fill="#4A2410" stroke="none"/><circle cx="14" cy="-134" r="4.5" fill="#4A2410" stroke="none"/>'
         '<path d="M-16 -88 L16 -88 L0 -78 Z" fill="#E5533D"/><path d="M-30 -98 L-6 -84 L-30 -70 Z M30 -98 L6 -84 L30 -70 Z" fill="#E5533D"/>'
         f'<ellipse cx="-44" cy="-70" rx="14" ry="22" fill="{c}" transform="rotate(30 -44 -70)"/><ellipse cx="44" cy="-70" rx="14" ry="22" fill="{c}" transform="rotate(-30 44 -70)"/>')
    return T(x, y, s, b)


def toy_ball(x, y, s):
    b = (shadow(36) + '<circle cx="0" cy="-36" r="36" fill="#FFFFFF"/>'
         '<path d="M-36 -36 A36 36 0 0 1 0 -72 L0 -36 Z" fill="#E5533D" stroke="none"/><path d="M0 0 A36 36 0 0 1 -36 -36 L0 -36 Z" fill="#4FA3E3" stroke="none"/>'
         '<path d="M36 -36 A36 36 0 0 1 0 0 L0 -36 Z" fill="#FFC93C" stroke="none"/><circle cx="0" cy="-36" r="36" fill="none"/>' + hi(-14, -54, 9, 6, 0.6))
    return T(x, y, s, b)


def floor_lamp(x, y, s):
    b = (shadow(40) + '<ellipse cx="0" cy="-6" rx="30" ry="8" fill="#3A3A44"/><rect x="-4" y="-220" width="8" height="214" fill="#3A3A44"/>'
         '<path d="M-50 -210 L50 -210 L30 -270 L-30 -270 Z" fill="#FFC93C"/><ellipse cx="0" cy="-200" rx="70" ry="40" fill="#FFE9A6" opacity="0.3" stroke="none"/>')
    return T(x, y, s, b)


def toy_chest(x, y, s):
    b = (shadow(80) + '<rect x="-80" y="-80" width="160" height="80" rx="8" fill="#4FA3E3"/>'
         '<path d="M-84 -80 Q0 -120 84 -80 Z" fill="#3A7BD5"/><rect x="-80" y="-56" width="160" height="10" fill="#FFC93C" stroke="none"/>'
         '<rect x="-12" y="-62" width="24" height="22" rx="4" fill="#FFC93C"/>'
         '<circle cx="-50" cy="-100" r="16" fill="#E5533D"/><rect x="20" y="-118" width="26" height="26" rx="4" fill="#6CC24A"/>')
    return T(x, y, s, b)


def rocking_horse(x, y, s):
    b = (shadow(80) + '<path d="M-90 -10 Q0 30 90 -10" fill="none" stroke-width="14"/><path d="M-90 -10 Q0 30 90 -10" fill="none" stroke="#C9874A" stroke-width="8"/>'
         '<path d="M-50 4 L-40 -60 M50 4 L40 -60" stroke-width="10"/><path d="M-50 4 L-40 -60 M50 4 L40 -60" stroke="#E9C48A" stroke-width="5"/>'
         '<rect x="-60" y="-100" width="110" height="46" rx="20" fill="#FBF1DE"/><path d="M30 -96 L60 -160 L100 -150 L96 -128 L66 -122 L50 -90 Z" fill="#FBF1DE"/>'
         '<path d="M46 -140 Q30 -150 30 -110 L44 -104 Z" fill="#E5533D"/><circle cx="76" cy="-146" r="4" fill="#4A2410" stroke="none"/>'
         '<rect x="-30" y="-108" width="44" height="14" rx="5" fill="#E5533D"/><path d="M-60 -86 q-30 6 -36 34" stroke="#E5533D" stroke-width="10" fill="none"/>')
    return T(x, y, s, b)


def toy_train(x, y, s):
    b = shadow(110)
    b += '<rect x="-20" y="-80" width="100" height="70" rx="8" fill="#E5533D"/><rect x="40" y="-110" width="50" height="40" rx="6" fill="#E5533D"/>'
    b += '<rect x="50" y="-102" width="30" height="24" rx="4" fill="#9FD3F2"/><rect x="-10" y="-110" width="20" height="34" fill="#3A3A44"/>'
    b += '<rect x="-120" y="-60" width="90" height="50" rx="6" fill="#4FA3E3"/><rect x="-110" y="-74" width="70" height="16" rx="4" fill="#FFC93C"/>'
    for cx in (-100, -50, 0, 60):
        b += f'<circle cx="{cx}" cy="-8" r="16" fill="#3A3A44"/><circle cx="{cx}" cy="-8" r="6" fill="#FFC93C"/>'
    return T(x, y, s, b)


def books_stack(x, y, s):
    b = shadow(46)
    for k, (c, w) in enumerate([('#6CC24A', 96), ('#C58BF2', 84), ('#E5533D', 92)]):
        b += f'<rect x="{-w / 2 + (k % 2) * 8}" y="{-26 - k * 26}" width="{w}" height="26" rx="4" fill="{c}"/><rect x="{-w / 2 + (k % 2) * 8 + 6}" y="{-20 - k * 26}" width="{w - 12}" height="5" fill="#FFFFFF" opacity="0.6" stroke="none"/>'
    return T(x, y, s, b)


def things():
    sc = Scene(seed=191, curve=0, path_w=(110, 380))
    sc.defs.append(lin('nightSky', [(0, '#3B3F99', 1), (1, '#7C5BB5', 1)]))
    fl, fb = room_shell(sc, '#F7E3C7', '#EED3AE', '#D9A266', '#C98E52', '#F7EBD8', '#A8642E')
    floor_planks(sc, fl, '#B87A42')
    hz = sc.horizon
    # wallpaper dots
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#EBCBA0"/>' for x in range(200, 900, 60) for y in range(290, hz - 40, 60))
    sc.backdrop(dots)
    sc.backdrop(round_window(VX, 470, 150) + bookshelf(200, 560, 200, hz - 580) + bookshelf(680, 560, 200, hz - 580)
                + wall_clock(290, 380, 60) + picture(720, 320, 140, 110))
    # bunting across the room
    from props import bunting
    sc.backdrop(bunting(BACK_L, 300, BACK_R, 300, 1.2, ('#E5533D', '#FFC93C', '#4FA3E3', '#6CC24A', '#C58BF2')))
    rug(sc, '#4FA3E3', '#7FC1EE', '#FFFFFF')
    place_floor(sc, floor_lamp, 0.06, -1, 60)
    place_floor(sc, rocking_horse, 0.2, 1, 150)
    place_floor(sc, toy_chest, 0.3, -1, 150)
    place_floor(sc, teddy, 0.5, 1, 140)
    place_floor(sc, blocks, 0.62, -1, 170)
    place_floor(sc, toy_train, 0.8, 1, 240)
    place_floor(sc, toy_ball, 0.42, 1, 80)
    place_floor(sc, books_stack, 0.74, -1, 80)
    place_floor(sc, potted_plant, 0.12, 1, 60, '#E5533D')
    place_floor(sc, teddy, 0.96, -1, 170, '#E9B07A')
    place_floor(sc, toy_ball, 0.98, 1, 120)
    place_floor(sc, blocks, 0.36, -1, 50)
    sc.scatter(lambda x, y, s: sparkle(x, y - 200 * s, 0.4 + 0.4 * s, '#FFE9A6', 0.8), 14, 0.05, 1.0, 60, 400)
    sc.bottom_fade(0.22)
    return sc.render()


BUILDERS = {'kitchen': kitchen, 'things': things}
