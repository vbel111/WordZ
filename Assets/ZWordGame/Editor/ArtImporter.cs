using UnityEditor;

namespace ZWord.EditorTools
{
    /// <summary>Import settings for the Word Z art: UI sprites, no mipmaps, sensible max sizes.</summary>
    public class ArtImporter : AssetPostprocessor
    {
        // bump to make Unity re-run these import rules on existing textures
        public override uint GetVersion() => 5;

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
        }

        /// <summary>New or replaced map art is picked up by the Theme automatically.</summary>
        static void OnPostprocessAllAssets(string[] imported, string[] deleted, string[] moved, string[] movedFrom)
        {
            bool maps = false;
            foreach (var p in imported) if (p.StartsWith("Assets/ZWordGame/Art/Maps/")) { maps = true; break; }
            if (!maps) foreach (var p in moved) if (p.StartsWith("Assets/ZWordGame/Art/Maps/")) { maps = true; break; }
            if (!maps) return;
            EditorApplication.delayCall += () =>
            {
                var theme = AssetDatabase.LoadAssetAtPath<Theme>("Assets/ZWordGame/Resources/ZWordTheme.asset");
                if (theme == null) return;
                int n = ThemeAutoSetup.AssignMaps(theme);
                if (n > 0)
                {
                    AssetDatabase.SaveAssets();
                    UnityEngine.Debug.Log($"[ZWord] Applied new map art to {n} categor{(n == 1 ? "y" : "ies")}.", theme);
                }
            };
        }
    }
}
