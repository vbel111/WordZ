using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>Daily reward calendar popup, Daily Challenges page (mockup screen 10) and Quests page.</summary>
    public static class MetaScreens
    {
        // ---------------- Daily reward ----------------

        public static void OpenDailyReward()
        {
            var body = Widgets.WoodPopup("DAILY REWARD", new Vector2(900, 1080));
            int next = DailyRewards.NextDay;
            bool can = DailyRewards.CanClaim;
            // "claimed" days: those before the next day (when today is still claimable) or up to it (already claimed today)
            int claimedUpTo = can ? next : (next == 0 ? 7 : next);

            for (int i = 0; i < 7; i++)
            {
                bool big = i == 6;
                Vector2 size = big ? new Vector2(740, 190) : new Vector2(230, 230);
                Vector2 pos = big ? new Vector2(0, -632) : new Vector2(-250 + (i % 3) * 250, -138 - (i / 3) * 250);
                var tile = Widgets.Card(body, size, i == next && can ? Palette.Hex("FFF1C2") : Color.white);
                tile.Place(new Vector2(0.5f, 1), pos, size);

                var day = UI.Label(tile, "DAY " + (i + 1), 30, Skin.InkSoft, TextAnchor.MiddleCenter, false);
                day.rectTransform.Place(new Vector2(big ? 0 : 0.5f, 1), new Vector2(big ? 150 : 0, -30), new Vector2(200, 40));

                int coins = GameConfig.DailyCoins[i], gems = GameConfig.DailyGems[i];
                if (big)
                {
                    // big chest on the left, coin and gem amounts side by side on the right
                    var chest = Theme.Current.chestPurple != null ? Theme.Current.chestPurple : Theme.Current.chest;
                    if (chest != null)
                    {
                        var c = UI.Img(tile, chest, Color.white, "Chest");
                        c.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(150, -24), new Vector2(118, 118));
                        c.preserveAspect = true;
                    }
                    var ci = Widgets.CurrencyIcon(tile, Currency.Coins, 60);
                    ci.Place(new Vector2(0.5f, 0.5f), new Vector2(-30, -6), new Vector2(60, 60));
                    var ct = UI.Label(tile, "+" + coins, 44, Skin.Ink, TextAnchor.MiddleLeft, false);
                    ct.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(70, -6), new Vector2(130, 60));
                    var gi = Widgets.CurrencyIcon(tile, Currency.Gems, 60);
                    gi.Place(new Vector2(0.5f, 0.5f), new Vector2(170, -6), new Vector2(60, 60));
                    var gt = UI.Label(tile, "+" + gems, 44, Skin.Ink, TextAnchor.MiddleLeft, false);
                    gt.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(250, -6), new Vector2(100, 60));
                }
                else
                {
                    var icon = Widgets.CurrencyIcon(tile, gems > 0 ? Currency.Gems : Currency.Coins, 96);
                    icon.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 4), new Vector2(96, 96));
                    var amt = UI.Label(tile, "+" + coins, 32, Skin.Ink, TextAnchor.MiddleCenter, false);
                    amt.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(gems > 0 ? -22 : 0, 32), new Vector2(150, 44));
                    if (gems > 0)
                    {
                        var g = Widgets.CurrencyIcon(tile, Currency.Gems, 34);
                        g.Place(new Vector2(0.5f, 0), new Vector2(54, 32), new Vector2(34, 34));
                        var gl = UI.Label(tile, "+" + gems, 30, Skin.Ink, TextAnchor.MiddleLeft, false);
                        gl.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(104, 32), new Vector2(60, 44));
                    }
                }

                if (i < claimedUpTo)
                {
                    UI.Img(tile, Sprites.Rounded, new Color(1, 1, 1, 0.6f), "Done", 0.9f).rectTransform.Stretch();
                    var chk = UI.Img(tile, Theme.Current.iconCheck != null ? Theme.Current.iconCheck : Sprites.Check, Color.white, "Check");
                    chk.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(90, 90));
                }
                else if (i == next && can) tile.gameObject.AddComponent<Pulse>().Amount = 0.04f;
            }

            if (can)
            {
                var claim = Widgets.IconTextButton(body, new Vector2(520, 120), Skin.Green, "CLAIM", null, 54, () =>
                {
                    var (c, g) = DailyRewards.Claim();
                    ZWordApp.I.ShowReward("DAY " + (next + 1) + " REWARD", c, g);
                });
                ((RectTransform)claim.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 30), new Vector2(520, 120));
            }
            else
            {
                var wait = UI.Label(body, "Next reward in " + Day.Countdown(), 38, Skin.InkSoft, TextAnchor.MiddleCenter, false);
                wait.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 70), new Vector2(700, 60));
                wait.gameObject.AddComponent<Ticker>().OnTick = () => { if (wait) wait.text = "Next reward in " + Day.Countdown(); };
            }
        }

        // ---------------- Daily challenges ----------------

        public static void OpenChallenges()
        {
            var root = Widgets.FullPanel("CHALLENGES");
            Build(root);
        }

        static void Build(RectTransform root)
        {
            var content = UI.Rect("Content", root).Stretch(0, 0, 0, 180);

            var timer = UI.Rect("Timer", content).Place(new Vector2(0.5f, 1), new Vector2(0, -50), new Vector2(300, 66));
            UI.Img(timer, Sprites.Rounded, Skin.ChipBg, "Bg", 1.6f).rectTransform.Stretch();
            var tIcon = UI.Img(timer, Theme.Current.timer != null ? Theme.Current.timer : Sprites.Clock, Color.white, "Clock");
            tIcon.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(40, 0), new Vector2(50, 50));
            tIcon.preserveAspect = true;
            var tText = UI.Label(timer, Day.Countdown(), 34, Color.white, TextAnchor.MiddleCenter);
            tText.rectTransform.Stretch(60, 0, 10, 0);
            timer.gameObject.AddComponent<Ticker>().OnTick = () => { if (tText) tText.text = Day.Countdown(); };

            for (int i = 0; i < Challenges.Count; i++)
            {
                int slot = i;
                var def = Challenges.Get(slot);
                int prog = Challenges.Progress(slot);
                bool complete = Challenges.Complete(slot), claimed = Challenges.Claimed(slot);

                var card = Widgets.Card(content, new Vector2(900, 190), claimed ? Palette.Hex("F6EEE1") : Skin.Cream);
                card.Place(new Vector2(0.5f, 1), new Vector2(0, -190 - i * 214), new Vector2(900, 190));
                Tween.PopIn(card, 0.25f, i * 0.06f);

                var circle = UI.Rect("Check", card).Place(new Vector2(0, 0.5f), new Vector2(76, 0), new Vector2(88, 88));
                UI.Img(circle, Sprites.CircleSprite, complete ? Skin.Gold : Palette.Hex("FBEACB"), "Bg").rectTransform.Stretch();
                if (complete)
                {
                    var chk = UI.Img(circle, Sprites.Check, Color.white, "Tick");
                    chk.rectTransform.Stretch(16, 16, 16, 16);
                }

                var title = UI.Label(card, def.Text, 38, Skin.Ink, TextAnchor.MiddleLeft, false);
                title.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(150 + 230, 34), new Vector2(460, 50));
                var bar = Widgets.Progress(card, new Vector2(440, 40), Skin.Green, Skin.CreamShade, true);
                bar.Root.Place(new Vector2(0, 0.5f), new Vector2(150 + 220, -30), new Vector2(440, 40));
                bar.Set((float)prog / def.Target, prog.ToString("N0") + "/" + def.Target.ToString("N0"));
                bar.Label.color = Skin.Ink;
                bar.Label.fontSharedMaterial = Fonts.Plain;

                Color btnColor = claimed ? Palette.Hex("CFC2AE") : complete ? Skin.Green : Palette.Hex("F2B53A");
                string label = claimed ? "DONE" : def.Coins.ToString();
                var btn = Widgets.PriceButton(card, new Vector2(190, 96), claimed ? (Currency?)null : Currency.Coins, label, () =>
                {
                    if (Challenges.Claimed(slot)) return;
                    if (!Challenges.Complete(slot))
                    {
                        AudioManager.Error();
                        ZWordApp.Toast(root, "KEEP PLAYING TO FINISH!", new Vector2(0, -200), Palette.Yellow);
                        return;
                    }
                    int coins = Challenges.Claim(slot);
                    ZWordApp.I.ShowReward("CHALLENGE DONE!", coins, 0, () => MetaScreens.OpenChallenges());
                }, btnColor);
                ((RectTransform)btn.transform).Place(new Vector2(1, 0.5f), new Vector2(-120, 0), new Vector2(190, 96));
                if (complete && !claimed) btn.gameObject.AddComponent<Pulse>().Amount = 0.05f;
            }

            // all-done chest
            var bonus = Widgets.Card(content, new Vector2(900, 300));
            bonus.Place(new Vector2(0.5f, 1), new Vector2(0, -190 - Challenges.Count * 214 - 70), new Vector2(900, 300));
            var chestSprite = Theme.Current.chestPurple != null ? Theme.Current.chestPurple : Theme.Current.chest;
            if (chestSprite != null)
            {
                var chest = UI.Img(bonus, chestSprite, Color.white, "Chest");
                chest.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(150, 10), new Vector2(210, 210));
                chest.preserveAspect = true;
                if (Challenges.BonusReady) chest.gameObject.AddComponent<Pulse>().Amount = 0.07f;
            }
            var msg = UI.Label(bonus, "Complete all challenges\nto get a special reward!", 34, Skin.Ink, TextAnchor.MiddleLeft, false);
            msg.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(290 + 270, 60), new Vector2(540, 100));
            var allBar = Widgets.Progress(bonus, new Vector2(520, 46), Skin.Gold, Skin.CreamShade, true);
            allBar.Root.Place(new Vector2(0, 0.5f), new Vector2(290 + 260, -40), new Vector2(520, 46));
            allBar.Set((float)Challenges.ClaimedCount / Challenges.Count, Challenges.ClaimedCount + "/" + Challenges.Count);
            allBar.Label.color = Skin.Ink;
            allBar.Label.fontSharedMaterial = Fonts.Plain;
            if (Challenges.BonusReady)
            {
                var claim = UI.Chunky(bonus, new Vector2(300, 90), Skin.Green, "CLAIM", 42, () =>
                {
                    if (Challenges.ClaimBonus())
                        ZWordApp.I.ShowReward("SPECIAL REWARD!", GameConfig.ChallengeAllCoins, GameConfig.ChallengeAllGems, () => MetaScreens.OpenChallenges());
                });
                ((RectTransform)claim.transform).Place(new Vector2(0, 0), new Vector2(290 + 160, 60), new Vector2(300, 90));
            }
            else if (Save.Data.challengeBonusClaimed)
            {
                var done = UI.Label(bonus, "Claimed! New challenges at midnight.", 28, Skin.InkSoft, TextAnchor.MiddleLeft, false);
                done.rectTransform.Place(new Vector2(0, 0), new Vector2(290 + 270, 50), new Vector2(540, 40));
            }
        }

        // ---------------- Quests ----------------

        public static void OpenQuests()
        {
            var root = Widgets.FullPanel("QUESTS");

            var viewport = UI.Rect("Viewport", root);
            viewport.anchorMin = Vector2.zero;
            viewport.anchorMax = Vector2.one;
            viewport.offsetMin = new Vector2(0, 30);
            viewport.offsetMax = new Vector2(0, -190);
            viewport.gameObject.AddComponent<RectMask2D>();
            viewport.gameObject.AddComponent<Image>().color = new Color(0, 0, 0, 0);
            var content = UI.Rect("Content", viewport);
            content.anchorMin = new Vector2(0, 1);
            content.anchorMax = new Vector2(1, 1);
            content.pivot = new Vector2(0.5f, 1);
            int count = Quests.All.Length;
            content.sizeDelta = new Vector2(0, 40 + count * 214);
            var scroll = viewport.gameObject.AddComponent<ScrollRect>();
            scroll.viewport = viewport;
            scroll.content = content;
            scroll.horizontal = false;

            var questIcon = Theme.Current.quest;
            for (int q = 0; q < count; q++)
            {
                int qi = q;
                var def = Quests.All[q];
                bool done = Quests.Done(q), ready = Quests.Ready(q);
                int target = Quests.Target(q), value = Mathf.Min(def.Value(), target);

                var card = Widgets.Card(content, new Vector2(900, 190), done ? Palette.Hex("F6EEE1") : Skin.Cream);
                card.Place(new Vector2(0.5f, 1), new Vector2(0, -115 - q * 214), new Vector2(900, 190));
                Tween.PopIn(card, 0.25f, q * 0.05f);

                if (questIcon != null)
                {
                    var ic = UI.Img(card, questIcon, Color.white, "Icon");
                    ic.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(80, 0), new Vector2(100, 100));
                    ic.preserveAspect = true;
                }
                // tier pips
                for (int t = 0; t < def.Tiers.Length; t++)
                {
                    var pip = UI.Img(card, Sprites.Star, t < Quests.Tier(q) ? Skin.Gold : Palette.Hex("E8DCC6"), "Pip");
                    pip.rectTransform.Place(new Vector2(0, 0), new Vector2(40 + t * 26, 26), new Vector2(26, 26));
                }

                var title = UI.Label(card, done ? "All tiers complete!" : string.Format(def.Format, target.ToString("N0")), 36, Skin.Ink, TextAnchor.MiddleLeft, false);
                title.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(160 + 230, 34), new Vector2(460, 50));
                var bar = Widgets.Progress(card, new Vector2(440, 40), Skin.Blue, Skin.CreamShade, true);
                bar.Root.Place(new Vector2(0, 0.5f), new Vector2(160 + 220, -30), new Vector2(440, 40));
                bar.Set(done ? 1f : (float)value / target, done ? "DONE" : value.ToString("N0") + "/" + target.ToString("N0"));
                bar.Label.color = Skin.Ink;
                bar.Label.fontSharedMaterial = Fonts.Plain;

                if (!done)
                {
                    int coins = Quests.RewardCoins(q), gems = Quests.RewardGems(q);
                    var btn = Widgets.PriceButton(card, new Vector2(190, 96), Currency.Coins, coins + (gems > 0 ? "+" + gems + "g" : ""), () =>
                    {
                        if (!Quests.Ready(qi))
                        {
                            AudioManager.Error();
                            ZWordApp.Toast(root, "NOT YET - KEEP GOING!", new Vector2(0, -200), Palette.Yellow);
                            return;
                        }
                        var (c, g) = Quests.Claim(qi);
                        ZWordApp.I.ShowReward("QUEST COMPLETE!", c, g, () => MetaScreens.OpenQuests());
                    }, ready ? Skin.Green : Palette.Hex("F2B53A"));
                    ((RectTransform)btn.transform).Place(new Vector2(1, 0.5f), new Vector2(-120, 0), new Vector2(190, 96));
                    if (ready) btn.gameObject.AddComponent<Pulse>().Amount = 0.05f;
                }
            }
        }
    }

    /// <summary>Calls OnTick once a second (countdowns).</summary>
    public class Ticker : MonoBehaviour
    {
        public System.Action OnTick;
        float t;
        void Update()
        {
            t += Time.unscaledDeltaTime;
            if (t < 1f) return;
            t = 0;
            OnTick?.Invoke();
        }
    }
}
