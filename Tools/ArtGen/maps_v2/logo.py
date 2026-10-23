"""Word Z logo + app icon in the 'sky & candy' style. python3 logo.py out_dir -> logo.svg, app_icon.svg"""
import math
import os
import sys

INK = '#3A2F6B'
FONT = "Baloo, 'Arial Black', Arial, sans-serif"


def hexpts(cx, cy, r, ry=None, rot=0):
    ry = ry or r
    return ' '.join(f'{cx + math.cos(math.radians(a + rot)) * r:.1f},{cy + math.sin(math.radians(a + rot)) * ry:.1f}' for a in range(0, 360, 60))


def sparkle(x, y, s, c='#FFFFFF'):
    return (f'<path d="M{x} {y - 22 * s} Q{x + 3 * s} {y - 3 * s} {x + 22 * s} {y} Q{x + 3 * s} {y + 3 * s} {x} {y + 22 * s} '
            f'Q{x - 3 * s} {y + 3 * s} {x - 22 * s} {y} Q{x - 3 * s} {y - 3 * s} {x} {y - 22 * s} Z" fill="{c}"/>')


def tile(x, y, letter, rot, size=120):
    h = size / 2
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="{-h}" y="{-h + 12}" width="{size}" height="{size}" rx="24" fill="#B7A9E8" stroke="{INK}" stroke-width="9"/>'
            f'<rect x="{-h}" y="{-h}" width="{size}" height="{size}" rx="24" fill="#FFFFFF" stroke="{INK}" stroke-width="9"/>'
            f'<text x="0" y="{h * 0.42:.0f}" font-family="{FONT}" font-weight="800" font-size="{size * 0.66:.0f}" text-anchor="middle" fill="#6C4BD8">{letter}</text></g>')


DEFS = '''<defs>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF27A"/><stop offset="0.55" stop-color="#FFC93C"/><stop offset="1" stop-color="#F59B23"/></linearGradient>
<linearGradient id="purp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B58CFF"/><stop offset="1" stop-color="#6C3FE0"/></linearGradient>
<linearGradient id="iconbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6FC3F5"/><stop offset="0.55" stop-color="#8B7CF2"/><stop offset="1" stop-color="#B36BE8"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.6"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
</defs>'''


def logo():
    W, H = 1200, 860
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', DEFS]
    # big Z hex badge
    cx, cy = 600, 590
    out.append(f'<polygon points="{hexpts(cx, cy + 18, 200, 180)}" fill="#5B3BC4" stroke="{INK}" stroke-width="14" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{hexpts(cx, cy, 200, 180)}" fill="url(#purp)" stroke="{INK}" stroke-width="14" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{hexpts(cx - 20, cy - 30, 140, 110)}" fill="#FFFFFF" opacity="0.18"/>')
    out.append(f'<text x="{cx}" y="{cy + 112}" font-family="{FONT}" font-weight="800" font-size="330" text-anchor="middle" '
               f'fill="#FFFFFF" stroke="{INK}" stroke-width="16" paint-order="stroke" stroke-linejoin="round">Z</text>')
    # WORD in gold
    out.append(f'<text x="600" y="380" font-family="{FONT}" font-weight="800" font-size="290" text-anchor="middle" letter-spacing="6" '
               f'fill="{INK}" stroke="{INK}" stroke-width="34" stroke-linejoin="round" transform="translate(0,14)">WORD</text>')
    out.append(f'<text x="600" y="380" font-family="{FONT}" font-weight="800" font-size="290" text-anchor="middle" letter-spacing="6" '
               f'fill="url(#gold)" stroke="{INK}" stroke-width="18" paint-order="stroke" stroke-linejoin="round">WORD</text>')
    # floating tiles + sparkles
    out += [tile(150, 150, 'A', -12), tile(1060, 140, 'C', 10), tile(200, 640, 'W', 8, 110), tile(1000, 640, 'D', -8, 110)]
    out += [sparkle(330, 520, 1.2), sparkle(880, 470, 1.0), sparkle(700, 90, 0.9), sparkle(80, 420, 0.8, '#FFE36A'), sparkle(1130, 420, 0.9, '#FFE36A')]
    out.append('</svg>')
    return ''.join(out)


def app_icon():
    S = 1024
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">', DEFS,
           f'<rect width="{S}" height="{S}" fill="url(#iconbg)"/>',
           f'<circle cx="420" cy="360" r="520" fill="url(#glow)"/>']
    # faint honeycomb
    r = 110
    for row in range(-1, 8):
        for col in range(-1, 9):
            x = col * r * 1.5
            y = row * r * 1.732 + (r * 0.866 if col % 2 else 0)
            out.append(f'<polygon points="{hexpts(x, y, r - 10)}" fill="none" stroke="#FFFFFF" stroke-width="8" opacity="0.10"/>')
    cx, cy = 512, 530
    out.append(f'<polygon points="{hexpts(cx, cy + 34, 360, 320)}" fill="#4A2FB0" opacity="0.55"/>')
    out.append(f'<polygon points="{hexpts(cx, cy + 22, 340, 300)}" fill="#B7A9E8" stroke="{INK}" stroke-width="22" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{hexpts(cx, cy, 340, 300)}" fill="#FFFFFF" stroke="{INK}" stroke-width="22" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{hexpts(cx - 40, cy - 70, 230, 170)}" fill="#EEE9FF" opacity="0.8"/>')
    out.append(f'<text x="{cx}" y="{cy + 180}" font-family="{FONT}" font-weight="800" font-size="560" text-anchor="middle" '
               f'fill="url(#gold)" stroke="{INK}" stroke-width="26" paint-order="stroke" stroke-linejoin="round">Z</text>')
    out += [sparkle(820, 190, 2.4), sparkle(190, 820, 1.8, '#FFE36A'), sparkle(880, 860, 1.2)]
    out.append('</svg>')
    return ''.join(out)


if __name__ == '__main__':
    d = sys.argv[1]
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'logo.svg'), 'w').write(logo())
    open(os.path.join(d, 'app_icon.svg'), 'w').write(app_icon())
    print('ok')
