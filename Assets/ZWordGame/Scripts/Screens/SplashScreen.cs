using System;
using UnityEngine;

namespace ZWord
{
    /// <summary>Logo over the sky with clouds and a loading bar while the dictionary loads.</summary>
    public class SplashScreen : MonoBehaviour
    {
        ProgressBar bar;
        Action done;
        float t;
        bool finished;
        const float MinTime = 1.6f, MaxTime = 6f;

        public static void Build(RectTransform root, Action onDone)
        {
            var s = root.gameObject.AddComponent<SplashScreen>();
            s.done = onDone;

            // drifting clouds and sparkles over the shared sky background
            Ambience.Add(root, AmbienceKind.Clouds, new Color(1, 1, 1, 0.85f), 5, 0.25f);
            Ambience.Add(root, AmbienceKind.Twinkle, Color.white, 14, 3f);

            var logo = Widgets.Logo(root, 1.05f);
            logo.anchorMin = logo.anchorMax = new Vector2(0.5f, 0.5f);
            logo.sizeDelta = new Vector2(900, 645);
            logo.anchoredPosition = new Vector2(0, 230);
            Tween.PopIn(logo, 0.5f, 0.1f);
            logo.gameObject.AddComponent<Bobber>().Amplitude = 6;

            s.bar = Widgets.Progress(root, new Vector2(560, 50), Skin.Gold, new Color(0.36f, 0.2f, 0.06f, 0.5f));
            s.bar.Root.Place(new Vector2(0.5f, 0), new Vector2(0, 560), new Vector2(560, 50));
            s.bar.Set(0.02f);
            var lbl = UI.Label(root, "Loading...", 40, Color.white, TextAnchor.MiddleCenter);
            lbl.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 490), new Vector2(500, 60));
            UI.Outlined(lbl);
        }

        void Update()
        {
            if (finished) return;
            t += Time.unscaledDeltaTime;
            float target = WordDictionary.Ready ? 1f : 0.85f;
            bar.Set(Mathf.Min(target, t / MinTime));
            if (t >= MinTime && (WordDictionary.Ready || t > MaxTime))
            {
                finished = true;
                bar.Set(1f);
                done?.Invoke();
            }
        }
    }
}
