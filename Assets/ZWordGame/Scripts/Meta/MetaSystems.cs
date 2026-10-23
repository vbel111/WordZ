using System;
using System.Linq;

namespace ZWord
{
    public enum Metric { Levels, Words, Score, Bonus, ThreeStars, Hints, Combos, LongWords, NoHints, DailyPuzzle, Rotate }

    static class Day
    {
        public static string Today => DateTime.Now.ToString("yyyy-MM-dd");
        public static string Yesterday => DateTime.Now.AddDays(-1).ToString("yyyy-MM-dd");
        public static TimeSpan UntilMidnight => DateTime.Today.AddDays(1) - DateTime.Now;

        public static string Countdown()
        {
            var t = UntilMidnight;
            return t.TotalHours >= 1 ? $"{(int)t.TotalHours}h {t.Minutes:00}m" : $"{t.Minutes}m {t.Seconds:00}s";
        }
    }

    /// <summary>7-day login calendar. Missing a day restarts at day 1; day 7 is the big chest.</summary>
    public static class DailyRewards
    {
        public static bool CanClaim => Save.Data.dailyLastClaim != Day.Today;

        /// <summary>Index (0-6) of the day that will be claimed next.</summary>
        public static int NextDay
        {
            get
            {
                var d = Save.Data;
                if (!string.IsNullOrEmpty(d.dailyLastClaim) && d.dailyLastClaim != Day.Today && d.dailyLastClaim != Day.Yesterday)
                    return 0; // streak broken
                return d.dailyDay % 7;
            }
        }

        public static (int coins, int gems) Claim()
        {
            if (!CanClaim) return (0, 0);
            int day = NextDay;
            int coins = GameConfig.DailyCoins[day], gems = GameConfig.DailyGems[day];
            var d = Save.Data;
            d.dailyDay = (day + 1) % 7;
            d.dailyLastClaim = Day.Today;
            d.dailyClaims++;
            Save.Coins += coins;
            if (gems > 0) Save.Gems += gems;
            return (coins, gems);
        }
    }

    /// <summary>Three daily challenges picked from a pool with a date seed (same for everyone that day).</summary>
    public static class Challenges
    {
        public struct Def
        {
            public Metric Metric;
            public int Target;
            public int Coins;
            public string Text;
            public Def(Metric m, int target, int coins, string text) { Metric = m; Target = target; Coins = coins; Text = text; }
        }

        public static readonly Def[] Pool =
        {
            new Def(Metric.Levels, 3, 100, "Complete 3 levels"),
            new Def(Metric.Levels, 5, 150, "Complete 5 levels"),
            new Def(Metric.Levels, 8, 220, "Complete 8 levels"),
            new Def(Metric.Words, 10, 150, "Find 10 words"),
            new Def(Metric.Words, 25, 200, "Find 25 words"),
            new Def(Metric.Words, 40, 260, "Find 40 words"),
            new Def(Metric.Score, 8000, 120, "Score 8,000 points"),
            new Def(Metric.Score, 20000, 200, "Score 20,000 points"),
            new Def(Metric.Score, 35000, 280, "Score 35,000 points"),
            new Def(Metric.Bonus, 3, 150, "Find 3 bonus words"),
            new Def(Metric.Bonus, 6, 220, "Find 6 bonus words"),
            new Def(Metric.ThreeStars, 2, 180, "Get 3 stars twice"),
            new Def(Metric.ThreeStars, 4, 260, "Get 3 stars 4 times"),
            new Def(Metric.Hints, 2, 80, "Use 2 hints"),
            new Def(Metric.Hints, 5, 120, "Use 5 hints"),
            new Def(Metric.Combos, 3, 150, "Make 3 combos"),
            new Def(Metric.Combos, 8, 240, "Make 8 combos"),
            new Def(Metric.LongWords, 3, 160, "Find 3 words of 6+ letters"),
            new Def(Metric.LongWords, 6, 240, "Find 6 words of 6+ letters"),
            new Def(Metric.NoHints, 2, 180, "Win 2 levels without hints"),
            new Def(Metric.NoHints, 4, 260, "Win 4 levels without hints"),
            new Def(Metric.DailyPuzzle, 1, 120, "Solve the Daily Puzzle"),
            new Def(Metric.Rotate, 5, 80, "Rotate the board 5 times"),
        };

        static void EnsureToday()
        {
            var d = Save.Data;
            int n = GameConfig.ChallengesPerDay;
            if (d.challengeDate == Day.Today && d.challengeIds != null && d.challengeIds.Length == n) return;
            int seed = 17;
            foreach (char ch in Day.Today) seed = unchecked(seed * 31 + ch);
            var rng = new Random(seed);
            var ids = Enumerable.Range(0, Pool.Length).OrderBy(_ => rng.Next()).ToList();
            // never two challenges of the same kind on one day
            var chosen = new System.Collections.Generic.List<int>();
            foreach (var id in ids)
            {
                if (chosen.Any(c => Pool[c].Metric == Pool[id].Metric)) continue;
                chosen.Add(id);
                if (chosen.Count == n) break;
            }
            d.challengeDate = Day.Today;
            d.challengeIds = chosen.ToArray();
            d.challengeProgress = new int[n];
            d.challengeClaimed = new bool[n];
            d.challengeBonusClaimed = false;
            Save.Write();
        }

        public static Def Get(int slot) { EnsureToday(); return Pool[Save.Data.challengeIds[slot]]; }
        public static int Progress(int slot) { EnsureToday(); return Save.Data.challengeProgress[slot]; }
        public static bool Claimed(int slot) { EnsureToday(); return Save.Data.challengeClaimed[slot]; }
        public static bool Complete(int slot) => Progress(slot) >= Get(slot).Target;
        public static int Count => GameConfig.ChallengesPerDay;
        public static int ClaimedCount { get { EnsureToday(); return Save.Data.challengeClaimed.Count(c => c); } }
        public static bool BonusReady => ClaimedCount == Count && !Save.Data.challengeBonusClaimed;

        public static int Claimable
        {
            get
            {
                EnsureToday();
                int n = 0;
                for (int i = 0; i < Count; i++) if (Complete(i) && !Claimed(i)) n++;
                return n + (BonusReady ? 1 : 0);
            }
        }

        public static void Report(Metric m, int amount)
        {
            EnsureToday();
            var d = Save.Data;
            for (int i = 0; i < d.challengeIds.Length; i++)
                if (Pool[d.challengeIds[i]].Metric == m) d.challengeProgress[i] = Math.Min(Pool[d.challengeIds[i]].Target, d.challengeProgress[i] + amount);
        }

        public static int Claim(int slot)
        {
            if (!Complete(slot) || Claimed(slot)) return 0;
            Save.Data.challengeClaimed[slot] = true;
            int coins = Get(slot).Coins;
            Save.Data.challengesClaimed++;
            Save.Coins += coins;
            return coins;
        }

        public static bool ClaimBonus()
        {
            if (!BonusReady) return false;
            Save.Data.challengeBonusClaimed = true;
            Save.Coins += GameConfig.ChallengeAllCoins;
            Save.Gems += GameConfig.ChallengeAllGems;
            return true;
        }
    }

    /// <summary>
    /// One special level a day, the same for every player (date seed). Solving it on consecutive days builds a
    /// streak: more coins each day, and every 7th day pays out a pile of gems.
    /// </summary>
    public static class DailyPuzzle
    {
        static int Seed()
        {
            int seed = 7919;
            foreach (char ch in Day.Today) seed = unchecked(seed * 31 + ch);
            return seed & 0x7fffffff;
        }

        /// <summary>Today's level: any category (locked ones too), from the middle of its difficulty curve.</summary>
        public static void Pick(out int cat, out int lvl)
        {
            var rng = new Random(Seed());
            cat = rng.Next(WordData.Categories.Length);
            int count = Math.Max(1, WordData.Categories[cat].LevelCount);
            int lo = Math.Min(count - 1, count / 4), hi = Math.Max(lo + 1, count * 4 / 5);
            lvl = rng.Next(lo, hi);
        }

        public static bool DoneToday => Save.Data.dailyPuzzleDate == Day.Today;

        /// <summary>Current streak as shown to the player (0 if a day was missed).</summary>
        public static int Streak
        {
            get
            {
                var d = Save.Data;
                return d.dailyPuzzleDate == Day.Today || d.dailyPuzzleDate == Day.Yesterday ? d.dailyPuzzleStreak : 0;
            }
        }

        public static int CoinsFor(int streakDay) => 150 + 25 * Math.Min(Math.Max(streakDay - 1, 0), 6);
        public static int GemsFor(int streakDay) => streakDay > 0 && streakDay % 7 == 0 ? 5 : 1;

        /// <summary>Records today's solve. Returns the reward, or (0,0) if it was already solved today.</summary>
        public static (int coins, int gems, int streak) Complete(int score)
        {
            var d = Save.Data;
            if (score > d.dailyPuzzleBest) d.dailyPuzzleBest = score;
            if (DoneToday) return (0, 0, d.dailyPuzzleStreak);
            d.dailyPuzzleStreak = d.dailyPuzzleDate == Day.Yesterday ? d.dailyPuzzleStreak + 1 : 1;
            d.dailyPuzzleDate = Day.Today;
            d.dailyPuzzlesSolved++;
            d.dailyPuzzleBestStreak = Math.Max(d.dailyPuzzleBestStreak, d.dailyPuzzleStreak);
            Challenges.Report(Metric.DailyPuzzle, 1);
            int coins = CoinsFor(d.dailyPuzzleStreak), gems = GemsFor(d.dailyPuzzleStreak);
            Save.Coins += coins;
            Save.Gems += gems;
            return (coins, gems, d.dailyPuzzleStreak);
        }
    }

    /// <summary>Lifetime achievements with tiers.</summary>
    public static class Quests
    {
        public struct Def
        {
            public string Format;   // "{0}" = target
            public Func<int> Value;
            public int[] Tiers;
            public Def(string f, Func<int> v, params int[] tiers) { Format = f; Value = v; Tiers = tiers; }
        }

        public static readonly Def[] All =
        {
            new Def("Finish {0} levels", () => Save.Data.levelsCompleted, 5, 25, 100, 250, 500),
            new Def("Find {0} words", () => Save.Data.wordsFound, 50, 250, 1000, 3000),
            new Def("Win {0} levels with 3 stars", () => Save.Data.threeStarWins, 5, 25, 100, 250),
            new Def("Find {0} bonus words", () => Save.Data.bonusWords, 10, 50, 200, 500),
            new Def("Unlock {0} categories", UnlockedCount, 7, 10, 15, 20),
            new Def("Collect {0} stars", () => Save.StarPoints, 10000, 50000, 200000, 500000),
            new Def("Find {0} words of 6+ letters", () => Save.Data.longWords, 10, 50, 200, 500),
            new Def("Make {0} combos", () => Save.Data.combos, 10, 50, 200, 600),
            new Def("Win {0} levels without hints", () => Save.Data.noHintWins, 5, 25, 100, 300),
            new Def("Complete {0} categories", CompletedCategories, 1, 3, 6, 10, 20),
            new Def("Solve {0} Daily Puzzles", () => Save.Data.dailyPuzzlesSolved, 3, 10, 30, 100),
            new Def("Reach a {0}-day Daily Puzzle streak", () => Save.Data.dailyPuzzleBestStreak, 3, 7, 14, 30),
            new Def("Claim {0} daily rewards", () => Save.Data.dailyClaims, 7, 30, 100, 365),
            new Def("Finish {0} daily challenges", () => Save.Data.challengesClaimed, 10, 50, 150, 500),
        };

        static int CompletedCategories()
        {
            int n = 0;
            var cats = WordData.Categories;
            for (int c = 0; c < cats.Length; c++) if (Save.Completed(c) >= cats[c].LevelCount) n++;
            return n;
        }

        static int UnlockedCount()
        {
            int n = 0;
            for (int c = 0; c < WordData.Categories.Length; c++) if (Save.Unlocked(c)) n++;
            return n;
        }

        static void Ensure()
        {
            var d = Save.Data;
            if (d.questTiers == null || d.questTiers.Length < All.Length)
            {
                var t = new int[All.Length];
                if (d.questTiers != null) Array.Copy(d.questTiers, t, Math.Min(d.questTiers.Length, t.Length));
                d.questTiers = t;
            }
        }

        public static int Tier(int q) { Ensure(); return Save.Data.questTiers[q]; }
        public static bool Done(int q) => Tier(q) >= All[q].Tiers.Length;
        public static int Target(int q) => All[q].Tiers[Math.Min(Tier(q), All[q].Tiers.Length - 1)];
        public static bool Ready(int q) => !Done(q) && All[q].Value() >= Target(q);
        public static int RewardCoins(int q) => 100 * (Tier(q) + 1);
        public static int RewardGems(int q) => Tier(q) >= 2 ? Tier(q) : 0;

        public static int Claimable
        {
            get
            {
                int n = 0;
                for (int q = 0; q < All.Length; q++) if (Ready(q)) n++;
                return n;
            }
        }

        public static (int coins, int gems) Claim(int q)
        {
            if (!Ready(q)) return (0, 0);
            int coins = RewardCoins(q), gems = RewardGems(q);
            Save.Data.questTiers[q]++;
            Save.Coins += coins;
            if (gems > 0) Save.Gems += gems;
            return (coins, gems);
        }
    }
}
