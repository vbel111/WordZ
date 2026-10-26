"""App icon = the exact home-screen logo (Art/Logo/logo.png) on a soft version of the home scene.
python3 app_icon_from_logo.py <ZWordGame dir> <out.png> [preview.png]"""
import sys
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

game, out = sys.argv[1], sys.argv[2]
bg = Image.open(f'{game}/Art/Backgrounds/home_bg.jpg').convert('RGB')
logo = Image.open(f'{game}/Art/Logo/logo.png').convert('RGBA')
S = 1024

# background: top square of the home scene (sky, mountains, town), softened so the logo pops
W = bg.width
c = bg.crop((0, 0, W, W)).resize((S, S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(9))
c = ImageEnhance.Color(c).enhance(1.1)
# gentle light behind the logo
glow = Image.new('L', (S, S), 0)
ImageDraw.Draw(glow).ellipse((90, 160, 934, 880), fill=120)
glow = glow.filter(ImageFilter.GaussianBlur(120))
c = Image.composite(Image.new('RGB', (S, S), (255, 250, 235)), c, glow)

lg = logo.crop(logo.getbbox())
k = 950 / lg.width
lg = lg.resize((int(lg.width * k), int(lg.height * k)), Image.LANCZOS)
sh = Image.new('RGBA', lg.size, (40, 20, 5, 0))
sh.putalpha(lg.split()[3].filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.45)))
icon = c.convert('RGBA')
x, y = (S - lg.width) // 2, 520 - lg.height // 2
icon.alpha_composite(sh, (x, y + 16))
icon.alpha_composite(lg, (x, y))
icon = icon.convert('RGB')          # App Store icons must be opaque
icon.save(out)

if len(sys.argv) > 3:
    m = Image.new('L', (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, S - 1, S - 1), radius=230, fill=255)
    p = Image.new('RGB', (S, S), (30, 30, 30))
    p.paste(icon, (0, 0), m)
    prev = Image.new('RGB', (560, 300), (30, 30, 30))
    for sz, xy in [(240, (20, 30)), (120, (300, 30)), (60, (450, 30)), (40, (450, 120))]:
        prev.paste(p.resize((sz, sz), Image.LANCZOS), xy)
    prev.save(sys.argv[3])
print('ok')
