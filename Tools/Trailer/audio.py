"""Trailer soundtrack: Garden Stroll (original) + code-made SFX placed on the animation's events.
python3 audio.py music.wav out.wav"""
import sys, os
import numpy as np
from scipy.io import wavfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'MusicGen'))
from compose import SR, kalimba, marimba, kick, snare, hat, midi, lp, hp, bp, t_axis

DUR = 28.0
N = int(DUR * SR)
rng = np.random.default_rng(3)
sfx = np.zeros(N)


def put(sig, at, gain=1.0):
    i = int(at * SR)
    n = min(len(sig), N - i)
    if n > 0:
        sfx[i:i + n] += sig[:n] * gain


def whoosh(dur=0.5, up=True):
    t = t_axis(dur)
    n = rng.standard_normal(len(t))
    env = np.sin(np.pi * t / dur) ** 2
    lo, hi = (600, 5000) if up else (5000, 600)
    out = np.zeros_like(n)
    steps = 12
    for k in range(steps):
        a, b = k * len(t) // steps, (k + 1) * len(t) // steps
        f = lo + (hi - lo) * (k / steps)
        out[a:b] = bp(n, max(80, f * 0.6), min(18000, f * 1.6))[a:b]
    return out * env * 0.5


def rumble(dur=0.8):
    t = t_axis(dur)
    return lp(rng.standard_normal(len(t)), 140, 4) * np.exp(-t / (dur / 2)) * 2.5


def chime(notes, gap=0.07, g=0.6):
    total = np.zeros(int((gap * len(notes) + 1.6) * SR))
    for k, n in enumerate(notes):
        s = kalimba(midi(n)) * g
        i = int(k * gap * SR)
        total[i:i + len(s)] += s[:len(total) - i]
    return total


PENTA = [72, 74, 76, 79, 81, 84, 86, 88]
# 1 hook: tiles pop in, Z pops, tremble, the word explodes
for i in range(5):
    put(marimba(midi(PENTA[i])), 0.05 + i * 0.06, 0.8)
put(chime([84, 88]), 0.32, 0.7)
put(rumble(0.6), 0.75, 0.6)
put(whoosh(0.8, True), 1.25, 1.0)
put(kick(1.0), 1.35, 1.0)
put(snare(0.6), 1.36, 0.6)
# 2 fall and landing
put(whoosh(0.9, False), 3.55, 0.9)
put(kick(0.9), 4.6, 1.0)
put(marimba(midi(67)), 4.62, 0.5)
put(chime([79, 84, 88], 0.09), 4.95, 0.5)
# 3 board assembles, swipe H-O-U-S-E, words light up
for i in range(19):
    put(hat(0.8), 7.7 + i * 0.035 + 0.45, 0.6)
put(whoosh(0.5, False), 7.6, 0.7)
for k in range(5):
    put(kalimba(midi(PENTA[k] + 12)), 9.4 + k * 0.32, 0.8)
put(chime([72, 76, 79, 84], 0.06, 0.7), 11.0)
put(chime([84, 88, 91], 0.05, 0.6), 11.05)
for j, tw in enumerate([11.9, 12.35, 12.8]):
    put(chime([74 + j * 2, 79 + j * 2, 86 + j * 2], 0.05, 0.55), tw)
# 4 journey: whoosh per world, ticking counter, streak flame
for a in [13.9, 15.55, 17.1, 18.65]:
    put(whoosh(0.55, True), a, 0.75)
for k in range(16):
    put(hat(0.7), 14.4 + k * 0.125, 0.5)
put(chime([84, 91, 96], 0.06, 0.6), 17.2)
# 5 boss: slam, rumble, spiral in, fill pops, gold impact + fanfare, crown lands
put(whoosh(0.5, False), 20.1, 0.8)
put(kick(1.0), 20.4, 1.2)
put(rumble(1.0), 20.4, 1.0)
put(whoosh(0.9, True), 20.7, 0.6)
for k in range(12):
    put(marimba(midi(PENTA[k % 8])), 21.9 + k * 0.09, 0.45)
put(kick(1.0), 22.95, 1.2)
put(snare(1.0), 22.95, 0.7)
fan = [72, 76, 79, 84, 79, 84, 88]
put(chime(fan, 0.11, 0.75), 23.0)
put(chime([96, 100, 103], 0.05, 0.4), 23.6)
# 6 end card: logo lands, promise, CTA
put(whoosh(0.5, False), 24.4, 0.7)
put(kick(0.8), 24.95, 0.9)
put(chime([72, 79, 84, 88], 0.08, 0.6), 25.0)
put(marimba(midi(84)), 25.45, 0.5)
put(chime([88, 91], 0.06, 0.6), 26.05)

music_sr, music = wavfile.read(sys.argv[1])
music = music.astype(np.float32) / 32767
if music.ndim > 1:
    music = music.mean(1)
reps = int(np.ceil(N / len(music)))
music = np.tile(music, reps)[:N]
t = np.arange(N) / SR
duck = np.ones(N)
for a, b, d in [(1.3, 2.2, 0.5), (20.3, 21.4, 0.45), (22.9, 24.2, 0.45)]:
    m = (t > a) & (t < b)
    duck[m] = d
duck = np.convolve(duck, np.ones(2205) / 2205, mode='same')
fade = np.clip((DUR - t) / 1.2, 0, 1) * np.clip(t / 0.3, 0, 1)
mix = music * 0.55 * duck * fade + sfx * 0.55 * np.clip((DUR - t) / 0.4, 0, 1)
mix = np.tanh(mix * 1.1) / 1.1
mix *= 10 ** (-1.5 / 20) / max(1e-6, np.abs(mix).max())
st = np.stack([mix, mix], 1)
wavfile.write(sys.argv[2], SR, (st * 32767).astype(np.int16))
print('ok', len(mix) / SR)
