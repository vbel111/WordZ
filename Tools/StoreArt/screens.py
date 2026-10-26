"""Store screenshot screens for Word Z, drawn from the game's real art, level data and UI layout
(GameScreen / MapScreen / HomeScreen / FeatureScreens). python3 screens.py out_dir -> screen_*.svg
Render with Tools/ArtGen/maps_v2/render.js. Canvas = the game's UI space on a 6.9" iPhone: 1080 x 2346."""
import base64, json, math, os, sys, random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
GAME = os.path.join(ROOT, 'ZWordGame')
sys.path.insert(0, os.path.join(ROOT, 'Tools', 'LevelTools'))
W, H = 1080, 2346
TOP, BOT = 130, 70            # safe-area insets (notch / home bar)
INK = '#5B3418'
FONT = "Baloo, 'Arial Black', sans-serif"
SQ3 = math.sqrt(3)
WORD_COLORS = ['#4CD137', '#F46FD8', '#3AA0F5', '#FF8A3D', '#9B59E6', '#1FC1B5', '#F2506A']


def img64(path):
    ext = 'png' if path.endswith('.png') else 'jpeg'
    return f'data:image/{ext};base64,' + base64.b64encode(open(os.path.join(GAME, path), 'rb').read()).decode()


_cache = {}
def I(path):
    if path not in _cache:
        _cache[path] = img64(path)
    return _cache[path]


def image(path, x, y, w, h, extra=''):
    return f'<image href="{I(path)}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="xMidYMid slice" {extra}/>'


def icon(path, cx, cy, size):
    return f'<image href="{I(path)}" x="{cx - size / 2:.1f}" y="{cy - size / 2:.1f}" width="{size:.1f}" height="{size:.1f}" preserveAspectRatio="xMidYMid meet"/>'


def text(x, y, s, size, fill='#FFFFFF', outline=None, anchor='middle', weight=800, extra=''):
    o = f'stroke="{outline}" stroke-width="{size * 0.16:.1f}" paint-order="stroke" stroke-linejoin="round"' if outline else ''
    return (f'<text x="{x:.1f}" y="{y + size * 0.35:.1f}" font-family="{FONT}" font-weight="{weight}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{fill}" {o} {extra}>{s}</text>')


def rrect(x, y, w, h, r, fill, extra=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="{fill}" {extra}/>'


def darken(c, f=0.7):
    v = [int(c[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{int(x * f):02X}' for x in v)


def chunky(cx, cy, w, h, face, label=None, size=60, r=None, depth=14):
    r = r if r is not None else min(h / 2, 34)
    out = [rrect(cx - w / 2, cy - h / 2 + depth, w, h - depth, r, darken(face)),
           rrect(cx - w / 2, cy - h / 2, w, h - depth, r, face),
           rrect(cx - w / 2 + 10, cy - h / 2 + 6, w - 20, (h - depth) * 0.42, r * 0.8, '#FFFFFF', 'opacity="0.22"')]
    if label:
        out.append(text(cx, cy - depth / 2, label, size, '#FFFFFF', '#4A2410'))
    return ''.join(out)


def round_btn(cx, cy, d, face, icon_path=None, glyph=None):
    out = [f'<circle cx="{cx}" cy="{cy + 8}" r="{d / 2}" fill="{darken(face)}"/>', f'<circle cx="{cx}" cy="{cy}" r="{d / 2}" fill="{face}"/>',
           f'<ellipse cx="{cx}" cy="{cy - d * 0.2}" rx="{d * 0.32}" ry="{d * 0.16}" fill="#FFFFFF" opacity="0.25"/>']
    if icon_path:
        out.append(icon(icon_path, cx, cy, d * 0.6))
    return ''.join(out)


def header(title, tab=None, gear=True):
    y = TOP + 104
    out = [round_btn(84, y, 104, '#FFC928', 'Art/Icons/back.png')]
    if gear:
        out.append(round_btn(W - 84, y, 104, '#FFC928', 'Art/Icons/gear.png'))
    out += [rrect(W / 2 - 210, y - 48, 420, 96, 40, '#E39A12'), rrect(W / 2 - 210, y - 48, 420, 86, 40, '#FFD02E'),
            text(W / 2, y - 6, title, 50, INK)]
    if tab:
        out += [rrect(W / 2 - 60, y - 48 - 26, 120, 40, 20, '#FFF3B0'), text(W / 2, y - 54, tab, 24, INK)]
    return ''.join(out)


def sky(path='Resources/UI/app_bg.jpg'):
    return image(path, 0, 0, W, H)


def chip(cx, cy, w, kind, value):
    icon_p = {'star': 'Art/Icons/star.png', 'coin': 'Art/Icons/coin.png', 'gem': 'Art/Icons/gem.png'}[kind]
    return (rrect(cx - w / 2 + 18, cy - 29, w - 18, 58, 29, '#5C3310', 'opacity="0.55"') + icon(icon_p, cx - w / 2 + 30, cy, 70) +
            text(cx + 30, cy - 2, value, 38, '#FFFFFF', '#4A2410'))


# ------------------------------------------------------------------ hex board
def hex_pts(cx, cy, r):
    return ' '.join(f'{cx + math.cos(math.radians(a)) * r:.1f},{cy + math.sin(math.radians(a)) * r * 0.9:.1f}' for a in range(0, 360, 60))


def board(cells, letters, cx, cy, radius, colours=None, selection=(), gold=None):
    """cells: list of (q,r). colours: {cell: hex}. selection: ordered cells being dragged."""
    colours = colours or {}
    pos = {c: (radius * 1.5 * c[0], radius * SQ3 * (c[1] + c[0] * 0.5)) for c in cells}
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    ox, oy = cx - (min(xs) + max(xs)) / 2, cy - (min(ys) + max(ys)) / 2
    out = [f'<ellipse cx="{cx}" cy="{cy}" rx="{(max(xs) - min(xs)) * 0.75 + radius * 1.6:.0f}" ry="{(max(ys) - min(ys)) * 0.75 + radius * 1.6:.0f}" fill="url(#plate)"/>']
    r = radius * 0.95
    for c in cells:
        x, y = pos[c][0] + ox, pos[c][1] + oy
        sel = c in selection
        face = '#FFD02E' if sel else colours.get(c, '#FFF3C4' if c == gold else '#FFFDF8')
        shadow = '#E39A12' if sel else (darken(colours[c]) if c in colours else ('#E7A51C' if c == gold else '#EDBE62'))
        ink = '#FFFFFF' if c in colours and not sel else ('#9A5A06' if c == gold else INK)
        if c == gold:
            out.append(f'<polygon points="{hex_pts(x, y + 6, r + 14)}" fill="#FFC21A"/>')
        out.append(f'<polygon points="{hex_pts(x, y + 12, r)}" fill="{shadow}"/>')
        out.append(f'<polygon points="{hex_pts(x, y, r)}" fill="{face}"/>')
        out.append(f'<polygon points="{hex_pts(x, y - r * 0.18, r * 0.72)}" fill="#FFFFFF" opacity="0.22"/>')
        out.append(text(x, y + 2, letters[c], radius * 0.85, ink))
        if c == gold:
            out.append(icon('Art/Icons/star.png', x + r * 0.62, y - r * 0.62, r * 0.55))
    for a, b in zip(selection, selection[1:]):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        x1 += ox; x2 += ox; y1 += oy; y2 += oy
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        L = math.hypot(x2 - x1, y2 - y1) * 0.42
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        out.append(f'<g transform="translate({mx:.1f} {my:.1f}) rotate({ang:.1f})"><rect x="{-L / 2:.1f}" y="-9" width="{L:.1f}" height="18" rx="9" fill="#FFFFFF" opacity="0.85"/>'
                   f'<path d="M{L / 2 - 4:.1f} -18 L{L / 2 + 22:.1f} 0 L{L / 2 - 4:.1f} 18 Z" fill="#FFFFFF" opacity="0.95"/></g>')
    return ''.join(out)


def level_cells(entry):
    cs = entry['cells']
    cells = [(cs[i], cs[i + 1]) for i in range(0, len(cs), 2)]
    letters = {cells[i]: entry['letters'][i] for i in range(len(cells))}
    words = [(w['w'], [cells[k] for k in w['p']]) for w in entry['words']]
    return cells, letters, words


def fit_radius(cells, maxw, maxh, cap=100):
    xs = [1.5 * c[0] for c in cells]; ys = [SQ3 * (c[1] + c[0] * 0.5) for c in cells]
    uw, uh = max(xs) - min(xs) + 2, max(ys) - min(ys) + SQ3
    return min(cap, maxw / uw, maxh / uh)


def slots(words, found, bottom_y, box=56, gap=8, wgap=40):
    """answer slot rows above the boosters (GameScreen.BuildSlots)."""
    lines, cur, wsum = [], [], 0
    for w, _ in words:
        ww = len(w) * box + (len(w) - 1) * gap
        add = ww if not cur else ww + wgap
        if cur and wsum + add > 980:
            lines.append(cur); cur, wsum, add = [], 0, ww
        cur.append(w); wsum += add
    if cur: lines.append(cur)
    lineH = 70
    totalH = len(lines) * lineH
    top = bottom_y - totalH
    out = [rrect(W / 2 - 510, top - 17, 1020, totalH + 34, 34, '#4D290A', 'opacity="0.38"')]
    for li, line in enumerate(lines):
        lw = sum(len(w) * box + (len(w) - 1) * gap for w in line) + (len(line) - 1) * wgap
        x = W / 2 - lw / 2
        y = top + lineH * (li + 0.5)
        for w in line:
            col = found.get(w)
            for k, ch in enumerate(w):
                out.append(rrect(x, y - box / 2 + 5, box, box, 14, '#33100A', 'opacity="0.35"'))
                out.append(rrect(x, y - box / 2, box, box, 14, col or '#FFFFFF', '' if col else 'opacity="0.92"'))
                if col:
                    out.append(text(x + box / 2, y, ch, box * 0.64, '#FFFFFF'))
                x += box + gap
            x += wgap - gap
    return ''.join(out), top


def boosters():
    out = []
    specs = [('#FFB61E', 'Art/Icons/letter.png', '3'), ('#9B4DE0', 'Art/Icons/shuffle.png', '2'), ('#2F9BEA', 'Art/Icons/clock.png', '3'), ('#4CC23A', 'Art/Icons/magnifier.png', '1')]
    for i, (c, ic, n) in enumerate(specs):
        cx, cy = W / 2 - 330 + i * 220, H - BOT - 128
        out.append(f'<circle cx="{cx}" cy="{cy + 10}" r="78" fill="{darken(c)}"/><circle cx="{cx}" cy="{cy}" r="78" fill="{c}"/>'
                   f'<circle cx="{cx}" cy="{cy}" r="62" fill="#FFFFFF" opacity="0.92"/>' + icon(ic, cx, cy, 92) +
                   f'<circle cx="{cx + 52}" cy="{cy - 52}" r="26" fill="#FFFFFF"/><circle cx="{cx + 52}" cy="{cy - 52}" r="22" fill="#E5484D"/>' +
                   text(cx + 52, cy - 52, n, 30))
    return ''.join(out)


def hud(frac=0.72, secs='84'):
    y = TOP + 250
    x0, w = W / 2 - 40 - 430, 860
    out = [rrect(x0 - 9, y - 30 - 7, w + 18, 79, 37, '#D9990B'), rrect(x0, y - 30, w, 60, 30, '#FFFFFF'),
           rrect(x0 + 6, y - 24, (w - 12) * frac, 48, 24, '#FFC21A'), rrect(x0 + 14, y - 22, (w - 28) * frac, 18, 9, '#FFFFFF', 'opacity="0.35"')]
    for at in (0.05, 0.25, 0.5):
        out.append(icon('Art/Icons/star.png', x0 + w * at, y + 4 - 4, 86))
    cx = x0 + w + 30
    out += [f'<circle cx="{cx}" cy="{y + 2}" r="59" fill="#D9990B"/><circle cx="{cx}" cy="{y}" r="52" fill="#FFFFFF"/>', text(cx, y + 2, secs, 44, INK)]
    return ''.join(out)


def backdrop(slug):
    return (image(f'Resources/GameBg/bg_{slug}.jpg', 0, 0, W, H) + f'<rect width="{W}" height="{H}" fill="#1F0D1A" opacity="0.18"/>'
            f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')


DEFS = ('<defs><radialGradient id="vig"><stop offset="0.55" stop-color="#26081E" stop-opacity="0"/><stop offset="1" stop-color="#26081E" stop-opacity="0.6"/></radialGradient>'
        '<radialGradient id="plate"><stop offset="0" stop-color="#4D290A" stop-opacity="0.42"/><stop offset="1" stop-color="#4D290A" stop-opacity="0"/></radialGradient></defs>')


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{body}</svg>'


def game_screen(slug, title, tab, entry, found_idx, sel_word=None, sel_len=0, gold_word=None, combo=None, secs='84', frac=0.72, preview=None):
    cells, letters, words = level_cells(entry)
    found = {words[i][0]: WORD_COLORS[i % 7] for i in found_idx}
    colours = {c: found[w] for w, p in words if w in found for c in p}
    selection = []
    if sel_word is not None:
        selection = words[sel_word][1][:sel_len]
    gold = words[gold_word][1][len(words[gold_word][1]) // 2] if gold_word is not None else None
    sl, slots_top = slots(words, found, H - BOT - 262)
    availH = slots_top - 24 - (TOP + 430)
    radius = fit_radius(cells, 1000, availH)
    cy = TOP + 430 + availH / 2
    body = [backdrop(slug), header(title, tab), hud(frac, secs), round_btn(84, TOP + 372, 92, '#FFC928', 'Art/Icons/restart.png'),
            round_btn(W - 84, TOP + 372, 92, '#FFC928', 'Art/Icons/bulb.png'),
            board(cells, letters, W / 2, cy, radius, colours, selection, gold), sl, boosters()]
    if preview:
        pw = 70 + len(preview) * 34
        body.append(rrect(W / 2 - pw / 2, TOP + 330, pw, 84, 30, '#FFFFFF') + text(W / 2, TOP + 372, preview, 54, INK))
    if combo:
        body.append(rrect(W / 2 - 120, TOP + 286, 240, 40, 20, '#5C3310', 'opacity="0.7"') + rrect(W / 2 - 116, TOP + 290, 232 * 0.62, 32, 16, '#FFC21A') +
                    text(W / 2, TOP + 305, combo, 26, '#FFFFFF', '#4A2410'))
    return svg(''.join(body))


def map_screen(slug, title, tab, count, done, scroll=0.0, boss_at=(24, 49), stars=None):
    r = random.Random(3)
    body = [image(f'Art/Maps/map_{slug}.jpg', 0, 0, W, H)]
    body.append(f'<rect x="160" y="0" width="760" height="{H}" fill="#4D2B0D" opacity="0.10"/>')
    # visible node positions: level i at y from bottom (MapScreen formula, contentH = 150*count/2*2 + 600)
    contentH = max(2400, 300 * count / 2 + 600)
    viewH = H - TOP - 180
    pos = {}
    for i in range(count):
        y = 330 + (contentH - 590) * i / (count - 1)
        x = W / 2 + math.sin(i * 0.95) * 270
        pos[i] = (x, y)
    base = pos[done][1] - viewH * 0.4 if scroll == 0 else scroll
    def sy(y): return H - (y - base) - 180 - BOT
    vis = [i for i in range(count) if -120 < sy(pos[i][1]) < H + 120]
    for i in vis:
        if i + 1 >= count: continue
        (ax, ay), (bx, by) = pos[i], pos[i + 1]
        n = max(3, int(math.hypot(bx - ax, by - ay) / 34))
        for k in range(1, n):
            t = k / n
            x = ax + (bx - ax) * t + math.sin(t * math.pi) * 30 * (1 if i % 2 == 0 else -1)
            y = sy(ay + (by - ay) * t)
            body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#5C3310" opacity="0.85"/><circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{"#FFC21A" if i < done else "#FFFFFF"}"/>')
    for i in vis:
        x, y = pos[i][0], sy(pos[i][1])
        boss = i in boss_at
        cur = i == done
        size = (150 if cur else 112) * (1.25 if boss else 1)
        face = '#FFC21A' if cur else ('#DCD6E4' if i < done else '#8D8496')
        if cur:
            body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size * 0.95:.0f}" fill="#FFE680" opacity="0.45"/>')
        body.append(f'<circle cx="{x:.1f}" cy="{y + size * 0.08:.1f}" r="{size / 2:.1f}" fill="{darken(face)}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{size / 2:.1f}" fill="{face}"/>'
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size / 2 - 9:.1f}" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.55"/>')
        if i > done:
            body.append(icon('Art/Icons/lock.png', x, y, size * 0.46))
        else:
            body.append(text(x, y, str(i + 1), size * 0.46, '#FFFFFF' if cur else '#5B3418', '#4A2410' if cur else None))
        if i < done:
            st = (stars or {}).get(i, 3)
            for s in range(3):
                body.append(icon('Art/Icons/star.png', x - 34 + s * 34, y + size / 2 + 4 + (6 if s == 1 else 0), 40) if s < st else
                            f'<circle cx="{x - 34 + s * 34}" cy="{y + size / 2 + 4}" r="14" fill="#4C3F4C" opacity="0.6"/>')
        if boss:
            body.append(icon('Art/Icons/crown.png', x, y - size / 2 - 20, size * 0.6) + text(x, y + size / 2 + (40 if i < done else 14), 'BOSS', 30, '#FFFFFF', '#4A2410'))
        if cur:
            body.append(f'<circle cx="{x:.1f}" cy="{y - size / 2 - 72:.1f}" r="54" fill="#FFFFFF"/>' + icon('Art/Icons/avatar.png', x, y - size / 2 - 72, 96))
    # header + progress card
    body.append(header(title, tab))
    cy = H - BOT - 120
    have = sum(((stars or {}).get(i, 3) for i in range(done)))
    body += [rrect(90, cy - 85 + 12, 900, 170, 40, '#6B3D0E', 'opacity="0.25"'), rrect(90, cy - 85, 900, 170, 40, '#FFFFFF'),
             text(300, cy - 47, title + ' PROGRESS', 34, '#5B3418', anchor='start'), icon('Art/Icons/star.png', 156, cy + 31, 56),
             rrect(200, cy + 7, 540, 48, 24, '#FBEACB'), rrect(203, cy + 10, 534 * have / (count * 3), 42, 21, '#FFC21A'),
             text(470, cy + 30, f'{have} / {count * 3}', 30, '#5B3418'), icon('Art/Icons/chest.png', 904, cy, 150)]
    return svg(''.join(body))


def home_screen():
    b = [image('Art/Backgrounds/home_bg.jpg', 0, 0, W, H), f'<rect width="{W}" height="230" fill="#4D2B0D" opacity="0.18"/>']
    # top bar
    y = TOP + 65
    b += [rrect(80, y - 38, 270, 76, 38, '#5C3310', 'opacity="0.55"'), icon('Art/Icons/avatar.png', 90, y, 90), text(150, y - 2, 'Player', 36, '#FFFFFF', '#4A2410', anchor='start'),
          chip(W / 2 + 40, y, 220, 'star', '48,250'), chip(W / 2 + 270, y, 200, 'coin', '2,140'), round_btn(W - 70, y, 96, '#FFC928', 'Art/Icons/gear.png')]
    lw = 780
    b.append(f'<image href="{I("Art/Logo/logo.png")}" x="{W / 2 - lw / 2}" y="{TOP + 470 - 280}" width="{lw}" height="560" preserveAspectRatio="xMidYMid meet"/>')
    # event banner, daily puzzle, info, play, categories, dock (bottom-anchored like HomeScreen)
    def bottom(yb): return H - BOT - yb
    ex, ey = W / 2 + 30, bottom(1012)
    b += [rrect(ex - 300, ey - 62 + 10, 600, 124, 40, '#2B1608', 'opacity="0.5"'), rrect(ex - 300, ey - 62, 600, 124, 40, '#4A2A14'),
          icon('Resources/HomeIcons/icon_event_halloween.png', ex - 300 + 85, ey - 8, 150),
          text(ex - 300 + 175, ey - 20, 'HALLOWEEN EVENT', 34, '#FFC21A', '#2B1608', anchor='start'),
          text(ex - 300 + 175, ey + 26, '6/15 levels  •  ends in 12d 4h', 26, '#FFFFFF', anchor='start', weight=600),
          f'<circle cx="{ex + 238}" cy="{ey}" r="42" fill="#FFC21A"/>', f'<path d="M{ex + 228} {ey - 18} L{ex + 254} {ey} L{ex + 228} {ey + 18} Z" fill="#5B3418"/>']
    dx, dy = W / 2 + 30, bottom(870)
    b += [rrect(dx - 300, dy - 62 + 10, 600, 124, 40, '#6B3D0E', 'opacity="0.5"'), rrect(dx - 300, dy - 62, 600, 124, 40, '#FFC928'),
          rrect(dx - 220, dy - 54, 500, 44, 22, '#FFFFFF', 'opacity="0.18"'),
          icon('Resources/HomeIcons/icon_daily_puzzle.png', dx - 300 + 85, dy - 6, 150),
          text(dx - 300 + 175, dy - 20, 'DAILY PUZZLE', 46, '#FFFFFF', '#4A2410', anchor='start'),
          text(dx - 300 + 175, dy + 26, 'Keep your 5-day streak going!', 26, '#5B3418', anchor='start', weight=600),
          f'<circle cx="{dx + 238}" cy="{dy}" r="42" fill="#FFFFFF"/>', f'<path d="M{dx + 228} {dy - 18} L{dx + 254} {dy} L{dx + 228} {dy + 18} Z" fill="#5B3418"/>',
          f'<g transform="rotate(6 {dx - 300 + 70} {dy - 62})">' + rrect(dx - 300 + 36, dy - 62 - 32, 92, 64, 30, '#E5484D') +
          icon('Resources/HomeIcons/icon_flame.png', dx - 300 + 44, dy - 66, 64) + text(dx - 300 + 98, dy - 64, '5', 36, '#FFFFFF', '#4A2410') + '</g>']
    iy = bottom(720)
    b += [rrect(W / 2 - 215, iy - 32, 430, 64, 32, '#5C3310', 'opacity="0.55"'), text(W / 2, iy, 'CITY  •  LEVEL 32', 34, '#FFFFFF', '#4A2410'),
          chunky(W / 2, bottom(580), 640, 160, '#5BC236', 'PLAY', 86, 50, 18), chunky(W / 2, bottom(410), 580, 128, '#FFC928', 'CATEGORIES', 58, 44, 14)]
    dock = [('Rewards', 'Resources/HomeIcons/icon_calendar.png'), ('Challenges', 'Resources/HomeIcons/icon_trophy.png'), ('Words', 'Resources/HomeIcons/icon_book.png'),
            ('Shop', 'Resources/HomeIcons/icon_shop.png'), ('Quests', 'Resources/HomeIcons/icon_quests.png')]
    for i, (lab, ic) in enumerate(dock):
        cx, cy = W / 2 - 404 + i * 202, bottom(190)
        b += [rrect(cx - 66, cy - 66 + 10, 132, 132, 30, darken('#FFC928')), rrect(cx - 66, cy - 66, 132, 122, 30, '#FFC928'),
              rrect(cx - 56, cy - 56, 112, 102, 24, '#FFFFFF'), icon(ic, cx, cy - 6, 102), text(cx, cy + 92, lab, 30, '#FFFFFF', '#4A2410')]
        if lab in ('Rewards', 'Words'):
            b.append(f'<circle cx="{cx + 58}" cy="{cy - 58}" r="23" fill="#FFFFFF"/><circle cx="{cx + 58}" cy="{cy - 58}" r="19" fill="#E5484D"/>' + text(cx + 58, cy - 58, '1', 25))
    return svg(''.join(b))


def book_screen(cat_name, color, words, have):
    b = [sky(), header(cat_name, None, gear=False), text(W / 2, TOP + 205, f'{len(have)} / {len(words)} words', 38, '#FFFFFF', '#4A2410')]
    maxW, chipH, gx, gy, lw = 940, 74, 14, 16, 27
    rows, x, y = [], 0, 0
    lay = []
    for w in words:
        width = 44 + len(w) * lw
        if x > 0 and x + width > maxW:
            x = 0; y += chipH + gy
        lay.append((w, x, y, width)); x += width + gx
    rowW = {}
    for w, x, y, width in lay: rowW[y] = x + width
    top = TOP + 290
    for w, x, y, width in lay:
        if top + y + chipH > H - BOT - 40: break
        X = (W - maxW) / 2 + x + (maxW - rowW[y]) / 2
        got = w in have
        b.append(rrect(X, top + y + 6, width, chipH, 24, darken(color, 0.75) if got else '#5C3310', '' if got else 'opacity="0.25"'))
        b.append(rrect(X, top + y, width, chipH, 24, color if got else '#FFFFFF', '' if got else 'opacity="0.75"'))
        b.append(text(X + width / 2, top + y + chipH / 2, w if got else w[0] + '_' * (len(w) - 1), 36, '#FFFFFF' if got else '#9A7550', '#4A2410' if got else None))
    return svg(''.join(b))


def main(out):
    os.makedirs(out, exist_ok=True)
    lv = json.load(open(os.path.join(GAME, 'Resources/Levels/levels.json')))
    cats = {c['name']: c for c in lv['categories']}
    city = cats['CITY']['levels'][10]                    # THEATER HOUSE SHOP BUS
    open(os.path.join(out, 'screen_game.svg'), 'w').write(game_screen('city', 'CITY', 'LV 11', city, [0, 3], sel_word=1, sel_len=4, preview='HOUS', gold_word=2))
    # boss board: a real 37-tile deal made with the game's own algorithm (Tools/LevelTools/bake_sim.py)
    import bake_sim as bs
    rng = random.Random(7)
    pool = [w for w in cats['SPACE']['levels'][0]['words'][0]['w'].split()]
    space_words = sorted({w['w'] for l in cats['SPACE']['levels'] for w in l['words']})
    cs = bs.cells(bs.S37)
    for _ in range(200):
        ch = bs.pick(space_words, {w: 0 for w in space_words}, 37, 5, 7, 4, 8, rng, set())
        if not ch: continue
        ch.sort(key=len, reverse=True)
        paths = bs.tile(cs, [len(w) for w in ch], rng)
        if paths: break
    idx = {c: i for i, c in enumerate(cs)}
    letters = [''] * 37
    entry = {'cells': [v for c in cs for v in c], 'words': []}
    for w, p in zip(ch, paths):
        for k, c in enumerate(p): letters[idx[c]] = w[k]
        entry['words'].append({'w': w, 'p': [idx[c] for c in p]})
    entry['letters'] = ''.join(letters)
    open(os.path.join(out, 'screen_boss.svg'), 'w').write(game_screen('space', 'SPACE', 'BOSS', entry, [0, 2, 4], gold_word=1, combo='NEXT WORD x2!', secs='191', frac=0.74))
    open(os.path.join(out, 'screen_map.svg'), 'w').write(map_screen('city', 'CITY', 'LV 32', 50, 31, stars={27: 2, 29: 2}))
    open(os.path.join(out, 'screen_event.svg'), 'w').write(map_screen('halloween', 'HALLOWEEN', 'LV 7', 15, 6, boss_at=(14,), stars={2: 2}))
    open(os.path.join(out, 'screen_home.svg'), 'w').write(home_screen())
    ocean = cats['OCEAN']['levels'][18]
    open(os.path.join(out, 'screen_daily.svg'), 'w').write(game_screen('ocean', 'DAILY', 'OCT 26', ocean, [0, 2], sel_word=1, sel_len=3, secs='112', frac=0.81,
                                                                       preview=''.join(level_cells(ocean)[2][1][0][:3]) and level_cells(ocean)[2][1][0][:3]))
    animals = sorted({w['w'] for l in cats['ANIMALS']['levels'] for w in l['words']})
    have = set(animals[::2] + animals[1::5])
    open(os.path.join(out, 'screen_book.svg'), 'w').write(book_screen('ANIMALS', '#FF8A3D', animals, have))
    print('ok', ch)


if __name__ == '__main__':
    main(sys.argv[1])
