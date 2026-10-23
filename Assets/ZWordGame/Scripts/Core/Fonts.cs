using TMPro;
using UnityEngine;
using UnityEngine.TextCore.LowLevel;

namespace ZWord
{
    /// <summary>
    /// TextMeshPro font + three shared material presets (plain, soft drop-shadow, outlined) so labels batch well.
    /// Uses the font asset and materials the editor bakes into the Theme (so shader variants ship in builds);
    /// falls back to building them at runtime, then to TMP's default font.
    /// </summary>
    public static class Fonts
    {
        static TMP_FontAsset asset;
        static Material plain, shadow, outline;

        public static TMP_FontAsset Asset { get { Init(); return asset; } }
        public static Material Plain { get { Init(); return plain; } }
        public static Material Shadow { get { Init(); return shadow; } }
        public static Material Outline { get { Init(); return outline; } }

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ResetStatics() { asset = null; plain = shadow = outline = null; }

        /// <summary>Warm dark brown outline, matching the logo.</summary>
        public static readonly Color OutlineColor = new Color(0.36f, 0.18f, 0.05f, 0.9f);

        static void Init()
        {
            if (asset != null && plain != null && shadow != null && outline != null) return;
            InitMaterials();
            if (outline != null) outline.SetColor(ShaderUtilities.ID_OutlineColor, OutlineColor);
        }

        static void InitMaterials()
        {
            var theme = Theme.Current;

            if (theme.fontAsset != null)
            {
                asset = theme.fontAsset;
                plain = asset.material;
                shadow = theme.fontShadow != null ? theme.fontShadow : MakeShadow(plain);
                outline = theme.fontOutline != null ? theme.fontOutline : MakeOutline(plain);
                return;
            }

            if (theme.font != null)
            {
                asset = TMP_FontAsset.CreateFontAsset(theme.font, 72, 9, GlyphRenderMode.SDFAA, 1024, 1024,
                    AtlasPopulationMode.Dynamic, false);
                if (asset != null) asset.TryAddCharacters(Charset);
            }
            if (asset == null) asset = TMP_Settings.defaultFontAsset;

            plain = asset.material;
            shadow = MakeShadow(plain);
            outline = MakeOutline(plain);
        }

        public const string Charset =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !?%+-:,.'/";

        public static Material MakeShadow(Material source)
        {
            var m = new Material(source) { name = "ZWord Shadow" };
            m.EnableKeyword(ShaderUtilities.Keyword_Underlay);
            m.SetColor(ShaderUtilities.ID_UnderlayColor, new Color(0f, 0f, 0f, 0.3f));
            m.SetFloat(ShaderUtilities.ID_UnderlayOffsetX, 0f);
            m.SetFloat(ShaderUtilities.ID_UnderlayOffsetY, -0.6f);
            m.SetFloat(ShaderUtilities.ID_UnderlaySoftness, 0.15f);
            return m;
        }

        public static Material MakeOutline(Material source)
        {
            var m = MakeShadow(source);
            m.name = "ZWord Outline";
            m.EnableKeyword(ShaderUtilities.Keyword_Outline);
            m.SetFloat(ShaderUtilities.ID_OutlineWidth, 0.18f);
            m.SetColor(ShaderUtilities.ID_OutlineColor, OutlineColor);
            m.SetFloat(ShaderUtilities.ID_FaceDilate, 0.1f);
            return m;
        }
    }
}
