using System.Globalization;
using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>Level Complete / Level Failed screens (mockup screens 7 and 8).</summary>
    public static class ResultScreen
    {
        static string N(int v) => v.ToString("N0", CultureInfo.InvariantCulture);

        public static void Build(RectTransform root, ResultData d)
        {
            var cat = WordData.Categories[d.Category];
            if (d.Daily)
            {
                Widgets.Header(root, "DAILY", System.DateTime.Now.ToString("MMM d").ToUpperInvariant(), () => ZWordApp.I.ShowHome(), gear: false);
                ZWordApp.I.OnBack = () => ZWordApp.I.ShowHome();
            }
            else
            {
                Widgets.Header(root, cat.Name, "LV " + (d.Level + 1), () => ZWordApp.I.ShowMap(d.Category), gear: false);
                ZWordApp.I.OnBack = () => ZWordApp.I.ShowMap(d.Category);
            }
            if (d.Won) BuildComplete(root, d);
            else BuildFailed(root, d);
        }

        // ---------------- Level Complete ----------------

        static void BuildComplete(RectTransform root, ResultData d)
        {
            var confetti = Ambience.Add(root, AmbienceKind.Confetti, Color.white, 70, 40f);
            Tween.Value(2.2f, _ => { }, null, 0, () => { if (confetti) confetti.Rate = 4f; });

            var card = Widgets.Card(root, new Vector2(820, 900));
            card.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 90), new Vector2(820, 900));
            Tween.PopIn(card, 0.4f);

            // rays + 3 big stars above the card
            var rays = UI.Img(card, Sprites.Rays, new Color(1f, 0.92f, 0.5f, 0.55f), "Rays");
            rays.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, 40), new Vector2(760, 760));
            rays.transform.SetAsFirstSibling();
            rays.gameObject.AddComponent<Spinner>();
            BigStars(card, d.Won ? d.Rating : 0f, false);

            var ribbon = Widgets.Ribbon(card, d.Daily ? "PUZZLE SOLVED!" : "LEVEL COMPLETE!", 760);
            ribbon.Place(new Vector2(0.5f, 1), new Vector2(0, -150), new Vector2(760, 120));
            ribbon.localRotation = Quaternion.Euler(0, 0, 0);
            Tween.PopIn(ribbon, 0.4f, 0.25f);

            // time
            var timeRow = UI.Rect("Time", card).Place(new Vector2(0.5f, 1), new Vector2(d.Daily && d.Streak > 0 ? -190 : 0, -275), new Vector2(380, 80));
            var clockSprite = Theme.Current.iconClock != null ? Theme.Current.iconClock : Sprites.Clock;
            var clock = UI.Img(timeRow, clockSprite, Theme.Current.iconClock != null ? Color.white : Skin.Ink, "Clock");
            clock.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(-92, 0), new Vector2(66, 66));
            clock.preserveAspect = true;
            int secs = Mathf.RoundToInt(d.TimeTaken);
            var tt = UI.Label(timeRow, (secs / 60) + ":" + (secs % 60).ToString("00"), 66, Skin.Ink, TextAnchor.MiddleLeft, false);
            tt.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(70, 0), new Vector2(240, 80));

            // score card
            ScoreBox(card, "TOTAL SCORE", d.Total, d.BestScore, d.NewBest, -440);

            // reward row
            var rewards = UI.Rect("Rewards", card).Place(new Vector2(0.5f, 1), new Vector2(0, -628), new Vector2(560, 100));
            UI.Img(rewards, Sprites.Rounded, Skin.CreamShade, "Bg", 1.4f).rectTransform.Stretch();
            bool gems = d.GemsEarned > 0;
            if (d.Daily && d.CoinsEarned == 0)
            {
                var again = UI.Label(rewards, "Already solved today - come back tomorrow!", 30, Skin.InkSoft, TextAnchor.MiddleCenter, false);
                again.rectTransform.Stretch(10, 0, 10, 0);
            }
            else
            {
                RewardItem(rewards, Currency.Coins, d.CoinsEarned, new Vector2(gems ? -120 : 0, 0), 0.9f);
                if (gems) RewardItem(rewards, Currency.Gems, d.GemsEarned, new Vector2(120, 0), 1.05f);
            }
            if (d.Daily) StreakTag(card, d.Streak, -275);

            // NEXT LEVEL (overlapping the card bottom)
            bool hasNext = !d.Daily && d.Level + 1 < cat(d).LevelCount;
            var next = Widgets.IconTextButton(card, new Vector2(620, 140), Skin.Green, d.Daily ? "CONTINUE" : hasNext ? "NEXT LEVEL" : "CATEGORY MAP",
                Theme.Current.iconPlay != null ? Theme.Current.iconPlay : Sprites.Play, 58, () =>
                {
                    if (d.Daily) ZWordApp.I.ShowHome();
                    else if (hasNext) ZWordApp.I.StartLevel(d.Category, d.Level + 1);
                    else ZWordApp.I.ShowMap(d.Category);
                });
            ((RectTransform)next.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 40), new Vector2(620, 140));
            Tween.PopIn(next.transform, 0.35f, 1.1f);
            next.gameObject.AddComponent<Pulse>().Amount = 0.025f;

            BottomRow(root, d, false);
        }

        static Category cat(ResultData d) => WordData.Categories[d.Category];

        static void Replay(ResultData d)
        {
            if (d.Daily) ZWordApp.I.StartDailyPuzzle();
            else ZWordApp.I.StartLevel(d.Category, d.Level);
        }

        /// <summary>Orange "N-DAY STREAK" tag under the Daily Puzzle rewards.</summary>
        static void StreakTag(RectTransform card, int streak, float y)
        {
            if (streak <= 0) return;
            var tag = UI.Rect("Streak", card).Place(new Vector2(0.5f, 1), new Vector2(170, y), new Vector2(360, 64));
            UI.Img(tag, Sprites.Rounded, Palette.Hex("F59B23"), "Bg", 2f).rectTransform.Stretch();
            var t = UI.Label(tag, streak == 1 ? "STREAK STARTED!" : streak + "-DAY STREAK!", 32, Color.white, TextAnchor.MiddleCenter);
            t.rectTransform.Stretch();
            UI.Outlined(t);
            Tween.PopIn(tag, 0.35f, 1.3f);
            tag.gameObject.AddComponent<Pulse>().Amount = 0.04f;
        }

        // ---------------- Level Failed ----------------

        static void BuildFailed(RectTransform root, ResultData d)
        {
            var card = Widgets.Card(root, new Vector2(820, 760));
            card.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 140), new Vector2(820, 760));
            Tween.PopIn(card, 0.4f);

            BigStars(card, 0f, true);

            var sad = Theme.Current.sadFace;
            if (sad != null)
            {
                var face = UI.Img(card, sad, Color.white, "Sad");
                face.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -60), new Vector2(150, 150));
                Tween.PopIn(face.transform, 0.4f, 0.5f);
                face.gameObject.AddComponent<Bobber>().Amplitude = 5;
            }

            var ribbon = Widgets.Ribbon(card, "LEVEL FAILED", 720);
            ribbon.Place(new Vector2(0.5f, 1), new Vector2(0, -200), new Vector2(720, 120));
            Tween.PopIn(ribbon, 0.4f, 0.25f);

            ScoreBox(card, "SCORE", d.WordScore + d.BonusScore, d.BestScore, false, -440);

            var retry = Widgets.IconTextButton(card, new Vector2(620, 140), Skin.Green, "TRY AGAIN",
                Theme.Current.iconPlay != null ? Theme.Current.iconPlay : Sprites.Play, 58, () => Replay(d));
            ((RectTransform)retry.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 40), new Vector2(620, 140));
            Tween.PopIn(retry.transform, 0.35f, 0.7f);
            retry.gameObject.AddComponent<Pulse>().Amount = 0.025f;

            BottomRow(root, d, true);
        }

        // ---------------- shared pieces ----------------

        /// <summary>Three big stars; the middle one is larger. Fill animates to the rating (partial stars allowed).</summary>
        static void BigStars(RectTransform card, float rating, bool grey)
        {
            var sprite = Theme.Current.iconStar != null ? Theme.Current.iconStar : Sprites.Star;
            var xs = new[] { -230f, 0f, 230f };
            var ys = new[] { 10f, 60f, 10f };
            var size = new[] { 200f, 250f, 200f };
            for (int i = 0; i < 3; i++)
            {
                var holder = UI.Rect("BigStar" + i, card).Place(new Vector2(0.5f, 1), new Vector2(xs[i], ys[i]), Vector2.one * size[i]);
                holder.localRotation = Quaternion.Euler(0, 0, i == 0 ? 12 : i == 2 ? -12 : 0);
                var empty = UI.Img(holder, sprite, new Color(0.62f, 0.6f, 0.66f, 1f), "Empty");
                empty.rectTransform.Stretch();
                if (grey) { Tween.PopIn(holder, 0.35f, 0.2f + i * 0.15f); continue; }

                var fill = UI.Img(holder, sprite, Color.white, "Fill");
                fill.rectTransform.Stretch();
                fill.type = Image.Type.Filled;
                fill.fillMethod = Image.FillMethod.Horizontal;
                fill.fillOrigin = 0;
                fill.fillAmount = 0;
                float target = Mathf.Clamp01(rating - i);
                holder.localScale = Vector3.zero;
                int idx = i;
                Tween.Value(0.45f, k =>
                {
                    if (!holder) return;
                    holder.localScale = Vector3.one * Tween.OutBack(k);
                    fill.fillAmount = target * Mathf.Clamp01(k * 1.4f);
                }, null, 0.45f + i * 0.28f, () => { if (target > 0) { AudioManager.Star(idx); Haptics.Light(); } });
            }
        }

        static void ScoreBox(RectTransform card, string label, int score, int best, bool newBest, float y)
        {
            var box = UI.Rect("Score", card).Place(new Vector2(0.5f, 1), new Vector2(0, y), new Vector2(640, 220));
            UI.Img(box, Sprites.Rounded, Skin.CreamShade, "Rim", 1.1f).rectTransform.Stretch();
            UI.Img(box, Sprites.Rounded, Palette.Hex("FFF8EA"), "Face", 1.1f).rectTransform.Stretch(6, 10, 6, 4);
            var l = UI.Label(box, label, 30, Skin.InkSoft, TextAnchor.MiddleCenter, false);
            l.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -36), new Vector2(600, 40));
            var num = UI.Label(box, "0", 84, Skin.Ink, TextAnchor.MiddleCenter, false);
            num.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 8), new Vector2(600, 96));
            Tween.Value(1.1f, k => { if (num) num.text = N(Mathf.RoundToInt(score * k)); }, Tween.OutCubic, 0.6f);

            var bestRow = UI.Rect("Best", box).Place(new Vector2(0.5f, 0), new Vector2(0, 34), new Vector2(420, 46));
            var crownSprite = Theme.Current.crown;
            if (crownSprite != null)
            {
                var crown = UI.Img(bestRow, crownSprite, Color.white, "Crown");
                crown.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(40, 2), new Vector2(46, 40));
                crown.preserveAspect = true;
            }
            var bl = UI.Label(bestRow, "BEST SCORE  " + N(Mathf.Max(best, newBest ? score : best)), 30, Palette.Hex("B07A1E"), TextAnchor.MiddleLeft, false);
            bl.rectTransform.Stretch(76, 0, 0, 0);

            if (newBest)
            {
                var badge = UI.Rect("NewBest", box).Place(new Vector2(1, 1), new Vector2(-40, -10), new Vector2(170, 60));
                badge.localRotation = Quaternion.Euler(0, 0, -12);
                UI.Img(badge, Sprites.Rounded, Skin.Red, "Bg", 2f).rectTransform.Stretch();
                var t = UI.Label(badge, "NEW BEST!", 28, Color.white, TextAnchor.MiddleCenter);
                t.rectTransform.Stretch();
                Tween.PopIn(badge, 0.4f, 1.6f);
                badge.gameObject.AddComponent<Pulse>().Amount = 0.06f;
            }
        }

        static void RewardItem(RectTransform parent, Currency kind, int amount, Vector2 pos, float delay)
        {
            var r = UI.Rect("Reward_" + kind, parent).Place(new Vector2(0.5f, 0.5f), pos, new Vector2(220, 90));
            var icon = Widgets.CurrencyIcon(r, kind, 76);
            icon.Place(new Vector2(0, 0.5f), new Vector2(44, 0), new Vector2(76, 76));
            var t = UI.Label(r, "+" + amount, 48, Skin.Ink, TextAnchor.MiddleLeft, false);
            t.rectTransform.Stretch(92, 0, 0, 0);
            Tween.PopIn(r, 0.35f, delay);
            Tween.Value(0.01f, _ => { }, null, delay, () => AudioManager.Bonus());
        }

        static void BottomRow(RectTransform root, ResultData d, bool failed)
        {
            var t = Theme.Current;
            var row = UI.Rect("BottomRow", root).Place(new Vector2(0.5f, 0), new Vector2(0, 200), new Vector2(800, 150));

            var home = Widgets.DockButton(row, t.home != null ? t.home : Sprites.HomeGlyph, Color.white, null, () => ZWordApp.I.ShowHome(), 140);
            ((RectTransform)home.transform).Place(new Vector2(0.5f, 0.5f), new Vector2(-260, 0), new Vector2(140, 140));
            var replay = Widgets.DockButton(row, t.replay != null ? t.replay : Sprites.ReplayGlyph, Color.white, null,
                () => Replay(d), 140);
            ((RectTransform)replay.transform).Place(new Vector2(0.5f, 0.5f), new Vector2(-80, 0), new Vector2(140, 140));

            if (!failed)
            {
                var share = Widgets.DockButton(row, t.share != null ? t.share : Sprites.ShareGlyph, Color.white, null, () => ShareScore(d), 140);
                ((RectTransform)share.transform).Place(new Vector2(0.5f, 0.5f), new Vector2(100, 0), new Vector2(140, 140));
                return;
            }

            // FREE HINT card: Word Z has no ads, so it's simply a free gift after a loss
            bool claimed = false;
            Button free = null;
            free = UI.Chunky(row, new Vector2(240, 170), Skin.Purple, null, 0, () =>
            {
                if (claimed) return;
                claimed = true;
                Save.SetBooster(Booster.Letter, Save.GetBooster(Booster.Letter) + 1);
                AudioManager.Bonus();
                ZWordApp.Toast(root, "+1 REVEAL LETTER!", new Vector2(0, -420), Palette.Yellow);
                free.GetComponentInChildren<TMPro.TMP_Text>().text = "CLAIMED";
            }, null, 1.4f, 14);
            ((RectTransform)free.transform).Place(new Vector2(0.5f, 0.5f), new Vector2(170, 10), new Vector2(240, 170));
            var face = free.transform.Find("Body/Face");
            var bulb = UI.Img(face, t.iconBulb != null ? t.iconBulb : Sprites.BulbGlyph, Color.white, "Bulb");
            bulb.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -60), new Vector2(86, 86));
            bulb.preserveAspect = true;
            var lbl = UI.Label(face, "FREE HINT", 34, Color.white, TextAnchor.MiddleCenter);
            lbl.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 30), new Vector2(230, 44));
            UI.Outlined(lbl);
            free.gameObject.AddComponent<Pulse>().Amount = 0.04f;
        }

        static void ShareScore(ResultData d)
        {
            string text = $"I just scored {N(d.Total)} on {cat(d).Name} level {d.Level + 1} in {GameConfig.GameName}! Can you beat it?";
            Share.Text(text);
        }
    }

    /// <summary>Slow constant rotation (sun rays).</summary>
    public class Spinner : MonoBehaviour
    {
        public float Speed = 18f;
        void Update() => transform.Rotate(0, 0, -Speed * Time.unscaledDeltaTime);
    }
}
