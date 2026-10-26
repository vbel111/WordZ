"""Writes data.json for the trailer: a real City board and a real 37-tile boss deal (game algorithm)."""
import json, os, random, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'Tools', 'LevelTools'))
import bake_sim as bs
lv = json.load(open(os.path.join(ROOT, 'ZWordGame/Resources/Levels/levels.json')))
cats = {c['name']: c for c in lv['categories']}
city = cats['CITY']['levels'][10]
cs = city['cells']; cells = [[cs[i], cs[i + 1]] for i in range(0, len(cs), 2)]
board = {'cells': cells, 'letters': city['letters'], 'words': [{'w': w['w'], 'p': w['p']} for w in city['words']]}
space = sorted({w['w'] for l in cats['SPACE']['levels'] for w in l['words']})
rng = random.Random(11)
c37 = bs.cells(bs.S37)
while True:
    ch = bs.pick(space, {w: 0 for w in space}, 37, 5, 7, 4, 8, rng, set())
    if not ch: continue
    ch.sort(key=len, reverse=True)
    paths = bs.tile(c37, [len(w) for w in ch], rng)
    if paths: break
idx = {c: i for i, c in enumerate(c37)}
letters = [''] * 37
words = []
for w, p in zip(ch, paths):
    for k, c in enumerate(p): letters[idx[c]] = w[k]
    words.append({'w': w, 'p': [idx[c] for c in p]})
boss = {'cells': [list(c) for c in c37], 'letters': ''.join(letters), 'words': words}
json.dump({'board': board, 'boss': boss}, open(sys.argv[1], 'w'))
print(board['words'], [w['w'] for w in words])
