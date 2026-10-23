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
        public const string RevenueCatAppleKey = "REPLACE_WITH_APPL_KEY";
        public const string RevenueCatGoogleKey = "REPLACE_WITH_GOOG_KEY";

        // links (edit before release)
        public const string SupportEmail = "support@wordz.game";
        public const string PrivacyUrl = "https://example.com/wordz/privacy";
        public const string TermsUrl = "https://example.com/wordz/terms";

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
        public static int UnlockGems(int group) => group <= 1 ? 0 : group == 2 ? 15 : 25;

        // map chests at 25 / 50 / 75 stars
        public static readonly int[] ChestStars = { 25, 50, 75 };
        public static readonly int[] ChestCoins = { 150, 300, 600 };
        public static readonly int[] ChestGems = { 1, 2, 5 };

        // daily reward calendar (day 7 is the big chest)
        public static readonly int[] DailyCoins = { 100, 120, 150, 200, 250, 300, 600 };
        public static readonly int[] DailyGems = { 1, 0, 2, 0, 1, 2, 8 };

        // daily challenges
        public const int ChallengesPerDay = 4;
        public const int ChallengeAllCoins = 300;
        public const int ChallengeAllGems = 3;
    }
}
