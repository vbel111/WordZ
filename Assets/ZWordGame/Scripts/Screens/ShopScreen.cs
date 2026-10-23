using System.Globalization;
using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>Shop (mockup screen 11): COINS / HINTS / GEMS tabs with pack cards.</summary>
    public static class ShopScreen
    {
        static readonly string[] Tabs = { "COINS", "HINTS", "GEMS" };

        public static void Open(int tab = 0)
        {
            var root = Widgets.FullPanel("SHOP", () => Save.Write());

            var coins = Widgets.CurrencyChip(root, Currency.Coins, 200);
            coins.Place(new Vector2(1, 1), new Vector2(-118, -104), new Vector2(200, 66));
            var gems = Widgets.CurrencyChip(root, Currency.Gems, 160);
            gems.Place(new Vector2(0, 1), new Vector2(250, -198), new Vector2(160, 62));

            var content = UI.Rect("TabContent", root);
            content.anchorMin = Vector2.zero;
            content.anchorMax = Vector2.one;
            content.offsetMin = new Vector2(0, 40);
            content.offsetMax = new Vector2(0, -360);

            // tab bar
            var bar = UI.Rect("Tabs", root).Place(new Vector2(0.5f, 1), new Vector2(0, -290), new Vector2(900, 96));
            UI.Img(bar, Sprites.Rounded, new Color(0.36f, 0.2f, 0.06f, 0.45f), "Bg", 1.6f).rectTransform.Stretch(-8, -8, -8, -8);
            var tabButtons = new Image[Tabs.Length];
            for (int i = 0; i < Tabs.Length; i++)
            {
                int idx = i;
                var tb = UI.Rect("Tab_" + Tabs[i], bar);
                tb.anchorMin = new Vector2(i / 3f, 0);
                tb.anchorMax = new Vector2((i + 1) / 3f, 1);
                tb.offsetMin = new Vector2(6, 0);
                tb.offsetMax = new Vector2(-6, 0);
                var bg = UI.Img(tb, Sprites.Rounded, Color.white, "Bg", 1.8f);
                bg.rectTransform.Stretch();
                bg.raycastTarget = true;
                tabButtons[i] = bg;
                var lbl = UI.Label(tb, Tabs[i], 36, Color.white, TextAnchor.MiddleCenter);
                lbl.rectTransform.Stretch();
                UI.Outlined(lbl);
                var b = tb.gameObject.AddComponent<Button>();
                b.transition = Selectable.Transition.None;
                b.targetGraphic = bg;
                b.onClick.AddListener(() => { AudioManager.Click(); Show(idx); });
            }

            void Show(int which)
            {
                for (int i = 0; i < tabButtons.Length; i++)
                    tabButtons[i].color = i == which ? Skin.Green : Skin.Wood;
                for (int i = content.childCount - 1; i >= 0; i--) Object.Destroy(content.GetChild(i).gameObject);
                if (which == 0) CoinsTab(content);
                else if (which == 1) HintsTab(content);
                else GemsTab(content);
            }
            Show(Mathf.Clamp(tab, 0, Tabs.Length - 1));
        }

        // ---------------- tabs ----------------

        static void CoinsTab(RectTransform content)
        {
            var packs = GameConfig.CoinPacks;
            for (int i = 0; i < packs.Length; i++)
            {
                var (id, amount, price, tag) = packs[i];
                var card = PackCard(content, i, tag);
                CoinStack(card, Mathf.Min(3, i + 1));
                Title(card, amount.ToString("N0", CultureInfo.InvariantCulture) + " Coins");
                Buy(card, null, Store.Price(id, price), () => Purchase(content, id, null));
            }
        }

        static void HintsTab(RectTransform content)
        {
            var bundles = GameConfig.HintBundles;
            for (int i = 0; i < bundles.Length; i++)
            {
                var (booster, amount, cost, title) = bundles[i];
                var card = PackCard(content, i, null);
                var icon = UI.Img(card, BoosterIcon(booster), Color.white, "Icon");
                icon.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(96, 0), new Vector2(110, 110));
                icon.preserveAspect = true;
                Title(card, title);
                var own = UI.Label(card, "You have " + Save.GetBooster(booster), 26, Skin.InkSoft, TextAnchor.MiddleLeft, false);
                own.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(190 + 220, -30), new Vector2(440, 36));
                Buy(card, Currency.Coins, cost.ToString(), () =>
                {
                    if (!Save.TrySpendCoins(cost))
                    {
                        AudioManager.Error();
                        ZWordApp.Toast(content, "NOT ENOUGH COINS", Vector2.zero, Palette.Yellow);
                        return;
                    }
                    Save.SetBooster(booster, Save.GetBooster(booster) + amount);
                    own.text = "You have " + Save.GetBooster(booster);
                    AudioManager.Bonus();
                    Tween.Punch(card, 0.06f);
                    ZWordApp.Toast(content, "+" + amount + " " + title.Substring(title.IndexOf(' ') + 1).ToUpperInvariant(), Vector2.zero, Palette.Hex("7CF06B"));
                });
            }
        }

        static void GemsTab(RectTransform content)
        {
            var packs = GameConfig.GemPacks;
            int i = 0;
            for (; i < packs.Length; i++)
            {
                var (id, amount, price, tag) = packs[i];
                var card = PackCard(content, i, tag);
                var g = Widgets.CurrencyIcon(card, Currency.Gems, 96 + i * 8);
                g.Place(new Vector2(0, 0.5f), new Vector2(96, 0), Vector2.one * (96 + i * 8));
                Title(card, amount + " Gems");
                Buy(card, null, Store.Price(id, price), () => Purchase(content, id, null));
            }
            // Supporter Pack (one-time): replaces "Remove Ads" since Word Z has no ads
            var sup = PackCard(content, i, Save.Data.supporter ? "THANK YOU!" : "SUPPORT US");
            var gift = UI.Img(sup, Theme.Current.gift != null ? Theme.Current.gift : Sprites.Star, Color.white, "Icon");
            gift.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(96, 0), new Vector2(110, 110));
            gift.preserveAspect = true;
            Title(sup, "Supporter Pack");
            var what = UI.Label(sup, GameConfig.SupporterCoins.ToString("N0", CultureInfo.InvariantCulture) + " coins, " + GameConfig.SupporterGems + " gems, "
                + GameConfig.SupporterBoosters + " of every hint", 24, Skin.InkSoft, TextAnchor.MiddleLeft, false);
            what.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(190 + 220, -34), new Vector2(440, 36));
            if (Save.Data.supporter)
            {
                var owned = UI.Label(sup, "OWNED", 36, Skin.Green, TextAnchor.MiddleCenter);
                owned.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-130, 0), new Vector2(210, 100));
            }
            else Buy(sup, null, Store.Price(GameConfig.SupporterId, GameConfig.SupporterPrice),
                () => Purchase(content, GameConfig.SupporterId, () => ShopScreen.Open(2)));

            // Apple requires a way to restore non-consumable purchases
            var restore = UI.Chunky(content, new Vector2(420, 90), Skin.Wood, "RESTORE PURCHASES", 32, () =>
            {
                AudioManager.Click();
                Store.Restore((ok, msg) =>
                {
                    if (msg != null) ZWordApp.Toast(content, msg, Vector2.zero, ok ? Palette.Hex("7CF06B") : Palette.Yellow);
                    if (ok && Save.Data.supporter) ShopScreen.Open(2);
                });
            });
            ((RectTransform)restore.transform).Place(new Vector2(0.5f, 1), new Vector2(0, -100 - (i + 1) * 196 + 20), new Vector2(420, 90));
        }

        // ---------------- pieces ----------------

        static RectTransform PackCard(RectTransform content, int index, string tag)
        {
            var card = Widgets.Card(content, new Vector2(880, 170));
            card.Place(new Vector2(0.5f, 1), new Vector2(0, -100 - index * 196), new Vector2(880, 170));
            Tween.PopIn(card, 0.25f, index * 0.05f);
            if (!string.IsNullOrEmpty(tag))
            {
                var r = UI.Rect("Tag", card).Place(new Vector2(1, 1), new Vector2(-180, 4), new Vector2(220, 52));
                UI.Img(r, Sprites.Rounded, Skin.Red, "Bg", 2.4f).rectTransform.Stretch();
                var t = UI.Label(r, tag, 26, Color.white, TextAnchor.MiddleCenter);
                t.rectTransform.Stretch();
            }
            return card;
        }

        static void Title(RectTransform card, string text)
        {
            var t = UI.Label(card, text, 44, Skin.Ink, TextAnchor.MiddleLeft, false);
            t.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(190 + 220, 10), new Vector2(440, 60));
        }

        static void Buy(RectTransform card, Currency? icon, string price, System.Action onBuy)
        {
            var b = Widgets.PriceButton(card, new Vector2(210, 100), icon, price, onBuy);
            ((RectTransform)b.transform).Place(new Vector2(1, 0.5f), new Vector2(-130, 0), new Vector2(210, 100));
        }

        /// <summary>1-3 overlapping coins.</summary>
        static void CoinStack(RectTransform card, int n)
        {
            for (int k = 0; k < n; k++)
            {
                var c = Widgets.CurrencyIcon(card, Currency.Coins, 86);
                c.Place(new Vector2(0, 0.5f), new Vector2(76 + k * 22, -14 + k * 16), new Vector2(86, 86));
            }
        }

        static Sprite BoosterIcon(Booster b)
        {
            var t = Theme.Current;
            switch (b)
            {
                case Booster.Letter: return t.iconLetter != null ? t.iconLetter : Sprites.Letters;
                case Booster.Shuffle: return t.iconShuffle != null ? t.iconShuffle : Sprites.ShuffleGlyph;
                case Booster.Time: return t.iconClock != null ? t.iconClock : Sprites.Clock;
                case Booster.Reveal: return t.iconMagnifier != null ? t.iconMagnifier : Sprites.Magnifier;
                default: return t.iconWand != null ? t.iconWand : Sprites.TargetGlyph;
            }
        }

        static void Purchase(RectTransform content, string id, System.Action after)
        {
            AudioManager.Click();
            Store.Buy(id, (ok, msg) =>
            {
                if (ok)
                {
                    AudioManager.Win();
                    Haptics.Success();
                    ZWordApp.Toast(content, "THANK YOU!", Vector2.zero, Palette.Hex("7CF06B"));
                    after?.Invoke();
                }
                else if (msg != null)
                {
                    AudioManager.Error();
                    ZWordApp.Toast(content, msg, Vector2.zero, Palette.Yellow);
                }
            });
        }
    }
}
