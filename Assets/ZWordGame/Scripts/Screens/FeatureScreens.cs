using System.Globalization;
using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>Word Book pages, event badges and the reminders opt-in popup.</summary>
    public static class FeatureScreens
    {
        static string N(int v) => v.ToString("N0", CultureInfo.InvariantCulture);

        static RectTransform ScrollArea(RectTransform root, float top, float contentH, out ScrollRect scroll)
        {
            var viewport = UI.Rect("Viewport", root);
            viewport.anchorMin = Vector2.zero;
            viewport.anchorMax = Vector2.one;
            viewport.offsetMin = new Vector2(0, 30);
            viewport.offsetMax = new Vector2(0, -top);
            viewport.gameObject.AddComponent<RectMask2D>();
            viewport.gameObject.AddComponent<Image>().color = new Color(0, 0, 0, 0);
            var content = UI.Rect("Content", viewport);
            content.anchorMin = new Vector2(0, 1);
            content.anchorMax = new Vector2(1, 1);
            content.pivot = new Vector2(0.5f, 1);
            content.sizeDelta = new Vector2(0, contentH);
            scroll = viewport.gameObject.AddComponent<ScrollRect>();
            scroll.viewport = viewport;
            scroll.content = content;
            scroll.horizontal = false;
            scroll.scrollSensitivity = 40;
            return content;
        }

        // ---------------- Word Book ----------------

        public static void OpenWordBook()
        {
            WordBook.EnsureSeeded();
            var root = Widgets.FullPanel("WORD BOOK");

            var sum = UI.Rect("Summary", root).Place(new Vector2(0.5f, 1), new Vector2(0, -205), new Vector2(560, 66));
            UI.Img(sum, Sprites.Rounded, Skin.ChipBg, "Bg", 1.6f).rectTransform.Stretch();
            var bookIcon = UI.Img(sum, Widgets.HomeIcon("icon_book", Sprites.ScrollGlyph), Color.white, "Icon");
            bookIcon.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(40, 2), new Vector2(76, 76));
            bookIcon.preserveAspect = true;
            var st = UI.Label(sum, N(WordBook.TotalFound) + " / " + N(WordBook.TotalWords) + " words found", 34, Color.white, TextAnchor.MiddleCenter);
            st.rectTransform.Stretch(70, 0, 10, 0);

            var pages = new System.Collections.Generic.List<int>(WordBook.Pages());
            var content = ScrollArea(root, 260, 40 + pages.Count * 176, out _);
            for (int i = 0; i < pages.Count; i++) PageRow(content, pages[i], i);
        }

        static void PageRow(RectTransform content, int c, int i)
        {
            var cat = WordData.Categories[c];
            int found = WordBook.Found(c), total = WordBook.Total(c);
            bool claim = WordBook.CanClaim(c), done = WordBook.Complete(c) && !claim;

            var card = Widgets.Card(content, new Vector2(900, 156), done ? Palette.Hex("FFF6DF") : Skin.Cream);
            card.Place(new Vector2(0.5f, 1), new Vector2(0, -98 - i * 176), new Vector2(900, 156));
            Tween.PopIn(card, 0.25f, Mathf.Min(i, 10) * 0.03f);
            var icon = Widgets.CategoryIcon(card, cat, 104);
            icon.Place(new Vector2(0, 0.5f), new Vector2(80, 0), new Vector2(104, 104));
            var name = UI.Label(card, cat.Name, 38, Skin.Ink, TextAnchor.MiddleLeft, false);
            name.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(150 + 220, 28), new Vector2(440, 50));
            var bar = Widgets.Progress(card, new Vector2(440, 40), done ? Skin.Gold : cat.Color, Skin.CreamShade, true);
            bar.Root.Place(new Vector2(0, 0.5f), new Vector2(150 + 220, -30), new Vector2(440, 40));
            bar.Set(total > 0 ? (float)found / total : 0f, found + "/" + total);
            bar.Label.color = Skin.Ink;
            bar.Label.fontSharedMaterial = Fonts.Plain;

            if (claim)
            {
                var b = Widgets.PriceButton(card, new Vector2(190, 96), Currency.Gems, "+" + GameConfig.BookPageGems, () =>
                {
                    int g = WordBook.Claim(c);
                    if (g > 0) ZWordApp.I.ShowReward("PAGE COMPLETE!", 0, g, OpenWordBook);
                });
                ((RectTransform)b.transform).Place(new Vector2(1, 0.5f), new Vector2(-120, 0), new Vector2(190, 96));
                b.gameObject.AddComponent<Pulse>().Amount = 0.05f;
            }
            else
            {
                var mark = UI.Img(card, done ? Sprites.Check : Sprites.ChevronRight, done ? Skin.Green : Skin.InkSoft, "Mark");
                mark.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-70, 0), new Vector2(done ? 64 : 44, done ? 64 : 44));
            }
            var hit = card.gameObject.AddComponent<Image>();
            hit.color = new Color(0, 0, 0, 0);
            var open = card.gameObject.AddComponent<Button>();
            open.transition = Selectable.Transition.None;
            open.targetGraphic = hit;
            open.onClick.AddListener(() => { AudioManager.Click(); OpenPage(c); });
        }

        /// <summary>One category's page: found words in colour, missing ones as their first letter and dots.</summary>
        public static void OpenPage(int c)
        {
            var cat = WordData.Categories[c];
            var root = Widgets.FullPanel(cat.Name, null, OpenWordBook);
            var words = LevelDatabase.WordsIn(c);
            int found = WordBook.Found(c);

            var sum = UI.Label(root, found + " / " + words.Length + " words", 38, Color.white, TextAnchor.MiddleCenter);
            sum.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -205), new Vector2(700, 60));
            UI.Outlined(sum);

            // flow the chips into rows
            const float maxW = 940f, chipH = 74f, gapX = 14f, gapY = 16f, letterW = 27f;
            var layout = new System.Collections.Generic.List<(string w, Vector2 pos, float width)>();
            float x = 0, y = 0;
            foreach (var w in words)
            {
                float width = 44 + w.Length * letterW;
                if (x > 0 && x + width > maxW) { x = 0; y += chipH + gapY; }
                layout.Add((w, new Vector2(x, y), width));
                x += width + gapX;
            }
            float contentH = y + chipH + 80;
            var content = ScrollArea(root, 270, contentH, out _);
            var grid = UI.Rect("Grid", content).Place(new Vector2(0.5f, 1), new Vector2(0, -20 - contentH / 2f), new Vector2(maxW, contentH));

            // centre each row
            var rowWidth = new System.Collections.Generic.Dictionary<float, float>();
            foreach (var (w, pos, width) in layout) rowWidth[pos.y] = pos.x + width;

            var have = Save.BookWords(c);
            foreach (var (w, pos, width) in layout)
            {
                bool got = have.Contains(w);
                float offset = (maxW - rowWidth[pos.y]) / 2f;
                var chip = UI.Rect("Word_" + w, grid);
                chip.anchorMin = chip.anchorMax = new Vector2(0, 1);
                chip.pivot = new Vector2(0, 1);
                chip.anchoredPosition = new Vector2(pos.x + offset, -pos.y);
                chip.sizeDelta = new Vector2(width, chipH);
                UI.Img(chip, Sprites.Rounded, got ? Palette.Darken(cat.Color, 0.75f) : new Color(0.36f, 0.2f, 0.06f, 0.25f), "Shadow", 2f).rectTransform.Stretch(0, -6, 0, 6);
                UI.Img(chip, Sprites.Rounded, got ? cat.Color : new Color(1, 1, 1, 0.75f), "Face", 2f).rectTransform.Stretch();
                string text = got ? w : w[0] + new string('_', w.Length - 1);
                var t = UI.Label(chip, text, 36, got ? Color.white : Skin.InkSoft, TextAnchor.MiddleCenter, got);
                t.rectTransform.Stretch(4, 2, 4, 0);
            }

            if (WordBook.CanClaim(c))
            {
                var b = Widgets.PriceButton(root, new Vector2(420, 110), Currency.Gems, "CLAIM +" + GameConfig.BookPageGems, () =>
                {
                    int g = WordBook.Claim(c);
                    if (g > 0) ZWordApp.I.ShowReward("PAGE COMPLETE!", 0, g, OpenWordBook);
                });
                ((RectTransform)b.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 110), new Vector2(420, 110));
                b.gameObject.AddComponent<Pulse>().Amount = 0.05f;
            }
        }

        // ---------------- badges ----------------

        public static Sprite BadgeSprite(string badge) =>
            Widgets.HomeIcon("badge_" + Widgets.Slug(badge), Theme.Current.crown != null ? Theme.Current.crown : Sprites.Star);

        /// <summary>"BADGE EARNED" popup (rewards were already paid).</summary>
        public static void ShowBadge(string badge, bool withRewards)
        {
            var body = Widgets.WoodPopup("BADGE EARNED!", new Vector2(760, 780));
            var rays = UI.Img(body, Sprites.Rays, new Color(1f, 0.85f, 0.4f, 0.5f), "Rays");
            rays.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -190), new Vector2(460, 460));
            rays.gameObject.AddComponent<Spinner>();
            var img = UI.Img(body, BadgeSprite(badge), Color.white, "Badge");
            img.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -190), new Vector2(250, 250));
            img.preserveAspect = true;
            Tween.PopIn(img.transform, 0.45f, 0.1f);
            var name = UI.Label(body, badge, 50, Skin.Ink, TextAnchor.MiddleCenter, false);
            name.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -360), new Vector2(680, 64));
            if (withRewards)
            {
                Chip(body, Currency.Coins, GameConfig.EventBadgeCoins, new Vector2(-130, -450));
                Chip(body, Currency.Gems, GameConfig.EventBadgeGems, new Vector2(130, -450));
            }
            var collect = UI.Chunky(body, new Vector2(460, 120), Skin.Green, "COLLECT", 52, () => ZWordApp.I.ClosePopups());
            ((RectTransform)collect.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 80), new Vector2(460, 120));
            AudioManager.Win();
            Haptics.Success();
        }

        static void Chip(RectTransform parent, Currency kind, int amount, Vector2 pos)
        {
            var r = UI.Rect("Reward", parent).Place(new Vector2(0.5f, 1), pos, new Vector2(230, 90));
            var icon = Widgets.CurrencyIcon(r, kind, 80);
            icon.Place(new Vector2(0, 0.5f), new Vector2(46, 0), new Vector2(80, 80));
            var t = UI.Label(r, "+" + amount, 50, Skin.Ink, TextAnchor.MiddleLeft, false);
            t.rectTransform.Stretch(96, 0, 0, 0);
            Tween.PopIn(r, 0.35f, 0.3f);
        }

        /// <summary>Badges card for the top of the Quests page: one slot per event (earned, live or missed).</summary>
        public static float BadgesCard(RectTransform content, float top)
        {
            var cats = WordData.Categories;
            var events = new System.Collections.Generic.List<int>();
            for (int c = 0; c < cats.Length; c++) if (cats[c].IsEvent) events.Add(c);
            if (events.Count == 0) return 0;

            var card = Widgets.Card(content, new Vector2(900, 230), Palette.Hex("FFF6DF"));
            card.Place(new Vector2(0.5f, 1), new Vector2(0, top - 115), new Vector2(900, 230));
            var title = UI.Label(card, "EVENT BADGES", 34, Skin.Ink, TextAnchor.MiddleLeft, false);
            title.rectTransform.Place(new Vector2(0, 1), new Vector2(40 + 200, -36), new Vector2(400, 44));
            for (int i = 0; i < events.Count && i < 5; i++)
            {
                var cat = cats[events[i]];
                bool earned = Save.HasBadge(cat.Badge);
                var slot = UI.Rect("Badge", card).Place(new Vector2(0, 0), new Vector2(110 + i * 170, 92), new Vector2(150, 150));
                var img = UI.Img(slot, BadgeSprite(cat.Badge), earned ? Color.white : new Color(0.3f, 0.25f, 0.2f, 0.35f), "Icon");
                img.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -50), new Vector2(110, 110));
                img.preserveAspect = true;
                string status = earned ? "EARNED" : cat.Live ? Events.TimeLeftText(cat) + " LEFT" : "MISSED";
                var lbl = UI.Label(slot, status, 22, earned ? Skin.Green : Skin.InkSoft, TextAnchor.MiddleCenter, false);
                lbl.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 12), new Vector2(170, 30));
                if (earned)
                {
                    var b = slot.gameObject.AddComponent<Button>();
                    b.transition = Selectable.Transition.None;
                    b.targetGraphic = img;
                    img.raycastTarget = true;
                    string badge = cat.Badge;
                    b.onClick.AddListener(() => ShowBadge(badge, false));
                }
            }
            return 254;
        }

        // ---------------- reminders opt-in ----------------

        /// <summary>Friendly ask before the system permission prompt (shown once, after a Daily Puzzle win).</summary>
        public static void AskReminders()
        {
            var d = Save.Data;
            if (d.remindersAsked || d.remindersOn || !Reminders.Supported) return;
            d.remindersAsked = true;
            Save.Write();
            var body = Widgets.WoodPopup("REMINDERS", new Vector2(780, 760));
            var bell = UI.Img(body, Widgets.HomeIcon("icon_bell", Sprites.Clock), Color.white, "Bell");
            bell.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -120), new Vector2(170, 170));
            bell.preserveAspect = true;
            bell.gameObject.AddComponent<Bobber>().Amplitude = 6;
            var msg = UI.Label(body, "Want a gentle reminder when\na new Daily Puzzle is ready?", 38, Skin.Ink, TextAnchor.MiddleCenter, false);
            msg.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -290), new Vector2(700, 110));
            var sub = UI.Label(body, "One a day at most. Turn it off any time in Settings.", 26, Skin.InkSoft, TextAnchor.MiddleCenter, false);
            sub.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -370), new Vector2(700, 40));
            var yes = UI.Chunky(body, new Vector2(480, 120), Skin.Green, "YES, REMIND ME", 44, () =>
            {
                ZWordApp.I.ClosePopups();
                Reminders.Enable(on => { if (on && ZWordApp.I.CurrentScreen) ZWordApp.Toast(ZWordApp.I.CurrentScreen, "REMINDERS ON!", new Vector2(0, -300), Palette.Hex("7CF06B")); });
            });
            ((RectTransform)yes.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 170), new Vector2(480, 120));
            var no = UI.Chunky(body, new Vector2(320, 90), Skin.Wood, "NO THANKS", 36, () => ZWordApp.I.ClosePopups());
            ((RectTransform)no.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 50), new Vector2(320, 90));
        }
    }
}
