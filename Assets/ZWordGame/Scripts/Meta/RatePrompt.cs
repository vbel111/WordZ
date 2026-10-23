using UnityEngine;

namespace ZWord
{
    /// <summary>
    /// "Rate Word Z" prompt, shown once right after the first-launch tutorial.
    ///
    /// iOS: Apple only allows its own review sheet (guideline 5.6.1), so we call it directly - no custom popup.
    /// Android / Editor: a simple popup with RATE NOW / LATER that opens the Play Store page.
    /// Never asks again once shown.
    /// </summary>
    public static class RatePrompt
    {
        public static string StoreUrl =>
#if UNITY_ANDROID
            "market://details?id=" + GameConfig.BundleId;
#else
            "https://play.google.com/store/apps/details?id=" + GameConfig.BundleId;
#endif

        /// <summary>Called after the tutorial; shows the prompt the first time only.</summary>
        public static void ShowAfterTutorial()
        {
            if (Save.Data.ratePromptShown) return;
            Save.Data.ratePromptShown = true;
            Save.Write();
            // let the home screen fade in first
            Tween.Value(0.01f, _ => { }, null, 0.6f, Show);
        }

        public static void Show()
        {
#if UNITY_IOS && !UNITY_EDITOR
            if (UnityEngine.iOS.Device.RequestStoreReview()) return;
#endif
            ShowPopup();
        }

        static void ShowPopup()
        {
            var body = Widgets.WoodPopup("ENJOYING WORD Z?", new Vector2(820, 760), OpenDailyIfDue);

            // five stars
            for (int i = 0; i < 5; i++)
            {
                var s = UI.Img(body, Sprites.Star, Skin.Wood, "Star");
                s.rectTransform.Place(new Vector2(0.5f, 1), new Vector2((i - 2) * 125, -110), new Vector2(115, 115));
                Tween.PopIn(s.transform, 0.35f, 0.1f + i * 0.08f);
            }

            var msg = UI.Label(body, "Thanks for playing! A quick rating helps other word lovers find the game.", 40, Skin.Ink, TextAnchor.MiddleCenter, false);
            msg.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -290), new Vector2(680, 170));
            msg.textWrappingMode = TMPro.TextWrappingModes.Normal;

            var rate = UI.Chunky(body, new Vector2(460, 120), Skin.Green, "RATE NOW", 50, () =>
            {
                Save.Data.rated = true;
                Save.Write();
                Application.OpenURL(StoreUrl);
                ZWordApp.I.ClosePopups();
            });
            ((RectTransform)rate.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 170), new Vector2(460, 120));

            var later = UI.Chunky(body, new Vector2(300, 90), Skin.Wood, "LATER", 38, () => ZWordApp.I.ClosePopups());
            ((RectTransform)later.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 50), new Vector2(300, 90));
        }

        /// <summary>The daily reward would normally auto-open on Home; the prompt took its slot, so open it after.</summary>
        static void OpenDailyIfDue()
        {
            if (DailyRewards.CanClaim && !ZWordApp.I.PopupOpen) ZWordApp.I.OpenDailyReward();
        }
    }
}
