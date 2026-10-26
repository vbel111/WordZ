"""Python port of Editor/LevelBaker.cs word picking + LevelGenerator.Tile, to test new board shapes before baking in Unity.
python3 bake_sim.py categories.json enable1.txt"""
import json, random, sys, time

DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]


def cells(cols):
    out, n = [], len(cols)
    for i in range(n):
        q = i - (n - 1) // 2
        L = cols[i]
        shift = 0 if (L - 1) % 2 == q % 2 else (1 if q > 0 else -1)
        for k in range(L):
            v = -(L - 1) + 2 * k + shift
            out.append((q, (v - q) // 2))
    return out


S7, S13, S17, S19, S23, S27, S37 = [2, 3, 2], [4, 5, 4], [3, 4, 3, 4, 3], [3, 4, 5, 4, 3], [5, 4, 5, 4, 5], [5, 6, 5, 6, 5], [4, 5, 6, 7, 6, 5, 4]
S29, S33 = [5, 6, 7, 6, 5], [2, 5, 6, 7, 6, 5, 2]


def ramp(event=False):
    r = []
    def add(n, c, a, b, lo, hi): r.extend([(c, a, b, lo, hi)] * n)
    if event:
        add(2, S13, 3, 3, 3, 6); add(3, S17, 3, 4, 3, 7); add(4, S19, 3, 5, 3, 8); add(3, S23, 4, 5, 4, 8); add(2, S27, 4, 6, 4, 8); add(1, S37, 5, 7, 4, 8)
    else:
        add(2, S7, 2, 2, 3, 4); add(4, S13, 3, 3, 3, 6); add(4, S17, 3, 4, 3, 7); add(6, S19, 3, 5, 3, 8); add(4, S23, 4, 5, 4, 8); add(4, S27, 4, 6, 4, 8); add(1, S37, 5, 7, 4, 8)
        add(3, S23, 4, 5, 4, 8); add(5, S27, 4, 6, 4, 8); add(6, S29, 5, 6, 4, 8); add(10, S33, 5, 7, 4, 8); add(1, S37, 5, 7, 5, 8)
    return r


def tile(cs, lengths, rng, budget=[0]):
    free = set(cs)
    res = []
    b = [40000]

    def comps_ok(frm):
        if not free: return frm == len(lengths)
        mn = min(lengths[frm:]) if frm < len(lengths) else 999
        seen = set()
        for c in list(free):
            if c in seen: continue
            st = [c]; seen.add(c); size = 0
            while st:
                h = st.pop(); size += 1
                for d in DIRS:
                    n = (h[0] + d[0], h[1] + d[1])
                    if n in free and n not in seen: seen.add(n); st.append(n)
            if size < mn: return False
            can = [False] * (size + 1); can[0] = True
            for L in lengths[frm:]:
                for s in range(size, L - 1, -1):
                    if can[s - L]: can[s] = True
            if not can[size]: return False
        return True

    def rec(wi):
        if wi == len(lengths): return not free
        b[0] -= 1
        if b[0] < 0: return False
        starts = sorted(free, key=lambda _: rng.random())
        for s in starts:
            path = [s]; free.discard(s)
            if ext(path, wi): return True
            free.add(s)
            if b[0] < 0: return False
        return False

    def ext(path, wi):
        b[0] -= 1
        if b[0] < 0: return False
        if len(path) == lengths[wi]:
            if not comps_ok(wi + 1): return False
            res.append(list(path))
            if rec(wi + 1): return True
            res.pop(); return False
        last = path[-1]
        for d in sorted(DIRS, key=lambda _: rng.random()):
            n = (last[0] + d[0], last[1] + d[1])
            if n not in free: continue
            free.discard(n); path.append(n)
            if ext(path, wi): return True
            path.pop(); free.add(n)
            if b[0] < 0: return False
        return False

    return res if rec(0) else None


def pick(pool, usage, total, minW, maxW, lo, hi, rng, avoid):
    cand = [w for w in pool if lo <= len(w) <= hi and w not in avoid]
    rng.shuffle(cand)
    cand.sort(key=lambda w: usage[w])
    chosen = []

    def P(start, rem):
        if rem == 0: return len(chosen) >= minW
        if len(chosen) >= maxW or rem < lo: return False
        for i in range(start, len(cand)):
            w = cand[i]
            if len(w) > rem: continue
            if any(x in w or w in x for x in chosen): continue
            chosen.append(w)
            if P(i + 1, rem - len(w)): return True
            chosen.pop()
        return False
    return chosen if P(0, total) else None


def bake(name, pool, event, seed):
    usage = {w: 0 for w in pool}; prev = set(); out = []
    for li, (cols, minW, maxW, lo, hi) in enumerate(ramp(event)):
        cs = cells(cols); rng = random.Random(seed * 31 + li)
        paths = None; tries = 0
        for attempt in range(300):
            tries += 1
            ch = pick(pool, usage, len(cs), minW, maxW, lo, hi, rng, prev)
            if ch is None:
                if lo > 3: lo -= 1
                elif minW > 1: minW -= 1
                hi = min(8, hi + 1); maxW += 1; continue
            ch.sort(key=len, reverse=True)
            paths = tile(cs, [len(w) for w in ch], rng)
            if paths: break
        if not paths: return f'{name} level {li+1} FAILED'
        for w in ch: usage[w] += 1
        prev = set(ch)
        out.append((len(cs), ch, tries))
    return out


if __name__ == '__main__':
    defs = json.load(open(sys.argv[1]))['categories']
    d = set(w.strip().upper() for w in open(sys.argv[2]))
    for k, c in enumerate(defs):
        allow = set((c.get('allow') or '').replace(',', ' ').upper().split())
        pool = []
        for w in dict.fromkeys(c['words'].upper().split()):
            if 3 <= len(w) <= 8 and w.isalpha() and (c.get('properNouns') or w in allow or w in d): pool.append(w)
        t = time.time()
        r = bake(c['name'], pool, bool(c.get('eventStart')), k + 1)
        if isinstance(r, str): print(r); continue
        last = r[-1]
        from collections import Counter
        use = Counter(w for _, ws, _ in r for w in ws)
        print(f"{c['name']:12s} {len(r)} levels  shapes {sorted(set(x[0] for x in r))}  maxtries {max(x[2] for x in r)}  words used {len(use)}/{len(pool)} maxreuse {max(use.values())}  {time.time()-t:.1f}s")
