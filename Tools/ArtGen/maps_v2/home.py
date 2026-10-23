"""Home screen art (v2): background illustration + menu icons in the same style as the maps.
python3 home.py out_dir  -> home_bg.svg and icon_*.svg (render with render.js)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from props import T, apple_tree, balloon, flagpole, hi, house, mushroom, pine, shadow, windmill  # noqa: E402
from scene import H, OL, VX, W, Scene, combine, hills, lin, mountains, rad, shade, sparkle, tex_edge_dots, tex_stones  # noqa: E402
from style import bird, bush, cloud, flower, grass_tuft, round_tree  # noqa: E402

FONT = "Baloo, 'Arial Black', Arial, sans-serif"


def hex_tile(x, y, s, letter, face='#FBF1DE', ink='#7A4520', tilt=0):
    """Big wooden-cream hex letter tile standing in the meadow (flat-top, like the game board)."""
    pts = ' '.join(f'{math.cos(math.radians(a)) * 60:.1f},{-62 + math.sin(math.radians(a)) * 52:.1f}' for a in range(0, 360, 60))
    pts2 = ' '.join(f'{math.cos(math.radians(a)) * 60:.1f},{-48 + math.sin(math.radians(a)) * 52:.1f}' for a in range(0, 360, 60))
    b = (shadow(64, 12, 0.25) + f'<polygon points="{pts2}" fill="{shade(face, -0.28)}"/>'
         f'<polygon points="{pts}" fill="{face}"/>'
         f'<polygon points="{pts}" fill="#FFFFFF" opacity="0.25" stroke="none" transform="translate(-6,-6) scale(0.8) translate(0,-14)"/>'
         f'<text x="0" y="-38" font-family="{FONT}" font-weight="800" font-size="68" text-anchor="middle" fill="{ink}" stroke="none">{letter}</text>')
    return T(x, y, s, f'<g transform="rotate({tilt})">{b}</g>')


def letter_balloon(x, y, s, c, letter):
    b = (f'<path d="M0 -40 q-6 40 6 90" stroke="{OL}" stroke-width="3" fill="none"/>'
         f'<ellipse cx="0" cy="-100" rx="52" ry="62" fill="{c}"/><path d="M-8 -40 L8 -40 L4 -30 L-4 -30 Z" fill="{shade(c, -0.2)}"/>'
         + hi(-20, -128, 12, 18, 0.45) +
         f'<text x="0" y="-78" font-family="{FONT}" font-weight="800" font-size="62" text-anchor="middle" fill="#FFFFFF" stroke="{OL}" stroke-width="3">{letter}</text>')
    return T(x, y, s, b)


def word_tower(cx, base):
    """Storybook clock tower on the hill with a Z flag - the 'capital' of Word Z."""
    out = [f'<rect x="{cx - 70}" y="{base - 330}" width="140" height="330" fill="#F2D6AE" stroke="{OL}" stroke-width="7"/>',
           f'<rect x="{cx + 30}" y="{base - 330}" width="40" height="330" fill="#E2BE8E" stroke="none"/>',
           f'<rect x="{cx - 70}" y="{base - 330}" width="140" height="330" fill="none" stroke="{OL}" stroke-width="7"/>',
           f'<path d="M{cx - 92} {base - 330} L{cx} {base - 470} L{cx + 92} {base - 330} Z" fill="#7C4DCC" stroke="{OL}" stroke-width="7" stroke-linejoin="round"/>',
           f'<path d="M{cx} {base - 470} L{cx + 92} {base - 330} L{cx + 40} {base - 330} Z" fill="#5E35A8"/>',
           f'<circle cx="{cx}" cy="{base - 250}" r="44" fill="#FFF3C4" stroke="{OL}" stroke-width="6"/>',
           f'<path d="M{cx} {base - 250} l0 -30 M{cx} {base - 250} l20 10" stroke="{OL}" stroke-width="6" stroke-linecap="round"/>',
           f'<path d="M{cx - 34} {base} L{cx - 34} {base - 80} Q{cx} {base - 112} {cx + 34} {base - 80} L{cx + 34} {base} Z" fill="#9A5B27" stroke="{OL}" stroke-width="6"/>',
           f'<rect x="{cx - 46}" y="{base - 170}" width="30" height="40" rx="6" fill="#FFD86B" stroke="{OL}" stroke-width="4"/>',
           f'<rect x="{cx + 16}" y="{base - 170}" width="30" height="40" rx="6" fill="#9FD3F2" stroke="{OL}" stroke-width="4"/>',
           f'<line x1="{cx}" y1="{base - 470}" x2="{cx}" y2="{base - 560}" stroke="{OL}" stroke-width="6"/>',
           f'<path d="M{cx + 3} {base - 560} L{cx + 86} {base - 540} L{cx + 3} {base - 512} Z" fill="#FFC93C" stroke="{OL}" stroke-width="5" stroke-linejoin="round"/>',
           f'<text x="{cx + 34}" y="{base - 525}" font-family="{FONT}" font-weight="800" font-size="34" text-anchor="middle" fill="#7A4520">Z</text>']
    return ''.join(out)


def home_bg():
    sc = Scene(seed=777, horizon=1250, curve=90, curve_freq=1.3, path_w=(60, 420))
    sc.sky([(0, '#6CB9EC'), (0.5, '#B9E2F8'), (0.85, '#FFEFC6'), (1, '#FFE3A8')], sun=(860, 470, 80, '#FFE39A'),
           clouds=[(160, 330, 1.0, 1), (930, 260, 0.75, 0.95), (120, 760, 0.7, 0.9), (980, 820, 0.6, 0.9)],
           birds=[(300, 560, 1.1), (338, 540, 0.8), (720, 690, 0.9)])
    hz = sc.horizon
    sc.backdrop(mountains(hz - 80, [(120, 300, 260), (980, 340, 280), (700, 220, 200)], '#A9C8E6', shade_c='#95B6DA'))
    sc.backdrop(hills(hz, [('#BCDFA6', 150), ('#A6D58C', 70)], seed=21, amp=(50, 90)))
    # village on the hill around the tower
    vill = ''
    for x, wall, roof, s in [(660, '#FBE6C4', '#E5533D', 0.55), (720, '#FCE1CF', '#3A7BD5', 0.42), (960, '#FFFFFF', '#2E9E4A', 0.5),
                             (1030, '#F6D9A8', '#E99A12', 0.42), (400, '#E9F2FB', '#9B59B6', 0.4), (300, '#FBE6C4', '#E5533D', 0.45)]:
        vill += house(x, hz - 60, s, wall, roof, flip=x > VX)
    sc.backdrop(vill + word_tower(840, hz - 50))
    sc.backdrop(windmill(170, hz - 70, 0.6) + round_tree(80, hz - 60, 0.5) + round_tree(560, hz - 50, 0.4))
    for x, y, s, c, l in [(110, 960, 0.8, '#E5533D', 'W'), (270, 850, 0.6, '#4FA3E3', 'O'), (620, 900, 0.65, '#6CC24A', 'R'), (1000, 800, 0.55, '#C58BF2', 'D')]:
        sc.backdrop(letter_balloon(x, y, s, c, l))
    sc.ground([(0, '#CDE8AC'), (0.2, '#A6D77A'), (1, '#78C452')])
    sc.path('#EBD3A2', texture=combine(tex_stones('#D6B47A', 150), tex_edge_dots('#FBF1DE', 0.05)), border=('#D9C08C', 10))
    letters = 'WORDZPLAYFUN'
    tiles = [(-1, 0.12, 120, 'A', -8), (1, 0.18, 140, 'Z', 6), (-1, 0.36, 200, 'W', 10), (1, 0.42, 160, 'O', -10),
             (-1, 0.6, 140, 'R', -6), (1, 0.68, 230, 'D', 8), (-1, 0.86, 260, 'S', 4), (1, 0.92, 120, 'E', -8)]
    for side, t, off, l, tilt in tiles:
        sc.place(lambda x, y, s, l=l, tilt=tilt: hex_tile(x, y, s, l, tilt=tilt), t, side, off)
    sc.populate([(3, lambda x, y, s: round_tree(x, y, s, sc.r.choice(['#6CC24A', '#5DB03E', '#7CCB4E']))), (2, bush), (1, pine),
                 (1, mushroom), (1, apple_tree)], gap=170, start=(330, 400), step=0.065)
    sc.scatter(lambda x, y, s: grass_tuft(x, y, 0.5 + s, '#4E9F36'), 90, 0.05, 1.02, 30, 520)
    sc.scatter(lambda x, y, s: flower(x, y, 0.4 + 0.9 * s, sc.r.choice(['#FF7FA8', '#FFFFFF', '#FFD23F', '#C58BF2'])), 70, 0.08, 1.02, 30, 520)
    sc.haze('#FFF4DC', 360, 0.5)
    sc.bottom_fade(0.15)
    return sc.render()


# =====================================================================================
# icons (256 x 256, transparent)
# =====================================================================================

def icon_svg(body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><defs>{defs}</defs>'
            f'<g stroke="{OL}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round">{body}</g></svg>')


def icon_calendar():
    body = ('<rect x="40" y="58" width="176" height="166" rx="22" fill="#FFFFFF"/>'
            '<path d="M40 80 Q40 58 62 58 L194 58 Q216 58 216 80 L216 110 L40 110 Z" fill="#E5533D"/>'
            '<rect x="48" y="66" width="120" height="10" rx="5" fill="#FF8A73" stroke="none"/>'
            '<rect x="78" y="34" width="18" height="46" rx="9" fill="#9AA6B8"/><rect x="160" y="34" width="18" height="46" rx="9" fill="#9AA6B8"/>'
            f'<text x="128" y="200" font-family="{FONT}" font-weight="800" font-size="92" text-anchor="middle" fill="#4A2410" stroke="none">7</text>'
            # gift in the corner
            '<rect x="158" y="160" width="78" height="66" rx="8" fill="#6CC24A"/><rect x="152" y="146" width="90" height="24" rx="6" fill="#7CD85A"/>'
            '<rect x="190" y="146" width="14" height="80" fill="#FFC93C"/>'
            '<path d="M197 146 Q170 116 162 132 Q160 146 197 146 Q224 116 232 132 Q234 146 197 146 Z" fill="#FFC93C"/>')
    return icon_svg(body)


def icon_trophy():
    body = ('<path d="M76 54 Q30 54 34 94 Q38 134 92 140" fill="none" stroke-width="16"/><path d="M76 54 Q30 54 34 94 Q38 134 92 140" fill="none" stroke="#FFC93C" stroke-width="7"/>'
            '<path d="M180 54 Q226 54 222 94 Q218 134 164 140" fill="none" stroke-width="16"/><path d="M180 54 Q226 54 222 94 Q218 134 164 140" fill="none" stroke="#FFC93C" stroke-width="7"/>'
            '<path d="M66 40 L190 40 L184 112 Q176 168 128 172 Q80 168 72 112 Z" fill="url(#gold)"/>'
            '<path d="M150 46 L184 46 L178 112 Q172 150 140 164 Q164 130 150 46 Z" fill="#E99A12" stroke="none"/>'
            '<rect x="112" y="170" width="32" height="30" fill="#E99A12"/>'
            '<rect x="70" y="196" width="116" height="34" rx="8" fill="#9A5B27"/><rect x="84" y="204" width="88" height="10" rx="5" fill="#C9874A" stroke="none"/>'
            '<path d="M128 72 l10 22 l24 2 l-18 15 l6 24 l-22 -13 l-22 13 l6 -24 l-18 -15 l24 -2 Z" fill="#FFF3C4" stroke-width="5"/>'
            '<path d="M84 56 L92 104" stroke="#FFFFFF" stroke-width="9" opacity="0.7"/>')
    return icon_svg(body, lin('gold', [(0, '#FFE45A', 1), (1, '#F5A511', 1)]))


def icon_shop():
    body = ('<rect x="46" y="110" width="164" height="114" rx="10" fill="#F6D9A8"/>'
            '<rect x="64" y="140" width="64" height="84" rx="6" fill="#9A5B27"/><circle cx="116" cy="184" r="5" fill="#FFC93C"/>'
            '<rect x="142" y="140" width="52" height="46" rx="6" fill="#9FD3F2"/><path d="M150 176 L168 150" stroke="#FFFFFF" stroke-width="5" opacity="0.8"/>')
    for k in range(5):
        x = 34 + k * 37.6
        c = '#E5533D' if k % 2 == 0 else '#FFFFFF'
        body += f'<path d="M{x:.1f} 70 h37.6 v40 q-18.8 18 -37.6 0 Z" fill="{c}"/>'
    body += ('<path d="M30 70 L58 34 L198 34 L226 70 Z" fill="#B93A28"/>'
             '<circle cx="200" cy="196" r="34" fill="url(#gold)"/><circle cx="200" cy="196" r="22" fill="none" stroke="#E99A12" stroke-width="6"/>'
             f'<text x="200" y="210" font-family="{FONT}" font-weight="800" font-size="38" text-anchor="middle" fill="#E99A12" stroke="none">$</text>')
    return icon_svg(body, lin('gold', [(0, '#FFE45A', 1), (1, '#F5A511', 1)]))


def icon_quests():
    body = ('<path d="M60 40 L188 40 Q206 40 206 58 L206 206 L74 206 Q56 206 56 188 L56 58" fill="#FBEBCB"/>'
            '<path d="M48 40 Q30 40 30 58 Q30 76 48 76 L66 76 L66 58 Q66 40 48 40 Z" fill="#E9C48A"/>'
            '<path d="M206 206 Q226 206 226 188 Q226 170 206 170 L190 170 L190 188 Q190 206 206 206 Z" fill="#E9C48A"/>')
    for i, done in enumerate([True, True, False]):
        y = 82 + i * 40
        body += f'<rect x="80" y="{y}" width="26" height="26" rx="6" fill="#FFFFFF" stroke-width="5"/>'
        if done:
            body += f'<path d="M84 {y + 13} l8 8 l14 -18" fill="none" stroke="#3E9A2E" stroke-width="7"/>'
        body += f'<rect x="118" y="{y + 8}" width="{66 - i * 10}" height="10" rx="5" fill="#C9A06A" stroke="none"/>'
    body += ('<circle cx="176" cy="184" r="30" fill="#E5533D"/><path d="M162 208 l-6 30 l20 -12 l20 12 l-6 -30" fill="#E5533D"/>'
             '<path d="M176 168 l5 10 l11 1 l-8 7 l3 11 l-11 -6 l-11 6 l3 -11 l-8 -7 l11 -1 Z" fill="#FFC93C" stroke-width="3"/>')
    return icon_svg(body)


def icon_daily_puzzle():
    pts = ' '.join(f'{128 + math.cos(math.radians(a)) * 100:.1f},{136 + math.sin(math.radians(a)) * 88:.1f}' for a in range(0, 360, 60))
    pts2 = ' '.join(f'{128 + math.cos(math.radians(a)) * 100:.1f},{152 + math.sin(math.radians(a)) * 88:.1f}' for a in range(0, 360, 60))
    body = (f'<polygon points="{pts2}" fill="#D98A00"/><polygon points="{pts}" fill="#FFC93C"/>'
            f'<polygon points="{pts}" fill="#FFFFFF" opacity="0.18" stroke="none" transform="translate(20,10) scale(0.8)"/>'
            f'<text x="128" y="172" font-family="{FONT}" font-weight="800" font-size="104" text-anchor="middle" fill="#FFFFFF" stroke="{OL}" stroke-width="5">?</text>'
            '<path d="M204 40 Q208 58 226 62 Q208 66 204 84 Q200 66 182 62 Q200 58 204 40 Z" fill="#FFE36A" stroke-width="4"/>'
            '<path d="M44 196 Q47 208 58 210 Q47 213 44 224 Q41 213 30 210 Q41 208 44 196 Z" fill="#FFE36A" stroke-width="3"/>')
    return icon_svg(body)


ICONS = {'calendar': icon_calendar, 'trophy': icon_trophy, 'shop': icon_shop, 'quests': icon_quests, 'daily_puzzle': icon_daily_puzzle}


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'home_bg.svg'), 'w').write(home_bg())
    for n, f in ICONS.items():
        open(os.path.join(out, f'icon_{n}.svg'), 'w').write(f())
    print('ok')
