using System.Linq;
using UnityEditor;
using UnityEngine;

namespace ZWord.EditorTools
{
    /// <summary>
    /// Creates Assets/ZWordGame/Resources/ZWordTheme.asset on first load and fills empty slots
    /// from the installed packs (Hyper Casual UI font, Free Casual Music Pack).
    /// Also sets sensible import settings for music (streamed Vorbis) to keep memory low on phones.
    /// </summary>
    [InitializeOnLoad]
    public static class ThemeAutoSetup
    {
        const string ResourcesDir = "Assets/ZWordGame/Resources";
        const string ThemePath = ResourcesDir + "/ZWordTheme.asset";
        const string MusicDir = "Assets/FREE CASUAL MUSIC PACK";
        const string UiDir = "Assets/Hyper_Casual_UI";

        static ThemeAutoSetup()
        {
            EditorApplication.delayCall += () => Ensure(false);
        }

        [MenuItem("ZWord/Rebuild Theme (fill empty slots)")]
        static void RebuildMenu() => Ensure(true);

        static void Ensure(bool verbose)
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode) return;

            var theme = AssetDatabase.LoadAssetAtPath<Theme>(ThemePath);
            bool created = false;
            if (theme == null)
            {
                if (!AssetDatabase.IsValidFolder(ResourcesDir))
                    AssetDatabase.CreateFolder("Assets/ZWordGame", "Resources");
                theme = ScriptableObject.CreateInstance<Theme>();
                AssetDatabase.CreateAsset(theme, ThemePath);
                created = true;
            }
            else if (!verbose && theme.autoFillVersion >= CurrentFillVersion)
            {
                return; // already set up; only refill when asked from the menu
            }

            bool changed = created;

            if (theme.font == null)
            {
                theme.font = FindFont("Baloo2-ExtraBold") ?? FindFont("Baloo2-Bold");
                changed |= theme.font != null;
            }

            if (theme.font != null && theme.fontAsset == null)
            {
                BakeFont(theme);
                changed = true;
            }

            if (AssetDatabase.IsValidFolder(MusicDir))
            {
                var clips = AssetDatabase.FindAssets("t:AudioClip", new[] { MusicDir })
                    .Select(g => AssetDatabase.GUIDToAssetPath(g))
                    .ToArray();

                AudioClip Clip(string contains) => clips
                    .Where(p => System.IO.Path.GetFileNameWithoutExtension(p).ToUpperInvariant().Contains(contains))
                    .Select(p => AssetDatabase.LoadAssetAtPath<AudioClip>(p))
                    .FirstOrDefault();

                string[] Paths(params string[] keys) => clips
                    .Where(p => keys.Any(k => System.IO.Path.GetFileNameWithoutExtension(p).ToUpperInvariant().Contains(k)))
                    .OrderBy(p => p)
                    .ToArray();

                var homePaths = Paths("TROPICAL", "MARIMBA");
                var gamePaths = Paths("CASUAL THEME", "RUNNING WILD");

                if (theme.homeMusic == null || theme.homeMusic.Length == 0)
                {
                    theme.homeMusic = homePaths.Select(p => AssetDatabase.LoadAssetAtPath<AudioClip>(p)).Where(c => c).ToArray();
                    changed = true;
                }
                if (theme.gameMusic == null || theme.gameMusic.Length == 0)
                {
                    theme.gameMusic = gamePaths.Select(p => AssetDatabase.LoadAssetAtPath<AudioClip>(p)).Where(c => c).ToArray();
                    changed = true;
                }
                foreach (var p in homePaths.Concat(gamePaths)) MakeStreamingMusic(p);

                if (theme.letter == null) { theme.letter = Clip("POP"); changed = true; }
                if (theme.wordFound == null) { theme.wordFound = Clip("SPECIAL COLECT"); changed = true; }
                if (theme.booster == null) { theme.booster = Clip("POWERUP"); changed = true; }
                if (theme.win == null) { theme.win = Clip("FIREWORKS"); changed = true; }
            }

            if (theme.autoFillVersion < CurrentFillVersion || verbose)
            {
                if (theme.autoFillVersion < 3 && AssetDatabase.IsValidFolder(ArtDir))
                    AssetDatabase.ImportAsset(ArtDir, ImportAssetOptions.ImportRecursive | ImportAssetOptions.ForceUpdate);
                FillGeneratedArt(theme);
                FillIcons(theme);
                FillCategoryArt(theme);
                if (PlayerSettings.productName != GameConfig.GameName) PlayerSettings.productName = GameConfig.GameName;
                theme.autoFillVersion = CurrentFillVersion;
                changed = true;
            }

            if (changed)
            {
                EditorUtility.SetDirty(theme);
                AssetDatabase.SaveAssets();
            }
            if (verbose || created)
                Debug.Log($"[ZWord] Theme ready at {ThemePath} (font: {(theme.font ? theme.font.name : "none")}, " +
                          $"home music: {theme.homeMusic?.Length ?? 0}, game music: {theme.gameMusic?.Length ?? 0}).", theme);
        }

        /// <summary>Saves a dynamic TMP font asset (+ atlas, material) and shadow/outline material presets.</summary>
        static void BakeFont(Theme theme)
        {
            const string fontPath = ResourcesDir + "/ZWordFont SDF.asset";
            var fa = AssetDatabase.LoadAssetAtPath<TMPro.TMP_FontAsset>(fontPath);
            if (fa == null)
            {
                fa = TMPro.TMP_FontAsset.CreateFontAsset(theme.font, 72, 9,
                    UnityEngine.TextCore.LowLevel.GlyphRenderMode.SDFAA, 1024, 1024,
                    TMPro.AtlasPopulationMode.Dynamic, false);
                if (fa == null) { Debug.LogWarning("[ZWord] Could not create TMP font from " + theme.font.name); return; }
                fa.name = "ZWordFont SDF";
                AssetDatabase.CreateAsset(fa, fontPath);
                fa.atlasTextures[0].name = "ZWordFont Atlas";
                AssetDatabase.AddObjectToAsset(fa.atlasTextures[0], fa);
                fa.material.name = "ZWordFont Material";
                AssetDatabase.AddObjectToAsset(fa.material, fa);
                fa.TryAddCharacters(Fonts.Charset);
                EditorUtility.SetDirty(fa);
            }

            var shadow = Fonts.MakeShadow(fa.material);
            AssetDatabase.CreateAsset(shadow, ResourcesDir + "/ZWordFont Shadow.mat");
            var outline = Fonts.MakeOutline(fa.material);
            AssetDatabase.CreateAsset(outline, ResourcesDir + "/ZWordFont Outline.mat");

            theme.fontAsset = fa;
            theme.fontShadow = shadow;
            theme.fontOutline = outline;
        }

        const int CurrentFillVersion = 3;
        const string ArtDir = "Assets/ZWordGame/Art";

        static Sprite UiSprite(string relative)
        {
            var path = UiDir + "/Sprites/" + relative;
            var sprite = AssetDatabase.LoadAssetAtPath<Sprite>(path);
            if (sprite == null && AssetImporter.GetAtPath(path) is TextureImporter ti && ti.textureType != TextureImporterType.Sprite)
            {
                ti.textureType = TextureImporterType.Sprite;
                ti.spriteImportMode = SpriteImportMode.Single;
                ti.SaveAndReimport();
                sprite = AssetDatabase.LoadAssetAtPath<Sprite>(path);
            }
            return sprite;
        }

        /// <summary>Icons from the Hyper Casual UI pack that match the Word Z mockup. Only fills empty slots.</summary>
        static void FillIcons(Theme t)
        {
            if (!AssetDatabase.IsValidFolder(UiDir)) return;
            if (t.chestOpen == null) t.chestOpen = UiSprite("Icons/Opened Gold Treasure box.png");
            if (t.chest == null) t.chest = UiSprite("Icons/Gold Treasure box.png");
            if (t.crown == null) t.crown = UiSprite("Icons/Untitled design - 2026-04-20T163344.301 1.png");
            if (t.close == null) t.close = UiSprite("Icons/Close.png");
            if (t.lockIcon == null) t.lockIcon = UiSprite("Icons/lock.png");
            if (t.gift == null) t.gift = UiSprite("Icons/gift.png");
            if (t.trophy == null) t.trophy = UiSprite("Icons/leaderboard.png");
            if (t.shopIcon == null) t.shopIcon = UiSprite("Icons/shop.png");
            if (t.quest == null) t.quest = UiSprite("Icons/badge.png");
            if (t.timer == null) t.timer = UiSprite("Icons/timer.png");
        }

        static Sprite Art(string relative)
        {
            var path = ArtDir + "/" + relative;
            var s = AssetDatabase.LoadAssetAtPath<Sprite>(path);
            if (s == null && AssetImporter.GetAtPath(path) is TextureImporter ti)
            {
                ti.textureType = TextureImporterType.Sprite;
                ti.spriteImportMode = SpriteImportMode.Single;
                ti.SaveAndReimport();
                s = AssetDatabase.LoadAssetAtPath<Sprite>(path);
            }
            return s;
        }

        static readonly string[] ImageExt = { ".png", ".jpg", ".jpeg", ".webp", ".tga", ".psd" };

        static string Norm(string s)
        {
            var sb = new System.Text.StringBuilder();
            foreach (char c in s.ToLowerInvariant()) if (char.IsLetterOrDigit(c)) sb.Append(c);
            return sb.ToString();
        }

        /// <summary>
        /// Points every category at the best map image in Art/Maps (any sub-folder, any image type).
        /// A file matches when its name contains the category slug ("map_city.png", "City_AI_v2.jpg",
        /// "fruit veg.png"...). When several match, the most recently modified file wins, so newly
        /// dropped AI art replaces the generated maps automatically.
        /// </summary>
        public static int AssignMaps(Theme t)
        {
            var dir = ArtDir + "/Maps";
            if (t == null || !AssetDatabase.IsValidFolder(dir)) return 0;
            FillCategoryArt(t);
            var files = AssetDatabase.FindAssets("t:Texture2D", new[] { dir })
                .Select(AssetDatabase.GUIDToAssetPath)
                .Where(p => ImageExt.Contains(System.IO.Path.GetExtension(p).ToLowerInvariant()))
                .ToArray();
            int changed = 0;
            foreach (var a in t.categoryArt)
            {
                if (a == null) continue;
                var slug = Slug(a.category);
                var full = Norm(slug);
                var first = Norm(slug.Split('_')[0]);
                // an exact "map_<slug>.<ext>" file always wins; otherwise the newest file whose name contains the slug
                var exact = files.Where(p => System.IO.Path.GetFileNameWithoutExtension(p).ToLowerInvariant() == "map_" + slug)
                    .OrderByDescending(p => System.IO.File.GetLastWriteTimeUtc(p)).FirstOrDefault();
                var best = exact ?? files
                    .Where(p =>
                    {
                        var n = Norm(System.IO.Path.GetFileNameWithoutExtension(p));
                        return n.Contains(full) || (first.Length >= 4 && n.Contains(first));
                    })
                    .OrderByDescending(p => System.IO.File.GetLastWriteTimeUtc(p))
                    .FirstOrDefault();
                if (best == null) continue;
                var sprite = Art(best.Substring(ArtDir.Length + 1));
                if (sprite != null && sprite != a.mapBackground)
                {
                    a.mapBackground = sprite;
                    changed++;
                }
            }
            if (changed > 0) EditorUtility.SetDirty(t);
            return changed;
        }

        [MenuItem("ZWord/Reassign Map Backgrounds")]
        public static void ReassignMapsMenu()
        {
            var theme = AssetDatabase.LoadAssetAtPath<Theme>(ThemePath);
            int n = AssignMaps(theme);
            if (n > 0) AssetDatabase.SaveAssets();
            Debug.Log($"[ZWord] Map backgrounds: {n} categor{(n == 1 ? "y" : "ies")} updated.", theme);
        }

        public static string Slug(string category) => category.ToLowerInvariant().Replace(" & ", "_").Replace(' ', '_');

        /// <summary>The original Word Z art set in Assets/ZWordGame/Art (generated by Tools/ArtGen).</summary>
        static void FillGeneratedArt(Theme t)
        {
            if (!AssetDatabase.IsValidFolder(ArtDir)) return;
            Sprite I(string n) => Art("Icons/" + n + ".png");
            if (t.coin == null) t.coin = I("coin");
            if (t.gem == null) t.gem = I("gem");
            if (t.chest == null) t.chest = I("chest");
            if (t.chestPurple == null) t.chestPurple = I("chest_purple");
            if (t.crown == null) t.crown = I("crown");
            if (t.lockIcon == null) t.lockIcon = I("lock");
            if (t.gift == null) t.gift = I("gift");
            if (t.trophy == null) t.trophy = I("trophy");
            if (t.shopIcon == null) t.shopIcon = I("shop");
            if (t.quest == null) t.quest = I("quest");
            if (t.timer == null) t.timer = I("clock");
            if (t.sadFace == null) t.sadFace = I("sad");
            if (t.home == null) t.home = I("home");
            if (t.share == null) t.share = I("share");
            if (t.replay == null) t.replay = I("replay");
            if (t.iconStar == null) t.iconStar = I("star");
            if (t.iconBulb == null) t.iconBulb = I("bulb");
            if (t.iconShuffle == null) t.iconShuffle = I("shuffle");
            if (t.iconWand == null) t.iconWand = I("wand");
            if (t.iconMagnifier == null) t.iconMagnifier = I("magnifier");
            if (t.iconClock == null) t.iconClock = I("clock");
            if (t.iconPlay == null) t.iconPlay = I("play");
            if (t.iconPause == null) t.iconPause = I("pause");
            if (t.iconRestart == null) t.iconRestart = I("restart");
            if (t.iconExit == null) t.iconExit = I("exit");
            if (t.iconGear == null) t.iconGear = I("gear");
            if (t.iconBack == null) t.iconBack = I("back");
            if (t.iconCheck == null) t.iconCheck = I("check");
            if (t.iconAd == null) t.iconAd = I("ad");
            if (t.iconCalendar == null) t.iconCalendar = I("calendar");
            if (t.iconAvatar == null) t.iconAvatar = I("avatar");
            if (t.iconLetter == null) t.iconLetter = I("letter");
            if (t.logo == null) t.logo = Art("Logo/logo.png");
            if (t.homeBackground == null) t.homeBackground = Art("Backgrounds/home_bg.jpg");
            if (t.leafCorner == null) t.leafCorner = Art("Backgrounds/leaf_corner.png");
            if (t.skyline == null) t.skyline = Art("Backgrounds/skyline.png");

            FillCategoryArt(t);
            foreach (var a in t.categoryArt)
            {
                if (a == null) continue;
                var slug = Slug(a.category);
                if (a.icon == null) a.icon = Art("Categories/cat_" + slug + ".png");
            }
            AssignMaps(t);

            var appIcon = AssetDatabase.LoadAssetAtPath<Texture2D>(ArtDir + "/Logo/app_icon.png");
            if (appIcon != null)
            {
                var current = PlayerSettings.GetIcons(UnityEditor.Build.NamedBuildTarget.Unknown, IconKind.Any);
                if (current == null || current.Length == 0 || current[0] == null)
                    PlayerSettings.SetIcons(UnityEditor.Build.NamedBuildTarget.Unknown, new[] { appIcon }, IconKind.Any);
            }
        }

        /// <summary>One empty entry per category so you can drop in icons and map backgrounds by name.</summary>
        static void FillCategoryArt(Theme t)
        {
            const string catPath = "Assets/ZWordGame/Content/categories.json";
            if (!System.IO.File.Exists(catPath)) return;
            var defs = JsonUtility.FromJson<CategoryDefFile>(System.IO.File.ReadAllText(catPath));
            if (defs?.categories == null) return;
            var list = (t.categoryArt ?? new CategoryArt[0]).ToList();
            foreach (var d in defs.categories)
                if (!list.Any(a => a != null && a.category == d.name)) list.Add(new CategoryArt { category = d.name });
            t.categoryArt = list.ToArray();
        }

        static Font FindFont(string name)
        {
            var dirs = AssetDatabase.IsValidFolder(UiDir) ? new[] { UiDir } : new[] { "Assets" };
            var guid = AssetDatabase.FindAssets(name + " t:Font", dirs).FirstOrDefault();
            return guid == null ? null : AssetDatabase.LoadAssetAtPath<Font>(AssetDatabase.GUIDToAssetPath(guid));
        }

        static void MakeStreamingMusic(string path)
        {
            if (!(AssetImporter.GetAtPath(path) is AudioImporter imp)) return;
            var s = imp.defaultSampleSettings;
            if (s.loadType == AudioClipLoadType.Streaming && s.compressionFormat == AudioCompressionFormat.Vorbis) return;
            s.loadType = AudioClipLoadType.Streaming;
            s.compressionFormat = AudioCompressionFormat.Vorbis;
            s.quality = 0.6f;
            imp.defaultSampleSettings = s;
            imp.SaveAndReimport();
        }
    }
}
