using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    public enum AmbienceKind { Leaves, Fireflies, Bubbles, Twinkle, Notes, Hearts, Sparkles, Rain, Steam, Letters, Clouds, Birds, Confetti }

    /// <summary>
    /// Lightweight UI particle system that makes backgrounds feel alive: falling leaves, rising bubbles,
    /// twinkling stars, drifting clouds, birds... Works inside any RectTransform (spawns across its
    /// visible area). No Unity ParticleSystem needed, so it renders correctly inside the UI.
    /// </summary>
    public class Ambience : MonoBehaviour
    {
        class P
        {
            public RectTransform Rt;
            public Graphic G;
            public Vector2 Pos, Vel;
            public float Age, Life, Size, Spin, Phase, Alpha;
        }

        public AmbienceKind Kind;
        public int MaxCount = 24;
        public float Rate = 3f;              // spawns per second
        public Color Tint = Color.white;
        /// <summary>Optional: returns the visible rect in this transform's local space (for scrolling content).</summary>
        public System.Func<Rect> VisibleArea;

        readonly List<P> live = new List<P>();
        RectTransform rt;
        float spawnAcc;

        public static Ambience Add(RectTransform parent, AmbienceKind kind, Color tint, int max = 24, float rate = 3f)
        {
            var layer = UI.Rect("Ambience_" + kind, parent).Stretch();
            var a = layer.gameObject.AddComponent<Ambience>();
            a.Kind = kind;
            a.Tint = tint;
            a.MaxCount = max;
            a.Rate = rate;
            return a;
        }

        /// <summary>Picks a fitting effect for a category map.</summary>
        public static (AmbienceKind kind, Color tint) ForCategory(string name)
        {
            switch (name)
            {
                case "NATURE": case "ANIMALS": case "FRUIT & VEG": return (AmbienceKind.Leaves, Color.white);
                case "ELECTRONIC": return (AmbienceKind.Fireflies, Palette.Hex("6FF2FF"));
                case "MUSIC": return (AmbienceKind.Notes, Color.white);
                case "BODY": return (AmbienceKind.Hearts, Color.white);
                case "CLOTHES": return (AmbienceKind.Sparkles, Palette.Hex("FFC3E1"));
                case "WEATHER": return (AmbienceKind.Rain, Palette.Hex("D6F1FF"));
                case "SPACE": case "CINEMA": return (AmbienceKind.Twinkle, Palette.Hex("FFF3B0"));
                case "OCEAN": case "COUNTRIES": return (AmbienceKind.Bubbles, Color.white);
                case "KITCHEN": case "MEALS": return (AmbienceKind.Steam, Color.white);
                case "SCHOOL": return (AmbienceKind.Letters, Color.white);
                case "CITY": case "JOBS": case "TRAVEL": return (AmbienceKind.Birds, Palette.Hex("3B2414"));
                default: return (AmbienceKind.Fireflies, Palette.Hex("FFE58A"));
            }
        }

        void Awake() => rt = (RectTransform)transform;

        Rect Area()
        {
            if (VisibleArea != null) return VisibleArea();
            var r = rt.rect;
            return r.width > 1 ? r : new Rect(-540, -960, 1080, 1920);
        }

        void Update()
        {
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            spawnAcc += dt * Rate;
            while (spawnAcc >= 1f && live.Count < MaxCount) { spawnAcc -= 1f; Spawn(); }
            if (spawnAcc > 1f) spawnAcc = 1f;

            var area = Area();
            for (int i = live.Count - 1; i >= 0; i--)
            {
                var p = live[i];
                p.Age += dt;
                float k = p.Age / p.Life;
                if (k >= 1f || p.Rt == null)
                {
                    if (p.Rt != null) Destroy(p.Rt.gameObject);
                    live.RemoveAt(i);
                    continue;
                }
                Step(p, dt, k, area);
            }
        }

        // ---------------- spawning ----------------

        void Spawn()
        {
            var a = Area();
            var p = new P { Phase = Random.value * 10f };
            Sprite sprite;
            switch (Kind)
            {
                case AmbienceKind.Leaves:
                    sprite = Sprites.Leaf;
                    p.Size = Random.Range(34f, 58f);
                    p.Pos = new Vector2(Random.Range(a.xMin, a.xMax), a.yMax + 40);
                    p.Vel = new Vector2(Random.Range(-30f, 30f), Random.Range(-90f, -55f));
                    p.Life = (a.height + 80) / -p.Vel.y;
                    p.Spin = Random.Range(-90f, 90f);
                    break;
                case AmbienceKind.Bubbles:
                    sprite = Sprites.Ring;
                    p.Size = Random.Range(18f, 46f);
                    p.Pos = new Vector2(Random.Range(a.xMin, a.xMax), a.yMin - 30);
                    p.Vel = new Vector2(0, Random.Range(70f, 140f));
                    p.Life = (a.height + 60) / p.Vel.y;
                    break;
                case AmbienceKind.Notes:
                case AmbienceKind.Hearts:
                case AmbienceKind.Steam:
                case AmbienceKind.Letters:
                    sprite = Kind == AmbienceKind.Hearts ? HeartSprite() : Kind == AmbienceKind.Notes ? NoteSprite() : Kind == AmbienceKind.Steam ? Sprites.Soft : null;
                    p.Size = Kind == AmbienceKind.Steam ? Random.Range(60f, 120f) : Random.Range(36f, 64f);
                    p.Pos = new Vector2(Random.Range(a.xMin, a.xMax), Random.Range(a.yMin, a.yMin + a.height * 0.6f));
                    p.Vel = new Vector2(Random.Range(-15f, 15f), Random.Range(40f, 80f));
                    p.Life = Random.Range(3.5f, 6f);
                    p.Spin = Random.Range(-25f, 25f);
                    break;
                case AmbienceKind.Confetti:
                    sprite = Random.value < 0.3f ? Sprites.CircleSprite : null;
                    p.Size = Random.Range(16f, 30f);
                    p.Pos = new Vector2(Random.Range(a.xMin, a.xMax), a.yMax + 30);
                    p.Vel = new Vector2(Random.Range(-60f, 60f), Random.Range(-420f, -260f));
                    p.Life = (a.height + 60) / -p.Vel.y;
                    p.Spin = Random.Range(-400f, 400f);
                    break;
                case AmbienceKind.Rain:
                    sprite = Sprites.Streak;
                    p.Size = Random.Range(40f, 70f);
                    p.Pos = new Vector2(Random.Range(a.xMin, a.xMax + 200), a.yMax + 40);
                    p.Vel = new Vector2(-180f, -900f);
                    p.Life = (a.height + 80) / 900f;
                    break;
                case AmbienceKind.Clouds:
                    sprite = Sprites.Cloud;
                    p.Size = Random.Range(180f, 320f);
                    p.Pos = new Vector2(a.xMin - 200, Random.Range(a.center.y, a.yMax - 80));
                    p.Vel = new Vector2(Random.Range(18f, 40f), 0);
                    p.Life = (a.width + 400) / p.Vel.x;
                    break;
                case AmbienceKind.Birds:
                    sprite = Sprites.Bird;
                    p.Size = Random.Range(34f, 54f);
                    bool ltr = Random.value < 0.5f;
                    p.Pos = new Vector2(ltr ? a.xMin - 60 : a.xMax + 60, Random.Range(a.center.y, a.yMax - 60));
                    p.Vel = new Vector2((ltr ? 1 : -1) * Random.Range(110f, 170f), Random.Range(-10f, 15f));
                    p.Life = (a.width + 120) / Mathf.Abs(p.Vel.x);
                    break;
                default: // Fireflies, Twinkle, Sparkles
                    sprite = Kind == AmbienceKind.Twinkle || Kind == AmbienceKind.Sparkles ? Sprites.Star : Sprites.Soft;
                    p.Size = Kind == AmbienceKind.Fireflies ? Random.Range(16f, 30f) : Random.Range(20f, 42f);
                    p.Pos = new Vector2(Random.Range(a.xMin, a.xMax), Random.Range(a.yMin, a.yMax));
                    p.Vel = Kind == AmbienceKind.Fireflies ? Random.insideUnitCircle * 25f : Vector2.zero;
                    p.Life = Random.Range(2.2f, 4.5f);
                    p.Spin = Kind == AmbienceKind.Twinkle ? 0 : Random.Range(-60f, 60f);
                    break;
            }

            if (Kind == AmbienceKind.Letters)
            {
                var t = UI.Label(rt, ((char)('A' + Random.Range(0, 26))).ToString(), p.Size, Tint, TextAnchor.MiddleCenter, false);
                p.Rt = t.rectTransform;
                p.G = t;
                p.Rt.sizeDelta = new Vector2(p.Size, p.Size);
            }
            else
            {
                var img = UI.Img(rt, sprite, Tint, "P");
                p.Rt = img.rectTransform;
                p.G = img;
                float aspect = sprite != null && sprite.rect.height > 0 ? sprite.rect.width / sprite.rect.height : 1f;
                p.Rt.sizeDelta = new Vector2(p.Size * aspect, p.Size);
                if (Kind == AmbienceKind.Leaves) img.color = Color.Lerp(Palette.Hex("4FA83A"), Palette.Hex("F2B33D"), Random.value * 0.6f);
                if (Kind == AmbienceKind.Confetti)
                {
                    img.color = Palette.WordColors[Random.Range(0, Palette.WordColors.Length)];
                    if (sprite == null) p.Rt.sizeDelta = new Vector2(p.Size * 0.55f, p.Size);
                }
            }
            p.Rt.anchorMin = p.Rt.anchorMax = new Vector2(0.5f, 0.5f);
            if (Kind == AmbienceKind.Rain) p.Rt.localRotation = Quaternion.Euler(0, 0, -11);
            p.Alpha = p.G.color.a;
            p.Rt.anchoredPosition = ToAnchored(p.Pos);
            live.Add(p);
        }

        Vector2 ToAnchored(Vector2 local) => local - rt.rect.center;

        // ---------------- motion ----------------

        void Step(P p, float dt, float k, Rect area)
        {
            float t = p.Age + p.Phase;
            float fade = Mathf.Clamp01(Mathf.Min(k * 6f, (1f - k) * 4f));
            switch (Kind)
            {
                case AmbienceKind.Leaves:
                    p.Pos += p.Vel * dt + new Vector2(Mathf.Sin(t * 1.8f) * 40f * dt, 0);
                    p.Rt.localRotation = Quaternion.Euler(0, 0, Mathf.Sin(t * 1.5f) * 50f + p.Spin * k);
                    break;
                case AmbienceKind.Bubbles:
                    p.Pos += p.Vel * dt + new Vector2(Mathf.Sin(t * 2.4f) * 22f * dt, 0);
                    fade *= 0.75f;
                    break;
                case AmbienceKind.Fireflies:
                    p.Vel += Random.insideUnitCircle * 60f * dt;
                    p.Vel = Vector2.ClampMagnitude(p.Vel, 40f);
                    p.Pos += p.Vel * dt;
                    fade *= 0.5f + 0.5f * Mathf.Sin(t * 5f);
                    break;
                case AmbienceKind.Twinkle:
                case AmbienceKind.Sparkles:
                {
                    float tw = Mathf.Sin(k * Mathf.PI);
                    p.Rt.localScale = Vector3.one * (0.3f + tw);
                    p.Rt.localRotation = Quaternion.Euler(0, 0, p.Spin * k);
                    fade = tw;
                    break;
                }
                case AmbienceKind.Steam:
                    p.Pos += p.Vel * dt;
                    p.Rt.localScale = Vector3.one * (0.6f + k);
                    fade *= 0.35f;
                    break;
                case AmbienceKind.Notes:
                case AmbienceKind.Hearts:
                case AmbienceKind.Letters:
                    p.Pos += p.Vel * dt + new Vector2(Mathf.Sin(t * 2f) * 30f * dt, 0);
                    p.Rt.localRotation = Quaternion.Euler(0, 0, Mathf.Sin(t * 1.6f) * 15f + p.Spin * k);
                    if (Kind == AmbienceKind.Letters) fade *= 0.45f;
                    break;
                case AmbienceKind.Birds:
                {
                    p.Pos += p.Vel * dt;
                    float flap = 0.55f + 0.45f * Mathf.Abs(Mathf.Sin(t * 9f));
                    p.Rt.localScale = new Vector3(Mathf.Sign(p.Vel.x), flap, 1);
                    fade *= 0.8f;
                    break;
                }
                case AmbienceKind.Clouds:
                    p.Pos += p.Vel * dt;
                    fade *= 0.85f;
                    break;
                case AmbienceKind.Confetti:
                    p.Pos += p.Vel * dt + new Vector2(Mathf.Sin(t * 4f) * 60f * dt, 0);
                    p.Rt.localRotation = Quaternion.Euler(0, 0, p.Spin * p.Age);
                    p.Rt.localScale = new Vector3(Mathf.Cos(t * 7f), 1, 1);
                    fade = Mathf.Clamp01((1f - k) * 5f);
                    break;
                default:
                    p.Pos += p.Vel * dt;
                    fade *= 0.6f;
                    break;
            }
            var c = p.G.color;
            c.a = p.Alpha * fade;
            p.G.color = c;
            p.Rt.anchoredPosition = ToAnchored(p.Pos);
        }

        static Sprite HeartSprite() => Theme.Current.ArtFor("BODY")?.icon ?? Sprites.Star;
        static Sprite NoteSprite() => Theme.Current.ArtFor("MUSIC")?.icon ?? Sprites.Star;

        void OnDestroy()
        {
            foreach (var p in live) if (p.Rt != null) Destroy(p.Rt.gameObject);
            live.Clear();
        }
    }
}
