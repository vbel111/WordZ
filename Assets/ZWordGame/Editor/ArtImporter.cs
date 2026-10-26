using System.Linq;
using UnityEditor;

namespace ZWord.EditorTools
{
    /// <summary>Import settings for the Word Z art: UI sprites, no mipmaps, sensible max sizes.</summary>
    public class ArtImporter : AssetPostprocessor
    {
        // bump to make Unity re-run these import rules on existing textures
        public override uint GetVersion() => 6;

        /// <summary>Gameplay music in Resources/Music: streamed Vorbis so each loop uses little RAM.</summary>
        void OnPreprocessAudio()
        {
            if (!assetPath.StartsWith("Assets/ZWordGame/Resources/Music/")) return;
            var ai = (AudioImporter)assetImporter;
            var s = ai.defaultSampleSettings;
            s.loadType = UnityEngine.AudioClipLoadType.Streaming;
            s.compressionFormat = UnityEngine.AudioCompressionFormat.Vorbis;
            s.quality = 0.6f;
            ai.defaultSampleSettings = s;
            ai.loadInBackground = true;
        }

        void OnPreprocessTexture()
        {
            // in-game backgrounds and the tutorial hand are loaded with Resources.Load<Texture2D> into RawImages
            if (assetPath.StartsWith("Assets/ZWordGame/Resources/GameBg/") || assetPath.StartsWith("Assets/ZWordGame/Resources/UI/")
                || assetPath.StartsWith("Assets/ZWordGame/Resources/CatCards/") || assetPath.EndsWith("Resources/tutorial_hand.png"))
            {
                var rti = (TextureImporter)assetImporter;
                rti.textureType = TextureImporterType.Default;
                rti.npotScale = TextureImporterNPOTScale.None;
                rti.mipmapEnabled = false;
                rti.alphaIsTransparency = true;
                rti.wrapMode = UnityEngine.TextureWrapMode.Clamp;
                rti.maxTextureSize = assetPath.Contains("/UI/") ? 2048 : 1024;
                rti.textureCompression = TextureImporterCompression.Compressed;
                return;
            }
            // home menu icons are loaded with Resources.Load<Sprite>
            if (assetPath.StartsWith("Assets/ZWordGame/Resources/HomeIcons/"))
            {
                var hti = (TextureImporter)assetImporter;
                hti.textureType = TextureImporterType.Sprite;
                hti.spriteImportMode = SpriteImportMode.Single;
                hti.mipmapEnabled = false;
                hti.alphaIsTransparency = true;
                hti.maxTextureSize = 256;
                hti.textureCompression = TextureImporterCompression.Compressed;
                return;
            }
            if (!assetPath.StartsWith("Assets/ZWordGame/Art/")) return;
            var ti = (TextureImporter)assetImporter;
            bool appIcon = assetPath.EndsWith("app_icon.png");
            ti.textureType = appIcon ? TextureImporterType.Default : TextureImporterType.Sprite;
            if (!appIcon) ti.spriteImportMode = SpriteImportMode.Single;
            ti.mipmapEnabled = false;
            ti.alphaIsTransparency = true;
            ti.wrapMode = UnityEngine.TextureWrapMode.Clamp;
            bool big = assetPath.Contains("/Maps/") || assetPath.Contains("/Backgrounds/") || assetPath.Contains("/Logo/");
            ti.maxTextureSize = appIcon ? 1024 : big ? 2048 : 256;
            // the iOS/Android icon exporter can't read compressed textures (ASTC) - keep the icon as raw RGBA
            ti.textureCompression = appIcon ? TextureImporterCompression.Uncompressed : TextureImporterCompression.Compressed;
            if (appIcon) ti.isReadable = true;
            // full-screen painted maps/backgrounds: ASTC 8x8 is ~45% smaller than the default 6x6 and looks the same
            if (assetPath.Contains("/Maps/") || assetPath.Contains("/Backgrounds/home_bg"))
                foreach (var plat in new[] { "iPhone", "Android" })
                {
                    var ps = ti.GetPlatformTextureSettings(plat);
                    ps.overridden = true;
                    ps.maxTextureSize = 2048;
                    ps.format = TextureImporterFormat.ASTC_8x8;
                    ti.SetPlatformTextureSettings(ps);
                }
        }

        /// <summary>New or replaced map art is picked up by the Theme automatically.</summary>
        static void OnPostprocessAllAssets(string[] imported, string[] deleted, string[] moved, string[] movedFrom)
        {
            bool Hit(string p) => p.StartsWith("Assets/ZWordGame/Art/Maps/") || p.StartsWith("Assets/ZWordGame/Art/Categories/")
                                  || p == "Assets/ZWordGame/Content/categories.json";
            if (!imported.Any(Hit) && !moved.Any(Hit)) return;
            EditorApplication.delayCall += () =>
            {
                var theme = AssetDatabase.LoadAssetAtPath<Theme>("Assets/ZWordGame/Resources/ZWordTheme.asset");
                if (theme == null) return;
                if (ThemeAutoSetup.SyncCategoryArt(theme))
                {
                    EditorUtility.SetDirty(theme);
                    AssetDatabase.SaveAssets();
                    UnityEngine.Debug.Log("[ZWord] Updated category icons / map art.", theme);
                }
            };
        }
    }
}
