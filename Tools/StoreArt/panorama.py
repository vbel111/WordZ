"""Panoramic store background (one scene across all screenshots) + pop-out hex tiles in the game's style.
python3 panorama.py out_dir N  -> pano.svg (N*1320 x 2868), tile_*.svg"""
import math, os, random, sys
from screens import hex_pts, darken, FONT, I

FW, FH = 1320, 2868


def pano(n):
    W = FW * n
    r = random.Random(5)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{FH}" viewBox="0 0 {W} {FH}"><defs>'
         '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3FA7EE"/><stop offset="0.42" stop-color="#8ED2F8"/>'
         '<stop offset="0.8" stop-color="#FFE9A8"/><stop offset="1" stop-color="#FFD25A"/></linearGradient>'
         '<radialGradient id="glow"><stop offset="0" stop-color="#FFF6C8" stop-opacity="0.9"/><stop offset="1" stop-color="#FFF6C8" stop-opacity="0"/></radialGradient>'
         '<linearGradient id="tileF" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF3B0"/><stop offset="1" stop-color="#FFC93C"/></linearGradient>'
         f'</defs><rect width="{W}" height="{FH}" fill="url(#sky)"/>']
    # giant faint honeycomb
    R = 150
    for row in range(-1, int(FH / (R * 1.732)) + 2):
        for col in range(-1, int(W / (R * 1.5)) + 2):
            x = col * R * 1.5
            y = row * R * 1.732 + (R * 0.866 if col % 2 else 0)
            op = 0.07 + 0.05 * r.random()
            fill = f'fill="#FFFFFF" fill-opacity="{0.06 * r.random():.3f}"' if r.random() < 0.25 else 'fill="none"'
            pts = ' '.join(f'{x + math.cos(math.radians(a)) * (R - 8):.0f},{y + math.sin(math.radians(a)) * (R - 8):.0f}' for a in range(0, 360, 60))
            o.append(f'<polygon points="{pts}" {fill} stroke="#FFFFFF" stroke-opacity="{op:.2f}" stroke-width="6"/>')
    # soft light pools behind each caption
    for k in range(n):
        o.append(f'<ellipse cx="{k * FW + FW / 2}" cy="330" rx="760" ry="380" fill="url(#glow)" opacity="0.55"/>')
    # continuous golden trail of letter tiles winding through the lower half (connects the frames)
    letters = 'FINDTHEHIDDENWORDSWORDZ' * 8
    li = 0
    t = 0.0
    x = -120
    while x < W + 200:
        y = 2080 + math.sin(x / 640.0) * 330 + math.sin(x / 233.0) * 60
        s = 0.8 + 0.25 * math.sin(x / 410.0)
        rr = 92 * s
        o.append(f'<ellipse cx="{x:.0f}" cy="{y + rr * 0.95:.0f}" rx="{rr * 0.9:.0f}" ry="{rr * 0.22:.0f}" fill="#7A4A10" opacity="0.18"/>')
        o.append(f'<polygon points="{hex_pts(x, y + 14 * s, rr)}" fill="#D9990B"/>')
        o.append(f'<polygon points="{hex_pts(x, y, rr)}" fill="url(#tileF)"/>')
        o.append(f'<polygon points="{hex_pts(x, y - rr * 0.2, rr * 0.7)}" fill="#FFFFFF" opacity="0.28"/>')
        o.append(f'<text x="{x:.0f}" y="{y + rr * 0.32:.0f}" font-family="{FONT}" font-weight="800" font-size="{rr * 0.9:.0f}" text-anchor="middle" fill="#7A4A10">{letters[li]}</text>')
        li += 1
        x += rr * 1.75
    # sparkles
    for _ in range(int(W / 90)):
        sx, sy, ss = r.uniform(0, W), r.uniform(700, FH - 100), r.uniform(0.6, 1.6)
        o.append(f'<path d="M{sx} {sy - 22 * ss} Q{sx + 3 * ss} {sy - 3 * ss} {sx + 22 * ss} {sy} Q{sx + 3 * ss} {sy + 3 * ss} {sx} {sy + 22 * ss} '
                 f'Q{sx - 3 * ss} {sy + 3 * ss} {sx - 22 * ss} {sy} Q{sx - 3 * ss} {sy - 3 * ss} {sx} {sy - 22 * ss} Z" fill="#FFFFFF" opacity="{r.uniform(0.5, 0.95):.2f}"/>')
    # leafy ground at the very bottom (brand motif)
    for k in range(int(W / 260) + 2):
        bx = k * 260 + r.uniform(-40, 40)
        o.append(f'<ellipse cx="{bx:.0f}" cy="{FH + 30}" rx="{r.uniform(150, 220):.0f}" ry="{r.uniform(90, 140):.0f}" fill="{r.choice(["#5CBF3F", "#6CC24A", "#4FB043"])}" stroke="#3A6B1E" stroke-width="6"/>')
    o.append('</svg>')
    return ''.join(o)


def tile(letter, face, size=360, gold=False):
    r = size * 0.42
    cx, cy = size / 2, size / 2 - 8
    shadow = darken(face)
    ink = '#FFFFFF' if face not in ('#FFFDF8', '#FFF3C4') else ('#9A5A06' if gold else '#5B3418')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">']
    if gold:
        o.append(f'<polygon points="{hex_pts(cx, cy + 6, r + 16)}" fill="#FFC21A"/>')
    o += [f'<polygon points="{hex_pts(cx, cy + 22, r)}" fill="{shadow}"/>', f'<polygon points="{hex_pts(cx, cy, r)}" fill="{face}"/>',
          f'<polygon points="{hex_pts(cx, cy - r * 0.18, r * 0.72)}" fill="#FFFFFF" opacity="0.25"/>',
          f'<text x="{cx}" y="{cy + r * 0.3:.0f}" font-family="{FONT}" font-weight="800" font-size="{r * 0.95:.0f}" text-anchor="middle" fill="{ink}" '
          f'stroke="{"#4A2410" if ink == "#FFFFFF" else "none"}" stroke-width="{r * 0.08:.1f}" paint-order="stroke">{letter}</text>']
    if gold:
        o.append(f'<image href="{I("Art/Icons/star.png")}" x="{cx + r * 0.3:.0f}" y="{cy - r * 1.05:.0f}" width="{r * 0.7:.0f}" height="{r * 0.7:.0f}"/>')
    o.append('</svg>')
    return ''.join(o)


if __name__ == '__main__':
    out, n = sys.argv[1], int(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'pano.svg'), 'w').write(pano(n))
    for name, (l, c, g) in {'W_green': ('W', '#4CD137', False), 'O_pink': ('O', '#F46FD8', False), 'R_blue': ('R', '#3AA0F5', False),
                            'D_yellow': ('D', '#FFD02E', False), 'Z_gold': ('Z', '#FFF3C4', True), 'S_purple': ('S', '#9B59E6', False),
                            'A_cream': ('A', '#FFFDF8', False), 'E_teal': ('E', '#1FC1B5', False)}.items():
        open(os.path.join(out, f'tile_{name}.svg'), 'w').write(tile(l, c, gold=g))
    print('ok')
