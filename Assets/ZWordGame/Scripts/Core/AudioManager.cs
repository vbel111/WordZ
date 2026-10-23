using System.Collections;
using UnityEngine;

namespace ZWord
{
    public enum MusicContext { None, Home, Game }

    /// <summary>
    /// Music (two crossfading sources, home/game playlists) and sound effects.
    /// Clips come from the Theme; anything missing falls back to a synthesized sound.
    /// Letter selection plays a pentatonic scale so dragging a word sounds musical.
    /// </summary>
    public class AudioManager : MonoBehaviour
    {
        static AudioManager I;

        AudioSource musicA, musicB, sfx, letters;
        bool usingA = true;
        MusicContext context = MusicContext.None;
        int playlistIndex = -1;
        Coroutine fadeCo;
        float musicDuck = 1f;

        // Synth fallbacks
        AudioClip synthBlip, synthClick, synthSuccess, synthError, synthWin, synthLose, synthStar, synthBooster, synthTick, synthBonus;
        const int Rate = 44100;

        // C major pentatonic, in semitones, two octaves
        static readonly int[] Pentatonic = { 0, 2, 4, 7, 9, 12, 14, 16, 19, 21, 24 };

        public static void Init(GameObject host)
        {
            if (I != null) return;
            I = host.AddComponent<AudioManager>();
            I.Setup();
        }

        void Setup()
        {
            var theme = Theme.Current;
            musicA = MakeSource("MusicA", theme.musicGroup, true);
            musicB = MakeSource("MusicB", theme.musicGroup, true);
            sfx = MakeSource("Sfx", theme.sfxGroup, false);
            letters = MakeSource("Letters", theme.sfxGroup, false);

            synthBlip = Tone("blip", new[] { 523.25f }, 0.12f, 0.35f);
            synthClick = Tone("click", new[] { 660f }, 0.05f, 0.25f);
            synthSuccess = Arp("success", new[] { 523f, 659f, 784f, 1046f }, 0.07f, 0.35f);
            synthError = Tone("error", new[] { 140f, 147f }, 0.22f, 0.3f, true);
            synthWin = Arp("win", new[] { 523f, 659f, 784f, 659f, 784f, 1046f }, 0.11f, 0.4f);
            synthLose = Arp("lose", new[] { 392f, 330f, 262f }, 0.18f, 0.35f);
            synthStar = Arp("star", new[] { 1046f, 1318f }, 0.06f, 0.3f);
            synthBooster = Arp("booster", new[] { 392f, 523f, 659f, 784f }, 0.05f, 0.3f);
            synthTick = Tone("tick", new[] { 1760f }, 0.035f, 0.35f);
            synthBonus = Arp("bonus", new[] { 784f, 988f, 1175f, 1568f }, 0.045f, 0.3f);
            ApplyVolumes();
        }

        AudioSource MakeSource(string name, UnityEngine.Audio.AudioMixerGroup group, bool loop)
        {
            var go = new GameObject(name);
            go.transform.SetParent(transform, false);
            var s = go.AddComponent<AudioSource>();
            s.playOnAwake = false;
            s.loop = loop;
            s.spatialBlend = 0f;
            s.outputAudioMixerGroup = group;
            return s;
        }

        // ---------------- Volumes ----------------

        public static void ApplyVolumes()
        {
            if (I == null) return;
            float sv = Save.SfxVolume;
            I.sfx.volume = sv;
            I.letters.volume = sv * 0.8f;
            var active = I.usingA ? I.musicA : I.musicB;
            if (I.fadeCo == null) active.volume = Save.MusicVolume * I.musicDuck;
        }

        /// <summary>Temporarily lower the music (e.g. under the win fanfare).</summary>
        public static void Duck(float amount, float seconds)
        {
            if (I == null) return;
            I.StartCoroutine(I.DuckCo(amount, seconds));
        }

        IEnumerator DuckCo(float amount, float seconds)
        {
            musicDuck = amount;
            ApplyVolumes();
            yield return new WaitForSecondsRealtime(seconds);
            musicDuck = 1f;
            ApplyVolumes();
        }

        // ---------------- Music ----------------

        public static void PlayMusic(MusicContext ctx, bool nextTrack = false)
        {
            if (I == null) return;
            if (ctx == I.context && !nextTrack) return;
            var list = ctx == MusicContext.Home ? Theme.Current.homeMusic
                     : ctx == MusicContext.Game ? Theme.Current.gameMusic : null;
            if (ctx != I.context) I.playlistIndex = -1;
            I.context = ctx;

            AudioClip clip = null;
            if (list != null && list.Length > 0)
            {
                // Next track in a shuffled-ish rotation, never the same twice in a row
                int idx = list.Length == 1 ? 0 : (I.playlistIndex + 1 + Random.Range(0, list.Length - 1)) % list.Length;
                I.playlistIndex = idx;
                clip = list[idx];
            }
            I.CrossfadeTo(clip, 0.8f);
        }

        void CrossfadeTo(AudioClip clip, float seconds)
        {
            var from = usingA ? musicA : musicB;
            var to = usingA ? musicB : musicA;
            if (clip != null && from.clip == clip && from.isPlaying) return;
            usingA = !usingA;
            if (fadeCo != null) StopCoroutine(fadeCo);
            fadeCo = StartCoroutine(Fade(from, to, clip, seconds));
        }

        IEnumerator Fade(AudioSource from, AudioSource to, AudioClip clip, float seconds)
        {
            float startFrom = from.volume;
            if (clip != null)
            {
                to.clip = clip;
                to.volume = 0f;
                to.Play();
            }
            float t = 0f;
            while (t < seconds)
            {
                t += Time.unscaledDeltaTime;
                float k = Mathf.Clamp01(t / seconds);
                float target = Save.MusicVolume * musicDuck;
                from.volume = Mathf.Lerp(startFrom, 0f, k);
                if (clip != null) to.volume = Mathf.Lerp(0f, target, k);
                yield return null;
            }
            from.Stop();
            from.clip = null;
            fadeCo = null;
            ApplyVolumes();
        }

        // ---------------- SFX ----------------

        void Play(AudioClip themed, AudioClip fallback, float volume = 1f, float pitch = 1f)
        {
            var clip = themed != null ? themed : fallback;
            if (clip == null || Save.SfxVolume <= 0.001f) return;
            sfx.pitch = pitch;
            sfx.PlayOneShot(clip, volume);
        }

        /// <summary>Tile selected: walk up a pentatonic scale.</summary>
        public static void Letter(int index)
        {
            if (I == null || Save.SfxVolume <= 0.001f) return;
            var clip = Theme.Current.letter != null ? Theme.Current.letter : I.synthBlip;
            int step = Pentatonic[Mathf.Clamp(index, 0, Pentatonic.Length - 1)];
            I.letters.pitch = Mathf.Pow(2f, step / 12f);
            I.letters.PlayOneShot(clip, 0.9f);
        }

        public static void Click() => I?.Play(Theme.Current.click, I.synthClick, 0.8f);
        public static void Success() => I?.Play(Theme.Current.wordFound, I.synthSuccess, 0.9f);
        public static void Error() => I?.Play(Theme.Current.wrong, I.synthError, 0.8f);
        public static void Booster() => I?.Play(Theme.Current.booster, I.synthBooster, 0.8f);
        /// <summary>Clock tick for the last seconds of a level.</summary>
        public static void Tick(bool urgent) => I?.Play(null, I.synthTick, urgent ? 0.9f : 0.6f, urgent ? 1.25f : 1f);
        public static void Bonus() => I?.Play(null, I.synthBonus, 0.8f);
        public static void StarLost() => I?.Play(null, I.synthError, 0.5f, 1.6f);
        public static void Star(int index) => I?.Play(Theme.Current.starChime, I.synthStar, 0.9f, 1f + index * 0.12f);

        public static void Win()
        {
            if (I == null) return;
            Duck(0.25f, 2.5f);
            I.Play(Theme.Current.win, I.synthWin, 0.9f);
        }

        public static void Lose()
        {
            if (I == null) return;
            Duck(0.3f, 1.5f);
            I.Play(Theme.Current.lose, I.synthLose, 0.9f);
        }

        // ---------------- Synth ----------------

        static AudioClip Tone(string name, float[] freqs, float dur, float vol, bool square = false)
        {
            int n = (int)(Rate * dur);
            var data = new float[n];
            for (int i = 0; i < n; i++)
            {
                float t = (float)i / Rate;
                float env = Mathf.Min(1f, i / 200f) * Mathf.Pow(1f - (float)i / n, 2f);
                float s = 0;
                foreach (var f in freqs)
                {
                    float v = Mathf.Sin(2 * Mathf.PI * f * t) + 0.25f * Mathf.Sin(4 * Mathf.PI * f * t);
                    s += square ? Mathf.Sign(v) * 0.5f : v;
                }
                data[i] = s / freqs.Length * env * vol;
            }
            var clip = AudioClip.Create(name, n, 1, Rate, false);
            clip.SetData(data, 0);
            return clip;
        }

        static AudioClip Arp(string name, float[] notes, float step, float vol)
        {
            int per = (int)(Rate * step);
            int tail = (int)(Rate * 0.25f);
            int n = per * notes.Length + tail;
            var data = new float[n];
            for (int k = 0; k < notes.Length; k++)
            {
                int len = per + tail;
                for (int i = 0; i < len && k * per + i < n; i++)
                {
                    float t = (float)i / Rate;
                    float env = Mathf.Min(1f, i / 150f) * Mathf.Exp(-t * 9f);
                    float v = Mathf.Sin(2 * Mathf.PI * notes[k] * t) + 0.3f * Mathf.Sin(4 * Mathf.PI * notes[k] * t);
                    data[k * per + i] += v * env * vol * 0.6f;
                }
            }
            var clip = AudioClip.Create(name, n, 1, Rate, false);
            clip.SetData(data, 0);
            return clip;
        }
    }
}
