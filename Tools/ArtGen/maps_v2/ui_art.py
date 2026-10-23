"""UI art for the 'sky & candy' skin: app background (1080x2400) and category card pictures cut from the maps.
python3 ui_art.py <maps_dir> <out_resources_dir>"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from style import W, H, cloud, lin, rad, svg  # noqa: E402
from scene import sparkle  # noqa: E402


def app_bg():
    r = random.Random(5)
    defs = (lin('bgG', [(0, '#7FC8F4', 1), (0.45, '#A9C9F6', 1), (0.8, '#C7B6F2', 1), (1, '#B9A2EC', 1)]) +
            rad('glowG', [(0, '#FFFFFF', 0.55), (1, '#FFFFFF', 0)]))
    body = [f'<rect width="{W}" height="{H}" fill="url(#bgG)"/>',
            f'<circle cx="540" cy="700" r="700" fill="url(#glowG)"/>']
    # faint honeycomb pattern (the game board's shape) in the lower half
    import math
    hexr = 70
    for row in range(0, 22):
        for col in range(0, 10):
            cx = col * hexr * 1.5
            cy = 1100 + row * hexr * 1.732 + (hexr * 0.866 if col % 2 else 0)
            if cy > H + 80:
                continue
            pts = ' '.join(f'{cx + math.cos(math.radians(a)) * (hexr - 6):.0f},{cy + math.sin(math.radians(a)) * (hexr - 6):.0f}' for a in range(0, 360, 60))
            op = 0.05 + 0.06 * min(1, (cy - 1100) / 900)
            body.append(f'<polygon points="{pts}" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="{op:.2f}"/>')
    for x, y, s, o in [(160, 260, 1.0, 0.9), (900, 180, 0.8, 0.85), (980, 700, 0.6, 0.7), (90, 900, 0.7, 0.7),
                       (620, 520, 0.5, 0.6), (300, 1500, 0.6, 0.45), (880, 1700, 0.7, 0.4)]:
        body.append(cloud(x, y, s, o))
    for _ in range(40):
        body.append(sparkle(r.uniform(20, W - 20), r.uniform(20, H - 20), r.uniform(0.4, 1.1), '#FFFFFF', r.uniform(0.3, 0.8)))
    return svg(''.join(body), defs)


if __name__ == '__main__':
    maps, out = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(out, 'UI'), exist_ok=True)
    os.makedirs(os.path.join(out, 'CatCards'), exist_ok=True)
    open(os.path.join(out, 'UI', 'app_bg.svg'), 'w').write(app_bg())
    from PIL import Image
    for f in sorted(os.listdir(maps)):
        if f.startswith('map_') and f.endswith('.jpg') and f.count('.') == 1:
            im = Image.open(os.path.join(maps, f)).convert('RGB')
            band = im.crop((0, 500, 1080, 1220)).resize((480, 320), Image.LANCZOS)
            band.save(os.path.join(out, 'CatCards', 'card_' + f[4:]), quality=86)
    print('ok')
