"""Word Z feature icons (256x256, transparent) in the home-icon style: thick warm-brown outline, two-tone
fills with a light top/left highlight. python3 icons5.py out_dir -> *.svg (render with render.js)."""
import os
import sys
from style import OL, lin, rad

FONT = "Baloo, 'Arial Black', Arial, sans-serif"


def icon_svg(body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><defs>{defs}</defs>'
            f'<g stroke="{OL}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round">{body}</g></svg>')


def flame():
    d = lin('fl', [(0, '#FFE45A', 1), (0.55, '#FFB21F', 1), (1, '#F0731C', 1)]) + lin('fl2', [(0, '#FFF6C2', 1), (1, '#FFD23F', 1)])
    body = ('<path d="M128 22 Q150 70 186 96 Q226 128 214 176 Q200 228 128 234 Q56 228 42 176 Q32 132 70 100 Q74 132 96 140 '
            'Q84 96 104 62 Q116 42 128 22 Z" fill="url(#fl)"/>'
            '<path d="M130 112 Q150 140 164 156 Q182 180 168 204 Q154 224 128 224 Q102 224 90 204 Q80 182 98 160 Q104 176 116 178 '
            'Q110 148 130 112 Z" fill="url(#fl2)" stroke-width="6"/>'
            '<path d="M70 150 Q66 176 82 196" fill="none" stroke="#FFFFFF" stroke-width="9" opacity="0.6"/>')
    return icon_svg(body, d)


def book():
    d = lin('bk', [(0, '#FF8576', 1), (1, '#D9473A', 1)])
    body = ('<path d="M34 58 Q80 40 128 62 Q176 40 222 58 L222 206 Q176 190 128 210 Q80 190 34 206 Z" fill="url(#bk)"/>'
            '<path d="M48 64 Q86 52 122 70 L122 196 Q86 180 48 192 Z" fill="#FFF8EA" stroke-width="6"/>'
            '<path d="M134 70 Q170 52 208 64 L208 192 Q170 180 134 196 Z" fill="#FFF8EA" stroke-width="6"/>'
            '<path d="M128 62 L128 210" stroke-width="7"/>'
            # word lines + a hex on each page
            + ''.join(f'<rect x="62" y="{y}" width="{w}" height="9" rx="4.5" fill="#E6CFA6" stroke="none"/>' for y, w in [(96, 46), (118, 40), (140, 48), (162, 34)])
            + '<path d="M170 96 l18 10 l0 22 l-18 10 l-18 -10 l0 -22 Z" fill="#FFC93C" stroke-width="5"/>'
            f'<text x="170" y="133" font-family="{FONT}" font-weight="800" font-size="30" text-anchor="middle" fill="{OL}" stroke="none">A</text>'
            + ''.join(f'<rect x="150" y="{y}" width="{w}" height="9" rx="4.5" fill="#E6CFA6" stroke="none"/>' for y, w in [(152, 44), (172, 36)])
            + '<path d="M176 40 L176 92 L190 80 L204 92 L204 40" fill="#FFC93C" stroke-width="6"/>')
    return icon_svg(body, d)


def bell():
    d = lin('bl', [(0, '#FFE45A', 1), (1, '#F5A511', 1)])
    body = ('<circle cx="128" cy="46" r="14" fill="#FFC93C"/>'
            '<path d="M128 56 Q70 58 66 128 Q64 168 40 188 L216 188 Q192 168 190 128 Q186 58 128 56 Z" fill="url(#bl)"/>'
            '<rect x="34" y="182" width="188" height="24" rx="12" fill="#F5A511"/>'
            '<path d="M106 210 Q128 246 150 210 Z" fill="#9A5B27"/>'
            '<path d="M92 96 Q82 120 84 150" fill="none" stroke="#FFFFFF" stroke-width="10" opacity="0.7"/>'
            '<path d="M30 92 Q18 112 26 136 M226 92 Q238 112 230 136" fill="none" stroke-width="8"/>')
    return icon_svg(body, d)


def pumpkin_body(cx=128, cy=146, s=1.0, face=True):
    def P(x, y): return f'{cx + x * s:.1f} {cy + y * s:.1f}'
    out = [f'<path d="M{P(-6, -76)} Q{P(-2, -100)} {P(14, -108)} L{P(22, -96)} Q{P(10, -88)} {P(10, -72)} Z" fill="#6C9E3A" stroke-width="7"/>',
           f'<path d="M{P(10, -84)} Q{P(40, -112)} {P(66, -94)} Q{P(44, -72)} {P(12, -78)} Z" fill="#7CCB4E" stroke-width="6"/>']
    lobes = [(-58, 78, 74), (58, 78, 74), (-26, 64, 80), (26, 64, 80), (0, 46, 82)]
    for x, rx, ry in lobes:
        out.append(f'<ellipse cx="{cx + x * s:.1f}" cy="{cy:.1f}" rx="{rx * s:.1f}" ry="{ry * s:.1f}" fill="url(#pk)"/>')
    out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{46 * s:.1f}" ry="{82 * s:.1f}" fill="url(#pk)" stroke="none"/>')
    out.append(f'<path d="M{P(-70, -30)} Q{P(-80, 0)} {P(-66, 34)}" fill="none" stroke="#FFFFFF" stroke-width="{9 * s:.1f}" opacity="0.55"/>')
    if face:
        out += [f'<path d="M{P(-44, -18)} L{P(-20, -34)} L{P(-14, -6)} Z" fill="#5A2A0E" stroke-width="5"/>',
                f'<path d="M{P(44, -18)} L{P(20, -34)} L{P(14, -6)} Z" fill="#5A2A0E" stroke-width="5"/>',
                f'<path d="M{P(-46, 18)} Q{P(0, 64)} {P(46, 18)} L{P(30, 24)} L{P(18, 14)} L{P(6, 28)} L{P(-6, 18)} L{P(-18, 30)} L{P(-30, 18)} Z" fill="#5A2A0E" stroke-width="5"/>',
                f'<path d="M{P(-30, 30)} Q{P(0, 52)} {P(30, 30)}" fill="none" stroke="#FFD23F" stroke-width="{5 * s:.1f}" opacity="0.8"/>']
    return ''.join(out)


PK = lin('pk', [(0, '#FFC23A', 1), (1, '#F08A12', 1)])


def pumpkin_event():
    body = pumpkin_body(126, 150, 0.84) + ('<path d="M206 40 Q210 58 228 62 Q210 66 206 84 Q202 66 184 62 Q202 58 206 40 Z" fill="#FFE36A" stroke-width="4"/>'
                             '<path d="M40 196 Q43 208 54 210 Q43 213 40 224 Q37 213 26 210 Q37 208 40 196 Z" fill="#FFE36A" stroke-width="3"/>')
    return icon_svg(body, PK)


def pumpkin_cat():
    return icon_svg(pumpkin_body(128, 146, 0.86), PK)


def badge_halloween():
    d = PK + lin('gd', [(0, '#FFE45A', 1), (1, '#F5A511', 1)]) + rad('night', [(0, '#5A3E6E', 1), (1, '#3A2848', 1)])
    body = ('<path d="M76 176 L48 244 L80 232 L98 254 L120 190 Z" fill="#E5533D" stroke-width="6"/>'
            '<path d="M180 176 L208 244 L176 232 L158 254 L136 190 Z" fill="#E5533D" stroke-width="6"/>'
            '<circle cx="128" cy="116" r="98" fill="url(#gd)"/>'
            '<circle cx="128" cy="116" r="76" fill="#4A2A14" stroke-width="6"/>'
            '<circle cx="168" cy="78" r="16" fill="#FFF3C4" stroke="none"/><circle cx="174" cy="74" r="13" fill="#4A2A14" stroke="none"/>'
            + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="#FFF3C4" stroke="none"/>' for x, y in [(86, 72), (104, 60), (148, 58), (74, 98)])
            + pumpkin_body(128, 136, 0.5)
            + '<path d="M60 70 Q50 100 58 130" fill="none" stroke="#FFFFFF" stroke-width="9" opacity="0.6"/>')
    return icon_svg(body, d)


ICONS = {'icon_flame': flame, 'icon_book': book, 'icon_bell': bell, 'icon_event_halloween': pumpkin_event,
         'cat_halloween': pumpkin_cat, 'badge_halloween_2026': badge_halloween}

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for n, f in ICONS.items():
        open(os.path.join(out, n + '.svg'), 'w').write(f())
    print('ok')
