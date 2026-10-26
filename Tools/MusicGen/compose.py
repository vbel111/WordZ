"""Original, royalty-free gameplay loops for Word Z (no samples, pure synthesis).

python3 compose.py out_dir  -> garden_stroll.ogg, lofi_leaves.ogg, honey_breeze.ogg (+ .wav)
Each file loops seamlessly (the reverb/decay tail is wrapped back onto the start).
"""
import os
import subprocess
import sys

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
rng = np.random.default_rng(7)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def lp(x, hz, order=2):
    return sosfilt(butter(order, hz, 'low', fs=SR, output='sos'), x)


def hp(x, hz, order=2):
    return sosfilt(butter(order, hz, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)


# ---------------- instruments ----------------

def kalimba(f, dur=2.2):
    t = t_axis(dur)
    env = np.exp(-t / 0.75) * (1 - np.exp(-t / 0.002))
    x = np.sin(2 * np.pi * f * t) * env
    x += 0.25 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t / 0.35)
    x += 0.12 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / 0.06)      # bright tine "tink"
    x += 0.05 * np.sin(2 * np.pi * f * 7.1 * t) * np.exp(-t / 0.03)
    return x * 0.5


def epiano(f, dur=2.6, bright=1.0):
    t = t_axis(dur)
    idx = (0.25 + 1.6 * bright * np.exp(-t / 0.25))
    mod = np.sin(2 * np.pi * f * t)
    x = np.sin(2 * np.pi * f * t + idx * mod)
    x += 0.18 * np.sin(2 * np.pi * f * 14 * t) * np.exp(-t / 0.015)      # tine strike
    env = np.exp(-t / 1.1) * (1 - np.exp(-t / 0.004))
    trem = 1 + 0.12 * np.sin(2 * np.pi * 4.2 * t)
    return x * env * trem * 0.35


def marimba(f, dur=1.4):
    t = t_axis(dur)
    env = np.exp(-t / 0.32) * (1 - np.exp(-t / 0.0015))
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 4.0 * t) * np.exp(-t / 0.05)
    x += 0.1 * np.sin(2 * np.pi * f * 10 * t) * np.exp(-t / 0.01)
    return x * env * 0.45


def pad(freqs, dur, cutoff=1400):
    t = t_axis(dur)
    x = np.zeros_like(t)
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):
            ff = f * 2 ** (det / 12)
            ph = rng.random()
            x += 2 * ((ff * t + ph) % 1) - 1                                # saw
    x = lp(x, cutoff, 2) / (len(freqs) * 3)
    a, r = 0.9, 1.0
    env = np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (dur - t) / r))
    return x * env * 0.5


def bass(f, dur):
    t = t_axis(dur + 0.25)
    env = (1 - np.exp(-t / 0.01)) * np.exp(-t / 1.6)
    env *= np.minimum(1, np.maximum(0, (dur + 0.25 - t) / 0.25))
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return lp(x * env, 600) * 0.55


def kick(vol=1.0):
    t = t_axis(0.45)
    f = 48 + 70 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.16) * 0.8 * vol


def snare(vol=1.0):
    t = t_axis(0.3)
    n = bp(rng.standard_normal(len(t)), 900, 5000) * np.exp(-t / 0.07)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    return (0.45 * n + 0.35 * tone) * vol


def hat(vol=1.0, open_=False):
    t = t_axis(0.25 if open_ else 0.08)
    n = hp(rng.standard_normal(len(t)), 7000) * np.exp(-t / (0.08 if open_ else 0.022))
    return n * 0.18 * vol


def shaker(vol=1.0):
    t = t_axis(0.12)
    env = np.minimum(1, t / 0.02) * np.exp(-t / 0.04)
    return bp(rng.standard_normal(len(t)), 4000, 11000) * env * 0.16 * vol


# ---------------- arrangement helpers ----------------

class Track:
    def __init__(self, bpm, bars):
        self.bpm = bpm
        self.beat = 60.0 / bpm
        self.length = int(bars * 4 * self.beat * SR)
        self.tail = int(4 * SR)
        self.dry = np.zeros((2, self.length + self.tail))
        self.wet = np.zeros((2, self.length + self.tail))

    def add(self, sig, beat_pos, pan=0.0, send=0.3, gain=1.0, swing=0.0):
        b = beat_pos
        if swing and (b * 2) % 2 == 1:                       # delay off-beat eighths
            b += swing
        i = int(b * self.beat * SR)
        i += int(rng.normal(0, 0.003) * SR) if i > 0 else 0   # tiny human timing
        i = max(0, i)
        sig = sig * gain
        n = min(len(sig), self.dry.shape[1] - i)
        l, r = np.sqrt((1 - pan) / 2), np.sqrt((1 + pan) / 2)
        self.dry[0, i:i + n] += sig[:n] * l
        self.dry[1, i:i + n] += sig[:n] * r
        self.wet[0, i:i + n] += sig[:n] * l * send
        self.wet[1, i:i + n] += sig[:n] * r * send

    def render(self, reverb_sec=2.4, warmth=9000, crackle=0.0):
        out = self.dry.copy()
        for ch in range(2):
            t = t_axis(reverb_sec)
            ir = rng.standard_normal(len(t)) * np.exp(-t / (reverb_sec / 5))
            ir = lp(ir, 5000)
            ir[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
            w = fftconvolve(self.wet[ch], ir)[: out.shape[1]]
            out[ch] += w / np.sqrt(np.sum(ir ** 2)) * 0.6
        out = np.vstack([lp(out[0], warmth), lp(out[1], warmth)])
        if crackle:
            n = out.shape[1]
            c = np.zeros(n)
            pos = rng.integers(0, n, int(n / SR * 6))
            c[pos] = rng.uniform(-1, 1, len(pos))
            c = bp(c, 1500, 7000) * crackle + lp(rng.standard_normal(n), 3000) * crackle * 0.05
            out += c
        # wrap the tail onto the start -> seamless loop
        loop = out[:, : self.length].copy()
        loop[:, : self.tail] += out[:, self.length: self.length + self.tail]
        loop = np.tanh(loop * 1.2) / 1.2
        rms = np.sqrt(np.mean(loop ** 2))
        loop *= 10 ** (-17 / 20) / rms                      # ~ -17 dBFS RMS, calm background level
        peak = np.max(np.abs(loop))
        if peak > 0.89:
            loop *= 0.89 / peak
        return loop


# C major voicings (midi)
CH = {
    'Fmaj7': [53, 57, 60, 64], 'Em7': [52, 55, 59, 62], 'Dm7': [50, 53, 57, 60], 'Cmaj7': [48, 52, 55, 59],
    'Am7': [57, 60, 64, 67], 'G6': [55, 59, 62, 64], 'Gsus': [55, 60, 62, 67], 'Am': [57, 60, 64],
    'Fadd9': [53, 57, 60, 67], 'C': [48, 52, 55, 60], 'G': [55, 59, 62], 'Em': [52, 55, 59],
}
ROOT = {'Fmaj7': 41, 'Em7': 40, 'Dm7': 38, 'Cmaj7': 36, 'Am7': 45, 'G6': 43, 'Gsus': 43, 'Am': 45,
        'Fadd9': 41, 'C': 36, 'G': 43, 'Em': 40}
PENTA = [60, 62, 64, 67, 69, 72, 74, 76, 79, 81]


def melody_bar(chord, rhythm, start_note, rnd):
    """A gentle stepwise phrase over the chord: (beat offset, midi, length) list."""
    notes = []
    tones = set((n % 12) for n in CH[chord])
    i = min(range(len(PENTA)), key=lambda k: abs(PENTA[k] - start_note))
    for pos, ln in rhythm:
        step = rnd.choice([-1, -1, 0, 1, 1, 2, -2])
        i = int(np.clip(i + step, 2, len(PENTA) - 2))
        n = PENTA[i]
        if pos == 0 and (n % 12) not in tones:                 # land on a chord tone on the downbeat
            for d in (1, -1, 2, -2):
                j = int(np.clip(i + d, 0, len(PENTA) - 1))
                if PENTA[j] % 12 in tones:
                    i, n = j, PENTA[j]
                    break
        notes.append((pos, n, ln))
    return notes, PENTA[i]


# ---------------- songs ----------------

def garden_stroll():
    """Kalimba + marimba over a soft pad, light shaker. Calm, sunny, 86 bpm."""
    prog = ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7', 'Fmaj7', 'Em7', 'Am7', 'Gsus'] * 2
    tr = Track(86, len(prog))
    rnd = np.random.default_rng(11)
    rhythms = [[(0, 1), (1.5, 0.5), (2, 1), (3, 1)], [(0, 1.5), (1.5, 0.5), (2, 2)], [(0.5, 0.5), (1, 1), (2.5, 1.5)],
               [(0, 2), (3, 1)]]
    motif = None
    note = 72
    for bar, ch in enumerate(prog):
        b0 = bar * 4
        tr.add(pad([midi(n) for n in CH[ch]], 4 * tr.beat + 0.6), b0, 0, 0.6, 0.55)
        tr.add(bass(midi(ROOT[ch]), 2 * tr.beat), b0, 0, 0.1, 0.8)
        tr.add(bass(midi(ROOT[ch] + 7 if bar % 2 else ROOT[ch]), 2 * tr.beat), b0 + 2, 0, 0.1, 0.6)
        # kalimba arpeggio: up-down eighths
        arp = CH[ch] + [CH[ch][1] + 12]
        order = [0, 2, 1, 3, 4, 3, 2, 1]
        for k in range(8):
            tr.add(kalimba(midi(arp[order[k]] + 12)), b0 + k * 0.5, -0.35 + 0.1 * (k % 3), 0.35, 0.45 if k % 2 else 0.6)
        # marimba melody: phrase A A' B A over 4 bars
        if bar % 8 in (0, 1, 2, 3, 4, 6):
            if bar % 4 == 0 or motif is None:
                motif, note = melody_bar(ch, rhythms[(bar // 4) % len(rhythms)], note, rnd)
                notes = motif
            else:
                notes, note = melody_bar(ch, rhythms[(bar + 1) % len(rhythms)], note, rnd)
            for pos, n, ln in notes:
                tr.add(marimba(midi(n)), b0 + pos, 0.3, 0.45, 0.7)
                tr.add(marimba(midi(n + 12)), b0 + pos + 0.02, 0.35, 0.5, 0.12)
        # percussion: shaker on eighths, soft kick on 1 and the "and" of 3
        for k in range(8):
            tr.add(shaker(), b0 + k * 0.5, 0.25, 0.1, 0.55 if k % 2 else 0.85)
        tr.add(kick(0.7), b0, 0, 0.05)
        tr.add(kick(0.45), b0 + 2.5, 0, 0.05)
        if bar % 2 == 1:
            tr.add(snare(0.35), b0 + 3, -0.1, 0.4)
    return tr.render(reverb_sec=2.6, warmth=10000)


def lofi_leaves():
    """Warm electric piano, round bass, swung lo-fi drums and a little vinyl. Relaxed focus, 74 bpm."""
    prog = ['Fmaj7', 'Em7', 'Dm7', 'Cmaj7', 'Fmaj7', 'Em7', 'Am7', 'G6'] * 2
    tr = Track(74, len(prog))
    rnd = np.random.default_rng(5)
    sw = 0.08
    note = 76
    for bar, ch in enumerate(prog):
        b0 = bar * 4
        v = CH[ch]
        for pos in (0, 1.5):
            for j, n in enumerate(v):
                tr.add(epiano(midi(n), bright=0.7), b0 + pos + j * 0.012, -0.2 + 0.13 * j, 0.35, 0.42 if pos else 0.5)
        if bar % 2 == 1:
            tr.add(epiano(midi(v[-1] + 12), bright=0.5), b0 + 3, 0.3, 0.5, 0.28)
        tr.add(bass(midi(ROOT[ch]), 1.4 * tr.beat), b0, 0, 0.05, 0.95)
        tr.add(bass(midi(ROOT[ch]), 0.5 * tr.beat), b0 + 2.5, 0, 0.05, 0.6)
        tr.add(bass(midi(ROOT[ch] + 7), 0.8 * tr.beat), b0 + 3, 0, 0.05, 0.55)
        # sparse EP melody, answered every other bar
        if bar % 2 == 0:
            notes, note = melody_bar(ch, [(0.5, 0.5), (1, 0.5), (2, 1), (3.5, 0.5)], note, rnd)
            for pos, n, ln in notes:
                tr.add(epiano(midi(n + 12), bright=1.0), b0 + pos, 0.25, 0.55, 0.35, swing=sw)
        # drums
        tr.add(kick(0.9), b0)
        tr.add(kick(0.6), b0 + 2.5, swing=sw)
        tr.add(snare(0.55), b0 + 1, 0, 0.25)
        tr.add(snare(0.55), b0 + 3, 0, 0.25)
        for k in range(8):
            tr.add(hat(0.9 if k % 2 == 0 else 0.55, open_=(k == 7 and bar % 4 == 3)), b0 + k * 0.5, 0.3, 0.1, swing=sw)
    return tr.render(reverb_sec=2.0, warmth=6500, crackle=0.02)


def honey_breeze():
    """Very gentle: kalimba melody + pad only, no drums. Good for Relax Mode / long thinking. 70 bpm."""
    prog = ['Fadd9', 'C', 'Am', 'G', 'Fadd9', 'C', 'Em', 'Gsus'] * 2
    tr = Track(70, len(prog))
    rnd = np.random.default_rng(23)
    note = 74
    for bar, ch in enumerate(prog):
        b0 = bar * 4
        tr.add(pad([midi(n) for n in CH[ch]] + [midi(CH[ch][0] - 12)], 4 * tr.beat + 0.8, cutoff=1100), b0, 0, 0.7, 0.75)
        tr.add(bass(midi(ROOT[ch]), 3.5 * tr.beat), b0, 0, 0.2, 0.55)
        for k, idx in enumerate([0, 1, 2, 1]):
            tr.add(kalimba(midi(CH[ch][idx] + 12)), b0 + k, -0.4, 0.5, 0.38)
        notes, note = melody_bar(ch, [(0, 1.5), (1.5, 0.5), (2, 1)] if bar % 2 == 0 else [(0.5, 1), (2, 2)], note, rnd)
        for pos, n, ln in notes:
            tr.add(kalimba(midi(n + 12)), b0 + pos, 0.35, 0.6, 0.6)
    return tr.render(reverb_sec=3.2, warmth=9000)


def save(name, loop, d):
    from scipy.io import wavfile
    wav = os.path.join(d, name + '.wav')
    wavfile.write(wav, SR, (loop.T * 32767).astype(np.int16))
    ogg = os.path.join(d, name + '.ogg')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', '5', ogg], check=True)
    mp3 = os.path.join(d, name + '_preview.mp3')
    # preview = loop played twice so you can hear the seam
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-stream_loop', '1', '-i', wav, '-c:a', 'libmp3lame', '-q:a', '3', mp3], check=True)
    print(name, f'{loop.shape[1] / SR:.1f}s')


if __name__ == '__main__':
    d = sys.argv[1]
    os.makedirs(d, exist_ok=True)
    save('garden_stroll', garden_stroll(), d)
    save('lofi_leaves', lofi_leaves(), d)
    save('honey_breeze', honey_breeze(), d)
