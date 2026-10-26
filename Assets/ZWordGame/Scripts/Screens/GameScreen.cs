using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>The main play screen: timer HUD, hex board, word slots, bonus words and boosters.</summary>
    public class GameScreen : MonoBehaviour
    {
        // Star rating: finishing = 1 star; 2 stars with a quarter of the time left, 3 stars with half of it left.
        public const float RatingSlope = 4f;
        static readonly float[] StarAt = { 0f, 1f / RatingSlope, 2f / RatingSlope };
        const int BonusCoins = 5;

        class SlotRow
        {
            public PlacedWord Word;
            public List<Image> Boxes = new List<Image>();
            public List<TMP_Text> Letters = new List<TMP_Text>();
        }

        RectTransform root;
        Level level;
        HexBoard board;
        float timeLeft, elapsed;
        bool running, paused;
        int wordScore, bonusScore;
        readonly HashSet<string> bonusFound = new HashSet<string>();
        int lastTickSecond = -1;

        // HUD
        RectTransform hud, barTrack, barFill, timePill;
        Image barFillImg;
        TMP_Text timeText, wordsText;
        readonly Image[] starIcons = new Image[3];
        readonly bool[] starLit = { true, true, true };
        float shownFrac = 1f;

        // Preview / slots / boosters
        RectTransform previewRoot;
        TMP_Text previewText;
        Image previewBg;
        readonly List<SlotRow> slots = new List<SlotRow>();
        readonly Dictionary<Booster, TMP_Text> badges = new Dictionary<Booster, TMP_Text>();
        readonly Dictionary<Booster, RectTransform> boosterButtons = new Dictionary<Booster, RectTransform>();

        static readonly Color StarGold = Palette.Hex("FFD02E");
        static readonly Color StarLost = new Color(0.55f, 0.5f, 0.5f, 0.75f);
        RectTransform hintsButton, rotateButton;
        TMP_Text hintsBadge;

        // Relax mode (no timer; stars come from hints used) and the tutorial hooks
        bool relax;
        int hintsUsed;
        float lastFoundTime = -99f;
        int combo;
        bool hasGold;
        Hex goldHex;
        int goldGems, newBookWords;
        RectTransform comboMeter, comboFill;
        TMPro.TMP_Text comboText;
        bool IsBoss => !DailyMode && !TutorialMode && LevelDatabase.IsBoss(level.CategoryIndex, level.LevelIndex);
        public bool TutorialMode { get; private set; }
        public bool DailyMode { get; private set; }
        public event System.Action<PlacedWord> WordFound;
        public event System.Action Rotated;
        public event System.Action<Booster> BoosterUsed;
        public System.Action TutorialWin, TutorialSkip;
        public HexBoard Board => board;
        public Level CurrentLevel => level;
        public RectTransform RotateButton => rotateButton;
        public RectTransform BoosterButton(Booster b) => boosterButtons.TryGetValue(b, out var r) ? r : null;

        public static GameScreen Build(RectTransform root, int cat, int lvl) =>
            BuildCustom(root, LevelVariant.For(cat, lvl), false);

        public static GameScreen BuildCustom(RectTransform root, Level level, bool tutorial, bool daily = false)
        {
            var gs = root.gameObject.AddComponent<GameScreen>();
            gs.root = root;
            gs.level = level;
            gs.TutorialMode = tutorial;
            gs.DailyMode = daily;
            gs.relax = tutorial || Save.Data.relaxMode;
            gs.BuildUI();
            return gs;
        }

#if UNITY_EDITOR || DEVELOPMENT_BUILD
        // ---- test hooks (smoke test) ----
        public bool DebugFindNextWord()
        {
            var w = level.Words.FirstOrDefault(x => !x.Found);
            if (w == null || !running) return false;
            OnSelectionCompleted(new List<Hex>(w.Path));
            return true;
        }

        public void DebugRunOutOfTime()
        {
            if (!relax && running) timeLeft = 0.05f;
        }
#endif

        static string Slug(string category) => category.ToLowerInvariant().Replace(" & ", "_").Replace(' ', '_');

        /// <summary>The category's own scenery (a soft, blurred copy of its map) instead of plain wood.</summary>
        void BuildBackdrop()
        {
            var tex = Resources.Load<Texture2D>("GameBg/bg_" + Slug(level.Category.Name));
            if (tex == null) return;
            var go = new GameObject("Backdrop", typeof(RectTransform), typeof(RawImage));
            var rt = (RectTransform)go.transform;
            rt.SetParent(root, false);
            rt.SetAsFirstSibling();
            rt.anchorMin = new Vector2(0, 1);
            rt.anchorMax = new Vector2(1, 1);
            rt.pivot = new Vector2(0.5f, 1);
            float h = 1080f * tex.height / Mathf.Max(1, tex.width);
            rt.sizeDelta = new Vector2(0, Mathf.Max(h, 2700f)); // tall enough to also cover notch + home bar
            rt.anchoredPosition = Vector2.zero;
            var raw = go.GetComponent<RawImage>();
            raw.texture = tex;
            raw.raycastTarget = false;
            // gentle tint + vignette so the tiles and text always read well
            var tint = UI.Img(root, null, new Color(0.12f, 0.05f, 0.1f, 0.18f), "Tint");
            tint.rectTransform.Stretch();
            tint.raycastTarget = false;
            tint.transform.SetSiblingIndex(1);
            var vig = UI.Img(root, Sprites.Vignette, new Color(0.15f, 0.05f, 0.12f, 0.7f), "Vignette");
            vig.rectTransform.Stretch(-80, -80, -80, -80);
            vig.raycastTarget = false;
            vig.transform.SetSiblingIndex(2);
            // run the art under the notch / home bar too (the HUD stays in the safe area)
            SafeAreaBleed.Add(rt);
            SafeAreaBleed.Add(tint.rectTransform);
            SafeAreaBleed.Add(vig.rectTransform);
        }

        void BuildUI()
        {
            var cat = level.Category;
            BuildBackdrop();
            if (TutorialMode) ZWordApp.Header(root, "HOW TO PLAY", null, () => TutorialSkip?.Invoke());
            else if (DailyMode) ZWordApp.Header(root, "DAILY", System.DateTime.Now.ToString("MMM d").ToUpperInvariant(), OpenPause);
            else ZWordApp.Header(root, cat.Name, IsBoss ? "BOSS" : "LV " + (level.LevelIndex + 1), OpenPause);

            BuildHud();
            BuildComboMeter();

            // under the bar: rotate (left) and hints (right), mockup screen 4
            var rotate = Widgets.RoundButton(root, Sprites.RotateArrow, 92, Skin.Wood, () => { board.Rotate(); Rotated?.Invoke(); if (!TutorialMode) Challenges.Report(Metric.Rotate, 1); }, 0.55f);
            rotateButton = (RectTransform)rotate.transform;
            rotateButton.Place(new Vector2(0, 1), new Vector2(84, -372), new Vector2(92, 92));

            var bulb = Theme.Current.iconBulb != null ? Theme.Current.iconBulb : Sprites.BulbGlyph;
            var hints = Widgets.RoundButton(root, bulb, 92, Skin.Wood, OpenHints, 0.66f);
            hintsButton = (RectTransform)hints.transform;
            hintsButton.Place(new Vector2(1, 1), new Vector2(-84, -372), new Vector2(92, 92));

            // Current word preview bubble
            previewRoot = UI.Rect("Preview", root).Place(new Vector2(0.5f, 1), new Vector2(0, -372), new Vector2(200, 84));
            previewBg = UI.Img(previewRoot, Sprites.Rounded, Color.white, "Bg", 1.2f);
            previewBg.rectTransform.Stretch();
            previewText = UI.Label(previewRoot, "", 54, Palette.Brown, TextAnchor.MiddleCenter, false);
            previewText.rectTransform.Stretch();
            previewRoot.gameObject.SetActive(false);

            BuildBoosters();
            float slotsTop = BuildSlots();

            // Fit the board between the preview row and the word slots.
            Canvas.ForceUpdateCanvases();
            float H = root.rect.height > 100 ? root.rect.height : 1920f;
            const float topReserved = 430f;
            float bottomReserved = slotsTop + 24f;
            float availH = Mathf.Max(300f, H - topReserved - bottomReserved);
            float radius = HexBoard.FitRadius(level, 1000f, availH, 100f);

            // soft shadow plate behind the board so it stands out on any scenery
            var ext = HexBoard.Extents(level, radius);
            var plate = UI.Img(root, Sprites.Soft, new Color(0.3f, 0.16f, 0.04f, 0.42f), "BoardPlate");
            plate.rectTransform.anchorMin = plate.rectTransform.anchorMax = new Vector2(0.5f, 0f);
            plate.rectTransform.sizeDelta = ext * 1.45f + new Vector2(120, 120);
            plate.rectTransform.anchoredPosition = new Vector2(0, bottomReserved + availH * 0.5f);
            plate.raycastTarget = false;

            board = HexBoard.Create(root, level, radius);
            var brt = (RectTransform)board.transform;
            brt.anchorMin = brt.anchorMax = new Vector2(0.5f, 0f);
            brt.anchoredPosition = new Vector2(0, bottomReserved + availH * 0.5f);
            board.SelectionChanged += OnSelectionChanged;
            board.SelectionCompleted += OnSelectionCompleted;
            rotate.gameObject.SetActive(board.CanRotate);

            // golden hex: sometimes one tile is gold; the word through it pays a gem
            if (!TutorialMode && GoldenHex.Roll())
            {
                goldHex = level.Cells[Random.Range(0, level.Cells.Count)];
                hasGold = true;
                board.SetGolden(goldHex);
                Tween.Value(0.01f, _ => { }, null, 0.9f, () => { if (this && running) ZWordApp.Toast(root, "FIND THE GOLDEN HEX!", new Vector2(0, 300), Palette.Hex("FFD02E")); });
            }
            if (IsBoss)
                Tween.Value(0.01f, _ => { }, null, 0.5f, () => { if (this && running) ZWordApp.Toast(root, "BOSS BOARD!", new Vector2(0, 420), Skin.Gold); });

            timeLeft = level.TimeLimit;
            running = true;
            UpdateHud(true);
            RefreshBadges();
            ZWordApp.I.OnBack = OpenPause;
        }

        // ---------------- HUD: cream bar with gold fill, stars on the bar, seconds bubble ----------------

        void BuildHud()
        {
            hud = UI.Rect("Hud", root).Place(new Vector2(0.5f, 1), new Vector2(-40, -250), new Vector2(860, 60));

            barTrack = hud;
            UI.Img(hud, Sprites.Rounded, Skin.WoodDark, "Rim", 2f).rectTransform.Stretch(-9, -12, -9, -7);
            UI.Img(hud, Sprites.Rounded, Skin.Cream, "Track", 2f).rectTransform.Stretch();

            barFill = UI.Rect("Fill", hud);
            barFill.anchorMin = Vector2.zero;
            barFill.anchorMax = Vector2.one;
            barFill.offsetMin = new Vector2(6, 6);
            barFill.offsetMax = new Vector2(-6, -6);
            barFillImg = UI.Img(barFill, Sprites.Rounded, Skin.Gold, "FillImg", 2.4f);
            barFillImg.rectTransform.Stretch();
            var gloss = UI.Img(barFill, Sprites.Rounded, new Color(1, 1, 1, 0.35f), "Gloss", 4f);
            gloss.rectTransform.anchorMin = new Vector2(0, 0.55f);
            gloss.rectTransform.anchorMax = Vector2.one;
            gloss.rectTransform.offsetMin = new Vector2(8, 0);
            gloss.rectTransform.offsetMax = new Vector2(-8, -3);

            // Star markers sit where the fill must stay to keep that star.
            var starSprite = Theme.Current.iconStar != null ? Theme.Current.iconStar : Sprites.Star;
            for (int i = 0; i < 3; i++)
            {
                float at = i == 0 ? 0.05f : StarAt[i];
                var holder = UI.Rect("Star" + (i + 1), hud);
                holder.anchorMin = holder.anchorMax = new Vector2(at, 0.5f);
                holder.pivot = new Vector2(0.5f, 0.5f);
                holder.sizeDelta = new Vector2(86, 86);
                holder.anchoredPosition = new Vector2(0, 4);
                starIcons[i] = UI.Img(holder, starSprite, Color.white, "Icon");
                starIcons[i].rectTransform.Stretch();
            }

            // seconds bubble at the right end
            timePill = UI.Rect("Time", hud).Place(new Vector2(1, 0.5f), new Vector2(30, 0), new Vector2(104, 104));
            UI.Img(timePill, Sprites.CircleSprite, Skin.WoodDark, "Rim").rectTransform.Stretch(-7, -9, -7, -5);
            UI.Img(timePill, Sprites.CircleSprite, Color.white, "Bg").rectTransform.Stretch();
            timeText = UI.Label(timePill, "0", 44, Skin.Ink, TextAnchor.MiddleCenter, false);
            timeText.rectTransform.Stretch(0, 3, 0, 0);
        }

        void UpdateHud(bool instant = false)
        {
            if (relax) { UpdateRelaxHud(instant); return; }
            float frac = Mathf.Clamp01(timeLeft / level.TimeLimit);
            shownFrac = instant ? frac : Mathf.MoveTowards(shownFrac, frac, Time.unscaledDeltaTime * 0.8f + Mathf.Abs(frac - shownFrac) * 0.15f);
            barFill.anchorMax = new Vector2(Mathf.Max(shownFrac, 0.001f), 1);
            barFill.gameObject.SetActive(shownFrac > 0.002f);

            // gold, turning orange then red when time runs low
            barFillImg.color = frac > 0.3f ? Skin.Gold : Color.Lerp(Palette.Hex("FF5A3C"), Palette.Hex("FF9A1F"), frac / 0.3f);

            int secs = Mathf.CeilToInt(Mathf.Max(0, timeLeft));
            timeText.text = secs.ToString();
            bool urgent = timeLeft <= 10f && timeLeft > 0f;
            timeText.color = urgent ? Palette.Red : Palette.Brown;

            if (urgent && secs != lastTickSecond && !instant)
            {
                lastTickSecond = secs;
                AudioManager.Tick(secs <= 5);
                Tween.Punch(timePill, 0.12f, 0.2f);
            }

            for (int i = 0; i < 3; i++)
            {
                bool lit = i == 0 ? timeLeft > 0f : frac >= StarAt[i];
                if (lit == starLit[i]) continue;
                starLit[i] = lit;
                starIcons[i].color = lit ? Color.white : StarLost;
                if (!lit && !instant) DropStar(i);
                else if (lit && !instant) Tween.Punch(starIcons[i].transform.parent, 0.35f, 0.3f);
            }
        }

        /// <summary>Relax mode: the bar shows words found; stars are lost by using hints (3 = none, 2 = up to 2).</summary>
        int RelaxStars => hintsUsed == 0 ? 3 : hintsUsed <= 2 ? 2 : 1;

        void UpdateRelaxHud(bool instant)
        {
            int found = level.Words.Count(w => w.Found);
            float frac = Mathf.Clamp01(found / (float)Mathf.Max(1, level.Words.Count));
            shownFrac = instant ? frac : Mathf.MoveTowards(shownFrac, frac, Time.unscaledDeltaTime * 1.5f);
            barFill.anchorMax = new Vector2(Mathf.Max(shownFrac, 0.001f), 1);
            barFill.gameObject.SetActive(shownFrac > 0.002f);
            barFillImg.color = Skin.Gold;
            timeText.text = found + "/" + level.Words.Count;
            timeText.fontSize = level.Words.Count >= 10 ? 30 : 36;
            timeText.color = Palette.Brown;
            for (int i = 0; i < 3; i++)
            {
                bool lit = RelaxStars > i;
                if (lit == starLit[i]) continue;
                starLit[i] = lit;
                starIcons[i].color = lit ? Color.white : StarLost;
                if (!lit && !instant) DropStar(i);
            }
        }

        /// <summary>A lost star falls off the bar and fades, leaving an empty slot behind.</summary>
        void DropStar(int i)
        {
            AudioManager.StarLost();
            var src = (RectTransform)starIcons[i].transform.parent;
            var ghost = UI.Img(hud, starIcons[i].sprite, Color.white, "FallingStar");
            ghost.rectTransform.sizeDelta = src.sizeDelta;
            ghost.rectTransform.position = src.position;
            var start = ghost.rectTransform.anchoredPosition;
            float spin = Random.Range(-200f, 200f);
            Tween.Value(0.7f, k =>
            {
                if (!ghost) return;
                ghost.rectTransform.anchoredPosition = start + new Vector2(spin * 0.15f * k, -160f * k * k + 30f * k);
                ghost.rectTransform.localRotation = Quaternion.Euler(0, 0, spin * k);
                ghost.color = new Color(1f, 1f, 1f, 1f - k);
            }, null, 0, () => { if (ghost) Destroy(ghost.gameObject); });
            Tween.Shake(src, 6f, 0.25f);
        }

        void UpdateWordsCounter()
        {
            if (wordsText == null || level == null) return;
            wordsText.text = level.Words.Count(w => w.Found) + "/" + level.Words.Count;
        }

        void Update()
        {
            if (!running) return;
            bool popup = ZWordApp.I != null && ZWordApp.I.PopupOpen;
            board.Interactable = !popup && !paused;
            if (paused || popup) return;

            elapsed += Time.deltaTime;
            if (!relax) timeLeft -= Time.deltaTime;
            UpdateHud();
            UpdateComboMeter();
            if (!relax && timeLeft <= 0f) OutOfTime();
        }

        // ---------------- Word slots ----------------

        /// <summary>Builds the answer slots above the boosters; returns the y of their top edge (from screen bottom).</summary>
        float BuildSlots()
        {
            const float maxW = 980f, bottom = 262f;
            float box = 56, gap = 8, wordGap = 40, lineH = 70;

            List<List<PlacedWord>> Flow()
            {
                var result = new List<List<PlacedWord>>();
                var cur = new List<PlacedWord>();
                float w = 0;
                foreach (var pw in level.Words)
                {
                    float ww = pw.Word.Length * box + (pw.Word.Length - 1) * gap;
                    float add = cur.Count == 0 ? ww : ww + wordGap;
                    if (cur.Count > 0 && w + add > maxW) { result.Add(cur); cur = new List<PlacedWord>(); w = 0; add = ww; }
                    cur.Add(pw); w += add;
                }
                if (cur.Count > 0) result.Add(cur);
                return result;
            }

            var lines = Flow();
            if (lines.Count > 2)
            {
                box = 46; gap = 6; wordGap = 30; lineH = 58;
                lines = Flow();
            }

            float totalH = lines.Count * lineH;
            var panel = UI.Img(root, Sprites.Rounded, new Color(0.3f, 0.16f, 0.04f, 0.38f), "SlotsPanel", 2f);
            panel.rectTransform.anchorMin = panel.rectTransform.anchorMax = new Vector2(0.5f, 0);
            panel.rectTransform.sizeDelta = new Vector2(maxW + 40, totalH + 34);
            panel.rectTransform.anchoredPosition = new Vector2(0, bottom + totalH * 0.5f);
            panel.raycastTarget = false;
            var area = UI.Rect("Slots", root);
            area.anchorMin = area.anchorMax = new Vector2(0.5f, 0);
            area.sizeDelta = new Vector2(maxW, totalH);
            area.anchoredPosition = new Vector2(0, bottom + totalH * 0.5f);

            for (int li = 0; li < lines.Count; li++)
            {
                var line = lines[li];
                float lineW = line.Sum(p => p.Word.Length * box + (p.Word.Length - 1) * gap) + (line.Count - 1) * wordGap;
                float x = -lineW / 2f;
                float y = totalH / 2f - lineH * (li + 0.5f);
                foreach (var pw in line)
                {
                    var row = new SlotRow { Word = pw };
                    for (int i = 0; i < pw.Word.Length; i++)
                    {
                        var b = UI.Img(area, Sprites.Rounded, new Color(1f, 1f, 1f, 0.92f), "Box", 3.5f * 56f / box);
                        b.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(x + box / 2f, y), new Vector2(box, box));
                        var sh = b.gameObject.AddComponent<Shadow>();
                        sh.effectColor = new Color(0.2f, 0.06f, 0.15f, 0.4f);
                        sh.effectDistance = new Vector2(0, -5);
                        var t = UI.Label(b.transform, "", box * 0.64f, Color.white, TextAnchor.MiddleCenter, false);
                        t.rectTransform.Stretch();
                        row.Boxes.Add(b);
                        row.Letters.Add(t);
                        x += box + gap;
                    }
                    x += wordGap - gap;
                    slots.Add(row);
                }
            }
            return bottom + totalH;
        }

        SlotRow RowFor(PlacedWord pw) => slots.First(s => s.Word == pw);

        void FillRow(PlacedWord pw)
        {
            var row = RowFor(pw);
            for (int i = 0; i < row.Boxes.Count; i++)
            {
                row.Boxes[i].color = pw.Color;
                row.Letters[i].text = pw.Word[i].ToString();
                row.Letters[i].color = Color.white;
                var tr = row.Boxes[i].transform;
                Tween.Value(0.01f, _ => { }, null, i * 0.05f, () => Tween.Punch(tr, 0.3f, 0.25f));
            }
        }

        void RevealLetter(PlacedWord pw, int index)
        {
            var row = RowFor(pw);
            row.Letters[index].text = pw.Word[index].ToString();
            row.Letters[index].color = pw.Color;
            Tween.Punch(row.Boxes[index].transform, 0.35f, 0.3f);
        }

        // ---------------- Boosters ----------------

        static readonly (Booster type, string color)[] BoosterRow =
        {
            (Booster.Letter, "FFB61E"), (Booster.Shuffle, "9B4DE0"), (Booster.Time, "2F9BEA"), (Booster.Reveal, "4CC23A")
        };

        static Sprite BoosterIcon(Booster b)
        {
            var t = Theme.Current;
            switch (b)
            {
                case Booster.Letter: return t.iconLetter != null ? t.iconLetter : Sprites.Letters;
                case Booster.Shuffle: return t.iconShuffle != null ? t.iconShuffle : Sprites.ShuffleGlyph;
                case Booster.Time: return t.iconClock != null ? t.iconClock : Sprites.Clock;
                case Booster.Reveal: return t.iconMagnifier != null ? t.iconMagnifier : Sprites.Magnifier;
                case Booster.Starts: return t.iconWand != null ? t.iconWand : Sprites.TargetGlyph;
                default: return Sprites.Star;
            }
        }

        void BuildBoosters()
        {
            for (int i = 0; i < BoosterRow.Length; i++)
            {
                var (type, hex) = BoosterRow[i];
                var color = Palette.Hex(hex);
                var b = UI.Chunky(root, new Vector2(156, 156), color, null, 0, () => UseBooster(type), Sprites.CircleSprite, 1f, 12);
                var brt = (RectTransform)b.transform;
                brt.Place(new Vector2(0.5f, 0), new Vector2(-330 + i * 220, 128), new Vector2(156, 156));
                var face = brt.Find("Body/Face");
                var disc = UI.Img(face, Sprites.CircleSprite, new Color(1, 1, 1, 0.92f), "Disc");
                disc.rectTransform.Stretch(16, 16, 16, 16);
                var ic = UI.Img(face, BoosterIcon(type), Color.white, "Icon");
                ic.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(92, 92));
                ic.preserveAspect = true;
                boosterButtons[type] = brt;

                var badge = UI.Rect("Badge", brt).Place(new Vector2(1, 1), new Vector2(-14, -14), new Vector2(52, 52));
                UI.Img(badge, Sprites.CircleSprite, Color.white, "Rim").rectTransform.Stretch();
                UI.Img(badge, Sprites.CircleSprite, Skin.Red, "Dot").rectTransform.Stretch(4, 4, 4, 4);
                var bt = UI.Label(badge, "", 30, Color.white, TextAnchor.MiddleCenter, false);
                bt.rectTransform.Stretch(0, 2, 0, 0);
                badges[type] = bt;
                Tween.PopIn(brt, 0.3f, 0.3f + i * 0.06f);
            }
        }

        void RefreshBadges()
        {
            foreach (var kv in badges)
            {
                int n = Save.GetBooster(kv.Key);
                kv.Value.text = n > 0 ? n.ToString() : "+";
            }
        }

        /// <summary>Bottom row: use a booster from the inventory, or open the Hints shop when empty.</summary>
        void UseBooster(Booster type)
        {
            if (!running) return;
            if (TutorialMode)
            {
                if (ApplyHint(type)) { Tween.Punch(boosterButtons[type], 0.15f); BoosterUsed?.Invoke(type); }
                return;
            }
            int count = Save.GetBooster(type);
            if (count <= 0) { OpenHints(); return; }
            if (!ApplyHint(type)) return;
            Save.SetBooster(type, count - 1);
            BoosterUsed?.Invoke(type);
            Challenges.Report(Metric.Hints, 1);
            RefreshBadges();
            Tween.Punch(boosterButtons[type], 0.15f);
        }

        /// <summary>Performs a hint. Returns false when it would do nothing (so nothing is charged).</summary>
        bool ApplyHint(Booster type)
        {
            switch (type)
            {
                case Booster.Letter:
                {
                    var pw = level.Words.Where(w => !w.Found && w.Revealed < w.Word.Length - 1)
                        .OrderBy(w => w.Revealed).FirstOrDefault();
                    if (pw == null) return Nothing("Every word already has its letters shown");
                    RevealLetter(pw, pw.Revealed);
                    board.Glow(new List<Hex> { pw.Path[pw.Revealed] }, 2f);
                    pw.Revealed++;
                    break;
                }
                case Booster.Starts:
                {
                    var starts = level.Words.Where(w => !w.Found).Select(w => w.Path[0]).ToList();
                    if (starts.Count == 0) return false;
                    board.Glow(starts, 4f, 0.1f);
                    foreach (var w in level.Words.Where(w => !w.Found && w.Revealed == 0)) { RevealLetter(w, 0); w.Revealed = 1; }
                    break;
                }
                case Booster.Shuffle:
                    if (!Shuffle()) return Nothing("Nothing left to shuffle");
                    break;
                case Booster.Time:
                    if (relax) return Nothing("No timer in Relax Mode");
                    if (timeLeft >= level.TimeLimit - 1f) return Nothing("The timer is already full");
                    timeLeft = Mathf.Min(level.TimeLimit, timeLeft + 30f);
                    Tween.Punch(timePill, 0.3f, 0.35f);
                    ZWordApp.Toast(root, "+30s", new Vector2(330, 620), Color.white);
                    break;
                case Booster.Reveal:
                {
                    var pw = level.Words.FirstOrDefault(w => !w.Found);
                    if (pw == null) return false;
                    board.Glow(pw.Path, 2.6f, 0.15f);
                    if (pw.Revealed == 0) { RevealLetter(pw, 0); pw.Revealed = 1; }
                    break;
                }
                default:
                    return false;
            }
            AudioManager.Booster();
            if (type != Booster.Time && type != Booster.Shuffle) { hintsUsed++; if (relax) UpdateHud(); }
            return true;
        }

        bool Nothing(string why)
        {
            AudioManager.Error();
            ZWordApp.Toast(root, why.ToUpperInvariant(), new Vector2(0, -560), Palette.Yellow);
            return false;
        }

        /// <summary>Re-deals the unsolved tiles with the remaining words; always stays solvable.</summary>
        bool Shuffle()
        {
            var free = level.Cells.Where(c => !IsLocked(c)).ToList();
            var rest = level.Words.Where(w => !w.Found).OrderByDescending(w => w.Word.Length).ToList();
            if (rest.Count == 0 || free.Count < 2) return false;
            for (int attempt = 0; attempt < 25; attempt++)
            {
                var paths = LevelGenerator.Tile(free, rest.Select(w => w.Word.Length).ToList(), new System.Random(Random.Range(1, int.MaxValue)));
                if (paths == null) continue;
                for (int i = 0; i < rest.Count; i++)
                {
                    rest[i].Path = paths[i];
                    for (int k = 0; k < paths[i].Count; k++) level.Letters[paths[i][k]] = rest[i].Word[k];
                }
                board.Relabel(free);
                return true;
            }
            return false;
        }

        // ---------------- popups ----------------

        static readonly (Booster type, string title, string sub, int cost)[] HintShop =
        {
            (Booster.Letter, "Reveal a Letter", "Show the next letter of a word", GameConfig.CostRevealLetter),
            (Booster.Starts, "Show Word Starts", "Light up where every word begins", GameConfig.CostWordStarts),
            (Booster.Shuffle, "Shuffle", "Re-deal the unsolved letters", GameConfig.CostShuffle),
            (Booster.Reveal, "Reveal Word", "Show the path of one word", GameConfig.CostRevealWord),
        };

        void OpenHints()
        {
            if (!running) return;
            board.ClearSelection();
            var body = Widgets.WoodPopup("HINTS", new Vector2(860, 900));

            var wallet = Widgets.CurrencyChip(body, Currency.Coins, 220);
            wallet.Place(new Vector2(0.5f, 1), new Vector2(0, -50), new Vector2(220, 66));
            wallet.GetComponentInChildren<UnityEngine.UI.Image>().color = new Color(0.36f, 0.2f, 0.06f, 0.7f);

            for (int i = 0; i < HintShop.Length; i++)
            {
                var (type, title, sub, cost) = HintShop[i];
                var row = Widgets.Card(body, new Vector2(780, 150), Color.white);
                row.Place(new Vector2(0.5f, 1), new Vector2(0, -170 - i * 168), new Vector2(780, 150));
                var ic = UI.Img(row, BoosterIcon(type), Color.white, "Icon");
                ic.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(80, 0), new Vector2(96, 96));
                ic.preserveAspect = true;
                var t = UI.Label(row, title, 40, Skin.Ink, TextAnchor.MiddleLeft, false);
                t.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(150 + 200, 22), new Vector2(400, 50));
                var st = UI.Label(row, sub, 26, Skin.InkSoft, TextAnchor.MiddleLeft, false);
                st.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(150 + 200, -24), new Vector2(400, 40));
                var buy = Widgets.PriceButton(row, new Vector2(190, 96), Currency.Coins, cost.ToString(), () => BuyHint(type, cost));
                ((RectTransform)buy.transform).Place(new Vector2(1, 0.5f), new Vector2(-114, 2), new Vector2(190, 96));
            }
        }

        void BuyHint(Booster type, int cost)
        {
            if (!running) return;
            if (Save.Coins < cost)
            {
                AudioManager.Error();
                ZWordApp.Toast(ZWordApp.I.CurrentScreen, "NOT ENOUGH COINS", new Vector2(0, 0), Palette.Yellow);
                ZWordApp.I.ShowShop(0);
                return;
            }
            ZWordApp.I.ClosePopups();
            if (ApplyHint(type))
            {
                Save.TrySpendCoins(cost);
                Challenges.Report(Metric.Hints, 1);
            }
        }

        void OpenPause()
        {
            if (!running || TutorialMode) return;
            paused = true;
            board.ClearSelection();
            var body = Widgets.WoodPopup("PAUSED", new Vector2(720, 800), () => paused = false);
            var t = Theme.Current;
            void Btn(string label, Color c, Sprite icon, float y, System.Action a)
            {
                var b = Widgets.IconTextButton(body, new Vector2(560, 124), c, label, icon, 50, a);
                ((RectTransform)b.transform).Place(new Vector2(0.5f, 1), new Vector2(0, y), new Vector2(560, 124));
            }
            Btn("RESUME", Skin.Green, t.iconPlay != null ? t.iconPlay : Sprites.Play, -110, () => ZWordApp.I.ClosePopups());
            Btn("RESTART", Skin.Wood, t.iconRestart != null ? t.iconRestart : Sprites.RotateArrow, -255, () =>
            {
                if (DailyMode) ZWordApp.I.StartDailyPuzzle();
                else ZWordApp.I.StartLevel(level.CategoryIndex, level.LevelIndex);
            });
            Btn("SETTINGS", Skin.Wood, t.iconGear != null ? t.iconGear : Sprites.Gear, -400, () => ZWordApp.I.OpenSettings());
            Btn("QUIT", Skin.Wood, t.iconExit != null ? t.iconExit : Sprites.ExitGlyph, -545, () =>
            {
                if (DailyMode) ZWordApp.I.ShowHome();
                else ZWordApp.I.ShowMap(level.CategoryIndex);
            });
        }

        // Auto-pause when the app is backgrounded (phone call, home button...)
        void OnApplicationPause(bool appPaused)
        {
            if (appPaused && running && !paused && !TutorialMode && ZWordApp.I != null && !ZWordApp.I.PopupOpen) OpenPause();
        }

        // ---------------- Selection handling ----------------

        void OnSelectionChanged(string word)
        {
            previewRoot.gameObject.SetActive(!string.IsNullOrEmpty(word));
            previewText.text = word;
            previewBg.color = Color.white;
            previewRoot.sizeDelta = new Vector2(Mathf.Max(120, previewText.preferredWidth + 70), 84);
        }

        void OnSelectionCompleted(List<Hex> path)
        {
            if (!running) return;
            var word = new string(path.Select(h => level.Letters[h]).ToArray());
            var candidates = level.Words.Where(w => !w.Found && w.Word == word).ToList();

            PlacedWord match = candidates.FirstOrDefault(w => w.Path.SequenceEqual(path));
            if (match == null && candidates.Count > 0)
            {
                // Spelled correctly along a different route: accept it only if the rest is still solvable.
                var free = new HashSet<Hex>(level.Cells.Where(c => !IsLocked(c)));
                foreach (var h in path) free.Remove(h);
                var rest = level.Words.Where(w => !w.Found && w != candidates[0]).ToList();
                var solution = Solver.Solve(level, free, rest.Select(w => w.Word).ToList());
                if (solution != null)
                {
                    match = candidates[0];
                    match.Path = new List<Hex>(path);
                    for (int i = 0; i < rest.Count; i++) rest[i].Path = solution[i];
                }
                else
                {
                    Wrong(path, "TRY ANOTHER PATH!");
                    return;
                }
            }

            if (match == null)
            {
                if (level.Words.Any(w => w.Found && w.Word == word)) { Wrong(path, "ALREADY FOUND"); return; }
                if (TryBonus(word, path)) return;
                Wrong(path, null);
                return;
            }

            match.Found = true;
            Save.Data.wordsFound++;
            Challenges.Report(Metric.Words, 1);
            board.MarkFound(match.Path, match.Color);
            FillRow(match);
            UpdateWordsCounter();
            int pts = match.Word.Length * 100 + Mathf.Max(0, match.Word.Length - 3) * 50;
            combo = Time.unscaledTime - lastFoundTime < GameConfig.ComboWindow ? combo + 1 : 1;
            lastFoundTime = Time.unscaledTime;
            // chain words quickly: x1.5 points for the 2nd, x2 from the 3rd (plus a couple of coins)
            float mult = combo >= 3 ? 2f : combo == 2 ? 1.5f : 1f;
            int comboPts = Mathf.RoundToInt(pts * (mult - 1f));
            if (combo >= 3 && !TutorialMode) Save.Coins += GameConfig.ComboCoins;
            wordScore += pts + comboPts;
            if (!TutorialMode && Save.RecordWord(level.CategoryIndex, match.Word)) newBookWords++;
            if (hasGold && match.Path.Contains(goldHex))
            {
                hasGold = false;
                int g = GoldenHex.Collect();
                goldGems += g;
                if (g > 0) GemBurst(match.Path);
            }
            AudioManager.Success();
            Haptics.Medium();
            ZWordApp.Toast(root, "+" + (pts + comboPts), new Vector2(0, 520), Color.white);
            Praise(match, comboPts);
            if (!TutorialMode)
            {
                if (match.Word.Length >= 6) { Save.Data.longWords++; Challenges.Report(Metric.LongWords, 1); }
                if (combo > 1) { Save.Data.combos++; Challenges.Report(Metric.Combos, 1); }
            }
            if (relax) UpdateHud();
            WordFound?.Invoke(match);

            if (level.Words.All(w => w.Found)) Win();
            else if (level.Words.Count(w => !w.Found) == 1 && level.Words.Count > 2)
                Tween.Value(0.01f, _ => { }, null, 1.0f, () => { if (this && running) ZWordApp.Toast(root, "LAST WORD!", new Vector2(0, 380), Palette.Hex("FFD02E")); });
        }

        static readonly string[] PraiseWords = { "GOOD!", "GOOD!", "GOOD!", "GOOD!", "GREAT!", "AWESOME!", "AMAZING!", "FANTASTIC!", "INCREDIBLE!" };

        /// <summary>Big tilted praise word over the board, plus a combo tag when words come quickly.</summary>
        void Praise(PlacedWord w, int comboPts)
        {
            string text = PraiseWords[Mathf.Clamp(w.Word.Length, 0, PraiseWords.Length - 1)];
            var holder = UI.Rect("Praise", root).Place(new Vector2(0.5f, 0.5f), new Vector2(0, 260), new Vector2(900, 200));
            var t = UI.Label(holder, text, w.Word.Length >= 6 ? 120 : 104, w.Color, TextAnchor.MiddleCenter);
            t.rectTransform.Stretch();
            UI.Outlined(t);
            holder.localRotation = Quaternion.Euler(0, 0, Random.Range(-6f, 6f));
            if (comboPts > 0)
            {
                var c = UI.Label(holder, (combo >= 3 ? "COMBO x2" : "COMBO x1.5") + "  +" + comboPts, 52, Palette.Hex("FFD02E"), TextAnchor.MiddleCenter);
                c.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, -20), new Vector2(800, 70));
                UI.Outlined(c);
            }
            holder.localScale = Vector3.zero;
            Tween.Value(1.3f, k =>
            {
                if (!holder) return;
                float s = k < 0.25f ? Tween.OutBack(k / 0.25f) * 1.05f : 1.05f + (k - 0.25f) * 0.12f;
                holder.localScale = Vector3.one * s;
                float a = 1f - Mathf.Clamp01((k - 0.7f) / 0.3f);
                foreach (var g in holder.GetComponentsInChildren<TMP_Text>()) g.alpha = a;
                holder.anchoredPosition = new Vector2(0, 260 + k * 40);
            }, null, 0, () => { if (holder) Destroy(holder.gameObject); });
        }

        /// <summary>Small pill under the timer: the multiplier the next word gets, with a bar draining over the combo window.</summary>
        void BuildComboMeter()
        {
            comboMeter = UI.Rect("Combo", root).Place(new Vector2(0.5f, 1), new Vector2(0, -306), new Vector2(240, 40));
            UI.Img(comboMeter, Sprites.Rounded, new Color(0.36f, 0.2f, 0.06f, 0.7f), "Bg", 2.6f).rectTransform.Stretch();
            comboFill = UI.Rect("Fill", comboMeter);
            comboFill.anchorMin = Vector2.zero;
            comboFill.anchorMax = Vector2.one;
            comboFill.offsetMin = new Vector2(4, 4);
            comboFill.offsetMax = new Vector2(-4, -4);
            UI.Img(comboFill, Sprites.Rounded, Skin.Gold, "FillImg", 3f).rectTransform.Stretch();
            comboText = UI.Label(comboMeter, "", 26, Color.white, TextAnchor.MiddleCenter);
            comboText.rectTransform.Stretch();
            UI.Outlined(comboText);
            comboMeter.gameObject.SetActive(false);
        }

        void UpdateComboMeter()
        {
            if (comboMeter == null || TutorialMode) return;
            float left = GameConfig.ComboWindow - (Time.unscaledTime - lastFoundTime);
            bool show = running && left > 0f && combo >= 1 && level.Words.Any(w => !w.Found);
            if (comboMeter.gameObject.activeSelf != show) comboMeter.gameObject.SetActive(show);
            if (!show) return;
            comboFill.anchorMax = new Vector2(Mathf.Clamp01(left / GameConfig.ComboWindow), 1);
            comboText.text = combo >= 2 ? "NEXT WORD x2!" : "NEXT WORD x1.5";
        }

        /// <summary>The golden hex pays out: gems fly from the word to the top of the screen.</summary>
        void GemBurst(List<Hex> path)
        {
            AudioManager.Bonus();
            Haptics.Success();
            ZWordApp.Toast(root, "GOLDEN HEX! +" + GameConfig.GoldenGems + " GEM", new Vector2(0, 420), Palette.Hex("FFD02E"));
            Vector2 from = root.InverseTransformPoint(board.CellWorldPos(path[path.Count / 2]));
            Vector2 to = new Vector2(0, root.rect.height * 0.5f - 120f);
            for (int i = 0; i < 4; i++)
            {
                var gem = Widgets.CurrencyIcon(root, Currency.Gems, 70);
                gem.anchorMin = gem.anchorMax = new Vector2(0.5f, 0.5f);
                gem.anchoredPosition = from;
                var spread = Random.insideUnitCircle * 160f;
                Tween.Value(0.9f, k =>
                {
                    if (!gem) return;
                    var mid = from + spread;
                    gem.anchoredPosition = Vector2.Lerp(Vector2.Lerp(from, mid, k), Vector2.Lerp(mid, to, k), k);
                    gem.localScale = Vector3.one * (k < 0.2f ? k / 0.2f : 1f);
                }, Tween.OutCubic, i * 0.08f, () => { if (gem) Destroy(gem.gameObject); });
            }
        }

        /// <summary>Coins burst out of a bonus word and fly up to the hints button.</summary>
        void CoinBurst(List<Hex> path, int count)
        {
            if (hintsButton == null) return;
            Vector2 from = root.InverseTransformPoint(board.CellWorldPos(path[path.Count / 2]));
            Vector2 to = root.InverseTransformPoint(hintsButton.position);
            for (int i = 0; i < count; i++)
            {
                var coin = Widgets.CurrencyIcon(root, Currency.Coins, 64);
                coin.anchorMin = coin.anchorMax = new Vector2(0.5f, 0.5f);
                coin.anchoredPosition = from;
                var spread = Random.insideUnitCircle * 140f;
                Tween.Value(0.75f, k =>
                {
                    if (!coin) return;
                    var mid = from + spread;
                    var p1 = Vector2.Lerp(from, mid, k);
                    var p2 = Vector2.Lerp(mid, to, k);
                    coin.anchoredPosition = Vector2.Lerp(p1, p2, k);
                    coin.localScale = Vector3.one * (k < 0.2f ? k / 0.2f : 1f - (k - 0.8f) * 2.5f * (k > 0.8f ? 1 : 0));
                }, Tween.OutCubic, i * 0.06f, () =>
                {
                    if (coin) Destroy(coin.gameObject);
                    if (hintsButton) Tween.Punch(hintsButton, 0.12f, 0.15f);
                });
            }
        }

        /// <summary>A real English word that isn't one of the answers earns a few coins.</summary>
        bool TryBonus(string word, List<Hex> path)
        {
            if (word.Length < 3 || !WordDictionary.Contains(word)) return false;
            if (!bonusFound.Add(word))
            {
                AudioManager.Error();
                ZWordApp.Toast(root, "BONUS ALREADY FOUND", new Vector2(0, 520), Palette.Yellow);
                return true;
            }
            bonusScore += GameConfig.BonusWordPoints;
            Save.Data.bonusWords++;
            Challenges.Report(Metric.Bonus, 1);
            Save.Coins += GameConfig.BonusWordCoins;
            AudioManager.Bonus();
            board.Glow(path, 0.6f, 0.04f);
            CoinBurst(path, 5);
            ZWordApp.Toast(root, "BONUS WORD +" + GameConfig.BonusWordCoins + " COINS", new Vector2(0, 520), Palette.Hex("7CF06B"));
            return true;
        }

        bool IsLocked(Hex h) => level.Words.Any(w => w.Found && w.Path.Contains(h));

        void Wrong(List<Hex> path, string message)
        {
            AudioManager.Error();
            board.ShakeTiles(path);
            if (message != null) ZWordApp.Toast(root, message, new Vector2(0, 520), Palette.Yellow);
        }

        // ---------------- End of level ----------------

        void Win()
        {
            running = false;
            board.Interactable = false;
            if (TutorialMode)
            {
                AudioManager.Win();
                Haptics.Success();
                Tween.Value(0.01f, _ => { }, null, 0.9f, () => { if (this) TutorialWin?.Invoke(); });
                return;
            }
            float frac = Mathf.Clamp01(timeLeft / level.TimeLimit);
            float rating = relax ? RelaxStars : Mathf.Clamp(1f + frac * RatingSlope, 1f, 3f);
            int stars = Mathf.FloorToInt(rating + 0.0001f);
            int timeBonus = relax ? stars * 400 : Mathf.CeilToInt(Mathf.Max(0, timeLeft)) * 25;

            var data = new ResultData
            {
                Category = level.CategoryIndex,
                Level = level.LevelIndex,
                Won = true,
                Rating = rating,
                Stars = stars,
                TimeTaken = elapsed,
                WordScore = wordScore,
                TimeBonus = timeBonus,
                BonusScore = bonusScore,
                BonusWords = bonusFound.Count,
                CoinsEarned = GameConfig.LevelCoins(stars) + (Store.IsPro ? GameConfig.ProLevelBonusCoins : 0),
                GemsEarned = stars == 3 ? GameConfig.GemsForThreeStars : 0,
                GoldGems = goldGems,
                NewBookWords = newBookWords
            };
            if (comboMeter) comboMeter.gameObject.SetActive(false);
            var d = Save.Data;
            if (hintsUsed == 0) { d.noHintWins++; Challenges.Report(Metric.NoHints, 1); }
            if (DailyMode)
            {
                // the daily level never advances category progress; it pays its own streak reward
                var (dc, dg, streak) = DailyPuzzle.Complete(data.Total);
                data.Daily = true;
                data.Streak = streak;
                data.CoinsEarned = dc;
                data.GemsEarned = dg;
                data.BestScore = d.dailyPuzzleBest;
                data.NewBest = data.Total >= d.dailyPuzzleBest && dc > 0;
                d.levelsCompleted++;
                if (stars == 3) d.threeStarWins++;
                Challenges.Report(Metric.Levels, 1);
                Challenges.Report(Metric.Score, data.Total);
                if (stars == 3) Challenges.Report(Metric.ThreeStars, 1);
                Save.StarPoints += data.Total;
                Save.Write();
                AudioManager.Win();
                Haptics.Success();
                Tween.Value(1.1f, _ => { }, null, 0, () => { if (this) ZWordApp.I.ShowResult(data); });
                return;
            }
            d.levelsCompleted++;
            if (stars == 3) d.threeStarWins++;
            Challenges.Report(Metric.Levels, 1);
            Challenges.Report(Metric.Score, data.Total);
            if (stars == 3) Challenges.Report(Metric.ThreeStars, 1);
            d.lastCategory = level.CategoryIndex;
            if (IsBoss)
            {
                data.Boss = true;
                var (bc, bg) = Boss.Crown(level.CategoryIndex, level.LevelIndex);
                data.CrownEarned = bc > 0;
                data.CoinsEarned += bc;
                data.GemsEarned += bg;
            }
            Save.SetStars(level.CategoryIndex, level.LevelIndex, stars);
            Save.SetCompleted(level.CategoryIndex, level.LevelIndex + 1);
            if (Events.TryAwardBadge(level.CategoryIndex)) data.BadgeEarned = level.Category.Badge;
            data.NewBest = Save.SubmitScore(level.CategoryIndex, level.LevelIndex, data.Total);
            data.BestScore = Save.BestScore(level.CategoryIndex, level.LevelIndex);
            Save.StarPoints += data.Total;
            Save.Coins += data.CoinsEarned;
            if (data.GemsEarned > 0) Save.Gems += data.GemsEarned;   // golden hex gems were already paid when found

            AudioManager.Win();
            Haptics.Success();
            Tween.Value(1.1f, _ => { }, null, 0, () => { if (this) ZWordApp.I.ShowResult(data); });
        }

        bool continueOffered;

        /// <summary>Time ran out: offer +30s once (gems or coins), otherwise the level is lost.</summary>
        void OutOfTime()
        {
            running = false;
            timeLeft = 0;
            UpdateHud(true);
            board.Interactable = false;
            board.ClearSelection();
            if (continueOffered) { Lose(); return; }
            continueOffered = true;

            AudioManager.Error();
            bool decided = false;
            var body = Widgets.WoodPopup("OUT OF TIME", new Vector2(780, 820), () => { if (!decided) { decided = true; Lose(); } });

            var clockSprite = Theme.Current.iconClock != null ? Theme.Current.iconClock : Sprites.Clock;
            var clock = UI.Img(body, clockSprite, Color.white, "Clock");
            clock.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -130), new Vector2(160, 160));
            clock.preserveAspect = true;
            clock.gameObject.AddComponent<Pulse>().Amount = 0.06f;
            var msg = UI.Label(body, "Keep going with +" + GameConfig.ContinueSeconds + " seconds?", 40, Skin.Ink, TextAnchor.MiddleCenter, false);
            msg.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -260), new Vector2(700, 60));
            int left = level.Words.Count(w => !w.Found);
            var sub = UI.Label(body, left == 1 ? "Only 1 word left!" : left + " words left", 32, Skin.InkSoft, TextAnchor.MiddleCenter, false);
            sub.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -314), new Vector2(700, 46));

            void Continue()
            {
                decided = true;
                ZWordApp.I.ClosePopups();
                timeLeft = GameConfig.ContinueSeconds;
                running = true;
                lastTickSecond = -1;
                UpdateHud(true);
                AudioManager.Booster();
                Tween.Punch(timePill, 0.3f, 0.35f);
            }

            var gems = Widgets.PriceButton(body, new Vector2(560, 120), Currency.Gems, GameConfig.ContinueGems + "   +" + GameConfig.ContinueSeconds + "s", () =>
            {
                if (Save.TrySpendGems(GameConfig.ContinueGems)) Continue();
                else { AudioManager.Error(); ZWordApp.Toast(body, "NOT ENOUGH GEMS", Vector2.zero, Palette.Yellow); }
            }, Skin.Purple);
            ((RectTransform)gems.transform).Place(new Vector2(0.5f, 1), new Vector2(0, -420), new Vector2(560, 120));

            var coins = Widgets.PriceButton(body, new Vector2(560, 120), Currency.Coins, GameConfig.ContinueCoins + "   +" + GameConfig.ContinueSeconds + "s", () =>
            {
                if (Save.TrySpendCoins(GameConfig.ContinueCoins)) Continue();
                else { AudioManager.Error(); ZWordApp.Toast(body, "NOT ENOUGH COINS", Vector2.zero, Palette.Yellow); }
            });
            ((RectTransform)coins.transform).Place(new Vector2(0.5f, 1), new Vector2(0, -560), new Vector2(560, 120));

            var giveUp = UI.Chunky(body, new Vector2(360, 96), Skin.Wood, "GIVE UP", 40, () => ZWordApp.I.ClosePopups());
            ((RectTransform)giveUp.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 50), new Vector2(360, 96));
        }

        void Lose()
        {
            running = false;
            timeLeft = 0;
            UpdateHud(true);
            board.Interactable = false;
            board.ClearSelection();
            AudioManager.Lose();
            var data = new ResultData
            {
                Category = level.CategoryIndex,
                Level = level.LevelIndex,
                Won = false,
                TimeTaken = elapsed,
                WordScore = wordScore,
                BonusScore = bonusScore,
                BonusWords = bonusFound.Count,
                BestScore = DailyMode ? Save.Data.dailyPuzzleBest : Save.BestScore(level.CategoryIndex, level.LevelIndex),
                Daily = DailyMode,
                Streak = DailyPuzzle.Streak
            };
            ZWordApp.Toast(root, "TIME'S UP!", new Vector2(0, 0), Palette.Yellow);
            Tween.Value(1.2f, _ => { }, null, 0, () => { if (this) ZWordApp.I.ShowResult(data); });
        }
    }
}
