namespace ZWord
{
    /// <summary>
    /// Economy and tuning numbers in one place. (In M5 these become Remote Config keys so they can be
    /// tuned without an app update.)
    /// </summary>
    public static class GameConfig
    {
        public const string GameName = "Word Z";

        // store identity (used by ZWord > Apply Release Settings). Must match App Store Connect / Play Console / RevenueCat.
        public const string BundleId = "com.zdev.wordz";
        public const string CompanyName = "Word Z";
        public const string Version = "1.0.0";
        public const int BuildNumber = 1;   // increase for every upload

        // RevenueCat public SDK keys (Project settings > API keys in the RevenueCat dashboard). Safe to ship in the app.
        public const string RevenueCatAppleKey = "appl_cyYraodxUAHRrKSTWrahYljTBRD";
        public const string RevenueCatGoogleKey = "REPLACE_WITH_GOOG_KEY";
        // RevenueCat Test Store key: real purchase flow with fake money, no App Store / Play setup needed.
        // Use it for development + TestFlight; set UseRevenueCatTestStore = false (and fill the two keys above) for release.
        public const string RevenueCatTestKey = "test_FyGNvRbPQHceOTEToxJLAQDIktx";
        public const bool UseRevenueCatTestStore = false;

        // Word Z Pro (RevenueCat entitlement - attach your subscription/lifetime products to it in the dashboard)
        public const bool ProEnabled = false;          // no Pro for now: Word Z sells coins, gems and the Supporter Pack
        public const string ProEntitlement = "wordz_pro";
        public const int ProDailyMultiplier = 2;       // Pro: daily reward coins x2
        public const int ProLevelBonusCoins = 20;      // Pro: extra coins on every level win

        // the "consumable" product (one-time, can be bought again) - what it gives
        public const string ConsumableId = "consumable";
        public const int ConsumableCoins = 500;

        // links (edit before release)
        public const string SupportEmail = "support@wordz.game";
        public const string PrivacyUrl = "https://vbel111.github.io/WordZ/privacy.html";
        public const string TermsUrl = "https://vbel111.github.io/WordZ/terms.html";

        // App Store Connect > your app > App Information > "Apple ID" (a number like 6741234567)
        public const string AppleAppId = "6826203884";

        /// <summary>Store page for this platform - used by Share and the rate prompt.</summary>
        public static string StoreUrl =>
#if UNITY_IOS
            string.IsNullOrEmpty(AppleAppId) ? "" : "https://apps.apple.com/app/id" + AppleAppId;
#else
            "https://play.google.com/store/apps/details?id=" + BundleId;
#endif

        // shop (product ids are used by IAP in M5)
        public static readonly (string id, int coins, string price, string tag)[] CoinPacks =
        {
            ("wordz.coins.500", 500, "$0.99", null),
            ("wordz.coins.1200", 1200, "$1.99", "POPULAR"),
            ("wordz.coins.2800", 2800, "$3.99", null),
            ("wordz.coins.6500", 6500, "$6.99", "BEST VALUE"),
        };
        public static readonly (string id, int gems, string price, string tag)[] GemPacks =
        {
            ("wordz.gems.20", 20, "$1.99", null),
            ("wordz.gems.60", 60, "$4.99", "POPULAR"),
            ("wordz.gems.150", 150, "$9.99", "BEST VALUE"),
        };
        /// <summary>One-time "thank you" bundle. Word Z has no ads, so this replaces Remove Ads.</summary>
        public const string SupporterId = "wordz.supporter";
        public const string SupporterPrice = "$2.99";
        public const int SupporterCoins = 2000;
        public const int SupporterGems = 30;
        public const int SupporterBoosters = 5;   // of each booster
        /// <summary>Hint bundles bought with coins: (booster, amount, coin price, title).</summary>
        public static readonly (Booster booster, int amount, int coins, string title)[] HintBundles =
        {
            (Booster.Letter, 5, 120, "5 Reveal Letters"),
            (Booster.Shuffle, 3, 150, "3 Shuffles"),
            (Booster.Time, 3, 120, "3 Time Boosts"),
            (Booster.Reveal, 3, 240, "3 Reveal Words"),
        };

        // starting wallet
        // Word Z is generous and ad-free: everything can be earned by playing; purchases are optional.
        public const int StartCoins = 500;
        public const int StartGems = 10;

        // finishing the first-launch tutorial
        public const int TutorialCoins = 200;

        // level rewards
        public static int LevelCoins(int stars) => 60 + 20 * (stars - 1);
        public const int GemsForThreeStars = 1;
        public const int BonusWordCoins = 10;
        public const int BonusWordPoints = 50;

        // hint prices (coins) - order matches the Hints popup
        public const int CostRevealLetter = 30;
        public const int CostWordStarts = 60;
        public const int CostShuffle = 60;
        public const int CostRevealWord = 90;
        public const int CostExtraTime = 50;

        // continue when time runs out
        public const int ContinueSeconds = 30;
        public const int ContinueGems = 1;
        public const int ContinueCoins = 80;

        // category unlock
        /// <summary>Gems to skip a star goal: about 1 gem per 20 stars, at least 10 (150 stars = 10, 1,600 stars = 80).</summary>
        public static int UnlockGems(int starsNeeded) => starsNeeded <= 0 ? 0 : System.Math.Max(10, (int)System.Math.Round(starsNeeded / 20.0));

        // map chests every 25 stars (50 levels x 3 stars = 150)
        public static readonly int[] ChestStars = { 25, 50, 75, 100, 125, 150 };
        public static readonly int[] ChestCoins = { 150, 300, 600, 800, 1000, 1500 };
        public static readonly int[] ChestGems = { 1, 2, 5, 5, 8, 12 };

        // daily reward calendar (day 7 is the big chest)
        public static readonly int[] DailyCoins = { 100, 120, 150, 200, 250, 300, 600 };
        public static readonly int[] DailyGems = { 1, 0, 2, 0, 1, 2, 8 };

        // boss board (last level of each category, 37 tiles): one-time crown reward
        public const int BossCoins = 300;
        public const int BossGems = 5;

        // golden hex: a gold tile hidden in some levels; finding the word through it pays a gem (capped per day)
        public const float GoldenChance = 0.35f;
        public const int GoldenPerDay = 3;
        public const int GoldenGems = 1;

        // combos: words found within this many seconds of each other chain up; x1.5 then x2 points, +coins from x3
        public const float ComboWindow = 6f;
        public const int ComboCoins = 2;

        // Word Book: completing a category's page
        public const int BookPageGems = 10;

        // limited-time event: finishing every level earns its badge + this
        public const int EventBadgeCoins = 500;
        public const int EventBadgeGems = 10;

        // daily challenges
        public const int ChallengesPerDay = 4;
        public const int ChallengeAllCoins = 300;
        public const int ChallengeAllGems = 3;
    }
}
