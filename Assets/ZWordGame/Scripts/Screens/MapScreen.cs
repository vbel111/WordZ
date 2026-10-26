using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>
    /// Category level map (mockup screen 3): themed background, a winding dotted path with 25 level
    /// nodes, auto-scroll to the current level, and a progress card with a reward chest.
    /// </summary>
    public static class MapScreen
    {
        const float ContentW = 1080f;

        public static void Build(RectTransform root, int cat)
        {
            var category = WordData.Categories[cat];
            int count = Mathf.Max(1, category.LevelCount);
            int current = Mathf.Min(Save.Completed(cat), count - 1);

            Widgets.Header(root, category.Name, "LV " + (current + 1), () => ZWordApp.I.ShowCategories());
            ZWordApp.I.OnBack = () => ZWordApp.I.ShowCategories();

            // scroll area between header and progress card
            var viewport = UI.Rect("Viewport", root);
            viewport.anchorMin = Vector2.zero;
            viewport.anchorMax = Vector2.one;
            viewport.offsetMin = new Vector2(0, 0);
            viewport.offsetMax = new Vector2(0, -180);
            viewport.gameObject.AddComponent<RectMask2D>();
            viewport.gameObject.AddComponent<Image>().color = new Color(0, 0, 0, 0);
            SafeAreaBleed.Add(viewport); // map art also fills the notch / home-bar area

            var art = Theme.Current.ArtFor(category.Name);
            var bgSprite = art != null ? art.mapBackground : null;
            float contentH = bgSprite != null ? ContentW * bgSprite.rect.height / bgSprite.rect.width : 2400f;
            contentH = Mathf.Max(contentH, 300f * count / 2f + 600f);

            var content = UI.Rect("Content", viewport);
            content.anchorMin = new Vector2(0.5f, 1);
            content.anchorMax = new Vector2(0.5f, 1);
            content.pivot = new Vector2(0.5f, 1);
            content.sizeDelta = new Vector2(ContentW, contentH);
            content.anchoredPosition = Vector2.zero;

            RectTransform parallaxBg = null;
            float bgH = 0f;
            if (bgSprite != null)
            {
                // The art is shown whole and undistorted behind the path and scrolls slower than the
                // levels (parallax): level 1 sits on the bottom of the picture, level 25 under its sky.
                var bg = UI.Img(viewport, bgSprite, Color.white, "MapBg");
                parallaxBg = bg.rectTransform;
                parallaxBg.SetAsFirstSibling();
                parallaxBg.anchorMin = parallaxBg.anchorMax = new Vector2(0.5f, 0);
                parallaxBg.pivot = new Vector2(0.5f, 0);
                bgH = ContentW * bgSprite.rect.height / bgSprite.rect.width;
                parallaxBg.sizeDelta = new Vector2(ContentW, bgH);
                // soft shade down the middle so the level path reads on busy art
                var shade = UI.Img(parallaxBg, Sprites.Soft, new Color(0.3f, 0.17f, 0.05f, 0.18f), "PathShade");
                shade.rectTransform.anchorMin = new Vector2(0.5f, 0);
                shade.rectTransform.anchorMax = new Vector2(0.5f, 1);
                shade.rectTransform.sizeDelta = new Vector2(760, 0);
                shade.rectTransform.anchoredPosition = Vector2.zero;
            }
            else
            {
                var bg = UI.Img(content, null, Palette.Lighten(category.Color, 0.35f), "MapBg");
                bg.rectTransform.Stretch();
            }

            // living background: leaves, bubbles, stars, birds... over the visible part of the map
            var (kind, tint) = Ambience.ForCategory(category.Name);
            var amb = Ambience.Add(content, kind, tint, 26, kind == AmbienceKind.Rain ? 14f : 3.5f);
            amb.VisibleArea = () =>
            {
                float s = content.anchoredPosition.y;
                float vh = viewport.rect.height;
                float top = contentH / 2f - s;
                return new Rect(-ContentW / 2f, top - vh, ContentW, vh);
            };
            if (kind == AmbienceKind.Birds || kind == AmbienceKind.Leaves)
            {
                var clouds = Ambience.Add(content, AmbienceKind.Clouds, new Color(1, 1, 1, 0.75f), 4, 0.2f);
                clouds.VisibleArea = amb.VisibleArea;
            }

            var scroll = viewport.gameObject.AddComponent<ScrollRect>();
            scroll.viewport = viewport;
            scroll.content = content;
            scroll.horizontal = false;
            scroll.movementType = ScrollRect.MovementType.Clamped;
            scroll.scrollSensitivity = 40;

            // node positions: level 1 at the bottom, winding upwards
            float bottomPad = 330f, topPad = 260f;
            var pos = new List<Vector2>();
            for (int i = 0; i < count; i++)
            {
                float y = bottomPad + (contentH - bottomPad - topPad) * i / Mathf.Max(1, count - 1);
                float x = ContentW / 2f + Mathf.Sin(i * 0.95f) * 270f;
                pos.Add(new Vector2(x, y));
            }

            // dotted path
            var pathLayer = UI.Rect("Path", content).Stretch();
            for (int i = 0; i + 1 < pos.Count; i++)
            {
                var a = pos[i]; var b = pos[i + 1];
                int dots = Mathf.Max(3, Mathf.RoundToInt(Vector2.Distance(a, b) / 34f));
                for (int k = 1; k < dots; k++)
                {
                    float t = k / (float)dots;
                    var p = Vector2.Lerp(a, b, t) + new Vector2(Mathf.Sin(t * Mathf.PI) * 30f * (i % 2 == 0 ? 1 : -1), 0);
                    bool doneSeg = i < current;
                    var dot = UI.Img(pathLayer, Sprites.CircleSprite, new Color(0.36f, 0.2f, 0.06f, 0.85f), "DotBorder");
                    dot.rectTransform.anchorMin = dot.rectTransform.anchorMax = Vector2.zero;
                    dot.rectTransform.anchoredPosition = p;
                    dot.rectTransform.sizeDelta = new Vector2(24, 24);
                    var inner = UI.Img(dot.transform, Sprites.CircleSprite, doneSeg ? Skin.Gold : Skin.Cream, "Dot");
                    inner.rectTransform.Stretch(4, 4, 4, 4);
                }
            }

            // nodes
            var nodeLayer = UI.Rect("Nodes", content).Stretch();
            for (int i = 0; i < count; i++) Node(nodeLayer, cat, i, current, pos[i]);

            BuildProgressCard(root, cat);

            // scroll so the current level sits a bit below the middle
            Canvas.ForceUpdateCanvases();
            float viewH = viewport.rect.height > 10 ? viewport.rect.height : 1500f;
            float target = pos[current].y - viewH * 0.4f;              // distance from content bottom
            float range = Mathf.Max(1f, contentH - viewH);
            scroll.verticalNormalizedPosition = Mathf.Clamp01(target / range);

            if (parallaxBg != null)
            {
                void Parallax(float t)
                {
                    float vh = viewport.rect.height > 10 ? viewport.rect.height : viewH;
                    // grow the picture if the screen is taller than it (tablets / tall phones)
                    float scale = Mathf.Max(1f, vh / bgH, viewport.rect.width / ContentW);
                    parallaxBg.localScale = new Vector3(scale, scale, 1);
                    float extra = Mathf.Max(0f, bgH * scale - vh);
                    parallaxBg.anchoredPosition = new Vector2(0, -extra * Mathf.Clamp01(t));
                }
                scroll.onValueChanged.AddListener(v => Parallax(v.y));
                Parallax(scroll.verticalNormalizedPosition);
            }
        }

        static void Node(RectTransform parent, int cat, int i, int current, Vector2 p)
        {
            bool done = i < Save.Completed(cat);
            bool isCurrent = i == current && !done;
            bool locked = !done && !isCurrent;
            bool boss = LevelDatabase.IsBoss(cat, i);
            float size = (isCurrent ? 150 : 112) * (boss ? 1.25f : 1f);

            var root = UI.Rect("Level" + (i + 1), parent);
            root.anchorMin = root.anchorMax = Vector2.zero;
            root.anchoredPosition = p;
            root.sizeDelta = new Vector2(size, size);

            Color face = isCurrent ? Skin.Gold : done ? Palette.Hex("DCD6E4") : Palette.Hex("8D8496");
            var btn = UI.Chunky(root, new Vector2(size, size), face, null, 0, () =>
            {
                if (locked)
                {
                    AudioManager.Error();
                    Tween.Shake(root, 10f);
                    return;
                }
                ZWordApp.I.StartLevel(cat, i);
            }, Sprites.CircleSprite, 1f, size * 0.08f);
            ((RectTransform)btn.transform).Stretch();

            var faceT = btn.transform.Find("Body/Face");
            var ring = UI.Img(faceT, Sprites.Ring, new Color(1, 1, 1, 0.55f), "Ring");
            ring.rectTransform.Stretch(6, 6, 6, 6);
            if (locked)
            {
                var l = UI.Img(faceT, Sprites.LockGlyph, new Color(1, 1, 1, 0.9f), "Lock");
                l.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(size * 0.42f, size * 0.42f));
                l.preserveAspect = true;
            }
            else
            {
                var t = UI.Label(faceT, (i + 1).ToString(), size * 0.46f, isCurrent ? Color.white : Skin.Ink, TextAnchor.MiddleCenter, false);
                t.rectTransform.Stretch(0, size * 0.04f, 0, 0);
                if (isCurrent) UI.Outlined(t);
            }

            if (done)
            {
                int stars = Save.Stars(cat, i);
                var starSprite = Theme.Current.iconStar != null ? Theme.Current.iconStar : Sprites.Star;
                for (int s = 0; s < 3; s++)
                {
                    var st = UI.Img(root, starSprite, s < stars ? Color.white : new Color(0.3f, 0.25f, 0.3f, 0.75f), "Star" + s);
                    st.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(-34 + s * 34, -14 + (s == 1 ? -6 : 0)), new Vector2(40, 40));
                }
            }
            if (boss)
            {
                // boss node: crown on top (gold once beaten) and a BOSS label
                var crownSprite = Theme.Current.crown;
                if (crownSprite != null)
                {
                    var crown = UI.Img(root, crownSprite, Save.HasCrown(cat) || !locked ? Color.white : new Color(0.55f, 0.5f, 0.5f, 1f), "Crown");
                    crown.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(isCurrent ? 70 : 0, 26), new Vector2(size * 0.62f, size * 0.5f));
                    crown.preserveAspect = true;
                }
                var tag = UI.Label(root, "BOSS", 30, Color.white, TextAnchor.MiddleCenter);
                tag.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, done ? -56 : -22), new Vector2(160, 40));
                UI.Outlined(tag);
            }
            if (isCurrent)
            {
                root.gameObject.AddComponent<Pulse>().Amount = 0.06f;
                // glow + "you are here" marker
                var glow = UI.Img(root, Sprites.Soft, new Color(1f, 0.9f, 0.4f, 0.8f), "Glow");
                glow.rectTransform.Stretch(-70, -70, -70, -70);
                glow.transform.SetAsFirstSibling();
                var av = Theme.Current.iconAvatar != null ? Theme.Current.iconAvatar : Sprites.AvatarGlyph;
                var pin = UI.Rect("YouAreHere", root).Place(new Vector2(0.5f, 1), new Vector2(0, 70), new Vector2(96, 96));
                UI.Img(pin, Sprites.CircleSprite, Color.white, "Ring").rectTransform.Stretch(-6, -6, -6, -6);
                UI.Img(pin, av, Color.white, "Avatar").rectTransform.Stretch();
                var tip = UI.Img(pin, Sprites.Play, Color.white, "Tip");
                tip.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, -14), new Vector2(34, 34));
                tip.rectTransform.localRotation = Quaternion.Euler(0, 0, -90);
                var bob = pin.gameObject.AddComponent<Bobber>();
                bob.Amplitude = 10; bob.Tilt = 0; bob.Speed = 3f;
            }
        }

        static void BuildProgressCard(RectTransform root, int cat)
        {
            var category = WordData.Categories[cat];
            int maxStars = category.LevelCount * 3;
            int have = Save.TotalStars(cat);

            var card = Widgets.Card(root, new Vector2(900, 170));
            card.Place(new Vector2(0.5f, 0), new Vector2(0, 120), new Vector2(900, 170));

            var title = UI.Label(card, category.Name + " PROGRESS", 34, Skin.Ink, TextAnchor.MiddleLeft, false);
            title.rectTransform.Place(new Vector2(0, 1), new Vector2(40 + 260, -38), new Vector2(520, 46));

            var star = Widgets.CurrencyIcon(card, Currency.Stars, 56);
            star.Place(new Vector2(0, 0), new Vector2(66, 54), new Vector2(56, 56));
            var bar = Widgets.Progress(card, new Vector2(540, 48), Skin.Gold, Skin.CreamShade, true);
            bar.Root.Place(new Vector2(0, 0), new Vector2(110 + 270, 54), new Vector2(540, 48));
            bar.Set((float)have / Mathf.Max(1, maxStars), have + " / " + maxStars);
            bar.Label.color = Skin.Ink;
            bar.Label.fontSharedMaterial = Fonts.Plain;

            // chest at the next threshold
            int opened = Save.ChestsOpened(cat);
            bool allOpened = opened >= GameConfig.ChestStars.Length;
            int need = allOpened ? 0 : GameConfig.ChestStars[opened];
            bool ready = !allOpened && have >= need;
            var chestSprite = ready || allOpened ? (Theme.Current.chestOpen != null ? Theme.Current.chestOpen : Theme.Current.chest) : Theme.Current.chest;
            Button chestBtn;
            if (chestSprite != null) chestBtn = UI.FlatIcon(card, chestSprite, new Vector2(150, 150), Color.white, () => OpenChest(cat));
            else chestBtn = Widgets.RoundButton(card, Sprites.Star, 130, Skin.Wood, () => OpenChest(cat));
            ((RectTransform)chestBtn.transform).Place(new Vector2(1, 0.5f), new Vector2(-86, 10), new Vector2(150, 150));
            chestBtn.transform.Find("Face")?.GetComponent<Image>()?.SetPreserveAspect();
            if (ready)
            {
                chestBtn.gameObject.AddComponent<Pulse>().Amount = 0.08f;
                Widgets.Badge(chestBtn.transform, "!", 46);
            }
            else if (!allOpened)
            {
                // the font has no star glyph, so draw the number + a star sprite
                var needLbl = UI.Label(card, need.ToString(), 28, Skin.InkSoft, TextAnchor.MiddleRight, false);
                needLbl.rectTransform.Place(new Vector2(1, 0), new Vector2(-106, 22), new Vector2(80, 34));
                var needStar = UI.Img(card, Sprites.Star, Skin.Gold, "NeedStar");
                needStar.rectTransform.Place(new Vector2(1, 0), new Vector2(-50, 22), new Vector2(30, 30));
                needStar.preserveAspect = true;
            }
        }

        static void OpenChest(int cat)
        {
            int opened = Save.ChestsOpened(cat);
            if (opened >= GameConfig.ChestStars.Length)
            {
                ZWordApp.Toast(ZWordApp.I.CurrentScreen, "ALL CHESTS OPENED!", new Vector2(0, -500), Palette.Yellow);
                return;
            }
            int need = GameConfig.ChestStars[opened];
            if (Save.TotalStars(cat) < need)
            {
                AudioManager.Error();
                ZWordApp.Toast(ZWordApp.I.CurrentScreen, "COLLECT " + need + " STARS TO OPEN", new Vector2(0, -500), Palette.Yellow);
                return;
            }
            int coins = GameConfig.ChestCoins[opened], gems = GameConfig.ChestGems[opened];
            Save.SetChestsOpened(cat, opened + 1);
            Save.Coins += coins;
            Save.Gems += gems;
            ZWordApp.I.ShowReward("CHEST OPENED!", coins, gems, () => ZWordApp.I.ShowMap(cat));
        }
    }

    static class ImageExt
    {
        public static void SetPreserveAspect(this Image img) { if (img != null) img.preserveAspect = true; }
    }
}
