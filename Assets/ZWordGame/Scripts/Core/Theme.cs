using TMPro;
using UnityEngine;
using UnityEngine.Audio;

namespace ZWord
{
    /// <summary>
    /// All swappable look-and-sound assets in one place. Lives at Resources/ZWordTheme.asset.
    /// Any empty slot falls back to the procedural art / synthesized sound, so the game always runs.
    /// The editor auto-fills this from the installed asset packs (menu: ZWord > Rebuild Theme).
    /// </summary>
    [System.Serializable]
    public class CategoryArt
    {
        public string category;
        public Sprite icon;
        public Sprite mapBackground;
    }

    [CreateAssetMenu(menuName = "ZWord/Theme", fileName = "ZWordTheme")]
    public class Theme : ScriptableObject
    {
        [Header("Font (TTF/OTF, turned into a TextMeshPro font at runtime)")]
        public Font font;
        [Tooltip("Generated from 'font' by the editor (ZWord > Rebuild Theme). Saved as an asset so it ships in builds.")]
        public TMP_FontAsset fontAsset;
        public Material fontShadow;
        public Material fontOutline;

        [Header("Sprites (optional - procedural art is used when empty)")]
        public Sprite panel;
        public Sprite hexTile;
        public Sprite star;
        public Sprite coin;
        public Sprite back;
        public Sprite settings;
        public Sprite pause;
        public Sprite clock;
        public Sprite magnifier;
        public Sprite rotate;
        public Sprite home;
        public Sprite share;
        public Sprite replay;
        public Sprite lockIcon;
        public Sprite gem;
        public Sprite chest;
        public Sprite chestOpen;
        public Sprite crown;
        public Sprite close;
        public Sprite gift;
        public Sprite trophy;
        public Sprite shopIcon;
        public Sprite quest;
        public Sprite timer;
        public Sprite sadFace;
        public Sprite leaf;

        [Header("Colour icons (Art/Icons)")]
        public Sprite iconStar;
        public Sprite iconBulb;
        public Sprite iconShuffle;
        public Sprite iconWand;
        public Sprite iconMagnifier;
        public Sprite iconClock;
        public Sprite iconPlay;
        public Sprite iconPause;
        public Sprite iconRestart;
        public Sprite iconExit;
        public Sprite iconGear;
        public Sprite iconBack;
        public Sprite iconCheck;
        public Sprite iconAd;
        public Sprite iconCalendar;
        public Sprite iconAvatar;
        public Sprite iconLetter;
        public Sprite chestPurple;

        [Header("Decorations")]
        public Sprite leafCorner;
        public Sprite skyline;

        [Header("Illustrations (optional)")]
        [Tooltip("Designed WORD Z logo. When empty the logo is built from text and tiles.")]
        public Sprite logo;
        public Sprite homeBackground;
        [Tooltip("Per-category icon and map background, matched by category name (e.g. CITY).")]
        public CategoryArt[] categoryArt = new CategoryArt[0];

        [HideInInspector] public int autoFillVersion;

        public CategoryArt ArtFor(string categoryName)
        {
            if (categoryArt == null) return null;
            foreach (var a in categoryArt)
                if (a != null && string.Equals(a.category, categoryName, System.StringComparison.OrdinalIgnoreCase)) return a;
            return null;
        }

        [Header("Music playlists (loops)")]
        public AudioClip[] homeMusic;
        public AudioClip[] gameMusic;

        [Header("Sound effects")]
        [Tooltip("Played for each selected tile, pitched up a pentatonic scale")]
        public AudioClip letter;
        public AudioClip wordFound;
        public AudioClip wrong;
        public AudioClip click;
        public AudioClip booster;
        public AudioClip starChime;
        public AudioClip win;
        public AudioClip lose;

        [Header("Optional mixer routing")]
        public AudioMixerGroup musicGroup;
        public AudioMixerGroup sfxGroup;

        static Theme current;

        public static Theme Current
        {
            get
            {
                if (current == null)
                {
                    current = Resources.Load<Theme>("ZWordTheme");
                    if (current == null)
                    {
                        current = CreateInstance<Theme>();
                        current.name = "ZWordTheme (empty)";
                    }
                }
                return current;
            }
        }
    }
}
