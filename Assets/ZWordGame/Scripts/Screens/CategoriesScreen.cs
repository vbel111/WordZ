using System.Globalization;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>
    /// Categories: a 2-column grid of picture cards. Each card shows a slice of that category's map art,
    /// its icon, name, stars and progress. Locked cards are dimmed with a lock and their star cost.
    /// </summary>
    public static class CategoriesScreen
    {
        const float CardW = 470f, CardH = 400f, ArtH = 236f;

        public static void Build(RectTransform root)
        {
            Widgets.Header(root, "CATEGORIES", null, () => ZWordApp.I.ShowHome(), gear: false);
            ZWordApp.I.OnBack = () => ZWordApp.I.ShowHome();

            var stars = Widgets.CurrencyChip(root, Currency.Stars, 230);
            stars.Place(new Vector2(0.5f, 1), new Vector2(-130, -204), new Vector2(230, 62));
            var coins = Widgets.CurrencyChip(root, Currency.Coins, 200);
            coins.Place(new Vector2(0.5f, 1), new Vector2(130, -204), new Vector2(200, 62));

            var viewport = UI.Rect("Viewport", root);
            viewport.anchorMin = Vector2.zero;
            viewport.anchorMax = Vector2.one;
            viewport.offsetMin = new Vector2(0, 0);
            viewport.offsetMax = new Vector2(0, -250);
            viewport.gameObject.AddComponent<RectMask2D>();
            viewport.gameObject.AddComponent<Image>().color = new Color(0, 0, 0, 0);

            var content = UI.Rect("Content", viewport);
            content.anchorMin = new Vector2(0, 1);
            content.anchorMax = new Vector2(1, 1);
            content.pivot = new Vector2(0.5f, 1);
            content.offsetMin = content.offsetMax = Vector2.zero;
            var grid = content.gameObject.AddComponent<GridLayoutGroup>();
            grid.cellSize = new Vector2(CardW, CardH);
            grid.spacing = new Vector2(30, 34);
            grid.padding = new RectOffset(0, 0, 26, 120);
            grid.childAlignment = TextAnchor.UpperCenter;
            grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            grid.constraintCount = 2;
            content.gameObject.AddComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            var scroll = viewport.gameObject.AddComponent<ScrollRect>();
            scroll.viewport = viewport;
            scroll.content = content;
            scroll.horizontal = false;
            scroll.scrollSensitivity = 40;

            var cats = WordData.Categories;
            int index = 0;
            for (int c = 0; c < cats.Length; c++)
                if (Save.Unlocked(c)) Tween.PopIn(Card(content, c, false), 0.3f, 0.03f * index++);
            for (int c = 0; c < cats.Length; c++)
                if (!Save.Unlocked(c)) Tween.PopIn(Card(content, c, true), 0.3f, 0.03f * index++);
        }

        static string Slug(string name) => name.ToLowerInvariant().Replace(" & ", "_").Replace(' ', '_');

        static RectTransform Card(RectTransform parent, int c, bool locked)
        {
            var cat = WordData.Categories[c];
            int done = Save.Completed(c);
            int total = Mathf.Max(1, cat.LevelCount);
            float pct = Mathf.Clamp01((float)done / total);
            bool complete = !locked && done >= total;
            bool current = !locked && !complete && Save.Data.lastCategory == c;

            var holder = UI.Rect("Card_" + cat.Name, parent);
            // shadow + white face, coloured rim in the category colour
            UI.Img(holder, Sprites.Rounded, new Color(0.42f, 0.25f, 0.06f, 0.28f), "Shadow", 1.2f).rectTransform.Stretch(0, -14, 0, 14);
            var rim = UI.Img(holder, Sprites.Rounded, locked ? Palette.Hex("BFB2A0") : cat.Color, "Rim", 1.2f);
            rim.rectTransform.Stretch();
            rim.raycastTarget = true;
            var face = UI.Img(holder, Sprites.Rounded, Color.white, "Face", 1.2f);
            face.rectTransform.Stretch(8, 8, 8, 8);

            // picture: a slice of the category's map, clipped to a rounded rect
            var mask = UI.Img(holder, Sprites.Rounded, Color.white, "ArtMask", 1.4f);
            mask.rectTransform.anchorMin = new Vector2(0, 1);
            mask.rectTransform.anchorMax = new Vector2(1, 1);
            mask.rectTransform.pivot = new Vector2(0.5f, 1);
            mask.rectTransform.offsetMin = new Vector2(16, -ArtH - 16);
            mask.rectTransform.offsetMax = new Vector2(-16, -16);
            mask.gameObject.AddComponent<Mask>().showMaskGraphic = false;
            var tex = Resources.Load<Texture2D>("CatCards/card_" + Slug(cat.Name));
            if (tex != null)
            {
                var go = new GameObject("Art", typeof(RectTransform), typeof(RawImage));
                var art = (RectTransform)go.transform;
                art.SetParent(mask.transform, false);
                art.Stretch();
                var raw = go.GetComponent<RawImage>();
                raw.texture = tex;
                raw.raycastTarget = false;
                if (locked) raw.color = new Color(0.62f, 0.6f, 0.72f, 1f);
            }
            else UI.Img(mask.transform, null, Palette.Lighten(cat.Color, 0.3f), "ArtFallback").rectTransform.Stretch();

            // icon badge overlapping the art's bottom-left corner
            var icon = Widgets.CategoryIcon(holder, cat, 104);
            icon.Place(new Vector2(0, 1), new Vector2(72, -ArtH - 8), new Vector2(104, 104));

            var name = UI.Label(holder, cat.Name, 40, locked ? Skin.InkSoft : Skin.Ink, TextAnchor.MiddleLeft, false);
            name.rectTransform.Place(new Vector2(0, 1), new Vector2(130 + 160, -ArtH - 50), new Vector2(320, 52));
            name.enableAutoSizing = true;
            name.fontSizeMin = 26;
            name.fontSizeMax = 40;

            if (locked)
            {
                var shade = UI.Img(mask.transform, null, new Color(0.25f, 0.16f, 0.06f, 0.35f), "Dim");
                shade.rectTransform.Stretch();
                var lockBg = UI.Img(mask.transform, Sprites.CircleSprite, new Color(1, 1, 1, 0.92f), "LockBg");
                lockBg.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(110, 110));
                var lockImg = UI.Img(lockBg.transform, Sprites.LockGlyph, Skin.WoodDark, "Lock");
                lockImg.rectTransform.Stretch(26, 26, 26, 26);
                lockImg.preserveAspect = true;

                var cost = UI.Rect("Cost", holder).Place(new Vector2(0.5f, 0), new Vector2(0, 52), new Vector2(300, 64));
                UI.Img(cost, Sprites.Rounded, Skin.Wood, "Bg", 2f).rectTransform.Stretch();
                var star = Widgets.CurrencyIcon(cost, Currency.Stars, 46);
                star.Place(new Vector2(0, 0.5f), new Vector2(40, 0), new Vector2(46, 46));
                var ct = UI.Label(cost, cat.UnlockCost.ToString("N0", CultureInfo.InvariantCulture), 34, Color.white, TextAnchor.MiddleCenter);
                ct.rectTransform.Stretch(60, 0, 10, 0);
                UI.Outlined(ct);

                Button btn = holder.gameObject.AddComponent<Button>();
                btn.transition = Selectable.Transition.None;
                btn.targetGraphic = rim;
                btn.onClick.AddListener(() => { AudioManager.Click(); AskUnlock(c, btn); });
                return holder;
            }

            // stars earned + progress
            int starsEarned = Save.TotalStars(c);
            var starRow = UI.Rect("Stars", holder).Place(new Vector2(0, 1), new Vector2(130 + 160, -ArtH - 98), new Vector2(320, 40));
            var si = Widgets.CurrencyIcon(starRow, Currency.Stars, 34);
            si.Place(new Vector2(0, 0.5f), new Vector2(18, 0), new Vector2(34, 34));
            var st = UI.Label(starRow, starsEarned + " / " + total * 3, 28, Skin.InkSoft, TextAnchor.MiddleLeft, false);
            st.rectTransform.Stretch(44, 0, 0, 0);

            var bar = Widgets.Progress(holder, new Vector2(10, 26), complete ? Skin.Gold : cat.Color, new Color(0.36f, 0.2f, 0.06f, 0.12f));
            bar.Root.anchorMin = new Vector2(0, 0);
            bar.Root.anchorMax = new Vector2(1, 0);
            bar.Root.offsetMin = new Vector2(30, 30);
            bar.Root.offsetMax = new Vector2(-130, 56);
            bar.Set(Mathf.Max(pct, 0.02f));
            var pt = UI.Label(holder, done + "/" + total, 28, Skin.Ink, TextAnchor.MiddleRight, false);
            pt.rectTransform.Place(new Vector2(1, 0), new Vector2(-66, 43), new Vector2(110, 40));

            if (complete || current)
            {
                var tag = UI.Rect("Tag", holder).Place(new Vector2(1, 1), new Vector2(-84, -30), new Vector2(170, 52));
                tag.localRotation = Quaternion.Euler(0, 0, -6);
                UI.Img(tag, Sprites.Rounded, complete ? Skin.Gold : Skin.Green, "Bg", 2.2f).rectTransform.Stretch();
                var tt = UI.Label(tag, complete ? "DONE!" : "PLAYING", 28, Color.white, TextAnchor.MiddleCenter);
                tt.rectTransform.Stretch();
                UI.Outlined(tt);
                if (current) tag.gameObject.AddComponent<Pulse>().Amount = 0.04f;
            }

            var open = holder.gameObject.AddComponent<Button>();
            open.transition = Selectable.Transition.None;
            open.targetGraphic = rim;
            open.onClick.AddListener(() => { AudioManager.Click(); ZWordApp.I.ShowMap(c); });
            return holder;
        }

        static void AskUnlock(int c, Button row)
        {
            var cat = WordData.Categories[c];
            var body = Widgets.WoodPopup("UNLOCK", new Vector2(760, 720));

            var icon = Widgets.CategoryIcon(body, cat, 150);
            icon.Place(new Vector2(0.5f, 1), new Vector2(0, -110), new Vector2(150, 150));
            var name = UI.Label(body, cat.Name, 56, Skin.Ink, TextAnchor.MiddleCenter, false);
            name.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -230), new Vector2(640, 70));
            var info = UI.Label(body, cat.LevelCount + " new levels", 34, Skin.InkSoft, TextAnchor.MiddleCenter, false);
            info.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -285), new Vector2(640, 50));

            bool canStars = Save.StarPoints >= cat.UnlockCost;
            var withStars = Widgets.PriceButton(body, new Vector2(520, 120), Currency.Stars, cat.UnlockCost.ToString("N0", CultureInfo.InvariantCulture), () =>
            {
                if (Save.TryUnlock(c)) Unlocked(c);
                else { AudioManager.Error(); ZWordApp.Toast(body, "NOT ENOUGH STARS", new Vector2(0, 0), Palette.Yellow); }
            }, canStars ? Skin.Green : Palette.Hex("A99C88"));
            ((RectTransform)withStars.transform).Place(new Vector2(0.5f, 1), new Vector2(0, -390), new Vector2(520, 120));

            int gems = GameConfig.UnlockGems(cat.Group);
            var withGems = Widgets.PriceButton(body, new Vector2(520, 120), Currency.Gems, gems + "  INSTANT", () =>
            {
                if (Save.TryUnlockWithGems(c)) Unlocked(c);
                else { AudioManager.Error(); ZWordApp.Toast(body, "NOT ENOUGH GEMS", new Vector2(0, 0), Palette.Yellow); }
            }, Skin.Purple);
            ((RectTransform)withGems.transform).Place(new Vector2(0.5f, 1), new Vector2(0, -530), new Vector2(520, 120));
        }

        static void Unlocked(int c)
        {
            AudioManager.Win();
            ZWordApp.I.ClosePopups();
            ZWordApp.I.ShowCategories();
        }
    }
}
