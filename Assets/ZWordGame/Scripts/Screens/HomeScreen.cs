using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>Home: profile + wallet bar, logo over the city, PLAY / CATEGORIES and the bottom dock (mockup screen 2).</summary>
    public static class HomeScreen
    {
        public static void Build(RectTransform root)
        {
            // Illustrated city behind everything on this screen
            var bgArt = Theme.Current.homeBackground;
            if (bgArt != null)
            {
                var holder = UI.Rect("HomeBgHolder", root).Stretch();
                SafeAreaBleed.Add(holder);
                var bg = UI.Img(holder, bgArt, Color.white, "HomeBg");
                bg.rectTransform.Stretch();
                var fit = bg.gameObject.AddComponent<AspectRatioFitter>();
                fit.aspectMode = AspectRatioFitter.AspectMode.EnvelopeParent;
                fit.aspectRatio = bgArt.rect.width / bgArt.rect.height;
            }
            var topShade = UI.Img(root, Sprites.Vignette, new Color(0.3f, 0.17f, 0.05f, 0.3f), "TopShade");
            topShade.rectTransform.anchorMin = new Vector2(0, 1);
            topShade.rectTransform.anchorMax = new Vector2(1, 1);
            topShade.rectTransform.pivot = new Vector2(0.5f, 1);
            topShade.rectTransform.sizeDelta = new Vector2(0, 220);
            topShade.rectTransform.anchoredPosition = Vector2.zero;
            SafeAreaBleed.Add(topShade.rectTransform);

            // life in the sky
            Ambience.Add(root, AmbienceKind.Clouds, new Color(1, 1, 1, 0.8f), 5, 0.18f);
            Ambience.Add(root, AmbienceKind.Birds, Palette.Hex("3B2414"), 3, 0.25f);

            BuildTopBar(root);

            var logo = Widgets.Logo(root, 0.95f);
            logo.anchorMin = logo.anchorMax = new Vector2(0.5f, 1);
            logo.sizeDelta = new Vector2(780, 560);
            logo.anchoredPosition = new Vector2(0, -470);
            logo.gameObject.AddComponent<Bobber>().Amplitude = 5;

            // PLAY + where it leads
            Progression.NextLevel(out int cat, out int lvl);
            var catDef = WordData.Categories[cat];

            var info = UI.Rect("NextInfo", root).Place(new Vector2(0.5f, 0), new Vector2(0, 720), new Vector2(430, 64));
            UI.Img(info, Sprites.Rounded, Skin.ChipBg, "Bg", 2f).rectTransform.Stretch();
            var infoText = UI.Label(info, catDef.Name + "  •  LEVEL " + (lvl + 1), 34, Color.white, TextAnchor.MiddleCenter);
            infoText.rectTransform.Stretch();

            var play = UI.Chunky(root, new Vector2(640, 160), Skin.Green, "PLAY", 86, () => ZWordApp.I.StartLevel(cat, lvl), null, 1f, 18);
            ((RectTransform)play.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 580), new Vector2(640, 160));
            play.gameObject.AddComponent<Pulse>();

            var cats = UI.Chunky(root, new Vector2(580, 128), Skin.Wood, "CATEGORIES", 58, () => ZWordApp.I.ShowCategories(), null, 1f, 14);
            ((RectTransform)cats.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 410), new Vector2(580, 128));
            Tween.PopIn(cats.transform, 0.35f, 0.22f);

            BuildDailyPuzzle(root);
            BuildEventBanner(root);

            BuildDock(root);
        }

        static Sprite Icon(string name, Sprite fallback)
        {
            var s = Resources.Load<Sprite>("HomeIcons/" + name);
            return s != null ? s : fallback;
        }

        /// <summary>Purple Daily Puzzle banner: today's special level, streak and countdown.</summary>
        static void BuildDailyPuzzle(RectTransform root)
        {
            bool done = DailyPuzzle.DoneToday;
            int streak = DailyPuzzle.Streak;
            var card = UI.Rect("DailyPuzzle", root).Place(new Vector2(0.5f, 0), new Vector2(30, 870), new Vector2(600, 124));
            UI.Img(card, Sprites.Rounded, new Color(0.45f, 0.18f, 0.03f, 0.5f), "Shadow", 1.6f).rectTransform.Stretch(0, -10, 0, 10);
            var face = UI.Img(card, Sprites.Rounded, done ? Palette.Hex("E6C15A") : Palette.Hex("FFC928"), "Face", 1.6f);
            face.rectTransform.Stretch();
            face.raycastTarget = true;
            var gloss = UI.Img(card, Sprites.Rounded, new Color(1, 1, 1, 0.18f), "Gloss", 2.4f);
            gloss.rectTransform.anchorMin = new Vector2(0, 0.55f);
            gloss.rectTransform.anchorMax = Vector2.one;
            gloss.rectTransform.offsetMin = new Vector2(80, 0);
            gloss.rectTransform.offsetMax = new Vector2(-16, -8);

            var icon = UI.Img(card, Icon("icon_daily_puzzle", Sprites.CalendarGlyph), Color.white, "Icon");
            icon.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(10, 6), new Vector2(150, 150));
            icon.preserveAspect = true;
            if (!done) icon.gameObject.AddComponent<Bobber>().Amplitude = 4;

            var title = UI.Label(card, "DAILY PUZZLE", 46, Color.white, TextAnchor.MiddleLeft);
            title.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(330, 20), new Vector2(380, 56));
            UI.Outlined(title);
            string subText = done ? "Solved! Next one in " + Day.Countdown()
                : streak > 0 ? "Keep your " + streak + "-day streak going!"
                : "Win +" + DailyPuzzle.CoinsFor(1) + " coins and a gem";
            var sub = UI.Label(card, subText, 26, new Color(1, 1, 1, 0.92f), TextAnchor.MiddleLeft, false);
            sub.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(330, -26), new Vector2(380, 40));

            var go = UI.Rect("Go", card).Place(new Vector2(1, 0.5f), new Vector2(-62, 0), new Vector2(84, 84));
            UI.Img(go, Sprites.CircleSprite, done ? Skin.Green : Color.white, "Bg").rectTransform.Stretch();
            UI.Img(go, done ? Sprites.Check : Sprites.Play, done ? Color.white : Palette.Brown, "Glyph").rectTransform.Stretch(20, 20, 18, 20);

            var btn = card.gameObject.AddComponent<Button>();
            btn.transition = Selectable.Transition.None;
            btn.targetGraphic = face;
            btn.onClick.AddListener(() => { AudioManager.Click(); ZWordApp.I.StartDailyPuzzle(); });
            card.gameObject.AddComponent<PressEffect>();
            if (!done)
            {
                Widgets.Badge(card, "!", 46);
                card.gameObject.AddComponent<Pulse>().Amount = 0.02f;
            }

            // streak flame: number of days in a row, top-left corner of the card
            if (streak > 0)
            {
                var flame = UI.Rect("Streak", card).Place(new Vector2(0, 1), new Vector2(18, -6), new Vector2(110, 64));
                UI.Img(flame, Sprites.Rounded, Palette.Hex("E5484D"), "Bg", 2.2f).rectTransform.Stretch(18, 0, 0, 0);
                var fi = UI.Img(flame, Widgets.HomeIcon("icon_flame", Sprites.Star), Color.white, "Flame");
                fi.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(26, 6), new Vector2(64, 64));
                fi.preserveAspect = true;
                var fn = UI.Label(flame, streak.ToString(), 36, Color.white, TextAnchor.MiddleCenter);
                fn.rectTransform.Stretch(52, 0, 4, 0);
                UI.Outlined(fn);
                flame.localRotation = Quaternion.Euler(0, 0, 6);
                if (!done) flame.gameObject.AddComponent<Pulse>().Amount = 0.05f;
            }
            Tween.PopIn(card, 0.35f, 0.15f);
        }

        /// <summary>Limited-time event banner (e.g. HALLOWEEN) above the Daily Puzzle while the event is live.</summary>
        static void BuildEventBanner(RectTransform root)
        {
            int ev = WordData.ActiveEvent();
            if (ev < 0) return;
            var cat = WordData.Categories[ev];
            int done = Mathf.Min(Save.Completed(ev), cat.LevelCount);
            bool finished = done >= cat.LevelCount;

            var card = UI.Rect("Event", root).Place(new Vector2(0.5f, 0), new Vector2(30, 1012), new Vector2(600, 124));
            UI.Img(card, Sprites.Rounded, new Color(0.2f, 0.1f, 0.03f, 0.5f), "Shadow", 1.6f).rectTransform.Stretch(0, -10, 0, 10);
            var face = UI.Img(card, Sprites.Rounded, Palette.Hex("4A2A14"), "Face", 1.6f);
            face.rectTransform.Stretch();
            face.raycastTarget = true;
            var gloss = UI.Img(card, Sprites.Rounded, new Color(1, 1, 1, 0.12f), "Gloss", 2.4f);
            gloss.rectTransform.anchorMin = new Vector2(0, 0.55f);
            gloss.rectTransform.anchorMax = Vector2.one;
            gloss.rectTransform.offsetMin = new Vector2(80, 0);
            gloss.rectTransform.offsetMax = new Vector2(-16, -8);

            var icon = UI.Img(card, Widgets.HomeIcon("icon_event_" + Widgets.Slug(cat.Name), Sprites.Star), Color.white, "Icon");
            icon.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(10, 8), new Vector2(150, 150));
            icon.preserveAspect = true;
            icon.gameObject.AddComponent<Bobber>().Amplitude = 4;

            var title = UI.Label(card, cat.Name + " EVENT", 42, Skin.Gold, TextAnchor.MiddleLeft);
            title.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(330, 20), new Vector2(380, 56));
            UI.Outlined(title);
            title.enableAutoSizing = true;
            title.fontSizeMin = 28;
            title.fontSizeMax = 42;
            string Sub() => finished ? "Badge earned! Ends in " + Events.TimeLeftText(cat)
                                     : done + "/" + cat.LevelCount + " levels  •  ends in " + Events.TimeLeftText(cat);
            var sub = UI.Label(card, Sub(), 26, new Color(1, 1, 1, 0.92f), TextAnchor.MiddleLeft, false);
            sub.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(330, -26), new Vector2(380, 40));
            sub.gameObject.AddComponent<Ticker>().OnTick = () => { if (sub) sub.text = Sub(); };

            var go = UI.Rect("Go", card).Place(new Vector2(1, 0.5f), new Vector2(-62, 0), new Vector2(84, 84));
            UI.Img(go, Sprites.CircleSprite, finished ? Skin.Green : Skin.Gold, "Bg").rectTransform.Stretch();
            UI.Img(go, finished ? Sprites.Check : Sprites.Play, finished ? Color.white : Palette.Brown, "Glyph").rectTransform.Stretch(20, 20, 18, 20);

            var btn = card.gameObject.AddComponent<Button>();
            btn.transition = Selectable.Transition.None;
            btn.targetGraphic = face;
            btn.onClick.AddListener(() => { AudioManager.Click(); ZWordApp.I.ShowMap(ev); });
            card.gameObject.AddComponent<PressEffect>();
            if (!finished) Widgets.Badge(card, "!", 46);
            Tween.PopIn(card, 0.35f, 0.1f);
        }

        static void BuildTopBar(RectTransform root)
        {
            var bar = UI.Rect("TopBar", root);
            bar.anchorMin = new Vector2(0, 1);
            bar.anchorMax = new Vector2(1, 1);
            bar.pivot = new Vector2(0.5f, 1);
            bar.sizeDelta = new Vector2(0, 150);
            bar.anchoredPosition = Vector2.zero;

            // profile pill
            var prof = UI.Rect("Profile", bar).Place(new Vector2(0, 0.5f), new Vector2(170, -10), new Vector2(240, 76));
            UI.Img(prof, Sprites.Rounded, Skin.ChipBg, "Bg", 1.6f).rectTransform.Stretch(30, 0, 0, 0);
            var av = Theme.Current.iconAvatar != null ? Theme.Current.iconAvatar : Sprites.AvatarGlyph;
            var avatar = UI.Img(prof, av, Color.white, "Avatar");
            avatar.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(40, 0), new Vector2(90, 90));
            var name = UI.Label(prof, Save.Data.playerName, 36, Color.white, TextAnchor.MiddleLeft);
            name.rectTransform.Stretch(96, 0, 14, 0);
            var profBtn = prof.gameObject.AddComponent<Button>();
            profBtn.transition = Selectable.Transition.None;
            profBtn.targetGraphic = avatar;
            avatar.raycastTarget = true;
            profBtn.onClick.AddListener(() => { AudioManager.Click(); ZWordApp.I.OpenSettings(); });

            var stars = Widgets.CurrencyChip(bar, Currency.Stars, 190);
            stars.Place(new Vector2(0.5f, 0.5f), new Vector2(-140, -10), new Vector2(190, 66));
            var coins = Widgets.CurrencyChip(bar, Currency.Coins, 180);
            coins.Place(new Vector2(0.5f, 0.5f), new Vector2(55, -10), new Vector2(180, 66));
            var gems = Widgets.CurrencyChip(bar, Currency.Gems, 170);
            gems.Place(new Vector2(0.5f, 0.5f), new Vector2(245, -10), new Vector2(170, 66));

            var gear = Widgets.RoundButton(bar, Sprites.Gear, 96, Skin.Wood, () => ZWordApp.I.OpenSettings(), 0.56f);
            ((RectTransform)gear.transform).Place(new Vector2(1, 0.5f), new Vector2(-70, -10), new Vector2(96, 96));
        }

        static void BuildDock(RectTransform root)
        {
            var t = Theme.Current;
            var specs = new (string label, Sprite icon, System.Action action)[]
            {
                ("Rewards", Icon("icon_calendar", t.iconCalendar != null ? t.iconCalendar : Sprites.CalendarGlyph), () => ZWordApp.I.OpenDailyReward()),
                ("Challenges", Icon("icon_trophy", t.trophy != null ? t.trophy : Sprites.TrophyGlyph), () => ZWordApp.I.ShowChallenges()),
                ("Words", Icon("icon_book", Sprites.ScrollGlyph), () => FeatureScreens.OpenWordBook()),
                ("Shop", Icon("icon_shop", t.shopIcon != null ? t.shopIcon : Sprites.ShopGlyph), () => ZWordApp.I.ShowShop()),
                ("Quests", Icon("icon_quests", t.quest != null ? t.quest : Sprites.ScrollGlyph), () => ZWordApp.I.ShowQuests()),
            };
            for (int i = 0; i < specs.Length; i++)
            {
                var (label, icon, action) = specs[i];
                var b = Widgets.DockButton(root, icon, Color.white, label, action, 132, 0.78f);
                ((RectTransform)b.transform).Place(new Vector2(0.5f, 0), new Vector2(-404 + i * 202, 190), new Vector2(132, 132));
                Tween.PopIn(b.transform, 0.3f, 0.3f + i * 0.06f);
                int badge = ZWordApp.I.DockBadge(i);
                if (badge > 0) Widgets.Badge(b.transform, badge.ToString(), 46);
            }
        }
    }

    /// <summary>Slow "breathing" scale to draw the eye to the main button.</summary>
    public class Pulse : MonoBehaviour
    {
        public float Amount = 0.035f, Speed = 2.4f;
        void Update()
        {
            float s = 1f + Mathf.Sin(Time.unscaledTime * Speed) * Amount;
            transform.localScale = new Vector3(s, s, 1f);
        }
    }
}
