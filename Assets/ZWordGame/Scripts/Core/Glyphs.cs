using UnityEngine;

namespace ZWord
{
    /// <summary>
    /// More procedural sprites for the Word Z UI: white glyph masks (tinted at use), shapes for
    /// leaves, ribbons, gems and coins, a sky gradient and a ray burst. Theme sprites override the
    /// ones that have a slot.
    /// </summary>
    public static partial class Sprites
    {
        // Convex polygon (counter-clockwise points). Approximate distance, fine for anti-aliasing.
        static float Poly(Vector2 p, Vector2[] pts)
        {
            float d = float.MinValue;
            for (int i = 0; i < pts.Length; i++)
            {
                var a = pts[i];
                var b = pts[(i + 1) % pts.Length];
                var e = (b - a).normalized;
                var n = new Vector2(e.y, -e.x); // outward for CCW
                d = Mathf.Max(d, Vector2.Dot(p - a, n));
            }
            return d;
        }

        static float RingSdf(Vector2 p, float r, float th) => Mathf.Abs(p.magnitude - r) - th;

        static Sprite Themed(Sprite themed, System.Func<Sprite> fallback) => themed != null ? themed : fallback();

        // ---------------- glyphs (white masks) ----------------

        public static Sprite HomeGlyph => Themed(Theme.Current.home, () => Make("g_home", 128, 128, p =>
        {
            float roof = Tri(p - new Vector2(0, 22), 50) - 4;
            float body = Box(p - new Vector2(0, -20), new Vector2(36, 30), 6);
            float door = Box(p - new Vector2(0, -34), new Vector2(10, 17), 4);
            return Mathf.Max(Mathf.Min(roof, body), -door);
        }));

        public static Sprite ShareGlyph => Themed(Theme.Current.share, () => Make("g_share", 128, 128, p =>
        {
            Vector2 a = new Vector2(-30, 0), b = new Vector2(28, 32), c = new Vector2(28, -32);
            float d = Mathf.Min(Circle(p - a, 16), Mathf.Min(Circle(p - b, 16), Circle(p - c, 16)));
            d = Mathf.Min(d, Seg(p, a, b, 6));
            return Mathf.Min(d, Seg(p, a, c, 6));
        }));

        public static Sprite ReplayGlyph => Themed(Theme.Current.replay, () => RotateArrow);

        public static Sprite CalendarGlyph => Make("g_calendar", 128, 128, p =>
        {
            float outline = Mathf.Abs(Box(p - new Vector2(0, -6), new Vector2(46, 42), 10)) - 6;
            float top = Box(p - new Vector2(0, 24), new Vector2(46, 12), 8);
            float rings = Mathf.Min(Box(p - new Vector2(-20, 42), new Vector2(6, 12), 3), Box(p - new Vector2(20, 42), new Vector2(6, 12), 3));
            float dots = float.MaxValue;
            for (int x = -1; x <= 1; x++)
            for (int y = 0; y < 2; y++)
                dots = Mathf.Min(dots, Box(p - new Vector2(x * 22, -6 - y * 22), new Vector2(7, 7), 2));
            return Mathf.Min(Mathf.Min(outline, top), Mathf.Min(rings, dots));
        });

        public static Sprite TrophyGlyph => Make("g_trophy", 128, 128, p =>
        {
            float cup = Box(p - new Vector2(0, 22), new Vector2(32, 28), 16);
            cup = Mathf.Min(cup, Box(p - new Vector2(0, 40), new Vector2(34, 10), 3));
            float handles = Mathf.Min(RingSdf(p - new Vector2(-34, 26), 14, 5), RingSdf(p - new Vector2(34, 26), 14, 5));
            float stem = Box(p - new Vector2(0, -16), new Vector2(8, 14), 2);
            float bas = Box(p - new Vector2(0, -38), new Vector2(28, 9), 4);
            return Mathf.Min(Mathf.Min(cup, handles), Mathf.Min(stem, bas));
        });

        public static Sprite ShopGlyph => Make("g_shop", 128, 128, p =>
        {
            float awning = Box(p - new Vector2(0, 30), new Vector2(50, 14), 6);
            float scallops = float.MaxValue;
            for (int i = -2; i <= 2; i++) scallops = Mathf.Min(scallops, Circle(p - new Vector2(i * 20, 16), 10));
            float body = Mathf.Abs(Box(p - new Vector2(0, -22), new Vector2(40, 26), 4)) - 6;
            float door = Box(p - new Vector2(14, -28), new Vector2(10, 20), 2);
            return Mathf.Min(Mathf.Min(awning, scallops), Mathf.Min(body, door));
        });

        public static Sprite ScrollGlyph => Make("g_scroll", 128, 128, p =>
        {
            float body = Box(p, new Vector2(34, 44), 8);
            float rollTop = Box(p - new Vector2(0, 44), new Vector2(44, 9), 9);
            float rollBot = Box(p - new Vector2(0, -44), new Vector2(44, 9), 9);
            float lines = Mathf.Min(Box(p - new Vector2(0, 16), new Vector2(20, 4), 2),
                Mathf.Min(Box(p - new Vector2(0, 0), new Vector2(20, 4), 2), Box(p - new Vector2(-6, -16), new Vector2(14, 4), 2)));
            return Mathf.Max(Mathf.Min(body, Mathf.Min(rollTop, rollBot)), -lines);
        });

        public static Sprite ExitGlyph => Make("g_exit", 128, 128, p =>
        {
            float door = Mathf.Abs(Box(p - new Vector2(-14, 0), new Vector2(26, 44), 6)) - 6;
            door = Mathf.Max(door, -Box(p - new Vector2(12, 0), new Vector2(8, 16), 0)); // gap for the arrow
            float shaft = Seg(p, new Vector2(-4, 0), new Vector2(34, 0), 7);
            float head = Tri(new Vector2(-(p.y), p.x - 40), 15) - 2;
            return Mathf.Min(door, Mathf.Min(shaft, head));
        });

        public static Sprite BulbGlyph => Make("g_bulb", 128, 128, p =>
        {
            float glass = Circle(p - new Vector2(0, 14), 32);
            float neck = Box(p - new Vector2(0, -22), new Vector2(16, 12), 4);
            float base1 = Box(p - new Vector2(0, -40), new Vector2(13, 5), 3);
            return Mathf.Min(glass, Mathf.Min(neck, base1));
        });

        public static Sprite LockGlyph => Themed(Theme.Current.lockIcon, () => Make("g_lock", 128, 128, p =>
        {
            float shackle = Mathf.Max(RingSdf(p - new Vector2(0, 14), 22, 7), -(p.y - 14));
            shackle = Mathf.Min(shackle, Box(p - new Vector2(-22, 6), new Vector2(7, 9), 0));
            shackle = Mathf.Min(shackle, Box(p - new Vector2(22, 6), new Vector2(7, 9), 0));
            float body = Box(p - new Vector2(0, -22), new Vector2(36, 28), 8);
            float hole = Mathf.Min(Circle(p - new Vector2(0, -16), 8), Box(p - new Vector2(0, -28), new Vector2(4, 9), 2));
            return Mathf.Min(shackle, Mathf.Max(body, -hole));
        }));

        public static Sprite ShuffleGlyph => Make("g_shuffle", 128, 128, p =>
        {
            float a = Mathf.Min(Seg(p, new Vector2(-44, -26), new Vector2(-14, -26), 6), Seg(p, new Vector2(-14, -26), new Vector2(14, 26), 6));
            a = Mathf.Min(a, Seg(p, new Vector2(14, 26), new Vector2(30, 26), 6));
            float b = Mathf.Min(Seg(p, new Vector2(-44, 26), new Vector2(-14, 26), 6), Seg(p, new Vector2(-14, 26), new Vector2(14, -26), 6));
            b = Mathf.Min(b, Seg(p, new Vector2(14, -26), new Vector2(30, -26), 6));
            float h1 = Tri(new Vector2(-(p.y - 26), p.x - 36), 14) - 2;
            float h2 = Tri(new Vector2(-(p.y + 26), p.x - 36), 14) - 2;
            return Mathf.Min(Mathf.Min(a, b), Mathf.Min(h1, h2));
        });

        public static Sprite AvatarGlyph => Make("g_avatar", 128, 128, p =>
        {
            float head = Circle(p - new Vector2(0, 18), 24);
            float body = Mathf.Max(Circle(p - new Vector2(0, -50), 44), -(p.y + 50));
            return Mathf.Min(head, body);
        });

        public static Sprite TargetGlyph => Make("g_target", 128, 128, p =>
            Mathf.Min(RingSdf(p, 40, 7), Mathf.Min(RingSdf(p, 20, 6), Circle(p, 6))));

        public static Sprite ChevronRight => Make("g_chev", 128, 128,
            p => Mathf.Min(Seg(p, new Vector2(-14, 36), new Vector2(18, 0), 11), Seg(p, new Vector2(18, 0), new Vector2(-14, -36), 11)));

        public static Sprite Check => Make("g_check", 128, 128,
            p => Mathf.Min(Seg(p, new Vector2(-34, 2), new Vector2(-10, -24), 11), Seg(p, new Vector2(-10, -24), new Vector2(36, 28), 11)));

        public static Sprite Cross => Make("g_cross", 128, 128,
            p => Mathf.Min(Seg(p, new Vector2(-30, -30), new Vector2(30, 30), 11), Seg(p, new Vector2(-30, 30), new Vector2(30, -30), 11)));

        public static Sprite Pencil => Make("g_pencil", 128, 128, p =>
        {
            var q = Rot(p, -45);
            float body = Box(q - new Vector2(6, 0), new Vector2(34, 11), 2);
            float tip = Tri(new Vector2(q.y, -(q.x + 40)), 11);
            return Mathf.Min(body, tip);
        });

        public static Sprite AdGlyph => Make("g_ad", 128, 128, p =>
        {
            float screen = Mathf.Abs(Box(p, new Vector2(46, 34), 8)) - 6;
            float play = Tri(new Vector2(-p.y, p.x - 3), 16);
            return Mathf.Min(screen, play);
        });

        // ---------------- shapes ----------------

        /// <summary>Leaf pointing up (vesica). Tint it green.</summary>
        public static Sprite Leaf => Themed(Theme.Current.leaf, () => Make("leaf", 96, 160, p =>
            Mathf.Max(Circle(p - new Vector2(-34, 0), 70), Circle(p - new Vector2(34, 0), 70))));

        public static Sprite LeafVein => Make("leafvein", 96, 160, p =>
            Mathf.Max(Seg(p, new Vector2(0, -66), new Vector2(0, 60), 2.2f), Mathf.Max(Circle(p - new Vector2(-34, 0), 66), Circle(p - new Vector2(34, 0), 66))));

        /// <summary>Ribbon tail with a notch on the outer (left) side; mirror it for the right tail.</summary>
        public static Sprite RibbonTail => Make("ribbontail", 128, 96, p =>
        {
            float rect = Box(p, new Vector2(60, 38), 4);
            float notch = Poly(p, new[] { new Vector2(-64, 42), new Vector2(-64, -42), new Vector2(-30, 0) });
            return Mathf.Max(rect, -notch);
        });

        static readonly Vector2[] GemPts =
        {
            new Vector2(0, -50), new Vector2(54, 10), new Vector2(32, 40), new Vector2(-32, 40), new Vector2(-54, 10)
        };

        public static Sprite GemShape => Make("gem", 128, 128, p => Poly(p, GemPts));

        public static Sprite GemTopFacet => Make("gemtop", 128, 128, p =>
            Mathf.Max(Poly(p, GemPts), -(p.y - 10)));

        public static Sprite GemMidFacet => Make("gemmid", 128, 128, p =>
            Poly(p, new[] { new Vector2(0, -44), new Vector2(18, 10), new Vector2(-18, 10) }));

        /// <summary>Sun-ray burst for celebration screens.</summary>
        public static Sprite Rays => Make("rays", 256, 256, p =>
        {
            float a = Mathf.Atan2(p.y, p.x);
            float k = Mathf.Abs(Mathf.Sin(a * 8f));          // 16 rays
            float ray = (0.25f - k) * p.magnitude * 0.6f;    // distance-ish to ray edge
            float fade = p.magnitude - 126f;
            return Mathf.Max(-ray, fade);
        });

        public static Sprite SpeakerGlyph => Make("g_speaker", 128, 128, p =>
        {
            float body = Box(p - new Vector2(-30, 0), new Vector2(14, 18), 3);
            float cone = Poly(p, new[] { new Vector2(-22, -16), new Vector2(8, -42), new Vector2(8, 42), new Vector2(-22, 16) });
            float w1 = Mathf.Max(RingSdf(p - new Vector2(4, 0), 26, 5), -(p.x - 20));
            float w2 = Mathf.Max(RingSdf(p - new Vector2(4, 0), 44, 5), -(p.x - 30));
            return Mathf.Min(Mathf.Min(body, cone), Mathf.Min(w1, w2));
        });

        public static Sprite NoteGlyph => Make("g_note", 128, 128, p =>
        {
            float head = Circle(p - new Vector2(-14, -30), 20);
            float stem = Box(p - new Vector2(2, 8), new Vector2(5, 40), 2);
            float flag = Seg(p, new Vector2(2, 46), new Vector2(34, 22), 7);
            return Mathf.Min(head, Mathf.Min(stem, flag));
        });

        public static Sprite PhoneGlyph => Make("g_phone", 128, 128, p =>
        {
            float body = Mathf.Abs(Box(p, new Vector2(24, 44), 8)) - 6;
            float waves = Mathf.Min(Seg(p, new Vector2(-40, -16), new Vector2(-40, 16), 5), Seg(p, new Vector2(40, -16), new Vector2(40, 16), 5));
            waves = Mathf.Min(waves, Mathf.Min(Seg(p, new Vector2(-52, -8), new Vector2(-52, 8), 4), Seg(p, new Vector2(52, -8), new Vector2(52, 8), 4)));
            return Mathf.Min(body, waves);
        });

        public static Sprite GlobeGlyph => Make("g_globe", 128, 128, p =>
        {
            float ring = RingSdf(p, 44, 6);
            float meridian = Mathf.Max(Mathf.Abs(new Vector2(p.x * 2.2f, p.y).magnitude - 44) - 6, Circle(p, 44));
            float eq = Mathf.Max(Box(p, new Vector2(44, 4), 0), Circle(p, 44));
            float lat = Mathf.Max(Mathf.Min(Box(p - new Vector2(0, 22), new Vector2(40, 3), 0), Box(p + new Vector2(0, 22), new Vector2(40, 3), 0)), Circle(p, 44));
            return Mathf.Min(Mathf.Min(ring, meridian), Mathf.Min(eq, lat));
        });

        /// <summary>Puffy cloud (white mask).</summary>
        public static Sprite Cloud => Make("cloud", 256, 128, p =>
            Mathf.Min(Mathf.Min(Circle(p - new Vector2(-62, -18), 40), Circle(p - new Vector2(-12, 10), 56)),
                Mathf.Min(Circle(p - new Vector2(52, -8), 46), Box(p - new Vector2(0, -36), new Vector2(100, 22), 22))));

        /// <summary>Simple bird (two wings), white mask.</summary>
        public static Sprite Bird => Make("bird", 128, 64, p =>
            Mathf.Min(Seg(p, new Vector2(-50, 14), new Vector2(0, -8), 6), Seg(p, new Vector2(0, -8), new Vector2(50, 14), 6)));

        /// <summary>Raindrop streak.</summary>
        public static Sprite Streak => Make("streak", 32, 128, p => Seg(p, new Vector2(0, -56), new Vector2(0, 56), 5));

        static Sprite sky;

        /// <summary>Vertical sky gradient (warm sunset), used behind the procedural home scene.</summary>
        public static Sprite SkyGradient
        {
            get
            {
                if (sky != null && sky.texture != null) return sky;
                const int h = 256;
                var tex = new Texture2D(4, h, TextureFormat.RGBA32, false) { wrapMode = TextureWrapMode.Clamp, name = "sky" };
                var top = Palette.Hex("6FB7E8");
                var mid = Palette.Hex("F9D59B");
                var bottom = Palette.Hex("F0A35E");
                for (int y = 0; y < h; y++)
                {
                    float t = y / (h - 1f);
                    var c = t > 0.45f ? Color.Lerp(mid, top, (t - 0.45f) / 0.55f) : Color.Lerp(bottom, mid, t / 0.45f);
                    for (int x = 0; x < 4; x++) tex.SetPixel(x, y, c);
                }
                tex.Apply(false, true);
                sky = Sprite.Create(tex, new Rect(0, 0, 4, h), new Vector2(0.5f, 0.5f), 100f);
                return sky;
            }
        }
    }
}
