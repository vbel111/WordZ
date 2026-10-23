using System.Collections.Generic;
using UnityEngine;

namespace ZWord
{
    /// <summary>
    /// Generates every sprite the game needs at runtime from signed distance functions,
    /// so the project needs no art assets. Results are cached.
    /// </summary>
    public static partial class Sprites
    {
        static readonly Dictionary<string, Sprite> cache = new Dictionary<string, Sprite>();

        delegate float Sdf(Vector2 p);

        // With "Enter Play Mode Options" (no domain reload) static caches survive between play sessions while
        // Unity destroys the textures/sprites made at runtime -> images fell back to plain blocky rectangles.
        // Clear everything at the start of each session, and never hand out a destroyed sprite.
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ResetStatics()
        {
            cache.Clear();
            wood = null;
            vignette = null;
            sky = null;
        }

        static Sprite Make(string key, int w, int h, Sdf sdf, Vector4 border = default)
        {
            if (cache.TryGetValue(key, out var cached) && cached != null && cached.texture != null) return cached;
            var tex = new Texture2D(w, h, TextureFormat.RGBA32, false)
            {
                wrapMode = TextureWrapMode.Clamp,
                filterMode = FilterMode.Bilinear,
                name = key
            };
            var px = new Color32[w * h];
            for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
            {
                var p = new Vector2(x + 0.5f - w * 0.5f, y + 0.5f - h * 0.5f);
                float a = Mathf.Clamp01(0.5f - sdf(p));
                px[y * w + x] = new Color32(255, 255, 255, (byte)(a * 255f));
            }
            tex.SetPixels32(px);
            tex.Apply(false, true);
            var s = Sprite.Create(tex, new Rect(0, 0, w, h), new Vector2(0.5f, 0.5f), 100f, 0, SpriteMeshType.FullRect, border);
            s.name = key;
            cache[key] = s;
            return s;
        }

        // ---------- SDF primitives ----------
        static float Box(Vector2 p, Vector2 b, float r)
        {
            var q = new Vector2(Mathf.Abs(p.x) - b.x + r, Mathf.Abs(p.y) - b.y + r);
            return Vector2.Max(q, Vector2.zero).magnitude + Mathf.Min(Mathf.Max(q.x, q.y), 0f) - r;
        }

        static float Circle(Vector2 p, float r) => p.magnitude - r;

        static float Seg(Vector2 p, Vector2 a, Vector2 b, float th)
        {
            var pa = p - a; var ba = b - a;
            float h = Mathf.Clamp01(Vector2.Dot(pa, ba) / Vector2.Dot(ba, ba));
            return (pa - ba * h).magnitude - th;
        }

        // Flat-top hexagon, r = inradius (half height)
        static float HexSdf(Vector2 p, float r)
        {
            const float kx = -0.866025404f, ky = 0.5f, kz = 0.577350269f;
            p = new Vector2(Mathf.Abs(p.x), Mathf.Abs(p.y)); // flat top/bottom edges
            float d = Mathf.Min(kx * p.x + ky * p.y, 0f);
            p -= 2f * d * new Vector2(kx, ky);
            p -= new Vector2(Mathf.Clamp(p.x, -kz * r, kz * r), r);
            return p.magnitude * Mathf.Sign(p.y);
        }

        static float Star5(Vector2 p, float r, float rf)
        {
            var k1 = new Vector2(0.809016994375f, -0.587785252292f);
            var k2 = new Vector2(-k1.x, k1.y);
            p.x = Mathf.Abs(p.x);
            p -= 2f * Mathf.Max(Vector2.Dot(k1, p), 0f) * k1;
            p -= 2f * Mathf.Max(Vector2.Dot(k2, p), 0f) * k2;
            p.x = Mathf.Abs(p.x);
            p.y -= r;
            var ba = rf * new Vector2(-k1.y, k1.x) - new Vector2(0, 1);
            float h = Mathf.Clamp(Vector2.Dot(p, ba) / Vector2.Dot(ba, ba), 0f, r);
            return (p - ba * h).magnitude * Mathf.Sign(p.y * ba.x - p.x * ba.y);
        }

        static float Tri(Vector2 p, float r)
        {
            const float k = 1.7320508f;
            p.x = Mathf.Abs(p.x) - r;
            p.y = p.y + r / k;
            if (p.x + k * p.y > 0f) p = new Vector2(p.x - k * p.y, -k * p.x - p.y) / 2f;
            p.x -= Mathf.Clamp(p.x, -2f * r, 0f);
            return -p.magnitude * Mathf.Sign(p.y);
        }

        static Vector2 Rot(Vector2 p, float deg)
        {
            float a = deg * Mathf.Deg2Rad, c = Mathf.Cos(a), s = Mathf.Sin(a);
            return new Vector2(c * p.x - s * p.y, s * p.x + c * p.y);
        }

        // ---------- Public sprites ----------

        /// <summary>9-sliced rounded rectangle (corner radius 48 at multiplier 1).</summary>
        /// <summary>Coin icon from the theme, or the star when none is set.</summary>
        public static Sprite Coin => Theme.Current.coin != null ? Theme.Current.coin : Star;

        public static Sprite Rounded => Make("rounded", 128, 128, p => Box(p, new Vector2(63, 63), 48), new Vector4(50, 50, 50, 50));

        public static Sprite Hexagon => Theme.Current.hexTile != null ? Theme.Current.hexTile : Make("hex", 192, 168, p => HexSdf(p, 80f - 14f) - 14f);

        public static Sprite CircleSprite => Make("circle", 128, 128, p => Circle(p, 62));

        public static Sprite Ring => Make("ring", 128, 128, p => Mathf.Abs(Circle(p, 56)) - 6);

        public static Sprite Star => Theme.Current.star != null ? Theme.Current.star : Make("star", 128, 128, p => Star5(p + new Vector2(0, 6), 56 - 8, 0.5f) - 8);

        public static Sprite Play => Make("play", 128, 128, p => Tri(new Vector2(-p.y, p.x - 6), 36) - 10);

        public static Sprite Pause => Theme.Current.pause != null ? Theme.Current.pause : Make("pause", 128, 128,
            p => Mathf.Min(Box(p - new Vector2(-20, 0), new Vector2(12, 40), 6), Box(p - new Vector2(20, 0), new Vector2(12, 40), 6)));

        public static Sprite Back => Theme.Current.back != null ? Theme.Current.back : Make("back", 128, 128,
            p => Mathf.Min(Seg(p, new Vector2(18, 42), new Vector2(-22, 0), 14), Seg(p, new Vector2(-22, 0), new Vector2(18, -42), 14)));

        public static Sprite Gear => Theme.Current.settings != null ? Theme.Current.settings : Make("gear", 128, 128, p =>
        {
            float d = Circle(p, 38);
            for (int i = 0; i < 8; i++)
            {
                var q = Rot(p, -i * 45f);
                d = Mathf.Min(d, Box(q - new Vector2(0, 46), new Vector2(11, 14), 4));
            }
            return Mathf.Max(d, -Circle(p, 16));
        });

        public static Sprite Clock => Theme.Current.clock != null ? Theme.Current.clock : Make("clock", 128, 128, p =>
        {
            float d = Mathf.Abs(Circle(p, 48)) - 9;
            d = Mathf.Min(d, Seg(p, Vector2.zero, new Vector2(0, 30), 7));
            d = Mathf.Min(d, Seg(p, Vector2.zero, new Vector2(22, 0), 7));
            return d;
        });

        public static Sprite Magnifier => Theme.Current.magnifier != null ? Theme.Current.magnifier : Make("magnifier", 128, 128, p =>
        {
            float d = Mathf.Abs(Circle(p - new Vector2(-10, 12), 32)) - 9;
            return Mathf.Min(d, Seg(p, new Vector2(14, -14), new Vector2(44, -44), 13));
        });

        public static Sprite RotateArrow => Theme.Current.rotate != null ? Theme.Current.rotate : Make("rotate", 128, 128, p =>
        {
            float ring = Mathf.Abs(Circle(p, 36)) - 9;
            if (p.x > 0 && p.y > 0) ring = Mathf.Max(ring, Mathf.Min(p.x, p.y));
            // Arrow head at the end of the arc (top), pointing right
            var q = p - new Vector2(8, 36);
            float head = Tri(new Vector2(-q.y, q.x), 18) - 3;
            return Mathf.Min(ring, head);
        });

        public static Sprite Letters => Make("abc", 128, 128, p =>
        {
            float d = Circle(p - new Vector2(-20, 18), 26);
            d = Mathf.Min(d, Circle(p - new Vector2(22, 18), 26));
            d = Mathf.Min(d, Circle(p - new Vector2(0, -22), 26));
            return d;
        });

        public static Sprite Soft => Make("soft", 64, 64, p => (p.magnitude - 4f) / 28f - 0.5f);

        static Sprite wood;
        /// <summary>Procedural wood planks texture.</summary>
        public static Sprite Wood
        {
            get
            {
                if (wood != null && wood.texture != null) return wood;
                const int w = 256, h = 512;
                var tex = new Texture2D(w, h, TextureFormat.RGBA32, false) { wrapMode = TextureWrapMode.Clamp, name = "wood" };
                var px = new Color32[w * h];
                var light = new Color(0.78f, 0.47f, 0.22f);
                var dark = new Color(0.56f, 0.31f, 0.13f);
                for (int y = 0; y < h; y++)
                {
                    int plank = y / 96;
                    float plankShade = 0.92f + 0.08f * Mathf.PerlinNoise(plank * 3.1f, 0.5f);
                    for (int x = 0; x < w; x++)
                    {
                        float n = Mathf.PerlinNoise(x * 0.012f + plank * 10f, y * 0.06f);
                        float grain = Mathf.Sin((y * 0.11f + n * 7f)) * 0.5f + 0.5f;
                        float fine = Mathf.PerlinNoise(x * 0.2f, y * 0.9f) * 0.15f;
                        var c = Color.Lerp(dark, light, grain * 0.7f + fine + 0.1f) * plankShade;
                        int iy = y % 96;
                        if (iy < 3) c *= 0.55f;
                        else if (iy < 6) c *= 1.08f;
                        c.a = 1f;
                        px[y * w + x] = c;
                    }
                }
                tex.SetPixels32(px);
                tex.Apply(false, true);
                wood = Sprite.Create(tex, new Rect(0, 0, w, h), new Vector2(0.5f, 0.5f), 100f);
                return wood;
            }
        }

        static Sprite vignette;
        public static Sprite Vignette
        {
            get
            {
                if (vignette != null && vignette.texture != null) return vignette;
                const int s = 128;
                var tex = new Texture2D(s, s, TextureFormat.RGBA32, false) { wrapMode = TextureWrapMode.Clamp, name = "vignette" };
                var px = new Color32[s * s];
                for (int y = 0; y < s; y++)
                for (int x = 0; x < s; x++)
                {
                    float dx = (x + 0.5f) / s * 2f - 1f, dy = (y + 0.5f) / s * 2f - 1f;
                    float d = Mathf.Sqrt(dx * dx * 0.9f + dy * dy * 0.6f);
                    float a = Mathf.SmoothStep(0f, 1f, Mathf.InverseLerp(0.45f, 1.25f, d));
                    px[y * s + x] = new Color32(255, 255, 255, (byte)(a * 255));
                }
                tex.SetPixels32(px);
                tex.Apply(false, true);
                vignette = Sprite.Create(tex, new Rect(0, 0, s, s), new Vector2(0.5f, 0.5f), 100f);
                return vignette;
            }
        }
    }
}
