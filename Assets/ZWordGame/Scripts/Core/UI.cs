using System;
using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>Palette used across the game.</summary>
    public static class Palette
    {
        public static readonly Color Brown = Hex("5B3418");   // main ink (warm dark brown, like the logo outline)
        public static readonly Color DarkPurple = Hex("6F62C9");
        public static readonly Color Cream = Hex("FFFDF8");   // board tiles
        public static readonly Color CreamShadow = Hex("EDBE62");
        public static readonly Color Yellow = Hex("FFD02E");
        public static readonly Color YellowShadow = Hex("E39A12");
        public static readonly Color Green = Hex("4CD137");
        public static readonly Color Red = Hex("F2506A");
        public static readonly Color Blue = Hex("3AA0F5");
        public static readonly Color Purple = Hex("9B59E6");
        public static readonly Color Panel = Hex("FFF8EC");
        public static readonly Color White = Color.white;

        public static readonly Color[] WordColors =
        {
            Hex("4CD137"), Hex("F46FD8"), Hex("3AA0F5"), Hex("FF8A3D"), Hex("9B59E6"), Hex("1FC1B5"), Hex("F2506A")
        };

        public static Color Hex(string hex)
        {
            ColorUtility.TryParseHtmlString("#" + hex, out var c);
            return c;
        }

        public static Color Darken(Color c, float f = 0.75f) => new Color(c.r * f, c.g * f, c.b * f, c.a);
        public static Color Lighten(Color c, float f = 0.3f) => Color.Lerp(c, Color.white, f);
    }

    /// <summary>Small helpers to build uGUI hierarchies from code.</summary>
    public static class UI
    {

        public static RectTransform Rect(string name, Transform parent)
        {
            var go = new GameObject(name, typeof(RectTransform));
            go.layer = 5; // UI
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        public static RectTransform Place(this RectTransform rt, Vector2 anchor, Vector2 pos, Vector2 size)
        {
            rt.anchorMin = rt.anchorMax = anchor;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = pos;
            rt.sizeDelta = size;
            return rt;
        }

        public static RectTransform Stretch(this RectTransform rt, float l = 0, float b = 0, float r = 0, float t = 0)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.offsetMin = new Vector2(l, b);
            rt.offsetMax = new Vector2(-r, -t);
            return rt;
        }

        public static Image Img(Transform parent, Sprite sprite, Color color, string name = "Image", float cornerScale = 1f)
        {
            var rt = Rect(name, parent);
            var img = rt.gameObject.AddComponent<Image>();
            img.sprite = sprite;
            img.color = color;
            img.raycastTarget = false;
            if (sprite != null && sprite.border != Vector4.zero)
            {
                img.type = Image.Type.Sliced;
                img.pixelsPerUnitMultiplier = cornerScale;
            }
            return img;
        }

        public static TextMeshProUGUI Label(Transform parent, string text, float size, Color color, TextAnchor align = TextAnchor.MiddleCenter, bool shadow = true)
        {
            var rt = Rect("Label", parent);
            var t = rt.gameObject.AddComponent<TextMeshProUGUI>();
            t.font = Fonts.Asset;
            t.fontSharedMaterial = shadow ? Fonts.Shadow : Fonts.Plain;
            t.fontStyle = FontStyles.Normal;
            t.fontSize = size;
            t.color = color;
            t.alignment = Align(align);
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.richText = false;
            t.raycastTarget = false;
            t.text = text;
            return t;
        }

        /// <summary>Switch a label to the chunky outlined style (titles, button captions).</summary>
        public static TMP_Text Outlined(TMP_Text t)
        {
            t.fontSharedMaterial = Fonts.Outline;
            return t;
        }

        static TextAlignmentOptions Align(TextAnchor a)
        {
            switch (a)
            {
                case TextAnchor.UpperLeft: return TextAlignmentOptions.TopLeft;
                case TextAnchor.UpperCenter: return TextAlignmentOptions.Top;
                case TextAnchor.UpperRight: return TextAlignmentOptions.TopRight;
                case TextAnchor.MiddleLeft: return TextAlignmentOptions.Left;
                case TextAnchor.MiddleRight: return TextAlignmentOptions.Right;
                case TextAnchor.LowerLeft: return TextAlignmentOptions.BottomLeft;
                case TextAnchor.LowerCenter: return TextAlignmentOptions.Bottom;
                case TextAnchor.LowerRight: return TextAlignmentOptions.BottomRight;
                default: return TextAlignmentOptions.Center;
            }
        }

        /// <summary>Raised "3D" button: darker base, coloured face, glossy strip, label.</summary>
        public static Button Chunky(Transform parent, Vector2 size, Color face, string label, int fontSize, Action onClick,
            Sprite sprite = null, float cornerScale = 1f, float depth = 12f)
        {
            sprite = sprite ?? Sprites.Rounded;
            var root = Rect("Btn_" + label, parent);
            root.sizeDelta = size;
            var hit = root.gameObject.AddComponent<Image>();
            hit.color = new Color(0, 0, 0, 0);
            hit.raycastTarget = true;

            var body = Rect("Body", root).Stretch();
            var baseImg = Img(body, sprite, Palette.Darken(face, 0.7f), "Base", cornerScale);
            baseImg.rectTransform.Stretch(0, 0, 0, depth);
            var faceImg = Img(body, sprite, face, "Face", cornerScale);
            faceImg.rectTransform.Stretch(0, depth, 0, 0);
            var gloss = Img(faceImg.transform, sprite, new Color(1, 1, 1, 0.22f), "Gloss", cornerScale * 1.6f);
            gloss.rectTransform.anchorMin = new Vector2(0, 0.55f);
            gloss.rectTransform.anchorMax = new Vector2(1, 1);
            gloss.rectTransform.offsetMin = new Vector2(10, 0);
            gloss.rectTransform.offsetMax = new Vector2(-10, -6);

            if (!string.IsNullOrEmpty(label))
            {
                var t = Label(faceImg.transform, label, fontSize, Color.white);
                t.rectTransform.Stretch(8, 0, 8, 0);
                Outlined(t);
            }

            var btn = root.gameObject.AddComponent<Button>();
            btn.targetGraphic = hit;
            btn.transition = Selectable.Transition.None;
            btn.onClick.AddListener(() => { AudioManager.Click(); onClick?.Invoke(); });
            var press = root.gameObject.AddComponent<PressEffect>();
            press.body = body;
            press.depth = depth;
            return btn;
        }

        /// <summary>Round icon button (like the booster buttons in the mockup).</summary>
        public static Button IconButton(Transform parent, float diameter, Color color, Sprite icon, Action onClick, float iconScale = 0.55f)
        {
            var btn = Chunky(parent, new Vector2(diameter, diameter), color, null, 0, onClick, Sprites.CircleSprite, 1f, diameter * 0.08f);
            var face = btn.transform.Find("Body/Face");
            var ic = Img(face, icon, Color.white, "Icon");
            ic.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, Vector2.one * diameter * iconScale);
            var sh = ic.gameObject.AddComponent<Shadow>();
            sh.effectColor = new Color(0, 0, 0, 0.25f);
            sh.effectDistance = new Vector2(0, -4);
            return btn;
        }

        /// <summary>Plain flat icon button (back / settings in the header).</summary>
        public static Button FlatIcon(Transform parent, Sprite icon, Vector2 size, Color color, Action onClick)
        {
            var rt = Rect("Icon", parent);
            rt.sizeDelta = size;
            var shadow = Img(rt, icon, new Color(0, 0, 0, 0.3f), "Shadow");
            shadow.rectTransform.Stretch(0, -8, 0, 8);
            var img = Img(rt, icon, color, "Face");
            img.rectTransform.Stretch();
            var hit = rt.gameObject.AddComponent<Image>();
            hit.color = new Color(0, 0, 0, 0);
            var b = rt.gameObject.AddComponent<Button>();
            b.targetGraphic = hit;
            b.transition = Selectable.Transition.None;
            b.onClick.AddListener(() => { AudioManager.Click(); onClick?.Invoke(); });
            rt.gameObject.AddComponent<PressEffect>().body = rt;
            return b;
        }

        /// <summary>Yellow title pill used for screen headings.</summary>
        public static RectTransform TitlePill(Transform parent, string title, string tab = null)
        {
            var root = Rect("Title", parent);
            root.sizeDelta = new Vector2(420, 96);
            var b = Img(root, Sprites.Rounded, Palette.YellowShadow, "Base", 1.4f);
            b.rectTransform.Stretch(0, 0, 0, 0);
            var f = Img(root, Sprites.Rounded, Palette.Yellow, "Face", 1.4f);
            f.rectTransform.Stretch(0, 10, 0, 0);
            var t = Label(f.transform, title, 50, Palette.Brown, TextAnchor.MiddleCenter, false);
            t.rectTransform.Stretch(0, 0, 0, 0);
            if (tab != null)
            {
                var tb = Img(root, Sprites.Rounded, Palette.Hex("F59B23"), "Tab", 3f);
                tb.rectTransform.Place(new Vector2(0.5f, 1f), new Vector2(0, 6), new Vector2(120, 40));
                var tt = Label(tb.transform, tab, 24, Palette.Brown, TextAnchor.MiddleCenter, false);
                tt.rectTransform.Stretch();
            }
            return root;
        }

        /// <summary>Rounded horizontal slider (0..1) used for volume settings.</summary>
        public static UnityEngine.UI.Slider VolumeSlider(Transform parent, Vector2 size, Color fill, float value, Action<float> onChange)
        {
            var root = Rect("Slider", parent);
            root.sizeDelta = size;
            var hit = root.gameObject.AddComponent<Image>();
            hit.color = new Color(0, 0, 0, 0);

            float inset = size.y * 0.3f;
            var track = Img(root, Sprites.Rounded, new Color(0.2f, 0.06f, 0.15f, 0.22f), "Track", 3f);
            track.rectTransform.Stretch(0, inset, 0, inset);
            var fillArea = Rect("FillArea", root).Stretch(0, inset, size.y * 0.5f, inset);
            var fillImg = Img(fillArea, Sprites.Rounded, fill, "Fill", 3f);
            fillImg.rectTransform.Stretch();

            var handleArea = Rect("HandleArea", root).Stretch(size.y * 0.5f, 0, size.y * 0.5f, 0);
            var handle = Img(handleArea, Sprites.CircleSprite, Color.white, "Handle");
            handle.rectTransform.sizeDelta = new Vector2(size.y, 0);
            var hs = handle.gameObject.AddComponent<Shadow>();
            hs.effectColor = new Color(0, 0, 0, 0.3f);
            hs.effectDistance = new Vector2(0, -4);

            var s = root.gameObject.AddComponent<UnityEngine.UI.Slider>();
            s.fillRect = fillImg.rectTransform;
            s.handleRect = handle.rectTransform;
            s.targetGraphic = handle;
            s.transition = Selectable.Transition.None;
            s.direction = UnityEngine.UI.Slider.Direction.LeftToRight;
            s.minValue = 0f;
            s.maxValue = 1f;
            s.SetValueWithoutNotify(value);
            s.onValueChanged.AddListener(v => onChange?.Invoke(v));
            return s;
        }

        public static CanvasGroup Overlay(Transform parent, float alpha = 0.6f)
        {
            var rt = Rect("Overlay", parent).Stretch();
            var img = rt.gameObject.AddComponent<Image>();
            img.color = new Color(0.12f, 0.04f, 0.1f, alpha);
            img.raycastTarget = true;
            var cg = rt.gameObject.AddComponent<CanvasGroup>();
            return cg;
        }
    }

    /// <summary>Pushes a chunky button down while pressed.</summary>
    public class PressEffect : MonoBehaviour, IPointerDownHandler, IPointerUpHandler, IPointerExitHandler
    {
        public RectTransform body;
        public float depth;
        Vector2 basePos;
        bool down;

        void Start() { if (body) basePos = body.anchoredPosition; }

        public void OnPointerDown(PointerEventData e)
        {
            if (!body) return;
            down = true;
            body.anchoredPosition = basePos + new Vector2(0, -depth * 0.6f);
            body.localScale = Vector3.one * 0.97f;
        }

        public void OnPointerUp(PointerEventData e) => Release();
        public void OnPointerExit(PointerEventData e) { if (down) Release(); }

        void Release()
        {
            down = false;
            if (!body) return;
            body.anchoredPosition = basePos;
            body.localScale = Vector3.one;
        }
    }

    /// <summary>Tiny coroutine tween library (unscaled time).</summary>
    public static class Tween
    {
        public static MonoBehaviour Runner;

        public static float OutBack(float t)
        {
            const float c1 = 1.70158f, c3 = c1 + 1f;
            return 1f + c3 * Mathf.Pow(t - 1f, 3) + c1 * Mathf.Pow(t - 1f, 2);
        }

        public static float OutCubic(float t) => 1f - Mathf.Pow(1f - t, 3);

        public static Coroutine Run(IEnumerator e) => Runner != null ? Runner.StartCoroutine(e) : null;

        public static Coroutine Value(float duration, Action<float> step, Func<float, float> ease = null, float delay = 0f, Action done = null)
            => Run(ValueCo(duration, step, ease, delay, done));

        static IEnumerator ValueCo(float duration, Action<float> step, Func<float, float> ease, float delay, Action done)
        {
            if (delay > 0) yield return new WaitForSecondsRealtime(delay);
            float t = 0;
            while (t < duration)
            {
                t += Time.unscaledDeltaTime;
                float k = Mathf.Clamp01(t / duration);
                try { step(ease != null ? ease(k) : k); }
                catch (MissingReferenceException) { yield break; }
                yield return null;
            }
            done?.Invoke();
        }

        public static void PopIn(Transform t, float duration = 0.35f, float delay = 0f)
        {
            if (t == null) return;
            t.localScale = Vector3.zero;
            Value(duration, k => { if (t) t.localScale = Vector3.one * OutBack(k); }, null, delay);
        }

        public static void Punch(Transform t, float amount = 0.15f, float duration = 0.25f)
        {
            if (t == null) return;
            Value(duration, k => { if (t) t.localScale = Vector3.one * (1f + Mathf.Sin(k * Mathf.PI) * amount); });
        }

        public static void Shake(RectTransform rt, float amount = 18f, float duration = 0.35f)
        {
            if (rt == null) return;
            var start = rt.anchoredPosition;
            Value(duration, k =>
            {
                if (!rt) return;
                rt.anchoredPosition = start + new Vector2(Mathf.Sin(k * 40f) * amount * (1f - k), 0);
            }, null, 0, () => { if (rt) rt.anchoredPosition = start; });
        }

        public static void Fade(CanvasGroup cg, float from, float to, float duration = 0.25f, Action done = null)
        {
            if (cg == null) return;
            cg.alpha = from;
            Value(duration, k => { if (cg) cg.alpha = Mathf.Lerp(from, to, k); }, OutCubic, 0, done);
        }
    }
}
