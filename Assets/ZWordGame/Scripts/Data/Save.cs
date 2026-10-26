using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace ZWord
{
    public enum Booster { Pause = 0, Letter = 1, Time = 2, Reveal = 3, Shuffle = 4, Starts = 5 }

    [Serializable]
    public class CategoryProgress
    {
        public string name;     // keyed by name so reordering categories never scrambles progress
        public int completed;
        public bool unlocked;
        public List<int> stars = new List<int>();
        public List<int> best = new List<int>();   // best score per level
        public int chests;                           // map chests opened (at 25 / 50 / 75 stars)
        public List<string> words = new List<string>();   // Word Book: answer words found in this category
        public bool bookClaimed;                     // Word Book page completed and its reward claimed
        public bool crown;                           // boss level (last board) beaten
    }

    /// <summary>Everything we persist. Bump <see cref="CurrentVersion"/> and extend Migrate() when adding fields.</summary>
    [Serializable]
    public class SaveData
    {
        public const int CurrentVersion = 2;

        public int version = CurrentVersion;
        public int stars;                 // score points; unlock categories
        public int coins = GameConfig.StartCoins;   // soft currency; buys hints
        public int gems = GameConfig.StartGems;     // premium currency
        public int[] boosters = { 0, 3, 3, 3, 2, 1 };
        public List<CategoryProgress> categories = new List<CategoryProgress>();
        public int bonusWords;   // lifetime bonus words found (feeds the bonus jar in M3)

        // settings
        public float musicVolume = 0.6f;
        public float sfxVolume = 1f;
        public bool haptics = true;
        public bool relaxMode;                      // no timer; stars come from hints used
        public bool musicOn = true;
        public bool sfxOn = true;

        // profile
        public string playerName = "Player";
        public string playerId = "";
        public int lastCategory;

        // lifetime counters (quests / challenges)
        public int levelsCompleted;
        public int wordsFound;
        public int threeStarWins;
        public int longWords;            // words of 6+ letters found
        public int combos;               // combo chains (word found within 6s of the previous)
        public int noHintWins;           // levels won without using a hint
        public int dailyPuzzlesSolved;
        public int dailyPuzzleBestStreak;
        public int dailyClaims;          // daily reward calendar claims
        public int challengesClaimed;    // daily challenges claimed

        // daily reward calendar
        public string dailyLastClaim = "";   // yyyy-MM-dd
        public int dailyDay;                 // 0..6, next day to claim
        public string dailyPuzzleDate = "";  // last day the Daily Puzzle was solved (yyyy-MM-dd)
        public int dailyPuzzleStreak;        // consecutive days solved
        public int dailyPuzzleBest;          // best Daily Puzzle score (any day)

        // daily challenges
        public string challengeDate = "";
        public int[] challengeIds = new int[0];
        public int[] challengeProgress = new int[0];
        public bool[] challengeClaimed = new bool[0];
        public bool challengeBonusClaimed;

        // quests (achievements): claimed tier per quest
        public int[] questTiers = new int[0];
        public bool bookSeeded;                     // Word Book filled in from levels finished before it existed
        public List<string> badges = new List<string>();   // event badges earned (e.g. "HALLOWEEN 2026")
        public int bossWins;                        // boss boards beaten (first time each)
        public string goldDate = "";                // golden hexes: day + how many paid out that day (max per day)
        public int goldCount;
        public int goldenHexes;                     // lifetime golden hexes found
        public bool remindersOn;                    // opt-in local notifications
        public bool remindersAsked;                 // the soft "want reminders?" popup was shown
        public bool supporter;                      // bought the one-time Supporter Pack
        public bool pro;                            // last known "wordz_pro" entitlement (RevenueCat is the source of truth)

        // meta / onboarding (used from M3 on)
        public bool tutorialDone;
        public bool ratePromptShown;                // "Rate Word Z" shown after the tutorial
        public bool rated;                          // tapped RATE NOW
        public string firstLaunchUtc;
        public int sessions;
    }

    /// <summary>
    /// Player progress stored as JSON in persistentDataPath (atomic write + backup).
    /// Existing PlayerPrefs progress from the prototype is migrated on first run.
    /// </summary>
    public static class Save
    {
        const string FileName = "zword_save.json";
        static SaveData data;

        static string PathMain => System.IO.Path.Combine(Application.persistentDataPath, FileName);
        static string PathTemp => PathMain + ".tmp";
        static string PathBackup => PathMain + ".bak";

        public static SaveData Data
        {
            get
            {
                if (data == null) Load();
                return data;
            }
        }

        // ---------------- load / write ----------------

        static void Load()
        {
            data = TryRead(PathMain) ?? TryRead(PathBackup);
            bool fresh = data == null;
            if (fresh)
            {
                data = new SaveData { firstLaunchUtc = DateTime.UtcNow.ToString("o") };
                MigrateFromPlayerPrefs(data);
            }
            Migrate(data);
            if (fresh) Write();
        }

        static SaveData TryRead(string path)
        {
            try
            {
                if (!File.Exists(path)) return null;
                var json = File.ReadAllText(path);
                return string.IsNullOrWhiteSpace(json) ? null : JsonUtility.FromJson<SaveData>(json);
            }
            catch (Exception e)
            {
                Debug.LogWarning($"[ZWord] Could not read save '{path}': {e.Message}");
                return null;
            }
        }

        /// <summary>Whole save as JSON (used by the smoke test to put the player's progress back afterwards).</summary>
        public static string Snapshot() => JsonUtility.ToJson(Data);

        public static void RestoreSnapshot(string json)
        {
            var d = JsonUtility.FromJson<SaveData>(json);
            if (d == null) return;
            data = d;
            Write();
            WalletChanged?.Invoke();
        }

        public static void Write()
        {
            if (data == null) return;
            try
            {
                File.WriteAllText(PathTemp, JsonUtility.ToJson(data, true));
                if (File.Exists(PathMain)) File.Copy(PathMain, PathBackup, true);
                if (File.Exists(PathMain)) File.Delete(PathMain);
                File.Move(PathTemp, PathMain);
            }
            catch (Exception e)
            {
                Debug.LogError($"[ZWord] Save failed: {e.Message}");
            }
        }

        static void Migrate(SaveData d)
        {
            if (d.boosters == null || d.boosters.Length < 6)
            {
                var b = new[] { 0, 3, 3, 3, 2, 1 };
                if (d.boosters != null) Array.Copy(d.boosters, b, Mathf.Min(d.boosters.Length, 6));
                d.boosters = b;
            }
            if (d.categories == null) d.categories = new List<CategoryProgress>();
            foreach (var c in d.categories)
            {
                if (c.stars == null) c.stars = new List<int>();
                if (c.best == null) c.best = new List<int>();
                if (c.words == null) c.words = new List<string>();
            }
            if (d.badges == null) d.badges = new List<string>();
            if (d.goldDate == null) d.goldDate = "";
            if (d.version < 2)
            {
                // v1 kept score points in "coins". They become Stars; coins and gems start fresh.
                d.stars = d.coins;
                d.coins = GameConfig.StartCoins;
                d.gems = GameConfig.StartGems;
                d.musicOn = d.musicVolume > 0.001f;
                d.sfxOn = d.sfxVolume > 0.001f;
                if (!d.musicOn) d.musicVolume = 0.6f;
                if (!d.sfxOn) d.sfxVolume = 1f;
                if (string.IsNullOrEmpty(d.playerName)) d.playerName = "Player";
                d.tutorialDone = true; // existing players skip onboarding
            }
            if (d.challengeIds == null) d.challengeIds = new int[0];
            if (d.challengeProgress == null) d.challengeProgress = new int[0];
            if (d.challengeClaimed == null) d.challengeClaimed = new bool[0];
            if (d.questTiers == null) d.questTiers = new int[0];
            if (string.IsNullOrEmpty(d.playerId))
            {
                const string chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
                var rng = new System.Random();
                var id = new char[8];
                for (int i = 0; i < id.Length; i++) id[i] = chars[rng.Next(chars.Length)];
                d.playerId = new string(id);
            }
            d.version = SaveData.CurrentVersion;
        }

        /// <summary>One-time import of the prototype's PlayerPrefs keys ("zword_*").</summary>
        static void MigrateFromPlayerPrefs(SaveData d)
        {
            const string P = "zword_";
            if (!PlayerPrefs.HasKey(P + "coins") && !PlayerPrefs.HasKey(P + "done_0") && !PlayerPrefs.HasKey(P + "sound"))
                return;

            d.stars = PlayerPrefs.GetInt(P + "coins", 0);
            d.tutorialDone = true;
            if (PlayerPrefs.GetInt(P + "sound", 1) == 0) d.sfxVolume = 0f;
            for (int b = 1; b < 4; b++) d.boosters[b] = PlayerPrefs.GetInt(P + "boost_" + b, 3);

            for (int c = 0; c < WordData.Categories.Length; c++)
            {
                var cp = Cat(d, c);
                cp.completed = PlayerPrefs.GetInt(P + "done_" + c, 0);
                cp.unlocked = PlayerPrefs.GetInt(P + "unlock_" + c, 0) == 1;
                for (int l = 0; l < WordData.LevelsPerCategory; l++)
                {
                    int s = PlayerPrefs.GetInt(P + "stars_" + c + "_" + l, 0);
                    if (s > 0) { EnsureStars(cp, l); cp.stars[l] = s; }
                }
            }
            Debug.Log("[ZWord] Migrated prototype progress from PlayerPrefs.");
        }

        static CategoryProgress Cat(SaveData d, int cat)
        {
            var name = WordData.Categories[cat].Name;
            var cp = d.categories.Find(x => x.name == name);
            if (cp == null)
            {
                cp = new CategoryProgress { name = name };
                d.categories.Add(cp);
            }
            return cp;
        }

        static CategoryProgress Cat(int cat) => Cat(Data, cat);

        static void EnsureStars(CategoryProgress cp, int lvl)
        {
            while (cp.stars.Count <= lvl) cp.stars.Add(0);
        }

        // ---------------- public API ----------------

        /// <summary>Raised whenever stars, coins or gems change (currency chips listen to this).</summary>
        public static event Action WalletChanged;

        /// <summary>Star points (score). Shown as the star counter; unlocks categories.</summary>
        public static int StarPoints
        {
            get => Data.stars;
            set { Data.stars = Mathf.Max(0, value); Write(); WalletChanged?.Invoke(); }
        }

        public static int Coins
        {
            get => Data.coins;
            set { Data.coins = Mathf.Max(0, value); Write(); WalletChanged?.Invoke(); }
        }

        public static int Gems
        {
            get => Data.gems;
            set { Data.gems = Mathf.Max(0, value); Write(); WalletChanged?.Invoke(); }
        }

        public static bool TrySpendCoins(int amount)
        {
            if (Data.coins < amount) return false;
            Coins = Data.coins - amount;
            return true;
        }

        public static bool TrySpendGems(int amount)
        {
            if (Data.gems < amount) return false;
            Gems = Data.gems - amount;
            return true;
        }

        /// <summary>Effective music volume (0 when music is switched off).</summary>
        public static float MusicVolume
        {
            get => Data.musicOn ? Data.musicVolume : 0f;
            set { Data.musicVolume = Mathf.Clamp01(value); Write(); }
        }

        /// <summary>Effective sound-effects volume (0 when sound is switched off).</summary>
        public static float SfxVolume
        {
            get => Data.sfxOn ? Data.sfxVolume : 0f;
            set { Data.sfxVolume = Mathf.Clamp01(value); Write(); }
        }

        public static int BestScore(int cat, int lvl)
        {
            var cp = Cat(cat);
            return lvl < cp.best.Count ? cp.best[lvl] : 0;
        }

        /// <summary>Stores the score if it beats the best; returns true for a new best.</summary>
        public static bool SubmitScore(int cat, int lvl, int score)
        {
            var cp = Cat(cat);
            while (cp.best.Count <= lvl) cp.best.Add(0);
            if (score <= cp.best[lvl]) return false;
            cp.best[lvl] = score;
            Write();
            return true;
        }

        // ---------------- Word Book / boss crowns / badges ----------------

        /// <summary>Adds a found answer word to the category's Word Book page. True if it is new.</summary>
        public static bool RecordWord(int cat, string word)
        {
            var cp = Cat(cat);
            if (cp.words.Contains(word)) return false;
            cp.words.Add(word);
            return true;
        }

        public static List<string> BookWords(int cat) => Cat(cat).words;
        public static bool BookClaimed(int cat) => Cat(cat).bookClaimed;
        public static void SetBookClaimed(int cat) { Cat(cat).bookClaimed = true; Write(); }

        public static bool HasCrown(int cat) => Cat(cat).crown;
        public static void SetCrown(int cat) { Cat(cat).crown = true; Write(); }

        public static bool HasBadge(string badge) => Data.badges.Contains(badge);

        public static int ChestsOpened(int cat) => Cat(cat).chests;

        public static void SetChestsOpened(int cat, int n)
        {
            Cat(cat).chests = n;
            Write();
        }

        public static bool Haptics
        {
            get => Data.haptics;
            set { Data.haptics = value; Write(); }
        }

        public static int Completed(int cat) => Cat(cat).completed;

        public static void SetCompleted(int cat, int count)
        {
            var cp = Cat(cat);
            if (count > cp.completed) { cp.completed = count; Write(); }
        }

        public static int Stars(int cat, int lvl)
        {
            var cp = Cat(cat);
            return lvl < cp.stars.Count ? cp.stars[lvl] : 0;
        }

        public static void SetStars(int cat, int lvl, int stars)
        {
            var cp = Cat(cat);
            EnsureStars(cp, lvl);
            if (stars > cp.stars[lvl]) { cp.stars[lvl] = stars; Write(); }
        }

        public static int TotalStars(int cat)
        {
            int s = 0;
            foreach (var v in Cat(cat).stars) s += v;
            return s;
        }

        public static bool Unlocked(int cat) => WordData.Categories[cat].UnlockCost <= 0 || Cat(cat).unlocked;

        /// <summary>Unlock with star points (they are spent).</summary>
        public static bool TryUnlock(int cat)
        {
            if (Unlocked(cat)) return true;
            int cost = WordData.Categories[cat].UnlockCost;
            if (Data.stars < cost) return false;
            Cat(cat).unlocked = true;
            StarPoints = Data.stars - cost;
            return true;
        }

        /// <summary>Instant unlock with gems.</summary>
        public static bool TryUnlockWithGems(int cat)
        {
            if (Unlocked(cat)) return true;
            if (!TrySpendGems(GameConfig.UnlockGems(WordData.Categories[cat].Group))) return false;
            Cat(cat).unlocked = true;
            Write();
            return true;
        }

        public static int GetBooster(Booster b) => Data.boosters[(int)b];

        public static void SetBooster(Booster b, int v)
        {
            Data.boosters[(int)b] = Mathf.Clamp(v, 0, 99);
            Write();
        }

        public static void ResetAll()
        {
            var keepMusic = Data.musicVolume;
            var keepSfx = Data.sfxVolume;
            var keepHaptics = Data.haptics;
            var keepName = Data.playerName;
            var keepReminders = Data.remindersOn;
            var keepAsked = Data.remindersAsked;
            data = new SaveData
            {
                firstLaunchUtc = DateTime.UtcNow.ToString("o"),
                musicVolume = keepMusic,
                sfxVolume = keepSfx,
                haptics = keepHaptics,
                playerName = keepName,
                remindersOn = keepReminders,
                remindersAsked = keepAsked
            };
            Write();
            WalletChanged?.Invoke();
        }
    }
}
