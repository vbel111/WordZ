using System;
using System.Collections.Generic;
using System.Linq;

namespace ZWord
{
    /// <summary>
    /// Word Book: every answer word a player has found, one page per category. A full page pays gems once.
    /// Words found before the book existed are filled in from finished levels the first time it is used.
    /// </summary>
    public static class WordBook
    {
        public static void EnsureSeeded()
        {
            var d = Save.Data;
            if (d.bookSeeded) return;
            var cats = WordData.Categories;
            for (int c = 0; c < cats.Length; c++)
            {
                int done = Math.Min(Save.Completed(c), cats[c].LevelCount);
                for (int l = 0; l < done; l++)
                    foreach (var w in LevelDatabase.WordsOfLevel(c, l)) Save.RecordWord(c, w);
            }
            d.bookSeeded = true;
            Save.Write();
        }

        public static int Total(int cat) => LevelDatabase.WordsIn(cat).Length;

        /// <summary>Found words that are on this category's page (ignores stray words from old boards).</summary>
        public static int Found(int cat)
        {
            var page = LevelDatabase.WordsIn(cat);
            var have = Save.BookWords(cat);
            int n = 0;
            foreach (var w in page) if (have.Contains(w)) n++;
            return n;
        }

        public static bool Has(int cat, string w) => Save.BookWords(cat).Contains(w);
        public static bool Complete(int cat) { int t = Total(cat); return t > 0 && Found(cat) >= t; }
        public static bool CanClaim(int cat) => Complete(cat) && !Save.BookClaimed(cat);

        /// <summary>Categories shown in the book: every normal category, plus events that are live or already started.</summary>
        public static IEnumerable<int> Pages()
        {
            var cats = WordData.Categories;
            for (int c = 0; c < cats.Length; c++)
                if (!cats[c].IsEvent || cats[c].Live || Save.BookWords(c).Count > 0) yield return c;
        }

        public static int Claimable => Pages().Count(c => CanClaim(c));
        public static int TotalFound => Pages().Sum(c => Found(c));
        public static int TotalWords => Pages().Sum(c => Total(c));

        public static int Claim(int cat)
        {
            if (!CanClaim(cat)) return 0;
            Save.SetBookClaimed(cat);
            Save.Gems += GameConfig.BookPageGems;
            return GameConfig.BookPageGems;
        }
    }

    /// <summary>Limited-time events (a special category with dates) and the badges they award.</summary>
    public static class Events
    {
        /// <summary>Awards the event badge once every level is done. True when it was just earned.</summary>
        public static bool TryAwardBadge(int cat)
        {
            var cats = WordData.Categories;
            if (cat < 0 || cat >= cats.Length || !cats[cat].IsEvent) return false;
            var c = cats[cat];
            if (Save.Completed(cat) < c.LevelCount || Save.HasBadge(c.Badge)) return false;
            Save.Data.badges.Add(c.Badge);
            Save.Coins += GameConfig.EventBadgeCoins;
            Save.Gems += GameConfig.EventBadgeGems;
            return true;
        }

        public static string TimeLeftText(Category c)
        {
            var t = c.EventTimeLeft;
            if (t.TotalSeconds <= 0) return "ENDED";
            if (t.TotalDays >= 1) return (int)t.TotalDays + "d " + t.Hours + "h";
            return t.Hours + "h " + t.Minutes.ToString("00") + "m";
        }
    }

    /// <summary>Golden hex: one gold tile in some levels; the word that uses it pays a gem (a few per day).</summary>
    public static class GoldenHex
    {
        public static int LeftToday
        {
            get
            {
                var d = Save.Data;
                return d.goldDate == Day.Today ? Math.Max(0, GameConfig.GoldenPerDay - d.goldCount) : GameConfig.GoldenPerDay;
            }
        }

        public static bool Roll() => LeftToday > 0 && UnityEngine.Random.value < GameConfig.GoldenChance;

        public static int Collect()
        {
            if (LeftToday <= 0) return 0;
            var d = Save.Data;
            if (d.goldDate != Day.Today) { d.goldDate = Day.Today; d.goldCount = 0; }
            d.goldCount++;
            d.goldenHexes++;
            Save.Gems += GameConfig.GoldenGems;
            return GameConfig.GoldenGems;
        }
    }

    /// <summary>Boss boards (the 37-tile last level of a category): a crown and a one-time reward.</summary>
    public static class Boss
    {
        /// <summary>Call on a boss win (before stars are saved). Pays once per boss board: (coins, gems), else (0,0).</summary>
        public static (int coins, int gems) Crown(int cat, int lvl)
        {
            bool firstWin = Save.Stars(cat, lvl) == 0;
            if (!Save.HasCrown(cat)) Save.SetCrown(cat);
            if (!firstWin) return (0, 0);
            Save.Data.bossWins++;
            return (GameConfig.BossCoins, GameConfig.BossGems);
        }
    }
}

namespace ZWord
{
    /// <summary>
    /// Personal boards: every player gets their own deal of each level - same board shape, same word lengths
    /// (so the same difficulty) but words drawn from the category's pool and laid out with a seed from the
    /// player's id. Replaying a level on a new install / another device gives a fresh board instead of
    /// one you already know by heart. The Daily Puzzle stays the same for everyone.
    /// </summary>
    public static class LevelVariant
    {
        public static Level For(int cat, int lvl)
        {
            var baked = LevelDatabase.Get(cat, lvl);
            if (baked == null) return LevelGenerator.Generate(cat, lvl);
            try { return Personalize(baked) ?? baked; }
            catch (Exception e)
            {
                UnityEngine.Debug.LogWarning("[ZWord] Personal board failed, using the baked one: " + e.Message);
                return baked;
            }
        }

        static int Hash(string s)
        {
            unchecked
            {
                int h = (int)2166136261;
                foreach (char c in s ?? "") h = (h ^ c) * 16777619;
                return h & 0x7fffffff;
            }
        }

        static Level Personalize(Level baked)
        {
            int cat = baked.CategoryIndex, lvl = baked.LevelIndex;
            var rng = new Random(Hash(Save.Data.playerId + "|" + WordData.Categories[cat].Name + "|" + lvl));
            var lengths = baked.Words.Select(w => w.Word.Length).OrderByDescending(n => n).ToList();
            var pool = LevelDatabase.WordsIn(cat);
            // words of the previous level are avoided so neighbours don't repeat
            var avoid = new HashSet<string>(LevelDatabase.WordsOfLevel(cat, lvl - 1));

            for (int attempt = 0; attempt < 12; attempt++)
            {
                var words = Pick(pool, lengths, avoid, rng) ?? baked.Words.Select(w => w.Word).OrderByDescending(w => w.Length).ToList();
                var paths = LevelGenerator.Tile(baked.Cells, words.Select(w => w.Length).ToList(), rng);
                if (paths == null) continue;
                var level = new Level { CategoryIndex = cat, LevelIndex = lvl, Cells = new List<Hex>(baked.Cells), TimeLimit = baked.TimeLimit, RotStep = baked.RotStep };
                for (int i = 0; i < words.Count; i++)
                {
                    var pw = new PlacedWord { Word = words[i], Path = paths[i], Color = Palette.WordColors[i % Palette.WordColors.Length] };
                    for (int k = 0; k < pw.Path.Count; k++) level.Letters[pw.Path[k]] = pw.Word[k];
                    level.Words.Add(pw);
                }
                return level;
            }
            return null;
        }

        /// <summary>One word per requested length, no word inside another (CAR / CART), none from 'avoid'.</summary>
        static List<string> Pick(string[] pool, List<int> lengths, HashSet<string> avoid, Random rng)
        {
            var chosen = new List<string>();
            foreach (int len in lengths)
            {
                var cand = pool.Where(w => w.Length == len && !avoid.Contains(w) && !chosen.Any(x => x.Contains(w) || w.Contains(x)))
                               .OrderBy(_ => rng.Next()).FirstOrDefault();
                if (cand == null) return null;
                chosen.Add(cand);
            }
            return chosen;
        }
    }
}
