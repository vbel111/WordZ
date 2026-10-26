using System;
using System.Globalization;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>Word Z colour skin: "sky & candy" (white cards, purple accents, indigo ink). Names kept from the old wood skin.</summary>
    public static class Skin
    {
        public static readonly Color Cream = Palette.Hex("FFFFFF");
        public static readonly Color CreamShade = Palette.Hex("FBEACB");
        public static readonly Color Ink = Palette.Hex("5B3418");
        public static readonly Color InkSoft = Palette.Hex("9A7550");
        public static readonly Color Wood = Palette.Hex("FFC928");      // secondary buttons (logo yellow)
        public static readonly Color WoodDark = Palette.Hex("D9990B");
        public static readonly Color Plank = Palette.Hex("FFD447");
        public static readonly Color Green = Palette.Hex("5BC236");
        public static readonly Color Red = Palette.Hex("E5484D");
        public static readonly Color Gold = Palette.Hex("FFC21A");
        public static readonly Color Purple = Palette.Hex("9B4DE0");
        public static readonly Color Blue = Palette.Hex("2F9BEA");
        public static readonly Color Slate = Palette.Hex("56658A");
        public static readonly Color ChipBg = new Color(0.36f, 0.2f, 0.06f, 0.55f);
    }

    public enum Currency { Stars, Coins, Gems }

    /// <summary>A rounded progress bar; call Set(0..1).</summary>
    public class ProgressBar
    {
        public RectTransform Root, Fill;
        public TMP_Text Label;

        public void Set(float v, string label = null)
        {
            v = Mathf.Clamp01(v);
            Fill.anchorMax = new Vector2(v, 1);
            Fill.gameObject.SetActive(v > 0.001f);
            if (Label != null && label != null) Label.text = label;
        }
    }

    /// <summary>Keeps a currency chip's number in sync with the wallet.</summary>
    public class CurrencyChipView : MonoBehaviour
    {
        public Currency Kind;
        public TMP_Text Text;
        int shown = -1;

        void OnEnable() { Save.WalletChanged += Refresh; Refresh(); }
        void OnDisable() { Save.WalletChanged -= Refresh; }

        public void Refresh()
        {
            if (Text == null) return;
            int v = Kind == Currency.Stars ? Save.StarPoints : Kind == Currency.Coins ? Save.Coins : Save.Gems;
            if (shown >= 0 && v != shown) Tween.Punch(transform, 0.15f, 0.25f);
            shown = v;
            Text.text = v.ToString("N0", CultureInfo.InvariantCulture);
        }
    }

    /// <summary>Gentle floating motion for decorative tiles.</summary>
    public class Bobber : MonoBehaviour
    {
        public float Amplitude = 10f, Speed = 1.4f, Phase, Tilt = 4f;
        Vector2 basePos;
        float baseRot;
        RectTransform rt;

        void Start()
        {
            rt = (RectTransform)transform;
            basePos = rt.anchoredPosition;
            baseRot = rt.localEulerAngles.z;
        }

        void Update()
        {
            float t = Time.unscaledTime * Speed + Phase;
            rt.anchoredPosition = basePos + new Vector2(0, Mathf.Sin(t) * Amplitude);
            rt.localRotation = Quaternion.Euler(0, 0, baseRot + Mathf.Sin(t * 0.7f) * Tilt);
        }
    }

    /// <summary>Building blocks for the Word Z screens (see the UI mockup).</summary>
    public static class Widgets
    {
        // ---------------- header ----------------

        /// <summary>Round brown back button, yellow title pill (+ LV tab), round gear (or nothing).</summary>
        public static void Header(RectTransform parent, string title, string tab, Action onBack, bool gear = true)
        {
            if (onBack != null)
            {
                var back = RoundButton(parent, Sprites.Back, 104, Skin.Wood, onBack, 0.46f);
                ((RectTransform)back.transform).Place(new Vector2(0, 1), new Vector2(84, -104), new Vector2(104, 104));
            }
            if (gear)
            {
                var g = RoundButton(parent, Sprites.Gear, 104, Skin.Wood, () => ZWordApp.I.OpenSettings(), 0.56f);
                ((RectTransform)g.transform).Place(new Vector2(1, 1), new Vector2(-84, -104), new Vector2(104, 104));
            }
            var pill = UI.TitlePill(parent, title, tab);
            pill.anchorMin = pill.anchorMax = new Vector2(0.5f, 1);
            pill.anchoredPosition = new Vector2(0, -104);
        }

        public static Button RoundButton(Transform parent, Sprite icon, float size, Color color, Action onClick, float iconScale = 0.5f)
            => UI.IconButton(parent, size, color, icon, onClick, iconScale);

        // ---------------- currency ----------------

        public static RectTransform CurrencyIcon(Transform parent, Currency kind, float size)
        {
            var root = UI.Rect(kind + "Icon", parent);
            root.sizeDelta = new Vector2(size, size);
            switch (kind)
            {
                case Currency.Stars:
                {
                    var sh = UI.Img(root, Sprites.Star, new Color(0.45f, 0.25f, 0f, 0.5f), "Shadow");
                    sh.rectTransform.Stretch(0, -size * 0.06f, 0, size * 0.06f);
                    var s = UI.Img(root, Sprites.Star, Skin.Gold, "Star");
                    s.rectTransform.Stretch();
                    break;
                }
                case Currency.Coins:
                    if (Theme.Current.coin != null)
                    {
                        UI.Img(root, Theme.Current.coin, Color.white, "Coin").rectTransform.Stretch();
                        break;
                    }
                    UI.Img(root, Sprites.CircleSprite, Palette.Hex("C97C06"), "Rim").rectTransform.Stretch();
                    UI.Img(root, Sprites.CircleSprite, Palette.Hex("FFC928"), "Face").rectTransform.Stretch(size * 0.08f, size * 0.12f, size * 0.08f, size * 0.04f);
                    UI.Img(root, Sprites.Ring, Palette.Hex("FFE680"), "Ring").rectTransform.Stretch(size * 0.18f, size * 0.22f, size * 0.18f, size * 0.14f);
                    UI.Img(root, Sprites.Star, Palette.Hex("E39A0C"), "Emboss").rectTransform.Stretch(size * 0.3f, size * 0.32f, size * 0.3f, size * 0.24f);
                    break;
                case Currency.Gems:
                    if (Theme.Current.gem != null)
                    {
                        UI.Img(root, Theme.Current.gem, Color.white, "Gem").rectTransform.Stretch();
                        break;
                    }
                    UI.Img(root, Sprites.GemShape, Palette.Hex("6E22C2"), "Shadow").rectTransform.Stretch(0, -size * 0.05f, 0, size * 0.05f);
                    UI.Img(root, Sprites.GemShape, Palette.Hex("9B4DE8"), "Body").rectTransform.Stretch();
                    UI.Img(root, Sprites.GemTopFacet, Palette.Hex("C493FF"), "Top").rectTransform.Stretch();
                    UI.Img(root, Sprites.GemMidFacet, new Color(1f, 1f, 1f, 0.35f), "Shine").rectTransform.Stretch();
                    break;
            }
            return root;
        }

        /// <summary>Dark pill with a currency icon and a live number.</summary>
        public static RectTransform CurrencyChip(Transform parent, Currency kind, float width = 210)
        {
            var root = UI.Rect(kind + "Chip", parent);
            root.sizeDelta = new Vector2(width, 66);
            var bg = UI.Img(root, Sprites.Rounded, Skin.ChipBg, "Bg", 1.6f);
            bg.rectTransform.Stretch(18, 4, 0, 4);
            var icon = CurrencyIcon(root, kind, 70);
            icon.Place(new Vector2(0, 0.5f), new Vector2(30, 0), new Vector2(70, 70));
            var t = UI.Label(root, "0", 38, Color.white, TextAnchor.MiddleCenter);
            t.rectTransform.Stretch(64, 0, 10, 0);
            var view = root.gameObject.AddComponent<CurrencyChipView>();
            view.Kind = kind;
            view.Text = t;
            view.Refresh(); // OnEnable ran before Text was set, so show the real balance now
            return root;
        }

        // ---------------- bars, badges, toggles ----------------

        public static ProgressBar Progress(Transform parent, Vector2 size, Color fill, Color track, bool withLabel = false)
        {
            var root = UI.Rect("Progress", parent);
            root.sizeDelta = size;
            float corner = 128f / Mathf.Max(8f, size.y) * 0.5f;
            UI.Img(root, Sprites.Rounded, track, "Track", corner).rectTransform.Stretch();
            var fillRt = UI.Rect("Fill", root);
            fillRt.anchorMin = Vector2.zero;
            fillRt.anchorMax = Vector2.one;
            fillRt.offsetMin = new Vector2(3, 3);
            fillRt.offsetMax = new Vector2(-3, -3);
            UI.Img(fillRt, Sprites.Rounded, fill, "FillImg", corner * 1.1f).rectTransform.Stretch();
            var gloss = UI.Img(fillRt, Sprites.Rounded, new Color(1, 1, 1, 0.28f), "Gloss", corner * 2f);
            gloss.rectTransform.anchorMin = new Vector2(0, 0.55f);
            gloss.rectTransform.anchorMax = Vector2.one;
            gloss.rectTransform.offsetMin = new Vector2(6, 0);
            gloss.rectTransform.offsetMax = new Vector2(-6, -2);
            var bar = new ProgressBar { Root = root, Fill = fillRt };
            if (withLabel)
            {
                bar.Label = UI.Label(root, "", size.y * 0.62f, Color.white, TextAnchor.MiddleCenter);
                bar.Label.rectTransform.Stretch();
            }
            return bar;
        }

        /// <summary>Small red notification dot with an optional number, pinned to the parent's top-right.</summary>
        public static RectTransform Badge(Transform parent, string text, float size = 44)
        {
            var b = UI.Rect("Badge", parent).Place(new Vector2(1, 1), new Vector2(-size * 0.2f, -size * 0.2f), new Vector2(size, size));
            UI.Img(b, Sprites.CircleSprite, Color.white, "Rim").rectTransform.Stretch();
            UI.Img(b, Sprites.CircleSprite, Skin.Red, "Dot").rectTransform.Stretch(4, 4, 4, 4);
            var t = UI.Label(b, text, size * 0.55f, Color.white, TextAnchor.MiddleCenter, false);
            t.rectTransform.Stretch(0, 2, 0, 0);
            return b;
        }

        /// <summary>Green / grey switch.</summary>
        public static RectTransform Switch(Transform parent, bool on, Action<bool> changed)
        {
            var root = UI.Rect("Switch", parent);
            root.sizeDelta = new Vector2(108, 58);
            var hit = root.gameObject.AddComponent<Image>();
            hit.color = new Color(0, 0, 0, 0);
            var track = UI.Img(root, Sprites.Rounded, on ? Skin.Green : Palette.Hex("E2D4BE"), "Track", 2.2f);
            track.rectTransform.Stretch();
            var knob = UI.Img(root, Sprites.CircleSprite, Color.white, "Knob");
            knob.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(on ? 25 : -25, 0), new Vector2(48, 48));
            var sh = knob.gameObject.AddComponent<Shadow>();
            sh.effectColor = new Color(0, 0, 0, 0.25f);
            sh.effectDistance = new Vector2(0, -3);

            bool state = on;
            var btn = root.gameObject.AddComponent<Button>();
            btn.targetGraphic = hit;
            btn.transition = Selectable.Transition.None;
            btn.onClick.AddListener(() =>
            {
                state = !state;
                AudioManager.Click();
                float from = state ? -25 : 25, to = state ? 25 : -25;
                Tween.Value(0.15f, k =>
                {
                    if (!knob) return;
                    knob.rectTransform.anchoredPosition = new Vector2(Mathf.Lerp(from, to, k), 0);
                }, Tween.OutCubic);
                track.color = state ? Skin.Green : Palette.Hex("E2D4BE");
                changed?.Invoke(state);
            });
            return root;
        }

        // ---------------- buttons ----------------

        /// <summary>Chunky button with an icon left of the caption (RESUME, RESTART...).</summary>
        public static Button IconTextButton(Transform parent, Vector2 size, Color color, string label, Sprite icon, int fontSize, Action onClick)
        {
            var b = UI.Chunky(parent, size, color, label, fontSize, onClick);
            var face = b.transform.Find("Body/Face");
            var t = face.GetComponentInChildren<TMP_Text>();
            if (icon != null)
            {
                float s = size.y * 0.46f;
                var ic = UI.Img(face, icon, Color.white, "Icon");
                ic.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(size.y * 0.55f, 0), new Vector2(s, s));
                var sh = ic.gameObject.AddComponent<Shadow>();
                sh.effectColor = new Color(0, 0, 0, 0.25f);
                sh.effectDistance = new Vector2(0, -3);
                if (t != null)
                {
                    t.rectTransform.Stretch(size.y * 0.9f, 0, size.y * 0.3f, 0);
                    t.alignment = TextAlignmentOptions.Center;
                }
            }
            return b;
        }

        /// <summary>Green pill with a currency icon and a price ("50", "$0.99").</summary>
        public static Button PriceButton(Transform parent, Vector2 size, Currency? icon, string price, Action onClick, Color? color = null)
        {
            var b = UI.Chunky(parent, size, color ?? Skin.Green, price, (int)(size.y * 0.42f), onClick, null, 1.6f, size.y * 0.1f);
            if (icon.HasValue)
            {
                var face = b.transform.Find("Body/Face");
                var ic = CurrencyIcon(face, icon.Value, size.y * 0.62f);
                ic.Place(new Vector2(0, 0.5f), new Vector2(size.y * 0.45f, 0), Vector2.one * size.y * 0.62f);
                var t = face.GetComponentInChildren<TMP_Text>();
                if (t != null) t.rectTransform.Stretch(size.y * 0.7f, 0, 6, 0);
            }
            return b;
        }

        /// <summary>Square wooden tile with an icon and a caption underneath (home dock, result screens).</summary>
        public static Button DockButton(Transform parent, Sprite icon, Color iconColor, string label, Action onClick, float size = 132, float iconScale = 0.56f)
        {
            var b = UI.Chunky(parent, new Vector2(size, size), Skin.Wood, null, 0, onClick, null, 1.4f, size * 0.08f);
            var face = b.transform.Find("Body/Face");
            var inner = UI.Img(face, Sprites.Rounded, Color.white, "Inner", 1.8f);
            inner.rectTransform.Stretch(10, 10, 10, 10);
            var ic = UI.Img(face, icon, iconColor, "Icon");
            ic.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 2), Vector2.one * size * iconScale);
            ic.preserveAspect = true;
            var sh = ic.gameObject.AddComponent<Shadow>();
            sh.effectColor = new Color(0, 0, 0, 0.3f);
            sh.effectDistance = new Vector2(0, -4);
            if (!string.IsNullOrEmpty(label))
            {
                var t = UI.Label(b.transform, label, 30, Color.white, TextAnchor.MiddleCenter);
                t.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, -26), new Vector2(size + 60, 40));
                UI.Outlined(t);
            }
            return b;
        }

        public static Button CloseButton(Transform parent, float size, Action onClick)
        {
            if (Theme.Current.close != null)
            {
                var b = UI.FlatIcon(parent, Theme.Current.close, new Vector2(size, size), Color.white, onClick);
                return b;
            }
            return RoundButton(parent, Sprites.Cross, size, Skin.Red, onClick, 0.5f);
        }

        // ---------------- panels ----------------

        /// <summary>Cream rounded card with a soft shadow.</summary>
        public static RectTransform Card(Transform parent, Vector2 size, Color? color = null)
        {
            var root = UI.Rect("Card", parent);
            root.sizeDelta = size;
            UI.Img(root, Sprites.Rounded, new Color(0.42f, 0.25f, 0.06f, 0.25f), "Shadow", 0.9f).rectTransform.Stretch(0, -12, 0, 12);
            UI.Img(root, Sprites.Rounded, color ?? Skin.Cream, "Face", 0.9f).rectTransform.Stretch();
            return root;
        }

        /// <summary>
        /// Popup with a wooden plank title bar, cream body and a red X (mockup: PAUSED / HINTS).
        /// Returns the body; its top 120 units are covered by the plank.
        /// </summary>
        public static RectTransform WoodPopup(string title, Vector2 size, Action onClose = null)
        {
            var overlay = ZWordApp.I.NewPopup(title, onClose);
            var root = UI.Rect("WoodPopup", overlay).Place(new Vector2(0.5f, 0.5f), Vector2.zero, size);

            UI.Img(root, Sprites.Rounded, new Color(0.38f, 0.21f, 0.04f, 0.45f), "Shadow").rectTransform.Stretch(-6, -20, -6, 6);
            UI.Img(root, Sprites.Rounded, Skin.WoodDark, "Frame").rectTransform.Stretch();
            var body = UI.Img(root, Sprites.Rounded, Skin.Cream, "Body", 1.2f);
            body.rectTransform.Stretch(18, 18, 18, 110);

            // plank
            var plank = UI.Rect("Plank", root);
            plank.anchorMin = new Vector2(0, 1);
            plank.anchorMax = new Vector2(1, 1);
            plank.pivot = new Vector2(0.5f, 1);
            plank.offsetMin = new Vector2(-14, -134);
            plank.offsetMax = new Vector2(14, 10);
            UI.Img(plank, Sprites.Rounded, Skin.WoodDark, "Base", 1.4f).rectTransform.Stretch();
            UI.Img(plank, Sprites.Rounded, Skin.Plank, "Face", 1.4f).rectTransform.Stretch(0, 12, 0, 0);
            var gloss = UI.Img(plank, Sprites.Rounded, new Color(1f, 1f, 1f, 0.22f), "Gloss", 2f);
            gloss.rectTransform.anchorMin = new Vector2(0, 0.55f); gloss.rectTransform.anchorMax = Vector2.one;
            gloss.rectTransform.offsetMin = new Vector2(20, 0); gloss.rectTransform.offsetMax = new Vector2(-20, -8);
            var t = UI.Label(plank, title, 60, Color.white, TextAnchor.MiddleCenter);
            t.rectTransform.Stretch(0, 14, 0, 0);
            UI.Outlined(t);

            var x = CloseButton(root, 92, () => ZWordApp.I.ClosePopups());
            ((RectTransform)x.transform).Place(new Vector2(1, 1), new Vector2(-6, 0), new Vector2(92, 92));

            Tween.PopIn(root, 0.3f);
            var content = UI.Rect("Content", body.transform).Stretch(0, 0, 0, 30);
            return content;
        }

        /// <summary>
        /// Full-screen page shown in the popup layer (so it also works on top of a running level):
        /// wood background, leaf corners and the standard header. Back / Escape closes it.
        /// </summary>
        public static RectTransform FullPanel(string title, Action onClose = null, Action onBack = null)
        {
            var overlay = ZWordApp.I.NewPopup(title, onClose);
            var root = UI.Rect("Page_" + title, overlay).Stretch();
            AppBackground(root);
            var leaf = (Sprite)null;
            if (leaf != null)
            {
                void Corner(Vector2 anchor, Vector2 scale)
                {
                    var img = UI.Img(root, leaf, Color.white, "Leaf");
                    img.rectTransform.anchorMin = img.rectTransform.anchorMax = anchor;
                    img.rectTransform.pivot = Vector2.zero;
                    img.rectTransform.sizeDelta = new Vector2(300, 300);
                    img.rectTransform.anchoredPosition = Vector2.zero;
                    img.rectTransform.localScale = new Vector3(scale.x, scale.y, 1);
                }
                Corner(new Vector2(0, 0), new Vector2(1, 1));
                Corner(new Vector2(1, 0), new Vector2(-1, 1));
                Corner(new Vector2(0, 1), new Vector2(1, -1));
                Corner(new Vector2(1, 1), new Vector2(-1, -1));
            }
            Header(root, title, null, onBack ?? (() => ZWordApp.I.ClosePopups()), gear: false);
            var cg = root.gameObject.AddComponent<CanvasGroup>();
            Tween.Fade(cg, 0f, 1f, 0.2f);
            return root;
        }

        /// <summary>The shared sky background (gradient, clouds, faint honeycomb) used behind every screen.</summary>
        public static void AppBackground(RectTransform parent)
        {
            // container runs under the notch / home bar; the image inside keeps its aspect-fill
            var holder = UI.Rect("SkyHolder", parent).Stretch();
            SafeAreaBleed.Add(holder);
            var tex = Resources.Load<Texture2D>("UI/app_bg");
            if (tex == null) { UI.Img(holder, null, Palette.Hex("A9C9F6"), "Sky").rectTransform.Stretch(); return; }
            var go = new GameObject("Sky", typeof(RectTransform), typeof(RawImage));
            var rt = (RectTransform)go.transform;
            rt.SetParent(holder, false);
            rt.Stretch();
            var raw = go.GetComponent<RawImage>();
            raw.texture = tex;
            raw.raycastTarget = false;
            var fit = go.AddComponent<AspectRatioFitter>();
            fit.aspectMode = AspectRatioFitter.AspectMode.EnvelopeParent;
            fit.aspectRatio = (float)tex.width / tex.height;
        }

        /// <summary>Single-line text field (player name).</summary>
        public static TMP_InputField TextInput(Transform parent, Vector2 size, string value, string placeholder, int maxChars, Action<string> onDone)
        {
            var root = UI.Rect("Input", parent);
            root.sizeDelta = size;
            var bg = UI.Img(root, Sprites.Rounded, new Color(1, 1, 1, 0.0f), "Bg", 2f);
            bg.rectTransform.Stretch();
            bg.raycastTarget = true;
            var area = UI.Rect("TextArea", root).Stretch(6, 0, 6, 0);
            area.gameObject.AddComponent<RectMask2D>();
            var ph = UI.Label(area, placeholder, size.y * 0.62f, new Color(Skin.InkSoft.r, Skin.InkSoft.g, Skin.InkSoft.b, 0.6f), TextAnchor.MiddleLeft, false);
            ph.rectTransform.Stretch();
            var txt = UI.Label(area, "", size.y * 0.62f, Skin.Ink, TextAnchor.MiddleLeft, false);
            txt.rectTransform.Stretch();
            var input = root.gameObject.AddComponent<TMP_InputField>();
            input.textViewport = area;
            input.textComponent = txt;
            input.placeholder = ph;
            input.targetGraphic = bg;
            input.characterLimit = maxChars;
            input.lineType = TMP_InputField.LineType.SingleLine;
            input.fontAsset = Fonts.Asset;
            input.pointSize = size.y * 0.62f;
            input.customCaretColor = true;
            input.caretColor = Skin.Ink;
            input.selectionColor = new Color(1f, 0.8f, 0.3f, 0.5f);
            input.text = value;
            input.onEndEdit.AddListener(v => onDone?.Invoke(v));
            return input;
        }

        /// <summary>Settings-style row: small coloured icon tile, label, and a right-side widget area.</summary>
        public static RectTransform ListRow(Transform parent, Sprite icon, Color iconBg, string label, float y, float width = 820)
        {
            var row = UI.Rect("Row_" + label, parent).Place(new Vector2(0.5f, 1), new Vector2(0, y), new Vector2(width, 96));
            var tile = UI.Rect("IconTile", row).Place(new Vector2(0, 0.5f), new Vector2(46, 0), new Vector2(68, 68));
            UI.Img(tile, Sprites.Rounded, iconBg, "Bg", 3f).rectTransform.Stretch();
            if (icon != null)
            {
                var ic = UI.Img(tile, icon, Color.white, "Icon");
                ic.rectTransform.Stretch(12, 12, 12, 12);
                ic.preserveAspect = true;
            }
            var t = UI.Label(row, label, 38, Skin.Ink, TextAnchor.MiddleLeft, false);
            t.rectTransform.Stretch(100, 0, 220, 0);
            return row;
        }

        /// <summary>Thin divider line inside cards.</summary>
        public static void Divider(Transform parent, float y, float width = 780)
        {
            var d = UI.Img(parent, null, new Color(0.55f, 0.4f, 0.25f, 0.18f), "Divider");
            d.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, y), new Vector2(width, 3));
        }

        /// <summary>Red ribbon banner with folded tails (LEVEL COMPLETE! / LEVEL FAILED).</summary>
        public static RectTransform Ribbon(Transform parent, string text, float width, Color? color = null)
        {
            var c = color ?? Palette.Hex("E23B3B");
            var root = UI.Rect("Ribbon", parent);
            root.sizeDelta = new Vector2(width, 120);
            var dark = Palette.Darken(c, 0.62f);

            var lt = UI.Img(root, Sprites.RibbonTail, Palette.Darken(c, 0.78f), "TailL");
            lt.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(20, -24), new Vector2(150, 96));
            var rtail = UI.Img(root, Sprites.RibbonTail, Palette.Darken(c, 0.78f), "TailR");
            rtail.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-20, -24), new Vector2(150, 96));
            rtail.rectTransform.localScale = new Vector3(-1, 1, 1);
            var fl = UI.Img(root, null, dark, "FoldL");
            fl.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(84, -42), new Vector2(36, 30));
            fl.rectTransform.localRotation = Quaternion.Euler(0, 0, 35);
            var fr = UI.Img(root, null, dark, "FoldR");
            fr.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-84, -42), new Vector2(36, 30));
            fr.rectTransform.localRotation = Quaternion.Euler(0, 0, -35);

            var band = UI.Rect("Band", root).Stretch(70, 10, 70, 0);
            UI.Img(band, Sprites.Rounded, dark, "Base", 2f).rectTransform.Stretch();
            UI.Img(band, Sprites.Rounded, c, "Face", 2f).rectTransform.Stretch(0, 8, 0, 0);
            var gloss = UI.Img(band, Sprites.Rounded, new Color(1, 1, 1, 0.18f), "Gloss", 3f);
            gloss.rectTransform.anchorMin = new Vector2(0, 0.6f);
            gloss.rectTransform.anchorMax = Vector2.one;
            gloss.rectTransform.offsetMin = new Vector2(12, 0);
            gloss.rectTransform.offsetMax = new Vector2(-12, -6);
            var t = UI.Label(band, text, 64, Color.white, TextAnchor.MiddleCenter);
            t.rectTransform.Stretch(10, 12, 10, 0);
            UI.Outlined(t);
            return root;
        }

        // ---------------- decorations ----------------

        /// <summary>A bunch of leaves fanning out from a point; rotate/flip the returned rect to place it.</summary>
        public static RectTransform LeafCluster(Transform parent, float scale = 1f)
        {
            var root = UI.Rect("Leaves", parent);
            root.sizeDelta = new Vector2(10, 10);
            var greens = new[] { Palette.Hex("2F7426"), Palette.Hex("3E8E2F"), Palette.Hex("4FA83A"), Palette.Hex("5DBB45"), Palette.Hex("3A8530") };
            var angles = new[] { -75f, -40f, -8f, 24f, 58f };
            var lengths = new[] { 150f, 190f, 210f, 180f, 140f };
            for (int i = 0; i < angles.Length; i++)
            {
                var holder = UI.Rect("Leaf" + i, root);
                holder.anchoredPosition = Vector2.zero;
                holder.localRotation = Quaternion.Euler(0, 0, angles[i]);
                float L = lengths[i] * scale, W = L * 0.6f;
                var leaf = UI.Img(holder, Sprites.Leaf, greens[i], "Shape");
                leaf.rectTransform.pivot = new Vector2(0.5f, 0f);
                leaf.rectTransform.anchoredPosition = Vector2.zero;
                leaf.rectTransform.sizeDelta = new Vector2(W, L);
                if (Theme.Current.leaf == null)
                {
                    var vein = UI.Img(leaf.transform, Sprites.LeafVein, new Color(1f, 1f, 0.8f, 0.25f), "Vein");
                    vein.rectTransform.Stretch();
                }
            }
            return root;
        }

        /// <summary>Leaf clusters in the four corners of a screen (behind interactive UI).</summary>
        public static void LeafCorners(RectTransform parent, float scale = 1f)
        {
            void Corner(Vector2 anchor, float rot)
            {
                var c = LeafCluster(parent, scale);
                c.anchorMin = c.anchorMax = anchor;
                c.anchoredPosition = Vector2.zero;
                c.localRotation = Quaternion.Euler(0, 0, rot);
            }
            Corner(new Vector2(0, 1), -135f);
            Corner(new Vector2(1, 1), 135f);
            Corner(new Vector2(0, 0), -45f);
            Corner(new Vector2(1, 0), 45f);
        }

        /// <summary>Cream letter tile (logo decoration, tutorial).</summary>
        public static RectTransform LetterTile(Transform parent, string letter, float size, float rotation)
        {
            var root = UI.Rect("Tile_" + letter, parent);
            root.sizeDelta = new Vector2(size, size);
            root.localRotation = Quaternion.Euler(0, 0, rotation);
            UI.Img(root, Sprites.Rounded, Palette.Hex("EDBE62"), "Base", 128f / size * 0.45f).rectTransform.Stretch(0, -size * 0.1f, 0, size * 0.1f);
            UI.Img(root, Sprites.Rounded, Palette.Hex("FBE6C4"), "Face", 128f / size * 0.45f).rectTransform.Stretch();
            var t = UI.Label(root, letter, size * 0.62f, Palette.Hex("C9780A"), TextAnchor.MiddleCenter);
            t.rectTransform.Stretch(0, size * 0.04f, 0, 0);
            return root;
        }

        /// <summary>The Word Z logo: gold "WORD" over a big cream "Z", floating letter tiles and leaves.</summary>
        public static RectTransform Logo(Transform parent, float scale = 1f)
        {
            var root = UI.Rect("Logo", parent);
            root.sizeDelta = new Vector2(760, 520) * scale;

            if (Theme.Current.logo != null)
            {
                var img = UI.Img(root, Theme.Current.logo, Color.white, "LogoArt");
                img.rectTransform.Stretch();
                img.preserveAspect = true;
                return root;
            }

            var leftLeaves = LeafCluster(root, 0.75f * scale);
            leftLeaves.anchorMin = leftLeaves.anchorMax = new Vector2(0.18f, 0.32f);
            leftLeaves.localRotation = Quaternion.Euler(0, 0, 70);
            var rightLeaves = LeafCluster(root, 0.75f * scale);
            rightLeaves.anchorMin = rightLeaves.anchorMax = new Vector2(0.82f, 0.3f);
            rightLeaves.localRotation = Quaternion.Euler(0, 0, -70);

            var word = UI.Label(root, "WORD", 190 * scale, Color.white, TextAnchor.MiddleCenter);
            word.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 110 * scale), new Vector2(760 * scale, 200 * scale));
            UI.Outlined(word);
            word.enableVertexGradient = true;
            word.colorGradient = new VertexGradient(Palette.Hex("FFF06A"), Palette.Hex("FFF06A"), Palette.Hex("F7A21B"), Palette.Hex("F7A21B"));
            word.characterSpacing = -4;

            var z = UI.Label(root, "Z", 300 * scale, Color.white, TextAnchor.MiddleCenter);
            z.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -105 * scale), new Vector2(400 * scale, 300 * scale));
            UI.Outlined(z);
            z.enableVertexGradient = true;
            z.colorGradient = new VertexGradient(Palette.Hex("FFFFFF"), Palette.Hex("FFFFFF"), Palette.Hex("F1D7A8"), Palette.Hex("F1D7A8"));
            z.rectTransform.localRotation = Quaternion.Euler(0, 0, -4);

            void Tile(string l, Vector2 pos, float rot, float phase)
            {
                var t = LetterTile(root, l, 110 * scale, rot);
                t.anchoredPosition = pos * scale;
                var bob = t.gameObject.AddComponent<Bobber>();
                bob.Phase = phase;
                bob.Amplitude = 9 * scale;
            }
            Tile("A", new Vector2(-300, 230), 12, 0f);
            Tile("C", new Vector2(300, 220), -14, 1.7f);
            Tile("W", new Vector2(-280, -150), -10, 3.1f);
            return root;
        }

        /// <summary>Colour icon from Resources/HomeIcons (dock, badges, streak flame...), or the fallback.</summary>
        public static Sprite HomeIcon(string name, Sprite fallback)
        {
            var sp = Resources.Load<Sprite>("HomeIcons/" + name);
            return sp != null ? sp : fallback;
        }

        public static string Slug(string name) => name.ToLowerInvariant().Replace(" & ", "_").Replace(' ', '_');

        /// <summary>Category icon: themed art, or a white disc with the category's first letter.</summary>
        public static RectTransform CategoryIcon(Transform parent, Category cat, float size)
        {
            var root = UI.Rect("CatIcon", parent);
            root.sizeDelta = new Vector2(size, size);
            var art = Theme.Current.ArtFor(cat.Name);
            if (art != null && art.icon != null)
            {
                var img = UI.Img(root, art.icon, Color.white, "Icon");
                img.rectTransform.Stretch();
                img.preserveAspect = true;
                return root;
            }
            UI.Img(root, Sprites.CircleSprite, new Color(0, 0, 0, 0.18f), "Shadow").rectTransform.Stretch(0, -5, 0, 5);
            UI.Img(root, Sprites.CircleSprite, Color.white, "Disc").rectTransform.Stretch();
            var t = UI.Label(root, cat.Name.Substring(0, 1), size * 0.56f, cat.Color, TextAnchor.MiddleCenter, false);
            t.rectTransform.Stretch(0, size * 0.04f, 0, 0);
            return root;
        }
    }
}
