using UnityEngine;
using UnityEngine.UI;

namespace ZWord
{
    /// <summary>Settings page (mockup screen 12): profile, sound/music/vibration switches, info links, reset.</summary>
    public static class SettingsScreen
    {
        public static void Open()
        {
            var root = Widgets.FullPanel("SETTINGS", () => Save.Write());
            var t = Theme.Current;

            // ---- profile card ----
            var profile = Widgets.Card(root, new Vector2(900, 190));
            profile.Place(new Vector2(0.5f, 1), new Vector2(0, -320), new Vector2(900, 190));
            var av = UI.Img(profile, t.iconAvatar != null ? t.iconAvatar : Sprites.AvatarGlyph, Color.white, "Avatar");
            av.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(100, 0), new Vector2(130, 130));
            var nameInput = Widgets.TextInput(profile, new Vector2(520, 70), Save.Data.playerName, "Your name", 14, v =>
            {
                v = string.IsNullOrWhiteSpace(v) ? "Player" : v.Trim();
                Save.Data.playerName = v;
                Save.Write();
            });
            ((RectTransform)nameInput.transform).Place(new Vector2(0, 0.5f), new Vector2(190 + 260, 26), new Vector2(520, 70));
            var id = UI.Label(profile, "Player ID: " + Save.Data.playerId, 28, Skin.InkSoft, TextAnchor.MiddleLeft, false);
            id.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(190 + 260, -34), new Vector2(520, 40));
            var edit = Widgets.RoundButton(profile, Sprites.Pencil, 76, Skin.Wood, () => nameInput.ActivateInputField(), 0.5f);
            ((RectTransform)edit.transform).Place(new Vector2(1, 0.5f), new Vector2(-70, 0), new Vector2(76, 76));

            // ---- switches ----
            var toggles = Widgets.Card(root, new Vector2(900, 534));
            toggles.Place(new Vector2(0.5f, 1), new Vector2(0, -707), new Vector2(900, 534));
            SwitchRow(toggles, Sprites.SpeakerGlyph, Skin.Blue, "Sound Effects", -62, Save.Data.sfxOn, v =>
            {
                Save.Data.sfxOn = v;
                AudioManager.ApplyVolumes();
            });
            Widgets.Divider(toggles, -112);
            SwitchRow(toggles, Sprites.NoteGlyph, Skin.Purple, "Music", -164, Save.Data.musicOn, v =>
            {
                Save.Data.musicOn = v;
                AudioManager.ApplyVolumes();
            });
            Widgets.Divider(toggles, -214);
            SwitchRow(toggles, Sprites.PhoneGlyph, Skin.Green, "Vibration", -266, Save.Data.haptics, v =>
            {
                Save.Data.haptics = v;
                if (v) Haptics.Medium();
            });
            Widgets.Divider(toggles, -316);
            SwitchRow(toggles, Sprites.Clock, Skin.Gold, "Relax Mode (no timer)", -368, Save.Data.relaxMode, v =>
            {
                Save.Data.relaxMode = v;
                Save.Write();
                if (v) ZWordApp.Toast(root, "NO TIMER - USE FEWER HINTS FOR 3 STARS", new Vector2(0, -260), Palette.Yellow);
            });
            Widgets.Divider(toggles, -418);
            // opt-in daily reminder (asks the system for permission when switched on)
            SwitchRow(toggles, Widgets.HomeIcon("icon_bell", Sprites.CalendarGlyph), Skin.Red, "Daily Reminder", -470, Save.Data.remindersOn, v =>
            {
                if (!v) { Reminders.Disable(); return; }
                Reminders.Enable(ok =>
                {
                    if (!ok) ZWordApp.Toast(root, "ALLOW NOTIFICATIONS IN YOUR PHONE SETTINGS", new Vector2(0, -260), Palette.Yellow);
                    else ZWordApp.Toast(root, "REMINDERS ON!", new Vector2(0, -260), Palette.Hex("7CF06B"));
                });
            });

            // ---- links ----
            float linksH = GameConfig.ProEnabled ? 532 : 430;
            var links = Widgets.Card(root, new Vector2(900, linksH));
            links.Place(new Vector2(0.5f, 1), new Vector2(0, -1012 - linksH / 2), new Vector2(900, linksH));
            LinkRow(links, Sprites.Play, Skin.Blue, "How to Play", null, -62, () =>
            {
                ZWordApp.I.ClosePopups();
                ZWordApp.I.StartTutorial();
            });
            Widgets.Divider(links, -112);
            LinkRow(links, null, Skin.Gold, "Help & Support", null, -164,
                () => Application.OpenURL("mailto:" + GameConfig.SupportEmail + "?subject=" + System.Uri.EscapeDataString(GameConfig.GameName + " support (ID " + Save.Data.playerId + ")")), "?");
            Widgets.Divider(links, -214);
            LinkRow(links, Sprites.LockGlyph, Palette.Hex("4F5D7E"), "Privacy Policy", null, -266, () => Application.OpenURL(GameConfig.PrivacyUrl));
            Widgets.Divider(links, -316);
            LinkRow(links, null, Skin.Green, "About", null, -368, ShowAbout, "i");
            if (GameConfig.ProEnabled)
            {
            Widgets.Divider(links, -418);
            // Word Z Pro: paywall when not subscribed, RevenueCat Customer Center (manage / cancel / refund) when Pro
            LinkRow(links, Sprites.Star, Skin.Gold, Store.IsPro ? "Manage Word Z Pro" : "Word Z Pro", Store.IsPro ? "ACTIVE" : null, -470, () =>
                Store.OpenPro(msg =>
                {
                    if (msg != null) ZWordApp.Toast(root, msg, new Vector2(0, -260), Palette.Hex("7CF06B"));
                }));
            }

            // ---- reset (becomes Sign Out once accounts arrive in M5) ----
            bool armed = false;
            Button reset = null;
            reset = UI.Chunky(root, new Vector2(620, 120), Skin.Red, "RESET PROGRESS", 46, () =>
            {
                if (!armed)
                {
                    armed = true;
                    reset.GetComponentInChildren<TMPro.TMP_Text>().text = "TAP AGAIN TO CONFIRM";
                    return;
                }
                Save.ResetAll();
                ZWordApp.I.ClosePopups();
                ZWordApp.I.ShowHome();
            });
            ((RectTransform)reset.transform).Place(new Vector2(0.5f, 0), new Vector2(0, 150), new Vector2(620, 120));

            var ver = UI.Label(root, GameConfig.GameName + "  v" + Application.version, 28, new Color(1, 1, 1, 0.75f), TextAnchor.MiddleCenter);
            ver.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 60), new Vector2(600, 40));
        }

        static void SwitchRow(RectTransform card, Sprite icon, Color color, string label, float y, bool on, System.Action<bool> changed)
        {
            var row = Widgets.ListRow(card, icon, color, label, y);
            var sw = Widgets.Switch(row, on, changed);
            sw.Place(new Vector2(1, 0.5f), new Vector2(-70, 0), new Vector2(108, 58));
        }

        static void LinkRow(RectTransform card, Sprite icon, Color color, string label, string value, float y, System.Action onClick, string glyphText = null)
        {
            var row = Widgets.ListRow(card, icon, color, label, y);
            if (glyphText != null)
            {
                var g = UI.Label(row.Find("IconTile"), glyphText, 44, Color.white, TextAnchor.MiddleCenter, false);
                g.rectTransform.Stretch(0, 4, 0, 0);
            }
            if (value != null)
            {
                var v = UI.Label(row, value, 32, Skin.InkSoft, TextAnchor.MiddleRight, false);
                v.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-150, 0), new Vector2(200, 50));
            }
            var chev = UI.Img(row, Sprites.ChevronRight, Skin.InkSoft, "Chevron");
            chev.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-30, 0), new Vector2(34, 34));
            var hit = row.gameObject.AddComponent<Image>();
            hit.color = new Color(0, 0, 0, 0);
            var b = row.gameObject.AddComponent<Button>();
            b.transition = Selectable.Transition.None;
            b.targetGraphic = hit;
            b.onClick.AddListener(() => { AudioManager.Click(); onClick?.Invoke(); });
        }

        static void ShowAbout()
        {
            var body = Widgets.WoodPopup("ABOUT", new Vector2(780, 820));
            var logo = Widgets.Logo(body, 0.42f);
            logo.Place(new Vector2(0.5f, 1), new Vector2(0, -150), new Vector2(380, 270));
            var text = UI.Label(body,
                GameConfig.GameName + "  v" + Application.version + "\n\n" +
                "Find the hidden words on the honeycomb!\n\n" +
                "Art: original, made for Word Z\n" +
                "Music: Free Casual Music Pack (Matheus Klein)\n" +
                "Font: Baloo 2 (SIL Open Font License)\n" +
                "Word list: ENABLE (public domain)", 28, Skin.Ink, TextAnchor.UpperCenter, false);
            text.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -470), new Vector2(680, 360));
            text.textWrappingMode = TMPro.TextWrappingModes.Normal;
        }
    }
}
