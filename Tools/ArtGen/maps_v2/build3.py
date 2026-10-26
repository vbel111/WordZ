"""python3 build3.py out_dir [name ...] -> renders the v3 (3/4 view) maps to out_dir/map_<name>.jpg + a contact sheet."""
import importlib, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MODULES = ['maps3_outdoor', 'maps3_special', 'maps3_indoor', 'maps3_event', 'home3']


def builders():
    out = {}
    for m in MODULES:
        try:
            out.update(importlib.import_module(m).BUILDERS)
        except ModuleNotFoundError as e:
            if e.name != m:
                raise
    import city2
    out['city'] = city2.build
    return out


if __name__ == '__main__':
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    b = builders()
    names = sys.argv[2:] or sorted(b)
    args = []
    for n in names:
        p = os.path.join(out_dir, f'map_{n}.svg')
        open(p, 'w').write(b[n]())
        args += [p, os.path.join(out_dir, f'map_{n}.png')]
    env = dict(os.environ, NODE_PATH=subprocess.check_output(['npm', 'root', '-g'], text=True).strip())
    subprocess.check_call(['node', os.path.join(HERE, 'render.js')] + args, env=env)
    from PIL import Image
    tiles = []
    for n in names:
        im = Image.open(os.path.join(out_dir, f'map_{n}.png')).convert('RGB')
        im.save(os.path.join(out_dir, f'map_{n}.jpg'), quality=88)
        os.remove(os.path.join(out_dir, f'map_{n}.png'))
        tiles.append(im.resize((360, 800)))
    sheet = Image.new('RGB', (370 * len(tiles), 800), 'white')
    for k, t in enumerate(tiles):
        sheet.paste(t, (k * 370, 0))
    sheet.save(os.path.join(out_dir, 'sheet.jpg'), quality=85)
    print('ok', names)
