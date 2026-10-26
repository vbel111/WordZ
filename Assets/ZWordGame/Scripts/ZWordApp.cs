using System;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.UI;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>
    /// Entry point. Builds the canvas, event system and screens entirely from code.
    /// It boots automatically when you press Play in any scene (see AutoBoot), or you can
    /// add this component to a GameObject yourself.
    /// </summary>
    public class ZWordApp : MonoBehaviour
    {
        /// <summary>Set to false if you'd rather add ZWordApp to a scene manually.</summary>
        public static bool AutoBoot = true;

        public static ZWordApp I { get; private set; }

        CanvasScaler scaler;
        RectTransform frame, screenRoot, popupRoot;
        Action popupOnClose;
        bool popupVisible;

        /// <summary>True while a popup is on screen (games pause their timer meanwhile).</summary>
        public bool PopupOpen => popupVisible;

        /// <summary>What the Android back button / Escape does on the current screen. Reset on every screen change.</summary>
        public Action OnBack;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        static void Boot()
        {
            if (!AutoBoot) return;
            if (FindAnyObjectByType<ZWordApp>() != null) return;
            new GameObject("ZWordApp").AddComponent<ZWordApp>();
        }

        void Awake()
        {
            if (I != null && I != this) { Destroy(gameObject); return; }
            I = this;
            DontDestroyOnLoad(gameObject);
            Application.targetFrameRate = 60;
            Screen.orientation = ScreenOrientation.Portrait;
            Screen.sleepTimeout = SleepTimeout.SystemSetting;
            Tween.Runner = this;
            Save.Data.sessions++;
            Save.Write();
            AudioManager.Init(gameObject);
            WordDictionary.Preload();
            Store.Init(this);
            EnsureEventSystem();
            BuildCanvas();
            ShowSplash();
#if UNITY_EDITOR
            if (PlayerPrefs.GetInt(Testing.SmokeTest.PrefKey, 0) == 1)
            {
                PlayerPrefs.DeleteKey(Testing.SmokeTest.PrefKey);
                gameObject.AddComponent<Testing.SmokeTest>();
            }
#endif
        }

        static void EnsureEventSystem()
        {
            if (FindAnyObjectByType<EventSystem>() != null) return;
            var es = new GameObject("EventSystem", typeof(EventSystem));
            var module = es.AddComponent<InputSystemUIInputModule>();
            module.AssignDefaultActions();
            DontDestroyOnLoad(es);
        }

        void BuildCanvas()
        {
            var canvasGo = new GameObject("ZWordCanvas", typeof(RectTransform));
            canvasGo.layer = 5;
            canvasGo.transform.SetParent(transform, false);
            var canvas = canvasGo.AddComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.sortingOrder = 10;
            scaler = canvasGo.AddComponent<CanvasScaler>();
            scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(1080, 1920);
            scaler.referencePixelsPerUnit = 100;
            canvasGo.AddComponent<GraphicRaycaster>();
            UpdateScaler();

            var root = (RectTransform)canvasGo.transform;
            // the sky fills the whole screen (tablets / wide phones see it beside the 1080-wide frame)
            Widgets.AppBackground(root);

            // Portrait "phone" frame: 1080 wide, full height.
            frame = UI.Rect("Frame", root);
            frame.anchorMin = new Vector2(0.5f, 0);
            frame.anchorMax = new Vector2(0.5f, 1);
            frame.sizeDelta = new Vector2(1080, 0);
            frame.anchoredPosition = Vector2.zero;
            frame.gameObject.AddComponent<RectMask2D>();


            screenRoot = UI.Rect("Screens", frame).Stretch();
            popupRoot = UI.Rect("Popups", frame).Stretch();
            // keep buttons and text clear of notches, camera holes and the home indicator
            screenRoot.gameObject.AddComponent<SafeAreaFitter>();
            popupRoot.gameObject.AddComponent<SafeAreaFitter>();
        }

        /// <summary>Leaf clusters in the frame corners (mockup), behind every screen.</summary>
        static void BuildCornerLeaves(RectTransform frame)
        {
            var art = Theme.Current.leafCorner;
            if (art == null) { Widgets.LeafCorners(frame, 0.9f); return; }
            void Corner(Vector2 anchor, Vector2 scale)
            {
                var img = UI.Img(frame, art, Color.white, "LeafCorner");
                var rt = img.rectTransform;
                rt.anchorMin = rt.anchorMax = anchor;
                rt.pivot = new Vector2(0, 0);
                rt.sizeDelta = new Vector2(330, 330);
                rt.anchoredPosition = Vector2.zero;
                rt.localScale = new Vector3(scale.x, scale.y, 1);
            }
            Corner(new Vector2(0, 0), new Vector2(1, 1));
            Corner(new Vector2(1, 0), new Vector2(-1, 1));
            Corner(new Vector2(0, 1), new Vector2(1, -1));
            Corner(new Vector2(1, 1), new Vector2(-1, -1));
        }

        void UpdateScaler()
        {
            if (scaler == null) return;
            float aspect = (float)Screen.width / Mathf.Max(1, Screen.height);
            // Wider than 9:16 -> fit height, otherwise fit width.
            scaler.matchWidthOrHeight = aspect > 1080f / 1920f ? 1f : 0f;
        }

        void Update()
        {
            UpdateScaler();
            var kb = Keyboard.current;
            if (kb != null && kb.escapeKey.wasPressedThisFrame) HandleBack();
        }

        /// <summary>Android back / Escape: close popup first, then the screen's own back action, else ask to quit.</summary>
        public void HandleBack()
        {
            if (popupVisible) { ClosePopups(); return; }
            if (OnBack != null) { OnBack(); return; }
            ConfirmQuit();
        }

        void ConfirmQuit()
        {
            var overlay = NewPopup("Quit");
            var panel = Panel(overlay, new Vector2(720, 460), "EXIT?");
            var msg = UI.Label(panel, "Leave the game?", 48, Palette.Hex("3E2A4F"), TextAnchor.MiddleCenter, false);
            msg.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -150), new Vector2(640, 70));
            var stay = UI.Chunky(panel, new Vector2(290, 120), Palette.Green, "STAY", 46, ClosePopups);
            ((RectTransform)stay.transform).Place(new Vector2(0.5f, 0), new Vector2(-160, 110), new Vector2(290, 120));
            var quit = UI.Chunky(panel, new Vector2(290, 120), Palette.Red, "EXIT", 46, () =>
            {
                Save.Write();
                Application.Quit();
            });
            ((RectTransform)quit.transform).Place(new Vector2(0.5f, 0), new Vector2(160, 110), new Vector2(290, 120));
        }

        void OnApplicationPause(bool paused)
        {
            if (paused) { Save.Write(); Reminders.Reschedule(); }
            else Store.OnResume();   // pick up subscription renewals / expirations / refunds
        }
        void OnApplicationQuit() { Save.Write(); Reminders.Reschedule(); }

        // ---------------- Navigation ----------------

        void ClearScreens()
        {
            for (int i = screenRoot.childCount - 1; i >= 0; i--) Destroy(screenRoot.GetChild(i).gameObject);
            ClosePopups();
        }

        public void ClosePopups()
        {
            for (int i = popupRoot.childCount - 1; i >= 0; i--) Destroy(popupRoot.GetChild(i).gameObject);
            popupVisible = false;
            var cb = popupOnClose;
            popupOnClose = null;
            cb?.Invoke();
        }

        /// <summary>The screen currently shown (for toasts from static screen builders).</summary>
        public RectTransform CurrentScreen { get; private set; }

        RectTransform NewScreen(string name)
        {
            ClearScreens();
            OnBack = null;
            var rt = UI.Rect(name, screenRoot).Stretch();
            CurrentScreen = rt;
            var cg = rt.gameObject.AddComponent<CanvasGroup>();
            Tween.Fade(cg, 0f, 1f, 0.25f);
            return rt;
        }

        public void ShowSplash()
        {
            SplashScreen.Build(NewScreen("Splash"), () => { if (Save.Data.tutorialDone) ShowHome(); else StartTutorial(); });
            AudioManager.PlayMusic(MusicContext.Home);
        }

        public void ShowHome()
        {
            HomeScreen.Build(NewScreen("Home"));
            AudioManager.PlayMusic(MusicContext.Home);
            if (!dailyShownThisSession && DailyRewards.CanClaim)
            {
                dailyShownThisSession = true;
                Tween.Value(0.01f, _ => { }, null, 0.7f, () => { if (!PopupOpen) OpenDailyReward(); });
            }
        }

        public void ShowCategories()
        {
            CategoriesScreen.Build(NewScreen("Categories"));
            AudioManager.PlayMusic(MusicContext.Home);
        }

        public void ShowMap(int cat)
        {
            Save.Data.lastCategory = cat;
            MapScreen.Build(NewScreen("Map"), cat);
            AudioManager.PlayMusic(MusicContext.Home);
        }

        // Screens arriving in the next M3 batches.
        public void OpenDailyReward() => MetaScreens.OpenDailyReward();
        public void ShowChallenges() => MetaScreens.OpenChallenges();
        public void ShowShop() => ShopScreen.Open(0);
        public void ShowShop(int tab) => ShopScreen.Open(tab);
        public void ShowQuests() => MetaScreens.OpenQuests();

        /// <summary>Red badge count for the home dock buttons (Rewards, Challenges, Words, Shop, Quests).</summary>
        public int DockBadge(int index)
        {
            switch (index)
            {
                case 0: return DailyRewards.CanClaim ? 1 : 0;
                case 1: return Challenges.Claimable;
                case 2: return WordBook.Claimable;
                case 4: return Quests.Claimable;
                default: return 0;
            }
        }

        bool dailyShownThisSession;

        void ComingSoon(string what) => Toast(CurrentScreen, what + " coming next update!", new Vector2(0, -300), Palette.Yellow);

        /// <summary>Reward popup: open chest, coin and gem amounts, COLLECT.</summary>
        public void ShowReward(string title, int coins, int gems, Action after = null)
        {
            var body = Widgets.WoodPopup(title, new Vector2(760, 720), after);
            var chest = Theme.Current.chestOpen;
            if (chest != null)
            {
                var img = UI.Img(body, chest, Color.white, "Chest");
                img.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -170), new Vector2(260, 240));
                img.preserveAspect = true;
                Tween.PopIn(img.transform, 0.45f, 0.1f);
            }
            float x = coins > 0 && gems > 0 ? -130 : 0;
            if (coins > 0) RewardChip(body, Currency.Coins, coins, new Vector2(x, -360));
            if (gems > 0) RewardChip(body, Currency.Gems, gems, new Vector2(coins > 0 ? 130 : 0, -360));
            var collect = UI.Chunky(body, new Vector2(460, 120), Skin.Green, "COLLECT", 52, ClosePopups);
            ((RectTransform)collect.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 90), new Vector2(460, 120));
            AudioManager.Win();
        }

        static void RewardChip(RectTransform parent, Currency kind, int amount, Vector2 pos)
        {
            var r = UI.Rect("Reward", parent).Place(new Vector2(0.5f, 1), pos, new Vector2(230, 90));
            var icon = Widgets.CurrencyIcon(r, kind, 80);
            icon.Place(new Vector2(0, 0.5f), new Vector2(46, 0), new Vector2(80, 80));
            var t = UI.Label(r, "+" + amount, 50, Skin.Ink, TextAnchor.MiddleLeft, false);
            t.rectTransform.Stretch(96, 0, 0, 0);
            Tween.PopIn(r, 0.35f, 0.3f);
        }

        public void StartLevel(int cat, int lvl)
        {
            GameScreen.Build(NewScreen("Game"), cat, lvl);
            AudioManager.PlayMusic(MusicContext.Game, nextTrack: true);
        }

        /// <summary>First-launch "how to play" level (also reachable from Settings).</summary>
        public void StartTutorial()
        {
            Tutorial.Begin(NewScreen("Tutorial"));
            AudioManager.PlayMusic(MusicContext.Game, nextTrack: true);
        }

        /// <summary>Today's Daily Puzzle (same level for everyone; rewards once a day, replays allowed).</summary>
        public void StartDailyPuzzle()
        {
            var level = DailyPuzzle.Build();
            GameScreen.BuildCustom(NewScreen("DailyPuzzle"), level, false, true);
            AudioManager.PlayMusic(MusicContext.Game, nextTrack: true);
        }

        public void ShowResult(ResultData data) => ResultScreen.Build(NewScreen("Result"), data);

        /// <param name="onClose">Runs when the popup is closed by any route (button, back key, replaced).</param>
        public RectTransform NewPopup(string name, Action onClose = null)
        {
            ClosePopups();
            popupVisible = true;
            popupOnClose = onClose;
            var cg = UI.Overlay(popupRoot, 0.65f);
            cg.gameObject.name = name;
            Tween.Fade(cg, 0f, 1f, 0.2f);
            return (RectTransform)cg.transform;
        }

        // ---------------- Shared widgets ----------------

        /// <summary>Back button, title pill and settings gear across the top of a screen.</summary>
        public static void Header(RectTransform parent, string title, string tab, Action onBack) =>
            Widgets.Header(parent, title, tab, onBack);

        public void OpenSettings() => SettingsScreen.Open();

        /// <summary>White rounded popup panel with a title pill on top.</summary>
        public static RectTransform Panel(RectTransform parent, Vector2 size, string title)
        {
            var root = UI.Rect("Panel", parent).Place(new Vector2(0.5f, 0.5f), Vector2.zero, size);
            var sh = UI.Img(root, Sprites.Rounded, Palette.Hex("E2C89A"), "Shadow");
            sh.rectTransform.Stretch(0, -16, 0, 16);
            var face = UI.Img(root, Sprites.Rounded, Palette.Panel, "Face");
            face.rectTransform.Stretch();
            if (title != null)
            {
                var pill = UI.TitlePill(root, title);
                pill.anchorMin = pill.anchorMax = new Vector2(0.5f, 1);
                pill.anchoredPosition = new Vector2(0, 0);
            }
            Tween.PopIn(root, 0.3f);
            return root;
        }

        public static void Toast(RectTransform parent, string text, Vector2 pos, Color color)
        {
            var t = UI.Label(parent, text, 54, color);
            t.rectTransform.Place(new Vector2(0.5f, 0.5f), pos, new Vector2(800, 80));
            UI.Outlined(t);
            Tween.PopIn(t.transform, 0.25f);
            Tween.Value(0.9f, k =>
            {
                if (!t) return;
                t.rectTransform.anchoredPosition = pos + new Vector2(0, k * 90);
                t.color = new Color(color.r, color.g, color.b, 1f - Mathf.Clamp01((k - 0.6f) / 0.4f));
            }, null, 0.25f, () => { if (t) Destroy(t.gameObject); });
        }
    }

    public class ResultData
    {
        public int Category, Level;
        public bool Won;
        public float Rating;
        public int Stars;
        public float TimeTaken;
        public int WordScore, TimeBonus, BonusScore, BonusWords;
        public int Total => WordScore + TimeBonus + BonusScore;
        public string Reward;
        public int CoinsEarned, GemsEarned, BestScore;
        public bool NewBest;
        public bool Daily;      // Daily Puzzle result
        public int Streak;      // Daily Puzzle streak after this solve
        public int GoldGems;    // gems from the golden hex (already in the wallet)
        public int NewBookWords;            // words added to the Word Book this level
        public bool Boss, CrownEarned;      // boss board / first win on it
        public string BadgeEarned;          // event badge just earned (null if none)
    }
}
