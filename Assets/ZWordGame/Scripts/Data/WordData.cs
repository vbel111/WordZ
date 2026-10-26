using System.Linq;
using UnityEngine;

namespace ZWord
{
    public class Category
    {
        public string Name;
        public Color Color;
        public int Group;       // 1 = "LEVEL 1" section, 2 = "LEVEL 2" section
        public int UnlockCost;  // coins needed to unlock (0 = free)
        public string[] Words = new string[0];   // only used by the runtime fallback generator
        public int LevelCount;

        // ---- limited-time events (e.g. HALLOWEEN) ----
        public bool IsEvent;
        public System.DateTime EventStart, EventEnd;   // local dates, EventEnd inclusive
        public string Badge;

        public void SetEvent(string start, string end, string badge)
        {
            if (string.IsNullOrEmpty(start) || string.IsNullOrEmpty(end)) return;
            if (!System.DateTime.TryParseExact(start, "yyyy-MM-dd", System.Globalization.CultureInfo.InvariantCulture, System.Globalization.DateTimeStyles.None, out EventStart)) return;
            if (!System.DateTime.TryParseExact(end, "yyyy-MM-dd", System.Globalization.CultureInfo.InvariantCulture, System.Globalization.DateTimeStyles.None, out EventEnd)) return;
            IsEvent = true;
            Badge = string.IsNullOrEmpty(badge) ? Name : badge;
        }

        /// <summary>Normal categories are always live; events only between their dates.</summary>
        public bool Live => !IsEvent || (System.DateTime.Today >= EventStart.Date && System.DateTime.Today <= EventEnd.Date);

        /// <summary>Time left before an event closes (end of its last day).</summary>
        public System.TimeSpan EventTimeLeft => EventEnd.Date.AddDays(1) - System.DateTime.Now;

        /// <summary>From baked levels.</summary>
        public Category(string name, string hex, int group, int cost, int levelCount)
        {
            Name = name;
            Color = Palette.Hex(hex);
            Group = group;
            UnlockCost = cost;
            LevelCount = levelCount;
        }

        /// <summary>Fallback definition with a word pool, used when no baked levels exist.</summary>
        public Category(string name, string hex, int group, int cost, string words)
        {
            LevelCount = WordData.FallbackLevels;
            Name = name;
            Color = Palette.Hex(hex);
            Group = group;
            UnlockCost = cost;
            Words = words.Split(' ')
                .Select(w => w.Trim().ToUpperInvariant())
                .Where(w => w.Length >= 3 && w.Length <= 7 && w.All(ch => ch >= 'A' && ch <= 'Z'))
                .Distinct()
                .ToArray();
        }
    }

    /// <summary>
    /// Category access. Real content comes from the baked levels (edit Content/categories.json and bake);
    /// the small built-in list below is only a fallback so the game still runs before the first bake.
    /// </summary>
    public static class WordData
    {
        public const int FallbackLevels = 10;

        public static Category[] Categories => LevelDatabase.Loaded ? LevelDatabase.Categories : Fallback;

        /// <summary>Levels in a category (all baked categories have 25).</summary>
        /// <summary>A normal (non-event) category: counts for quests, the Daily Puzzle and PLAY.</summary>
        public static bool IsRegular(int c) => c >= 0 && c < Categories.Length && !Categories[c].IsEvent;

        /// <summary>Index of the event running today, or -1.</summary>
        public static int ActiveEvent()
        {
            var cats = Categories;
            for (int c = 0; c < cats.Length; c++) if (cats[c].IsEvent && cats[c].Live) return c;
            return -1;
        }

        public static int LevelsPerCategory => LevelDatabase.Loaded ? BoardShapes.LevelsPerCategory : FallbackLevels;

        static readonly Category[] Fallback =
        {
            new Category("CITY", "F5A623", 1, 0,
                "STREET PARK BRIDGE TOWER MAYOR TAXI METRO PLAZA MALL BANK HOTEL CAFE ROAD LANE SQUARE TRAFFIC OFFICE MUSEUM LIBRARY SUBWAY ALLEY BUS TRAM MARKET SCHOOL CHURCH CORNER SIGNAL AVENUE SUBURB HARBOR STATION TUNNEL ZONE"),
            new Category("ELECTRONIC", "8E44EC", 1, 0,
                "RADIO PHONE LAPTOP CABLE MOUSE SCREEN CAMERA TABLET ROUTER SPEAKER CHARGER BATTERY MODEM DRONE ROBOT CHIP WIRE PLUG LASER SENSOR MONITOR CONSOLE PRINTER HEADSET REMOTE FAN LAMP CLOCK WATCH DIODE BULB"),
            new Category("THINGS", "3DC3F2", 1, 0,
                "CHAIR TABLE PENCIL BOTTLE MIRROR PILLOW BASKET CANDLE KEY CUP BOX BAG HAT SPOON FORK KNIFE PLATE BRUSH COMB TOWEL BUCKET LADDER HAMMER ROPE NEEDLE WALLET GLOVE SOCK BLANKET"),
            new Category("MEALS", "3DCB3A", 1, 0,
                "PIZZA PASTA SALAD SOUP BURGER STEAK RICE BREAD CURRY SUSHI TACO WAFFLE OMELET NOODLE CHEESE BACON TOAST PANCAKE RISOTTO KEBAB STEW FRIES CEREAL DONUT MUFFIN PIE CAKE TART BAGEL LASAGNA"),
            new Category("MUSIC", "A64BE0", 1, 0,
                "PIANO GUITAR DRUM VIOLIN FLUTE BASS SONG NOTE CHORD TEMPO RHYTHM MELODY OPERA JAZZ BLUES ROCK BAND CHOIR LYRIC TUNE HARP CELLO TRUMPET BANJO DISCO REGGAE BEAT ALBUM SINGER STAGE"),
            new Category("SPORT", "F2506A", 1, 0,
                "SOCCER TENNIS GOLF RUGBY BOXING HOCKEY CHESS SKIING POLO JUDO KARATE CYCLING ROWING DIVING SURF SKATE BALL GOAL TEAM COACH MATCH SCORE RACE SPRINT TROPHY MEDAL ARENA PLAYER REFEREE"),
            new Category("COUNTRIES", "2F8CF0", 2, 10000,
                "FRANCE SPAIN ITALY JAPAN CHINA INDIA BRAZIL CANADA MEXICO EGYPT PERU CHILE CUBA IRAN IRAQ NEPAL KENYA GHANA GREECE SWEDEN NORWAY POLAND TURKEY ICELAND IRELAND MALI CHAD OMAN QATAR LAOS FIJI TOGO"),
            new Category("CINEMA", "1FB5AD", 2, 10000,
                "MOVIE FILM ACTOR SCENE SCRIPT CAMERA DRAMA COMEDY HORROR POPCORN TICKET SCREEN SEQUEL OSCAR STUDIO STAR ROLE CAST CREW PLOT HERO VILLAIN TRAILER EDITOR STUNT ACTION CINEMA REEL SEAT"),
            new Category("ANIMALS", "FF8A3D", 2, 10000,
                "LION TIGER ZEBRA HORSE MONKEY RABBIT TURTLE EAGLE SHARK WHALE PANDA KOALA CAMEL BEAR WOLF FOX DEER GOAT SHEEP MOUSE SNAKE FROG OWL PARROT DONKEY GIRAFFE OTTER LLAMA BISON HIPPO"),
            new Category("NATURE", "5DB833", 2, 10000,
                "RIVER OCEAN FOREST DESERT VALLEY ISLAND CLOUD STORM RAIN SNOW WIND LEAF TREE FLOWER STONE LAKE BEACH CANYON MEADOW GLACIER VOLCANO SUNSET MOSS FERN ROOT SEED PLANT WAVE CAVE"),
        };
    }
}
