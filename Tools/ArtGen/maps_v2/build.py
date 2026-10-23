"""python3 build.py out_dir [name ...]  -> renders the v2 maps to out_dir/map_<name>.jpg plus a preview sheet."""
import importlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MODULES = ['outdoor', 'themed', 'special', 'indoor']


def builders():
    out = {}
    for m in MODULES:
        try:
            out.update(importlib.import_module(m).BUILDERS)
        except ModuleNotFoundError:
            pass
    import city
    out['city'] = city.build
    return out


if __name__ == '__main__':
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    b = builders()
    names = sys.argv[2:] or sorted(b)
    args = []
    for n in names:
        svg_path = os.path.join(out_dir, f'map_{n}.svg')
        open(svg_path, 'w').write(b[n]())
        args += [svg_path, os.path.join(out_dir, f'map_{n}.png')]
    env = dict(os.environ, NODE_PATH=subprocess.check_output(['npm', 'root', '-g'], text=True).strip())
    subprocess.check_call(['node', os.path.join(HERE, 'render.js')] + args, env=env)
    from PIL import Image
    tiles = []
    for n in names:
        im = Image.open(os.path.join(out_dir, f'map_{n}.png')).convert('RGB')
        im.save(os.path.join(out_dir, f'map_{n}.jpg'), quality=90)
        os.remove(os.path.join(out_dir, f'map_{n}.png'))
        tiles.append(im.resize((324, 720)))
    sheet = Image.new('RGB', (324 * len(tiles), 720), 'white')
    for k, t in enumerate(tiles):
        sheet.paste(t, (k * 324, 0))
    sheet.save(os.path.join(out_dir, 'sheet_' + '_'.join(names)[:60] + '.jpg'), quality=85)
    print('ok', names)
